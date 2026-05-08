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
Create System Security Plans from Component Definitions and Inventory.
This script generates OSCAL SSPs by:
1. Reading component definitions (Ubuntu_Linux_24_04_LTS)
2. Extracting inventory from XCCDF scan result files
3. Generating complete SSPs with components AND inventory
4. One SSP per profile (fedramp-low, fedramp-moderate, fedramp-high, dora)
"""

from pathlib import Path
from datetime import datetime
import uuid
import xml.etree.ElementTree as ET
import json
from typing import Dict, List, Any
from trestle_api import TrestleAPI
import trestle.oscal.ssp as ssp_module

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))

# XCCDF results directory
XCCDF_DIR = Path('source-data/xccdf-results')

# Source component definition directory (has control-implementations)
SOURCE_COMP_DEF_DIR = Path('source-data/component-definitions')

# Profile/Catalog configurations
PROFILES = [
    {
        'name': 'fedramp-low',
        'title': 'FedRAMP Low',
        'ref_name': 'FedRAMP-Rev5-Low',
        'description': 'FedRAMP Rev 5 Low baseline',
        'ref_type': 'profile'
    },
    {
        'name': 'fedramp-moderate',
        'title': 'FedRAMP Moderate',
        'ref_name': 'FedRAMP-Rev5-Moderate',
        'description': 'FedRAMP Rev 5 Moderate baseline',
        'ref_type': 'profile'
    },
    {
        'name': 'fedramp-high',
        'title': 'FedRAMP High',
        'ref_name': 'FedRAMP-Rev5-High',
        'description': 'FedRAMP Rev 5 High baseline',
        'ref_type': 'profile'
    },
    {
        'name': 'dora',
        'title': 'DORA',
        'ref_name': 'EU-Dora',
        'description': 'EU Digital Operational Resilience Act',
        'ref_type': 'catalog'
    }
]


def extract_inventory_from_xccdf() -> List[Dict[str, str]]:
    """
    Extract inventory information from XCCDF scan result files.
    
    Returns:
        List of inventory item dictionaries
    """
    inventory = []
    
    if not XCCDF_DIR.exists():
        print(f"Warning: XCCDF directory not found: {XCCDF_DIR}")
        return inventory
    
    # Find all XCCDF result files
    xccdf_files = sorted(XCCDF_DIR.glob('*-xccdf-results.xml'))
    
    for xccdf_file in xccdf_files:
        try:
            # Parse XCCDF file
            tree = ET.parse(xccdf_file)
            root = tree.getroot()
            
            # Extract namespace
            ns = {'xccdf': 'http://checklists.nist.gov/xccdf/1.2'}
            
            # Get target information
            target_elem = root.find('.//xccdf:target', ns)
            target_facts = root.findall('.//xccdf:target-facts/xccdf:fact', ns)
            
            hostname = None
            ip_address = None
            
            # Extract hostname from target element or filename
            if target_elem is not None and target_elem.text:
                hostname = target_elem.text
            else:
                # Extract from filename: ubuntu-web-01-xccdf-results.xml -> ubuntu-web-01
                hostname = xccdf_file.stem.replace('-xccdf-results', '')
            
            # Extract IP address from target facts
            for fact in target_facts:
                fact_name = fact.get('name', '')
                if 'ip' in fact_name.lower() or 'address' in fact_name.lower():
                    ip_address = fact.text
                    break
            
            # Generate IP if not found (for demo purposes)
            if not ip_address:
                # Assign IPs based on hostname pattern
                if 'web-01' in hostname:
                    ip_address = '10.0.1.10'
                elif 'web-02' in hostname:
                    ip_address = '10.0.1.11'
                elif 'web-03' in hostname:
                    ip_address = '10.0.1.12'
                elif 'db' in hostname:
                    ip_address = '10.0.2.10'
                elif 'app' in hostname:
                    ip_address = '10.0.3.10'
                elif 'mgmt' in hostname:
                    ip_address = '10.0.4.10'
                else:
                    ip_address = '10.0.0.10'
            
            # Determine role and title from hostname
            if 'web' in hostname:
                role = 'web-server'
                title = f"Ubuntu Web Server {hostname.split('-')[-1].upper()}"
            elif 'db' in hostname:
                role = 'database-server'
                title = "Ubuntu Database Server"
            elif 'app' in hostname:
                role = 'application-server'
                title = "Ubuntu Application Server"
            elif 'mgmt' in hostname:
                role = 'management-server'
                title = "Ubuntu Management Server"
            else:
                role = 'server'
                title = f"Ubuntu Server {hostname}"
            
            inventory.append({
                'hostname': hostname,
                'title': title,
                'description': f'{title} running Ubuntu 24.04 LTS',
                'ip': ip_address,
                'role': role
            })
            
        except Exception as e:
            print(f"Warning: Could not parse {xccdf_file.name}: {e}")
            continue
    
    return inventory


def create_ssp(profile_config: Dict[str, str], inventory: List[Dict[str, str]]) -> bool:
    """
    Create an SSP for a given profile.
    
    Args:
        profile_config: Profile configuration dictionary
        inventory: List of inventory items
    
    Returns:
        True if successful
    """
    profile_name = profile_config['name']
    profile_title = profile_config['title']
    profile_ref = profile_config['ref_name']
    ref_type = profile_config['ref_type']
    
    print(f"\nCreating SSP for {profile_title}...")
    
    # Load component definition from source-data (has control-implementations)
    source_comp_file = SOURCE_COMP_DEF_DIR / 'Ubuntu_Linux_24_04_LTS' / 'component-definition.json'
    if not source_comp_file.exists():
        print(f"Error: Source component definition not found: {source_comp_file}")
        return False
    
    with open(source_comp_file) as f:
        source_comp_data = json.load(f)
    
    source_comp_def = source_comp_data.get('component-definition', {})
    source_components = source_comp_def.get('components', [])
    
    if not source_components:
        print(f"Error: No components found in source component definition")
        return False
    
    source_component_data = source_components[0]
    
    # Also load via trestle API for basic info
    comp_def = trestle_api.load_component('Ubuntu_Linux_24_04_LTS')
    if not comp_def:
        print(f"Error: Could not load component definition via trestle API")
        return False
    
    if not comp_def.components or len(comp_def.components) == 0:
        print(f"Error: No components found in component definition")
        return False
    
    source_component = comp_def.components[0]
    
    # Get control-implementations from source
    ctrl_impls = source_component_data.get('control-implementations', [])
    
    print(f"  Component: {source_component.title}")
    print(f"  Inventory items: {len(inventory)}")
    print(f"  Control implementations: {len(ctrl_impls)}")
    if ctrl_impls:
        impl_reqs = ctrl_impls[0].get('implemented-requirements', [])
        print(f"  Implemented requirements: {len(impl_reqs)}")
    
    # Create SSP name
    ssp_name = f'Ubuntu-System-ssp-{profile_name}'
    
    # Build SSP as dictionary
    now = datetime.now()
    
    # Create inventory items
    inventory_items = []
    for inv in inventory:
        inventory_items.append({
            'uuid': str(uuid.uuid4()),
            'description': inv['description'],
            'props': [
                {'name': 'asset-id', 'value': inv['hostname']},
                {'name': 'asset-type', 'value': 'server'},
                {'name': 'ipv4-address', 'value': inv['ip']},
                {'name': 'role', 'value': inv['role']},
                {'name': 'operating-system', 'value': 'Ubuntu 24.04 LTS'}
            ],
            'implemented-components': [
                {
                    'component-uuid': str(source_component.uuid)
                }
            ]
        })
    
    # Build component for SSP (different structure than component-definition)
    component_for_ssp = {
        'uuid': str(source_component.uuid),
        'type': source_component.type,
        'title': source_component.title,
        'description': source_component.description,
        'status': {
            'state': 'operational'
        }
    }
    
    # Copy props if they exist
    if hasattr(source_component, 'props') and source_component.props:
        component_for_ssp['props'] = [
            {
                'name': prop.name,
                'ns': prop.ns if hasattr(prop, 'ns') and prop.ns else None,
                'value': prop.value,
                'remarks': prop.remarks if hasattr(prop, 'remarks') and prop.remarks else None
            }
            for prop in source_component.props
        ]
        # Remove None values
        for prop in component_for_ssp['props']:
            prop_clean = {k: v for k, v in prop.items() if v is not None}
            prop.clear()
            prop.update(prop_clean)
    
    ssp_dict = {
        'system-security-plan': {
            'uuid': str(uuid.uuid4()),
            'metadata': {
                'title': f'Ubuntu System Security Plan - {profile_title}',
                'last-modified': now.isoformat(),
                'version': '1.0',
                'oscal-version': ssp_module.OSCAL_VERSION
            },
            'import-profile': {
                'href': f"trestle://{'profiles' if ref_type == 'profile' else 'catalogs'}/{profile_ref}/{'profile' if ref_type == 'profile' else 'catalog'}.json"
            },
            'system-characteristics': {
                'system-ids': [
                    {'id': 'ubuntu-system-001'}
                ],
                'system-name': 'Ubuntu 24.04 LTS Fleet',
                'description': f'System Security Plan for Ubuntu Linux 24.04 LTS {len(inventory)}-server fleet with OSCAP compliance validation - {profile_title} baseline',
                'system-information': {
                    'information-types': [
                        {
                            'title': 'System and Network Configuration',
                            'description': 'Information related to system configuration, security settings, compliance validation, and network infrastructure'
                        }
                    ]
                },
                'security-sensitivity-level': 'moderate',
                'status': {
                    'state': 'operational'
                },
                'authorization-boundary': {
                    'description': f'Ubuntu Linux 24.04 LTS {len(inventory)}-server fleet operating within a single authorization boundary, implementing {profile_title} security controls'
                }
            },
            'system-implementation': {
                'users': [
                    {
                        'uuid': str(uuid.uuid4()),
                        'title': 'System Administrator',
                        'role-ids': ['admin']
                    }
                ],
                'components': [component_for_ssp],
                'inventory-items': inventory_items
            },
            'control-implementation': {
                'description': f'Control implementation for {profile_title} baseline using Ubuntu Linux 24.04 LTS',
                'implemented-requirements': [
                    {
                        'uuid': str(uuid.uuid4()),
                        'control-id': req.get('control-id'),
                        'props': req.get('props', []) if req.get('props') else []
                    }
                    for req in ctrl_impls[0].get('implemented-requirements', [])
                ] if ctrl_impls else []
            }
        }
    }
    
    # Load as trestle object and save using API
    try:
        ssp = ssp_module.SystemSecurityPlan(**ssp_dict['system-security-plan'])
        if trestle_api.save_ssp(ssp, ssp_name):
            print(f"✓ Created: trestle-workspace/system-security-plans/{ssp_name}/system-security-plan.json")
            print(f"  Components: 1 (Ubuntu_Linux_24_04_LTS)")
            print(f"  Inventory items: {len(inventory_items)}")
            for inv in inventory:
                print(f"    - {inv['hostname']}: {inv['ip']}")
            return True
        else:
            print(f"✗ Failed to save SSP for {ssp_name}")
            return False
    except Exception as e:
        print(f"✗ Error creating SSP: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution function"""
    print("=" * 80)
    print("System Security Plans Generator")
    print("=" * 80)
    
    # Extract inventory from XCCDF files
    print(f"\nExtracting inventory from XCCDF scan results...")
    inventory = extract_inventory_from_xccdf()
    
    if not inventory:
        print("Error: No inventory items found in XCCDF files")
        return
    
    print(f"\nFound {len(inventory)} inventory items:")
    for inv in inventory:
        print(f"  - {inv['hostname']}: {inv['title']} ({inv['ip']})")
    
    print(f"\nComponent Definition: Ubuntu_Linux_24_04_LTS")
    print(f"\nProfiles: {len(PROFILES)}")
    for profile in PROFILES:
        print(f"  - {profile['name']}: {profile['title']}")
    
    # Create SSP for each profile
    success_count = 0
    for profile in PROFILES:
        if create_ssp(profile, inventory):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {success_count}/{len(PROFILES)} SSPs")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob