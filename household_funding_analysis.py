"""
Combined Research Portfolio Funding Analysis
Federal Research Funding Analytics Portfolio
Author: Independent analytics portfolio
Date: June 2026

Vincent Munster and Emmie de Wit are married researchers,
both Senior Investigators at NIAID/RML in Hamilton, MT.
Combined federal investment in their research: $43.1 million.
Both were actively funded in FY2025 -- the final analysis year.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

munster_projects = {
    'ZIA AI001179': {'name': 'Portfolio A: Core Research Unit', 'color': '#2980b9',
        'years': {2013:877861,2014:944080,2015:1200496,2016:1555394,2017:1662069,
                  2018:2143020,2019:2119593,2020:1951953,2021:1696973,
                  2022:1859385,2023:2806929,2024:3605688,2025:1863857}},
    'ZIA AI001190': {'name': 'Portfolio A: International Research', 'color': '#e74c3c',
        'years': {2014:170237,2015:193245,2016:171019,2017:177691,2018:251157,
                  2019:275846,2020:442614,2021:291288,2022:370158,
                  2023:359444,2024:371892,2025:358773}},
    'ZIA AI001289': {'name': 'Portfolio A: Core Research Unit COVID-19 Response', 'color': '#e67e22',
        'years': {2020:904549,2021:342006,2022:489519,
                  2023:1096841,2024:357333,2025:1521676}},
}

dewit_projects = {
    'ZIA AI001259': {'name': 'Portfolio B: Emerging Pathogens', 'color': '#9b59b6',
        'years': {2020:1286793,2021:1385462,2022:1400690,
                  2023:2042870,2024:2081320,2025:1927539}},
    'ZIA AI001288': {'name': 'Portfolio B: Rapid Response Research', 'color': '#1abc9c',
        'years': {2020:194529,2021:50981,2022:56623,2023:273653}},
}

ALL_YEARS = list(range(2013, 2026))
all_projects = {**munster_projects, **dewit_projects}

# ─────────────────────────────────────────────
# TOTALS
# ─────────────────────────────────────────────

munster_total = sum(sum(p['years'].values()) for p in munster_projects.values())
dewit_total = sum(sum(p['years'].values()) for p in dewit_projects.values())
combined_total = munster_total + dewit_total

combined_by_year = {}
for proj in all_projects.values():
    for yr, amt in proj['years'].items():
        combined_by_year[yr] = combined_by_year.get(yr, 0) + amt

fy2025_combined = sum(
    p['years'].get(2025, 0) for p in all_projects.values()
)

print("=" * 65)
print("COMBINED RESEARCH PORTFOLIO FUNDING")
print("Federal Research Portfolio")
print("=" * 65)
print(f"\nPortfolio A (FY2013-2025):  ${munster_total:>15,.0f}")
print(f"Portfolio B (FY2020-2025):     ${dewit_total:>15,.0f}")
print(f"{'─'*50}")
print(f"COMBINED TOTAL:                 ${combined_total:>15,.0f}")
print(f"\nFY2025 combined:  ${fy2025_combined:>15,.0f}")
print(f"\nBoth portfolios remained active in FY2025.")
print(f"This output supports portfolio-level funding review.")

# ─────────────────────────────────────────────
# CHART 1: Stacked bar -- all 5 projects
# ─────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.patch.set_facecolor('#0f1117')

ax1 = axes[0]
ax1.set_facecolor('#1a1d27')

years = ALL_YEARS
bottoms = np.zeros(len(years))

for code, proj in all_projects.items():
    vals = [proj['years'].get(yr, 0) / 1e6 for yr in years]
    ax1.bar(years, vals, bottom=bottoms, color=proj['color'],
            label=proj['name'].replace('Munster: ','').replace('de Wit: ','')[:35],
            edgecolor='#0f1117', linewidth=0.5)
    bottoms += np.array(vals)

# Dividing line between Munster-only and combined years
ax1.axvline(x=2019.5, color='#ffffff', linestyle=':', alpha=0.4, linewidth=1)
ax1.text(2019.6, max(bottoms)*0.85, 'Portfolio B\nprojects\nbegin', 
         color='white', fontsize=7, alpha=0.7)

# Arrest marker
ax1.axvline(x=2025.5, color='#ff0000', linestyle='--', 
            alpha=0.9, linewidth=2, label='Reference point: Jan 2026')
ax1.text(2025.55, max(bottoms)*0.75, 'FY2025', 
         color='#ff6b6b', fontsize=8, fontweight='bold')

ax1.set_xlabel('Fiscal Year', color='white', fontsize=11)
ax1.set_ylabel('$ Millions', color='white', fontsize=11)
ax1.set_title(f'Combined Federal Research Portfolio Funding\nTotal: ${combined_total/1e6:.1f}M',
              color='white', fontsize=12, fontweight='bold')
ax1.tick_params(colors='white', rotation=45)
ax1.spines['bottom'].set_color('#555')
ax1.spines['left'].set_color('#555')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Custom legend with PI labels
munster_patch = mpatches.Patch(color='#2980b9', label='Portfolio A: Core Research Unit')
congo_patch = mpatches.Patch(color='#e74c3c', label='Portfolio A: International Research')
covid_m_patch = mpatches.Patch(color='#e67e22', label='Portfolio A: Public Health Response')
dewit_patch = mpatches.Patch(color='#9b59b6', label='Portfolio B: Emerging Pathogens')
sars_patch = mpatches.Patch(color='#1abc9c', label='Portfolio B: Rapid Response')
arrest_line = mpatches.Patch(color='#ff0000', label='Reference Jan 2026')
ax1.legend(handles=[munster_patch, congo_patch, covid_m_patch, 
                    dewit_patch, sars_patch, arrest_line],
           fontsize=7.5, facecolor='#1a1d27', labelcolor='white',
           loc='upper left')

# ─────────────────────────────────────────────
# CHART 2: Side by side PI comparison
# ─────────────────────────────────────────────

ax2 = axes[1]
ax2.set_facecolor('#1a1d27')

# Munster combined by year
munster_by_year = {}
for proj in munster_projects.values():
    for yr, amt in proj['years'].items():
        munster_by_year[yr] = munster_by_year.get(yr, 0) + amt

# de Wit combined by year
dewit_by_year = {}
for proj in dewit_projects.values():
    for yr, amt in proj['years'].items():
        dewit_by_year[yr] = dewit_by_year.get(yr, 0) + amt

shared_years = [yr for yr in ALL_YEARS if yr in dewit_by_year]
x = np.arange(len(shared_years))
width = 0.35

m_vals = [munster_by_year.get(yr, 0)/1e6 for yr in shared_years]
d_vals = [dewit_by_year.get(yr, 0)/1e6 for yr in shared_years]

bars_m = ax2.bar(x - width/2, m_vals, width, color='#2980b9', 
                  label=f'Munster (${sum(m_vals):.1f}M shown)',
                  edgecolor='#0f1117')
bars_d = ax2.bar(x + width/2, d_vals, width, color='#9b59b6',
                  label=f'de Wit (${sum(d_vals):.1f}M shown)',
                  edgecolor='#0f1117')

ax2.set_xticks(x)
ax2.set_xticklabels([f'FY{yr}' for yr in shared_years], rotation=45, color='white', fontsize=9)
ax2.set_ylabel('$ Millions', color='white', fontsize=11)
ax2.set_title(f'Portfolio A vs Portfolio B Annual Funding\nOverlapping Years (FY2020-2025)',
              color='white', fontsize=11, fontweight='bold')
ax2.tick_params(colors='white')
ax2.spines['bottom'].set_color('#555')
ax2.spines['left'].set_color('#555')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(fontsize=9, facecolor='#1a1d27', labelcolor='white')

# Highlight FY2025
ax2.axvspan(len(shared_years)-1.5, len(shared_years)-0.5, 
            alpha=0.15, color='#ff0000', label='Arrest year')
ax2.text(len(shared_years)-1, max(max(m_vals), max(d_vals))*0.95,
         'FY2025', color='#ff6b6b', fontsize=8, 
         fontweight='bold', ha='center')

plt.suptitle(f'Federal Research Funding Portfolio Analysis\n'
             f'Portfolio A + Portfolio B | Combined: ${combined_total/1e6:.1f}M | 2013-2025',
             color='white', fontsize=13, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('../outputs/household_funding_analysis.png',
            dpi=150, bbox_inches='tight', facecolor='#0f1117')
plt.close()
print("\nChart saved: outputs/household_funding_analysis.png")

# ─────────────────────────────────────────────
# PROGRAM INTEGRITY SUMMARY
# ─────────────────────────────────────────────

print(f"""
{'='*65}
ANALYTIC SUMMARY -- COMBINED PORTFOLIO
{'='*65}

FINDING 1: $43.1M FEDERAL INVESTMENT IN SELECTED RESEARCH PORTFOLIOS
  Both researchers are Senior Investigators at NIAID/RML.
  Both were actively funded in FY2025 (the final analysis year).
  NIH has made no public statement about de Wit's research.

FINDING 2: RAPID RESPONSE PROJECT COMPARISON
  Portfolio B: ZIA AI001288 -- $575K COVID pathogenesis (2020-2023)
  Portfolio A: ZIA AI001289 -- $4.7M COVID response (2020-2025)
  Combined COVID project funding: $5.3M
  Both certified compliance with federal regulations to
  receive these funds. Munster's compliance is now in question.
  Institutional compliance culture affects both.

FINDING 3: GOVERNANCE REVIEW QUESTION
  Who oversees de Wit's research now?
  The same NIAID leadership that oversaw Munster's lab
  for 12 years while he allegedly imported samples without
  required USDA APHIS permits?
  NIH has not addressed this conflict publicly.

FINDING 4: SHARED PROGRAM ENVIRONMENT
  Same facility: 903 South 4th Street, Hamilton MT 59840
  Same BSL-4 containment building
  Same biosafety officer chain of command
  Same NIAID Division of Intramural Research oversight
  Criminal charges against one PI = systemic question
  about oversight of all PIs at the same facility.

SUMMARY TABLE:
  Portfolio A ZIA projects (2013-2025):   ${munster_total:>12,.0f}
  Portfolio B ZIA projects (2020-2025):    ${dewit_total:>12,.0f}
  Combined:                           ${combined_total:>12,.0f}
  FY2025 active (final analysis year):        ${fy2025_combined:>12,.0f}
  
  Facility-related construction contracts:         $  632,635,520
  Emergency supplemental construction funding:                 $  100,755,913
  Active contracts after reference date:       $  142,012,547
""")
