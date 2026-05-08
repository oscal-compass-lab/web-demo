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
OSCAL Compliance Demo - Flask Web Application
Reads OSCAL documents from trestle workspace using compliance-trestle
"""

from flask import Flask, render_template, jsonify, redirect, send_from_directory
import flask
import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import json
from trestle_api import TrestleAPI

app = Flask(__name__, template_folder='app-config/templates', static_folder='app-config/static')

# Add route to serve charts from source-data
@app.route('/charts/<path:filename>')
def serve_chart(filename):
    """Serve chart images from source-data/charts directory"""
    return send_from_directory('source-data/charts', filename)

# Initialize Trestle API
TRESTLE_ROOT = Path('trestle-workspace')
trestle_api = TrestleAPI(TRESTLE_ROOT)

# Title display mapping - simplify certain titles for display
TITLE_DISPLAY_MAP = {
    # FedRAMP Profiles and Catalogs
    'FedRAMP High Baseline (NIST 800-53 Rev5)': 'FedRAMP',
    'FedRAMP Moderate Baseline (NIST 800-53 Rev5)': 'FedRAMP',
    'FedRAMP Low Baseline (NIST 800-53 Rev5)': 'FedRAMP',
    'FedRAMP Rev 5 High Baseline': 'FedRAMP',
    'FedRAMP Rev 5 Moderate Baseline': 'FedRAMP',
    'FedRAMP Rev 5 Low Baseline': 'FedRAMP',
    # DORA
    'Digital Operational Resilience Act (DORA)': 'DORA',
    # NIST 800-53
    'Electronic (OSCAL) Version of NIST SP 800-53 Rev 5.2.0 Controls and SP 800-53A Rev 5.2.0 Assessment Procedures': 'NIST SP 800-53',
    # Mappings
    'NIST SP 800-53 Rev 5 to Digital Operational Resilience Act (DORA)': 'NIST SP 800-53 Rev 5 to DORA',
    # Components
    'Component definition for Ubuntu_Linux_24.04_LTS': 'Ubuntu 24.04 LTS',
    # SSPs
    'Ubuntu System Security Plan - FedRAMP Low': 'Ubuntu FedRAMP Low',
    'Ubuntu System Security Plan - FedRAMP Moderate': 'Ubuntu FedRAMP Moderate',
    'Ubuntu System Security Plan - FedRAMP High': 'Ubuntu FedRAMP High',
    'Ubuntu System Security Plan - DORA': 'Ubuntu DORA',
    # Assessment Plans
    'Ubuntu System Assessment Plan - FedRAMP Low': 'Ubuntu FedRAMP Low',
    'Ubuntu System Assessment Plan - FedRAMP Moderate': 'Ubuntu FedRAMP Moderate',
    'Ubuntu System Assessment Plan - FedRAMP High': 'Ubuntu FedRAMP High',
    'Ubuntu System Assessment Plan - DORA': 'Ubuntu DORA',
    # Assessment Results
    'Ubuntu System Assessment Results - FedRAMP Low': 'Ubuntu FedRAMP Low',
    'Ubuntu System Assessment Results - FedRAMP Moderate': 'Ubuntu FedRAMP Moderate',
    'Ubuntu System Assessment Results - FedRAMP High': 'Ubuntu FedRAMP High',
    'Ubuntu System Assessment Results - DORA': 'Ubuntu DORA',
    # POA&Ms (directory names)
    'Ubuntu-System-poam-fedramp-low': 'Ubuntu FedRAMP Low',
    'Ubuntu-System-poam-fedramp-moderate': 'Ubuntu FedRAMP Moderate',
    'Ubuntu-System-poam-fedramp-high': 'Ubuntu FedRAMP High',
    'Ubuntu-System-poam-dora': 'Ubuntu DORA',
    # POA&Ms (full titles from JSON)
    'Ubuntu System Plan of Action and Milestones - FedRAMP Low': 'Ubuntu FedRAMP Low',
    'Ubuntu System Plan of Action and Milestones - FedRAMP Moderate': 'Ubuntu FedRAMP Moderate',
    'Ubuntu System Plan of Action and Milestones - FedRAMP High': 'Ubuntu FedRAMP High',
    'Ubuntu System Plan of Action and Milestones - DORA': 'Ubuntu DORA',
}

def get_display_title(title):
    """Get simplified display title if mapping exists, otherwise return original"""
    return TITLE_DISPLAY_MAP.get(title, title)

def get_catalogs():
    """Get list of available catalogs using trestle API"""
    return trestle_api.list_catalogs()

def get_profiles():
    """Get list of available profiles using trestle API"""
    return trestle_api.list_profiles()

def load_catalog(catalog_name):
    """Load a specific catalog using trestle API"""
    return trestle_api.load_catalog_dict(catalog_name)

def load_profile(profile_name):
    """Load a specific profile using trestle API"""
    return trestle_api.load_profile_dict(profile_name)

def load_component(component_name):
    """Load a specific component definition using trestle API"""
    return trestle_api.load_component_dict(component_name)

def load_ssp(ssp_name):
    """Load a specific SSP using trestle API"""
    return trestle_api.load_ssp_dict(ssp_name)

def get_components():
    """Get list of available component definitions using trestle API"""
    components = trestle_api.list_components()
    # Add type info from first component
    for comp_info in components:
        comp_obj = trestle_api.load_component(comp_info['name'])
        if comp_obj and comp_obj.components:
            comp_info['type'] = str(comp_obj.components[0].type)
        else:
            comp_info['type'] = 'N/A'
    return components

def get_ssps():
    """Get list of available SSPs using trestle API"""
    return trestle_api.list_ssps()

def get_assessment_plans():
    """Get list of available assessment plans using trestle API"""
    return trestle_api.list_assessment_plans()

def get_assessment_results():
    """Get list of available assessment results using trestle API"""
    return trestle_api.list_assessment_results()

def get_poams():
    """Get list of available POA&Ms using trestle API"""
    return trestle_api.list_poams()

def get_mappings():
    """Get list of available mappings using trestle API"""
    return trestle_api.list_mappings()

def get_xccdf_results():
    """Get list of available XCCDF result files"""
    xccdf_dir = Path('source-data/xccdf-results')
    if not xccdf_dir.exists():
        return []
    
    results = []
    for xml_file in sorted(xccdf_dir.glob('*.xml')):
        # Parse basic info from filename
        name = xml_file.stem.replace('-xccdf-results', '')
        results.append({
            'name': name,
            'filename': xml_file.name,
            'title': f"XCCDF {name}",
            'path': str(xml_file.relative_to(Path('.')))
        })
    return results

@app.route('/')
def index():
    """Main navigation page"""
    catalogs = get_catalogs()
    profiles = get_profiles()
    components = sorted(get_components(), key=lambda x: (x.get('type') != 'software', x.get('name')))
    ssps = get_ssps()
    assessment_plans = get_assessment_plans()
    xccdf_results = get_xccdf_results()
    assessment_results = get_assessment_results()
    poams = get_poams()
    mappings = get_mappings()
    
    # Apply display title mapping to profiles, catalogs, mappings, components, SSPs, assessment plans, assessment results, and POA&Ms
    for profile in profiles:
        profile['display_title'] = get_display_title(profile['title'])
    for catalog in catalogs:
        catalog['display_title'] = get_display_title(catalog['title'])
    for mapping in mappings:
        mapping['display_title'] = get_display_title(mapping['title'])
    for component in components:
        component['display_title'] = get_display_title(component['title'])
    for ssp in ssps:
        ssp['display_title'] = get_display_title(ssp['title'])
    for plan in assessment_plans:
        plan['display_title'] = get_display_title(plan['title'])
    for result in assessment_results:
        result['display_title'] = get_display_title(result['title'])
    for poam in poams:
        poam['display_title'] = get_display_title(poam['title'])
    
    total_docs = len(catalogs) + len(profiles) + len(components) + len(ssps) + len(assessment_plans) + len(xccdf_results) + len(assessment_results) + len(poams) + len(mappings)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OSCAL Compliance Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); position: relative; }}
            .powered-by {{ position: absolute; top: 10px; right: 20px; font-size: 11px; color: #7f8c8d; background: #f8f9fa; padding: 5px 10px; border-radius: 4px; border: 1px solid #e0e0e0; }}
            .header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }}
            .logo {{ height: 60px; width: auto; }}
            .header-text {{ flex: 1; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin: 0; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 400px)); gap: 20px; margin: 20px 0; }}
            .card {{ background: #e8f4f8; border: 1px solid #ddd; border-radius: 8px; padding: 20px; transition: transform 0.2s, box-shadow 0.2s; width: 400px; box-sizing: border-box; }}
            .card:hover {{ transform: translateY(-5px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
            .card h3 {{ color: #2980b9; margin-top: 0; }}
            .card p {{ color: #7f8c8d; margin: 10px 0; }}
            .card a {{ display: inline-block; margin-top: 10px; padding: 8px 16px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
            .card a:hover {{ background: #2980b9; }}
            .status {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
            .status.ready {{ background: #2ecc71; color: white; }}
            .status.pending {{ background: #f39c12; color: white; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; }}
            .info {{ background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
            .frameworks-image {{ width: 100%; max-width: 800px; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="powered-by">
                <strong>Powered by:</strong> compliance-trestle 4.0+ | Flask {flask.__version__}
            </div>
            <div class="header">
                <img src="/static/images/oscal-compass-logo.png" alt="OSCAL Compass Logo" class="logo">
                <div class="header-text">
                    <h1>OSCAL Compass Compliance Demo</h1>
                </div>
            </div>
            <p>Comprehensive demonstration comprising complete set of OSCAL documents using OSCAL Compass <a href="https://pypi.org/project/compliance-trestle/" target="_blank" style="color: #3498db; text-decoration: none; font-weight: bold;">compliance-trestle</a></p>
            
            <p>Presented are a complete set of OSCAL documents covering:</p>
            <ul>
                <li>2 regulations DORA and FedRAMP (Low, Moderate, and High levels)</li>
                <li>6 inventory items (ubuntu VMs)</li>
            </ul>
            <p>The documents have been constructed using OSCAL Compass Compliance-trestle.</p>
            
            <div class="info">
                <strong>📊 Total Documents:</strong> {total_docs} OSCAL documents + <a href="#xccdf-results">{len(xccdf_results)} XCCDF results</a><br>
                <strong>📚 Breakdown:</strong>
                <a href="#catalogs">{len(catalogs)} catalogs</a>,
                <a href="#profiles">{len(profiles)} profiles</a>,
                <a href="#mappings">{len(mappings)} mapping-collections</a>,
                <a href="#components">{len(components)} component definitions</a>,
                <a href="#ssps">{len(ssps)} SSPs</a>,
                <a href="#assessment-plans">{len(assessment_plans)} assessment plans</a>,
                <a href="#xccdf-results">{len(xccdf_results)} XCCDF results</a>,
                <a href="#assessment-results">{len(assessment_results)} assessment results</a>,
                <a href="#charts">compliance charts</a>,
                <a href="#poams">{len(poams)} POA&Ms</a>
            </div>
            
            <img src="/static/images/oscal-framework-layers.png" alt="OSCAL Framework Layers" class="frameworks-image">
            
            <h2 id="catalogs">📚 OSCAL Catalogs and Resolved Profiles ({len(catalogs)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{cat['title']}">
                    <h3>📖 {cat.get('display_title', cat['title'])}</h3>
                    <p><strong>Name:</strong> {cat['name']}</p>
                    <p><strong>Version:</strong> {cat['version']}</p>
                    <a href="/catalog/{cat['name']}">View Catalog</a>
                </div>
                ''' for cat in catalogs])}
            </div>
            
            <h2 id="profiles">📋 OSCAL Profiles ({len(profiles)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{prof['title']}">
                    <h3>📋 {prof.get('display_title', prof['title'])}</h3>
                    <p><strong>Name:</strong> {prof['name']}</p>
                    <p><strong>Version:</strong> {prof['version']}</p>
                    <a href="/profile/{prof['name']}">View Profile</a>
                </div>
                ''' for prof in profiles])}
            </div>
            
            <h2 id="mappings">🔗 OSCAL Mapping Collections ({len(mappings)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{mapping['title']}">
                    <h3>🔗 {mapping.get('display_title', mapping['title'])}</h3>
                    <p><strong>Name:</strong> {mapping['name']}</p>
                    <p><strong>Version:</strong> {mapping['version']}</p>
                    <a href="/mapping/{mapping['name']}">View Mapping Collection</a>
                </div>
                ''' for mapping in mappings]) if mappings else '<p><em>No mappings found. Run "make create-docs" to generate demo documents.</em></p>'}
            </div>
            
            <h2 id="components">🔧 OSCAL Component Definitions ({len(components)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{comp['title']}">
                    <h3>{'🔍' if comp.get('type') == 'validation' else '🔧'} {comp.get('display_title', comp['title'])}</h3>
                    <p><strong>Name:</strong> {comp['name']}</p>
                    <p><strong>Version:</strong> {comp['version']}</p>
                    <a href="/component/{comp['name']}">View Component Definition</a>
                </div>
                ''' for comp in components]) if components else '<p><em>No component definitions found. Run "make create-docs" to generate demo documents.</em></p>'}
            </div>
            
            <h2 id="ssps">📄 OSCAL System Security Plans ({len(ssps)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{ssp['title']}">
                    <h3>📄 {ssp.get('display_title', ssp['title'])}</h3>
                    <p><strong>Name:</strong> {ssp['name']}</p>
                    <p><strong>Version:</strong> {ssp['version']}</p>
                    <a href="/ssp/{ssp['name']}">View SSP</a>
                </div>
                ''' for ssp in ssps]) if ssps else '<p><em>No SSPs found. Run "make create-docs" to generate demo documents.</em></p>'}
            </div>
            
            <h2 id="assessment-plans">📋 OSCAL Assessment Plans ({len(assessment_plans)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{plan['title']}">
                    <h3>📋 {plan.get('display_title', plan['title'])}</h3>
                    <p><strong>Name:</strong> {plan['name']}</p>
                    <p><strong>Version:</strong> {plan['version']}</p>
                    <a href="/assessment-plan/{plan['name']}">View Assessment Plan</a>
                </div>
                ''' for plan in assessment_plans]) if assessment_plans else '<p><em>No assessment plans found. Run "make create-docs" to generate demo documents.</em></p>'}
            </div>
            
            <h2 id="xccdf-results">🔍 OpenSCAP XCCDF Scan Results ({len(xccdf_results)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{result['title']}">
                    <h3>🔍 {result['title']}</h3>
                    <p><strong>Server:</strong> {result['name']}</p>
                    <p><strong>File:</strong> {result['filename']}</p>
                    <a href="/xccdf-result/{result['name']}">View XCCDF Results</a>
                </div>
                ''' for result in xccdf_results]) if xccdf_results else '<p><em>No XCCDF results found. Run "python3 create_xccdf_results.py" to generate scan results.</em></p>'}
            </div>
            
            <h2 id="assessment-results">📊 OSCAL Assessment Results ({len(assessment_results)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{result['title']}">
                    <h3>📊 {result.get('display_title', result['title'])}</h3>
                    <p><strong>Name:</strong> {result['name']}</p>
                    <p><strong>Version:</strong> {result['version']}</p>
                    <a href="/assessment-results/{result['name']}">View Assessment Results</a>
                </div>
                ''' for result in assessment_results]) if assessment_results else '<p><em>No assessment results found. Run "make create-docs" to generate demo documents.</em></p>'}
            </div>
            
            <h2 id="charts">📈 Compliance Status Charts</h2>
            <div class="info">
                <p><strong>📊 Visual Dashboard:</strong> View all compliance status charts in one place showing control compliance across regulatory frameworks.</p>
                <p><strong>Available Charts:</strong> FedRAMP (Low, Moderate, High), DORA, and Cross-Regulation Comparison</p>
                <p style="text-align: center; margin-top: 15px;">
                    <a href="/charts" style="display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 1.1em;">📈 View Assessment Charts</a>
                </p>
            </div>
            
            <h2 id="poams">📝 OSCAL Plan of Action & Milestones ({len(poams)})</h2>
            <div class="grid">
                {''.join([f'''
                <div class="card" title="{poam['title']}">
                    <h3>📝 {poam.get('display_title', poam['title'])}</h3>
                    <p><strong>Name:</strong> {poam['name']}</p>
                    <p><strong>Version:</strong> {poam['version']}</p>
                    <a href="/poam/{poam['name']}">View POA&M</a>
                </div>
                ''' for poam in poams]) if poams else '<p><em>No POA&Ms found. Run "make create-docs" to generate demo documents.</em></p>'}
            </div>
            
            <div class="footer">
                <p><strong>OSCAL Compass Demo</strong></p>
                <p><a href="https://pages.nist.gov/OSCAL/">OSCAL Documentation</a> | <a href="https://oscal-compass.github.io/compliance-trestle/">Trestle Docs</a> | <a href="https://github.com/oscal-compass">OSCAL Compass</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/catalog/<catalog_name>')
def catalog(catalog_name):
    """View specific catalog with fully expandable control details, sub-groups, sub-controls, and parameters"""
    data = load_catalog(catalog_name)
    if not data:
        return f"Catalog '{catalog_name}' not found", 404
    
    catalog_data = data.get('catalog', {})
    metadata = catalog_data.get('metadata', {})
    groups = catalog_data.get('groups', [])
    
    # Helper function to render expandable parameter
    def render_parameter(param, param_idx, parent_id):
        """Render a parameter with expandable details"""
        param_id = param.get('id', 'N/A')
        param_label = param.get('label', 'No label')
        param_values = param.get('values', [])
        param_select = param.get('select', {})
        param_guidelines = param.get('guidelines', [])
        param_remarks = param.get('remarks', '')
        param_props = param.get('props', [])
        param_links = param.get('links', [])
        param_constraints = param.get('constraints', [])
        
        # Build parameter summary
        param_summary = f'<code>{param_id}</code>: {param_label}'
        if param_values:
            param_summary += f' <span class="param-badge">Values: {len(param_values)}</span>'
        if param_select:
            choice = param_select.get('choice', [])
            if choice:
                param_summary += f' <span class="param-badge">Choices: {len(choice)}</span>'
        
        # Build expandable details
        details_html = []
        
        if param_values:
            details_html.append(f'<div class="param-detail"><strong>Values:</strong> {", ".join(param_values)}</div>')
        
        if param_select:
            choice = param_select.get('choice', [])
            how_many = param_select.get('how-many', 'one')
            if choice:
                details_html.append(f'<div class="param-detail"><strong>Select ({how_many}):</strong><ul>{"".join([f"<li>{c}</li>" for c in choice])}</ul></div>')
        
        if param_guidelines:
            guidelines_text = '<ul>'
            for guideline in param_guidelines:
                prose = guideline.get('prose', '')
                if prose:
                    guidelines_text += f'<li>{prose}</li>'
            guidelines_text += '</ul>'
            details_html.append(f'<div class="param-detail"><strong>Guidelines:</strong>{guidelines_text}</div>')
        
        if param_constraints:
            constraints_text = '<ul>'
            for constraint in param_constraints:
                description = constraint.get('description', '')
                if description:
                    constraints_text += f'<li>{description}</li>'
            constraints_text += '</ul>'
            details_html.append(f'<div class="param-detail"><strong>Constraints:</strong>{constraints_text}</div>')
        
        if param_remarks:
            details_html.append(f'<div class="param-detail"><strong>Remarks:</strong> {param_remarks}</div>')
        
        if param_props:
            props_text = '<ul>'
            for prop in param_props:
                prop_name = prop.get('name', 'N/A')
                prop_value = prop.get('value', 'N/A')
                props_text += f'<li><strong>{prop_name}:</strong> {prop_value}</li>'
            props_text += '</ul>'
            details_html.append(f'<div class="param-detail"><strong>Properties:</strong>{props_text}</div>')
        
        if param_links:
            links_text = '<ul>'
            for link in param_links:
                href = link.get('href', '#')
                text = link.get('text', href)
                links_text += f'<li><a href="{href}" target="_blank">{text}</a></li>'
            links_text += '</ul>'
            details_html.append(f'<div class="param-detail"><strong>Links:</strong>{links_text}</div>')
        
        details_content = ''.join(details_html) if details_html else '<p class="no-content">No additional details</p>'
        
        return f'''
        <div class="param-item">
            <div class="param-header" onclick="toggleElement('param-{parent_id}-{param_idx}', 'icon-param-{parent_id}-{param_idx}')">
                <span class="toggle-icon" id="icon-param-{parent_id}-{param_idx}">▶</span>
                <span class="param-summary">{param_summary}</span>
            </div>
            <div class="param-details" id="param-{parent_id}-{param_idx}" style="display: none;">
                {details_content}
            </div>
        </div>
        '''
    
    # Helper function to recursively render parts with nested structure
    def render_parts_recursive(parts, depth=0):
        """Recursively render parts and their nested sub-parts"""
        if not parts:
            return ''
        
        parts_html = []
        for part in parts:
            part_id = part.get('id', 'N/A')
            part_name = part.get('name', 'unknown')
            part_title = part.get('title', '')
            part_prose = part.get('prose', '')
            part_props = part.get('props', [])
            nested_parts = part.get('parts', [])
            
            # Get label from props if available
            label = ''
            for prop in part_props:
                if prop.get('name') == 'label':
                    label = prop.get('value', '')
                    break
            
            # Build part header
            part_header = f'{part_name.replace("-", " ").title()}'
            if label:
                part_header += f' {label}'
            if part_title:
                part_header += f': {part_title}'
            
            # Render nested parts recursively
            nested_html = render_parts_recursive(nested_parts, depth + 1)
            
            # Only render if there's prose or nested content
            if part_prose or nested_html:
                indent_style = f'margin-left: {depth * 20}px;' if depth > 0 else ''
                parts_html.append(f'''
                <div class="part" style="{indent_style}">
                    <strong>{part_header}</strong>
                    {f'<div class="prose">{part_prose}</div>' if part_prose else ''}
                    {nested_html}
                </div>
                ''')
        
        return ''.join(parts_html)
    
    # Helper function to recursively render controls (including sub-controls/enhancements)
    def render_control_recursive(control, level, parent_id, ctrl_idx):
        """Recursively render a control and its sub-controls"""
        control_id = control.get('id', 'N/A')
        control_title = control.get('title', 'No title')
        control_class = control.get('class', 'N/A')
        
        # Get ALL parts (statement, guidance, etc.) and render recursively
        parts = control.get('parts', [])
        parts_html = render_parts_recursive(parts)
        
        # Get ALL parameters with expandable details
        params = control.get('params', [])
        params_html = ''
        if params:
            params_html = '<div class="params-section"><strong>Parameters:</strong>'
            for param_idx, param in enumerate(params):
                params_html += render_parameter(param, param_idx, f'{parent_id}-{ctrl_idx}')
            params_html += '</div>'
        
        # Get properties
        props = control.get('props', [])
        props_html = ''
        if props:
            props_html = '<div class="props-section"><strong>Properties:</strong><ul>'
            for prop in props:
                prop_name = prop.get('name', 'N/A')
                prop_value = prop.get('value', 'N/A')
                props_html += f'<li><strong>{prop_name}:</strong> {prop_value}</li>'
            props_html += '</ul></div>'
        
        # Recursively render sub-controls (enhancements)
        sub_controls = control.get('controls', [])
        sub_controls_html = ''
        if sub_controls:
            sub_controls_list = []
            for sub_idx, sub_control in enumerate(sub_controls):
                sub_controls_list.append(render_control_recursive(sub_control, level + 1, f'{parent_id}-{ctrl_idx}', sub_idx))
            sub_controls_html = f'<div class="sub-controls level-{level + 1}">{"".join(sub_controls_list)}</div>'
        
        level_class = f'level-{level}'
        control_html = f'''
        <div class="control-item {level_class}">
            <div class="control-header" onclick="toggleElement('ctrl-{parent_id}-{ctrl_idx}', 'icon-ctrl-{parent_id}-{ctrl_idx}')">
                <span class="toggle-icon" id="icon-ctrl-{parent_id}-{ctrl_idx}">▶</span>
                <span class="control-id-badge">{control_id}</span>
                <span class="control-title-text">{control_title}</span>
                <span class="control-class">{control_class}</span>
            </div>
            <div class="control-details" id="ctrl-{parent_id}-{ctrl_idx}" style="display: none;">
                {parts_html if parts_html else '<p class="no-content">No statement available</p>'}
                {params_html}
                {props_html}
                {sub_controls_html}
            </div>
        </div>
        '''
        return control_html
    
    # Helper function to recursively render groups (including sub-groups)
    def render_group_recursive(group, level, parent_id, group_idx):
        """Recursively render a group and its sub-groups"""
        group_id = group.get('id', 'N/A')
        group_title = group.get('title', 'Unknown')
        controls = group.get('controls', [])
        sub_groups = group.get('groups', [])
        
        # Get group-level parts (e.g., recitals, citations, etc.) and render recursively
        parts = group.get('parts', [])
        parts_html = ''
        if parts:
            parts_html = '<div class="group-parts-section">' + render_parts_recursive(parts) + '</div>'
        
        # Generate controls HTML
        controls_html = []
        for ctrl_idx, control in enumerate(controls):
            controls_html.append(render_control_recursive(control, 1, f'g{group_idx}', ctrl_idx))
        
        # Recursively generate sub-groups HTML
        sub_groups_html = []
        for sub_idx, sub_group in enumerate(sub_groups):
            sub_groups_html.append(render_group_recursive(sub_group, level + 1, f'{parent_id}-{group_idx}', sub_idx))
        
        level_class = f'level-{level}'
        parts_count = f", {len(parts)} parts" if parts else ""
        group_html = f'''
        <div class="group-item {level_class}">
            <div class="group-header" onclick="toggleElement('group-{parent_id}-{group_idx}', 'icon-group-{parent_id}-{group_idx}')">
                <span class="toggle-icon" id="icon-group-{parent_id}-{group_idx}">▶</span>
                <span class="group-id-badge">{group_id}</span>
                <span class="group-title-text">{group_title}</span>
                <span class="control-count">({len(controls)} controls{f", {len(sub_groups)} sub-groups" if sub_groups else ""}{parts_count})</span>
            </div>
            <div class="group-controls" id="group-{parent_id}-{group_idx}" style="display: none;">
                {parts_html}
                {''.join(controls_html)}
                {''.join(sub_groups_html)}
            </div>
        </div>
        '''
        return group_html
    
    # Count total controls (including sub-controls and controls in sub-groups)
    def count_controls_recursive(controls):
        count = len(controls)
        for control in controls:
            sub_controls = control.get('controls', [])
            if sub_controls:
                count += count_controls_recursive(sub_controls)
        return count
    
    def count_group_controls_recursive(group):
        """Count all controls in a group and its sub-groups"""
        count = count_controls_recursive(group.get('controls', []))
        sub_groups = group.get('groups', [])
        for sub_group in sub_groups:
            count += count_group_controls_recursive(sub_group)
        return count
    
    total_controls = 0
    for group in groups:
        total_controls += count_group_controls_recursive(group)
    
    # Generate all groups HTML
    groups_html = []
    for group_idx, group in enumerate(groups):
        groups_html.append(render_group_recursive(group, 0, 'root', group_idx))
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{metadata.get('title', catalog_name)}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }}
            .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a202c; margin-bottom: 10px; border-bottom: 3px solid #3182ce; padding-bottom: 15px; }}
            .back {{ display: inline-block; margin-bottom: 20px; padding: 10px 20px; background: #718096; color: white; text-decoration: none; border-radius: 6px; transition: background 0.2s; }}
            .back:hover {{ background: #4a5568; }}
            .info {{ background: #edf2f7; padding: 25px; border-radius: 8px; margin: 25px 0; border-left: 5px solid #3182ce; }}
            .info p {{ margin: 8px 0; color: #2d3748; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 25px 0; }}
            .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-box h3 {{ margin: 0; font-size: 36px; }}
            .stat-box p {{ margin: 5px 0 0 0; opacity: 0.9; }}
            
            /* Group styles */
            .group-item {{ background: #ffffff; border: 1px solid #e2e8f0; margin: 15px 0; border-radius: 8px; overflow: hidden; }}
            .group-header {{ padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; cursor: pointer; display: flex; align-items: center; gap: 15px; transition: background 0.2s; }}
            .group-header:hover {{ background: linear-gradient(135deg, #5568d3 0%, #653a8b 100%); }}
            .group-id-badge {{ background: rgba(255,255,255,0.3); padding: 6px 14px; border-radius: 6px; font-weight: bold; font-size: 14px; }}
            .group-title-text {{ flex: 1; font-size: 18px; font-weight: 600; }}
            .control-count {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 4px; font-size: 13px; }}
            .group-controls {{ padding: 0; }}
            
            /* Control styles */
            .control-item {{ border-bottom: 1px solid #e2e8f0; }}
            .control-item:last-child {{ border-bottom: none; }}
            .control-header {{ padding: 15px 20px; background: #f7fafc; cursor: pointer; display: flex; align-items: center; gap: 12px; transition: background 0.2s; }}
            .control-header:hover {{ background: #edf2f7; }}
            .control-id-badge {{ background: #4299e1; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold; font-size: 13px; min-width: 80px; text-align: center; }}
            .control-title-text {{ flex: 1; color: #2d3748; font-weight: 500; }}
            .control-class {{ background: #e2e8f0; color: #4a5568; padding: 3px 10px; border-radius: 4px; font-size: 12px; }}
            .control-details {{ padding: 20px; background: white; border-top: 1px solid #e2e8f0; }}
            
            /* Control content styles */
            .part {{ margin: 15px 0; padding: 15px; background: #f7fafc; border-left: 4px solid #4299e1; border-radius: 4px; }}
            .part strong {{ color: #2c5282; display: block; margin-bottom: 8px; text-transform: capitalize; }}
            .prose {{ color: #4a5568; line-height: 1.7; }}
            
            /* Group parts section styles */
            .group-parts-section {{ margin: 15px 20px; padding: 20px; background: #fffaf0; border: 2px solid #ed8936; border-radius: 8px; }}
            .group-parts-section .part {{ background: #fff; border-left: 4px solid #ed8936; }}
            .group-parts-section .part strong {{ color: #c05621; }}
            .params-section {{ margin: 15px 0; padding: 15px; background: #fff5f5; border-left: 4px solid #fc8181; border-radius: 4px; }}
            .params-section strong {{ color: #742a2a; display: block; margin-bottom: 8px; }}
            .params-section ul {{ margin: 8px 0; padding-left: 20px; }}
            .params-section li {{ color: #742a2a; margin: 6px 0; line-height: 1.6; }}
            .params-section code {{ background: #fed7d7; padding: 2px 8px; border-radius: 3px; font-size: 13px; font-weight: 600; }}
            .props-section {{ margin: 15px 0; padding: 15px; background: #f0fff4; border-left: 4px solid #48bb78; border-radius: 4px; }}
            .props-section strong {{ color: #22543d; display: block; margin-bottom: 8px; }}
            .props-section ul {{ margin: 8px 0; padding-left: 20px; }}
            .props-section li {{ color: #22543d; margin: 6px 0; }}
            .no-content {{ color: #a0aec0; font-style: italic; }}
            
            /* Parameter expandable styles */
            .param-item {{ margin: 10px 0; border: 1px solid #feb2b2; border-radius: 6px; overflow: hidden; }}
            .param-header {{ padding: 10px 15px; background: #fff5f5; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: background 0.2s; }}
            .param-header:hover {{ background: #fed7d7; }}
            .param-summary {{ flex: 1; color: #742a2a; font-size: 14px; }}
            .param-summary code {{ background: #fed7d7; padding: 2px 8px; border-radius: 3px; font-weight: 600; }}
            .param-badge {{ background: #fc8181; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-left: 5px; }}
            .param-details {{ padding: 15px; background: white; border-top: 1px solid #feb2b2; }}
            .param-detail {{ margin: 10px 0; padding: 10px; background: #fffaf0; border-left: 3px solid #fc8181; border-radius: 4px; }}
            .param-detail strong {{ color: #742a2a; display: block; margin-bottom: 5px; }}
            .param-detail ul {{ margin: 5px 0; padding-left: 20px; }}
            .param-detail li {{ color: #4a5568; margin: 3px 0; }}
            
            /* Sub-controls styles */
            .sub-controls {{ margin-top: 15px; padding-left: 20px; border-left: 3px solid #cbd5e0; }}
            .level-0 {{ /* Top level groups */ }}
            .level-1 {{ margin-left: 0; }}
            .level-2 {{ margin-left: 20px; }}
            .level-3 {{ margin-left: 40px; }}
            .level-4 {{ margin-left: 60px; }}
            
            /* Toggle icon */
            .toggle-icon {{ font-size: 14px; transition: transform 0.2s; display: inline-block; width: 20px; }}
            .toggle-icon.expanded {{ transform: rotate(90deg); }}
            
            /* Buttons */
            .expand-all-btn {{ display: inline-block; margin: 15px 10px 15px 0; padding: 10px 20px; background: #4299e1; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; transition: background 0.2s; }}
            .expand-all-btn:hover {{ background: #3182ce; }}
            .api-link {{ display: inline-block; margin: 25px 0; padding: 12px 24px; background: #48bb78; color: white; text-decoration: none; border-radius: 6px; transition: background 0.2s; }}
            .api-link:hover {{ background: #38a169; }}
        </style>
        <script>
            function toggleElement(elementId, iconId) {{
                const element = document.getElementById(elementId);
                const icon = document.getElementById(iconId);
                if (element.style.display === 'none') {{
                    element.style.display = 'block';
                    icon.classList.add('expanded');
                }} else {{
                    element.style.display = 'none';
                    icon.classList.remove('expanded');
                }}
            }}
            
            function expandAll() {{
                const groups = document.querySelectorAll('.group-controls');
                const controls = document.querySelectorAll('.control-details');
                const params = document.querySelectorAll('.param-details');
                const subControls = document.querySelectorAll('.sub-controls');
                const icons = document.querySelectorAll('.toggle-icon');
                
                groups.forEach(g => g.style.display = 'block');
                controls.forEach(c => c.style.display = 'block');
                params.forEach(p => p.style.display = 'block');
                subControls.forEach(s => s.style.display = 'block');
                icons.forEach(i => i.classList.add('expanded'));
            }}
            
            function collapseAll() {{
                const groups = document.querySelectorAll('.group-controls');
                const controls = document.querySelectorAll('.control-details');
                const params = document.querySelectorAll('.param-details');
                const subControls = document.querySelectorAll('.sub-controls');
                const icons = document.querySelectorAll('.toggle-icon');
                
                groups.forEach(g => g.style.display = 'none');
                controls.forEach(c => c.style.display = 'none');
                params.forEach(p => p.style.display = 'none');
                subControls.forEach(s => s.style.display = 'none');
                icons.forEach(i => i.classList.remove('expanded'));
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <a href="/" class="back">← Back to Home</a>
                <a href="/api/catalog/{catalog_name}" class="back">📄 Display JSON</a>
            </div>
            <h1>📖 {metadata.get('title', catalog_name)}</h1>
            
            <div class="info">
                <p><strong>UUID:</strong> {catalog_data.get('uuid', 'N/A')}</p>
                <p><strong>Version:</strong> {metadata.get('version', 'N/A')}</p>
                <p><strong>Last Modified:</strong> {metadata.get('last-modified', 'N/A')}</p>
                <p><strong>OSCAL Version:</strong> {metadata.get('oscal-version', 'N/A')}</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>{len(groups)}</h3>
                    <p>Control Groups</p>
                </div>
                <div class="stat-box">
                    <h3>{total_controls}</h3>
                    <p>Total Controls</p>
                </div>
            </div>
            
            <div style="margin: 25px 0;">
                <button class="expand-all-btn" onclick="expandAll()">▼ Expand All</button>
                <button class="expand-all-btn" onclick="collapseAll()">▲ Collapse All</button>
            </div>
            
            <h2>Control Groups and Controls</h2>
            <p style="color: #718096; margin-bottom: 20px;">
                Click on any group, control, or parameter to expand/collapse.
                Supports nested sub-groups and sub-controls (enhancements).
                All data visible with no truncation.
            </p>
            
            {''.join(groups_html)}
        </div>
    </body>
    </html>
    """

@app.route('/profile/<profile_name>')
def profile(profile_name):
    """View specific profile structure"""
    data = load_profile(profile_name)
    if not data:
        return f"Profile '{profile_name}' not found", 404
    
    profile_data = data.get('profile', {})
    metadata = profile_data.get('metadata', {})
    # Default: Show profile structure
    imports = profile_data.get('imports', [])
    merge = profile_data.get('merge', {})
    modify = profile_data.get('modify', {})
    
    # Count total controls
    total_included = 0
    total_excluded = 0
    
    # Extract import details with expandable control lists
    imports_html = []
    for imp_idx, imp in enumerate(imports):
        href = imp.get('href', 'N/A')
        include_all = imp.get('include-all', {})
        include_controls = imp.get('include-controls', [])
        exclude_controls = imp.get('exclude-controls', [])
        
        # Build included controls list
        included_html = ''
        if include_controls:
            # Count total controls (handle both with-id and with-ids)
            control_ids = []
            for ctrl in include_controls:
                # Check for with-ids (array of IDs)
                if 'with-ids' in ctrl:
                    control_ids.extend(ctrl.get('with-ids', []))
                # Check for with-id (single ID)
                elif 'with-id' in ctrl:
                    control_ids.append(ctrl.get('with-id'))
            
            total_included += len(control_ids)
            
            if control_ids:
                included_html = f'''
                <div class="control-list-header" onclick="toggleElement('inc-{imp_idx}', 'icon-inc-{imp_idx}')">
                    <span class="toggle-icon" id="icon-inc-{imp_idx}">▶</span>
                    <span class="badge-clickable">Includes: {len(control_ids)} control(s) - Click to expand</span>
                </div>
                <div class="control-list" id="inc-{imp_idx}" style="display: none;">
                    <ul>
                '''
                for ctrl_id in control_ids:
                    # Check if it's an enhancement (has a dot or parenthesis)
                    is_enhancement = '.' in ctrl_id or '(' in ctrl_id
                    child_badge = ' <span class="mini-badge">enhancement</span>' if is_enhancement else ''
                    included_html += f'<li><code>{ctrl_id}</code>{child_badge}</li>'
                included_html += '</ul></div>'
        
        # Build excluded controls list
        excluded_html = ''
        if exclude_controls:
            # Count total controls (handle both with-id and with-ids)
            excluded_ids = []
            for ctrl in exclude_controls:
                # Check for with-ids (array of IDs)
                if 'with-ids' in ctrl:
                    excluded_ids.extend(ctrl.get('with-ids', []))
                # Check for with-id (single ID)
                elif 'with-id' in ctrl:
                    excluded_ids.append(ctrl.get('with-id'))
            
            total_excluded += len(excluded_ids)
            
            if excluded_ids:
                excluded_html = f'''
                <div class="control-list-header" onclick="toggleElement('exc-{imp_idx}', 'icon-exc-{imp_idx}')">
                    <span class="toggle-icon" id="icon-exc-{imp_idx}">▶</span>
                    <span class="badge-clickable">Excludes: {len(excluded_ids)} control(s) - Click to expand</span>
                </div>
                <div class="control-list" id="exc-{imp_idx}" style="display: none;">
                    <ul>
                '''
                for ctrl_id in excluded_ids:
                    # Check if it's an enhancement (has a dot or parenthesis)
                    is_enhancement = '.' in ctrl_id or '(' in ctrl_id
                    child_badge = ' <span class="mini-badge">enhancement</span>' if is_enhancement else ''
                    excluded_html += f'<li><code>{ctrl_id}</code>{child_badge}</li>'
                excluded_html += '</ul></div>'
        
        import_detail = f'''
        <div class="import-item">
            <strong>Import:</strong> {href}
            {f'<br><span class="badge">Include All Controls</span>' if include_all else ''}
            {included_html}
            {excluded_html}
        </div>
        '''
        imports_html.append(import_detail)
    
    # Extract modifications
    set_parameters = modify.get('set-parameters', [])
    alters = modify.get('alters', [])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{metadata.get('title', profile_name)}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }}
            .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a202c; margin-bottom: 10px; border-bottom: 3px solid #9f7aea; padding-bottom: 15px; }}
            h2 {{ color: #2d3748; margin-top: 30px; }}
            .back {{ display: inline-block; margin-bottom: 20px; padding: 10px 20px; background: #718096; color: white; text-decoration: none; border-radius: 6px; transition: background 0.2s; }}
            .back:hover {{ background: #4a5568; }}
            .view-toggle {{ display: inline-block; margin-bottom: 20px; margin-left: 10px; padding: 10px 20px; background: #48bb78; color: white; text-decoration: none; border-radius: 6px; transition: background 0.2s; }}
            .view-toggle:hover {{ background: #38a169; }}
            .info {{ background: #faf5ff; padding: 25px; border-radius: 8px; margin: 25px 0; border-left: 5px solid #9f7aea; }}
            .info p {{ margin: 8px 0; color: #2d3748; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 25px 0; }}
            .stat-box {{ background: linear-gradient(135deg, #9f7aea 0%, #805ad5 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-box h3 {{ margin: 0; font-size: 36px; }}
            .stat-box p {{ margin: 5px 0 0 0; opacity: 0.9; }}
            .import-item {{ background: #edf2f7; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 4px solid #4299e1; }}
            .badge {{ display: inline-block; background: #4299e1; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; margin: 5px 5px 0 0; }}
            .badge-clickable {{ display: inline-block; background: #4299e1; color: white; padding: 6px 12px; border-radius: 4px; font-size: 13px; margin: 8px 0; cursor: pointer; transition: background 0.2s; }}
            .badge-clickable:hover {{ background: #3182ce; }}
            .control-list-header {{ display: flex; align-items: center; gap: 10px; margin: 8px 0; cursor: pointer; }}
            .control-list {{ margin: 10px 0 10px 30px; padding: 10px; background: white; border-radius: 4px; border-left: 3px solid #4299e1; }}
            .control-list ul {{ margin: 5px 0; padding-left: 20px; list-style: none; }}
            .control-list li {{ margin: 5px 0; padding: 5px; background: #f7fafc; border-radius: 3px; }}
            .control-list code {{ background: #e2e8f0; padding: 3px 8px; border-radius: 3px; font-weight: 600; color: #2d3748; }}
            .mini-badge {{ display: inline-block; background: #fc8181; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-left: 5px; }}
            .toggle-icon {{ font-size: 14px; transition: transform 0.2s; display: inline-block; width: 20px; }}
            .toggle-icon.expanded {{ transform: rotate(90deg); }}
            .section {{ background: #f7fafc; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #9f7aea; }}
            .api-link {{ display: inline-block; margin: 25px 10px 25px 0; padding: 12px 24px; background: #48bb78; color: white; text-decoration: none; border-radius: 6px; transition: background 0.2s; }}
            .api-link:hover {{ background: #38a169; }}
            pre {{ background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px; }}
        </style>
        <script>
            function toggleElement(elementId, iconId) {{
                const element = document.getElementById(elementId);
                const icon = document.getElementById(iconId);
                if (element.style.display === 'none') {{
                    element.style.display = 'block';
                    icon.classList.add('expanded');
                }} else {{
                    element.style.display = 'none';
                    icon.classList.remove('expanded');
                }}
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <a href="/" class="back">← Back to Home</a>
                <div>
                    <a href="/api/profile/{profile_name}" class="back" style="margin-right: 10px;">📄 Display JSON</a>
                    <a href="/profile/{profile_name}/resolved" class="back">📖 View Resolved</a>
                </div>
            </div>
            <h1>📋 {metadata.get('title', profile_name)}</h1>
            
            <div class="info">
                <p><strong>UUID:</strong> {profile_data.get('uuid', 'N/A')}</p>
                <p><strong>Version:</strong> {metadata.get('version', 'N/A')}</p>
                <p><strong>Last Modified:</strong> {metadata.get('last-modified', 'N/A')}</p>
                <p><strong>OSCAL Version:</strong> {metadata.get('oscal-version', 'N/A')}</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>{total_included if total_included > 0 else 'All'}</h3>
                    <p>Included Controls</p>
                </div>
                <div class="stat-box">
                    <h3>{total_excluded}</h3>
                    <p>Excluded Controls</p>
                </div>
                <div class="stat-box">
                    <h3>{len(set_parameters)}</h3>
                    <p>Set Parameters</p>
                </div>
                <div class="stat-box">
                    <h3>{len(alters)}</h3>
                    <p>Alterations</p>
                </div>
            </div>
            
            <h2>📥 Imports & Control Selection</h2>
            <p style="color: #718096;">Catalogs and controls imported by this profile. Click badges to expand control lists:</p>
            {''.join(imports_html) if imports_html else '<p style="color: #a0aec0; font-style: italic;">No imports defined</p>'}
            
            <h2>🔧 Modifications</h2>
            <div class="section">
                <p><strong>Set Parameters:</strong> {len(set_parameters)} parameter(s) configured</p>
                <p><strong>Alterations:</strong> {len(alters)} control alteration(s) defined</p>
            </div>
            
            <h2>🔀 Merge Strategy</h2>
            <div class="section">
                <pre>{json.dumps(merge, indent=2) if merge else 'No merge strategy defined'}</pre>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/api/catalogs')
def api_catalogs():
    """API: List all catalogs"""
    return jsonify(get_catalogs())

@app.route('/api/profiles')
def api_profiles():
    """API: List all profiles"""
    return jsonify(get_profiles())

@app.route('/api/catalog/<catalog_name>')
def api_catalog(catalog_name):
    """API: Get specific catalog"""
    json_file = trestle_api.load_catalog_json_file(catalog_name)
    if json_file and json_file.exists():
        with open(json_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Catalog not found'}), 404

@app.route('/api/profile/<profile_name>')
def api_profile(profile_name):
    """API: Get specific profile"""
    json_file = trestle_api.load_profile_json_file(profile_name)
    if json_file and json_file.exists():
        with open(json_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/components')
def api_components():
    """API: List all component definitions"""
    return jsonify(get_components())

@app.route('/api/component/<component_name>')
def api_component(component_name):
    """API: Get specific component definition"""
    json_file = trestle_api.load_component_json_file(component_name)
    if json_file and json_file.exists():
        with open(json_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Component not found'}), 404

@app.route('/api/ssps')
def api_ssps():
    """API: List all system security plans"""
    return jsonify(get_ssps())

@app.route('/api/ssp/<ssp_name>')
def api_ssp(ssp_name):
    """API: Get specific system security plan"""
    json_file = trestle_api.load_ssp_json_file(ssp_name)
    if json_file and json_file.exists():
        with open(json_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'SSP not found'}), 404

@app.route('/api/assessment-plans')
def api_assessment_plans():
    """API: List all assessment plans"""
    return jsonify(trestle_api.list_assessment_plans())

@app.route('/api/assessment-plan/<plan_name>')
def api_assessment_plan_json(plan_name):
    """API: Get specific assessment plan"""
    json_file = trestle_api.load_assessment_plan_json_file(plan_name)
    if json_file and json_file.exists():
        with open(json_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Assessment plan not found'}), 404

@app.route('/xccdf-result/<result_name>')
def xccdf_result(result_name):
    """Display XCCDF scan result"""
    xml_file = Path('source-data/xccdf-results') / f'{result_name}-xccdf-results.xml'
    
    if not xml_file.exists():
        return f"<h1>XCCDF Result Not Found</h1><p>File: {xml_file}</p>", 404
    
    # Parse XML to extract key information
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Define namespace
        ns = {'cdf': 'http://checklists.nist.gov/xccdf/1.2'}
        
        # Extract test result info
        test_result = root.find('.//cdf:TestResult', ns)
        if test_result is None:
            return "<h1>Error</h1><p>No TestResult found in XCCDF file</p>", 500
        
        title = test_result.find('cdf:title', ns).text if test_result.find('cdf:title', ns) is not None else 'XCCDF Scan Result'
        target = test_result.find('cdf:target', ns).text if test_result.find('cdf:target', ns) is not None else 'Unknown'
        target_address = test_result.find('cdf:target-address', ns).text if test_result.find('cdf:target-address', ns) is not None else 'N/A'
        start_time = test_result.get('start-time', 'N/A')
        end_time = test_result.get('end-time', 'N/A')
        
        # Extract score
        score_elem = test_result.find('cdf:score', ns)
        score = float(score_elem.text) if score_elem is not None else 0.0
        
        # Extract target facts
        facts = {}
        for fact in test_result.findall('.//cdf:fact', ns):
            fact_name = fact.get('name', '').split(':')[-1]
            facts[fact_name] = fact.text
        
        # Extract rule results
        rule_results = []
        for rule_result in test_result.findall('cdf:rule-result', ns):
            rule_id = rule_result.get('idref', '').split('_rule_')[-1]
            result_elem = rule_result.find('cdf:result', ns)
            result = result_elem.text if result_elem is not None else 'unknown'
            severity = rule_result.get('severity', 'unknown')
            
            # Get message if failed
            message = ''
            msg_elem = rule_result.find('cdf:message', ns)
            if msg_elem is not None:
                message = msg_elem.text
            
            rule_results.append({
                'id': rule_id,
                'result': result,
                'severity': severity,
                'message': message
            })
        
        # Count results
        pass_count = sum(1 for r in rule_results if r['result'] == 'pass')
        fail_count = sum(1 for r in rule_results if r['result'] == 'fail')
        other_count = len(rule_results) - pass_count - fail_count
        
    except Exception as e:
        return f"<h1>Error Parsing XCCDF</h1><p>{str(e)}</p>", 500
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .back {{ display: inline-block; margin-bottom: 20px; padding: 8px 16px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
            .back:hover {{ background: #2980b9; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .info {{ background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
            .stat-box {{ background: #e8f4f8; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-box h3 {{ margin: 0; font-size: 2em; color: #2980b9; }}
            .stat-box p {{ margin: 10px 0 0 0; color: #7f8c8d; }}
            .score {{ font-size: 3em; font-weight: bold; color: {'#27ae60' if score >= 80 else '#e67e22' if score >= 60 else '#e74c3c'}; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #34495e; color: white; }}
            tr:hover {{ background: #f5f5f5; }}
            .pass {{ color: #27ae60; font-weight: bold; }}
            .fail {{ color: #e74c3c; font-weight: bold; }}
            .notchecked {{ color: #95a5a6; }}
            .severity-high {{ background: #ffebee; }}
            .severity-medium {{ background: #fff3e0; }}
            .severity-low {{ background: #e8f5e9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <a href="/" class="back">← Back to Home</a>
                <a href="/xccdf-result/{result_name}/raw" class="back">📄 View Raw XML</a>
            </div>
            <h1>🔍 {title}</h1>
            
            <div class="info">
                <strong>Target System:</strong> {target}<br>
                <strong>IP Address:</strong> {target_address}<br>
                <strong>OS:</strong> {facts.get('os_name', 'N/A')} {facts.get('os_version', '')}<br>
                <strong>Scan Start:</strong> {start_time}<br>
                <strong>Scan End:</strong> {end_time}
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3 class="pass">{pass_count}</h3>
                    <p>Passed</p>
                </div>
                <div class="stat-box">
                    <h3 class="fail">{fail_count}</h3>
                    <p>Failed</p>
                </div>
                <div class="stat-box">
                    <h3>{other_count}</h3>
                    <p>Other</p>
                </div>
            </div>
            
            <h2>Rule Check Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rule ID</th>
                        <th>Result</th>
                        <th>Severity</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr class="severity-{r['severity']}">
                        <td><code>{r['id']}</code></td>
                        <td class="{r['result']}">{r['result'].upper()}</td>
                        <td>{r['severity'].upper()}</td>
                        <td>{r['message'] if r['message'] else '-'}</td>
                    </tr>
                    ''' for r in rule_results])}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

@app.route('/xccdf-result/<result_name>/raw')
def xccdf_result_raw(result_name):
    """Serve raw XCCDF XML file"""
    xml_file = Path('source-data/xccdf-results') / f'{result_name}-xccdf-results.xml'
    if xml_file.exists():
        with open(xml_file, 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/xml'}
    return "File not found", 404

@app.route('/health')
def health():
    """Health check endpoint"""
    catalogs = get_catalogs()
    profiles = get_profiles()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'trestle_workspace': str(TRESTLE_ROOT.absolute()),
        'catalogs_count': len(catalogs),
        'profiles_count': len(profiles),
        'catalogs': [c['name'] for c in catalogs],
        'profiles': [p['name'] for p in profiles]
    })
@app.route('/profile/<profile_name>/resolved')
def profile_resolved(profile_name):
    """Redirect to the resolved catalog for this profile"""
    resolved_catalog_name = f"resolved-{profile_name}"
    return redirect(f'/catalog/{resolved_catalog_name}')


@app.route('/component/<component_name>')
def component(component_name):
    """View specific component definition with control implementations"""
    data = trestle_api.load_component_dict(component_name)
    if not data:
        return f"Component definition '{component_name}' not found", 404
    
    comp_data = data.get('component-definition', {})
    metadata = comp_data.get('metadata', {})
    components = comp_data.get('components', [])
    
    # Load software component to get rule-to-control mapping for validation components
    rule_to_controls_map = {}
    software_data = trestle_api.load_component_dict('Ubuntu_Linux_24_04_LTS')
    if software_data:
        software_comps = software_data.get('component-definition', {}).get('components', [])
        for sw_comp in software_comps:
            for ctrl_impl in sw_comp.get('control-implementations', []):
                for req in ctrl_impl.get('implemented-requirements', []):
                    ctrl_id = req.get('control-id', '')
                    for prop in req.get('props', []):
                        if prop.get('name') == 'Rule_Id':
                            rule_id = prop.get('value', '')
                            if rule_id not in rule_to_controls_map:
                                rule_to_controls_map[rule_id] = []
                            if ctrl_id not in rule_to_controls_map[rule_id]:
                                rule_to_controls_map[rule_id].append(ctrl_id)
    
    # Build components HTML with control implementations
    components_html = []
    for comp in components:
        comp_title = comp.get('title', 'Unknown Component')
        comp_type = comp.get('type', 'N/A')
        comp_desc = comp.get('description', 'N/A')
        
        # Get control implementations first
        control_impls = comp.get('control-implementations', [])
        
        # Get rule/check properties
        props = comp.get('props', [])
        rules = {}
        for prop in props:
            prop_name = prop.get('name', '')
            if prop_name in ['Rule_Id', 'Check_Id']:
                rule_id = prop.get('value', '')
                remarks = prop.get('remarks', '')
                if remarks not in rules:
                    rules[remarks] = {'id': rule_id, 'description': '', 'check_id': '', 'target': ''}
                if prop_name == 'Rule_Id':
                    rules[remarks]['id'] = rule_id
                elif prop_name == 'Check_Id':
                    rules[remarks]['check_id'] = rule_id
        
        for prop in props:
            prop_name = prop.get('name', '')
            remarks = prop.get('remarks', '')
            if remarks in rules:
                if prop_name == 'Rule_Description':
                    rules[remarks]['description'] = prop.get('value', '')
                elif prop_name == 'Check_Description':
                    rules[remarks]['description'] = prop.get('value', '')
                elif prop_name == 'Target_Component':
                    rules[remarks]['target'] = prop.get('value', '')
        
        # Display rules/checks organized by control for validation components
        rules_html = ''
        if rules and comp_type == 'validation' and len(control_impls) == 0:
            # Group checks by control using the rule-to-control mapping
            controls_checks_map = {}
            for rule_data in rules.values():
                rule_id = rule_data.get('id', 'N/A')
                check_id = rule_data.get('check_id', '')
                target = rule_data.get('target', '')
                
                # Get controls for this rule
                controls = rule_to_controls_map.get(rule_id, ['unmapped'])
                for ctrl_id in controls:
                    if ctrl_id not in controls_checks_map:
                        controls_checks_map[ctrl_id] = []
                    controls_checks_map[ctrl_id].append({
                        'rule_id': rule_id,
                        'check_id': check_id,
                        'target': target
                    })
            
            # Build HTML organized by control
            controls_list_html = []
            for ctrl_id in sorted(controls_checks_map.keys()):
                checks = controls_checks_map[ctrl_id]
                checks_html = []
                for check in checks:
                    checks_html.append(f'''
                    <div class="rule-item">
                        <p><strong>Rule ID:</strong> <code>{check['rule_id']}</code></p>
                        {f"<p><strong>Check ID:</strong> <code>{check['check_id']}</code></p>" if check['check_id'] else ''}
                        {f"<p><strong>Target:</strong> {check['target']}</p>" if check['target'] else ''}
                    </div>
                    ''')
                
                controls_list_html.append(f'''
                <div class="control-impl">
                    <div class="control-impl-header" onclick="toggleElement('val-ctrl-{ctrl_id.replace(".", "-")}', 'icon-val-ctrl-{ctrl_id.replace(".", "-")}')">
                        <span class="toggle-icon" id="icon-val-ctrl-{ctrl_id.replace(".", "-")}">▶</span>
                        <span class="control-id-badge">{ctrl_id.upper()}</span>
                        <span class="rule-count">({len(checks)} checks)</span>
                    </div>
                    <div class="control-impl-details" id="val-ctrl-{ctrl_id.replace(".", "-")}" style="display: none;">
                        <div class="rules-list">
                            {''.join(checks_html)}
                        </div>
                    </div>
                </div>
                ''')
            
            rules_html = f'''
            <div class="control-implementation">
                <h4>Validation Checks by Control</h4>
                <p><strong>Total Checks:</strong> {len(rules)}</p>
                <p><strong>Controls Covered:</strong> {len(controls_checks_map)}</p>
                <div class="controls-list">
                    {''.join(controls_list_html)}
                </div>
            </div>
            '''
        
        # Build control implementations HTML (already have control_impls from above)
        control_impls_html = []
        
        for ctrl_impl in control_impls:
            source = ctrl_impl.get('source', 'N/A')
            description = ctrl_impl.get('description', 'N/A')
            impl_reqs = ctrl_impl.get('implemented-requirements', [])
            
            # Group by control-id
            controls_map = {}
            for req in impl_reqs:
                ctrl_id = req.get('control-id', 'N/A')
                if ctrl_id not in controls_map:
                    controls_map[ctrl_id] = []
                
                # Get rule IDs for this control
                req_props = req.get('props', [])
                for prop in req_props:
                    if prop.get('name') == 'Rule_Id':
                        controls_map[ctrl_id].append(prop.get('value', ''))
            
            controls_list_html = []
            for ctrl_id, rule_ids in sorted(controls_map.items()):
                controls_list_html.append(f'''
                <div class="control-impl">
                    <div class="control-impl-header" onclick="toggleElement('ctrl-{ctrl_id.replace(".", "-")}', 'icon-ctrl-{ctrl_id.replace(".", "-")}')">
                        <span class="toggle-icon" id="icon-ctrl-{ctrl_id.replace(".", "-")}">▶</span>
                        <span class="control-id-badge">{ctrl_id.upper()}</span>
                        <span class="rule-count">({len(rule_ids)} rules)</span>
                    </div>
                    <div class="control-impl-details" id="ctrl-{ctrl_id.replace(".", "-")}" style="display: none;">
                        <ul class="rule-list">
                            {''.join([f'<li><code>{rule_id}</code></li>' for rule_id in rule_ids])}
                        </ul>
                    </div>
                </div>
                ''')
            
            control_impls_html.append(f'''
            <div class="control-implementation">
                <h4>Control Implementation</h4>
                <p><strong>Source:</strong> {source}</p>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Controls Implemented:</strong> {len(controls_map)}</p>
                <div class="controls-list">
                    {''.join(controls_list_html)}
                </div>
            </div>
            ''')
        
        components_html.append(f'''
        <div class="component-card">
            <h3>{'🔍' if comp_type == 'validation' else '🔧'} {comp_title}</h3>
            <p><strong>Type:</strong> {comp_type}</p>
            <p><strong>Description:</strong> {comp_desc}</p>
            <p><strong>{'Checks' if comp_type == 'validation' else 'Rules'} Defined:</strong> {len(rules)}</p>
            {rules_html}
            {''.join(control_impls_html)}
        </div>
        ''')
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{metadata.get('title', component_name)}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }}
            .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a202c; margin-bottom: 10px; border-bottom: 3px solid #3182ce; padding-bottom: 15px; }}
            .back {{ display: inline-block; margin-bottom: 20px; padding: 10px 20px; background: #718096; color: white; text-decoration: none; border-radius: 6px; transition: background 0.2s; }}
            .back:hover {{ background: #4a5568; }}
            .info {{ background: #edf2f7; padding: 25px; border-radius: 8px; margin: 25px 0; border-left: 5px solid #3182ce; }}
            .info p {{ margin: 8px 0; color: #2d3748; }}
            
            .component-card {{ background: #ffffff; border: 1px solid #e2e8f0; margin: 20px 0; padding: 25px; border-radius: 8px; }}
            .component-card h3 {{ color: #2d3748; margin-top: 0; }}
            
            .control-implementation {{ background: #f7fafc; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #4299e1; }}
            .control-implementation h4 {{ color: #2c5282; margin-top: 0; }}
            
            .controls-list {{ margin-top: 15px; }}
            .control-impl {{ background: white; border: 1px solid #e2e8f0; margin: 10px 0; border-radius: 6px; overflow: hidden; }}
            .control-impl-header {{ padding: 12px 15px; background: #edf2f7; cursor: pointer; display: flex; align-items: center; gap: 12px; transition: background 0.2s; }}
            .control-impl-header:hover {{ background: #e2e8f0; }}
            .control-id-badge {{ background: #4299e1; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold; font-size: 13px; }}
            .rule-count {{ color: #718096; font-size: 13px; }}
            .control-impl-details {{ padding: 15px; background: white; border-top: 1px solid #e2e8f0; }}
            
            .rule-list {{ list-style: none; padding: 0; margin: 0; }}
            .rule-list li {{ padding: 8px 12px; margin: 5px 0; background: #f7fafc; border-left: 3px solid #4299e1; border-radius: 4px; }}
            .rule-list code {{ color: #2d3748; font-family: 'Courier New', monospace; font-size: 13px; }}
            
            .rules-section {{ background: #fffaf0; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #ed8936; }}
            .rules-section h4 {{ color: #c05621; margin-top: 0; }}
            .rules-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; margin-top: 15px; }}
            .rule-item {{ background: white; padding: 15px; border-radius: 6px; border: 1px solid #fed7d7; }}
            .rule-item p {{ margin: 8px 0; }}
            .rule-item code {{ background: #fed7d7; padding: 2px 6px; border-radius: 3px; font-size: 12px; }}
            
            .toggle-icon {{ font-size: 14px; transition: transform 0.2s; display: inline-block; width: 20px; }}
            .toggle-icon.expanded {{ transform: rotate(90deg); }}
            
            .expand-all-btn {{ display: inline-block; margin: 15px 10px 15px 0; padding: 10px 20px; background: #4299e1; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; transition: background 0.2s; }}
            .expand-all-btn:hover {{ background: #3182ce; }}
        </style>
        <script>
            function toggleElement(elementId, iconId) {{
                const element = document.getElementById(elementId);
                const icon = document.getElementById(iconId);
                if (element.style.display === 'none') {{
                    element.style.display = 'block';
                    icon.classList.add('expanded');
                }} else {{
                    element.style.display = 'none';
                    icon.classList.remove('expanded');
                }}
            }}
            
            function expandAll() {{
                const details = document.querySelectorAll('.control-impl-details');
                const icons = document.querySelectorAll('.toggle-icon');
                details.forEach(d => d.style.display = 'block');
                icons.forEach(i => i.classList.add('expanded'));
            }}
            
            function collapseAll() {{
                const details = document.querySelectorAll('.control-impl-details');
                const icons = document.querySelectorAll('.toggle-icon');
                details.forEach(d => d.style.display = 'none');
                icons.forEach(i => i.classList.remove('expanded'));
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <a href="/" class="back">← Back to Home</a>
                <a href="/api/component/{component_name}" class="back">📄 Display JSON</a>
            </div>
            <h1>🔧 {metadata.get('title', component_name)}</h1>
            
            <div class="info">
                <p><strong>UUID:</strong> {comp_data.get('uuid', 'N/A')}</p>
                <p><strong>Version:</strong> {metadata.get('version', 'N/A')}</p>
                <p><strong>Last Modified:</strong> {metadata.get('last-modified', 'N/A')}</p>
                <p><strong>OSCAL Version:</strong> {metadata.get('oscal-version', 'N/A')}</p>
                <p><strong>Components:</strong> {len(components)}</p>
            </div>
            
            <div style="margin: 25px 0;">
                <button class="expand-all-btn" onclick="expandAll()">▼ Expand All</button>
                <button class="expand-all-btn" onclick="collapseAll()">▲ Collapse All</button>
            </div>
            
            <h2>Components and Control Implementations</h2>
            {''.join(components_html)}
        </div>
    </body>
    </html>
    """

@app.route('/ssp/<ssp_name>')
def ssp(ssp_name):
    """View specific SSP with control implementations"""
    data = trestle_api.load_ssp_dict(ssp_name)
    if not data:
        return f"SSP '{ssp_name}' not found", 404
    
    ssp_data = data.get('system-security-plan', {})
    metadata = ssp_data.get('metadata', {})
    system_chars = ssp_data.get('system-characteristics', {})
    system_impl = ssp_data.get('system-implementation', {})
    control_impl = ssp_data.get('control-implementation', {})
    
    import_profile = ssp_data.get('import-profile', {})
    regulation_href = import_profile.get('href', 'N/A')
    regulation_info = trestle_api.resolve_regulation_reference(
        regulation_href if regulation_href != 'N/A' else None
    )
    regulation = regulation_info.get('label', 'N/A')
    
    # Group controls by family
    implemented_reqs = control_impl.get('implemented-requirements', [])
    controls_by_family = {}
    for req in implemented_reqs:
        control_id = req.get('control-id', 'unknown')
        family = control_id.split('-')[0].upper() if '-' in control_id else 'OTHER'
        if family not in controls_by_family:
            controls_by_family[family] = []
        controls_by_family[family].append(req)
    
    # Build control families HTML
    families_html = []
    for family in sorted(controls_by_family.keys()):
        controls = controls_by_family[family]
        family_id = family.lower().replace(' ', '-')
        
        controls_list_html = []
        for ctrl in controls:
            ctrl_id = ctrl.get('control-id', 'N/A')
            ctrl_uuid = ctrl.get('uuid', '')
            statements = ctrl.get('statements', [])
            by_components = ctrl.get('by-components', [])
            
            # Build statements HTML
            statements_html = ''
            if statements:
                stmt_items = []
                for stmt in statements:
                    stmt_id = stmt.get('statement-id', 'N/A')
                    stmt_uuid = stmt.get('uuid', '')
                    stmt_desc = stmt.get('description', 'No description')
                    stmt_by_comps = stmt.get('by-components', [])
                    
                    comp_details = []
                    for comp in stmt_by_comps:
                        comp_uuid = comp.get('component-uuid', '')
                        comp_desc = comp.get('description', '')
                        if comp_desc:
                            comp_details.append(f'<div class="component-impl">{comp_desc}</div>')
                    
                    stmt_items.append(f'''
                    <div class="statement">
                        <div class="statement-id"><strong>Statement {stmt_id}:</strong></div>
                        <div class="statement-desc">{stmt_desc}</div>
                        {"".join(comp_details)}
                    </div>
                    ''')
                statements_html = "".join(stmt_items)
            
            # Build by-components HTML
            by_comp_html = ''
            if by_components:
                comp_items = []
                for comp in by_components:
                    comp_uuid = comp.get('component-uuid', '')
                    comp_desc = comp.get('description', '')
                    impl_status = comp.get('implementation-status', {}).get('state', 'N/A')
                    if comp_desc:
                        comp_items.append(f'''
                        <div class="component-impl">
                            <p><strong>Implementation Status:</strong> <span class="status-badge">{impl_status}</span></p>
                            <p>{comp_desc}</p>
                        </div>
                        ''')
                by_comp_html = "".join(comp_items)
            
            controls_list_html.append(f'''
            <div class="control-item">
                <div class="control-header" onclick="toggleElement('ctrl-{ctrl_id.replace(".", "-")}', 'icon-ctrl-{ctrl_id.replace(".", "-")}')">
                    <span class="toggle-icon" id="icon-ctrl-{ctrl_id.replace(".", "-")}">▶</span>
                    <span class="control-id-badge">{ctrl_id.upper()}</span>
                </div>
                <div id="ctrl-{ctrl_id.replace(".", "-")}" class="control-details" style="display: none;">
                    {statements_html}
                    {by_comp_html}
                </div>
            </div>
            ''')
        
        families_html.append(f'''
        <div class="family-section">
            <div class="family-header" onclick="toggleElement('family-{family_id}', 'icon-family-{family_id}')">
                <span class="toggle-icon" id="icon-family-{family_id}">▶</span>
                <h2>{family} Family ({len(controls)} controls)</h2>
            </div>
            <div id="family-{family_id}" class="family-controls" style="display: none;">
                {"".join(controls_list_html)}
            </div>
        </div>
        ''')
    
    # Get components info
    components = system_impl.get('components', [])
    components_html = []
    for comp in components:
        comp_title = comp.get('title', 'Unknown')
        comp_type = comp.get('type', 'N/A')
        comp_desc = comp.get('description', 'N/A')
        components_html.append(f'''
        <div class="component-info">
            <p><strong>{comp_title}</strong> ({comp_type})</p>
            <p>{comp_desc}</p>
        </div>
        ''')
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{metadata.get('title', ssp_name)}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; margin-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            .back {{ display: inline-block; margin-bottom: 20px; padding: 8px 16px; background: #95a5a6; color: white; text-decoration: none; border-radius: 4px; }}
            .back:hover {{ background: #7f8c8d; }}
            .info {{ background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .info p {{ margin: 8px 0; }}
            
            .family-section {{ margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
            .family-header {{ background: #3498db; color: white; padding: 15px; cursor: pointer; display: flex; align-items: center; }}
            .family-header:hover {{ background: #2980b9; }}
            .family-header h2 {{ margin: 0; font-size: 1.2em; }}
            .family-controls {{ padding: 15px; background: #f8f9fa; }}
            
            .control-item {{ margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; background: white; }}
            .control-header {{ padding: 12px; cursor: pointer; display: flex; align-items: center; background: #fff; }}
            .control-header:hover {{ background: #f8f9fa; }}
            .control-id-badge {{ background: #e74c3c; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold; margin-left: 10px; }}
            .control-details {{ padding: 15px; border-top: 1px solid #ddd; background: #fafafa; }}
            
            .statement {{ margin: 15px 0; padding: 10px; background: white; border-left: 3px solid #3498db; }}
            .statement-id {{ font-weight: bold; color: #2c3e50; margin-bottom: 5px; }}
            .statement-desc {{ margin: 10px 0; line-height: 1.6; }}
            
            .component-impl {{ margin: 10px 0; padding: 10px; background: #e8f4f8; border-left: 3px solid #16a085; }}
            .component-info {{ margin: 10px 0; padding: 10px; background: #fff3cd; border-left: 3px solid #ffc107; }}
            
            .status-badge {{ background: #27ae60; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.9em; }}
            
            .toggle-icon {{ display: inline-block; width: 20px; font-family: monospace; transition: transform 0.3s; }}
            .toggle-icon.expanded {{ transform: rotate(90deg); }}
            
            .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
            .stat-box {{ flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-number {{ font-size: 2em; font-weight: bold; }}
            .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
        </style>
        <script>
            function toggleElement(elementId, iconId) {{
                const element = document.getElementById(elementId);
                const icon = document.getElementById(iconId);
                if (element.style.display === 'none') {{
                    element.style.display = 'block';
                    icon.classList.add('expanded');
                }} else {{
                    element.style.display = 'none';
                    icon.classList.remove('expanded');
                }}
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <a href="/" class="back">← Back to Home</a>
                <a href="/api/ssp/{ssp_name}" class="back">📄 Display JSON</a>
            </div>
            <h1>📄 {metadata.get('title', ssp_name)}</h1>
            
            <div class="info">
                <p><strong>System Name:</strong> {system_chars.get('system-name', 'N/A')}</p>
                <p><strong>System ID:</strong> {system_chars.get('system-ids', [{}])[0].get('id', 'N/A')}</p>
                <p><strong>Regulation:</strong> {regulation}</p>
                <p><strong>Source Title:</strong> {regulation_info.get('title', 'N/A')}</p>
                <p><strong>Source Version:</strong> {regulation_info.get('version', 'N/A')}</p>
                <p><strong>Catalog/Profile Reference:</strong> <code>{regulation_href}</code></p>
                <p><strong>Description:</strong> {system_chars.get('description', 'N/A')}</p>
                <p><strong>Status:</strong> {system_chars.get('status', {}).get('state', 'N/A')}</p>
                <p><strong>Version:</strong> {metadata.get('version', 'N/A')}</p>
                <p><strong>Last Modified:</strong> {metadata.get('last-modified', 'N/A')}</p>
                <p><strong>OSCAL Version:</strong> {metadata.get('oscal-version', 'N/A')}</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{len(implemented_reqs)}</div>
                    <div class="stat-label">Implemented Controls</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(controls_by_family)}</div>
                    <div class="stat-label">Control Families</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(components)}</div>
                    <div class="stat-label">Components</div>
                </div>
            </div>
            
            <h2>System Components</h2>
            <div>
                {"".join(components_html) if components_html else '<p>No components defined</p>'}
            </div>
            
            <h2>Control Implementations</h2>
            <div>
                {"".join(families_html) if families_html else '<p>No control implementations found</p>'}
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/charts')
def charts():
    """View all compliance status charts"""
    return render_template('charts.html')

@app.route('/assessment-plan/<plan_name>')
def assessment_plan(plan_name):
    """View specific assessment plan"""
    data = trestle_api.load_assessment_plan_dict(plan_name)
    if not data:
        return f"Assessment plan '{plan_name}' not found", 404
    
    return render_template('assessment_plan.html', plan_name=plan_name, data=data.get('assessment-plan', {}))

@app.route('/assessment-results/<results_name>')
def assessment_results_view(results_name):
    """View specific assessment results"""
    data = trestle_api.load_assessment_results_view(results_name)
    if not data:
        return f"Assessment results '{results_name}' not found", 404
    
    return render_template('assessment_results.html', results_name=results_name, data=data)

@app.route('/poam/<poam_name>')
def poam(poam_name):
    """View specific POA&M"""
    data = trestle_api.load_poam_view(poam_name)
    if not data:
        return f"POA&M '{poam_name}' not found", 404
    
    return render_template('poam.html', poam_name=poam_name, data=data)

@app.route('/mapping/<mapping_name>')
def mapping(mapping_name):
    """View specific mapping collection (OSCAL 1.2.1)"""
    mapping_file = trestle_api.mappings_dir / mapping_name / 'mapping-collection.json'
    if not mapping_file.exists():
        return f"Mapping '{mapping_name}' not found", 404
    
    data = trestle_api.load_mapping_dict(mapping_name)
    if not data:
        return f"Mapping '{mapping_name}' could not be loaded", 500
    
    mapping_collection = data.get('mapping-collection', {})
    metadata = mapping_collection.get('metadata', {})
    provenance = mapping_collection.get('provenance', {})
    mappings = mapping_collection.get('mappings', [])
    
    # Count total map entries across all mappings
    total_maps = sum(len(m.get('maps', [])) for m in mappings)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{metadata.get('title', mapping_name)}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
            h1 {{ color: #2c3e50; }}
            .nav-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
            .back {{ display: inline-block; padding: 8px 16px; background: #95a5a6; color: white; text-decoration: none; border-radius: 4px; }}
            .download {{ display: inline-block; padding: 8px 16px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
            .info {{ background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .mapping {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; border-radius: 4px; }}
            .map-entry {{ background: #fff; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }}
            .confidence {{ display: inline-block; padding: 4px 8px; background: #27ae60; color: white; border-radius: 4px; font-size: 0.9em; }}
            .coverage {{ display: inline-block; padding: 4px 8px; background: #f39c12; color: white; border-radius: 4px; font-size: 0.9em; }}
            pre {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 4px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-bar">
                <a href="/" class="back">← Back to Home</a>
                <a href="/api/mapping/{mapping_name}" class="download">📄 Display JSON</a>
            </div>
            <h1>🔗 {metadata.get('title', mapping_name)}</h1>
            <div class="info">
                <p><strong>UUID:</strong> {mapping_collection.get('uuid', 'N/A')}</p>
                <p><strong>Version:</strong> {metadata.get('version', 'N/A')}</p>
                <p><strong>Last Modified:</strong> {metadata.get('last-modified', 'N/A')}</p>
                <p><strong>OSCAL Version:</strong> {metadata.get('oscal-version', 'N/A')}</p>
                <p><strong>Method:</strong> {provenance.get('method', 'N/A')}</p>
                <p><strong>Matching Rationale:</strong> {provenance.get('matching-rationale', 'N/A')}</p>
                <p><strong>Status:</strong> {provenance.get('status', 'N/A')}</p>
                <p><strong>Description:</strong> {provenance.get('mapping-description', 'N/A')}</p>
                <p><strong>Total Mappings:</strong> {len(mappings)}</p>
                <p><strong>Total Map Entries:</strong> {total_maps}</p>
            </div>
            
            <h2>OSCAL Mapping Collections ({len(mappings)})</h2>
            {''.join([f'''
            <div class="mapping">
                <p><strong>Source:</strong> {m.get('source-resource', {}).get('href', 'N/A')}</p>
                <p><strong>Target:</strong> {m.get('target-resource', {}).get('href', 'N/A')}</p>
                <p><strong>Maps:</strong> {len(m.get('maps', []))} entries</p>
                {''.join([f"""
                <div class="map-entry">
                    <p><strong>Sources:</strong> {', '.join([s.get('id-ref', 'N/A') for s in map_entry.get('sources', [])])}</p>
                    <p><strong>Targets:</strong> {', '.join([t.get('id-ref', 'N/A') for t in map_entry.get('targets', [])])}</p>
                    <p><strong>Relationship:</strong> {map_entry.get('relationship', 'N/A')}</p>
                    {f'<span class="confidence">Confidence: {map_entry.get("confidence-score", {}).get("percentage", 0):.0%}</span>' if 'confidence-score' in map_entry else ''}
                    {f'<span class="coverage">Coverage: {map_entry.get("coverage", {}).get("target-coverage", 0):.0%}</span>' if 'coverage' in map_entry else ''}
                </div>
                """ for map_entry in m.get('maps', [])])}
            </div>
            ''' for m in mappings])}
        </div>
    </body>
    </html>
    """

@app.route('/api/mapping/<mapping_name>')
def api_mapping(mapping_name):
    """Get mapping collection JSON"""
    data = trestle_api.load_mapping_dict(mapping_name)
    if not data:
        return jsonify({'error': f"Mapping '{mapping_name}' not found"}), 404
    
    return jsonify(data)

@app.route('/api/assessment-results/<results_name>')
def api_assessment_results(results_name):
    """Get assessment results JSON"""
    data = trestle_api.load_assessment_results_dict(results_name)
    if not data:
        return jsonify({'error': f"Assessment results '{results_name}' not found"}), 404
    
    return jsonify(data)

@app.route('/api/poam/<poam_name>')
def api_poam(poam_name):
    """Get POA&M JSON"""
    data = trestle_api.load_poam_dict(poam_name)
    if not data:
        return jsonify({'error': f"POA&M '{poam_name}' not found"}), 404
    
    return jsonify(data)

if __name__ == '__main__':
    print("=" * 70)
    print("OSCAL Compliance Demo - Web Server")
    print("=" * 70)
    print(f"Trestle Workspace: {TRESTLE_ROOT.absolute()}")
    print(f"Catalogs: {len(get_catalogs())}")
    print(f"Profiles: {len(get_profiles())}")
    print(f"Server: http://localhost:5000")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
