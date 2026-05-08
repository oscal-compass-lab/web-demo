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
Update OSCAL version in trestle workspace documents to match trestle's OSCAL_VERSION.
This script uses trestle API to update OSCAL versions in copied files.
"""

import sys
from pathlib import Path
from trestle_api import TrestleAPI
from trestle.oscal import OSCAL_VERSION


def main():
    """Main execution function"""
    print("=" * 80)
    print(f"OSCAL Version Updater - Target Version: {OSCAL_VERSION}")
    print("=" * 80)
    
    # Initialize Trestle API
    workspace = Path('trestle-workspace')
    if not workspace.exists():
        print(f"Error: Trestle workspace not found: {workspace}")
        return 1
    
    trestle_api = TrestleAPI(workspace)
    
    success_count = 0
    total_count = 0
    
    # Find all OSCAL JSON files in trestle workspace
    oscal_files = [
        *workspace.glob('catalogs/*/catalog.json'),
        *workspace.glob('profiles/*/profile.json'),
        *workspace.glob('component-definitions/*/component-definition.json'),
        *workspace.glob('mapping-collections/*/mapping-collection.json')
    ]
    
    print(f"\nFound {len(oscal_files)} OSCAL files to process\n")
    
    for file_path in oscal_files:
        total_count += 1
        if trestle_api.update_oscal_version(file_path):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully processed {success_count}/{total_count} files")
    print("=" * 80)
    
    return 0 if success_count == total_count else 1


if __name__ == '__main__':
    sys.exit(main())

# Made with Bob