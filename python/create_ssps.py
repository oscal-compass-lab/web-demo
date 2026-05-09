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
1. Reading component definitions (Ubuntu_Linux_24_04_LTS and Kubernetes_1_28)
2. Extracting inventory from XCCDF scan result files (Ubuntu servers and K8s nodes)
3. Generating complete SSPs with components AND inventory
4. Two SSPs per profile (one for Ubuntu fleet, one for K8s cluster)
5. Profiles: fedramp-low, fedramp-moderate, fedramp-high, dora

Total output: 8 SSPs (4 profiles × 2 platforms)
"""

import sys
from pathlib import Path
from datetime import datetime
import uuid
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
import traceback
sys.path.insert(0, str(Path(__file__).parent.parent))
from trestle_api import TrestleAPI
import trestle.oscal.ssp as ssp_module
from trestle.oscal import OSCAL_VERSION
from server_config import get_all_servers, get_server_by_name, get_all_k8s_nodes, get_k8s_node_by_name

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))

# XCCDF results directory
XCCDF_DIR = Path('source-data/xccdf-results')

# Component definition directory (has control-implementations)
# Use trestle workspace which has enhanced component definitions
SOURCE_COMP_DEF_DIR = Path('trestle-workspace/component-definitions')

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


def extract_inventory_from_xccdf() -> tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    Extract inventory information from XCCDF scan result files.
    Uses common server configuration for consistent data.
    
    Returns:
        Tuple of (ubuntu_inventory, k8s_inventory) lists
    """
    ubuntu_inventory = []
    k8s_inventory = []
    
    if not XCCDF_DIR.exists():
        print(f"Warning: XCCDF directory not found: {XCCDF_DIR}")
        return ubuntu_inventory, k8s_inventory
    
    # Get all server and node configurations
    all_servers = get_all_servers()
    all_k8s_nodes = get_all_k8s_nodes()
    
    # Find all XCCDF result files
    xccdf_files = sorted(XCCDF_DIR.glob('*-xccdf-results.xml'))
    
    for xccdf_file in xccdf_files:
        try:
            # Extract name from filename: ubuntu-web-01-xccdf-results.xml -> ubuntu-web-01
            item_name = xccdf_file.stem.replace('-xccdf-results', '')
            
            # Check if it's a Kubernetes node
            if item_name.startswith('k8s-'):
                node_config = get_k8s_node_by_name(item_name)
                
                if not node_config:
                    print(f"Warning: No configuration found for {item_name}, skipping")
                    continue
                
                # Use data from common configuration
                hostname = node_config['hostname']
                ip_address = node_config['ip']
                role = node_config['role']
                description = node_config['description']
                node_type = node_config['node_type']
                k8s_version = node_config['k8s_version']
                
                # Determine title from role
                if node_type == 'master':
                    title = f"Kubernetes Control Plane Node {item_name.split('-')[-1].upper()}"
                else:
                    title = f"Kubernetes Worker Node {item_name.split('-')[-1].upper()}"
                
                k8s_inventory.append({
                    'hostname': hostname,
                    'title': title,
                    'description': description,
                    'ip': ip_address,
                    'role': f"k8s-{role}",
                    'node_type': node_type,
                    'k8s_version': k8s_version
                })
            else:
                # It's an Ubuntu server
                server_config = get_server_by_name(item_name)
                
                if not server_config:
                    print(f"Warning: No configuration found for {item_name}, skipping")
                    continue
                
                # Use data from common configuration
                hostname = server_config['hostname']
                ip_address = server_config['ip']
                role = server_config['role']
                description = server_config['description']
                
                # Determine title from role
                if role == 'web':
                    title = f"Ubuntu Web Server {item_name.split('-')[-1].upper()}"
                elif role == 'database':
                    title = "Ubuntu Database Server"
                elif role == 'application':
                    title = "Ubuntu Application Server"
                elif role == 'management':
                    title = "Ubuntu Management Server"
                else:
                    title = f"Ubuntu Server {item_name}"
                
                ubuntu_inventory.append({
                    'hostname': hostname,
                    'title': title,
                    'description': description,
                    'ip': ip_address,
                    'role': f"{role}-server"
                })
            
        except Exception as e:
            print(f"Warning: Could not process {xccdf_file.name}: {e}")
            continue
    
    return ubuntu_inventory, k8s_inventory


def create_ssp(profile_config: Dict[str, str], inventory: List[Dict[str, str]], component_name: str = 'Ubuntu_Linux_24_04_LTS', ssp_suffix: str = '') -> bool:
    """
    Create an SSP for a given profile.
    
    Args:
        profile_config: Profile configuration dictionary
        inventory: List of inventory items
        component_name: Name of the component definition to use
        ssp_suffix: Suffix to add to SSP name (e.g., '-k8s')
    
    Returns:
        True if successful
    """
    profile_name = profile_config['name']
    profile_title = profile_config['title']
    profile_ref = profile_config['ref_name']
    ref_type = profile_config['ref_type']
    
    print(f"\nCreating SSP for {profile_title}...")
    
    # Load the profile to get the list of controls
    profile = trestle_api.load_profile(profile_ref)
    if profile and profile.imports:
        profile_controls = set()
        for imp in profile.imports:
            if imp.include_controls:
                for inc in imp.include_controls:
                    if inc.with_ids:
                        profile_controls.update(inc.with_ids)
        print(f"  Profile contains {len(profile_controls)} controls")
    else:
        print(f"  Warning: Could not load profile controls, including all")
        profile_controls = None
    
    # Load component definition using trestle_api
    source_comp_data = trestle_api.load_component_dict(component_name)
    if not source_comp_data:
        print(f"Error: Could not load component definition {component_name}")
        return False
    
    source_comp_def = source_comp_data.get('component-definition', {})
    source_components = source_comp_def.get('components', [])
    
    if not source_components:
        print(f"Error: No components found in source component definition")
        return False
    
    # For Kubernetes, use the software component (first one)
    source_component_data = source_components[0]
    
    # Also load via trestle API for component object
    comp_def = trestle_api.load_component(component_name)
    if not comp_def:
        print(f"Error: Could not load component definition via trestle API")
        return False
    
    if not comp_def.components or len(comp_def.components) == 0:
        print(f"Error: No components found in component definition")
        return False
    
    # For Kubernetes, use the software component
    source_component = comp_def.components[0]
    
    # Get control-implementations from source
    ctrl_impls = source_component_data.get('control-implementations', [])
    
    print(f"  Component: {source_component.title}")
    print(f"  Inventory items: {len(inventory)}")
    print(f"  Control implementations: {len(ctrl_impls)}")
    if ctrl_impls:
        impl_reqs = ctrl_impls[0].get('implemented-requirements', [])
        print(f"  Implemented requirements: {len(impl_reqs)}")
    
    # Create SSP name - use appropriate prefix based on platform
    platform_prefix = 'Kubernetes-System-ssp' if 'k8s' in ssp_suffix else 'Ubuntu-System-ssp'
    ssp_name = f'{platform_prefix}-{profile_name}'
    
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
                {'name': 'asset-type', 'value': 'k8s-node' if 'k8s_version' in inv else 'server'},
                {'name': 'ipv4-address', 'value': inv['ip']},
                {'name': 'role', 'value': inv['role']},
                {'name': 'operating-system', 'value': f"Kubernetes {inv['k8s_version']}" if 'k8s_version' in inv else 'Ubuntu 24.04 LTS'}
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
                'title': f'{"Kubernetes" if "k8s" in ssp_suffix else "Ubuntu"} System Security Plan - {profile_title}',
                'last-modified': now.isoformat(),
                'version': '1.0',
                'oscal-version': OSCAL_VERSION
            },
            'import-profile': {
                'href': f"trestle://{'profiles' if ref_type == 'profile' else 'catalogs'}/{profile_ref}/{'profile' if ref_type == 'profile' else 'catalog'}.json"
            },
            'system-characteristics': {
                'system-ids': [
                    {'id': 'ubuntu-system-001'}
                ],
                'system-name': f'{"Kubernetes 1.28 Cluster" if "k8s" in ssp_suffix else "Ubuntu 24.04 LTS Fleet"}',
                'description': f'System Security Plan for {"Kubernetes 1.28 cluster with " + str(len(inventory)) + " nodes and kube-bench compliance validation" if "k8s" in ssp_suffix else "Ubuntu Linux 24.04 LTS " + str(len(inventory)) + "-server fleet with OSCAP compliance validation"} - {profile_title} baseline',
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
                    'description': f'{"Kubernetes 1.28 cluster with " + str(len(inventory)) + " nodes" if "k8s" in ssp_suffix else "Ubuntu Linux 24.04 LTS " + str(len(inventory)) + "-server fleet"} operating within a single authorization boundary, implementing {profile_title} security controls'
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
                'description': f'Control implementation for {profile_title} baseline using {"Kubernetes 1.28" if "k8s" in ssp_suffix else "Ubuntu Linux 24.04 LTS"}',
                'implemented-requirements': [
                    {
                        'uuid': str(uuid.uuid4()),
                        'control-id': req.get('control-id'),
                        'props': req.get('props', []) if req.get('props') else []
                    }
                    for req in ctrl_impls[0].get('implemented-requirements', [])
                    if profile_controls is None or req.get('control-id') in profile_controls
                ] if ctrl_impls else []
            }
        }
    }
    
    # Load as trestle object and save using API
    try:
        ssp = ssp_module.SystemSecurityPlan(**ssp_dict['system-security-plan'])
        if trestle_api.save_ssp(ssp, ssp_name):
            print(f"✓ Created: trestle-workspace/system-security-plans/{ssp_name}/system-security-plan.json")
            print(f"  Components: 1 ({component_name})")
            print(f"  Inventory items: {len(inventory_items)}")
            for inv in inventory:
                print(f"    - {inv['hostname']}: {inv['ip']}")
            return True
        else:
            print(f"✗ Failed to save SSP for {ssp_name}")
            return False
    except Exception as e:
        print(f"✗ Error creating SSP: {e}")
        traceback.print_exc()
        return False


def main():
    """Main execution function"""
    print("=" * 80)
    print("System Security Plans Generator")
    print("=" * 80)
    
    # Extract inventory from XCCDF files
    print(f"\nExtracting inventory from XCCDF scan results...")
    ubuntu_inventory, k8s_inventory = extract_inventory_from_xccdf()
    
    if not ubuntu_inventory and not k8s_inventory:
        print("Error: No inventory items found in XCCDF files")
        return
    
    print(f"\nFound {len(ubuntu_inventory)} Ubuntu servers:")
    for inv in ubuntu_inventory:
        print(f"  - {inv['hostname']}: {inv['title']} ({inv['ip']})")
    
    print(f"\nFound {len(k8s_inventory)} Kubernetes nodes:")
    for inv in k8s_inventory:
        print(f"  - {inv['hostname']}: {inv['title']} ({inv['ip']})")
    
    print(f"\nProfiles: {len(PROFILES)}")
    for profile in PROFILES:
        print(f"  - {profile['name']}: {profile['title']}")
    
    # Create SSPs for Ubuntu servers
    print(f"\n{'='*80}")
    print("Creating SSPs for Ubuntu servers...")
    print(f"{'='*80}")
    ubuntu_success_count = 0
    if ubuntu_inventory:
        for profile in PROFILES:
            if create_ssp(profile, ubuntu_inventory, 'Ubuntu_Linux_24_04_LTS', ''):
                ubuntu_success_count += 1
    
    # Create SSPs for Kubernetes nodes
    print(f"\n{'='*80}")
    print("Creating SSPs for Kubernetes cluster...")
    print(f"{'='*80}")
    k8s_success_count = 0
    if k8s_inventory:
        for profile in PROFILES:
            if create_ssp(profile, k8s_inventory, 'Kubernetes_1_28', '-k8s'):
                k8s_success_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {ubuntu_success_count}/{len(PROFILES)} Ubuntu SSPs")
    print(f"✓ Successfully created {k8s_success_count}/{len(PROFILES)} Kubernetes SSPs")
    print(f"✓ Total: {ubuntu_success_count + k8s_success_count}/{len(PROFILES) * 2} SSPs")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob