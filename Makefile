.PHONY: all venv help ws run validate create-catalogs create-profiles create-resolve create-mappings create-xccdf create-compdefs create-ssps create-aps create-ars create-poams create-oscal clean-catalogs clean-profiles clean-resolve clean-mappings clean-compdefs clean-ssps clean-aps clean-ars clean-poams clean-oscal clean-ws clean-venv

# Python virtual environment directory
VENV_DIR = .venv
TRESTLE_WORKSPACE = trestle-workspace

all: venv ws create-xccdf create-oscal validate run

help:
	@echo "Available targets:"
	@echo "  all            - Default target, sets up environment, validates, and runs app"
	@echo "  venv           - Create virtual environment and install dependencies from requirements.txt"
	@echo "  ws             - Create trestle-workspace and initialize trestle"
	@echo "  create-xccdf   - Generate XCCDF scan result files"
	@echo "  create-catalogs - Copy catalogs from source-data to trestle workspace"
	@echo "  create-profiles - Copy profiles from source-data to trestle workspace"
	@echo "  create-resolve - Resolve profiles to catalogs"
	@echo "  create-mappings - Create NIST to DORA mapping collection"
	@echo "  create-compdefs - Copy component definitions from source-data to trestle workspace"
	@echo "  create-ssps    - Generate SSPs from component definitions and XCCDF inventory"
	@echo "  create-aps     - Generate assessment plans from SSPs"
	@echo "  create-ars     - Generate assessment results from XCCDF scan files"
	@echo "  create-poams   - Generate POA&Ms from assessment results"
	@echo "  create-oscal   - Create all OSCAL documents (catalogs, profiles, resolve, mappings, compdefs, ssps, aps, ars, poams)"
	@echo "  validate       - Validate all OSCAL documents with trestle"
	@echo "  run            - Launch Flask application"
	@echo "  clean-catalogs - Remove catalogs from trestle workspace"
	@echo "  clean-profiles - Remove profiles from trestle workspace"
	@echo "  clean-resolve  - Remove resolved catalogs"
	@echo "  clean-mappings - Remove NIST to DORA mapping collection"
	@echo "  clean-compdefs - Remove component definitions from trestle workspace"
	@echo "  clean-ssps     - Remove all generated SSPs"
	@echo "  clean-aps      - Remove all generated assessment plans"
	@echo "  clean-ars      - Remove all generated assessment results"
	@echo "  clean-poams    - Remove all generated POA&Ms"
	@echo "  clean-oscal    - Remove all OSCAL documents (catalogs, profiles, resolve, mappings, compdefs, ssps, aps, ars, poams)"
	@echo "  clean-ws       - Remove trestle-workspace folder and contents"
	@echo "  clean-venv     - Remove virtual environment"

create-xccdf: venv ws
	@if [ ! -f "source-data/xccdf-results/ubuntu-web-01-xccdf-results.xml" ]; then \
		echo "Creating XCCDF scan result files..."; \
		. $(VENV_DIR)/bin/activate && python3 create_xccdf_results.py; \
	else \
		echo "XCCDF results already exist: source-data/xccdf-results/"; \
	fi

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
	@echo "✅ Catalogs copied"

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
	@echo "✅ Profiles copied"

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
	@if [ ! -f "$(TRESTLE_WORKSPACE)/mapping-collections/nist-800-53-rev5-to-EU-Dora/mapping-collection.json" ]; then \
		echo "Creating NIST to DORA mapping collection..."; \
		. $(VENV_DIR)/bin/activate && python3 create_dora_nist_mapping.py; \
	else \
		echo "DORA mapping already exists: mapping-collections/nist-800-53-rev5-to-EU-Dora"; \
	fi

clean-mappings:
	@echo "Removing NIST to DORA mapping collection..."
	@rm -rf $(TRESTLE_WORKSPACE)/mapping-collections/nist-800-53-rev5-to-EU-Dora
	@echo "✅ Mapping collection removed"

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
	@echo "✅ Component definitions copied"

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
	@. $(VENV_DIR)/bin/activate && python3 create_ssps.py

clean-ssps:
	@echo "Removing all generated SSPs..."
	@rm -rf $(TRESTLE_WORKSPACE)/system-security-plans/Ubuntu-System-ssp-*
	@echo "✅ SSPs removed"

create-aps: clean-aps venv ws create-ssps
	@echo "Creating assessment plans from SSPs..."
	@. $(VENV_DIR)/bin/activate && python3 create_assessment_plans.py

clean-aps:
	@echo "Removing all generated assessment plans..."
	@rm -rf $(TRESTLE_WORKSPACE)/assessment-plans/Ubuntu-System-ap-*
	@echo "✅ Assessment plans removed"

create-ars: clean-ars venv ws create-xccdf
	@echo "Creating assessment results from XCCDF scan files..."
	@. $(VENV_DIR)/bin/activate && python3 create_assessment_results.py

clean-ars:
	@echo "Removing all generated assessment results..."
	@rm -rf $(TRESTLE_WORKSPACE)/assessment-results/Ubuntu-System-ar-*
	@echo "✅ Assessment results removed"

create-poams: clean-poams venv ws create-ars
	@echo "Creating POA&Ms from assessment results..."
	@. $(VENV_DIR)/bin/activate && python3 create_poams.py

clean-poams:
	@echo "Removing all generated POA&Ms..."
	@rm -rf $(TRESTLE_WORKSPACE)/plan-of-action-and-milestones/Ubuntu-System-poam-*
	@echo "✅ POA&Ms removed"

clean-oscal: clean-poams clean-ars clean-aps clean-ssps clean-compdefs clean-mappings clean-resolve clean-profiles clean-catalogs
	@echo "✅ All OSCAL documents removed"

validate: venv ws
	@echo "Validating all OSCAL documents in trestle workspace..."
	@cd $(TRESTLE_WORKSPACE) && . ../$(VENV_DIR)/bin/activate && \
	trestle validate -a && \
	echo "✅ All OSCAL documents validated successfully!"

run: venv ws create-resolve create-ssps validate
	@. $(VENV_DIR)/bin/activate && python app.py

ws: venv
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
