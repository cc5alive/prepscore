"""Preparedness gift guide (/preparedness-gifts). Prices stay in the data and render as bands only."""

TITLE = "Emergency Preparedness Gifts People Will Actually Use (2026 Gift Guide)"
META = ("Practical preparedness gifts by price band: headlamps, power banks, weather radios, car kits, first aid and power stations, "
        "plus a free gift that matters most and the survival gear to skip.")
H1 = "Preparedness gifts people will actually use"
DEK = ("The best prep gifts earn their place in a drawer or a car long before an emergency: a headlamp for the next outage, "
       "a jump starter for a dead battery, a radio that wakes you for a tornado warning. Here they are by price band.")

# id, name, asin, price (rendered as a band), why, good for, guide slug
GIFTS = [
    ("can-opener", "OXO Good Grips manual can opener", "B00004OCJW", "$10 to $20",
     "The most forgotten item in emergency pantries. A good one gets used every week anyway.", "Every kitchen", "food"),
    ("mylar", "Mylar emergency blankets, 10-pack", "B00DZ1NFSK", "$10 to $15",
     "Pocket-size warmth for cars, go-bags and stadium seats. Ten means one for every bag in the family.", "Stocking stuffers", "light-heat"),
    ("doc-bag", "Fire- and water-resistant document bag", "B08K34LMXP", "$15 to $30",
     "Holds passports, deeds and a USB drive of records, ready to grab in an evacuation.", "New homeowners, parents", "go-bag"),
    ("sas", "SAS Survival Handbook (3rd edition)", "0062378074", "$12 to $20",
     "The classic all-round survival book: shelter, water, first aid, and plenty of armchair reading.", "Readers and campers", None),
    ("pet-tag", "Engraved pet ID tag (GoTags)", "B085MH756K", "$10 to $20",
     "A phone number on the collar is the fastest way home for a lost pet. Pair it with a microchip check at the vet.", "Pet owners", "pets"),
    ("lifestraw", "LifeStraw Peak Solo personal water filter", "B0CVJ7R5BS", "$20 to $30",
     "A personal filter for hikes and go-bags. It removes bacteria and parasites; not chemicals or salt.", "Hikers and go-bags", "water"),
    ("co-alarm", "Kidde battery-powered CO alarm", "B004Y6V5CI", "$20 to $40",
     "Keeps working when the power is out, which is when generators and fuel heaters cause carbon monoxide poisoning.", "New homeowners, renters", "power"),
    ("car-charger", "Anker 40W dual-port car charger", "B0843SCLYH", "$15 to $40",
     "Charges two phones fast from the car, the backup charger in any outage.", "Every driver", "car"),
    ("headlamp", "Black Diamond Spot 400-R rechargeable headlamp", "B09NQK87MN", "$30 to $60",
     "Hands-free light for outages, car trouble and walking the dog. Rechargeable, so no dead-battery drawer surprise.", "Almost anyone", "light-heat"),
    ("power-bank", "Anker 20,000 mAh power bank", "B0CXDXP8VR", "$30 to $60",
     "About four phone charges. Used for travel all year; keeps the phone alive in an outage.", "Commuters, travelers, teens", "power"),
    ("weather-radio", "Midland WR120 NOAA weather alert radio", "B00176T9OY", "$30 to $50",
     "Sounds an alarm for warnings in your county, even at 3 a.m. with phones on silent.", "Tornado, flood and hurricane country", "radios"),
    ("first-aid", "Adventure Medical Kits family first-aid kit", "B0079ODGHO", "$30 to $60",
     "Organized by injury, so anyone can find what they need fast. Better than the bandage drawer.", "Families, cars, cabins", "first-aid"),
    ("tourniquet", "C-A-T tourniquet (North American Rescue)", "B01ITAKG6A", "$30 to $40",
     "The genuine article, not a knockoff. Best given with a free Stop the Bleed class.", "Car kits, the medically minded", "first-aid"),
    ("wool-blanket", "Arcturus military wool blanket", "B01IJWUYLK", "$40 to $50",
     "Warm even when damp, tough enough to live in the trunk, and nice on the couch.", "Drivers in cold climates", "car"),
    ("lantern", "Goal Zero Lighthouse 600 lantern", "B08HRM4J8Y", "$40 to $90",
     "Lights a room in an outage, charges from USB or a hand crank, and doubles as camping gear.", "Families, campers", "light-heat"),
    ("inflator", "AstroAI portable tire inflator", "B07QR4Q42L", "$30 to $70",
     "Tops up a soft tire from the 12 V outlet. Saves a roadside wait, and gets used for bikes and balls too.", "Every driver", "car"),
    ("crank-radio", "Midland ER310 crank and solar emergency radio", "B015QIC1PW", "$50 to $80",
     "AM, FM and NOAA weather with a crank, solar panel and flashlight. Charges a phone in a pinch.", "Anyone without a radio", "radios"),
    ("gmrs", "Midland GMRS two-way radios (two-pack)", "B001WMFYH4", "$60 to $150",
     "Keeps the family in touch when cell networks jam. Useful on ski trips, road trips and campgrounds too.", "Families, road trippers", "radios"),
    ("jump-starter", "NOCO Boost GB40 jump starter", "B015TKUPIC", "$90 to $120",
     "Starts a dead car battery without another car. Most drivers need it once a winter.", "Every driver, new drivers", "car"),
    ("multitool", "Leatherman Wave Plus multi-tool", "B079MJBP21", "$90 to $120",
     "A tool kit that lives on a belt or in a glovebox, and gets used for everyday fixes.", "The handy one", "go-bag"),
    ("myfak", "MyMedic MyFAK Standard first-aid kit", "B0CZM49VLQ", "$100 to $250",
     "A serious kit with trauma supplies, organized in labeled pouches.", "Hikers, hunters, the medically minded", "first-aid"),
    ("backpack", "Osprey Talon 33 backpack", "B08LP2CLJY", "$100 to $200",
     "A comfortable go-bag that's also a great day-hiking pack, so it gets used.", "Hikers, anyone building a go-bag", "go-bag"),
    ("solar", "Renogy 200W portable solar panel", "B0CNPHD4VY", "$150 to $400",
     "Recharges a power station during long outages. Best for someone who already has a station.", "Power station owners", "power"),
    ("inreach", "Garmin inReach Mini 2 satellite messenger", "B09PSKG7C3", "$300 to $450",
     "Texts and SOS from anywhere with a view of the sky. Needs a paid subscription, so check the plans first.", "Backcountry hikers, rural drivers", "radios"),
    ("power-station", "Anker SOLIX C1000 power station (1 kWh)", "B0C5C89QKZ", "$400 to $900",
     "Runs a CPAP, a fridge for hours, or phones and lights for days, silently and safely indoors.", "CPAP users, apartment dwellers", "power"),
]

PEOPLE = [
    ("For drivers", ["jump-starter", "inflator", "car-charger", "wool-blanket"]),
    ("For new homeowners and renters", ["co-alarm", "doc-bag", "headlamp", "first-aid"]),
    ("For hikers and campers", ["lifestraw", "inreach", "backpack", "myfak"]),
    ("For the person who has everything", ["weather-radio", "gmrs", "lantern", "power-station"]),
    ("Stocking stuffers", ["mylar", "can-opener", "pet-tag", "sas"]),
]

FREE_GIFT = [
    "Sit down together and sign them up for their county's emergency alerts. It takes ten minutes and is the single most useful step in any city.",
    "Agree on an out-of-area contact everyone in the family texts after a disaster, and write it on a card for every wallet.",
    "Take the free PrepScore quiz together and print the one-page plan it makes. It lists their three biggest gaps and a free option for each.",
    "Check their smoke and CO alarms and replace the batteries. Bring the batteries.",
]

SKIP = [
    ("\"250-piece\" survival kits", "Most of the pieces are filler: tiny compasses, wire saws and whistles that break. One good headlamp beats the whole box."),
    ("Surprise food buckets", "Long-term food is personal: tastes, allergies, diets and storage space. Ask first, or give a can opener and a pantry list instead."),
    ("A gas generator as a surprise", "It needs a safe outdoor spot 20 feet from the house, fuel storage and regular running. It's a decision for the owner, not a gift."),
    ("Bargain knockoffs of safety gear", "Counterfeit tourniquets and uncertified masks fail when it matters. Buy brands with real certifications from sellers you trust."),
]

FAQS = [
    ("What's a good emergency preparedness gift for someone who has everything?",
     "A NOAA weather alert radio, a pair of GMRS radios or a good lantern. Most people own none of these, and each is useful outside emergencies. If budget allows, a 1,000 Wh power station is the gift they'll be most grateful for in an outage."),
    ("What's a good prep gift under $25?",
     "A manual can opener, a 10-pack of Mylar blankets, an engraved pet tag, a document bag or the SAS Survival Handbook. All are cheap, useful and rarely already owned."),
    ("Are survival kits good gifts?",
     "Most pre-made \"survival kits\" are full of filler. A pre-made 72-hour kit can be a fine starting point for someone with nothing, but a few quality items, like a headlamp, power bank and first-aid kit, are more useful than a box of gadgets."),
    ("Is a power station a good gift?",
     "For someone who uses a CPAP, lives in an apartment or gets long outages, yes. It's silent, safe indoors and useful for camping. For a house with a yard and long outages, a generator may suit them better, but that's their call."),
    ("Is it weird to give emergency gear as a gift?",
     "Not if it's useful every day. Headlamps, power banks, car chargers and multi-tools get used all year. Save the doomsday framing; just say you want them to be safe."),
]
