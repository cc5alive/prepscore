"""Content for /library: free printable survival guides (PDF) and the best prepper books."""

TITLE = "Free Printable Survival Guides (PDF) and Best Prepper Books"
META = ("Free survival and emergency guides you can download and print, from FEMA, the CDC, the U.S. Army and Hesperian, "
        "plus the best prepper and survival books, with what each is best for.")
H1 = "The prepper's library: free printable guides and the best books"
DEK = ("When the power and internet are out, the guide on your phone won't help. Print the essentials now, "
       "keep them in a binder with your kit, and add a few good books for the skills that take longer to learn.")

PRINT_TIPS = [
    "Start with the first section: the supply checklist, the family plan and the wallet cards.",
    "Put printouts in sheet protectors in a binder, and keep it with your kit or go-bag.",
    "Fill in the family plan and wallet cards by hand, and give a copy to everyone in the house.",
    "Long guides don't need printing cover to cover. Print the chapters you'd actually need, and save the full PDF to a USB drive.",
    "Review the binder twice a year, when you check your kit.",
]

# (title, url, publisher, kind ["PDF" or "Download page"], best_for, about)
PDF_SECTIONS = [
    ("print-first", "Print these first", "Short checklists and forms. Fill them in, put them in your kit.", [
        ("Emergency supply kit checklist", "https://www.ready.gov/sites/default/files/2024-05/ready_supply-kit-checklist.pdf", "Ready.gov (FEMA)", "PDF",
         "Checking off your kit as you build it.", "The official list of basic supplies, plus extras for babies, pets, older adults and medical needs."),
        ("Family emergency communication plan", "https://www.ready.gov/sites/default/files/2021-04/family-emergency-communication-plan.pdf", "Ready.gov (FEMA)", "PDF",
         "Writing down how your household will reach each other and where you'll meet.", "A fill-in form for phone numbers, an out-of-town contact, meeting places and school or work plans."),
        ("Family communication plan wallet cards", "https://www.ready.gov/sites/default/files/2025-06/family-communication-plan_fillable-card.pdf", "Ready.gov (FEMA)", "PDF",
         "A card for every wallet and backpack.", "Fillable cards with key numbers and meeting places, for when phones are dead and nobody remembers a number."),
        ("Be Red Cross Ready checklist", "https://www.redcross.org/content/dam/redcross/atg/PDF_s/Preparedness___Disaster_Recovery/Disaster_Preparedness/Be-Red-Cross-Ready-Preparedness-Factsheet.pdf", "American Red Cross", "PDF",
         "A one-glance summary to post on the fridge.", "Get a kit, make a plan, be informed, in a few pages, with emergency contact cards."),
        ("Emergency Financial First Aid Kit", "https://www.ready.gov/sites/default/files/2020-03/ready_emergency-financial-first-aid-toolkit.pdf", "FEMA and Operation Hope", "PDF",
         "Gathering the documents and account details you'd need to rebuild.", "Checklists and forms for IDs, insurance, medical records, bank accounts and bills."),
        ("Pet owners fact sheet", "https://www.ready.gov/sites/default/files/2020-04/pet-owners-fact-sheet_printer-friendly.pdf", "Ready.gov (FEMA)", "PDF",
         "Making a plan and a kit for your pets.", "What to pack for each pet and how to plan for shelters that don't take animals."),
    ]),
    ("guides", "In-depth guides", "Longer references worth saving and printing in part.", [
        ("Are You Ready? An In-Depth Guide to Citizen Preparedness", "https://www.ready.gov/sites/default/files/2021-11/are-you-ready-guide.pdf", "FEMA", "PDF",
         "One printed reference that covers every common disaster.", "FEMA's book-length guide: plans and kits, then what to do before, during and after floods, fires, quakes, storms, pandemics and more. Also in Spanish on Ready.gov."),
        ("In Case of Crisis or War", "https://www.mcf.se/en/advice-for-individuals/the-brochure-in-case-of-crisis-or-war/", "Swedish Civil Defence and Resilience Agency", "Download page",
         "A short, well-designed take on preparing for a week without normal services.", "The brochure Sweden mails to every household, in English. Its home-preparedness advice works anywhere."),
        ("Putting Down Roots in Earthquake Country", "https://pubs.usgs.gov/gip/2005/15/gip-15.pdf", "USGS", "PDF",
         "Earthquake prep in detail, with the Seven Steps to Earthquake Safety.", "The San Francisco Bay Area edition, but most of its advice applies in any earthquake region."),
    ]),
    ("medical", "Medical", "For when help is far away or delayed.", [
        ("Where There Is No Doctor", "https://languages.hesperian.org/pages/en/pdf.html", "Hesperian Health Guides", "Download page",
         "Recognizing and treating common illnesses and injuries without a doctor.", "The classic village health care handbook, free to download chapter by chapter. Hesperian asks people who can afford it to buy a copy or donate."),
        ("Where There Is No Dentist", "https://languages.hesperian.org/pages/en/pdf.html", "Hesperian Health Guides", "Download page",
         "Handling tooth pain, infections and dental emergencies.", "The dental companion to Where There Is No Doctor, on the same download page."),
    ]),
    ("water-food", "Water and food", "Exact methods you'll want on paper.", [
        ("Make Water Safe During an Emergency", "https://www.cdc.gov/water-emergency/media/pdfs/make-water-safe-during-emergency-p.pdf", "CDC", "PDF",
         "Boiling and disinfecting water, with bleach amounts.", "A short reference to tape inside a cabinet door."),
        ("USDA Complete Guide to Home Canning", "https://nchfp.uga.edu/resources/entry/about-the-usda-guide-to-home-canning-2015-revision", "USDA, via the National Center for Home Food Preservation", "Download page",
         "Safe, tested canning times and methods.", "The reference standard for home canning, free in eight parts. Print the principles and the sections for foods you actually can."),
    ]),
    ("grid-down", "Wilderness and grid-down", "Deeper skills for longer, rougher situations.", [
        ("U.S. Army ATP 3-50.21: Survival", "https://irp.fas.org/doddir/army/atp3-50-21.pdf", "U.S. Army, hosted by the Federation of American Scientists", "PDF",
         "Shelter, water, fire, food and navigation outdoors.", "The Army's current survival manual and a successor to the classic FM 21-76. Approved for public release."),
        ("Nuclear War Survival Skills", "https://apps.dtic.mil/sti/html/tr/ADA328301/index.html", "Oak Ridge National Laboratory, via DTIC", "Download page",
         "Fallout, shelter and ventilation in a worst-case scenario.", "Cresson Kearny's 1987 civil defense manual, tested by researchers at Oak Ridge. Grim, but practical and still widely cited."),
    ]),
]

# Books: (title, author, asin, price, best_for, why)
BOOK_SECTIONS = [
    ("start-books", "Start here", [
        ("The Prepper's Blueprint", "Tess Pennington", "1496092589", "about $20",
         "A step-by-step plan, a layer at a time.",
         "Breaks preparedness into short, ordered steps with checklists, from a basic kit up to longer emergencies. Good if you want a path to follow."),
        ("Handbook to Practical Disaster Preparedness for the Family (3rd ed.)", "Arthur T. Bradley", "1475136536", "about $25",
         "The most complete single book on household preparedness.",
         "Water, food, power, sanitation, communications, security and medical, written clearly and practically for families."),
        ("Just in Case", "Kathy Harrison", "1603420355", "about $16",
         "A friendly, home-focused start.",
         "Practical self-sufficiency for ordinary families: pantry, power outages, heat and keeping kids calm."),
    ]),
    ("medical-books", "Medical", [
        ("Where There Is No Doctor", "David Werner", "0942364155", "about $29",
         "The paper copy of the free classic.",
         "Worth owning in print even though the PDF is free, because you'll want it when nothing works."),
        ("The Survival Medicine Handbook (4th ed.)", "Joseph Alton MD and Amy Alton ARNP", "0988872501", "about $38",
         "Medical care when help isn't coming.",
         "Written for disasters rather than remote villages: wounds, infections, fractures, medications and what to stock."),
    ]),
    ("skills-books", "Skills and wilderness", [
        ("SAS Survival Handbook (3rd ed.)", "John “Lofty” Wiseman", "0062378074", "about $13",
         "The classic all-round survival reference.",
         "Shelter, water, fire, food, navigation and first aid in every climate, from a longtime SAS survival instructor."),
        ("Bushcraft 101", "Dave Canterbury", "1440579776", "about $16",
         "Outdoor skills with a small kit.",
         "Fire, shelter, cordage and tools, built around the idea that knowledge weighs less than gear."),
        ("98.6 Degrees", "Cody Lundin", "1586852345", "about $20",
         "Staying warm, hydrated and alive in the first hours.",
         "Funny and practical on the body's needs in a crisis and what to carry. The title is crude; the advice is solid."),
    ]),
    ("long-books", "Self-reliance and long emergencies", [
        ("When Technology Fails (Revised and Expanded)", "Matthew Stein", "1645023478", "about $28",
         "Long-term self-reliance.",
         "Water, food, energy, medicine and shelter when systems are down for a long time."),
        ("Ball Complete Book of Home Preserving", "Judi Kingry and Lauren Devine", "0778801314", "about $24",
         "Canning and preserving with tested recipes.",
         "Hundreds of recipes from the jar maker's test kitchen, with step-by-step methods."),
        ("ARRL Ham Radio License Manual (6th ed.)", "ARRL", "1625952392", "about $33",
         "Passing the Technician exam for a ham radio license.",
         "The current edition of the standard study guide, with the question pool and explanations."),
    ]),
    ("mind-books", "Mindset", [
        ("The Unthinkable (Revised and Updated)", "Amanda Ripley", "0593796721", "about $19",
         "Understanding how people actually behave in disasters.",
         "Why some people freeze and others act, and how to train yourself to be the one who acts."),
        ("Deep Survival", "Laurence Gonzales", "0393353710", "about $16",
         "The psychology of who lives and who dies.",
         "Real survival stories and the habits of mind that made the difference."),
    ]),
]
