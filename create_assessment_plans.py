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
Create Assessment Plans from System Security Plans.
This script generates OSCAL assessment plans for each SSP by:
1. Reading existing SSPs
2. Extracting inventory items (servers) from the SSP
3. Creating assessment plans that reference the SSPs and their inventory
4. Defining assessment activities, subjects, and tasks
"""

from pathlib import Path
from datetime import datetime, timedelta
import uuid
from typing import Dict, List
from trestle_api import TrestleAPI
import trestle.oscal.assessment_plan as ap_module

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))


def get_inventory_uuids(ssp) -> List[str]:
    """
    Extract inventory item UUIDs from an SSP.
    
    Args:
        ssp: The SSP object
    
    Returns:
        List of inventory item UUIDs
    """
    inventory_uuids = []
    
    if hasattr(ssp, 'system_implementation') and ssp.system_implementation:
        if hasattr(ssp.system_implementation, 'inventory_items') and ssp.system_implementation.inventory_items:
            for item in ssp.system_implementation.inventory_items:
                if hasattr(item, 'uuid'):
                    inventory_uuids.append(str(item.uuid))
    
    return inventory_uuids


def create_assessment_plan(ssp_name: str) -> bool:
    """
    Create an assessment plan for a given SSP.
    
    Args:
        ssp_name: Name of the SSP (e.g., 'Ubuntu-System-ssp-fedramp-low')
    
    Returns:
        True if successful
    """
    print(f"\nCreating assessment plan for {ssp_name}...")
    
    # Load the SSP to get metadata and inventory
    ssp = trestle_api.load_ssp(ssp_name)
    if not ssp:
        print(f"Error: Could not load SSP {ssp_name}")
        return False
    
    # Extract inventory item UUIDs
    inventory_uuids = get_inventory_uuids(ssp)
    if not inventory_uuids:
        print(f"Warning: No inventory items found in SSP {ssp_name}")
        print(f"  SSPs should be created with inventory-items using create_ssps.py")
        # Continue anyway - assessment plan can exist without specific subjects
    
    # Extract regulation from SSP title
    ssp_title = ssp.metadata.title
    if "FedRAMP" in ssp_title and "Low" in ssp_title:
        regulation = "FedRAMP Rev 5 Low"
    elif "FedRAMP" in ssp_title and "Moderate" in ssp_title:
        regulation = "FedRAMP Rev 5 Moderate"
    elif "FedRAMP" in ssp_title and "High" in ssp_title:
        regulation = "FedRAMP Rev 5 High"
    elif "DORA" in ssp_title:
        regulation = "EU DORA"
    else:
        regulation = "Security Assessment"
    
    print(f"  Regulation: {regulation}")
    print(f"  Inventory items: {len(inventory_uuids)}")
    
    # Create AP name from SSP name
    ap_name = ssp_name.replace('-ssp-', '-ap-')
    
    # Build assessment plan as dictionary
    now = datetime.now()
    kickoff_date = now + timedelta(days=7)
    assessment_start = now + timedelta(days=14)
    assessment_end = now + timedelta(days=35)
    results_date = now + timedelta(days=45)
    
    ap_dict = {
        'assessment-plan': {
            'uuid': str(uuid.uuid4()),
            'metadata': {
                'title': f"{ssp_title.replace('Security Plan', 'Assessment Plan')}",
                'published': now.isoformat(),
                'last-modified': now.isoformat(),
                'version': '1.0',
                'oscal-version': ap_module.OSCAL_VERSION,
                'props': [
                    {'name': 'assessment-type', 'value': 'security-assessment'},
                    {'name': 'assessment-scope', 'value': 'host-assessment'},
                    {'name': 'assessment-frequency', 'value': 'annual'},
                    {'name': 'regulation', 'value': regulation},
                    {'name': 'subject-count', 'value': str(len(inventory_uuids))}
                ]
            },
            'import-ssp': {
                'href': f"../system-security-plans/{ssp_name}/system-security-plan.json"
            },
            'local-definitions': {
                'activities': [
                    {
                        'uuid': str(uuid.uuid4()),
                        'title': 'Automated Security Scanning',
                        'description': 'Automated vulnerability scanning and configuration compliance checks using OSCAP',
                        'props': [
                            {'name': 'method', 'value': 'TEST'},
                            {'name': 'assessment-type', 'value': 'automated'}
                        ],
                        'steps': [
                            {
                                'uuid': str(uuid.uuid4()),
                                'title': 'Run OSCAP Scan',
                                'description': 'Execute OpenSCAP security compliance scan against the Ubuntu 24.04 LTS fleet'
                            },
                            {
                                'uuid': str(uuid.uuid4()),
                                'title': 'Analyze Results',
                                'description': 'Review scan results and identify non-compliant controls'
                            }
                        ]
                    },
                    {
                        'uuid': str(uuid.uuid4()),
                        'title': 'Manual Control Testing',
                        'description': 'Manual review and testing of security controls that cannot be automated',
                        'props': [
                            {'name': 'method', 'value': 'EXAMINE'},
                            {'name': 'assessment-type', 'value': 'manual'}
                        ],
                        'steps': [
                            {
                                'uuid': str(uuid.uuid4()),
                                'title': 'Document Review',
                                'description': 'Review security policies, procedures, configurations, and evidence artifacts'
                            },
                            {
                                'uuid': str(uuid.uuid4()),
                                'title': 'Interview Personnel',
                                'description': 'Interview system administrators and security personnel'
                            }
                        ]
                    },
                    {
                        'uuid': str(uuid.uuid4()),
                        'title': 'Resilience and Response Validation',
                        'description': 'Validate operational resilience, response, and recovery capabilities across the Ubuntu fleet',
                        'props': [
                            {'name': 'method', 'value': 'TEST'},
                            {'name': 'assessment-type', 'value': 'scenario-based'}
                        ],
                        'steps': [
                            {
                                'uuid': str(uuid.uuid4()),
                                'title': 'Scenario Walkthrough',
                                'description': 'Review incident, disruption, and recovery scenarios applicable to the system'
                            },
                            {
                                'uuid': str(uuid.uuid4()),
                                'title': 'Evidence Correlation',
                                'description': 'Correlate technical evidence with implemented controls and procedures'
                            }
                        ]
                    }
                ]
            },
            'reviewed-controls': {
                'description': f'Assessment of controls for the {regulation} baseline',
                'props': [
                    {'name': 'assessment-baseline', 'value': regulation},
                    {'name': 'control-selection', 'value': 'all-imported-controls'}
                ],
                'control-selections': [
                    {
                        'description': 'All controls imported by the referenced SSP will be assessed',
                        'include-all': {}
                    }
                ]
            },
            'assessment-assets': {
                'assessment-platforms': [
                    {
                        'uuid': str(uuid.uuid4()),
                        'title': 'OpenSCAP Scanner',
                        'props': [
                            {'name': 'tool-type', 'value': 'scanner'},
                            {'name': 'tool-version', 'value': '1.3.x'}
                        ]
                    },
                    {
                        'uuid': str(uuid.uuid4()),
                        'title': 'Evidence Review Toolkit',
                        'props': [
                            {'name': 'tool-type', 'value': 'analysis'},
                            {'name': 'tool-version', 'value': '1.0'}
                        ]
                    }
                ]
            },
            'tasks': [
                {
                    'uuid': str(uuid.uuid4()),
                    'type': 'action',
                    'title': 'Assessment Kickoff',
                    'description': 'Schedule and conduct the assessment kickoff meeting',
                    'timing': {
                        'on-date': {
                            'date': kickoff_date.isoformat()
                        }
                    }
                },
                {
                    'uuid': str(uuid.uuid4()),
                    'type': 'action',
                    'title': 'Execute Automated and Manual Assessment Activities',
                    'description': 'Perform automated scans, document review, interviews, and validation activities',
                    'timing': {
                        'within-date-range': {
                            'start': assessment_start.isoformat(),
                            'end': assessment_end.isoformat()
                        }
                    }
                },
                {
                    'uuid': str(uuid.uuid4()),
                    'type': 'milestone',
                    'title': 'Assessment Results Ready',
                    'description': 'Complete evidence review and prepare assessment results',
                    'timing': {
                        'on-date': {
                            'date': results_date.isoformat()
                        }
                    }
                }
            ]
        }
    }
    
    # Add assessment subjects if inventory items exist
    if inventory_uuids:
        ap_dict['assessment-plan']['assessment-subjects'] = [
            {
                'type': 'inventory-item',
                'description': 'Ubuntu Linux 24.04 LTS server fleet',
                'include-subjects': [
                    {'subject-uuid': subj_uuid, 'type': 'inventory-item'}
                    for subj_uuid in inventory_uuids
                ]
            }
        ]
    
    # Load as trestle object and save using API
    try:
        assessment_plan = ap_module.AssessmentPlan(**ap_dict['assessment-plan'])
        if trestle_api.save_assessment_plan(assessment_plan, ap_name):
            print(f"✓ Created: trestle-workspace/assessment-plans/{ap_name}/assessment-plan.json")
            print(f"  Activities: {len(ap_dict['assessment-plan']['local-definitions']['activities'])}")
            print(f"  Tasks: {len(ap_dict['assessment-plan']['tasks'])}")
            return True
        else:
            print(f"✗ Failed to save assessment plan for {ap_name}")
            return False
    except Exception as e:
        print(f"✗ Error creating assessment plan: {e}")
        return False


def main():
    """Main execution function"""
    print("=" * 80)
    print("Assessment Plans Generator")
    print("=" * 80)
    
    # Get all SSPs
    ssps = trestle_api.list_ssps()
    if not ssps:
        print("Error: No SSPs found")
        return
    
    print(f"\nFound {len(ssps)} SSPs:")
    for ssp in ssps:
        print(f"  - {ssp['name']}: {ssp['title']}")
    
    # Create assessment plan for each SSP
    success_count = 0
    for ssp in ssps:
        if create_assessment_plan(ssp['name']):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {success_count}/{len(ssps)} assessment plans")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob