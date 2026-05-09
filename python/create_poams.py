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
Create Plan of Action and Milestones (POA&M) from Assessment Results.
This script generates OSCAL POA&Ms by:
1. Reading assessment results to identify findings and risks (Ubuntu and K8s)
2. Creating POA&M items for each identified risk or non-compliant control
3. Defining milestones, responsible parties, and remediation timelines

Works generically with all assessment results regardless of platform.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import uuid
from typing import Dict, List, Any
import traceback
sys.path.insert(0, str(Path(__file__).parent.parent))
from trestle_api import TrestleAPI
import trestle.oscal.poam as poam_module
import trestle.oscal.common as common

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))


def extract_findings_from_assessment_results(ar_name: str) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extract findings and risks from assessment results.
    
    Args:
        ar_name: Name of the assessment results
    
    Returns:
        Tuple of (findings_list, risks_list)
    """
    findings_data = []
    risks_data = []
    
    # Load assessment results
    ar_dict = trestle_api.load_assessment_results_dict(ar_name)
    if not ar_dict:
        print(f"Warning: Could not load assessment results {ar_name}")
        return findings_data, risks_data
    
    ar = ar_dict.get('assessment-results', {})
    
    # Extract findings from observations with failures
    for result in ar.get('results', []):
        for observation in result.get('observations', []):
            # Look for observations with status indicating issues
            props = observation.get('props', [])
            control_id = None
            status = None
            fail_count = 0
            
            for prop in props:
                if prop.get('name') == 'control-id':
                    control_id = prop.get('value')
                elif prop.get('name') == 'status':
                    status = prop.get('value')
                elif prop.get('name') == 'fail-count':
                    try:
                        fail_count = int(prop.get('value', 0))
                    except ValueError:
                        fail_count = 0
            
            # Only create findings for controls with failures
            if control_id and status == 'partially-satisfied' and fail_count > 0:
                findings_data.append({
                    'control_id': control_id,
                    'status': status,
                    'description': observation.get('description', ''),
                    'title': observation.get('title', f'Control {control_id} finding'),
                    'fail_count': fail_count,
                    'observation_uuid': observation.get('uuid')
                })
        
        # Extract explicit risks
        for risk in result.get('risks', []):
            risks_data.append({
                'uuid': risk.get('uuid'),
                'title': risk.get('title', 'Identified Risk'),
                'description': risk.get('description', ''),
                'statement': risk.get('statement', ''),
                'status': risk.get('status', 'open')
            })
    
    return findings_data, risks_data


def create_poam(ar_name: str) -> bool:
    """
    Create a POA&M for a given assessment results.
    
    Args:
        ar_name: Name of the assessment results (e.g., 'Ubuntu-System-ar-fedramp-low')
    
    Returns:
        True if successful
    """
    print(f"\nCreating POA&M for {ar_name}...")
    
    # Load the assessment results
    ar = trestle_api.load_assessment_results(ar_name)
    if not ar:
        print(f"Error: Could not load assessment results {ar_name}")
        return False
    
    # Extract regulation from AR metadata
    regulation = 'Unknown'
    for prop in ar.metadata.props or []:
        if prop.name == 'regulation':
            regulation = prop.value
            break
    
    print(f"  Regulation: {regulation}")
    
    # Extract findings and risks from assessment results
    findings_data, risks_data = extract_findings_from_assessment_results(ar_name)
    
    if not findings_data and not risks_data:
        print(f"  No findings or risks requiring remediation - POA&M not needed")
        return True
    
    print(f"  Findings: {len(findings_data)}, Risks: {len(risks_data)}")
    
    # Create POA&M name from AR name
    poam_name = ar_name.replace('-ar-', '-poam-')
    
    # Build POA&M structure
    now = datetime.now()
    
    # Create findings list
    findings = []
    finding_uuid_map = {}
    for finding_data in findings_data:
        finding_uuid = str(uuid.uuid4())
        finding_uuid_map[finding_data['control_id']] = finding_uuid
        
        # Create target for the finding
        target = common.FindingTarget(
            type='objective-id',
            target_id=finding_data['control_id'],
            title=f"Control {finding_data['control_id']}",
            description=f"Assessment finding for control {finding_data['control_id']}"
        )
        
        # Create related observations if available
        related_obs = []
        if finding_data.get('observation_uuid'):
            related_obs.append(common.RelatedObservation(
                observation_uuid=finding_data['observation_uuid']
            ))
        
        finding = common.Finding(
            uuid=finding_uuid,
            title=finding_data['title'],
            description=finding_data['description'],
            target=target,
            related_observations=related_obs if related_obs else None
        )
        findings.append(finding)
    
    # Create risks list
    risks = []
    risk_uuid_map = {}
    for risk_data in risks_data:
        risk_uuid = risk_data.get('uuid') or str(uuid.uuid4())
        risk_uuid_map[risk_data['title']] = risk_uuid
        
        risk = common.Risk(
            uuid=risk_uuid,
            title=risk_data['title'],
            description=risk_data['description'],
            statement=risk_data['statement'],
            status=risk_data['status']
        )
        risks.append(risk)
    
    # Create POA&M items
    poam_items = []
    
    # Create POA&M items for findings
    for finding_data in findings_data:
        control_id = finding_data['control_id']
        finding_uuid = finding_uuid_map[control_id]
        
        # Set priority based on severity
        if finding_data.get('fail_count', 0) > 5:
            priority = 'high'
        elif finding_data.get('fail_count', 0) > 2:
            priority = 'medium'
        else:
            priority = 'low'
        
        # Create related findings reference
        related_findings = [poam_module.RelatedFinding(
            finding_uuid=finding_uuid
        )]
        
        # Create related observations if available
        related_obs = []
        if finding_data.get('observation_uuid'):
            related_obs.append(common.RelatedObservation(
                observation_uuid=finding_data['observation_uuid']
            ))
        
        poam_item = poam_module.PoamItem(
            uuid=str(uuid.uuid4()),
            title=f"Remediate {control_id}",
            description=f"Address non-compliance for control {control_id} with {finding_data.get('fail_count', 0)} failing rule evaluations",
            props=[
                common.Property(name='control-id', value=control_id),
                common.Property(name='priority', value=priority),
                common.Property(name='fail-count', value=str(finding_data.get('fail_count', 0)))
            ],
            related_findings=related_findings,
            related_observations=related_obs if related_obs else None
        )
        poam_items.append(poam_item)
    
    # Create POA&M items for risks
    for risk_data in risks_data:
        risk_uuid = risk_uuid_map[risk_data['title']]
        
        # Create related risks reference
        related_risks = [common.AssociatedRisk(
            risk_uuid=risk_uuid
        )]
        
        poam_item = poam_module.PoamItem(
            uuid=str(uuid.uuid4()),
            title=f"Mitigate: {risk_data['title']}",
            description=risk_data['description'],
            props=[
                common.Property(name='priority', value='high'),
                common.Property(name='risk-status', value=risk_data['status'])
            ],
            related_risks=related_risks
        )
        poam_items.append(poam_item)
    
    # Build complete POA&M document
    poam = poam_module.PlanOfActionAndMilestones(
        uuid=str(uuid.uuid4()),
        metadata=common.Metadata(
            title=f"{ar.metadata.title.replace('Assessment Results', 'Plan of Action and Milestones')}",
            published=now,
            last_modified=now,
            version='1.0',
            oscal_version=poam_module.OSCAL_VERSION,
            props=[
                common.Property(name='regulation', value=regulation),
                common.Property(name='poam-item-count', value=str(len(poam_items))),
                common.Property(name='source-assessment', value=ar_name)
            ]
        ),
        import_ssp=common.ImportSsp(
            href=f"trestle://system-security-plans/{ar_name.replace('-ar-', '-ssp-')}/system-security-plan.json"
        ),
        system_id=common.SystemId(id='system-001'),
        local_definitions=poam_module.LocalDefinitions(
            components=[
                common.SystemComponent(
                    uuid=str(uuid.uuid4()),
                    type='software',
                    title='System Component',
                    description='System component requiring remediation',
                    status=common.Status(state='under-development')
                )
            ]
        ),
        findings=findings if findings else None,
        risks=risks if risks else None,
        poam_items=poam_items
    )
    
    # Save POA&M using trestle
    try:
        poam_dir = trestle_api.poams_dir / poam_name
        poam_dir.mkdir(parents=True, exist_ok=True)
        poam_file = poam_dir / 'plan-of-action-and-milestones.json'
        poam.oscal_write(poam_file)
        
        print(f"✓ Created: trestle-workspace/plan-of-action-and-milestones/{poam_name}/plan-of-action-and-milestones.json")
        print(f"  Findings: {len(findings)}")
        print(f"  Risks: {len(risks)}")
        print(f"  POA&M items: {len(poam_items)}")
        
        # Print summary by priority
        priority_counts = {'high': 0, 'medium': 0, 'low': 0}
        for item in poam_items:
            for prop in item.props or []:
                if prop.name == 'priority':
                    priority_counts[prop.value] = priority_counts.get(prop.value, 0) + 1
        
        print(f"  Priority breakdown: High={priority_counts['high']}, Medium={priority_counts['medium']}, Low={priority_counts['low']}")
        return True
    except Exception as e:
        print(f"✗ Error creating POA&M: {e}")
        traceback.print_exc()
        return False


def main():
    """Main execution function"""
    print("=" * 80)
    print("Plan of Action and Milestones (POA&M) Generator")
    print("=" * 80)
    
    # Get all assessment results
    assessment_results = trestle_api.list_assessment_results()
    if not assessment_results:
        print("Error: No assessment results found")
        return
    
    print(f"\nFound {len(assessment_results)} assessment results:")
    for ar in assessment_results:
        print(f"  - {ar['name']}: {ar['title']}")
    
    # Create POA&M for each assessment result
    success_count = 0
    for ar in assessment_results:
        if create_poam(ar['name']):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {success_count}/{len(assessment_results)} POA&Ms")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob