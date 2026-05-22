# game_config.py - All game constants and configuration

# ==========================================
# ACHIEVEMENTS
# ==========================================
ACHIEVEMENTS = {
    # Tab 1: Foraging
    "foraging_novice": {"name": "🌿 Novice Forager", "desc": "Find 1 unique plant", "tab": 1},
    "foraging_botanist": {"name": "📚 Botanist", "desc": "Collect 25 unique plants", "tab": 1},
    "foraging_master": {"name": "🏅 Seasonal Master", "desc": "Earn a badge in all 4 seasons", "tab": 1},

    # Tab 2: Survival
    "survival_scout": {"name": "🕵️ Scout", "desc": "Solve 1 case", "tab": 2},
    "survival_expert": {"name": "🎓 Graduate", "desc": "Unlock Level 2 (Fungi & Roots)", "tab": 2},
    "survival_detective": {"name": "🔍 Detective", "desc": "Solve 20 cases total", "tab": 2},

    # Tab 3: Quiz
    "quiz_streak": {"name": "🔥 Quick Wit", "desc": "5 correct in a row", "tab": 3},
    "quiz_challenger": {"name": "⚔️ Challenger", "desc": "Complete Challenge Mode (1 life, 10 questions)", "tab": 3},

    # Tab 4: Eco-Village
    "eco_survivor": {"name": "🏘️ Settler", "desc": "Survive 30 Days", "tab": 4},
    "eco_wealth": {"name": "💰 Eco-Tycoon", "desc": "Reach £2000 in the bank", "tab": 4},

    # Tab 5: Farm
    "farm_harvest": {"name": "🌱 Green Thumb", "desc": "Harvest your first crop", "tab": 5},
    "farm_rancher": {"name": "🐮 Rancher", "desc": "Own 5 animals", "tab": 5},
    "farm_winner": {"name": "🏆 Landowner", "desc": "Buy the Manor (Win)", "tab": 5},

    # Tab 6: Kitchen
    "kitchen_apprentice": {"name": "👨‍🍳 Apprentice", "desc": "Unlock 3 recipes", "tab": 6},
    "kitchen_master": {"name": "🍽️ Master Chef", "desc": "Unlock all Intermediate recipes", "tab": 6},

    # Tab 7: Apiary
    "apiary_first_harvest": {"name": "🍯 First Harvest", "desc": "Harvest your first honey", "tab": 7},
    "apiary_overwinter": {"name": "❄️ Survivor", "desc": "Overwinter a colony successfully", "tab": 7},
    "apiary_keeper": {"name": "🐝 Beekeeper", "desc": "Manage 3+ hives at once", "tab": 7},
    "apiary_5_hives": {"name": "🏠 Apiarist", "desc": "Own 5+ hives at once", "tab": 7},
    "apiary_varroa": {"name": "🛡️ Mite Fighter", "desc": "Treat varroa successfully for a full season", "tab": 7},

    # Tab 8: Market Garden
    "mg_first_harvest": {"name": "🌱 First Crop", "desc": "Harvest your first market garden crop", "tab": 8},
    "mg_companion": {"name": "🤝 Companion", "desc": "Plant a companion pair together", "tab": 8},
    "mg_rotation": {"name": "🔄 Rotator", "desc": "Complete a 3-bed crop rotation", "tab": 8},
    "mg_market_master": {"name": "💰 Market Master", "desc": "Earn £500 from market sales", "tab": 8},
    "mg_golden": {"name": "🌟 Golden Touch", "desc": "Find a Golden crop", "tab": 8},
    "mg_rainwater": {"name": "🌧️ Rain Dancer", "desc": "Save £20 by using rain instead of watering", "tab": 8},
    "mg_polytunnel": {"name": "🫧 Early Starter", "desc": "Build a polytunnel", "tab": 8},

}

# ==========================================
# FORAGING QUEST CONFIG
# ==========================================
HABITAT_ICONS = {
    "Woodland": "🌲", "Hedgerow": "🌿", "Coastal": "🏖️",
    "Urban": "🏡", "Meadow": "🌾", "Damp": "💧",
    "Rocky": "🪨", "Grassland": "🌾", "Wet": "💧"
}

SEASON_ICONS = {
    "Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"
}

SEASON_MONTHS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"]
}

# ==========================================
# SURVIVAL SCHOOL CONFIG
# ==========================================
SURVIVAL_DIFFICULTY = {
    1: "🌱 Level 1: Plants & Leaves",
    2: "🍄 Level 2: Fungi, Roots & Advanced",
    3: "☠️ Level 3: Expert Identification"
}

# ==========================================
# ECO-VILLAGE CONFIG (REBALANCED)
# ==========================================
VILLAGE_ITEMS = {
    "Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 1, "food": 2},
    "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1, "food": 3},
    "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 2, "food": 4},
    "Wood": {"icon": "🪵", "rarity": 0.6, "value": 3, "food": 0},
    "Stone": {"icon": "🪨", "rarity": 0.4, "value": 3, "food": 0},
    "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 5, "food": 1},
    "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 12, "food": 12},
    "Fish": {"icon": "🐟", "rarity": 0.0, "value": 15, "food": 25},
    "Apple": {"icon": "🍎", "rarity": 0.0, "value": 3, "food": 3},
    "Pear": {"icon": "🍐", "rarity": 0.0, "value": 3, "food": 3},
    "Orange": {"icon": "🍊", "rarity": 0.0, "value": 3, "food": 3},
    "Dandelion Tea": {"icon": "🍵", "rarity": 0.0, "value": 25, "food": 0, "stamina": 15},
    "Nettle Soup": {"icon": "🥣", "rarity": 0.0, "value": 30, "food": 18},
    "Smoked Fish": {"icon": "🍣", "rarity": 0.0, "value": 50, "food": 45},
    "Cordial": {"icon": "🍶", "rarity": 0.0, "value": 60, "food": 5, "stamina": 30},
    "Jerky": {"icon": "🥩", "rarity": 0.0, "value": 40, "food": 50},
    "Apple Juice": {"icon": "🧃", "rarity": 0.0, "value": 40, "food": 10},
    "Pear Juice": {"icon": "🧃", "rarity": 0.0, "value": 40, "food": 10},
    "Orange Juice": {"icon": "🧃", "rarity": 0.0, "value": 40, "food": 10}
}

VILLAGE_BUILDINGS = {
    "House": {"cost": 80, "icon": "🏠", "desc": "+20 Stamina/day", "repair": 15},
    "Well": {"cost": 40, "icon": "🪨", "desc": "+5 Water/day", "repair": 8},
    "Coop": {"cost": 100, "icon": "🐔", "desc": "1 Egg/day", "repair": 15},
    "DIY Solar": {"cost": 80, "icon": "🔋", "desc": "+2 Power/day", "repair": 12},
    "Solar Array": {"cost": 400, "icon": "☀️", "desc": "+10 Power/day", "repair": 50},
    "Reserve": {"cost": 200, "icon": "🌳", "desc": "Restores Nature", "repair": 25},
    "Barn": {"cost": 300, "icon": "🏚️", "desc": "+20 Storage", "repair": 25},
    "Orchard": {"cost": 300, "icon": "🌴", "desc": "Fruits Daily", "repair": 20},
    "Cold Frame": {"cost": 150, "icon": "🫧", "desc": "+3 Food in Winter", "repair": 12},
    "Smokehouse": {"cost": 250, "icon": "🥓", "desc": "Cook without Power", "repair": 20}
}

VILLAGE_PRODUCTION = {
    "Dandelion Tea": {"ingredients": {"Dandelion": 5}, "power": 2, "output": "Dandelion Tea", "qty": 1},
    "Nettle Soup": {"ingredients": {"Nettle": 5, "Water": 1}, "power": 0, "output": "Nettle Soup", "qty": 1},
    "Smoked Fish": {"ingredients": {"Fish": 1, "Wood": 1}, "power": 5, "output": "Smoked Fish", "qty": 1, "smokehouse": True},
    "Elderflower Cordial": {"ingredients": {"Elderflower": 10}, "power": 5, "output": "Cordial", "qty": 1},
    "Jerky": {"ingredients": {"Eggs": 3, "Wood": 1}, "power": 3, "output": "Jerky", "qty": 1, "smokehouse": True},
    "Apple Juice": {"ingredients": {"Apple": 10}, "power": 5, "output": "Apple Juice", "qty": 1},
    "Pear Juice": {"ingredients": {"Pear": 10}, "power": 5, "output": "Pear Juice", "qty": 1},
    "Orange Juice": {"ingredients": {"Orange": 10}, "power": 5, "output": "Orange Juice", "qty": 1}
}

# ==========================================
# FARM TYCOON CONFIG
# ==========================================
FARM_ICONS = {
    0: "🟫",   # empty/dirt
    1: "🌊",   # stream
    2: "🌱",   # seedling
    3: "🌿",   # growing
    4: "🌾",   # ready to harvest
    7: "🧹",   # weeds
    8: "🏚️",  # barn
    9: "🐝",   # beehive
    10: "🦅",  # scarecrow
    11: "💦",  # sprinkler
    12: "🐔",  # chicken
    13: "🐄",  # cow
    14: "🐐",  # goat
    15: "🫧",  # cold frame
    16: "🏡"   # manor
}

FARM_BUILDINGS = {
    "Manor": {"cost": 5000, "id": 16, "desc": "Win the game! 🏆"},
    "Barn": {"cost": 300, "id": 8, "desc": "+20 Storage"},
    "Beehive": {"cost": 150, "id": 9, "desc": "Produces Honey"},
    "Scarecrow": {"cost": 100, "id": 10, "desc": "Prevents pests"},
    "Sprinkler": {"cost": 200, "id": 11, "desc": "Prevents drought"},
    "Cold Frame": {"cost": 250, "id": 15, "desc": "Protects crops in winter"},
    "Chicken Coop": {"cost": 200, "id": 12, "desc": "Produces Eggs (Year 2+)"},
    "Cow Pasture": {"cost": 500, "id": 13, "desc": "Produces Milk (Year 2+)"},
    "Goat Pen": {"cost": 300, "id": 14, "desc": "Produces Milk (Year 2+)"}
}

SEED_COST = {
    "Carrot": 5,
    "Wheat": 3,
    "Corn": 4
}

BASE_PRICES = {
    "Carrot": 8,
    "Wheat": 6,
    "Corn": 7,
    "Egg": 12,
    "Milk": 15,
    "Honey": 20,
    "Apple": 5,
    "Pear": 5,
    "Orange": 5,
    "Feed": 5
}

# ==========================================
# MARKET GARDEN CONFIG
# ==========================================
MG_CROPS = {
    "Carrot": {"icon": "🥕", "family": "Root", "season": ["Spring", "Summer"], "days": 3, "seed_cost": 3, "sell": 8, "nutrient_drain": {"N": 10, "P": 15, "K": 10}},
    "Tomato": {"icon": "🍅", "family": "Fruit", "season": ["Summer"], "days": 4, "seed_cost": 5, "sell": 15, "nutrient_drain": {"N": 25, "P": 15, "K": 20}},
    "Lettuce": {"icon": "🥬", "family": "Leaf", "season": ["Spring", "Autumn"], "days": 2, "seed_cost": 2, "sell": 6, "nutrient_drain": {"N": 15, "P": 5, "K": 10}},
    "Cabbage": {"icon": "🥦", "family": "Brassica", "season": ["Spring", "Autumn"], "days": 4, "seed_cost": 4, "sell": 12, "nutrient_drain": {"N": 30, "P": 10, "K": 15}},
    "Beans": {"icon": "🫘", "family": "Legume", "season": ["Summer"], "days": 3, "seed_cost": 3, "sell": 10, "nutrient_drain": {"N": -10, "P": 10, "K": 10}},
    "Potato": {"icon": "🥔", "family": "Root", "season": ["Spring"], "days": 4, "seed_cost": 3, "sell": 10, "nutrient_drain": {"N": 15, "P": 20, "K": 25}},
    "Onion": {"icon": "🧅", "family": "Allium", "season": ["Spring", "Summer"], "days": 3, "seed_cost": 3, "sell": 9, "nutrient_drain": {"N": 10, "P": 10, "K": 5}},
    "Basil": {"icon": "🌿", "family": "Herb", "season": ["Summer"], "days": 2, "seed_cost": 4, "sell": 12, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Marigold": {"icon": "🌻", "family": "Herb", "season": ["Spring", "Summer"], "days": 2, "seed_cost": 3, "sell": 5, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Sage": {"icon": "🌱", "family": "Herb", "season": ["Spring", "Autumn"], "days": 2, "seed_cost": 4, "sell": 10, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Sweetcorn": {"icon": "🌽", "family": "Fruit", "season": ["Summer"], "days": 4, "seed_cost": 4, "sell": 12, "nutrient_drain": {"N": 25, "P": 15, "K": 15}},
    "Squash": {"icon": "🎃", "family": "Cucurbit", "season": ["Summer"], "days": 4, "seed_cost": 4, "sell": 11, "nutrient_drain": {"N": 20, "P": 15, "K": 20}},
    "Strawberry": {"icon": "🍓", "family": "Berry", "season": ["Spring", "Summer"], "days": 3, "seed_cost": 6, "sell": 18, "nutrient_drain": {"N": 15, "P": 20, "K": 15}},
    "Peas": {"icon": "🟢", "family": "Legume", "season": ["Spring"], "days": 3, "seed_cost": 3, "sell": 9, "nutrient_drain": {"N": -10, "P": 10, "K": 10}},
    "Beetroot": {"icon": "🔴", "family": "Root", "season": ["Spring", "Autumn"], "days": 3, "seed_cost": 3, "sell": 9, "nutrient_drain": {"N": 10, "P": 15, "K": 15}},
    "Chives": {"icon": "🧅", "family": "Allium", "season": ["Spring", "Summer", "Autumn"], "days": 2, "seed_cost": 3, "sell": 8, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Borage": {"icon": "💜", "family": "Herb", "season": ["Summer"], "days": 2, "seed_cost": 4, "sell": 7, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
}

MG_COMPANIONS = {
    ("Tomato", "Basil"): {"bonus": "Pest resistance +15%", "yield_bonus": 1.15},
    ("Tomato", "Marigold"): {"bonus": "Nematode resistance", "yield_bonus": 1.10},
    ("Carrot", "Onion"): {"bonus": "Confuses carrot fly", "yield_bonus": 1.10},
    ("Carrot", "Chives"): {"bonus": "Repels aphids", "yield_bonus": 1.10},
    ("Cabbage", "Sage"): {"bonus": "Repels cabbage moth", "yield_bonus": 1.15},
    ("Cabbage", "Chives"): {"bonus": "Repels aphids", "yield_bonus": 1.10},
    ("Lettuce", "Chives"): {"bonus": "Repels aphids", "yield_bonus": 1.10},
    ("Strawberry", "Borage"): {"bonus": "Attracts pollinators", "yield_bonus": 1.15},
    ("Beans", "Sweetcorn"): {"bonus": "Fixes nitrogen for corn", "yield_bonus": 1.10},
    ("Squash", "Sweetcorn"): {"bonus": "Shade suppresses weeds", "yield_bonus": 1.10},
    ("Squash", "Beans"): {"bonus": "Three Sisters trio", "yield_bonus": 1.20},
    ("Potato", "Marigold"): {"bonus": "Nematode resistance", "yield_bonus": 1.10},
    ("Tomato", "Carrot"): {"bonus": "Carrot aerates soil", "yield_bonus": 1.05},
    ("Peas", "Carrot"): {"bonus": "Nitrogen for carrots", "yield_bonus": 1.10},
    ("Lettuce", "Strawberry"): {"bonus": "Ground cover", "yield_bonus": 1.05},
}

MG_ANTAGONISTS = {
    ("Tomato", "Cabbage"): "Tomatoes stunt cabbage growth",
    ("Beans", "Onion"): "Onions inhibit bean growth",
    ("Beans", "Chives"): "Alliums inhibit bean growth",
    ("Potato", "Tomato"): "Both susceptible to blight",
    # ("Carrot", "Dill"): "Dill stunts carrot growth",  # removed - Dill not in game
}

MG_SEASONS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"],
}

MG_MARKET_BASE = {
    "Carrot": 3, "Tomato": 5, "Lettuce": 2, "Cabbage": 4, "Beans": 4,
    "Potato": 3, "Onion": 3, "Basil": 5, "Marigold": 2, "Sage": 4,
    "Sweetcorn": 5, "Squash": 4, "Strawberry": 6, "Peas": 3,
    "Beetroot": 3, "Chives": 3, "Borage": 2,
    "Golden Carrot": 30, "Golden Tomato": 50, "Golden Strawberry": 60,
    "Golden Cabbage": 40, "Golden Squash": 40, "Golden Sweetcorn": 50,
}

# ==========================================
# APIARY CONFIG (Beekeeping Game)
# ==========================================
NECTAR_FLOW = {
    "January": {"flow": 0, "source": "None", "honey_type": None},
    "February": {"flow": 0, "source": "Snowdrops", "honey_type": None},
    "March": {"flow": 1, "source": "Willow, Crocus", "honey_type": None},
    "April": {"flow": 3, "source": "Oil Seed Rape, Dandelion, Cherry", "honey_type": "Spring Blossom"},
    "May": {"flow": 4, "source": "Hawthorn, Apple, Horse Chestnut", "honey_type": "Spring Blossom"},
    "June": {"flow": 5, "source": "Lime, Clover, Bramble", "honey_type": "Summer Wildflower"},
    "July": {"flow": 5, "source": "Lime, Clover, Blackberry", "honey_type": "Summer Wildflower"},
    "August": {"flow": 3, "source": "Heather, Ivy", "honey_type": "Heather"},
    "September": {"flow": 2, "source": "Ivy, Late flowers", "honey_type": "Autumn Blossom"},
    "October": {"flow": 1, "source": "Ivy", "honey_type": None},
    "November": {"flow": 0, "source": "None", "honey_type": None},
    "December": {"flow": 0, "source": "None", "honey_type": None},
}

HONEY_TYPES = {
    "Spring Blossom": {"value": 8, "icon": "🍯", "desc": "Light and floral, from spring flowers"},
    "Summer Wildflower": {"value": 12, "icon": "🍯", "desc": "Rich amber, from summer meadows"},
    "Heather": {"value": 20, "icon": "🍯", "desc": "Dark and thick, premium honey"},
    "Autumn Blossom": {"value": 10, "icon": "🍯", "desc": "Medium amber, late season"},
}

APIARY_PRODUCTS = {
    "Spring Honey": {"icon": "🍯", "value": 8},
    "Summer Honey": {"icon": "🍯", "value": 12},
    "Heather Honey": {"icon": "🍯", "value": 20},
    "Autumn Honey": {"icon": "🍯", "value": 10},
    "Beeswax": {"icon": "🕯️", "value": 5},
    "Propolis": {"icon": "🟤", "value": 15},
}

BEEKEEPING_SEASONS = {
    "Winter": ["December", "January", "February"],
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
}

WEATHER_CHANCES = {
    "Winter": {"sunny": 0.20, "cloudy": 0.30, "rainy": 0.40, "stormy": 0.10},
    "Spring": {"sunny": 0.35, "cloudy": 0.30, "rainy": 0.25, "stormy": 0.10},
    "Summer": {"sunny": 0.50, "cloudy": 0.25, "rainy": 0.20, "stormy": 0.05},
    "Autumn": {"sunny": 0.25, "cloudy": 0.30, "rainy": 0.35, "stormy": 0.10},
}

TEMP_RANGE = {
    "Winter": (-2, 8),
    "Spring": (8, 18),
    "Summer": (16, 28),
    "Autumn": (6, 16),
}

# ==========================================
# WILD KITCHEN CONFIG
# ==========================================
BASICS = ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"]

KITCHEN_RECIPES = [
    # --- BEGINNER ---
    {"name": "Nettle Soup", "ingredients": {"Nettles": 5, "Water": 1}, "prep_questions": [{"q": "Why must nettles be cooked?", "opts": ["To remove the sting", "To make them sweet", "To change color"], "a": "To remove the sting"}], "icon": "🥣", "desc": "A rich, green soup.", "diff": 1, "benefits": "High in Iron."},
    {"name": "Wild Garlic Pesto", "ingredients": {"Wild Garlic": 10, "Oil": 1}, "prep_questions": [{"q": "Which part of Wild Garlic is edible?", "opts": ["Only the flowers", "Leaves, flowers, and bulbs", "Only the roots"], "a": "Leaves, flowers, and bulbs"}], "icon": "🥗", "desc": "A fragrant pesto.", "diff": 1, "benefits": "Antibacterial."},
    {"name": "Dandelion Salad", "ingredients": {"Dandelion": 5}, "prep_questions": [{"q": "When is best to harvest Dandelion leaves?", "opts": ["When the flower is yellow", "Before the flower opens (young)", "In winter"], "a": "Before the flower opens (young)"}], "icon": "🥗", "desc": "Young leaves are less bitter.", "diff": 1, "benefits": "Liver health."},
    {"name": "Three-Cornered Leek Omelette", "ingredients": {"Three-Cornered Leek": 5, "Eggs": 2}, "prep_questions": [{"q": "How to ID Three-Cornered Leek?", "opts": ["Smells of garlic, triangular stem", "Blue flowers, round stem", "Yellow flowers, spiky"], "a": "Smells of garlic, triangular stem"}], "icon": "🍳", "desc": "A forager's breakfast.", "diff": 1, "benefits": "High protein."},
    {"name": "Pine Needle Tea", "ingredients": {"Pine Needles": 10, "Water": 1}, "prep_questions": [{"q": "How do you identify SAFE Pine needles?", "opts": ["Flat needles (Yew)", "Round needles in bundles", "Blue needles"], "a": "Round needles in bundles"}], "icon": "🍵", "desc": "High in Vitamin C.", "diff": 1, "benefits": "Vitamin C boost."},
    {"name": "Beech Leaf Liqueur", "ingredients": {"Beech Leaves": 20, "Sugar": 1, "Alcohol": 1}, "prep_questions": [{"q": "When should you pick Beech leaves?", "opts": ["Autumn (Brown)", "Spring (Young/Transparent)", "Winter"], "a": "Spring (Young/Transparent)"}], "icon": "🥃", "desc": "A sweet, gin-based liquor.", "diff": 1, "benefits": "Traditional tonic."},
    {"name": "Chickweed Salad", "ingredients": {"Chickweed": 10}, "prep_questions": [{"q": "How do you identify Chickweed?", "opts": ["Line of hairs on stem", "Purple spots on stem", "Blue flowers"], "a": "Line of hairs on stem"}], "icon": "🥗", "desc": "A mild, nutritious weed.", "diff": 1, "benefits": "Vitamins."},
    {"name": "Wild Strawberry Jam", "ingredients": {"Wild Strawberry": 20, "Sugar": 1}, "prep_questions": [{"q": "How do wild strawberries differ from barren strawberry?", "opts": ["Barren has petals with gaps", "Wild has blue flowers", "Barren has hairy leaves"], "a": "Barren has petals with gaps"}], "icon": "🍯", "desc": "Tiny but intense flavor.", "diff": 1, "benefits": "Antioxidants."},
    {"name": "Roasted Hazelnuts", "ingredients": {"Hazelnut": 10}, "prep_questions": [{"q": "What indicates a ripe Hazelnut?", "opts": ["Green husk", "Brown shell and leafy husk", "No leaves"], "a": "Brown shell and leafy husk"}], "icon": "🌰", "desc": "Autumn treat.", "diff": 1, "benefits": "Heart health."},
    {"name": "Sea Purslane Salad", "ingredients": {"Sea Purslane": 10}, "prep_questions": [{"q": "What is the main precaution with Sea Purslane?", "opts": ["It is very salty", "It is poisonous raw", "It has thorns"], "a": "It is very salty"}], "icon": "🥗", "desc": "Salty coastal green.", "diff": 1, "benefits": "Minerals."},
    # --- INTERMEDIATE ---
    {"name": "Dandelion Coffee", "ingredients": {"Dandelion": 20}, "prep_questions": [{"q": "Which part is used for coffee?", "opts": ["Leaves", "Flowers", "Roots"], "a": "Roots"}, {"q": "How must the roots be prepared?", "opts": ["Eaten raw", "Roasted and ground", "Boiled whole"], "a": "Roasted and ground"}], "icon": "☕", "desc": "Caffeine-free coffee substitute.", "diff": 2, "benefits": "Liver detox."},
    {"name": "Elderflower Cordial", "ingredients": {"Elderflower": 10, "Sugar": 1}, "prep_questions": [{"q": "Why should you not wash Elderflowers?", "opts": ["Loses pollen (flavor)", "Becomes poisonous", "Petals fall off"], "a": "Loses pollen (flavor)"}, {"q": "What must you check for before cooking?", "opts": ["Spiders", "Bugs/Maggots", "Birds"], "a": "Bugs/Maggots"}], "icon": "🥤", "desc": "A sweet summery drink.", "diff": 2, "benefits": "Vitamin C."},
    {"name": "Blackberry Jam", "ingredients": {"Blackberries": 20, "Sugar": 1}, "prep_questions": [{"q": "What must you check for when picking?", "opts": ["Check for bugs", "Check if they are red", "Check for thorns"], "a": "Check for bugs"}, {"q": "What helps the jam set (thicken)?", "opts": ["Water", "Pectin (naturally in fruit)", "Oil"], "a": "Pectin (naturally in fruit)"}], "icon": "🍯", "desc": "Preserved summer in a jar.", "diff": 2, "benefits": "Fiber."},
    {"name": "Rosehip Syrup", "ingredients": {"Rosehips": 15, "Sugar": 1}, "prep_questions": [{"q": "Why remove the seeds?", "opts": ["Bitter", "Itchy irritation", "Poisonous"], "a": "Itchy irritation"}, {"q": "What vitamin are Rosehips famous for?", "opts": ["Vitamin A", "Vitamin C", "Vitamin D"], "a": "Vitamin C"}], "icon": "🧴", "desc": "Rich in Vitamin C.", "diff": 2, "benefits": "Immune boost."},
    {"name": "Sorrel Soup", "ingredients": {"Sorrel": 15, "Water": 1}, "prep_questions": [{"q": "What gives Sorrel its sour taste?", "opts": ["Sugar", "Oxalic Acid", "Citrus"], "a": "Oxalic Acid"}, {"q": "Who should avoid large amounts?", "opts": ["Children", "People with kidney issues", "Elderly"], "a": "People with kidney issues"}], "icon": "🥣", "desc": "Tangy and refreshing.", "diff": 2, "benefits": "Vitamin C."},
    {"name": "Hawthorn Ketchup", "ingredients": {"Hawthorn": 30, "Sugar": 1}, "prep_questions": [{"q": "What do Hawthorn berries look like?", "opts": ["Blue pods", "Small red berries", "Blackberries"], "a": "Small red berries"}, {"q": "What should you avoid when eating?", "opts": ["The skin", "The seeds (pips)", "The stem"], "a": "The seeds (pips)"}], "icon": "🍅", "desc": "Tomato ketchup alternative.", "diff": 2, "benefits": "Heart health."},
    {"name": "Sweet Chestnut Roast", "ingredients": {"Sweet Chestnut": 20}, "prep_questions": [{"q": "How does the case differ from Horse Chestnut?", "opts": ["Smooth/Warty", "Very spiky", "Green"], "a": "Very spiky"}, {"q": "What must you do before roasting?", "opts": ["Peel them", "Score the shell", "Boil for 1 hour"], "a": "Score the shell"}], "icon": "🌰", "desc": "Roasting over an open fire.", "diff": 2, "benefits": "Starch source."},
    {"name": "Marsh Samphire Sauté", "ingredients": {"Marsh Samphire": 15, "Butter": 1}, "prep_questions": [{"q": "Where does Samphire grow?", "opts": ["Dry Meadows", "Saltmarshes/Mud", "Trees"], "a": "Saltmarshes/Mud"}, {"q": "How do you harvest sustainably?", "opts": ["Pull up roots", "Cut top 2 inches", "Dig with trowel"], "a": "Cut top 2 inches"}], "icon": "🥦", "desc": "Sea asparagus.", "diff": 2, "benefits": "Iodine."},
    # --- ADVANCED ---
    {"name": "Acorn Coffee", "ingredients": {"Oak (Acorns)": 20}, "prep_questions": [{"q": "Why not eat raw?", "opts": ["Too hard", "Contain tannins (bitter)", "Protected"], "a": "Contain tannins (bitter)"}, {"q": "How to remove tannins?", "opts": ["Leaching (soaking)", "Freezing", "Burning"], "a": "Leaching (soaking)"}, {"q": "When to harvest?", "opts": ["Green", "Brown (ripe)", "White"], "a": "Brown (ripe)"}], "icon": "☕", "desc": "Must be leached first.", "diff": 3, "benefits": "Gluten-free."},
    {"name": "Chanterelle Risotto", "ingredients": {"Chanterelle": 10, "Rice": 1}, "prep_questions": [{"q": "How to ID Chanterelle?", "opts": ["True gills (sheets)", "False gills (ridges)", "Sponge"], "a": "False gills (ridges)"}, {"q": "What does it smell like?", "opts": ["Aniseed/Apricot", "Mud", "Nothing"], "a": "Aniseed/Apricot"}, {"q": "Danger lookalike?", "opts": ["False Chanterelle", "Death Cap", "Field Mushroom"], "a": "False Chanterelle"}], "icon": "🍚", "desc": "A gourmet wild meal.", "diff": 3, "benefits": "Vitamin D."},
    {"name": "Crab Apple Jelly", "ingredients": {"Crab Apple": 25, "Sugar": 1}, "prep_questions": [{"q": "Why not eat raw?", "opts": ["Poisonous", "Too tart/sour", "Too hard"], "a": "Too tart/sour"}, {"q": "Why is it good for jelly?", "opts": ["High Pectin", "Red Color", "Soft skin"], "a": "High Pectin"}, {"q": "What to remove?", "opts": ["Skin", "Seeds and stems", "Nothing"], "a": "Seeds and stems"}], "icon": "🍯", "desc": "High pectin.", "diff": 3, "benefits": "Pectin source."},
    {"name": "Wood Ear Stir-fry", "ingredients": {"Wood Ear (Jelly Ear)": 10, "Oil": 1}, "prep_questions": [{"q": "Where does it grow?", "opts": ["Ground", "Elder trees", "Pine trees"], "a": "Elder trees"}, {"q": "Texture?", "opts": ["Soft", "Jelly/Rubbery", "Crunchy"], "a": "Jelly/Rubbery"}, {"q": "Must be cooked?", "opts": ["Yes", "No", "Only if old"], "a": "Yes"}], "icon": "🥡", "desc": "Jelly fungus.", "diff": 3, "benefits": "Blood circulation."},
    {"name": "Morel Risotto", "ingredients": {"Morel": 10, "Rice": 1}, "prep_questions": [{"q": "Cap texture?", "opts": ["Smooth", "Honeycomb pits", "Wrinkled brain"], "a": "Honeycomb pits"}, {"q": "Inside?", "opts": ["Solid", "Chambered", "Hollow"], "a": "Hollow"}, {"q": "Danger lookalike?", "opts": ["True Morel", "False Morel", "Chanterelle"], "a": "False Morel"}], "icon": "🍚", "desc": "Spring delicacy.", "diff": 3, "benefits": "Vitamin D."},
    {"name": "Burdock Root Stew", "ingredients": {"Burdock (Root)": 10, "Water": 1}, "prep_questions": [{"q": "Which root to dig?", "opts": ["Flowering plant", "First year plant", "Any"], "a": "First year plant"}, {"q": "Legal issue?", "opts": ["None", "Uprooting illegal without permission", "Poisonous"], "a": "Uprooting illegal without permission"}, {"q": "Taste?", "opts": ["Sweet", "Earthy/Artichoke", "Bitter"], "a": "Earthy/Artichoke"}], "icon": "🍲", "desc": "Requires digging.", "diff": 3, "benefits": "Blood purifier."},
    {"name": "Cockles in Vinegar", "ingredients": {"Cockles": 20, "Vinegar": 1}, "prep_questions": [{"q": "Shell shape?", "opts": ["Smooth", "Ribbed/Ridged", "Spiral"], "a": "Ribbed/Ridged"}, {"q": "Safety check?", "opts": ["Red tide/Pollution", "Size", "Color"], "a": "Red tide/Pollution"}, {"q": "Cooking?", "opts": ["Eat raw", "Steam until open", "Fry"], "a": "Steam until open"}], "icon": "🥣", "desc": "Coastal shellfish.", "diff": 3, "benefits": "Protein."}
]
