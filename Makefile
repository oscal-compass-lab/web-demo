.PHONY: all venv help ws run validate create-catalogs create-profiles create-resolve create-mappings create-xccdf create-compdefs create-ssps create-aps create-ars create-poams charts create-oscal artifacts clean-artifacts clean-catalogs clean-profiles clean-resolve clean-mappings clean-compdefs clean-ssps clean-aps clean-ars clean-poams clean-xccdf clean-charts clean-oscal clean-ws clean-venv copy-images

# Python virtual environment directory
VENV_DIR = .venv
TRESTLE_WORKSPACE = trestle-workspace

all: venv ws artifacts charts validate run

help:
	@echo "Available targets:"
	@echo "  all            - Default target, sets up environment, validates, and runs app"
	@echo "  venv           - Create virtual environment and install dependencies from requirements.txt"
	@echo "  clean-venv     - Remove virtual environment"
	@echo "  ws             - Create trestle-workspace and initialize trestle"
	@echo "  clean-ws       - Remove trestle-workspace folder and contents"
	@echo "  artifacts      - Generate all artifacts (XCCDF results and OSCAL documents) in correct order"
	@echo "  clean-artifacts - Remove all generated/copied artifacts (XCCDF results and OSCAL documents)"
	@echo "  validate       - Validate all OSCAL documents with trestle"
	@echo "  charts         - Generate compliance status charts from assessment results"
	@echo "  clean-charts   - Remove all generated charts"
	@echo "  run            - Launch Flask application"
	


create-xccdf: venv ws create-compdefs
	@echo "Creating XCCDF scan result files..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_xccdf_results.py

clean-xccdf:
	@echo "Removing generated XCCDF scan result files..."
	@rm -rf source-data/xccdf-results/*.xml
	@echo "✅ XCCDF results removed"

create-catalogs: venv ws
	@echo "Copying catalogs from source-data to trestle workspace..."
	@for catalog in source-data/catalogs/*; do \
		if [ -d "$$catalog" ] && [ "$$(basename $$catalog)" != ".keep" ]; then \
			catalog_name=$$(basename $$catalog); \
			echo "  Copying $$catalog_name..."; \
			rm -rf $(TRESTLE_WORKSPACE)/catalogs/$$catalog_name; \
			cp -r $$catalog $(TRESTLE_WORKSPACE)/catalogs/; \
		fi; \
	done
	@echo "Updating OSCAL versions in catalogs..."
	@. $(VENV_DIR)/bin/activate && python3 python/update_oscal_version.py
	@echo "✅ Catalogs copied and updated"

create-profiles: venv ws create-catalogs
	@echo "Copying profiles from source-data to trestle workspace..."
	@for profile in source-data/profiles/*; do \
		if [ -d "$$profile" ] && [ "$$(basename $$profile)" != ".keep" ]; then \
			profile_name=$$(basename $$profile); \
			echo "  Copying $$profile_name..."; \
			rm -rf $(TRESTLE_WORKSPACE)/profiles/$$profile_name; \
			cp -r $$profile $(TRESTLE_WORKSPACE)/profiles/; \
		fi; \
	done
	@echo "Updating OSCAL versions in profiles..."
	@. $(VENV_DIR)/bin/activate && python3 python/update_oscal_version.py
	@echo "✅ Profiles copied and updated"

create-resolve: venv ws create-profiles
	@cd $(TRESTLE_WORKSPACE) && \
	for profile in $$(ls -1 profiles 2>/dev/null | grep -v '.keep' || true); do \
		output_name="resolved-$$profile"; \
		if [ ! -d "catalogs/$$output_name" ]; then \
			echo "Resolving profile $$profile to catalog $$output_name..."; \
			. ../$(VENV_DIR)/bin/activate && \
			trestle author profile-resolve -n "$$profile" -o "$$output_name"; \
		fi; \
	done
	@echo "✅ Profiles resolved to catalogs"

create-mappings: venv ws
	@echo "Creating NIST to DORA mapping collection..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_dora_nist_mapping.py

create-oscal: create-catalogs create-profiles create-resolve create-mappings create-compdefs create-ssps create-aps create-ars create-poams
	@echo "✅ All OSCAL documents created"

create-compdefs: venv ws
	@echo "Copying component definitions from source-data to trestle workspace..."
	@for compdef in source-data/component-definitions/*; do \
		if [ -d "$$compdef" ] && [ "$$(basename $$compdef)" != ".keep" ]; then \
			compdef_name=$$(basename $$compdef); \
			echo "  Copying $$compdef_name..."; \
			rm -rf $(TRESTLE_WORKSPACE)/component-definitions/$$compdef_name; \
			cp -r $$compdef $(TRESTLE_WORKSPACE)/component-definitions/; \
		fi; \
	done
	@echo "Updating OSCAL versions in component definitions..."
	@. $(VENV_DIR)/bin/activate && python3 python/update_oscal_version.py
	@echo "Enhancing component definitions with FedRAMP Moderate/High controls..."
	@. $(VENV_DIR)/bin/activate && \
		COMP_DEF_DIR=$(TRESTLE_WORKSPACE)/component-definitions python3 python/update_component_definitions.py
	@echo "✅ Component definitions copied, updated, and enhanced"

# Clean targets (in reverse order of creation)
clean-catalogs:
	@echo "Removing catalogs from trestle workspace..."
	@cd $(TRESTLE_WORKSPACE) && rm -rf catalogs/NIST_SP-800-53_rev5
	@echo "✅ Catalogs removed"

clean-profiles:
	@echo "Removing profiles from trestle workspace..."
	@cd $(TRESTLE_WORKSPACE) && rm -rf profiles/fedramp-* profiles/dora
	@echo "✅ Profiles removed"

clean-resolve:
	@echo "Removing resolved catalogs..."
	@cd $(TRESTLE_WORKSPACE) && rm -rf catalogs/resolved-*
	@echo "✅ Resolved catalogs removed"

clean-mappings:
	@echo "Removing NIST to DORA mapping collection..."
	@rm -rf $(TRESTLE_WORKSPACE)/mapping-collections/nist-800-53-rev5-to-EU-Dora
	@echo "✅ Mapping collection removed"

clean-compdefs:
	@echo "Removing component definitions from trestle workspace..."
	@rm -rf $(TRESTLE_WORKSPACE)/component-definitions/Ubuntu_Linux_24_04_LTS
	@echo "✅ Component definitions removed"

create-ssps: clean-ssps venv ws create-xccdf create-compdefs
	@echo "Creating SSPs from component definitions and XCCDF inventory..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_ssps.py

clean-ssps:
	@echo "Removing all generated SSPs..."
	@rm -rf $(TRESTLE_WORKSPACE)/system-security-plans/Ubuntu-System-ssp-*
	@echo "✅ SSPs removed"

create-aps: clean-aps venv ws create-ssps
	@echo "Creating assessment plans from SSPs..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_assessment_plans.py

clean-aps:
	@echo "Removing all generated assessment plans..."
	@rm -rf $(TRESTLE_WORKSPACE)/assessment-plans/Ubuntu-System-ap-*
	@echo "✅ Assessment plans removed"

create-ars: clean-ars venv ws create-xccdf
	@echo "Creating assessment results from XCCDF scan files..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_assessment_results.py

clean-ars:
	@echo "Removing all generated assessment results..."
	@rm -rf $(TRESTLE_WORKSPACE)/assessment-results/Ubuntu-System-ar-*
	@echo "✅ Assessment results removed"

create-poams: clean-poams venv ws create-ars
	@echo "Creating POA&Ms from assessment results..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_poams.py

clean-poams:
	@echo "Removing all generated POA&Ms..."
	@rm -rf $(TRESTLE_WORKSPACE)/plan-of-action-and-milestones/Ubuntu-System-poam-*
	@echo "✅ POA&Ms removed"

charts: clean-charts venv ws create-ars
	@echo "Creating compliance status charts from assessment results..."
	@. $(VENV_DIR)/bin/activate && python3 python/create_assessment_result_charts.py

clean-charts:
	@echo "Removing all generated charts..."
	@rm -rf source-data/charts/*.png
	@echo "✅ Charts removed"

clean-oscal: clean-poams clean-ars clean-aps clean-ssps clean-compdefs clean-mappings clean-resolve clean-profiles clean-catalogs
	@echo "✅ All OSCAL documents removed"

# Artifacts targets - generate/clean all artifacts in correct order
artifacts: venv ws clean-xccdf create-xccdf create-oscal
	@echo ""
	@echo "=========================================="
	@echo "✅ All artifacts generated successfully!"
	@echo "=========================================="
	@echo "  XCCDF Results: source-data/xccdf-results/"
	@echo "  Catalogs: $(TRESTLE_WORKSPACE)/catalogs/"
	@echo "  Profiles: $(TRESTLE_WORKSPACE)/profiles/"
	@echo "  Resolved Catalogs: $(TRESTLE_WORKSPACE)/catalogs/resolved-*"
	@echo "  Mappings: $(TRESTLE_WORKSPACE)/mapping-collections/"
	@echo "  Component Definitions: $(TRESTLE_WORKSPACE)/component-definitions/"
	@echo "  SSPs: $(TRESTLE_WORKSPACE)/system-security-plans/"
	@echo "  Assessment Plans: $(TRESTLE_WORKSPACE)/assessment-plans/"
	@echo "  Assessment Results: $(TRESTLE_WORKSPACE)/assessment-results/"
	@echo "  POA&Ms: $(TRESTLE_WORKSPACE)/plan-of-action-and-milestones/"
	@echo "=========================================="

clean-artifacts: clean-xccdf clean-oscal
	@echo ""
	@echo "=========================================="
	@echo "✅ All artifacts cleaned successfully!"
	@echo "=========================================="

validate: venv ws
	@echo "Validating all OSCAL documents in trestle workspace..."
	@cd $(TRESTLE_WORKSPACE) && . ../$(VENV_DIR)/bin/activate && \
	trestle validate -a && \
	echo "✅ All OSCAL documents validated successfully!"

run: venv
	@. $(VENV_DIR)/bin/activate && python app.py

copy-images:
	@echo "Copying images to app-config/static/images..."
	@mkdir -p app-config/static/images
	@cp -f images/oscal-framework-layers.png app-config/static/images/
	@echo "✅ Images copied"

ws: venv copy-images
	@if [ ! -d "$(TRESTLE_WORKSPACE)" ]; then \
		mkdir -p $(TRESTLE_WORKSPACE); \
		cd $(TRESTLE_WORKSPACE) && . ../$(VENV_DIR)/bin/activate && trestle init; \
		cp -r source-data/catalogs/* $(TRESTLE_WORKSPACE)/catalogs/; \
		cp -r source-data/component-definitions/* $(TRESTLE_WORKSPACE)/component-definitions/; \
		cp -r source-data/profiles/* $(TRESTLE_WORKSPACE)/profiles/; \
	fi

clean-ws:
	@rm -rf $(TRESTLE_WORKSPACE)
	@echo "✅ Trestle workspace removed"

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		$(VENV_DIR)/bin/pip install --upgrade pip; \
		$(VENV_DIR)/bin/pip install -r requirements.txt; \
	fi

clean-venv:
	@rm -rf $(VENV_DIR)
	@echo "✅ Virtual environment removed"

# Made with Bob
