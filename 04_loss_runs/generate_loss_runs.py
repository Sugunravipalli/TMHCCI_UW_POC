"""
Generate 10 realistic Loss Run report text files for Tokio Marine HCC
commercial property underwriting POC.
"""

import os
from datetime import date

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Helper: format currency
# ---------------------------------------------------------------------------
def fmt(amount):
    """Format integer dollars as $XXX,XXX."""
    if amount == 0:
        return "$0"
    return f"${amount:,.0f}"


# ---------------------------------------------------------------------------
# Helper: build the full loss-run text
# ---------------------------------------------------------------------------
def build_loss_run(
    carrier,
    policy_number,
    insured_name,
    policy_start,
    policy_end,
    report_date,
    broker,
    claims,            # list of dicts
    annual_premium,    # dict  year_label -> premium
    adjuster_name,
    extra_footer_lines=None,
):
    """
    claims: list of dict with keys
        claim_no, date_of_loss, loss_type, status, paid, reserved, description
    annual_premium: dict  "YYYY-YYYY" -> int premium
    """

    SEP  = "=" * 96
    DSEP = "-" * 96

    lines = []
    lines.append(SEP)
    lines.append(f"{'LOSS RUN REPORT':^96}")
    lines.append(SEP)
    lines.append(f"Issuing Carrier:   {carrier}")
    lines.append(f"Policy Number:     {policy_number}")
    lines.append(f"Named Insured:     {insured_name}")
    lines.append(f"Policy Period:     {policy_start} to {policy_end}")
    lines.append(f"Report Date:       {report_date}")
    lines.append(f"Prepared For:      {broker}")
    lines.append(SEP)
    lines.append("")

    # ---- Claim detail section ------------------------------------------------
    lines.append("CLAIM DETAIL")
    lines.append(DSEP)

    hdr = (
        f"{'Claim #':<12}| {'Date of Loss':<14}| {'Type':<17}| {'Status':<9}"
        f"| {'Paid':<12}| {'Reserved':<12}| {'Total Incurred':<17}| Description"
    )
    lines.append(hdr)
    lines.append(
        f"{'-'*12}|{'-'*14}|{'-'*17}|{'-'*9}"
        f"|{'-'*12}|{'-'*12}|{'-'*17}|{'-'*25}"
    )

    if not claims:
        lines.append(f"{'':^96}")
        lines.append(f"{'*** NO CLAIMS ON FILE FOR THE REPORTED PERIOD ***':^96}")
        lines.append(f"{'':^96}")
    else:
        for c in claims:
            total = c["paid"] + c["reserved"]
            row = (
                f"{c['claim_no']:<12}| {c['date_of_loss']:<13}| {c['loss_type']:<16}"
                f"| {c['status']:<8}| {fmt(c['paid']):<11}| {fmt(c['reserved']):<11}"
                f"| {fmt(total):<16}| {c['description']}"
            )
            lines.append(row)

    lines.append(DSEP)
    lines.append("")

    # ---- Five-year loss summary ----------------------------------------------
    lines.append(SEP)
    lines.append("FIVE-YEAR LOSS SUMMARY")
    lines.append(DSEP)

    shdr = (
        f"{'Policy Year':<17}| {'# Claims':<10}| {'Total Paid':<14}"
        f"| {'Total Reserved':<17}| {'Total Incurred':<17}| Loss Ratio"
    )
    lines.append(shdr)
    lines.append(
        f"{'-'*17}|{'-'*10}|{'-'*14}|{'-'*17}|{'-'*17}|{'-'*12}"
    )

    year_labels = ["2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"]
    grand_claims = 0
    grand_paid = 0
    grand_reserved = 0

    for yl in year_labels:
        yr_claims = [c for c in claims if c.get("policy_year") == yl]
        n = len(yr_claims)
        paid = sum(c["paid"] for c in yr_claims)
        res  = sum(c["reserved"] for c in yr_claims)
        inc  = paid + res
        prem = annual_premium.get(yl, 0)
        lr   = (inc / prem * 100) if prem else 0.0

        grand_claims += n
        grand_paid   += paid
        grand_reserved += res

        row = (
            f"{yl:<17}| {n:<9}| {fmt(paid):<13}"
            f"| {fmt(res):<16}| {fmt(inc):<16}| {lr:.1f}%"
        )
        lines.append(row)

    lines.append(DSEP)
    grand_inc = grand_paid + grand_reserved
    total_prem = sum(annual_premium.values())
    grand_lr = (grand_inc / total_prem * 100) if total_prem else 0.0
    trow = (
        f"{'TOTAL':<17}| {grand_claims:<9}| {fmt(grand_paid):<13}"
        f"| {fmt(grand_reserved):<16}| {fmt(grand_inc):<16}| {grand_lr:.1f}%"
    )
    lines.append(trow)
    lines.append(SEP)
    lines.append("")

    # ---- Footer --------------------------------------------------------------
    lines.append(f"Prepared by: {adjuster_name}, Claims Department")
    if extra_footer_lines:
        for fl in extra_footer_lines:
            lines.append(fl)
    lines.append("This report is provided for informational purposes only and does not")
    lines.append("constitute a guarantee of coverage or waiver of any policy terms.")
    lines.append(SEP)
    lines.append("")

    return "\n".join(lines)


# ===========================================================================
# 1. LR_pacific_retail.txt
# ===========================================================================
def pacific_retail():
    premiums = {
        "2021-2022": 185000, "2022-2023": 192000, "2023-2024": 198000,
        "2024-2025": 205000, "2025-2026": 212000,
    }
    claims = [
        {
            "claim_no": "CLM-ZU-88412",
            "date_of_loss": "03/15/2024",
            "loss_type": "Fire",
            "status": "Closed",
            "paid": 125000,
            "reserved": 0,
            "description": "Kitchen fire at Store #7, grease ignition; sprinkler activation limited spread",
            "policy_year": "2023-2024",
        },
    ]
    return build_loss_run(
        carrier="Zurich Insurance Company Ltd",
        policy_number="POL-ZU-CPP-2025-77341",
        insured_name="Pacific Retail Group, Inc.",
        policy_start="04/01/2025",
        policy_end="04/01/2026",
        report_date="03/18/2026",
        broker="Marsh McLennan - San Francisco",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Linda Vasquez, CPCU",
    )


# ===========================================================================
# 2. LR_acme_industrial.txt
# ===========================================================================
def acme_industrial():
    premiums = {
        "2021-2022": 310000, "2022-2023": 325000, "2023-2024": 340000,
        "2024-2025": 358000, "2025-2026": 375000,
    }
    claims = [
        {
            "claim_no": "CLM-HT-50219",
            "date_of_loss": "11/02/2023",
            "loss_type": "Fire",
            "status": "Closed",
            "paid": 85000,
            "reserved": 0,
            "description": "Electrical panel fire in Bldg C machine shop; fire dept responded within 8 min",
            "policy_year": "2023-2024",
        },
        {
            "claim_no": "CLM-HT-50387",
            "date_of_loss": "06/18/2024",
            "loss_type": "Water Damage",
            "status": "Closed",
            "paid": 200000,
            "reserved": 0,
            "description": "Roof drain failure during severe thunderstorm; flooding in warehouse sections A-D",
            "policy_year": "2024-2025",
        },
    ]
    return build_loss_run(
        carrier="The Hartford Financial Services Group, Inc.",
        policy_number="POL-HT-BOP-2025-13067",
        insured_name="Acme Industrial Supply Co.",
        policy_start="07/01/2025",
        policy_end="07/01/2026",
        report_date="03/05/2026",
        broker="Aon plc - Chicago",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Robert Kimball, AIC",
    )


# ===========================================================================
# 3. LR_northern_mfg.txt  (renewal - zero claims)
# ===========================================================================
def northern_mfg():
    premiums = {
        "2021-2022": 420000, "2022-2023": 415000, "2023-2024": 410000,
        "2024-2025": 405000, "2025-2026": 398000,
    }
    return build_loss_run(
        carrier="Tokio Marine HCC",
        policy_number="POL-TM-CPP-2025-40221",
        insured_name="Northern Manufacturing Corp.",
        policy_start="01/01/2025",
        policy_end="01/01/2026",
        report_date="02/28/2026",
        broker="Willis Towers Watson - Minneapolis",
        claims=[],
        annual_premium=premiums,
        adjuster_name="Karen Lindstrom, SCLA",
        extra_footer_lines=[
            "Note: This is a renewal account. Zero claims reported over the five-year period.",
        ],
    )


# ===========================================================================
# 4. LR_heritage_hotels.txt  (3 wind claims, $2.1M)
# ===========================================================================
def heritage_hotels():
    premiums = {
        "2021-2022": 780000, "2022-2023": 850000, "2023-2024": 920000,
        "2024-2025": 1050000, "2025-2026": 1150000,
    }
    claims = [
        {
            "claim_no": "CLM-AIG-91204",
            "date_of_loss": "09/28/2022",
            "loss_type": "Wind / Hurricane",
            "status": "Closed",
            "paid": 875000,
            "reserved": 0,
            "description": "Hurricane Fiona - roof and facade damage at Grand Cayman resort property",
            "policy_year": "2022-2023",
        },
        {
            "claim_no": "CLM-AIG-92510",
            "date_of_loss": "08/14/2023",
            "loss_type": "Wind / Hurricane",
            "status": "Closed",
            "paid": 640000,
            "reserved": 0,
            "description": "Tropical Storm Harold - water intrusion and structural damage, St. Thomas location",
            "policy_year": "2023-2024",
        },
        {
            "claim_no": "CLM-AIG-93785",
            "date_of_loss": "10/05/2024",
            "loss_type": "Wind / Hurricane",
            "status": "Closed",
            "paid": 585000,
            "reserved": 0,
            "description": "Hurricane Milton - exterior envelope and pool deck damage, Nassau property",
            "policy_year": "2024-2025",
        },
    ]
    return build_loss_run(
        carrier="AIG Property Casualty (American International Group, Inc.)",
        policy_number="POL-AIG-COM-2025-60418",
        insured_name="Heritage Hotels & Resorts, LLC",
        policy_start="06/01/2025",
        policy_end="06/01/2026",
        report_date="03/12/2026",
        broker="Lockton Companies - Miami",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="David Morales, AIC, CPCU",
        extra_footer_lines=[
            "Note: All three wind/hurricane claims fall within the named-storm sub-limit.",
            "Cat modeling data available upon request from AIG Catastrophe Management.",
        ],
    )


# ===========================================================================
# 5. LR_western_distribution.txt  (renewal, 4 claims)
# ===========================================================================
def western_distribution():
    premiums = {
        "2021-2022": 275000, "2022-2023": 290000, "2023-2024": 305000,
        "2024-2025": 318000, "2025-2026": 335000,
    }
    claims = [
        {
            "claim_no": "CLM-TM-71002",
            "date_of_loss": "02/10/2022",
            "loss_type": "Fire",
            "status": "Closed",
            "paid": 180000,
            "reserved": 0,
            "description": "Forklift battery charging station fire; warehouse section B, Portland facility",
            "policy_year": "2021-2022",
        },
        {
            "claim_no": "CLM-TM-71589",
            "date_of_loss": "07/22/2023",
            "loss_type": "Collapse",
            "status": "Closed",
            "paid": 95000,
            "reserved": 0,
            "description": "Partial mezzanine collapse due to overloading; no injuries reported",
            "policy_year": "2023-2024",
        },
        {
            "claim_no": "CLM-TM-72104",
            "date_of_loss": "01/08/2024",
            "loss_type": "Theft",
            "status": "Closed",
            "paid": 42000,
            "reserved": 0,
            "description": "Forced entry at Boise depot; electronic equipment and copper wiring stolen",
            "policy_year": "2023-2024",
        },
        {
            "claim_no": "CLM-TM-72835",
            "date_of_loss": "11/19/2024",
            "loss_type": "Water Damage",
            "status": "Closed",
            "paid": 35000,
            "reserved": 0,
            "description": "Sprinkler head accidental discharge; limited water damage to stored inventory",
            "policy_year": "2024-2025",
        },
    ]
    return build_loss_run(
        carrier="Tokio Marine HCC",
        policy_number="POL-TM-CPP-2025-40587",
        insured_name="Western Distribution Services, Inc.",
        policy_start="03/01/2025",
        policy_end="03/01/2026",
        report_date="03/01/2026",
        broker="Brown & Brown - Portland",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Jennifer Kowalski, AIC",
        extra_footer_lines=[
            "Note: This is a renewal account. Insured has implemented corrective actions after each loss event.",
        ],
    )


# ===========================================================================
# 6. LR_cascade_tech.txt  (zero claims, pristine)
# ===========================================================================
def cascade_tech():
    premiums = {
        "2021-2022": 520000, "2022-2023": 510000, "2023-2024": 505000,
        "2024-2025": 498000, "2025-2026": 490000,
    }
    return build_loss_run(
        carrier="FM Global (Factory Mutual Insurance Company)",
        policy_number="POL-FM-HPR-2025-22984",
        insured_name="Cascade Technology Partners, Inc.",
        policy_start="05/01/2025",
        policy_end="05/01/2026",
        report_date="03/15/2026",
        broker="Gallagher - Seattle",
        claims=[],
        annual_premium=premiums,
        adjuster_name="Michael Sorensen, ARM",
        extra_footer_lines=[
            "Note: Insured maintains FM Approved fire protection throughout all facilities.",
            "HPR status confirmed. No losses reported during the entire five-year period.",
        ],
    )


# ===========================================================================
# 7. LR_gulf_coast_energy.txt  (1 claim, $25K open reserve)
# ===========================================================================
def gulf_coast_energy():
    premiums = {
        "2021-2022": 680000, "2022-2023": 720000, "2023-2024": 765000,
        "2024-2025": 810000, "2025-2026": 860000,
    }
    claims = [
        {
            "claim_no": "CLM-ST-44891",
            "date_of_loss": "08/22/2025",
            "loss_type": "Wind / Named Storm",
            "status": "Open",
            "paid": 120000,
            "reserved": 25000,
            "description": "Tropical Storm Nora - debris impact to tank farm piping and control building roof",
            "policy_year": "2025-2026",
        },
    ]
    return build_loss_run(
        carrier="Starr Indemnity & Liability Company",
        policy_number="POL-ST-ENR-2025-09176",
        insured_name="Gulf Coast Energy Holdings, LLC",
        policy_start="06/15/2025",
        policy_end="06/15/2026",
        report_date="03/20/2026",
        broker="McGriff Insurance Services - Houston",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Thomas Nguyen, CPCU, AIC",
        extra_footer_lines=[
            "Note: CLM-ST-44891 remains open; $25,000 reserve for pending contractor remediation estimate.",
        ],
    )


# ===========================================================================
# 8. LR_midwest_ag.txt  (3 small weather claims)
# ===========================================================================
def midwest_ag():
    premiums = {
        "2021-2022": 195000, "2022-2023": 205000, "2023-2024": 215000,
        "2024-2025": 225000, "2025-2026": 235000,
    }
    claims = [
        {
            "claim_no": "CLM-NW-33102",
            "date_of_loss": "06/04/2023",
            "loss_type": "Hail",
            "status": "Closed",
            "paid": 78000,
            "reserved": 0,
            "description": "Severe hail event; metal roof and siding damage at grain elevator complex",
            "policy_year": "2022-2023",
        },
        {
            "claim_no": "CLM-NW-33540",
            "date_of_loss": "04/17/2024",
            "loss_type": "Lightning",
            "status": "Closed",
            "paid": 45000,
            "reserved": 0,
            "description": "Lightning strike to electrical transformer; surge damage to processing controls",
            "policy_year": "2023-2024",
        },
        {
            "claim_no": "CLM-NW-33912",
            "date_of_loss": "09/29/2024",
            "loss_type": "Wind",
            "status": "Closed",
            "paid": 32000,
            "reserved": 0,
            "description": "Straight-line winds (est. 75 mph); barn door and overhead door replacement",
            "policy_year": "2024-2025",
        },
    ]
    return build_loss_run(
        carrier="Nationwide Mutual Insurance Company",
        policy_number="POL-NW-AGR-2025-55829",
        insured_name="Midwest Agricultural Cooperative",
        policy_start="10/01/2025",
        policy_end="10/01/2026",
        report_date="03/10/2026",
        broker="Gallagher - Des Moines",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Sarah Mitchell, AIC",
    )


# ===========================================================================
# 9. LR_atlantic_seafood.txt  (renewal, large loss $2.1M)
# ===========================================================================
def atlantic_seafood():
    premiums = {
        "2021-2022": 350000, "2022-2023": 365000, "2023-2024": 380000,
        "2024-2025": 475000, "2025-2026": 550000,
    }
    claims = [
        {
            "claim_no": "CLM-TM-80210",
            "date_of_loss": "12/18/2023",
            "loss_type": "Equipment Breakdown",
            "status": "Closed",
            "paid": 2100000,
            "reserved": 0,
            "description": "Catastrophic ammonia refrigeration compressor failure; total loss of cold-storage inventory ($1.65M product spoilage + $450K equipment repair)",
            "policy_year": "2023-2024",
        },
        {
            "claim_no": "CLM-TM-80745",
            "date_of_loss": "05/09/2024",
            "loss_type": "Water Damage",
            "status": "Closed",
            "paid": 65000,
            "reserved": 0,
            "description": "Pipe burst in processing facility washdown area; floor and wall damage",
            "policy_year": "2024-2025",
        },
        {
            "claim_no": "CLM-TM-81102",
            "date_of_loss": "09/03/2025",
            "loss_type": "Fire",
            "status": "Closed",
            "paid": 28000,
            "reserved": 0,
            "description": "Minor grease fire in employee break room kitchen; suppression system activated",
            "policy_year": "2025-2026",
        },
    ]
    return build_loss_run(
        carrier="Tokio Marine HCC",
        policy_number="POL-TM-CPP-2025-40903",
        insured_name="Atlantic Seafood Processing, Inc.",
        policy_start="11/01/2025",
        policy_end="11/01/2026",
        report_date="03/22/2026",
        broker="USI Insurance Services - Boston",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Paul Demetriou, CPCU, AIC",
        extra_footer_lines=[
            "Note: This is a renewal account. Large loss (CLM-TM-80210) triggered mandatory",
            "equipment breakdown re-inspection; insured has since installed redundant refrigeration.",
            "Premium increase in 2024-2025 and 2025-2026 reflects large-loss surcharge.",
        ],
    )


# ===========================================================================
# 10. LR_summit_office.txt  (1 small claim, closed)
# ===========================================================================
def summit_office():
    premiums = {
        "2021-2022": 145000, "2022-2023": 148000, "2023-2024": 152000,
        "2024-2025": 155000, "2025-2026": 158000,
    }
    claims = [
        {
            "claim_no": "CLM-CB-20417",
            "date_of_loss": "01/27/2025",
            "loss_type": "Water Damage",
            "status": "Closed",
            "paid": 38000,
            "reserved": 0,
            "description": "Frozen pipe burst on 4th floor; water damage to ceiling tiles, carpet, and drywall on floors 3-4",
            "policy_year": "2024-2025",
        },
    ]
    return build_loss_run(
        carrier="Chubb Limited (Federal Insurance Company) - Lead Market",
        policy_number="POL-CB-OFC-2025-87612",
        insured_name="Summit Office REIT, LP",
        policy_start="02/01/2025",
        policy_end="02/01/2026",
        report_date="03/08/2026",
        broker="Marsh McLennan - Denver",
        claims=claims,
        annual_premium=premiums,
        adjuster_name="Christine Faber, SCLA",
    )


# ===========================================================================
# Main: write all files
# ===========================================================================
ACCOUNTS = [
    ("LR_pacific_retail.txt",       pacific_retail),
    ("LR_acme_industrial.txt",      acme_industrial),
    ("LR_northern_mfg.txt",         northern_mfg),
    ("LR_heritage_hotels.txt",      heritage_hotels),
    ("LR_western_distribution.txt", western_distribution),
    ("LR_cascade_tech.txt",         cascade_tech),
    ("LR_gulf_coast_energy.txt",    gulf_coast_energy),
    ("LR_midwest_ag.txt",           midwest_ag),
    ("LR_atlantic_seafood.txt",     atlantic_seafood),
    ("LR_summit_office.txt",        summit_office),
]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename, builder in ACCOUNTS:
        path = os.path.join(OUTPUT_DIR, filename)
        content = builder()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        line_count = content.count("\n") + 1
        print(f"  [OK] {filename:40s} ({line_count:>3d} lines)")
    print(f"\nAll {len(ACCOUNTS)} loss-run files written to:\n  {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
