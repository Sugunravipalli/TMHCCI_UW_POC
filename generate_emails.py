#!/usr/bin/env python3
"""
generate_emails.py
Generate 50+ realistic .eml submission emails for Tokio Marine HCC International
commercial property underwriting POC.

All business routed through Lloyd's brokers to submissions@tmhcci.com.
"""

import os
import random
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime, timedelta, timezone

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "01_submission_emails")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def _date_str(dt: datetime) -> str:
    """RFC 2822 date string."""
    return formatdate(timeval=dt.timestamp(), localtime=False, usegmt=True)


def _make_eml(*, from_addr: str, to_addr: str, cc: str | None, subject: str,
              body: str, date: datetime, message_id_tag: str,
              references: str | None = None,
              in_reply_to: str | None = None) -> str:
    """Return a full RFC 2822 .eml string."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = from_addr
    msg["To"] = to_addr
    if cc:
        msg["Cc"] = cc
    msg["Subject"] = subject
    msg["Date"] = _date_str(date)
    msg["Message-ID"] = f"<{message_id_tag}@mail.brokerdom.com>"
    if references:
        msg["References"] = references
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    msg["X-Mailer"] = "Microsoft Outlook 16.0"
    return msg.as_string()


def _write(filename: str, content: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  wrote {filename}")


def _rand_date(start: str = "2025-09-01", end: str = "2026-03-31") -> datetime:
    s = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
    e = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
    delta = (e - s).days
    return s + timedelta(days=random.randint(0, delta),
                         hours=random.randint(7, 17),
                         minutes=random.randint(0, 59))


# ── 10 Hero Initial Submissions ─────────────────────────────────────────────

HERO_SUBS = [
    # 1 - Pacific Retail Group
    {
        "file": "SUB-2026-0001_pacific_retail.eml",
        "from": "Sarah Chen <sarah.chen@aon.com>",
        "cc": "property.submissions@aon.com",
        "subject": "New Business Submission - Pacific Retail Group LLC - Commercial Property - $120M TIV - 47 Locations",
        "date": datetime(2026, 1, 12, 9, 14, tzinfo=timezone.utc),
        "tag": "sub-2026-0001",
        "body": """Dear Property Underwriting Team,

I hope this email finds you well. We are pleased to submit the following new business opportunity for your consideration.

SUBMISSION REFERENCE: SUB-2026-0001

NAMED INSURED: Pacific Retail Group LLC
RISK TYPE: Commercial Property - Retail Portfolio
TOTAL INSURED VALUES: USD 120,000,000 (One Hundred Twenty Million)
NUMBER OF LOCATIONS: 47
OCCUPANCIES: Regional shopping centres, retail strip malls, standalone big-box retail, mixed-use retail/office

COVERAGE REQUESTED:
- All-Risk Property including Named Windstorm
- Business Interruption (12 months ALE)
- Equipment Breakdown
- Flood (Zones B & C; Zone A buy-up on 3 locations)
- Earthquake (3 CA locations)
- Ordinance or Law - Coverage A, B, C
- Terrorism (TRIA certified acts)

PROGRAMME STRUCTURE:
- Seeking USD 50,000,000 per occurrence limit
- USD 100,000,000 annual aggregate
- Target deductible: USD 100,000 per occurrence / 72-hour windstorm
- Layered placement anticipated; looking for lead market

INCEPTION DATE: 1st April 2026
EXPIRY DATE: 31st March 2027

LOSS HISTORY: 5-year loss history attached. Total incurred over the period is USD 1,240,000 across 12 claims, predominantly slip-and-fall GL (not property). No property losses exceeding USD 50,000. Loss ratio well below 30%.

ATTACHMENTS:
1. Statement of Values (SOV) - Excel - 47 locations with construction, occupancy, protection, exposure detail
2. Completed ACORD 140 Property Application
3. 5-Year Loss Run (PDF)
4. Location photographs and aerial imagery (ZIP)
5. Most recent property inspection report (Zurich Risk Engineering, dated November 2025)

The insured is a well-capitalised regional retail REIT with institutional-quality assets, predominantly concrete tilt-up and steel frame construction. Majority of locations have automatic sprinkler protection. The risk has been with a domestic carrier for six years and is seeking London market capacity for the upcoming renewal.

We would appreciate receiving your initial indication by 24th January 2026 if possible, as the client has a board meeting in early February and would like to present market feedback at that time.

Please do not hesitate to contact me should you require any additional information.

Kind regards,

Sarah Chen
Vice President, Property Broking
Aon Reinsurance Solutions
The Aon Centre | The Leadenhall Building
122 Leadenhall Street, London EC3V 4AN
Tel: +44 (0)20 7086 XXXX
Mob: +44 (0)7700 900XXX
sarah.chen@aon.com

This e-mail is confidential and is intended solely for the addressee. If you are not the intended recipient, please notify the sender immediately and delete this e-mail.
"""
    },
    # 2 - Acme Industrial (INCOMPLETE)
    {
        "file": "SUB-2026-0002_acme_industrial.eml",
        "from": "David Armstrong <david.armstrong@wtwco.com>",
        "cc": "london.property@wtwco.com",
        "subject": "New Submission - Acme Industrial Holdings Inc - Property - $45M TIV - 3 Locations",
        "date": datetime(2026, 1, 15, 14, 32, tzinfo=timezone.utc),
        "tag": "sub-2026-0002",
        "body": """Dear TMHCC Property Team,

Please find below a new business submission for your review.

SUBMISSION REFERENCE: SUB-2026-0002

NAMED INSURED: Acme Industrial Holdings Inc
RISK TYPE: Commercial Property - Heavy Manufacturing
TOTAL INSURED VALUES: USD 45,000,000
NUMBER OF LOCATIONS: 3

LOCATIONS:
1. Main Manufacturing Plant - 2400 Industrial Blvd, Detroit, MI 48201
   Building Value: USD 18,000,000 | Contents: USD 8,000,000 | BI: USD 5,000,000
   Construction: Non-combustible steel frame | Year Built: 1998 | Sprinklered: Yes (wet pipe)
   Occupancy: Automotive component manufacturing (metal stamping, welding, assembly)

2. Warehouse & Distribution - 500 Commerce Dr, Toledo, OH 43604
   Building Value: USD 6,000,000 | Contents: USD 4,000,000 | BI: USD 1,500,000
   Construction: Metal clad steel frame | Year Built: 2005 | Sprinklered: Yes (ESFR)
   Occupancy: Finished goods warehousing and distribution

3. Corporate Office & R&D Lab - 100 Innovation Way, Ann Arbor, MI 48104
   Building Value: USD 1,500,000 | Contents: USD 500,000 | BI: USD 500,000
   Construction: Fire resistive | Year Built: 2012 | Sprinklered: Yes
   Occupancy: Office and research laboratory

COVERAGE REQUESTED:
- All-Risk Property Damage and Business Interruption
- Extra Expense
- Equipment Breakdown / Mechanical & Electrical
- Transit coverage (USD 2,000,000 any one conveyance)

DESIRED LIMITS:
- USD 45,000,000 blanket per occurrence
- USD 250,000 deductible per occurrence

INCEPTION: 1st March 2026

ATTACHMENTS:
1. SOV Schedule (Excel)
2. ACORD 140 Application (partially completed - awaiting signatures)

** PLEASE NOTE: We are still awaiting the insured's loss runs from the current carrier (Travelers). We have chased the client and expect to have these within the next 5-7 business days. We wanted to get the submission in front of markets early given the tight timeline. We will forward the loss history as soon as it is received. **

The insured is a Tier 2 automotive supplier with long-term contracts with Ford and General Motors. Revenue has been stable at approximately USD 85M per annum over the last three years.

Happy to arrange a call to discuss further.

Best regards,

David Armstrong
Director, Property Facultative
Willis Towers Watson
51 Lime Street, London EC3M 7DQ
Tel: +44 (0)20 3124 XXXX
david.armstrong@wtwco.com
"""
    },
    # 3 - Northern Manufacturing (RENEWAL)
    {
        "file": "SUB-2026-0003_northern_manufacturing.eml",
        "from": "James Whitfield <james.whitfield@marsh.com>",
        "cc": "uk.property.submissions@marsh.com",
        "subject": "Renewal Submission - Northern Manufacturing Co Ltd - Property - $28M TIV - Ref: POL-TMHCC-2025-NM-0044",
        "date": datetime(2026, 2, 3, 10, 47, tzinfo=timezone.utc),
        "tag": "sub-2026-0003",
        "body": """Dear Underwriting Team,

We write in respect of the forthcoming renewal of the above-captioned policy. The current policy expires on 30th April 2026 and we would be grateful for your renewal terms at your earliest convenience.

SUBMISSION REFERENCE: SUB-2026-0003
EXISTING POLICY: POL-TMHCC-2025-NM-0044

NAMED INSURED: Northern Manufacturing Co Ltd
RISK TYPE: Commercial Property - Precision Manufacturing
TOTAL INSURED VALUES: USD 28,000,000 (per attached SOV; values updated for 2026)
NUMBER OF LOCATIONS: 1

LOCATION: Unit 14-18, Riverside Industrial Estate, Sheffield S9 2RX, United Kingdom
CONSTRUCTION: Reinforced concrete frame with composite metal deck roof, brick/block infill walls
YEAR BUILT: 2003 (office wing refurbished 2019)
AREA: 85,000 sq ft (manufacturing 60,000 / warehouse 15,000 / office 10,000)
SPRINKLERS: Full wet-pipe sprinkler throughout, FM Global-approved design
OCCUPANCY: CNC precision machining - aerospace and medical device components

VALUES BREAKDOWN:
- Building: GBP 8,500,000
- Machinery & Plant: GBP 9,200,000 (includes 12 CNC milling centres, 4 lathes, EDM, CMM)
- Stock & WIP: GBP 2,800,000
- Business Interruption (24 months indemnity period): GBP 6,500,000
- Total Insured Value (GBP equivalent): approx. GBP 22,000,000 / USD 28,000,000

EXPIRING TERMS:
- Carrier: TMHCC (100% signed line)
- Limit: GBP 22,000,000 blanket
- Deductible: GBP 25,000 each and every loss
- Rate: 0.085%
- Premium: GBP 18,700

LOSS HISTORY: The insured has had a completely CLEAN loss record during the current policy period and the prior 7 years. No claims have been reported to any carrier in the last decade.

CHANGES FROM EXPIRY:
- TIV increase of approximately 4% reflecting updated valuations
- No change in occupancy, construction, or operations
- Client has invested GBP 450,000 in upgraded fire detection (aspirating smoke detection) and CCTV system

ATTACHMENTS:
1. Updated SOV (Excel)
2. Current policy schedule (PDF)
3. 10-year claims-free letter from insured's risk manager
4. Fire risk assessment report (dated January 2026)
5. Photographs of new fire detection system

Given the clean record and improved risk profile, the insured would expect flat to favourable renewal terms. We look forward to receiving your indication.

Yours sincerely,

James Whitfield
Senior Vice President, UK Property
Marsh Ltd
Tower Place, London EC3R 5BU
Tel: +44 (0)20 7357 XXXX
james.whitfield@marsh.com
"""
    },
    # 4 - Heritage Hotels (Coastal FL/Caribbean)
    {
        "file": "SUB-2026-0004_heritage_hotels.eml",
        "from": "Emily Hartwell <emily.hartwell@lockton.com>",
        "cc": "london.property@lockton.com, hospitality@lockton.com",
        "subject": "New Business Submission - Heritage Hotels International PLC - Hospitality Property - $200M TIV - 12 Locations",
        "date": datetime(2026, 1, 20, 11, 5, tzinfo=timezone.utc),
        "tag": "sub-2026-0004",
        "body": """Dear TMHCC Property Underwriters,

We are delighted to present the following new business submission for your consideration. Heritage Hotels International is a premium hospitality group and we believe this account represents an excellent fit for your book.

SUBMISSION REFERENCE: SUB-2026-0004

NAMED INSURED: Heritage Hotels International PLC
PARENT COMPANY: Heritage Hospitality Group (LSE-listed, market cap approx. GBP 1.8 billion)
RISK TYPE: Commercial Property - Hospitality / Hotels & Resorts
TOTAL INSURED VALUES: USD 200,000,000
NUMBER OF LOCATIONS: 12

PORTFOLIO OVERVIEW:
The insured operates 12 boutique and full-service resort properties across the Southeastern United States and the Caribbean. The portfolio is weighted towards coastal Florida and the Caribbean Basin:

- 5 properties in Coastal Florida (Miami Beach, Key West, Naples, Destin, Palm Beach)
- 3 properties in the Caribbean (Grand Cayman, Turks & Caicos, St. Barths)
- 2 properties in South Carolina (Charleston, Hilton Head)
- 1 property in Savannah, Georgia
- 1 property in New Orleans, Louisiana

WINDSTORM EXPOSURE: We recognise the concentration of Named Windstorm exposure in this portfolio. The insured has invested significantly in structural hardening across all coastal properties, including:
- Miami-Dade rated impact-resistant windows and doors at all FL locations
- Reinforced concrete construction (poured-in-place or CBS) at 9 of 12 locations
- Emergency generator backup at all locations
- Comprehensive hurricane preparedness plans reviewed annually

COVERAGE REQUESTED:
- All-Risk Property Damage including Named Windstorm
- Business Interruption (18 months Extended Period of Indemnity)
- Contingent Business Interruption
- Flood (NFIP + excess; Zones A, V, and X locations)
- Earthquake
- Equipment Breakdown
- Spoilage / Refrigeration
- Ordinance or Law
- Terrorism (TRIPRA)

PROGRAMME STRUCTURE:
- USD 100,000,000 per occurrence limit
- USD 200,000,000 annual aggregate (for Named Windstorm / Flood)
- Named Windstorm Deductible: 5% of location TIV, USD 500,000 minimum
- All Other Perils Deductible: USD 250,000
- Seeking capacity in the USD 50M xs USD 50M layer; Arch are expected to lead the primary

INCEPTION: 1st June 2026
EXPIRY: 31st May 2027

LOSS HISTORY: 5-year loss runs attached. The portfolio experienced a USD 3.2M claim following Hurricane Ian (2022) at the Naples property, which has since been fully repaired and upgraded. No other losses exceeding USD 100,000.

ATTACHMENTS:
1. Statement of Values (SOV) - all 12 locations with detailed construction, year built, and COPE data
2. ACORD 140 Application
3. 5-Year Loss Runs
4. Wind Mitigation Reports (FL properties)
5. Structural Engineering Reports (Caribbean properties)
6. RMS RiskLink catastrophe model output summary (PML and AAL)

We understand this is a CAT-exposed account and we are realistic about pricing expectations. We are targeting a rate on line in the range of 0.35% - 0.45% for the excess layer. The client has budgeted accordingly.

We would be happy to arrange a call with the insured's VP of Risk Management to discuss the portfolio and risk mitigation efforts in more detail.

We would appreciate an initial indication by 7th February 2026.

Best regards,

Emily Hartwell
Partner, Hospitality & Leisure Practice
Lockton Companies LLP
The St Botolph Building, 138 Houndsditch, London EC3A 7AG
Tel: +44 (0)20 7933 XXXX
Mob: +44 (0)7824 XXXXXX
emily.hartwell@lockton.com
"""
    },
    # 5 - Western Distribution (RENEWAL, prior claims)
    {
        "file": "SUB-2026-0005_western_distribution.eml",
        "from": "Michael Cross <michael.cross@howdengroup.com>",
        "cc": "property.fac@howdengroup.com",
        "subject": "Renewal Submission - Western Distribution Corp - Commercial Property - $65M TIV - 8 Locations - Ref: WDC-TMHCC-2025",
        "date": datetime(2026, 2, 10, 8, 23, tzinfo=timezone.utc),
        "tag": "sub-2026-0005",
        "body": """Dear Colleagues,

We attach the renewal submission for Western Distribution Corp. The current policy with TMHCC expires on 30th April 2026 and we would welcome your renewal indication at your earliest convenience.

SUBMISSION REFERENCE: SUB-2026-0005
CURRENT POLICY: WDC-TMHCC-2025-PP-0128

NAMED INSURED: Western Distribution Corp
RISK TYPE: Commercial Property - Warehousing & Distribution
TOTAL INSURED VALUES: USD 65,000,000
NUMBER OF LOCATIONS: 8

LOCATIONS: The insured operates a network of eight distribution centres across the Western United States:
1. Phoenix, AZ - 240,000 sq ft - USD 14,500,000
2. Las Vegas, NV - 180,000 sq ft - USD 10,200,000
3. Sacramento, CA - 150,000 sq ft - USD 9,800,000
4. Portland, OR - 120,000 sq ft - USD 7,500,000
5. Denver, CO - 200,000 sq ft - USD 8,900,000
6. Salt Lake City, UT - 95,000 sq ft - USD 5,100,000
7. Boise, ID - 85,000 sq ft - USD 4,800,000
8. Albuquerque, NM - 75,000 sq ft - USD 4,200,000

CONSTRUCTION: All locations are tilt-up concrete or metal-clad steel frame. All are single storey. All locations sprinklered.

COVERAGE: All-Risk including Earthquake (Sacramento, Portland, Salt Lake City locations), Equipment Breakdown, Business Interruption (12 months).

LIMIT: USD 65,000,000 blanket
DEDUCTIBLE: USD 100,000 each and every loss / 72 hours for windstorm
EQ DEDUCTIBLE: 5% of values at affected location(s), USD 250,000 minimum

EXPIRING PREMIUM: USD 89,500 (rate 0.138%)

LOSS HISTORY - THIS IS IMPORTANT:
We want to be transparent about the claims experience on this account during the current policy period:

1. 14th July 2025: Phoenix location - Roof-mounted HVAC unit failure caused water ingress to warehouse. Approximately 8,000 sq ft of stored consumer electronics inventory damaged. PAID: USD 420,000 (Contents) + USD 85,000 (Property Damage to ceiling/flooring). TOTAL: USD 505,000.

2. 22nd September 2025: Sacramento location - Forklift operator struck fire sprinkler riser, causing partial discharge. Water damage to racking and stored goods. PAID: USD 178,000.

TOTAL INCURRED (Current Policy Year): USD 683,000
CURRENT YEAR LOSS RATIO: approximately 76%

5-YEAR LOSS HISTORY: Prior to the current year, the account had a clean 4-year record with TMHCC. Total 5-year incurred is USD 683,000.

REMEDIATION STEPS TAKEN:
- Phoenix: Complete roof HVAC replacement programme (USD 340,000 investment); secondary containment trays installed beneath all rooftop units
- Sacramento: Bollard protection installed around all sprinkler risers; enhanced forklift operator training programme; quarterly sprinkler system inspections

We acknowledge the elevated loss ratio this year and understand the need for rate adjustment. The insured has been a loyal TMHCC policyholder for five years and has invested meaningfully in loss prevention. We would respectfully request that the renewal be rated on the 5-year record rather than the single adverse year.

ATTACHMENTS:
1. Updated SOV (Excel)
2. 5-Year Loss Runs (PDF)
3. Remediation photographs and invoices
4. ACORD 140 Application

We look forward to your indication and are happy to arrange a call to discuss.

Regards,

Michael Cross
Divisional Director, Property
Howden Broking Group
One Creechurch Place, London EC3A 5AF
Tel: +44 (0)20 7623 XXXX
michael.cross@howdengroup.com
"""
    },
    # 6 - Cascade Technology Campus (Data Centres)
    {
        "file": "SUB-2026-0006_cascade_technology.eml",
        "from": "Rachel Foster <rachel.foster@ajg.com>",
        "cc": "london.specialty.property@ajg.com",
        "subject": "New Business Submission - Cascade Technology Campus Inc - Data Centre Property - $180M TIV - 2 Locations",
        "date": datetime(2026, 1, 22, 15, 8, tzinfo=timezone.utc),
        "tag": "sub-2026-0006",
        "body": """Dear TMHCC Underwriting Team,

We are pleased to present a new business submission for Cascade Technology Campus Inc, a specialist data centre operator. This is a high-quality risk with significant investment in resilience and redundancy.

SUBMISSION REFERENCE: SUB-2026-0006

NAMED INSURED: Cascade Technology Campus Inc
RISK TYPE: Commercial Property - Data Centre / Technology
TOTAL INSURED VALUES: USD 180,000,000
NUMBER OF LOCATIONS: 2

LOCATION 1 - PRIMARY DATA CENTRE CAMPUS
Address: 15000 Datacentre Way, Ashburn, VA 20147 ("Data Alley")
Building Value: USD 45,000,000
M&E / Contents: USD 65,000,000 (servers, networking, UPS, cooling infrastructure, generators)
Business Interruption: USD 25,000,000 (12-month indemnity)
Total Location TIV: USD 135,000,000
Construction: Reinforced concrete, fire-resistive, purpose-built 2018
Tier: Uptime Institute Tier III certified
Area: 120,000 sq ft (60,000 sq ft raised floor)
Power: 20MW IT load, 2N power redundancy, N+1 cooling
Fire Protection: Pre-action dry pipe + VESDA aspirating detection + clean agent (Novec 1230) suppression in all server halls. No water-based suppression in IT spaces.
Security: 24/7/365 on-site security, mantrap entry, biometric access, perimeter fencing

LOCATION 2 - DISASTER RECOVERY / SECONDARY SITE
Address: 2200 Enterprise Park, Columbus, OH 43219
Building Value: USD 12,000,000
M&E / Contents: USD 18,000,000
Business Interruption: USD 15,000,000
Total Location TIV: USD 45,000,000
Construction: Reinforced concrete, purpose-built 2021
Tier: Uptime Institute Tier III design
Area: 45,000 sq ft (22,000 sq ft raised floor)
Power: 8MW IT load, 2N redundancy
Fire Protection: Same specification as primary site

COVERAGE REQUESTED:
- All-Risk Property Damage
- Business Interruption including Contingent BI and Service Interruption
- Equipment Breakdown / Electrical & Mechanical
- Cyber Physical Damage (data restoration sublimit)
- Transit (equipment in transit between facilities)
- Flood (both locations in Zone X)
- Earthquake
- Terrorism

PROGRAMME STRUCTURE:
- USD 150,000,000 per occurrence limit
- AOP Deductible: USD 500,000
- Waiting period for BI: 12 hours
- Seeking lead or significant line on a subscription placement

INCEPTION: 1st May 2026

The insured has 99.999% uptime SLAs with its tenants, which include three Fortune 500 companies. Revenue is approximately USD 95M per annum with strong EBITDA margins.

LOSS HISTORY: Zero losses in the insured's 8-year operating history. Prior carrier was AIG.

REASON FOR MARKETING: The insured is seeking broader London market capacity and more competitive terms as they prepare for a Series C funding round in H2 2026.

ATTACHMENTS:
1. SOV Schedule (Excel)
2. ACORD 140 Application
3. Uptime Institute Tier III Certificates
4. Fire protection system specifications and inspection reports
5. Business continuity plan summary
6. 8-Year Loss-Free Letter

We believe this is a best-in-class data centre risk and a strong fit for TMHCC's technology property appetite. We would welcome the opportunity to discuss in person.

Kind regards,

Rachel Foster
Managing Director, Technology & Cyber Practice
Gallagher Specialty
The Walbrook Building, 25 Walbrook, London EC4N 8AW
Tel: +44 (0)20 7204 XXXX
rachel.foster@ajg.com
"""
    },
    # 7 - Gulf Coast Energy Storage
    {
        "file": "SUB-2026-0007_gulf_coast_energy.eml",
        "from": "Thomas Keane <thomas.keane@mcgillandpartners.com>",
        "cc": "energy.property@mcgillandpartners.com",
        "subject": "New Business Submission - Gulf Coast Energy Storage LLC - Energy Storage Property - $95M TIV - 5 Locations - TX Coast",
        "date": datetime(2026, 1, 28, 13, 45, tzinfo=timezone.utc),
        "tag": "sub-2026-0007",
        "body": """Dear TMHCC Property Team,

Please find below a new business submission for Gulf Coast Energy Storage LLC, a growing battery energy storage system (BESS) and natural gas storage operator based in Texas.

SUBMISSION REFERENCE: SUB-2026-0007

NAMED INSURED: Gulf Coast Energy Storage LLC
RISK TYPE: Energy Property - Battery Storage & Gas Storage
TOTAL INSURED VALUES: USD 95,000,000
NUMBER OF LOCATIONS: 5

LOCATION SCHEDULE:
1. Freeport BESS Facility, Freeport, TX 77541
   TIV: USD 32,000,000 | 200MW lithium-ion BESS | Commissioned: 2024
   Construction: Open-air containerised battery modules on concrete pads
   Fire Protection: Dedicated fire suppression per container, thermal management, 24/7 BMS monitoring

2. Corpus Christi Gas Storage, Corpus Christi, TX 78401
   TIV: USD 28,000,000 | Salt cavern natural gas storage, 12 Bcf capacity
   Surface facilities: Compressor station, dehydration, metering
   Construction: Steel / industrial

3. Galveston BESS Facility, Texas City, TX 77590
   TIV: USD 18,000,000 | 100MW lithium-ion BESS | Commissioned: 2025
   Similar specification to Freeport

4. Port Arthur Gas Processing, Port Arthur, TX 77640
   TIV: USD 12,000,000 | Gas conditioning and compression
   Construction: Industrial steel / process equipment

5. Houston Control Centre & Office, Houston, TX 77002
   TIV: USD 5,000,000 | Office and SCADA control centre
   Construction: Fire-resistive office building

WINDSTORM / FLOOD EXPOSURE:
All five locations are within 50 miles of the Texas Gulf Coast. We have attached detailed flood zone maps and elevation certificates. The BESS facilities at Freeport and Texas City are on elevated pads (12 ft above grade) based on lessons learned from Hurricane Harvey. The Corpus Christi facility withstood Hurricane Hanna (2020) without damage.

COVERAGE REQUESTED:
- All-Risk Property Damage including Named Windstorm and Flood
- Business Interruption (18 months) including Contingent BI
- Equipment Breakdown (critical for BESS battery degradation / thermal runaway)
- Pollution Legal Liability (sublimit)
- Transit
- Terrorism

PROGRAMME STRUCTURE:
- USD 75,000,000 per occurrence limit
- Named Windstorm deductible: 5% of values at affected location, USD 500,000 minimum
- Flood deductible: USD 500,000
- AOP deductible: USD 250,000
- BI waiting period: 48 hours (72 hours for Named Windstorm)

INCEPTION: 1st June 2026

LOSS HISTORY: No losses since inception. The company was formed in 2022 and the facilities were built new.

KEY RISK CONSIDERATIONS:
- Lithium-ion battery thermal runaway is the primary concern; the insured has implemented comprehensive thermal management, fire suppression, and monitoring systems
- BESS containers are spaced per NFPA 855 requirements with minimum 10ft separation
- All facilities comply with ERCOT interconnection requirements
- The insured has a full-time HSE manager and contracts with a third-party risk engineering firm

ATTACHMENTS:
1. SOV (Excel)
2. ACORD 140 Application
3. BESS Fire Safety Report (prepared by Jensen Hughes)
4. Flood Zone Maps and Elevation Certificates
5. RMS Hurricane Model Results
6. Company overview and management bios

This is an emerging and growing asset class. The insured has strong institutional backing (PE-sponsored by Blackrock Infrastructure) and best-in-class safety protocols. We recognise the CAT and technology exposures and look forward to a constructive dialogue on terms.

Best regards,

Thomas Keane
Partner, Energy & Power
McGill and Partners
Gracechurch Street, London EC3V 0AT
Tel: +44 (0)20 3468 XXXX
thomas.keane@mcgillandpartners.com
"""
    },
    # 8 - Midwest Agricultural Cooperative
    {
        "file": "SUB-2026-0008_midwest_agricultural.eml",
        "from": "Charlotte Webb <charlotte.webb@millerinsurance.com>",
        "cc": "agri.property@millerinsurance.com",
        "subject": "New Business Submission - Midwest Agricultural Cooperative - Agricultural Property - $35M TIV - 22 Locations",
        "date": datetime(2026, 2, 5, 10, 20, tzinfo=timezone.utc),
        "tag": "sub-2026-0008",
        "body": """Dear Underwriting Team,

We write to present a new business submission for the Midwest Agricultural Cooperative, a member-owned agricultural cooperative operating grain storage and handling facilities across the American Midwest.

SUBMISSION REFERENCE: SUB-2026-0008

NAMED INSURED: Midwest Agricultural Cooperative
RISK TYPE: Agricultural Property - Grain Storage & Handling
TOTAL INSURED VALUES: USD 35,000,000
NUMBER OF LOCATIONS: 22

PORTFOLIO SUMMARY:
The cooperative operates 22 grain elevator and storage facilities across Iowa, Nebraska, and Minnesota. Facilities range from modern concrete silos to older corrugated steel bins. Total storage capacity is approximately 45 million bushels. Principal commodities: corn, soybeans, and wheat.

FACILITY BREAKDOWN:
- 8 x Large terminal elevators (concrete, 2M+ bushel capacity each) - Total TIV: USD 22,000,000
- 10 x Country elevators (steel bins, 500K-1M bushel capacity) - Total TIV: USD 9,000,000
- 3 x Drying and processing facilities - Total TIV: USD 3,000,000
- 1 x Administrative headquarters (West Des Moines, IA) - Total TIV: USD 1,000,000

CONSTRUCTION: Mix of reinforced concrete (terminal elevators) and corrugated galvanised steel (country elevators). All facilities have concrete foundations. Office/admin buildings are wood frame or masonry.

KEY HAZARDS:
- Grain dust explosion: All facilities comply with OSHA grain handling standards (29 CFR 1910.272). Explosion venting installed on all bins. Dust collection and housekeeping programmes in place.
- Spontaneous combustion: Temperature monitoring cables installed in all bins exceeding 100,000 bushel capacity.
- Windstorm: Tornado exposure across all locations; steel bins anchored per engineered specifications.
- Flood: 3 locations within 500-year flood plain (Zone X shaded). No locations in 100-year flood zone.

COVERAGE REQUESTED:
- All-Risk Property Damage
- Stock Throughput (grain in storage and in transit between facilities)
- Business Interruption (12 months)
- Equipment Breakdown
- Windstorm / Tornado
- Flood (sublimit)

LIMITS: USD 35,000,000 blanket per occurrence
DEDUCTIBLE: USD 50,000 each and every loss; USD 100,000 for windstorm/tornado

INCEPTION: 1st April 2026

LOSS HISTORY:
- 2023: Lightning strike to country elevator in Clarinda, IA. Minor fire damage to headhouse, quickly extinguished by local fire department. Incurred: USD 45,000.
- 2021: Straight-line wind event (derecho) damaged roofing on two country elevators in eastern Iowa. Incurred: USD 128,000.
- No other losses in last 10 years.

TOTAL 10-YEAR INCURRED: USD 173,000

ATTACHMENTS:
1. SOV Schedule (Excel) - all 22 locations
2. ACORD 140 Application
3. Loss Run Summary (10 years)
4. Grain dust explosion prevention programme documentation
5. Most recent grain elevator inspection reports (state-certified)

The cooperative has been in continuous operation since 1947 and has a strong risk management culture. Membership includes over 2,400 farming operations. We believe this is an attractively priced agricultural risk and look forward to your indication.

Regards,

Charlotte Webb
Senior Broker, Agricultural Property
Miller Insurance Services LLP
70 Mark Lane, London EC3R 7NQ
Tel: +44 (0)20 7031 XXXX
charlotte.webb@millerinsurance.com
"""
    },
    # 9 - Atlantic Seafood Processing (RENEWAL, prior large loss)
    {
        "file": "SUB-2026-0009_atlantic_seafood.eml",
        "from": "Andrew Patel <andrew.patel@bmsgroup.com>",
        "cc": "property.london@bmsgroup.com",
        "subject": "Renewal Submission - Atlantic Seafood Processing Inc - Food Processing Property - $50M TIV - 4 Locations - PRIOR LARGE LOSS",
        "date": datetime(2026, 2, 14, 9, 55, tzinfo=timezone.utc),
        "tag": "sub-2026-0009",
        "body": """Dear TMHCC Property Underwriting,

We submit the attached renewal for Atlantic Seafood Processing Inc. We are writing to you well in advance of the expiry date to allow adequate time for review given the claims history on this account.

SUBMISSION REFERENCE: SUB-2026-0009
CURRENT POLICY: ASP-TMHCC-2025-0067
EXPIRY DATE: 30th June 2026

NAMED INSURED: Atlantic Seafood Processing Inc
RISK TYPE: Commercial Property - Food Processing / Cold Storage
TOTAL INSURED VALUES: USD 50,000,000
NUMBER OF LOCATIONS: 4

LOCATIONS:
1. Gloucester, MA - Main Processing Plant - TIV: USD 22,000,000
   Occupancy: Fish processing (filleting, smoking, packaging), blast freezing, cold storage (-25C)
   Construction: Masonry and steel frame, insulated metal panel cold rooms
   Built: 1992, significantly renovated 2020 and again 2025 (post-loss)
   Sprinklered: Yes, wet pipe (processing areas), dry pipe (cold storage)

2. Portland, ME - Secondary Processing & Distribution - TIV: USD 14,000,000
   Occupancy: Shellfish processing, packaging, refrigerated distribution
   Construction: Tilt-up concrete, 2008
   Sprinklered: Yes

3. New Bedford, MA - Cold Storage Warehouse - TIV: USD 9,000,000
   Occupancy: Frozen seafood storage, -20C to -30C
   Construction: Insulated metal panels on steel frame, 2015
   Sprinklered: Dry pipe

4. Boston, MA - Office & Sales - TIV: USD 5,000,000
   Occupancy: Corporate offices
   Construction: Fire-resistive, multi-tenant office building

PRIOR LARGE LOSS - GLOUCESTER FACILITY (2024):
On 18th August 2024, an ammonia refrigerant leak in the Gloucester facility's main compressor room led to an explosion and subsequent fire. The fire spread to the adjacent processing hall before being brought under control by the fire department. Fortunately, no fatalities occurred, though three employees were treated for minor ammonia exposure.

LOSS DETAILS:
- Property Damage: USD 6,800,000 (compressor room, processing hall, cold storage inventory)
- Business Interruption: USD 3,400,000 (facility was offline for 4.5 months)
- TOTAL INCURRED: USD 10,200,000
- STATUS: Closed. All repairs completed. Facility returned to full operations January 2025.

REMEDIATION & RISK IMPROVEMENTS (USD 2.8M investment by the insured):
1. Complete replacement of ammonia refrigeration system with modern CO2/ammonia cascade system incorporating leak detection and automatic isolation
2. Installation of blast-resistant walls around new compressor room
3. Upgraded fire detection (aspirating smoke detection) and suppression throughout
4. New emergency ventilation system in all refrigeration areas
5. Comprehensive ammonia safety training programme for all staff
6. Engagement of a specialist refrigeration risk engineer (Stellar Engineering) for ongoing quarterly inspections
7. Full compliance with IIAR-2 (International Institute of Ammonia Refrigeration) standards

PRIOR 5-YEAR LOSS HISTORY (excluding the 2024 event):
- 2023: Compressor motor failure, Gloucester. Incurred: USD 65,000 (Equipment Breakdown)
- No other losses.

TOTAL 5-YEAR INCURRED (including 2024 event): USD 10,265,000

EXPIRING TERMS:
- Premium: USD 162,000 (rate: 0.324%)
- Deductible: USD 100,000
- Note: These were already loaded at last renewal following the loss. We understand further adjustment may be required but would ask for a measured approach given the significant investment in risk improvement.

ATTACHMENTS:
1. Updated SOV (Excel)
2. 5-Year Loss Runs (PDF)
3. Post-loss remediation report with photographs
4. Stellar Engineering quarterly inspection report (Q4 2025)
5. Ammonia safety management programme documentation
6. CO2/ammonia cascade system specifications

We are committed to this market and the insured has demonstrated their commitment to risk improvement through significant capital investment. We respectfully request your best renewal terms and look forward to discussing.

Kind regards,

Andrew Patel
Executive Director, Property Broking
BMS Group Ltd
Bishopsgate Court, 4-12 Norton Folgate, London E1 6DB
Tel: +44 (0)20 7480 XXXX
andrew.patel@bmsgroup.com
"""
    },
    # 10 - Summit Office Partners (FOLLOW placement)
    {
        "file": "SUB-2026-0010_summit_office.eml",
        "from": "Laura Simpson <laura.simpson@edbroking.com>",
        "cc": "property.placements@edbroking.com",
        "subject": "New Business Submission - Summit Office Partners LP - Office Property - $75M TIV - 6 Locations - FOLLOW Placement (Chubb Lead)",
        "date": datetime(2026, 2, 18, 16, 30, tzinfo=timezone.utc),
        "tag": "sub-2026-0010",
        "body": """Dear TMHCC Property Team,

We are seeking follow capacity on the below commercial property placement. Chubb have agreed to lead this programme and we are now approaching follow markets for the remaining capacity.

SUBMISSION REFERENCE: SUB-2026-0010

NAMED INSURED: Summit Office Partners LP
RISK TYPE: Commercial Property - Class A Office Portfolio
TOTAL INSURED VALUES: USD 75,000,000
NUMBER OF LOCATIONS: 6

LEAD MARKET: Chubb (25% signed line)
CAPACITY SOUGHT FROM FOLLOW MARKETS: 75% remaining (seeking lines of 10-25%)

LOCATIONS:
1. One Summit Plaza, Charlotte, NC 28202 - 18-storey Class A office tower - TIV: USD 22,000,000
2. Summit Tech Centre, Raleigh, NC 27601 - 6-storey office/lab building - TIV: USD 15,000,000
3. Summit Financial Centre, Atlanta, GA 30303 - 12-storey office tower - TIV: USD 14,000,000
4. Summit Midtown, Nashville, TN 37203 - 8-storey mixed-use (office/retail) - TIV: USD 10,000,000
5. Summit Greenville, Greenville, SC 29601 - 4-storey suburban office park - TIV: USD 8,000,000
6. Summit Harbour, Jacksonville, FL 32202 - 10-storey waterfront office - TIV: USD 6,000,000

CONSTRUCTION: All properties are fire-resistive or non-combustible construction. All fully sprinklered. Majority are multi-tenant with institutional-quality fit-out.

AGREED LEAD TERMS (Chubb):
- Limit: USD 75,000,000 blanket per occurrence
- AOP Deductible: USD 50,000
- Named Windstorm Deductible: 3% of TIV at affected location, USD 100,000 minimum
- Flood Deductible: USD 250,000
- EQ Deductible: 5% of TIV at affected location
- Coverage: All-Risk including Named Windstorm, Flood, EQ, Equipment Breakdown, BI (12 months)
- Rate: 0.095% on TIV
- Premium: USD 71,250 (100% basis)
- Brokerage: 20%

INCEPTION: 1st May 2026

LOSS HISTORY: Claims-free for the last 7 years under prior carrier (Zurich).

LEAD SLIP: Attached for your reference. Chubb signed at 25% on 12th February 2026.

We would welcome a written line of 15-25% on the above terms. Please note we are looking to close this placement by 15th March 2026.

ATTACHMENTS:
1. SOV Schedule (Excel)
2. Lead Market Slip (Chubb signed)
3. ACORD 140 Application
4. 7-Year Loss-Free Letter
5. Property photographs

Please let us know if you require any additional information. Happy to discuss by phone.

Best regards,

Laura Simpson
Associate Director, Property Broking
Ed Broking LLP
Plantation Place South, 60 Great Tower Street, London EC3R 5AZ
Tel: +44 (0)20 3700 XXXX
laura.simpson@edbroking.com
"""
    },
]

# ── 15 Additional Initial Submissions ────────────────────────────────────────

ADDITIONAL_INITIAL = [
    {
        "file": "SUB-2026-0011_continental_bakeries.eml",
        "from": "Fiona McCarthy <fiona.mccarthy@ajg.com>",
        "cc": None,
        "subject": "New Business Submission - Continental Bakeries Group - Food Processing - $42M TIV - 3 Locations",
        "date": _rand_date("2025-10-01", "2026-01-15"),
        "tag": "sub-2026-0011",
        "body": """Dear Submissions Team,

Please find below a new property submission for your consideration.

SUBMISSION REFERENCE: SUB-2026-0011

NAMED INSURED: Continental Bakeries Group Inc
RISK TYPE: Commercial Property - Food Manufacturing / Bakery
TOTAL INSURED VALUES: USD 42,000,000
NUMBER OF LOCATIONS: 3

LOCATIONS:
1. Main bakery production facility, Edison, NJ - TIV: USD 24,000,000 (industrial bakery, continuous production lines, bulk flour/sugar storage)
2. Distribution centre, Allentown, PA - TIV: USD 11,000,000 (temperature-controlled warehouse)
3. Corporate offices, Newark, NJ - TIV: USD 7,000,000

CONSTRUCTION: Locations 1 & 2 are non-combustible steel frame with concrete block walls, fully sprinklered. Location 3 is fire-resistive multi-tenant.

COVERAGE: All-Risk Property, Business Interruption (12 months), Equipment Breakdown, Spoilage, Transit. Seeking USD 42M blanket limit, USD 50,000 deductible.

INCEPTION: 1st March 2026

LOSS HISTORY: Minor conveyor belt fire in 2023, incurred USD 32,000. No other claims in 5 years.

ATTACHMENTS: SOV, ACORD 140, 5-year loss runs attached.

The insured supplies private-label baked goods to major grocery chains and has annual revenue of approximately USD 110M. Well-managed risk with strong housekeeping practices.

Please let me know if you require any further information.

Best regards,
Fiona McCarthy
Gallagher Specialty
fiona.mccarthy@ajg.com
"""
    },
    {
        "file": "SUB-2026-0012_sunbelt_self_storage.eml",
        "from": "Kevin O'Brien <kevin.obrien@aon.com>",
        "cc": "property.team@aon.com",
        "subject": "New Business Submission - Sunbelt Self Storage REIT - Self Storage Property - $88M TIV - 30 Locations",
        "date": _rand_date("2025-11-01", "2026-01-31"),
        "tag": "sub-2026-0012",
        "body": """Dear TMHCC Property Underwriters,

SUBMISSION REFERENCE: SUB-2026-0012

NAMED INSURED: Sunbelt Self Storage REIT Inc
RISK TYPE: Commercial Property - Self Storage Portfolio
TOTAL INSURED VALUES: USD 88,000,000
NUMBER OF LOCATIONS: 30

OVERVIEW: The insured is a publicly traded self-storage REIT operating 30 facilities across the Sun Belt states (FL, GA, TX, AZ, NC, SC). Average facility is approximately 55,000 sq ft with climate-controlled and non-climate-controlled units.

CONSTRUCTION: Mix of single-storey masonry/steel frame. Climate-controlled buildings have insulated metal panels. All facilities have fire alarm systems; 18 of 30 have sprinkler protection.

WINDSTORM EXPOSURE: 12 locations in coastal FL and TX counties. All constructed to post-2002 Florida Building Code or equivalent standards.

COVERAGE REQUESTED:
- All-Risk including Named Windstorm and Flood
- USD 88M blanket limit
- Windstorm deductible: 5% of TIV at affected location
- AOP deductible: USD 25,000
- Business Interruption 12 months

INCEPTION: 1st April 2026

LOSS HISTORY: Two minor wind claims totalling USD 67,000 over 5 years. Clean record otherwise.

ATTACHMENTS: SOV, application, loss runs, sample property photos.

We look forward to your indication.

Kevin O'Brien
Vice President, Real Estate Practice
Aon
kevin.obrien@aon.com
"""
    },
    {
        "file": "SUB-2026-0013_precision_pharma.eml",
        "from": "Natasha Volkov <natasha.volkov@marsh.com>",
        "cc": "life.sciences.property@marsh.com",
        "subject": "New Submission - Precision Pharmaceuticals Inc - Life Sciences Property - $155M TIV - 4 Locations",
        "date": _rand_date("2025-12-01", "2026-02-15"),
        "tag": "sub-2026-0013",
        "body": """Dear TMHCC Underwriting Team,

SUBMISSION REFERENCE: SUB-2026-0013

NAMED INSURED: Precision Pharmaceuticals Inc
RISK TYPE: Commercial Property - Pharmaceutical Manufacturing & R&D
TOTAL INSURED VALUES: USD 155,000,000
NUMBER OF LOCATIONS: 4

LOCATIONS:
1. API Manufacturing Facility, Research Triangle Park, NC - TIV: USD 65,000,000
   Occupancy: Active pharmaceutical ingredient synthesis, clean rooms (ISO 5-7)
   Construction: Reinforced concrete, purpose-built 2016, fully sprinklered

2. Finished Dosage Facility, Morristown, NJ - TIV: USD 48,000,000
   Occupancy: Tablet compression, coating, packaging
   Construction: Fire-resistive, 2010, fully sprinklered

3. R&D Laboratory, Cambridge, MA - TIV: USD 28,000,000
   Occupancy: Research laboratories, pilot plant
   Construction: Fire-resistive, leased space in multi-tenant biotech campus

4. Cold Chain Distribution Centre, Memphis, TN - TIV: USD 14,000,000
   Occupancy: Temperature-controlled pharmaceutical distribution (-20C to +25C)
   Construction: Tilt-up concrete, 2019

COVERAGE: All-Risk Property, BI (24 months, extended indemnity), Equipment Breakdown, Spoilage (temperature-sensitive products), Transit, Ordinance or Law.

LIMITS: USD 100,000,000 per occurrence
DEDUCTIBLE: USD 250,000 AOP; 72-hour BI waiting period

INCEPTION: 1st July 2026

LOSS HISTORY: No property losses in 8 years of operations. One equipment breakdown claim (HVAC failure at Cambridge lab, USD 18,000) in 2024.

KEY CONSIDERATIONS:
- High concentration of M&E values (specialised pharmaceutical equipment)
- Critical temperature control requirements
- FDA-regulated facilities; any property loss could trigger regulatory consequences
- Contingent BI exposure (single-source API supply for two oncology drugs)

ATTACHMENTS: SOV, ACORD 140, loss runs, FDA inspection history, business continuity plan.

Regards,
Natasha Volkov
Managing Director, Life Sciences
Marsh Specialty
natasha.volkov@marsh.com
"""
    },
    {
        "file": "SUB-2026-0014_liberty_lumber.eml",
        "from": "Robert Dawson <robert.dawson@wtwco.com>",
        "cc": None,
        "subject": "New Submission - Liberty Lumber & Timber Inc - Forestry/Wood Products - $22M TIV - 2 Locations",
        "date": _rand_date("2025-11-15", "2026-01-20"),
        "tag": "sub-2026-0014",
        "body": """Dear Property Team,

SUBMISSION REFERENCE: SUB-2026-0014

NAMED INSURED: Liberty Lumber & Timber Inc
RISK TYPE: Commercial Property - Sawmill & Timber Processing
TOTAL INSURED VALUES: USD 22,000,000
NUMBER OF LOCATIONS: 2

LOCATION 1: Sawmill and lumber yard, Bend, OR 97701 - TIV: USD 16,000,000
LOCATION 2: Kiln-drying and planing facility, Eugene, OR 97402 - TIV: USD 6,000,000

OCCUPANCY: Softwood lumber production (Douglas fir, pine). Sawmill processes approximately 80 million board feet per annum. Kiln-drying facility has 12 dry kilns.

CONSTRUCTION: Both locations are a mix of heavy timber and steel frame construction. Open-sided log storage and lumber yards. Enclosed processing buildings.

FIRE PROTECTION: Bend - hydrant system with fire pump, no sprinklers in sawmill (outdoor operations), sprinklered in offices and maintenance buildings. Eugene - fully sprinklered dry kilns and planing mill, fire pump, dedicated fire brigade.

COVERAGE: All-Risk, BI (12 months), Equipment Breakdown, Wildfire sublimit.
LIMIT: USD 22,000,000 blanket
DEDUCTIBLE: USD 75,000

INCEPTION: 1st May 2026

LOSS HISTORY: Kiln fire in 2022, incurred USD 210,000. Sawblade incident damaging carriage in 2024, USD 45,000. No other losses.

ATTACHMENTS: SOV, application, loss runs, fire prevention plan, wildfire defensible space assessment.

Kind regards,
Robert Dawson
Willis Towers Watson
robert.dawson@wtwco.com
"""
    },
    {
        "file": "SUB-2026-0015_greenfield_cannabis.eml",
        "from": "Marcus Lee <marcus.lee@howdengroup.com>",
        "cc": "specialty.property@howdengroup.com",
        "subject": "New Business Submission - Greenfield Cultivation LLC - Cannabis Cultivation & Processing - $18M TIV - 1 Location",
        "date": _rand_date("2025-12-01", "2026-02-28"),
        "tag": "sub-2026-0015",
        "body": """Dear Underwriters,

SUBMISSION REFERENCE: SUB-2026-0015

NAMED INSURED: Greenfield Cultivation LLC
RISK TYPE: Commercial Property - Licensed Cannabis Cultivation & Processing
TOTAL INSURED VALUES: USD 18,000,000
NUMBER OF LOCATIONS: 1

LOCATION: 400 Industrial Avenue, Denver, CO 80216
AREA: 120,000 sq ft indoor cultivation and processing facility
CONSTRUCTION: Tilt-up concrete, purpose-built 2022
SPRINKLERED: Yes, wet pipe throughout
SECURITY: 24/7 on-site security, access control, comprehensive CCTV as required by Colorado MED regulations

VALUES BREAKDOWN:
- Building: USD 5,500,000
- Contents (growing equipment, HVAC, lighting, extraction equipment): USD 6,000,000
- Stock (growing plants, harvested product, finished goods): USD 3,500,000
- Business Interruption (12 months): USD 3,000,000

COVERAGE: All-Risk Property, BI, Equipment Breakdown, Spoilage (crop loss), Transit (to licensed dispensaries).
LIMIT: USD 18,000,000
DEDUCTIBLE: USD 50,000

INCEPTION: 1st June 2026

LOSS HISTORY: No claims. Facility opened in 2022 under current ownership.

NOTE: The insured holds all required state and local licenses. We can provide full licensing documentation. The insured does NOT engage in any federally prohibited interstate commerce. All operations are within the State of Colorado.

ATTACHMENTS: SOV, application, loss runs, Colorado MED license, facility photos, security plan.

Regards,
Marcus Lee
Howden Broking Group
marcus.lee@howdengroup.com
"""
    },
    {
        "file": "SUB-2026-0016_harbour_marina.eml",
        "from": "Samantha Drake <samantha.drake@lockton.com>",
        "cc": None,
        "subject": "New Submission - Harbour Point Marina & Resort - Hospitality/Marine - $30M TIV - 1 Location - Coastal NC",
        "date": _rand_date("2025-10-15", "2026-01-31"),
        "tag": "sub-2026-0016",
        "body": """Dear TMHCC Property Team,

SUBMISSION REFERENCE: SUB-2026-0016

NAMED INSURED: Harbour Point Marina & Resort LLC
RISK TYPE: Commercial Property - Marina & Hospitality
TOTAL INSURED VALUES: USD 30,000,000
NUMBER OF LOCATIONS: 1 (multi-structure campus)

LOCATION: 1 Marina Drive, Wrightsville Beach, NC 28480

FACILITY COMPRISES:
- 60-room boutique hotel (3-storey, wood frame on elevated pilings, built 2015)
- Full-service restaurant and event centre
- 120-slip marina with floating docks and fuel dock
- Ship's store and marina office
- Swimming pool and spa facility

VALUES:
- Buildings: USD 18,000,000
- Contents/FF&E: USD 5,000,000
- Marina structures (docks, pilings, fuel systems): USD 4,000,000
- Business Interruption: USD 3,000,000

WINDSTORM EXPOSURE: Located on the NC Outer Banks barrier island. The hotel is constructed on reinforced concrete pilings with first habitable floor 14 feet above sea level. Windows and doors rated to 150mph impact. The insured has a comprehensive hurricane preparedness plan including dock de-tensioning procedures.

COVERAGE: All-Risk including Named Windstorm, Flood (Zone VE), BI.
LIMIT: USD 30,000,000
WINDSTORM DEDUCTIBLE: 5% of TIV, USD 250,000 minimum
FLOOD DEDUCTIBLE: USD 500,000
AOP DEDUCTIBLE: USD 25,000

INCEPTION: 1st June 2026

LOSS HISTORY: Hurricane Florence (2018) caused USD 1.8M damage to marina docks (prior ownership). Current owner rebuilt to enhanced specifications. No losses under current ownership (2019-present).

ATTACHMENTS: SOV, application, loss runs, wind mitigation inspection, flood elevation certificate, marina photos.

Regards,
Samantha Drake
Lockton Companies LLP
samantha.drake@lockton.com
"""
    },
    {
        "file": "SUB-2026-0017_sterling_auto.eml",
        "from": "Jonathan Pierce <jonathan.pierce@bmsgroup.com>",
        "cc": None,
        "subject": "New Submission - Sterling Automotive Group - Auto Dealership Portfolio - $110M TIV - 15 Locations",
        "date": _rand_date("2025-11-01", "2026-02-15"),
        "tag": "sub-2026-0017",
        "body": """Dear Property Underwriting,

SUBMISSION REFERENCE: SUB-2026-0017

NAMED INSURED: Sterling Automotive Group LLC
RISK TYPE: Commercial Property - Automobile Dealerships
TOTAL INSURED VALUES: USD 110,000,000
NUMBER OF LOCATIONS: 15

OVERVIEW: The insured operates 15 franchised automobile dealerships across the Mid-Atlantic and Southeast US. Brands include BMW, Mercedes-Benz, Lexus, Honda, and Toyota. Facilities include showrooms, service centres, parts departments, and body shops.

LOCATIONS: Virginia (5), Maryland (4), North Carolina (3), South Carolina (3)

CONSTRUCTION: Predominantly masonry/steel frame, single and two-storey. All showrooms have large glass frontages. Service centres equipped with vehicle lifts, paint booths, and parts storage. All locations sprinklered.

VALUES INCLUDE:
- Buildings: USD 55,000,000
- Contents/Equipment: USD 15,000,000
- Dealer Vehicle Inventory: USD 30,000,000 (average inventory value)
- Business Interruption: USD 10,000,000

COVERAGE: All-Risk including Windstorm, Flood, Equipment Breakdown, BI (12 months). Open lot coverage for vehicle inventory (hail, wind, flood).
LIMIT: USD 75,000,000 per occurrence
DEDUCTIBLE: USD 100,000 AOP; 2% for hail damage to vehicle inventory

INCEPTION: 1st April 2026

LOSS HISTORY: Hail damage to vehicle inventory at Charlotte, NC location in 2024, incurred USD 380,000. No other losses in 5 years.

ATTACHMENTS: SOV, application, loss runs.

Best,
Jonathan Pierce
BMS Group
jonathan.pierce@bmsgroup.com
"""
    },
    {
        "file": "SUB-2026-0018_evergreen_senior.eml",
        "from": "Diana Moss <diana.moss@marsh.com>",
        "cc": "healthcare.property@marsh.com",
        "subject": "New Submission - Evergreen Senior Living Corp - Healthcare/Senior Living - $62M TIV - 5 Locations",
        "date": _rand_date("2025-12-15", "2026-02-28"),
        "tag": "sub-2026-0018",
        "body": """Dear TMHCC Underwriting,

SUBMISSION REFERENCE: SUB-2026-0018

NAMED INSURED: Evergreen Senior Living Corp
RISK TYPE: Commercial Property - Senior Living / Assisted Living Facilities
TOTAL INSURED VALUES: USD 62,000,000
NUMBER OF LOCATIONS: 5

PORTFOLIO: Five assisted living and memory care communities across the Northeast US:
1. Evergreen at Westchester, White Plains, NY - 120 units - TIV: USD 18,000,000
2. Evergreen at Princeton, Princeton, NJ - 95 units - TIV: USD 14,000,000
3. Evergreen at Bryn Mawr, Bryn Mawr, PA - 80 units - TIV: USD 12,000,000
4. Evergreen at Greenwich, Greenwich, CT - 110 units - TIV: USD 11,000,000
5. Evergreen at Wellesley, Wellesley, MA - 60 units - TIV: USD 7,000,000

CONSTRUCTION: All facilities are fire-resistive or non-combustible, fully sprinklered, with emergency generator backup. All built or substantially renovated within the last 15 years. Life safety systems exceed code requirements given the vulnerable occupant population.

COVERAGE: All-Risk Property, BI including Extra Expense (24 months - critical due to resident relocation requirements), Equipment Breakdown, Ordinance or Law.
LIMIT: USD 62,000,000 blanket
DEDUCTIBLE: USD 50,000

INCEPTION: 1st July 2026

LOSS HISTORY: Kitchen grease fire at Princeton location in 2023, quickly suppressed by Ansul system. Property damage USD 12,000. No other losses in 6 years.

KEY CONSIDERATION: Evacuation and temporary relocation of elderly/memory care residents is extremely costly and disruptive; hence the extended BI period request.

ATTACHMENTS: SOV, application, loss runs, life safety compliance certificates.

Kind regards,
Diana Moss
Marsh Ltd
diana.moss@marsh.com
"""
    },
    {
        "file": "SUB-2026-0019_trident_cold_storage.eml",
        "from": "Oliver Grant <oliver.grant@edbroking.com>",
        "cc": None,
        "subject": "New Submission - Trident Cold Storage Inc - Refrigerated Warehousing - $40M TIV - 3 Locations",
        "date": _rand_date("2025-11-15", "2026-02-15"),
        "tag": "sub-2026-0019",
        "body": """Dear Property Team,

SUBMISSION REFERENCE: SUB-2026-0019

NAMED INSURED: Trident Cold Storage Inc
RISK TYPE: Commercial Property - Temperature-Controlled Warehousing
TOTAL INSURED VALUES: USD 40,000,000
NUMBER OF LOCATIONS: 3

LOCATIONS:
1. Jacksonville, FL - 200,000 sq ft multi-temp warehouse (-25F to +35F) - TIV: USD 18,000,000
2. Savannah, GA - 150,000 sq ft frozen storage (-20F) - TIV: USD 13,000,000
3. Norfolk, VA - 100,000 sq ft refrigerated cross-dock - TIV: USD 9,000,000

REFRIGERANT: Ammonia-based systems at all locations. All compliant with EPA RMP and OSHA PSM requirements. Annual third-party inspections by Global Cold Chain Alliance certified engineers.

CONSTRUCTION: Insulated metal panels on steel frame, concrete floors, built 2010-2018. All sprinklered (dry pipe in freezer areas, wet pipe elsewhere).

COVERAGE: All-Risk, BI (12 months), Equipment Breakdown (critical for refrigeration), Spoilage/Contamination, Ammonia Release/Cleanup sublimit.
LIMIT: USD 40,000,000
DEDUCTIBLE: USD 100,000 AOP; USD 250,000 ammonia release

INCEPTION: 1st May 2026

LOSS HISTORY: Evaporator coil failure at Jacksonville, 2024, spoilage claim USD 95,000. No other losses.

ATTACHMENTS: SOV, application, loss runs, ammonia safety programme, RMP executive summary.

Regards,
Oliver Grant
Ed Broking
oliver.grant@edbroking.com
"""
    },
    {
        "file": "SUB-2026-0020_pioneer_renewable.eml",
        "from": "Hannah Clarke <hannah.clarke@mcgillandpartners.com>",
        "cc": "renewables@mcgillandpartners.com",
        "subject": "New Submission - Pioneer Renewable Energy LLC - Solar Farm Portfolio - $78M TIV - 6 Locations",
        "date": _rand_date("2026-01-01", "2026-03-15"),
        "tag": "sub-2026-0020",
        "body": """Dear TMHCC Property Underwriting,

SUBMISSION REFERENCE: SUB-2026-0020

NAMED INSURED: Pioneer Renewable Energy LLC
RISK TYPE: Commercial Property - Utility-Scale Solar Photovoltaic
TOTAL INSURED VALUES: USD 78,000,000
NUMBER OF LOCATIONS: 6 solar farms

PORTFOLIO:
1. Pioneer Solar I - Fresno County, CA - 50MW - TIV: USD 18,000,000
2. Pioneer Solar II - Imperial County, CA - 40MW - TIV: USD 14,000,000
3. Pioneer Solar III - Maricopa County, AZ - 60MW - TIV: USD 20,000,000
4. Pioneer Solar IV - Clark County, NV - 35MW - TIV: USD 12,000,000
5. Pioneer Solar V - Dona Ana County, NM - 25MW - TIV: USD 8,000,000
6. Pioneer Solar VI - El Paso County, TX - 20MW - TIV: USD 6,000,000

Total Capacity: 230MW (AC)

EQUIPMENT: Bifacial monocrystalline PV modules (Tier 1 manufacturers: LONGi, Jinko), single-axis trackers, central inverters, step-up transformers, SCADA/monitoring systems.

COVERAGE: All-Risk Property including Windstorm, Hail, Flood, Earthquake, Equipment Breakdown, BI/DSU (based on PPA revenue), Transit.
LIMIT: USD 78,000,000 blanket
DEDUCTIBLE: USD 250,000 AOP; USD 500,000 CAT perils
BI WAITING PERIOD: 60 days

INCEPTION: 1st July 2026

HAIL EXPOSURE: Primary peril concern. All trackers equipped with hail stow functionality (modules rotate to near-vertical at >1 inch hail forecast). Weather monitoring stations at each site.

LOSS HISTORY: No losses. All facilities commissioned between 2021-2024.

ATTACHMENTS: SOV, application, equipment specifications, hail stow protocol documentation, PPA summaries, aerial photographs.

Kind regards,
Hannah Clarke
McGill and Partners
hannah.clarke@mcgillandpartners.com
"""
    },
    {
        "file": "SUB-2026-0021_apex_logistics.eml",
        "from": "Gary Brennan <gary.brennan@aon.com>",
        "cc": None,
        "subject": "New Submission - Apex Logistics & Fulfilment Inc - E-Commerce Fulfilment - $55M TIV - 4 Locations",
        "date": _rand_date("2025-10-15", "2026-02-28"),
        "tag": "sub-2026-0021",
        "body": """Dear TMHCC Property Team,

SUBMISSION REFERENCE: SUB-2026-0021

NAMED INSURED: Apex Logistics & Fulfilment Inc
RISK TYPE: Commercial Property - E-Commerce Fulfilment / Warehousing
TOTAL INSURED VALUES: USD 55,000,000
NUMBER OF LOCATIONS: 4

LOCATIONS:
1. Indianapolis, IN - 500,000 sq ft fulfilment centre - TIV: USD 22,000,000
2. Dallas, TX - 350,000 sq ft fulfilment centre - TIV: USD 15,000,000
3. Reno, NV - 250,000 sq ft fulfilment centre - TIV: USD 12,000,000
4. Lehigh Valley, PA - 200,000 sq ft fulfilment centre - TIV: USD 6,000,000

CONSTRUCTION: All tilt-up concrete or steel frame with metal cladding, high-bay racking (40ft clear height), ESFR sprinklers, fully automated sortation and conveying systems.

STOCK PROFILE: General merchandise, consumer electronics, health and beauty, pet supplies. High inventory turnover (average dwell time 14 days). Peak inventory values 40% higher during Q4 holiday season.

COVERAGE: All-Risk, BI (12 months), Equipment Breakdown (automated systems), Stock Throughput, Transit.
LIMIT: USD 55,000,000
DEDUCTIBLE: USD 100,000

INCEPTION: 1st April 2026

LOSS HISTORY: Conveyor system fire (electrical fault) at Indianapolis in 2023, incurred USD 145,000 (property damage and contents). No other losses.

ATTACHMENTS: SOV, application, loss runs, fire protection system details, racking layout diagrams.

Best regards,
Gary Brennan
Aon
gary.brennan@aon.com
"""
    },
    {
        "file": "SUB-2026-0022_coastal_brewing.eml",
        "from": "Sophie Reynolds <sophie.reynolds@lockton.com>",
        "cc": None,
        "subject": "New Submission - Coastal Brewing Company - Craft Brewery - $15M TIV - 1 Location",
        "date": _rand_date("2025-12-01", "2026-03-15"),
        "tag": "sub-2026-0022",
        "body": """Dear Underwriting Team,

SUBMISSION REFERENCE: SUB-2026-0022

NAMED INSURED: Coastal Brewing Company LLC
RISK TYPE: Commercial Property - Craft Brewery & Taproom
TOTAL INSURED VALUES: USD 15,000,000
NUMBER OF LOCATIONS: 1

LOCATION: 250 Harbour Way, San Diego, CA 92101
AREA: 45,000 sq ft (brewing 25,000 / barrel storage 10,000 / taproom & events 10,000)
CONSTRUCTION: Masonry and steel, built 1960, extensively renovated 2019
SPRINKLERED: Yes, wet pipe throughout
OCCUPANCY: Craft beer production (60,000 barrels/year), taproom, event space, canning line

VALUES:
- Building: USD 4,500,000
- Brewing Equipment (brew house, fermenters, brite tanks, canning line, cooling): USD 5,500,000
- Stock (raw materials, WIP, finished product): USD 2,000,000
- Business Interruption: USD 3,000,000

COVERAGE: All-Risk, BI, Equipment Breakdown, Spoilage, Earthquake.
LIMIT: USD 15,000,000
DEDUCTIBLE: USD 25,000 AOP; 5% EQ
INCEPTION: 1st June 2026

LOSS HISTORY: No claims in 5 years of operation.

ATTACHMENTS: SOV, application, loss runs, brewery photos.

Best,
Sophie Reynolds
Lockton Companies
sophie.reynolds@lockton.com
"""
    },
    {
        "file": "SUB-2026-0023_metro_parking.eml",
        "from": "Alan Crawford <alan.crawford@wtwco.com>",
        "cc": None,
        "subject": "New Submission - Metro Parking Systems Inc - Parking Structures - $48M TIV - 7 Locations",
        "date": _rand_date("2025-11-01", "2026-02-15"),
        "tag": "sub-2026-0023",
        "body": """Dear TMHCC Property,

SUBMISSION REFERENCE: SUB-2026-0023

NAMED INSURED: Metro Parking Systems Inc
RISK TYPE: Commercial Property - Parking Structures
TOTAL INSURED VALUES: USD 48,000,000
NUMBER OF LOCATIONS: 7

PORTFOLIO: Seven multi-storey parking structures in major US cities: Chicago (2), Minneapolis, Milwaukee, Detroit, Cleveland, Pittsburgh. Capacities range from 400 to 1,200 vehicles per structure.

CONSTRUCTION: All are reinforced concrete, post-tensioned slab construction. Ages range from 1985 to 2015. All open-sided (natural ventilation). EV charging stations installed at 4 locations.

COVERAGE: All-Risk Property, BI, Equipment Breakdown (elevators, access control systems, EV chargers), Collapse.
LIMIT: USD 48,000,000 blanket
DEDUCTIBLE: USD 50,000

INCEPTION: 1st April 2026

LOSS HISTORY: Vehicle fire in Chicago structure in 2024, limited damage to structure (concrete is inherently fire-resistive), incurred USD 28,000 for smoke cleaning and concrete spall repair. No other claims.

ATTACHMENTS: SOV, application, loss runs, structural condition assessments.

Regards,
Alan Crawford
Willis Towers Watson
alan.crawford@wtwco.com
"""
    },
    {
        "file": "SUB-2026-0024_pinnacle_healthcare.eml",
        "from": "Rebecca Torres <rebecca.torres@ajg.com>",
        "cc": "healthcare@ajg.com",
        "subject": "New Submission - Pinnacle Healthcare Properties REIT - Medical Office Buildings - $92M TIV - 10 Locations",
        "date": _rand_date("2026-01-01", "2026-03-15"),
        "tag": "sub-2026-0024",
        "body": """Dear Property Underwriters,

SUBMISSION REFERENCE: SUB-2026-0024

NAMED INSURED: Pinnacle Healthcare Properties REIT
RISK TYPE: Commercial Property - Medical Office Buildings
TOTAL INSURED VALUES: USD 92,000,000
NUMBER OF LOCATIONS: 10

PORTFOLIO: Ten medical office buildings (MOBs) located on or adjacent to hospital campuses across the Midwest and Southeast US. Multi-tenant properties leased to physician groups, outpatient surgery centres, imaging centres, and rehabilitation clinics.

LOCATIONS: Ohio (3), Kentucky (2), Tennessee (2), Indiana (2), Alabama (1)
CONSTRUCTION: All fire-resistive or non-combustible, 2-6 storeys, fully sprinklered, emergency generators.

COVERAGE: All-Risk, BI (18 months), Equipment Breakdown, Ordinance or Law.
LIMIT: USD 92,000,000 blanket
DEDUCTIBLE: USD 75,000

INCEPTION: 1st July 2026

LOSS HISTORY: Clean. No claims in 8 years.

ATTACHMENTS: SOV, application, loss-free letter.

Kind regards,
Rebecca Torres
Gallagher
rebecca.torres@ajg.com
"""
    },
    {
        "file": "SUB-2026-0025_iron_mountain_mining.eml",
        "from": "Patrick Sullivan <patrick.sullivan@millerinsurance.com>",
        "cc": None,
        "subject": "New Submission - Iron Mountain Mining Services Corp - Mining Support Property - $38M TIV - 2 Locations",
        "date": _rand_date("2025-12-01", "2026-03-01"),
        "tag": "sub-2026-0025",
        "body": """Dear TMHCC Underwriting,

SUBMISSION REFERENCE: SUB-2026-0025

NAMED INSURED: Iron Mountain Mining Services Corp
RISK TYPE: Commercial Property - Mining Support Services (Surface Facilities Only)
TOTAL INSURED VALUES: USD 38,000,000
NUMBER OF LOCATIONS: 2

LOCATIONS:
1. Equipment maintenance and overhaul facility, Elko, NV - TIV: USD 26,000,000
   Occupancy: Heavy equipment maintenance, welding, machine shop, parts warehouse
   Construction: Steel frame with metal cladding, 80,000 sq ft, built 2012
   Contents include fleet of haul trucks, excavators, drill rigs (when in for service)

2. Administrative offices and training centre, Salt Lake City, UT - TIV: USD 12,000,000
   Construction: Fire-resistive office building, 2008

COVERAGE: All-Risk Property, BI, Equipment Breakdown, Inland Marine (mobile equipment).
LIMIT: USD 38,000,000
DEDUCTIBLE: USD 100,000

INCEPTION: 1st May 2026

NOTE: This submission is for SURFACE FACILITIES ONLY. No underground mining property is included. The insured provides contract mining services to gold and copper mining operations.

LOSS HISTORY: Welding spark ignited oil residue in maintenance bay in 2023, minor fire damage USD 55,000. No other losses.

ATTACHMENTS: SOV, application, loss runs, facility photos.

Regards,
Patrick Sullivan
Miller Insurance Services
patrick.sullivan@millerinsurance.com
"""
    },
]

# ── 5 Additional Renewal Submissions ─────────────────────────────────────────

RENEWAL_SUBS = [
    {
        "file": "SUB-2026-0026_renewal_premier_plastics.eml",
        "from": "Catherine Hall <catherine.hall@marsh.com>",
        "cc": None,
        "subject": "Renewal Submission - Premier Plastics Manufacturing Inc - Property - $33M TIV - Ref: PPM-TMHCC-2025-0091",
        "date": _rand_date("2026-01-15", "2026-03-15"),
        "tag": "sub-2026-0026",
        "body": """Dear TMHCC Underwriting Team,

SUBMISSION REFERENCE: SUB-2026-0026
EXISTING POLICY: PPM-TMHCC-2025-0091

We write to request renewal terms for Premier Plastics Manufacturing Inc.

NAMED INSURED: Premier Plastics Manufacturing Inc
RISK TYPE: Commercial Property - Plastics Injection Moulding
TIV: USD 33,000,000 (up 3% from expiry reflecting updated valuations)
LOCATIONS: 2 (Main plant in Akron, OH; warehouse in Canton, OH)
EXPIRY: 31st May 2026

EXPIRING TERMS: USD 33M blanket, USD 50,000 deductible, rate 0.105%, premium USD 33,600.

LOSS HISTORY: Clean. No claims during the 3-year relationship with TMHCC or in the 5 years prior.

CHANGES: No material changes from expiry. Same operations, same occupancy. Minor TIV increase only.

The insured expects flat renewal terms given the clean record. We look forward to your indication.

ATTACHMENTS: Updated SOV, ACORD 140, 8-year claims-free letter.

Best regards,
Catherine Hall
Marsh Ltd
catherine.hall@marsh.com
"""
    },
    {
        "file": "SUB-2026-0027_renewal_valley_textiles.eml",
        "from": "Simon Blake <simon.blake@howdengroup.com>",
        "cc": None,
        "subject": "Renewal Submission - Valley Textiles Ltd - Manufacturing Property - $19M TIV - Ref: VT-TMHCC-2025-0112",
        "date": _rand_date("2026-01-01", "2026-03-01"),
        "tag": "sub-2026-0027",
        "body": """Dear Property Team,

SUBMISSION REFERENCE: SUB-2026-0027
EXISTING POLICY: VT-TMHCC-2025-0112

Please find attached the renewal submission for Valley Textiles Ltd.

NAMED INSURED: Valley Textiles Ltd
RISK TYPE: Commercial Property - Textile Manufacturing
TIV: USD 19,000,000
LOCATIONS: 1 (Greenville, SC)
EXPIRY: 30th June 2026

OCCUPANCY: Cotton and synthetic blend textile weaving and finishing. 150,000 sq ft facility with weaving, dyeing, finishing, and warehousing.

CONSTRUCTION: Masonry mill-type construction (former historic mill), significantly renovated 2015. Fully sprinklered. Approved by FM Global.

EXPIRING: USD 19M blanket, USD 25,000 deductible, rate 0.12%, premium USD 22,800.

LOSS HISTORY: Dye tank overflow in 2024, minor water damage USD 8,500. Clean otherwise.

CHANGES: No changes from expiry. Insured requesting flat terms.

ATTACHMENTS: Updated SOV, loss runs, FM Global report.

Regards,
Simon Blake
Howden Broking Group
simon.blake@howdengroup.com
"""
    },
    {
        "file": "SUB-2026-0028_renewal_skyline_apartments.eml",
        "from": "Jennifer Walsh <jennifer.walsh@aon.com>",
        "cc": None,
        "subject": "Renewal Submission - Skyline Apartment Holdings LP - Multifamily Residential - $85M TIV - 5 Communities - Ref: SAH-TMHCC-2025-0203",
        "date": _rand_date("2026-02-01", "2026-03-31"),
        "tag": "sub-2026-0028",
        "body": """Dear TMHCC Underwriting,

SUBMISSION REFERENCE: SUB-2026-0028
EXISTING POLICY: SAH-TMHCC-2025-0203

NAMED INSURED: Skyline Apartment Holdings LP
RISK TYPE: Commercial Property - Multifamily Residential
TIV: USD 85,000,000 (up 6% from expiry - two communities revalued)
LOCATIONS: 5 apartment communities (Austin TX x2, San Antonio TX, Charlotte NC, Tampa FL)
TOTAL UNITS: 1,850
EXPIRY: 31st July 2026

CONSTRUCTION: All communities are 3-4 storey wood frame with concrete podium (Type V over Type I). Built 2014-2020. All sprinklered.

EXPIRING: USD 85M blanket, USD 100K AOP, 5% windstorm, rate 0.145%, premium USD 116,000.

LOSS HISTORY: Two water damage claims (burst pipes) totalling USD 42,000 in current year. Pipe insulation upgrades completed. Prior 4 years clean.

The insured has been a valued TMHCC client for 3 years. Requesting renewal at expiring terms given the de minimis loss experience.

ATTACHMENTS: Updated SOV, loss runs, pipe remediation report.

Best regards,
Jennifer Walsh
Aon
jennifer.walsh@aon.com
"""
    },
    {
        "file": "SUB-2026-0029_renewal_central_cold.eml",
        "from": "Richard Hobbs <richard.hobbs@wtwco.com>",
        "cc": None,
        "subject": "Renewal Submission - Central Cold Logistics Inc - Cold Storage - $27M TIV - 2 Locations - Ref: CCL-TMHCC-2025-0078",
        "date": _rand_date("2026-01-15", "2026-03-15"),
        "tag": "sub-2026-0029",
        "body": """Dear Underwriters,

SUBMISSION REFERENCE: SUB-2026-0029
EXISTING POLICY: CCL-TMHCC-2025-0078

NAMED INSURED: Central Cold Logistics Inc
RISK TYPE: Commercial Property - Refrigerated Warehousing
TIV: USD 27,000,000
LOCATIONS: 2 (Kansas City, MO and Memphis, TN)
EXPIRY: 30th June 2026

CONSTRUCTION: Insulated metal panels, steel frame, both built 2016. Ammonia refrigeration. Full sprinklers (dry pipe in freezer zones).

EXPIRING: USD 27M blanket, USD 75,000 deductible, rate 0.148%, premium USD 39,960.

LOSS HISTORY: Clean. No claims in 4 years with TMHCC.

CHANGES: TIV increase of 5% for updated equipment valuations. New CO2 cascade system installed at Kansas City (reducing ammonia charge by 40%).

ATTACHMENTS: Updated SOV, claims-free letter, CO2 system specifications.

Regards,
Richard Hobbs
Willis Towers Watson
richard.hobbs@wtwco.com
"""
    },
    {
        "file": "SUB-2026-0030_renewal_patriot_paper.eml",
        "from": "Elizabeth Morgan <elizabeth.morgan@lockton.com>",
        "cc": None,
        "subject": "Renewal Submission - Patriot Paper Products Inc - Paper Manufacturing - $44M TIV - 1 Location - Ref: PPP-TMHCC-2025-0156",
        "date": _rand_date("2026-02-01", "2026-03-31"),
        "tag": "sub-2026-0030",
        "body": """Dear TMHCC Property Team,

SUBMISSION REFERENCE: SUB-2026-0030
EXISTING POLICY: PPP-TMHCC-2025-0156

NAMED INSURED: Patriot Paper Products Inc
RISK TYPE: Commercial Property - Paper Manufacturing
TIV: USD 44,000,000
LOCATIONS: 1 (paper mill in Bangor, ME)
EXPIRY: 31st August 2026

OCCUPANCY: Corrugated cardboard and packaging paper manufacturing. Two paper machines, converting and corrugating lines, warehouse. 300,000 sq ft facility.

CONSTRUCTION: Heavy steel frame with metal cladding and reinforced concrete machine foundations. Built 1978, modernised 2010 and 2020. Fully sprinklered including under-machine wet pipe systems.

EXPIRING: USD 44M blanket, USD 100,000 deductible, rate 0.165%, premium USD 72,600.

LOSS HISTORY: Paper machine bearing failure in 2025, equipment breakdown claim USD 180,000 (including 3-week BI). Prior 4 years clean.

CHANGES: New paper machine dryer section installed (USD 3M capital investment) improving fire safety. TIV updated accordingly.

The insured acknowledges the recent EB claim and understands a modest rate increase may be warranted. We would appreciate a constructive indication.

ATTACHMENTS: Updated SOV, loss runs, dryer section engineering specifications.

Kind regards,
Elizabeth Morgan
Lockton Companies
elizabeth.morgan@lockton.com
"""
    },
]

# ── 10 Follow-Up Emails ─────────────────────────────────────────────────────

FOLLOWUP_EMAILS = [
    {
        "file": "SUB-2026-0002_acme_industrial_followup_lossruns.eml",
        "from": "David Armstrong <david.armstrong@wtwco.com>",
        "cc": "london.property@wtwco.com",
        "subject": "RE: New Submission - Acme Industrial Holdings Inc - Property - $45M TIV - LOSS RUNS NOW ATTACHED",
        "date": datetime(2026, 1, 23, 11, 15, tzinfo=timezone.utc),
        "tag": "sub-2026-0002-fu1",
        "references": "<sub-2026-0002@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0002@mail.brokerdom.com>",
        "body": """Dear TMHCC Property Team,

Further to our submission dated 15th January for Acme Industrial Holdings Inc (SUB-2026-0002), please find attached the loss runs which were previously outstanding.

The insured's current carrier (Travelers) has now provided the 5-year loss history. I am pleased to confirm the record is CLEAN - no property claims have been reported during the current or prior four policy periods. There was one minor general liability claim in 2023 which is not relevant to the property programme.

The full submission package is now complete. We have attached:
1. 5-Year Loss Runs from Travelers (PDF)
2. Signed ACORD 140 Application (previously unsigned copy was submitted)

We would be grateful for your earliest indication given the approaching 1st March inception date.

Kind regards,

David Armstrong
Willis Towers Watson
david.armstrong@wtwco.com
"""
    },
    {
        "file": "SUB-2026-0004_heritage_hotels_followup_models.eml",
        "from": "Emily Hartwell <emily.hartwell@lockton.com>",
        "cc": "london.property@lockton.com",
        "subject": "RE: New Business Submission - Heritage Hotels International PLC - ADDITIONAL CAT MODEL DATA",
        "date": datetime(2026, 1, 28, 14, 50, tzinfo=timezone.utc),
        "tag": "sub-2026-0004-fu1",
        "references": "<sub-2026-0004@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0004@mail.brokerdom.com>",
        "body": """Dear Underwriting Team,

Following our initial submission for Heritage Hotels International PLC (SUB-2026-0004), and in anticipation of your questions regarding the catastrophe exposure, we are providing the following additional information:

1. UPDATED RMS RiskLink v23 Model Output:
   - 100-year OEP (Occurrence Exceedance Probability): USD 18.4M
   - 250-year OEP: USD 34.2M
   - AAL (Average Annual Loss): USD 1.85M
   - Standard deviation: USD 4.2M

2. AIR Touchstone Model Output (for comparison):
   - 100-year OEP: USD 16.9M
   - 250-year OEP: USD 31.8M
   - AAL: USD 1.72M

3. Scenario Analysis:
   - Cat 3 hurricane direct hit on Miami Beach property: estimated loss USD 8.5M
   - Cat 4 hurricane hitting Key West and Naples: estimated loss USD 22.0M
   - Cat 5 hurricane across Caribbean portfolio: estimated loss USD 45.0M

4. We have also attached the full COPE (Construction, Occupancy, Protection, Exposure) data for each location in a format compatible with your internal modelling.

Please also note that the insured has confirmed they will accept a 5% Named Windstorm deductible (as originally quoted) with a minimum of USD 500,000 per location.

We remain available for a call to walk through the modelling assumptions at your convenience.

Best regards,

Emily Hartwell
Lockton Companies LLP
emily.hartwell@lockton.com
"""
    },
    {
        "file": "SUB-2026-0007_gulf_coast_followup_engineering.eml",
        "from": "Thomas Keane <thomas.keane@mcgillandpartners.com>",
        "cc": None,
        "subject": "RE: Gulf Coast Energy Storage LLC - Additional Engineering Reports",
        "date": datetime(2026, 2, 5, 10, 30, tzinfo=timezone.utc),
        "tag": "sub-2026-0007-fu1",
        "references": "<sub-2026-0007@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0007@mail.brokerdom.com>",
        "body": """Dear TMHCC,

Further to our submission for Gulf Coast Energy Storage LLC (SUB-2026-0007), we attach the following additional documentation as discussed on our call last Thursday:

1. Jensen Hughes BESS Fire Safety Assessment (full report, 45 pages) - this covers both the Freeport and Texas City facilities and includes thermal runaway modelling, fire suppression adequacy assessment, and spacing analysis per NFPA 855.

2. Third-party battery cell testing certification (UL 9540A) for the LFP cells used across all BESS facilities.

3. Updated flood zone maps with post-Harvey revised FEMA flood boundaries for the Freeport and Texas City sites.

4. ERCOT interconnection agreements for all three TX BESS facilities.

5. 12-month operational data showing zero thermal events, zero safety incidents across all facilities.

We believe this additional information addresses the key concerns raised regarding battery technology risk and flood exposure. Please let us know if anything further is required.

Best regards,
Thomas Keane
McGill and Partners
thomas.keane@mcgillandpartners.com
"""
    },
    {
        "file": "SUB-2026-0009_atlantic_seafood_followup_inspection.eml",
        "from": "Andrew Patel <andrew.patel@bmsgroup.com>",
        "cc": None,
        "subject": "RE: Renewal - Atlantic Seafood Processing Inc - POST-LOSS INSPECTION REPORT",
        "date": datetime(2026, 2, 21, 9, 10, tzinfo=timezone.utc),
        "tag": "sub-2026-0009-fu1",
        "references": "<sub-2026-0009@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0009@mail.brokerdom.com>",
        "body": """Dear TMHCC Underwriting,

Following your request during our meeting on Wednesday regarding Atlantic Seafood Processing Inc (SUB-2026-0009), please find attached the comprehensive post-loss risk engineering inspection report prepared by Stellar Engineering, dated 15th February 2026.

Key findings from the report:

1. The new CO2/ammonia cascade refrigeration system is fully operational and performing to specification. Ammonia charge has been reduced by 65% compared to the previous system.

2. All blast-resistant walls around the compressor room have been independently load-tested and certified.

3. The new VESDA aspirating smoke detection system provides 15-minute early warning capability, significantly exceeding the previous point-detection system.

4. Stellar Engineering has rated the overall risk as "Good" (their second-highest category), up from "Fair" prior to the loss.

5. There are zero outstanding recommendations from the inspection.

We trust this report provides confidence in the remediated risk profile and supports a constructive renewal discussion.

Kind regards,
Andrew Patel
BMS Group
andrew.patel@bmsgroup.com
"""
    },
    {
        "file": "SUB-2026-0005_western_distribution_followup_remediation.eml",
        "from": "Michael Cross <michael.cross@howdengroup.com>",
        "cc": None,
        "subject": "RE: Renewal - Western Distribution Corp - Remediation Photos & Invoices",
        "date": datetime(2026, 2, 17, 15, 45, tzinfo=timezone.utc),
        "tag": "sub-2026-0005-fu1",
        "references": "<sub-2026-0005@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0005@mail.brokerdom.com>",
        "body": """Dear TMHCC,

As requested, please find attached the remediation evidence for Western Distribution Corp (SUB-2026-0005):

1. Phoenix location:
   - Photographs of completed HVAC replacement (before and after)
   - Contractor invoices totalling USD 342,000 for roof-top unit replacement
   - Secondary containment tray installation photographs and specifications
   - Sign-off from the insured's property manager confirming completion

2. Sacramento location:
   - Photographs of bollard protection installed around sprinkler risers
   - Updated forklift operator training programme syllabus
   - Quarterly sprinkler inspection schedule (signed by the insured's facilities director)

3. Additionally, the insured has appointed a dedicated Risk Manager (full-time hire as of January 2026) to oversee property risk across all eight locations. CV attached.

We hope this demonstrates the insured's commitment to loss prevention and supports a measured renewal approach.

Best regards,
Michael Cross
Howden Broking Group
michael.cross@howdengroup.com
"""
    },
    {
        "file": "SUB-2026-0001_pacific_retail_followup_query.eml",
        "from": "Sarah Chen <sarah.chen@aon.com>",
        "cc": None,
        "subject": "RE: Pacific Retail Group LLC - Responses to Underwriting Queries",
        "date": datetime(2026, 1, 20, 10, 5, tzinfo=timezone.utc),
        "tag": "sub-2026-0001-fu1",
        "references": "<sub-2026-0001@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0001@mail.brokerdom.com>",
        "body": """Dear TMHCC Property Team,

Thank you for your email of 16th January with underwriting queries on Pacific Retail Group LLC (SUB-2026-0001). Please find our responses below:

1. Q: Please confirm construction details for locations 12, 23, and 31 which show "TBC" in the SOV.
   A: Updated SOV attached with confirmed construction data for all locations. Location 12 is tilt-up concrete, Location 23 is steel frame with EIFS cladding, Location 31 is masonry/CMU.

2. Q: Several locations appear to have "unknown" sprinkler status. Please clarify.
   A: All 47 locations are fully sprinklered. The five locations showing "unknown" in the original SOV were data entry errors. Corrected SOV attached.

3. Q: Please provide the most recent property appraisal for the three largest locations by TIV.
   A: Attached - Marshall & Swift appraisals dated October 2025 for the Bellevue, Scottsdale, and Tysons Corner properties.

4. Q: Is there any current or planned construction at any location?
   A: Location 8 (Scottsdale, AZ) has a minor tenant improvement project (interior fit-out of 12,000 sq ft) expected to complete by March 2026. No structural work. All other locations have no construction activity.

We trust this addresses your queries. Please let us know if anything further is needed.

Kind regards,
Sarah Chen
Aon
sarah.chen@aon.com
"""
    },
    {
        "file": "SUB-2026-0003_northern_mfg_followup_valuation.eml",
        "from": "James Whitfield <james.whitfield@marsh.com>",
        "cc": None,
        "subject": "RE: Renewal - Northern Manufacturing Co Ltd - Updated Valuation Report",
        "date": datetime(2026, 2, 10, 11, 30, tzinfo=timezone.utc),
        "tag": "sub-2026-0003-fu1",
        "references": "<sub-2026-0003@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0003@mail.brokerdom.com>",
        "body": """Dear Underwriting Team,

Further to the renewal submission for Northern Manufacturing Co Ltd (SUB-2026-0003), the insured has now completed their annual property valuation exercise. Please find attached:

1. Updated professional reinstatement valuation report prepared by Bruton Knowles, dated February 2026. This supersedes the SOV values previously submitted.

2. Revised SOV reflecting the updated valuations. The total insured value has increased from GBP 22,000,000 to GBP 22,800,000 (approximately 3.6% increase) driven primarily by increased rebuild costs for the specialist CNC machining hall.

3. M&E asset register with individual values for all major items of plant and machinery.

All other aspects of the submission remain unchanged. We look forward to your renewal terms.

Yours sincerely,
James Whitfield
Marsh Ltd
james.whitfield@marsh.com
"""
    },
    {
        "file": "SUB-2026-0006_cascade_tech_followup_bcp.eml",
        "from": "Rachel Foster <rachel.foster@ajg.com>",
        "cc": None,
        "subject": "RE: Cascade Technology Campus Inc - Business Continuity Plan & Uptime Data",
        "date": datetime(2026, 2, 3, 16, 20, tzinfo=timezone.utc),
        "tag": "sub-2026-0006-fu1",
        "references": "<sub-2026-0006@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0006@mail.brokerdom.com>",
        "body": """Dear TMHCC Team,

As discussed on our call this morning, please find attached additional documentation for Cascade Technology Campus Inc (SUB-2026-0006):

1. Full Business Continuity Plan (BCP) - 82 pages - covering disaster recovery procedures, failover protocols between primary (Ashburn) and secondary (Columbus) facilities, and client communication procedures.

2. 36-month uptime report: The primary facility has achieved 99.9994% uptime over the last three years, with only 3.2 minutes of unplanned downtime (single UPS switchover event in March 2024, no client impact due to redundancy).

3. Tenant concentration analysis: Top 3 tenants represent 62% of revenue; all are on 5+ year contracts with escalation clauses.

4. Power redundancy schematic showing the full 2N power path from utility feed through UPS and generator to rack PDU.

We are confident this risk represents best-in-class data centre operations and warrants competitive terms.

Regards,
Rachel Foster
Gallagher Specialty
rachel.foster@ajg.com
"""
    },
    {
        "file": "SUB-2026-0010_summit_office_followup_firmorder.eml",
        "from": "Laura Simpson <laura.simpson@edbroking.com>",
        "cc": "property.placements@edbroking.com",
        "subject": "RE: Summit Office Partners LP - Firm Order / Closing Update",
        "date": datetime(2026, 3, 5, 9, 45, tzinfo=timezone.utc),
        "tag": "sub-2026-0010-fu1",
        "references": "<sub-2026-0010@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0010@mail.brokerdom.com>",
        "body": """Dear TMHCC Property Team,

Thank you for your written line of 15% on Summit Office Partners LP (SUB-2026-0010). We are pleased to confirm that we are now approaching firm order on this placement.

Current line-up:
- Chubb (Lead): 25%
- TMHCC: 15%
- Hiscox: 15%
- Beazley: 10%
- Liberty Specialty: 10%
- TOTAL PLACED: 75%

We are seeking the remaining 25% from two further follow markets (Brit and Canopius) and expect to close the placement within the next 5 business days.

Please confirm you are happy to proceed to firm order at your written line of 15% on the agreed Chubb lead terms. We will issue the closing slip for your review shortly.

Best regards,
Laura Simpson
Ed Broking
laura.simpson@edbroking.com
"""
    },
    {
        "file": "SUB-2026-0008_midwest_agri_followup_dustplan.eml",
        "from": "Charlotte Webb <charlotte.webb@millerinsurance.com>",
        "cc": None,
        "subject": "RE: Midwest Agricultural Cooperative - Dust Explosion Prevention Documentation",
        "date": datetime(2026, 2, 12, 13, 55, tzinfo=timezone.utc),
        "tag": "sub-2026-0008-fu1",
        "references": "<sub-2026-0008@mail.brokerdom.com>",
        "in_reply_to": "<sub-2026-0008@mail.brokerdom.com>",
        "body": """Dear TMHCC Underwriting,

Further to your request regarding the dust explosion prevention programme for Midwest Agricultural Cooperative (SUB-2026-0008), I attach the following:

1. Complete Grain Dust Explosion Prevention Plan - covers all 22 facilities, including housekeeping schedules, dust collection system maintenance, hot work permit procedures, and employee training records.

2. OSHA compliance audit results (most recent, dated November 2025) - all 22 facilities passed with zero citations. The cooperative has not received an OSHA citation in the last 8 years.

3. Explosion venting calculations and installation certificates for all bins exceeding 20,000 bushel capacity.

4. Emergency response plan including agreements with local fire departments at each location.

The cooperative takes grain dust explosion risk extremely seriously and has invested over USD 1.2M in dust collection and suppression systems across the portfolio in the last 5 years.

Regards,
Charlotte Webb
Miller Insurance Services
charlotte.webb@millerinsurance.com
"""
    },
]

# ── 5 Quote Response Emails ──────────────────────────────────────────────────

QUOTE_RESPONSES = [
    {
        "file": "SUB-2026-0011_continental_bakeries_quote_response.eml",
        "from": "Fiona McCarthy <fiona.mccarthy@ajg.com>",
        "cc": None,
        "subject": "RE: Continental Bakeries Group - Quote Response - Client Accepts Indication",
        "date": _rand_date("2026-01-20", "2026-02-28"),
        "tag": "sub-2026-0011-qr",
        "body": """Dear TMHCC Underwriting,

Thank you for your indication on Continental Bakeries Group Inc (SUB-2026-0011) dated 28th January.

We have presented your terms to the client and I am pleased to confirm that they would like to PROCEED on the basis of your indication:

YOUR INDICATION:
- Limit: USD 42,000,000 blanket
- Deductible: USD 50,000 each and every loss
- Rate: 0.098% on TIV
- Estimated Annual Premium: USD 41,160
- Line: 100%
- Coverage: All-Risk Property, BI (12 months), Equipment Breakdown, Spoilage

The client has confirmed these terms are within budget and would like to move to binding as soon as practicable. Please confirm any additional information or subjectivities you require to firm up the quote.

Best regards,
Fiona McCarthy
Gallagher Specialty
fiona.mccarthy@ajg.com
"""
    },
    {
        "file": "SUB-2026-0013_precision_pharma_quote_response.eml",
        "from": "Natasha Volkov <natasha.volkov@marsh.com>",
        "cc": None,
        "subject": "RE: Precision Pharmaceuticals Inc - Quote Response - Deductible Discussion",
        "date": _rand_date("2026-02-15", "2026-03-31"),
        "tag": "sub-2026-0013-qr",
        "body": """Dear TMHCC Team,

Thank you for your indication on Precision Pharmaceuticals Inc (SUB-2026-0013).

We have reviewed your terms with the client. They are broadly comfortable with the rate of 0.115% on TIV; however, they have raised the following points:

1. DEDUCTIBLE: Your indication included a USD 500,000 deductible. The client would prefer USD 250,000 as originally requested. Would you consider this with an appropriate premium adjustment? Alternatively, could you offer tiered pricing at both deductible levels?

2. BI WAITING PERIOD: You indicated a 24-hour waiting period. The client requests 12 hours given the critical nature of pharmaceutical production and FDA compliance timelines.

3. SPOILAGE SUBLIMIT: Your indication included USD 2,000,000 spoilage sublimit. The client requests USD 5,000,000 given the value of temperature-sensitive API and finished product inventory.

We believe there is a deal to be done here and would welcome your revised terms addressing the above points. The client has authorised us to confirm that a premium up to USD 195,000 is within their budget.

Kind regards,
Natasha Volkov
Marsh Specialty
natasha.volkov@marsh.com
"""
    },
    {
        "file": "SUB-2026-0016_harbour_marina_quote_response.eml",
        "from": "Samantha Drake <samantha.drake@lockton.com>",
        "cc": None,
        "subject": "RE: Harbour Point Marina & Resort - Quote Response - Revised Terms Requested",
        "date": _rand_date("2026-02-01", "2026-03-15"),
        "tag": "sub-2026-0016-qr",
        "body": """Dear TMHCC,

Thank you for your indication on Harbour Point Marina & Resort (SUB-2026-0016) received yesterday.

The client has reviewed and we have the following feedback:

1. The quoted rate of 0.52% on TIV is higher than anticipated. The client's budget allows for a maximum rate of 0.40%. Can you revisit?

2. The 10% Named Windstorm deductible is above market. We had originally requested 5% and believe this is achievable given the structural hardening investments.

3. The client is willing to accept a higher flood deductible (USD 750,000 vs your indication of USD 500,000) if that helps bring the overall rate down.

4. Would you consider a two-year deal at the revised rate, providing rate stability for the client?

We would appreciate revised terms at your earliest convenience.

Best regards,
Samantha Drake
Lockton Companies
samantha.drake@lockton.com
"""
    },
    {
        "file": "SUB-2026-0020_pioneer_solar_quote_response.eml",
        "from": "Hannah Clarke <hannah.clarke@mcgillandpartners.com>",
        "cc": None,
        "subject": "RE: Pioneer Renewable Energy LLC - Quote Response - Proceed at Indicated Terms",
        "date": _rand_date("2026-02-15", "2026-03-31"),
        "tag": "sub-2026-0020-qr",
        "body": """Dear TMHCC Property Team,

Thank you for your indication on Pioneer Renewable Energy LLC (SUB-2026-0020).

The client is pleased with your terms and would like to proceed:

ACCEPTED TERMS:
- Limit: USD 78,000,000 blanket
- AOP Deductible: USD 250,000
- CAT Deductible: USD 500,000
- BI Waiting Period: 60 days
- Rate: 0.135% on TIV
- Premium: USD 105,300 (100% basis)
- Your Line: 25%
- Your Premium Share: USD 26,325

The insured has confirmed acceptance and has asked us to proceed to binding. Please advise on any remaining subjectivities.

We are placing the balance with Beazley (25% lead), Chaucer (25%), and Brit (25%).

Kind regards,
Hannah Clarke
McGill and Partners
hannah.clarke@mcgillandpartners.com
"""
    },
    {
        "file": "SUB-2026-0022_coastal_brewing_quote_response.eml",
        "from": "Sophie Reynolds <sophie.reynolds@lockton.com>",
        "cc": None,
        "subject": "RE: Coastal Brewing Company - Quote Response - Client Would Like to Proceed",
        "date": _rand_date("2026-02-01", "2026-03-31"),
        "tag": "sub-2026-0022-qr",
        "body": """Dear TMHCC,

Thank you for the swift turnaround on Coastal Brewing Company (SUB-2026-0022).

The client has reviewed your indication and is happy to proceed on the following basis:

- Limit: USD 15,000,000
- AOP Deductible: USD 25,000
- EQ Deductible: 5% of TIV at affected location
- Rate: 0.12% on TIV
- Premium: USD 18,000
- Line: 100%

The client's only query is whether Equipment Breakdown coverage includes the brewing equipment (specifically the glycol chiller system and the canning line). Please confirm this is included as standard.

Please issue a binder at your earliest convenience. The client would like to have coverage in place by 15th May 2026 at the latest.

Best,
Sophie Reynolds
Lockton Companies
sophie.reynolds@lockton.com
"""
    },
]

# ── 5 Binding Order Emails ───────────────────────────────────────────────────

BINDING_ORDERS = [
    {
        "file": "SUB-2026-0003_northern_mfg_binding_order.eml",
        "from": "James Whitfield <james.whitfield@marsh.com>",
        "cc": "uk.property.submissions@marsh.com",
        "subject": "BINDING ORDER - Northern Manufacturing Co Ltd - Renewal - Ref: POL-TMHCC-2025-NM-0044",
        "date": datetime(2026, 3, 15, 14, 0, tzinfo=timezone.utc),
        "tag": "sub-2026-0003-bo",
        "body": """Dear TMHCC Underwriting,

BINDING ORDER

We hereby request that you bind the following renewal on behalf of the named insured:

SUBMISSION REF: SUB-2026-0003
EXISTING POLICY: POL-TMHCC-2025-NM-0044

NAMED INSURED: Northern Manufacturing Co Ltd
RISK: Commercial Property - Precision Manufacturing
LOCATION: Unit 14-18, Riverside Industrial Estate, Sheffield S9 2RX, UK

AGREED TERMS:
- Total Insured Value: GBP 22,800,000 / USD 28,900,000
- Limit: GBP 22,800,000 blanket per occurrence
- Deductible: GBP 25,000 each and every loss
- Coverage: All-Risk Property, BI (24 months), Equipment Breakdown
- Rate: 0.082% on TIV (flat to expiry on increased TIV)
- Premium: GBP 18,696
- Your Line: 100%
- Inception: 1st May 2026
- Expiry: 30th April 2027

SUBJECTIVITIES (to be satisfied within 30 days of inception):
1. Updated fire risk assessment (to be completed by insured's appointed fire risk assessor)
2. Confirmation of sprinkler system annual inspection and test (due April 2026)

The insured has authorised us to bind on these terms. Please confirm binding and issue the policy documentation at your earliest convenience.

Yours sincerely,
James Whitfield
Marsh Ltd
james.whitfield@marsh.com
"""
    },
    {
        "file": "SUB-2026-0026_premier_plastics_binding_order.eml",
        "from": "Catherine Hall <catherine.hall@marsh.com>",
        "cc": None,
        "subject": "BINDING ORDER - Premier Plastics Manufacturing Inc - Renewal - Ref: PPM-TMHCC-2025-0091",
        "date": _rand_date("2026-03-01", "2026-03-31"),
        "tag": "sub-2026-0026-bo",
        "body": """Dear TMHCC,

BINDING ORDER

Please bind the renewal for Premier Plastics Manufacturing Inc on the following agreed terms:

SUBMISSION REF: SUB-2026-0026
POLICY REF: PPM-TMHCC-2025-0091

NAMED INSURED: Premier Plastics Manufacturing Inc
TIV: USD 33,000,000
LIMIT: USD 33,000,000 blanket
DEDUCTIBLE: USD 50,000
COVERAGE: All-Risk Property, BI, Equipment Breakdown
RATE: 0.102% (slight reduction from expiry reflecting clean record)
PREMIUM: USD 33,660
LINE: 100%
INCEPTION: 1st June 2026
EXPIRY: 31st May 2027

No subjectivities. All underwriting information is on file.

Please confirm binding and issue renewal documentation.

Kind regards,
Catherine Hall
Marsh Ltd
catherine.hall@marsh.com
"""
    },
    {
        "file": "SUB-2026-0011_continental_bakeries_binding_order.eml",
        "from": "Fiona McCarthy <fiona.mccarthy@ajg.com>",
        "cc": None,
        "subject": "BINDING ORDER - Continental Bakeries Group Inc - New Business",
        "date": _rand_date("2026-02-15", "2026-03-15"),
        "tag": "sub-2026-0011-bo",
        "body": """Dear TMHCC Underwriting,

BINDING ORDER

Following the client's acceptance of your terms, we hereby request binding on the following basis:

SUBMISSION REF: SUB-2026-0011

NAMED INSURED: Continental Bakeries Group Inc
TIV: USD 42,000,000
LIMIT: USD 42,000,000 blanket per occurrence
DEDUCTIBLE: USD 50,000 each and every loss
COVERAGE: All-Risk Property, BI (12 months), Equipment Breakdown, Spoilage
RATE: 0.098% on TIV
PREMIUM: USD 41,160
LINE: 100%
INCEPTION: 1st March 2026
EXPIRY: 28th February 2027
BROKERAGE: 20%

SUBJECTIVITIES:
1. Satisfactory completion of risk engineering survey (to be conducted within 60 days of inception)
2. Receipt of signed proposal form

Premium payment terms: 30 days from inception.

Please confirm binding by return. The client requires evidence of cover prior to inception.

Best regards,
Fiona McCarthy
Gallagher Specialty
fiona.mccarthy@ajg.com
"""
    },
    {
        "file": "SUB-2026-0029_central_cold_binding_order.eml",
        "from": "Richard Hobbs <richard.hobbs@wtwco.com>",
        "cc": None,
        "subject": "BINDING ORDER - Central Cold Logistics Inc - Renewal - Ref: CCL-TMHCC-2025-0078",
        "date": _rand_date("2026-03-15", "2026-03-31"),
        "tag": "sub-2026-0029-bo",
        "body": """Dear TMHCC Property Team,

BINDING ORDER

We confirm the insured's instruction to bind the renewal on the following terms:

SUBMISSION REF: SUB-2026-0029
POLICY REF: CCL-TMHCC-2025-0078

NAMED INSURED: Central Cold Logistics Inc
TIV: USD 27,000,000
LIMIT: USD 27,000,000 blanket
DEDUCTIBLE: USD 75,000 AOP; USD 250,000 ammonia release
COVERAGE: All-Risk, BI (12 months), Equipment Breakdown, Spoilage/Contamination, Ammonia Release
RATE: 0.140% (reduction from expiry of 0.148% reflecting clean record and CO2 system upgrade)
PREMIUM: USD 37,800
LINE: 100%
INCEPTION: 1st July 2026
EXPIRY: 30th June 2027

SUBJECTIVITIES:
1. Completion of CO2 cascade system commissioning report (Kansas City) - expected by end of May 2026.

Please confirm binding.

Regards,
Richard Hobbs
Willis Towers Watson
richard.hobbs@wtwco.com
"""
    },
    {
        "file": "SUB-2026-0027_valley_textiles_binding_order.eml",
        "from": "Simon Blake <simon.blake@howdengroup.com>",
        "cc": None,
        "subject": "BINDING ORDER - Valley Textiles Ltd - Renewal - Ref: VT-TMHCC-2025-0112",
        "date": _rand_date("2026-03-01", "2026-03-31"),
        "tag": "sub-2026-0027-bo",
        "body": """Dear TMHCC,

BINDING ORDER

Please bind the renewal for Valley Textiles Ltd:

SUBMISSION REF: SUB-2026-0027
POLICY REF: VT-TMHCC-2025-0112

NAMED INSURED: Valley Textiles Ltd
TIV: USD 19,000,000
LIMIT: USD 19,000,000 blanket
DEDUCTIBLE: USD 25,000
COVERAGE: All-Risk Property, BI (12 months), Equipment Breakdown
RATE: 0.118% (flat to expiry)
PREMIUM: USD 22,420
LINE: 100%
INCEPTION: 1st July 2026
EXPIRY: 30th June 2027

No outstanding subjectivities. FM Global report on file.

Please confirm and issue renewal documents.

Best,
Simon Blake
Howden Broking Group
simon.blake@howdengroup.com
"""
    },
]


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    to = "submissions@tmhcci.com"

    all_emails = (
        [("HERO", e) for e in HERO_SUBS]
        + [("INITIAL", e) for e in ADDITIONAL_INITIAL]
        + [("RENEWAL", e) for e in RENEWAL_SUBS]
        + [("FOLLOWUP", e) for e in FOLLOWUP_EMAILS]
        + [("QUOTE_RESP", e) for e in QUOTE_RESPONSES]
        + [("BINDING", e) for e in BINDING_ORDERS]
    )

    print(f"Generating {len(all_emails)} .eml files in {OUTPUT_DIR}\n")

    for category, spec in all_emails:
        eml = _make_eml(
            from_addr=spec["from"],
            to_addr=to,
            cc=spec.get("cc"),
            subject=spec["subject"],
            body=spec["body"].strip(),
            date=spec["date"],
            message_id_tag=spec["tag"],
            references=spec.get("references"),
            in_reply_to=spec.get("in_reply_to"),
        )
        _write(spec["file"], eml)

    print(f"\nDone. {len(all_emails)} emails generated.")


if __name__ == "__main__":
    main()
