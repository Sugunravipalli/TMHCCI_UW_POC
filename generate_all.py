"""
TMHCCI POC - Synthetic Data Generator
Generates all 10 data sources for Snowflake ingestion.
"""

import csv
import os
import random
import json
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)  # Reproducible

BASE = Path(r"C:\Users\bharg\Downloads\OneDrive_2026-04-07\Tokio Marine\Tokio Marine POC - London\synthetic_data")

# =============================================================================
# MASTER DATA: Shared across all sources for entity linkage
# =============================================================================

BROKERS = [
    {"name": "Marsh McLennan", "contact": "James Whitfield", "email": "j.whitfield@marsh.com", "domain": "marsh.com"},
    {"name": "Aon plc", "contact": "Sarah Chen", "email": "s.chen@aon.com", "domain": "aon.com"},
    {"name": "Willis Towers Watson", "contact": "David Armstrong", "email": "d.armstrong@willistowerswatson.com", "domain": "willistowerswatson.com"},
    {"name": "Lockton Companies", "contact": "Emily Hartwell", "email": "e.hartwell@lockton.com", "domain": "lockton.com"},
    {"name": "Howden Group", "contact": "Michael Cross", "email": "m.cross@howdengroup.com", "domain": "howdengroup.com"},
    {"name": "Gallagher", "contact": "Rachel Foster", "email": "r.foster@ajg.com", "domain": "ajg.com"},
    {"name": "McGill and Partners", "contact": "Thomas Keane", "email": "t.keane@mcgillpartners.com", "domain": "mcgillpartners.com"},
    {"name": "Miller Insurance", "contact": "Charlotte Webb", "email": "c.webb@millerinsurance.com", "domain": "millerinsurance.com"},
    {"name": "BMS Group", "contact": "Andrew Patel", "email": "a.patel@bmsgroup.com", "domain": "bmsgroup.com"},
    {"name": "Ed Broking", "contact": "Laura Simpson", "email": "l.simpson@edbroking.com", "domain": "edbroking.com"},
]

UNDERWRITERS = [
    {"name": "Simon Button", "level": "SVP", "authority": 3, "max_net": 25_000_000, "max_tiv": 300_000_000},
    {"name": "Claire Hemsworth", "level": "Senior UW", "authority": 2, "max_net": 15_000_000, "max_tiv": 150_000_000},
    {"name": "Robert Tanner", "level": "Senior UW", "authority": 2, "max_net": 15_000_000, "max_tiv": 150_000_000},
    {"name": "Priya Nair", "level": "UW", "authority": 1, "max_net": 5_000_000, "max_tiv": 50_000_000},
    {"name": "James Whitlock", "level": "UW", "authority": 1, "max_net": 5_000_000, "max_tiv": 50_000_000},
]

OCCUPANCY_CLASSES = [
    "Retail - Shopping Centre", "Retail - Standalone", "Manufacturing - Light",
    "Manufacturing - Heavy", "Office - Class A", "Office - Class B",
    "Hospitality - Hotel", "Hospitality - Restaurant", "Warehouse - Distribution",
    "Warehouse - Cold Storage", "Technology - Data Centre", "Technology - Office Campus",
    "Healthcare - Hospital", "Healthcare - Clinic", "Education - University",
    "Food Processing", "Energy - Storage", "Energy - Renewable",
    "Agricultural - Processing", "Agricultural - Storage",
    "Real Estate - Mixed Use", "Real Estate - Residential Portfolio",
    "Pharmaceutical - Manufacturing", "Pharmaceutical - R&D",
    "Automotive - Manufacturing", "Automotive - Dealership",
]

CONSTRUCTION_TYPES = [
    "Fire Resistive", "Non-Combustible", "Joisted Masonry",
    "Heavy Timber", "Wood Frame", "Mixed",
]

US_STATES = {
    "FL": "Florida", "TX": "Texas", "CA": "California", "NY": "New York",
    "IL": "Illinois", "OH": "Ohio", "PA": "Pennsylvania", "GA": "Georgia",
    "NC": "North Carolina", "VA": "Virginia", "NJ": "New Jersey",
    "MA": "Massachusetts", "WA": "Washington", "CO": "Colorado",
    "TN": "Tennessee", "MN": "Minnesota", "WI": "Wisconsin",
    "IN": "Indiana", "MI": "Michigan", "MO": "Missouri",
    "SC": "South Carolina", "LA": "Louisiana", "AL": "Alabama",
    "CT": "Connecticut", "OR": "Oregon", "AZ": "Arizona",
}

UK_CITIES = ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Edinburgh", "Bristol", "Liverpool"]

LOSS_TYPES = [
    ("Fire", 0.20, 350000), ("Wind/Hurricane", 0.15, 800000),
    ("Water Damage", 0.20, 125000), ("Hail", 0.10, 200000),
    ("Theft/Vandalism", 0.08, 75000), ("Equipment Breakdown", 0.10, 150000),
    ("Flood", 0.05, 500000), ("Earthquake", 0.02, 1000000),
    ("Collapse", 0.03, 400000), ("Lightning", 0.04, 100000),
    ("Smoke Damage", 0.03, 80000),
]

DECLINE_REASONS = [
    "Outside appetite - territory concentration in Tier 1 wind zones",
    "Outside appetite - excluded occupancy class",
    "Rate inadequacy - broker target below minimum technical rate",
    "Excessive CAT exposure - aggregate PML exceeds tolerance",
    "Poor loss history - 5-year loss ratio exceeds 60%",
    "Incomplete submission - insufficient information to rate",
    "Capacity constraints - aggregate exposure limit reached for this territory",
    "Construction quality concerns - predominantly frame/wood construction",
    "Single location concentration risk exceeds net retention",
    "Reinsurance not available at viable economics",
]

# =============================================================================
# HERO SUBMISSIONS - 10 fully linked scenarios
# =============================================================================

HEROES = [
    {
        "id": "SUB-2026-0001", "insured": "Pacific Retail Group LLC",
        "insured_variants": ["Pacific Retail Group", "PACIFIC RETAIL GROUP LLC", "Pacific Retail Grp"],
        "tiv": 120_000_000, "locations": 47, "broker_idx": 1, "uw_idx": 0,
        "occupancy": "Retail - Shopping Centre", "construction": "Non-Combustible",
        "state": "GA", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-07-01", "premium": 504000, "rate": 0.42,
        "tech_rate": 0.45, "loss_ratio": 0.12, "num_claims": 1,
        "sprinklered": True, "year_built": 2008,
        "scenario": "Large retail portfolio, complete submission, clean history, slightly below technical but justified"
    },
    {
        "id": "SUB-2026-0002", "insured": "Acme Industrial Holdings Inc",
        "insured_variants": ["Acme Industrial Holdings", "ACME INDUSTRIAL", "Acme Industrial Hldgs"],
        "tiv": 45_000_000, "locations": 3, "broker_idx": 2, "uw_idx": 1,
        "occupancy": "Manufacturing - Heavy", "construction": "Mixed",
        "state": "OH", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-06-01", "premium": 247500, "rate": 0.55,
        "tech_rate": 0.65, "loss_ratio": 0.32, "num_claims": 2,
        "sprinklered": False, "year_built": 1978,
        "scenario": "Manufacturing, incomplete (missing loss runs), referred to senior UW for rate deviation"
    },
    {
        "id": "SUB-2026-0003", "insured": "Northern Manufacturing Co Ltd",
        "insured_variants": ["Northern Manufacturing", "NORTHERN MFG CO", "Northern Mfg Co Ltd"],
        "tiv": 28_000_000, "locations": 1, "broker_idx": 0, "uw_idx": 2,
        "occupancy": "Manufacturing - Light", "construction": "Fire Resistive",
        "state": "PA", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-04-01", "premium": 123200, "rate": 0.44,
        "tech_rate": 0.44, "loss_ratio": 0.0, "num_claims": 0,
        "sprinklered": True, "year_built": 2015,
        "scenario": "Renewal, clean history, straightforward, at technical rate"
    },
    {
        "id": "SUB-2026-0004", "insured": "Heritage Hotels International PLC",
        "insured_variants": ["Heritage Hotels International", "HERITAGE HOTELS INTL", "Heritage Hotels"],
        "tiv": 200_000_000, "locations": 12, "broker_idx": 3, "uw_idx": 0,
        "occupancy": "Hospitality - Hotel", "construction": "Fire Resistive",
        "state": "FL", "lead_follow": "Lead", "decision": "Declined",
        "eff_date": "2026-08-01", "premium": 0, "rate": 0,
        "tech_rate": 0.85, "loss_ratio": 0, "num_claims": 0,
        "sprinklered": True, "year_built": 2001,
        "scenario": "Coastal FL/Caribbean hotels, excessive CAT exposure, rate gap too wide, declined"
    },
    {
        "id": "SUB-2026-0005", "insured": "Western Distribution Corp",
        "insured_variants": ["Western Distribution", "WESTERN DISTRIBUTION CORP", "Western Dist Corp"],
        "tiv": 65_000_000, "locations": 8, "broker_idx": 4, "uw_idx": 1,
        "occupancy": "Warehouse - Distribution", "construction": "Non-Combustible",
        "state": "CO", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-05-01", "premium": 390000, "rate": 0.60,
        "tech_rate": 0.58, "loss_ratio": 0.47, "num_claims": 4,
        "sprinklered": True, "year_built": 2010,
        "scenario": "Renewal, prior claims, mixed experience, rate increase applied"
    },
    {
        "id": "SUB-2026-0006", "insured": "Cascade Technology Campus Inc",
        "insured_variants": ["Cascade Technology Campus", "CASCADE TECH CAMPUS", "Cascade Tech"],
        "tiv": 180_000_000, "locations": 2, "broker_idx": 5, "uw_idx": 0,
        "occupancy": "Technology - Data Centre", "construction": "Fire Resistive",
        "state": "WA", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-09-01", "premium": 630000, "rate": 0.35,
        "tech_rate": 0.38, "loss_ratio": 0.0, "num_claims": 0,
        "sprinklered": True, "year_built": 2020,
        "scenario": "High-value data centre, modern construction, below technical justified by quality"
    },
    {
        "id": "SUB-2026-0007", "insured": "Gulf Coast Energy Storage LLC",
        "insured_variants": ["Gulf Coast Energy Storage", "GULF COAST ENERGY", "Gulf Coast Energy Stg"],
        "tiv": 95_000_000, "locations": 5, "broker_idx": 6, "uw_idx": 0,
        "occupancy": "Energy - Storage", "construction": "Non-Combustible",
        "state": "TX", "lead_follow": "Lead", "decision": "Referred",
        "eff_date": "2026-07-01", "premium": 712500, "rate": 0.75,
        "tech_rate": 0.80, "loss_ratio": 0.15, "num_claims": 1,
        "sprinklered": True, "year_built": 2018,
        "scenario": "Energy sector, CAT-exposed TX coast, wind/flood risk, referred for senior review"
    },
    {
        "id": "SUB-2026-0008", "insured": "Midwest Agricultural Cooperative",
        "insured_variants": ["Midwest Agricultural Coop", "MIDWEST AG COOP", "Midwest Agri Cooperative"],
        "tiv": 35_000_000, "locations": 22, "broker_idx": 7, "uw_idx": 3,
        "occupancy": "Agricultural - Storage", "construction": "Heavy Timber",
        "state": "MN", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-06-01", "premium": 210000, "rate": 0.60,
        "tech_rate": 0.62, "loss_ratio": 0.25, "num_claims": 3,
        "sprinklered": False, "year_built": 1995,
        "scenario": "Many small locations, agricultural, hail exposure, clean enough to bind"
    },
    {
        "id": "SUB-2026-0009", "insured": "Atlantic Seafood Processing Inc",
        "insured_variants": ["Atlantic Seafood Processing", "ATLANTIC SEAFOOD PROC", "Atlantic Seafood"],
        "tiv": 50_000_000, "locations": 4, "broker_idx": 8, "uw_idx": 2,
        "occupancy": "Food Processing", "construction": "Joisted Masonry",
        "state": "MA", "lead_follow": "Lead", "decision": "Bound",
        "eff_date": "2026-03-01", "premium": 375000, "rate": 0.75,
        "tech_rate": 0.70, "loss_ratio": 0.58, "num_claims": 3,
        "sprinklered": True, "year_built": 1988,
        "scenario": "Renewal, prior large loss ($2M+ refrigeration failure), priced above technical"
    },
    {
        "id": "SUB-2026-0010", "insured": "Summit Office Partners LP",
        "insured_variants": ["Summit Office Partners", "SUMMIT OFFICE PARTNERS LP", "Summit Office"],
        "tiv": 75_000_000, "locations": 6, "broker_idx": 9, "uw_idx": 4,
        "occupancy": "Office - Class A", "construction": "Fire Resistive",
        "state": "NY", "lead_follow": "Follow", "decision": "Bound",
        "eff_date": "2026-10-01", "premium": 187500, "rate": 0.25,
        "tech_rate": 0.28, "loss_ratio": 0.05, "num_claims": 1,
        "sprinklered": True, "year_built": 2012,
        "scenario": "Follow placement, referencing lead terms from Chubb, clean office portfolio"
    },
]

def rand_date(start_year, end_year):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def fmt_money(val):
    return f"${val:,.0f}"

# =============================================================================
# SOURCE 5: PROMISED LINES (backbone - generate first)
# =============================================================================

def generate_promised_lines():
    print("Generating Source 5: Promised Lines...")
    outfile = BASE / "05_promised_lines" / "promised_lines.csv"

    rows = []
    pl_id = 1000

    # Hero submissions
    for h in HEROES:
        broker = BROKERS[h["broker_idx"]]
        uw = UNDERWRITERS[h["uw_idx"]]
        eff = datetime.strptime(h["eff_date"], "%Y-%m-%d")
        exp = eff + timedelta(days=365)
        sub_date = eff - timedelta(days=random.randint(30, 60))
        dec_date = sub_date + timedelta(days=random.randint(5, 20))

        rows.append({
            "promised_line_id": f"PL-{pl_id:05d}",
            "submission_id": h["id"],
            "submission_date": sub_date.strftime("%Y-%m-%d"),
            "insured_name": h["insured_variants"][0],
            "broker_name": broker["name"],
            "broker_contact": broker["contact"],
            "coverage_type": "Commercial Property",
            "effective_date": h["eff_date"],
            "expiry_date": exp.strftime("%Y-%m-%d"),
            "total_insured_value": h["tiv"],
            "limit_requested": min(h["tiv"], 25_000_000),
            "deductible": max(25000, int(h["tiv"] * 0.001)),
            "lead_follow": h["lead_follow"],
            "our_line_pct": 100 if h["lead_follow"] == "Lead" else random.choice([15, 20, 25]),
            "our_premium": h["premium"],
            "technical_premium": int(h["tiv"] * h["tech_rate"] / 100),
            "rate_per_million": h["rate"] * 10,
            "deviation_from_technical_pct": round((h["rate"] - h["tech_rate"]) / h["tech_rate"] * 100, 1) if h["tech_rate"] > 0 else 0,
            "decision": h["decision"],
            "decision_date": dec_date.strftime("%Y-%m-%d"),
            "decision_reason": "" if h["decision"] == "Bound" else (
                "Excessive CAT exposure - coastal concentration" if h["decision"] == "Declined"
                else "Referred to SVP - energy sector risk above authority"
            ),
            "underwriter_name": uw["name"],
            "authority_level": uw["level"],
            "referral_required": h["tiv"] > uw["max_tiv"] or abs((h["rate"] - h["tech_rate"]) / h["tech_rate"] * 100) > 15 if h["tech_rate"] > 0 else False,
            "decline_reason": DECLINE_REASONS[3] if h["decision"] == "Declined" else "",
            "ntu_reason": "",
            "bound_premium": h["premium"] if h["decision"] == "Bound" else 0,
            "bound_date": dec_date.strftime("%Y-%m-%d") if h["decision"] == "Bound" else "",
            "renewal_of": "",
            "fac_reinsurance_purchased": h["tiv"] > 100_000_000 and h["decision"] == "Bound",
            "fac_premium": int(h["premium"] * 0.15) if h["tiv"] > 100_000_000 and h["decision"] == "Bound" else 0,
            "number_of_locations": h["locations"],
            "primary_state": h["state"],
            "occupancy_class": h["occupancy"],
        })
        pl_id += 1

    # Generate 740 additional historical records
    decisions_weights = ["Bound"] * 50 + ["Declined"] * 25 + ["NTU"] * 15 + ["Referred"] * 5 + ["Expired"] * 5

    insured_names_pool = [
        "Apex Manufacturing Corp", "Bayside Properties LLC", "Central Valley Foods Inc",
        "Delta Warehousing Group", "Eastwood Retail Holdings", "Falcon Energy Partners",
        "Granite State Industries", "Highland Hospitality Group", "Imperial Tech Solutions",
        "Jasper Distribution LLC", "Kensington Real Estate Trust", "Lakewood Healthcare Systems",
        "Metro Commercial Partners", "Newport Industrial Corp", "Olympia Agricultural Co",
        "Pioneer Cold Storage Inc", "Quantum Data Systems LLC", "Ridgeway Office Parks",
        "Silverstone Automotive Group", "Timber Creek Manufacturing", "United Pharma Holdings",
        "Vanguard Logistics Corp", "Westfield Shopping Centres", "Xenon Technology Inc",
        "Yorkshire Building Materials", "Zenith Food Processing Corp",
        "Atlas Commercial Properties", "Beacon Light Industries", "Coastal Hospitality Group",
        "Dominion Storage Partners", "Eclipse Energy Holdings", "Frontier Agricultural Services",
        "Golden Gate Retail Corp", "Harbor Point Industries", "Ironclad Manufacturing LLC",
        "Junction City Warehousing", "Keystone Office Holdings", "Liberty Food Services Inc",
        "Meridian Healthcare Properties", "Northstar Distribution Co", "Omega Tech Campus LLC",
        "Platinum Automotive Corp", "Riverside Agricultural Coop", "Stonebridge Real Estate",
        "Trident Marine Processing", "Uptown Retail Partners", "Vista Energy Storage LLC",
        "Windmill Manufacturing Co", "Excalibur Property Trust", "Zephyr Logistics Holdings",
        "Albion Commercial Group", "Brunswick Industrial Corp", "Canterbury Hotels PLC",
        "Devonshire Properties Ltd", "Essex Food Manufacturing", "Fitzwilliam Office Trust",
        "Grosvenor Retail Holdings", "Hampshire Tech Parks Ltd", "Inverness Energy Group",
        "Kingsway Distribution Ltd", "Lancaster Manufacturing PLC", "Mayfair Hospitality Ltd",
        "Norfolk Agricultural Holdings", "Oxford Science Properties", "Portland Warehousing Inc",
        "Richmond Data Centres LLC", "Sheffield Steel Processing", "Trafalgar Real Estate",
        "Warwick Automotive Parts", "Exeter Healthcare Properties",
    ]

    for i in range(740):
        insured = random.choice(insured_names_pool)
        broker = random.choice(BROKERS)
        uw = random.choice(UNDERWRITERS)
        decision = random.choice(decisions_weights)
        occ = random.choice(OCCUPANCY_CLASSES)
        state = random.choice(list(US_STATES.keys()))
        tiv = random.choice([10, 15, 20, 25, 30, 40, 50, 65, 75, 85, 100, 120, 150, 200, 250]) * 1_000_000
        locations = random.randint(1, 50) if tiv > 50_000_000 else random.randint(1, 10)
        tech_rate = round(random.uniform(0.25, 1.20), 2)
        dev = round(random.uniform(-0.20, 0.10), 2)
        quoted_rate = round(tech_rate * (1 + dev), 2)
        premium = int(tiv * quoted_rate / 100) if decision in ("Bound", "Referred") else 0
        eff = rand_date(2021, 2026)
        exp = eff + timedelta(days=365)
        sub_date = eff - timedelta(days=random.randint(20, 90))
        dec_date = sub_date + timedelta(days=random.randint(3, 25))

        decline_reason = random.choice(DECLINE_REASONS) if decision == "Declined" else ""
        ntu_reason = random.choice(["Broker placed elsewhere", "Insured did not proceed", "Premium too high", "Coverage terms not acceptable"]) if decision == "NTU" else ""

        rows.append({
            "promised_line_id": f"PL-{pl_id:05d}",
            "submission_id": f"SUB-{eff.year}-{pl_id:04d}",
            "submission_date": sub_date.strftime("%Y-%m-%d"),
            "insured_name": insured,
            "broker_name": broker["name"],
            "broker_contact": broker["contact"],
            "coverage_type": "Commercial Property",
            "effective_date": eff.strftime("%Y-%m-%d"),
            "expiry_date": exp.strftime("%Y-%m-%d"),
            "total_insured_value": tiv,
            "limit_requested": min(tiv, 25_000_000),
            "deductible": max(25000, int(tiv * random.uniform(0.0005, 0.002))),
            "lead_follow": random.choice(["Lead"] * 7 + ["Follow"] * 3),
            "our_line_pct": random.choice([100, 50, 25, 20, 15]),
            "our_premium": premium,
            "technical_premium": int(tiv * tech_rate / 100),
            "rate_per_million": round(quoted_rate * 10, 2),
            "deviation_from_technical_pct": round(dev * 100, 1),
            "decision": decision,
            "decision_date": dec_date.strftime("%Y-%m-%d"),
            "decision_reason": decline_reason or ntu_reason,
            "underwriter_name": uw["name"],
            "authority_level": uw["level"],
            "referral_required": tiv > uw["max_tiv"] or abs(dev) > 0.15,
            "decline_reason": decline_reason,
            "ntu_reason": ntu_reason,
            "bound_premium": premium if decision == "Bound" else 0,
            "bound_date": dec_date.strftime("%Y-%m-%d") if decision == "Bound" else "",
            "renewal_of": f"PL-{random.randint(1000,1500):05d}" if random.random() < 0.3 else "",
            "fac_reinsurance_purchased": tiv > 100_000_000 and decision == "Bound" and random.random() > 0.3,
            "fac_premium": int(premium * random.uniform(0.10, 0.20)) if tiv > 100_000_000 and decision == "Bound" else 0,
            "number_of_locations": locations,
            "primary_state": state,
            "occupancy_class": occ,
        })
        pl_id += 1

    fields = list(rows[0].keys())
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {len(rows)} rows written to {outfile}")
    return rows


# =============================================================================
# SOURCE 8: CLAIMS DATA
# =============================================================================

def generate_claims(promised_lines):
    print("Generating Source 8: Claims Data...")
    outfile = BASE / "08_claims_data" / "claims.csv"

    bound_records = [r for r in promised_lines if r["decision"] == "Bound"]
    rows = []
    claim_id = 1

    # Hero claims
    hero_claims_map = {
        "SUB-2026-0001": [  # Pacific Retail - 1 small claim
            {"loss_type": "Fire", "paid": 125000, "reserved": 0, "desc": "Kitchen fire in food court unit, contained by sprinkler system. Minimal damage to adjacent units.", "date_offset": 120},
        ],
        "SUB-2026-0002": [  # Acme Industrial - 2 claims
            {"loss_type": "Fire", "paid": 85000, "reserved": 0, "desc": "Electrical fire in metalworking shop, caught early by night watchman. Equipment damage only.", "date_offset": 200},
            {"loss_type": "Water Damage", "paid": 200000, "reserved": 0, "desc": "Burst water main caused flooding in warehouse section. Inventory and flooring damage.", "date_offset": 450},
        ],
        "SUB-2026-0005": [  # Western Distribution - 4 claims
            {"loss_type": "Fire", "paid": 180000, "reserved": 0, "desc": "Forklift battery charging station fire. Building damage and 3 forklifts destroyed.", "date_offset": 90},
            {"loss_type": "Collapse", "paid": 95000, "reserved": 0, "desc": "Roof section collapse from accumulated snow load. Racking and stored goods damaged.", "date_offset": 280},
            {"loss_type": "Theft/Vandalism", "paid": 42000, "reserved": 0, "desc": "Break-in at distribution hub. Electronics and high-value goods stolen.", "date_offset": 400},
            {"loss_type": "Water Damage", "paid": 35000, "reserved": 0, "desc": "HVAC condensation leak damaged office area and server room.", "date_offset": 550},
        ],
        "SUB-2026-0007": [  # Gulf Coast Energy - 1 claim
            {"loss_type": "Wind/Hurricane", "paid": 145000, "reserved": 25000, "desc": "Tropical Storm damage to storage facility roofing and external piping. Partial operational shutdown.", "date_offset": 365},
        ],
        "SUB-2026-0008": [  # Midwest Ag Coop - 3 claims
            {"loss_type": "Hail", "paid": 78000, "reserved": 0, "desc": "Severe hail damaged metal roofing on 4 grain storage buildings.", "date_offset": 150},
            {"loss_type": "Lightning", "paid": 45000, "reserved": 0, "desc": "Lightning strike caused electrical surge, damaged grain drying equipment.", "date_offset": 320},
            {"loss_type": "Wind/Hurricane", "paid": 32000, "reserved": 0, "desc": "Straight-line winds damaged siding on 2 outbuildings.", "date_offset": 500},
        ],
        "SUB-2026-0009": [  # Atlantic Seafood - 3 claims including large loss
            {"loss_type": "Equipment Breakdown", "paid": 2100000, "reserved": 150000, "desc": "Catastrophic refrigeration system failure. Complete loss of cold storage inventory ($1.8M) plus equipment replacement and BI.", "date_offset": 180},
            {"loss_type": "Water Damage", "paid": 65000, "reserved": 0, "desc": "Processing floor drain backup, contamination of production area.", "date_offset": 400},
            {"loss_type": "Fire", "paid": 28000, "reserved": 0, "desc": "Small grease fire in smoking facility, contained quickly.", "date_offset": 600},
        ],
        "SUB-2026-0010": [  # Summit Office - 1 small claim
            {"loss_type": "Water Damage", "paid": 38000, "reserved": 0, "desc": "Pipe burst on 14th floor during weekend. Water damage to 3 floors of office space.", "date_offset": 250},
        ],
    }

    for sub_id, claims in hero_claims_map.items():
        hero = next(h for h in HEROES if h["id"] == sub_id)
        eff = datetime.strptime(hero["eff_date"], "%Y-%m-%d")
        for c in claims:
            loss_date = eff - timedelta(days=c["date_offset"])
            report_date = loss_date + timedelta(days=random.randint(1, 7))
            close_date = loss_date + timedelta(days=random.randint(30, 365)) if c["reserved"] == 0 else ""

            rows.append({
                "claim_id": f"CLM-{claim_id:06d}",
                "policy_id": f"POL-{sub_id.split('-')[2]}-{int(sub_id.split('-')[1]):04d}",
                "promised_line_id": next(pl["promised_line_id"] for pl in promised_lines if pl["submission_id"] == sub_id),
                "insured_name": hero["insured_variants"][random.randint(0, len(hero["insured_variants"])-1)],
                "loss_date": loss_date.strftime("%Y-%m-%d"),
                "report_date": report_date.strftime("%Y-%m-%d"),
                "close_date": close_date.strftime("%Y-%m-%d") if close_date else "",
                "claim_status": "Closed" if c["reserved"] == 0 else "Open",
                "loss_type": c["loss_type"],
                "loss_description": c["desc"],
                "location_state": hero["state"],
                "paid_amount": c["paid"],
                "reserved_amount": c["reserved"],
                "total_incurred": c["paid"] + c["reserved"],
                "deductible_applied": max(25000, int(hero["tiv"] * 0.001)),
                "recovery_amount": int(c["paid"] * random.uniform(0, 0.05)),
                "net_incurred": c["paid"] + c["reserved"] - int(c["paid"] * 0.02),
                "cause_of_loss": c["loss_type"],
                "cat_event_flag": c["loss_type"] in ("Wind/Hurricane", "Earthquake", "Flood"),
                "cat_event_name": "Tropical Storm" if c["loss_type"] == "Wind/Hurricane" else "",
                "large_loss_flag": (c["paid"] + c["reserved"]) > 250000,
            })
            claim_id += 1

    # Generate 350+ additional historical claims for non-hero bound policies
    for _ in range(360):
        rec = random.choice(bound_records)
        loss_type, _, avg_sev = random.choices(LOSS_TYPES, weights=[lt[1] for lt in LOSS_TYPES])[0]
        severity = int(avg_sev * random.uniform(0.2, 3.0))
        reserved = int(severity * random.uniform(0, 0.3)) if random.random() < 0.15 else 0
        loss_date = rand_date(2021, 2025)
        report_date = loss_date + timedelta(days=random.randint(1, 14))

        descs = {
            "Fire": ["Electrical fire in utility room", "Cooking fire spread to adjacent area", "Overheated machinery ignited nearby materials", "Welding sparks caused small fire"],
            "Wind/Hurricane": ["Hurricane wind damage to roofing and exterior", "Tropical storm caused debris impact damage", "High winds damaged signage and awnings"],
            "Water Damage": ["Pipe burst caused interior flooding", "Roof leak during heavy rain", "HVAC condensation leak", "Sprinkler malfunction caused water damage"],
            "Hail": ["Severe hailstorm damaged roofing and skylights", "Hail damage to vehicles in parking structure", "Hail cracked exterior cladding"],
            "Theft/Vandalism": ["Forced entry, electronics stolen", "Vandalism to exterior and lobby", "Copper wire theft from HVAC units"],
            "Equipment Breakdown": ["Compressor failure in HVAC system", "Elevator motor failure", "Generator failure during power outage", "Boiler malfunction"],
            "Flood": ["Flash flooding entered ground floor", "Storm surge caused basement flooding"],
            "Earthquake": ["Structural cracking from seismic event", "Foundation damage from earthquake"],
            "Collapse": ["Roof section collapsed under snow load", "Partial wall collapse"],
            "Lightning": ["Lightning strike damaged electrical systems", "Lightning caused transformer failure"],
            "Smoke Damage": ["Smoke damage from neighbouring property fire", "Internal smoke damage from electrical short"],
        }

        rows.append({
            "claim_id": f"CLM-{claim_id:06d}",
            "policy_id": f"POL-{rec['promised_line_id'][-5:]}",
            "promised_line_id": rec["promised_line_id"],
            "insured_name": rec["insured_name"],
            "loss_date": loss_date.strftime("%Y-%m-%d"),
            "report_date": report_date.strftime("%Y-%m-%d"),
            "close_date": (loss_date + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d") if reserved == 0 else "",
            "claim_status": "Closed" if reserved == 0 else "Open",
            "loss_type": loss_type,
            "loss_description": random.choice(descs.get(loss_type, ["Property damage"])),
            "location_state": rec.get("primary_state", random.choice(list(US_STATES.keys()))),
            "paid_amount": severity,
            "reserved_amount": reserved,
            "total_incurred": severity + reserved,
            "deductible_applied": int(rec.get("deductible", 25000)),
            "recovery_amount": int(severity * random.uniform(0, 0.05)),
            "net_incurred": severity + reserved,
            "cause_of_loss": loss_type,
            "cat_event_flag": loss_type in ("Wind/Hurricane", "Earthquake", "Flood"),
            "cat_event_name": "",
            "large_loss_flag": (severity + reserved) > 250000,
        })
        claim_id += 1

    fields = list(rows[0].keys())
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {len(rows)} claims written to {outfile}")
    return rows


# =============================================================================
# SOURCE 6: RATING DATA (ERS)
# =============================================================================

def generate_rating_data(promised_lines):
    print("Generating Source 6: Rating Data (ERS)...")
    outfile = BASE / "06_rating_data_ers" / "rating_data.csv"

    rated = [r for r in promised_lines if r["decision"] in ("Bound", "Referred")]
    rows = []
    rating_id = 1

    for rec in rated:
        tiv = rec["total_insured_value"]
        tech_prem = rec["technical_premium"]
        occ = rec["occupancy_class"]
        constr = random.choice(CONSTRUCTION_TYPES)
        sprinklered_pct = random.choice([0, 25, 50, 75, 85, 95, 100])
        year_built = random.randint(1960, 2024)

        base_rate = round(random.uniform(0.20, 0.50), 3)
        territory_factor = round(random.uniform(0.80, 1.80), 2)
        occupancy_factor = round(random.uniform(0.70, 2.00), 2)
        construction_factor = round(random.uniform(0.60, 1.50), 2)
        protection_factor = round(random.uniform(0.70, 1.30), 2)
        experience_mod = round(random.uniform(0.80, 1.25), 2)
        schedule_mod = round(random.uniform(0.85, 1.15), 2)
        uw_judgment = round(random.uniform(0.90, 1.10), 2)
        package_credit = round(random.uniform(0.90, 1.00), 2)

        cat_wind = round(random.uniform(0, 0.35), 3)
        cat_eq = round(random.uniform(0, 0.15), 3)
        cat_flood = round(random.uniform(0, 0.10), 3)

        rows.append({
            "rating_id": f"RAT-{rating_id:06d}",
            "promised_line_id": rec["promised_line_id"],
            "submission_id": rec["submission_id"],
            "insured_name": rec["insured_name"],
            "effective_date": rec["effective_date"],
            "coverage_type": "Commercial Property",
            "total_insured_value": tiv,
            "number_of_locations": rec["number_of_locations"],
            "primary_occupancy": occ,
            "primary_construction": constr,
            "primary_protection_class": random.randint(1, 10),
            "avg_year_built": year_built,
            "pct_sprinklered": sprinklered_pct,
            "base_rate": base_rate,
            "territory_factor": territory_factor,
            "occupancy_factor": occupancy_factor,
            "construction_factor": construction_factor,
            "protection_factor": protection_factor,
            "experience_mod": experience_mod,
            "schedule_mod": schedule_mod,
            "uw_judgment_factor": uw_judgment,
            "package_credit": package_credit,
            "technical_rate": round(rec["rate_per_million"] / 10, 4) if rec["rate_per_million"] else round(base_rate * territory_factor * occupancy_factor * construction_factor * protection_factor, 4),
            "technical_premium": tech_prem,
            "quoted_rate": round(rec["rate_per_million"] / 10, 4) if rec["rate_per_million"] else 0,
            "quoted_premium": rec["our_premium"],
            "deviation_pct": rec["deviation_from_technical_pct"],
            "cat_load_wind": cat_wind,
            "cat_load_earthquake": cat_eq,
            "cat_load_flood": cat_flood,
            "expense_ratio": round(random.uniform(0.28, 0.35), 3),
            "profit_margin": round(random.uniform(0.05, 0.15), 3),
            "layer_attachment": 0,
            "layer_limit": min(tiv, 25_000_000),
            "layer_premium": rec["our_premium"],
        })
        rating_id += 1

    fields = list(rows[0].keys())
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {len(rows)} rating records written to {outfile}")
    return rows


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TMHCCI POC - Synthetic Data Generation")
    print("=" * 60)

    pl = generate_promised_lines()
    claims = generate_claims(pl)
    ratings = generate_rating_data(pl)

    print("\n" + "=" * 60)
    print("Phase 1 complete: Structured CSVs generated")
    print("=" * 60)
