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
Create OSCAL Mapping Collection: NIST 800-53 Rev 5 to DORA
Uses transitive mapping through Harmonized controls:
  NIST 800-53 Rev 5 → Harmonized → DORA
Includes confidence scores and coverage metrics
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

print("Creating NIST 800-53 Rev 5 to DORA Mapping Collection...\n")

# Load Harmonized to DORA mapping
harmonized_dora_path = Path("source-data/mapping-collections/Harmonized-to-EU-Dora/mapping-collection.json")
with open(harmonized_dora_path) as f:
    harmonized_dora = json.load(f)

# Load Harmonized to NIST mapping
harmonized_nist_path = Path("source-data/mapping-collections/Harmonized-to-nist-800-53-rev5/mapping-collection.json")
with open(harmonized_nist_path) as f:
    harmonized_nist = json.load(f)

print(f"✓ Loaded Harmonized to DORA mapping: {len(harmonized_dora['mapping-collection']['mappings'])} mappings")
print(f"✓ Loaded Harmonized to NIST mapping: {len(harmonized_nist['mapping-collection']['mappings'])} mappings\n")

# Build Harmonized → DORA lookup (Harmonized control → DORA articles)
harmonized_to_dora = defaultdict(list)
for mapping in harmonized_dora['mapping-collection']['mappings']:
    for map_entry in mapping['maps']:
        for source in map_entry['sources']:
            harmonized_id = source['id-ref']
            for target in map_entry['targets']:
                dora_id = target['id-ref']
                harmonized_to_dora[harmonized_id].append({
                    'dora_id': dora_id,
                    'confidence': map_entry.get('confidence-score', {}).get('percentage', 0.5),
                    'coverage': map_entry.get('coverage', {}).get('target-coverage', 0.5),
                    'relationship': map_entry.get('relationship', 'intersects-with')
                })

# Build Harmonized → NIST lookup (Harmonized control → NIST controls)
harmonized_to_nist = defaultdict(list)
for mapping in harmonized_nist['mapping-collection']['mappings']:
    for map_entry in mapping['maps']:
        for source in map_entry['sources']:
            harmonized_id = source['id-ref']
            for target in map_entry['targets']:
                nist_id = target['id-ref']
                harmonized_to_nist[harmonized_id].append({
                    'nist_id': nist_id,
                    'confidence': map_entry.get('confidence-score', {}).get('percentage', 0.5),
                    'coverage': map_entry.get('coverage', {}).get('target-coverage', 0.5),
                    'relationship': map_entry.get('relationship', 'intersects-with')
                })

# Create transitive NIST → DORA mapping
nist_to_dora = defaultdict(lambda: defaultdict(list))

for harmonized_id in harmonized_to_dora.keys():
    if harmonized_id in harmonized_to_nist:
        for dora_info in harmonized_to_dora[harmonized_id]:
            for nist_info in harmonized_to_nist[harmonized_id]:
                # Calculate transitive confidence (multiply probabilities)
                transitive_confidence = dora_info['confidence'] * nist_info['confidence']
                # Calculate transitive coverage (minimum of both)
                transitive_coverage = min(dora_info['coverage'], nist_info['coverage'])
                
                nist_to_dora[nist_info['nist_id']][dora_info['dora_id']].append({
                    'via_harmonized': harmonized_id,
                    'confidence': transitive_confidence,
                    'coverage': transitive_coverage
                })

print(f"✓ Created transitive mappings for {len(nist_to_dora)} NIST controls\n")

# Create OSCAL mapping collection
mapping_collection = {
    "mapping-collection": {
        "uuid": str(uuid.uuid4()),
        "metadata": {
            "title": "NIST SP 800-53 Rev 5 to Digital Operational Resilience Act (DORA)",
            "last-modified": datetime.now(timezone.utc).isoformat(),
            "version": "1.0",
            "oscal-version": "1.2.1",
            "remarks": "Transitive mapping from NIST 800-53 Rev 5 to DORA through Harmonized Controls Framework"
        },
        "provenance": {
            "method": "automation",
            "matching-rationale": "semantic",
            "status": "draft",
            "mapping-description": "Mapping collection from NIST SP 800-53 Rev 5 to Digital Operational Resilience Act (DORA) created through transitive mapping via Harmonized controls"
        },
        "mappings": []
    }
}

# Create mapping entries for each NIST control
for nist_id in sorted(nist_to_dora.keys()):
    dora_mappings = nist_to_dora[nist_id]
    
    # Aggregate confidence and coverage for each DORA article
    dora_articles = {}
    for dora_id, paths in dora_mappings.items():
        # Use maximum confidence and coverage across all paths
        max_confidence = max(p['confidence'] for p in paths)
        max_coverage = max(p['coverage'] for p in paths)
        via_harmonized = [p['via_harmonized'] for p in paths]
        
        dora_articles[dora_id] = {
            'confidence': max_confidence,
            'coverage': max_coverage,
            'via_harmonized': via_harmonized
        }
    
    # Create map entries
    maps = []
    for dora_id, info in sorted(dora_articles.items()):
        map_entry = {
            "uuid": str(uuid.uuid4()),
            "relationship": "intersects-with",
            "sources": [
                {
                    "type": "control",
                    "id-ref": nist_id
                }
            ],
            "targets": [
                {
                    "type": "control",
                    "id-ref": dora_id
                }
            ],
            "props": [
                {
                    "name": "mapping-rationale",
                    "value": f"Transitive mapping via Harmonized controls: {', '.join(info['via_harmonized'])}",
                    "ns": "https://ibm.com/concert/ns/oscal"
                }
            ],
            "confidence-score": {
                "percentage": round(info['confidence'], 2)
            },
            "coverage": {
                "target-coverage": round(info['coverage'], 2)
            }
        }
        maps.append(map_entry)
    
    # Create the mapping
    mapping_entry = {
        "uuid": str(uuid.uuid4()),
        "source-resource": {
            "type": "catalog",
            "href": "trestle://catalogs/nist-800-53-rev5/catalog.json"
        },
        "target-resource": {
            "type": "catalog",
            "href": "trestle://catalogs/EU-Dora/catalog.json"
        },
        "maps": maps
    }
    
    mapping_collection["mapping-collection"]["mappings"].append(mapping_entry)
    
    print(f"✓ Mapped {nist_id}")
    print(f"  → {len(dora_articles)} DORA articles")
    avg_confidence = sum(c['confidence'] for c in dora_articles.values()) / len(dora_articles)
    avg_coverage = sum(c['coverage'] for c in dora_articles.values()) / len(dora_articles)
    print(f"  → Avg confidence: {avg_confidence:.2f}, Avg coverage: {avg_coverage:.2f}")

# Save mapping collection
mapping_dir = Path("trestle-workspace/mapping-collections/nist-800-53-rev5-to-EU-Dora")
mapping_dir.mkdir(parents=True, exist_ok=True)
mapping_file = mapping_dir / "mapping-collection.json"

with open(mapping_file, 'w') as f:
    json.dump(mapping_collection, f, indent=2)

print(f"\n✓ Mapping collection created successfully!")
print(f"  Location: {mapping_file}")
print(f"  Total NIST controls: {len(nist_to_dora)}")

# Count total DORA articles
total_dora = sum(len(dora_mappings) for dora_mappings in nist_to_dora.values())
unique_dora = len(set(dora_id for dora_mappings in nist_to_dora.values() for dora_id in dora_mappings.keys()))
print(f"  Total DORA article mappings: {total_dora}")
print(f"  Unique DORA articles: {unique_dora}")

# Made with Bob
