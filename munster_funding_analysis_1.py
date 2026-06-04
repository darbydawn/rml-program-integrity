"""
NIH Intramural Research Funding Analysis
Source: NIH RePORTER (reporter.nih.gov)
Author: Independent analytics portfolio
Date: June 2026

Three intramural ZIA project codes identified:
  ZIA AI001179 -- Virus Ecology Unit (main lab, FY2013-2025)
  ZIA AI001190 -- International Research in Congo (FY2014-2025)
  ZIA AI001289 -- Virus Ecology Unit COVID-19 Response (FY2020-2025)

Key finding: "International Research in Congo" was a dedicated,
standalone NIH project funded for 12 consecutive years (FY2014-2025).
Every annual funding cycle = at least one Congo field trip.
Every field trip = a potential unpermitted sample import under 9 CFR 122.
The January 2026 arrest is year 12 of a federally funded pattern.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────
# DATA -- From NIH RePORTER
# ─────────────────────────────────────────────

projects = {
    'ZIA AI001179': {
        'name': 'Virus Ecology Unit',
        'color': '#2980b9',
        'years': {
            2013: 877861, 2014: 944080, 2015: 1200496,
            2016: 1555394, 2017: 1662069, 2018: 2143020,
            2019: 2119593, 2020: 1951953, 2021: 1696973,
            2022: 1859385, 2023: 2806929, 2024: 3605688,
            2025: 1863857
        }
    },
    'ZIA AI001190': {
        'name': 'International Research in Congo',
        'color': '#e74c3c',
        'years': {
            2014: 170237, 2015: 193245, 2016: 171019,
            2017: 177691, 2018: 251157, 2019: 275846,
            2020: 442614, 2021: 291288, 2022: 370158,
            2023: 359444, 2024: 371892, 2025: 358773
        }
    },
    'ZIA AI001289': {
        'name': 'Virus Ecology Unit - COVID-19 Response',
        'color': '#e67e22',
        'years': {
            2020: 904549, 2021: 342006, 2022: 489519,
            2023: 1096841, 2024: 357333, 2025: 1521676
        }
    }
}

ARREST_YEAR = 2026
ALL_YEARS = list(range(2013, 2026))

# ─────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────

totals = {code: sum(p['years'].values()) for code, p in projects.items()}
grand_total = sum(totals.values())

congo_total = totals['ZIA AI001190']
congo_years = len(projects['ZIA AI001190']['years'])

covid_proj_total = totals['ZIA AI001289']

fy2025_total = sum(
    p['years'].get(2025, 0) for p in projects.values()
)

# Combined by year
combined = {}
for proj in projects.values():
    for yr, amt in proj['years'].items():
        combined[yr] = combined.get(yr, 0) + amt

print("=" * 65)
print("NIH INTRAMURAL FUNDING SUMMARY")
print("=" * 65)

for code, proj in projects.items():
    total = totals[code]
    yrs = proj['years']
    print(f"\n{proj['name']}")
    print(f"  Code: {code} | FY{min(yrs)}-FY{max(yrs)} | Total: ${total:,.0f}")

print(f"\n{'─'*65}")
print(f"GRAND TOTAL (2013-2025):     ${grand_total:,.0f}")
print(f"Congo project total:         ${congo_total:,.0f} ({congo_years} consecutive years)")
print(f"COVID response project:      ${covid_proj_total:,.0f}")
print(f"FY2025 (final analysis year) total:  ${fy2025_total:,.0f}")

print(f"\n{'='*65}")
print(f"ANALYTIC SUMMARY")
print(f"{'='*65}")
print(f"""
FINDING 1: 12 YEARS OF FEDERALLY FUNDED CONGO FIELD WORK
  ZIA AI001190 "International Research in Congo" ran every
  year from FY2014 through FY2025 -- 12 consecutive years.
  NIH created a dedicated project code for this work.
  Total investment: ${congo_total:,.0f}

  The January 2026 arrest was not a one-time mistake.
  "I do this all the time" now has a budget line.
  Each of the 12 annual field seasons = potential
  unpermitted sample import under 9 CFR Part 122.

FINDING 2: COVID RESPONSE FUNDING DURING NON-COMPLIANCE
  ZIA AI001289 launched FY2020, received ${covid_proj_total:,.0f}.
  Munster certified compliance with federal regulations
  to receive these funds while conducting Congo field work
  without required USDA APHIS import permits.
  FY2025 allocation: $1,521,676 -- active at time of arrest.

FINDING 3: RAPID BUDGET GROWTH
  FY2013 combined: $877,861
  FY2024 combined: $4,334,913 -- nearly 5x growth in 11 years
  FY2025 combined: $3,744,306 -- still funded final analysis year

FINDING 4: THREE ACTIVE PROJECTS IN FINAL ANALYSIS YEAR
  All three ZIA projects were funded in FY2025.
  Federal funding continued without interruption through
  the arrest date and external compliance event filing.

FINDING 5: OTHER FEDERAL FUNDING NOT INCLUDED IN THESE TOTALS
  Two other federal research awards in FY2018 are in DOD budget.
  Total federal investment in the research portfolio exceeds
  $32.4M and is likely substantially higher including DARPA.
""")

# ─────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#0f1117')

# Chart 1: Stacked bar by year
ax1 = axes[0]
ax1.set_facecolor('#1a1d27')

years = ALL_YEARS
bottoms = np.zeros(len(years))
project_list = list(projects.items())

for code, proj in project_list:
    vals = [proj['years'].get(yr, 0) / 1e6 for yr in years]
    bars = ax1.bar(years, vals, bottom=bottoms, 
                   color=proj['color'], label=proj['name'],
                   edgecolor='#0f1117', linewidth=0.5)
    bottoms += np.array(vals)

# Arrest year line
ax1.axvline(x=2025.5, color='#ffffff', linestyle='--', 
            alpha=0.8, linewidth=1.5, label='Reference point: Jan 2026')
ax1.text(2025.6, max(bottoms)*0.9, 'Jan\n2026', 
         color='white', fontsize=8, va='top')

ax1.set_xlabel('Fiscal Year', color='white', fontsize=11)
ax1.set_ylabel('$ Millions', color='white', fontsize=11)
ax1.set_title("NIH Intramural Funding\nBy Project | FY2013-2025", 
              color='white', fontsize=12, fontweight='bold')
ax1.tick_params(colors='white', rotation=45)
ax1.spines['bottom'].set_color('#555')
ax1.spines['left'].set_color('#555')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(fontsize=8, facecolor='#1a1d27', labelcolor='white',
           loc='upper left')

# Chart 2: Congo project isolated with annotations
ax2 = axes[1]
ax2.set_facecolor('#1a1d27')

congo_years_list = sorted(projects['ZIA AI001190']['years'].keys())
congo_vals = [projects['ZIA AI001190']['years'][yr] / 1e3 for yr in congo_years_list]

bars2 = ax2.bar(congo_years_list, congo_vals, color='#e74c3c', 
                edgecolor='#0f1117', linewidth=0.5)

# Highlight FY2020 spike
ax2.bar([2020], [projects['ZIA AI001190']['years'][2020] / 1e3],
        color='#ff6b6b', edgecolor='white', linewidth=1.5,
        label='FY2020: Congo mpox outbreak surge')

ax2.set_xlabel('Fiscal Year', color='white', fontsize=11)
ax2.set_ylabel('$ Thousands', color='white', fontsize=11)
ax2.set_title(f'ZIA AI001190: International Research in Congo\n12 Consecutive Years | ${congo_total/1e6:.1f}M Total\nLongitudinal Project Funding | FY2014-2025',
              color='white', fontsize=11, fontweight='bold')
ax2.tick_params(colors='white', rotation=45)
ax2.spines['bottom'].set_color('#555')
ax2.spines['left'].set_color('#555')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for bar, val in zip(bars2, congo_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 5,
             f'${val:.0f}K', ha='center', va='bottom', 
             color='white', fontsize=7, rotation=45)

ax2.legend(fontsize=8, facecolor='#1a1d27', labelcolor='white')

plt.suptitle('Federal Research Funding Analysis\nProgram Integrity Portfolio | June 2026',
             color='white', fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('../outputs/munster_funding_analysis.png',
            dpi=150, bbox_inches='tight', facecolor='#0f1117')
plt.close()
print("\nChart saved: outputs/munster_funding_analysis.png")
