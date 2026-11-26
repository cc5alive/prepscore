"""Buyer page: how long a power station runs common devices (/guides/power-station-runtime)."""

SLUG = "power-station-runtime"
PARENT = "power"
OG = "guide-runtime"
OG_CARD = ("Backup power", "Power station runtime", "How long 300 Wh to 3,600 Wh runs phones, lights, a CPAP, a fridge and more.")
TITLE = "How Long Will a Power Station Last? Runtime Table by Device"
META = ("How long a 300, 1,000, 2,000 or 3,600 Wh power station runs phones, lights, a router, a CPAP, a fridge, a freezer, "
        "a microwave and more, with the math so you can check your own devices.")
H1 = "How long will a power station last?"
DEK = ("One table for the question everyone asks before buying: what will this run, and for how long? Find your devices, "
       "then pick the smallest size that covers the outage you're planning for.")
REVIEWED = "DOE appliance-energy guidance, ResMed and ENERGY STAR figures, and manufacturer specifications"
CRUMB = "Power station runtime"

USABLE = 0.85  # share of rated capacity that reaches the AC outlets after inverter losses
# (column label, rated Wh, continuous output W, surge W): one row per station class, matching our picks
STATIONS = [("300 Wh", 300, 300, 600), ("1,000 Wh", 1000, 1800, 2400), ("2,000 Wh", 2042, 2200, 4400), ("3,600 Wh", 3584, 3600, 7200)]


def _dur(h):
    if h < 2:
        return f"{round(h * 60 / 5) * 5} minutes"
    if h < 10:
        return f"{round(h * 2) / 2:g} hours"
    if h < 48:
        return f"{round(h)} hours"
    return f"{h / 24:.1f} days".replace(".0 days", " days")


def _cell(kind, a, b, run_w, surge_w, st):
    _, wh, out, surge = st
    if run_w > out or surge_w > surge:
        return "Too big for this size"
    use = wh * USABLE
    if kind == "charges":
        return f"About {int(use / a)} charges"
    if kind == "nights":
        n = use / a
        return "Less than 1 night" if n < 1 else f"About {int(n)} night" + ("s" if int(n) != 1 else "")
    if kind == "perday":  # a, b = kWh a day, low and high
        lo, hi = use / (b * 1000) * 24, use / (a * 1000) * 24
        if round(lo) == round(hi):
            return _dur(lo)
        if hi < 48:
            return f"{round(lo)} to {round(hi)} hours"
        if lo >= 48:
            return f"{lo / 24:.1f} to {hi / 24:.1f} days".replace(".0 ", " ").replace(".0 days", " days")
        return f"{round(lo)} hours to {hi / 24:.1f} days".replace(".0 days", " days")
    return _dur(use / a)  # watts, running steadily


# (device, typical use as shown, kind, a, b, running W, surge W). Figures match our power station calculator.
DEVICES = [
    ("Phone", "About 15 Wh per full charge", "charges", 15, 0, 20, 0),
    ("LED bulb or lantern", "About 9 W", "watts", 9, 0, 9, 0),
    ("Wi-Fi router and modem", "About 15 W together", "watts", 15, 0, 15, 0),
    ("Laptop", "About 50 W in use", "watts", 50, 0, 50, 0),
    ("Box fan", "About 50 W on medium", "watts", 50, 0, 50, 0),
    ("Electric blanket", "About 60 W on low to medium", "watts", 60, 0, 60, 0),
    ("50-inch LED TV", "About 80 W", "watts", 80, 0, 80, 0),
    ("CPAP, humidifier and heated tube off", "About 85 Wh a night", "nights", 85, 0, 60, 0),
    ("CPAP with heated humidifier and tube", "About 400 Wh a night", "nights", 400, 0, 120, 0),
    ("Refrigerator, newer", "1 to 1.4 kWh a day", "perday", 1.0, 1.4, 150, 1200),
    ("Chest freezer", "About 0.8 kWh a day", "perday", 0.8, 0.8, 100, 800),
    ("Compact microwave", "About 1,200 W while running", "watts", 1200, 0, 1200, 0),
    ("Space heater", "About 1,500 W on high", "watts", 1500, 0, 1500, 0),
]

GRID = ("Runtime by device and station size",
        "One device at a time, at 85% of rated capacity, which is about what reaches the AC outlets. Run several at once and divide: "
        "a fridge plus lights plus a router uses the battery faster than the fridge alone. “Too big” means the device's running or starting "
        "watts are more than a typical station of that size can deliver.",
        ["Device", "Typical use"] + [s[0] for s in STATIONS],
        [[d, use] + [_cell(k, a, b, rw, sw, st) for st in STATIONS] for d, use, k, a, b, rw, sw in DEVICES])

VERDICT = [
    ("For phones, lights, a router and a CPAP, 300 to 500 Wh is plenty.", "A 300 Wh station charges a phone about 17 times, runs a router for about 17 hours, or covers 3 nights of CPAP with the heat off."),
    ("To keep a fridge cold, start at 1,000 Wh.", "That runs a newer fridge for about 15 to 20 hours. Small 300 W stations usually can't start a fridge's compressor at all. See our page on powering a refrigerator."),
    ("Heat and cooking drain any battery fast.", "A space heater empties a 1,000 Wh station in about half an hour. Use battery power for an electric blanket instead, and cook on a camp stove outdoors."),
    ("Check two numbers: watt-hours and watts.", "Watt-hours (Wh) decide how long it lasts. Watts (W) decide what it can run at once, including the brief surge when a motor starts."),
    ("Your own devices may differ.", "The label or power adapter gives watts. For an exact figure, use our calculator or a plug-in electricity meter."),
]

STEPS_TITLE = "How to work out your own runtime"
STEPS = [
    ("List what you want to run", "Phones, lights, a router, medical devices, the fridge. Skip anything with a heating element unless you have a big battery and a reason."),
    ("Find each device's watts", "Look on the label, the power adapter or the manual. For a fridge or freezer, the yellow EnergyGuide label gives kWh per year: divide by 365 for a day."),
    ("Multiply by hours", "Watts times hours of use equals watt-hours. A 15 W router on all day is 15 × 24 = 360 Wh."),
    ("Add it up and allow for losses", "Divide the total by 0.85 to cover the inverter's losses. That's the battery size you need for one day."),
    ("Check the watts", "Add the running watts of everything that will be on at once, and make sure the station's continuous rating covers it, with room for a motor's starting surge."),
    ("Plan for recharging", "For outages longer than a day, add a solar panel or plan to recharge from a car. Or use our calculator, which does all of this for you."),
]

SECTIONS = [
    ("Why your results will differ", [
        ("Inverter losses", "Converting the battery's DC power to household AC wastes energy. We assume you get 85% of the rated capacity; USB and 12 V outputs lose less."),
        ("Idle draw", "A station's AC inverter uses a little power even with nothing plugged in. Switch AC off when you aren't using it."),
        ("Temperature", "Batteries deliver less in the cold. A station in a freezing garage won't match the table; keep it indoors."),
        ("Battery age", "LiFePO4 batteries keep most of their capacity for thousands of charges. Older lithium-ion stations lose capacity faster."),
        ("Cycling loads", "Fridges, freezers and pumps switch on and off by themselves, so their daily energy use, not their peak watts, sets the runtime."),
    ]),
]

PICKS = [
    {"name": "Small power station, about 300 Wh (Anker SOLIX C300)", "asin": "B0D62GMQ3F", "price": "$150 to $250",
     "what": "A 288 Wh LiFePO4 station, rated 300 W continuous and 600 W surge, with AC, USB-C and a car port.",
     "why": "Covers phones, lights, a router and a few nights of CPAP with the heat off. About 9 pounds.",
     "watch": "300 W is the ceiling. It won't run a fridge, a microwave or a space heater. Make sure the listing is the AC model, not the C300 DC.",
     "best": "Apartments and short outages"},
    {"name": "1 kWh power station (Anker SOLIX C1000)", "asin": "B0C5C89QKZ", "price": "$400 to $900",
     "what": "A 1,056 Wh LiFePO4 station rated 1,800 W continuous and 2,400 W surge, with 6 AC outlets.",
     "why": "The size most households need: a newer fridge for 15 to 20 hours, or phones, lights and internet for days.",
     "watch": "About 28 pounds. Pair it with a solar panel for anything longer than a day or two.",
     "best": "Most households"},
    {"name": "2 kWh power station (Jackery Explorer 2000 v2)", "asin": "B0DFG2WDQH", "price": "$900 to $1,500",
     "what": "A 2,042 Wh LiFePO4 station rated 2,200 W continuous and 4,400 W surge.",
     "why": "About 30 to 40 hours of a newer fridge, or a day of the fridge plus phones, lights and internet.",
     "watch": "About 40 pounds, and only 3 AC outlets.",
     "best": "Houses and multi-day outages"},
    {"name": "Large expandable battery (Jackery HomePower 3600 Plus)", "asin": "B0FM8653F1", "price": "$1,500 to $3,000",
     "what": "A home backup battery of about 3.6 kWh that can add extra battery packs.",
     "why": "Two to three days of a newer fridge, or a fridge, freezer and medical device together.",
     "watch": "Heavy and expensive. At this size, compare it with a dual-fuel inverter generator run safely outdoors.",
     "best": "Long outages and medical needs"},
    {"name": "200 W portable solar panel (Renogy)", "asin": "B0CNPHD4VY", "price": "$150 to $300",
     "what": "A folding panel that recharges a power station in the sun.",
     "why": "Puts back roughly 400 to 700 Wh on a clear day, which turns a few days of phones, lights and CPAP into as long as the sun shines.",
     "watch": "Check that the connector and voltage match your station. Clouds and winter sun cut output a lot.",
     "best": "Outages longer than a day"},
]

FAQS = [
    ("How long will a 1,000 Wh power station last?",
     "It depends on what you plug in. At about 850 Wh usable, it charges a phone about 56 times, runs a router for about 2 days, a newer fridge for 15 to 20 hours, or a CPAP with the heat off for about 10 nights."),
    ("How do I calculate power station runtime?",
     "Multiply the station's rated watt-hours by 0.85 for inverter losses, then divide by the device's watts. A 1,000 Wh station running a 50 W fan: 1,000 × 0.85 ÷ 50 = about 17 hours."),
    ("What's the difference between watts and watt-hours?",
     "Watts measure how much power something uses at one moment. Watt-hours measure energy over time. A 50 W fan running for 10 hours uses 500 Wh."),
    ("Can a power station run a space heater?",
     "A big one can, but not for long: a 1,500 W heater empties a 1,000 Wh station in about half an hour. An electric blanket on low uses about 60 W and keeps you warm for many hours."),
    ("Why does my station run out sooner than the table says?",
     "Running several devices at once, cold temperatures, the inverter's own idle draw and an older battery all cut runtime. Turn off the AC output when you aren't using it."),
    ("Is a power station or a generator better?",
     "A power station is silent, has no fumes and is safe indoors, but it holds a fixed amount of energy. A generator runs as long as you have fuel, but it must run outdoors, at least 20 feet from doors and windows."),
]

SOURCES = [
    ("U.S. Department of Energy: Estimating appliance and home electronic energy use", "https://www.energy.gov/energysaver/articles/estimating-appliance-and-home-electronic-energy-use"),
    ("ENERGY STAR: Refrigerators", "https://www.energystar.gov/products/refrigerators"),
    ("ResMed battery guide (AirSense 10 power use by setting, PDF)", "https://cdn.shopify.com/s/files/1/2790/7304/files/ResMed_Battery_Guide_Converter.pdf"),
    ("Ready.gov: Power outages", "https://www.ready.gov/power-outages"),
    ("CDC: Avoiding carbon monoxide poisoning", "https://www.cdc.gov/natural-disasters/psa-toolkit/avoiding-carbon-monoxide-poisoning.html"),
]

RELATED = [("Power station calculator", "../power-calculator.html"), ("Backup power guide", "power.html"),
           ("What size power station runs a refrigerator", "power-station-for-refrigerator.html"),
           ("CPAP in a power outage", "cpap-power-outage.html"), ("Losing power in a winter storm", "winter-storm-power-outage.html")]
CALC_LINK = ("To add up your own devices and get a size, use the", "../power-calculator.html", "power station calculator")
