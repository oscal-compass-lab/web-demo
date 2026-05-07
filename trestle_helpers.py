#!/usr/bin/env python3
"""
Helper functions to convert trestle OSCAL objects to dictionaries for web display.
This allows us to use trestle API for loading while keeping existing display logic.
"""

from typing import Dict, Any, Optional, List
import trestle.oscal.catalog as catalog_module
import trestle.oscal.profile as profile_module
import trestle.oscal.component as component_module
import trestle.oscal.ssp as ssp_module


def catalog_to_dict(catalog: catalog_module.Catalog) -> Dict[str, Any]:
    """Convert Catalog object to dictionary matching the JSON structure"""
    return {
        'catalog': {
            'uuid': str(catalog.uuid),
            'metadata': metadata_to_dict(catalog.metadata),
            'groups': [group_to_dict(g) for g in (catalog.groups or [])],
            'controls': [control_to_dict(c) for c in (catalog.controls or [])]
        }
    }


def profile_to_dict(profile: profile_module.Profile) -> Dict[str, Any]:
    """Convert Profile object to dictionary matching the JSON structure"""
    return {
        'profile': {
            'uuid': str(profile.uuid),
            'metadata': metadata_to_dict(profile.metadata),
            'imports': [import_to_dict(i) for i in (profile.imports or [])],
            'merge': merge_to_dict(profile.merge) if profile.merge else None,
            'modify': modify_to_dict(profile.modify) if profile.modify else None
        }
    }


def component_to_dict(component_def: component_module.ComponentDefinition) -> Dict[str, Any]:
    """Convert ComponentDefinition object to dictionary matching the JSON structure"""
    return {
        'component-definition': {
            'uuid': str(component_def.uuid),
            'metadata': metadata_to_dict(component_def.metadata),
            'components': [comp_to_dict(c) for c in (component_def.components or [])]
        }
    }


def ssp_to_dict(ssp: ssp_module.SystemSecurityPlan) -> Dict[str, Any]:
    """Convert SystemSecurityPlan object to dictionary matching the JSON structure"""
    return {
        'system-security-plan': {
            'uuid': str(ssp.uuid),
            'metadata': metadata_to_dict(ssp.metadata),
            'import-profile': {
                'href': ssp.import_profile.href
            } if ssp.import_profile else None,
            'system-characteristics': sys_chars_to_dict(ssp.system_characteristics),
            'system-implementation': sys_impl_to_dict(ssp.system_implementation),
            'control-implementation': ctrl_impl_to_dict(ssp.control_implementation)
        }
    }


def metadata_to_dict(metadata) -> Dict[str, Any]:
    """Convert Metadata object to dictionary"""
    result = {}
    if hasattr(metadata, 'title') and metadata.title:
        result['title'] = str(metadata.title)
    if hasattr(metadata, 'last_modified') and metadata.last_modified:
        result['last-modified'] = str(metadata.last_modified)
    if hasattr(metadata, 'version') and metadata.version:
        result['version'] = str(metadata.version)
    if hasattr(metadata, 'oscal_version') and metadata.oscal_version:
        result['oscal-version'] = str(metadata.oscal_version)
    if hasattr(metadata, 'published') and metadata.published:
        result['published'] = str(metadata.published)
    if hasattr(metadata, 'props') and metadata.props:
        result['props'] = [prop_to_dict(p) for p in metadata.props]
    if hasattr(metadata, 'links') and metadata.links:
        result['links'] = [link_to_dict(l) for l in metadata.links]
    if hasattr(metadata, 'remarks') and metadata.remarks:
        result['remarks'] = str(metadata.remarks)
    return result


def group_to_dict(group) -> Dict[str, Any]:
    """Convert Group object to dictionary"""
    result = {
        'id': group.id,
        'class': group.class_,
        'title': group.title
    }
    if hasattr(group, 'params') and group.params:
        result['params'] = [param_to_dict(p) for p in group.params]
    if hasattr(group, 'props') and group.props:
        result['props'] = [prop_to_dict(p) for p in group.props]
    if hasattr(group, 'parts') and group.parts:
        result['parts'] = [part_to_dict(p) for p in group.parts]
    if hasattr(group, 'groups') and group.groups:
        result['groups'] = [group_to_dict(g) for g in group.groups]
    if hasattr(group, 'controls') and group.controls:
        result['controls'] = [control_to_dict(c) for c in group.controls]
    return result


def control_to_dict(control) -> Dict[str, Any]:
    """Convert Control object to dictionary"""
    result = {
        'id': control.id,
        'class': control.class_,
        'title': control.title
    }
    if hasattr(control, 'params') and control.params:
        result['params'] = [param_to_dict(p) for p in control.params]
    if hasattr(control, 'props') and control.props:
        result['props'] = [prop_to_dict(p) for p in control.props]
    if hasattr(control, 'parts') and control.parts:
        result['parts'] = [part_to_dict(p) for p in control.parts]
    if hasattr(control, 'controls') and control.controls:
        result['controls'] = [control_to_dict(c) for c in control.controls]
    return result


def param_to_dict(param) -> Dict[str, Any]:
    """Convert Parameter object to dictionary"""
    result = {'id': param.id}
    if hasattr(param, 'label') and param.label:
        result['label'] = param.label
    if hasattr(param, 'values') and param.values:
        result['values'] = param.values
    if hasattr(param, 'select') and param.select:
        result['select'] = select_to_dict(param.select)
    if hasattr(param, 'guidelines') and param.guidelines:
        result['guidelines'] = [guideline_to_dict(g) for g in param.guidelines]
    if hasattr(param, 'constraints') and param.constraints:
        result['constraints'] = [constraint_to_dict(c) for c in param.constraints]
    if hasattr(param, 'props') and param.props:
        result['props'] = [prop_to_dict(p) for p in param.props]
    if hasattr(param, 'remarks') and param.remarks:
        result['remarks'] = param.remarks
    return result


def part_to_dict(part) -> Dict[str, Any]:
    """Convert Part object to dictionary"""
    result = {}
    if part.id:
        result['id'] = part.id
    if part.name:
        result['name'] = part.name
    if part.prose:
        result['prose'] = part.prose
    if part.props:
        result['props'] = [prop_to_dict(p) for p in part.props]
    if part.parts:
        result['parts'] = [part_to_dict(p) for p in part.parts]
    return result


def prop_to_dict(prop) -> Dict[str, Any]:
    """Convert Property object to dictionary"""
    result = {
        'name': str(prop.name) if prop.name else None,
        'value': str(prop.value) if prop.value else None
    }
    if prop.ns:
        result['ns'] = str(prop.ns)
    if prop.class_:
        result['class'] = str(prop.class_)
    if hasattr(prop, 'remarks') and prop.remarks:
        result['remarks'] = str(prop.remarks)
    return result


def link_to_dict(link) -> Dict[str, Any]:
    """Convert Link object to dictionary"""
    return {
        'href': link.href,
        'rel': link.rel if hasattr(link, 'rel') and link.rel else None
    }


def select_to_dict(select) -> Dict[str, Any]:
    """Convert ParameterSelection object to dictionary"""
    result = {}
    if hasattr(select, 'how_many') and select.how_many:
        result['how-many'] = select.how_many
    if hasattr(select, 'choice') and select.choice:
        result['choice'] = select.choice
    return result


def guideline_to_dict(guideline) -> Dict[str, Any]:
    """Convert ParameterGuideline object to dictionary"""
    result = {}
    if hasattr(guideline, 'prose') and guideline.prose:
        result['prose'] = guideline.prose
    return result


def constraint_to_dict(constraint) -> Dict[str, Any]:
    """Convert ParameterConstraint object to dictionary"""
    result = {}
    if hasattr(constraint, 'description') and constraint.description:
        result['description'] = constraint.description
    return result


def import_to_dict(import_obj) -> Dict[str, Any]:
    """Convert Import object to dictionary"""
    result = {'href': import_obj.href}
    if import_obj.include_controls:
        result['include-controls'] = [{'with-ids': ic.with_ids} for ic in import_obj.include_controls]
    return result


def merge_to_dict(merge) -> Dict[str, Any]:
    """Convert Merge object to dictionary"""
    result = {}
    if hasattr(merge, 'as_is') and merge.as_is is not None:
        # Convert BooleanDatatype to Python bool
        result['as-is'] = bool(merge.as_is)
    if hasattr(merge, 'combine') and merge.combine:
        result['combine'] = {'method': merge.combine.method if hasattr(merge.combine, 'method') else None}
    if hasattr(merge, 'custom') and merge.custom:
        result['custom'] = str(merge.custom)
    return result


def modify_to_dict(modify) -> Dict[str, Any]:
    """Convert Modify object to dictionary"""
    result = {}
    if modify.set_parameters:
        result['set-parameters'] = [
            {'param-id': sp.param_id, 'values': sp.values}
            for sp in modify.set_parameters
        ]
    return result


def comp_to_dict(comp) -> Dict[str, Any]:
    """Convert DefinedComponent object to dictionary"""
    result = {
        'uuid': str(comp.uuid),
        'type': comp.type,
        'title': comp.title,
        'description': comp.description
    }
    if comp.props:
        result['props'] = [prop_to_dict(p) for p in comp.props]
    if comp.control_implementations:
        result['control-implementations'] = [
            ctrl_impl_comp_to_dict(ci) for ci in comp.control_implementations
        ]
    return result


def ctrl_impl_comp_to_dict(ctrl_impl) -> Dict[str, Any]:
    """Convert ControlImplementationSet object to dictionary"""
    return {
        'uuid': str(ctrl_impl.uuid),
        'source': ctrl_impl.source,
        'description': ctrl_impl.description,
        'implemented-requirements': [
            impl_req_to_dict(ir) for ir in (ctrl_impl.implemented_requirements or [])
        ]
    }


def impl_req_to_dict(impl_req) -> Dict[str, Any]:
    """Convert ImplementedRequirementControlImplementation object to dictionary"""
    result = {
        'uuid': str(impl_req.uuid),
        'control-id': impl_req.control_id,
        'description': impl_req.description
    }
    if impl_req.props:
        result['props'] = [prop_to_dict(p) for p in impl_req.props]
    return result


def sys_chars_to_dict(sys_chars) -> Dict[str, Any]:
    """Convert SystemCharacteristics object to dictionary"""
    return {
        'system-ids': [{'id': sid.id} for sid in sys_chars.system_ids],
        'system-name': sys_chars.system_name,
        'description': sys_chars.description,
        'system-information': {
            'information-types': [
                {'title': it.title, 'description': it.description}
                for it in sys_chars.system_information.information_types
            ]
        },
        'status': {'state': sys_chars.status.state},
        'authorization-boundary': {
            'description': sys_chars.authorization_boundary.description
        }
    }


def sys_impl_to_dict(sys_impl) -> Dict[str, Any]:
    """Convert SystemImplementation object to dictionary"""
    return {
        'components': [
            {
                'uuid': str(c.uuid),
                'type': c.type,
                'title': c.title,
                'description': c.description,
                'props': [prop_to_dict(p) for p in (c.props or [])],
                'status': {'state': c.status.state} if c.status else None
            }
            for c in sys_impl.components
        ]
    }


def ctrl_impl_to_dict(ctrl_impl) -> Dict[str, Any]:
    """Convert ControlImplementation object to dictionary"""
    return {
        'description': ctrl_impl.description,
        'implemented-requirements': [
            ssp_impl_req_to_dict(ir) for ir in ctrl_impl.implemented_requirements
        ]
    }


def ssp_impl_req_to_dict(impl_req) -> Dict[str, Any]:
    """Convert SSP ImplementedRequirement object to dictionary"""
    result = {
        'uuid': str(impl_req.uuid),
        'control-id': impl_req.control_id
    }
    if impl_req.statements:
        result['statements'] = [
            {
                'statement-id': stmt.statement_id,
                'uuid': str(stmt.uuid),
                'description': stmt.description if hasattr(stmt, 'description') else '',
                'by-components': [
                    {
                        'component-uuid': str(bc.component_uuid),
                        'description': bc.description,
                        'implementation-status': {'state': bc.implementation_status.state} if bc.implementation_status else None
                    }
                    for bc in (stmt.by_components or [])
                ] if hasattr(stmt, 'by_components') and stmt.by_components else []
            }
            for stmt in impl_req.statements
        ]
    if impl_req.by_components:
        result['by-components'] = [
            {
                'component-uuid': str(bc.component_uuid),
                'description': bc.description,
                'implementation-status': {'state': bc.implementation_status.state} if bc.implementation_status else None
            }
            for bc in impl_req.by_components
        ]
    return result

# Made with Bob



def assessment_plan_to_dict(plan) -> Dict[str, Any]:
    """Convert AssessmentPlan object to dictionary"""
    result = {
        'uuid': str(plan.uuid),
        'metadata': metadata_to_dict(plan.metadata)
    }
    
    if hasattr(plan, 'import_ssp') and plan.import_ssp:
        result['import-ssp'] = {
            'href': plan.import_ssp.href
        }
    
    if hasattr(plan, 'local_definitions') and plan.local_definitions:
        local_defs = {}
        if hasattr(plan.local_definitions, 'activities') and plan.local_definitions.activities:
            local_defs['activities'] = [
                {
                    'uuid': str(act.uuid),
                    'title': act.title,
                    'description': act.description if hasattr(act, 'description') else None,
                    'props': [prop_to_dict(p) for p in act.props] if hasattr(act, 'props') and act.props else [],
                    'steps': [
                        {
                            'uuid': str(step.uuid),
                            'title': step.title,
                            'description': step.description if hasattr(step, 'description') else None
                        }
                        for step in act.steps
                    ] if hasattr(act, 'steps') and act.steps else []
                }
                for act in plan.local_definitions.activities
            ]
        result['local-definitions'] = local_defs
    
    if hasattr(plan, 'assessment_assets') and plan.assessment_assets:
        assets = {}
        if hasattr(plan.assessment_assets, 'assessment_platforms') and plan.assessment_assets.assessment_platforms:
            assets['assessment-platforms'] = [
                {
                    'uuid': str(plat.uuid),
                    'title': plat.title,
                    'props': [prop_to_dict(p) for p in plat.props] if hasattr(plat, 'props') and plat.props else []
                }
                for plat in plan.assessment_assets.assessment_platforms
            ]
        result['assessment-assets'] = assets
    
    if hasattr(plan, 'reviewed_controls') and plan.reviewed_controls:
        result['reviewed-controls'] = {
            'description': plan.reviewed_controls.description if hasattr(plan.reviewed_controls, 'description') else None,
            'props': [prop_to_dict(p) for p in plan.reviewed_controls.props] if hasattr(plan.reviewed_controls, 'props') and plan.reviewed_controls.props else []
        }
    
    if hasattr(plan, 'assessment_subjects') and plan.assessment_subjects:
        result['assessment-subjects'] = [
            {
                'type': subj.type,
                'description': subj.description if hasattr(subj, 'description') else None,
                'include-subjects': len(subj.include_subjects) if hasattr(subj, 'include_subjects') and subj.include_subjects else 0
            }
            for subj in plan.assessment_subjects
        ]
    
    if hasattr(plan, 'tasks') and plan.tasks:
        result['tasks'] = [
            {
                'uuid': str(task.uuid),
                'type': task.type,
                'title': task.title,
                'description': task.description if hasattr(task, 'description') else None
            }
            for task in plan.tasks
        ]
    
    return result


def assessment_results_to_dict(results_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Assessment Results JSON for structured web display."""
    ar = results_data.get('assessment-results', results_data)

    metadata = ar.get('metadata', {})
    props = metadata.get('props', []) or []

    regulation = 'N/A'
    assessment_scope = 'N/A'
    subject_count = 'N/A'
    result_summary = 'N/A'
    for prop in props:
        name = prop.get('name')
        value = prop.get('value')
        if name == 'regulation':
            regulation = value
        elif name == 'assessment-scope':
            assessment_scope = value
        elif name == 'assessment-subject-count':
            subject_count = value
        elif name == 'result-summary':
            result_summary = value

    normalized_results = []
    for result in ar.get('results', []) or []:
        reviewed_controls = result.get('reviewed-controls', {}) or {}
        control_selections = reviewed_controls.get('control-selections', []) or []

        assessment_log = result.get('assessment-log', {}) or {}
        log_entries = assessment_log.get('entries', []) or []

        observations = []
        for observation in result.get('observations', []) or []:
            observations.append({
                'uuid': observation.get('uuid', 'N/A'),
                'title': observation.get('title', 'Untitled Observation'),
                'description': observation.get('description', 'N/A'),
                'methods': observation.get('methods', []) or [],
                'types': observation.get('types', []) or [],
                'collected': observation.get('collected', 'N/A'),
                'subject_count': len(observation.get('subjects', []) or []),
                'evidence': [
                    ev.get('description', 'N/A')
                    for ev in (observation.get('relevant-evidence', []) or [])
                ]
            })

        risks = []
        for risk in result.get('risks', []) or []:
            risks.append({
                'uuid': risk.get('uuid', 'N/A'),
                'title': risk.get('title', 'Untitled Risk'),
                'description': risk.get('description', 'N/A'),
                'statement': risk.get('statement', 'N/A'),
                'status': risk.get('status', 'N/A')
            })

        normalized_results.append({
            'uuid': result.get('uuid', 'N/A'),
            'title': result.get('title', 'Untitled Result'),
            'description': result.get('description', 'N/A'),
            'start': result.get('start', 'N/A'),
            'end': result.get('end', 'N/A'),
            'remarks': result.get('remarks', ''),
            'control_selections': control_selections,
            'assessment_log_entries': log_entries,
            'observations': observations,
            'risks': risks
        })

    activities = []
    local_definitions = ar.get('local-definitions', {}) or {}
    for activity in local_definitions.get('activities', []) or []:
        activities.append({
            'uuid': activity.get('uuid', 'N/A'),
            'title': activity.get('title', 'Untitled Activity'),
            'description': activity.get('description', 'N/A'),
            'steps': activity.get('steps', []) or []
        })

    return {
        'uuid': ar.get('uuid', 'N/A'),
        'metadata': {
            'title': metadata.get('title', 'N/A'),
            'version': metadata.get('version', 'N/A'),
            'last-modified': metadata.get('last-modified', 'N/A'),
            'oscal-version': metadata.get('oscal-version', 'N/A'),
            'published': metadata.get('published', 'N/A')
        },
        'import-ap': ar.get('import-ap'),
        'regulation': regulation,
        'assessment-scope': assessment_scope,
        'assessment-subject-count': subject_count,
        'result-summary': result_summary,
        'local-definitions': {
            'activities': activities
        },
        'results': normalized_results
    }


def resolve_regulation_reference(href: Optional[str], trestle_api) -> Dict[str, str]:
    """Resolve an SSP import-profile reference into normalized regulation display metadata."""
    result = {
        'label': 'N/A',
        'href': href or 'N/A',
        'title': 'N/A',
        'version': 'N/A',
        'source_type': 'unknown',
        'source_name': 'N/A'
    }

    if not href:
        return result

    parts = href.rstrip('/').split('/')
    if len(parts) < 2:
        result['label'] = href
        return result

    source_name = parts[-2]
    source_type = parts[-3] if len(parts) >= 3 else 'unknown'
    result['source_name'] = source_name

    if source_type == 'profiles':
        result['source_type'] = 'profile'
        profile_obj = trestle_api.load_profile(source_name)
        if profile_obj:
            title = str(profile_obj.metadata.title)
            version = str(profile_obj.metadata.version)
            result['title'] = title
            result['version'] = version
            normalized = {
                'FedRAMP-Rev5-Low': 'FedRAMP Rev 5 Low',
                'FedRAMP-Rev5-Moderate': 'FedRAMP Rev 5 Moderate',
                'FedRAMP-Rev5-High': 'FedRAMP Rev 5 High'
            }
            result['label'] = normalized.get(source_name, title)
        else:
            result['label'] = source_name
    elif source_type == 'catalogs':
        result['source_type'] = 'catalog'
        catalog_obj = trestle_api.load_catalog(source_name)
        if catalog_obj:
            title = str(catalog_obj.metadata.title)
            version = str(catalog_obj.metadata.version)
            result['title'] = title
            result['version'] = version
            normalized = {
                'EU-Dora': f'EU DORA {version}' if version and version != 'None' else 'EU DORA'
            }
            result['label'] = normalized.get(source_name, title)
        else:
            result['label'] = source_name
    else:
        result['label'] = source_name or href

    return result


def update_ssp_metadata(ssp: ssp_module.SystemSecurityPlan, trestle_api) -> ssp_module.SystemSecurityPlan:
    """Update SSP metadata with meaningful values after generation"""
    # Update metadata
    ssp.metadata.title = 'Ubuntu System Security Plan'
    ssp.metadata.version = '1.0'
    
    # Update system characteristics
    if ssp.system_characteristics.system_ids:
        ssp.system_characteristics.system_ids[0].id = 'ubuntu-system-001'
    ssp.system_characteristics.system_name = 'Ubuntu System with Security Compliance'
    ssp.system_characteristics.description = 'System Security Plan for Ubuntu Linux 24.04 LTS with OSCAP compliance validation, implementing FedRAMP Moderate baseline controls'
    
    if ssp.system_characteristics.system_information and ssp.system_characteristics.system_information.information_types:
        ssp.system_characteristics.system_information.information_types[0].title = 'System and Network Configuration'
        ssp.system_characteristics.system_information.information_types[0].description = 'Information related to system configuration, security settings, compliance validation, and network infrastructure'
    
    if ssp.system_characteristics.authorization_boundary:
        ssp.system_characteristics.authorization_boundary.description = 'Ubuntu Linux 24.04 LTS operating system with OSCAP security compliance validation, including all security configurations, access controls, and system hardening measures'
    
    # Update this-system component description
    if ssp.system_implementation and ssp.system_implementation.components:
        for comp in ssp.system_implementation.components:
            if comp.type == 'this-system' and comp.description == 'REPLACE_ME':
                comp.description = 'Ubuntu Linux 24.04 LTS system with integrated security compliance validation using OSCAP, implementing FedRAMP Moderate baseline security controls'
                comp.title = 'Ubuntu Security Compliance System'
    
    return ssp
