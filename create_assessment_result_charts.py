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
Create compliance status charts for assessment results.
Generates visual charts showing pass/fail statistics by regulation and by control.
"""

from pathlib import Path
import json
import re
from typing import Dict, List, Tuple
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Directories
ASSESSMENT_RESULTS_DIR = Path('trestle-workspace/assessment-results')
CHARTS_OUTPUT_DIR = Path('source-data/charts')

# Chart styling
COLORS = {
    'pass': '#27ae60',      # Green
    'fail': '#e74c3c',      # Red
    'satisfied': '#27ae60',
    'partially-satisfied': '#f39c12',  # Orange
    'not-satisfied': '#e74c3c'
}


def parse_control_description(description: str) -> Tuple[str, str, int, int]:
    """
    Parse control description to extract control ID, status, pass count, and fail count.
    
    Example: "ac-1: partially-satisfied (22 pass / 2 fail rule evaluations)"
    
    Returns:
        Tuple of (control_id, status, pass_count, fail_count)
    """
    # Extract control ID
    control_match = re.match(r'^([^:]+):', description)
    control_id = control_match.group(1) if control_match else 'unknown'
    
    # Extract status
    status_match = re.search(r':\s*(\S+)\s*\(', description)
    status = status_match.group(1) if status_match else 'unknown'
    
    # Extract pass/fail counts
    counts_match = re.search(r'\((\d+)\s+pass\s*/\s*(\d+)\s+fail', description)
    if counts_match:
        pass_count = int(counts_match.group(1))
        fail_count = int(counts_match.group(2))
    else:
        pass_count = 0
        fail_count = 0
    
    return control_id, status, pass_count, fail_count


def parse_assessment_result(ar_file: Path) -> Dict:
    """
    Parse an assessment result file and extract compliance statistics by control.
    
    Args:
        ar_file: Path to assessment-results.json file
    
    Returns:
        Dictionary with statistics
    """
    with open(ar_file) as f:
        data = json.load(f)
    
    ar = data.get('assessment-results', {})
    
    # Extract basic info
    metadata = ar.get('metadata', {})
    title = metadata.get('title', 'Unknown')
    
    # Get regulation and inventory count from props
    regulation = 'Unknown'
    inventory_count = 1  # Default to 1 if not found
    for prop in metadata.get('props', []):
        if prop.get('name') == 'regulation':
            regulation = prop.get('value', 'Unknown')
        elif prop.get('name') == 'assessment-subject-count':
            try:
                inventory_count = int(prop.get('value', '1'))
            except (ValueError, TypeError):
                inventory_count = 1
    
    # Parse control results
    controls = []
    results = ar.get('results', [])
    
    for result in results:
        reviewed_controls = result.get('reviewed-controls', {})
        control_selections = reviewed_controls.get('control-selections', [])
        
        for selection in control_selections:
            description = selection.get('description', '')
            control_id, status, pass_count, fail_count = parse_control_description(description)
            
            controls.append({
                'control_id': control_id,
                'status': status,
                'pass': pass_count,
                'fail': fail_count,
                'total': pass_count + fail_count
            })
    
    # Calculate summary statistics
    total_pass = sum(c['pass'] for c in controls)
    total_fail = sum(c['fail'] for c in controls)
    satisfied = sum(1 for c in controls if c['status'] == 'satisfied')
    partially_satisfied = sum(1 for c in controls if c['status'] == 'partially-satisfied')
    not_satisfied = sum(1 for c in controls if c['status'] == 'not-satisfied')
    
    # Calculate averages per inventory item
    avg_pass = total_pass / inventory_count if inventory_count > 0 else 0
    avg_fail = total_fail / inventory_count if inventory_count > 0 else 0
    
    return {
        'title': title,
        'regulation': regulation,
        'file': ar_file.name,
        'controls': controls,
        'inventory_count': inventory_count,
        'summary': {
            'total_controls': len(controls),
            'total_pass': total_pass,
            'total_fail': total_fail,
            'avg_pass': avg_pass,
            'avg_fail': avg_fail,
            'satisfied': satisfied,
            'partially_satisfied': partially_satisfied,
            'not_satisfied': not_satisfied
        }
    }


def create_regulation_summary_chart(stats: Dict, output_file: Path):
    """
    Create a summary chart for a regulation showing overall compliance status.
    
    Args:
        stats: Statistics dictionary
        output_file: Path to save the chart
    """
    summary = stats['summary']
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left chart: Control Status Distribution (Pie Chart)
    status_data = {
        'Satisfied': summary['satisfied'],
        'Partially Satisfied': summary['partially_satisfied'],
        'Not Satisfied': summary['not_satisfied']
    }
    
    # Filter out zero values
    status_data = {k: v for k, v in status_data.items() if v > 0}
    
    if status_data:
        labels = list(status_data.keys())
        sizes = list(status_data.values())
        colors = [COLORS.get(k.lower().replace(' ', '-'), '#95a5a6') for k in labels]
        
        wedges, texts, autotexts = ax1.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 11}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(13)
        
        ax1.set_title(f"Control Status Distribution\n({summary['total_controls']} controls)", 
                     fontsize=13, fontweight='bold', pad=15)
    
    # Right chart: Pass/Fail Distribution (Bar Chart) - Average per inventory item
    categories = ['Pass', 'Fail']
    values = [summary['avg_pass'], summary['avg_fail']]
    colors_list = [COLORS['pass'], COLORS['fail']]
    
    bars = ax2.bar(categories, values, color=colors_list, edgecolor='black', linewidth=1.5, width=0.6)
    
    # Add value labels on bars with both average and total
    inventory_count = stats.get('inventory_count', 1)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        if height > 0:
            total_val = summary['total_pass'] if i == 0 else summary['total_fail']
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}\n({total_val} total)',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Average Rule Evaluations per System', fontsize=12, fontweight='bold')
    total_evals = summary['total_pass'] + summary['total_fail']
    ax2.set_title(f"Rule Evaluation Results (Average per System)\n{inventory_count} systems assessed, {total_evals} total evaluations",
                 fontsize=12, fontweight='bold', pad=15)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Overall title
    fig.suptitle(f"{stats['regulation']} - Compliance Summary", 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Save figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Created regulation summary chart: {output_file}")


def create_control_detail_chart(stats: Dict, output_file: Path):
    """
    Create a detailed chart showing pass/fail for each control.
    
    Args:
        stats: Statistics dictionary
        output_file: Path to save the chart
    """
    controls = stats['controls']
    
    if not controls:
        print(f"  Warning: No controls to chart for {stats['regulation']}")
        return
    
    # Sort controls by control ID
    controls_sorted = sorted(controls, key=lambda x: x['control_id'])
    
    # Show all controls
    title_suffix = f" (All {len(controls)} controls)"
    
    # Create figure - adjust height based on number of controls
    fig_height = max(10, len(controls_sorted) * 0.25)
    fig, ax = plt.subplots(figsize=(16, fig_height))
    
    # Prepare data
    control_ids = [c['control_id'] for c in controls_sorted]
    pass_counts = [c['pass'] for c in controls_sorted]
    fail_counts = [c['fail'] for c in controls_sorted]
    
    # Create horizontal stacked bar chart
    y_pos = range(len(control_ids))
    
    bars1 = ax.barh(y_pos, pass_counts, color=COLORS['pass'], 
                    edgecolor='black', linewidth=0.5, label='Pass')
    bars2 = ax.barh(y_pos, fail_counts, left=pass_counts, color=COLORS['fail'],
                    edgecolor='black', linewidth=0.5, label='Fail')
    
    # Add value labels
    for i, (p, f) in enumerate(zip(pass_counts, fail_counts)):
        total = p + f
        if total > 0:
            # Pass label
            if p > 0:
                ax.text(p/2, i, str(p), ha='center', va='center', 
                       fontsize=9, fontweight='bold', color='white')
            # Fail label
            if f > 0:
                ax.text(p + f/2, i, str(f), ha='center', va='center',
                       fontsize=9, fontweight='bold', color='white')
            # Total label
            ax.text(total + max(pass_counts + fail_counts) * 0.02, i, f'{total}',
                   ha='left', va='center', fontsize=9, fontweight='bold')
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(control_ids, fontsize=10)
    ax.set_xlabel('Rule Evaluations', fontsize=12, fontweight='bold')
    ax.set_title(f"{stats['regulation']} - Control-Level Compliance{title_suffix}", 
                fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Invert y-axis to show first control at top
    ax.invert_yaxis()
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Created control detail chart: {output_file}")


def create_cross_regulation_comparison(all_stats: List[Dict], output_file: Path):
    """
    Create a comparison chart across all regulations.
    
    Args:
        all_stats: List of statistics dictionaries
        output_file: Path to save the chart
    """
    if not all_stats:
        return
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Prepare data
    regulations = [s['regulation'] for s in all_stats]
    total_controls = [s['summary']['total_controls'] for s in all_stats]
    satisfied = [s['summary']['satisfied'] for s in all_stats]
    partially_satisfied = [s['summary']['partially_satisfied'] for s in all_stats]
    not_satisfied = [s['summary']['not_satisfied'] for s in all_stats]
    
    # Left chart: Control Status by Regulation (Stacked Bar)
    x = range(len(regulations))
    width = 0.6
    
    bars1 = ax1.bar(x, satisfied, width, label='Satisfied',
                   color=COLORS['satisfied'], edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x, partially_satisfied, width, bottom=satisfied,
                   label='Partially Satisfied', color=COLORS['partially-satisfied'],
                   edgecolor='black', linewidth=1)
    bars3 = ax1.bar(x, not_satisfied, width,
                   bottom=[s+p for s, p in zip(satisfied, partially_satisfied)],
                   label='Not Satisfied', color=COLORS['not-satisfied'],
                   edgecolor='black', linewidth=1)
    
    # Add value labels on each segment
    for i, (sat, partial, notsat) in enumerate(zip(satisfied, partially_satisfied, not_satisfied)):
        # Satisfied segment (bottom)
        if sat > 0:
            ax1.text(i, sat/2, str(sat), ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
        # Partially satisfied segment (middle)
        if partial > 0:
            ax1.text(i, sat + partial/2, str(partial), ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
        # Not satisfied segment (top)
        if notsat > 0:
            ax1.text(i, sat + partial + notsat/2, str(notsat), ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
        # Total on top
        total = sat + partial + notsat
        if total > 0:
            ax1.text(i, total, str(total), ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='black')
    
    ax1.set_ylabel('Number of Controls', fontsize=12, fontweight='bold')
    ax1.set_title('Control Status Comparison Across Regulations',
                 fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(regulations, rotation=45, ha='right', fontsize=10)
    
    # Set y-axis limit to leave room for legend at top
    max_controls = max(total_controls)
    ax1.set_ylim(0, max_controls * 1.2)  # 20% headroom
    ax1.legend(fontsize=10, loc='upper right', framealpha=0.95)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Right chart: Pass/Fail by Regulation (Average per system)
    pass_counts = [s['summary']['avg_pass'] for s in all_stats]
    fail_counts = [s['summary']['avg_fail'] for s in all_stats]
    inventory_counts = [s.get('inventory_count', 1) for s in all_stats]
    
    x_pos = range(len(regulations))
    bar_width = 0.35
    
    bars1 = ax2.bar([i - bar_width/2 for i in x_pos], pass_counts, bar_width,
                   label='Pass', color=COLORS['pass'], edgecolor='black', linewidth=1)
    bars2 = ax2.bar([i + bar_width/2 for i in x_pos], fail_counts, bar_width,
                   label='Fail', color=COLORS['fail'], edgecolor='black', linewidth=1)
    
    # Add value labels showing average
    for i, (p, f) in enumerate(zip(pass_counts, fail_counts)):
        if p > 0:
            ax2.text(i - bar_width/2, p, f'{p:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        if f > 0:
            ax2.text(i + bar_width/2, f, f'{f:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax2.set_ylabel('Average Rule Evaluations per System', fontsize=12, fontweight='bold')
    ax2.set_title('Rule Evaluation Results Across Regulations\n(Average per system assessed)',
                 fontsize=12, fontweight='bold', pad=15)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(regulations, rotation=45, ha='right', fontsize=10)
    
    # Set y-axis limit to leave room for legend at top
    max_pass = max(pass_counts) if pass_counts else 0
    max_fail = max(fail_counts) if fail_counts else 0
    max_val = max(max_pass, max_fail)
    ax2.set_ylim(0, max_val * 1.25)  # 25% headroom
    ax2.legend(fontsize=10, loc='upper right', framealpha=0.95)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Overall title
    fig.suptitle('Cross-Regulation Compliance Comparison',
                fontsize=16, fontweight='bold', y=0.98)
    
    # Save figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Created cross-regulation comparison chart: {output_file}")


def main():
    """Main execution function"""
    print("=" * 80)
    print("Assessment Result Charts Generator")
    print("=" * 80)
    
    # Create output directory
    CHARTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all assessment result files
    if not ASSESSMENT_RESULTS_DIR.exists():
        print(f"Error: Assessment results directory not found: {ASSESSMENT_RESULTS_DIR}")
        print("Run 'python3 create_assessment_results.py' first to generate assessment results.")
        return
    
    ar_files = sorted(ASSESSMENT_RESULTS_DIR.glob('*/assessment-results.json'))
    
    if not ar_files:
        print(f"Error: No assessment result files found in {ASSESSMENT_RESULTS_DIR}")
        return
    
    print(f"\nFound {len(ar_files)} assessment result files\n")
    
    all_stats = []
    
    # Process each assessment result
    for ar_file in ar_files:
        ar_name = ar_file.parent.name
        print(f"Processing: {ar_name}")
        
        # Parse assessment result
        stats = parse_assessment_result(ar_file)
        all_stats.append(stats)
        
        print(f"  Regulation: {stats['regulation']}")
        print(f"  Total controls: {stats['summary']['total_controls']}")
        print(f"  Satisfied: {stats['summary']['satisfied']}, "
              f"Partially: {stats['summary']['partially_satisfied']}, "
              f"Not Satisfied: {stats['summary']['not_satisfied']}")
        print(f"  Total evaluations: Pass={stats['summary']['total_pass']}, "
              f"Fail={stats['summary']['total_fail']}")
        
        # Create charts for this regulation
        base_name = ar_name.replace('Ubuntu-System-ar-', '')
        
        # Regulation summary chart
        summary_file = CHARTS_OUTPUT_DIR / f"{base_name}-summary.png"
        create_regulation_summary_chart(stats, summary_file)
        
        # Control detail chart
        detail_file = CHARTS_OUTPUT_DIR / f"{base_name}-controls.png"
        create_control_detail_chart(stats, detail_file)
        
        print()
    
    # Create cross-regulation comparison
    if len(all_stats) > 1:
        comparison_file = CHARTS_OUTPUT_DIR / "cross-regulation-comparison.png"
        create_cross_regulation_comparison(all_stats, comparison_file)
    
    print("=" * 80)
    print(f"✓ Successfully created charts in {CHARTS_OUTPUT_DIR}/")
    print(f"  Regulations processed: {len(all_stats)}")
    print(f"  Charts per regulation: 2 (summary + control detail)")
    print(f"  Cross-regulation comparison: 1")
    print(f"  Total charts: {len(all_stats) * 2 + 1}")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob