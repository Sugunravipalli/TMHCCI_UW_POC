"""
Generate 8 realistic Commercial Property Insurance Application text files
for Tokio Marine HCC underwriting POC.
"""

import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "03_applications")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADER = """\
================================================================================
              COMMERCIAL PROPERTY INSURANCE APPLICATION
================================================================================
                    TOKIO MARINE HCC INTERNATIONAL
                      Lloyd's Syndicate 4141
================================================================================
"""

SEPARATOR = "--------------------------------------------------------------------------------"

# ---------------------------------------------------------------------------
# 1. Pacific Retail Group LLC
# ---------------------------------------------------------------------------
APP_PACIFIC_RETAIL = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Pacific Retail Group LLC
DBA (if any):           Pacific Centres
Mailing Address:        3200 Peachtree Road NE, Suite 1400, Atlanta, GA 30305
Primary Contact:        Sandra K. Whitfield, VP of Risk Management
Phone:                  (404) 555-2380
Email:                  s.whitfield@pacificretailgroup.com
Website:                www.pacificretailgroup.com
Federal Tax ID / EIN:   58-3471209
SIC Code:               6512
NAICS Code:             531120
Year Established:       1997
Annual Revenue:         $485,000,000
# Full-Time Employees:  2,340

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   47
Total Insured Value (TIV):   $120,000,000

Location Summary (see attached SOV for full schedule):
  Loc 1  - Peachtree Plaza, 3200 Peachtree Rd NE, Atlanta GA        - $8,200,000
  Loc 2  - Buckhead Station, 1250 Lenox Park Blvd, Atlanta GA       - $6,500,000
  Loc 3  - Savannah Commons, 420 Drayton St, Savannah GA             - $4,100,000
  Loc 4  - Augusta Crossing, 3540 Wheeler Rd, Augusta GA             - $3,800,000
  Loc 5  - Macon Town Centre, 101 Riverside Dr, Macon GA             - $3,200,000
  Remaining 42 locations across GA, SC, and TN - see attached SOV.

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Primary Construction:   Steel frame with masonry exterior (majority)
                        8 locations reinforced concrete, 4 wood-frame strip malls
Year Built Range:       1988 - 2019
Stories:                1 to 3 (majority single-storey retail)
Total Square Footage:   4,120,000 sq ft across all locations
Sprinkler Systems:      44 of 47 locations fully sprinklered (wet pipe)
                        3 older strip-mall locations have partial coverage only
Fire Alarm:             Centrally monitored fire alarm at all locations
Security:               24/7 on-site security at 12 major centres;
                        CCTV and alarm-only at remaining locations
Roof Type:              Built-up membrane (32 locations), TPO (12), metal (3)
Average Roof Age:       11 years; oldest roof replaced 2014

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $120,000,000 (blanket)
Business Interruption Limit:    $24,000,000 (12-month ALE)
Deductible Preference:          $100,000 per occurrence
Coverage Form:                  All Risk / Special Form
Valuation:                      Replacement Cost
Wind/Hail Sublimit:             $15,000,000 (2% location deductible)
Flood Sublimit:                 $10,000,000 (NFIP as primary, excess requested)
Earthquake Sublimit:            Not requested

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location              Cause of Loss       Gross Incurred    Status
----    --------              -------------       --------------    ------
2025    Loc 14, Valdosta GA   Wind / hail damage   $312,000         Closed
2024    Loc 3, Savannah GA    Roof leak / water    $87,500          Closed
2023    Loc 22, Dalton GA     Slip-and-fall claim  $42,000          Closed
2022    Loc 1, Atlanta GA     HVAC fire (small)    $165,000         Closed
2021    None reported         --                   --               --

Total 5-year incurred losses: $606,500

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- Wet-pipe automatic sprinklers at 44 of 47 locations
- 24/7 centrally monitored fire and burglar alarms (UL-listed)
- Emergency backup generators at 12 major retail centres
- Quarterly fire extinguisher inspections company-wide
- Annual third-party fire protection audit

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        Zurich Insurance (expiring 06/30/2026)
Reason for Marketing:   Seeking competitive terms on renewal; current premium
                        increased 14% at last renewal.
Prior Cancellations:    None
Bankruptcy History:     None
Pending Litigation:     None material to property coverage

APPLICANT SIGNATURE
Date:       March 12, 2026
Name:       Sandra K. Whitfield
Title:      VP of Risk Management, Pacific Retail Group LLC
"""

# ---------------------------------------------------------------------------
# 2. Acme Industrial Holdings Inc  (INCOMPLETE APPLICATION)
# ---------------------------------------------------------------------------
APP_ACME_INDUSTRIAL = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Acme Industrial Holdings Inc
DBA (if any):           Acme Metalworks
Mailing Address:        7600 Rockside Rd, Suite 200, Independence, OH 44131
Primary Contact:        Thomas J. Brennan, CFO
Phone:                  (216) 555-0194
Email:                  tbrennan@acmeindustrial.com
Website:                www.acmeindustrial.com
Federal Tax ID / EIN:   34-6192087
SIC Code:               3462
NAICS Code:             332111
Year Established:       1974
Annual Revenue:         $112,000,000
# Full-Time Employees:  485

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   3
Total Insured Value (TIV):   $45,000,000

  Loc 1  - Main Plant, 7600 Rockside Rd, Independence OH       - $22,000,000
           Contents/Equipment: $12,500,000; Building: $9,500,000
  Loc 2  - Warehouse & Shipping, 2100 Canal Rd, Cleveland OH   - $13,000,000
           Contents/Equipment: $5,800,000; Building: $7,200,000
  Loc 3  - Satellite Forge Shop, 490 Industrial Pkwy, Elyria OH- $10,000,000
           Contents/Equipment: $7,400,000; Building: $2,600,000

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Location 1 - Main Plant:
  Construction:     Non-combustible steel frame, metal-clad walls
  Year Built:       1974, renovated 2008
  Stories:          1 (high-bay, 40 ft clear height)
  Square Footage:   185,000 sq ft
  Sprinkler:        Wet-pipe throughout; dry-pipe in loading docks
  Fire Alarm:       Centrally monitored, photoelectric smoke detection
  Roof:             Standing-seam metal, replaced 2018

Location 2 - Warehouse:
  Construction:     Pre-engineered metal building
  Year Built:       1991
  Stories:          1
  Square Footage:   120,000 sq ft
  Sprinkler:        Wet-pipe, ESFR heads in high-pile storage areas
  Fire Alarm:       Centrally monitored
  Roof:             Metal panels, original 1991 (33 years old)

Location 3 - Satellite Forge Shop:
  Construction:     Reinforced concrete tilt-up
  Year Built:       1982
  Stories:          1
  Square Footage:   65,000 sq ft
  Sprinkler:        [NOT PROVIDED]
  Fire Alarm:       [NOT PROVIDED]
  Roof:             [NOT PROVIDED]

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $45,000,000 (blanket)
Business Interruption Limit:    $9,000,000
Deductible Preference:          $50,000 per occurrence
Coverage Form:                  All Risk / Special Form
Valuation:                      Replacement Cost
Equipment Breakdown:            Requested (critical presses/forge equipment)
Flood Sublimit:                 $5,000,000
Wind/Hail Sublimit:             Full limit

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
[NOT PROVIDED - Applicant has indicated loss runs will be supplied by
 current broker under separate cover. No loss data available at this time.]

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
Location 1:
  - Automatic sprinkler system (wet-pipe); dry-pipe at docks
  - 24/7 centrally monitored fire alarm
  - Perimeter fencing with electronic gate access
  - Backup diesel generator (500 kW)
Location 2:
  - ESFR sprinkler system
  - Centrally monitored alarm
  - Manned guard post (night shift only)
Location 3:
  - [NOT PROVIDED]

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        [NOT PROVIDED]
Expiring Premium:       [NOT PROVIDED]
Reason for Marketing:   New broker appointment; prior broker relationship ended.
Prior Cancellations:    None known
Bankruptcy History:     None
Pending Litigation:     [NOT PROVIDED]

NOTE: This application is submitted with known data gaps. Additional
information for Location 3 and the loss history will be forwarded as
soon as available. Applicant requests preliminary indication in the
interim.

APPLICANT SIGNATURE
Date:       February 28, 2026
Name:       Thomas J. Brennan
Title:      Chief Financial Officer, Acme Industrial Holdings Inc
"""

# ---------------------------------------------------------------------------
# 3. Heritage Hotels International PLC
# ---------------------------------------------------------------------------
APP_HERITAGE_HOTELS = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Heritage Hotels International PLC
DBA (if any):           Heritage Collection / Heritage Resorts
Mailing Address:        1200 Brickell Ave, Suite 3400, Miami, FL 33131
Primary Contact:        Claire DuPont-Moreau, Group Risk Director
Phone:                  (305) 555-7102
Email:                  c.dupont-moreau@heritagehotels.com
Website:                www.heritagehotels.com
Federal Tax ID / EIN:   65-4218730
SIC Code:               7011
NAICS Code:             721110
Year Established:       1985
Annual Revenue:         $620,000,000
# Full-Time Employees:  4,100

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   12
Total Insured Value (TIV):   $200,000,000

  Loc 1  - The Heritage Miami Beach, 4500 Collins Ave, Miami Beach FL  - $38,000,000
  Loc 2  - Heritage Fort Lauderdale, 3100 N Ocean Blvd, Ft Lauderdale - $22,000,000
  Loc 3  - Heritage Key West, 245 Front St, Key West FL                - $18,500,000
  Loc 4  - Heritage Palm Beach, 2800 S Ocean Blvd, Palm Beach FL      - $24,000,000
  Loc 5  - Heritage Naples, 851 Gulf Shore Blvd, Naples FL             - $16,000,000
  Loc 6  - Heritage Sarasota, 1111 Ritz Carlton Dr, Sarasota FL        - $14,500,000
  Loc 7  - Heritage Tampa, 725 S Harbour Island Blvd, Tampa FL         - $12,000,000
  Loc 8  - Heritage St. Augustine, 95 Cordova St, St. Augustine FL     - $9,500,000
  Loc 9  - Heritage Grand Cayman, 7 Mile Beach Rd, Grand Cayman        - $16,000,000
  Loc 10 - Heritage Nassau, Cable Beach, Nassau, Bahamas                - $12,500,000
  Loc 11 - Heritage St. Kitts, Frigate Bay, St. Kitts                   - $10,000,000
  Loc 12 - Heritage Turks & Caicos, Grace Bay, Providenciales           - $7,000,000

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Primary Construction:   Reinforced concrete, hurricane-rated windows (FL/Caribbean)
Year Built Range:       1985 - 2020 (most recently renovated within past 8 years)
Stories:                3 to 14
Total Square Footage:   1,850,000 sq ft
Sprinkler Systems:      All 12 locations fully sprinklered (wet-pipe)
Fire Alarm:             Addressable fire alarm with voice evacuation at all locations
Security:               24/7 front desk and roving security; electronic key card access
Roof Type:              Concrete tile (FL), flat reinforced membrane (Caribbean)
Hurricane Shutters:     Impact-rated windows or accordion shutters at all coastal properties
Wind Rating:            All FL properties built or retrofitted to FL Building Code 2010+

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $200,000,000 (blanket)
Business Interruption Limit:    $80,000,000 (18-month extended period)
Deductible Preference:          $250,000 per occurrence (AOP)
Coverage Form:                  All Risk / Special Form
Named Storm Deductible:         3% of location TIV
Flood Sublimit:                 $25,000,000 per occurrence / $50,000,000 aggregate
Wind/Named Storm Sublimit:      $100,000,000 per occurrence
Earthquake Sublimit:            Not requested
Ordinance or Law:               $10,000,000

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location                   Cause of Loss          Gross Incurred   Status
----    --------                   -------------          --------------   ------
2025    Loc 9, Grand Cayman        Hurricane (Cat 2)       $4,200,000      Open
2024    Loc 1, Miami Beach         Named storm / flood     $1,850,000      Closed
2024    Loc 5, Naples              Water damage (pipe)       $175,000      Closed
2023    Loc 12, Turks & Caicos     Hurricane (Cat 1)       $2,100,000      Closed
2022    Loc 3, Key West            Wind damage               $420,000      Closed
2021    Loc 6, Sarasota            Lightning / fire          $310,000      Closed

Total 5-year incurred losses: $9,055,000
Loss ratio note: Significant cat exposure; however, properties are built to
current hurricane standards and insured has invested >$12M in storm hardening.

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- Fully automatic wet-pipe sprinklers at all 12 locations
- Addressable fire alarm with 24/7 central station monitoring
- Emergency generators with 72-hour fuel capacity at each hotel
- Hurricane preparedness plan tested annually (documented)
- Impact-rated glazing or storm shutters at all coastal locations
- On-site engineering team maintains building envelopes quarterly

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        AIG / Lexington (lead), FM Global (excess)
Expiring Premium:       $2,850,000 (expiring 07/01/2026)
Reason for Marketing:   AIG reducing capacity in FL wind-exposed hospitality;
                        seeking replacement lead market.
Prior Cancellations:    None
Bankruptcy History:     None
Pending Litigation:     One slip-and-fall at Loc 1 (GL matter, not property)

APPLICANT SIGNATURE
Date:       March 5, 2026
Name:       Claire DuPont-Moreau
Title:      Group Risk Director, Heritage Hotels International PLC
"""

# ---------------------------------------------------------------------------
# 4. Cascade Technology Campus Inc
# ---------------------------------------------------------------------------
APP_CASCADE_TECH = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Cascade Technology Campus Inc
DBA (if any):           Cascade Data Centres
Mailing Address:        2200 Westlake Ave N, Suite 800, Seattle, WA 98109
Primary Contact:        Raj Patel, Director of Insurance & Risk
Phone:                  (206) 555-4490
Email:                  raj.patel@cascadetechcampus.com
Website:                www.cascadetechcampus.com
Federal Tax ID / EIN:   91-2087546
SIC Code:               7374
NAICS Code:             518210
Year Established:       2012
Annual Revenue:         $340,000,000
# Full-Time Employees:  310

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   2
Total Insured Value (TIV):   $180,000,000

  Loc 1  - Cascade East Campus, 15200 SE 37th St, Bellevue WA    - $110,000,000
           Building: $45,000,000   M&E/IT Infrastructure: $65,000,000
  Loc 2  - Cascade West Campus, 4800 S 188th St, SeaTac WA       - $70,000,000
           Building: $28,000,000   M&E/IT Infrastructure: $42,000,000

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Location 1 - Cascade East (Primary):
  Construction:     Reinforced concrete, raised-floor design
  Year Built:       2016
  Stories:          2 (plus basement mechanical level)
  Square Footage:   180,000 sq ft (95,000 sq ft white space)
  Sprinkler:        Pre-action dry-pipe (server halls), wet-pipe (offices)
  Fire Suppression: FM-200 clean-agent in all server rooms
  Fire Alarm:       VESDA very-early-smoke-detection, addressable panels
  Security:         Biometric + key card access; mantrap entries; 24/7 NOC
  Roof:             TPO membrane, installed 2016
  Power:            2N redundant utility feeds; 3x 2MW diesel generators;
                    48-hour on-site fuel; UPS with 15-minute battery bridge

Location 2 - Cascade West:
  Construction:     Steel frame with concrete tilt-up walls
  Year Built:       2019
  Stories:          1 (high-bay)
  Square Footage:   120,000 sq ft (72,000 sq ft white space)
  Sprinkler:        Pre-action dry-pipe throughout
  Fire Suppression: Novec 1230 clean-agent in server rooms
  Fire Alarm:       VESDA + addressable panels
  Security:         Same standard as Loc 1
  Roof:             TPO membrane, installed 2019
  Power:            2N utility feeds; 2x 2.5MW diesel generators;
                    48-hour fuel; UPS with 15-minute battery bridge

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $180,000,000 (blanket)
Business Interruption Limit:    $90,000,000 (18-month indemnity period)
Deductible Preference:          $500,000 per occurrence
Coverage Form:                  All Risk / Special Form
Equipment Breakdown:            Included (critical for generator/UPS/HVAC)
Contingent BI:                  $20,000,000 (utility service interruption)
Flood Sublimit:                 $15,000,000
Earthquake Sublimit:            $50,000,000 (5% of values at risk, Cascadia zone)
Data Restoration Costs:         $5,000,000

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location       Cause of Loss               Gross Incurred   Status
----    --------       -------------               --------------   ------
2025    None reported  --                           --               --
2024    Loc 1          UPS failure / brief outage    $620,000        Closed
2023    None reported  --                           --               --
2022    Loc 1          Cooling unit malfunction      $185,000        Closed
2021    None reported  --                           --               --

Total 5-year incurred losses: $805,000
Note: No property damage claims; losses relate to equipment breakdown only.

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- Pre-action sprinklers and FM-200/Novec clean-agent suppression
- VESDA laser-based smoke detection in all data halls
- 2N redundant power with generator and UPS backup
- 24/7 staffed Network Operations Centre (NOC) at each site
- Biometric + multi-factor access control; CCTV with 90-day retention
- N+1 redundant CRAC/CRAH cooling units
- Quarterly fire drills and annual FM Global engineering visits

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        FM Global (DIC/equipment breakdown), Zurich (property)
Expiring Premium:       $1,420,000 (expiring 09/01/2026)
Reason for Marketing:   Seeking broader earthquake capacity; current programme
                        provides only $25M EQ sublimit.
Prior Cancellations:    None
Bankruptcy History:     None
Tier III+ Certification: Uptime Institute certified at both facilities

APPLICANT SIGNATURE
Date:       March 18, 2026
Name:       Raj Patel
Title:      Director of Insurance & Risk, Cascade Technology Campus Inc
"""

# ---------------------------------------------------------------------------
# 5. Gulf Coast Energy Storage LLC
# ---------------------------------------------------------------------------
APP_GULF_COAST = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Gulf Coast Energy Storage LLC
DBA (if any):           GCES / Gulf Coast Storage
Mailing Address:        4700 Post Oak Blvd, Suite 1600, Houston, TX 77027
Primary Contact:        Marcus L. Thibodeaux, Risk Manager
Phone:                  (713) 555-8201
Email:                  m.thibodeaux@gulfcoastenergy.com
Website:                www.gulfcoastenergystorage.com
Federal Tax ID / EIN:   76-3890214
SIC Code:               5171
NAICS Code:             493190
Year Established:       2009
Annual Revenue:         $210,000,000
# Full-Time Employees:  275

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   5
Total Insured Value (TIV):   $95,000,000

  Loc 1  - Baytown Terminal, 3800 Decker Dr, Baytown TX           - $32,000,000
  Loc 2  - Texas City Facility, 9200 Hwy 146, Texas City TX      - $24,000,000
  Loc 3  - Beaumont Station, 5100 Delaware St, Beaumont TX        - $18,000,000
  Loc 4  - Port Arthur Depot, 2700 Twin City Hwy, Port Arthur TX  - $12,000,000
  Loc 5  - Corpus Christi Hub, 1400 Up River Rd, Corpus Christi TX- $9,000,000

Storage Products:  Refined petroleum products, natural gas liquids,
                   biodiesel, ethanol, lubricant base stocks
Total Shell Capacity: 4.2 million barrels

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Primary Construction:   Welded steel above-ground storage tanks (ASTs)
                        with concrete containment dikes; steel-frame pump
                        houses; pre-engineered metal office/control buildings
Tank Construction:      API 650 welded steel, cone/dome roofs
Year Built Range:       2009 - 2022 (newest tanks at Loc 5)
Office/Control Buildings: 1 to 2 stories, non-combustible
Sprinkler:              Fixed foam suppression on all tanks >50,000 bbl;
                        wet-pipe sprinklers in office and control buildings
Fire Protection:        On-site firewater loop with diesel-driven fire pumps;
                        monitor nozzles at each tank battery
Security:               Perimeter fencing, CCTV, manned gate 24/7 at all sites
Roof (buildings):       Metal panel, all less than 10 years old

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $95,000,000 (blanket)
Business Interruption Limit:    $30,000,000 (12-month)
Deductible Preference:          $250,000 per occurrence
Coverage Form:                  All Risk / Special Form
Named Storm Deductible:         5% of location TIV
Flood Sublimit:                 $20,000,000
Wind/Named Storm Sublimit:      $50,000,000
Pollution Legal Liability:      $10,000,000 (if available on property form)

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location              Cause of Loss            Gross Incurred   Status
----    --------              -------------            --------------   ------
2025    Loc 1, Baytown        Lightning strike / fire     $1,400,000    Closed
2024    Loc 3, Beaumont       Hurricane (Cat 1) wind       $780,000    Closed
2023    Loc 2, Texas City     Pump seal failure / spill    $340,000    Closed
2022    None reported         --                           --          --
2021    Loc 1, Baytown        Tropical storm flooding      $520,000    Closed

Total 5-year incurred losses: $3,040,000

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- Fixed foam suppression systems on all large-diameter tanks
- Diesel-driven fire pumps independent of electrical supply
- Firewater loop with hydrants every 250 ft
- Vapour detection system (continuous LEL monitoring)
- SPCC plans and secondary containment at all locations
- 24/7 manned control room with SCADA monitoring
- Annual API 653 tank inspections; 10-year internal inspections

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        Allianz Global Corporate & Specialty
Expiring Premium:       $1,050,000 (expiring 10/01/2026)
Reason for Marketing:   Adding Loc 5 (Corpus Christi); current carrier unwilling
                        to expand capacity without significant rate increase.
Prior Cancellations:    None
Bankruptcy History:     None
EPA/TCEQ Violations:    One Notice of Violation (2022) - corrected, no fine levied
PSM/RMP Compliance:     Fully compliant at all locations

APPLICANT SIGNATURE
Date:       March 22, 2026
Name:       Marcus L. Thibodeaux
Title:      Risk Manager, Gulf Coast Energy Storage LLC
"""

# ---------------------------------------------------------------------------
# 6. Midwest Agricultural Cooperative
# ---------------------------------------------------------------------------
APP_MIDWEST_AG = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Midwest Agricultural Cooperative
DBA (if any):           Midwest Ag Co-op
Mailing Address:        800 Marquette Ave, Suite 520, Minneapolis, MN 55402
Primary Contact:        Karen M. Lindstrom, Controller & Risk Coordinator
Phone:                  (612) 555-3147
Email:                  karen.lindstrom@midwestagcoop.com
Website:                www.midwestagcoop.com
Federal Tax ID / EIN:   41-5023871
SIC Code:               5153
NAICS Code:             493130
Year Established:       1952
Annual Revenue:         $95,000,000
# Full-Time Employees:  210 (plus 90 seasonal)

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   22
Total Insured Value (TIV):   $35,000,000

Location Summary (see attached SOV for full schedule):
  Loc 1  - Minneapolis HQ & Processing, 800 Marquette Ave, Minneapolis - $4,200,000
  Loc 2  - Mankato Elevator, 1200 Range St, Mankato MN                 - $3,100,000
  Loc 3  - Willmar Grain Terminal, 601 Litchfield Ave, Willmar MN      - $2,800,000
  Loc 4  - Moorhead Elevator, 315 Center Ave, Moorhead MN              - $2,400,000
  Loc 5  - Fergus Falls Storage, 710 W Lincoln Ave, Fergus Falls MN    - $1,900,000
  Remaining 17 locations are country elevators across MN - see SOV.
  Average value per country elevator: $1,210,000

Commodities Stored:  Corn, soybeans, spring wheat, barley, sunflower seeds

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Primary Construction:   Concrete slip-form grain elevators with steel bins;
                        wood-frame and metal offices; metal-clad processing buildings
Year Built Range:       1952 - 2018 (HQ office renovated 2015)
Stories:                Elevators up to 120 ft; offices 1-2 stories
Total Storage Capacity: 18,500,000 bushels
Sprinkler Systems:      Processing buildings sprinklered at 4 major locations;
                        grain elevators are NOT sprinklered (industry standard)
Fire Alarm:             Monitored heat detection in processing; smoke alarms in offices
Dust Collection:        Pneumatic dust suppression at all elevator legs and
                        conveyor transfer points (NFPA 652 compliant)
Security:               Locked and fenced; CCTV at 8 larger locations
Roof (office/processing): Metal panel; average age 14 years

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $35,000,000 (blanket)
Business Interruption Limit:    $7,000,000 (6-month, seasonal adjustment)
Deductible Preference:          $25,000 per occurrence
Coverage Form:                  All Risk / Special Form
Stock Throughput:               Requested for grain in transit
Dust Explosion Sublimit:        $10,000,000
Flood Sublimit:                 $5,000,000
Wind/Tornado Sublimit:          $10,000,000 (1% location deductible)

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location                Cause of Loss            Gross Incurred   Status
----    --------                -------------            --------------   ------
2025    Loc 9, Morris MN        Tornado damage            $410,000        Closed
2024    Loc 2, Mankato MN       Grain dryer fire          $215,000        Closed
2023    Loc 14, Benson MN       Leg boot bearing fire      $62,000        Closed
2022    None reported           --                        --              --
2021    Loc 4, Moorhead MN      Spring flooding            $185,000       Closed

Total 5-year incurred losses: $872,000

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- NFPA 652 compliant dust collection at all elevator locations
- Bearing temperature monitors on bucket elevator legs
- Magnetic separators on grain intake to prevent spark ignition
- Sprinklered processing/feed mill buildings (4 major sites)
- Lightning rods on all elevator headhouses
- Hot-work permit programme enforced at all locations
- Seasonal pre-harvest safety inspections at each country elevator

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        COUNTRY Financial (formerly Country Companies)
Expiring Premium:       $298,000 (expiring 04/01/2026)
Reason for Marketing:   Current carrier withdrawing from grain elevator class;
                        cooperative must find replacement coverage.
Prior Cancellations:    None
Bankruptcy History:     None
Co-op Membership:       1,480 member-farmers across 14 MN counties

APPLICANT SIGNATURE
Date:       February 10, 2026
Name:       Karen M. Lindstrom
Title:      Controller & Risk Coordinator, Midwest Agricultural Cooperative
"""

# ---------------------------------------------------------------------------
# 7. Atlantic Seafood Processing Inc
# ---------------------------------------------------------------------------
APP_ATLANTIC_SEAFOOD = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Atlantic Seafood Processing Inc
DBA (if any):           Atlantic Fresh / Cape Cod Catch
Mailing Address:        55 State Pier, Gloucester, MA 01930
Primary Contact:        Robert A. Mancini, Operations Manager
Phone:                  (978) 555-6233
Email:                  rmancini@atlanticseafood.com
Website:                www.atlanticseafoodprocessing.com
Federal Tax ID / EIN:   04-7681350
SIC Code:               2092
NAICS Code:             311710
Year Established:       2001
Annual Revenue:         $78,000,000
# Full-Time Employees:  195

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   4
Total Insured Value (TIV):   $50,000,000

  Loc 1  - Gloucester Processing Plant, 55 State Pier, Gloucester MA   - $22,000,000
           Building: $9,000,000  Equipment: $8,500,000  Stock: $4,500,000
  Loc 2  - New Bedford Cold Storage, 702 Herman Melville Blvd, New Bedford MA - $14,000,000
           Building: $6,000,000  Equipment: $4,200,000  Stock: $3,800,000
  Loc 3  - Plymouth Distribution Centre, 19 Industrial Park Rd, Plymouth MA   - $9,000,000
           Building: $5,500,000  Equipment: $2,000,000  Stock: $1,500,000
  Loc 4  - Boston Retail/Office, 1 Fish Pier St W, Boston MA           - $5,000,000
           Building: $3,800,000  Contents: $1,200,000

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Location 1 - Gloucester Processing Plant:
  Construction:     Masonry with steel frame interior
  Year Built:       1978, renovated 2014
  Stories:          2
  Square Footage:   62,000 sq ft
  Sprinkler:        Wet-pipe throughout; cold rooms have dry-pipe
  Fire Alarm:       Centrally monitored, heat + smoke detection
  Refrigeration:    Ammonia-based (NH3) industrial refrigeration, 120 tons
  Roof:             EPDM membrane, replaced 2019

Location 2 - New Bedford Cold Storage:
  Construction:     Insulated metal panel (IMP) on steel frame
  Year Built:       2010
  Stories:          1 (30 ft clear height)
  Square Footage:   45,000 sq ft
  Sprinkler:        Dry-pipe throughout (sub-zero environment)
  Fire Alarm:       Centrally monitored
  Refrigeration:    Ammonia-based, 200 tons, -10F to +34F zones
  Roof:             Metal standing-seam, original 2010

Location 3 - Plymouth Distribution Centre:
  Construction:     Pre-engineered metal building
  Year Built:       2005
  Stories:          1
  Square Footage:   35,000 sq ft
  Sprinkler:        Wet-pipe
  Fire Alarm:       Local alarm with central monitoring
  Roof:             Metal panel, re-coated 2020

Location 4 - Boston Retail/Office:
  Construction:     Historic brick/timber (heavy timber interior)
  Year Built:       1915, renovated 2008
  Stories:          3
  Square Footage:   8,500 sq ft
  Sprinkler:        Wet-pipe (added during 2008 renovation)
  Fire Alarm:       Centrally monitored
  Roof:             Modified bitumen, replaced 2018

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $50,000,000 (blanket)
Business Interruption Limit:    $15,000,000 (12-month)
Deductible Preference:          $50,000 per occurrence
Coverage Form:                  All Risk / Special Form
Spoilage / Refrigeration:       $8,000,000 (ammonia release or power failure)
Equipment Breakdown:            Requested (refrigeration compressors critical)
Flood Sublimit:                 $5,000,000 (coastal locations)
Wind Sublimit:                  Full limit

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location                Cause of Loss            Gross Incurred   Status
----    --------                -------------            --------------   ------
2025    Loc 2, New Bedford      Compressor failure /       $890,000       Closed
                                spoilage of 410,000 lbs
2024    Loc 1, Gloucester       Nor'easter roof damage     $145,000       Closed
2023    None reported           --                         --             --
2022    Loc 1, Gloucester       Electrical fire (panel)    $72,000        Closed
2021    Loc 3, Plymouth         Forklift impact / rack     $38,000        Closed
                                collapse

Total 5-year incurred losses: $1,145,000

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- Automatic sprinkler systems at all 4 locations
- Ammonia leak detection with automatic ventilation (Loc 1 & 2)
- Emergency backup generators at Loc 1 and Loc 2 (refrigeration critical)
- 24/7 temperature monitoring with remote alarm (all cold storage)
- Centrally monitored fire and burglar alarms
- HACCP and SQF Level 3 food safety certifications
- Annual ammonia system inspection by licensed refrigeration engineer

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        Sompo International
Expiring Premium:       $485,000 (expiring 08/01/2026)
Reason for Marketing:   Seeking improved spoilage/refrigeration sublimits;
                        current programme caps at $3M, inadequate for inventory.
Prior Cancellations:    None
Bankruptcy History:     None
FDA Registration:       All processing locations FDA-registered; last inspection
                        2024 with zero critical findings.

APPLICANT SIGNATURE
Date:       March 1, 2026
Name:       Robert A. Mancini
Title:      Operations Manager, Atlantic Seafood Processing Inc
"""

# ---------------------------------------------------------------------------
# 8. Summit Office Partners LP
# ---------------------------------------------------------------------------
APP_SUMMIT_OFFICE = HEADER + f"""
SECTION 1: APPLICANT INFORMATION
{SEPARATOR}
Named Insured:          Summit Office Partners LP
DBA (if any):           Summit Properties
Mailing Address:        450 Park Ave, 28th Floor, New York, NY 10022
Primary Contact:        David Chen, Managing Director
Phone:                  (212) 555-9088
Email:                  d.chen@summitoffice.com
Website:                www.summitofficepartners.com
Federal Tax ID / EIN:   13-6752041
SIC Code:               6512
NAICS Code:             531120
Year Established:       2005
Annual Revenue:         $145,000,000
# Full-Time Employees:  82

SECTION 2: PROPERTY INFORMATION
{SEPARATOR}
Total Number of Locations:   6
Total Insured Value (TIV):   $75,000,000

  Loc 1  - Summit Tower, 450 Park Ave, New York NY 10022          - $22,000,000
           (Floors 20-30 of 42-storey Class A high-rise; condo interest)
  Loc 2  - Summit Plaza, 1185 Avenue of the Americas, New York NY - $16,000,000
           (Floors 8-14 of 36-storey tower; leasehold interest)
  Loc 3  - Summit Westchester, 100 Main St, White Plains NY        - $12,000,000
           (Full ownership, 8-storey Class A office)
  Loc 4  - Summit Stamford, 300 Atlantic St, Stamford CT           - $10,500,000
           (Full ownership, 6-storey Class A office)
  Loc 5  - Summit Jersey City, 30 Hudson St, Jersey City NJ        - $8,500,000
           (Floors 5-8 of 30-storey tower; condo interest)
  Loc 6  - Summit Garden City, 600 Old Country Rd, Garden City NY  - $6,000,000
           (Full ownership, 4-storey suburban Class A)

SECTION 3: CONSTRUCTION & PROTECTION
{SEPARATOR}
Primary Construction:   Fire-resistive steel frame with curtain wall (Manhattan);
                        reinforced concrete (suburban locations)
Year Built Range:       1981 - 2017
Stories:                4 to 42 (see location details above)
Total Square Footage:   620,000 sq ft (rentable area under management)
Sprinkler Systems:      All 6 locations fully sprinklered (wet-pipe)
Fire Alarm:             Addressable fire alarm with voice evacuation (NYC);
                        conventional monitored systems (suburban)
Security:               Lobby attendant and CCTV at all locations; building
                        access card at all; 24/7 concierge at Loc 1 and Loc 2
Elevator:               Passenger and freight elevators at all locations
Roof Type:              Modified bitumen or TPO (suburban); common-area
                        responsibility at condo/leasehold locations
Average Occupancy:      93% leased across portfolio

SECTION 4: COVERAGE REQUESTED
{SEPARATOR}
Property Damage Limit:          $75,000,000 (blanket)
Business Interruption Limit:    $18,750,000 (12-month rental income)
Deductible Preference:          $100,000 per occurrence
Coverage Form:                  All Risk / Special Form
Valuation:                      Replacement Cost (owned); betterments &
                                improvements (leasehold interests)
Flood Sublimit:                 $10,000,000 (Loc 5 in Zone AE)
Wind Sublimit:                  Full limit
Earthquake Sublimit:            $15,000,000 (2% of TIV deductible)
Ordinance or Law:               $5,000,000
Loss of Rents / Rental Value:   $18,750,000

SECTION 5: LOSS HISTORY (PAST 5 YEARS)
{SEPARATOR}
Year    Location              Cause of Loss            Gross Incurred   Status
----    --------              -------------            --------------   ------
2025    Loc 3, White Plains   Burst pipe / water         $210,000       Closed
2024    Loc 1, Park Ave       Elevator motor failure     $125,000       Closed
2023    Loc 5, Jersey City    Tenant fit-out fire         $88,000       Closed
2022    None reported         --                         --             --
2021    None reported         --                         --             --

Total 5-year incurred losses: $423,000
Note: Excellent loss record relative to portfolio size.

SECTION 6: PROTECTIVE SAFEGUARDS
{SEPARATOR}
- Fully automatic wet-pipe sprinkler systems at all 6 locations
- Centrally monitored fire alarm systems (UL-listed monitoring)
- 24/7 lobby security and building management staff at NYC locations
- Emergency generators for life-safety systems at all properties
- Annual fire pump testing and 5-year sprinkler system inspections
- Water leak detection sensors on all occupied floors

SECTION 7: ADDITIONAL INFORMATION
{SEPARATOR}
Current Carrier:        Hartford Financial / Navigators (surplus lines)
Expiring Premium:       $612,000 (expiring 05/01/2026)
Reason for Marketing:   Seeking competitive pricing; loss record supports
                        rate reduction. Also exploring broader flood capacity
                        for Jersey City location.
Prior Cancellations:    None
Bankruptcy History:     None
Pending Litigation:     None
Tenant Profile:         Financial services (38%), legal (22%), technology (18%),
                        professional services (14%), other (8%)

APPLICANT SIGNATURE
Date:       February 25, 2026
Name:       David Chen
Title:      Managing Director, Summit Office Partners LP
"""

# ---------------------------------------------------------------------------
# Write all files
# ---------------------------------------------------------------------------
applications = {
    "APP_pacific_retail.txt":   APP_PACIFIC_RETAIL,
    "APP_acme_industrial.txt":  APP_ACME_INDUSTRIAL,
    "APP_heritage_hotels.txt":  APP_HERITAGE_HOTELS,
    "APP_cascade_tech.txt":     APP_CASCADE_TECH,
    "APP_gulf_coast_energy.txt": APP_GULF_COAST,
    "APP_midwest_ag.txt":       APP_MIDWEST_AG,
    "APP_atlantic_seafood.txt": APP_ATLANTIC_SEAFOOD,
    "APP_summit_office.txt":    APP_SUMMIT_OFFICE,
}

for filename, content in applications.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    line_count = content.strip().count("\n") + 1
    print(f"  Written: {filename}  ({line_count} lines)")

print(f"\nAll {len(applications)} application files written to:\n  {OUTPUT_DIR}")
