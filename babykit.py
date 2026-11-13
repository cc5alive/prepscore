"""Buyer page: emergency kit for babies and toddlers (/guides/baby-emergency-kit)."""

SLUG = "baby-emergency-kit"
PARENT = "go-bag"
OG = "guide-baby-kit"
OG_CARD = ("Babies and toddlers", "A baby emergency kit", "Feeding without power or clean water, diapers, safe sleep, and what goes in the bag.")
TITLE = "Baby Emergency Kit: What Babies and Toddlers Need in a Disaster"
META = ("What to pack for a baby or toddler in an emergency: feeding without power or clean water, ready-to-feed formula, diapers, "
        "safe sleep away from home, medicines and documents. Printable checklist.")
H1 = "An emergency kit for babies and toddlers"
DEK = ("Babies can't wait out an emergency the way adults can. They need safe feeding without power or clean water, a safe place to "
       "sleep, and the right supplies close at hand. Here's what to plan and pack, from newborn to toddler.")
REVIEWED = "CDC, American Academy of Pediatrics and Ready.gov guidance"
CRUMB = "Baby kit"

VERDICT = [
    ("Plan feeding that needs no power and no clean water.", "If you breastfeed, keep doing it: the CDC calls it the safest way to feed an infant in an emergency. If you use formula, keep enough unopened ready-to-feed formula, in your baby's usual brand, for several days. It needs no water and no refrigeration until opened."),
    ("Keep disposable bottles or cups.", "Washing bottles takes safe water you may not have. The CDC suggests disposable feeding items, or feeding with a clean cup, when you can't clean bottles properly."),
    ("Stock diapers and wipes for two weeks.", "Count how many your child uses in a day and multiply by 14. Size up as they grow; check the kit every few months."),
    ("Plan a safe place to sleep away from home.", "A portable play yard or travel crib, and a wearable blanket or sleep sack instead of loose blankets. Babies sleep on their backs, alone, on a firm flat surface, in a shelter or a hotel too."),
    ("Pack the papers and the medicines.", "Ask your pediatrician for a two-week supply of any prescriptions. Keep their contact information, immunization records, insurance cards and a recent photo of your child in a water-resistant bag."),
]

SECTIONS = [
    ("Feeding in an emergency", [
        ("Breastfeeding", "Keep going if you can. Learn to hand express in case a breast pump has no power. The CDC says expressed milk keeps up to 24 hours in a cooler with ice packs."),
        ("Ready-to-feed formula", "The simplest choice when power or water is out: no mixing, no water, and unopened bottles need no refrigeration. Buy your baby's usual brand and rotate it before it expires."),
        ("Powdered formula", "Mix it with bottled water. If you have none, the CDC says to bring water to a rolling boil for 1 minute (3 minutes above 6,500 feet), then let it cool before mixing. Never dilute formula to make it last longer."),
        ("Floodwater", "Throw away nipples, pacifiers and teethers that touched floodwater. They can't be cleaned well enough."),
        ("Toddlers", "Familiar shelf-stable foods your child already eats: pouches, crackers, shelf-stable milk if they drink it. A stressed toddler is far more likely to eat what they know."),
    ]),
    ("Staying warm, cool and safe", [
        ("Heat and cold", "Babies lose heat faster than adults, and overheat faster too. Dress them in about one more layer than you'd wear yourself, no more, and keep them out of hot cars and rooms."),
        ("Carbon monoxide", "Never run a generator, grill or camp stove indoors. Babies are more sensitive to carbon monoxide than adults. Keep a battery-powered CO alarm where your child sleeps."),
        ("Car seat", "If you evacuate by car, the car seat comes too. Keep it installed or by the door; shelters and rides arranged by others may not have one."),
        ("Carrier", "A baby carrier keeps your hands free on stairs, in crowds or on foot, and keeps your child close and calmer."),
    ]),
    ("Comfort and routine", [
        ("A favorite thing", "A comfort item, a couple of small toys and a familiar book. The AAP suggests comfort items for children, especially those with special needs."),
        ("Keep routines", "Naps, feeding times and bedtime rituals as close to normal as you can. Routines help young children cope with upheaval."),
        ("Hygiene", "Hand sanitizer, a changing pad, and trash bags for diapers. Keep diaper changes away from food preparation."),
    ]),
]

PICKS = [
    {"name": "Pre-sterilized disposable bottles or liners", "q": "disposable pre-sterilized baby bottles", "asin_name": "Amazon search results", "price": "$15 to $30",
     "what": "Single-use bottles or bottle liners that come sterile in the package.",
     "why": "Feeding without safe water to wash bottles is one of the hardest parts of an emergency with a baby. These skip the washing.",
     "watch": "Check that they work with your baby's usual nipple flow. Practice with one before you need it.",
     "best": "Formula-fed babies, and as backup for pumped milk"},
    {"name": "Wearable blanket (sleep sack)", "q": "baby sleep sack wearable blanket", "asin_name": "Amazon search results", "price": "$15 to $35",
     "what": "A sleeveless sack your baby sleeps in, instead of a loose blanket.",
     "why": "Keeps a baby warm in a cold house or a shelter while following safe sleep advice: no loose blankets in the crib.",
     "watch": "Pick the size for your baby's weight, and a warmer weight (TOG) for winter outages.",
     "best": "Babies under 1, in any home that loses heat in an outage"},
    {"name": "Portable play yard or travel crib", "q": "portable play yard travel crib", "asin_name": "Amazon search results", "price": "$60 to $200",
     "what": "A folding crib with a firm, flat mattress that packs into a bag.",
     "why": "Gives your baby a safe place to sleep at a shelter, a friend's house or a hotel.",
     "watch": "Use only the mattress that came with it; don't add padding. Check for recalls at cpsc.gov.",
     "best": "Families likely to evacuate for fire, hurricane or flood"},
    {"name": "Soft structured baby carrier", "q": "ergonomic baby carrier newborn toddler", "asin_name": "Amazon search results", "price": "$40 to $180",
     "what": "A carrier that holds your baby on your front or back.",
     "why": "Keeps both hands free if you have to leave on foot, take stairs in a building with no elevator, or wait in line.",
     "watch": "Follow the age and weight limits, and keep your baby's face visible and airway clear.",
     "best": "Babies and young toddlers"},
    {"name": "Rechargeable LED headlamp", "asin": "B09NQK87MN", "price": "$15 to $35",
     "what": "A light you wear on your head.",
     "why": "Night feeds and diaper changes in a blackout need two hands. A low setting is easier on a half-asleep baby.",
     "watch": "Keep it charged, and keep a spare set of batteries if it takes them.",
     "best": "Every parent"},
    {"name": "Fire- and water-resistant document bag", "asin": "B08K34LMXP", "price": "$15 to $30",
     "what": "A pouch for the papers you'd grab in an evacuation.",
     "why": "Holds birth certificates, immunization records, insurance cards, your pediatrician's details and a photo of your child.",
     "watch": "Resistant, not fireproof. Keep phone photos of the documents too.",
     "best": "Every family"},
]

CHECKLIST_TITLE = "Baby and toddler checklist"
CHECKLIST = [
    "Ready-to-feed formula for several days, or a breastfeeding plan", "Disposable bottles or a clean cup for feeding",
    "Bottled water for powdered formula and washing", "Familiar shelf-stable foods for a toddler",
    "Diapers for two weeks (a day's count × 14)", "Wipes, diaper cream and trash bags",
    "Two-week supply of prescriptions", "Fever reducer your pediatrician recommends, with their dosing chart",
    "Thermometer", "Sleep sack and a portable crib or play yard", "Warm layers, a hat and spare clothes",
    "Baby carrier", "Car seat ready to go", "Comfort item and a few small toys",
    "Pediatrician's contact information", "Immunization records, birth certificate and insurance cards",
    "A recent photo of your child", "Battery CO alarm where your child sleeps",
]
CHECKLIST_NOTE = "Check the kit every few months: sizes change fast and formula expires. Your progress stays in this browser."
CHECKLIST_LINK = ("Go-bags and evacuation guide", "go-bag.html")

FAQS = [
    ("How much formula should I keep for emergencies?",
     "The CDC suggests enough ready-to-feed formula to feed your child for several days. Ready-to-feed needs no water, and unopened bottles need no refrigeration. Stock your baby's usual brand and rotate it before it expires. If your baby uses a special formula, ask your pediatrician how to keep a reserve."),
    ("Can I mix powdered formula with tap water after a disaster?",
     "Only if officials say the tap water is safe. Otherwise use bottled water, or bring water to a rolling boil for 1 minute (3 minutes above 6,500 feet) and let it cool before mixing, as the CDC advises."),
    ("What if I'm breastfeeding?",
     "Keep going. The CDC calls breastfeeding the safest way to feed an infant in an emergency, since it needs no water, power or supplies. Learn to hand express in case your pump has no power, and keep a cooler and ice packs for stored milk."),
    ("How many diapers do I need?",
     "Count how many your child uses in a day and multiply by 14 for a two-week supply. Newborns go through far more than toddlers, so update the kit when you change sizes."),
    ("What medicines should be in a baby emergency kit?",
     "Any prescriptions (ask your pediatrician for a two-week supply), a thermometer, and the infant fever reducer your pediatrician recommends, with their dosing chart for your child's weight. Doses for babies depend on weight and product, so ask your pediatrician or pharmacist rather than guessing."),
]

SOURCES = [
    ("CDC: Special considerations for infant feeding in emergencies", "https://www.cdc.gov/infant-feeding-emergencies-toolkit/php/special-considerations.html"),
    ("CDC: Prepare and store powdered infant formula in an emergency", "https://www.cdc.gov/infant-feeding-emergencies-toolkit/php/powdered-infant-formula.html"),
    ("American Academy of Pediatrics (HealthyChildren.org): Family disaster supplies list", "https://www.healthychildren.org/English/safety-prevention/at-home/pages/Family-Disaster-Supplies-List.aspx"),
    ("American Academy of Pediatrics (HealthyChildren.org): Getting your family disaster ready", "https://healthychildren.org/English/safety-prevention/at-home/Pages/Getting-Your-Family-Disaster-Ready.aspx"),
    ("Ready.gov: Make a plan", "https://www.ready.gov/plan"),
]

RELATED = [("Go-bags and evacuation guide", "go-bag.html"), ("Food storage calculator", "../food-calculator.html"),
           ("Water storage calculator", "../water-calculator.html"), ("Losing power in a winter storm", "winter-storm-power-outage.html"),
           ("Older adults and people with disabilities", "older-adults-disabilities.html"), ("Get your PrepScore", "../quiz.html")]
CALC_LINK = ("To work out water for the whole household, including a baby, use the", "../water-calculator.html", "water calculator")
