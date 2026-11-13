"""Buyer page: winter storm power outage checklist (/guides/winter-storm-power-outage)."""

SLUG = "winter-storm-power-outage"
PARENT = "light-heat"
OG = "guide-winter-outage"
OG_CARD = ("Winter outages", "No power in a winter storm", "Heat one room, heat it safely, protect the pipes, and know when to leave. Printable checklist.")
TITLE = "Winter Storm Power Outage Checklist: How to Stay Warm and Safe Without Power"
META = ("What to do when a winter storm knocks out your power: heat one room safely, avoid carbon monoxide, keep pipes from freezing, "
        "keep food safe, and know when to go to a warming center. Printable checklist.")
H1 = "Losing power in a winter storm"
DEK = ("A winter outage is a heat problem first. Gather everyone in one warm room, heat it safely, keep the pipes from freezing, "
       "and know when it's time to go somewhere warmer. Here's the checklist, before the storm and after the lights go out.")
REVIEWED = "Ready.gov, CDC and USDA guidance"
CRUMB = "Winter outage"

VERDICT = [
    ("Heat one room, not the whole house.", "Pick a small room with few windows, close its doors, hang blankets over windows and doorways, and have everyone sleep there."),
    ("Never heat with a grill, camp stove, gas oven or generator indoors.", "They produce carbon monoxide, which you can't see or smell. Run generators outdoors only, at least 20 feet from doors and windows."),
    ("Put a battery-powered CO alarm on every sleeping floor.", "Plug-in alarms without a battery backup stop working when the power goes out, which is when they're needed most."),
    ("Keep the pipes from freezing.", "Let faucets drip and open the cabinet doors under sinks so warmer air reaches the pipes."),
    ("Know when to leave.", "If the house keeps getting colder, or someone is very young, old or relies on powered medical equipment, go to a warming center, a friend's place or a hotel."),
]

STEPS_TITLE = "Before the storm, and after the lights go out"
STEPS = [
    ("Before the storm: charge and stock up", "Charge phones, power banks and any power station. Fill the car's tank. Refill prescriptions. Bring pets inside. Store some water in case pipes freeze or a water main breaks."),
    ("When it goes out: report it and unplug", "Report the outage to your utility. Unplug electronics and appliances to protect them from a surge when power returns, and leave one lamp switched on so you know when it's back."),
    ("Gather in one warm room", "Close off rooms you aren't using. Cover windows and gaps under doors with blankets or towels. A small interior room loses heat more slowly."),
    ("Dress for the cold, indoors", "Layers, hats, wool socks and sleeping bags. Eat regular meals and drink water; your body needs fuel to make heat. Skip alcohol, which makes you lose heat faster."),
    ("Heat safely, or not at all", "Use only heaters rated for indoor use, follow the label's ventilation instructions, and keep a battery CO alarm nearby. A fireplace is fine with a clean chimney and the flue open. Never use the oven, a grill or a camp stove for heat."),
    ("Protect the pipes", "Keep faucets dripping. If a pipe freezes, thaw it slowly with warm towels, never an open flame. Know where your main water shutoff is in case one bursts."),
    ("Check on people, and leave if you need to", "Check on older neighbors. Call 211 or check local news for warming centers. Call 911 for signs of hypothermia: intense shivering, confusion, slurred speech or drowsiness."),
]

PICKS = [
    {"name": "Battery-powered CO alarm (Kidde, First Alert)", "asin": "B004Y6V5CI", "asin_name": "Kidde battery CO alarm", "price": "$20 to $40",
     "what": "A carbon monoxide alarm that keeps working with the power out.",
     "why": "Winter outages are when people bring heaters, generators and grills into the wrong places. This is the cheapest life-saver on the site.",
     "watch": "One on every sleeping floor, and near any fuel-burning heater. Test it before the storm.",
     "best": "Every home"},
    {"name": "Mr. Heater Buddy indoor-safe propane heater", "asin": "B0GYT8HCT6", "asin_name": "Mr. Heater Portable Buddy (Midnight Series)", "price": "$90 to $150",
     "what": "A portable propane heater rated for indoor use, with a low-oxygen shutoff and a tip-over switch.",
     "why": "Keeps one closed-off room livable without electricity. It runs on the small propane cylinders sold for camping.",
     "watch": "Follow the label's ventilation instructions, keep it 3 feet from anything that burns, and keep a battery CO alarm in the room. Store propane outdoors.",
     "best": "Homes that lose heat in long outages"},
    {"name": "Cold-rated sleeping bags", "asin": "B005EPRM4I", "asin_name": "TETON Celsius; pick the 20°F or 0°F version", "price": "$60 to $200 each",
     "what": "Sleeping bags rated for freezing temperatures.",
     "why": "The simplest heat source there is: no fuel, no fumes, no power. Everyone sleeps warm in a cold house.",
     "watch": "Temperature ratings are for survival, not comfort. Pick a bag rated 10 to 20 degrees colder than you expect.",
     "best": "Every person in a cold-climate home"},
    {"name": "Arcturus military wool blanket", "asin": "B01IJWUYLK", "price": "$40 to $50",
     "what": "A heavy wool blanket.",
     "why": "Warm even when damp, good for covering a doorway or window, and it doubles as the car blanket.",
     "watch": "Wool can be itchy; layer it over a sheet or a cotton blanket.",
     "best": "Covering doorways, extra warmth"},
    {"name": "1 kWh power station (Anker SOLIX C1000 or similar)", "asin": "B0C5C89QKZ", "asin_name": "Anker SOLIX C1000", "price": "$400 to $900",
     "what": "A silent battery with AC outlets, safe to use indoors.",
     "why": "Runs an electric blanket all night (about 60 W), a CPAP, phones, lights and a router.",
     "watch": "Not for space heaters: a 1,500 W heater would drain it in under 40 minutes. Use the power station calculator to size it.",
     "best": "CPAP users, apartments, long outages"},
    {"name": "Goal Zero Lighthouse 600 lantern", "asin": "B08HRM4J8Y", "price": "$40 to $90",
     "what": "A battery lantern that lights a room and charges by USB or hand crank.",
     "why": "Long winter nights mean many hours of darkness. Safer than candles, which start fires in outages every year.",
     "watch": "Charge it before the storm. The hand crank is for emergencies; it's slow.",
     "best": "The warm room"},
    {"name": "Midland ER310 crank and solar emergency radio", "asin": "B015QIC1PW", "asin_name": "Midland ER310", "price": "$50 to $80",
     "what": "An AM, FM and NOAA weather radio with a hand crank, solar panel and flashlight.",
     "why": "Updates on the storm, road closures and warming centers when phones are dying and the internet is down.",
     "watch": "Test the crank and the weather band before winter.",
     "best": "Every home"},
]

CHECKLIST_TITLE = "Winter outage checklist"
CHECKLIST = [
    "Battery CO alarm on every sleeping floor", "Smoke alarms tested", "Phones, power banks and power station charged",
    "Flashlight or headlamp for each person", "Battery or crank radio", "Sleeping bag or warm blankets for each person",
    "Hats, gloves and wool socks", "Indoor-safe heater and fuel (stored outdoors), or a plan without one",
    "Blankets or towels to cover windows and doors", "Water stored: 1 gallon per person per day",
    "No-cook food for 3 days or more", "Manual can opener", "Prescriptions refilled",
    "Cooler and ice packs for the fridge food", "Gas tank at least half full", "Main water shutoff located",
    "Utility's outage number saved", "Warming center or a warm place to go",
]
CHECKLIST_NOTE = "Tick items off before the storm. Your progress stays in this browser."
CHECKLIST_LINK = ("Staying warm without power", "light-heat.html")

SECTIONS = [
    ("Food and water in a winter outage", [
        ("Keep the fridge and freezer closed", "The USDA says a closed fridge keeps food safe for about 4 hours without power, and a full freezer about 48 hours (24 if half full)."),
        ("Don't store food outside in the snow", "The USDA warns that sun can thaw frozen food and that outdoor temperatures swing too much. Animals can get to it too. Use a cooler with ice or snow instead."),
        ("Keep drinking water", "Cold weather hides thirst. If pipes freeze or a main breaks, your stored water and the water heater are your supply. The water calculator shows how much to store."),
    ]),
    ("Medical needs", [
        ("Powered medical devices", "Size a power station for the device first, and tell your utility you rely on it. Turning off a CPAP's heated humidifier cuts its power use by four to five times."),
        ("Medicines that need refrigeration", "Keep insulin and similar medicines in a cooler with ice packs, not touching the ice. The first aid guide covers storage in an outage."),
    ]),
]

FAQS = [
    ("Is it safe to use a gas oven or stove to heat the house?",
     "No. The CDC warns never to use a gas range or oven to heat a home. It can produce carbon monoxide, and in a closed-up house during an outage it can build to deadly levels."),
    ("Can I run a space heater on a power station?",
     "Not for long. A space heater draws about 1,500 W, so a 1,000 Wh power station runs it for under 40 minutes. An electric blanket uses about 60 W and runs all night. Our power station calculator shows what yours can handle."),
    ("Should I let my faucets drip?",
     "Yes, during hard freezes. Ready.gov recommends letting cold water drip from faucets served by exposed pipes and opening cabinet doors so warmer air reaches the plumbing."),
    ("Can I use my fireplace?",
     "Yes, if the chimney has been cleaned and the flue is open. Most of a fireplace's heat goes up the chimney, so close off the room around it to make the most of it, use a screen, and keep a CO alarm nearby."),
    ("When should I go to a warming center?",
     "If your home keeps getting colder, if anyone is a baby, an older adult or relies on powered medical equipment, or if you can't heat a room safely. Call 211 or check local news for open warming centers."),
]

SOURCES = [
    ("Ready.gov: #WinterReady", "https://www.ready.gov/winter-ready"),
    ("Ready.gov: Power outages", "https://www.ready.gov/power-outages"),
    ("CDC: Avoiding carbon monoxide poisoning", "https://www.cdc.gov/natural-disasters/psa-toolkit/avoiding-carbon-monoxide-poisoning.html"),
    ("USDA: Keep your food safe during emergencies", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies"),
]

RELATED = [("Power station calculator", "../power-calculator.html"), ("Keeping a CPAP running in an outage", "cpap-power-outage.html"),
           ("Stuck in your car in a snowstorm", "stranded-in-car-winter.html"), ("Staying warm without power", "light-heat.html"),
           ("Food storage calculator", "../food-calculator.html"), ("Water storage calculator", "../water-calculator.html"),
           ("Older adults and people with disabilities", "older-adults-disabilities.html")]
CALC_LINK = ("To size backup power for an electric blanket, CPAP, phones and lights, use the", "../power-calculator.html", "power station calculator")
