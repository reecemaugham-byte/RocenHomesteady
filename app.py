import streamlit as st
import random
import time
import pandas as pd
from collections import Counter
from datetime import datetime
from openai import OpenAI
import os
import json

# --- SAFE IMPORTS ---
# Robust import handling to prevent crashes on deployment
try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import alpaca_trade_api as tradeapi
except ImportError:
    tradeapi = None

# Handle PIL deprecation safely
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    Image = None

# Safe import for edge_tts with async support
try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# ==========================================
# CONFIGURATION
# ==========================================
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "sk-proj--" # Placeholder

if not api_key:
    client = None
else:
    try:
        client = OpenAI(api_key=api_key)
    except:
        client = None

# ==========================================
# PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="Rocen Homesteady",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME FUNCTION ---
def apply_forest_theme():
    st.markdown("""
    <style>
    /* Main Background - Darker Sage */
    .stApp {
        background-color: #C8D6C8;
        background-image: radial-gradient(#A8BCA8 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Text Color - Deep Jungle Green */
    .stMarkdown, .stHeader, p, label {
        color: #1B4D3E !important;
    }

    /* Headings - Darker Brown */
    h1, h2, h3 {
        color: #3E2723 !important; 
        font-family: 'Georgia', serif !important;
        border-bottom: 2px solid #8FBC8F;
        padding-bottom: 10px;
    }

    /* Buttons - Primary Green */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        border: 2px solid #388E3C;
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #388E3C;
        transform: scale(1.02);
    }

    /* Sidebar - Dark Sage */
    [data-testid="stSidebar"] {
        background-color: #A8C0A8;
    }

    /* Metric Boxes - Soft Off-White */
    [data-testid="stMetric"] {
        background-color: #F5F9F5;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 0 0 1px #C8E6C9;
        border-left: 5px solid #4CAF50;
    }

    /* Tabs */
    .stTabs [data-badges="badge"] {
        background-color: #F1F8E9;
        color: #2E4A3E;
    }
    button[aria-selected="true"] {
        background-color: #66BB6A !important;
        color: white !important;
    }

    /* Expander (Used in Learning) */
    .streamlit-expanderHeader {
        background-color: #F5F9F5;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        font-weight: bold;
    }
    
    /* Custom Warning Box for Plants */
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        color: #856404;
    }
    
    /* Danger Box for Poisonous Plants */
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)

apply_forest_theme()

# ==========================================
# DATA (Expanded & Improved)
# ==========================================
UK_PLANTS = {
    "edible": [
        {"name": "Wild Garlic", "months": ["March", "April", "May"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Strong smell helps identification", "lookalikes": ["Lily of the Valley (Poisonous)"], "description": "**Identification:** Broad leaves, white flowers, smells strongly of garlic."},
        {"name": "Nettles", "months": ["February", "March", "April", "May", "June"], "habitat": "Woodlands, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Young leaves", "warnings": "Wear gloves when picking", "lookalikes": ["Dead-nettle (Edible, no sting)"], "description": "**Identification:** Jagged leaves, stinging hairs. **Uses:** Soup, tea."},
        {"name": "Dandelion", "months": ["February", "March", "April", "May", "June", "July"], "habitat": "Everywhere", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers, Roots", "warnings": "Avoid areas with dog waste", "lookalikes": ["Cat's Ear (Edible)"], "description": "**Identification:** Yellow flowers, hollow stems, 'lion's tooth' leaves."},
        {"name": "Three-Cornered Leek", "months": ["January", "February", "March", "April"], "habitat": "Woodlands, Hedgerows", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Leaves, Flowers, Bulbs", "warnings": "Invasive species - pick freely!", "lookalikes": ["Snowdrop (Inedible)", "Bluebell (Poisonous)"], "description": "**Identification:** Strap-like leaves with a 'keel' (triangular shape like a boat). Smells like onion/garlic."},
        {"name": "Wood Ear (Jelly Ear)", "months": ["January", "February", "November", "December"], "habitat": "Woodlands (Elder trees)", "regions": ["All"], "difficulty": 2, "parts": "Fungus", "warnings": "Must be cooked, raw can cause itchiness. Availability depends on wet weather.", "lookalikes": ["Other tree fungi"], "description": "**Identification:** Brown, jelly-like, grows on Elder branches."},
        {"name": "Sorrel", "months": ["April", "May", "June", "July"], "habitat": "Grassland, Meadows", "regions": ["All"], "difficulty": 1, "parts": "Leaves", "warnings": "Contains oxalic acid, eat in moderation", "lookalikes": ["Lords and Ladies (Poisonous)"], "description": "**Identification:** Arrow-shaped leaves, sharp lemon taste."},
        {"name": "Elderflower", "months": ["June", "July"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Flowers", "warnings": "Don't confuse with dwarf elder", "lookalikes": ["Hemlock (Poisonous)", "Cow Parsley"], "description": "**Identification:** Creamy-white flat flower heads."},
        {"name": "Blackberries", "months": ["August", "September"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Berries", "warnings": "Watch for thorns", "lookalikes": ["None dangerous in UK"], "description": "**Identification:** Bramble with thorns and dark purple/black berries."},
        {"name": "Rosehips", "months": ["September", "October", "November", "December"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Fruit", "warnings": "Remove seeds before eating", "lookalikes": ["None dangerous"], "description": "**Identification:** Red, oval hips on wild rose bushes."},
        {"name": "Hawthorn", "months": ["September", "October"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Berries", "warnings": "Pips contain cyanide - spit out", "lookalikes": ["None dangerous"], "description": "**Identification:** Thorny shrub with red berries (Haws)."},
        {"name": "Chanterelle", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 3, "parts": "Whole mushroom", "warnings": "EXPERT ONLY - False gills", "lookalikes": ["False Chanterelle (Inedible)"], "description": "**Identification:** Egg-yolk yellow, false gills (ridges), smells of apricots."},
        {"name": "Field Mushroom", "months": ["August", "September", "October"], "habitat": "Fields, Meadows", "regions": ["All"], "difficulty": 2, "parts": "Whole mushroom", "warnings": "Beware of yellow staining lookalikes", "lookalikes": ["Yellow Stainer (Poisonous)"], "description": "**Identification:** White cap, pink gills turning brown."},
        {"name": "Hazelnut", "months": ["September", "October"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Nuts", "warnings": "Pick before squirrels get them", "lookalikes": ["None dangerous"], "description": "**Identification:** Shrubby tree, nuts in green husks."},
        {"name": "Sweet Chestnut", "months": ["October", "November"], "habitat": "Woodlands", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Nuts", "warnings": "Do not confuse with Horse Chestnut", "lookalikes": ["Horse Chestnut (Poisonous)"], "description": "**Identification:** Pointed nuts, many nuts per case."},
        {"name": "Shepherd's Purse", "months": ["January", "February", "March", "April", "May", "June"], "habitat": "Fields, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Seeds", "warnings": "Best when young, peppery", "lookalikes": ["Thale Cress"], "description": "**Identification:** Heart-shaped seed pods (purses). Rosette of lobed leaves."},
        {"name": "Garlic Mustard", "months": ["April", "May", "June"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Smells of garlic when crushed", "lookalikes": ["None dangerous"], "description": "**Identification:** Heart-shaped leaves, white flowers, tall stems."},
        {"name": "Ground Elder", "months": ["March", "April", "May"], "habitat": "Gardens, Woodlands", "regions": ["All"], "difficulty": 2, "parts": "Young leaves", "warnings": "Can be invasive, pick young", "lookalikes": ["Elder (poisonous bark, different leaves)"], "description": "**Identification:** Leaflets in groups of three, celery smell."},
        {"name": "Wild Carrot", "months": ["June", "July", "August"], "habitat": "Grassland, Meadows", "regions": ["All"], "difficulty": 3, "parts": "Root (young)", "warnings": "EXPERT ONLY. Check for hairy stem. Smells of carrot. ILLEGAL TO UPROOT WITHOUT PERMISSION.", "lookalikes": ["Hemlock (Poisonous)"], "description": "**Identification:** White flat-topped flower, one central red flower (often), hairy stem."},
        {"name": "Pignut", "months": ["May", "June"], "habitat": "Meadows, Hedgerows", "regions": ["All"], "difficulty": 3, "parts": "Tubers", "warnings": "EXPERT ONLY. Difficult to identify. ILLEGAL TO UPROOT WITHOUT PERMISSION.", "lookalikes": ["Other umbellifers"], "description": "**Identification:** Delicate white flower, finely divided leaves. Tubers taste like chestnuts."},
        {"name": "Alexanders", "months": ["March", "April", "May"], "habitat": "Coastal, Roadsides", "regions": ["Coastal"], "difficulty": 2, "parts": "Stem, Flower buds", "warnings": "Strong celery smell", "lookalikes": ["Hemlock (Poisonous)"], "description": "**Identification:** Yellow-green flowers, glossy leaves. Common on coast."},
        {"name": "Hedge Mustard", "months": ["May", "June", "July"], "habitat": "Hedgerows, Roadsides", "regions": ["All"], "difficulty": 2, "parts": "Leaves, Flowers", "warnings": "Very bitter when old", "lookalikes": ["Other mustards"], "description": "**Identification:** Tall, spindly plant with tiny yellow flowers."},
        {"name": "Sea Kale", "months": ["May", "June", "July"], "habitat": "Coastal Shingle", "regions": ["Coastal"], "difficulty": 2, "parts": "Shoots, Leaves", "warnings": "Protected in some areas, pick sparingly", "lookalikes": ["None dangerous"], "description": "**Identification:** Blueish leaves, white flowers, found on shingle beaches."},
        {"name": "Wild Strawberry", "months": ["June", "July"], "habitat": "Woodlands, Grassland", "regions": ["All"], "difficulty": 1, "parts": "Berries", "warnings": "Tiny but tasty", "lookalikes": ["Barren Strawberry (Dry, tasteless)"], "description": "**Identification:** Small berries, seeds on outside, white flowers."},
        {"name": "Beech Leaves", "months": ["April", "May"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Young Leaves", "warnings": "Only eat young leaves", "lookalikes": ["None dangerous"], "description": "**Identification:** Oval leaves, soft and hairy when young."},
        {"name": "Lime Leaves", "months": ["April", "May", "June"], "habitat": "Woodlands, Parks", "regions": ["All"], "difficulty": 1, "parts": "Young Leaves, Flowers", "warnings": "None", "lookalikes": ["None dangerous"], "description": "**Identification:** Heart-shaped leaves. **Uses:** Excellent salad green when young."},
        {"name": "Pine Needles", "months": ["January", "February", "December"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Needles", "warnings": "Avoid Yew (flat needles)", "lookalikes": ["Yew (Poisonous)"], "description": "**Identification:** Long needles in bundles. **Uses:** Tea, rich in Vitamin C."},
        {"name": "Puffball", "months": ["August", "September"], "habitat": "Fields, Grassland", "regions": ["All"], "difficulty": 2, "parts": "Whole mushroom (young)", "warnings": "Must be pure white inside. Cut in half.", "lookalikes": ["Earthballs (Poisonous, purple inside)"], "description": "**Identification:** Round white balls. **Safety:** If inside is not pure white, do not eat."},
        {"name": "Jerusalem Artichoke", "months": ["October", "November", "December"], "habitat": "Gardens, Waste Ground", "regions": ["All"], "difficulty": 1, "parts": "Tubers", "warnings": "Can cause wind (flatulence)", "lookalikes": ["None dangerous"], "description": "**Identification:** Tall sunflower-like plant, knobbly tubers underground."},
        {"name": "Cleavers", "months": ["February", "March", "April"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 1, "parts": "Young stems", "warnings": "Best cooked or as tea", "lookalikes": ["None dangerous"], "description": "**Identification:** Sticky stems that cling to clothes."}
    ],
    "poisonous": [
        {"name": "Deadly Nightshade", "months": ["June", "July", "August", "September"], "habitat": "Woodlands, Gardens", "regions": ["All"], "danger": "EXTREME", "symptoms": "Dilated pupils, hallucinations, death", "lookalikes": ["Bilberry"], "description": "**Identification:** Bell-shaped purple flowers, shiny black berries. **Danger:** Fatal."},
        {"name": "Foxglove", "months": ["June", "July", "August"], "habitat": "Gardens, Woodlands", "regions": ["All"], "danger": "HIGH", "symptoms": "Heart failure, nausea", "lookalikes": ["Comfrey"], "description": "**Identification:** Tall spikes of pink/purple trumpet flowers. **Danger:** All parts toxic."},
        {"name": "Hemlock", "months": ["April", "May", "June", "July"], "habitat": "Rivers, Damp areas", "regions": ["All"], "danger": "EXTREME", "symptoms": "Respiratory failure, death", "lookalikes": ["Wild Carrot", "Cow Parsley"], "description": "**Identification:** Tall, purple-spotted stems, smell of mouse urine."},
        {"name": "Hemlock Water Dropwort", "months": ["April", "May", "June", "July"], "habitat": "Riverbanks, Wet ground", "regions": ["All"], "danger": "EXTREME", "symptoms": "Seizures, death", "lookalikes": ["Wild Parsnip", "Pignut"], "description": "**Identification:** White flowers, tuberous roots (deadliest part). **Danger:** Deadliest plant in UK."},
        {"name": "Fool's Parsley", "months": ["May", "June", "July"], "habitat": "Gardens, Waste ground", "regions": ["All"], "danger": "HIGH", "symptoms": "Vomiting, burning mouth", "lookalikes": ["Parsley", "Wild Carrot"], "description": "**Identification:** Looks like Parsley but has a long bract under flower. Smells unpleasant."},
        {"name": "Death Cap", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "danger": "EXTREME", "symptoms": "Liver/kidney failure, often fatal", "lookalikes": ["Straw Mushroom"], "description": "**Identification:** Green-yellow cap, white gills, volva (cup) at base. **Danger:** Most mushroom deaths."},
        {"name": "Lords and Ladies", "months": ["March", "April", "May"], "habitat": "Hedgerows, Woods", "regions": ["All"], "danger": "HIGH", "symptoms": "Mouth blistering, swelling", "lookalikes": ["Sorrel", "Wild Garlic"], "description": "**Identification:** Arrow-shaped leaves, orange berries. **Danger:** Causes burning pain."},
        {"name": "Yew", "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "habitat": "Churchyards, Gardens", "regions": ["All"], "danger": "EXTREME", "symptoms": "Cardiac arrest, death", "lookalikes": ["None (Distinctive tree)"], "description": "**Identification:** Dark evergreen needles, red berry cups (arils). **Danger:** Needles and seeds are deadly."},
        {"name": "Giant Hogweed", "months": ["June", "July", "August"], "habitat": "Riverbanks, Waste ground", "regions": ["England", "Scotland"], "danger": "HIGH", "symptoms": "Severe burns, skin sensitivity", "lookalikes": ["Cow Parsley", "Common Hogweed"], "description": "**Identification:** Huge (3m+), hairy stem with purple blotches. **Danger:** Sap burns skin."},
        {"name": "Dog's Mercury", "months": ["February", "March", "April"], "habitat": "Woodlands", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Vomiting, diarrhoea", "lookalikes": ["Nettles", "Good King Henry"], "description": "**Identification:** Low growing, jagged leaves. **Danger:** Eaten by mistake as salad green."},
        {"name": "Bluebell", "months": ["April", "May"], "habitat": "Woodlands", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Stomach upset, skin irritation", "lookalikes": ["Three-Cornered Leek"], "description": "**Identification:** Blue, bell-shaped flowers. **Danger:** Bulbs are toxic."},
        {"name": "Fly Agaric", "months": ["August", "September", "October"], "habitat": "Woodlands", "regions": ["All"], "danger": "HIGH", "symptoms": "Hallucinations, nausea", "lookalikes": ["None distinctive"], "description": "**Identification:** Classic red cap with white spots. Iconic fairy tale mushroom. **Danger:** Psychoactive and toxic."},
        {"name": "Monkshood", "months": ["June", "July"], "habitat": "Woodlands, Stream banks", "regions": ["UK"], "danger": "EXTREME", "symptoms": "Heart failure", "lookalikes": ["Larkspur"], "description": "**Identification:** Purple helmet-shaped flowers. **Danger:** Very toxic, touching sap can be harmful."},
        {"name": "Bracken", "months": ["Summer"], "habitat": "Moorland, Woods", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Cancer risk (long term)", "lookalikes": ["Other ferns"], "description": "**Identification:** Large fern. **Danger:** Young shoots (fiddleheads) are carcinogenic if eaten. Avoid."}
    ]
}

# ==========================================
# STATIC LESSON CONTENT (No AI Cost)
# ==========================================
LESSON_CONTENT = {
    # --- BEGINNER ---
    "Introduction to Foraging": {
        "text": """
## Welcome to Foraging! 🌿

**What is Foraging?**
Foraging is the act of finding and gathering wild food. It is the oldest human skill, but today we do it for fun, health, and connection to nature.

**The Golden Rule:** 
> *If in doubt, leave it out.* 
Never eat anything unless you are 100% sure what it is.

### The Safety Toolkit 🎒
1. **A Good Guide Book:** Pictures are never as good as a real book.
2. **Scissors/Knife:** To cut stems cleanly.
3. **Basket/Bag:** Never use plastic bags (plants sweat and go slimy).
4. **Gloves:** Essential for Nettles or suspicious plants.
5. **Phone:** For emergencies.

### The Conservation Code 🌍
We never take more than we need.
- **The 10% Rule:** Never pick more than 10% of a patch. Leave 90% for wildlife and for the plant to reproduce.
- **The 1 in 3 Rule:** Only pick from areas where there are at least 3 plants. If you only see one, leave it alone.
        """,
        "quiz": {
            "question": "How much of a plant patch should you leave for wildlife?",
            "options": ["10%", "50%", "90%", "All of it"],
            "answer": "90%"
        }
    },
    "Easy Plants to Identify": {
        "text": """
## The 'Big 4' for Beginners 🌼

These are the best plants to start with because they have clear identifying features and no deadly lookalikes.

### 1. Dandelion 🦁
- **Where:** Lawns, fields, path edges.
- **ID:** Yellow flower, hollow stem with white milky sap, 'Lion's Tooth' leaves (jagged edges).
- **Eat:** Leaves (bitter, good in salad), Flowers (wine/fritters), Roots (coffee).
- **Warning:** Avoid dog walking areas!

### 2. Nettle 🌿
- **Where:** Hedges, woods, gardens.
- **ID:** Jagged leaves, stinging hairs (ouch!).
- **Eat:** Young leaves (cooked like spinach). **Must be cooked** to remove sting.
- **Uses:** Soup, tea, pesto. High in iron!

### 3. Blackberry (Bramble) 🖤
- **Where:** Hedges, woods.
- **ID:** Thorns, 5-leaflet leaves, berries turn from red to black.
- **Eat:** Berries (raw, crumble, jam).
- **Warning:** Wear long sleeves to avoid scratches.

### 4. Wild Garlic (Ramsons) 🧄
- **Where:** Damp woodlands, near streams. Spring only.
- **ID:** Broad green leaves, smells strongly of garlic when crushed.
- **Warning:** Do not pick Lily of the Valley (no smell, poisonous).
        """,
        "quiz": {
            "question": "Why must Nettles be cooked before eating?",
            "options": ["They taste better", "They are poisonous raw", "To remove the sting", "They are too crunchy"],
            "answer": "To remove the sting"
        }
    },
    "Foraging Ethics": {
        "text": """
## Respecting the Land 🌍

Foraging is a privilege, not a right. We must respect nature so it stays for future generations.

### The Forager's Promise
1. **Leave No Trace:** If you brought a wrapper, take it home.
2. **Do Not Up-root:** Never pull a whole plant out of the ground. It kills the plant.
3. **Respect Wildlife:** Berries feed birds in winter; leave plenty for them.

### The Law (Quick Look)
- **Picking for Personal Use:** Usually allowed on public land.
- **Uprooting:** Illegal without permission.
- **Commercial Sale:** Illegal without landowner permission.

### Safety & Hygiene
- **Dog Waste:** Avoid areas near paths where dogs walk.
- **Roadside:** Avoid busy roads (pollution).
- **Spraying:** Check if fields have been sprayed with chemicals.
        """,
        "quiz": {
            "question": "Is it legal to pull a whole plant (uproot) from public land?",
            "options": ["Yes, if I only take one", "No, it is illegal without permission", "Only if it is a weed"],
            "answer": "No, it is illegal without permission"
        }
    },
    
    # --- INTERMEDIATE ---
    "Seasonal Foraging": {
        "text": """
## The Seasonal Calendar 🗓️

Nature has a menu that changes every month.

### 🌸 Spring (March - May)
*The Time of Greens.*
- **Wild Garlic:** Look for white flowers and that smell!
- **Nettles:** Pick the top 4-6 leaves (tips).
- **Dandelion:** Young leaves are less bitter now.
- **Elderflower:** Blossoms for cordial (June).

### ☀️ Summer (June - August)
*The Time of Flowers & Fruits.*
- **Elderflower:** (June/July) Cordial, fritters.
- **Wild Strawberry:** Tiny but tasty.
- **Cherries:** Look for trees in parks.
- **Meadowsweet:** Almond smell, good for tea.

### 🍂 Autumn (September - November)
*The Time of Nuts & Roots.*
- **Blackberries:** The classic foraging fruit.
- **Hazelnuts:** Look for squirrel signs (shells on ground).
- **Rosehips:** High Vitamin C.
- **Sweet Chestnuts:** Roasting material.
- **Sloes:** Gin ingredient (frost makes them sweeter).

### ❄️ Winter (December - February)
*The Time of Resilience.*
- **Pine Needles:** Tea (Vitamin C).
- **Rosehips:** Still available.
- **Winter Chanterelle:** Only for experts.
        """,
        "quiz": {
            "question": "Which season is best for picking Wild Garlic?",
            "options": ["Summer", "Autumn", "Spring", "Winter"],
            "answer": "Spring"
        }
    },
    "Coastal Foraging": {
        "text": """
## The Seashore Larder 🏖️

The coast offers unique foods, but you must check water quality and laws.

### Common Finds
1. **Samphire (Marsh Samphire):** 
   - 'Sea asparagus'. Green, juicy stems.
   - **Habitat:** Mudflats, estuaries.
   - **Eat:** Steam with butter. Salty!

2. **Sea Kale:**
   - Blueish leaves, white flowers.
   - **Warning:** Protected in some areas. Pick sparingly.

3. **Sea Spinach:**
   - Fleshy leaves, grows on shingle.

### Seaweeds 🌊
- **Laver (Sloke):** Purple/black sheets. Wash thoroughly! Used for Laverbread (Welsh).
- **Sugar Kelp:** Long, ribbon-like. Sweet taste.

### Rules 📜
- Check **Local Byelaws**: Some beaches ban picking.
- **Water Quality:** Do not pick near sewage outlets or harbours.
- **Clean:** Wash everything thoroughly to remove sand and salt.
        """,
        "quiz": {
            "question": "What should you do before eating Seaweeds like Laver?",
            "options": ["Eat raw", "Cook immediately", "Wash thoroughly to remove sand/salt", "Nothing"],
            "answer": "Wash thoroughly to remove sand/salt"
        }
    },
    "The Carrot Family": {
        "text": """
## The Umbellifer Challenge 🥕

The Carrot family (Apiaceae) has delicious foods and **deadly poisons**. You must learn to tell them apart.

### The Good (Edible)
- **Wild Carrot:** Hairy stem, smells of carrot.
- **Cow Parsley:** Rough hairy stem, smells parsley.
- **Alexanders:** Yellow-green flowers, celery smell (Coastal).

### The Bad (Dangerous)
- **Hemlock (DEADLY):** Smooth purple-spotted stem. Smells of mouse urine.
- **Hemlock Water Dropwort (DEADLY):** Grows in water. Tubers look like fingers. Deadliest in UK.
- **Fool's Parsley:** Smells 'hot' or metallic.

### ID Tips for Beginners
1. **Smell:** Does it smell like food (carrot/parsley/celery)? If it smells musty/mousy, leave it.
2. **Stem:** Hairy stems are usually safer in this family. Smooth/Purple spotted = Danger.
3. **Habitat:** Hemlock loves damp ditches.

> **Rule:** If you are not 100% sure, do not eat white umbrellas!
        """,
        "quiz": {
            "question": "What does Hemlock smell like?",
            "options": ["Carrot", "Parsley", "Mouse urine", "Garlic"],
            "answer": "Mouse urine"
        }
    },

    # --- ADVANCED ---
    "Mushroom Foraging": {
        "text": """
## Fungi: The Advanced Class 🍄

**Warning:** Mushroom foraging requires expert knowledge. One mistake can be fatal.

### The Golden Rules
1. **Never eat a mushroom unless 100% sure.**
2. **Cut, don't pull:** Use a knife to cut the stem. This leaves the 'roots' (mycelium) for next year.
3. **Spore Prints:** Sometimes you need to leave a cap on paper overnight to see the colour of the spores.

### The Deadly Duo to Avoid ☠️
1. **Death Cap (Amanita phalloides):**
   - Green-yellow cap.
   - White gills.
   - Volva (cup) at base (often underground).
   - Responsible for most mushroom deaths.

2. **Destroying Angel:** White all over.

### Good Beginners
- **Chanterelle:** Egg yolk yellow, false gills (ridges), smells of apricots.
- **Puffball:** Must be pure white inside. If purple/yellow inside, it is old.
- **Field Mushroom:** Pink gills turning brown. Avoid yellow stainers.
        """,
        "quiz": {
            "question": "If a mushroom has a 'volva' (cup) at the base, what should you do?",
            "options": ["Eat it", "Cut it open", "Leave it (High Poison Risk)", "Smell it"],
            "answer": "Leave it (High Poison Risk)"
        }
    },
    "The Umbellifer Challenge": {
        "text": """
## Mastering the Carrot Family 🥕

This module is for advanced students who want to master the ID of white flowers.

### Anatomy of an Umbellifer
- **Umbel:** The umbrella shape of the flowers.
- **Bracts:** The tiny leaves under the flower. **Key ID feature.**
- **Stem:** Check for spots, hairs, or ridges.

### The 'Hemlock' Checklist
If you see a tall white flower:
1. **Check the Stem:** Purple spots? Smooth? -> **HEMLOCK (POISON).**
2. **Check the Smell:** Mouse wee? -> **HEMLOCK.**
3. **Check the Root:** Does it have tubers like fingers? -> **HEMLOCK WATER DROPWORT (POISON).**

### The 'Safe' Checklist
1. **Hairy Stem:** Usually Cow Parsley or Wild Carrot.
2. **Smell:** Carrot, Parsley, Celery = Safe.
3. **Root:** Carrot smell = Wild Carrot (Edible, but illegal to uproot).

> **Final Word:** Do not uproot roots without permission. It is illegal and kills the plant.
        """,
        "quiz": {
            "question": "What feature usually indicates a SAFE member of the Carrot family?",
            "options": ["Purple spots", "Smooth stem", "Hairy stem", "Mouse smell"],
            "answer": "Hairy stem"
        }
    },

    # --- LAW & LAND ---
    "The Law of the Land": {
        "text": """
## Foraging and the Law ⚖️

Knowing the law protects you and nature.

### The Theft Act 1968
- **Wild Plants:** You can pick flowers, fruit, and foliage for **personal use**.
- **Uprooting:** It is illegal to dig up any wild plant without the landowner's permission.
- **Commercial:** You cannot sell what you pick without permission.

### The Countryside Act 1981
- **Protected Species:** It is a crime to pick, uproot, or destroy any plant listed under this Act (e.g., rare orchids).
- **SSSIs:** Sites of Special Scientific Interest have strict rules. Do not pick anything inside them.

### The 'Four Fs'
You can legally pick:
- **F**ruit
- **F**oliage
- **F**lowers
- **F**ungi
...for personal consumption, provided it is not a protected site or species.

### Key Takeaway
> If you are on a public footpath, you can pick blackberries. You cannot dig up roots. If you see a rare orchid, look but don't touch!
        """,
        "quiz": {
            "question": "Is it legal to dig up a Wild Carrot root from a public field?",
            "options": ["Yes, if I eat it", "Yes, if it is for dinner", "No, uprooting is illegal without permission"],
            "answer": "No, uprooting is illegal without permission"
        }
    },
    "Access Rights": {
        "text": """
## Where Can I Walk? 🚶‍♀️

Access rights vary across the UK.

### England & Wales
- **Public Rights of Way:** You can walk on footpaths, bridleways, and byways.
- **Access Land:** Some areas (mountains, moors, heaths) have 'Right to Roam'.
- **Private Land:** You need permission. Trespass is a civil offense.

### Scotland 🏴󠁧󠁢󠁳󠁣󠁴󠁿
- **Right to Roam:** Much more open. You can walk on most land (hills, forests, coast) provided you act responsibly.
- **Restrictions:** Do not disturb crops, livestock, or houses.

### The Forager's Code
1. **Ask Permission:** If you see a private wood with mushrooms, find the owner and ask.
2. **Be Discreet:** Do not strip an area.
3. **Respect Farmers:** Close gates. Do not scare sheep.

### Summary
- **Roadside Verges:** Often council land. Safe to pick, but wash well (spray/runoff).
- **Nature Reserves:** Often No Picking. Check signs.
        """,
        "quiz": {
            "question": "Which country has the most open 'Right to Roam' laws?",
            "options": ["England", "Wales", "Scotland", "Northern Ireland"],
            "answer": "Scotland"
        }
    }
}

# ==========================================
# SESSION STATE INIT
# ==========================================
def init_session_state():
    defaults = {
        'game_score': 0, 'game_lives': 3, 'game_streak': 0, 'current_question': None,
        'village': None, 'farm_game': None, 'survival_lives': 3, 'survival_score': 0,
        'current_survival_pair': None, 'quiz_score': 0, 'quiz_q_num': 0, 'quiz_max': 5,
        'q_data': None, 'chat_language': 'English', 'messages': [], 'selected_page': "Home",
        'book_content': {}, 'book_outline': "", 'active_season': "Summer",
        'season_badge_progress': [], 'survival_correct_count': 0, 'survival_current_case': None,
        'survival_result': None, 'daily_streak': 0, 'quiz_active': False, 'module_questions': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Helper for AI generation
def generate_text(prompt):
    if client is None:
        return "⚠️ AI Content Unavailable (API Key missing)."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating text: {e}"

# Helper for Audio
def generate_voice(text, filename="temp_audio.mp3"):
    if not EDGE_TTS_AVAILABLE:
        return None
    try:
        communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicate.save(filename))
        loop.close()
        return filename
    except Exception as e:
        print(f"Audio Error: {e}")
        return None

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("🌿 Rocen Homesteady")
st.sidebar.markdown("**Educational Foraging Tools**")
st.sidebar.markdown("---")
st.sidebar.warning("⚠️ **Safety First**")
st.sidebar.markdown("""
- Never eat a plant based solely on app ID.
- Always cross-reference with a field guide.
- **UK Law:** Only pick for personal use.
- It is illegal to uproot plants without permission.
""")

# ==========================================
# MAIN TABS
# ==========================================
main_tab1, main_tab2 = st.tabs(["📖 Learning", "🎮 Games"])

# ==========================================
# TAB 1: LEARNING
# ==========================================
with main_tab1:
    st.header("📖 UK Foraging Guide")
    st.info("**Disclaimer:** This guide is for educational purposes. Always consult a local expert before consuming wild plants.")

    # Create Sub-tabs for Learning
    learn_tab1, learn_tab2 = st.tabs(["🌱 Plant Guide", "🎓 Learning Modules"])

    # --- SUB-TAB 1: PLANT GUIDE ---
    with learn_tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search Plant")
        with col2:
            filter_type = st.selectbox("Type", ["All", "Edible Only", "Poisonous Only"])
        with col3:
            region_filter = st.selectbox("Region", ["All", "England", "Scotland", "Wales", "N. Ireland"])

        st.markdown("---")

        plants = []
        if filter_type == "Edible Only":
            plants = [("Edible", p) for p in UK_PLANTS["edible"]]
        elif filter_type == "Poisonous Only":
            plants = [("Poisonous", p) for p in UK_PLANTS["poisonous"]]
        else:
            plants = [("Edible", p) for p in UK_PLANTS["edible"]] + [("Poisonous", p) for p in UK_PLANTS["poisonous"]]

        for status, plant in plants:
            if search_term and search_term.lower() not in plant['name'].lower():
                continue

            # Safety Check for parts
            parts_text = plant.get('parts', 'Various')
            if isinstance(parts_text, list): parts_text = ", ".join(parts_text)

            # Determine Icon
            icon = "🌿" if status == "Edible" else "☠️"
            
            with st.expander(f"{icon} {plant['name']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Habitat:** {plant.get('habitat', 'Various')}")
                    st.markdown(f"**Months:** {', '.join(plant.get('months', []))}")
                with c2:
                    if status == "Edible":
                        st.markdown(f"**Parts:** {parts_text}")
                        st.markdown(f"**Difficulty:** {'🌱' * plant.get('difficulty', 1)}")
                    else:
                        st.markdown(f"**Danger:** {plant.get('danger', 'Unknown')}")

                # Improved Description Display
                desc = plant.get('description', 'No info available.')
                st.markdown(desc)

                # Visual Warning Boxes (KS2 Friendly)
                if status == "Edible":
                    warning_text = plant.get('warnings', '')
                    # Highlight legal warnings
                    if "Uproot" in warning_text or "Root" in plant.get('parts', ''):
                         st.warning(f"⚠️ **Legal Warning:** It is illegal to dig up roots without landowner permission.")
                    
                    # Highlight Lookalikes
                    lookalikes = plant.get('lookalikes', [])
                    if lookalikes:
                        st.error(f"👀 **Watch out for Lookalikes:** {', '.join(lookalikes)}")
                        
                else: # Poisonous
                    st.error(f"☠️ **Toxicity:** {plant.get('symptoms', 'Unknown')}")
                    st.warning(f"🔍 **Confused with:** {', '.join(plant.get('lookalikes', []))}")

                # Accessibility: Read Aloud Button
                if EDGE_TTS_AVAILABLE:
                    if st.button(f"🔊 Read Aloud", key=f"read_{plant['name']}"):
                        with st.spinner("Generating audio..."):
                            text_to_read = f"{plant['name']}. {plant.get('description', '')}"
                            audio_file = generate_voice(text_to_read)
                            if audio_file:
                                st.audio(audio_file)
                else:
                    st.caption("Audio disabled (library missing).")

    # --- SUB-TAB 2: LEARNING MODULES ---
    with learn_tab2:
        st.header("🎓 Learning Modules")
        st.markdown("### Structured learning paths for UK foraging")

        # ==========================================
        # STATIC LESSON CONTENT (No AI Cost)
        # ==========================================
        LESSON_CONTENT = {
            # --- BEGINNER ---
            "Introduction to Foraging": {
                "text": """
## Welcome to Foraging! 🌿

**What is Foraging?**
Foraging is the act of finding and gathering wild food. It is the oldest human skill, but today we do it for fun, health, and connection to nature.

**The Golden Rule:** 
> *If in doubt, leave it out.* 
Never eat anything unless you are 100% sure what it is.

### The Safety Toolkit 🎒
1. **A Good Guide Book:** Pictures are never as good as a real book.
2. **Scissors/Knife:** To cut stems cleanly.
3. **Basket/Bag:** Never use plastic bags (plants sweat and go slimy).
4. **Gloves:** Essential for Nettles or suspicious plants.
5. **Phone:** For emergencies.

### The Conservation Code 🌍
We never take more than we need.
- **The 10% Rule:** Never pick more than 10% of a patch. Leave 90% for wildlife and for the plant to reproduce.
- **The 1 in 3 Rule:** Only pick from areas where there are at least 3 plants. If you only see one, leave it alone.
                """,
                "quiz": {
                    "question": "How much of a plant patch should you leave for wildlife?",
                    "options": ["10%", "50%", "90%", "All of it"],
                    "answer": "90%"
                }
            },
            "Easy Plants to Identify": {
                "text": """
## The 'Big 4' for Beginners 🌼

These are the best plants to start with because they have clear identifying features and no deadly lookalikes.

### 1. Dandelion 🦁
- **Where:** Lawns, fields, path edges.
- **ID:** Yellow flower, hollow stem with white milky sap, 'Lion's Tooth' leaves (jagged edges).
- **Eat:** Leaves (bitter, good in salad), Flowers (wine/fritters), Roots (coffee).
- **Warning:** Avoid dog walking areas!

### 2. Nettle 🌿
- **Where:** Hedges, woods, gardens.
- **ID:** Jagged leaves, stinging hairs (ouch!).
- **Eat:** Young leaves (cooked like spinach). **Must be cooked** to remove sting.
- **Uses:** Soup, tea, pesto. High in iron!

### 3. Blackberry (Bramble) 🖤
- **Where:** Hedges, woods.
- **ID:** Thorns, 5-leaflet leaves, berries turn from red to black.
- **Eat:** Berries (raw, crumble, jam).
- **Warning:** Wear long sleeves to avoid scratches.

### 4. Wild Garlic (Ramsons) 🧄
- **Where:** Damp woodlands, near streams. Spring only.
- **ID:** Broad green leaves, smells strongly of garlic when crushed.
- **Warning:** Do not pick Lily of the Valley (no smell, poisonous).
                """,
                "quiz": {
                    "question": "Why must Nettles be cooked before eating?",
                    "options": ["They taste better", "They are poisonous raw", "To remove the sting", "They are too crunchy"],
                    "answer": "To remove the sting"
                }
            },
            "Foraging Ethics": {
                "text": """
## Respecting the Land 🌍

Foraging is a privilege, not a right. We must respect nature so it stays for future generations.

### The Forager's Promise
1. **Leave No Trace:** If you brought a wrapper, take it home.
2. **Do Not Up-root:** Never pull a whole plant out of the ground. It kills the plant.
3. **Respect Wildlife:** Berries feed birds in winter; leave plenty for them.

### The Law (Quick Look)
- **Picking for Personal Use:** Usually allowed on public land.
- **Uprooting:** Illegal without permission.
- **Commercial Sale:** Illegal without landowner permission.

### Safety & Hygiene
- **Dog Waste:** Avoid areas near paths where dogs walk.
- **Roadside:** Avoid busy roads (pollution).
- **Spraying:** Check if fields have been sprayed with chemicals.
                """,
                "quiz": {
                    "question": "Is it legal to pull a whole plant (uproot) from public land?",
                    "options": ["Yes, if I only take one", "No, it is illegal without permission", "Only if it is a weed"],
                    "answer": "No, it is illegal without permission"
                }
            },
            
            # --- INTERMEDIATE ---
            "Seasonal Foraging": {
                "text": """
## The Seasonal Calendar 🗓️

Nature has a menu that changes every month.

### 🌸 Spring (March - May)
*The Time of Greens.*
- **Wild Garlic:** Look for white flowers and that smell!
- **Nettles:** Pick the top 4-6 leaves (tips).
- **Dandelion:** Young leaves are less bitter now.
- **Elderflower:** Blossoms for cordial (June).

### ☀️ Summer (June - August)
*The Time of Flowers & Fruits.*
- **Elderflower:** (June/July) Cordial, fritters.
- **Wild Strawberry:** Tiny but tasty.
- **Cherries:** Look for trees in parks.
- **Meadowsweet:** Almond smell, good for tea.

### 🍂 Autumn (September - November)
*The Time of Nuts & Roots.*
- **Blackberries:** The classic foraging fruit.
- **Hazelnuts:** Look for squirrel signs (shells on ground).
- **Rosehips:** High Vitamin C.
- **Sweet Chestnuts:** Roasting material.
- **Sloes:** Gin ingredient (frost makes them sweeter).

### ❄️ Winter (December - February)
*The Time of Resilience.*
- **Pine Needles:** Tea (Vitamin C).
- **Rosehips:** Still available.
- **Winter Chanterelle:** Only for experts.
                """,
                "quiz": {
                    "question": "Which season is best for picking Wild Garlic?",
                    "options": ["Summer", "Autumn", "Spring", "Winter"],
                    "answer": "Spring"
                }
            },
            "Coastal Foraging": {
                "text": """
## The Seashore Larder 🏖️

The coast offers unique foods, but you must check water quality and laws.

### Common Finds
1. **Samphire (Marsh Samphire):** 
   - 'Sea asparagus'. Green, juicy stems.
   - **Habitat:** Mudflats, estuaries.
   - **Eat:** Steam with butter. Salty!

2. **Sea Kale:**
   - Blueish leaves, white flowers.
   - **Warning:** Protected in some areas. Pick sparingly.

3. **Sea Spinach:**
   - Fleshy leaves, grows on shingle.

### Seaweeds 🌊
- **Laver (Sloke):** Purple/black sheets. Wash thoroughly! Used for Laverbread (Welsh).
- **Sugar Kelp:** Long, ribbon-like. Sweet taste.

### Rules 📜
- Check **Local Byelaws**: Some beaches ban picking.
- **Water Quality:** Do not pick near sewage outlets or harbours.
- **Clean:** Wash everything thoroughly to remove sand and salt.
                """,
                "quiz": {
                    "question": "What should you do before eating Seaweeds like Laver?",
                    "options": ["Eat raw", "Cook immediately", "Wash thoroughly to remove sand/salt", "Nothing"],
                    "answer": "Wash thoroughly to remove sand/salt"
                }
            },
            "The Carrot Family": {
                "text": """
## The Umbellifer Challenge 🥕

The Carrot family (Apiaceae) has delicious foods and **deadly poisons**. You must learn to tell them apart.

### The Good (Edible)
- **Wild Carrot:** Hairy stem, smells of carrot.
- **Cow Parsley:** Rough hairy stem, smells parsley.
- **Alexanders:** Yellow-green flowers, celery smell (Coastal).

### The Bad (Dangerous)
- **Hemlock (DEADLY):** Smooth purple-spotted stem. Smells of mouse urine.
- **Hemlock Water Dropwort (DEADLY):** Grows in water. Tubers look like fingers. Deadliest in UK.
- **Fool's Parsley:** Smells 'hot' or metallic.

### ID Tips for Beginners
1. **Smell:** Does it smell like food (carrot/parsley/celery)? If it smells musty/mousy, leave it.
2. **Stem:** Hairy stems are usually safer in this family. Smooth/Purple spotted = Danger.
3. **Habitat:** Hemlock loves damp ditches.

> **Rule:** If you are not 100% sure, do not eat white umbrellas!
                """,
                "quiz": {
                    "question": "What does Hemlock smell like?",
                    "options": ["Carrot", "Parsley", "Mouse urine", "Garlic"],
                    "answer": "Mouse urine"
                }
            },

            # --- ADVANCED ---
            "Mushroom Foraging": {
                "text": """
## Fungi: The Advanced Class 🍄

**Warning:** Mushroom foraging requires expert knowledge. One mistake can be fatal.

### The Golden Rules
1. **Never eat a mushroom unless 100% sure.**
2. **Cut, don't pull:** Use a knife to cut the stem. This leaves the 'roots' (mycelium) for next year.
3. **Spore Prints:** Sometimes you need to leave a cap on paper overnight to see the colour of the spores.

### The Deadly Duo to Avoid ☠️
1. **Death Cap (Amanita phalloides):**
   - Green-yellow cap.
   - White gills.
   - Volva (cup) at base (often underground).
   - Responsible for most mushroom deaths.

2. **Destroying Angel:** White all over.

### Good Beginners
- **Chanterelle:** Egg yolk yellow, false gills (ridges), smells of apricots.
- **Puffball:** Must be pure white inside. If purple/yellow inside, it is old.
- **Field mushroom:** Pink gills turning brown. Avoid yellow stainers.
                """,
                "quiz": {
                    "question": "If a mushroom has a 'volva' (cup) at the base, what should you do?",
                    "options": ["Eat it", "Cut it open", "Leave it (High Poison Risk)", "Smell it"],
                    "answer": "Leave it (High Poison Risk)"
                }
            },
            "The Umbellifer Challenge": {
                "text": """
## Mastering the Carrot Family 🥕

This module is for advanced students who want to master the ID of white flowers.

### Anatomy of an Umbellifer
- **Umbel:** The umbrella shape of the flowers.
- **Bracts:** The tiny leaves under the flower. **Key ID feature.**
- **Stem:** Check for spots, hairs, or ridges.

### The 'Hemlock' Checklist
If you see a tall white flower:
1. **Check the Stem:** Purple spots? Smooth? -> **HEMLOCK (POISON).**
2. **Check the Smell:** Mouse wee? -> **HEMLOCK.**
3. **Check the Root:** Does it have tubers like fingers? -> **HEMLOCK WATER DROPWORT (POISON).**

### The 'Safe' Checklist
1. **Hairy Stem:** Usually Cow Parsley or Wild Carrot.
2. **Smell:** Carrot, Parsley, Celery = Safe.
3. **Root:** Carrot smell = Wild Carrot (Edible, but illegal to uproot).

> **Final Word:** Do not uproot roots without permission. It is illegal and kills the plant.
                """,
                "quiz": {
                    "question": "What feature usually indicates a SAFE member of the Carrot family?",
                    "options": ["Purple spots", "Smooth stem", "Hairy stem", "Mouse smell"],
                    "answer": "Hairy stem"
                }
            },

            # --- LAW & LAND ---
            "The Law of the Land": {
                "text": """
## Foraging and the Law ⚖️

Knowing the law protects you and nature.

### The Theft Act 1968
- **Wild Plants:** You can pick flowers, fruit, and foliage for **personal use**.
- **Uprooting:** It is illegal to dig up any wild plant without the landowner's permission.
- **Commercial:** You cannot sell what you pick without permission.

### The Countryside Act 1981
- **Protected Species:** It is a crime to pick, uproot, or destroy any plant listed under this Act (e.g., rare orchids).
- **SSSIs:** Sites of Special Scientific Interest have strict rules. Do not pick anything inside them.

### The 'Four Fs'
You can legally pick:
- **F**ruit
- **F**oliage
- **F**lowers
- **F**ungi
...for personal consumption, provided it is not a protected site or species.

### Key Takeaway
> If you are on a public footpath, you can pick blackberries. You cannot dig up roots. If you see a rare orchid, look but don't touch!
                """,
                "quiz": {
                    "question": "Is it legal to dig up a Wild Carrot root from a public field?",
                    "options": ["Yes, if I eat it", "Yes, if it is for dinner", "No, uprooting is illegal without permission"],
                    "answer": "No, uprooting is illegal without permission"
                }
            },
            "Access Rights": {
                "text": """
## Where Can I Walk? 🚶‍♀️

Access rights vary across the UK.

### England & Wales
- **Public Rights of Way:** You can walk on footpaths, bridleways, and byways.
- **Access Land:** Some areas (mountains, moors, heaths) have 'Right to Roam'.
- **Private Land:** You need permission. Trespass is a civil offense.

### Scotland 🏴󠁧󠁢󠁳󠁣󠁴󠁿
- **Right to Roam:** Much more open. You can walk on most land (hills, forests, coast) provided you act responsibly.
- **Restrictions:** Do not disturb crops, livestock, or houses.

### The Forager's Code
1. **Ask Permission:** If you see a private wood with mushrooms, find the owner and ask.
2. **Be Discreet:** Do not strip an area.
3. **Respect Farmers:** Close gates. Do not scare sheep.

### Summary
- **Roadside Verges:** Often council land. Safe to pick, but wash well (spray/runoff).
- **Nature Reserves:** Often No Picking. Check signs.
                """,
                "quiz": {
                    "question": "Which country has the most open 'Right to Roam' laws?",
                    "options": ["England", "Wales", "Scotland", "Northern Ireland"],
                    "answer": "Scotland"
                }
            }
        }

        # ==========================================
        # DISPLAY LOGIC
        # ==========================================
        modules = {
            "🌱 Beginner": ["Introduction to Foraging", "Easy Plants to Identify", "Foraging Ethics"],
            "🌿 Intermediate": ["Seasonal Foraging", "Coastal Foraging", "The Carrot Family"],
            "🌲 Advanced": ["Mushroom Foraging", "The Umbellifer Challenge"],
            "⚖️ UK Law & Land": ["The Law of the Land", "Access Rights"]
        }

        for level, module_list in modules.items():
            st.markdown(f"### {level}")
            for title in module_list:
                # Check if we have content for this module
                if title in LESSON_CONTENT:
                    data = LESSON_CONTENT[title]
                    
                    with st.expander(f"📚 {title} ({data['quiz']['question'][:20]}...)"): # Simple preview
                        # 1. Start Module Button
                        if st.button(f"Start Module: {title}", key=f"start_{title}"):
                            st.session_state['active_module'] = title
                            st.session_state['quiz_answered'] = False
                            st.rerun()

                        # 2. Display Lesson Content
                        if st.session_state.get('active_module') == title:
                            st.markdown("---")
                            st.markdown(data['text'])

                            # 3. Audio Button
                            if EDGE_TTS_AVAILABLE:
                                if st.button("🔊 Read Aloud", key=f"audio_{title}"):
                                    with st.spinner("Generating audio..."):
                                        audio_file = generate_voice(data['text'])
                                        if audio_file:
                                            st.audio(audio_file)
                            
                            st.markdown("---")
                            
                            # 4. Quiz Section
                            st.markdown("### 📝 Quiz")
                            q = data['quiz']
                            
                            # Display radio buttons
                            user_ans = st.radio(q['question'], q['options'], key=f"radio_{title}")
                            
                            # Submit Button
                            if st.button("Submit Answer", key=f"submit_{title}"):
                                if user_ans == q['answer']:
                                    st.success("✅ Correct! You have completed this module.")
                                    st.balloons()
                                    st.session_state['quiz_answered'] = True
                                else:
                                    st.error(f"❌ Incorrect. The correct answer was: {q['answer']}. Please review the lesson.")
                                    # Don't reset session state, let them try again or restart

                            # 5. Certificate Logic (Only shows after correct answer)
                            if st.session_state.get('quiz_answered'):
                                st.markdown("### 🏆 Claim your Certificate")
                                cert_name = st.text_input("Enter your name for the certificate:", key=f"name_{title}")
                                if st.button("Download Certificate", key=f"cert_{title}"):
                                    if cert_name:
                                        cert_text = f"""
CERTIFICATE OF COMPLETION
------------------------
Student: {cert_name}
Module: {title}
Date: {datetime.now().strftime("%Y-%m-%d")}
Platform: Rocen Homesteady
Status: PASSED
                                        """
                                        st.download_button("📥 Download Certificate (.txt)", cert_text, file_name=f"certificate_{title.replace(' ', '_')}.txt")
                                    else:
                                        st.warning("Please enter your name.")
                else:
                    # Fallback if content is missing from dictionary
                    st.warning(f"Content for '{title}' coming soon.")

# ==========================================
# TAB 2: GAMES
# ==========================================
with main_tab2:
    # Create Game Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌿 Foraging Quest",
        "☠️ Survival School",
        "🎲 Daily Quiz",
        "🏘️ Eco-Village",
        "🚜 Farm Tycoon"
    ])

    # ==========================================
    # GAME TAB 1: FORAGING QUEST
    # ==========================================
    with tab1:
        st.header("🌿 The Seasonal Quest")
        st.caption("📚 Curriculum Link: Science (Seasonal Changes, Plants)")

        # Instructions
        with st.expander("📖 How to Play"):
            st.markdown("""
            1. **Select a Season** using the buttons at the top.
            2. A plant will appear. Read its name.
            3. Choose the **Habitat** where it grows (e.g., Woodland, Coastal).
            4. Get it right to build a **Streak** for bonus points!
            5. Collect badges for all 4 seasons.
            """)

        habitat_icons = {"Woodland": "🌲", "Hedgerow": "🌿", "Coastal": "🏖️", "Urban": "🏡", "Meadow": "🌾"}
        if 'season_badge_progress' not in st.session_state: st.session_state.season_badge_progress = []

        st.markdown("### 🗓️ Choose a Season")
        season_cols = st.columns(4)
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        season_icons = {"Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"}

        current_month = datetime.now().strftime("%B")
        default_season = "Summer"
        if current_month in ["March", "April", "May"]: default_season = "Spring"
        elif current_month in ["June", "July", "August"]: default_season = "Summer"
        elif current_month in ["September", "October", "November"]: default_season = "Autumn"
        else: default_season = "Winter"

        if 'active_season' not in st.session_state: st.session_state.active_season = default_season

        for i, s in enumerate(seasons):
            is_earned = s in st.session_state.season_badge_progress
            badge_txt = "🏅" if is_earned else ""
            if season_cols[i].button(f"{season_icons[s]} {s} {badge_txt}", key=f"season_{s}", use_container_width=True):
                st.session_state.active_season = s
                st.session_state.current_question = None
                st.rerun()

        st.info(f"**Current Season:** {st.session_state.active_season} {season_icons[st.session_state.active_season]}")

        col1, col2, col3 = st.columns(3)
        col1.metric("🌟 Score", st.session_state.game_score)
        col2.metric("❤️ Lives", "❤️" * max(0, st.session_state.game_lives))
        col3.metric("🏅 Badge", f"{len(st.session_state.season_badge_progress)}/4")
        st.markdown("---")

        active_season = st.session_state.active_season
        season_months = {"Spring": ["March", "April", "May"], "Summer": ["June", "July", "August"], "Autumn": ["September", "October", "November"], "Winter": ["December", "January", "February"]}

        available_plants = [p for p in UK_PLANTS["edible"] if any(m in season_months[active_season] for m in p.get("months", []))]

        if not available_plants:
            st.warning(f"Not much grows in {active_season}! Try another season.")
        else:
            if st.session_state.get('current_question') is None:
                plant = random.choice(available_plants)
                
                # --- FIX: Standardize Habitat Names ---
                raw_habitat = plant['habitat'].split(',')[0].strip()
                
                # Map variations to the standard 5 buttons
                if raw_habitat in ["Woodlands", "Woods", "Wood"]: 
                    correct_habitat = "Woodland"
                elif raw_habitat in ["Hedgerows", "Hedgerow", "Roadsides"]: 
                    correct_habitat = "Hedgerow"
                elif raw_habitat in ["Meadows", "Grassland", "Fields", "Fields, Gardens"]: 
                    correct_habitat = "Meadow"
                elif raw_habitat in ["Coastal", "Coastal Shingle"]: 
                    correct_habitat = "Coastal"
                elif raw_habitat in ["Gardens", "Urban", "Everywhere", "Waste Ground"]: 
                    correct_habitat = "Urban"
                else:
                    # Fallback if something unexpected comes up
                    correct_habitat = "Woodland" 

                all_habitats = ["Woodland", "Coastal", "Hedgerow", "Urban", "Meadow"]
                wrong_habitats = [h for h in all_habitats if h != correct_habitat]
                options = [correct_habitat] + random.sample(wrong_habitats, min(3, len(wrong_habitats)))
                random.shuffle(options)
                st.session_state.current_question = {"plant": plant, "correct": correct_habitat, "options": options}

            q = st.session_state.current_question

            st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>🌿</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>You found a <b>{q['plant']['name']}</b>!</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: gray;'>It is {active_season}. Where should you look for it?</p>", unsafe_allow_html=True)

            btn_cols = st.columns(2)
            for i, option in enumerate(q['options']):
                col = btn_cols[i % 2]
                icon = habitat_icons.get(option, "❓")
                if col.button(f"{icon} {option}", key=f"opt_{i}", use_container_width=True):
                    if option == q['correct']:
                        st.session_state.game_score += 10 + (st.session_state.game_streak * 2)
                        st.session_state.game_streak += 1
                        st.balloons()
                        warning = q['plant'].get('warnings', 'Always double check identification.')
                        st.info(f"💡 **Did you know?** {warning}")
                        if active_season not in st.session_state.season_badge_progress:
                            st.session_state.season_badge_progress.append(active_season)
                            st.toast(f"🏅 You explored {active_season}!")
                        st.success(f"✅ Correct! {q['plant']['name']} loves the {option}!")
                    else:
                        st.session_state.game_lives -= 1
                        st.session_state.game_streak = 0
                        st.error(f"❌ Not quite! It actually prefers {q['correct']}.")
                    st.session_state.current_question = None
                    time.sleep(1)
                    st.rerun()

        if st.session_state.game_lives <= 0:
            st.markdown("### 🤕 Oh no! Adventure Over")
            st.markdown("Even the best explorers need a rest. Try again to learn more!")
            if st.button("🔄 Restart Adventure", key="restart_quest"):
                st.session_state.game_lives = 3
                st.session_state.game_score = 0
                st.session_state.current_question = None
                st.rerun()

    # ==========================================
    # GAME TAB 2: SURVIVAL SCHOOL
    # ==========================================
    with tab2:
        st.header("☠️ Survival School")
        st.caption("📚 Curriculum Link: Science (Plants), PSHE (Safety)")

        with st.expander("📖 How to Play"):
            st.markdown("""
            1. Read the **Case File** carefully. Look for clues in the description.
            2. You have two suspects: One is **Safe**, one is **Poisonous**.
            3. Click the **Safe** plant to solve the case.
            4. Solve 5 cases in a row to earn your **Safety Badge**.
            """)

        # Expanded Case Files
        # Added 'rule' to help learning, 'hint' for stuck players, and expanded safety reports.
        CASE_FILES = [
            # --- ORIGINAL 10 CASES ---
            {
                "clue": "You find a tall plant with white umbrella-shaped flowers ☂️. You check the stem. It is **smooth** (no hairs) and has **purple spots** on it.",
                "rule": "🚨 **Rule:** In the Carrot family, purple spots usually mean POISON.",
                "hint": "Check the stem texture! Safe Carrot family members usually have hairy stems.",
                "safe_plant": "Wild Carrot",
                "danger_plant": "Hemlock",
                "safe_icon": "🥕",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Hemlock (POISON):** Smooth stem with purple spots. Smells like mouse urine.\n- **Wild Carrot (Safe):** Hairy stem. Smells like carrots. Remember: **Hairy is Happy, Smooth is Suspicious!**",
                "safe_habitat": "Meadows"
            },
            {
                "clue": "You find a plant with broad green leaves in a damp woodland. You crush a leaf and it smells strongly of **garlic** 🧄.",
                "rule": "✅ **Rule:** Strong onion/garlic smell is usually a good sign.",
                "hint": "Use your nose! If it smells like food (garlic/onion), it might be food. If it has no smell, be careful.",
                "safe_plant": "Wild Garlic",
                "danger_plant": "Lily of the Valley",
                "safe_icon": "🌿",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Lily of the Valley (POISON):** Has no garlic smell. Has bell-shaped flowers.\n- **Wild Garlic (Safe):** Smells strongly of garlic. Perfect for pesto! **No smell = Leave it be.**",
                "safe_habitat": "Woodland"
            },
            {
                "clue": "A bright orange mushroom grows under an oak tree. Under the cap, it has **ridges** (like false gills) that run down the stem. It smells like **apricots** 🍑.",
                "rule": "✅ **Rule:** True gills are thin sheets. Ridges are blunt and thick.",
                "hint": "Look under the cap! Are they thin paper-like gills, or thick forked ridges?",
                "safe_plant": "Chanterelle",
                "danger_plant": "False Chanterelle",
                "safe_icon": "🍄",
                "danger_icon": "🚫",
                "fact": "🕵️ **Inspector's Report:**\n- **False Chanterelle (Inedible):** Has true gills (thin sheets). No apricot smell.\n- **Chanterelle (Safe):** Has 'false gills' (ridges) and smells fruity. **Ridges = Rewarding.**",
                "safe_habitat": "Woodland"
            },
            {
                "clue": "You find a bush with dark berries. The leaves are arranged in **pairs** opposite each other on the stem.",
                "rule": "✅ **Rule:** 'Opposite' leaves (pairs) are safe for Elder. 'Alternate' leaves are dangerous.",
                "hint": "Look at the leaves! Do they split off the stem in pairs, or one by one?",
                "safe_plant": "Elderflower",
                "danger_plant": "Dwarf Elder",
                "safe_icon": "🌸",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Dwarf Elder (POISON):** Leaves are alternate (one by one). Flowers stand upright.\n- **Elderflower (Safe):** Leaves are opposite (in pairs). Flowers droop down.",
                "safe_habitat": "Hedgerow"
            },
            {
                "clue": "A tall plant with white flowers grows by a river. You dig up the root. It smells like a **carrot** 🥕.",
                "rule": "✅ **Rule:** Smell is key! Carrot family roots should smell pleasant.",
                "hint": "Smell test! A pleasant veg smell is good. A rotten or mousey smell is bad.",
                "safe_plant": "Wild Parsnip",
                "danger_plant": "Hemlock Water Dropwort",
                "safe_icon": "🥬",
                "danger_icon": "💀",
                "fact": "🕵️ **Inspector's Report:**\n- **Hemlock Water Dropwort (POISON):** Smells unpleasant. Has tuberous roots (look like fingers). **Deadliest plant in UK.**\n- **Wild Parsnip (Safe):** Smells like parsnip/carrot. **Warning:** Be 100% sure before eating any root!",
                "safe_habitat": "Riverbanks"
            },
            {
                "clue": "You see a patch of green leaves growing on the forest floor. You touch them carefully with gloves. They **sting** your fingers!",
                "rule": "✅ **Rule:** A sting is painful, but usually safe if cooked.",
                "hint": "Does it hurt? A sting usually identifies Nettles. Non-stinging lookalikes might be dangerous.",
                "safe_plant": "Nettles",
                "danger_plant": "Dog's Mercury",
                "safe_icon": "🌿",
                "danger_icon": "⚠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Dog's Mercury (POISON):** Does not sting. Can make you very sick.\n- **Nettles (Safe):** Stings! But cooking destroys the sting. Delicious in soup. **Sting = Signal!**",
                "safe_habitat": "Woodland"
            },
            {
                "clue": "You find a tree with dark green needles and a red berry cup. It grows near a **churchyard** ⛪.",
                "rule": "🚨 **Rule:** Red berry cups (Yew) are often deadly.",
                "hint": "Look at the leaves! Are they flat needles? Are they dark green? Yew is deadly.",
                "safe_plant": "Juniper Berry",
                "danger_plant": "Yew",
                "safe_icon": "🫐",
                "danger_icon": "💀",
                "fact": "🕵️ **Inspector's Report:**\n- **Yew (POISON):** Every part is deadly except the red berry flesh. Common in churchyards.\n- **Juniper (Safe):** Blue berries, spiky needles. Used for gin. **Yew = You Die.**",
                "safe_habitat": "Churchyards"
            },
            {
                "clue": "A plant with strap-like leaves grows in the woods. You roll the stem between your fingers—it feels **triangular** (like a keel ⛵).",
                "rule": "✅ **Rule:** A triangular stem is a unique ID feature.",
                "hint": "Feel the stem! Is it round, or does it have edges/corners?",
                "safe_plant": "Three-Cornered Leek",
                "danger_plant": "Bluebell",
                "safe_icon": "🌸",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Bluebell (POISON):** Round stem. Blue bells. All parts toxic.\n- **Three-Cornered Leek (Safe):** Triangular stem. White flowers. Smells like onion/garlic. **Triangle = Tasty.**",
                "safe_habitat": "Woodland"
            },
            {
                "clue": "A huge plant (over 2 meters tall) with white flowers grows by a river. The stem has **bristly hairs** and is green.",
                "rule": "🚨 **Rule:** Giant Hogweed burns skin. Hairs can be a clue to identity.",
                "hint": "Size matters! If it's huge (taller than you) and has purple blotches, run!",
                "safe_plant": "Common Hogweed",
                "danger_plant": "Giant Hogweed",
                "safe_icon": "🌻",
                "danger_icon": "⚠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Giant Hogweed (POISON):** Sap burns skin in sunlight! Huge (3m+). Often has purple blotches.\n- **Common Hogweed (Safe):** Smaller (1-2m). Bristly stem. **Giant = Dangerous.**",
                "safe_habitat": "Riverbanks"
            },
            {
                "clue": "A fungus grows on an **Elder tree**. It is brown, jelly-like, and looks like an ear.",
                "rule": "✅ **Rule:** Fungi grow on specific trees. Host tree identification helps.",
                "hint": "Which tree is it on? Wood Ear only grows on Elder trees.",
                "safe_plant": "Wood Ear",
                "danger_plant": "Beech Bracket",
                "safe_icon": "👂",
                "danger_icon": "🪵",
                "fact": "🕵️ **Inspector's Report:**\n- **Beech Bracket (Inedible):** Woody texture. Grows on Beech trees.\n- **Wood Ear (Safe):** Jelly texture. Grows on Elder trees. **Jelly on Elder = Edible.**",
                "safe_habitat": "Woodland"
            },
            
            # --- NEW 15 CASES (Checked & Fixed) ---
            {
                "clue": "You find a nut on the ground. It is brown and sits inside a **spiky green case** (a bur).",
                "rule": "✅ **Rule:** Spikes outside usually mean sweet inside.",
                "hint": "Touch the case! Is it spiky? That's usually a Sweet Chestnut.",
                "safe_plant": "Sweet Chestnut",
                "danger_plant": "Horse Chestnut",
                "safe_icon": "🌰",
                "danger_icon": "🥜",
                "fact": "🕵️ **Inspector's Report:**\n- **Horse Chestnut (POISON):** Case is warty/bumpy, not spiky. Nut is shiny. (Conkers).\n- **Sweet Chestnut (Safe):** Case has long, sharp spikes. Nut has a 'tail' point. **Spikes are Safe!**",
                "safe_habitat": "Woodland"
            },
            {
                "clue": "A small white flower grows in the grass. It has **arrow-shaped leaves**. You take a tiny bite of a leaf and it tastes like **lemon sherbet**.",
                "rule": "✅ **Rule:** Taste is a clue! Sorrel tastes like apple/lemon peels.",
                "hint": "Does it taste like salad? If it burns your mouth, spit it out!",
                "safe_plant": "Wood Sorrel",
                "danger_plant": "Lords and Ladies",
                "safe_icon": "☘️",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Lords & Ladies (POISON):** Leaves can burn the mouth. Orange berries later in year.\n- **Wood Sorrel (Safe):** Tastes like lemon. Heart-shaped leaves. **Tasty = Safe. Burning = Bad.**",
                "safe_habitat": "Woodland"
            },
            {
                "clue": "A white mushroom grows in a field. You cut it open. The gills are **pink**, turning brown.",
                "rule": "✅ **Rule:** Field mushrooms have pink gills.",
                "hint": "Look under the cap! If the gills stain yellow when you rub them, DO NOT EAT.",
                "safe_plant": "Field Mushroom",
                "danger_plant": "Yellow Stainer",
                "safe_icon": "🍄",
                "danger_icon": "🚫",
                "fact": "🕵️ **Inspector's Report:**\n- **Yellow Stainer (POISON):** Stains bright yellow when rubbed. Smells like ink/chemicals.\n- **Field Mushroom (Safe):** Pink gills turn brown. Smells like mushrooms. **Yellow Stain = Pain.**",
                "safe_habitat": "Fields"
            },
            {
                "clue": "A round white ball sits on the grass. You cut it in half. The inside is **pure white** and solid.",
                "rule": "✅ **Rule:** Puffballs must be pure white inside.",
                "hint": "Cut it open! If it is purple, black, or powdery inside, it is dangerous.",
                "safe_plant": "Puffball",
                "danger_plant": "Earthball",
                "safe_icon": "⚪",
                "danger_icon": "🟤",
                "fact": "🕵️ **Inspector's Report:**\n- **Earthball (POISON):** Inside is purple/black. Thick skin.\n- **Puffball (Safe):** Inside is pure white (like a marshmallow). **White is Right.**",
                "safe_habitat": "Fields"
            },
            {
                "clue": "You see a tree with young green leaves. The leaves are **soft and hairy**. You want to make a salad.",
                "rule": "✅ **Rule:** Soft young leaves are often edible.",
                "hint": "Feel the leaf! Is it soft like paper? Or thick and leathery?",
                "safe_plant": "Beech Leaves",
                "danger_plant": "Cherry Laurel",
                "safe_icon": "🍃",
                "danger_icon": "🌿",
                "fact": "🕵️ **Inspector's Report:**\n- **Cherry Laurel (POISON):** Leaves are thick, leathery, and evergreen. Contains cyanide.\n- **Beech Leaves (Safe):** Soft, hairy, paper-thin. Only eat young ones. **Soft = Salad. Leathery = Leave it.**",
                "safe_habitat": "Hedgerow"
            },
            {
                "clue": "A bright yellow flower grows in the grass. The stem is **hollow** and has a milky white sap.",
                "rule": "✅ **Rule:** Dandelions have hollow stems.",
                "hint": "Check the stem! Is it hollow? Does it have milky sap?",
                "safe_plant": "Dandelion",
                "danger_plant": "Ragwort",
                "safe_icon": "🌼",
                "danger_icon": "🌻",
                "fact": "🕵️ **Inspector's Report:**\n- **Ragwort (POISON):** Toxic to liver. Tall, ragged leaves.\n- **Dandelion (Safe):** Hollow stem with milky sap. Leaves are 'Lion's Teeth'. **Hollow Stem = Dandelion.**",
                "safe_habitat": "Meadow"
            },
            {
                "clue": "A bush grows by the sea. It has **fleshy blue-green leaves**. The leaves taste salty.",
                "rule": "✅ **Rule:** Coastal plants are often salty/succulent.",
                "hint": "Taste! Is it salty? Succulent leaves hold water.",
                "safe_plant": "Sea Kale",
                "danger_plant": "Hemlock", # Hemlock can grow near water/coastal, providing a valid danger
                "safe_icon": "🥬",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Hemlock (POISON):** Purple spotted stem. Smells bad.\n- **Sea Kale (Safe):** Blue leaves, white flowers. Tastes salty. **Salty = Success.**",
                "safe_habitat": "Coastal"
            },
            {
                "clue": "A bright orange berry grows on a bush. You check the **seeds inside**. There is one single large stone/seed.",
                "rule": "✅ **Rule:** Single stone = usually a Sloe/Plum.",
                "hint": "Cut the berry open! Count the seeds. Many seeds in a berry can be dangerous.",
                "safe_plant": "Sloe (Blackthorn)",
                "danger_plant": "Deadly Nightshade",
                "safe_icon": "🫐",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Deadly Nightshade (POISON):** Shiny black berry with MANY seeds inside.\n- **Sloe (Safe):** One single stone inside. Very sour. Makes gin! **One Stone = Safe. Many Seeds = Danger.**",
                "safe_habitat": "Hedgerow"
            },
            {
                "clue": "A green plant grows in the hedge. It has **triangular leaves** that smell spicy.",
                "rule": "✅ **Rule:** Garlic smell = Leek. Pepper smell = Pepper.",
                "hint": "Crush the leaves! Does it smell like garlic or pepper?",
                "safe_plant": "Garlic Mustard",
                "danger_plant": "Lords and Ladies", # Fixed: Lords and Ladies is dangerous, Hedge Mustard is edible
                "safe_icon": "🌱",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Lords and Ladies (POISON):** Arrow-shaped leaves. Burns mouth.\n- **Garlic Mustard (Safe):** Smells of garlic! Triangular leaves. **Garlic Mustard is the tasty one!**",
                "safe_habitat": "Hedgerow"
            },
            {
                "clue": "A plant grows by the river. It has **yellow flowers**. You check the stem—it is smooth.",
                "rule": "🚨 **Rule:** Yellow flowers on a river? Check for hairs.",
                "hint": "Look at the stem! Hairs = safe (Alexanders). Smooth/Spotted = danger (Hemlock).",
                "safe_plant": "Alexanders",
                "danger_plant": "Hemlock",
                "safe_icon": "🌼",
                "danger_icon": "☠️",
                "fact": "🕵️ **Inspector's Report:**\n- **Hemlock (POISON):** White flowers. Purple spots. Smooth.\n- **Alexanders (Safe):** Yellow flowers. Smooth stem. Smells like celery. **Yellow is good (Alexanders). White is worry (Hemlock).**",
                "safe_habitat": "Coastal"
            },
            {
                "clue": "A tree has hanging clusters of brown nuts. The nuts have a **green leafy collar** around them.",
                "rule": "✅ **Rule:** Hazelnuts have a leafy 'skirt'.",
                "hint": "Look at the nut! Does it wear a leafy hat?",
                "safe_plant": "Hazelnut",
                "danger_plant": "Buckeye",
                "safe_icon": "🌰",
                "danger_icon": "🥜",
                "fact": "🕵️ **Inspector's Report:**\n- **Buckeye (POISON):** Similar nuts but the casing is smooth, not leafy.\n- **Hazelnut (Safe):** Leafy husk. Pointed nut. **Leafy Hat = Tasty.**",
                "safe_habitat": "Hedgerow"
            },
            {
                "clue": "A plant grows in the garden. It has **sticky stems** that cling to your clothes.",
                "rule": "✅ **Rule:** Sticky stems = Cleavers/Goosegrass.",
                "hint": "Does it stick to you? If yes, it's usually Cleavers.",
                "safe_plant": "Cleavers",
                "danger_plant": "Bindweed",
                "safe_icon": "🌿",
                "danger_icon": "🌸",
                "fact": "🕵️ **Inspector's Report:**\n- **Bindweed (POISON):** Twists around plants. Has large white trumpet flowers.\n- **Cleavers (Safe):** Sticky! Sticks to clothes. Tiny hairs. **Sticky = Safe.**",
                "safe_habitat": "Gardens"
            },
            {
                "clue": "A mushroom grows in the grass. It has a **white cap** and a ring around the stem.",
                "rule": "🚨 **Rule:** White cap + ring + sack at base = Death Cap. DEADLY.",
                "hint": "Dig around the base! Is there a cup/volva? If yes, DO NOT TOUCH.",
                "safe_plant": "Field Mushroom",
                "danger_plant": "Death Cap",
                "safe_icon": "🍄",
                "danger_icon": "💀",
                "fact": "🕵️ **Inspector's Report:**\n- **Death Cap (POISON):** White cap, ring, and a cup (volva) at the base. KILLS you.\n- **Field Mushroom (Safe):** Pink gills. No cup at the base. **White Gills + Cup = Cut!**",
                "safe_habitat": "Fields"
            },
            {
                "clue": "A red berry grows in the hedge. It looks like a small apple. The leaves are **serrated** (like a saw).",
                "rule": "✅ **Rule:** Red berries are often haws (Hawthorn) or Rosehips.",
                "hint": "Look at the leaves! Saw-tooth edges are Hawthorn.",
                "safe_plant": "Hawthorn",
                "danger_plant": "Cotoneaster",
                "safe_icon": "🍎",
                "danger_icon": "🚫",
                "fact": "🕵️ **Inspector's Report:**\n- **Cotoneaster (POISON):** Often garden escape. Berries contain cyanide.\n- **Hawthorn (Safe):** 'Haws' are edible. Saw-tooth leaves. Thorns. **Saw-tooth = Safe.**",
                "safe_habitat": "Hedgerow"
            }
        ]

        st.markdown("### 🕵️‍♂️ The Safety Inspector")
        progress = st.session_state.survival_correct_count / 5
        st.progress(progress, text=f"Badge Progress: {st.session_state.survival_correct_count}/5 Cases Solved")
        col1, col2 = st.columns(2)
        col1.metric("❤️ Lives", "❤️" * max(0, st.session_state.survival_lives))
        col2.metric("🌟 Score", st.session_state.survival_score)
        st.markdown("---")

        if st.session_state.survival_current_case is None:
            st.session_state.survival_current_case = random.choice(CASE_FILES)
            st.session_state.survival_result = None

        case = st.session_state.survival_current_case
        st.info(f"🔎 **New Case File Found!**")
        st.markdown(f"**Habitat:** {case['safe_habitat']}")
        st.markdown(f"**Your Observation:** {case['clue']}")
        st.markdown("#### ⚠️ VERDICT: Is this plant SAFE to touch/harvest?")

        options = [{"name": case['safe_plant'], "icon": case['safe_icon'], "is_safe": True}, {"name": case['danger_plant'], "icon": case['danger_icon'], "is_safe": False}]
        random.shuffle(options)

        if st.session_state.survival_result is None:
            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button(f"{options[0]['icon']} {options[0]['name']}", key="surv_opt_1", use_container_width=True):
                if options[0]['is_safe']: st.session_state.survival_result = "correct"; st.session_state.survival_score += 20; st.session_state.survival_correct_count += 1
                else: st.session_state.survival_result = "wrong"; st.session_state.survival_lives -= 1; st.session_state.survival_correct_count = 0
                st.rerun()
            if btn_col2.button(f"{options[1]['icon']} {options[1]['name']}", key="surv_opt_2", use_container_width=True):
                if options[1]['is_safe']: st.session_state.survival_result = "correct"; st.session_state.survival_score += 20; st.session_state.survival_correct_count += 1
                else: st.session_state.survival_result = "wrong"; st.session_state.survival_lives -= 1; st.session_state.survival_correct_count = 0
                st.rerun()
        else:
            if st.session_state.survival_result == "correct": st.success("✅ CASE SOLVED! Great work, Inspector."); st.balloons()
            else: st.error("☠️ DANGER! That was the wrong choice.")
            st.markdown("### 📝 Safety Report")
            st.warning(case['fact'])
            if st.session_state.survival_correct_count >= 5: st.markdown("# 🏅 BADGE EARNED: Plant Safety Expert!"); st.snow(); st.session_state.survival_correct_count = 0
            if st.button("📋 Next Case", key="next_case_btn"): st.session_state.survival_current_case = None; st.rerun()

        if st.session_state.survival_lives <= 0:
            st.markdown("## 🤕 Training Ended")
            st.markdown("Don't worry, even experts make mistakes. Review the case files and try again!")
            if st.button("🔄 Restart Training", key="restart_survival"): st.session_state.survival_lives = 3; st.session_state.survival_correct_count = 0; st.session_state.survival_current_case = None; st.session_state.survival_result = None; st.rerun()

    # ==========================================
    # GAME TAB 3: DAILY QUIZ
    # ==========================================
    with tab3:
        st.header("🎯 The Daily Challenge")
        st.caption("📚 Curriculum Link: Science (Plants), Seasonal Changes")
        with st.expander("📖 How to Play"):
            st.markdown("Answer 5 questions to complete the challenge. Build a streak for bonus points!")

        col1, col2, col3 = st.columns(3)
        col1.metric("🔥 Streak", f"{st.session_state.daily_streak} Days")
        col2.metric("🌟 Score", st.session_state.quiz_score)
        col3.metric("❓ Question", f"{st.session_state.quiz_q_num}/{st.session_state.quiz_max}")
        st.progress(st.session_state.quiz_q_num / st.session_state.quiz_max)

        if st.session_state.quiz_q_num < st.session_state.quiz_max:
            if st.session_state.get('q_data') is None:
                q_type = random.choice(["edible_check", "parts_check", "season_check"])
                plant = random.choice(UK_PLANTS['edible'] + UK_PLANTS['poisonous'])
                question_text, correct_answer, options, fun_fact = "", "", [], ""

                if q_type == "edible_check":
                    # Check status based on list presence
                    is_edible = plant in UK_PLANTS['edible']
                    question_text = f"Is **{plant['name']}** safe to eat?"
                    correct_answer = "Edible" if is_edible else "Poisonous"
                    options = ["Edible", "Poisonous"]
                    fun_fact = f"**Warning:** {plant.get('warnings', 'Check ID')}" if is_edible else f"**Danger:** {plant.get('symptoms', 'Toxic')}"
                elif q_type == "parts_check":
                    plant = random.choice(UK_PLANTS['edible'])
                    raw_parts = plant.get('parts', 'Leaves')
                    if isinstance(raw_parts, str): parts = [p.strip() for p in raw_parts.split(',')]
                    else: parts = raw_parts
                    if not parts: parts = ['Leaves']
                    correct_answer = parts[0]
                    wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark"]
                    wrong_options = [p for p in wrong_parts if p not in parts]
                    question_text = f"Which part of **{plant['name']}** do we usually eat?"
                    options = [correct_answer] + random.sample(wrong_options, min(2, len(wrong_options)))
                    fun_fact = f"**Tip:** {plant.get('warnings', 'Wash before eating.')}"
                elif q_type == "season_check":
                    plant = random.choice(UK_PLANTS['edible'])
                    correct_months = plant.get('months', ['Summer'])
                    correct_answer = random.choice(correct_months)
                    all_months = ["January", "March", "June", "August", "October", "December"]
                    wrong_months = [m for m in all_months if m not in correct_months]
                    question_text = f"When is **{plant['name']}** best harvested?"
                    options = [correct_answer] + random.sample(wrong_months, min(2, len(wrong_months)))
                    fun_fact = f"**Habitat:** {plant.get('habitat', 'Various')}"

                random.shuffle(options)
                st.session_state.q_data = {"plant": plant, "text": question_text, "correct": correct_answer, "options": options, "type": q_type, "fact": fun_fact}

            q = st.session_state.q_data
            st.markdown("### 🧠 Quick Question:")
            st.markdown(f"#### {q['text']}")
            cols = st.columns(len(q['options']))
            for i, opt in enumerate(q['options']):
                if cols[i].button(f"👉 {opt}", key=f"ans_{i}", use_container_width=True):
                    if opt == q['correct']: st.session_state.quiz_score += 1; st.session_state.daily_streak += 1; st.toast("✅ Correct!")
                    else: st.session_state.daily_streak = 0; st.toast("❌ Oops!")
                    st.session_state.quiz_q_num += 1; st.session_state.q_data = None; time.sleep(0.5); st.rerun()
        else:
            st.balloons(); st.markdown("## 🎉 Challenge Complete!")
            if st.session_state.quiz_score == st.session_state.quiz_max: st.success("PERFECT SCORE!")
            elif st.session_state.quiz_score >= st.session_state.quiz_max / 2: st.info("Good job!")
            else: st.warning("Keep practicing!")
            if st.button("🔄 Try Again", key="restart_quiz"): st.session_state.quiz_score = 0; st.session_state.quiz_q_num = 0; st.session_state.q_data = None; st.rerun()

    # ==========================================
    # GAME TAB 4: ECO-VILLAGE
    # ==========================================
    with tab4:
        st.header("🏘️ Eco-Village Builder")
        st.caption("📚 Manage resources sustainably!")
        with st.expander("📖 How to Play"):
            st.markdown("""
            - **Forage:** Gather resources (Costs Stamina & Nature).
            - **Build:** Buy buildings on the Map (Costs Money).
            - **Craft:** Make items in the Workshop.
            - **Rest:** Click 'Next Day' to recover Stamina.
            - **Goal:** Build a village without destroying the **Nature Health** bar!
            """)

        ITEMS_DATA = {"Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 2}, "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1}, "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 3}, "Wood": {"icon": "🪵", "rarity": 0.6, "value": 2}, "Stone": {"icon": "🪨", "rarity": 0.4, "value": 2}, "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 5}, "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 10}, "Milk": {"icon": "🥛", "rarity": 0.0, "value": 15}}
        BUILDINGS = {"House": {"cost": 50, "icon": "🏠", "desc": "Shelter to recover stamina."}, "Well": {"cost": 30, "icon": "🪨", "desc": "Passive water income."}, "Coop": {"cost": 40, "icon": "🐔", "desc": "Hold up to 5 chickens."}}

        if st.session_state.get('village') is None: st.session_state.village = {'grid': [['🌲' for _ in range(6)] for _ in range(4)], 'stats': {'Food': 50, 'Water': 50, 'Power': 0, 'Stamina': 100, 'Money': 100}, 'inventory': {}, 'animals': [], 'buildings': [], 'day': 1, 'season': 'Spring', 'placement_mode': None, 'nature_health': 100}
        game = st.session_state.village

        def render_stats():
            s = game['stats']
            cols = st.columns(6)
            cols[0].metric("🍖 Food", s['Food'])
            cols[1].metric("💧 Water", s['Water'])
            cols[2].metric("⚡ Power", s['Power'])
            cols[3].metric("💪 Stamina", s['Stamina'])
            cols[4].metric("💰 Money", f"£{s['Money']}")
            nature = game['nature_health']
            cols[5].metric(f"{'🟢' if nature > 50 else '🟡' if nature > 20 else '🔴'} Nature", nature)
            if nature < 20: st.warning("⚠️ The forest is struggling! Over-harvesting detected.")
            st.markdown("---")

        map_tab, forage_tab = st.tabs(["🗺️ Map", "🌲 Forage"])
        with map_tab:
            st.markdown(f"### 📅 Day {game['day']} | {game['season']}")
            render_stats()
            st.markdown("#### 🛠️ Build")
            options = ["None"] + list(BUILDINGS.keys())
            selected_build = st.selectbox("Select Building", options)
            game['placement_mode'] = selected_build if selected_build != "None" else None
            if game['placement_mode']:
                b = BUILDINGS[game['placement_mode']]
                st.write(f"**Cost:** £{b['cost']} | {b['desc']}")
            st.markdown("---")
            st.markdown("#### 🗺️ Your Land")
            for row_idx in range(4):
                cols = st.columns(6)
                for col_idx in range(6):
                    current_icon = game['grid'][row_idx][col_idx]
                    if game['placement_mode'] and current_icon == '🌲':
                        can_afford = game['stats']['Money'] >= BUILDINGS[game['placement_mode']]['cost']
                        if cols[col_idx].button("Place Here", key=f"place_{row_idx}_{col_idx}", disabled=not can_afford):
                            game['stats']['Money'] -= BUILDINGS[game['placement_mode']]['cost']
                            game['grid'][row_idx][col_idx] = BUILDINGS[game['placement_mode']]['icon']
                            st.rerun()
                    else:
                        cols[col_idx].markdown(f"<div style='text-align:center; font-size:24px;'>{current_icon}</div>", unsafe_allow_html=True)
            if st.button("⏭️ Next Day"): game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20); game['day'] += 1; st.rerun()

        with forage_tab:
            st.markdown("### 🌲 Gather Resources")
            render_stats()
            if st.button("Forage Plants", key="fp1"):
                if game['stats']['Stamina'] >= 10:
                    game['stats']['Stamina'] -= 10
                    game['nature_health'] = max(0, game['nature_health'] - 5) # Impact nature
                    found = [name for name, data in ITEMS_DATA.items() if random.random() < data['rarity']]
                    for f in found: game['inventory'][f] = game['inventory'].get(f, 0) + 1
                    st.success(f"Found: {', '.join(found[:3])}...")
                    st.rerun()
                else:
                    st.error("Not enough stamina! Rest (Next Day) to recover.")

    # ==========================================
    # GAME TAB 5: FARM TYCOON
    # ==========================================
    with tab5:
        st.header("🚜 Farm Tycoon: Nature Guardians")
        st.caption("📚 Build your farm, watch for Invasive Species!")

        # Instructions
        with st.expander("📖 How to Play"):
            st.markdown("""
            - Select a **Tool** (Crop or Animal) and click the brown soil to place it.
            - Press **Next Day** to let crops grow.
            - Harvest crops when they are ready (Yellow icons).
            - **Watch out!** Invasive plants (🥀) will try to grow. Use the **Clear** tool to remove them!
            """)

        # --- GAME STATE INIT ---
        if st.session_state.get('farm_game') is None:
            # Create Grid 5x6 (30 tiles)
            # 0 = Dirt, 1 = Water, 2 = Seed, 3 = Growing, 4 = Ready, 5 = Chicken, 6 = Cow, 7 = INVASIVE
            grid = [[0 for _ in range(6)] for _ in range(5)]

            # Generate Random Stream
            stream_col = random.randint(1, 4)
            for r in range(5):
                grid[r][stream_col] = 1
                if random.random() > 0.5: stream_col = max(0, min(5, stream_col + random.choice([-1, 1]))); grid[r][stream_col] = 1

            st.session_state.farm_game = {
                'grid': grid,
                'money': 100,
                'day': 1,
                'season': 'Spring',
                'weather': '☀️ Sunny',
                'tool': 'Carrot', # Default tool
                'game_over': False,
                'invasives_cleared': 0
            }

        game = st.session_state.farm_game

        # --- UI HEADER ---
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Day", game['day'])
        col2.metric("💰 Money", f"£{game['money']}")
        col3.metric("🛡️ Guard Badge", game['invasives_cleared'])

        st.markdown("---")

        # --- TOOL SELECTION ---
        st.markdown("### 🛠️ Toolbox")

        # Expanded Tools
        tools = {
            "🥕 Carrot (£10)": "Carrot",
            "🌾 Wheat (£15)": "Wheat",
            "🌽 Corn (£20)": "Corn",
            "🐔 Chicken (£50)": "Chicken",
            "🐄 Cow (£100)": "Cow",
            "🧹 Clear Invasive (Free)": "Clear"
        }

        tool_cols = st.columns(len(tools))

        for i, (label, val) in enumerate(tools.items()):
            if tool_cols[i].button(label, key=f"tool_{val}"):
                game['tool'] = val
                st.rerun()

        # Highlight selected tool
        if game['tool'] == val:
            tool_cols[i].markdown("**✅ Selected**")

        st.markdown("---")

        # --- THE GRID ---
        st.markdown("### 🗺️ Your Farm")
        st.markdown("`🟤` Dirt | `🌊` Stream | `🌱` Seed | `🌿` Growing | `🌾` Ready | `🐔` Chicken | `🐄` Cow | `🥀` **Invasive**")

        # Icons
        icons = {0: "🟤", 1: "🌊", 2: "🌱", 3: "🌿", 4: "🌾", 5: "🐔", 6: "🐄", 7: "🥀"}

        # Render Grid
        for r in range(5):
            cols = st.columns(6)
            for c in range(6):
                tile_val = game['grid'][r][c]
                icon = icons.get(tile_val, "❓")

                # 1. HANDLE INVASIVE CLEARING
                if tile_val == 7 and game['tool'] == "Clear":
                    if cols[c].button("🥀 CLEAR", key=f"{r}_{c}"):
                        game['grid'][r][c] = 0
                        game['invasives_cleared'] += 1
                        st.success("Invasive Removed!")
                        st.rerun()

                # 2. HANDLE PLANTING CROPS (Carrot, Wheat, Corn)
                elif tile_val == 0 and game['tool'] in ["Carrot", "Wheat", "Corn"]:

                    # Define costs
                    costs = {"Carrot": 10, "Wheat": 15, "Corn": 20}
                    cost = costs[game['tool']]

                    can_afford = game['money'] >= cost
                    if cols[c].button(f"Plant (£{cost})", key=f"plant_{r}_{c}", disabled=not can_afford):
                        game['money'] -= cost
                        game['grid'][r][c] = 2 # All crops start as Seed (ID 2)
                        st.rerun()

                # 3. HANDLE ANIMALS (Chicken, Cow)
                elif tile_val == 0 and game['tool'] in ["Chicken", "Cow"]:

                    # Define costs
                    costs = {"Chicken": 50, "Cow": 100}
                    cost = costs[game['tool']]

                    # Define ID for grid
                    animal_ids = {"Chicken": 5, "Cow": 6}

                    can_afford = game['money'] >= cost
                    if cols[c].button(f"Buy (£{cost})", key=f"buy_{r}_{c}", disabled=not can_afford):
                        game['money'] -= cost
                        game['grid'][r][c] = animal_ids[game['tool']]
                        st.rerun()

                # 4. HANDLE HARVESTING (Crops - Ready)
                elif tile_val == 4:
                    if cols[c].button("🌾 Harvest", key=f"harv_{r}_{c}"):
                        # Harvest value depends on crop? For now random.
                        harvest_val = random.randint(15, 30)
                        game['money'] += harvest_val
                        game['grid'][r][c] = 0
                        st.success(f"Harvested! +£{harvest_val}")
                        st.rerun()

                # 5. HANDLE SELLING ANIMALS (Click to sell)
                elif tile_val == 5: # Chicken
                    if cols[c].button("🐔 Sell", key=f"sell_chick_{r}_{c}"):
                        game['money'] += 25
                        game['grid'][r][c] = 0
                        st.success("Sold Chicken! +£25")
                        st.rerun()

                elif tile_val == 6: # Cow
                    if cols[c].button("🐄 Sell", key=f"sell_cow_{r}_{c}"):
                        game['money'] += 60
                        game['grid'][r][c] = 0
                        st.success("Sold Cow! +£60")
                        st.rerun()

                # 6. DEFAULT DISPLAY (Show Icon)
                else:
                    cols[c].markdown(f"<div style='text-align:center; font-size:24px;'>{icon}</div>", unsafe_allow_html=True)

        st.markdown("---")

        # --- NEXT DAY BUTTON ---
        if st.button("⏭️ Next Day", key="next_day_farm"):
            # 1. Crop Growth
            for r in range(5):
                for c in range(6):
                    if game['grid'][r][c] == 2: game['grid'][r][c] = 3
                    elif game['grid'][r][c] == 3: game['grid'][r][c] = 4

            # 2. RANDOM EVENTS (Weather & Market)
            event_roll = random.random()

            if event_roll < 0.2:
                market_item = random.choice(["Carrot", "Wheat", "Corn"])
                st.toast(f"📈 Market News: {market_item} prices fluctuated!")

            elif event_roll < 0.3:
                st.toast("🌧️ Heavy Rain! Some crops were washed away.")
                crops = [(r,c) for r in range(5) for c in range(6) if game['grid'][r][c] in [2, 3]]
                if crops:
                    rr, cc = random.choice(crops)
                    game['grid'][rr][cc] = 0

            # 3. INVASIVE SPECIES EVENT
            elif event_roll < 0.6:
                invasives = [
                    {"name": "Japanese Knotweed", "fact": "Damages foundations!"},
                    {"name": "Himalayan Balsam", "fact": "Takes over riverbanks."},
                    {"name": "Giant Hogweed", "fact": "Sap causes burns!"},
                    {"name": "Rhododendron", "fact": "Toxic soil."}
                ]
                invasive = random.choice(invasives)
                empty_spots = [(r,c) for r in range(5) for c in range(6) if game['grid'][r][c] == 0]
                if empty_spots:
                    rr, cc = random.choice(empty_spots)
                    game['grid'][rr][cc] = 7
                    st.toast(f"⚠️ {invasive['name']} spotted! {invasive['fact']}")

            game['day'] += 1
            st.rerun()
