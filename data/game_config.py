# game_config.py - All game constants and configuration
#
# ==========================================
# TABLE OF CONTENTS
# ==========================================
#   1. ACHIEVEMENTS
#   2. SHARED SEASON CONFIG (used by Foraging, Market Garden & Apiary)
#   3. FORAGING QUEST CONFIG
#   4. WINTER HEAT CONFIG
#   5. SURVIVAL SCHOOL CONFIG
#   6. ECO-VILLAGE CONFIG
#   7. FARM TYCOON CONFIG
#   8. MARKET GARDEN CONFIG
#   9. FARM TYCOON — EXPANDED CONFIG
#  10. MARKET GARDEN — UNLOCK SYSTEM
#  11. APIARY CONFIG (Beekeeping Game)
#  12. APIARY — SMOKER, TEMPERAMENT, WASPS, EDUCATION & MENTOR
#  13. WILD KITCHEN CONFIG
#  14. SURVIVAL SCHOOL — ENHANCED CONFIG
# ==========================================


# ==========================================
# 1. ACHIEVEMENTS
# ==========================================
ACHIEVEMENTS = {
    # Tab 2: Survival (includes foraging, formerly Tab 1)
    "foraging_novice": {"name": "🌿 Novice Forager", "desc": "Identify your first plant", "tab": 2},
    "foraging_botanist": {"name": "📚 Botanist", "desc": "Collect 25 unique plants", "tab": 2},
    "foraging_master": {"name": "🏅 Seasonal Master", "desc": "Earn all 4 season badges", "tab": 2},

    # Tab 2: Survival (cases)
    "survival_scout": {"name": "🕵️ Scout", "desc": "Solve 1 case", "tab": 2},
    "survival_expert": {"name": "🎓 Graduate", "desc": "Unlock Level 2 (Fungi & Roots)", "tab": 2},
    "survival_detective": {"name": "🔍 Detective", "desc": "Solve 20 cases total", "tab": 2},

    # Tab 3: Quiz
    "quiz_first_quiz": {"name": "🎯 First Steps", "desc": "Complete your first quiz", "tab": 3},
    "quiz_streak": {"name": "🔥 Quick Wit", "desc": "5 correct in a row", "tab": 3},
    "quiz_streak_10": {"name": "⚡ On Fire", "desc": "10 correct in a row", "tab": 3},
    "quiz_perfect": {"name": "💯 Perfectionist", "desc": "Score 10/10 on any quiz", "tab": 3},
    "quiz_challenger": {"name": "⚔️ Challenger", "desc": "Complete Challenge Mode (1 life, 10 questions)", "tab": 3},
    "quiz_category_master": {"name": "🔬 Specialist", "desc": "Score 9+ in a single category quiz", "tab": 3},
    "quiz_plants_10": {"name": "🌿 Botanist", "desc": "Discover 10 different plants in quizzes", "tab": 3},
    "quiz_plants_25": {"name": "📚 Plant Scholar", "desc": "Discover 25 different plants", "tab": 3},
    "quiz_plants_50": {"name": "🏆 Plant Master", "desc": "Discover 50 different plants", "tab": 3},
    "quiz_safety_first": {"name": "☠️ Safety First", "desc": "Score 9+ in Safety & Poisoning", "tab": 3},
    "quiz_daily_7": {"name": "📅 Weekly Warrior", "desc": "Complete 7 daily quizzes", "tab": 3},
    "quiz_expert_clear": {"name": "🌳 Expert Survivor", "desc": "Complete Expert difficulty with 3 lives intact", "tab": 3},

    # Tab 4: Eco-Village
    "eco_survivor": {"name": "🏘️ Settler", "desc": "Survive 30 Days", "tab": 4},
    "eco_wealth": {"name": "💰 Eco-Tycoon", "desc": "Reach £2000 in the bank", "tab": 4},

    # Tab 5: Farm
    "farm_harvest": {"name": "🌱 Green Thumb", "desc": "Harvest your first crop", "tab": 5},
    "farm_rancher": {"name": "🐮 Rancher", "desc": "Own 5 animals", "tab": 5},
    "farm_winner": {"name": "🏆 Landowner", "desc": "Buy the Manor (Win)", "tab": 5},

    # Tab 6: Kitchen
    "kitchen_first_cook": {"name": "🍳 First Dish", "desc": "Cook your first recipe", "tab": 6},
    "kitchen_apprentice": {"name": "👨‍🍳 Apprentice", "desc": "Unlock 3 Beginner recipes", "tab": 6},
    "kitchen_beginner_complete": {"name": "🥉 Beginner Chef", "desc": "Unlock all Beginner recipes", "tab": 6},
    "kitchen_intermediate_first": {"name": "⭐ Rising Star", "desc": "Unlock your first Intermediate recipe", "tab": 6},
    "kitchen_master": {"name": "🍽️ Master Chef", "desc": "Unlock all Intermediate recipes", "tab": 6},
    "kitchen_advanced_first": {"name": "🔮 Adventurer", "desc": "Unlock your first Advanced recipe", "tab": 6},
    "kitchen_grand_master": {"name": "🏆 Grand Master", "desc": "Unlock all Advanced recipes", "tab": 6},
    "kitchen_complete": {"name": "📖 Complete Cookbook", "desc": "Unlock every recipe in the game", "tab": 6},
    "kitchen_score_100": {"name": "👨‍🍳 Line Cook", "desc": "Reach Kitchen Score 100", "tab": 6},
    "kitchen_score_500": {"name": "🧑‍🍳 Sous Chef", "desc": "Reach Kitchen Score 500", "tab": 6},
    "kitchen_score_1000": {"name": "👩‍🍳 Head Chef", "desc": "Reach Kitchen Score 1000", "tab": 6},
    "kitchen_pantry": {"name": "🧺 Well Stocked", "desc": "Have 20+ items in your pantry", "tab": 6},

    # Tab 7: Apiary
    "apiary_first_harvest": {"name": "🍯 First Harvest", "desc": "Harvest your first honey", "tab": 7},
    "apiary_overwinter": {"name": "❄️ Survivor", "desc": "Overwinter a colony successfully", "tab": 7},
    "apiary_keeper": {"name": "🐝 Beekeeper", "desc": "Manage 3+ hives at once", "tab": 7},
    "apiary_5_hives": {"name": "🏠 Apiarist", "desc": "Own 5+ hives at once", "tab": 7},
    "apiary_varroa": {"name": "🛡️ Mite Fighter", "desc": "Treat varroa successfully for a full season", "tab": 7},
    "apiary_processor": {"name": "⚗️ Processor", "desc": "Process your first product", "tab": 7},
    "apiary_mead_master": {"name": "🍺 Mead Master", "desc": "Produce 5 batches of Mead", "tab": 7},
    "apiary_swarm_catcher": {"name": "🪤 Swarm Catcher", "desc": "Catch a swarm", "tab": 7},
    "apiary_5_harvests": {"name": "🍯 Honey Maker", "desc": "Harvest honey 5 times", "tab": 7},
    "apiary_disease_free": {"name": "🏥 Healthy Colony", "desc": "Keep a colony disease-free for a year", "tab": 7},

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
# 2. SHARED SEASON CONFIG
# ==========================================
# Used by Foraging, Market Garden, and Apiary.
# Aliases preserve backward compatibility with existing code.

SEASONS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"],
}

SEASON_MONTHS = SEASONS       # Foraging / Eco-Village
MG_SEASONS = SEASONS           # Market Garden
BEEKEEPING_SEASONS = SEASONS   # Apiary


# ==========================================
# 3. FORAGING QUEST CONFIG
# ==========================================
# NOTE: "Grassland" & "Meadow" share the same icon (🌾).
#       "Damp" & "Wet" share the same icon (💧).
#       Consider merging or differentiating if they represent distinct habitats.

HABITAT_ICONS = {
    "Woodland": "🌲", "Hedgerow": "🌿", "Coastal": "🏖️",
    "Urban": "🏡", "Meadow": "🌾", "Damp": "💧",
    "Rocky": "🪨", "Grassland": "🌾", "Wet": "💧",
}

SEASON_ICONS = {
    "Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️",
}


# ==========================================
# 4. WINTER HEAT CONFIG
# ==========================================
WINTER_HEAT = {
    "wood_per_house": 1,
    "damage_interval": 2,
}


# ==========================================
# 5. SURVIVAL SCHOOL CONFIG
# ==========================================
SURVIVAL_DIFFICULTY = {
    1: "🌱 Level 1: Plants & Leaves",
    2: "🍄 Level 2: Fungi, Roots & Advanced",
    3: "☠️ Level 3: Expert Identification",
}


# ==========================================
# 6. ECO-VILLAGE CONFIG
# ==========================================
VILLAGE_ITEMS = {
    # ── Wild Forageables ──
    "Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 1, "food": 2},
    "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1, "food": 3},
    "Wild Garlic": {"icon": "🧄", "rarity": 0.5, "value": 2, "food": 4},
    "Three-Cornered Leek": {"icon": "🧅", "rarity": 0.4, "value": 3, "food": 3},
    "Pine Needles": {"icon": "🌲", "rarity": 0.6, "value": 1, "food": 0},
    "Beech Leaves": {"icon": "🍃", "rarity": 0.5, "value": 1, "food": 0},
    "Chickweed": {"icon": "🌱", "rarity": 0.6, "value": 1, "food": 2},
    "Wild Strawberry": {"icon": "🍓", "rarity": 0.3, "value": 4, "food": 3},
    "Hazelnut": {"icon": "🌰", "rarity": 0.3, "value": 4, "food": 5},
    "Sea Purslane": {"icon": "🌿", "rarity": 0.25, "value": 5, "food": 2},
    "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 5, "food": 1},
    "Blackberry": {"icon": "🫐", "rarity": 0.4, "value": 3, "food": 4},
    "Rosehips": {"icon": "🌹", "rarity": 0.3, "value": 4, "food": 2},
    "Sorrel": {"icon": "🥬", "rarity": 0.5, "value": 2, "food": 2},
    "Hawthorn": {"icon": "🔴", "rarity": 0.35, "value": 3, "food": 1},
    "Sweet Chestnut": {"icon": "🌰", "rarity": 0.25, "value": 5, "food": 8},
    "Marsh Samphire": {"icon": "🥦", "rarity": 0.2, "value": 6, "food": 3},
    "Oak (Acorns)": {"icon": "🌰", "rarity": 0.35, "value": 2, "food": 0},
    "Chanterelle": {"icon": "🍄", "rarity": 0.15, "value": 10, "food": 8},
    "Crab Apple": {"icon": "🍎", "rarity": 0.4, "value": 2, "food": 2},
    "Wood Ear (Jelly Ear)": {"icon": "🍄", "rarity": 0.2, "value": 5, "food": 3},
    "Morel": {"icon": "🍄", "rarity": 0.1, "value": 15, "food": 10},
    "Burdock (Root)": {"icon": "🌿", "rarity": 0.2, "value": 4, "food": 5},
    "Cockles": {"icon": "🐚", "rarity": 0.15, "value": 8, "food": 10},

    # ── Building-Produced (rarity 0 = not forageable) ──
    "Wood": {"icon": "🪵", "rarity": 0.6, "value": 3, "food": 0},
    "Stone": {"icon": "🪨", "rarity": 0.4, "value": 3, "food": 0},
    "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 12, "food": 12},
    "Fish": {"icon": "🐟", "rarity": 0.0, "value": 15, "food": 25},
    "Apple": {"icon": "🍎", "rarity": 0.0, "value": 3, "food": 3},
    "Pear": {"icon": "🍐", "rarity": 0.0, "value": 3, "food": 3},
    "Orange": {"icon": "🍊", "rarity": 0.0, "value": 3, "food": 3},
    "Milk": {"icon": "🥛", "rarity": 0.0, "value": 8, "food": 10},
    "Strawberry": {"icon": "🍓", "rarity": 0.0, "value": 5, "food": 4},
    "Tomato": {"icon": "🍅", "rarity": 0.0, "value": 4, "food": 4},
    "Pepper": {"icon": "🌶️", "rarity": 0.0, "value": 5, "food": 3},
    "Cucumber": {"icon": "🥒", "rarity": 0.0, "value": 3, "food": 3},
    "Lettuce": {"icon": "🥬", "rarity": 0.0, "value": 2, "food": 2},

    # ── Crafted / Produced (rarity 0) ──
    "Dandelion Tea": {"icon": "🍵", "rarity": 0.0, "value": 25, "food": 0, "stamina": 15},
    "Nettle Soup": {"icon": "🥣", "rarity": 0.0, "value": 30, "food": 18},
    "Smoked Fish": {"icon": "🍣", "rarity": 0.0, "value": 50, "food": 45},
    "Cordial": {"icon": "🍶", "rarity": 0.0, "value": 60, "food": 5, "stamina": 30},
    "Jerky": {"icon": "🥩", "rarity": 0.0, "value": 40, "food": 50},
    "Apple Juice": {"icon": "🧃", "rarity": 0.0, "value": 40, "food": 10},
    "Pear Juice": {"icon": "🧃", "rarity": 0.0, "value": 40, "food": 10},
    "Orange Juice": {"icon": "🧃", "rarity": 0.0, "value": 40, "food": 10},
    "Goat Cheese": {"icon": "🧀", "rarity": 0.0, "value": 35, "food": 30},
    "Tomato Sauce": {"icon": "🍝", "rarity": 0.0, "value": 25, "food": 15},
    "Strawberry Jam": {"icon": "🍯", "rarity": 0.0, "value": 45, "food": 12},
}



VILLAGE_BUILDINGS = {
    "House": {"cost": 80, "icon": "🏠", "desc": "+20 Stamina/day (needs 1 Wood/day in Winter)", "repair": 15},
    "Well": {"cost": 40, "icon": "🪨", "desc": "+5 Water/day", "repair": 8},
    "Coop": {"cost": 100, "icon": "🐔", "desc": "1 Egg/day", "repair": 15},
    "Solar Panel": {"cost": 80, "icon": "🔆", "desc": "+2 Power/day. Stops in Winter.", "repair": 12},
    "Wind Turbine": {"cost": 400, "icon": "💨", "desc": "+10 Power/day. Stops in Winter.", "repair": 50},
    "Reserve": {"cost": 200, "icon": "🌳", "desc": "Restores Nature", "repair": 25},
    "Barn": {"cost": 300, "icon": "🏚️", "desc": "+20 Storage & +20 Barn Storage", "repair": 25},
    "Orchard": {"cost": 300, "icon": "🌴", "desc": "Fruits Daily", "repair": 20},
    "Cold Frame": {"cost": 150, "icon": "🫧", "desc": "+3 Food in Winter", "repair": 12},
    "Smokehouse": {"cost": 250, "icon": "🥓", "desc": "+1 Wood/day, Cook without Power", "repair": 20},
    "Goat Pen": {"cost": 200, "icon": "🐐", "desc": "1 Milk/day. Goats thrive in any season.", "repair": 20},
    "Greenhouse": {"cost": 300, "icon": "🌱", "desc": "1-2 crops/day year-round (Strawberry, Tomato, Pepper, Cucumber, Lettuce)", "repair": 30},
}


VILLAGE_PRODUCTION = {
    "Dandelion Tea": {"ingredients": {"Dandelion": 5}, "power": 2, "output": "Dandelion Tea", "qty": 1},
    "Nettle Soup": {"ingredients": {"Nettle": 5, "Water": 1}, "power": 0, "output": "Nettle Soup", "qty": 1},
    "Smoked Fish": {"ingredients": {"Fish": 1, "Wood": 1}, "power": 5, "output": "Smoked Fish", "qty": 1, "smokehouse": True},
    "Elderflower Cordial": {"ingredients": {"Elderflower": 10}, "power": 5, "output": "Cordial", "qty": 1},
    "Jerky": {"ingredients": {"Eggs": 3, "Wood": 1}, "power": 3, "output": "Jerky", "qty": 1, "smokehouse": True},
    "Apple Juice": {"ingredients": {"Apple": 10}, "power": 5, "output": "Apple Juice", "qty": 1},
    "Pear Juice": {"ingredients": {"Pear": 10}, "power": 5, "output": "Pear Juice", "qty": 1},
    "Orange Juice": {"ingredients": {"Orange": 10}, "power": 5, "output": "Orange Juice", "qty": 1},
    "Goat Cheese": {"ingredients": {"Milk": 3}, "power": 2, "output": "Goat Cheese", "qty": 1},
    "Tomato Sauce": {"ingredients": {"Tomato": 5, "Water": 1}, "power": 3, "output": "Tomato Sauce", "qty": 1},
    "Strawberry Jam": {"ingredients": {"Strawberry": 10, "Sugar": 1}, "power": 3, "output": "Strawberry Jam", "qty": 1},
}



# ==========================================
# 7. FARM TYCOON CONFIG
# ==========================================
FARM_ICONS = {
    0: "🟫",   # empty/dirt
    1: "🌊",   # stream
    2: "🌱",   # seedling
    3: "🌿",   # growing
    4: "🌾",   # ready to harvest
    5: "⛰️",   # rock (clearable)
    # 6: reserved
    7: "🧹",   # weeds
    8: "🏚️",   # barn
    9: "🐝",   # beehive
    10: "🦅",  # scarecrow
    11: "💦",  # sprinkler
    12: "🐔",  # chicken
    13: "🐄",  # cow
    14: "🐐",  # goat
    15: "🫧",  # cold frame
    16: "🏡",  # manor
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
    "Goat Pen": {"cost": 300, "id": 14, "desc": "Produces Milk (Year 2+)"},
}

SEED_COST = {
    "Carrot": 5,
    "Wheat": 3,
    "Corn": 4,
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
    "Feed": 5,
}


# ==========================================
# 8. MARKET GARDEN CONFIG
# ==========================================
MG_CROPS = {
    "Carrot": {"icon": "🥕", "family": "Root", "season": ["Spring", "Summer"], "days": 3, "seed_cost": 3, "sell": 8, "nutrient_drain": {"N": 10, "P": 15, "K": 10}},
    "Tomato": {"icon": "🍅", "family": "Fruit", "season": ["Summer"], "days": 4, "seed_cost": 5, "sell": 15, "nutrient_drain": {"N": 20, "P": 12, "K": 15}},
    "Lettuce": {"icon": "🥬", "family": "Leaf", "season": ["Spring", "Autumn"], "days": 2, "seed_cost": 2, "sell": 6, "nutrient_drain": {"N": 12, "P": 5, "K": 8}},
    "Cabbage": {"icon": "🥦", "family": "Brassica", "season": ["Spring", "Autumn"], "days": 4, "seed_cost": 4, "sell": 12, "nutrient_drain": {"N": 22, "P": 8, "K": 12}},
    "Beans": {"icon": "🫘", "family": "Legume", "season": ["Summer"], "days": 3, "seed_cost": 3, "sell": 10, "nutrient_drain": {"N": -10, "P": 8, "K": 8}},
    "Potato": {"icon": "🥔", "family": "Root", "season": ["Spring"], "days": 4, "seed_cost": 3, "sell": 10, "nutrient_drain": {"N": 12, "P": 15, "K": 18}},
    "Onion": {"icon": "🧅", "family": "Allium", "season": ["Spring", "Summer"], "days": 3, "seed_cost": 3, "sell": 9, "nutrient_drain": {"N": 8, "P": 8, "K": 5}},
    "Basil": {"icon": "🌿", "family": "Herb", "season": ["Summer"], "days": 2, "seed_cost": 4, "sell": 12, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Marigold": {"icon": "🌻", "family": "Herb", "season": ["Spring", "Summer"], "days": 2, "seed_cost": 3, "sell": 5, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Sage": {"icon": "🌱", "family": "Herb", "season": ["Spring", "Autumn"], "days": 2, "seed_cost": 4, "sell": 10, "nutrient_drain": {"N": 5, "P": 5, "K": 5}},
    "Sweetcorn": {"icon": "🌽", "family": "Fruit", "season": ["Summer"], "days": 4, "seed_cost": 4, "sell": 12, "nutrient_drain": {"N": 18, "P": 12, "K": 12}},
    "Squash": {"icon": "🎃", "family": "Cucurbit", "season": ["Summer"], "days": 4, "seed_cost": 4, "sell": 11, "nutrient_drain": {"N": 15, "P": 12, "K": 15}},
    "Strawberry": {"icon": "🍓", "family": "Berry", "season": ["Spring", "Summer"], "days": 3, "seed_cost": 6, "sell": 18, "nutrient_drain": {"N": 12, "P": 15, "K": 12}},
    "Peas": {"icon": "🟢", "family": "Legume", "season": ["Spring"], "days": 3, "seed_cost": 3, "sell": 9, "nutrient_drain": {"N": -10, "P": 8, "K": 8}},
    "Beetroot": {"icon": "🔴", "family": "Root", "season": ["Spring", "Autumn"], "days": 3, "seed_cost": 3, "sell": 9, "nutrient_drain": {"N": 8, "P": 12, "K": 12}},
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
}

MG_MARKET_BASE = {
    "Carrot": 8, "Tomato": 15, "Lettuce": 6, "Cabbage": 12, "Beans": 10,
    "Potato": 10, "Onion": 9, "Basil": 12, "Marigold": 5, "Sage": 10,
    "Sweetcorn": 12, "Squash": 11, "Strawberry": 18, "Peas": 9,
    "Beetroot": 9, "Chives": 8, "Borage": 7,
    "Golden Carrot": 30, "Golden Tomato": 50, "Golden Strawberry": 60,
    "Golden Cabbage": 40, "Golden Squash": 40, "Golden Sweetcorn": 50,
}


# ==========================================
# 9. FARM TYCOON — EXPANDED CONFIG
# ==========================================
FARM_CROP_UNLOCKS = {
    "Wheat": {"require": "always", "desc": "Available from start"},
    "Carrot": {"require": "always", "desc": "Available from start"},
    "Corn": {"require": "always", "desc": "Available from start"},
    "Potato": {"require": "harvest_5", "desc": "Harvest 5 crops to unlock"},
    "Cabbage": {"require": "building_Barn", "desc": "Build a Barn to unlock"},
    "Basil": {"require": "building_Beehive", "desc": "Build a Beehive to unlock"},
    "Strawberry": {"require": "building_Scarecrow", "desc": "Build a Scarecrow to unlock"},
    "Pumpkin": {"require": "year_2", "desc": "Reach Year 2 to unlock"},
}

FARM_CROP_SEASONS = {
    "Wheat": ["Spring", "Summer", "Autumn"],
    "Carrot": ["Spring", "Summer"],
    "Corn": ["Summer"],
    "Potato": ["Spring"],
    "Cabbage": ["Spring", "Autumn"],
    "Basil": ["Summer"],
    "Strawberry": ["Spring", "Summer"],
    "Pumpkin": ["Summer", "Autumn"],
}

FARM_CROP_DAYS = {
    "Wheat": 3, "Carrot": 3, "Corn": 3,
    "Potato": 4, "Cabbage": 4, "Basil": 2,
    "Strawberry": 3, "Pumpkin": 5,
}

FARM_SEASONAL_PRICES = {
    "Strawberry": {"Spring": 1.5, "Summer": 1.0, "Autumn": 0.7, "Winter": 0.5},
    "Pumpkin": {"Spring": 0.7, "Summer": 1.0, "Autumn": 1.5, "Winter": 0.5},
    "Basil": {"Spring": 1.2, "Summer": 1.0, "Autumn": 0.8, "Winter": 0.5},
    "Cabbage": {"Spring": 1.0, "Summer": 0.8, "Autumn": 1.3, "Winter": 0.6},
    "Potato": {"Spring": 1.2, "Summer": 1.0, "Autumn": 0.9, "Winter": 0.5},
}

FARM_ROCK_CLEAR_COST = 50

FARM_FISHING = {
    "Fish": {"chance": 0.55, "sell": 15, "icon": "🐟", "desc": "A decent fish"},
    "Eel": {"chance": 0.20, "sell": 25, "icon": "🦎", "desc": "A slippery eel!"},
    "Old Boot": {"chance": 0.18, "sell": 0, "icon": "👢", "desc": "Just an old boot..."},
    "Treasure": {"chance": 0.07, "sell": 100, "icon": "💎", "desc": "A treasure from the depths!"},
}

FARM_CONTRACTS = [
    {"name": "Village Feast", "item": "Wheat", "qty": 5, "reward": 50, "desc": "Supply 5 Wheat for the village feast"},
    {"name": "Carrot Contract", "item": "Carrot", "qty": 5, "reward": 55, "desc": "The market needs 5 Carrots"},
    {"name": "Corn Delivery", "item": "Corn", "qty": 8, "reward": 80, "desc": "Deliver 8 Corn to the mill"},
    {"name": "Baker's Order", "item": "Wheat", "qty": 10, "reward": 90, "desc": "The baker needs 10 Wheat"},
    {"name": "Soup Kitchen", "item": "Potato", "qty": 5, "reward": 65, "desc": "5 Potatoes for the soup kitchen"},
    {"name": "Harvest Festival", "item": "Pumpkin", "qty": 3, "reward": 80, "desc": "3 Pumpkins for the festival"},
    {"name": "Berry Picking", "item": "Strawberry", "qty": 5, "reward": 110, "desc": "5 Strawberries wanted"},
    {"name": "Dairy Order", "item": "Milk", "qty": 3, "reward": 60, "desc": "3 Milk for the dairy"},
    {"name": "Egg Order", "item": "Egg", "qty": 5, "reward": 75, "desc": "5 Eggs for the restaurant"},
]

FARM_WEATHER_EVENTS = [
    {"type": "drought", "seasons": ["Summer"], "chance": 0.08, "desc": "☀️ Drought! Crops without Sprinkler lose 1 day.", "effect": "drought"},
    {"type": "storm", "seasons": ["Autumn"], "chance": 0.06, "desc": "⛈️ Storm! A building was damaged.", "effect": "storm"},
    {"type": "frost", "seasons": ["Spring"], "chance": 0.07, "desc": "🥶 Late frost! Seedlings lost 1 day.", "effect": "frost"},
    {"type": "pest", "seasons": ["Summer"], "chance": 0.08, "desc": "🐛 Pest outbreak! Crops without Scarecrow may be hit.", "effect": "pest"},
    {"type": "bountiful", "seasons": ["Spring"], "chance": 0.05, "desc": "🌸 Bountiful spring! All soil health +10.", "effect": "bountiful"},
]

FARM_DIVERSITY_BONUS = {"min_crops": 3, "bonus": 0.15}


# ==========================================
# 10. MARKET GARDEN — UNLOCK SYSTEM
# ==========================================
MG_STARTING_CROPS = ["Carrot", "Lettuce", "Potato", "Beans", "Onion", "Peas"]

MG_CROP_UNLOCKS = {
    "Tomato": {"require": "total_harvests", "threshold": 5, "desc": "Harvest 5 crops"},
    "Beetroot": {"require": "total_harvests", "threshold": 5, "desc": "Harvest 5 crops"},
    "Cabbage": {"require": "total_earned", "threshold": 200, "desc": "Earn £200 from sales"},
    "Strawberry": {"require": "total_earned", "threshold": 200, "desc": "Earn £200 from sales"},
    "Sweetcorn": {"require": "harvest_family", "family": "Legume", "threshold": 3, "desc": "Harvest 3 Legume crops"},
    "Squash": {"require": "total_earned", "threshold": 500, "desc": "Earn £500 from sales"},
    "Basil": {"require": "has_polytunnel", "desc": "Build a Polytunnel"},
    "Marigold": {"require": "has_polytunnel", "desc": "Build a Polytunnel"},
    "Sage": {"require": "total_earned", "threshold": 500, "desc": "Earn £500 from sales"},
    "Chives": {"require": "harvest_family", "family": "Allium", "threshold": 3, "desc": "Harvest 3 Allium crops"},
    "Borage": {"require": "total_earned", "threshold": 800, "desc": "Earn £800 from sales"},
}

MG_PEST_EVENTS = [
    {"name": "Aphid Outbreak", "seasons": ["Summer"], "chance": 0.08, "affects": ["Fruit", "Leaf"], "desc": "Aphids! Fruit & Leaf crops lose 1 day.", "companions_resist": ["Chives", "Basil", "Marigold"]},
    {"name": "Cabbage White Butterfly", "seasons": ["Spring", "Summer"], "chance": 0.06, "affects": ["Brassica"], "desc": "Cabbage whites! Brassica crops lose 1 day.", "companions_resist": ["Sage", "Chives"]},
    {"name": "Carrot Fly", "seasons": ["Summer"], "chance": 0.06, "affects": ["Root"], "desc": "Carrot fly! Root crops lose 1 day.", "companions_resist": ["Onion", "Chives"]},
    {"name": "Slugs", "seasons": ["Autumn"], "chance": 0.07, "affects": ["Leaf", "Berry"], "desc": "Slugs! Leaf & Berry crops lose 1 day.", "companions_resist": []},
]


# ==========================================
# 11. APIARY CONFIG (Beekeeping Game)
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

# NOTE: APIARY_PRODUCTS uses short display names (e.g. "Summer Honey")
#       while HONEY_TYPES / NECTAR_FLOW use descriptive names (e.g. "Summer Wildflower").
#       Game code should map between them: honey_type → product_name.
APIARY_PRODUCTS = {
    "Spring Honey": {"icon": "🍯", "value": 8, "cat": "raw"},
    "Summer Honey": {"icon": "🍯", "value": 12, "cat": "raw"},
    "Heather Honey": {"icon": "🍯", "value": 20, "cat": "raw"},
    "Autumn Honey": {"icon": "🍯", "value": 10, "cat": "raw"},
    "Beeswax": {"icon": "🕯️", "value": 5, "cat": "raw"},
    "Propolis": {"icon": "🟤", "value": 15, "cat": "raw"},
    "Mead": {"icon": "🍺", "value": 45, "cat": "processed"},
    "Beeswax Candles": {"icon": "🕯️", "value": 18, "cat": "processed"},
    "Propolis Tincture": {"icon": "🧴", "value": 30, "cat": "processed"},
    "Lip Balm": {"icon": "💋", "value": 15, "cat": "processed"},
    "Wax Wraps": {"icon": "📦", "value": 22, "cat": "processed"},
}

APIARY_PROCESSING = {
    "Mead": {"ingredients": {"Summer Honey": 3}, "weeks": 4, "icon": "🍺", "desc": "Fermented honey wine"},
    "Beeswax Candles": {"ingredients": {"Beeswax": 3}, "weeks": 1, "icon": "🕯️", "desc": "Hand-dipped candles"},
    "Propolis Tincture": {"ingredients": {"Propolis": 2}, "weeks": 2, "icon": "🧴", "desc": "Natural antiseptic tincture"},
    "Lip Balm": {"ingredients": {"Beeswax": 1, "Summer Honey": 1}, "weeks": 1, "icon": "💋", "desc": "Moisturising lip balm"},
    "Wax Wraps": {"ingredients": {"Beeswax": 2}, "weeks": 1, "icon": "📦", "desc": "Eco-friendly food wraps"},
}

# Merged: foulbrood, mice, robbing + wasp_attack (formerly in separate dict)
APIARY_THREATS = {
    "foulbrood": {"name": "American Foulbrood", "icon": "🦠", "season": ["Summer"], "chance": 0.03, "desc": "Deadly bacterial disease — notifiable!"},
    "mice": {"name": "Mouse Damage", "icon": "🐭", "season": ["Winter"], "chance": 0.08, "desc": "Mice eat stores and damage comb"},
    "robbing": {"name": "Robbing", "icon": "🐝", "season": ["Summer", "Autumn"], "chance": 0.05, "desc": "Other bees steal honey from weak hives"},
    "wasp_attack": {"name": "Wasp Attack", "icon": "🪱", "season": ["August", "September"], "chance": 0.08, "desc": "Wasps invade weak hives to steal honey and kill brood.", "damage": {"honey_frames": -2, "population": -3000}},
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
# 12. APIARY — SMOKER, TEMPERAMENT, WASPS, EDUCATION & MENTOR
# ==========================================
SMOKER_CONFIG = {
    "cost": 2,
    "aggression_reduction": 0.7,
    "inspection_quality_bonus": 0.15,
    "smoke_duration_weeks": 1,
    "sting_chance_no_smoke": {
        "gentle": 0.05,
        "moderate": 0.20,
        "defensive": 0.45,
    },
    "sting_chance_with_smoke": {
        "gentle": 0.01,
        "moderate": 0.05,
        "defensive": 0.12,
    },
}

HIVE_TEMPERAMENTS = {
    "gentle": {
        "label": "Gentle",
        "icon": "🕊️",
        "desc": "Calm and easy to work with. Low sting risk.",
        "growth_bonus": 0.0,
        "swarm_chance_mult": 1.0,
    },
    "moderate": {
        "label": "Moderate",
        "icon": "🐝",
        "desc": "Standard temperament. Use smoker for inspections.",
        "growth_bonus": 0.02,
        "swarm_chance_mult": 1.1,
    },
    "defensive": {
        "label": "Defensive",
        "icon": "😠",
        "desc": "Aggressive colony. Always smoke before inspecting!",
        "growth_bonus": 0.05,
        "swarm_chance_mult": 1.2,
    },
}

QUEEN_MARK_COLOURS = {
    "2023": {"colour": "#E53935", "name": "Red"},
    "2024": {"colour": "#1E88E5", "name": "Blue"},
    "2025": {"colour": "#FDD835", "name": "Yellow"},
    "2026": {"colour": "#E0E0E0", "name": "White"},
    "2027": {"colour": "#E53935", "name": "Red"},
    "2028": {"colour": "#1E88E5", "name": "Blue"},
}

LEVEL_UNLOCKS = {
    1: {"max_hives": 2, "label": "Beginner", "features": ["inspect", "feed", "market"]},
    2: {"max_hives": 3, "label": "Novice", "features": ["inspect", "feed", "market", "super"]},
    3: {"max_hives": 4, "label": "Intermediate", "features": ["inspect", "feed", "market", "super", "processing"]},
    4: {"max_hives": 5, "label": "Experienced", "features": ["inspect", "feed", "market", "super", "processing", "swarm"]},
    5: {"max_hives": 6, "label": "Master", "features": ["inspect", "feed", "market", "super", "processing", "swarm", "requeen"]},
}

APIARY_EDUCATION_FACTS = {
    "queen_present": [
        "A queen can lay up to 2,000 eggs per day during peak season!",
        "The queen produces a pheromone called 'queen substance' that keeps the colony calm and working together.",
        "A queen bee can live for 3-5 years, much longer than worker bees who live just 6 weeks in summer.",
        "The queen is the only bee in the hive that can lay fertilised eggs that become workers or new queens.",
    ],
    "queen_failing": [
        "When a queen runs out of sperm stored in her spermatheca, she can only lay unfertilised eggs that become drones.",
        "A failing queen is often called a 'drone-layer' because she produces only male bees.",
        "Beekeepers mark queens with a coloured dot — the colour indicates the year she was born!",
    ],
    "varroa_low": [
        "Varroa destructor is an external parasitic mite that attaches to bees and feeds on their fat bodies.",
        "Varroa were originally parasites of Asian honey bees (Apis cerana) but jumped to Western honey bees (Apis mellifera).",
    ],
    "varroa_high": [
        "High varroa levels weaken individual bees by spreading viruses like Deformed Wing Virus (DWV).",
        "A varroa count above 3 per 300 bees (1%) in summer indicates treatment is needed soon.",
        "Leaving varroa untreated is the #1 reason colonies die in the UK over winter.",
    ],
    "swarm_season": [
        "Swarming is the natural way bees reproduce — the old queen leaves with half the colony to find a new home.",
        "A primary swarm contains the old queen. After she leaves, the remaining bees raise a new queen from a young larva.",
        "Beekeepers prevent swarming by removing queen cells and providing more space (supers).",
    ],
    "honey_stores_good": [
        "Bees need approximately 18-22kg of honey (about 7-9 full frames) to survive a UK winter.",
        "A strong colony can collect enough nectar to make 20-30kg of surplus honey for the beekeeper in a good year!",
    ],
    "honey_stores_low": [
        "If stores are low in autumn, feed thick sugar syrup (2:1 ratio) so bees can store it for winter.",
        "In winter, bees cluster together and vibrate their flight muscles to generate heat — this requires lots of stored energy.",
    ],
    "winter": [
        "In winter, the bees form a tight cluster around the queen to stay warm, keeping the centre at about 35°C!",
        "You should NEVER open a hive in winter unless absolutely necessary — it breaks the cluster and the cold can kill the colony.",
        "Winter is when you 'heft' the hive — lift it slightly to judge the weight of stores inside.",
    ],
    "super": [
        "A 'super' (short for superstructure) is a box added on top of the brood box for bees to store surplus honey.",
        "A queen excluder stops the queen from laying eggs in the super, keeping honey frames clean for harvest.",
    ],
    "foulbrood": [
        "American Foulbrood (AFB) is a notifiable disease in the UK — you MUST report it to the National Bee Unit!",
        "AFB produces a distinctive 'ropiness' — if you poke a larva with a matchstick, it strings out like glue.",
        "European Foulbrood (EFB) is also notifiable but less severe — the larva dies before it's capped.",
    ],
}

MENTOR_TIPS = {
    "first_week": "Welcome to your apiary! This is hive 'Willow'. Start by inspecting it — click the Inspect tab. ☝️",
    "first_inspect": "Great! You've inspected your hive. The frame diagram shows what's inside: honey, pollen, brood (baby bees), and more.",
    "first_spring": "Spring is here! Bees are building up fast. Check for queen cells — if you see them, consider swarm control.",
    "first_summer": "The nectar flow is strong! If your colony is filling frames, add a super so they have space to store honey.",
    "first_harvest": "When a super has 4+ frames of honey, you can harvest! Go to the Market tab to extract and sell.",
    "first_autumn": "Autumn means preparing for winter. Feed thick syrup and treat for varroa before the cold sets in.",
    "first_winter": "In winter, don't open the hive! Just heft it (lift) to check stores are sufficient. Feed fondant if light.",
    "varroa_warning": "🪲 Varroa levels are rising! Treat in August (Apivar strips) or December (Oxalic acid).",
    "swarm_warning": "🐝 Queen cells found! This colony wants to swarm. Either split it or remove the queen cells.",
    "low_stores": "🍯 Honey stores are low! Feed syrup in spring, thick syrup in autumn, or fondant in winter.",
    "aggressive_hive": "😠 This colony has a defensive temperament! Always use your smoker before inspecting.",
    "first_foulbrood": "🦠 Foulbrood detected! This is a serious disease. Treat immediately — £25 for treatment.",
    "first_processing": "⚗️ You can now process products! Mead, candles, and more are available in the Market tab.",
    "first_swarm_catch": "🪤 Swarm season! You can try catching a swarm to start a new colony — it's free but not guaranteed.",
}


# ==========================================
# 13. WILD KITCHEN CONFIG
# ==========================================
BASICS = ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol", "Salt", "Flour"]


# Eco-Village uses a reduced basics list (only Water is free)
ECO_BASICS = ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol", "Salt", "Flour"]


KITCHEN_RECIPES = [
    # --- BEGINNER (diff: 1) ---
    {"name": "Nettle Soup", "ingredients": {"Nettle": 5, "Water": 1},
     "prep_questions": [{"q": "Why must nettles be cooked?", "opts": ["To remove the sting", "To make them sweet", "To change color"], "a": "To remove the sting"}],
     "icon": "🥣", "desc": "A rich, green soup.", "diff": 1,
     "benefits": "High in Iron.", "benefit_detail": "Nettles are remarkably high in iron, supporting healthy blood and reducing fatigue. Used for centuries as a spring tonic to replenish the body after winter.", "benefit_tags": ["Iron", "Blood", "Energy"], "pot_colour": "#4a7c3f"},

    {"name": "Wild Garlic Pesto", "ingredients": {"Wild Garlic": 10, "Oil": 1},
     "prep_questions": [{"q": "Which part of Wild Garlic is edible?", "opts": ["Only the flowers", "Leaves, flowers, and bulbs", "Only the roots"], "a": "Leaves, flowers, and bulbs"}],
     "icon": "🥗", "desc": "A fragrant pesto.", "diff": 1,
     "benefits": "Antibacterial.", "benefit_detail": "Wild Garlic contains allicin, a natural antibacterial compound that supports heart health and helps fight infections.", "benefit_tags": ["Heart", "Immune", "Antibacterial"], "pot_colour": "#3d8b37"},

    {"name": "Dandelion Salad", "ingredients": {"Dandelion": 5},
     "prep_questions": [{"q": "When is best to harvest Dandelion leaves?", "opts": ["When the flower is yellow", "Before the flower opens (young)", "In winter"], "a": "Before the flower opens (young)"}],
     "icon": "🥗", "desc": "Young leaves are less bitter.", "diff": 1,
     "benefits": "Liver health.", "benefit_detail": "Dandelion leaves are a powerful liver tonic, stimulating bile production and aiding digestion. Young leaves are tender and less bitter.", "benefit_tags": ["Liver", "Digestion", "Vitamins"], "pot_colour": "#8db600"},

    {"name": "Three-Cornered Leek Omelette", "ingredients": {"Three-Cornered Leek": 5, "Eggs": 2},
     "prep_questions": [{"q": "How to ID Three-Cornered Leek?", "opts": ["Smells of garlic, triangular stem", "Blue flowers, round stem", "Yellow flowers, spiky"], "a": "Smells of garlic, triangular stem"}],
     "icon": "🍳", "desc": "A forager's breakfast.", "diff": 1,
     "benefits": "High protein.", "benefit_detail": "Packed with protein from eggs and the natural antibacterial properties of wild garlic. A sustaining breakfast for a day outdoors.", "benefit_tags": ["Protein", "Energy", "Immune"], "pot_colour": "#d4a843"},

    {"name": "Pine Needle Tea", "ingredients": {"Pine Needles": 10, "Water": 1},
     "prep_questions": [{"q": "How do you identify SAFE Pine needles?", "opts": ["Flat needles (Yew)", "Round needles in bundles", "Blue needles"], "a": "Round needles in bundles"}],
     "icon": "🍵", "desc": "High in Vitamin C.", "diff": 1,
     "benefits": "Vitamin C boost.", "benefit_detail": "Pine needles contain up to 5 times more Vitamin C than oranges, plus vitamin A. A warming brew that supports the immune system and respiratory health.", "benefit_tags": ["Vitamin C", "Immune", "Respiratory"], "pot_colour": "#6b8e3a"},

    {"name": "Beech Leaf Liqueur", "ingredients": {"Beech Leaves": 20, "Sugar": 1, "Alcohol": 1},
     "prep_questions": [{"q": "When should you pick Beech leaves?", "opts": ["Autumn (Brown)", "Spring (Young/Transparent)", "Winter"], "a": "Spring (Young/Transparent)"}],
     "icon": "🥃", "desc": "A sweet, gin-based liquor.", "diff": 1,
     "benefits": "Traditional tonic.", "benefit_detail": "A traditional country liqueur made from young beech leaves, steeped in gin with sugar. Aids digestion and lifts the spirits.", "benefit_tags": ["Digestion", "Traditional", "Relaxation"], "pot_colour": "#a8c43a"},

    {"name": "Chickweed Salad", "ingredients": {"Chickweed": 10},
     "prep_questions": [{"q": "How do you identify Chickweed?", "opts": ["Line of hairs on stem", "Purple spots on stem", "Blue flowers"], "a": "Line of hairs on stem"}],
     "icon": "🥗", "desc": "A mild, nutritious weed.", "diff": 1,
     "benefits": "Vitamins.", "benefit_detail": "Chickweed is rich in vitamins A, B, and C, plus minerals like iron and calcium. Traditionally used to soothe skin and support digestion.", "benefit_tags": ["Vitamins", "Skin", "Minerals"], "pot_colour": "#78a844"},

    {"name": "Wild Strawberry Jam", "ingredients": {"Wild Strawberry": 20, "Sugar": 1},
     "prep_questions": [{"q": "How do wild strawberries differ from barren strawberry?", "opts": ["Barren has petals with gaps", "Wild has blue flowers", "Barren has hairy leaves"], "a": "Barren has petals with gaps"}],
     "icon": "🍯", "desc": "Tiny but intense flavor.", "diff": 1,
     "benefits": "Antioxidants.", "benefit_detail": "Wild strawberries pack far more flavour and antioxidants than their cultivated cousins. Rich in vitamin C and manganese, supporting heart and skin health.", "benefit_tags": ["Antioxidants", "Heart", "Skin"], "pot_colour": "#c41e3a"},

    {"name": "Roasted Hazelnuts", "ingredients": {"Hazelnut": 10},
     "prep_questions": [{"q": "What indicates a ripe Hazelnut?", "opts": ["Green husk", "Brown shell and leafy husk", "No leaves"], "a": "Brown shell and leafy husk"}],
     "icon": "🌰", "desc": "Autumn treat.", "diff": 1,
     "benefits": "Heart health.", "benefit_detail": "Hazelnuts are rich in healthy fats, vitamin E, and folate. Roasting intensifies their flavour and makes the nutrients more bioavailable.", "benefit_tags": ["Heart", "Brain", "Healthy Fats"], "pot_colour": "#8b6914"},

    {"name": "Sea Purslane Salad", "ingredients": {"Sea Purslane": 10},
     "prep_questions": [{"q": "What is the main precaution with Sea Purslane?", "opts": ["It is very salty", "It is poisonous raw", "It has thorns"], "a": "It is very salty"}],
     "icon": "🥗", "desc": "Salty coastal green.", "diff": 1,
     "benefits": "Minerals.", "benefit_detail": "Sea Purslane is naturally rich in iodine and minerals from coastal soils. Its saltiness means little seasoning is needed — nature's own seasoning.", "benefit_tags": ["Minerals", "Iodine", "Hydration"], "pot_colour": "#6b8e5a"},

    # --- INTERMEDIATE (diff: 2) ---
    {"name": "Dandelion Coffee", "ingredients": {"Dandelion": 20},
     "prep_questions": [
         {"q": "Which part is used for coffee?", "opts": ["Leaves", "Flowers", "Roots"], "a": "Roots"},
         {"q": "How must the roots be prepared?", "opts": ["Eaten raw", "Roasted and ground", "Boiled whole"], "a": "Roasted and ground"},
     ],
     "icon": "☕", "desc": "Caffeine-free coffee substitute.", "diff": 2,
     "benefits": "Liver detox.", "benefit_detail": "Dandelion root coffee is a powerful liver detoxifier that tastes remarkably like real coffee. Roasting transforms the bitter root into a rich, earthy brew.", "benefit_tags": ["Liver", "Detox", "Energy"], "pot_colour": "#3e2723"},

    {"name": "Elderflower Cordial", "ingredients": {"Elderflower": 10, "Sugar": 1},
     "prep_questions": [
         {"q": "Why should you not wash Elderflowers?", "opts": ["Loses pollen (flavor)", "Becomes poisonous", "Petals fall off"], "a": "Loses pollen (flavor)"},
         {"q": "What must you check for before cooking?", "opts": ["Spiders", "Bugs/Maggots", "Birds"], "a": "Bugs/Maggots"},
     ],
     "icon": "🥤", "desc": "A sweet summery drink.", "diff": 2,
     "benefits": "Vitamin C.", "benefit_detail": "Elderflower cordial captures the essence of early summer. The flowers are rich in vitamin C and have natural anti-inflammatory properties, traditionally used to ease colds and hay fever.", "benefit_tags": ["Vitamin C", "Immune", "Anti-inflammatory"], "pot_colour": "#f5deb3"},

    {"name": "Blackberry Jam", "ingredients": {"Blackberry": 20, "Sugar": 1},
     "prep_questions": [
         {"q": "What must you check for when picking?", "opts": ["Check for bugs", "Check if they are red", "Check for thorns"], "a": "Check for bugs"},
         {"q": "What helps the jam set (thicken)?", "opts": ["Water", "Pectin (naturally in fruit)", "Oil"], "a": "Pectin (naturally in fruit)"},
     ],
     "icon": "🍯", "desc": "Preserved summer in a jar.", "diff": 2,
     "benefits": "Fiber.", "benefit_detail": "Blackberries are one of nature's richest sources of antioxidants and fibre. Cooking them into jam concentrates their goodness, though the sugar content means enjoy in moderation.", "benefit_tags": ["Fiber", "Antioxidants", "Digestion"], "pot_colour": "#4a0e2e"},

    {"name": "Rosehip Syrup", "ingredients": {"Rosehips": 15, "Sugar": 1},
     "prep_questions": [
         {"q": "Why remove the seeds?", "opts": ["Bitter", "Itchy irritation", "Poisonous"], "a": "Itchy irritation"},
         {"q": "What vitamin are Rosehips famous for?", "opts": ["Vitamin A", "Vitamin C", "Vitamin D"], "a": "Vitamin C"},
     ],
     "icon": "🧴", "desc": "Rich in Vitamin C.", "diff": 2,
     "benefits": "Immune boost.", "benefit_detail": "Rosehips contain 20 times more vitamin C than oranges by weight. This syrup has been used for centuries to boost immunity, ease joint inflammation, and fight off winter colds.", "benefit_tags": ["Vitamin C", "Immune", "Joints"], "pot_colour": "#cc5500"},

    {"name": "Sorrel Soup", "ingredients": {"Sorrel": 15, "Water": 1},
     "prep_questions": [
         {"q": "What gives Sorrel its sour taste?", "opts": ["Sugar", "Oxalic Acid", "Citrus"], "a": "Oxalic Acid"},
         {"q": "Who should avoid large amounts?", "opts": ["Children", "People with kidney issues", "Elderly"], "a": "People with kidney issues"},
     ],
     "icon": "🥣", "desc": "Tangy and refreshing.", "diff": 2,
     "benefits": "Vitamin C.", "benefit_detail": "Sorrel's distinctive lemony flavour comes from oxalic acid. Rich in vitamins A and C, it supports immune health — but those with kidney issues should enjoy it in moderation.", "benefit_tags": ["Vitamin C", "Iron", "Digestion"], "pot_colour": "#5a8a3a"},

    {"name": "Hawthorn Ketchup", "ingredients": {"Hawthorn": 30, "Sugar": 1},
     "prep_questions": [
         {"q": "What do Hawthorn berries look like?", "opts": ["Blue pods", "Small red berries", "Blackberries"], "a": "Small red berries"},
         {"q": "What should you avoid when eating?", "opts": ["The skin", "The seeds (pips)", "The stem"], "a": "The seeds (pips)"},
     ],
     "icon": "🍅", "desc": "Tomato ketchup alternative.", "diff": 2,
     "benefits": "Heart health.", "benefit_detail": "Hawthorn berries are one of nature's most powerful heart medicines, traditionally used to support cardiovascular health, regulate blood pressure, and improve circulation.", "benefit_tags": ["Heart", "Circulation", "Antioxidants"], "pot_colour": "#b22222"},

    {"name": "Sweet Chestnut Roast", "ingredients": {"Sweet Chestnut": 20},
     "prep_questions": [
         {"q": "How does the case differ from Horse Chestnut?", "opts": ["Smooth/Warty", "Very spiky", "Green"], "a": "Very spiky"},
         {"q": "What must you do before roasting?", "opts": ["Peel them", "Score the shell", "Boil for 1 hour"], "a": "Score the shell"},
     ],
     "icon": "🌰", "desc": "Roasting over an open fire.", "diff": 2,
     "benefits": "Starch source.", "benefit_detail": "Sweet chestnuts are unique among nuts — low in fat and high in complex carbohydrates. A natural energy source and gluten-free flour alternative when dried and ground.", "benefit_tags": ["Starch", "Energy", "Gluten-free"], "pot_colour": "#8b4513"},

    {"name": "Marsh Samphire Sauté", "ingredients": {"Marsh Samphire": 15, "Butter": 1},
     "prep_questions": [
         {"q": "Where does Samphire grow?", "opts": ["Dry Meadows", "Saltmarshes/Mud", "Trees"], "a": "Saltmarshes/Mud"},
         {"q": "How do you harvest sustainably?", "opts": ["Pull up roots", "Cut top 2 inches", "Dig with trowel"], "a": "Cut top 2 inches"},
     ],
     "icon": "🥦", "desc": "Sea asparagus.", "diff": 2,
     "benefits": "Iodine.", "benefit_detail": "Marsh Samphire is rich in iodine, vitamin A, and vitamin C — a nutritional powerhouse from the coast. Its natural saltiness means no added salt is needed.", "benefit_tags": ["Iodine", "Minerals", "Low Calorie"], "pot_colour": "#556b2f"},

    # --- ADVANCED (diff: 3) ---
    {"name": "Acorn Coffee", "ingredients": {"Oak (Acorns)": 20},
     "prep_questions": [
         {"q": "Why not eat raw?", "opts": ["Too hard", "Contain tannins (bitter)", "Protected"], "a": "Contain tannins (bitter)"},
         {"q": "How to remove tannins?", "opts": ["Leaching (soaking)", "Freezing", "Burning"], "a": "Leaching (soaking)"},
         {"q": "When to harvest?", "opts": ["Green", "Brown (ripe)", "White"], "a": "Brown (ripe)"},
     ],
     "icon": "☕", "desc": "Must be leached first.", "diff": 3,
     "benefits": "Gluten-free.", "benefit_detail": "Acorns were a staple food for thousands of years. Once the bitter tannins are leached out, acorns provide a rich, gluten-free flour and a coffee-like drink packed with complex carbohydrates.", "benefit_tags": ["Gluten-free", "Starch", "Traditional"], "pot_colour": "#5c3317"},

    {"name": "Chanterelle Risotto", "ingredients": {"Chanterelle": 10, "Rice": 1},
     "prep_questions": [
         {"q": "How to ID Chanterelle?", "opts": ["True gills (sheets)", "False gills (ridges)", "Sponge"], "a": "False gills (ridges)"},
         {"q": "What does it smell like?", "opts": ["Aniseed/Apricot", "Mud", "Nothing"], "a": "Aniseed/Apricot"},
         {"q": "Danger lookalike?", "opts": ["False Chanterelle", "Death Cap", "Field Mushroom"], "a": "False Chanterelle"},
     ],
     "icon": "🍚", "desc": "A gourmet wild meal.", "diff": 3,
     "benefits": "Vitamin D.", "benefit_detail": "Chanterelles are one of the few natural sources of vitamin D2, essential for bone health and immune function. Their apricot scent and peppery taste make them one of the world's finest wild foods.", "benefit_tags": ["Vitamin D", "Protein", "Immune"], "pot_colour": "#daa520"},

    {"name": "Crab Apple Jelly", "ingredients": {"Crab Apple": 25, "Sugar": 1},
     "prep_questions": [
         {"q": "Why not eat raw?", "opts": ["Poisonous", "Too tart/sour", "Too hard"], "a": "Too tart/sour"},
         {"q": "Why is it good for jelly?", "opts": ["High Pectin", "Red Color", "Soft skin"], "a": "High Pectin"},
         {"q": "What to remove?", "opts": ["Skin", "Seeds and stems", "Nothing"], "a": "Seeds and stems"},
     ],
     "icon": "🍯", "desc": "High pectin.", "diff": 3,
     "benefits": "Pectin source.", "benefit_detail": "Crab apples are one of the richest natural sources of pectin, the setting agent that makes jelly possible. Their sharp flavour creates a beautiful ruby jelly that pairs with anything from toast to roast pork.", "benefit_tags": ["Pectin", "Digestion", "Heart"], "pot_colour": "#dc143c"},

    {"name": "Wood Ear Stir-fry", "ingredients": {"Wood Ear (Jelly Ear)": 10, "Oil": 1},
     "prep_questions": [
         {"q": "Where does it grow?", "opts": ["Ground", "Elder trees", "Pine trees"], "a": "Elder trees"},
         {"q": "Texture?", "opts": ["Soft", "Jelly/Rubbery", "Crunchy"], "a": "Jelly/Rubbery"},
         {"q": "Must be cooked?", "opts": ["Yes", "No", "Only if old"], "a": "Yes"},
     ],
     "icon": "🥡", "desc": "Jelly fungus.", "diff": 3,
     "benefits": "Blood circulation.", "benefit_detail": "Wood Ear has been used in Chinese medicine for centuries to improve blood circulation and lower cholesterol. Its unique jelly-rubbery texture absorbs flavours beautifully in stir-fries.", "benefit_tags": ["Circulation", "Iron", "Minerals"], "pot_colour": "#4a3728"},

    {"name": "Morel Risotto", "ingredients": {"Morel": 10, "Rice": 1},
     "prep_questions": [
         {"q": "Cap texture?", "opts": ["Smooth", "Honeycomb pits", "Wrinkled brain"], "a": "Honeycomb pits"},
         {"q": "Inside?", "opts": ["Solid", "Chambered", "Hollow"], "a": "Hollow"},
         {"q": "Danger lookalike?", "opts": ["True Morel", "False Morel", "Chanterelle"], "a": "False Morel"},
     ],
     "icon": "🍚", "desc": "Spring delicacy.", "diff": 3,
     "benefits": "Vitamin D.", "benefit_detail": "Morels are among the most prized wild mushrooms in the world. Rich in vitamin D, copper, and manganese, they support bone health and immune function — but must always be cooked thoroughly.", "benefit_tags": ["Vitamin D", "Protein", "Immune"], "pot_colour": "#c4a35a"},

    {"name": "Burdock Root Stew", "ingredients": {"Burdock (Root)": 10, "Water": 1},
     "prep_questions": [
         {"q": "Which root to dig?", "opts": ["Flowering plant", "First year plant", "Any"], "a": "First year plant"},
         {"q": "Legal issue?", "opts": ["None", "Uprooting illegal without permission", "Poisonous"], "a": "Uprooting illegal without permission"},
         {"q": "Taste?", "opts": ["Sweet", "Earthy/Artichoke", "Bitter"], "a": "Earthy/Artichoke"},
     ],
     "icon": "🍲", "desc": "Requires digging.", "diff": 3,
     "benefits": "Blood purifier.", "benefit_detail": "Burdock root has been used for millennia as a blood purifier and liver tonic. Its earthy, artichoke-like flavour makes a deeply nourishing stew — but remember, uprooting plants without landowner permission is illegal.", "benefit_tags": ["Liver", "Blood", "Detox"], "pot_colour": "#6b4226"},

    {"name": "Cockles in Vinegar", "ingredients": {"Cockles": 20, "Vinegar": 1},
     "prep_questions": [
         {"q": "Shell shape?", "opts": ["Smooth", "Ribbed/Ridged", "Spiral"], "a": "Ribbed/Ridged"},
         {"q": "Safety check?", "opts": ["Red tide/Pollution", "Size", "Color"], "a": "Red tide/Pollution"},
         {"q": "Cooking?", "opts": ["Eat raw", "Steam until open", "Fry"], "a": "Steam until open"},
     ],
     "icon": "🥣", "desc": "Coastal shellfish.", "diff": 3,
     "benefits": "Protein.", "benefit_detail": "Cockles are a protein-rich coastal delicacy, packed with iodine, iron, and vitamin B12. Always check for red tide warnings before harvesting, and steam until every shell opens.", "benefit_tags": ["Protein", "Iodine", "Minerals"], "pot_colour": "#e8d5b5"},
]


# ==========================================
# 14. SURVIVAL SCHOOL — ENHANCED CONFIG
# ==========================================

# Plant mastery thresholds (times correctly identified)
MASTERY_LEVELS = {
    "discovered": 1,
    "learned": 3,
    "mastered": 5,
}

DIFFICULTY_MODES = {
    "patrol": {
        "name": "🌿 Patrol",
        "desc": "Learn at your pace. No timer. Detailed explanations.",
        "timer": None,
        "lives": 3,
        "points_multiplier": 1,
        "wrong_consequence": True,
    },
    "field_test": {
        "name": "🔍 Field Test",
        "desc": "30-second timer per question. Prove you know it.",
        "timer": 30,
        "lives": 3,
        "points_multiplier": 1.5,
        "wrong_consequence": True,
    },
    "survival": {
        "name": "☠️ Survival",
        "desc": "15-second timer. 1 life. Double points. Expert only.",
        "timer": 15,
        "lives": 1,
        "points_multiplier": 2,
        "wrong_consequence": True,
    },
}

STREAK_MILESTONES = [
    {"streak": 3, "title": "Warming Up!", "icon": "🔥", "bonus_xp": 0},
    {"streak": 5, "title": "Hot Streak!", "icon": "🔥", "bonus_xp": 0},
    {"streak": 10, "title": "On Fire!", "icon": "🔥🔥", "bonus_xp": 50},
    {"streak": 15, "title": "Unstoppable!", "icon": "🔥🔥🔥", "bonus_xp": 75},
    {"streak": 20, "title": "Legendary!", "icon": "⭐", "bonus_xp": 100},
]

WRONG_CONSEQUENCES = {
    "survival": {
        "DEADLY": "In real life, this mistake could be fatal. {danger_plant} contains toxins that cause {symptoms}. Always double-check before eating anything in the wild.",
        "EXTREME": "This is an extremely dangerous mistake. {danger_plant} can cause {symptoms}. Hospital treatment would be needed immediately.",
        "HIGH": "A dangerous confusion. {danger_plant} can cause {symptoms}. This is why positive identification is essential.",
        "POISONOUS": "{danger_plant} is poisonous and can cause {symptoms}. Never eat a plant unless you're 100% certain.",
        "default": "{danger_plant} is dangerous and should never be consumed. This is exactly the kind of mistake that gets foragers into trouble.",
    },
    "habitat": "Knowing where plants grow is essential for efficient foraging. You could waste hours searching in the wrong habitat — or worse, find a dangerous lookalike in the wrong place.",
    "identification": "Misidentifying plants is the #1 cause of foraging accidents. Always check multiple identification features, not just one.",
    "lookalike": "Confusing safe plants with dangerous lookalikes is how most foraging accidents happen. This is the most important skill to practice.",
    "parts": "Eating the wrong part of an otherwise edible plant can still make you ill. Always confirm which parts are safe before consuming.",
    "season": "Foraging at the wrong time means plants may not be available, or worse — may be toxic at certain stages of growth.",
    "warning": "Safety warnings exist because people have been harmed. Ignoring them is how accidents happen.",
    "bonus": "Bonus rounds test deeper knowledge. Missing these means there are gaps in your understanding.",
}

CORRECT_BENEFITS = {
    "survival": "You've correctly identified the safe plant. This knowledge could genuinely save your life in a wild situation.",
    "habitat": "Knowing where to find plants means you can forage efficiently and avoid searching in the wrong places.",
    "identification": "Strong identification skills are the foundation of safe foraging. Every correct ID builds your confidence and knowledge.",
    "lookalike": "Recognising dangerous lookalikes is the most critical foraging skill. You've just demonstrated real competence.",
    "parts": "Knowing which parts are edible maximises what you can safely harvest while avoiding potential toxins in other parts.",
    "season": "Seasonal knowledge means you know when plants are at their best and safest — and when to leave them alone.",
    "warning": "Understanding safety warnings protects you and others. This knowledge could prevent a serious accident.",
    "bonus": "Excellent recall under pressure! Deep knowledge is what separates experienced foragers from beginners.",
}

EMERGENCY_SCENARIOS = [
    {
        "id": "hike_rain",
        "scenario": "You're hiking in the Lake District. It's been raining for two days and you're hungry. You spot berries on a low bush...",
        "setting": "Lake District, October, raining",
        "follow_up_types": ["lookalike", "habitat"],
    },
    {
        "id": "coastal_walk",
        "scenario": "Walking along a coastal path in Cornwall, you notice some greens growing on the cliff edge. They look familiar but the sea spray makes identification tricky...",
        "setting": "Cornwall coast, July, windy",
        "follow_up_types": ["habitat", "identification"],
    },
    {
        "id": "forest_camp",
        "scenario": "You've set up camp in a forest. Dawn breaks and you need breakfast. Near your tent, two similar-looking plants are growing side by side...",
        "setting": "Forest, May, damp morning",
        "follow_up_types": ["survival", "lookalike"],
    },
    {
        "id": "river_crossing",
        "scenario": "Crossing a riverbank, you spot some leafy greens growing in the mud. Your water supply is running low and these look like they could provide both food and moisture...",
        "setting": "Riverbank, August, hot",
        "follow_up_types": ["parts", "habitat"],
    },
    {
        "id": "winter_foraging",
        "scenario": "It's a cold January and you're short on food. Most plants are dormant, but you notice some evergreens and roots that might be edible...",
        "setting": "Countryside, January, freezing",
        "follow_up_types": ["season", "parts"],
    },
    {
        "id": "garden_escape",
        "scenario": "You're in an overgrown garden and spot what looks like a cultivated herb growing wild. But the garden also has ornamental plants that look very similar...",
        "setting": "Overgrown garden, June",
        "follow_up_types": ["lookalike", "identification"],
    },
    {
        "id": "hedgerow_harvest",
        "scenario": "Walking home through the hedgerows in September, you see an abundance of berries and nuts. But which ones are safe? Some look tempting but could be toxic...",
        "setting": "Hedgerow, September, mild",
        "follow_up_types": ["lookalike", "season"],
    },
    {
        "id": "marsh_find",
        "scenario": "Exploring marshland, you spot some unfamiliar plants. The wet ground means identification is harder — mud and water can disguise key features...",
        "setting": "Marsh, March, foggy",
        "follow_up_types": ["habitat", "identification"],
    },
]
