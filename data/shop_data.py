"""
Shop data for Rocen Homesteady.
Affiliate links, digital products, and seasonal recommendations.

Amazon Associates ID: rocehomestead-21
Buy Me a Coffee: buymeacoffee.com/rocehomesteady
"""

AMAZON_TAG = "rocehomestead-21"
BMC_URL = "https://buymeacoffee.com/rocehomesteady"

SEASON_PRODUCTS = {
    "Spring": {
        "name": "Spring Foraging Kit",
        "desc": "Everything you need for spring wild garlic and nettles",
        "url": f"https://www.amazon.co.uk/s?k=foraging+knife+basket+spring&tag={AMAZON_TAG}",
        "emoji": "🌸",
    },
    "Summer": {
        "name": "Summer Foraging Kit",
        "desc": "Berry-picking essentials for hedgerow harvests",
        "url": f"https://www.amazon.co.uk/s?k=foraging+bag+basket+summer&tag={AMAZON_TAG}",
        "emoji": "☀️",
    },
    "Autumn": {
        "name": "Autumn Mushroom Kit",
        "desc": "Mushroom hunting gear for the peak fungi season",
        "url": f"https://www.amazon.co.uk/s?k=mushroom+hunting+kit+identification&tag={AMAZON_TAG}",
        "emoji": "🍂",
    },
    "Winter": {
        "name": "Winter Foraging Guide",
        "desc": "What to forage in the cold months — plus a good thermos",
        "url": f"https://www.amazon.co.uk/s?k=winter+foraging+guide+book+uk&tag={AMAZON_TAG}",
        "emoji": "❄️",
    },
}

SEASON_COLOURS = {
    "Spring": "#4CAF50",
    "Summer": "#FFC107",
    "Autumn": "#FF8F00",
    "Winter": "#90CAF9",
}

AFFILIATE_PRODUCTS = {
    "books": [
        {
            "name": "The Forager's Calendar",
            "author": "John Wright",
            "price": "£9.99",
            "desc": "Month-by-month guide to what's in season across the UK. The book we recommend most.",
            "url": f"https://www.amazon.co.uk/s?k=foragers+calendar+john+wright&tag={AMAZON_TAG}",
            "emoji": "📖",
        },
        {
            "name": "Food for Free",
            "author": "Richard Mabey",
            "price": "£7.49",
            "desc": "The classic foraging bible — over 250 wild plants, fruits, and fungi. A British essential.",
            "url": f"https://www.amazon.co.uk/s?k=food+for+free+richard+mabey&tag={AMAZON_TAG}",
            "emoji": "📖",
        },
        {
            "name": "River Cottage Handbook: Hedgerow",
            "author": "John Wright",
            "price": "£10.49",
            "desc": "Everything you need to know about foraging in UK hedgerows, from sloes to sorrel.",
            "url": f"https://www.amazon.co.uk/s?k=river+cottage+hedgerow+john+wright&tag={AMAZON_TAG}",
            "emoji": "📖",
        },
        {
            "name": "Collins Mushroom Guide",
            "author": "Thomas Laessoe",
            "price": "£12.99",
            "desc": "The most trusted UK mushroom identification guide. Essential before you pick any fungus.",
            "url": f"https://www.amazon.co.uk/s?k=collins+mushroom+guide+laessoe&tag={AMAZON_TAG}",
            "emoji": "🍄",
        },
        {
            "name": "Self-Sufficiency for the 21st Century",
            "author": "Dick Strawbridge & James Strawbridge",
            "price": "£14.99",
            "desc": "The complete guide to living off-grid in the UK. From growing to preserving to foraging.",
            "url": f"https://www.amazon.co.uk/s?k=self+sufficiency+21st+century+strawbridge&tag={AMAZON_TAG}",
            "emoji": "🏘️",
        },
                {
            "name": "The Hedgerow Handbook",
            "author": "Adele Nozedar",
            "price": "£8.99",
            "desc": "A beautiful guide to the wild plants, remedies, and recipes hiding in UK hedgerows.",
            "url": f"https://www.amazon.co.uk/s?k=hedgerow+handbook+adele+nozedar&tag={AMAZON_TAG}",
            "emoji": "🌿",
        },
    ],
    "gear": [
        {
            "name": "Hultafors HVK Foraging Knife",
            "price": "£18.50",
            "desc": "The go-to knife for UK foragers — sharp, safe, and built to last. Our top pick.",
            "url": f"https://www.amazon.co.uk/s?k=hultafors+foraging+knife&tag={AMAZON_TAG}",
            "emoji": "🔪",
        },
        {
            "name": "Wicker Foraging Basket",
            "price": "£14.99",
            "desc": "Traditional basket for collecting wild food. Lets spores spread as you walk — better than plastic bags.",
            "url": f"https://www.amazon.co.uk/s?k=wicker+foraging+basket&tag={AMAZON_TAG}",
            "emoji": "🧺",
        },
        {
            "name": "Waterproof Roll-Top Bag",
            "price": "£12.99",
            "desc": "Keep your foraged finds dry on wet days. Roll-top seal, lightweight, and affordable.",
            "url": f"https://www.amazon.co.uk/s?k=waterproof+roll+top+bag+small&tag={AMAZON_TAG}",
            "emoji": "🎒",
        },
        {
            "name": "10x Plant Identification Loupe",
            "price": "£6.99",
            "desc": "Essential magnifier for examining leaves, stems, and spore prints. Every forager needs one.",
            "url": f"https://www.amazon.co.uk/s?k=10x+loupe+magnifier+plant&tag={AMAZON_TAG}",
            "emoji": "🔍",
        },
        {
            "name": "Waterproof Field Notebook",
            "price": "£8.99",
            "desc": "Rite in the Rain notebook — write in any weather. Perfect for recording foraging spots.",
            "url": f"https://www.amazon.co.uk/s?k=rite+in+the+rain+notebook&tag={AMAZON_TAG}",
            "emoji": "📝",
        },
                {
            "name": "Compact First Aid Kit",
            "price": "£9.99",
            "desc": "Waterproof pocket kit with bandages, plasters, and antiseptic. Essential for any foraging trip.",
            "url": f"https://www.amazon.co.uk/s?k=compact+first+aid+kit+outdoor+waterproof&tag={AMAZON_TAG}",
            "emoji": "🩹",
        },
    ],
    "beekeeping": [
        {
            "name": "Practical Beekeeping",
            "author": "Clive de Bruyn",
            "price": "£12.99",
            "desc": "The essential guide to starting your first hive in the UK. Clear, practical, and comprehensive.",
            "url": f"https://www.amazon.co.uk/s?k=practical+beekeeping+clive+de+bruyn&tag={AMAZON_TAG}",
            "emoji": "🐝",
        },
        {
            "name": "Full Beekeeping Suit with Veil",
            "price": "£39.99",
            "desc": "Essential protection for hive inspections. Full suit with integrated veil and gloves.",
            "url": f"https://www.amazon.co.uk/s?k=beekeeping+suit+full+body+veil&tag={AMAZON_TAG}",
            "emoji": "🧤",
        },
        {
            "name": "Stainless Steel Bee Smoker",
            "price": "£24.99",
            "desc": "Calm your bees during inspections. Stainless steel with heat shield — built to last.",
            "url": f"https://www.amazon.co.uk/s?k=stainless+steel+bee+smoker&tag={AMAZON_TAG}",
            "emoji": "💨",
        },
        {
            "name": "Cedar National Beehive",
            "price": "£149.99",
            "desc": "British Standard National hive in cedar. The most popular hive style in the UK.",
            "url": f"https://www.amazon.co.uk/s?k=national+beehive+cedar+uk&tag={AMAZON_TAG}",
            "emoji": "🏠",
        },
                {
            "name": "Stainless Steel Hive Tool",
            "price": "£8.99",
            "desc": "The most used tool in beekeeping. Essential for prying apart frames and scraping propolis.",
            "url": f"https://www.amazon.co.uk/s?k=stainless+steel+hive+tool+beekeeping&tag={AMAZON_TAG}",
            "emoji": "🛠️",
        },
        {
            "name": "Rapid Bee Feeder",
            "price": "£6.99",
            "desc": "Essential for feeding sugar syrup in winter and spring. Fits directly over the crown board.",
            "url": f"https://www.amazon.co.uk/s?k=rapid+bee+feeder+uk&tag={AMAZON_TAG}",
            "emoji": "🍯",
        },
    ],
}

DIGITAL_PRODUCTS = [
    {
        "name": "UK Foraging Season Calendar 2026",
        "desc": "A3 printable wall calendar showing every edible plant, month by month. Never miss a season again!",
        "price": "£4.99",
        "url": "https://buymeacoffee.com/rocehomesteady/e/558993",
        "emoji": "📋",  # Kept in case you use it elsewhere
        "category": "printable",
        "image": "/static/images/shop/Season-Calendar-26.png"  # <-- ADDED
    },
    {
        "name": "Mushroom Identification Flash Cards",
        "desc": "30 printable flashcards covering the most common UK mushrooms — edible and deadly. Perfect for families and beginners.",
        "price": "£3.99",
        "url": "https://buymeacoffee.com/rocehomesteady/e/559000",
        "emoji": "🍄",
        "category": "printable",
        "image": "/static/images/shop/Mushroom.png"  # <-- ADDED
    },
    {
        "name": "Dangerous Lookalikes Cheat Sheet",
        "desc": "A4 printable showing every dangerous plant side-by-side with its safe lookalike. Could save a life.",
        "price": "£2.99",
        "url": "https://buymeacoffee.com/rocehomesteady/e/559001",
        "emoji": "☠️",
        "category": "safety",
        "image": "/static/images/shop/Lookalikes.png"  # <-- ADDED
    },
    {
        "name": "Family Foraging Adventure Pack",
        "desc": "Complete pack for families: ID cards, activity sheets, safety checklist, and seasonal calendar. Ages 5-11.",
        "price": "£7.99",
        "url": "https://buymeacoffee.com/rocehomesteady/e/559003",
        "emoji": "🧒",
        "category": "family",
        "image": "/static/images/shop/Adventure.png"  # <-- ADDED
    },
]
