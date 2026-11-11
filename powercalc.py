"""Power station size calculator: devices, FAQ and sources.

Each device: id, name, hint, run watts (while on), Wh per unit of use, unit, default use, default qty, surge watts.
unit: "h" hours a day (editable), "chg" charges a day (editable), "night" once a night (fixed), "day" all day (fixed).
Figures are typical values; the page tells people to check their own labels.
"""

DEVICES = [
    ("phone", "Phone", "About 15 Wh per full charge", 20, 15, "chg", 1, 2, 0),
    ("laptop", "Laptop", "About 50 W while in use", 50, 50, "h", 3, 0, 0),
    ("router", "Wi-Fi router and modem", "About 15 W together, on all day", 15, 15, "h", 24, 1, 0),
    ("light", "LED bulb or lantern", "About 9 W, as bright as an old 60 W bulb", 9, 9, "h", 5, 2, 0),
    ("fan", "Box fan", "About 50 W on medium", 50, 50, "h", 8, 0, 0),
    ("tv", "TV", "About 80 W for a 50-inch LED", 80, 80, "h", 3, 0, 0),
    ("cpap", "CPAP, humidifier and heated tube off", "About 85 Wh a night", 60, 85, "night", 1, 0, 0),
    ("cpaph", "CPAP with heated humidifier and tube", "About 400 Wh a night", 120, 400, "night", 1, 0, 0),
    ("fridge", "Refrigerator", "About 1.5 kWh a day; surges when the compressor starts", 150, 1500, "day", 1, 0, 1200),
    ("freezer", "Chest freezer", "About 0.8 kWh a day; surges when it starts", 100, 800, "day", 1, 0, 800),
    ("blanket", "Electric blanket", "About 60 W on low to medium", 60, 60, "h", 8, 0, 0),
    ("micro", "Microwave (compact)", "About 1,200 W from the outlet while running", 1200, 1200, "h", 0.2, 0, 0),
    ("sump", "Sump pump (1/3 hp)", "About 800 W while pumping; large surge at start", 800, 800, "h", 1, 0, 2400),
]

UNIT_LABEL = {"h": "hours a day", "chg": "charges a day", "night": "each night", "day": "runs all day"}

FAQ = [
    ("What size power station do I need?",
     "Add up the watt-hours your devices use in a day (watts × hours), divide by 0.85 for the energy lost converting battery power to AC, and multiply by the number of days you want to cover without recharging. Add about 20% so you aren't running the battery to empty. Then check that the station's output in watts covers everything you'll run at once, and its surge rating covers anything with a motor."),
    ("How long will a 1,000 Wh power station last?",
     "About 850 Wh is usable through the AC outlets. That's roughly a day and a half of phones, a router and two LED lights (about 480 Wh a day), 9 to 11 nights of a CPAP with the humidifier off, or 12 to 14 hours of a typical refrigerator."),
    ("Can a power station run a refrigerator?",
     "Yes, if its surge rating covers the compressor's start, which most 1,000 Wh stations do. A typical fridge uses 1 to 2 kWh a day, so a 1,000 Wh station keeps it going for about half a day. Keep the door closed: the USDA says a closed fridge keeps food safe for about 4 hours without power, and a full freezer about 48 hours. You can also run the fridge for an hour or two at a time to stretch the battery."),
    ("Can I run a space heater on a power station?",
     "Not for long. A space heater draws about 1,500 W, so a 1,000 Wh station runs it for under 40 minutes. For warmth in a winter outage, an electric blanket at about 60 W runs all night on a mid-size station, and warm sleeping bags need no power at all."),
    ("What's the difference between watts and watt-hours?",
     "Watts are how much power a device draws at a moment; watt-hours are how much energy it uses over time. A 50 W fan running for 8 hours uses 400 Wh. A power station's capacity is in watt-hours; its output limit is in watts. You need enough of both."),
    ("How do I find out how much power my device uses?",
     "Look for watts (W) on the label or power adapter. For a fridge or freezer, the yellow EnergyGuide label gives kWh per year: divide by 365 for a day. A plug-in electricity meter measures real use, which is often lower than the label. CPAP makers publish power figures in the manual or battery guide."),
    ("Is solar worth adding?",
     "For outages longer than a day or two, yes. A 200 W folding panel typically puts back about 400 to 700 Wh on a clear day, depending on the season and the angle. That can keep phones, lights, a router and a CPAP going indefinitely, but it won't keep up with a fridge plus everything else."),
]

SOURCES = [
    ("U.S. Department of Energy: Estimating appliance and home electronic energy use", "https://www.energy.gov/energysaver/articles/estimating-appliance-and-home-electronic-energy-use"),
    ("Ready.gov: Power outages", "https://www.ready.gov/power-outages"),
    ("USDA: Keep your food safe during emergencies", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies"),
    ("ResMed battery guide (AirSense 10 power use by setting, PDF)", "https://cdn.shopify.com/s/files/1/2790/7304/files/ResMed_Battery_Guide_Converter.pdf"),
]
