"""Buyer page: insulin and refrigerated medicine in a power outage (/guides/insulin-power-outage)."""

SLUG = "insulin-power-outage"
PARENT = "first-aid"
OG = "guide-insulin-outage"
OG_CARD = ("Medicine", "Insulin in a power outage", "How long insulin lasts without a fridge, keeping it cool without freezing it, and what to do with other refrigerated medicine.")
TITLE = "Insulin and Refrigerated Medicine in a Power Outage: What to Do"
META = ("How long insulin lasts without refrigeration, how to keep it cool without freezing it, when to replace it, and what to do with "
        "other refrigerated medicines in a power outage. Based on FDA and CDC guidance.")
H1 = "Insulin and refrigerated medicine in a power outage"
DEK = ("Losing the fridge doesn't mean losing your insulin. Here's how long it lasts, how to keep it cool, and what the FDA and CDC say "
       "about other medicines that need refrigeration.")
REVIEWED = "FDA and CDC emergency guidance on insulin and refrigerated drugs"
CRUMB = "Insulin in an outage"

GRID_TOC = "Quick guide"
GRID = ("Quick guide",
        "General guidance from the FDA and CDC. Your medicine's package insert is the final word, and your pharmacist can tell you about your exact product.",
        ["Situation", "What to do"],
        [["Insulin vials or cartridges, out of the fridge", "The FDA says they can stay unrefrigerated between 59°F and 86°F for up to 28 days and keep working, opened or not. Some pens allow fewer or more days; check the leaflet."],
         ["Insulin got hotter than 86°F", "It loses strength the longer it's hot. In an emergency you may still need to use it: check your blood sugar more often, and replace it as soon as you can."],
         ["Insulin froze", "Don't use it, even after it thaws. Freezing breaks it down."],
         ["Insulin pump reservoir", "Heat shortens how long insulin lasts in the pump; follow the pump and insulin instructions, which usually allow about a week or less in the reservoir."],
         ["Other refrigerated medicine, power out a day or more", "The CDC says to throw it away unless the label says otherwise. If a life depends on it, keep using it only until you get a new supply."],
         ["Not sure if it's still good", "Check the storage instructions, or ask a pharmacist, your doctor or the manufacturer."]])

VERDICT = [
    ("Most insulin is fine out of the fridge for weeks.", "The FDA says insulin vials and cartridges can be kept between 59°F and 86°F for up to 28 days and still work. Keep it out of heat and sun, and check your blood sugar more often."),
    ("Keep it cool, but never let it freeze.", "Don't put insulin directly on ice or a frozen gel pack. Wrap it in a cloth inside a cooler, or use an evaporative cooling wallet that never gets below freezing."),
    ("Other refrigerated medicine is stricter.", "The CDC says to throw it away after a day or more without power unless the label says otherwise. If someone's life depends on it, use it until you can replace it."),
    ("Keep a week's supply and a written list.", "Ask about refilling early before a storm, and keep a list of every medicine, dose and prescriber in your go-bag."),
    ("A power station can run a small fridge.", "A compact fridge uses about 0.3 to 0.8 kWh a day, so a 1,000 Wh station keeps one cold for roughly a day or more."),
]

STEPS_TITLE = "When the power goes out"
STEPS = [
    ("Leave the fridge closed at first", "A closed fridge stays cold for about 4 hours. Short outages may need nothing more."),
    ("Move insulin to a cool, dark spot", "If the outage drags on or the fridge warms up, take insulin out and keep it somewhere cool, out of sun and away from heaters. Room temperature is fine."),
    ("In a heat wave, cool it gently", "Use a cooler with ice or gel packs wrapped in a towel, so the insulin never touches anything frozen, or an evaporative cooling wallet."),
    ("Check your blood sugar more often", "Insulin exposed to heat can work less well. If readings run high, contact your doctor."),
    ("Write down when it left the fridge", "Insulin out of the fridge has a shorter life. Mark the date on the box so you know when to replace it."),
    ("Replace it when you can", "Ask your pharmacist about an emergency supply. Many states let pharmacists dispense a short emergency supply, and insurers often allow early refills during declared emergencies."),
]

SECTIONS = [
    ("Other medicines and supplies", [
        ("Refrigerated medicines other than insulin", "Some liquid antibiotics, some injectable medicines and many biologics need refrigeration. Many labels give a room-temperature allowance; check yours now, before an outage, and write it on the box."),
        ("Medicines that should not be refrigerated", "Epinephrine auto-injectors are stored at room temperature, not in the fridge. Keep them out of a hot car and away from freezing."),
        ("Glucose meters and test strips", "Strips and meters have their own temperature limits, and extreme heat or cold can affect readings. Keep them with your insulin, not in a hot car."),
        ("Pumps and sensors", "Keep chargers and spare batteries for pumps, sensors and phones, plus backup pens or syringes in case a pump fails. A power bank keeps a phone-based glucose monitor running."),
        ("Your go-bag", "Pack a week of medicine and supplies, fast-acting sugar, a written list of doses and a copy of your prescriptions."),
    ]),
]

PICKS = [
    {"name": "Evaporative insulin cooling wallet", "asin": "B00022628K", "asin_name": "FRIO Duo cooling wallet (2 pens or vials)", "price": "$20 to $35",
     "what": "A fabric wallet with crystals that turn to gel when soaked in water, then cool by evaporation.",
     "why": "Needs no ice or electricity, and can't freeze insulin. The maker says one soak cools for 2 to 4 days; soak it again to restart.",
     "watch": "Evaporative cooling works less well in very humid weather. Comes in sizes from one pen to several vials; pick the one that fits your supply.",
     "best": "Anyone on insulin or another refrigerated injectable"},
    {"name": "Fridge and freezer thermometer", "q": "refrigerator freezer thermometer", "price": "$5 to $15",
     "what": "A small thermometer that sits inside the fridge.",
     "why": "Shows whether the fridge has stayed cold, so you know when to move insulin and whether other medicine is still within its label.",
     "watch": "Get one for the fridge and one for the freezer.",
     "best": "Every household with refrigerated medicine"},
    {"name": "Small cooler with reusable gel packs", "q": "small cooler with reusable ice packs", "price": "$15 to $40",
     "what": "A small insulated cooler and a few gel packs you keep frozen.",
     "why": "Keeps a few days of insulin or other medicine cool in a long, hot outage, or when you evacuate.",
     "watch": "Wrap medicine in a towel so it never touches a frozen pack. Swap packs with a neighbor or shelter that has a freezer.",
     "best": "Longer outages and evacuations"},
    {"name": "Anker 20,000 mAh power bank", "asin": "B0CXDXP8VR", "price": "$30 to $60",
     "what": "A pocket battery that recharges a phone about four times.",
     "why": "Keeps a phone-based glucose monitor, a pump's phone app or a sensor reader running for days.",
     "watch": "Recharge it every few months; batteries slowly drain on the shelf.",
     "best": "Anyone who uses a phone with their diabetes devices"},
    {"name": "1 kWh power station (Anker SOLIX C1000)", "asin": "B0C5C89QKZ", "price": "$400 to $900",
     "what": "A 1,056 Wh LiFePO4 battery with 6 AC outlets, safe to use indoors.",
     "why": "Runs a compact fridge for medicine for roughly a day or more per charge, plus phones and a CPAP. Recharge it from a car or solar panel.",
     "watch": "About 28 pounds. For a full-size fridge, see our refrigerator runtime table first.",
     "best": "Households with medicine that must stay refrigerated"},
]

FAQS = [
    ("How long can insulin go without refrigeration?",
     "The FDA says insulin in vials or cartridges, opened or unopened, can be kept unrefrigerated between 59°F and 86°F for up to 28 days and continue to work. Some pens are labeled for fewer or more days, so check your product's leaflet."),
    ("Can I use insulin that got too hot?",
     "Heat makes insulin lose strength over time, and the FDA says that in an emergency you might still need to use insulin stored above 86°F. Check your blood sugar more often and replace it as soon as you can."),
    ("Is frozen insulin safe to use?",
     "No. The CDC says insulin that has been frozen can break down and be less effective. Don't use it, even after it thaws."),
    ("Should I put insulin on ice in a power outage?",
     "Only if it can't touch the ice. Wrap it in a towel inside a cooler, or use an evaporative cooling wallet. Room temperature is fine for most insulin, so ice is mainly for heat waves."),
    ("What about other refrigerated medicines?",
     "The CDC says to throw away refrigerated medicine after the power has been out for a day or more, unless the label says otherwise. If a life depends on it, use it only until a new supply is available. A pharmacist can tell you about a specific medicine."),
    ("How do I get a refill after a disaster?",
     "Call your pharmacy or another branch of the same chain; many can see your prescriptions. Many states let pharmacists give an emergency supply, and insurers often relax refill limits during declared emergencies."),
]

SOURCES = [
    ("FDA: Information regarding insulin storage and switching between products in an emergency", "https://www.fda.gov/drugs/emergency-preparedness-drugs/information-regarding-insulin-storage-and-switching-between-products-emergency"),
    ("FDA: Safe drug use after a natural disaster", "https://www.fda.gov/drugs/emergency-preparedness-drugs/safe-drug-use-after-natural-disaster"),
    ("CDC: Managing insulin in an emergency", "https://www.cdc.gov/diabetes/articles/managing-insulin-in-emergency.html"),
    ("CDC: Refrigerated drugs", "https://www.cdc.gov/natural-disasters/psa-toolkit/refrigerated-drugs.html"),
    ("USDA FSIS: Keep your food safe during emergencies (fridge and freezer times)", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies"),
]

RELATED = [("Older adults and people with disabilities", "older-adults-disabilities.html"), ("First-aid guide", "first-aid.html"),
           ("Power station for a fridge", "power-station-for-refrigerator.html"), ("CPAP in a power outage", "cpap-power-outage.html"),
           ("Backup power guide", "power.html")]
