# lessons_data.py — Structured learning modules for Rocen Homesteady
# ═══════════════════════════════════════════════════════════════════════
#
# TABLE OF CONTENTS
# ═══════════════════
#
# 🌿 FORAGING PATH
#   01. Introduction to Foraging
#   02. Easy Plants to Identify
#   03. The Carrot Family
#   04. Mushroom Foraging
#   05. The Law of the Land
#   06. The Coastal Code
#   07. Winter Foraging
#   08. The Cabbage Family
#   09. UK Foraging Law: The Complete Guide
#   10. Trees & Hedgerows
#   11. Foraging Through the Seasons
#   12. Medicinal Plants & Herbal Remedies
#   13. Seaweed & Shellfish Foraging
#   14. Foraging in Scotland: Different Rules
#
# 🏘️ OFF-GRID LIVING PATH
#   15. Introduction to Off-Grid Living
#   16. Water: Collection, Filtration & Storage
#   17. Power: Solar, Wind & Alternatives
#   18. Preserving & Storing Food
#   19. Building & Planning: OPD in Wales
#
# 🚜 HOMESTEADING PATH
#   20. Keeping Chickens
#   21. Ducks & Geese
#   22. Keeping Goats
#   23. Starting an Orchard
#   24. Composting & Soil Health
#   25. Small-Scale Vegetable Growing
#   26. Beekeeping Basics
#   27. Natural Remedies from the Garden
#
# ═══════════════════════════════════════════════════════════════════════

TABLE_OF_CONTENTS = {
    "Foraging": [
        "Introduction to Foraging",
        "Easy Plants to Identify",
        "The Carrot Family",
        "Mushroom Foraging",
        "The Law of the Land",
        "The Coastal Code",
        "Winter Foraging",
        "The Cabbage Family",
        "UK Foraging Law: The Complete Guide",
        "Trees & Hedgerows",
        "Foraging Through the Seasons",
        "Medicinal Plants & Herbal Remedies",
        "Seaweed & Shellfish Foraging",
        "Foraging in Scotland: Different Rules",
    ],
    "Off-Grid Living": [
        "Introduction to Off-Grid Living",
        "Water: Collection, Filtration & Storage",
        "Power: Solar, Wind & Alternatives",
        "Preserving & Storing Food",
        "Building & Planning: OPD in Wales",
    ],
    "Homesteading": [
        "Keeping Chickens",
        "Ducks & Geese",
        "Keeping Goats",
        "Starting an Orchard",
        "Composting & Soil Health",
        "Small-Scale Vegetable Growing",
        "Beekeeping Basics",
        "Natural Remedies from the Garden",
    ],
}

# ═══════════════════════════════════════════════════════════════
# MODULE METADATA — Path, level, and icon for each module
# Used by the modules page and lesson API endpoints
# ═══════════════════════════════════════════════════════════════

MODULE_METADATA = {
    # ── Foraging Path ──
    "Introduction to Foraging":               {"path": "Foraging",       "level": "Beginner",     "icon": "🌿"},
    "Easy Plants to Identify":                {"path": "Foraging",       "level": "Beginner",     "icon": "🌼"},
    "The Carrot Family":                      {"path": "Foraging",       "level": "Intermediate", "icon": "🥕"},
    "Mushroom Foraging":                      {"path": "Foraging",       "level": "Specialist",   "icon": "🍄"},
    "The Law of the Land":                    {"path": "Foraging",       "level": "Beginner",     "icon": "⚖️"},
    "The Coastal Code":                       {"path": "Foraging",       "level": "Intermediate", "icon": "🏖️"},
    "Winter Foraging":                        {"path": "Foraging",       "level": "Intermediate", "icon": "❄️"},
    "The Cabbage Family":                     {"path": "Foraging",       "level": "Beginner",     "icon": "🥬"},
    "UK Foraging Law: The Complete Guide":    {"path": "Foraging",       "level": "Intermediate", "icon": "🏛️"},
    "Trees & Hedgerows":                      {"path": "Foraging",       "level": "Intermediate", "icon": "🌳"},
    "Foraging Through the Seasons":           {"path": "Foraging",       "level": "Beginner",     "icon": "🗓️"},
    "Medicinal Plants & Herbal Remedies":     {"path": "Foraging",       "level": "Specialist",   "icon": "💊"},
    "Seaweed & Shellfish Foraging":          {"path": "Foraging",       "level": "Intermediate", "icon": "🦪"},
    "Foraging in Scotland: Different Rules":  {"path": "Foraging",       "level": "Intermediate", "icon": "🏴󠁧󠁢󠁳󠁣󠁴󠁿"},
    # ── Off-Grid Living Path ──
    "Introduction to Off-Grid Living":        {"path": "Off-Grid Living", "level": "Beginner",    "icon": "🏠"},
    "Water: Collection, Filtration & Storage":{"path": "Off-Grid Living", "level": "Intermediate", "icon": "💧"},
    "Power: Solar, Wind & Alternatives":      {"path": "Off-Grid Living", "level": "Intermediate", "icon": "⚡"},
    "Preserving & Storing Food":              {"path": "Off-Grid Living", "level": "Beginner",     "icon": "🫙"},
    "Building & Planning: OPD in Wales":      {"path": "Off-Grid Living", "level": "Specialist",   "icon": "🏗️"},
    # ── Homesteading Path ──
    "Keeping Chickens":                       {"path": "Homesteading",   "level": "Beginner",      "icon": "🐔"},
    "Ducks & Geese":                          {"path": "Homesteading",   "level": "Intermediate",  "icon": "🦆"},
    "Keeping Goats":                          {"path": "Homesteading",   "level": "Intermediate",  "icon": "🐐"},
    "Starting an Orchard":                    {"path": "Homesteading",   "level": "Beginner",      "icon": "🍎"},
    "Composting & Soil Health":                {"path": "Homesteading",   "level": "Beginner",      "icon": "🪱"},
    "Small-Scale Vegetable Growing":          {"path": "Homesteading",   "level": "Intermediate",  "icon": "🌱"},
    "Beekeeping Basics":                      {"path": "Homesteading",   "level": "Specialist",    "icon": "🐝"},
    "Natural Remedies from the Garden":       {"path": "Homesteading",   "level": "Specialist",    "icon": "🌿"},
}

# Path display info — used for section headers and badges
PATH_INFO = {
    "Foraging": {
        "icon": "🌿",
        "description": "Find, identify, and safely gather wild food across the UK",
        "colour": "#4CAF50",
        "slug": "foraging",
    },
    "Off-Grid Living": {
        "icon": "🏠",
        "description": "Water, power, preservation, and sustainable living",
        "colour": "#FFA726",
        "slug": "offgrid",
    },
    "Homesteading": {
        "icon": "🚜",
        "description": "Animals, growing, and making the most of your land",
        "colour": "#42A5F5",
        "slug": "homesteading",
    },
}


LESSON_CONTENT = {

    # ═════════════════════════════════════════════════
    # FORAGING PATH
    # ═════════════════════════════════════════════════

    "Introduction to Foraging": {
        "curriculum": ["Sc2/1a", "PSHE/H18"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## Welcome to Foraging! 🌿

**What is Foraging?**
Foraging is the act of finding and gathering wild food. It is the oldest human skill, but today we do it for fun, health, and connection to nature.

**The Golden Rule:**
> *If in doubt, leave it out.*
Never eat anything unless you are 100% sure what it is.
"""
            },
            {
                "type": "quiz",
                "question": "The 'Golden Rule' of foraging is...",
                "options": ["Eat everything you find", "If in doubt, leave it out", "Cook it first"],
                "answer": "If in doubt, leave it out",
                "feedback": "Correct! Safety is always the priority."
            },
            {
                "type": "text",
                "content": """
### The Safety Toolkit 🎒
Before you go out, you need the right gear.
1. **A Good Guide Book:** Pictures are never as good as a real book.
2. **Scissors/Knife:** To cut stems cleanly.
3. **Basket/Bag:** Never use plastic bags (plants sweat and go slimy).
4. **Gloves:** Essential for Nettles or suspicious plants.
5. **Phone:** For emergencies.
"""
            },
            {
                "type": "plant_card",
                "plant_name": "Nettles"
            },
            {
                "type": "text",
                "content": """
### The Conservation Code 🌍
We never take more than we need.
- **The 10% Rule:** Never pick more than 10% of a patch. Leave 90% for wildlife.
- **The 1 in 3 Rule:** Only pick from areas where there are at least 3 plants. If you only see one, leave it alone.
"""
            },
            {
                "type": "final_quiz",
                "question": "How much of a plant patch should you leave for wildlife?",
                "options": ["10%", "50%", "90%", "All of it"],
                "answer": "90%",
                "reward": 10
            }
        ]
    },

    "Easy Plants to Identify": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "7-9",
        "steps": [
            {
                "type": "text",
                "content": "## The 'Big 3' for Beginners 🌼\nThese are the best plants to start with because they have clear identifying features and no deadly lookalikes."
            },
            {
                "type": "plant_card",
                "plant_name": "Dandelion"
            },
            {
                "type": "quiz",
                "question": "What is the 'Lion's Tooth'?",
                "options": ["The root", "The jagged leaves", "The yellow flower"],
                "answer": "The jagged leaves",
                "feedback": "Correct! The leaves look like lion's teeth."
            },
            {
                "type": "plant_card",
                "plant_name": "Blackberries"
            },
            {
                "type": "text",
                "content": "### ⚠️ Safety Tip\nBlackberries have **thorns**. Always wear long sleeves and gloves when picking them to avoid scratches."
            },
            {
                "type": "plant_card",
                "plant_name": "Wild Garlic"
            },
            {
                "type": "text",
                "content": "### The Smell Test\nWild Garlic is one of the safest plants because of its strong smell. If it doesn't smell like garlic, **do not eat it**."
            },
            {
                "type": "final_quiz",
                "question": "Why is Wild Garlic considered safe for beginners?",
                "options": ["It grows everywhere", "The strong garlic smell identifies it", "It has no thorns"],
                "answer": "The strong garlic smell identifies it",
                "reward": 15
            }
        ]
    },

    "The Carrot Family": {
        "curriculum": ["Sc2/1a", "PSHE/H18", "PSHE/R11"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": "## The Umbellifer Challenge 🥕\nThe Carrot family (Apiaceae) has delicious foods and **deadly poisons**. You must learn to tell them apart."
            },
            {
                "type": "text",
                "content": "### The Good (Edible)\n- **Wild Carrot:** Hairy stem, smells of carrot.\n- **Cow Parsley:** Rough hairy stem, smells parsley."
            },
            {
                "type": "plant_card",
                "plant_name": "Wild Carrot"
            },
            {
                "type": "quiz",
                "question": "Wild Carrot stems are...",
                "options": ["Smooth with purple spots", "Hairy", "Blue"],
                "answer": "Hairy",
                "feedback": "Correct! Hairy stems are a key ID for Wild Carrot (and Cow Parsley)."
            },
            {
                "type": "plant_card",
                "plant_name": "Hemlock"
            },
            {
                "type": "quiz",
                "question": "Hemlock has a distinctive feature on its stem. What is it?",
                "options": ["Hairy texture", "Purple spots", "Blue stripes"],
                "answer": "Purple spots",
                "feedback": "Correct! Purple spots usually mean danger in this family."
            },
            {
                "type": "text",
                "content": "### ID Tips for Beginners\n1. **Smell:** Does it smell like food (carrot/parsley)? If it smells musty/mousy, leave it.\n2. **Stem:** Hairy stems are usually safer. Smooth/Purple spotted = Danger.\n3. **Habitat:** Hemlock loves damp ditches."
            },
            {
                "type": "final_quiz",
                "question": "What does Hemlock smell like?",
                "options": ["Carrot", "Parsley", "Mouse urine", "Garlic"],
                "answer": "Mouse urine",
                "reward": 20
            }
        ]
    },

    "Mushroom Foraging": {
        "curriculum": ["Sc2/1a", "PSHE/H18", "PSHE/R11"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": "## Fungi: The Advanced Class 🍄\n**Warning:** Mushroom foraging requires expert knowledge. One mistake can be fatal."
            },
            {
                "type": "plant_card",
                "plant_name": "Death Cap"
            },
            {
                "type": "quiz",
                "question": "What feature does the Death Cap have at its base?",
                "options": ["A ring", "A volva (cup)", "Blue spots"],
                "answer": "A volva (cup)",
                "feedback": "Correct! The volva is often underground, so you must dig carefully."
            },
            {
                "type": "plant_card",
                "plant_name": "Chanterelle"
            },
            {
                "type": "text",
                "content": "### Golden Rules\n1. **Never eat a mushroom unless 100% sure.**\n2. **Cut, don't pull:** Leave the 'roots' (mycelium) for next year.\n3. **Spore Prints:** Sometimes you need to leave a cap on paper overnight to check spore colour."
            },
            {
                "type": "final_quiz",
                "question": "Should you pull mushrooms out of the ground?",
                "options": ["Yes, get the whole thing", "No, cut the stem", "Only if they are red"],
                "answer": "No, cut the stem",
                "reward": 25
            }
        ]
    },

    "The Law of the Land": {
        "curriculum": ["PSHE/H18", "PSHE/L11", "GEO/6a"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## Foraging and the Law ⚖️
Knowing the law protects you and nature.
"""
            },
            {
                "type": "text",
                "content": "### The Theft Act 1968\n- **Wild Plants:** You can pick flowers, fruit, and foliage for **personal use**.\n- **Uprooting:** It is illegal to dig up any wild plant without the landowner's permission.\n- **Commercial:** You cannot sell what you pick without permission."
            },
            {
                "type": "quiz",
                "question": "Is it legal to dig up a Wild Carrot root from a public field?",
                "options": ["Yes, if I only take one", "Yes, if it is for dinner", "No, uprooting is illegal without permission"],
                "answer": "No, uprooting is illegal without permission",
                "feedback": "Correct! You can pick the leaves/flowers, but digging requires permission."
            },
            {
                "type": "text",
                "content": "### The 'Four Fs'\nYou can legally pick:\n- **F**ruit\n- **F**oliage\n- **F**lowers\n- **F**ungi\n...for personal consumption, provided it is not a protected site or species."
            },
            {
                "type": "final_quiz",
                "question": "What are the 'Four Fs' you can legally pick?",
                "options": ["Food, Fuel, Furniture, Fences", "Fruit, Foliage, Flowers, Fungi", "Fish, Fowl, Foxes, Ferns"],
                "answer": "Fruit, Foliage, Flowers, Fungi",
                "reward": 15
            }
        ]
    },

    "The Coastal Code": {
        "curriculum": ["Sc2/1a", "PSHE/H18", "GEO/6a"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": "## Coastal Foraging 🏖️\nThe coast offers amazing food like Samphire and Cockles, but it has unique dangers."
            },
            {
                "type": "text",
                "content": "### Safety First\n1. **Tides:** Always check the tide times. You can get cut off by rising water.\n2. **Pollution:** Do not pick shellfish near sewage pipes or harbours.\n3. **Red Tides:** Algal blooms can make shellfish toxic. Check local warnings."
            },
            {
                "type": "plant_card",
                "plant_name": "Marsh Samphire"
            },
            {
                "type": "quiz",
                "question": "Why should you avoid picking shellfish near harbours?",
                "options": ["Too many boats", "Pollution risk", "They are protected"],
                "answer": "Pollution risk",
                "feedback": "Correct! Harbours often have heavy boat traffic and pollution."
            },
            {
                "type": "plant_card",
                "plant_name": "Cockles"
            },
            {
                "type": "text",
                "content": "### The 'R' Rule\nOnly harvest shellfish in months with an 'R' (Septemb**r** to Ap**r**il). In summer, they spawn and can be less safe to eat."
            },
            {
                "type": "final_quiz",
                "question": "When is it safer to eat shellfish?",
                "options": ["Summer months", "Months with an 'R'", "Only on Mondays"],
                "answer": "Months with an 'R'",
                "reward": 20
            }
        ]
    },

    "Winter Foraging": {
        "curriculum": ["Sc2/3b", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": "## Winter Survival ❄️\nForaging doesn't stop in winter! This is the time for roots and evergreens."
            },
            {
                "type": "text",
                "content": "### Roots & Bark\nWinter is the best time to dig roots because the plants send energy down to their roots.\n- **Burdock:** Look for the dead flower stalks (burrs) to find the root."
            },
            {
                "type": "plant_card",
                "plant_name": "Burdock (Root)"
            },
            {
                "type": "plant_card",
                "plant_name": "Pine Needles"
            },
            {
                "type": "quiz",
                "question": "Why are roots often better in winter?",
                "options": ["They are sweeter", "Plants store energy in roots", "They are easier to see"],
                "answer": "Plants store energy in roots",
                "feedback": "Correct! The energy moves from leaves to roots in winter."
            },
            {
                "type": "text",
                "content": "### Safety\nBeware of **Yew** trees in winter. They are evergreen but **deadly poisonous**. Remember: Pine needles are ROUND, Yew needles are FLAT."
            },
            {
                "type": "final_quiz",
                "question": "Which needle is POISONOUS?",
                "options": ["Pine (Round)", "Yew (Flat)", "Spruce (Sharp)"],
                "answer": "Yew (Flat)",
                "reward": 25
            }
        ]
    },

    "The Cabbage Family": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "7-9",
        "steps": [
            {
                "type": "text",
                "content": "## The Brassicaceae Family (Cabbage) 🥬\nThis is one of the **safest** families for beginners.\n\n**Why?** Almost all plants in this family are edible. They have a distinctive 'Cross' shape (4 petals)."
            },
            {
                "type": "text",
                "content": "### The 'Cross' Rule ✝️\nLook at the flower. Does it have **4 petals** in the shape of a cross?\n\n- **YES?** It is likely a Cabbage/Mustard relative.\n- **NO?** Be careful.\n\n**Mnemonic:** 'Crucifers have Crosses.'"
            },
            {
                "type": "plant_card",
                "plant_name": "Shepherd's Purse"
            },
            {
                "type": "quiz",
                "question": "If a flower has 4 petals arranged in a cross shape, which family is it likely from?",
                "options": ["Carrot Family", "Cabbage Family", "Rose Family"],
                "answer": "Cabbage Family",
                "feedback": "Correct! The Cabbage family (Brassicaceae) always has 4 petals in a cross."
            },
            {
                "type": "plant_card",
                "plant_name": "Charlock"
            },
            {
                "type": "text",
                "content": "### Safety Check ⚠️\nWhile the Cabbage family is safe, **Hairy Bittercress** (also edible) looks similar.\nAlways check the smell. Most Brassicas have a mustardy/cabbage smell when crushed."
            },
            {
                "type": "final_quiz",
                "question": "What is the key identifier for the Cabbage family?",
                "options": ["5 petals", "4 petals in a cross", "Umbrella flowers"],
                "answer": "4 petals in a cross",
                "reward": 20
            }
        ]
    },

    "UK Foraging Law: The Complete Guide": {
        "curriculum": ["Sc2/1a", "PSHE/H18", "PSHE/L11", "GEO/6a"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🏛️ The Law and You 🏛️

Foraging in the UK is legal — but there are **important rules** you must follow.
These rules exist to protect plants, wildlife, and the land.

**The most important rule:**
> *If in doubt, leave it out.*

You are **allowed** to pick the **Four Fs** for your own use:
- **F**ruit
- **F**oliage (leaves)
- **F**lowers
- **F**ungi

But you are **NOT** allowed to **uproot** (dig up) any wild plant without the landowner's permission.
"""
            },
            {
                "type": "quiz",
                "question": "What are the 'Four Fs' you can legally pick for personal use?",
                "options": ["Food, Fuel, Furniture, Fences", "Fruit, Foliage, Flowers, Fungi", "Fish, Fowl, Foxes, Ferns"],
                "answer": "Fruit, Foliage, Flowers, Fungi",
                "feedback": "Correct! The Four Fs are what you can pick from the wild for personal use."
            },
            {
                "type": "text",
                "content": """
### 🚫 The Theft Act 1968

This is the main law about foraging in England and Wales.

**What it says:**
- You can pick the Four Fs (Fruit, Foliage, Flowers, Fungi) for **personal use**
- You **cannot** uproot any wild plant without permission
- You **cannot** sell what you pick without permission
- You **cannot** pick from someone's garden without asking

**Important:** Even if a plant is growing on public land (like a park or roadside), the plants belong to the landowner or the council. You can pick the Four Fs, but not for selling.

**Scotland is different!** Scotland has much stronger rights to roam (see the section below).
"""
            },
            {
                "type": "quiz",
                "question": "Is it legal to dig up a wild carrot root from a public field?",
                "options": ["Yes, if I only take one", "Yes, if it is for dinner", "No, uprooting is illegal without permission"],
                "answer": "No, uprooting is illegal without permission",
                "feedback": "Correct! You can pick the leaves and flowers, but digging up the root is uprooting — that's illegal without permission."
            },
            {
                "type": "text",
                "content": """
### 🦉 The Wildlife and Countryside Act 1981

This law protects **rare and endangered plants**.

**What it says:**
- Some plants are **Schedule 8** — these are the rarest and most endangered
- It is **illegal to pick, uproot, or destroy** any Schedule 8 plant
- Examples include: **Wild Gladiolus, Creeping Ladies-tresses, Killarney Fern**

**What this means for you:**
- If you find a very rare plant, **leave it alone** and report it to a local wildlife trust
- Never pick a plant if you're not 100% sure what it is
- Rare plants need our protection, not our picking!

**How to check:** The Wildlife Trusts website has a full list of protected plants.
"""
            },
            {
                "type": "plant_card",
                "plant_name": "Yew"
            },
            {
                "type": "text",
                "content": """
### 🏞️ SSSIs: Sites of Special Scientific Interest

An **SSSI** (Site of Special Scientific Interest) is a protected area of land.

**The rule:** On SSSIs, you often **cannot pick ANYTHING** — even the Four Fs.

**Why?** These sites have rare habitats and species that need complete protection.

**How to know if you're on an SSSI:**
- Look for signs at nature reserves
- Check the Natural England website (they have a map of all SSSIs)
- National Nature Reserves and many country parks are SSSIs

**What to do:** Stick to public footpaths and commons. Don't pick from nature reserves.
"""
            },
            {
                "type": "text",
                "content": """
### 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland: Different Rules!

Scotland has its own laws that are **more friendly** to foragers.

**The Land Reform (Scotland) Act 2003** gives everyone:
- **Right to roam** — you can walk on most land and water
- **Right to forage** — you can pick wild plants for personal use

**But there are still rules:**
- You must not cause damage
- You must not pick protected species
- You must not pick for commercial use without permission
- Be considerate of other people and wildlife

**The Scottish Outdoor Access Code** says:
- Take responsibility for your own actions
- Respect the interests of other people
- Care for the environment

So if you're foraging in Scotland, you have more freedom — but still be respectful!
"""
            },
            {
                "type": "quiz",
                "question": "Which country has stronger rights to roam and forage?",
                "options": ["England", "Wales", "Scotland"],
                "answer": "Scotland",
                "feedback": "Correct! Scotland's Land Reform Act gives everyone the right to roam and forage responsibly."
            },
            {
                "type": "text",
                "content": """
### 📋 The Countryside Code

Whether you're in England, Wales, Scotland, or Northern Ireland, always follow the **Countryside Code**:

1. **Respect** — Keep to paths, leave gates as you find them, don't drop litter
2. **Protect** — Don't start fires, don't damage plants, keep dogs under control
3. **Enjoy** — Know your route, be prepared, check the weather

**For foragers specifically:**
- Only pick what you need (the 10% rule — never take more than 10% of a patch)
- Leave enough for wildlife (the 1-in-3 rule — only pick from groups of 3+)
- Don't pick from roadside verges (pollution from cars)
- Don't pick from parks where dogs foul (health risk)
- Always get the landowner's permission if you're on private land
- Never pick near fields that have been sprayed with chemicals
"""
            },
            {
                "type": "text",
                "content": """
### 🏠 One Planet Development (Wales)

**OPD** is a special Welsh planning policy that allows people to live on and work the land in a sustainable way.

**What it means:**
- You can build a home on agricultural land IF you meet strict sustainability criteria
- You must produce a significant portion of your own food and energy
- You must demonstrate that you're living lightly on the land

**How foraging connects to OPD:**
- If you're applying for OPD, you need to show you can provide food from the land
- Foraging skills are a key part of low-impact living
- Knowing which wild plants are edible can supplement your diet and reduce your ecological footprint

**The 3 Food Groups:**
- 🌿 **Foragers** — Find wild food in hedgerows, woodlands, and coastlines
- 🏘️ **Off-Grid Dwellers** — Preserve, store, and cook wild and homegrown food
- 🚜 **Farmers** — Grow food on the land sustainably

All three groups need each other. Foragers find the food, off-grid dwellers preserve it, and farmers grow it. Together, they create a complete food system.

**Want to learn more?** Search "One Planet Development Wales" or "OPD planning policy" to find the latest guidance.
"""
            },
            {
                "type": "text",
                "content": """
### 🚨 Summary: The Golden Rules

1. **Only pick the Four Fs** — Fruit, Foliage, Flowers, Fungi
2. **Never uproot** without permission — it's illegal
3. **Never pick rare plants** — check the Schedule 8 list
4. **Never pick from SSSIs** — nature reserves are protected
5. **Only take what you need** — leave 90% for wildlife
6. **Be safe** — if you're not 100% sure, leave it out
7. **Respect the land** — follow the Countryside Code
8. **Check your country** — Scotland has different rules to England and Wales
"""
            },
            {
                "type": "final_quiz",
                "question": "What is the most important rule of foraging?",
                "options": ["Pick everything you find", "If in doubt, leave it out", "Only pick pretty flowers"],
                "answer": "If in doubt, leave it out",
                "reward": 25
            }
        ]
    },

    "Trees & Hedgerows": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## Trees & Hedgerows 🌳

Hedgerows are one of the UK's richest foraging habitats. A single hedgerow can contain dozens of edible species.

**Why Hedgerows?**
- They connect habitats across the countryside
- They provide food, shelter, and nesting sites
- They have been part of the British landscape for over 1,000 years

**The Rule of Hedgerows:**
> *Never strip a hedgerow bare. Take only what you need, and leave plenty for wildlife.*

Many of our most familiar foods come from hedgerow trees and shrubs: blackberries, elderberries, sloes, hazelnuts, and hawthorn berries.
"""
            },
            {
                "type": "plant_card",
                "plant_name": "Elder"
            },
            {
                "type": "text",
                "content": """
### Edible Trees to Know

**Oak** — Acorns can be eaten but must be processed (leached) to remove bitter tannins. Not beginner-friendly!

**Hazel** — Hazelnuts ripen in September. Pick early or the squirrels will get them first.

**Beech** — Young beech leaves are edible in spring (beech leaf noyau is a traditional drink). Beech nuts are edible but small and fiddly.

**Lime (Linden)** — Young lime leaves are tender and slightly sweet — one of the best tree salad leaves.

### Hedgerow Shrubs
- **Hawthorn** — Berries (haws) are edible, can be made into jelly
- **Blackthorn** — Sloe berries are extremely tart — perfect for sloe gin
- **Dog Rose** — Rosehips are packed with vitamin C
- **Elder** — Flowers for elderflower cordial, berries for elderberry wine
"""
            },
            {
                "type": "quiz",
                "question": "Why should you never strip a hedgerow bare?",
                "options": ["It is illegal", "Wildlife needs it too", "The fruit won't taste good", "The tree will die"],
                "answer": "Wildlife needs it too",
                "feedback": "Correct! Hedgerows are vital habitats. Always leave plenty for the birds, insects, and mammals that depend on them."
            },
            {
                "type": "text",
                "content": """
### Hedgerow Safety ⚠️

1. **Check for spraying** — Farmers sometimes spray hedgerows with chemicals. Avoid hedgerows next to sprayed fields.
2. **Roadsides** — Avoid foraging on busy roads where pollution from cars coats the plants.
3. **Identification** — Many hedgerow plants have dangerous lookalikes. Always check carefully.
4. **The 1-in-3 Rule** — Only pick from areas where there are at least 3 plants. Leave the rest.
"""
            },
            {
                "type": "final_quiz",
                "question": "Which tree produces edible young leaves in spring that are slightly sweet?",
                "options": ["Oak", "Lime (Linden)", "Blackthorn", "Hawthorn"],
                "answer": "Lime (Linden)",
                "reward": 20
            }
        ]
    },

    "Foraging Through the Seasons": {
        "curriculum": ["Sc2/3b", "Sc2/1a", "PSHE/H18"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🗓️ Foraging Through the Seasons

Nature doesn't produce food all year round. Knowing **what's available when** is one of the most important foraging skills.

**The Seasonal Rule:**
> *If you can't identify it in every season, you shouldn't eat it in any season.*

Many plants look completely different in winter than they do in summer. Learn to recognise them in all their stages.
"""
            },
            {
                "type": "text",
                "content": """
### 🌸 Spring (March – May)

Spring is the time for **leaves and flowers**.

**What to forage:**
- 🌿 Wild Garlic — leaves and flowers (April–May)
- 🌿 Nettles — young tops (March–May)
- 🌼 Dandelion — leaves and flowers
- 🌿 Cleavers (Goosegrass) — sticky stems
- 🌳 Lime (Linden) leaves — young and tender
- 🌼 Elderflower — from late May

**Spring safety:** Many poisonous plants also emerge in spring when everything is small and hard to identify. Take your time.
"""
            },
            {
                "type": "text",
                "content": """
### ☀️ Summer (June – August)

Summer is the time for **flowers and early fruit**.

**What to forage:**
- 🌼 Elderflower — June (if not picked in spring)
- 🫐 Blackberries — start from late July
- 🫐 Wild strawberries — June–July
- 🌿 Meadowsweet — flowers for tea
- 🫐 Raspberries — wild ones in July
- 🌿 Chamomile — flowers for tea

**Summer safety:** Only pick shellfish in months with an 'R' (see the Coastal Code module). Hot weather can make some plants go bitter.
"""
            },
            {
                "type": "text",
                "content": """
### 🍂 Autumn (September – November)

Autumn is the **forager's harvest** — the most abundant season.

**What to forage:**
- 🌰 Hazelnuts — September
- 🍎 Crab apples — September–October
- 🫐 Sloes (Blackthorn) — after first frost
- 🍎 Rosehips — October–November
- 🍄 Chanterelles — if you're experienced
- 🌰 Sweet chestnuts — October–November
- 🍎 Elderberries — September (cook before eating!)

**Autumn safety:** Sloes must be picked after the first frost (or frozen at home) to reduce bitterness. Never eat elderberries raw — always cook them.
"""
            },
            {
                "type": "text",
                "content": """
### ❄️ Winter (December – February)

Winter foraging is limited but **roots and evergreens** are still available.

**What to forage:**
- 🥕 Burdock root — dig in winter when energy is stored below ground
- 🌿 Pine needles — for tea, rich in vitamin C
- 🦪 Cockles — in months with an 'R'
- 🌿 Rosemary — evergreen herb
- 🌿 Wild garlic — can appear in late February in mild areas

**Winter safety:** Never eat Yew berries or leaves — they are deadly year-round. Pine is safe; Yew is not. **Pine needles are ROUND. Yew needles are FLAT.**
"""
            },
            {
                "type": "quiz",
                "question": "Which season is the most abundant for foraging?",
                "options": ["Spring", "Summer", "Autumn", "Winter"],
                "answer": "Autumn",
                "feedback": "Correct! Autumn is the harvest season with nuts, berries, and mushrooms in abundance."
            },
            {
                "type": "final_quiz",
                "question": "Why should you learn to identify plants in EVERY season, not just when they're fruiting?",
                "options": ["It's more fun", "You might need them in winter", "Plants look different each season — you could misidentify", "The law requires it"],
                "answer": "Plants look different each season — you could misidentify",
                "reward": 20
            }
        ]
    },

    "Medicinal Plants & Herbal Remedies": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18", "PSHE/R11"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🌿 Medicinal Plants & Herbal Remedies

⚠️ **IMPORTANT WARNING:** This module is about **traditional knowledge and safe identification**. It does NOT replace medical advice. Never use wild plants as medicine without expert guidance.

**The Golden Rule of Herbal Medicine:**
> *Just because it's natural doesn't mean it's safe. Many natural remedies can interact with medicines or cause allergic reactions.*

**What you will learn:**
- Which plants have been traditionally used for remedies
- How they were prepared safely
- What to AVOID and why
"""
            },
            {
                "type": "plant_card",
                "plant_name": "Nettles"
            },
            {
                "type": "text",
                "content": """
### Traditional Remedies (Safe When Prepared Correctly)

**Nettles** — One of the most useful plants in Britain:
- **Nettle tea:** Dried nettle leaves steeped in hot water. Rich in iron and vitamins.
- **Nettle soup:** Cooked nettles lose their sting. A traditional spring tonic.
- **Nettle dye:** Was used to make green cloth.

**Dandelion** — Another multi-use plant:
- **Dandelion root tea:** Traditionally used for digestion
- **Dandelion leaf:** A diuretic (makes you wee) — hence the old name 'wet-the-bed'
- **Dandelion coffee:** Roasted roots ground up as a coffee substitute

**Plantain (the weed, not the banana!)** — Found in lawns everywhere:
- **Crushed leaves:** Applied to insect stings and small cuts as a traditional poultice
- **Plantain tea:** Traditionally used for coughs
"""
            },
            {
                "type": "text",
                "content": """
### 🚫 What NEVER to Use as Medicine

Some plants are **dangerous** even in small amounts:

- **Foxglove (Digitalis)** — Contains a powerful heart drug. A small error in dose can be FATAL. Used in medicine but ONLY under strict pharmaceutical control.
- **Deadly Nightshade (Belladonna)** — Extremely poisonous. Causes hallucinations, paralysis, and death.
- **Hemlock** — The poison that killed Socrates. There is NO safe dose.
- **Yew** — All parts except the berry flesh are deadly poisonous.

> *These plants are studied by scientists who know how to extract the active compounds safely. You should NEVER attempt this yourself.*
"""
            },
            {
                "type": "quiz",
                "question": "Why should you never try to make medicine from Foxglove?",
                "options": [
                    "It tastes bad",
                    "A small error in dose can be fatal",
                    "It's illegal",
                    "It doesn't have any medicinal properties"
                ],
                "answer": "A small error in dose can be fatal",
                "feedback": "Correct! Foxglove contains digitalis, a powerful heart drug. The difference between a medicine and a poison is the dose."
            },
            {
                "type": "text",
                "content": """
### Safe Preparation Methods

If you want to try **safe, traditional remedies**, here are the basic preparation methods:

1. **Infusion (Tea):** Pour boiling water over dried or fresh leaves. Steep for 5–10 minutes. Strain and drink.
2. **Decoction:** Simmer tougher plant parts (roots, bark) in water for 15–20 minutes.
3. **Poultice:** Crush fresh leaves and apply directly to the skin for stings or small cuts.
4. **Tincture:** Soak herbs in alcohol for several weeks. **This is advanced — do not attempt without expert guidance.**

**Always:**
- Identify the plant with 100% certainty
- Use clean water and clean equipment
- Start with a small amount to check for allergies
- Tell an adult what you're doing
"""
            },
            {
                "type": "final_quiz",
                "question": "What is the MOST IMPORTANT rule about using wild plants as remedies?",
                "options": [
                    "Use as much as possible for maximum effect",
                    "It's natural so it must be safe",
                    "Never use wild plants as medicine without expert guidance",
                    "Only use plants that taste good"
                ],
                "answer": "Never use wild plants as medicine without expert guidance",
                "reward": 25
            }
        ]
    },

    "Seaweed & Shellfish Foraging": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18", "GEO/6a"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🏖️ Seaweed & Shellfish Foraging

The UK coastline is one of the richest foraging environments in the world — but it comes with **unique dangers**.

**Before you even think about coastal foraging:**
1. **Check the tides** — Getting cut off by the tide is life-threatening
2. **Check for pollution** — Never forage near sewage outlets, harbours, or industrial areas
3. **Check for red tides** — Algal blooms can make shellfish toxic
4. **Tell someone where you're going**
"""
            },
            {
                "type": "plant_card",
                "plant_name": "Marsh Samphire"
            },
            {
                "type": "text",
                "content": """
### Edible Seaweeds

**Dulse** — Dark red-purple, found on rocks at low tide. Can be eaten raw or dried. Rich in minerals.

**Sea Lettuce** — Bright green, thin, translucent sheets. Found on rocks and in rock pools. Eat raw or lightly cooked.

**Kelp (various species)** — Large brown seaweeds. The stipe (stalk) can be cut into strips and cooked. Rich in iodine.

**Carrageen (Irish Moss)** — Reddish-purple, found in rock pools. Traditionally used to set desserts (like vegetarian gelatine).

**Safety Rules for Seaweed:**
- Only pick from clean water
- Wash thoroughly before eating
- Don't pick seaweed that is rotting or washed up on the beach
- Pick only a small amount from each patch
- Cut with scissors — don't pull the whole plant from the rock
"""
            },
            {
                "type": "plant_card",
                "plant_name": "Cockles"
            },
            {
                "type": "text",
                "content": """
### The 'R' Rule for Shellfish 🦪

Only harvest shellfish in months with the letter **R** in their name:

✅ **Safe months:** Septembe**r**, Octobe**r**, Novembe**r**, Decembe**r**, Janua**r**y, Feb**r**ua**r**y, Ma**r**ch, Ap**r**il

❌ **Avoid months:** May, June, July, August

**Why?** In summer, shellfish are spawning (reproducing). This can make them:
- Less nutritious
- More likely to contain toxins from algal blooms
- Potentially harmful to eat

**Additional Shellfish Safety:**
- Only collect from clean beaches — check the Environment Agency website for water quality
- If a shellfish doesn't close when tapped, it's dead — throw it away
- Cook shellfish thoroughly — never eat them raw unless you are absolutely certain the water is clean
- Soak cockles and clams in clean salt water for several hours to purge them of sand
"""
            },
            {
                "type": "quiz",
                "question": "Which months should you AVOID eating shellfish?",
                "options": [
                    "September, October, November",
                    "December, January, February",
                    "May, June, July, August",
                    "March, April, May"
                ],
                "answer": "May, June, July, August",
                "feedback": "Correct! Months without an 'R' (May–August) are when shellfish are spawning and more likely to contain toxins."
            },
            {
                "type": "final_quiz",
                "question": "What is the MOST important safety check before coastal foraging?",
                "options": [
                    "Wearing sunscreen",
                    "Checking the tides and water quality",
                    "Bringing a bucket",
                    "Going with a friend"
                ],
                "answer": "Checking the tides and water quality",
                "reward": 25
            }
        ]
    },

    "Foraging in Scotland: Different Rules": {
        "curriculum": ["Sc2/1a", "PSHE/L11", "GEO/6a"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Foraging in Scotland

Scotland has **very different rules** to England and Wales when it comes to accessing land and foraging. Understanding these differences is important if you plan to forage north of the border.

**The Key Difference:**
- **England & Wales:** You can only access certain types of land (public footpaths, commons, some beaches)
- **Scotland:** You can access almost ALL land and water — it's your **right**
"""
            },
            {
                "type": "text",
                "content": """
### The Scottish Outdoor Access Code

In 2003, Scotland passed a law giving everyone the **Right to Roam**. This means you can:

✅ Walk on most land and water
✅ Forage for personal use
✅ Camp wild (with restrictions)
✅ Swim in lochs and rivers

**But you must be RESPONSIBLE:**
- Don't damage crops or property
- Don't disturb livestock or wildlife
- Don't leave litter
- Don't make excessive noise
- Keep dogs under control (especially near livestock and ground-nesting birds)

**The three principles:**
1. **Respect** the interests of other people
2. **Care** for the environment
3. **Take responsibility** for your own actions
"""
            },
            {
                "type": "text",
                "content": """
### What Can You Forage in Scotland?

Under the Scottish Outdoor Access Code, you can forage **wild plants for personal consumption** including:

🌿 **Berries** — Blaeberry (wild bilberry), raspberry, cloudberry, crowberry
🍄 **Fungi** — Chanterelle, cep, hedgehog mushroom (with expert ID only)
🌲 **Tree products** — Pine needles, birch sap
🫐 **Seaweed** — From clean beaches

**Special Scottish Plants:**
- **Blaeberry** (wild bilberry) — Abundant on Scottish hillsides, much more common than in England
- **Cloudberry** — A rare Arctic berry found on Scottish mountains
- **Crowberry** — Black berries on heather moorland

### What You Still CAN'T Do

Even in Scotland, you **cannot:**
- Pick protected species (Schedule 8 plants)
- Pick on SSSIs without permission
- Forage commercially without permission
- Damage plants or habitats
"""
            },
            {
                "type": "quiz",
                "question": "What is the key difference between foraging law in Scotland vs England and Wales?",
                "options": [
                    "Foraging is illegal in Scotland",
                    "Scotland gives everyone the right to roam and forage responsibly",
                    "Scotland has no rules at all",
                    "You need a licence in Scotland"
                ],
                "answer": "Scotland gives everyone the right to roam and forage responsibly",
                "feedback": "Correct! The Scottish Outdoor Access Code gives everyone the right to access land and forage for personal use."
            },
            {
                "type": "final_quiz",
                "question": "What is a 'blaeberry'?",
                "options": [
                    "A type of Scottish seaweed",
                    "A wild bilberry found on Scottish hillsides",
                    "A poisonous berry",
                    "A type of mushroom"
                ],
                "answer": "A wild bilberry found on Scottish hillsides",
                "reward": 15
            }
        ]
    },

    # ═════════════════════════════════════════════════
    # OFF-GRID LIVING PATH
    # ═════════════════════════════════════════════════

    "Introduction to Off-Grid Living": {
        "curriculum": ["Sc2/3a", "Sc4/1a", "PSHE/H18", "GEO/6a"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🏠 What Does 'Off-Grid' Mean?

Living 'off-grid' means you are not connected to the **mains services** that most people rely on:
- **Mains water** — you collect and purify your own
- **Mains electricity** — you generate your own power
- **Mains gas** — you heat your home differently
- **Sewerage** — you manage your own waste

**Why go off-grid?**
- To live more sustainably and reduce your environmental impact
- To be self-sufficient and resilient
- To live closer to nature and the seasons
- As part of a One Planet Development (OPD) in Wales
"""
            },
            {
                "type": "text",
                "content": """
### The Three Essentials

If you're going to live off-grid, you need to solve three problems every day:

**1. 💧 Water**
You need water for drinking, cooking, washing, and growing food. Options:
- **Rainwater collection** — Most reliable in the UK (it rains a lot!)
- **Spring or borehole** — If you're lucky enough to have one
- **Stream or river** — Must be filtered and purified

**2. ⚡ Energy**
You need power for lights, devices, and maybe heating:
- **Solar panels** — The most popular option in the UK
- **Wind turbine** — Works well in exposed locations
- **Wood burner** — For heating and cooking
- **Hydro power** — If you have a stream with a drop

**3. 🌱 Food**
You need to eat! Off-grid food comes from:
- **Growing your own** — Vegetables, fruit, herbs
- **Foraging** — Wild food from the land around you
- **Keeping animals** — Chickens for eggs, goats for milk
- **Preserving** — Storing food for winter
"""
            },
            {
                "type": "text",
                "content": """
### The Off-Grid Mindset 🧠

Living off-grid isn't just about technology — it's about **how you think**:

- **Conserve first:** Use less before generating more. A well-insulated house needs less energy to heat.
- **Plan ahead:** When your power comes from the sun, you learn to do laundry on sunny days.
- **Respect nature:** You're not fighting the weather — you're working with it.
- **Learn constantly:** Every problem is a chance to learn something new.
- **Share knowledge:** Off-grid communities thrive on sharing skills and experience.

**The Off-Grid Rule:**
> *Reduce first, then produce.* The cheapest and greenest energy is the energy you don't use.
"""
            },
            {
                "type": "quiz",
                "question": "What are the three essentials you need to solve for off-grid living?",
                "options": [
                    "TV, Wi-Fi, and a fridge",
                    "Water, energy, and food",
                    "Money, a car, and a phone",
                    "Bricks, cement, and paint"
                ],
                "answer": "Water, energy, and food",
                "feedback": "Correct! Water, energy, and food are the three essentials you need to provide for yourself off-grid."
            },
            {
                "type": "final_quiz",
                "question": "What does 'Reduce first, then produce' mean in off-grid living?",
                "options": [
                    "Use less energy before you try to generate more",
                    "Build a small house then extend it",
                    "Buy less food then grow more",
                    "Reduce your family size"
                ],
                "answer": "Use less energy before you try to generate more",
                "reward": 10
            }
        ]
    },

    "Water: Collection, Filtration & Storage": {
        "curriculum": ["Sc2/3a", "Sc4/1a", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 💧 Water: The Most Important Resource

You can survive **3 weeks without food** but only **3 days without water**. On a homestead, water is your #1 priority.

**How much water do you need?**
- Drinking: 2–3 litres per person per day
- Cooking: 1–2 litres per person per day
- Washing: 10–20 litres per person per day
- Growing food: 20–50 litres per day in dry weather

That's **30–75 litres per person per day** — or up to 300 litres for a family of four.
"""
            },
            {
                "type": "text",
                "content": """
### Collecting Water

**Rainwater Harvesting** 🌧️
The UK gets plenty of rain (800–1,400mm per year depending on where you live). A roof of 100m² can collect about **80,000 litres a year** in Wales.

**How it works:**
1. Rain falls on your roof
2. It runs into gutters
3. Gutters feed into a filter (to remove leaves and debris)
4. Filtered water goes into a storage tank
5. Tank water is pumped or gravity-fed to where you need it

**Other sources:**
- **Springs** — If you have a natural spring, you have the best water source
- **Boreholes** — Deep wells drilled into the ground (expensive but reliable)
- **Streams** — Need filtration and purification before drinking
- **Wells** — Traditional hand-dug wells still work in many places
"""
            },
            {
                "type": "text",
                "content": """
### Filtration & Purification

**Rainwater is NOT safe to drink straight from the tank.** It can contain bird droppings, dust, bacteria, and other contaminants.

**The 3-Stage Purification Process:**

1. **Filtration** — Remove particles and some bacteria
   - Sand filters (cheap, simple, effective)
   - Ceramic filters (very fine, remove bacteria)
   - Carbon filters (remove tastes and chemicals)

2. **Purification** — Kill remaining bacteria and viruses
   - Boiling (rolling boil for 1 minute — the most reliable method)
   - UV light purifiers (use sunlight or a UV lamp)
   - Chemical treatment (chlorine tablets — for emergencies only)

3. **Storage** — Keep water clean after purifying
   - Store in dark, cool containers (light grows algae)
   - Use food-grade containers (not anything that held chemicals)
   - Rotate stored water every 6 months
"""
            },
            {
                "type": "quiz",
                "question": "Why can't you drink rainwater straight from the collection tank?",
                "options": [
                    "It tastes bad",
                    "It can contain bird droppings, dust, and bacteria",
                    "It's illegal",
                    "It's too cold"
                ],
                "answer": "It can contain bird droppings, dust, and bacteria",
                "feedback": "Correct! Rainwater picks up contamination from your roof and gutters. Always filter and purify before drinking."
            },
            {
                "type": "text",
                "content": """
### Water Conservation 🚿

On a homestead, every litre counts. Here are ways to use less:

- **Low-flow showerheads** — Cut shower water use in half
- **Dual-flush toilets** — Or use a compost toilet (uses no water at all!)
- **Grey water recycling** — Water from washing can water your garden
- **Rainwater for the garden** — Don't use purified drinking water on plants
- **Fix leaks immediately** — A dripping tap wastes 15 litres a day
- **Mulch your garden** — Retains moisture, means less watering

**The Water Hierarchy (use the lowest quality water for each job):**
1. **Drinking & cooking** — Purified water (highest quality)
2. **Washing** — Filtered water
3. **Garden** — Rainwater or grey water (lowest quality needed)
"""
            },
            {
                "type": "final_quiz",
                "question": "What is the most reliable way to purify water for drinking?",
                "options": [
                    "Leaving it in the sun",
                    "Adding chlorine tablets",
                    "Bringing it to a rolling boil for 1 minute",
                    "Running it through sand"
                ],
                "answer": "Bringing it to a rolling boil for 1 minute",
                "reward": 20
            }
        ]
    },

    "Power: Solar, Wind & Alternatives": {
        "curriculum": ["Sc4/1a", "Sc4/1b", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## ⚡ Generating Your Own Power

When you live off-grid, you become your own **power station**. No more electricity bills — but also no more power cuts being someone else's problem!

**How much power do you need?**
- A basic off-grid home uses **3–5 kWh per day**
- The average UK home uses **8–10 kWh per day**
- An off-grid home uses less because it's designed to conserve energy

**The Off-Grid Power Rule:**
> *Every watt you don't use is a watt you don't have to generate.*
"""
            },
            {
                "type": "text",
                "content": """
### ☀️ Solar Power

Solar panels (photovoltaic or PV panels) convert sunlight into electricity. They are the most popular off-grid power source in the UK.

**How they work:**
1. Sunlight hits the solar panel
2. The panel converts light into DC electricity
3. A charge controller regulates the power
4. Batteries store the electricity for when the sun isn't shining
5. An inverter converts DC to AC (for normal appliances)

**UK Solar Reality:**
- A 1kW solar panel system in Wales generates about **800–900 kWh per year**
- Summer: Lots of power (long days)
- Winter: Very little power (short, cloudy days)
- **You need batteries** to store summer power for winter use

**Tip:** Angle your panels to maximise winter sun (steeper angle, about 35–40° in the UK), because that's when you need it most.
"""
            },
            {
                "type": "text",
                "content": """
### 💨 Wind Power

Wind turbines generate electricity from wind. They work **day and night** but need consistent wind.

**Pros:**
- Works when there's no sun
- Can generate power 24 hours a day
- Complements solar (windiest in winter when solar is weakest)

**Cons:**
- Needs average wind speeds of 5+ metres per second
- Moving parts need maintenance
- Can be noisy
- Planning permission may be required for larger turbines

### 🔥 Wood & Other Heat Sources

For **heating**, electricity is expensive. Off-grid homes often use:
- **Wood burners** — The heart of an off-grid home. Burns logs from your own land.
- **Biomass boilers** — Burns wood pellets or chips automatically
- **Ground source heat pumps** — Use the warmth in the ground (needs electricity to run)
- **Rayburns / Agas** — Cook and heat your home AND provide hot water from one fire

### 🔋 Batteries: Storing Your Power

**Without batteries, solar and wind are only useful when they're generating.**

Battery types:
- **Lead-acid** — Cheap but heavy, shorter lifespan
- **Lithium-ion** — Expensive but light, long lifespan, more efficient
- **Saltwater** — New technology, environmentally friendly

**The Battery Rule:** Size your battery bank for **3 days of cloudy weather**.
"""
            },
            {
                "type": "quiz",
                "question": "Why do off-grid homes need batteries?",
                "options": [
                    "To make the electricity cheaper",
                    "Because solar panels don't work at night and wind isn't constant",
                    "Because it's the law",
                    "Batteries are optional for off-grid living"
                ],
                "answer": "Because solar panels don't work at night and wind isn't constant",
                "feedback": "Correct! Batteries store excess power for when generation is low (night, cloudy days, still wind)."
            },
            {
                "type": "final_quiz",
                "question": "What is the most important rule of off-grid power?",
                "options": [
                    "Always have a backup generator",
                    "Buy the biggest solar panels you can afford",
                    "Every watt you don't use is a watt you don't have to generate",
                    "Wind power is better than solar power"
                ],
                "answer": "Every watt you don't use is a watt you don't have to generate",
                "reward": 20
            }
        ]
    },

    "Preserving & Storing Food": {
        "curriculum": ["Sc2/3a", "PSHE/H18", "Sc2/1a"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🫙 Preserving & Storing Food

If you grow or forage food, you'll have **gluts** — times when you have way more than you can eat. Without a supermarket to rely on, preserving is essential.

**Why preserve?**
- Reduce waste (don't let food rot)
- Store food for winter when little grows
- Save money (your preserved food is free)
- Keep the goodness all year round

**The 6 main methods:**
1. Drying
2. Freezing
3. Fermenting
4. Pickling
5. Jamming & Jellying
6. Root cellaring
"""
            },
            {
                "type": "text",
                "content": """
### Drying ☀️

The oldest preservation method. Remove the water and bacteria can't grow.

**What you can dry:**
- Herbs — Hang in small bunchs in a warm, dry place
- Apples — Slice thin, dry in a low oven or dehydrator
- Mushrooms — Slice and dry on a rack
- Tomatoes — Sun-dry or use a dehydrator
- Seaweed — Dry on a rack in the sun

**The Rule:** Food must be **completely dry** or it will go mouldy. If in doubt, dry it more.

### Freezing ❄️

The easiest method if you have freezer capacity. But on an off-grid home, freezer space is limited and uses a lot of power!

**What freezes well:**
- Berries (freeze on a tray first, then bag)
- Beans, peas, sweetcorn (blanch first: boil 2 mins, plunge into ice water)
- Herbs (chop and freeze in ice cube trays with water)
- Soups and stews

**What doesn't freeze well:**
- Lettuce, cucumber, radishes (go mushy)
- Raw potatoes (go grainy)
- Cream (separates)
"""
            },
            {
                "type": "text",
                "content": """
### Fermenting 🦠

Not the same as going off! Fermentation uses **good bacteria** to preserve food and create new flavours.

**Kimchi** — Korean fermented vegetables (spicy!)
**Sauerkraut** — German fermented cabbage
**Kombucha** — Fermented sweet tea
**Kefir** — Fermented milk drink

**Basic Sauerkraut Method:**
1. Shred cabbage finely
2. Add salt (2% by weight)
3. Squeeze and massage until liquid comes out
4. Pack tightly into a sterilised jar
5. Make sure cabbage is completely under the liquid
6. Leave at room temperature for 1–4 weeks
7. Taste it — when you like the flavour, move to the fridge

**The Rule:** Everything must stay **under the brine**. If cabbage pokes above the liquid, it can go mouldy.

### Pickling 🥒

Preserving in vinegar. Simpler than fermenting.

**Quick Pickle:** Pour hot vinegar solution over vegetables in a jar. Seal. Ready in 24 hours, keeps for weeks.

**Pickled eggs:** Hard-boiled eggs in spiced vinegar. A classic!

### Jams & Jellies 🍓

Cooking fruit with sugar and pectin creates a preserve that lasts months or years.

**The Rule:** Jam needs **60% sugar** to preserve properly. Low-sugar jams need refrigeration and won't last as long.
"""
            },
            {
                "type": "text",
                "content": """
### Root Cellaring 🥕

The original refrigeration! A root cellar uses the natural cool temperature of the ground to store vegetables through winter.

**What stores well in a root cellar:**
- Potatoes (in the dark or they'll go green)
- Carrots (in sand or sawdust)
- Beetroot (in sand)
- Onions (hanging in nets)
- Apples (wrap individually in newspaper)
- Cabbages (hang roots up)

**Root cellar conditions:**
- Temperature: 2–4°C (just above freezing)
- Humidity: 85–95% (to stop things shrivelling)
- Dark (light makes potatoes produce poison)
- Ventilated (to prevent mould)

**No root cellar?** A cool garage, shed, or even a hole in the ground lined with straw can work!
"""
            },
            {
                "type": "quiz",
                "question": "When making sauerkraut, what is the most important rule?",
                "options": [
                    "Use boiling water",
                    "Keep all cabbage under the brine",
                    "Add lots of sugar",
                    "Cook it for an hour"
                ],
                "answer": "Keep all cabbage under the brine",
                "feedback": "Correct! If cabbage pokes above the liquid, mould can grow. Keep everything submerged."
            },
            {
                "type": "final_quiz",
                "question": "Why is food preservation essential for off-grid living?",
                "options": [
                    "It makes food taste better",
                    "You have gluts of food that would otherwise rot, and need to store for winter",
                    "It's a legal requirement",
                    "Preserved food is more nutritious"
                ],
                "answer": "You have gluts of food that would otherwise rot, and need to store for winter",
                "reward": 20
            }
        ]
    },

    "Building & Planning: OPD in Wales": {
        "curriculum": ["PSHE/L11", "GEO/6a", "Sc2/3a"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🏗️ One Planet Development (OPD) in Wales

One Planet Development is a **special planning policy in Wales** that allows people to build a home on agricultural land — IF they meet strict environmental criteria.

**Why does this matter for foraging and homesteading?**
Because OPD is one of the few legal routes to live on and work the land in the UK. If you want to build a smallholding from scratch, this might be your path.

> *OPD is about proving you can live lightly on the land — providing your own food, energy, and income while keeping your ecological footprint small.*
"""
            },
            {
                "type": "text",
                "content": """
### The OPD Criteria

To get OPD planning permission, you must prove:

**1. 🏠 You provide at least 65% of your basic household needs from the land**
This includes food, energy, and water. The remaining 35% can come from outside, but you must show a realistic plan.

**2. 📊 Your ecological footprint is low**
Measured using a calculator that looks at travel, energy, food, waste, and more. Your target footprint must be significantly lower than the Welsh average.

**3. 💰 You have a viable land-based business**
You must earn at least the Minimum Agricultural Income (around £30,000/year from the land). This can come from:
- Selling produce (vegetables, eggs, meat)
- Value-added products (jam, preserves, crafts)
- Educational services (courses, tours, experiences)

**4. 📋 You have a management plan**
A detailed document showing:
- How you'll manage the land ecologically
- What you'll grow and how
- How you'll generate energy
- How you'll manage waste
- Your 5-year plan with targets
"""
            },
            {
                "type": "text",
                "content": """
### The Three Food Groups

As we mentioned in the law module, OPD works best when three types of food provision work together:

🌿 **Foragers** — Find wild food in hedgerows, woodlands, and coastlines. This is the lowest-impact food source because you don't have to grow anything.

🏘️ **Off-Grid Dwellers** — Preserve, store, and cook wild and homegrown food. If you can dry herbs, ferment vegetables, make jam, and store root crops, you can eat your own produce all year.

🚜 **Farmers** — Grow food on the land sustainably. This means permaculture, organic methods, and working with nature rather than against it.

**All three roles overlap on a successful OPD.** The person foraging is also the person preserving, and the person growing. That's what makes it a homestead rather than just a house.

### Applying for OPD

1. **Find land** in Wales (OPD only applies in Wales, not England or Scotland)
2. **Write a management plan** — This is the hard part. You need to prove your plans are realistic.
3. **Submit a planning application** — With your management plan, ecological footprint assessment, and business plan
4. **Get permission** — Usually for 5 years initially, then reviewed
5. **Build and live** — Prove you can meet your targets over time
"""
            },
            {
                "type": "quiz",
                "question": "What percentage of basic household needs must you provide from the land for OPD?",
                "options": ["25%", "50%", "65%", "100%"],
                "answer": "65%",
                "feedback": "Correct! OPD requires you to provide at least 65% of your basic needs from the land, with a realistic plan for the rest."
            },
            {
                "type": "final_quiz",
                "question": "Why does OPD require a management plan?",
                "options": [
                    "To make the application expensive",
                    "To prove your plans are realistic and sustainable",
                    "To stop anyone from applying",
                    "To compare you to other applicants"
                ],
                "answer": "To prove your plans are realistic and sustainable",
                "reward": 25
            }
        ]
    },

    # ═════════════════════════════════════════════════
    # HOMESTEADING PATH
    # ═════════════════════════════════════════════════

    "Keeping Chickens": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🐔 Keeping Chickens

Chickens are the **gateway animal** for homesteading. They're relatively easy to keep, provide fresh eggs, and help in the garden by eating pests and providing fertiliser.

**What chickens give you:**
- 🥚 Eggs — A good hen lays 250–300 eggs per year
- 🐛 Pest control — They eat slugs, snails, and insects
- 💩 Manure — Chicken manure is excellent for the garden (after composting!)
- 🍗 Meat — If you choose to (not everyone does)
"""
            },
            {
                "type": "text",
                "content": """
### Choosing Breeds

**Good beginner breeds:**
- **Warren / ISA Brown** — The classic egg layer. Friendly, reliable, 300+ eggs per year
- **Rhode Island Red** — Hardy, dual-purpose (eggs + meat), 250+ eggs per year
- **Sussex** — Calm, friendly, good in cold weather, 250+ eggs per year
- **Hybrid layers** — Crossbreeds designed for maximum egg production

**Avoid as a beginner:**
- Pure breeds that go broody (sit on eggs instead of laying)
- Very rare breeds (expensive and harder to keep)
- Bantams (small chickens) — Cute but lay small eggs

### Housing & Run

**The Coop (indoor house):**
- Waterproof and predator-proof
- 30cm perch space per bird
- Nesting boxes (1 per 4 hens)
- Ventilation without draughts
- Easy to clean

**The Run (outdoor area):**
- Minimum 2m² per bird
- Fenced with chicken wire AND a roof (foxes climb!)
- Enrichment: logs, dust bath area, hanging vegetables
- Protection from hawks (netting over the top)

> *The number one predator in the UK is the fox. Assume foxes WILL find your chickens. Make your coop fox-proof.*
"""
            },
            {
                "type": "text",
                "content": """
### Feeding & Daily Care

**Daily routine (15–20 minutes):**
1. Let chickens out of the coop in the morning
2. Check food and water — refill as needed
3. Collect eggs
4. Quick health check (bright eyes, clean feathers, active)
5. Close coop at dusk (foxes are nocturnal!)

**What to feed:**
- **Layers pellets or mash** — Complete nutrition for egg layers
- **Grain** — As a treat, not main food (wheat, mixed corn)
- **Greens** — Cabbage, kale, grass (hang them up for entertainment)
- **Grit** — Essential for eggshell formation
- **Fresh water** — Always available, changed daily

**What NOT to feed:**
- Avocado (toxic to chickens)
- Chocolate (toxic)
- Onions (affects egg taste)
- Citrus (can cause issues)
- Mouldy or salty food

**How much?** A laying hen eats about 120–150g of feed per day.
"""
            },
            {
                "type": "quiz",
                "question": "What is the most important predator to protect chickens from in the UK?",
                "options": ["Badgers", "Foxes", "Cats", "Hawks"],
                "answer": "Foxes",
                "feedback": "Correct! Foxes are the number one threat to UK chickens. They can climb, dig, and squeeze through small gaps."
            },
            {
                "type": "final_quiz",
                "question": "How many eggs per year can a good egg-laying breed produce?",
                "options": ["50–100", "100–150", "250–300", "500+"],
                "answer": "250–300",
                "reward": 15
            }
        ]
    },

    "Ducks & Geese": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🦆 Ducks & Geese

Ducks and geese are excellent additions to a homestead. They're hardy, entertaining, and produce eggs, meat, and pest control.

**Ducks vs Chickens:**
- Ducks lay more consistently through winter
- Duck eggs are richer and larger than chicken eggs
- Ducks are more cold-hardy
- Ducks don't scratch up your garden (chickens do!)
- Ducks need water to be happy (chickens don't)
- Ducks are MESSY with water
"""
            },
            {
                "type": "text",
                "content": """
### Duck Breeds

**For eggs:**
- **Khaki Campbell** — The best egg layer, 300+ eggs per year
- **Indian Runner** — Upright walking ducks, 250+ eggs per year, very entertaining

**For dual purpose (eggs + meat):**
- **Aylesbury** — Large white ducks, good meat birds
- **Rouen** — Mallard-like, good forager, decent egg layer

**For pest control:**
- **Call Ducks** — Small, noisy, excellent at attracting and catching insects
- **Muscovy** — Not a true duck, eats huge amounts of flies and mosquitoes

### Goose Breeds

**For the homestead:**
- **Embden** — Large white geese, good meat and weeders
- **Toulouse** — Hardy, calm temperament
- **Chinese Geese** — Excellent watchdogs (very noisy!), good foragers

### Housing & Water

**Duck housing:**
- Simpler than chicken coops (ducks don't need perches)
- Must be predator-proof
- Floor-level sleeping (ducks sleep on the ground)
- Plenty of straw bedding (ducks are very messy)

**Water requirements:**
- Ducks need water to submerge their heads (to clean their eyes and nostrils)
- A child's paddling pool works well for a small flock
- Geese need enough water to swim
- **Mud management is essential** — ducks turn any water source into a mud bath
- Position water sources away from housing!
"""
            },
            {
                "type": "text",
                "content": """
### Care & Feeding

**Duck feed:**
- **Layers pellets** — Same as chicken layers pellets (ducks can eat them)
- **Waterfowl feed** — Specifically formulated (if available)
- **Grain** — As a treat (wheat, mixed corn)
- **Greens** — Ducks love grass, lettuce, peas
- **Slugs and snails** — Ducks will eat garden pests happily!

**Goose grazing:**
- Geese are **grazers** — they eat grass like sheep
- They can get most of their food from good pasture in summer
- Supplement with grain in winter
- Geese are excellent at **weeding** — they eat grass but leave many vegetables alone

**Health:**
- Ducks are generally healthier than chickens (fewer respiratory issues)
- Clean water is ESSENTIAL — dirty water leads to infections
- Watch for leg injuries (ducks are heavy and can injure their legs)
- Geese can be aggressive — respect their space, especially in breeding season
"""
            },
            {
                "type": "quiz",
                "question": "What is a major advantage of ducks over chickens for egg production?",
                "options": [
                    "Duck eggs are smaller",
                    "Ducks lay more consistently through winter",
                    "Ducks are quieter",
                    "Ducks need less water"
                ],
                "answer": "Ducks lay more consistently through winter",
                "feedback": "Correct! Ducks continue laying through the darker months when chickens often slow down or stop."
            },
            {
                "type": "final_quiz",
                "question": "What is the main reason geese are useful on a homestead (besides eggs and meat)?",
                "options": [
                    "They produce lots of manure",
                    "They are excellent watchdogs and weeders",
                    "They catch mice",
                    "They plough fields"
                ],
                "answer": "They are excellent watchdogs and weeders",
                "reward": 20
            }
        ]
    },

    "Keeping Goats": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🐐 Keeping Goats

Goats are brilliant homestead animals — they provide **milk, cheese, meat, and land management**. But they're also escape artists and need serious fencing!

**What goats give you:**
- 🥛 Milk — 2–4 litres per day from a good milking doe
- 🧀 Cheese, yoghurt, butter — From goat's milk
- 💩 Manure — Excellent for the garden
- 🌿 Brush clearance — Goats eat brambles, nettles, and weeds that other animals won't touch
"""
            },
            {
                "type": "text",
                "content": """
### Choosing a Breed

**Dairy goats (for milk):**
- **Saanen** — Large, white, highest milk yield (3–5 litres/day). Calm temperament.
- **Toggenburg** — Medium, brown and white. Reliable milk producer. Hardy.
- **British Alpine** — Black and white. Good milk yield, good temperament.
- **Pygmy** — Small, friendly, lower milk yield but great for small plots.

**Dual purpose (milk + meat):**
- **Boer** — The main meat breed. Muscular, fast-growing.
- **Kiko** — Hardy, good foragers, low maintenance.

### Housing & Fencing

**Housing:**
- A dry, draught-free shelter (3–4m² per goat)
- Must have good ventilation (goat respiratory issues are common)
- Raised sleeping platforms (goats hate damp ground)
- Separate kidding area if breeding

**Fencing (the most important thing!):**
- Stock fencing at least 1.2m high
- Goats will test EVERY weak point
- They can squeeze through tiny gaps
- They will climb on anything and use it as a ladder
- Electric fencing works well as a second line of defence

> *If you think your fence is goat-proof, check again. Then check a third time.*
"""
            },
            {
                "type": "text",
                "content": """
### Feeding & Milking

**Goat diet:**
- **Hay** — The staple food, especially in winter (ad lib access)
- **Concentrate/goat mix** — For milking goats (about 1kg per day)
- **Grazing** — Goats are browsers, not grazers. They prefer shrubs, hedges, and brambles to grass
- **Fresh water** — Always available, goats drink 5–10 litres per day

**Milking:**
- Milk twice a day (morning and evening)
- Wash the udder before milking
- Use a clean, sterilised container
- Goat's milk tastes sweeter than cow's milk (and is easier to digest)
- A good dairy goat produces milk for 8–10 months after kidding

**Making cheese:**
- Soft cheese (chèvre) is easy — just add rennet and culture, drain, season
- Hard cheese takes longer — press and age
- Yoghurt is even easier — just add culture to warm milk

### UK Regulations

- You need a **holding number** from the Rural Payments Agency
- Each goat needs an **identification tag**
- You must keep **movement records**
- You cannot sell raw milk directly to the public without a licence
"""
            },
            {
                "type": "quiz",
                "question": "Why is fencing so important with goats?",
                "options": [
                    "Goats are expensive to buy",
                    "Goats are escape artists that will test every weak point",
                    "Goats are noisy neighbours",
                    "Goats need very large fields"
                ],
                "answer": "Goats are escape artists that will test every weak point",
                "feedback": "Correct! Goats are notorious escape artists. They can squeeze through tiny gaps and climb over obstacles."
            },
            {
                "type": "final_quiz",
                "question": "What is the key difference between how goats and sheep eat?",
                "options": [
                    "Goats eat more",
                    "Goats are browsers (prefer shrubs and hedges), sheep are grazers (prefer grass)",
                    "Goats only eat grass",
                    "There is no difference"
                ],
                "answer": "Goats are browsers (prefer shrubs and hedges), sheep are grazers (prefer grass)",
                "reward": 20
            }
        ]
    },

    "Starting an Orchard": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🍎 Starting an Orchard

An orchard is a planted area of fruit trees. In the UK, orchards have been part of the landscape for over 2,000 years. Growing your own fruit is one of the most rewarding things you can do on a homestead.

**Why plant an orchard?**
- 🍎 Fresh fruit for months every year
- 🍺 Cider, juice, preserves, and dried fruit
- 🌳 Habitat for wildlife (birds, insects, fungi)
- 🏠 Shade and shelter
- 💰 A mature orchard can produce hundreds of kilos of fruit per year
"""
            },
            {
                "type": "text",
                "content": """
### Choosing Your Trees

**The Big Five UK Orchard Fruits:**

1. **🍎 Apple** — The king of orchards. Eaters, cookers, and cider varieties. Over 2,000 UK varieties!

2. **🍐 Pear** — Sweet, buttery fruit. Eat fresh or cook. Fewer varieties than apples but still excellent.

3. ** Plum** — Sweet and juicy. Blossom is beautiful in spring. Good for jam.

4. **🍒 Cherry** — Sweet or sour. Birds love them too — netting is essential!

5. **🍐 Damson** — A small, tart plum. Makes incredible jam and gin.

**Choosing varieties:**
- Choose **disease-resistant** varieties for fewer problems
- Check the **rootstock** — this determines the tree's final size:
  - **M27** — Very small (1.8m) — good for small gardens
  - **M9** — Small (2.5m) — needs support
  - **M26** — Medium (3m) — good for most orchards
  - **MM106** — Large (4m) — traditional orchard size

**Pollination groups:** Apple trees need a partner that flowers at the same time to produce fruit. Check pollination groups before buying!
"""
            },
            {
                "type": "text",
                "content": """
### Planting & Early Care

**When to plant:** November–March (dormant season, bare-root trees)

**How to plant:**
1. Dig a hole wider than the roots (about 60cm wide, 30cm deep)
2. Drive in a stake on the windward side
3. Place the tree in the hole, spreading the roots
4. The graft union (the bump near the base) should be ABOVE the soil
5. Backfill with soil, firming gently
6. Water well
7. Mulch around the base (but not touching the trunk)
8. Tie the tree to the stake with a flexible tie

**First year care:**
- Water in dry spells (especially the first summer)
- Keep a 1m circle around the base clear of grass and weeds
- Don't let the tree fruit in its first year (remove flowers)
- Prune in winter to establish a good shape

### Pruning Basics ✂️

**Winter pruning** (November–February) — For established apple and pear trees:
- Remove dead, diseased, and crossing branches
- Aim for an open centre (goblet shape)
- Cut just above an outward-facing bud

**Summer pruning** (July–August) — For trained trees (cordons, espaliers):
- Cut back new growth to 3–4 leaves
- Keeps trees compact and productive
"""
            },
            {
                "type": "quiz",
                "question": "Why do apple trees need a pollination partner?",
                "options": [
                    "For moral support",
                    "Most apple trees are not self-fertile — they need pollen from another variety",
                    "To make the tree grow faster",
                    "Only cider apples need partners"
                ],
                "answer": "Most apple trees are not self-fertile — they need pollen from another variety",
                "feedback": "Correct! Most apples need a different variety flowering at the same time to produce fruit."
            },
            {
                "type": "final_quiz",
                "question": "When is the best time to plant a bare-root fruit tree in the UK?",
                "options": [
                    "June–August",
                    "November–March",
                    "Any time of year",
                    "Only in January"
                ],
                "answer": "November–March",
                "reward": 15
            }
        ]
    },

    "Composting & Soil Health": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "7-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🪱 Composting & Soil Health

**Soil is alive.** A single teaspoon of healthy soil contains more microorganisms than there are people on Earth. If you look after your soil, your soil will look after your plants.

**The composting cycle:**
> *Kitchen scraps → Compost heap → Rich soil → Healthy plants → Food → Kitchen scraps → Compost heap*

Nothing is wasted in nature. Composting is nature's way of recycling.
"""
            },
            {
                "type": "text",
                "content": """
### Hot Composting 🔥

The fastest method. A hot compost heap can turn waste into compost in **6–8 weeks**.

**The recipe:**
1. **Greens (nitrogen-rich)** — Kitchen scraps, grass clippings, coffee grounds, manure
2. **Browns (carbon-rich)** — Dry leaves, cardboard, straw, paper, wood chips
3. **Water** — The heap should be as damp as a wrung-out sponge
4. **Air** — Turn the heap every 1–2 weeks

**The ideal ratio:** About 3 parts browns to 1 part greens by volume.

**How it works:**
- Microorganisms eat the greens and browns
- Their activity generates heat (the centre can reach 60°C!)
- The heat kills weed seeds and most pathogens
- After a few weeks, the material breaks down into dark, crumbly compost

**Signs your compost is working:**
- It's warm in the middle (put your hand in — it should feel warm)
- It smells earthy, not rotten
- It's shrinking in volume
- You can see worms and other creatures
"""
            },
            {
                "type": "text",
                "content": """
### Cold Composting 🧊

Slower but easier. Just pile it up and wait. Takes **6–12 months**.

**Pros:** No turning, no checking temperature, less work
**Cons:** Slower, doesn't kill weed seeds, may attract rats if you add food waste

**What to compost:**
✅ Vegetable peelings, fruit scraps
✅ Tea bags (remove staples), coffee grounds
✅ Eggshells (crushed)
✅ Garden waste (chopped up)
✅ Cardboard (torn up), newspaper
✅ Hair, nail clippings (yes, really!)

**What NOT to compost:**
❌ Meat, fish, bones (attracts rats)
❌ Dairy products (attracts pests)
❌ Cooked food (attracts rats)
❌ Diseased plants (cold compost won't kill the disease)
❌ Cat/dog poo (contains harmful pathogens)
❌ Plastic, metal, glass (obviously!)

### Wormeries 🪱

A wormery is a compact composting system using **special composting worms** (tiger worms or red wigglers).

**Why wormeries are great:**
- Small — fits on a balcony or patio
- Fast — worms eat their weight in food every day
- Produces liquid fertiliser (worm tea) AND solid compost
- Can handle kitchen waste that cold compost can't (in small amounts)

**Wormery tips:**
- Don't overfeed — add small amounts regularly
- Keep moist but not waterlogged
- Keep in a sheltered spot (not in direct sun or frost)
- Worms eat HALF their body weight per day
"""
            },
            {
                "type": "text",
                "content": """
### Understanding Your Soil

**The Squeeze Test:**
1. Take a handful of moist soil
2. Squeeze it firmly
3. Open your hand:
   - If it falls apart immediately → **Sandy soil** (drains fast, needs watering)
   - If it holds its shape but crumbles when poked → **Loam** (the ideal soil!)
   - If it holds its shape and feels sticky → **Clay soil** (holds water, hard to dig)

**Improving any soil:**
- **Sandy soil** — Add compost and manure to hold water and nutrients
- **Clay soil** — Add compost and grit to improve drainage
- **Loam** — Add compost to keep it healthy

**The pH test:** Most vegetables prefer soil with a pH of 6.5–7.0 (slightly acidic to neutral). Buy a simple pH testing kit from a garden centre.

**The Golden Rule:**
> *Feed the soil, not the plant. If your soil is healthy, your plants will be healthy.*
"""
            },
            {
                "type": "quiz",
                "question": "What is the ideal ratio of browns to greens in a hot compost heap?",
                "options": ["1 part browns to 3 parts greens", "Equal parts", "3 parts browns to 1 part greens", "All greens"],
                "answer": "3 parts browns to 1 part greens",
                "feedback": "Correct! About 3 parts browns (carbon) to 1 part greens (nitrogen) by volume gives the microorganisms the right balance."
            },
            {
                "type": "final_quiz",
                "question": "What is the golden rule of soil health?",
                "options": [
                    "Add fertiliser every week",
                    "Feed the soil, not the plant",
                    "Never walk on the soil",
                    "Only grow native plants"
                ],
                "answer": "Feed the soil, not the plant",
                "reward": 15
            }
        ]
    },

    "Small-Scale Vegetable Growing": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🥕 Small-Scale Vegetable Growing

You don't need acres of land to grow food. A well-managed 10m × 10m plot can produce a significant amount of vegetables for a family.

**The key principles:**
1. **Grow what you eat** — Don't grow turnips if nobody likes turnips
2. **Plan for succession** — When one crop finishes, another takes its place
3. **Rotate your crops** — Don't grow the same thing in the same spot every year
4. **Start small and expand** — Better to manage 2 beds well than 6 beds badly
"""
            },
            {
                "type": "text",
                "content": """
### Crop Rotation 🔄

Growing the same crop in the same place year after year causes **build-up of pests and diseases** and **depletion of specific nutrients**. Crop rotation prevents this.

**The 4-Bed Rotation:**

**Bed 1: Roots** — Carrots, parsnips, beetroot, potatoes
- Need: Light soil, don't like fresh manure
- Follow with: Legumes (Bed 2 next year)

**Bed 2: Legumes** — Peas, beans, broad beans
- Need: Support structures
- Give back: Fix nitrogen in the soil (good for the next crop!)
- Follow with: Brassicas (Bed 3 next year)

**Bed 3: Brassicas** — Cabbage, broccoli, kale, Brussels sprouts
- Need: Firm soil, nitrogen (left by the legumes)
- Follow with: Others (Bed 4 next year)

**Bed 4: Others** — Onions, leeks, tomatoes, courgettes, salad
- Follow with: Roots (Bed 1 next year)

**The cycle:** Roots → Legumes → Brassicas → Others → Roots → ...

Each group moves to the next bed every year. After 4 years, everything is back where it started.
"""
            },
            {
                "type": "text",
                "content": """
### What to Grow When 📅

**Spring (March–May) — Sow:**
- Early potatoes, onions, peas, broad beans, radishes, lettuce
- Under cover: tomatoes, peppers, courgettes, squash

**Summer (June–August) — Sow & Harvest:**
- Harvest: peas, beans, early potatoes, salad, courgettes, tomatoes
- Sow for winter: kale, winter cabbage, leeks, beetroot

**Autumn (September–November) — Harvest:**
- Harvest: maincrop potatoes, onions, squash, sweetcorn, beans
- Sow: garlic, winter lettuce, broad beans (for next year)
- Clear beds and add compost

**Winter (December–February) — Plan:**
- Order seeds and plan your rotation
- Chit potatoes (sprout them before planting)
- Sow indoors: chillies, peppers, early tomatoes

### Easy Crops for Beginners

1. 🥬 **Lettuce & salad leaves** — Grow in 4 weeks, can succession sow
2. 🥕 **Radishes** — Ready in 4 weeks, very forgiving
3. 🫘 **Beans (French and runner)** — Easy to grow, produce for weeks
4. 🥒 **Courgettes** — Just 2 plants will feed a family all summer
5. 🥔 **Potatoes** — Almost foolproof, grow in the ground or in bags
6. 🌿 **Herbs** — Mint, chives, parsley, basil — expensive to buy, easy to grow
"""
            },
            {
                "type": "text",
                "content": """
### Common Pests & Problems 🐛

**Slugs & Snails** — The number one enemy of the vegetable garden
- Solutions: Beer traps, copper tape, nematodes, hand-picking at dusk, encourage frogs/hedgehogs

**Cabbage White Butterfly** — Lays eggs on brassicas, caterpillars devour leaves
- Solutions: Net brassicas with fine mesh, check undersides of leaves, pick off caterpillars

**Aphids (Greenfly/Blackfly)** — Suck sap, weaken plants, spread disease
- Solutions: Spray with soapy water, encourage ladybirds, don't over-feed (soft growth attracts aphids)

**Carrot Fly** — Larvae tunnel into carrots
- Solutions: Grow in raised beds, sow after mid-May (flies less active), companion plant with onions

**Blight** — Fungal disease that destroys tomatoes and potatoes
- Solutions: Good ventilation, don't wet leaves when watering, remove infected plants immediately, grow resistant varieties

**The Best Pest Control:**
> *Healthy plants resist pests. Stressed plants attract them. Good soil, proper watering, and correct spacing prevent most problems.*
"""
            },
            {
                "type": "quiz",
                "question": "Why is crop rotation important?",
                "options": [
                    "It makes the garden look organised",
                    "It prevents build-up of pests, diseases, and nutrient depletion",
                    "It's required by law",
                    "It makes plants grow faster"
                ],
                "answer": "It prevents build-up of pests, diseases, and nutrient depletion",
                "feedback": "Correct! Rotating crops prevents the same pests and diseases building up in the soil year after year."
            },
            {
                "type": "final_quiz",
                "question": "What is the correct order in a 4-bed crop rotation?",
                "options": [
                    "Brassicas → Roots → Legumes → Others",
                    "Roots → Legumes → Brassicas → Others",
                    "Legumes → Roots → Others → Brassicas",
                    "Others → Roots → Brassicas → Legumes"
                ],
                "answer": "Roots → Legumes → Brassicas → Others",
                "reward": 20
            }
        ]
    },

    "Beekeeping Basics": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18", "PSHE/R11"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🐝 Beekeeping Basics

Bees are essential for life on Earth. They pollinate around **one third of the food we eat**. Keeping bees is fascinating, rewarding, and produces the most incredible honey.

⚠️ **Safety Warning:** Beekeeping involves working with stinging insects. Some people are severely allergic to bee stings. Always wear protective clothing and work calmly and slowly around bees.

**Why keep bees?**
- 🍯 Honey — 15–30kg per hive per year
- 🐝 Pollination — Bees increase yields of fruit and vegetables by 20–30%
- 🕯️ Beeswax — For candles, polish, and cosmetics
- 🌺 Biodiversity — Your garden and surrounding area will benefit enormously
"""
            },
            {
                "type": "text",
                "content": """
### The Hive

The most common hive in the UK is the **National Hive**. It's a stack of wooden boxes:

1. **Floor** — The entrance at the bottom
2. **Brood box** — The largest box where the queen lays eggs and the colony lives
3. **Queen excluder** — A grid that lets workers through but keeps the queen in the brood box
4. **Supers** — Smaller boxes on top where the bees store excess honey (that we harvest)
5. **Crown board** — The roof, with a hole for feeding
6. **Roof** — Weather protection

**The colony consists of:**
- **One queen** — Lays all the eggs (up to 2,000 per day in summer!)
- **Thousands of workers** (all female) — Forage, nurse young, build comb, guard the hive
- **Drones** (male, in summer only) — Mate with virgin queens, then die. They do no work in the hive.

### The Beekeeping Year

**🌸 Spring (March–May):**
- Check colonies have survived winter
- Check the queen is laying
- Add supers as the colony grows
- Watch for swarming (see below)

**☀️ Summer (June–August):**
- Peak honey production
- Add more supers as needed
- Extract honey when frames are capped (sealed with wax)
- Swarm control!

**🍂 Autumn (September–November):**
- Final honey extraction
- Treat for varroa mites (a bee parasite)
- Feed sugar syrup if stores are low
- Prepare hives for winter

**❄️ Winter (December–February):**
- Leave the bees alone (they cluster to keep warm)
- Heft the hive (lift one side to check weight of stores)
- Plan for next season
"""
            },
            {
                "type": "text",
                "content": """
### Swarms 🐝

A swarm is how bees reproduce. When a colony gets too big, the old queen leaves with half the bees to find a new home. A new queen stays behind with the other half.

**What to do if your bees swarm:**
1. Don't panic — swarming bees are calm (they've eaten honey before leaving and are full!)
2. Collect the swarm (if it's accessible) into a hive or box
3. They can be re-hived and will start a new colony

**How to prevent swarming:**
- Give the bees enough space (add supers early)
- Do regular inspections (every 7 days in May and June)
- If you see queen cells (peanut-shaped cells), the bees are planning to swarm
- Create an artificial swarm (split the colony) to keep both halves

### Honey Extraction 🍯

1. Remove super frames when most cells are capped (sealed with wax)
2. Uncap the cells using a hot knife or uncapping fork
3. Spin frames in a honey extractor (centrifugal force pushes honey out)
4. Strain honey through a fine mesh
5. Bottle and label!
6. Return empty frames to the bees to clean up

> *A good beekeeper takes only what the bees can spare. Leave enough honey for the bees to survive winter.*
"""
            },
            {
                "type": "quiz",
                "question": "What is a swarm?",
                "options": [
                    "A group of angry bees",
                    "How bees reproduce — the old queen leaves with half the colony",
                    "A disease that kills bees",
                    "A type of beehive"
                ],
                "answer": "How bees reproduce — the old queen leaves with half the colony",
                "feedback": "Correct! Swarming is natural reproduction. The old queen and half the bees leave to start a new colony."
            },
            {
                "type": "final_quiz",
                "question": "How much honey can a single hive produce in a good year?",
                "options": ["1–5 kg", "5–10 kg", "15–30 kg", "50–100 kg"],
                "answer": "15–30 kg",
                "reward": 25
            }
        ]
    },

    "Natural Remedies from the Garden": {
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18", "PSHE/R11"],
        "ks2_age": "9-11",
        "steps": [
            {
                "type": "text",
                "content": """
## 🌿 Natural Remedies from the Garden

⚠️ **IMPORTANT WARNING:** This module is about traditional and historical uses of common garden plants. It does NOT replace medical advice. Always consult a qualified professional for health concerns. Never use wild plants as medicine without expert identification.

**What you'll learn:**
- Common garden plants with traditional remedy uses
- How they were historically prepared
- What is SAFE to try and what is NOT
"""
            },
            {
                "type": "text",
                "content": """
### Safe Garden Remedies (With Adult Supervision)

These are gentle, commonly available plants with well-established traditional uses:

**🌿 Mint (Peppermint)**
- Traditional use: Mint tea for digestion and headaches
- How: Steep fresh or dried leaves in hot water for 5 minutes
- Safety: Very safe for most people (avoid large amounts in pregnancy)

**🌿 Chamomile**
- Traditional use: Chamomile tea for calm and sleep
- How: Steep flower heads in hot water
- Safety: Very safe (avoid if allergic to daisies/ragweed)

**🌿 Lavender**
- Traditional use: Lavender sachets for better sleep; lavender oil for minor burns
- How: Dry flowers for sachets; diluted essential oil for skin
- Safety: Safe externally (don't take essential oil internally)

**🌿 Thyme**
- Traditional use: Thyme tea for coughs and sore throats
- How: Steep fresh thyme in hot water, add honey
- Safety: Very safe as a tea

**🌿 Rosemary**
- Traditional use: Rosemary tea for concentration and memory
- How: Steep fresh sprigs in hot water
- Safety: Safe in moderation (avoid large amounts in pregnancy)

**🌿 Calendula (Pot Marigold)**
- Traditional use: Calendula salve for minor cuts, scrapes, and skin irritation
- How: Infuse petals in oil, then use as a salve
- Safety: Very safe externally
"""
            },
            {
                "type": "text",
                "content": """
### How to Make Simple Preparations

**1. Herbal Tea (Infusion)**
- Take 1–2 teaspoons of dried herb (or 2–3 of fresh)
- Pour boiling water over
- Cover and steep for 5–10 minutes
- Strain and drink
- Add honey to taste if desired

**2. Herbal Oil**
- Fill a jar with dried herbs
- Cover with olive oil
- Leave on a sunny windowsill for 2–4 weeks
- Strain through muslin
- Store in a dark bottle
- Use externally as a massage oil or in salves

**3. Simple Salve**
- Melt 100g of herbal oil with 15g of beeswax
- Pour into tins while still liquid
- Allow to set
- Use externally on dry skin, minor scrapes, etc.

### 🚫 What NEVER to Use

**Never use these as remedies without professional guidance:**

- **Foxglove** — Contains digitalis, a powerful heart drug. The difference between medicine and poison is the dose.
- **Deadly Nightshade** — Extremely poisonous. Causes hallucinations, paralysis, and death.
- **Hemlock** — Fatal. There is no safe dose.
- **Yew** — All parts except the berry flesh are deadly.
- **Any plant you cannot identify with 100% certainty**

> *If you are unsure about a plant, DO NOT USE IT. When in doubt, leave it out.*
"""
            },
            {
                "type": "quiz",
                "question": "What is the safest way to use lavender as a remedy?",
                "options": [
                    "Drink lavender essential oil",
                    "Eat large quantities of lavender",
                    "Dry flowers for sachets, or use diluted oil externally",
                    "Apply concentrated essential oil directly to wounds"
                ],
                "answer": "Dry flowers for sachets, or use diluted oil externally",
                "feedback": "Correct! Lavender is safest used externally — as dried flowers for sleep sachets, or diluted oil for minor skin issues."
            },
            {
                "type": "final_quiz",
                "question": "What is the most important rule about using plants as remedies?",
                "options": [
                    "Use as much as possible for the strongest effect",
                    "Only use plants that taste good",
                    "Never use wild plants as medicine without expert guidance and identification",
                    "All natural remedies are safe"
                ],
                "answer": "Never use wild plants as medicine without expert guidance and identification",
                "reward": 25
            }
        ]
    },
}
