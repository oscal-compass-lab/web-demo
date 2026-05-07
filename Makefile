.PHONY: all venv clean help ws ws-clean resolve run create-docs validate create-mappings create-xccdf

# Python virtual environment directory
VENV_DIR = .venv
TRESTLE_WORKSPACE = trestle-workspace

all: venv ws resolve create-xccdf create-mappings create-docs validate run

help:
	@echo "Available targets:"
	@echo "  all            - Default target, sets up environment, validates, and runs app"
	@echo "  venv           - Create virtual environment and install dependencies from requirements.txt"
	@echo "  ws             - Create trestle-workspace and initialize trestle"
	@echo "  resolve        - Resolve profiles to catalogs"
	@echo "  create-xccdf   - Generate XCCDF scan result files"
	@echo "  create-mappings - Create NIST to DORA mapping collection"
	@echo "  create-docs    - Generate SSP documents from component definitions"
	@echo "  validate       - Validate all OSCAL documents with trestle"
	@echo "  run            - Launch Flask application"
	@echo "  ws-clean       - Remove trestle-workspace folder and contents"
	@echo "  clean          - Remove virtual environment"

create-xccdf: venv ws
	@if [ ! -f "source-data/xccdf-results/ubuntu-web-01-xccdf-results.xml" ]; then \
		echo "Creating XCCDF scan result files..."; \
		. $(VENV_DIR)/bin/activate && python3 create_xccdf_results.py; \
	else \
		echo "XCCDF results already exist: source-data/xccdf-results/"; \
	fi

resolve: venv ws
	@cd $(TRESTLE_WORKSPACE) && \
	for profile in $$(ls -1 profiles 2>/dev/null | grep -v '.keep' || true); do \
		output_name="resolved-$$profile"; \
		if [ ! -d "catalogs/$$output_name" ]; then \
			. ../$(VENV_DIR)/bin/activate && \
			trestle author profile-resolve -n "$$profile" -o "$$output_name"; \
		fi; \
	done

create-mappings: venv ws
	@if [ ! -f "$(TRESTLE_WORKSPACE)/mapping-collections/nist-800-53-rev5-to-EU-Dora/mapping-collection.json" ]; then \
		echo "Creating NIST to DORA mapping collection..."; \
		. $(VENV_DIR)/bin/activate && python3 create_dora_nist_mapping.py; \
	else \
		echo "DORA mapping already exists: mapping-collections/nist-800-53-rev5-to-EU-Dora"; \
	fi

create-docs: resolve create-mappings
	@echo "SSP documents already exist (profile-specific SSPs maintained separately)"
	@echo "Available SSPs:"
	@ls -1 $(TRESTLE_WORKSPACE)/system-security-plans/ 2>/dev/null | grep -v '.keep' || echo "  None found"

validate: venv ws
	@echo "Validating all OSCAL documents in trestle workspace..."
	@cd $(TRESTLE_WORKSPACE) && . ../$(VENV_DIR)/bin/activate && \
	trestle validate -a && \
	echo "✅ All OSCAL documents validated successfully!"

run: venv ws resolve create-docs validate
	@. $(VENV_DIR)/bin/activate && python app.py

ws: venv
	@if [ ! -d "$(TRESTLE_WORKSPACE)" ]; then \
		mkdir -p $(TRESTLE_WORKSPACE); \
		cd $(TRESTLE_WORKSPACE) && . ../$(VENV_DIR)/bin/activate && trestle init; \
		cp -r source-data/catalogs/* $(TRESTLE_WORKSPACE)/catalogs/; \
		cp -r source-data/component-definitions/* $(TRESTLE_WORKSPACE)/component-definitions/; \
		cp -r source-data/profiles/* $(TRESTLE_WORKSPACE)/profiles/; \
	fi

ws-clean:
	@rm -rf $(TRESTLE_WORKSPACE)

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		$(VENV_DIR)/bin/pip install --upgrade pip; \
		$(VENV_DIR)/bin/pip install -r requirements.txt; \
	fi

clean:
	@rm -rf $(VENV_DIR)

# Made with Bob
