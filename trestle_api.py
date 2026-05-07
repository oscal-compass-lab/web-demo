#!/usr/bin/env python3
"""
Trestle API module for reading OSCAL documents using compliance-trestle library.
This module provides a clean interface for loading catalogs, profiles, component definitions,
and SSPs using trestle's built-in functionality.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import trestle.oscal.catalog as catalog_module
import trestle.oscal.profile as profile_module
import trestle.oscal.component as component_module
import trestle.oscal.ssp as ssp_module
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
    
    
    def list_assessment_plans(self) -> List[Dict[str, str]]:
        """List all available assessment plans"""
        plans = []
        if self.assessment_plans_dir.exists():
            for plan_dir in self.assessment_plans_dir.iterdir():
                if plan_dir.is_dir() and plan_dir.name != '.keep':
                    # Assessment plans not yet implemented in trestle, return basic info
                    plans.append({
                        'name': plan_dir.name,
                        'title': plan_dir.name,
                        'version': 'N/A',
                        'path': str(plan_dir)
                    })
        return plans
    
    def list_assessment_results(self) -> List[Dict[str, str]]:
        """List all available assessment results"""
        results = []
        if self.assessment_results_dir.exists():
            for result_dir in self.assessment_results_dir.iterdir():
                if result_dir.is_dir() and result_dir.name != '.keep':
                    # Read the assessment results JSON to get metadata
                    ar_file = result_dir / 'assessment-results.json'
                    title = result_dir.name
                    version = 'N/A'
                    
                    if ar_file.exists():
                        try:
                            with open(ar_file, 'r') as f:
                                ar_data = json.load(f)
                                ar = ar_data.get('assessment-results', {})
                                metadata = ar.get('metadata', {})
                                title = metadata.get('title', result_dir.name)
                                version = metadata.get('version', 'N/A')
                        except (json.JSONDecodeError, KeyError):
                            pass  # Use defaults if file is invalid
                    
                    results.append({
                        'name': result_dir.name,
                        'title': title,
                        'version': version,
                        'path': str(result_dir)
                    })
        return results
    
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
                    mappings.append({
                        'name': mapping_dir.name,
                        'title': mapping_dir.name,
                        'version': 'N/A',
                        'path': str(mapping_dir)
                    })
        return mappings

# Made with Bob
