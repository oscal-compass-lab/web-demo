#!/usr/bin/env python3
"""
Update component definitions with new XCCDF rules for FedRAMP Moderate and High controls.
This script adds both Rule_Id properties AND control-implementations.

By default, updates files in source-data/component-definitions/
Set COMP_DEF_DIR environment variable to update files in a different location (e.g., trestle-workspace)
"""

import json
from pathlib import Path
from datetime import datetime
import uuid
import os

# New rules for FedRAMP Moderate (not in Low)
MODERATE_RULES = [
    {'rule_id': 'account_automated_provisioning_enabled', 'description': 'Verify automated account management is configured', 'control': 'ac-2.1'},
    {'rule_id': 'account_temporary_expiration_configured', 'description': 'Verify temporary account expiration is automated', 'control': 'ac-2.2'},
    {'rule_id': 'account_disable_inactive_accounts', 'description': 'Verify inactive account disabling mechanism', 'control': 'ac-2.3'},
    {'rule_id': 'sudo_security_function_authorization', 'description': 'Verify sudo configuration restricts security functions', 'control': 'ac-6.1'},
    {'rule_id': 'service_nonprivileged_user_execution', 'description': 'Verify services run as non-root users', 'control': 'ac-6.2'},
    {'rule_id': 'screen_lock_timeout_configured', 'description': 'Verify screen lock timeout is configured', 'control': 'ac-11'},
    {'rule_id': 'screen_lock_pattern_hiding_enabled', 'description': 'Verify screen blanking on lock', 'control': 'ac-11.1'},
    {'rule_id': 'sshd_logging_enabled', 'description': 'Verify SSH logging is enabled and comprehensive', 'control': 'ac-17.1'},
    {'rule_id': 'auditd_extended_information_enabled', 'description': 'Verify extended audit information is captured', 'control': 'au-3.1'},
    {'rule_id': 'log_analysis_tool_configured', 'description': 'Verify automated log analysis tool is configured', 'control': 'au-6.1'},
    {'rule_id': 'change_control_documentation_required', 'description': 'Verify change control process documentation', 'control': 'cm-3.2'},
    {'rule_id': 'service_periodic_review_enabled', 'description': 'Verify periodic service review process', 'control': 'cm-7.1'},
    {'rule_id': 'package_update_automation_configured', 'description': 'Verify automated patch management', 'control': 'si-2.2'},
    {'rule_id': 'intrusion_detection_tool_installed', 'description': 'Verify IDS/IPS tool is installed and running', 'control': 'si-4.2'}
]

# New rules for FedRAMP High (not in Moderate)
HIGH_RULES = [
    {'rule_id': 'encrypted_traffic_inspection_configured', 'description': 'Verify encrypted traffic inspection capability', 'control': 'ac-4.4'},
    {'rule_id': 'privileged_command_network_restriction', 'description': 'Verify network-based restrictions on privileged commands', 'control': 'ac-6.3'},
    {'rule_id': 'concurrent_session_limit_configured', 'description': 'Verify concurrent session limits', 'control': 'ac-10'},
    {'rule_id': 'auditd_storage_threshold_alert', 'description': 'Verify audit storage threshold alerting', 'control': 'au-5.1'},
    {'rule_id': 'auditd_realtime_alerts_enabled', 'description': 'Verify real-time audit failure alerts', 'control': 'au-5.2'},
    {'rule_id': 'centralized_logging_configured', 'description': 'Verify centralized logging is configured', 'control': 'au-6.4'},
    {'rule_id': 'audit_logs_remote_storage', 'description': 'Verify audit logs are sent to remote system', 'control': 'au-9.2'},
    {'rule_id': 'audit_logs_encrypted', 'description': 'Verify audit log encryption/signing', 'control': 'au-9.3'},
    {'rule_id': 'critical_action_signing_enabled', 'description': 'Verify digital signatures for critical actions', 'control': 'au-10'},
    {'rule_id': 'time_synchronization_configured', 'description': 'Verify NTP/chrony is configured and running', 'control': 'au-12.1'}
]

ALL_NEW_RULES = MODERATE_RULES + HIGH_RULES

# Group rules by control for control-implementations
def group_rules_by_control(rules):
    grouped = {}
    for rule in rules:
        ctrl = rule['control']
        if ctrl not in grouped:
            grouped[ctrl] = []
        grouped[ctrl].append(rule)
    return grouped

def get_next_rule_set_number(props):
    max_num = -1
    for prop in props:
        if 'remarks' in prop and prop['remarks'].startswith('rule_set_'):
            try:
                num = int(prop['remarks'].split('_')[-1])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return max_num + 1

def add_rules_to_software_component(comp_def_path):
    """Add Rule_Id props AND control-implementations to software component."""
    print(f"\nUpdating software component: {comp_def_path}")
    with open(comp_def_path, 'r') as f:
        data = json.load(f)
    
    component = data['component-definition']['components'][0]
    props = component['props']
    
    # Add Rule_Id properties
    start_num = get_next_rule_set_number(props)
    props_added = 0
    for idx, rule in enumerate(ALL_NEW_RULES):
        rule_set_num = start_num + idx
        rule_set_id = f"rule_set_{rule_set_num:02d}"
        props.append({"name": "Rule_Id", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": rule['rule_id'], "remarks": rule_set_id})
        props.append({"name": "Rule_Description", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": rule['description'], "remarks": rule_set_id})
        props_added += 1
    
    # Add control-implementations
    rules_by_control = group_rules_by_control(ALL_NEW_RULES)
    ci = component['control-implementations'][0]
    existing_reqs = ci['implemented-requirements']
    existing_control_ids = [r['control-id'] for r in existing_reqs]
    
    controls_added = 0
    for control_id, rules in sorted(rules_by_control.items()):
        if control_id not in existing_control_ids:
            new_req = {
                "uuid": str(uuid.uuid4()),
                "control-id": control_id,
                "description": f"Implementation of {control_id.upper()} via XCCDF validation",
                "props": [
                    {"name": "Rule_Id", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": rule['rule_id']}
                    for rule in rules
                ]
            }
            existing_reqs.append(new_req)
            controls_added += 1
    
    data['component-definition']['metadata']['last-modified'] = datetime.now().isoformat()
    data['component-definition']['metadata']['version'] = 'V1.2'
    
    with open(comp_def_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"  ✓ Added {props_added} rule properties")
    print(f"  ✓ Added {controls_added} control implementations")
    print(f"  ✓ Total controls: {len(existing_reqs)}")
    return props_added, controls_added

def add_rules_to_validation_component(comp_def_path):
    print(f"\nUpdating validation component: {comp_def_path}")
    with open(comp_def_path, 'r') as f:
        data = json.load(f)
    component = data['component-definition']['components'][0]
    props = component['props']
    start_num = get_next_rule_set_number(props)
    added_count = 0
    for idx, rule in enumerate(ALL_NEW_RULES):
        rule_set_num = start_num + idx
        rule_set_id = f"rule_set_{rule_set_num:02d}"
        props.append({"name": "Rule_Id", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": rule['rule_id'], "remarks": rule_set_id})
        props.append({"name": "Check_Id", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": f"xccdf_org.ssgproject.content_rule_{rule['rule_id']}", "remarks": rule_set_id})
        props.append({"name": "Check_Description", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": rule['description'], "remarks": rule_set_id})
        props.append({"name": "Target_Component", "ns": "https://oscal-compass/compliance-trestle/schemas/oscal/cd", "value": "Ubuntu_Linux_24.04_LTS", "remarks": rule_set_id})
        added_count += 1
    data['component-definition']['metadata']['last-modified'] = datetime.now().isoformat()
    data['component-definition']['metadata']['version'] = 'V1.1'
    with open(comp_def_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Added {added_count} new rules")
    return added_count

def main():
    print("=" * 80)
    print("Component Definition Updater - FedRAMP Moderate/High Controls")
    print("=" * 80)
    print(f"\nAdding {len(MODERATE_RULES)} FedRAMP Moderate-specific rules")
    print(f"Adding {len(HIGH_RULES)} FedRAMP High-specific rules")
    print(f"Total: {len(ALL_NEW_RULES)} new rules")

    # Use COMP_DEF_DIR environment variable if set, otherwise use source-data
    comp_def_dir = os.getenv('COMP_DEF_DIR', 'source-data/component-definitions')
    print(f"Target directory: {comp_def_dir}")

    software_path = Path(comp_def_dir) / 'Ubuntu_Linux_24_04_LTS' / 'component-definition.json'
    validation_path = Path(comp_def_dir) / 'oscap' / 'component-definition.json'

    if software_path.exists():
        props_count, controls_count = add_rules_to_software_component(software_path)
    else:
        print(f"  ✗ Software component not found: {software_path}")
        props_count, controls_count = 0, 0

    if validation_path.exists():
        validation_count = add_rules_to_validation_component(validation_path)
    else:
        print(f"  ✗ Validation component not found: {validation_path}")
        validation_count = 0

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Software component (Ubuntu_Linux_24_04_LTS):")
    print(f"  - Rule properties added: {props_count}")
    print(f"  - Control implementations added: {controls_count}")
    print(f"Validation component (oscap):")
    print(f"  - Rules added: {validation_count}")
    print()
    print("✓ Component definitions updated successfully!")
    print("✓ Run 'make clean-artifacts artifacts' to regenerate all OSCAL documents")
    print("=" * 80)

if __name__ == '__main__':
    main()
