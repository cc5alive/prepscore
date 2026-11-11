"""Food storage calculator: planning figures, example pantry items, FAQ and sources.

Calorie planning figures follow the ranges in the Dietary Guidelines for Americans
(adults roughly 1,600 to 3,000 kcal a day; children 4 to 13 roughly 1,200 to 2,600).
Pantry items use typical label calories; the page says brands vary.
"""

KCAL = {"adult": 2000, "adult_active": 2500, "child": 1400}

# id, name, unit, kcal per unit, share of calories (no-cook), share (with a stove), note
PANTRY = [
    ("pb", "Peanut butter", "16 oz jar", 2600, 0.22, 0.17, "Or another nut or seed butter"),
    ("nuts", "Trail mix, nuts or dried fruit", "1 lb bag", 2100, 0.22, 0.12, ""),
    ("crackers", "Crackers", "1 lb box", 1900, 0.15, 0.05, "Whole-grain keeps you fuller"),
    ("bars", "Granola or protein bars", "bar", 200, 0.1, 0.05, "Or 3,600-calorie ration bars"),
    ("beans", "Canned beans, chili or soup (ready to eat)", "15 oz can", 380, 0.23, 0.15, "Eat cold from the can if you must"),
    ("tuna", "Canned tuna or chicken", "5 oz can", 150, 0.03, 0.03, ""),
    ("fruitveg", "Canned fruit and vegetables", "15 oz can", 150, 0.05, 0.05, "Pick fruit packed in juice"),
    ("rice", "White rice", "1 lb bag", 1650, 0.0, 0.17, "Needs about 2 cups of water per cup of rice"),
    ("oats", "Rolled oats", "42 oz canister", 4500, 0.0, 0.1, ""),
    ("pasta", "Pasta", "1 lb box", 1600, 0.0, 0.11, "Needs a pot of water to cook"),
]

FAQ = [
    ("How much food should I store per person?",
     "Plan on about 2,000 calories per adult per day, more for people doing hard physical work, and about 1,400 for younger children. Store at least 3 days, and build toward two weeks. Many local emergency agencies recommend two weeks after a major earthquake or hurricane."),
    ("How many calories do you need in an emergency?",
     "About what you eat now. The Dietary Guidelines for Americans put most adults between 1,600 and 3,000 calories a day depending on age, sex and activity. Clearing debris, evacuating on foot or staying warm in a cold house burns more, so don't plan on eating less."),
    ("What's the best food to store?",
     "Food your household already eats, that keeps for months without a fridge and needs little or no cooking: peanut butter, canned beans and soups, canned fish and chicken, crackers, nuts, dried fruit, cereal and bars. If you have a camp stove, add rice, oats and pasta. Keep a manual can opener with it."),
    ("Do I need special emergency food?",
     "No. A deeper everyday pantry, used and replaced as you go, covers most emergencies. Freeze-dried meals and ration bars are useful for a go-bag, a car, or food you want to store for years without rotating."),
    ("How long does canned food last?",
     "The USDA says high-acid canned foods like tomatoes and fruit keep their best quality for 12 to 18 months, and low-acid foods like beans, meat and vegetables for 2 to 5 years. Cans that bulge, leak, rust deeply or spurt when opened should be thrown out."),
    ("How do I keep my stored food from going to waste?",
     "Rotate it: put new groceries at the back and eat from the front. Write the purchase month on cans with a marker, and check the whole stash twice a year, when the clocks change."),
    ("What about babies, special diets and pets?",
     "Store at least two weeks of formula or baby food, any foods needed for allergies or medical diets, and pet food in a sealed container. These are the hardest things to find in a store after a disaster."),
]

SOURCES = [
    ("Ready.gov: Food", "https://www.ready.gov/food"),
    ("Dietary Guidelines for Americans", "https://www.dietaryguidelines.gov/"),
    ("USDA FSIS: Shelf-stable food safety", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/shelf-stable-food"),
    ("USDA FSIS: Keep your food safe during emergencies", "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/emergencies/keep-your-food-safe-during-emergencies"),
]
