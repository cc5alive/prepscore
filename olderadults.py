"""Buyer page: emergency planning for older adults and people with disabilities (/guides/older-adults-disabilities)."""

SLUG = "older-adults-disabilities"
PARENT = "first-aid"
OG = "guide-older-adults"
OG_CARD = ("Plan for everyone", "Older adults and disabilities", "Medications, power-dependent devices, getting out, and the people and programs that help.")
TITLE = "Emergency Preparedness for Older Adults and People With Disabilities"
META = ("An emergency plan for older adults and people with disabilities: medications, oxygen and other power-dependent devices, "
        "mobility and evacuation, a support network, and the programs that help. Printable checklist.")
H1 = "Emergency planning for older adults and people with disabilities"
DEK = ("Most prep advice assumes you can carry a heavy bag and walk out the door. This page is for everyone else: what to plan "
       "when you rely on medications, powered equipment, mobility aids or other people, and who can help.")
REVIEWED = "Ready.gov, FDA, ADA.gov and utility program guidance"
CRUMB = "Older adults"

VERDICT = [
    ("Build a support network of two or three people.", "Family, neighbors or friends who will check on you, have a spare key, know where your supplies are, and know how to use your equipment and give your medications. Practice the plan with them."),
    ("Keep at least a week of medications, two if you can.", "Plus a written list of every medication, dose and prescriber. Ask your pharmacist and insurer how to get early refills; rules vary by plan and state."),
    ("Plan power for anything that plugs in.", "Oxygen concentrators, CPAPs, power wheelchairs, refrigerated medicine. Know how long each runs on battery, size backup power for it, and tell your utility you rely on it."),
    ("Plan how you'd get out, before you need to.", "Who drives you, how your mobility aids and service animal come along, and where you'd go. Ask whether your county keeps a registry of people who may need help evacuating."),
    ("Switch benefit payments to direct deposit.", "Ready.gov notes that mail can stop for days or weeks after a disaster. Direct deposit or the Treasury's Direct Express card keeps Social Security and other payments coming."),
]

SECTIONS = [
    ("Medications and medical needs", [
        ("A written list", "Every medication, dose, schedule and prescriber, plus allergies and conditions. Keep a copy in your wallet and one with your supplies."),
        ("Refrigerated medicine", "Keep a small cooler and ice packs, or an evaporative cooling case for insulin. Ask your pharmacist how long yours stays good at room temperature."),
        ("Your care providers' plans", "Ask your dialysis center, clinic or home-care agency what they do in a disaster and where you'd go if they close. Ready.gov suggests finding backup providers."),
        ("Glasses, hearing aids and dentures", "A spare pair of glasses, extra hearing aid batteries or a charger, and denture supplies. They're easy to forget and hard to replace in a hurry."),
    ]),
    ("Power-dependent equipment", [
        ("Know your runtimes", "How long does each device run on its own battery? Write it on a card taped to the device."),
        ("Backup power", "A battery power station runs a CPAP or a power wheelchair charger silently and safely indoors. Use our power station calculator to size one. A gas generator runs outdoors only."),
        ("Oxygen", "Concentrators need power. Ask your supplier for backup cylinders that don't, and how long they last at your flow rate."),
        ("Tell your utility", "Many utilities run medical or life-support programs that give advance notice of planned shutoffs; in California it's called Medical Baseline. Ask yours."),
    ]),
    ("Getting out", [
        ("Transportation", "Arrange a ride with someone in your network, and a backup. If you use paratransit, ask how it works in an evacuation."),
        ("Mobility aids and service animals", "Plan how your wheelchair, walker or scooter comes with you. Pack food, water and records for a service animal."),
        ("Shelters", "Under the Americans with Disabilities Act, public emergency shelters must be accessible and must allow service animals. Some areas also run medical or functional-needs shelters; your county emergency office can tell you."),
        ("Registries", "Many counties keep a voluntary list of residents who may need help in an emergency. Call 211 or your county's emergency management office to ask."),
    ]),
    ("Communication", [
        ("Alerts you can notice", "If you're deaf or hard of hearing, turn on text alerts from your county and consider a weather radio with a strobe or bed-shaker attachment. Blind or low-vision users can ask whether local alerts come by phone call."),
        ("A card that speaks for you", "Write down how to communicate with you, what equipment you use and who to call. Keep it in your wallet and on the fridge."),
    ]),
]

PICKS = [
    {"name": "1 kWh power station (Anker SOLIX C1000 or similar)", "asin": "B0C5C89QKZ", "asin_name": "Anker SOLIX C1000", "price": "$400 to $900",
     "what": "A silent battery with AC outlets, safe to use indoors.",
     "why": "Runs a CPAP for 9 to 11 nights with the humidifier off, recharges a power wheelchair or keeps phones and lights going. No fumes and nothing to fuel.",
     "watch": "Check your device's watts against the station's output, and keep it charged. Not for oxygen concentrators that draw several hundred watts all day; ask your supplier.",
     "best": "Anyone with a CPAP, power wheelchair or other plug-in equipment"},
    {"name": "Insulin cooling case (evaporative, such as FRIO)", "q": "frio insulin cooling wallet", "asin_name": "Amazon search results for FRIO cooling cases", "price": "$20 to $40",
     "what": "A wallet that keeps insulin cool for days by evaporation after you soak it in water. No ice or power needed.",
     "why": "Refrigerated medicine is one of the first things at risk in an outage or evacuation.",
     "watch": "Pick the size for your pens or vials. In very humid weather evaporation works less well; a cooler with ice packs is the backup.",
     "best": "Anyone who takes insulin or other refrigerated medicine"},
    {"name": "Midland WR120 NOAA weather alert radio", "asin": "B00176T9OY", "price": "$30 to $50",
     "what": "A radio that sounds an alarm for warnings in your county.",
     "why": "Wakes you for a tornado or flood warning even with the phone on silent. It has a jack for a strobe light or bed shaker for people who are deaf or hard of hearing.",
     "watch": "Program your county code when you set it up, and keep fresh batteries in it for outages.",
     "best": "Anyone who lives alone, and households with a deaf member"},
    {"name": "Fire- and water-resistant document bag", "asin": "B08K34LMXP", "price": "$15 to $30",
     "what": "A pouch for papers you'd grab in an evacuation.",
     "why": "Holds your medication list, insurance and Medicare cards, equipment details and contacts, ready to go.",
     "watch": "Resistant, not fireproof. Keep digital copies too.",
     "best": "Everyone, especially anyone managing several conditions"},
    {"name": "Medical ID bracelet", "q": "medical id bracelet engraved", "asin_name": "Amazon search results", "price": "$15 to $40",
     "what": "An engraved bracelet or tag with your conditions, medications and an emergency contact.",
     "why": "Speaks for you if you can't, for example to responders after a fall or in a crowded shelter.",
     "watch": "Keep the engraving short and current: main conditions, critical allergies, a phone number.",
     "best": "People with diabetes, heart conditions, dementia or severe allergies"},
    {"name": "Weekly pill organizer (AM/PM)", "q": "weekly pill organizer am pm", "asin_name": "Amazon search results", "price": "$10 to $20",
     "what": "A seven-day organizer with morning and evening compartments.",
     "why": "Grab-and-go a week of medications in an evacuation, and keeps doses straight when routines fall apart.",
     "watch": "Keep the original bottles or a printed list too; shelters and pharmacies may need to see them.",
     "best": "Anyone taking several daily medications"},
]

CHECKLIST_TITLE = "Personal emergency checklist"
CHECKLIST = [
    "Two or three people in my support network, with a spare key", "Written list of medications, doses and prescribers",
    "A week or more of medications, two if possible", "Plan for refrigerated medicine", "Spare glasses, hearing aid batteries or charger",
    "Each device's battery runtime written down", "Backup power sized for my equipment", "Utility told I rely on powered equipment",
    "Backup oxygen cylinders, if I use oxygen", "A ride out, and a backup ride", "Plan for my mobility aids and service animal",
    "Asked about my county's registry (call 211)", "Benefit payments on direct deposit", "Copies of insurance and Medicare cards",
    "Text alerts from my county turned on", "A card explaining how to communicate with me", "Water and no-cook food for at least 3 days",
    "Flashlight or headlamp by the bed",
]
CHECKLIST_NOTE = "Print this and go through it with someone in your support network. Your progress stays in this browser."
CHECKLIST_LINK = ("First aid and medical guide", "first-aid.html")

FAQS = [
    ("How many days of medication should I keep?",
     "At least a week, and two if you can. The American Academy of Pediatrics suggests two weeks of prescriptions for families, and many emergency agencies say the same for adults. Ask your pharmacist and insurer about refilling early; rules vary by plan, and some states allow emergency refills during a declared disaster."),
    ("What if I use oxygen?",
     "Concentrators need electricity, so a long outage is an emergency. Ask your supplier for backup cylinders that don't need power and how long they last at your flow rate, register with your utility's medical program, and know where you'd go if the power stays out."),
    ("Will a shelter take my service animal and wheelchair?",
     "Public emergency shelters must be accessible and must allow service animals under the Americans with Disabilities Act. Bring your own supplies for the animal, and your equipment's chargers. Some areas also run medical or functional-needs shelters for people who need more care."),
    ("What's an emergency registry, and should I join one?",
     "Many counties keep a voluntary list of residents who may need help in a disaster, such as people who use oxygen or can't drive. It doesn't guarantee a rescue, but it helps responders plan. Call 211 or your county emergency management office to ask whether yours has one."),
    ("I live alone. What matters most?",
     "Your support network. Arrange for at least two people to check on you when a storm or outage hits, give one a key, and agree on how you'll reach each other if phones are down."),
]

SOURCES = [
    ("Ready.gov: Older adults", "https://www.ready.gov/older-adults"),
    ("Ready.gov: Individuals with disabilities and access and functional needs", "https://www.ready.gov/individuals-access-functional-needs"),
    ("FDA: Tips about medical devices and natural disasters", "https://www.fda.gov/medical-devices/emergency-situations-medical-devices/fda-offers-tips-about-medical-devices-and-natural-disasters"),
    ("ADA.gov: Emergency planning", "https://www.ada.gov/topics/emergency-planning/"),
    ("California Public Utilities Commission: Medical Baseline fact sheet (PDF)", "https://www.cpuc.ca.gov/-/media/cpuc-website/about-cpuc/documents/transparency-and-reporting/fact_sheets/medical_baseline_101921.pdf"),
]

RELATED = [("Keeping a CPAP running in an outage", "cpap-power-outage.html"), ("Power station calculator", "../power-calculator.html"),
           ("First aid and medical guide", "first-aid.html"), ("Losing power in a winter storm", "winter-storm-power-outage.html"),
           ("Get your PrepScore", "../quiz.html")]
CALC_LINK = ("To size backup power for a CPAP, wheelchair charger or other equipment, use the", "../power-calculator.html", "power station calculator")
