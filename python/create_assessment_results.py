#!/usr/bin/env python3
# Copyright (c) 2026 The OSCAL Compass Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Create Assessment Results from XCCDF scan results.
This script generates OSCAL assessment results for each assessment plan by:
1. Reading XCCDF result files for each Ubuntu server
2. Parsing rule-level pass/fail results
3. Mapping rules to controls using component definitions
4. Creating observations and findings for each control
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from collections import defaultdict
import uuid
from typing import Dict, List, Tuple, Set
sys.path.insert(0, str(Path(__file__).parent.parent))
from trestle_api import TrestleAPI
import trestle.oscal.assessment_results as ar_module
import trestle.oscal.common as common

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))

# XCCDF namespace
XCCDF_NS = {'xccdf': 'http://checklists.nist.gov/xccdf/1.2'}

def parse_xccdf_results(xccdf_file: Path) -> Tuple[Dict[str, str], Dict[str, any]]:
    """
    Parse XCCDF results file and extract rule results and metadata.
    
    Returns:
        Tuple of (rule_results dict, metadata dict)
        rule_results: {rule_id: 'pass'|'fail'}
        metadata: {hostname, ip, scan_start, scan_end, score}
    """
    tree = ET.parse(xccdf_file)
    root = tree.getroot()
    
    # Find TestResult element
    test_result = root.find('.//xccdf:TestResult', XCCDF_NS)
    if test_result is None:
        print(f"Warning: No TestResult found in {xccdf_file}")
        return {}, {}
    
    # Extract metadata
    metadata = {
        'hostname': test_result.find('xccdf:target', XCCDF_NS).text if test_result.find('xccdf:target', XCCDF_NS) is not None else 'unknown',
        'ip': test_result.find('xccdf:target-address', XCCDF_NS).text if test_result.find('xccdf:target-address', XCCDF_NS) is not None else 'unknown',
        'scan_start': test_result.get('start-time', ''),
        'scan_end': test_result.get('end-time', ''),
        'score': test_result.find('xccdf:score', XCCDF_NS).text if test_result.find('xccdf:score', XCCDF_NS) is not None else '0'
    }
    
    # Extract rule results
    rule_results = {}
    for rule_result in test_result.findall('xccdf:rule-result', XCCDF_NS):
        rule_id_ref = rule_result.get('idref', '')
        # Extract the actual rule ID from the full reference
        # Format: xccdf_org.ssgproject.content_rule_<rule_id>
        if 'rule_' in rule_id_ref:
            rule_id = rule_id_ref.split('rule_')[-1]
        else:
            rule_id = rule_id_ref
        
        result_elem = rule_result.find('xccdf:result', XCCDF_NS)
        if result_elem is not None:
            result = result_elem.text
            rule_results[rule_id] = result
    
    return rule_results, metadata


def load_rule_to_control_mapping(ssp_name: str) -> Dict[str, Set[str]]:
    """
    Load rule-to-control mapping from SSP's control-implementations.
    
    Args:
        ssp_name: Name of the SSP to load mapping from
    
    Returns:
        Dict mapping rule_id to set of control_ids
    """
    # Load the SSP
    ssp = trestle_api.load_ssp_dict(ssp_name)
    if not ssp:
        print(f"Warning: Could not load SSP {ssp_name}")
        return {}
    
    # Extract rule-to-control mapping from control-implementations
    rule_to_controls = defaultdict(set)
    
    ssp_data = ssp.get('system-security-plan', {})
    control_impl = ssp_data.get('control-implementation', {})
    implemented_reqs = control_impl.get('implemented-requirements', [])
    
    for req in implemented_reqs:
        control_id = req.get('control-id')
        if not control_id:
            continue
        
        # Get rules directly from props on implemented-requirements
        props = req.get('props', [])
        for prop in props:
            if prop.get('name') == 'Rule_Id':
                rule_id = prop.get('value')
                if rule_id:
                    rule_to_controls[rule_id].add(control_id)
        
        # Also check by-components for backwards compatibility
        by_components = req.get('by-components', [])
        for comp in by_components:
            comp_props = comp.get('props', [])
            for prop in comp_props:
                if prop.get('name') == 'Rule_Id':
                    rule_id = prop.get('value')
                    if rule_id:
                        rule_to_controls[rule_id].add(control_id)
    
    return dict(rule_to_controls)


def load_mapping_coverage(regulation: str) -> Dict[str, float]:
    """
    Load mapping coverage percentages for regulations that use mapping-collections.
    
    Args:
        regulation: Regulation name (e.g., 'EU DORA')
    
    Returns:
        Dict mapping control_id to coverage percentage (0.0-1.0)
    """
    coverage_map = {}
    
    # Check if this is a mapping-based regulation
    if 'DORA' not in regulation:
        return coverage_map
    
    # Load the NIST to DORA mapping collection using trestle_api
    mapping_data = trestle_api.load_mapping_dict('nist-800-53-rev5-to-EU-Dora')
    if not mapping_data:
        print(f"  Warning: Mapping collection 'nist-800-53-rev5-to-EU-Dora' not found")
        return coverage_map
    
    try:
        # Extract coverage from mappings
        mappings = mapping_data.get('mapping-collection', {}).get('mappings', [])
        for mapping in mappings:
            for map_entry in mapping.get('maps', []):
                # Get source control ID (NIST)
                sources = map_entry.get('sources', [])
                if sources and sources[0].get('type') == 'control':
                    source_id = sources[0].get('id-ref', '')
                    
                    # Get target coverage
                    coverage_info = map_entry.get('coverage', {})
                    target_coverage = coverage_info.get('target-coverage', 1.0)
                    
                    # Store the coverage (use minimum if multiple mappings exist)
                    if source_id:
                        if source_id in coverage_map:
                            coverage_map[source_id] = min(coverage_map[source_id], target_coverage)
                        else:
                            coverage_map[source_id] = target_coverage
        
        print(f"  Loaded mapping coverage for {len(coverage_map)} controls")
        
    except Exception as e:
        print(f"  Warning: Could not load mapping coverage: {e}")
    
    return coverage_map


def aggregate_results_by_control(xccdf_results: Dict[str, Tuple[Dict, Dict]],
                                  rule_to_controls: Dict[str, Set[str]],
                                  subject_uuids: List[str],
                                  coverage_map: Dict[str, float] = None) -> Dict[str, Dict]:
    """
    Aggregate XCCDF results by control across all subjects.
    
    Args:
        xccdf_results: XCCDF scan results
        rule_to_controls: Mapping of rules to controls
        subject_uuids: List of subject UUIDs
        coverage_map: Optional mapping coverage percentages for controls
    
    Returns:
        Dict mapping control_id to aggregated results
    """
    control_results = defaultdict(lambda: {
        'pass_count': 0,
        'fail_count': 0,
        'rules': set(),
        'subjects': set(),
        'coverage': 1.0
    })
    
    # Process each server's results
    for server_name, (rule_results, metadata) in xccdf_results.items():
        subject_idx = list(xccdf_results.keys()).index(server_name)
        if subject_idx < len(subject_uuids):
            subject_uuid = subject_uuids[subject_idx]
        else:
            subject_uuid = str(uuid.uuid4())
        
        # Map each rule result to its controls
        for rule_id, result in rule_results.items():
            if rule_id in rule_to_controls:
                for control_id in rule_to_controls[rule_id]:
                    control_results[control_id]['rules'].add(rule_id)
                    control_results[control_id]['subjects'].add(subject_uuid)
                    
                    # Apply coverage percentage if available
                    if coverage_map and control_id in coverage_map:
                        control_results[control_id]['coverage'] = coverage_map[control_id]
                    
                    if result == 'pass':
                        control_results[control_id]['pass_count'] += 1
                    elif result == 'fail':
                        control_results[control_id]['fail_count'] += 1
    
    return dict(control_results)


def create_assessment_results(plan_name: str, xccdf_dir: Path) -> bool:
    """
    Create assessment results for a given assessment plan.
    
    Args:
        plan_name: Name of the assessment plan (e.g., 'Ubuntu-System-ap-fedramp-low')
        xccdf_dir: Directory containing XCCDF result files
    
    Returns:
        True if successful
    """
    print(f"\nCreating assessment results for {plan_name}...")
    
    # Load the assessment plan
    plan = trestle_api.load_assessment_plan(plan_name)
    if not plan:
        print(f"Error: Could not load assessment plan {plan_name}")
        return False
    
    # Extract regulation/profile from plan metadata
    regulation = 'Unknown'
    for prop in plan.metadata.props or []:
        if prop.name == 'regulation':
            regulation = prop.value
            break
    
    # Get subject UUIDs from the plan
    subject_uuids = []
    if plan.assessment_subjects:
        for subj_group in plan.assessment_subjects:
            if subj_group.include_subjects:
                for subj in subj_group.include_subjects:
                    subject_uuids.append(str(subj.subject_uuid))
    
    print(f"  Regulation: {regulation}")
    print(f"  Subjects: {len(subject_uuids)}")
    
    # Parse all XCCDF result files
    xccdf_results = {}
    for xccdf_file in xccdf_dir.glob('*.xml'):
        server_name = xccdf_file.stem.replace('-xccdf-results', '')
        rule_results, metadata = parse_xccdf_results(xccdf_file)
        if rule_results:
            xccdf_results[server_name] = (rule_results, metadata)
            print(f"  Parsed {xccdf_file.name}: {len(rule_results)} rules")
    
    if not xccdf_results:
        print("Error: No XCCDF results found")
        return False
    
    # Determine SSP name from plan name
    ssp_name = plan_name.replace('-ap-', '-ssp-')
    
    # Load rule-to-control mapping from SSP
    print(f"  Loading rule-to-control mapping from {ssp_name}...")
    rule_to_controls = load_rule_to_control_mapping(ssp_name)
    print(f"  Mapped {len(rule_to_controls)} rules to controls")
    
    # Load mapping coverage if this is a mapping-based regulation
    coverage_map = load_mapping_coverage(regulation)
    
    # Aggregate results by control
    print("  Aggregating results by control...")
    control_results = aggregate_results_by_control(xccdf_results, rule_to_controls, subject_uuids, coverage_map)
    print(f"  Generated results for {len(control_results)} controls")
    
    # Create assessment results structure
    now = datetime.now()
    assessment_start = now - timedelta(days=30)
    assessment_end = now
    
    ar_name = plan_name.replace('-ap-', '-ar-')
    
    # Build assessment results as dictionary (simpler than using trestle objects)
    # Then load and save with trestle API for validation
    
    # Build reviewed-controls
    reviewed_controls_list = []
    for control_id in sorted(control_results.keys()):
        cr = control_results[control_id]
        coverage = cr.get('coverage', 1.0)
        
        # Calculate status considering coverage
        # If coverage < 1.0, the control can only be partially-satisfied at best
        # because the mapping doesn't fully cover the control requirements
        if coverage < 1.0:
            adjusted_pass = int(cr['pass_count'] * coverage)
            adjusted_fail = int(cr['fail_count'] * coverage)
            # Partial coverage means control is automatically partially-satisfied
            status = 'partially-satisfied'
            coverage_note = f", {int(coverage*100)}% coverage"
        else:
            adjusted_pass = cr['pass_count']
            adjusted_fail = cr['fail_count']
            
            # Determine status: not-satisfied if ALL failures (no passes)
            if adjusted_pass == 0 and adjusted_fail > 0:
                status = 'not-satisfied'
            elif adjusted_fail == 0:
                status = 'satisfied'
            else:
                status = 'partially-satisfied'
            coverage_note = ""
        
        reviewed_controls_list.append({
            'description': f"{control_id}: {status} ({adjusted_pass} pass / {adjusted_fail} fail rule evaluations{coverage_note})",
            'include-controls': [{'control-id': control_id}]
        })
    
    # Build observations
    observations_list = []
    for control_id in sorted(control_results.keys()):
        cr = control_results[control_id]
        coverage = cr.get('coverage', 1.0)
        
        # Calculate status considering coverage
        # Partial coverage means control is automatically partially-satisfied
        if coverage < 1.0:
            adjusted_pass = int(cr['pass_count'] * coverage)
            adjusted_fail = int(cr['fail_count'] * coverage)
            status = 'partially-satisfied'
            coverage_desc = f" with {int(coverage*100)}% mapping coverage (partial coverage = partially-satisfied)"
        else:
            adjusted_pass = cr['pass_count']
            adjusted_fail = cr['fail_count']
            
            # Determine status: not-satisfied if ALL failures (no passes)
            if adjusted_pass == 0 and adjusted_fail > 0:
                status = 'not-satisfied'
                coverage_desc = " (all rule evaluations failed)"
            elif adjusted_fail == 0:
                status = 'satisfied'
                coverage_desc = ""
            else:
                status = 'partially-satisfied'
                coverage_desc = ""
        
        rules_list = ', '.join(sorted(cr['rules']))
        
        observations_list.append({
            'uuid': str(uuid.uuid4()),
            'title': f"Control {control_id} assessment outcome",
            'description': f"Control {control_id} is {status} based on {adjusted_pass} passing and {adjusted_fail} failing mapped XCCDF rule evaluations across {len(cr['subjects'])} assessed subjects{coverage_desc}.",
            'methods': ['TEST'],
            'types': ['finding'],
            'collected': assessment_end.isoformat() + 'Z',
            'relevant-evidence': [{'description': f"Mapped rules: {rules_list}"}],
            'subjects': [{'subject-uuid': subj_uuid, 'type': 'component'} for subj_uuid in sorted(cr['subjects'])],
            'props': [
                {'name': 'control-id', 'value': control_id},
                {'name': 'status', 'value': status},
                {'name': 'pass-count', 'value': str(adjusted_pass)},
                {'name': 'fail-count', 'value': str(adjusted_fail)},
                {'name': 'rule-count', 'value': str(len(cr['rules']))},
                {'name': 'coverage', 'value': str(coverage)}
            ]
        })
    
    # Build assessment results dictionary
    ar_dict = {
        'assessment-results': {
            'uuid': str(uuid.uuid4()),
            'metadata': {
                'title': f"{plan.metadata.title.replace('Assessment Plan', 'Assessment Results')}",
                'published': now.isoformat() + 'Z',
                'last-modified': now.isoformat() + 'Z',
                'version': '1.0',
                'oscal-version': ar_module.OSCAL_VERSION,
                'props': [
                    {'name': 'regulation', 'value': regulation},
                    {'name': 'assessment-scope', 'value': 'host-assessment'},
                    {'name': 'assessment-subject-count', 'value': str(len(subject_uuids))},
                    {'name': 'result-summary', 'value': 'partial-pass-with-findings'},
                    {'name': 'mapped-control-count', 'value': str(len(control_results))}
                ]
            },
            'import-ap': {'href': f"../assessment-plans/{plan_name}/assessment-plan.json"},
            'local-definitions': {
                'activities': [{
                    'uuid': str(uuid.uuid4()),
                    'title': 'Mapped XCCDF evidence analysis',
                    'description': f'XCCDF rule results were normalized and mapped to {regulation} control identifiers.',
                    'steps': [
                        {
                            'uuid': str(uuid.uuid4()),
                            'title': 'Parse XCCDF rule results',
                            'description': f'Collected rule pass/fail results for all {len(xccdf_results)} Ubuntu servers.'
                        },
                        {
                            'uuid': str(uuid.uuid4()),
                            'title': 'Map rules to controls',
                            'description': 'Used component definition implemented-requirement Rule_Id properties to associate evidence with controls.'
                        }
                    ]
                }]
            },
            'results': [{
                'uuid': str(uuid.uuid4()),
                'title': f'{regulation} assessment execution results',
                'description': f'Assessment results for the Ubuntu 24.04 LTS {len(xccdf_results)}-server fleet evaluated against {regulation} using mapped XCCDF evidence.',
                'start': assessment_start.isoformat() + 'Z',
                'end': assessment_end.isoformat() + 'Z',
                'reviewed-controls': {'control-selections': reviewed_controls_list},
                'assessment-log': {
                    'entries': [
                        {
                            'uuid': str(uuid.uuid4()),
                            'title': 'XCCDF scans executed',
                            'description': f'Executed OpenSCAP security compliance scans on {len(xccdf_results)} Ubuntu 24.04 LTS servers.',
                            'start': assessment_start.isoformat() + 'Z',
                            'end': (assessment_start + timedelta(days=1)).isoformat() + 'Z'
                        },
                        {
                            'uuid': str(uuid.uuid4()),
                            'title': 'Control mapping analysis completed',
                            'description': 'Mapped rule-level evidence to control identifiers using component definitions and regulatory mappings.',
                            'start': (assessment_end - timedelta(days=1)).isoformat() + 'Z',
                            'end': assessment_end.isoformat() + 'Z'
                        }
                    ]
                },
                'observations': observations_list,
                'risks': [],
                'remarks': f'Assessment results generated from XCCDF scan data for {len(xccdf_results)} servers with {len(control_results)} controls evaluated.'
            }]
        }
    }
    
    # Load as trestle object and save using API
    try:
        assessment_results = ar_module.AssessmentResults(**ar_dict['assessment-results'])
        if trestle_api.save_assessment_results(assessment_results, ar_name):
            print(f"✓ Created: trestle-workspace/assessment-results/{ar_name}/assessment-results.json")
            print(f"  Controls: {len(control_results)}")
            print(f"  Observations: {len(observations_list)}")
            return True
        else:
            print(f"✗ Failed to save assessment results for {ar_name}")
            return False
    except Exception as e:
        print(f"✗ Error creating assessment results: {e}")
        return False


def main():
    """Main execution function"""
    print("=" * 80)
    print("Assessment Results Generator")
    print("=" * 80)
    
    # XCCDF results directory
    xccdf_dir = Path('source-data/xccdf-results')
    if not xccdf_dir.exists():
        print(f"Error: XCCDF results directory not found: {xccdf_dir}")
        return
    
    # Get all assessment plans
    plans = trestle_api.list_assessment_plans()
    if not plans:
        print("Error: No assessment plans found")
        return
    
    print(f"\nFound {len(plans)} assessment plans:")
    for plan in plans:
        print(f"  - {plan['name']}: {plan['title']}")
    
    # Create assessment results for each plan
    success_count = 0
    for plan in plans:
        if create_assessment_results(plan['name'], xccdf_dir):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {success_count}/{len(plans)} assessment results")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob