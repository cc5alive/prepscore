"""Buyer page: Sawyer Squeeze vs LifeStraw (/guides/sawyer-squeeze-vs-lifestraw)."""

SLUG = "sawyer-squeeze-vs-lifestraw"
PARENT = "water"
OG = "guide-sawyer-lifestraw"
OG_CARD = ("Water filters", "Sawyer Squeeze vs LifeStraw", "Which emergency water filter to buy, what each removes, and what neither one does.")
TITLE = "Sawyer Squeeze vs LifeStraw: Which Water Filter for Emergencies?"
META = ("Sawyer Squeeze vs LifeStraw for emergency water: pore size, what each removes, how long it lasts, whether it can fill a pot "
        "for your household, and what neither filter removes.")
H1 = "Sawyer Squeeze vs LifeStraw"
DEK = ("The two best-known budget water filters, compared for emergencies at home rather than for hiking. The short version: they "
       "remove the same kinds of germs, but only one can easily make water for a whole household.")
REVIEWED = "CDC and Minnesota Department of Health water-treatment guidance and manufacturer specifications"
CRUMB = "Sawyer vs LifeStraw"

GRID_TOC = "Side by side"
GRID = ("Side by side",
        "From each maker's published specifications. All three are hollow-fiber membrane filters.",
        ["", "Sawyer Squeeze", "LifeStraw Personal", "LifeStraw Peak Solo"],
        [["Pore size", "0.1 micron (absolute)", "0.2 micron", "0.2 micron"],
         ["Bacteria removed", "99.99999%", "99.999999%", "99.999999%"],
         ["Parasites (Giardia, Crypto)", "99.9999%", "99.999%", "99.999%"],
         ["Viruses", "No", "No", "No"],
         ["Chemicals, chlorine, salt", "No", "No", "No"],
         ["Rated life", "Up to 100,000 gallons", "1,000 gallons (4,000 L)", "About 500 gallons (2,000 L)"],
         ["How you use it", "Squeeze a pouch or bottle into a container, inline on a tube, or as a gravity filter", "Drink straight from the source", "Drink from the source, or screw onto a standard bottle"],
         ["Can fill a pot or jug", "Yes", "No", "Yes, by squeezing a soft bottle"],
         ["Filter weight", "About 3 oz", "About 2 oz", "About 1.7 oz"],
         ["Price band", "$$", "$", "$"]])

VERDICT = [
    ("For a home emergency kit, get the Sawyer Squeeze.", "It can fill pots and jugs for everyone in the house, it's rated for far more water, and you can backflush it to restore the flow."),
    ("A LifeStraw Personal is a one-person backup.", "You drink through it straight from the source, so it can't make water for cooking, a child or a pet. It's cheap and light, which makes it a good extra for a car or go-bag."),
    ("Neither removes viruses or chemicals.", "If the source could contain sewage, such as a stream after heavy rain, also treat the water with tablets or boil it. Never drink floodwater or water that may contain fuel or chemicals; these filters won't make it safe."),
    ("Don't let either one freeze.", "Ice can crack the fibers without any sign, letting germs through. Store the filter indoors, and replace it if it may have frozen."),
    ("Under a boil-water notice, boil.", "Follow the notice from your water utility: boil tap water or use bottled water. A filter alone isn't a substitute."),
]

STEPS_TITLE = "Using a squeeze filter in an emergency"
STEPS = [
    ("Pick the clearest water you have", "Rain barrels, a lake or stream, or a pool for the last resort (see our pool water page first). Let cloudy water settle, or pour it through a cloth."),
    ("Fill the pouch or soft bottle", "Use the dirty-water pouch only for dirty water. Mark it so nobody drinks from it by mistake."),
    ("Squeeze into a clean container", "Screw on the filter and squeeze steadily into a clean pot or jug. Don't let the filter's clean end touch the dirty pouch or water."),
    ("Add tablets if viruses are a risk", "If the source could contain sewage, treat the filtered water with purification tablets or boil it."),
    ("Backflush when the flow slows", "Push clean water back through the filter with the included plunger. It takes a minute and restores most of the flow."),
    ("Keep it dry and warm between uses", "Shake out the water, store it where it can't freeze, and keep the caps on both ends."),
]

SECTIONS = [
    ("Which other filter to consider", [
        ("Sawyer Mini", "The same 0.1 micron filtration as the Squeeze in a smaller body, for less money. It flows more slowly, which matters when you're filtering gallons."),
        ("A gravity filter", "For a family, a gravity bag filter does the squeezing for you: hang it up and it fills a pot while you do something else. See the picks in our water guide."),
        ("A virus-rated purifier", "If you expect to use water that may contain sewage, look for a purifier rated for viruses, or plan to add tablets every time."),
        ("Tablets and bleach", "Chemical treatment kills viruses that filters miss and weighs almost nothing. It doesn't remove dirt or Cryptosporidium as reliably, so many people carry both."),
    ]),
]

PICKS = [
    {"name": "Sawyer Squeeze filter", "asin": "B0DTJJ88BR", "asin_name": "Sawyer Squeeze with a 1-liter bottle (SP302)", "price": "$45 to $65",
     "what": "A palm-sized 0.1 micron hollow-fiber filter with a soft 1-liter bottle, a cleaning plunger and a coupling.",
     "why": "Fills pots and jugs for a household, screws onto standard bottles, backflushes in a minute and is rated up to 100,000 gallons.",
     "watch": "Doesn't remove viruses or chemicals. The soft pouches and bottles wear out before the filter; extra ones are cheap.",
     "best": "Home kits and families"},
    {"name": "LifeStraw Personal", "asin": "B006QF3TW4", "price": "$15 to $25",
     "what": "The original straw filter: you drink through it straight from the water.",
     "why": "Cheap, very light and simple. A good backup for a car, desk or go-bag.",
     "watch": "Can't fill a container, so it won't help with cooking or anyone who can't use a straw. Rated for 1,000 gallons.",
     "best": "A one-person backup"},
    {"name": "LifeStraw Peak Solo", "asin": "B0CVJ7R5BS", "price": "$20 to $30",
     "what": "A small LifeStraw filter you can drink through or screw onto a standard bottle.",
     "why": "More versatile than the original straw: squeeze a soft bottle through it to fill a cup or pot.",
     "watch": "Rated for about 2,000 liters, a fraction of the Sawyer's rating. Doesn't remove viruses or chemicals.",
     "best": "Go-bags and light kits"},
    {"name": "Sawyer Mini", "asin": "B00FA2RLX2", "price": "$20 to $35",
     "what": "Sawyer's smaller filter with the same 0.1 micron rating, a 16-ounce pouch and a straw.",
     "why": "The same filtration as the Squeeze for less money and weight.",
     "watch": "Slower flow, which gets tiring when you're filtering for several people.",
     "best": "A budget filter for one or two people"},
    {"name": "Water purification tablets", "asin": "B09B2TVKGB", "asin_name": "Aquatabs 49mg, 100-pack", "price": "$10 to $25",
     "what": "Chlorine tablets that disinfect water, including the viruses filters miss.",
     "why": "Pairs with either filter for water that may contain sewage, and weighs almost nothing.",
     "watch": "Follow the label for dose and wait time. Doesn't remove dirt, and less effective against Cryptosporidium.",
     "best": "Adding virus protection"},
]

FAQS = [
    ("Is the Sawyer Squeeze better than LifeStraw?",
     "For emergencies at home, usually yes. Both remove bacteria and parasites, but the Sawyer can fill containers for a whole household and is rated for far more water. A LifeStraw Personal is cheaper and lighter, and fine as a one-person backup."),
    ("Does a Sawyer or LifeStraw remove viruses?",
     "No. Their pores are 0.1 and 0.2 micron, too large to block viruses reliably. The CDC says filters like these remove bacteria and parasites but not viruses. Add purification tablets or boil the water if viruses are a risk."),
    ("Can I use a water filter during a boil-water notice?",
     "Follow your utility's notice, which usually means boiling tap water or using bottled water. These filters don't remove viruses, so they aren't a substitute for boiling."),
    ("How long does a Sawyer Squeeze last?",
     "Sawyer rates it up to 100,000 gallons and backs it with a lifetime limited warranty. In practice the flow slows as it clogs; backflushing restores most of it."),
    ("What happens if my water filter freezes?",
     "Ice can damage the hollow fibers so that germs get through, and you can't see the damage. Keep filters where they won't freeze, and replace one that may have frozen."),
    ("Can I filter pool water with a Sawyer or LifeStraw?",
     "Not by itself. Neither removes chlorine, salt or the chemicals in pool water. See our pool water page for what does."),
]

SOURCES = [
    ("CDC: Water treatment options when hiking, camping or traveling", "https://cdc.gov/drinking-water/prevention/water-treatment-hiking-camping-traveling.html"),
    ("Minnesota Department of Health: Water treatment in the backcountry", "https://www.health.state.mn.us/diseases/waterborne/prevention/backcountry.html"),
    ("Sawyer: Water filtration FAQs", "https://sawyer.com/water-filtration/faqs"),
    ("LifeStraw Personal: Filtration performance sheet (PDF)", "https://cdn.shopify.com/s/files/1/2631/0778/files/LifeStraw_-_Personal_Water_Filter_-_Filtration_Performance_Sheet.pdf"),
]

RELATED = [("Emergency water guide", "water.html"), ("Water storage for apartments", "apartment-water-storage.html"),
           ("Drinking pool water", "pool-water.html"), ("Water storage calculator", "../water-calculator.html")]
