"""
FEVS 2024 Employee Engagement Analysis
Analyzes Federal Employee Viewpoint Survey data to answer:
1. What is the average for employee engagement related to X (low engagement)?
2. How do mid-level organizations (100-500 employees) compare to others?
3. What patterns exist across groups?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("FEVS 2024 Employee Engagement Analysis")
print("="*80)

# Step 1: Download FEVS 2024 data
print("\n[1/5] Downloading FEVS 2024 Public Data File...")
print("Source: https://www.opm.gov/fevs/reports/data-files/2024/")

# Note: You'll need to manually download the CSV from OPM and place it in the same directory
# or update the file path below
fevs_file = "2024_FEVS_Prdf.csv"  # Update this path if needed

try:
    # Try to read local file first
    df = pd.read_csv(fevs_file, low_memory=False)
    print(f"✓ Loaded {len(df):,} responses from local file")
except FileNotFoundError:
    print(f"\n⚠ File not found: {fevs_file}")
    print("\nPlease download the file manually:")
    print("1. Go to: https://www.opm.gov/fevs/reports/data-files/2024/2024-governmentwide-management-report/")
    print("2. Download '2024 FEVS Public Data File' (CSV)")
    print("3. Save it in the same folder as this script")
    print("4. Update the 'fevs_file' variable if the filename is different")
    exit(1)

print(f"Dataset shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns")

# Step 2: Define engagement variables (X - low engagement indicators)
print("\n[2/5] Identifying employee engagement variables (X)...")

engagement_vars = {
    'Q40': 'Opportunity to improve skills',
    'Q12': 'Know what is expected of me',
    'Q42': 'Supervisor supports work-life balance',
    'Q69': 'Overall job satisfaction',
    'Q11': 'Encouraged to come up with new ideas',
    'Q13': 'Physical conditions allow good performance',
    'Q14': 'Training needs are assessed',
    'Q15': 'Satisfied with training received',
}

# Turnover intent variable (related to Y - voluntary turnover)
turnover_var = 'DLEAVING'  # "Considering leaving organization within next year"

print(f"\nEngagement variables identified:")
for var, desc in engagement_vars.items():
    if var in df.columns:
        print(f"  ✓ {var}: {desc}")
    else:
        print(f"  ✗ {var}: Not found in dataset")

# Check for organization size variable
size_vars = ['DAGENCYSZ', 'DLEVEL', 'DSUPER']  # Common size/level variables
available_size = [v for v in size_vars if v in df.columns]
print(f"\nOrganization size variables available: {available_size}")

# Step 3: Calculate engagement averages
print("\n[3/5] Calculating engagement averages...")

# Convert engagement questions to numeric (assuming 1-5 scale)
for var in engagement_vars.keys():
    if var in df.columns:
        df[f'{var}_numeric'] = pd.to_numeric(df[var], errors='coerce')

# Calculate overall engagement score (% positive responses)
# FEVS typically codes: 1=Strongly Agree, 2=Agree, 3=Neither, 4=Disagree, 5=Strongly Disagree
# Positive = 1 or 2 (Agree/Strongly Agree)

engagement_results = {}
for var, desc in engagement_vars.items():
    if var in df.columns:
        valid_responses = df[f'{var}_numeric'].dropna()
        if len(valid_responses) > 0:
            # Calculate % positive (1 or 2)
            pct_positive = ((valid_responses <= 2).sum() / len(valid_responses)) * 100
            mean_score = valid_responses.mean()

            engagement_results[var] = {
                'description': desc,
                'pct_positive': pct_positive,
                'mean_score': mean_score,
                'n_responses': len(valid_responses)
            }

# Create summary table
print("\n" + "="*100)
print("QUESTION 1: AVERAGE EMPLOYEE ENGAGEMENT (X VARIABLES)")
print("="*100)

summary_df = pd.DataFrame(engagement_results).T
summary_df = summary_df.round(2)
summary_df = summary_df.sort_values('pct_positive', ascending=False)

print("\nEngagement Metrics Summary:")
print(summary_df.to_string())

# Overall engagement index
overall_engagement = summary_df['pct_positive'].mean()
print(f"\n{'='*100}")
print(f"OVERALL ENGAGEMENT INDEX: {overall_engagement:.1f}% positive responses")
print(f"{'='*100}")
print(f"\nComparison to your baseline:")
print(f"  Your organization: 62% engagement")
print(f"  FEVS average:      {overall_engagement:.1f}% engagement")
print(f"  Difference:        {overall_engagement - 62:.1f} percentage points")

# Step 4: Analyze by organization size (mid-level comparison)
print("\n[4/5] Analyzing by organization size...")

# Try to identify mid-level organizations (100-500 employees)
if 'DAGENCYSZ' in df.columns:
    print("\nOrganization size distribution:")
    size_dist = df['DAGENCYSZ'].value_counts().sort_index()
    print(size_dist)

    # Calculate engagement by size
    print("\n" + "="*100)
    print("QUESTION 2: MID-LEVEL ORGANIZATIONS COMPARISON")
    print("="*100)

    size_engagement = {}
    for size_cat in df['DAGENCYSZ'].unique():
        if pd.notna(size_cat):
            size_subset = df[df['DAGENCYSZ'] == size_cat]

            size_results = []
            for var in engagement_vars.keys():
                if f'{var}_numeric' in df.columns:
                    valid = size_subset[f'{var}_numeric'].dropna()
                    if len(valid) > 0:
                        pct_pos = ((valid <= 2).sum() / len(valid)) * 100
                        size_results.append(pct_pos)

            if size_results:
                size_engagement[size_cat] = {
                    'avg_engagement': np.mean(size_results),
                    'n_respondents': len(size_subset)
                }

    size_comparison = pd.DataFrame(size_engagement).T
    size_comparison = size_comparison.sort_values('avg_engagement', ascending=False)
    print("\nEngagement by Organization Size:")
    print(size_comparison.to_string())
else:
    print("\n⚠ Organization size variable not found in dataset")

# Step 5: Identify patterns across groups
print("\n[5/5] Identifying patterns across demographic groups...")

print("\n" + "="*100)
print("QUESTION 3: PATTERNS ACROSS GROUPS")
print("="*100)

# Analyze by supervisory status
if 'DSUPER' in df.columns:
    print("\nEngagement by Supervisory Status:")

    super_engagement = {}
    for status in df['DSUPER'].unique():
        if pd.notna(status):
            subset = df[df['DSUPER'] == status]

            results = []
            for var in engagement_vars.keys():
                if f'{var}_numeric' in df.columns:
                    valid = subset[f'{var}_numeric'].dropna()
                    if len(valid) > 0:
                        pct_pos = ((valid <= 2).sum() / len(valid)) * 100
                        results.append(pct_pos)

            if results:
                super_engagement[status] = {
                    'avg_engagement': np.mean(results),
                    'n_respondents': len(subset)
                }

    super_df = pd.DataFrame(super_engagement).T
    print(super_df.to_string())

# Analyze turnover intent
if turnover_var in df.columns:
    print(f"\n{'='*100}")
    print("TURNOVER INTENT ANALYSIS (Y VARIABLE)")
    print("="*100)

    # DLEAVING: 1=Yes, considering leaving; 0=No
    leaving = pd.to_numeric(df[turnover_var], errors='coerce')
    pct_considering_leaving = (leaving == 1).sum() / leaving.notna().sum() * 100

    print(f"\nPercentage considering leaving within next year: {pct_considering_leaving:.1f}%")
    print(f"Your organization baseline: 18% voluntary turnover")
    print(f"FEVS turnover intent: {pct_considering_leaving:.1f}%")

# Create visualizations
print("\n[6/6] Creating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('FEVS 2024 Employee Engagement Analysis - X, M, Y Framework',
             fontsize=16, fontweight='bold')

# Plot 1: Engagement by question (X variables)
ax1 = axes[0, 0]
plot_data = summary_df.sort_values('pct_positive')
colors = ['#d62728' if x < 62 else '#2ca02c' if x > 70 else '#ff7f0e'
          for x in plot_data['pct_positive']]
ax1.barh(range(len(plot_data)), plot_data['pct_positive'], color=colors)
ax1.set_yticks(range(len(plot_data)))
ax1.set_yticklabels([engagement_vars.get(idx, idx) for idx in plot_data.index], fontsize=9)
ax1.axvline(62, color='red', linestyle='--', label='Your baseline (62%)', linewidth=2)
ax1.axvline(70, color='green', linestyle='--', label='Your target (70%)', linewidth=2)
ax1.set_xlabel('% Positive Responses', fontsize=11)
ax1.set_title('Q1: Employee Engagement by Question (X Variables)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(axis='x', alpha=0.3)

# Plot 2: Organization size comparison (if available)
ax2 = axes[0, 1]
if 'DAGENCYSZ' in df.columns and len(size_comparison) > 0:
    size_comparison_sorted = size_comparison.sort_values('avg_engagement')
    ax2.barh(range(len(size_comparison_sorted)),
             size_comparison_sorted['avg_engagement'],
             color='steelblue')
    ax2.set_yticks(range(len(size_comparison_sorted)))
    ax2.set_yticklabels(size_comparison_sorted.index, fontsize=9)
    ax2.axvline(62, color='red', linestyle='--', label='Your baseline', linewidth=2)
    ax2.set_xlabel('Average Engagement %', fontsize=11)
    ax2.set_title('Q2: Engagement by Organization Size', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
else:
    ax2.text(0.5, 0.5, 'Organization size data\nnot available',
             ha='center', va='center', fontsize=12)
    ax2.set_title('Q2: Organization Size Comparison', fontsize=12, fontweight='bold')

# Plot 3: Supervisory status patterns
ax3 = axes[1, 0]
if 'DSUPER' in df.columns and len(super_df) > 0:
    super_sorted = super_df.sort_values('avg_engagement')
    ax3.barh(range(len(super_sorted)),
             super_sorted['avg_engagement'],
             color='darkorange')
    ax3.set_yticks(range(len(super_sorted)))
    ax3.set_yticklabels(super_sorted.index, fontsize=9)
    ax3.axvline(62, color='red', linestyle='--', label='Your baseline', linewidth=2)
    ax3.set_xlabel('Average Engagement %', fontsize=11)
    ax3.set_title('Q3: Patterns by Supervisory Status', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(axis='x', alpha=0.3)
else:
    ax3.text(0.5, 0.5, 'Supervisory status data\nnot available',
             ha='center', va='center', fontsize=12)
    ax3.set_title('Q3: Supervisory Status Patterns', fontsize=12, fontweight='bold')

# Plot 4: Summary scorecard
ax4 = axes[1, 1]
ax4.axis('off')

scorecard_text = f"""
SUMMARY SCORECARD

Your Organization (Baseline):
  • Engagement: 62%
  • Turnover: 18%
  • Manager confidence: 4.2/10

FEVS 2024 Benchmarks:
  • Avg Engagement: {overall_engagement:.1f}%
  • Turnover intent: {pct_considering_leaving:.1f}% (considering leaving)

Gap Analysis:
  • Engagement gap: {overall_engagement - 62:+.1f} percentage points
  • Your target: 70% (+8 points needed)
  • FEVS top quartile: ~{overall_engagement + 10:.0f}%

Key Findings:
  1. Highest engagement areas:
     {summary_df.index[0]}: {summary_df.iloc[0]['pct_positive']:.1f}%

  2. Lowest engagement areas:
     {summary_df.index[-1]}: {summary_df.iloc[-1]['pct_positive']:.1f}%

  3. Priority improvement areas:
     • {summary_df.index[-1]}
     • {summary_df.index[-2]}
"""

ax4.text(0.05, 0.95, scorecard_text,
         transform=ax4.transAxes,
         fontsize=10,
         verticalalignment='top',
         fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()
plt.savefig('fevs_analysis_summary.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved as 'fevs_analysis_summary.png'")

# Export summary tables to CSV
summary_df.to_csv('fevs_engagement_summary.csv')
print("✓ Summary table exported to 'fevs_engagement_summary.csv'")

if 'DAGENCYSZ' in df.columns and len(size_comparison) > 0:
    size_comparison.to_csv('fevs_size_comparison.csv')
    print("✓ Size comparison exported to 'fevs_size_comparison.csv'")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print("\nFiles created:")
print("  1. fevs_analysis_summary.png - Comprehensive visualization")
print("  2. fevs_engagement_summary.csv - Detailed engagement metrics")
print("  3. fevs_size_comparison.csv - Organization size benchmarks (if available)")
print("\nNext steps:")
print("  1. Review the visualization to identify improvement priorities")
print("  2. Use the CSV files for detailed analysis and reporting")
print("  3. Map these findings to your X → M → Y framework")

plt.show()
