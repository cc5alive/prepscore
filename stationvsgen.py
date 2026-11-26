"""Buyer page: power station vs generator (/guides/power-station-vs-generator)."""

SLUG = "power-station-vs-generator"
PARENT = "power"
OG = "guide-station-vs-generator"
OG_CARD = ("Backup power", "Power station or generator?", "Which to buy for outages: indoor safety, runtime, fuel, noise and cost, side by side.")
TITLE = "Power Station vs Generator for Power Outages: Which Should You Buy?"
META = ("Power station vs generator for home backup: indoor safety, how long each runs a fridge, fuel and storage, noise, upkeep and cost, "
        "plus when to get both and how to run a generator safely.")
H1 = "Power station or generator?"
DEK = ("Both keep the lights, the fridge and your phones going when the grid goes down. They differ in where they can run, how long they "
       "last and what they need from you. Here's how to choose.")
REVIEWED = "CPSC, CDC and Washington State Department of Health generator guidance, Honda and Champion specifications"
CRUMB = "Power station vs generator"

GRID_TOC = "Side by side"
GRID = ("Side by side",
        "A typical 2,000 Wh power station compared with a typical 2,000 to 4,000 W inverter generator.",
        ["", "Power station", "Generator"],
        [["Where it can run", "Indoors, next to what it powers", "Outdoors only, at least 20 feet from doors, windows and vents"],
         ["Noise", "Silent, apart from a small fan", "About as loud as a conversation to a busy road, depending on size and load"],
         ["Runs a newer fridge for", "About 30 to 40 hours per charge", "As long as you have fuel; a small inverter generator burns about 3 gallons of gas a day at light load"],
         ["Big loads (microwave, well pump, space heater)", "Briefly, if the output rating covers them; they drain the battery fast", "Yes, within its running watts"],
         ["Refueling", "Recharge from the wall, a car or solar panels", "Gasoline or propane; gas goes stale in months without stabilizer"],
         ["Upkeep", "Charge it every few months", "Run it monthly, change the oil, keep fresh fuel"],
         ["Upfront cost", "About the same as a 4,000 W generator at 2,000 Wh; much less for a 300 to 1,000 Wh station", "About the same as a 2,000 Wh station, for far more power"],
         ["Biggest risk", "Little: keep it dry and charged", "Carbon monoxide poisoning if run too close to the house"]])

VERDICT = [
    ("In an apartment, or for outages of a day or two, get a power station.", "It's safe indoors, silent and needs no fuel. A 1,000 to 2,000 Wh station covers phones, lights, internet, a CPAP and a fridge for a day or more."),
    ("For long outages in a house with a yard, a generator goes further.", "It runs as long as you have fuel and handles big loads. A dual-fuel inverter generator with an automatic carbon monoxide shutoff is the safest kind to buy."),
    ("Many households do best with both.", "Run the generator outdoors during the day to keep the fridge cold and recharge the station; let the station run the CPAP, phones and lights quietly at night."),
    ("A generator must never run inside, even in a garage with the door open.", "The CPSC says nearly 100 people a year die from carbon monoxide from portable generators. Keep it at least 20 feet from the house and put battery CO alarms inside."),
    ("Never plug a generator into a wall outlet.", "This \"backfeeding\" can electrocute utility workers and neighbors. Plug appliances into the generator, or have an electrician install a transfer switch or interlock."),
]

STEPS_TITLE = "How to decide"
STEPS = [
    ("List what has to keep running", "Usually phones, lights, the fridge, internet and any medical device. Add a sump pump, well pump or furnace blower if you have one."),
    ("Add up the power", "Use the power station calculator to total watts and daily energy. Big motors and heaters push you toward a generator or a large home battery."),
    ("Check where you live", "No yard or balcony 20 feet from openings? A generator isn't an option; get a power station. Some generator models also aren't sold in California, so check the listing ships to you."),
    ("Think about outage length", "Outages of a day or two favor a power station. Multi-day storms and planned power shutoffs favor a generator, a station with solar, or both."),
    ("Plan fuel or charging", "For a generator, store fuel safely outside the house and rotate it. For a station, keep it charged and consider a folding solar panel."),
]

SECTIONS = [
    ("Running a generator safely", [
        ("Distance", "Outdoors only, at least 20 feet from the house, with the exhaust pointed away from doors, windows and vents. Never in a garage, basement, shed or under a carport."),
        ("Carbon monoxide alarms", "Put battery-powered CO alarms on every floor, near sleeping areas. Even at 20 feet, wind can carry exhaust inside."),
        ("Cords", "Use heavy-duty, outdoor-rated extension cords rated for the total load, with no cuts and all three prongs."),
        ("Weather", "Keep it dry: run it on a dry surface under an open, canopy-like cover, with a few feet of clear space all around, and touch it only with dry hands."),
        ("Refueling", "Turn it off and let it cool before adding fuel. Store gasoline in approved containers away from the house and any flame."),
        ("Connecting to the house", "The only safe way is a transfer switch or interlock installed by a licensed electrician. It also lets you run hardwired loads like a furnace blower."),
    ]),
]

PICKS = [
    {"name": "2 kWh power station (Jackery Explorer 2000 v2)", "asin": "B0DFG2WDQH", "price": "$900 to $1,500",
     "what": "A 2,042 Wh LiFePO4 station rated 2,200 W continuous and 4,400 W surge.",
     "why": "Runs a newer fridge for about 30 to 40 hours, or a CPAP for many nights, silently and safely indoors.",
     "watch": "About 40 pounds, and only 3 AC outlets. It won't run central air or electric heat.",
     "best": "Apartments and houses, outages of a day or two"},
    {"name": "1 kWh power station (Anker SOLIX C1000)", "asin": "B0C5C89QKZ", "price": "$400 to $900",
     "what": "A 1,056 Wh LiFePO4 station rated 1,800 W continuous, with 6 AC outlets.",
     "why": "The budget way to keep phones, lights, internet and a CPAP going, and a fridge for most of a day.",
     "watch": "Too small to carry a fridge through a long outage on its own.",
     "best": "Apartments, CPAP users and smaller budgets"},
    {"name": "Dual-fuel inverter generator (Champion 4000W or similar)", "asin": "B0D6SQR1L1", "asin_name": "Champion 4000W dual-fuel inverter with CO shutoff", "q": "dual fuel inverter generator co shutoff", "price": "$700 to $1,500",
     "what": "A 4,000-watt starting, 3,000-watt running inverter generator that runs on gasoline or propane, with an automatic CO shutoff.",
     "why": "Champion rates it for up to 10 hours on gasoline and up to 25 on propane. Propane stores for years without going stale.",
     "watch": "Outdoors only, 20 feet from the house. Stock often runs out before storms, and some models don't ship to California; buy early.",
     "best": "Houses with a yard and multi-day outages"},
    {"name": "Battery-powered CO alarm", "asin": "B004Y6V5CI", "asin_name": "Kidde battery CO alarm", "price": "$20 to $40",
     "what": "A carbon monoxide alarm that runs on batteries, so it works when the power is out.",
     "why": "The single most important item to buy with a generator, and worth having in any home with gas appliances.",
     "watch": "Plug-in alarms without a battery backup go dark in an outage. Test monthly.",
     "best": "Every floor of every home"},
    {"name": "200 W folding solar panel", "asin": "B0CNPHD4VY", "asin_name": "Renogy 200W portable panel", "price": "$150 to $400",
     "what": "A folding panel that plugs into most power stations.",
     "why": "Puts back roughly 400 to 700 Wh on a clear day, so a station keeps going through a multi-day outage with no fuel at all.",
     "watch": "Check that the plug and voltage match your station. Output drops in winter and cloudy weather.",
     "best": "Wildfire shutoffs and long outages"},
]

FAQS = [
    ("Can I run a generator in my garage with the door open?",
     "No. Health officials and the CPSC say never to run a portable generator in a garage, carport, basement or crawl space, even with ventilation; open doors and fans won't stop carbon monoxide from building up. Run it outdoors, at least 20 feet away."),
    ("Is a power station enough to back up a house?",
     "For essentials, yes: phones, lights, internet, a fridge and a medical device for a day or two. It won't run central air, an electric furnace or a well pump for long unless you buy a large home battery system with a transfer switch."),
    ("How much fuel does a generator use?",
     "It depends on the size and the load. Honda rates its small EU2200i for 8.1 hours on less than a gallon at a quarter load, which works out to about 3 gallons a day. Larger generators under heavier loads use more."),
    ("Can a generator recharge a power station?",
     "Yes. Plug the station's charger into the generator. An inverter generator gives clean power that's safe for electronics. It's a good way to run the generator only a few hours a day."),
    ("Which is cheaper?",
     "Upfront, a 4,000 W generator costs about the same as a 2,000 Wh power station and does much more. Over years, the station needs no fuel or oil, and solar can recharge it for free."),
    ("What is backfeeding?",
     "Plugging a generator into a wall outlet to power the house. It can send electricity back into the power lines and electrocute utility workers or neighbors. Use a transfer switch or interlock installed by an electrician."),
]

SOURCES = [
    ("CPSC: Portable generator carbon monoxide deaths and safety tips", "https://www.cpsc.gov/Newsroom/News-Releases/2024/As-Winter-Storms-Continue-CPSC-Urges-Families-to-Take-Steps-to-Prevent-Carbon-Monoxide-Poisoning-and-Fires"),
    ("CDC: Generator safety during a power outage", "https://www.cdc.gov/carbon-monoxide/factsheets/generator-safety-fact-sheet.html"),
    ("Washington State Department of Health: Generator use during a power outage (PDF)", "https://doh.wa.gov/sites/default/files/legacy/Documents/Pubs/821-034_GeneratorUse_LT.pdf"),
    ("Honda EU2200i specifications", "https://powerequipment.honda.com/Generators/models/eu2200i"),
    ("Electrical Safety Foundation: Use backup power safely", "https://esfi.org/generator-safety"),
]

RELATED = [("Power station calculator", "../power-calculator.html"), ("Backup power guide", "power.html"),
           ("How long a power station lasts", "power-station-runtime.html"), ("Power station for a fridge", "power-station-for-refrigerator.html"),
           ("Losing power in a winter storm", "winter-storm-power-outage.html")]
CALC_LINK = ("To size a power station for what you want to run, use the", "../power-calculator.html", "power station calculator")
