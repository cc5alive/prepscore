"""Buyer page: emergency kit on a budget, $100 / $300 / $1,000 (/guides/emergency-kit-on-a-budget)."""

SLUG = "emergency-kit-on-a-budget"
PARENT = "go-bag"
OG = "guide-budget-kits"
OG_CARD = ("Emergency kits", "A kit for $100, $300 or $1,000", "What to buy first at each budget, and what to get free from your own kitchen.")
TITLE = "Emergency Kit on a Budget: What to Buy for $100, $300 or $1,000"
META = ("How to build an emergency kit for about $100, $300 or $1,000: what to buy first at each budget, what you can get free, "
        "and what to skip. Built on Ready.gov and Red Cross kit lists.")
H1 = "An emergency kit for $100, $300 or $1,000"
DEK = ("You don't need to spend a lot to be ready for the first few days. Here's what to buy first at each budget, for a household of "
       "two, in the order that matters most.")
REVIEWED = "Ready.gov and American Red Cross kit lists and manufacturer specifications"
CRUMB = "Kit on a budget"

GRID_TOC = "What each budget buys"
GRID_LINK = "Amounts for your household"
GRID = ("What each budget buys",
        "For two people. Budgets are rough running totals at typical prices, and each one builds on the one before it; the $1,000 column assumes you buy the power station on sale.",
        ["", "About $100", "About $300", "About $1,000"],
        [["Water", "6 gallons of store-bought jugs (3 days for two), plus clean bottles you fill free", "Two stackable 5-gallon containers", "Stackable containers for 2 weeks (28 gallons) and a Sawyer Squeeze filter"],
         ["Food", "3 days of canned and shelf-stable food you already eat, and a manual can opener", "Add emergency food bars for go-bags", "2 weeks of pantry food you rotate, and a camp stove for use outdoors"],
         ["Light", "Two LED flashlights or budget headlamps", "A rechargeable headlamp each", "Same headlamps, with spare batteries or a way to charge them"],
         ["Phone power", "A 10,000 mAh power bank", "A 20,000 mAh power bank each", "A 1,000 Wh power station, which also runs a CPAP or fridge for hours"],
         ["News and alerts", "Free: turn on emergency alerts on your phone and sign up for county alerts", "A crank and solar NOAA weather radio", "Same radio"],
         ["First aid", "A small first-aid kit and a week of daily medications", "A family first-aid kit", "Add a tourniquet, and take a first-aid class"],
         ["Sanitation", "A bucket, heavy trash bags, wipes and hand sanitizer", "Toilet bags with gel, plus a toilet seat for the bucket", "A two-bucket toilet setup and two weeks of bags and cover material"],
         ["Warmth and air", "A few N95 masks; blankets from home", "A wool blanket each and N95s", "A battery CO alarm; warmer bedding if your winters are cold"],
         ["Documents and cash", "Free: photos of IDs and insurance in a secure cloud folder; some small bills", "A fire- and water-resistant document bag", "Same bag, kept with a packed go-bag by the door"]])

VERDICT = [
    ("Start with water, food you already eat, light and a way to charge your phone.", "Those four cover most of what goes wrong in a typical outage or evacuation, and about $100 buys all of them for two people."),
    ("Get the free things done first.", "Fill clean bottles with tap water, turn on emergency alerts on your phone, photograph your documents and set aside a week of medications. None of it costs anything."),
    ("At $300, the kit gets sturdier.", "A weather radio, a real first-aid kit, a headlamp each and a toilet plan are the upgrades that matter most."),
    ("At $1,000, plan for two weeks.", "Ready.gov suggests several days of supplies; two weeks at home covers the long outages that follow hurricanes, ice storms and earthquakes. A small power station is the biggest single upgrade."),
    ("Skip most premade kits.", "Many are filled with tiny first-aid kits, thin blankets and little water. Building your own costs about the same and covers what you'll actually use."),
]

STEPS_TITLE = "Free steps that come first"
STEPS = [
    ("Store tap water", "Clean, food-grade bottles filled from the tap work. Label them with the date and replace every 6 months."),
    ("Turn on alerts", "Check that Wireless Emergency Alerts are on in your phone's settings, and sign up for your county's alert system."),
    ("Make a plan", "Agree where you'll meet and who outside the area everyone checks in with. Write numbers on paper; phones die."),
    ("Protect your documents", "Photograph IDs, insurance and medical records and store them in a secure cloud folder."),
    ("Check your pantry", "Count how many days of no-cook food you already have. Most homes have more than they think."),
    ("Refill prescriptions early", "Ask your pharmacist or insurer about refilling a few days early so you always have a week on hand."),
]

SECTIONS = [
    ("Where to save and where not to", [
        ("Save on food", "Buy what you already eat and rotate it. Specialty emergency food costs far more per day than canned and dry goods."),
        ("Save on water", "Store-bought gallon jugs and refilled bottles cost little. Containers are an upgrade for space and durability, not a requirement."),
        ("Don't skimp on light", "Candles cause house fires during outages. A cheap LED flashlight is safer and costs less than a box of good candles."),
        ("Don't skimp on medications", "A week of daily medications and spare glasses matter more than anything you can buy."),
        ("Buy on sale", "Power stations, radios and headlamps go on sale around Black Friday, Prime Day and before hurricane season."),
    ]),
]

PICKS = [
    {"name": "Manual can opener", "asin": "B00004OCJW", "asin_name": "OXO Good Grips manual can opener", "price": "$15 to $20",
     "what": "A hand-crank can opener with soft handles.",
     "why": "Turns any canned food in your pantry into emergency food. The cheapest piece of a $100 kit, and the one people forget.",
     "watch": "Electric openers stop with the power. Keep this one with the kit, not in the kitchen drawer.",
     "best": "Every kit, at every budget"},
    {"name": "Anker 20,000 mAh power bank", "asin": "B0CXDXP8VR", "price": "$30 to $60",
     "what": "A pocket battery that recharges a phone about four times.",
     "why": "Your phone is your map, flashlight and alert system. This keeps it going for several days.",
     "watch": "Recharge it every few months; batteries slowly drain on the shelf.",
     "best": "The $100 and $300 kits"},
    {"name": "Midland ER310 crank and solar emergency radio", "asin": "B015QIC1PW", "price": "$50 to $80",
     "what": "An AM/FM and NOAA weather radio you can power by crank, solar or batteries, with a flashlight and USB charging.",
     "why": "Gets official alerts and news when cell networks are down. The top upgrade at $300.",
     "watch": "Cranking charges slowly; keep batteries in it too.",
     "best": "The $300 kit and up"},
    {"name": "Adventure Medical Kits Family first-aid kit", "asin": "B0079ODGHO", "price": "$30 to $60",
     "what": "A first-aid kit stocked for a household, organized by injury.",
     "why": "Covers the cuts, burns and sprains you'll treat yourself when emergency services are stretched.",
     "watch": "Open it once so you know what's inside, and add your own medications.",
     "best": "The $300 kit and up"},
    {"name": "Reliance Double Doodie toilet waste bags", "asin": "B07M863D89", "price": "$25 to $70",
     "what": "Toilet bags with a gel that solidifies waste, for a bucket or your toilet bowl.",
     "why": "If water stops, toilets stop. This is the simplest toilet plan.",
     "watch": "Twelve bags won't last two people long; for two weeks, see our sanitation guide's bag math.",
     "best": "The $300 kit and up"},
    {"name": "1 kWh power station (Anker SOLIX C1000)", "asin": "B0C5C89QKZ", "price": "$400 to $900",
     "what": "A 1,056 Wh LiFePO4 battery with 6 AC outlets, safe to use indoors.",
     "why": "The biggest single upgrade at $1,000: keeps phones, lights, internet and a CPAP going for days, and a fridge for most of a day.",
     "watch": "About 28 pounds. Watch for sales; prices swing widely.",
     "best": "The $1,000 kit"},
]

FAQS = [
    ("What should I buy first for an emergency kit?",
     "Water, food you can eat without cooking, a flashlight or headlamp, and a power bank for your phone. Add a first-aid kit and a week of medications. These match the core of Ready.gov's basic kit list."),
    ("Is a premade emergency kit worth it?",
     "Usually not as your only kit. Many contain very little water and food and low-quality first-aid supplies. A premade kit can be a quick start for a car or office, but building your own covers more for the money."),
    ("How much water do I need for three days?",
     "Ready.gov says one gallon per person per day, so 3 gallons per person for three days, and more for hot weather, nursing mothers, children and pets."),
    ("Can I build a kit for under $100?",
     "Yes, especially if you start with free steps: tap water in clean bottles, food you already have, a plan and phone alerts. Then spend on a can opener, flashlights, a power bank, a small first-aid kit and sanitation basics."),
    ("Where should I keep my kit?",
     "Keep a home kit somewhere easy to reach, like a hall closet, and a smaller go-bag by the door or in the car. Store water and food somewhere cool and dark."),
]

SOURCES = [
    ("Ready.gov: Build a Kit", "https://www.ready.gov/kit"),
    ("American Red Cross: Make a survival kit", "https://www.redcross.org/get-help/how-to-prepare-for-emergencies/survival-kit-supplies.html"),
    ("Ready.gov: Water", "https://www.ready.gov/water"),
    ("FEMA: Wireless Emergency Alerts", "https://www.fema.gov/emergency-managers/practitioners/integrated-public-alert-warning-system/public/wireless-emergency-alerts"),
]

RELATED = [("The 3-day kit, for any household size", "../72-hour-kit.html"), ("Go-bag guide", "go-bag.html"),
           ("Emergency water guide", "water.html"), ("Emergency sanitation guide", "sanitation.html"),
           ("Prep gear worth buying on sale", "../black-friday.html")]
CALC_LINK = ("For exact amounts for your household, use the", "../72-hour-kit.html", "3-day kit checklist")
