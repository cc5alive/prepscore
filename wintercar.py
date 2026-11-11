"""Buyer page: stranded in a car in winter (/guides/stranded-in-car-winter)."""

SLUG = "stranded-in-car-winter"
PARENT = "car"
OG = "guide-winter-car"
OG_CARD = ("Winter driving", "Stuck in your car in snow", "What to do from the first minute, and the winter extras that make a long night bearable.")
TITLE = "Stranded in Your Car in a Snowstorm: What to Do and What to Keep in the Car"
META = ("What to do if you're stuck in your car in winter: staying warm, avoiding carbon monoxide, getting found, "
        "how much gas idling uses, and the winter extras to keep in your car kit.")
H1 = "Stuck in your car in a snowstorm"
DEK = ("Stay with the car, keep the tailpipe clear, and run the engine about 10 minutes an hour. Here's what to do from the first minute, "
       "and the few winter extras that turn a long night into an inconvenience.")
REVIEWED = "National Weather Service, Ready.gov, CDC and Department of Energy guidance"
CRUMB = "Stuck in snow"

VERDICT = [
    ("Stay with the car.", "It's shelter, and it's much easier for rescuers to find than a person walking in a storm."),
    ("Keep the tailpipe clear of snow.", "A blocked exhaust can fill the car with carbon monoxide, which you can't see or smell. Check it every time before you run the engine."),
    ("Run the engine about 10 minutes each hour, with a window cracked.", "That's the National Weather Service's advice: enough heat to stay safe, while saving fuel and letting fresh air in."),
    ("Make the car easy to see.", "Turn on the dome light at night while the engine runs, tie a bright cloth to the antenna or door, and raise the hood once the snow stops."),
    ("Keep at least half a tank in winter.", "Idling uses about 0.2 to 0.5 gallons an hour, so 10 minutes an hour burns only about 1 to 2 gallons a day."),
]

STEPS_TITLE = "What to do, step by step"
STEPS = [
    ("Get safe and call", "Pull as far off the road as you can and turn on your hazard lights. Call 911 if anyone is in danger, or roadside assistance if not, and say where you are: road, direction, nearest exit or mile marker."),
    ("Save your phone", "Turn the brightness down and close apps. Keep the phone in an inside pocket; cold drains batteries fast. Charge it while the engine runs."),
    ("Clear the tailpipe, then warm up in bursts", "Run the engine about 10 minutes each hour with a downwind window cracked. Recheck the tailpipe each time, especially if snow is still falling or drifting."),
    ("Layer up and stay dry", "Put on the hat, gloves and extra socks. Wrap in the blanket, with a Mylar blanket inside it to hold heat. Huddle together. Avoid sweating: damp clothes chill you."),
    ("Keep moving a little", "Clap, flex your fingers and toes, and move your arms and legs to keep blood flowing. Don't stay in one cramped position for hours."),
    ("Eat and drink", "Snack regularly; your body burns fuel to stay warm. Drink water. If you have to use snow, melt it first rather than eating it."),
    ("Take turns sleeping", "If there's more than one of you, keep one person awake to watch the tailpipe, the fuel and anyone showing signs of hypothermia: intense shivering, confusion, slurred speech or drowsiness."),
]

PICKS = [
    {"name": "Arcturus military wool blanket", "asin": "B01IJWUYLK", "price": "$40 to $50",
     "what": "A heavy wool blanket that lives in the trunk.",
     "why": "Wool keeps you warm even when damp from melting snow, and it's tough enough to kneel on while you dig.",
     "watch": "One per person on long winter trips, or add a sleeping bag for mountain passes.",
     "best": "Every car in a cold climate"},
    {"name": "Mylar emergency blankets, 10-pack", "asin": "B00DZ1NFSK", "asin_name": "Primacare 10-pack", "price": "$10 to $15 for a 10-pack",
     "what": "Foil blankets that reflect body heat.",
     "why": "Inside a wool blanket, they cut heat loss. They also make a bright signal on the snow.",
     "watch": "They tear easily and don't insulate on their own. Use them with a blanket, not instead of one.",
     "best": "Glovebox and go-bags"},
    {"name": "Air-activated hand and toe warmers", "q": "hothands hand warmers 40 pairs", "asin_name": "Amazon search results for HotHands", "price": "$15 to $35",
     "what": "Disposable packets that heat up for hours once opened.",
     "why": "Warm hands and feet without running the engine. Put them in pockets, gloves or around your core.",
     "watch": "Don't put them directly on skin for long, and keep them away from small children.",
     "best": "Long nights, kids, people who run cold"},
    {"name": "Collapsible snow shovel", "asin": "B07HDZW7YQ", "asin_name": "Yukon Charlie's collapsible shovel", "price": "$20 to $50",
     "what": "A packable shovel that fits in the trunk.",
     "why": "Clears the tailpipe and digs out the wheels. A car stuck in a plowed berm is often free in 15 minutes.",
     "watch": "Pace yourself. Shoveling is hard work in the cold; rest before you sweat.",
     "best": "Anywhere it snows"},
    {"name": "NOCO Boost GB40 jump starter", "asin": "B015TKUPIC", "price": "$90 to $120",
     "what": "A compact lithium battery that starts a car with a dead battery.",
     "why": "Cold weakens car batteries, and running the engine in bursts all night is hard on them. This starts the car without another driver.",
     "watch": "Recharge it every few months; cold drains it too.",
     "best": "Every driver in a cold climate"},
    {"name": "LED road flares", "asin": "B07K3YFMVH", "asin_name": "Tobfit 6-pack LED flares (batteries not included)", "price": "$15 to $40",
     "what": "Bright, flashing battery flares.",
     "why": "Make you visible to plows and rescuers without the fire risk of road flares.",
     "watch": "Add batteries and keep spares. Lithium batteries handle cold better.",
     "best": "Rural roads and highways"},
    {"name": "S.O.S. Rations 3600 emergency food bars", "asin": "B075TXP1P5", "price": "$10 to $20 per 3,600 kcal pack",
     "what": "Dense, sealed food bars built to survive heat and cold in a car.",
     "why": "Calories keep you warm, and these won't freeze solid or spoil in the trunk.",
     "watch": "Check the date printed on the package and replace as needed.",
     "best": "Long commutes and road trips"},
]

CHECKLIST_TITLE = "Winter car checklist"
CHECKLIST = [
    "Half a tank of gas or more", "Wool blanket or sleeping bag", "Mylar blankets", "Hat, gloves, warm socks and winter boots",
    "Hand and toe warmers", "Collapsible shovel", "Ice scraper and snow brush", "Cat litter or sand for traction",
    "Jump starter or jumper cables", "Phone charger and power bank", "Headlamp or flashlight", "LED flares or reflective triangles",
    "Bright cloth for the antenna", "Water in an insulated bottle", "High-calorie snacks or ration bars", "First aid kit",
    "Washer fluid rated for freezing", "A day of any prescription medicines",
]
CHECKLIST_NOTE = "This adds winter extras to our year-round car kit. The car guide covers the rest: tire inflator, tow strap, tools and more."

FAQS = [
    ("Should I leave my car and walk for help?",
     "Usually not. The car is shelter and easier to spot than a person. Leave only if you can see help close by and the weather allows, and tell someone where you're going."),
    ("How long should I run the engine when I'm stuck?",
     "About 10 minutes each hour, with a window slightly open and the tailpipe clear of snow, according to the National Weather Service. Turn on the dome light while it runs so you're easier to see at night."),
    ("How much gas does idling use?",
     "The Department of Energy puts idling at about 0.2 to 0.5 gallons an hour for passenger vehicles. At 10 minutes an hour, that's roughly 1 to 2 gallons a day, so half a tank lasts days."),
    ("Is it safe to sleep in the car with the engine running?",
     "No. If snow blocks the tailpipe, carbon monoxide can build up while you sleep. Run the engine in short bursts, keep a window cracked, and keep someone awake to check the tailpipe."),
    ("What about an electric car?",
     "An EV makes no exhaust, so carbon monoxide from the car isn't a risk, and climate control draws from the battery. Use seat heaters and a lower cabin temperature to stretch range, and charge fully before driving into a winter storm."),
]

SOURCES = [
    ("National Weather Service: Winter safety (PDF)", "https://www.weather.gov/media/twc/WinterSafety-OnePager-2-27-19.pdf"),
    ("Ready.gov: #WinterReady", "https://www.ready.gov/winter-ready"),
    ("Ready.gov: Car safety", "https://www.ready.gov/car"),
    ("CDC: Avoiding carbon monoxide poisoning", "https://www.cdc.gov/natural-disasters/psa-toolkit/avoiding-carbon-monoxide-poisoning.html"),
    ("U.S. Department of Energy: Idling and fuel use (PDF)", "https://afdc.energy.gov/files/u/publication/which_is_greener.pdf"),
]

RELATED = [("Car emergency kit guide", "car.html"), ("Staying warm without power", "light-heat.html"),
           ("Radios and communication", "radios.html"), ("Preparedness gift guide", "../preparedness-gifts.html")]
