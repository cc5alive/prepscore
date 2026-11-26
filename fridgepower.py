"""Buyer page: what size power station runs a refrigerator (/guides/power-station-for-refrigerator)."""

SLUG = "power-station-for-refrigerator"
PARENT = "power"
OG = "guide-fridge-power"
OG_CARD = ("Backup power", "Power station for a fridge", "How long each size runs your refrigerator, what surge it needs, and what to buy.")
TITLE = "What Size Power Station Runs a Refrigerator? Runtime Table"
META = ("How long a 1,000, 2,000 or 3,600 Wh power station runs a refrigerator, by fridge type, plus the surge rating you need, "
        "why cycling the fridge doesn't stretch the battery, and what to buy.")
H1 = "What size power station runs a refrigerator?"
DEK = ("A fridge is the load most people want to save in an outage, and the one that drains a battery fastest. Here's how long each size "
       "lasts, what to check before you buy, and how to make the battery go further.")
REVIEWED = "USDA, DOE, ENERGY STAR and manufacturer specifications"
CRUMB = "Power station for a fridge"

USABLE = 0.85  # share of rated capacity you get out of the AC outlets, after inverter losses
STATIONS = [("1,000 Wh", 1000), ("2,000 Wh", 2042), ("3,600 Wh", 3584)]
FRIDGES = [  # (type, low kWh/day, high kWh/day)
    ("Compact or dorm fridge (under 5 cu ft)", 0.3, 0.8),
    ("Newer top- or bottom-freezer fridge", 1.0, 1.4),
    ("Newer side-by-side or French door", 1.5, 2.2),
    ("Fridge 20 or more years old", 2.5, 4.5),
]


def _span(lo_kwh, hi_kwh, wh):
    usable = wh * USABLE
    a, b = usable / (hi_kwh * 1000) * 24, usable / (lo_kwh * 1000) * 24
    if b < 48:
        return f"{round(a)} to {round(b)} hours"
    d = lambda h: f"{h / 24:.1f}".replace(".0", "")
    if a >= 48:
        return f"{d(a)} to {d(b)} days"
    return f"{round(a)} hours to {d(b)} days"


GRID = ("How long a power station runs a fridge",
        "Hours of fridge-only use at 85% of rated capacity, which is about what you get through the AC outlets. Real results vary with "
        "the room temperature, how full the fridge is and how often the door opens. Your fridge's yellow EnergyGuide label gives kWh per year; "
        "divide by 365 for a day.",
        ["Fridge type", "Typical use per day"] + [s for s, _ in STATIONS],
        [[t, f"{lo:g} to {hi:g} kWh"] + [_span(lo, hi, wh) for _, wh in STATIONS] for t, lo, hi in FRIDGES])

VERDICT = [
    ("For most newer fridges, 1,000 Wh buys about 15 to 20 hours.", "That covers the common outage of a day or less, which is when a fridge matters most. For two days or more, look at 2,000 Wh and up, or add solar."),
    ("Check the surge rating, not just the battery size.", "A fridge draws a few hundred watts running, and several times that for a moment when the compressor starts. A station rated around 1,500 W continuous handles most household fridges; small 300 W stations usually can't."),
    ("Turning the fridge off and on doesn't stretch the battery much.", "While it's off, heat leaks in, and the compressor has to remove it when you switch back on. Unplug to share the station or to recharge it, not to save energy."),
    ("Keep the doors shut and the fridge full.", "That saves more battery than anything else, and the USDA says a closed fridge keeps food safe for about 4 hours even with no power at all."),
    ("Old fridges can use three times the energy.", "If yours is 20 or more years old, even a 3,600 Wh station runs it for only about a day. Check the EnergyGuide label or measure it with a plug-in meter first."),
]

STEPS_TITLE = "Before an outage, and when the power goes out"
STEPS = [
    ("Find your fridge's real number", "Look for kWh per year on the yellow EnergyGuide label and divide by 365, or plug the fridge into an inexpensive electricity meter for a day. That number decides everything else."),
    ("Check the station's specs", "Continuous output of about 1,500 W or more and a surge rating a few times your fridge's running watts. LiFePO4 batteries last for thousands of charges."),
    ("Keep it charged", "Top up the station every few months and before any storm or planned power shutoff. A half-empty battery gives half the runtime."),
    ("Prepare the fridge", "Set it to 37°F, keep it full (jugs of water work), and freeze a few bottles in the freezer to act as ice packs. Put a thermometer inside."),
    ("When the power goes out", "Plug the fridge straight into the station's AC outlet with its own cord, not a thin extension cord. Keep the doors shut, and plan meals so you open it as little as possible."),
    ("Watch the temperature", "The USDA says to discard perishables that sit above 40°F for more than 2 hours. A thermometer tells you instead of guessing."),
    ("Recharge when you can", "From the wall when power returns, from a car while driving, or from a solar panel during the day."),
]

SECTIONS = [
    ("What affects runtime", [
        ("Surge", "A compressor needs a burst of power to start. If the station's surge rating is too low, it will shut off every time the fridge kicks on. Inverter-driven fridges start more gently."),
        ("Cycling", "A fridge already cycles on and off by itself. Unplugging it for hours and plugging it back in mostly moves the energy use around: the compressor works harder afterward to pull the heat back out. Switching the station's AC output off when nothing is plugged in does save its small idle draw."),
        ("The defrost heater", "Frost-free fridges run a heater for a short time every so often to melt frost, which can briefly draw more than the compressor. It's one reason a fridge's daily use varies."),
        ("Room temperature", "A fridge in a hot garage works much harder than one in a cool kitchen. In a summer outage, expect the low end of the table."),
        ("Freezers", "A full chest freezer often uses less than a fridge and holds its temperature for about 48 hours closed (24 if half full). If you need the station for other things, a full freezer can go unpowered for a few hours at a time because frozen food holds cold well; check it with a thermometer."),
    ]),
]

PICKS = [
    {"name": "1 kWh power station (Anker SOLIX C1000)", "asin": "B0C5C89QKZ", "price": "$400 to $900",
     "what": "A 1,056 Wh LiFePO4 station rated 1,800 W continuous and 2,400 W surge, with 6 AC outlets.",
     "why": "Runs most newer fridges for about 15 to 20 hours, with enough surge for the compressor, and also handles phones, lights and a CPAP.",
     "watch": "About 28 pounds. Not enough for more than a day of fridge use on its own; pair with solar for longer outages.",
     "best": "Apartments and outages of a day or less"},
    {"name": "2 kWh power station (Jackery Explorer 2000 v2)", "asin": "B0DFG2WDQH", "price": "$900 to $1,500",
     "what": "A 2,042 Wh LiFePO4 station rated 2,200 W continuous and 4,400 W surge.",
     "why": "About 30 to 40 hours of a newer fridge, or about a day of the fridge plus phones, lights and internet.",
     "watch": "About 40 pounds, and only 3 AC outlets. Check the outlet count against what you want to plug in.",
     "best": "Houses with a full-size fridge and multi-day outages"},
    {"name": "Large expandable battery (Jackery HomePower 3600 Plus)", "asin": "B0FM8653F1", "price": "$1,500 to $3,000",
     "what": "A home backup battery of about 3.6 kWh that can add extra battery packs.",
     "why": "Two to three days of a newer fridge, or a fridge plus a freezer, with room to grow.",
     "watch": "Heavy and expensive. At this size, compare it with a dual-fuel inverter generator run safely outdoors.",
     "best": "Long outages, fridge plus freezer, medical refrigeration"},
    {"name": "Fridge and freezer thermometer", "q": "refrigerator freezer thermometer", "price": "$5 to $15",
     "what": "A small dial or digital thermometer that sits inside the fridge or freezer.",
     "why": "Tells you whether food is still below 40°F, so you don't have to guess what to throw out.",
     "watch": "Get one for the fridge and one for the freezer.",
     "best": "Every household"},
    {"name": "Plug-in electricity usage meter", "q": "plug in electricity usage monitor", "price": "$15 to $30",
     "what": "A meter that plugs in between the wall and the appliance and shows watts and kWh used.",
     "why": "Measures what your fridge really uses in a day, so you can size the station to your fridge instead of a guess.",
     "watch": "Leave it for a full 24 hours; a fridge's use swings a lot hour to hour.",
     "best": "Anyone about to spend hundreds on a power station"},
]

FAQS = [
    ("Can a 1,000 Wh power station run a refrigerator?",
     "Yes, if its continuous and surge ratings cover the compressor, which most 1,000 Wh stations rated 1,500 W or more do. A newer fridge using 1 to 1.4 kWh a day runs about 15 to 20 hours on one charge."),
    ("Can a 500 Wh or 300 Wh station run a fridge?",
     "A 300 W station usually can't start a full-size fridge's compressor. A 500 W station may run a compact fridge, but it's not enough to count on for a full-size one. Use smaller stations for phones, lights and a CPAP."),
    ("Does running the fridge a few hours at a time save battery?",
     "Not much. While the fridge is off, heat leaks in, and the compressor has to remove it when it restarts, so the total energy is about the same. Unplugging still helps if you need the station for something else or want to recharge it."),
    ("How long does food stay safe without power?",
     "The USDA says about 4 hours in a closed refrigerator, about 48 hours in a full freezer and about 24 in a half-full one. Discard perishables that have been above 40°F for more than 2 hours."),
    ("Will solar keep a fridge running?",
     "Partly. A 200 W folding panel typically puts back 400 to 700 Wh on a clear day, about half of what a newer fridge uses. Two panels on a 2,000 Wh station can come close in sunny weather."),
    ("Is a generator better for a fridge?",
     "For long outages, often yes: a gas or dual-fuel generator runs a fridge for as long as you have fuel. It must run outdoors, at least 20 feet from doors and windows, because of carbon monoxide. A power station is silent and safe indoors."),
]

SOURCES = [
    ("USDA FSIS: Keep your food safe during emergencies", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies"),
    ("U.S. Department of Energy: Estimating appliance and home electronic energy use", "https://www.energy.gov/energysaver/estimating-appliance-and-home-electronic-energy-use"),
    ("ENERGY STAR: Refrigerators", "https://www.energystar.gov/products/refrigerators"),
    ("Minnesota Commerce Department: Refrigerators and freezers (old vs. new energy use)", "https://mn.gov/commerce-stat/pdfs/refrigerators-and-freezers.pdf"),
    ("CDC: What to do during a power outage", "https://www.cdc.gov/natural-disasters/response/what-to-do-protect-yourself-during-a-power-outage.html"),
]

RELATED = [("Power station calculator", "../power-calculator.html"), ("Backup power guide", "power.html"),
           ("Keeping a CPAP running in an outage", "cpap-power-outage.html"), ("Losing power in a winter storm", "winter-storm-power-outage.html"),
           ("Emergency food guide", "food.html")]
CALC_LINK = ("To size a station for your fridge plus everything else you want to run, use the", "../power-calculator.html", "power station calculator")
