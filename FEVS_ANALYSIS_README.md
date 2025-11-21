# FEVS 2024 Analysis - Setup & Run Guide

## Quick Start

### Step 1: Download the FEVS 2024 Data
1. Go to: https://www.opm.gov/fevs/reports/data-files/2024/2024-governmentwide-management-report/
2. Download the **"2024 FEVS Public Data File"** (CSV format)
3. Save it to: `C:\Users\hrobe\OneDrive\Desktop\EBM-Project-Rober5jh\`
4. Rename it to: `2024_FEVS_Prdf.csv` (or update the filename in the script)

### Step 2: Install Required Python Packages
```powershell
pip install pandas numpy matplotlib seaborn requests
```

### Step 3: Run the Analysis
```powershell
cd C:\Users\hrobe\OneDrive\Desktop\EBM-Project-Rober5jh
python fevs_analysis.py
```

## What the Script Does

### Answers Your Questions:

**Question 1: What is the average for employee engagement (X)?**
- Calculates % positive responses for 8 engagement variables
- Compares to your 62% baseline
- Identifies highest and lowest engagement areas

**Question 2: How do mid-level organizations compare?**
- Breaks down engagement by organization size
- Compares 100-500 employee orgs to others
- Shows where mid-level orgs rank

**Question 3: What patterns exist across groups?**
- Analyzes engagement by supervisory status
- Examines turnover intent patterns
- Identifies demographic trends

### Outputs Created:

1. **fevs_analysis_summary.png** - 4-panel visualization showing:
   - Engagement by question (X variables)
   - Organization size comparison
   - Supervisory status patterns
   - Summary scorecard with key findings

2. **fevs_engagement_summary.csv** - Detailed metrics table:
   - % positive responses per question
   - Mean scores
   - Number of responses
   - Ranked by engagement level

3. **fevs_size_comparison.csv** - Organization size benchmarks:
   - Average engagement by size category
   - Number of respondents per category

## Troubleshooting

### Error: "File not found"
- Make sure you downloaded the CSV from OPM
- Check the filename matches exactly: `2024_FEVS_Prdf.csv`
- Verify it's in the same folder as the script

### Error: "Module not found"
```powershell
pip install --upgrade pandas numpy matplotlib seaborn
```

### Want to use a different filename?
Edit line 26 in `fevs_analysis.py`:
```python
fevs_file = "YOUR_FILENAME_HERE.csv"
```

## Next Steps After Analysis

1. **Review the visualization** - Identify which engagement questions are below your 62% baseline

2. **Map to your X → M → Y framework:**
   - **X (Low engagement):** Questions with <62% positive responses
   - **M (Interventions):** Q40 (skills), Q42 (autonomy), Q14/Q15 (training)
   - **Y (Outcomes):** Overall satisfaction (Q69) + turnover intent

3. **Compare organization sizes** - See if mid-level orgs (your target) have unique patterns

4. **Prioritize improvements** - Focus M interventions on lowest-scoring X variables

## Integration with Your Dashboard

After running the analysis, you can:
1. Add the PNG visualization to your `index.html`
2. Reference the CSV benchmarks in your problem definition
3. Use the findings to refine your intervention targets
