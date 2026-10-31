"""Content for /guides/pool-water: making chlorinated and saltwater pool water drinkable as a last resort."""

TITLE = "Can You Drink Pool Water? Chlorine and Saltwater Pools Explained"
META = ("Official agencies say don't drink pool water. Here's what's in it, why a filter alone isn't enough, "
        "and the gear that makes chlorinated and saltwater pool water drinkable as a last resort.")
H1 = "Can you drink your pool water in an emergency?"
DEK = ("Not straight from the pool, and not through a filter alone. A backyard pool holds years of water for a household, "
       "but making it drinkable means removing chemicals and, in a saltwater pool, salt. Here's what that takes.")

HOWMUCH = [
    ("A 15 × 30 ft pool", "≈17,000 gal", "at a 5 ft average depth. Years of drinking water for a family of four."),
    ("Salt in a saltwater pool", "3,200 ppm", "the level salt systems aim for. Nearly 8× the EPA guideline for chloride."),
    ("Stabilizer in many pools", "30–100 ppm", "of cyanuric acid. The WHO drinking-water guideline is 40."),
    ("Distilling 1 gallon", "≈2.7 kWh", "of heat. Roughly a 1 lb propane canister on a camp stove."),
]

VERDICT = [
    ("Use it for everything except drinking, first.", "The CDC says pool and spa water is fine for personal hygiene and cleaning, but not for drinking. Flushing toilets, washing and cleaning with pool water stretches your stored drinking water much further."),
    ("A filter alone isn't enough.", "Camping filters remove germs. Some also remove chlorine and taste. None remove salt or pool stabilizer, which stay dissolved in the water."),
    ("Boiling makes it worse.", "Boiling kills germs, but chemicals and salt stay behind and get more concentrated as water boils off."),
    ("To drink it, distill it or run it through reverse osmosis.", "Those are the only home methods that remove dissolved salt and chemicals. Then polish it with a carbon filter and check it with a TDS meter."),
]

# name, typical level, guideline, what removes it
CONTAMINANTS = [
    ("Germs, including Crypto", "Chlorine kills most quickly. Crypto survives more than 7 days in properly chlorinated water, and once the pump stops, chlorine fades and algae grows.", "None should be present", "A 0.1-micron or finer filter, a purifier, distillation or RO"),
    ("Chlorine", "1–4 ppm in a maintained pool", "Not the main risk, but it tastes bad", "Activated carbon, KDF, or letting it sit uncovered in sun"),
    ("Cyanuric acid (stabilizer)", "30–100+ ppm in outdoor pools", "WHO: 40 mg/L", "Only distillation or reverse osmosis. It doesn't break down, and pools can only lower it by draining."),
    ("Salt (saltwater pools)", "2,700–3,400 ppm", "EPA chloride guideline: 250 mg/L", "Only distillation or reverse osmosis"),
    ("Copper", "From copper algaecides, ionizers or corroding heaters", "EPA: 1.0 mg/L", "Distillation or RO. KDF and carbon reduce some."),
    ("Total dissolved solids", "Rise every time chemicals are added and water evaporates", "EPA: 500 mg/L", "Only distillation or reverse osmosis"),
    ("Flood water, fuel, wildfire ash", "Anything that washed or blew in", "CDC: water with fuel or toxic chemicals can't be made safe", "Don't drink it. Use it for flushing only, if at all."),
]

BEFORE = [
    "Test your pool now for cyanuric acid, copper and salt, and measure total dissolved solids (TDS) with a meter. Write the numbers down.",
    "If the pool is part of your water plan, keep cyanuric acid at the low end (30 to 50 ppm) and skip copper algaecides and ionizers.",
    "Work out your pool's volume: length × width × average depth in feet × 7.5 = gallons.",
    "Buy the gear before you need it: a way to distill or run RO, a carbon filter, a TDS meter and test strips.",
    "Have a pool cover, or at least a tarp, to keep out debris, ash and animals during a disaster.",
]

CHLORINE_STEPS = [
    ("Use it for non-drinking jobs first", "Flush toilets with a bucket, wash and clean with pool water. Keep your stored water for drinking and cooking."),
    ("Stop adding anything except plain chlorine", "No algaecides, clarifiers, phosphate removers or stabilizer while you may be drinking from it."),
    ("Draw clean water", "Dip from the middle of the pool, below the surface and away from the steps and skimmer. Pour it through a clean cloth and let sediment settle."),
    ("Distill it, or run it through reverse osmosis", "Distillation is the most reliable at home: it leaves the chlorine salts, stabilizer, copper and minerals behind. A countertop RO unit is a good second choice if you have power."),
    ("Polish it with a carbon filter", "A filter with activated carbon removes any chlorine smell that carried over and improves taste. This is where a 3-stage filter earns its place."),
    ("Check it with a TDS meter", "Distilled water should read close to zero. Anything you drink should be under 500 ppm, the EPA guideline. If it reads high, treat it again."),
]

SALT_STEPS = [
    ("Know what you're dealing with", "A saltwater pool is a chlorine pool. The salt cell makes chlorine from dissolved salt, and most outdoor salt pools also use stabilizer. Everything about chlorine pools applies, plus the salt."),
    ("Don't drink it filtered or boiled", "No camping filter, pump or carbon stage removes salt, whatever the listing says. Boiling concentrates it."),
    ("Distill it or use reverse osmosis", "Distillation removes salt completely. A countertop RO unit is built for tap water, so on salt pool water it will run slower, waste more water and wear its membrane faster. Check its output every time."),
    ("Polish with carbon and test", "Run the distilled or RO water through a carbon filter, then check it with a TDS meter. Under 500 ppm is the bar; distilled should be close to zero."),
]

SALT_FACTS = [
    "Salt systems aim for about 3,200 ppm, roughly a tenth as salty as seawater, but far above drinking-water guidelines.",
    "At 3,200 ppm, each liter carries about 1,260 mg of sodium. Two liters is more than the 2,300 mg daily limit in U.S. dietary guidance, before you eat anything.",
    "That load is riskiest for babies, older adults and anyone with kidney disease, heart failure or high blood pressure.",
]

LAST_RESORT = ("If you have no way to distill or run RO, a chlorine-only pool (never a salt pool) is the least-bad case. "
               "That's only if your tested numbers are low (TDS under 500 ppm, cyanuric acid under 40, no copper), "
               "nothing flooded or blew into it, and you run it through a filter with carbon and a 0.1-micron or finer membrane. "
               "Official guidance still says don't drink it. Treat this as a bridge until you can get safe water.")

# CC's own purchase
CC_PICK = {
    "name": "EmbraceYe 3-stage hand pump filter",
    "asin": "B0CTK2FNQ8",
    "price": "$50",
    "stages": [
        ("KDF", "Reduces chlorine and some dissolved metals, such as copper and lead."),
        ("Activated carbon fiber", "Removes chlorine taste and smell, and some organic chemicals."),
        ("0.01-micron hollow fiber", "Physically blocks bacteria and protozoa, according to the maker."),
    ],
    "limits": ("What it can't do: remove salt, stabilizer, calcium or most dissolved solids. The listing says it reduces TDS, "
               "but none of its stages are built for that, so check its output with a TDS meter. The listing cites NSF/ANSI test "
               "standards without showing a certification, so treat its claims as the maker's. It's rated for 2,000 liters, and "
               "chlorinated water uses up carbon faster."),
}
CC_NOTE = ("I bought this filter for my own kit because of its three stages: carbon and KDF for chlorine on top of a fine membrane for germs. "
           "Researching this page changed how I'll use it. For pool water it's the final step after distilling, not the whole answer. "
           "It's also my everyday filter for rain barrels and lakes.")

# Alternatives to CC's filter: name, asin, price, kind, germs, chlorine/taste, salt+stabilizer, note
FILTERS = [
    ("EmbraceYe 3-stage pump (CC's pick)", "B0CTK2FNQ8", "$50", "Hand pump: KDF, carbon, 0.01 µm hollow fiber", "Bacteria, protozoa", "Yes", "No", "Most features for the money; claims aren't independently certified."),
    ("Sawyer Squeeze", "B00B1OSU4W", "$35–50", "Squeeze filter: 0.1 µm hollow fiber", "Bacteria, protozoa", "No", "No", "The best-known budget filter. No carbon, so pair it with a carbon stage for pool water."),
    ("GRAYL GeoPress", "B09255PYRM", "$100", "Press bottle purifier with carbon", "Bacteria, protozoa, viruses", "Yes", "No", "Removes viruses too, and the carbon handles chlorine. Only 24 oz at a time."),
    ("MSR Guardian", "B0CQRX4FT2", "$400", "Pump purifier", "Bacteria, protozoa, viruses", "No", "No", "Tested to the U.S. military's purifier protocol and self-cleans as you pump. No carbon stage."),
    ("Platypus GravityWorks 4L", "B0CV9RPT8Y", "$135", "Gravity bag filter: 0.2 µm hollow fiber", "Bacteria, protozoa", "No", "No", "Filters liters at a time with no pumping, the easiest for a family. Add carbon for taste."),
]

# Gear that actually removes salt and stabilizer, plus testing
GEAR = [
    ("Countertop distiller (CO-Z 4L)", "B078GHJ921", "$120", "Electric distiller: 750 W, about 0.3 gal an hour, glass pot.", "The budget way to remove salt, stabilizer and metals. Needs about 2.5 kWh a gallon, so plan on a generator, a home battery or the grid."),
    ("Countertop distiller (Megahome)", "B000ANW7HQ", "$300", "Stainless distiller with a glass collection jug, 1 gallon every 5.5 hours.", "Better built and widely recommended. Water doesn't touch plastic."),
    ("Countertop reverse osmosis (Bluevua RO100ROPOT)", "B09KRDK677", "$390", "No-install RO with a carbon pre-filter, an output TDS display and a glass carafe.", "Faster and uses less power than distilling. Built for tap water, so expect slower output and shorter filter life on salt pool water."),
    ("TDS meter (HM Digital TDS-3)", "B000VTQM70", "$15", "Reads 0 to 9,990 ppm, so it covers salt pools.", "The cheapest way to know your treated water is actually clean. Distilled should read near zero."),
    ("9-in-1 pool test strips", "B0FD9RJ6RH", "$14", "Strips that read salt, cyanuric acid, copper, chlorine and hardness.", "Tells you what's in your pool before an emergency. Strips are rough, so treat the results as ranges."),
]

NO_POWER = [
    "Pot still: put a heat-safe bowl on a rack inside a large pot of pool water, set the lid on upside down, and put ice or cold water on the lid. Steam condenses on the lid and drips into the bowl.",
    "Run it outdoors on a camp stove, never indoors. Expect roughly a 1 lb propane canister per gallon, so it suits drinking water for one or two people, not the household.",
    "Solar stills work, but slowly: plan on cups a day, not gallons.",
]

FAQS = [
    ("Can you drink pool water if you boil it?",
     "No. Boiling kills germs, but chlorine byproducts, stabilizer, copper and salt stay behind and get more concentrated as water evaporates. You need to catch and condense the steam, which is distillation."),
    ("Will a LifeStraw or Sawyer make pool water safe?",
     "Not on its own. Those filters remove bacteria and protozoa, but pool water's main problem is dissolved chemicals, and in a saltwater pool, salt. They work well as a step after distilling, not instead of it."),
    ("Is saltwater pool water like seawater?",
     "No. It's about a tenth as salty as seawater, but at around 3,200 ppm it's still far above drinking-water guidelines and can't be filtered. It needs distillation or reverse osmosis."),
    ("Can I flush toilets with pool water?",
     "Yes. The CDC says pool water can be used for hygiene and cleaning. Pour a bucket into the toilet bowl to flush. This is the best use of a pool in an outage or water main break."),
    ("How long does pool water stay usable without power?",
     "Without the pump and chlorine, warm pools can turn green within days. Green water is still fine for flushing. To drink it, distill it, and pre-filter algae through cloth first."),
    ("What about hot tubs and spas?",
     "The same rules apply, and the CDC and FEMA include spas in their warnings. Spa water is hotter, more concentrated and often uses bromine, so distill it if you drink it at all."),
]

SOURCES = [
    ("CDC: Finding other water sources in an emergency", "https://www.cdc.gov/healthywater/emergency/finding-other-sources.html"),
    ("FEMA: Emergency water sources if you run out of clean water", "https://www.fema.gov/node/what-are-emergency-water-sources-if-im-running-out-clean-water"),
    ("CDC: Preventing swimming-related illnesses (Crypto survival in chlorine)", "https://www.cdc.gov/healthy-swimming/prevention/index.html"),
    ("WHO: Sodium dichloroisocyanurate fact sheet (cyanuric acid guideline)", "https://www.who.int/docs/default-source/wash-documents/wash-chemicals/sodium-dichloroisocyanurate-chemical-fact-sheet.pdf"),
    ("EPA: Secondary drinking water standards, 40 CFR 143.3", "https://www.ecfr.gov/current/title-40/chapter-I/subchapter-D/part-143"),
    ("Oregon Health Authority: Cyanuric acid in pools", "https://www.oregon.gov/oha/PH/HEALTHYENVIRONMENTS/RECREATION/POOLSLODGING/Documents/FactSheet6CyanuricAcid.pdf"),
    ("Hayward: How much salt a salt system requires", "https://www.hayward.com/knowledge-base/how-much-salt-does-the-system-require/"),
    ("FDA: Sodium in your diet", "https://www.fda.gov/food/nutrition-education-resources-materials/sodium-your-diet"),
]

# City pages that get a "Have a pool?" link (hot, pool-heavy metros)
POOL_CITIES = {"los-angeles", "san-diego", "phoenix", "miami", "tampa", "orlando", "houston", "dallas", "new-orleans"}
