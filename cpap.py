"""CPAP in a power outage: buyer page content (/guides/cpap-power-outage)."""

TITLE = "Best Power Station for a CPAP in a Power Outage (With Runtime Table)"
META = ("How long will a power station run your CPAP? Runtime by setting for 300 to 2,000 Wh stations, which size to buy, "
        "why to turn off the humidifier, and how to set it up before an outage.")
H1 = "Keeping a CPAP running in a power outage"
DEK = ("Turn off the heat, use the right cable, and a mid-size power station runs most CPAPs for a week or more. "
       "Here's the math by setting, what to buy, and how to set it up before you need it.")

VERDICT = [
    ("Turn off the humidifier and heated tube.", "With heat off, ResMed's figures put an AirSense 10 at about 80 to 90 Wh a night. With the humidifier and heated tube on, it's 340 to 470 Wh: four to five times as much."),
    ("A 1,000 Wh power station is the sweet spot.", "About 9 to 11 nights with heat off, or 1 to 2 with full heat, and it can also run a fridge for half a day or keep phones and lights going."),
    ("A 500 Wh station covers about 5 nights", "with heat off. It's lighter and cheaper if the CPAP is all you need to power."),
    ("Use the maker's DC cable or converter if there is one.", "Plugging into the station's DC port skips the energy lost converting battery power to AC and back. Buy it from your CPAP maker or supplier, matched to your exact model."),
    ("Tell your utility and your equipment supplier.", "Many utilities have a medical or life-support customer program with advance notice of planned shutoffs; in California it's called Medical Baseline. Ask your supplier what they recommend for backup power."),
]

# ResMed battery guide, AirSense 10, pressures 8 to 10 cmH2O, 12 V DC through ResMed's converter (Wh per 8-hour night,
# current x 12 V x 8 h, without the guide's 50% safety margin).
SETTINGS = [
    ("Humidifier off, standard tube", 76, 89),
    ("Humidifier off, heated tube on", 115, 146),
    ("Humidifier on (medium), standard tube", 192, 221),
    ("Humidifier and heated tube on", 341, 472),
]
STATIONS = [300, 500, 1000, 2000]

PICKS = [
    {"name": "Mid-size LiFePO4 power station, about 1,000 Wh", "asin": "B0C5C89QKZ", "asin_name": "Anker SOLIX C1000", "price": "$400 to $900",
     "what": "A silent battery with AC outlets, a 12 V car-style port and USB, rechargeable from the wall, a car or solar.",
     "why": "About 850 Wh usable: 9 to 11 nights of CPAP with heat off, and enough left over for a fridge, phones or a fan in a short outage.",
     "watch": "Check that your CPAP's DC cable matches the station's 12 V port. LiFePO4 chemistry lasts thousands of cycles.",
     "best": "Most CPAP users, apartments, outages of a few days"},
    {"name": "Small power station, about 500 Wh", "q": "500wh lifepo4 portable power station", "price": "$200 to $450",
     "what": "A lighter station, usually under 15 pounds, with AC and 12 V outputs.",
     "why": "About 5 nights of CPAP with heat off, at roughly half the weight and cost of a 1,000 Wh station.",
     "watch": "Compare usable capacity, not just the number in the name, and check for pure sine wave AC and a 12 V port.",
     "best": "CPAP only, short outages, camping and travel by car"},
    {"name": "100 to 200 W folding solar panel", "asin": "B0CNPHD4VY", "asin_name": "Renogy 200W portable panel", "price": "$150 to $400",
     "what": "A portable panel that recharges a power station during the day.",
     "why": "On a clear day a 200 W panel puts back roughly 400 to 700 Wh, several nights of CPAP with heat off. It turns a few nights into as long as the sun shines.",
     "watch": "Real output is well under the rated watts with clouds, heat or a low winter sun. Match the connector to your station.",
     "best": "Wildfire shutoffs, hurricanes and long outages"},
]

DC_NOTE = ("Most CPAP makers sell a DC power cord or converter for their machines (ResMed, for example, sells one for the AirSense line). "
           "It lets you plug into a power station's 12 V port or a car outlet without going through the station's AC inverter, which stretches runtime. "
           "Buy it from your CPAP maker or equipment supplier so it matches your exact model. We don't link one, because the wrong cable can damage the machine.")

SETUP = [
    ("Charge it now, then every few months", "Power stations slowly lose charge in storage. Put a reminder on your calendar to top it up when the clocks change."),
    ("Test one night before you need it", "Run your CPAP from the station on a normal night and note the battery percentage in the morning. That's your real nightly use at your pressure."),
    ("Turn off the heat in your machine's settings", "Set the humidifier and heated tube to off (your manual shows how). Some machines need the water tub or an end cap in place to run without humidity; check the manual."),
    ("Plug into DC if you can", "Use your maker's DC cable in the station's 12 V port. If you use the AC outlet, plug in the CPAP's normal power supply, and switch the station's AC output off in the morning: the inverter uses power even with nothing running."),
    ("Recharge during the day", "From a wall outlet if power is back anywhere you can reach, from a car's 12 V outlet while driving, or from a solar panel in the sun."),
    ("Keep it ventilated", "A lithium power station is safe in a bedroom with no fumes. Don't cover it or put it on bedding. Never run a gas generator indoors or in a garage, even with the door open."),
]

FAQS = [
    ("How long will a 1,000 Wh power station run a CPAP?",
     "About 9 to 11 nights with the humidifier and heated tube off, based on ResMed's figures for the AirSense 10 at 8 to 10 cmH2O and about 850 Wh usable. With the humidifier and heated tube on, 1 to 2 nights. Higher pressures and other machines differ, so test yours."),
    ("Do I need a pure sine wave power station for a CPAP?",
     "Use pure sine wave AC for medical devices. Nearly all lithium power stations sold today put out pure sine wave AC, but check the spec sheet, especially on cheap car inverters."),
    ("Can I run my CPAP from my car?",
     "With your maker's DC cord, yes, from the 12 V outlet while the engine is running. Run the car outdoors only, never in a garage, and don't run a car battery down overnight with the engine off: it may not start in the morning."),
    ("Is it safe to skip the humidifier for a few nights?",
     "For most people it's fine for a short outage, though you may wake with a dry nose or mouth. If you have a medical reason to use humidity, or can't go without your CPAP, ask your doctor what to do in an outage."),
    ("What about a CPAP travel battery?",
     "Batteries made for a specific CPAP, such as those from Medistrom or the CPAP maker, are small and often under 100 Wh, so they're allowed in carry-on bags on most flights. They usually last one night with heat off. Good for travel; too small for a multi-day outage."),
    ("What if I use an oxygen concentrator or a ventilator?",
     "Those draw far more power than a CPAP, and some are life support. Talk to your doctor and equipment supplier about backup oxygen cylinders or batteries, register with your utility's medical program, and know where you'll go if the power stays out."),
]

SOURCES = [
    ("ResMed battery guide (AirSense 10 power use by setting, PDF)", "https://cdn.shopify.com/s/files/1/2790/7304/files/ResMed_Battery_Guide_Converter.pdf"),
    ("FDA: Tips about medical devices and natural disasters", "https://www.fda.gov/medical-devices/emergency-situations-medical-devices/fda-offers-tips-about-medical-devices-and-natural-disasters"),
    ("ASPR TRACIE: Preparing medical devices that need electricity for power outages", "https://asprtracie.hhs.gov/technical-resources/resource/4139/home-use-devices-how-to-prepare-for-and-handle-power-outages-for-medical-devices-that-require-electricity"),
    ("California Public Utilities Commission: Medical Baseline fact sheet (PDF)", "https://www.cpuc.ca.gov/-/media/cpuc-website/about-cpuc/documents/transparency-and-reporting/fact_sheets/medical_baseline_101921.pdf"),
    ("Ready.gov: Power outages", "https://www.ready.gov/power-outages"),
]
