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
Create XCCDF result files for each Ubuntu server component
Uses all rules from the OSCAP validation component definition
"""

from pathlib import Path
from datetime import datetime, timedelta
import random
from trestle_api import TrestleAPI
from server_config import get_all_servers

# Initialize Trestle API
trestle_api = TrestleAPI(Path('trestle-workspace'))

# Load OSCAP component to get all rules
print("Loading OSCAP component definition...")
oscap_comp = trestle_api.load_component('oscap')
if not oscap_comp or not oscap_comp.components:
    print("Error: Could not load OSCAP component")
    exit(1)

# Extract all Rule_Id properties
oscap_component = oscap_comp.components[0]
rules = []
if oscap_component.props:
    for prop in oscap_component.props:
        if prop.name == 'Rule_Id':
            rules.append(str(prop.value))

print(f"Found {len(rules)} rules in OSCAP component\n")

# Get server configurations from common data file
servers = get_all_servers()

# Create results directory
results_dir = Path("source-data/xccdf-results")
results_dir.mkdir(parents=True, exist_ok=True)

print("Creating XCCDF result files for Ubuntu servers...\n")

base_time = datetime.now()

for server in servers:
    filename = results_dir / f"{server['name']}-xccdf-results.xml"
    
    # Calculate pass/fail based on compliance rate
    num_rules = len(rules)
    num_pass = int(num_rules * server['compliance_rate'])
    num_fail = num_rules - num_pass
    
    # Randomly assign pass/fail to rules
    results = ['pass'] * num_pass + ['fail'] * num_fail
    random.shuffle(results)
    
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
    for rule_id, result in zip(rules, results):
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

print(f"\n✓ All XCCDF result files created in {results_dir}/")
print(f"  Total servers: {len(servers)}")
print(f"  Rules per server: {len(rules)} (from OSCAP component definition)")

# Made with Bob
