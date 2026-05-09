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
Create XCCDF result files for inventory items (Ubuntu servers and Kubernetes nodes).

For Ubuntu servers:
- Uses all rules from the OSCAP validation component definition
- Generates OpenSCAP-format XCCDF results

For Kubernetes nodes:
- Uses all rules from the kube-bench validation component definition
- Generates CIS Kubernetes Benchmark-format XCCDF results
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
sys.path.insert(0, str(Path(__file__).parent.parent))
from trestle_api import TrestleAPI
from server_config import get_all_servers, get_all_k8s_nodes

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))

# Load OSCAP component to get all rules for Ubuntu servers
print("Loading OSCAP component definition...")
oscap_comp = trestle_api.load_component('oscap')
if not oscap_comp or not oscap_comp.components:
    print("Error: Could not load OSCAP component")
    exit(1)

# Extract all Rule_Id properties from OSCAP
oscap_component = oscap_comp.components[0]
oscap_rules = []
if oscap_component.props:
    for prop in oscap_component.props:
        if prop.name == 'Rule_Id':
            oscap_rules.append(str(prop.value))

print(f"Found {len(oscap_rules)} rules in OSCAP component\n")

# Load Kubernetes component to get all rules for K8s nodes
print("Loading Kubernetes component definition...")
k8s_comp = trestle_api.load_component('Kubernetes_1_28')
if not k8s_comp or not k8s_comp.components:
    print("Error: Could not load Kubernetes component")
    exit(1)

# Extract all Rule_Id properties from kube-bench (validation component)
kube_bench_component = None
for comp in k8s_comp.components:
    if comp.type == 'validation':
        kube_bench_component = comp
        break

if not kube_bench_component:
    print("Error: Could not find kube-bench validation component")
    exit(1)

k8s_rules = []
if kube_bench_component.props:
    for prop in kube_bench_component.props:
        if prop.name == 'Rule_Id':
            k8s_rules.append(str(prop.value))

print(f"Found {len(k8s_rules)} rules in kube-bench component\n")

# Get server and node configurations from common data file
servers = get_all_servers()
k8s_nodes = get_all_k8s_nodes()

# Create results directory
results_dir = Path("source-data/xccdf-results")
results_dir.mkdir(parents=True, exist_ok=True)

print("Creating XCCDF result files for Ubuntu servers...\n")

base_time = datetime.now()

# Force certain rules to always fail to create exactly 2 "not-satisfied" controls
# au-2 has 1 unique rule: sshd_set_loglevel_info
# au-3 has 2 rules, one unique: sudo_custom_logfile
UBUNTU_ALWAYS_FAIL_RULES = [
    'sshd_set_loglevel_info',  # au-2 control (1 control affected)
    'sudo_custom_logfile'       # au-3 control (1 control affected)
]

# Force certain K8s rules to always fail
K8S_ALWAYS_FAIL_RULES = [
    'control_plane_api_server_audit_log_path',  # au-2 control
    'worker_node_kubelet_anonymous_auth'        # ac-2 control
]

print("Creating XCCDF result files for Ubuntu servers...\n")

for server in servers:
    filename = results_dir / f"{server['name']}-xccdf-results.xml"
    
    # Calculate pass/fail based on compliance rate
    num_rules = len(oscap_rules)
    num_pass = int(num_rules * server['compliance_rate'])
    num_fail = num_rules - num_pass
    
    # Randomly assign pass/fail to rules
    results = ['pass'] * num_pass + ['fail'] * num_fail
    random.shuffle(results)
    
    # Force specific rules to always fail (creates not-satisfied controls)
    for i, rule_id in enumerate(oscap_rules):
        if rule_id in UBUNTU_ALWAYS_FAIL_RULES:
            results[i] = 'fail'
    
    # Assign random severity to each rule
    severities = ['high', 'medium', 'low']
    
    # Generate XCCDF XML
    scan_start = base_time - timedelta(hours=random.randint(1, 48))
    scan_end = scan_start + timedelta(minutes=random.randint(5, 15))
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Benchmark xmlns="http://checklists.nist.gov/xccdf/1.2"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           id="xccdf_org.ssgproject.content_benchmark_UBUNTU-24-04"
           resolved="true">
  
  <status date="{scan_start.strftime('%Y-%m-%d')}">accepted</status>
  <title>Guide to the Secure Configuration of Ubuntu 24.04 LTS</title>
  <description>
    This guide presents a catalog of security-relevant configuration settings for Ubuntu
    24.04 LTS. It is a rendering of content structured in the eXtensible Configuration
    Checklist Description Format (XCCDF) in order to support security automation.
  </description>
  <version>1.0.0</version>
  
  <Profile id="xccdf_org.ssgproject.content_profile_fedramp_moderate">
    <title>FedRAMP Moderate Baseline for Ubuntu 24.04 LTS</title>
    <description>
      This profile contains configuration checks that align to the FedRAMP Moderate baseline.
    </description>
  </Profile>
  
  <TestResult id="xccdf_org.open-scap_testresult_xccdf_org.ssgproject.content_profile_fedramp_moderate"
              start-time="{scan_start.isoformat()}"
              end-time="{scan_end.isoformat()}"
              version="1.2"
              test-system="cpe:/a:open-scap:openscap:1.3.9">
    
    <benchmark href="/usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml"
               id="xccdf_org.ssgproject.content_benchmark_UBUNTU-24-04"/>
    
    <title>OSCAP Scan Result - {server['description']}</title>
    
    <identity authenticated="true" privileged="true">root</identity>
    
    <profile idref="xccdf_org.ssgproject.content_profile_fedramp_moderate"/>
    
    <target>{server['hostname']}</target>
    <target-address>{server['ip']}</target-address>
    <target-facts>
      <fact name="urn:xccdf:fact:asset:identifier:host_name" type="string">{server['hostname']}</fact>
      <fact name="urn:xccdf:fact:asset:identifier:ipv4" type="string">{server['ip']}</fact>
      <fact name="urn:xccdf:fact:asset:identifier:os_name" type="string">Ubuntu</fact>
      <fact name="urn:xccdf:fact:asset:identifier:os_version" type="string">24.04 LTS</fact>
    </target-facts>
    
    <platform idref="cpe:/o:canonical:ubuntu_linux:24.04"/>
    
    <score system="urn:xccdf:scoring:default" maximum="100.000000">{server['compliance_rate'] * 100:.1f}</score>
    
'''
    
    # Add rule results
    rule_time = scan_start
    for rule_id, result in zip(oscap_rules, results):
        rule_time += timedelta(seconds=random.randint(5, 15))
        severity = random.choice(severities)
        
        xml_content += f'''    <rule-result idref="xccdf_org.ssgproject.content_rule_{rule_id}"
                 time="{rule_time.isoformat()}"
                 severity="{severity}"
                 weight="1.000000">
      <result>{result}</result>
      <ident system="https://nvd.nist.gov/cce/index.cfm">CCE-{random.randint(80000, 90000)}-{random.randint(0, 9)}</ident>
      <check system="http://oval.mitre.org/XMLSchema/oval-definitions-5">
        <check-content-ref name="oval:ssg:def:{random.randint(100, 999)}" href="ssg-ubuntu2404-oval.xml"/>
      </check>
'''
        
        if result == 'fail':
            xml_content += f'''      <message severity="error">Check failed: {rule_id}</message>
'''
        
        xml_content += '''    </rule-result>
    
'''
    
    xml_content += '''  </TestResult>
</Benchmark>
'''
    
    # Write file
    with open(filename, 'w') as f:
        f.write(xml_content)
    
    print(f"✓ Created: {filename}")
    print(f"  Server: {server['hostname']}")
    print(f"  Rules checked: {num_rules}")
    print(f"  Compliance: {server['compliance_rate'] * 100:.1f}% ({num_pass}/{num_rules} passed)")
    print(f"  Scan time: {scan_start.strftime('%Y-%m-%d %H:%M:%S')}\n")

print(f"\n✓ All Ubuntu server XCCDF result files created")
print(f"  Total Ubuntu servers: {len(servers)}")
print(f"  Rules per server: {len(oscap_rules)} (from OSCAP component definition)\n")

# Now create XCCDF results for Kubernetes nodes
print("Creating XCCDF result files for Kubernetes nodes...\n")

for node in k8s_nodes:
    filename = results_dir / f"{node['name']}-xccdf-results.xml"
    
    # Calculate pass/fail based on compliance rate
    num_rules = len(k8s_rules)
    num_pass = int(num_rules * node['compliance_rate'])
    num_fail = num_rules - num_pass
    
    # Randomly assign pass/fail to rules
    results = ['pass'] * num_pass + ['fail'] * num_fail
    random.shuffle(results)
    
    # Force specific rules to always fail (creates not-satisfied controls)
    for i, rule_id in enumerate(k8s_rules):
        if rule_id in K8S_ALWAYS_FAIL_RULES:
            results[i] = 'fail'
    
    # Assign random severity to each rule
    severities = ['high', 'medium', 'low']
    
    # Generate XCCDF XML for Kubernetes
    scan_start = base_time - timedelta(hours=random.randint(1, 48))
    scan_end = scan_start + timedelta(minutes=random.randint(5, 15))
    
    # Determine profile based on node type
    profile_id = "xccdf_org.cisecurity.benchmarks_profile_Level_2_-_Master_Node" if node['node_type'] == 'master' else "xccdf_org.cisecurity.benchmarks_profile_Level_2_-_Worker_Node"
    profile_title = f"CIS Kubernetes Benchmark Level 2 - {node['node_type'].title()} Node"
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Benchmark xmlns="http://checklists.nist.gov/xccdf/1.2"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           id="xccdf_org.cisecurity.benchmarks_benchmark_kubernetes"
           resolved="true">
  
  <status date="{scan_start.strftime('%Y-%m-%d')}">accepted</status>
  <title>CIS Kubernetes Benchmark v1.8.0</title>
  <description>
    This benchmark provides prescriptive guidance for establishing a secure configuration
    posture for Kubernetes v{node['k8s_version']}. This guide was tested against Kubernetes
    running on Linux.
  </description>
  <version>1.8.0</version>
  
  <Profile id="{profile_id}">
    <title>{profile_title}</title>
    <description>
      This profile contains configuration checks that align to the CIS Kubernetes Benchmark
      Level 2 for {node['node_type']} nodes.
    </description>
  </Profile>
  
  <TestResult id="xccdf_org.kube-bench_testresult_{profile_id}"
              start-time="{scan_start.isoformat()}"
              end-time="{scan_end.isoformat()}"
              version="1.2"
              test-system="cpe:/a:aquasecurity:kube-bench:0.7.0">
    
    <benchmark href="/etc/kube-bench/cfg/cis-1.8/benchmark.yml"
               id="xccdf_org.cisecurity.benchmarks_benchmark_kubernetes"/>
    
    <title>kube-bench Scan Result - {node['description']}</title>
    
    <identity authenticated="true" privileged="true">root</identity>
    
    <profile idref="{profile_id}"/>
    
    <target>{node['hostname']}</target>
    <target-address>{node['ip']}</target-address>
    <target-facts>
      <fact name="urn:xccdf:fact:asset:identifier:host_name" type="string">{node['hostname']}</fact>
      <fact name="urn:xccdf:fact:asset:identifier:ipv4" type="string">{node['ip']}</fact>
      <fact name="urn:xccdf:fact:asset:identifier:platform" type="string">Kubernetes</fact>
      <fact name="urn:xccdf:fact:asset:identifier:k8s_version" type="string">{node['k8s_version']}</fact>
      <fact name="urn:xccdf:fact:asset:identifier:node_type" type="string">{node['node_type']}</fact>
    </target-facts>
    
    <platform idref="cpe:/a:kubernetes:kubernetes:{node['k8s_version']}"/>
    
    <score system="urn:xccdf:scoring:default" maximum="100.000000">{node['compliance_rate'] * 100:.1f}</score>
    
'''
    
    # Add rule results
    rule_time = scan_start
    for rule_id, result in zip(k8s_rules, results):
        rule_time += timedelta(seconds=random.randint(5, 15))
        severity = random.choice(severities)
        
        xml_content += f'''    <rule-result idref="xccdf_org.cisecurity.benchmarks_rule_{rule_id}"
                 time="{rule_time.isoformat()}"
                 severity="{severity}"
                 weight="1.000000">
      <result>{result}</result>
      <ident system="https://www.cisecurity.org/benchmark/kubernetes">CIS-K8S-{random.randint(1, 5)}.{random.randint(1, 9)}.{random.randint(1, 20)}</ident>
      <check system="http://oval.mitre.org/XMLSchema/oval-definitions-5">
        <check-content-ref name="oval:org.cisecurity.benchmarks:def:{random.randint(100, 999)}" href="cis-kubernetes-oval.xml"/>
      </check>
'''
        
        if result == 'fail':
            xml_content += f'''      <message severity="error">Check failed: {rule_id}</message>
'''
        
        xml_content += '''    </rule-result>
    
'''
    
    xml_content += '''  </TestResult>
</Benchmark>
'''
    
    # Write file
    with open(filename, 'w') as f:
        f.write(xml_content)
    
    print(f"✓ Created: {filename}")
    print(f"  Node: {node['hostname']}")
    print(f"  Type: {node['node_type']}")
    print(f"  Rules checked: {num_rules}")
    print(f"  Compliance: {node['compliance_rate'] * 100:.1f}% ({num_pass}/{num_rules} passed)")
    print(f"  Scan time: {scan_start.strftime('%Y-%m-%d %H:%M:%S')}\n")

print(f"\n{'='*60}")
print(f"✓ All XCCDF result files created in {results_dir}/")
print(f"{'='*60}")
print(f"  Ubuntu servers: {len(servers)} ({len(oscap_rules)} OSCAP rules each)")
print(f"  Kubernetes nodes: {len(k8s_nodes)} ({len(k8s_rules)} kube-bench rules each)")
print(f"  Total inventory items: {len(servers) + len(k8s_nodes)}")
print(f"{'='*60}")

# Made with Bob
