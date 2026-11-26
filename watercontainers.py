"""Buyer page: stackable water storage containers compared (/guides/water-storage-containers)."""

SLUG = "water-storage-containers"
PARENT = "water"
OG = "guide-water-containers"
OG_CARD = ("Water storage", "Water storage containers compared", "Stackable 5-gallon containers, water cans, collapsible jugs, barrels and bathtub liners: which to buy.")
TITLE = "Best Water Storage Containers for Emergencies: Stackable, Barrels and More"
META = ("Emergency water storage containers compared: stackable 5-gallon containers, water cans, collapsible jugs, 55-gallon barrels and "
        "bathtub liners. How much each holds and weighs, where it fits, and how to fill and rotate it.")
H1 = "Water storage containers, compared"
DEK = ("Stackable 5-gallon containers suit most homes, but they aren't the only option. Here's how each type compares on space, "
       "weight and cost, and how to fill them so the water stays safe.")
REVIEWED = "Ready.gov and CDC water storage guidance and manufacturer specifications"
CRUMB = "Water containers compared"

GRID_TOC = "Side by side"
GRID_LINK = "How much water you need"
GRID = ("Side by side",
        "Weights are for the water alone; add a few pounds for the container. Water weighs about 8.3 pounds a gallon.",
        ["Type", "Holds", "Weight full", "Stacks", "Best for", "Watch out"],
        [["Stackable 5-gallon containers", "5 gallons each", "About 42 lb", "Yes, flat tops and bottoms", "Most homes, closets and apartments", "Fill them where they'll live; stack only as high as the maker says"],
         ["5-gallon water can with a spout", "5 gallons", "About 42 lb", "No", "Pouring on a counter, car camping", "More floor space per gallon"],
         ["Collapsible jugs", "2 to 5 gallons", "Up to about 44 lb", "Loosely", "Small spaces, filling when a storm is forecast", "Less durable for years of storage"],
         ["55-gallon barrel", "55 gallons", "About 460 lb", "No", "Garages and houses on a slab", "Can't be moved once full; needs a pump and bung wrench"],
         ["Bathtub liner", "Up to about 100 gallons", "About 830 lb, in the tub", "No", "Hurricanes and other storms with warning", "Only useful with notice; the tub is out of use"],
         ["Store-bought gallon jugs", "1 gallon", "About 8 lb", "Not well", "Starting today with no tools", "Thin plastic can leak after a year or two"],
         ["Clean 2-liter soda bottles", "About half a gallon", "About 4.4 lb", "On their side", "Free storage, filling gaps", "Never use milk or juice jugs, which can't be cleaned well enough"]])

VERDICT = [
    ("For most homes, buy stackable 5-gallon containers.", "Four of them hold 20 gallons, about 10 days for two people, on roughly two square feet of floor. Add a spigot for easy pouring."),
    ("Store-bought water and clean soda bottles are a fine start.", "Ready.gov says commercially bottled water is the safest choice. Clean 2-liter soda bottles work for water you fill yourself; avoid milk and juice jugs."),
    ("A 55-gallon barrel is the cheapest per gallon, if you have the room.", "It's about 460 pounds full, so it belongs on a garage floor, on wood rather than bare concrete, and never upstairs."),
    ("Replace water you filled yourself about every 6 months.", "Ready.gov and the CDC recommend replacing stored tap water every 6 months. Keep store-bought water until its expiration date."),
    ("Keep containers cool, dark and away from chemicals.", "Heat and sunlight age plastic, and fumes from gasoline or pesticides can pass through it."),
]

STEPS_TITLE = "Filling and storing them"
STEPS = [
    ("Clean and sanitize", "Wash with soap and water and rinse. The CDC suggests sanitizing with a solution of 1 teaspoon of unscented bleach per quart of water, swished on all surfaces, then emptied."),
    ("Fill with tap water", "Treated tap water from a public system needs nothing added. If you're on a well, follow your health department's advice on treatment."),
    ("Label and date", "Write \"drinking water\" and the fill date on each container."),
    ("Store in the right place", "Somewhere cool and dark, off bare concrete, away from gasoline, paint and chemicals. Spread the weight in apartments."),
    ("Rotate every 6 months", "Use the water for plants or cleaning, then refill. A reminder on daylight saving time changes works well."),
    ("Keep a way to treat more", "Purification tablets or a filter let you make more water from other sources once your stored supply runs out."),
]

SECTIONS = [
    ("How much to store", [
        ("The minimum", "Ready.gov says at least one gallon per person per day for drinking and sanitation, for several days. Store more for hot weather, nursing mothers, children, people who are sick, and pets."),
        ("Two weeks", "For two weeks, that's 14 gallons per person: three stackable 5-gallon containers each."),
        ("Your household", "Our water storage calculator gives gallons, weight and the number of containers for your household."),
    ]),
]

PICKS = [
    {"name": "Stackable 5-gallon water containers (Saratoga Farms 4-pack)", "asin": "B092FYPZ55", "price": "$90 to $120 for 4",
     "what": "Four rigid, food-grade HDPE containers with flat tops and bottoms that stack.",
     "why": "Holds 20 gallons on a small footprint, and the handles make them easy to rotate.",
     "watch": "About 42 pounds each when full. A spigot makes pouring much easier; some kits include one.",
     "best": "Most homes, closets and apartments"},
    {"name": "Budget stackable containers (Hudson Exchange 4-pack)", "asin": "B07SK9FN9C", "price": "$40 to $70 for 4",
     "what": "Four plain 5-gallon HDPE containers with handles and caps, made to stack.",
     "why": "The same 20 gallons for less money, if you don't need extras.",
     "watch": "No spigot; plan to pour or siphon. Check the caps seal before storing.",
     "best": "Tight budgets"},
    {"name": "5-gallon water can with a spout", "asin": "B0D74164PZ", "asin_name": "Scepter Flow Control 5-gallon water can", "price": "$30 to $45",
     "what": "A rigid, leak-proof can with an adjustable flow-control spout.",
     "why": "Tough enough for years of storage and easy to pour from on a counter or tailgate.",
     "watch": "Doesn't stack, so it uses more floor space per gallon.",
     "best": "Kitchens, garages and car camping"},
    {"name": "Collapsible water containers", "asin": "B07FVJLYZ4", "asin_name": "WaterStorageCube collapsible containers (choose a size)", "price": "$12 to $30",
     "what": "Soft-sided jugs with a spigot that fold flat when empty.",
     "why": "Take almost no space until you fill them, which suits small apartments and storms with warning.",
     "watch": "Less durable than rigid containers for years of storage. Fill and check for leaks once before you need them.",
     "best": "Small spaces"},
    {"name": "55-gallon water barrel", "asin": "B06Y2H5GVX", "asin_name": "Augason Farms 55-gallon barrel", "price": "$100 to $200",
     "what": "A food-grade, BPA-free drum with two plugs for filling and drawing water.",
     "why": "The lowest cost per gallon: 55 days for one person in one footprint.",
     "watch": "About 460 pounds of water full. You'll need a bung wrench and a siphon pump, often sold separately.",
     "best": "Houses with a garage"},
    {"name": "Bathtub water liner (WaterBOB or similar)", "q": "waterbob bathtub emergency water storage", "price": "$25 to $45",
     "what": "A heavy plastic bag that lines the tub and holds up to about 100 gallons, with a hand pump.",
     "why": "Stores a lot of clean water in minutes when a storm is forecast, with nothing to store the rest of the year.",
     "watch": "Only useful with warning, and the tub is out of action while it's full.",
     "best": "Hurricane and winter storm areas"},
]

FAQS = [
    ("What is the best container for long-term water storage?",
     "Rigid, food-grade containers made for water, like stackable 5-gallon HDPE containers or a water barrel, kept cool and dark. Replace water you filled yourself about every 6 months."),
    ("Can I store water in milk jugs?",
     "No. Ready.gov advises against containers that held milk or fruit juice, because the protein and sugar can't be cleaned out well enough and bacteria can grow. Milk jugs also break down and leak."),
    ("Can I stack 5-gallon water containers?",
     "Containers made to stack have flat tops and bottoms; stack them only as high as the maker recommends, on a flat, solid floor. Round water cans and jugs aren't made to stack."),
    ("Is it safe to store water on a concrete floor?",
     "Many people put a board or pallet under containers and barrels on concrete, to keep them off the cold, damp surface and away from chemicals spilled in a garage."),
    ("How long does stored water last?",
     "Ready.gov says store-bought water can be kept until its expiration date, and water you filled yourself should be replaced every 6 months."),
]

SOURCES = [
    ("Ready.gov: Water", "https://www.ready.gov/water"),
    ("CDC: How to create an emergency water supply", "https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html"),
    ("USGS: Water density (weight per gallon)", "https://www.usgs.gov/special-topics/water-science-school/science/water-density"),
]

RELATED = [("Water storage calculator", "../water-calculator.html"), ("Emergency water guide", "water.html"),
           ("Water storage for apartments", "apartment-water-storage.html"), ("Sawyer Squeeze vs LifeStraw", "sawyer-squeeze-vs-lifestraw.html"),
           ("Drinking pool water", "pool-water.html")]
CALC_LINK = ("For gallons, weight and container counts for your household, use the", "../water-calculator.html", "water storage calculator")
