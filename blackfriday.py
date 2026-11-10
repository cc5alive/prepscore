"""Content for /black-friday: prep gear worth buying on sale, all linked to specific, verified Amazon products."""

CHECKED = "November 1, 2026"   # the date products were last checked as available
# Prices are shown only as bands ($ to $$$$); Amazon only allows prices pulled live from its API.
TITLE = "Black Friday Emergency Prep Deals 2026: Gear Worth Buying"
META = ("The emergency gear worth buying on Black Friday and Cyber Monday 2026: the essentials to get first, big-ticket items "
        "worth waiting for, small gifts, and how to tell a real deal from a fake one.")
H1 = "Black Friday prep gear worth buying"
DEK = ("Sales are a good time to fill the gaps in your kit. Here's what to buy first, what's worth waiting for, and how to "
       "tell a real deal from a fake one.")

DATES = [("Black Friday", "Fri, Nov 27"), ("Cyber Monday", "Mon, Nov 30"), ("Picks checked", "Nov 1")]

TIPS = [
    ("Buy the essentials first.", "A power station on sale won't help if you have no water. Work down the list in order."),
    ("Check the price history.", "A big “was” price doesn't mean much. Free price-history tools like Keepa or camelcamelcamel show whether a sale price is a true low or the usual price dressed up."),
    ("Check who's selling it.", "Look for “ships from and sold by Amazon” or the brand's own store, especially for first-aid and safety gear."),
    ("Skip padded survival bundles.", "Many kits inflate their item counts with filler. Buying the pieces below usually gets you better gear."),
]

# product: (name, asin, price_seen, why, best_for, guide_slug)
ESSENTIALS = [
    ("Saratoga Farms 5-gallon stackable water containers, 4-pack", "B092FYPZ55", "$119.98",
     "20 gallons in one closet corner: about 10 days of drinking water for two people.", "Every home", "water"),
    ("Sawyer Squeeze water filter", "B00B1OSU4W", "$45.95",
     "Makes creek, lake or rain-barrel water safe from bacteria and parasites once your stored water runs out.", "Backup water and go-bags", "water"),
    ("Anker SOLIX C1000 power station (1,056 Wh)", "B0C5C89QKZ", "$499.99",
     "Quiet, indoor-safe power for phones, lights, a CPAP or a fridge for hours. Power stations are often among the biggest Black Friday discounts.", "Outages and medical devices", "power"),
    ("Anker 20,000 mAh power bank", "B0CXDXP8VR", "$59.99",
     "Several full phone charges with no outlet. The cheapest way to stay reachable in an outage.", "Everyone", "power"),
    ("Midland ER310 crank and solar emergency radio", "B015QIC1PW", "$79.99",
     "NOAA weather alerts and AM/FM news when cell networks are down, charged by hand or sun.", "Every home", "radios"),
    ("Black Diamond Spot 400-R rechargeable headlamp", "B09NQK87MN", "$57.88",
     "Hands-free light that's far safer than candles. One per person.", "Every person in the house", "light-heat"),
    ("Adventure Medical Kits family first-aid kit", "B0079ODGHO", "$44.99",
     "An organized kit with wound care, medications and instructions for the injuries that come with cleanup.", "Every home", "first-aid"),
    ("Kidde battery-powered carbon monoxide alarm", "B004Y6V5CI", "$27.97",
     "Generators, heaters and stoves used in outages are a leading cause of CO deaths. This alarm works without power.", "Anyone with gas heat, a generator or a garage", "power"),
    ("Mountain House Chili Mac with Beef, 6 pouches", "B084BT84P9", "$69.99",
     "Just-add-hot-water meals that keep for years and taste like real food.", "Apartments and go-bags", "food"),
]

BIG_TICKET = [
    ("Jackery HomePower 3600 Plus (3.6 kWh, expandable)", "B0FM8653F1", "$1,899.00",
     "Whole-home-scale battery backup for a fridge, sump pump or well pump, with no fumes.", "Long outages and medical needs", "power"),
    ("Champion 4000-watt dual-fuel inverter generator", "B0D6SQR1L1", "$719.00",
     "Runs on gas or propane, with a CO shutoff. Days of power for a house, outdoors only.", "Houses with a yard", "power"),
    ("Renogy 200W portable solar panel", "B0CNPHD4VY", "$219.99",
     "Recharges a power station for as long as the sun shines. Match the connector to your station.", "Long outages and wildfire shutoffs", "power"),
    ("Garmin inReach Mini 2 satellite messenger", "B09PSKG7C3", "$314.00",
     "Two-way texting and SOS from almost anywhere. Needs a subscription plan.", "Rural areas, wildfire zones and travelers", "radios"),
    ("MyMedic MyFAK Standard first-aid kit", "B0CZM49VLQ", "$169.95",
     "A comprehensive, well-organized trauma and medical kit.", "Rural homes and serious preppers", "first-aid"),
    ("Osprey Talon 33 backpack", "B08LP2CLJY", "$199.95",
     "A real hiking pack with a hip belt, so a go-bag is carryable for miles. Pick your size.", "Building a go-bag", "go-bag"),
    ("Leatherman Wave Plus multi-tool", "B079MJBP21", "$103.95",
     "Pliers, knives, drivers and cutters for the small fixes an emergency throws at you.", "Every go-bag and car", "go-bag"),
]

GIFTS = [
    ("LifeStraw Peak Solo personal water filter", "B0CVJ7R5BS", "$20.97", "A water filter small enough for a stocking.", "Hikers and go-bags", "water"),
    ("SAS Survival Handbook (3rd edition)", "0062378074", "$13.04", "The classic all-round survival reference.", "Readers and outdoorspeople", None),
    ("The Prepper's Blueprint", "1496092589", "$19.82", "A step-by-step preparedness plan, one layer at a time.", "Anyone just starting out", None),
    ("Arcturus military wool blanket", "B01IJWUYLK", "$42.99", "Warm even when damp. Lives in the car or by the couch.", "Cars and cold climates", "car"),
    ("Midland WR120 NOAA weather alert radio", "B00176T9OY", "$46.90", "Wakes you for tornado and flood warnings in your county.", "Tornado and flood country", "radios"),
    ("C-A-T tourniquet (North American Rescue)", "B01ITAKG6A", "$33.96", "The genuine article from NAR's official store. Pair it with a free Stop the Bleed class.", "Car and home trauma kits", "first-aid"),
    ("Anker 40W dual-port car charger", "B0843SCLYH", "$16.88", "Keeps two phones charged on an evacuation drive.", "Every driver", "car"),
    ("Primacare emergency Mylar blankets, 10-pack", "B00DZ1NFSK", "$14.99", "Light, cheap warmth for every bag and car.", "Go-bags and car kits", "light-heat"),
    ("OXO Good Grips manual can opener", "B00004OCJW", "$17.26", "The most-forgotten item in emergency kits.", "Every pantry", "food"),
]

CATEGORIES = [
    ("water", "Water", [
        ("Reliance Jumbo-Tainer 2.0, 7 gallons", "B09NP5538N", "$38.99", "A rigid jug with a spigot, easy to fill and pour from.", "Garages and car camping", "water"),
        ("Platypus GravityWorks 4L filter", "B0CV9RPT8Y", "$134.95", "Filters liters at a time with no pumping, so it can supply a family every day.", "Families planning for weeks", "water"),
        ("Aquatabs water purification tablets, 100-pack", "B09B2TVKGB", "$24.99", "Kills viruses that filters miss, and weighs almost nothing.", "Go-bags and bad-water scenarios", "water"),
        ("Augason Farms 55-gallon water barrel", "B06Y2H5GVX", "$159.99", "The lowest cost per gallon. Add a bung wrench and pump, and order early: it ships slowly.", "Houses with a garage", "water"),
    ]),
    ("food", "Food and cooking", [
        ("ReadyWise 132-serving emergency food bucket", "B013CPYRJE", "$99.99", "Weeks of backup meals in one bucket that stacks and stores for years.", "Long-term planning", "food"),
        ("S.O.S. Rations 3600-calorie food bar", "B075TXP1P5", "$22.48", "Heat-tolerant calories with a five-year shelf life.", "Car kits and go-bags", "food"),
        ("Gas One GS-3400P dual-fuel camp stove", "B01HQRD8EO", "$29.99", "Boils water for meals and treatment. Outdoors only; fuel sold separately.", "Homes with a balcony or yard", "food"),
    ]),
    ("light-heat", "Light and warmth", [
        ("Goal Zero Lighthouse 600 lantern", "B08HRM4J8Y", "$79.95", "Lights a room for hours, recharges by USB or hand crank.", "Every home", "light-heat"),
        ("Mr. Heater Portable Buddy propane heater", "B0GYT8HCT6", "$89.99", "Approved for indoor use, with low-oxygen and tip-over shutoffs. Still needs a CO alarm.", "Cold regions with long outages", "light-heat"),
        ("TETON Celsius sleeping bag", "B005EPRM4I", "$84.99", "Keeps you warm in a cold house. Pick the 20°F or 0°F version.", "Winter outages", "light-heat"),
    ]),
    ("comms", "Radios and communication", [
        ("Midland GXT1000VP4 GMRS radios, 2-pack", "B001WMFYH4", "$89.99", "Talk across a neighborhood when phones are down. GMRS needs an FCC license (no exam).", "Families and neighbors", "radios"),
    ]),
    ("first-aid", "First aid", [
        ("QuikClot Advanced Clotting Gauze", "B07WW46HTF", "$38.49", "For bleeding where a tourniquet won't work. Add a pressure bandage and a class.", "Trauma add-on to any kit", "first-aid"),
    ]),
    ("go-bag", "Go-bag", [
        ("3M Aura 9205+ N95 masks, 20-pack", "B09FM2P1KF", "$18 (90¢ a mask)", "NIOSH-approved protection for smoke, ash and dust.", "Wildfire country and every go-bag", "go-bag"),
        ("Fire- and water-resistant document bag", "B08K34LMXP", "$15.99", "Keeps IDs, insurance papers and cash together and grab-ready.", "Every home", "go-bag"),
        ("Ready America 72-hour kit (1 person)", "B00475B96S", "$24.98", "A starter backpack with water pouches, food bars and basics. Upgrade the light and radio.", "Starting from zero today", "go-bag"),
    ]),
    ("car", "Car kit", [
        ("NOCO Boost GB40 jump starter", "B015TKUPIC", "$99.95", "Starts a dead battery without a second car, and charges your phone.", "Every vehicle", "car"),
        ("AstroAI 12V tire inflator", "B07QR4Q42L", "$30.39", "Tops up a slow leak from your car's outlet. Add a plug kit.", "Anyone without a trusted spare", "car"),
        ("Tobfit LED road flares, 6-pack", "B07K3YFMVH", "$32.99", "Makes a stopped car visible on a dark road. Batteries not included.", "Highway and rural drivers", "car"),
    ]),
    ("sanitation", "Sanitation", [
        ("Reliance Luggable Loo toilet seat and bucket", "B07Z2B1YYY", "$50.34", "A working toilet when the water or sewer is out.", "Earthquake and flood country", "sanitation"),
        ("Camco toilet waste bags with gelling powder", "B075BZ8NK3", "$31.00", "Bags with powder that gels waste and controls odor.", "Pairs with the Luggable Loo", "sanitation"),
    ]),
    ("pets", "Pets", [
        ("Amazon Basics 2-door hard-sided pet carrier", "B00OP6SVJW", "$51.59", "Shelters and hotels usually require pets to be crated.", "Cats and small dogs", "pets"),
        ("ARCA PET first-aid kit", "B07WRPCLYR", "$35.90", "Pet-specific supplies for when the vet is closed.", "Dog and cat owners", "pets"),
    ]),
    ("books", "Books", [
        ("Where There Is No Doctor", "0942364155", "$29.16", "The classic medical handbook for when help is far away.", "Every home library", None),
    ]),
]

FAQS = [
    ("When is Black Friday 2026?", "Black Friday is Friday, November 27, 2026, and Cyber Monday is Monday, November 30. Many retailers, including Amazon, usually start deals earlier in the week."),
    ("What prep gear is worth buying on Black Friday?", "Electronics like portable power stations, power banks, headlamps and radios have often been heavily discounted in past years. Water containers and food go on sale less often, so don't wait on those if you have nothing stored."),
    ("How do I know if a Black Friday deal is real?", "Look up the item's price history before you buy. Free tools such as Keepa or camelcamelcamel show what it has sold for over the past months, so you can see whether a sale price is actually low."),
    ("Do you earn money from these links?", "Yes. These are Amazon affiliate links, so we may earn a commission at no extra cost to you. Commissions never decide what we recommend, and every item here is one we recommend in our free guides."),
]
