# lessons_data.py

LESSON_CONTENT = {
    "Introduction to Foraging": {
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
        "steps": [
            {
                "type": "text",
                "content": "## Foraging and the Law ⚖️\nKnowing the law protects you and nature."
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
    # --- NEW MODULES ---
    "The Coastal Code": {
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
    }
}