"""Buyer page: emergency water storage for apartments (/guides/apartment-water-storage)."""

SLUG = "apartment-water-storage"
PARENT = "water"
OG = "guide-apt-water"
OG_CARD = ("Water for small spaces", "Apartment water storage", "How much you need, which containers fit, and where to put 200+ pounds of water.")
TITLE = "Emergency Water Storage for Apartments: What to Buy and Where to Put It"
META = ("How to store two weeks of emergency water in a small apartment: how much you need, which containers fit, "
        "where to put 200+ pounds of water, and what to do when it runs out.")
H1 = "Storing emergency water in an apartment"
DEK = ("Two weeks of water for two people is 28 gallons and about 230 pounds. Here's how to fit it into closets and under beds, "
       "which containers work best in small spaces, and how to stretch it when it runs out.")
REVIEWED = "Ready.gov and CDC guidance"
CRUMB = "Apartment water"

VERDICT = [
    ("Plan on 1 gallon per person per day.", "Start with 3 days, then build to two weeks: 14 gallons per person. The water calculator does the math for your household, pets included."),
    ("Use 5- to 7-gallon containers, not barrels.", "They fit in closets and under beds, and you can still lift one full (about 40 to 60 pounds). A full 55-gallon barrel weighs about 460 pounds and belongs on a ground floor or concrete slab."),
    ("Spread the weight around.", "A few containers in each closet is easier on floors, and on you, than a wall of water in one corner."),
    ("Add a filter and tablets for when storage runs out.", "A squeeze filter plus purification tablets turns tap water under a boil-water notice, or water from a bathtub you filled before a storm, into drinking water."),
    ("Fill the bathtub when a storm is coming.", "That's your washing and flushing water. A tub liner keeps it cleaner and easier to scoop."),
]

# Table: space and weight for two weeks, by household size (same assumptions as the water calculator)
TABLE_TITLE = "How much space and weight two weeks takes"
TABLE_NOTE = ("1 gallon per person per day; water weighs 8.34 pounds a gallon; stacked 5-gallon containers take roughly 2 square feet of floor per 20 gallons. "
              "Pets and hot weather add more.")

PICKS = [
    {"name": "Stackable 5-gallon water containers (Saratoga Farms 4-pack)", "asin": "B092FYPZ55", "price": "$90 to $120 for 4",
     "what": "Rigid, food-grade 5-gallon containers that stack in a closet.",
     "why": "The tidiest way to keep 20 gallons in about 2 square feet of floor. Each one weighs about 42 pounds full, so you can still move it.",
     "watch": "Stack no higher than the maker recommends, on a flat floor, away from heat and sunlight.",
     "best": "Long-term storage in a closet"},
    {"name": "Collapsible water jugs (WaterStorageCube 5.3 gal)", "asin": "B07FVJLYZ4", "price": "$12 to $20 each",
     "what": "Soft-sided cubes with a spigot that fold flat when empty.",
     "why": "Store a few flat under the bed and fill them from the tap when a storm or shutoff is forecast. Cheap way to add 20 gallons on short notice.",
     "watch": "Less durable than rigid containers for years of storage. Fill and check for leaks once before you need them.",
     "best": "Tight spaces, storms you see coming"},
    {"name": "Reliance 7-gallon water jug", "asin": "B09NP5538N", "asin_name": "Reliance Jumbo-Tainer 2.0, 7 gal", "price": "$30 to $45",
     "what": "A rigid 7-gallon jug with a spigot.",
     "why": "Fewer containers for the same water: four of them hold two weeks for two people.",
     "watch": "About 58 pounds full, which is heavy to lift onto a counter. Keep it on the floor and pour from the spigot.",
     "best": "Households that want fewer, bigger jugs"},
    {"name": "Bathtub water liner (WaterBOB or similar)", "q": "waterbob bathtub emergency water storage", "price": "$25 to $45",
     "what": "A heavy plastic bag that lines the tub and holds up to about 100 gallons, with a hand pump.",
     "why": "Turns the bathtub into a large, covered reservoir in about 20 minutes when a hurricane, freeze or water shutoff is coming.",
     "watch": "Only useful with warning, and the tub is out of action while it's full. Treat the water before drinking.",
     "best": "Hurricane, ice storm and shutoff areas"},
    {"name": "Sawyer Squeeze filter", "asin": "B00B1OSU4W", "price": "$35 to $50",
     "what": "A small filter that screws onto a pouch or bottle.",
     "why": "Removes bacteria and parasites from tap or tub water when your stored water runs low. Small enough for a kitchen drawer.",
     "watch": "It doesn't remove viruses or chemicals. Pair it with tablets, and don't use it on water that may have chemicals or fuel in it.",
     "best": "Backup for when storage runs out"},
    {"name": "Aquatabs or Katadyn Micropur tablets", "asin": "B09B2TVKGB", "asin_name": "Aquatabs 49mg, 100-pack", "price": "$10 to $25",
     "what": "Purification tablets that disinfect water.",
     "why": "Handle the viruses a filter can't. A 100-pack takes almost no space and treats a lot of water.",
     "watch": "Follow the wait time on the label, longer for cold or cloudy water.",
     "best": "Every apartment, with or without a filter"},
]

SECTIONS = [
    ("Where to put it", [
        ("Closet floors", "The best spot: dark, cool and out of the way. Put a towel or tray under containers on carpet in case of a leak."),
        ("Under beds", "Collapsible cubes stored flat, or low rigid containers on their side if they're rated for it."),
        ("Behind the couch or in a cabinet", "Any dark spot works. Spreading containers around keeps any one spot from carrying too much weight."),
        ("Not on the balcony", "Sun and heat grow algae and break down plastic, and water can freeze and split containers."),
        ("Not next to cleaning chemicals", "Plastic can absorb fumes. Keep water away from bleach, paint and fuel."),
    ]),
    ("Keep it fresh", [
        ("Store-bought bottled water", "Keep it sealed and follow the date on the label."),
        ("Water you bottle yourself", "Replace it every six months. Write the date on each container."),
        ("Clean containers before filling", "Wash with soap, rinse, then sanitize with a teaspoon of unscented bleach per quart of water and rinse again, as the CDC describes."),
        ("Skip milk and juice jugs", "They're hard to clean and break down over time. Use food-grade water containers."),
    ]),
    ("When the stored water runs out", [
        ("Your water heater", "Most hold 40 to 50 gallons. Turn off the power or gas and the cold-water supply first, let it cool, then drain from the valve at the bottom. In an apartment, ask the building manager where yours is."),
        ("Ice cubes and pipes", "Melt the ice. Open the highest faucet, then catch what's left in the pipes from the lowest one."),
        ("The toilet tank, not the bowl", "Usable for washing or, treated, as a last resort, unless you use colored tank-cleaning tablets."),
        ("Treat anything else", "Filter cloudy water, then disinfect with tablets, bleach or boiling. The water guide has the steps."),
    ]),
]

FAQS = [
    ("How much water should I store in an apartment?",
     "At least 3 gallons per person for 3 days, and ideally 14 gallons per person for two weeks. That's 28 gallons and about 230 pounds for two people. Add water for pets and hot weather."),
    ("Can my floor hold that much water?",
     "Spread across a few closets in 5- to 7-gallon containers, two weeks of water is like a few pieces of heavy furniture. A full 55-gallon barrel is different: about 460 pounds on a few square feet. Keep barrels on a ground floor or concrete slab, and ask your building manager before putting one on an upper floor."),
    ("Can I store water on my balcony?",
     "It's not a good idea. Sun and heat encourage algae and break down plastic, and water that freezes can split containers. A closet is better."),
    ("What's the cheapest way to start?",
     "A few cases of bottled water from the grocery store. A 24-pack of half-liter bottles is about 3 gallons, enough for one person for three days, and stacks neatly in a closet."),
    ("How long does stored water last?",
     "Store-bought bottled water lasts until the date on the label if it stays sealed. Water you bottle yourself from the tap should be replaced every six months."),
]

SOURCES = [
    ("Ready.gov: Water", "https://www.ready.gov/water"),
    ("CDC: Creating and storing an emergency water supply", "https://www.cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html"),
]

RELATED = [("Water storage calculator", "../water-calculator.html"), ("Water storage and filters guide", "water.html"),
           ("Drinking pool water", "pool-water.html"), ("LA renter checklist", "../la-renters.html"), ("Food storage calculator", "../food-calculator.html")]
CALC_LINK = ("For your household's exact amounts, use the", "../water-calculator.html", "water storage calculator")
