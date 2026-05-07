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
Trestle API module for reading OSCAL documents using compliance-trestle library.
This module provides a clean interface for loading catalogs, profiles, component definitions,
and SSPs using trestle's built-in functionality.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import trestle.oscal.catalog as catalog_module
import trestle.oscal.profile as profile_module
import trestle.oscal.component as component_module
import trestle.oscal.ssp as ssp_module
import trestle.oscal.mapping as mapping_module
import trestle.oscal.assessment_results as assessment_results_module
from trestle.common.model_utils import ModelUtils


class TrestleAPI:
    """API for interacting with OSCAL documents via trestle"""
    
    def __init__(self, trestle_root: Path):
        """
        Initialize TrestleAPI with the trestle workspace root.
        
        Args:
            trestle_root: Path to the trestle workspace directory
        """
        self.trestle_root = Path(trestle_root)
        self.catalogs_dir = self.trestle_root / 'catalogs'
        self.profiles_dir = self.trestle_root / 'profiles'
        self.components_dir = self.trestle_root / 'component-definitions'
        self.ssps_dir = self.trestle_root / 'system-security-plans'
        self.assessment_plans_dir = self.trestle_root / 'assessment-plans'
        self.assessment_results_dir = self.trestle_root / 'assessment-results'
        self.poams_dir = self.trestle_root / 'plan-of-action-and-milestones'
        self.mappings_dir = self.trestle_root / 'mapping-collections'
    
    def list_catalogs(self) -> List[Dict[str, str]]:
        """
        List all available catalogs.
        
        Returns:
            List of catalog info dictionaries with name, title, version
        """
        catalogs = []
        if self.catalogs_dir.exists():
            for catalog_dir in self.catalogs_dir.iterdir():
                if catalog_dir.is_dir() and catalog_dir.name != '.keep':
                    catalog_file = catalog_dir / 'catalog.json'
                    if catalog_file.exists():
                        try:
                            catalog_obj = catalog_module.Catalog.oscal_read(catalog_file)
                            catalogs.append({
                                'name': catalog_dir.name,
                                'title': catalog_obj.metadata.title,
                                'version': catalog_obj.metadata.version,
                                'path': str(catalog_dir)
                            })
                        except Exception as e:
                            print(f"Error loading catalog {catalog_dir.name}: {e}")
        return catalogs
    
    def load_catalog(self, catalog_name: str) -> Optional[catalog_module.Catalog]:
        """
        Load a specific catalog by name.
        
        Args:
            catalog_name: Name of the catalog directory
            
        Returns:
            Catalog object or None if not found
        """
        catalog_file = self.catalogs_dir / catalog_name / 'catalog.json'
        if catalog_file.exists():
            try:
                return catalog_module.Catalog.oscal_read(catalog_file)
            except Exception as e:
                print(f"Error loading catalog {catalog_name}: {e}")
        return None
    
    def load_catalog_dict(self, catalog_name: str) -> Optional[Dict[str, Any]]:
        """Load a specific catalog by name and return native OSCAL dictionary data."""
        catalog_obj = self.load_catalog(catalog_name)
        if catalog_obj:
            return catalog_obj.oscal_dict()
        return None

    def list_profiles(self) -> List[Dict[str, str]]:
        """
        List all available profiles.
        
        Returns:
            List of profile info dictionaries with name, title, version
        """
        profiles = []
        if self.profiles_dir.exists():
            for profile_dir in self.profiles_dir.iterdir():
                if profile_dir.is_dir() and profile_dir.name != '.keep':
                    profile_file = profile_dir / 'profile.json'
                    if profile_file.exists():
                        try:
                            profile_obj = profile_module.Profile.oscal_read(profile_file)
                            profiles.append({
                                'name': profile_dir.name,
                                'title': profile_obj.metadata.title,
                                'version': profile_obj.metadata.version,
                                'path': str(profile_dir)
                            })
                        except Exception as e:
                            print(f"Error loading profile {profile_dir.name}: {e}")
        return profiles
    
    def load_profile(self, profile_name: str) -> Optional[profile_module.Profile]:
        """
        Load a specific profile by name.
        
        Args:
            profile_name: Name of the profile directory
            
        Returns:
            Profile object or None if not found
        """
        profile_file = self.profiles_dir / profile_name / 'profile.json'
        if profile_file.exists():
            try:
                return profile_module.Profile.oscal_read(profile_file)
            except Exception as e:
                print(f"Error loading profile {profile_name}: {e}")
        return None
    
    def load_profile_dict(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """Load a specific profile by name and return native OSCAL dictionary data."""
        profile_obj = self.load_profile(profile_name)
        if profile_obj:
            return profile_obj.oscal_dict()
        return None

    def list_components(self) -> List[Dict[str, str]]:
        """
        List all available component definitions.
        
        Returns:
            List of component info dictionaries with name, title, version
        """
        components = []
        if self.components_dir.exists():
            for comp_dir in self.components_dir.iterdir():
                if comp_dir.is_dir() and comp_dir.name != '.keep':
                    comp_file = comp_dir / 'component-definition.json'
                    if comp_file.exists():
                        try:
                            comp_obj = component_module.ComponentDefinition.oscal_read(comp_file)
                            components.append({
                                'name': comp_dir.name,
                                'title': comp_obj.metadata.title,
                                'version': comp_obj.metadata.version,
                                'path': str(comp_dir)
                            })
                        except Exception as e:
                            print(f"Error loading component {comp_dir.name}: {e}")
        return components
    
    def load_component(self, component_name: str) -> Optional[component_module.ComponentDefinition]:
        """
        Load a specific component definition by name.
        
        Args:
            component_name: Name of the component directory
            
        Returns:
            ComponentDefinition object or None if not found
        """
        comp_file = self.components_dir / component_name / 'component-definition.json'
        if comp_file.exists():
            try:
                return component_module.ComponentDefinition.oscal_read(comp_file)
            except Exception as e:
                print(f"Error loading component {component_name}: {e}")
        return None
    
    def load_component_dict(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Load a specific component definition by name and return native OSCAL dictionary data."""
        comp_obj = self.load_component(component_name)
        if comp_obj:
            return comp_obj.oscal_dict()
        return None

    def list_ssps(self) -> List[Dict[str, str]]:
        """
        List all available system security plans.
        
        Returns:
            List of SSP info dictionaries with name, title, version
        """
        ssps = []
        if self.ssps_dir.exists():
            for ssp_dir in self.ssps_dir.iterdir():
                if ssp_dir.is_dir() and ssp_dir.name != '.keep':
                    ssp_file = ssp_dir / 'system-security-plan.json'
                    if ssp_file.exists():
                        try:
                            ssp_obj = ssp_module.SystemSecurityPlan.oscal_read(ssp_file)
                            ssps.append({
                                'name': ssp_dir.name,
                                'title': ssp_obj.metadata.title,
                                'version': ssp_obj.metadata.version,
                                'path': str(ssp_dir)
                            })
                        except Exception as e:
                            print(f"Error loading SSP {ssp_dir.name}: {e}")
        return ssps
    
    def load_ssp(self, ssp_name: str) -> Optional[ssp_module.SystemSecurityPlan]:
        """
        Load a specific system security plan by name.
        
        Args:
            ssp_name: Name of the SSP directory
            
        Returns:
            SystemSecurityPlan object or None if not found
        """
        ssp_file = self.ssps_dir / ssp_name / 'system-security-plan.json'
        if ssp_file.exists():
            try:
                return ssp_module.SystemSecurityPlan.oscal_read(ssp_file)
            except Exception as e:
                print(f"Error loading SSP {ssp_name}: {e}")
        return None
    
    def load_ssp_dict(self, ssp_name: str) -> Optional[Dict[str, Any]]:
        """Load a specific system security plan by name and return native OSCAL dictionary data."""
        ssp_obj = self.load_ssp(ssp_name)
        if ssp_obj:
            return ssp_obj.oscal_dict()
        return None

    def save_ssp(self, ssp: ssp_module.SystemSecurityPlan, ssp_name: str) -> bool:
        """
        Save a system security plan.
        
        Args:
            ssp: SystemSecurityPlan object to save
            ssp_name: Name of the SSP directory
            
        Returns:
            True if successful, False otherwise
        """
        ssp_dir = self.ssps_dir / ssp_name
        ssp_dir.mkdir(parents=True, exist_ok=True)
        ssp_file = ssp_dir / 'system-security-plan.json'
        try:
            ssp.oscal_write(ssp_file)
            return True
        except Exception as e:
            print(f"Error saving SSP {ssp_name}: {e}")
            return False
    def save_assessment_plan(self, plan, plan_name: str) -> bool:
        """
        Save an assessment plan.
        
        Args:
            plan: AssessmentPlan object to save
            plan_name: Name of the assessment plan directory
            
        Returns:
            True if successful, False otherwise
        """
        plan_dir = self.assessment_plans_dir / plan_name
        plan_dir.mkdir(parents=True, exist_ok=True)
        plan_file = plan_dir / 'assessment-plan.json'
        try:
            plan.oscal_write(plan_file)
            return True
        except Exception as e:
            print(f"Error saving assessment plan {plan_name}: {e}")
            return False
    
    def save_assessment_results(self, results, results_name: str) -> bool:
        """
        Save assessment results.
        
        Args:
            results: AssessmentResults object to save
            results_name: Name of the assessment results directory
            
        Returns:
            True if successful, False otherwise
        """
        results_dir = self.assessment_results_dir / results_name
        results_dir.mkdir(parents=True, exist_ok=True)
        results_file = results_dir / 'assessment-results.json'
        try:
            results.oscal_write(results_file)
            return True
        except Exception as e:
            print(f"Error saving assessment results {results_name}: {e}")
            return False
    
    def load_assessment_plan(self, plan_name: str):
        """
        Load an assessment plan by name.
        
        Args:
            plan_name: Name of the assessment plan directory
            
        Returns:
            AssessmentPlan object or None if not found
        """
        plan_file = self.assessment_plans_dir / plan_name / 'assessment-plan.json'
        if not plan_file.exists():
            return None
        try:
            import trestle.oscal.assessment_plan as ap_module
            return ap_module.AssessmentPlan.oscal_read(plan_file)
        except Exception as e:
            print(f"Error loading assessment plan {plan_name}: {e}")
            return None
    
    
    def load_assessment_plan_dict(self, plan_name: str) -> Optional[Dict[str, Any]]:
        """Load an assessment plan by name and return native OSCAL dictionary data."""
        plan_obj = self.load_assessment_plan(plan_name)
        if plan_obj:
            return plan_obj.oscal_dict()
        return None

    def list_assessment_plans(self) -> List[Dict[str, str]]:
        """List all available assessment plans"""
        plans = []
        if self.assessment_plans_dir.exists():
            for plan_dir in self.assessment_plans_dir.iterdir():
                if plan_dir.is_dir() and plan_dir.name != '.keep':
                    plan_file = plan_dir / 'assessment-plan.json'
                    title = plan_dir.name
                    version = 'N/A'
                    if plan_file.exists():
                        try:
                            import trestle.oscal.assessment_plan as ap_module
                            plan_obj = ap_module.AssessmentPlan.oscal_read(plan_file)
                            title = plan_obj.metadata.title or plan_dir.name
                            version = plan_obj.metadata.version or 'N/A'
                        except Exception as e:
                            print(f"Error loading assessment plan {plan_dir.name}: {e}")
                    plans.append({
                        'name': plan_dir.name,
                        'title': title,
                        'version': version,
                        'path': str(plan_dir)
                    })
        return plans
    
    def load_assessment_results(self, results_name: str):
        """Load assessment results by name."""
        results_file = self.assessment_results_dir / results_name / 'assessment-results.json'
        if not results_file.exists():
            return None
        try:
            return assessment_results_module.AssessmentResults.oscal_read(results_file)
        except Exception as e:
            print(f"Error loading assessment results {results_name}: {e}")
            return None

    def load_assessment_results_dict(self, results_name: str) -> Optional[Dict[str, Any]]:
        """Load assessment results by name and return native OSCAL dictionary data."""
        results_obj = self.load_assessment_results(results_name)
        if results_obj:
            return results_obj.oscal_dict()
        return None

    def load_assessment_results_view(self, results_name: str) -> Optional[Dict[str, Any]]:
        """Load assessment results by name and return normalized data for the web view."""
        data = self.load_assessment_results_dict(results_name)
        if not data:
            return None

        ar = data.get('assessment-results', data)

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

    def list_assessment_results(self) -> List[Dict[str, str]]:
        """List all available assessment results"""
        results = []
        if self.assessment_results_dir.exists():
            for result_dir in self.assessment_results_dir.iterdir():
                if result_dir.is_dir() and result_dir.name != '.keep':
                    ar_file = result_dir / 'assessment-results.json'
                    title = result_dir.name
                    version = 'N/A'

                    if ar_file.exists():
                        try:
                            ar_obj = assessment_results_module.AssessmentResults.oscal_read(ar_file)
                            title = ar_obj.metadata.title or result_dir.name
                            version = ar_obj.metadata.version or 'N/A'
                        except Exception as e:
                            print(f"Error loading assessment results {result_dir.name}: {e}")

                    results.append({
                        'name': result_dir.name,
                        'title': title,
                        'version': version,
                        'path': str(result_dir)
                    })
        return results
    
    def resolve_regulation_reference(self, href: Optional[str]) -> Dict[str, str]:
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
            profile_obj = self.load_profile(source_name)
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
            catalog_obj = self.load_catalog(source_name)
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

    def list_poams(self) -> List[Dict[str, str]]:
        """List all available POAMs"""
        poams = []
        if self.poams_dir.exists():
            for poam_dir in self.poams_dir.iterdir():
                if poam_dir.is_dir() and poam_dir.name != '.keep':
                    # POAMs not yet implemented in trestle, return basic info
                    poams.append({
                        'name': poam_dir.name,
                        'title': poam_dir.name,
                        'version': 'N/A',
                        'path': str(poam_dir)
                    })
        return poams
    
    def list_mappings(self) -> List[Dict[str, str]]:
        """List all available mapping collections"""
        mappings = []
        if self.mappings_dir.exists():
            for mapping_dir in self.mappings_dir.iterdir():
                if mapping_dir.is_dir() and mapping_dir.name != '.keep':
                    # Mapping collections not yet fully implemented, return basic info
                    mapping_file = mapping_dir / 'mapping-collection.json'
                    title = mapping_dir.name
                    version = 'N/A'
                    if mapping_file.exists():
                        try:
                            mapping_obj = mapping_module.MappingCollection.oscal_read(mapping_file)
                            title = mapping_obj.metadata.title or mapping_dir.name
                            version = mapping_obj.metadata.version or 'N/A'
                        except Exception as e:
                            print(f"Error loading mapping collection {mapping_dir.name}: {e}")
                    mappings.append({
                        'name': mapping_dir.name,
                        'title': title,
                        'version': version,
                        'path': str(mapping_dir)
                    })
        return mappings

    def load_mapping(self, mapping_name: str):
        """Load a mapping collection by name."""
        mapping_file = self.mappings_dir / mapping_name / 'mapping-collection.json'
        if not mapping_file.exists():
            return None
        try:
            return mapping_module.MappingCollection.oscal_read(mapping_file)
        except Exception as e:
            print(f"Error loading mapping collection {mapping_name}: {e}")
            return None

    def load_mapping_dict(self, mapping_name: str) -> Optional[Dict[str, Any]]:
        """Load a mapping collection by name and return native OSCAL dictionary data."""
        mapping_obj = self.load_mapping(mapping_name)
        if mapping_obj:
            return mapping_obj.oscal_dict()
        return None

# Made with Bob
