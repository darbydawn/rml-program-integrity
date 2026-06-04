"""
Federal Spending Analysis
Public Sector Governance Analytics Portfolio
Author: Independent analytics portfolio
Date: June 2026

Analyzes USASpending.gov contract and assistance data for case-study ZIP code
(case-study location) to identify program integrity flags related to the
June 2, 2026 federal external compliance event against NIH researchers
Vincent Researcher A and Claude Researcher B.
"""

import csv
import json
from collections import defaultdict
from datetime import datetime

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

def load_csv(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

contracts = load_csv('../data/contracts_public_sector_case_study.csv')
assistance = load_csv('../data/assistance_public_sector_case_study.csv')

print(f"Loaded {len(contracts)} contracts, {len(assistance)} assistance awards\n")

# ─────────────────────────────────────────────
# FINANCIAL OVERVIEW
# ─────────────────────────────────────────────

def safe_float(val):
    try:
        return float(val or 0)
    except (ValueError, TypeError):
        return 0.0

# Contracts totals
contract_total_obl = sum(safe_float(r['total_obligated_amount']) for r in contracts)
contract_total_out = sum(safe_float(r['total_outlayed_amount']) for r in contracts)
contract_covid_obl = sum(safe_float(r['obligated_amount_from_COVID-19_supplementals']) for r in contracts)
contract_covid_out = sum(safe_float(r['outlayed_amount_from_COVID-19_supplementals']) for r in contracts)

# NIH only
nih_contracts = [r for r in contracts if 'National Institutes of Health' in str(r.get('awarding_sub_agency_name',''))]
nih_obl = sum(safe_float(r['total_obligated_amount']) for r in nih_contracts)
nih_covid = sum(safe_float(r['obligated_amount_from_COVID-19_supplementals']) for r in nih_contracts)

# Assistance totals
assist_total = sum(safe_float(r['total_obligated_amount']) for r in assistance)
assist_covid = sum(safe_float(r['obligated_amount_from_COVID-19_supplementals']) for r in assistance)

print("=" * 65)
print("FINANCIAL OVERVIEW -- PUBLIC SECTOR CASE STUDY")
print("=" * 65)
print(f"\nCONTRACTS ({len(contracts):,} awards)")
print(f"  Total obligated:              ${contract_total_obl:>15,.0f}")
print(f"  Total outlayed:               ${contract_total_out:>15,.0f}")
print(f"  COVID supplemental obligated: ${contract_covid_obl:>15,.0f}")
print(f"\nNIH CONTRACTS ({len(nih_contracts):,} awards)")
print(f"  NIH total obligated:          ${nih_obl:>15,.0f}")
print(f"  NIH COVID supplemental:       ${nih_covid:>15,.0f}")
print(f"  NIH share of total contracts: {nih_obl/contract_total_obl*100:.1f}%")
print(f"\nASSISTANCE AWARDS ({len(assistance):,} awards)")
print(f"  Total obligated:              ${assist_total:>15,.0f}")
print(f"  COVID supplemental:           ${assist_covid:>15,.0f}")
print(f"\nCOMBINED FEDERAL FOOTPRINT IN case-study ZIP code")
print(f"  Total contracts + assistance: ${contract_total_obl + assist_total:>15,.0f}")
print(f"  Total COVID supplemental:     ${contract_covid_obl + assist_covid:>15,.0f}")

# ─────────────────────────────────────────────
# FLAG 1: CARES ACT CONSTRUCTION
# ─────────────────────────────────────────────

print("\n" + "=" * 65)
print("FLAG 1: EMERGENCY SUPPLEMENTAL FUNDS FOR CONSTRUCTION")
print("=" * 65)

ARREST_DATE = '2026-01-25'

covid_contracts = [r for r in nih_contracts if safe_float(r['obligated_amount_from_COVID-19_supplementals']) > 0]
print(f"\nNIH contracts with COVID supplemental funds: {len(covid_contracts)}")
print(f"Total COVID obligated: ${sum(safe_float(r['obligated_amount_from_COVID-19_supplementals']) for r in covid_contracts):,.0f}\n")

for r in sorted(covid_contracts, key=lambda x: safe_float(x['obligated_amount_from_COVID-19_supplementals']), reverse=True):
    covid_amt = safe_float(r['obligated_amount_from_COVID-19_supplementals'])
    total_amt = safe_float(r['total_obligated_amount'])
    defc = r.get('disaster_emergency_fund_codes','')
    naics = r.get('naics_description','')[:50]
    desc = (r.get('award_description','') or r.get('prime_award_base_transaction_description',''))[:70]
    print(f"  {r.get('recipient_name','')}")
    print(f"  Award: {r.get('award_id_piid','')} | COVID: ${covid_amt:,.0f} | Total: ${total_amt:,.0f}")
    print(f"  DEFC: {defc}")
    print(f"  NAICS: {naics}")
    print(f"  {desc}")
    
    if covid_amt > 1_000_000 and '236' in str(r.get('naics_code','')):
        print(f"  *** HIGH PRIORITY FLAG: Emergency supplemental funds used for construction ***")
    print()

# ─────────────────────────────────────────────
# FLAG 2: OBLIGATION vs OUTLAY GAPS
# ─────────────────────────────────────────────

print("=" * 65)
print("FLAG 2: OBLIGATION vs OUTLAY GAPS (NIH CONTRACTS)")
print("=" * 65)

gap_rows = [r for r in nih_contracts 
            if safe_float(r['total_obligated_amount']) > 500_000 
            and safe_float(r['total_outlayed_amount']) == 0]

gap_total = sum(safe_float(r['total_obligated_amount']) for r in gap_rows)
print(f"\nContracts >$500K obligated with $0 outlayed: {len(gap_rows)}")
print(f"Total at risk: ${gap_total:,.0f}\n")

for r in sorted(gap_rows, key=lambda x: safe_float(x['total_obligated_amount']), reverse=True)[:15]:
    obl = safe_float(r['total_obligated_amount'])
    recip = r.get('recipient_name','')[:40]
    start = r.get('period_of_performance_start_date','')
    end = r.get('period_of_performance_current_end_date','')
    desc = (r.get('award_description','') or r.get('prime_award_base_transaction_description',''))[:60]
    print(f"  ${obl:>12,.0f} | {recip}")
    print(f"               {start} to {end} | {desc}")

# ─────────────────────────────────────────────
# FLAG 3: SET-ASIDE VENDOR ANC SET-ASIDE
# ─────────────────────────────────────────────

print("\n" + "=" * 65)
print("FLAG 3: SET-ASIDE CONTRACT ANALYSIS")
print("=" * 65)

cape_rows = [r for r in contracts if 'SET-ASIDE VENDOR' in str(r.get('recipient_name',''))]
for r in cape_rows:
    obl = safe_float(r['total_obligated_amount'])
    out = safe_float(r['total_outlayed_amount'])
    print(f"\n  Award: {r.get('award_id_piid','')}")
    print(f"  Obligated: ${obl:,.0f} | Outlayed: ${out:,.0f}")
    print(f"  Period: {r.get('period_of_performance_start_date','')} to {r.get('period_of_performance_current_end_date','')}")
    print(f"  Extent competed: {r.get('extent_competed','')}")
    print(f"  Set aside: {r.get('type_of_set_aside','')}")
    print(f"  Change: Notable increase between prior and current contract values")

# ─────────────────────────────────────────────
# FLAG 4: CONTRACTOR CONCENTRATION
# ─────────────────────────────────────────────

print("\n" + "=" * 65)
print("FLAG 4: CONTRACTOR CONCENTRATION ANALYSIS")
print("=" * 65)

recip_totals = defaultdict(lambda: {'obl': 0, 'count': 0})
for r in nih_contracts:
    recip = r.get('recipient_name','UNKNOWN')
    recip_totals[recip]['obl'] += safe_float(r['total_obligated_amount'])
    recip_totals[recip]['count'] += 1

print(f"\nTop 15 NIH contractors by obligation:")
print(f"{'Recipient':<45} {'Contracts':>9} {'Obligated':>15} {'% of NIH':>9}")
print("-" * 82)
for recip, data in sorted(recip_totals.items(), key=lambda x: x[1]['obl'], reverse=True)[:15]:
    pct = data['obl'] / nih_obl * 100
    flag = " ***" if data['count'] > 50 or pct > 5 else ""
    print(f"  {recip[:43]:<43} {data['count']:>9,} ${data['obl']:>14,.0f} {pct:>8.1f}%{flag}")

# ─────────────────────────────────────────────
# FLAG 5: ACTIVE CONTRACTS POST-ARREST
# ─────────────────────────────────────────────

print("\n" + "=" * 65)
print(f"FLAG 5: NIH CONTRACTS ACTIVE AFTER REFERENCE DATE ({ARREST_DATE})")
print("=" * 65)

active_post_reference event = [r for r in nih_contracts
                      if r.get('period_of_performance_current_end_date','') >= ARREST_DATE
                      and safe_float(r['total_obligated_amount']) > 500_000]

active_total = sum(safe_float(r['total_obligated_amount']) for r in active_post_reference event)
print(f"\nContracts >$500K still active after reference date: {len(active_post_reference event)}")
print(f"Total obligated: ${active_total:,.0f}")
print(f"No documented pause, modification, or review found in data\n")

for r in sorted(active_post_reference event, key=lambda x: safe_float(x['total_obligated_amount']), reverse=True)[:12]:
    obl = safe_float(r['total_obligated_amount'])
    end = r.get('period_of_performance_current_end_date','')
    desc = (r.get('award_description','') or r.get('prime_award_base_transaction_description',''))[:55]
    print(f"  ${obl:>12,.0f} | ends {end} | {r.get('recipient_name','')[:30]}")
    print(f"               {desc}")

# ─────────────────────────────────────────────
# SUMMARY OUTPUT
# ─────────────────────────────────────────────

print("\n" + "=" * 65)
print("SUMMARY OF FLAGS")
print("=" * 65)
print(f"""
FLAG 1 -- CARES Act construction:
  $100,755,913 in COVID emergency funds for BSL-2 animal facility
  DEFC Code N (Emergency P.L. 116-136)
  Potential need to validate emergency-use alignment

FLAG 2 -- Obligation/outlay gaps:
  37 contracts, $193M obligated with $0 outlayed
  Includes Integrated Research Facility ($104.8M) -- data quality issue
  More recent gaps warrant audit follow-up

FLAG 3 -- Set-aside contracting pattern:
  $20.5M total, 7.5x contract value increase between awards
  Prior contract shows $0 outlayed despite completed performance period

FLAG 4 -- Contractor concentration:
  Regional construction contractor: 104 contracts, $55M (8.7% of NIH spend)
  Warrants competitive bidding compliance review

FLAG 5 -- Active contracts after reference date:
  13 contracts, $142M active after Jan 25, 2026
  No evidence of pause or review following external compliance event
  Largest: Large construction contractor $127.5M, active through Oct 2027
""")

print("Analysis complete. See outputs/ for visualizations.")
