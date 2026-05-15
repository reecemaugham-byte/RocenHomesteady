import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from openai import OpenAI
import os
import json
import asyncio

# --- SAFE IMPORTS ---
try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import alpaca_trade_api as tradeapi
except ImportError:
    tradeapi = None

try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    Image = None

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# --- CONFIGURATION & API ---
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

# --- SESSION STATE INIT ---
def init_session_state():
    defaults = {
        'game_score': 0, 'game_lives': 3, 'game_streak': 0, 'current_question': None,
        'village': None, 'farm_game': None, 'survival_lives': 3, 'survival_score': 0,
        'current_survival_pair': None, 'quiz_score': 0, 'quiz_q_num': 0, 'quiz_max': 5,
        'q_data': None, 'chat_language': 'English', 'messages': [], 'selected_page': "Home",
        'book_content': {}, 'book_outline': "", 'active_season': "Summer",
        'season_badge_progress': [], 'survival_correct_count': 0, 'survival_current_case': None,
        'survival_result': None, 'daily_streak': 0, 'quiz_active': False, 'module_questions': None,
        'player_title': "Novice Gatherer",
        'total_plants_identified': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# --- THEME FUNCTION ---
def apply_brand_theme():
    st.markdown("""
    <style>
    /* --- Main Background - Dark Earth --- */
    .stApp, section.main > div {
        background-color: #3A2416; /* Dark Coffee */
    }

    /* --- Text Color - White for contrast --- */
    .stMarkdown, .stHeader, p, label, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        color: #FFFFFF !important; 
    }

    /* --- Headings - Copper --- */
    h1, h2, h3 {
        color: #B87333 !important; /* COPPER */
        font-family: 'Georgia', serif !important;
        border-bottom: 2px solid #6B4226; /* Saddle Brown underline */
        padding-bottom: 10px;
    }

    /* --- Buttons - Saddle Brown --- */
    .stButton > button {
        background-color: #6B4226; /* Saddle Brown */
        color: white !important;
        border-radius: 20px;
        border: 1px solid #B87333; /* COPPER border */
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #B87333; /* COPPER Hover */
        color: #FFFFFF !important; 
        transform: scale(1.02);
    }

    /* --- Sidebar - Deep Evergreen --- */
    [data-testid="stSidebar"] {
        background-color: #1B3A28; /* DARKER GREEN */
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* White text on green */
    }
    
    /* Sidebar specific adjustments */
    [data-testid="stSidebar"] .stMarkdown hr {
        border-color: #B87333; /* Copper divider */
    }

    /* --- Metric Boxes - Wood Brown --- */
    [data-testid="stMetric"] {
        background-color: #6B4226; /* Saddle Brown */
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 0 1px #B87333; /* COPPER outline */
        border-left: 5px solid #B87333; /* COPPER left bar */
        color: white;
    }
    [data-testid="stMetric"] label {
        color: #B87333 !important; /* COPPER Label */
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important; /* Value Color */
    }

    /* --- Tabs --- */
    .stTabs [data-badges="badge"] {
        background-color: #3F5F2A;
        color: #FFFFFF;
    }
    button[aria-selected="true"] {
        background-color: #B87333 !important; /* COPPER active tab */
        color: #FFFFFF !important;
        border-bottom: 2px solid #6B4226;
    }

    /* --- Expander --- */
    .streamlit-expanderHeader {
        background-color: #6B4226 !important; /* Saddle Brown */
        border-radius: 10px;
        border-left: 5px solid #B87333; /* COPPER left bar */
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* --- Input Fields --- */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
        background-color: #3F5F2A !important; /* Green input bg */
        color: #FFFFFF !important;
        border: 1px solid #B87333; /* COPPER border */
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA (Updated Structure) ---
UK_PLANTS = {
    "edible": [
        # --- ORIGINAL & BATCH 1 PLANTS ---
        {
            "name": "Wild Garlic",
            "latin_name": "Allium ursinum",
            "category": "Plant",
            "months": ["February", "March", "April", "May", "June"],
            "habitat": "Damp Woodlands, Stream Banks",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Leaves, Flowers, Bulbs",
            "warnings": "Smell is the #1 identifier. If no garlic smell, leave it.",
            "description": "**Identification:** Long, tapered, bright green leaves with a single, pointed tip. Grows in dense carpets in damp woodlands.",
            "id_keys": {"Smell": "Strong garlic scent when crushed (Essential ID)", "Leaves": "Soft, translucent, spear-shaped (lanceolate)", "Flowers": "White, star-shaped, 6 petals in clusters", "Stem": "Triangular (3-cornered) flower stem"},
            "foraging_tips": {"where": "Damp, shaded ancient woodlands, near streams.", "when": "Best in early spring (Feb-April) before flowers fully open.", "sustainable": "Use scissors to cut leaves. Leave the bulb/roots intact for next year.", "danger_zone": "Beware of dense clusters—always inspect leaves individually."},
            "lookalikes": [{"name": "Lily of the Valley", "danger": "POISONOUS", "diff": "Leaves are leathery, darker green, grow in pairs. NO garlic smell."}, {"name": "Lords-and-Ladies", "danger": "POISONOUS", "diff": "Leaves are arrow-shaped and often have dark spots. NO garlic smell."}],
            "confusion_notes": "Do not rely on leaf shape alone. **The Smell Test is mandatory.**"
        },
        {
            "name": "Nettles",
            "latin_name": "Urtica dioica",
            "category": "Plant",
            "months": ["February", "March", "April", "May", "June"],
            "habitat": "Woodlands, Gardens, Hedgerows",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Young Leaves, Shoots",
            "warnings": "Must be cooked to remove sting. Wear gloves!",
            "description": "**Identification:** Jagged leaves, stinging hairs. Grows in dense clusters. **Uses:** Soup, tea, beer.",
            "id_keys": {
                "Touch": "Stings! (Formic Acid)",
                "Leaves": "Jagged, heart-shaped, opposite pairs",
                "Stem": "Green, square, hairy"
            },
            "foraging_tips": {
                "where": "Rich soil, hedgerows, woods.",
                "when": "Best in Spring (Feb-May). Young shoots only.",
                "sustainable": "Cut top leaves. Leave roots for next year.",
                "danger_zone": "Avoid older plants (tough/ gritty). Always cook thoroughly."
            },
            "lookalikes": [
                {"name": "White Dead-Nettle", "danger": "EDIBLE", "diff": "Does NOT sting. White flowers. Square stem."},
                {"name": "Red Dead-Nettle", "danger": "EDIBLE", "diff": "Does NOT sting. Purple flowers. Leaves similar but soft."}
            ],
            "confusion_notes": "Safe. The 'Dead-Nettles' look similar but are soft and edible. If it stings, it's a Nettle (and edible when cooked)."
        },
        {
            "name": "Dandelion",
            "latin_name": "Taraxacum officinale",
            "category": "Plant",
            "months": ["February", "March", "April", "May", "June", "July"],
            "habitat": "Lawns, Fields, Paths",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Leaves, Flowers, Roots",
            "warnings": "Avoid areas with dog waste (fouling). Bitter taste.",
            "description": "**Identification:** Yellow flower, hollow stem with white milky sap, 'Lion's Tooth' leaves. **Uses:** Coffee (roots), Salad (leaves), Wine (flowers).",
            "id_keys": {
                "Flower": "Single yellow flower on hollow stem",
                "Stem": "Hollow, milky white sap",
                "Leaves": "Toothed (Lion's tooth), rosette"
            },
            "foraging_tips": {
                "where": "Lawns, fields, paths.",
                "when": "Leaves (Spring), Flowers (May-Jun), Roots (Autumn).",
                "sustainable": "Pick young leaves for less bitterness. Dig roots with a trowel.",
                "danger_zone": "Avoid roadside verges (pollution) and dog walking areas."
            },
            "lookalikes": [
                {"name": "Cat's Ear", "danger": "EDIBLE", "diff": "Hairy stems and leaves. Dandelion has smooth/hollow stems."},
                {"name": "Hawkbit", "danger": "EDIBLE", "diff": "Flowers on branched stems. Dandelion is single stem."}
            ],
            "confusion_notes": "Safe. Most lookalikes are edible. Identify by the hollow stem and milky sap."
        },
        {
            "name": "Three-Cornered Leek",
            "latin_name": "Allium triquetrum",
            "category": "Plant",
            "months": ["January", "February", "March", "April"],
            "habitat": "Woodlands, Hedgerows, Roadsides",
            "regions": ["England", "Wales"],
            "difficulty": 1,
            "parts": "Leaves, Flowers, Bulbs",
            "warnings": "Invasive species - pick freely! Smells strongly of garlic.",
            "description": "**Identification:** Strap-like leaves with a 'keel' (triangular shape like a boat). White bell flowers. Smells of onion/garlic.",
            "id_keys": {
                "Smell": "Strong Onion/Garlic (Essential)",
                "Stem": "Triangular (3-cornered) cross-section",
                "Flowers": "White, bell-shaped, drooping"
            },
            "foraging_tips": {
                "where": "Damp woodlands, lanes, hedgerows.",
                "when": "Jan - April (Flowers later).",
                "sustainable": "Invasive! Pick as much as you like. Pull bulbs if allowed.",
                "danger_zone": "Confused with Bluebell (Poisonous). Must smell of garlic."
            },
            "lookalikes": [
                {"name": "Bluebell", "danger": "POISONOUS", "diff": "Blue/Pink flowers. NO garlic smell. Round stem."},
                {"name": "Snowdrop", "danger": "INEDIBLE", "diff": "White flowers but single. NO garlic smell."}
            ],
            "confusion_notes": "Critical: If it does NOT smell of garlic/onion, do not eat. Bluebell is poisonous."
        },
        {
            "name": "Wood Ear (Jelly Ear)",
            "latin_name": "Auricularia auricula-judae",
            "category": "Fungi",
            "months": ["January", "February", "November", "December"],
            "habitat": "Woodlands (Elder trees)",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Fungus",
            "warnings": "Must be cooked. Raw can cause itchiness. Check for bugs inside.",
            "description": "**Identification:** Brown, jelly-like, ear-shaped fungus. Grows specifically on Elder branches.",
            "id_keys": {
                "Texture": "Jelly-like, rubbery, gelatinous",
                "Shape": "Ear-shaped, cup-shaped",
                "Habitat": "ALWAYS on Elder trees (Sambucus nigra)"
            },
            "foraging_tips": {
                "where": "Dead/dying Elder branches in damp woods.",
                "when": "Best in Winter (Jan-Feb, Nov-Dec).",
                "sustainable": "Cut with a knife. Leave small ones.",
                "danger_zone": "Avoid if very dry/hard. Rehydrate in water before cooking."
            },
            "lookalikes": [
                {"name": "Other Tree Fungi", "danger": "VARIES", "diff": "Most other fungi on trees are harder/bracket shaped. Wood Ear is unique gelatinous texture."}
            ],
            "confusion_notes": "Safe. If it looks like an ear and feels like jelly, it is likely Wood Ear. Does NOT grow on the ground."
        },
        {
            "name": "Sorrel",
            "latin_name": "Rumex acetosa",
            "category": "Plant",
            "months": ["April", "May", "June", "July"],
            "habitat": "Grassland, Meadows, Gardens",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Leaves",
            "warnings": "Contains Oxalic Acid. Eat in moderation. Avoid if kidney issues.",
            "description": "**Identification:** Arrow-shaped leaves, sharp lemon taste. Tall reddish flower spikes.",
            "id_keys": {
                "Taste": "Sharp Lemon (Pop-rocks sensation)",
                "Leaves": "Arrow-shaped, pointed tips",
                "Flowers": "Red/Pink spikes"
            },
            "foraging_tips": {
                "where": "Grasslands, meadows, garden lawns.",
                "when": "Spring - Summer.",
                "sustainable": "Pick outer leaves. Leave centre for regrowth.",
                "danger_zone": "Don't eat huge bowls raw (kidney stones risk). Cooks down well."
            },
            "lookalikes": [
                {"name": "Lords and Ladies", "danger": "POISONOUS", "diff": "Arrow leaves but with spots/flowers. BURNS the mouth (No lemon taste)."}
            ],
            "confusion_notes": "Safe. Identified by the strong lemon taste. If it burns or has no taste, it is NOT Sorrel."
        },
        {
            "name": "Elderflower",
            "latin_name": "Sambucus nigra",
            "category": "Tree",
            "months": ["June", "July"],
            "habitat": "Hedgerows, Woods, Scrub",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Flowers",
            "warnings": "Do not confuse with Dwarf Elder (Sambucus ebulus). Cook flowers gently.",
            "description": "**Identification:** Creamy-white flat flower heads (umbels). Sweet summery smell. Bark is warty.",
            "id_keys": {
                "Flowers": "Flat, creamy-white clusters (Umbels)",
                "Smell": "Sweet, summery, floral",
                "Leaves": "Opposite pairs, feather-shaped"
            },
            "foraging_tips": {
                "where": "Hedgerows, woods, gardens.",
                "when": "June - July.",
                "sustainable": "Leave plenty for berries (Autumn). Don't strip the tree.",
                "danger_zone": "Don't wash - keeps the pollen (flavour). Check for bugs."
            },
            "lookalikes": [
                {"name": "Hemlock", "danger": "DEADLY", "diff": "Purple spots on stem. Smells of mouse urine. Elder has woody bark."},
                {"name": "Cow Parsley", "danger": "EDIBLE", "diff": "Flatter clusters. Hairy stem. Elder flowers are droopier."}
            ],
            "confusion_notes": "Critical: Check the stem. Hemlock has purple spots. Elder is woody and bark-like."
        },
        {
            "name": "Blackberries",
            "latin_name": "Rubus fruticosus",
            "category": "Shrub",
            "months": ["August", "September"],
            "habitat": "Hedgerows, Woods, Roadsides",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Berries",
            "warnings": "Watch for thorns. Avoid picking from exhaust fumes (busy roads).",
            "description": "**Identification:** Bramble with thorns. Dark purple/black aggregate berries.",
            "id_keys": {
                "Fruit": "Black, many small drupelets (bumpy)",
                "Stem": "Thorny (bramble), arching",
                "Leaves": "5 leaflets, toothed"
            },
            "foraging_tips": {
                "where": "Hedgerows, woods, waste ground.",
                "when": "August - September.",
                "sustainable": "Pick freely. Invasive habits.",
                "danger_zone": "Wear long sleeves (thorns). Check for maggots inside berry."
            },
            "lookalikes": [
                {"name": "Dewberry", "danger": "EDIBLE", "diff": "Blue-white bloom, few drupelets. Lower growing."}
            ],
            "confusion_notes": "Safe. No dangerous lookalikes in UK. All blackberry-like fruits are edible."
        },
        {
            "name": "Rosehips",
            "latin_name": "Rosa canina",
            "category": "Shrub",
            "months": ["September", "October", "November", "December"],
            "habitat": "Hedgerows, Scrub",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Fruit (Hip)",
            "warnings": "Seeds inside have irritating hairs (itchy powder). Must be removed/filtered.",
            "description": "**Identification:** Red, oval hips on wild rose bushes. Thorny stems.",
            "id_keys": {
                "Fruit": "Red, oval/round hips",
                "Stem": "Thorny, arching",
                "Flowers": "Pink/White (Summer)"
            },
            "foraging_tips": {
                "where": "Hedgerows, coastal scrub.",
                "when": "Late Autumn (after first frost softens them).",
                "sustainable": "Leave some for birds.",
                "danger_zone": "Do not eat raw seeds (itchy throat). Boil and strain for syrup/tea."
            },
            "lookalikes": [
                {"name": "None", "danger": "SAFE", "diff": "Distinctive red hips. No dangerous lookalikes."}
            ],
            "confusion_notes": "Safe. Ensure not harvested from sprayed roadsides."
        },
        {
            "name": "Hawthorn",
            "latin_name": "Crataegus monogyna",
            "category": "Tree",
            "months": ["September", "October"],
            "habitat": "Hedgerows, Woods",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Berries (Haws)",
            "warnings": "Pips contain cyanide precursors. Don't eat seeds in bulk.",
            "description": "**Identification:** Thorny shrub. Lobed leaves (like oak). Red berries (Haws).",
            "id_keys": {
                "Fruit": "Deep red berries (Haws)",
                "Leaves": "Lobed (oak-like)",
                "Thorns": "Sharp, long thorns"
            },
            "foraging_tips": {
                "where": "Hedgerows, fields, woods.",
                "when": "September - October.",
                "sustainable": "Common. Pick berries only.",
                "danger_zone": "Eat raw in moderation. Good for ketchup/jellies."
            },
            "lookalikes": [
                {"name": "None", "danger": "SAFE", "diff": "Distinctive thorny bush with red berries."}
            ],
            "confusion_notes": "Safe. Look for 'May' flower in spring to identify."
        },
        {
            "name": "Chanterelle",
            "latin_name": "Cantharellus cibarius",
            "category": "Fungi",
            "months": ["July", "August", "September"],
            "habitat": "Woodlands (Mossy areas)",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Whole mushroom",
            "warnings": "EXPERT LEVEL ID. Check gills (ridges) and smell.",
            "description": "**Identification:** Egg-yolk yellow. False gills (ridges). Smells of apricots. Meaty texture.",
            "id_keys": {
                "Gills": "FALSE gills (Ridges), forked, running down stem",
                "Smell": "Apricots (Distinct!)",
                "Colour": "Egg-yolk yellow (fades to white in age)"
            },
            "foraging_tips": {
                "where": "Mossy woodland floors, near oak/beech.",
                "when": "July - September.",
                "sustainable": "Cut stem (don't pull). Leave small ones.",
                "danger_zone": "Do not confuse with False Chanterelle or Jack O'Lantern."
            },
            "lookalikes": [
                {"name": "False Chanterelle", "danger": "INEDIBLE", "diff": "True gills (thin sheets). No apricot smell. Orange centre."},
                {"name": "Jack O'Lantern", "danger": "POISONOUS", "diff": "Grows in clumps on wood (Chanterelle on ground). Glows in dark."}
            ],
            "confusion_notes": "Critical: If it has true gills (thin blades), it is NOT a Chanterelle."
        },
        {
            "name": "Field Mushroom",
            "latin_name": "Agaricus campestris",
            "category": "Fungi",
            "months": ["August", "September", "October"],
            "habitat": "Fields, Meadows, Parks",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Whole mushroom",
            "warnings": "EXPERT CHECK. Check gills (Pink -> Brown) and stain (White/Yellow).",
            "description": "**Identification:** White cap, pink gills turning brown with age. White stem (ring).",
            "id_keys": {
                "Gills": "Pink (young) -> Brown (old)",
                "Stem": "White, short, ring present",
                "Smell": "Mushroomy, pleasant"
            },
            "foraging_tips": {
                "where": "Open fields, grassland, lawns.",
                "when": "Late Summer - Autumn.",
                "sustainable": "Cut stem. Leave small ones.",
                "danger_zone": "Beware of Yellow Stainer (Poisonous) and Death Cap (Deadly)."
            },
            "lookalikes": [
                {"name": "Yellow Stainer", "danger": "POISONOUS", "diff": "Stains BRIGHT YELLOW when bruised. Smells of ink/chemicals."},
                {"name": "Death Cap", "danger": "DEADLY", "diff": "White gills (never pink). Volva (cup) at base. Skirt on stem."}
            ],
            "confusion_notes": "Critical: If it stains bright yellow, do not eat. If gills are white, do not eat."
        },
        {
            "name": "Hazelnut",
            "latin_name": "Corylus avellana",
            "category": "Tree",
            "months": ["September", "October"],
            "habitat": "Hedgerows, Woods",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Nuts",
            "warnings": "Ripe nuts are delicious. Green hazelnuts (early) are tasty too.",
            "description": "**Identification:** Shrubby tree. Round/oval nuts in a leafy green husk.",
            "id_keys": {
                "Nut": "In a leafy green husk (Cobnut)",
                "Leaves": "Rounded, hairy, toothed",
                "Bush": "Multi-stemmed shrub"
            },
            "foraging_tips": {
                "where": "Hedgerows, woods, scrub.",
                "when": "September (Ripe). August (Green).",
                "sustainable": "Pick ripe ones. Leave green ones to mature (if late).",
                "danger_zone": "Race against squirrels!"
            },
            "lookalikes": [
                {"name": "Cobnut/Filbert", "danger": "EDIBLE", "diff": "Cultivated varieties. Longer husk."}
            ],
            "confusion_notes": "Safe. Look for the leafy 'hat' on the nut."
        },
        {
            "name": "Sweet Chestnut",
            "latin_name": "Castanea sativa",
            "category": "Tree",
            "months": ["October", "November"],
            "habitat": "Woodlands, Parks",
            "regions": ["England", "Wales"],
            "difficulty": 1,
            "parts": "Nuts",
            "warnings": "Do not confuse with Horse Chestnut (Conkers). Roast well.",
            "description": "**Identification:** Large tree. Long, toothed leaves. Nuts in VERY spiky cases.",
            "id_keys": {
                "Case": "Very spiky (like a sea urchin), many nuts inside",
                "Nut": "Pointed, triangular shape",
                "Leaves": "Long, toothed"
            },
            "foraging_tips": {
                "where": "Woodlands, parks. Often planted.",
                "when": "October - November.",
                "sustainable": "Gather fallen nuts.",
                "danger_zone": "Score shell before roasting or they explode!"
            },
            "lookalikes": [
                {"name": "Horse Chestnut", "danger": "POISONOUS", "diff": "WARTY/SMOOTH case (conkers). Sweet chestnut has LONG SPIKES."}
            ],
            "confusion_notes": "Critical: Horse Chestnut (Conkers) has a smooth/warty case. Sweet Chestnut has a spiky case."
        },
        {
            "name": "Pine Needles",
            "latin_name": "Pinus sylvestris",
            "category": "Tree",
            "months": ["January", "February", "December"],
            "habitat": "Woodlands, Plantations",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Needles",
            "warnings": "Avoid Yew (flat needles). Pine has ROUND needles bundles.",
            "description": "**Identification:** Long needles in bundles (2-3). Evergreen tree. Smells of resin. **Uses:** Tea, rich in Vitamin C.",
            "id_keys": {
                "Needles": "Long, ROUND, in bundles (2-3)",
                "Smell": "Pine resin (Christmas tree)",
                "Tree": "Evergreen conifer"
            },
            "foraging_tips": {
                "where": "Pine forests, plantations.",
                "when": "Year round (best in spring).",
                "sustainable": "Pick small handfuls. Don't strip branches.",
                "danger_zone": "Do not pick Yew (Deadly). Yew needles are FLAT. Pine needles are ROUND."
            },
            "lookalikes": [
                {"name": "Yew", "danger": "POISONOUS", "diff": "Flat needles (not round bundles). No smell/resin. Red berries."}
            ],
            "confusion_notes": "Critical: Pine needles are round and in bundles. Yew needles are flat and toxic."
        },

        # --- BATCH 1 ADDITIONS (Trees, Coastal, Fungi) ---
        {
            "name": "Silver Birch",
            "latin_name": "Betula pendula",
            "category": "Tree",
            "months": ["March", "April"],
            "habitat": "Woodlands, Heathland",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Sap",
            "warnings": "Requires tapping (drilling). Seal hole afterwards.",
            "description": "**Identification:** White peeling bark, triangular leaves. Graceful weeping shape.",
            "id_keys": {
                "Bark": "White, peeling papery layers",
                "Leaves": "Triangular, toothed",
                "Shape": "Graceful, weeping branches"
            },
            "foraging_tips": {
                "where": "Woodlands, heaths, gardens.",
                "when": "Spring (March-April) for sap.",
                "sustainable": "Drill small hole, insert tap/spile. Plug hole with wax/wood after.",
                "danger_zone": "Do not fell tree. Tap healthy trees only."
            },
            "lookalikes": [
                {"name": "Downy Birch", "danger": "EDIBLE", "diff": "Hairy leaves. Darker bark. Also edible sap."}
            ],
            "confusion_notes": "Safe. Identify by white bark. Do not tap diseased trees."
        },
        {
            "name": "Beech Leaves",
            "latin_name": "Fagus sylvatica",
            "category": "Tree",
            "months": ["April", "May", "June"],
            "habitat": "Woodlands, Parks",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Young leaves",
            "warnings": "Eat only young leaves (transparent). Older leaves are tough.",
            "description": "**Identification:** Oval leaves with wavy edges, soft hairs. Smooth grey bark.",
            "id_keys": {
                "Leaves": "Oval, wavy edges, soft hairs (when young)",
                "Texture": "Translucent when young",
                "Bark": "Smooth, grey (Elephant skin)"
            },
            "foraging_tips": {
                "where": "Deciduous woodlands, parks.",
                "when": "April - June (Young).",
                "sustainable": "Pick only lower leaves. Leave canopy.",
                "danger_zone": "Beech nuts (Autumn) are edible but high tannins (bitter)."
            },
            "lookalikes": [
                {"name": "None", "danger": "SAFE", "diff": "Distinctive oval leaves and smooth bark."}
            ],
            "confusion_notes": "Safe. One of the best tree leaves for salads."
        },
        {
            "name": "Marsh Samphire",
            "latin_name": "Salicornia europaea",
            "category": "Coastal",
            "months": ["June", "July", "August", "September"],
            "habitat": "Coastal Saltmarshes",
            "regions": ["Coastal"],
            "difficulty": 1,
            "parts": "Stems",
            "warnings": "Avoid pulling roots. Cut stems. Wash thoroughly.",
            "description": "**Identification:** Green, fleshy, jointed stems (like tiny cacti without spines). Turns red in autumn.",
            "id_keys": {
                "Stem": "Fleshy, green, jointed segments",
                "Habitat": "Muddy saltmarshes (Wet feet)",
                "Texture": "Crunchy, juicy"
            },
            "foraging_tips": {
                "where": "Coastal saltmarshes, estuaries.",
                "when": "June - September.",
                "sustainable": "Cut top 2 inches. Leave roots.",
                "danger_zone": "Wash in fresh water to remove salt/mud. Cook quickly (steam/blanch)."
            },
            "lookalikes": [
                {"name": "None", "danger": "SAFE", "diff": "Very distinctive. No dangerous lookalikes."}
            ],
            "confusion_notes": "Safe. Known as 'Sea Asparagus'. Do not confuse with unrelated upland plants."
        },
        {
            "name": "Sea Kale",
            "latin_name": "Crambe maritima",
            "category": "Coastal",
            "months": ["May", "June", "July"],
            "habitat": "Shingle Beaches, Coasts",
            "regions": ["Coastal"],
            "difficulty": 2,
            "parts": "Young shoots, leaves",
            "warnings": "Rare in some areas. Check local protection laws. Pick sparingly.",
            "description": "**Identification:** Large blue-green crinkled leaves. White flowers. Grows on shingle.",
            "id_keys": {
                "Leaves": "Blue-green, waxy, crinkled",
                "Habitat": "Shingle/sand beaches",
                "Flowers": "White, 4 petals"
            },
            "foraging_tips": {
                "where": "Shingle beaches, coasts.",
                "when": "Spring (May - July).",
                "sustainable": "Pick one leaf per plant. Do not uproot.",
                "danger_zone": "Do not pick from protected shores."
            },
            "lookalikes": [
                {"name": "None dangerous", "danger": "SAFE", "diff": "Garden Cabbage does not grow on shingle."}
            ],
            "confusion_notes": "Safe but protected. Identify by habitat and blue-green waxy leaves."
        },
        {
            "name": "Dulse",
            "latin_name": "Palmaria palmata",
            "category": "Seaweed",
            "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "habitat": "Rocky Coasts",
            "regions": ["Coastal"],
            "difficulty": 1,
            "parts": "Whole frond",
            "warnings": "Wash thoroughly. Check water quality notices (pollution).",
            "description": "**Identification:** Dark red/purple, hand-shaped (palmate) fronds. Leathery texture.",
            "id_keys": {
                "Colour": "Dark red / purple",
                "Shape": "Hand-shaped, broad fronds (split into fingers)",
                "Texture": "Leathery, tough"
            },
            "foraging_tips": {
                "where": "Rocky shores, attached to rocks.",
                "when": "Year round (best in Spring).",
                "sustainable": "Cut with scissors. Leave holdfast (root).",
                "danger_zone": "Eat raw or dried. Good 'bacon' substitute when fried."
            },
            "lookalikes": [
                {"name": "Other Seaweeds", "danger": "VARIES", "diff": "Most are edible but check ID. Dulse is distinctively red and hand-shaped."}
            ],
            "confusion_notes": "Safe. Very distinct shape. Avoid wire-like seaweeds."
        },
        {
            "name": "Cockles",
            "latin_name": "Cerastoderma edule",
            "category": "Shellfish",
            "months": ["September", "October", "November", "December", "January", "April"],
            "habitat": "Sandy/Muddy Beaches, Estuaries",
            "regions": ["Coastal"],
            "difficulty": 2,
            "parts": "Meat",
            "warnings": "Must be cooked thoroughly. Avoid during 'Red Tides' (algal blooms). Check water quality notices.",
            "description": "**Identification:** Symmetrical, heart-shaped shell with radiating ribs (ridges). Burrows in sand.",
            "id_keys": {
                "Shell": "Ridged (radiating ribs), symmetrical",
                "Shape": "Heart shape when viewed from side",
                "Size": "2-4cm"
            },
            "foraging_tips": {
                "where": "Sandy/muddy beaches, estuaries. Look for tiny holes in sand.",
                "when": "Months with an 'r' (Sept-April). Avoid summer breeding season.",
                "sustainable": "Rake gently. Return small ones.",
                "danger_zone": "Must be cooked. Do not eat raw. Check local pollution/red tide warnings."
            },
            "lookalikes": [
                {"name": "None dangerous", "danger": "SAFE", "diff": "Distinctive ribbed shell. Other clams look similar but are edible."}
            ],
            "confusion_notes": "Safe. Identify by the ribbed shell and heart shape."
        },
        {
            "name": "Morel",
            "latin_name": "Morchella esculenta",
            "category": "Fungi",
            "months": ["March", "April", "May"],
            "habitat": "Woodlands, Gardens, Disturbed Ground",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Whole mushroom",
            "warnings": "MUST BE COOKED. Raw is toxic. Expert ID required.",
            "description": "**Identification:** Honeycomb cap (pitted). Hollow inside. Cream stem.",
            "id_keys": {
                "Cap": "Honeycomb texture (Pits, not wrinkles)",
                "Inside": "Completely hollow (like a balloon)",
                "Stem": "Hollow, cream/white"
            },
            "foraging_tips": {
                "where": "Woodlands, disturbed soil, bark mulch.",
                "when": "Spring (March - May).",
                "sustainable": "Cut stem. Leave small ones.",
                "danger_zone": "Cook thoroughly (10 mins). Never eat raw."
            },
            "lookalikes": [
                {"name": "False Morel", "danger": "POISONOUS", "diff": "Brain-like cap (wrinkled, NOT pits). NOT hollow inside (Chambered)."}
            ],
            "confusion_notes": "Critical: If it is NOT hollow, it is NOT a Morel."
        },

        {
            "name": "Lime (Leaves)",
            "latin_name": "Tilia cordata",
            "category": "Tree",
            "months": ["April", "May", "June", "July"],
            "habitat": "Woodlands, Parks",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Young leaves",
            "warnings": "Older leaves are tough and can be a choking hazard.",
            "description": "**Identification:** Heart-shaped leaves, slightly serrated edges. **Uses:** Excellent salad green (mild, slightly sweet).",
            "id_keys": {
                "Leaves": "Heart-shaped, hairless on top",
                "Bark": "Smooth, grey",
                "Flowers": "Yellow-white clusters"
            },
            "foraging_tips": {
                "where": "Woodlands and parks. Look for low branches.",
                "when": "Best in Spring (April-June) when leaves are young.",
                "sustainable": "Pick a few leaves from each branch, do not strip.",
                "danger_zone": "Safe. No dangerous lookalikes."
            },
            "lookalikes": [
                {
                    "name": "None dangerous",
                    "danger": "SAFE",
                    "diff": "Common Lime is a hybrid. All Lime trees have edible leaves."
                }
            ],
            "confusion_notes": "Safe. One of the best tree leaves for eating."
        },
        {
            "name": "Oak (Acorns)",
            "latin_name": "Quercus robur",
            "category": "Tree",
            "months": ["September", "October", "November"],
            "habitat": "Woodlands, Hedgerows",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Nuts (Acorns)",
            "warnings": "MUST BE LEACHED (soaked) to remove tannins. Very bitter raw.",
            "description": "**Identification:** Lobed leaves (like a curved hand). Acorns in rough cups.",
            "id_keys": {
                "Leaves": "Lobed (wavy edges)",
                "Fruit": "Acorn in a rough cup",
                "Bark": "Rough, ridged"
            },
            "foraging_tips": {
                "where": "Woodlands, Hedgerows.",
                "when": "Autumn.",
                "sustainable": "Take only what you need; wildlife depend on them.",
                "danger_zone": "Raw acorns cause stomach upset due to tannins. Must be leached in running water."
            },
            "lookalikes": [
                {
                    "name": "Sessile Oak",
                    "danger": "EDIBLE",
                    "diff": "Sessile Oak acorns have shorter stalks. Both are edible."
                }
            ],
            "confusion_notes": "Safe if processed. Tannins cause stomach upset if eaten raw."
        },
        {
            "name": "Wild Strawberry",
            "latin_name": "Fragaria vesca",
            "category": "Plant",
            "months": ["June", "July", "August"],
            "habitat": "Woodlands, Grassland",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Berries, Leaves",
            "warnings": "Small yield but intense flavour.",
            "description": "**Identification:** Low growing, trifoliate leaves (3 leaflets), small red berries pointing upwards.",
            "id_keys": {
                "Leaves": "3 leaflets, toothed",
                "Flowers": "White, 5 petals",
                "Fruit": "Small, red, seeds on outside"
            },
            "foraging_tips": {
                "where": "Woodlands, grassland, tracks.",
                "when": "Summer.",
                "sustainable": "Pick ripe berries only.",
                "danger_zone": "Ensure correct identification to avoid Barren Strawberry."
            },
            "lookalikes": [
                {
                    "name": "Barren Strawberry",
                    "danger": "INEDIBLE",
                    "diff": "Barren Strawberry has petals with gaps between them. Wild Strawberry petals overlap."
                }
            ],
            "confusion_notes": "Confused with Barren Strawberry. **Key Diff:** Barren Strawberry has petals spaced apart (gaps show). Wild Strawberry petals overlap."
        },
        {
            "name": "Bilberry (Whortleberry)",
            "latin_name": "Vaccinium myrtillus",
            "category": "Shrub",
            "months": ["July", "August"],
            "habitat": "Moorland, Acid Soils",
            "regions": ["North", "Wales", "Scotland"],
            "difficulty": 2,
            "parts": "Berries",
            "warnings": "Stains fingers/teeth blue! Difficult to wash out.",
            "description": "**Identification:** Small deciduous shrub, blue-black berries (solo, not in clusters).",
            "id_keys": {
                "Berries": "Blue-black, soft, bloom",
                "Leaves": "Small, oval, finely toothed",
                "Habitat": "High moors"
            },
            "foraging_tips": {
                "where": "High moors, acid soils.",
                "when": "Late Summer.",
                "sustainable": "Pick sparingly; birds rely on them.",
                "danger_zone": "CRITICAL: Do not confuse with Deadly Nightshade. Bilberry is a LOW shrub."
            },
            "lookalikes": [
                {
                    "name": "Deadly Nightshade",
                    "danger": "POISONOUS",
                    "diff": "Nightshade is a tall leafy plant with large shiny black berries. Bilberry is a low shrub with small berries."
                }
            ],
            "confusion_notes": "Confused with Deadly Nightshade. **Key Diff:** Nightshade is a tall plant with large shiny black berries. Bilberry is a low shrub with small berries."
        },
        {
            "name": "Meadowsweet",
            "latin_name": "Filipendula ulmaria",
            "category": "Plant",
            "months": ["June", "July", "August"],
            "habitat": "Damp Meadows, Riverbanks",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Flowers, Leaves",
            "warnings": "Contains aspirin-like compounds. Avoid if allergic to aspirin.",
            "description": "**Identification:** Tall, frothy cream-white flower heads. Smells of almond/honey.",
            "id_keys": {
                "Flowers": "Cream, frothy clusters",
                "Smell": "Almond/Honey scent",
                "Leaves": "Compound, white underside"
            },
            "foraging_tips": {
                "where": "Damp meadows, riverbanks.",
                "when": "Summer.",
                "sustainable": "Pick flower heads, leave plenty for pollinators.",
                "danger_zone": "Avoid if allergic to aspirin (salicylates)."
            },
            "lookalikes": [
                {
                    "name": "Dropwort",
                    "danger": "POISONOUS",
                    "diff": "Dropwort grows on DRY ground. Meadowsweet loves DAMP ground."
                }
            ],
            "confusion_notes": "Confused with Dropwort. **Key Diff:** Dropwort is usually on dry ground. Meadowsweet loves damp ground and smells sweet."
        },
        {
            "name": "Chickweed",
            "latin_name": "Stellaria media",
            "category": "Plant",
            "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "habitat": "Gardens, Waste Ground",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Leaves, Stems",
            "warnings": "Eat raw or cooked. Very mild.",
            "description": "**Identification:** Low growing, small white star flowers, line of hairs on stem.",
            "id_keys": {
                "Stem": "Line of fine hairs (distinctive feature)",
                "Flowers": "Tiny white stars",
                "Leaves": "Oval, opposite pairs"
            },
            "foraging_tips": {
                "where": "Gardens, waste ground, fertile soil.",
                "when": "Year-round.",
                "sustainable": "Common weed, harvest freely.",
                "danger_zone": "Safe. Check for dog fouling in urban areas."
            },
            "lookalikes": [
                {
                    "name": "Mouse-ear Chickweed",
                    "danger": "EDIBLE",
                    "diff": "Mouse-ear is hairy and tough. Chickweed has a line of hairs on one side only."
                }
            ],
            "confusion_notes": "Safe. Very common weed. Hairy mouse-ear chickweed is edible but texture is rough."
        },
        {
            "name": "Sea Purslane",
            "latin_name": "Halimione portulacoides",
            "category": "Coastal",
            "months": ["May", "June", "July", "August", "September"],
            "habitat": "Coastal Saltmarsh, Shingle",
            "regions": ["Coastal"],
            "difficulty": 1,
            "parts": "Leaves",
            "warnings": "Salty! Use as seasoning.",
            "description": "**Identification:** Grey-green fleshy leaves, woody stems. Grows near Samphire.",
            "id_keys": {
                "Leaves": "Succulent, grey-green, oblong",
                "Stem": "Woody at base",
                "Taste": "Very salty"
            },
            "foraging_tips": {
                "where": "Coastal saltmarsh, shingle.",
                "when": "Spring to Autumn.",
                "sustainable": "Pick sparingly in protected areas.",
                "danger_zone": "Safe. Distinctive grey colour."
            },
            "lookalikes": [
                {
                    "name": "None dangerous",
                    "danger": "SAFE",
                    "diff": "Distinctive grey-green colour and salty taste."
                }
            ],
            "confusion_notes": "Safe. Distinctive grey colour."
        },
        {
            "name": "Burdock (Root)",
            "latin_name": "Arctium lappa",
            "category": "Plant",
            "months": ["September", "October", "November", "December"],
            "habitat": "Hedgerows, Waste Ground",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Root (First year)",
            "warnings": "Requires digging. Look for first-year plants (no burrs/flowers).",
            "description": "**Identification:** Large rhubarb-like leaves, purple thistle-like flowers that turn into sticky burrs.",
            "id_keys": {
                "Leaves": "Large, heart-shaped, rhubarb-like",
                "Flowers": "Purple thistle, sticky burrs",
                "Root": "Long, thin, brown skin"
            },
            "foraging_tips": {
                "where": "Hedgerows, waste ground.",
                "when": "Autumn/Winter (first year roots).",
                "sustainable": "Digging kills the plant. Only dig where abundant.",
                "danger_zone": "Only eat roots from first-year plants (those without flowers/burrs)."
            },
            "lookalikes": [
                {
                    "name": "None dangerous",
                    "danger": "SAFE",
                    "diff": "Large leaves and sticky burrs are distinctive."
                }
            ],
            "confusion_notes": "Safe. Identify by the large leaves and sticky burrs. Only eat roots from first-year plants."
        },
        {
            "name": "Pignut",
            "latin_name": "Bunium bulbocastanum",
            "category": "Plant",
            "months": ["May", "June", "July"],
            "habitat": "Grassland, Meadows",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "Tubers",
            "warnings": "Dig carefully. Distinctive nutty taste.",
            "description": "**Identification:** Delicate plant with fine, feathery leaves (like carrot). Small white flower umbels.",
            "id_keys": {
                "Leaves": "Feathery, carrot-like, delicate",
                "Flowers": "White umbels",
                "Root": "Small tuber, brown/black skin"
            },
            "foraging_tips": {
                "where": "Dry meadows, grassland.",
                "when": "Late Spring/Summer.",
                "sustainable": "Dig carefully, refill holes.",
                "danger_zone": "CRITICAL: Check ground is DRY. Hemlock Water Dropwort (Deadly) grows in WET ground."
            },
            "lookalikes": [
                {
                    "name": "Hemlock Water Dropwort",
                    "danger": "DEADLY",
                    "diff": "Dropwort grows in WET ground/ditches. Pignut grows in DRY meadows."
                }
            ],
            "confusion_notes": "CRITICAL: Confused with Hemlock Water Dropwort. **Key Diff:** Pignut grows in DRY meadows. Dropwort grows in WET ground/ditches. If feet are wet, stop digging."
        },
        {
            "name": "Sloe (Blackthorn)",
            "latin_name": "Prunus spinosa",
            "category": "Shrub",
            "months": ["September", "October", "November"],
            "habitat": "Hedgerows",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Berries",
            "warnings": "Very bitter raw! Best after frost or frozen.",
            "description": "**Identification:** Small blue-black berries with a white 'bloom'. Large thorns on black branches.",
            "id_keys": {
                "Fruit": "Small, blue-black, sour",
                "Stem": "Black bark, large sharp thorns",
                "Bush": "Dense, thicket-forming"
            },
            "foraging_tips": {
                "where": "Hedgerows.",
                "when": "Autumn (after frost).",
                "sustainable": "Leave plenty for birds.",
                "danger_zone": "Thorns are sharp and can cause infection."
            },
            "lookalikes": [
                {
                    "name": "Bullace",
                    "danger": "EDIBLE",
                    "diff": "Bullace is larger and less thorny."
                },
                {
                    "name": "Damson",
                    "danger": "EDIBLE",
                    "diff": "Damson is larger and less thorny."
                }
            ],
            "confusion_notes": "Safe. Bullace and Damson are larger and less thorny. All are edible."
        },
        {
            "name": "Crab Apple",
            "latin_name": "Malus sylvestris",
            "category": "Tree",
            "months": ["September", "October"],
            "habitat": "Woodlands, Hedgerows",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Fruit",
            "warnings": "Very tart/sour. Best for jams/jellies.",
            "description": "**Identification:** Small, round apples (golf ball size). Yellow/Green/Red. Often spiky look.",
            "id_keys": {
                "Fruit": "Small apples, long stalks",
                "Taste": "Very sour, dry mouth",
                "Leaves": "Oval, serrated"
            },
            "foraging_tips": {
                "where": "Woodlands, hedgerows.",
                "when": "Autumn.",
                "sustainable": "Use fallen fruit or pick sparingly.",
                "danger_zone": "Very tart. May cause stomach upset if eaten raw in quantity."
            },
            "lookalikes": [
                {
                    "name": "Cultivated Apples",
                    "danger": "EDIBLE",
                    "diff": "Cultivated apples are larger and sweeter."
                }
            ],
            "confusion_notes": "Safe. Confused with eating apples. Crab Apples are smaller and sourer."
        },
        {
            "name": "Wood Blewit",
            "latin_name": "Clitocybe nuda",
            "category": "Fungi",
            "months": ["September", "October", "November", "December"],
            "habitat": "Woodlands, Gardens",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Whole mushroom",
            "warnings": "Must be cooked. Some people have allergic reaction.",
            "description": "**Identification:** Lilac/Purple cap fading to tan. Lilac gills. Bulbous stem.",
            "id_keys": {
                "Cap": "Lilac turning tan",
                "Gills": "Lilac, crowded",
                "Stem": "Thick, bulbous, lilac"
            },
            "foraging_tips": {
                "where": "Woodlands, gardens (leaf litter).",
                "when": "Autumn.",
                "sustainable": "Cut at base, leave mycelium.",
                "danger_zone": "Must be cooked. Can cause allergic reaction in some people."
            },
            "lookalikes": [
                {
                    "name": "Lilac Fibrecap",
                    "danger": "POISONOUS",
                    "diff": "Fibrecap grows in GRASS. Blewit grows on WOOD/LEAVES."
                }
            ],
            "confusion_notes": "Confused with Lilac Fibrecap. **Key Diff:** Wood Blewit has a bulbous stem and grows on wood/leaves. Fibrecap grows in grass."
        },
        {
            "name": "Alexanders",
            "latin_name": "Smyrnium olusatrum",
            "category": "Coastal",
            "months": ["March", "April", "May"],
            "habitat": "Coastal, Hedgerows (near sea)",
            "regions": ["Coastal"],
            "difficulty": 2,
            "parts": "Stems, Roots, Flower buds",
            "warnings": "Seasonal - best in Spring.",
            "description": "**Identification:** Tall plant, yellow-green flowers, shiny green leaves. Smells of celery/parsley.",
            "id_keys": {
                "Stem": "Solid, green (not hollow like hemlock)",
                "Flowers": "Yellow-green umbels",
                "Smell": "Celery-like"
            },
            "foraging_tips": {
                "where": "Coastal hedgerows, near sea.",
                "when": "Spring.",
                "sustainable": "Common on coast, rarer inland.",
                "danger_zone": "Check for purple spotted stems (Hemlock)."
            },
            "lookalikes": [
                {
                    "name": "Hemlock",
                    "danger": "POISONOUS",
                    "diff": "Hemlock has purple spots on stem and smells of mouse urine. Alexanders is green and smells of celery."
                }
            ],
            "confusion_notes": "Confused with Hemlock. **Key Diff:** Hemlock has purple spots and smells of mouse urine. Alexanders is green, solid-stemmed, and smells like celery."
        }
    ],
    "poisonous": [
        {
            "name": "Deadly Nightshade",
            "latin_name": "Atropa belladonna",
            "category": "Plant",
            "months": ["June", "July", "August", "September"],
            "habitat": "Woodlands, Gardens, Waste Ground",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "All parts (especially berries)",
            "warnings": "EXTREME. Fatal in small doses. Do not handle without gloves.",
            "description": "**Identification:** A tall, bushy perennial. Bell-shaped purple flowers. Shiny black berries the size of cherries. **Danger:** Causes rapid heartbeat, dilated pupils, hallucinations, and death.",
            "id_keys": {
                "Flowers": "Purple, bell-shaped, nodding",
                "Berries": "Shiny black, cherry-sized, solitary",
                "Leaves": "Oval, pointed, large"
            },
            "danger_tips": {
                "where": "Often found in shady, damp woods or calcareous soils.",
                "when": "Berries appear late summer.",
                "sustainable": "Do not pick. Remove carefully if found in gardens.",
                "danger_zone": "EXTREME. Ingestion of 2-3 berries can be fatal to a child."
            },
            "lookalikes": [
                {
                    "name": "Bilberry",
                    "danger": "EDIBLE",
                    "diff": "Bilberry is a low shrub with small, matte blue-black berries. Deadly Nightshade is a tall leafy plant with large shiny black berries."
                }
            ],
            "confusion_notes": "Confused with Bilberry. **Key Diff:** Bilberry is a low shrub with small blue berries. Nightshade is a large leafy plant with cherry-sized berries."
        },
        {
            "name": "Foxglove",
            "latin_name": "Digitalis purpurea",
            "category": "Plant",
            "months": ["June", "July", "August"],
            "habitat": "Gardens, Woodlands, Acid Soils",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "All parts",
            "warnings": "HIGH. Can cause heart failure. Toxins can be absorbed through skin.",
            "description": "**Identification:** Tall spikes of pink/purple trumpet flowers. Large, fuzzy leaves at the base. **Danger:** Contains digitalis which affects heart rate.",
            "id_keys": {
                "Flowers": "Pink/Purple trumpets, spotted inside",
                "Stem": "Tall, green, sturdy spike",
                "Leaves": "Large, rosette at base, soft texture"
            },
            "danger_tips": {
                "where": "Common in gardens, woodland clearings, and heaths.",
                "when": "Flowering in summer.",
                "sustainable": "Admire from a distance. Do not touch.",
                "danger_zone": "HIGH. Nausea, vomiting, confusion, heart failure."
            },
            "lookalikes": [
                {
                    "name": "Comfrey",
                    "danger": "EDIBLE",
                    "diff": "Comfrey has bell-shaped flowers that hang in loose clusters. Foxglove flowers are distinct trumpets growing up a single tall spike."
                }
            ],
            "confusion_notes": "Confused with Comfrey. **Key Diff:** Comfrey flowers are smaller bells, usually cream/purple, and leaves are different shape. Foxglove is a distinct tall spike."
        },
        {
            "name": "Hemlock",
            "latin_name": "Conium maculatum",
            "category": "Plant",
            "months": ["April", "May", "June", "July"],
            "habitat": "Rivers, Damp areas, Roadsides",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "All parts",
            "warnings": "EXTREME. Deadliest plant in the UK. Mistaken for wild celery/parsley.",
            "description": "**Identification:** Tall plant (up to 2m). Smooth stem with distinctive purple spots. Smells of mouse urine. **Danger:** Causes respiratory paralysis.",
            "id_keys": {
                "Stem": "Smooth, hollow, purple spots (critical ID)",
                "Smell": "Unpleasant, mouse urine smell when crushed",
                "Flowers": "White umbels (flat-topped clusters)"
            },
            "danger_tips": {
                "where": "Damp ditches, riverbanks, waste ground.",
                "when": "Spring and early summer.",
                "sustainable": "Never cut or smell closely.",
                "danger_zone": "EXTREME. Respiratory failure, death. Toxins can be absorbed through skin."
            },
            "lookalikes": [
                {
                    "name": "Wild Carrot",
                    "danger": "EDIBLE",
                    "diff": "Wild Carrot has HAIRY stems. Hemlock has SMOOTH stems with purple spots."
                },
                {
                    "name": "Cow Parsley",
                    "danger": "EDIBLE",
                    "diff": "Cow Parsley stems are ridged/grooved and green. Hemlock stems are smooth with purple blotches."
                }
            ],
            "confusion_notes": "Confused with Wild Carrot/Cow Parsley. **Key Diff:** Hemlock has SMOOTH/PURPLE-SPOTTED stems and smells bad. Edible lookalikes have HAIRY/GREEN stems."
        },
        {
            "name": "Hemlock Water Dropwort",
            "latin_name": "Oenanthe crocata",
            "category": "Plant",
            "months": ["April", "May", "June", "July"],
            "habitat": "Riverbanks, Wet ground, Ditches",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "All parts (Roots deadliest)",
            "warnings": "EXTREME. 'Dead Man's Fingers'. Rapid death.",
            "description": "**Identification:** Grows in water/wet mud. White flowers. Roots are tuberous, resembling a cluster of pale fingers. **Danger:** Causes seizures and death rapidly.",
            "id_keys": {
                "Root": "Tubers like fingers (Dead Man's Fingers)",
                "Habitat": "Wet ground, feet in water",
                "Stem": "Grooved, hollow"
            },
            "danger_tips": {
                "where": "Riverbanks, streams, wet ditches.",
                "when": "Spring and Summer.",
                "sustainable": "Never dig roots in wet areas.",
                "danger_zone": "EXTREME. Rapid onset seizures, coma, death."
            },
            "lookalikes": [
                {
                    "name": "Wild Parsnip",
                    "danger": "EDIBLE",
                    "diff": "Wild Parsnip has YELLOW flowers. Dropwort has WHITE flowers."
                },
                {
                    "name": "Pignut",
                    "danger": "EDIBLE",
                    "diff": "Pignut grows in DRY meadows. Dropwort grows in WET ground/ditches. If your feet are wet, stop digging."
                }
            ],
            "confusion_notes": "Confused with Wild Parsnip or Pignut. **Key Diff:** Parsnip has yellow flowers. Dropwort has white flowers and 'finger' roots in wet ground."
        },
        {
            "name": "Death Cap",
            "latin_name": "Amanita phalloides",
            "category": "Fungi",
            "months": ["July", "August", "September"],
            "habitat": "Woodlands (especially Oak)",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Whole mushroom",
            "warnings": "EXTREME. Responsible for most mushroom deaths worldwide.",
            "description": "**Identification:** Greenish-yellow cap. White gills. Distinctive white cup (volva) at the base underground. **Danger:** Liver/kidney failure.",
            "id_keys": {
                "Cap": "Green-yellow, sometimes streaked",
                "Gills": "White, free from stem",
                "Base": "Volva (Cup) in ground, ring on stem"
            },
            "danger_tips": {
                "where": "Broadleaf woodland, often under Oak.",
                "when": "Summer and Autumn.",
                "sustainable": "Never pick mushrooms with a volva (cup) at the base.",
                "danger_zone": "EXTREME. Symptoms delayed 6-24 hours. Fatal liver damage."
            },
            "lookalikes": [
                {
                    "name": "Straw Mushroom",
                    "danger": "EDIBLE",
                    "diff": "Straw Mushroom has PINK gills. Death Cap has WHITE gills."
                },
                {
                    "name": "Caesar's Mushroom",
                    "danger": "EDIBLE",
                    "diff": "Caesar's has a bright orange/red cap. Death Cap is green/yellow."
                }
            ],
            "confusion_notes": "Confused with Straw Mushroom. **Key Diff:** Straw Mushroom has PINK gills. Death Cap has WHITE gills and a volva."
        },
        {
            "name": "Lords and Ladies",
            "latin_name": "Arum maculatum",
            "category": "Plant",
            "months": ["March", "April", "May", "August", "September"],
            "habitat": "Hedgerows, Woods",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "All parts",
            "warnings": "HIGH. Causes immediate burning pain and blisters.",
            "description": "**Identification:** Arrow-shaped leaves (often with black spots). Orange-red berries on a spike. **Danger:** Calcium oxalate crystals needle the tongue/throat.",
            "id_keys": {
                "Leaves": "Arrow-shaped, often spotted black",
                "Berries": "Bright orange cluster on a spike",
                "Flower": "Pale green 'hood' (spathe)"
            },
            "danger_tips": {
                "where": "Shady hedgerows and woods.",
                "when": "Leaves in Spring, Berries in Autumn.",
                "sustainable": "Do not touch or taste.",
                "danger_zone": "HIGH. Immediate burning sensation, swelling of throat."
            },
            "lookalikes": [
                {
                    "name": "Sorrel",
                    "danger": "EDIBLE",
                    "diff": "Sorrel leaves are arrow-shaped but smaller, usually unspotted, and taste lemony. Lords & Ladies are large, leathery, and have NO smell."
                },
                {
                    "name": "Wild Garlic",
                    "danger": "EDIBLE",
                    "diff": "Wild Garlic smells strongly of garlic. Lords & Ladies has NO garlic smell and different leaf texture."
                }
            ],
            "confusion_notes": "Confused with Wild Garlic or Sorrel. **Key Diff:** Wild Garlic smells of garlic. Lords & Ladies burns the mouth instantly."
        },
        {
            "name": "Yew",
            "latin_name": "Taxus baccata",
            "category": "Tree",
            "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "habitat": "Churchyards, Gardens, Woodlands",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Needles, Seeds",
            "warnings": "EXTREME. All parts deadly except the red berry flesh.",
            "description": "**Identification:** Dark evergreen tree. Flat, dark green needles. Red fleshy 'berries' (arils) with a dark seed inside. **Danger:** Causes cardiac arrest.",
            "id_keys": {
                "Needles": "Flat, dark green, pointed",
                "Fruit": "Red cup (aril) containing a dark seed",
                "Bark": "Reddish-brown, peeling"
            },
            "danger_tips": {
                "where": "Commonly planted in churchyards and gardens.",
                "when": "Evergreen all year. Berries in Autumn.",
                "sustainable": "Never eat the seed inside the red berry.",
                "danger_zone": "EXTREME. Sudden death, no antidote."
            },
            "lookalikes": [
                {
                    "name": "Pine",
                    "danger": "EDIBLE",
                    "diff": "Pine needles are ROUND and long. Yew needles are FLAT, short, and darker."
                },
                {
                    "name": "Fir",
                    "danger": "EDIBLE",
                    "diff": "Fir needles are flat but attach to the stem like a suction cup. Yew needles are distinct dark green."
                }
            ],
            "confusion_notes": "Confused with Pine/Fir. **Key Diff:** Yew needles are FLAT. Pine needles are ROUND."
        },
        {
            "name": "False Morel",
            "latin_name": "Gyromitra esculenta",
            "category": "Fungi",
            "months": ["March", "April", "May"],
            "habitat": "Woodlands, Sandy Soils",
            "regions": ["All"],
            "difficulty": 3,
            "parts": "Whole mushroom",
            "warnings": "EXTREME. Raw or poorly cooked it is deadly.",
            "description": "**Identification:** Brain-like cap (wrinkled, irregular lobes). NOT hollow inside. **Danger:** Contains gyromitrin (converted to rocket fuel in body).",
            "id_keys": {
                "Cap": "Brain-like, irregular lobes, reddish-brown",
                "Inside": "Chambered (not hollow)",
                "Texture": "Wrinkled, not honeycomb pits"
            },
            "danger_tips": {
                "where": "Coniferous woodlands, sandy soil.",
                "when": "Spring.",
                "sustainable": "Do not pick. Vapours can be toxic when cooking.",
                "danger_zone": "EXTREME. Liver damage, neurological issues."
            },
            "lookalikes": [
                {
                    "name": "Morel",
                    "danger": "EDIBLE",
                    "diff": "True Morel is HOLLOW inside like a balloon. False Morel is CHAMBERED/SOLID inside. True Morel has honeycomb pits; False Morel has brain wrinkles."
                }
            ],
            "confusion_notes": "Confused with True Morel. **Key Diff:** False Morel is NOT hollow. True Morel is hollow like a balloon."
        },
        {
            "name": "Spindle",
            "latin_name": "Euonymus europaeus",
            "category": "Shrub",
            "months": ["August", "September", "October"],
            "habitat": "Hedgerows, Woods",
            "regions": ["All"],
            "difficulty": 1,
            "parts": "Berries, Bark",
            "warnings": "HIGH. Strong laxative, liver damage.",
            "description": "**Identification:** Shrub with distinctive pink berries that split open to reveal orange seeds. Leaves turn red in autumn.",
            "id_keys": {
                "Fruit": "Pink, 4-lobed, orange seeds inside (distinctive)",
                "Leaves": "Opposite, pointed, serrated, turn red",
                "Twigs": "Green, angular"
            },
            "danger_tips": {
                "where": "Hedgerows and woodland edges.",
                "when": "Berries in Autumn.",
                "sustainable": "Admire the colour, do not eat.",
                "danger_zone": "HIGH. Severe stomach upset, liver and kidney damage."
            },
            "lookalikes": [
                {
                    "name": "None dangerous",
                    "danger": "SAFE",
                    "diff": "Distinctive bright pink/orange fruits are unique among common hedgerow plants. No edible plant has this fruit structure."
                }
            ],
            "confusion_notes": "Distinctive pink berries. No common edible lookalike."
        },
        {
            "name": "Woody Nightshade (Bittersweet)",
            "latin_name": "Solanum dulcamara",
            "category": "Plant",
            "months": ["June", "July", "August", "September"],
            "habitat": "Hedgerows, Woods",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "All parts (especially berries)",
            "warnings": "MEDIUM to HIGH. Poisonous, causes vomiting.",
            "description": "**Identification:** Climbing plant. Purple flowers with yellow centre cone. Bright red, egg-shaped berries.",
            "id_keys": {
                "Flowers": "Purple star, yellow cone centre",
                "Berries": "Red, egg-shaped, in clusters",
                "Leaves": "Arrow-shaped, often with basal lobes"
            },
            "danger_tips": {
                "where": "Hedgerows, scrambling over plants.",
                "when": "Flowers summer, berries autumn.",
                "sustainable": "Remove from gardens if children present.",
                "danger_zone": "MEDIUM. Vomiting, dizziness, diarrhoea."
            },
            "lookalikes": [
                {
                    "name": "Deadly Nightshade",
                    "danger": "POISONOUS",
                    "diff": "Deadly Nightshade has BLACK berries and purple/yellow BELL flowers. Woody Nightshade has RED egg berries and purple STAR flowers."
                }
            ],
            "confusion_notes": "Confused with Deadly Nightshade. **Key Diff:** Woody Nightshade has purple flowers (Deadly has purple bells) and red berries are egg-shaped (not shiny black)."
        },
        {
            "name": "White Bryony",
            "latin_name": "Bryonia dioica",
            "category": "Plant",
            "months": ["August", "September", "October"],
            "habitat": "Hedgerows, Woodlands",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "All parts (especially berries)",
            "warnings": "HIGH. Severe purgative. Can be fatal.",
            "description": "**Identification:** Climbing plant (creeper). Red berries. Large lobed leaves (ivy-like). Curling tendrils used to climb.",
            "id_keys": {
                "Fruit": "Red berries, size of peas",
                "Leaves": "Lobed, ivy-like, rough texture",
                "Climb": "Climbs using curling tendrils (vital ID)"
            },
            "danger_tips": {
                "where": "Hedgerows, scrambling over bushes.",
                "when": "Berries late summer/autumn.",
                "sustainable": "Do not touch berries.",
                "danger_zone": "HIGH. Severe vomiting, diarrhoea, dehydration."
            },
            "lookalikes": [
                {
                    "name": "None dangerous",
                    "danger": "SAFE",
                    "diff": "Distinctive climber with tendrils. No common edible climber has red berries in hedges."
                }
            ],
            "confusion_notes": "Distinctive climber. No common edible climber has red berries in hedges."
        },
        {
            "name": "Black Bryony",
            "latin_name": "Tamus communis",
            "category": "Plant",
            "months": ["August", "September", "October"],
            "habitat": "Hedgerows, Woods",
            "regions": ["All"],
            "difficulty": 2,
            "parts": "All parts (especially berries)",
            "warnings": "HIGH. Skin irritant. Poisonous if eaten.",
            "description": "**Identification:** Climbing plant. Shiny black berries. Heart-shaped glossy leaves. Twining stems (no tendrils).",
            "id_keys": {
                "Fruit": "Shiny black berries",
                "Leaves": "Heart-shaped, glossy, shiny",
                "Stem": "Twining climber (wraps around stems)"
            },
            "danger_tips": {
                "where": "Hedgerows, woods, shady places.",
                "when": "Autumn berries.",
                "sustainable": "Avoid skin contact with sap.",
                "danger_zone": "HIGH. Skin irritation, severe stomach pain."
            },
            "lookalikes": [
                {
                    "name": "None dangerous",
                    "danger": "SAFE",
                    "diff": "Shiny black berries and heart-shaped leaves on a twining stem. Unlikely to be confused with edibles."
                }
            ],
            "confusion_notes": "Do not touch the berries (irritant). Distinctive from wild hops or hops which have different fruit."
        }
    ]
} # <--- THIS WAS MISSING

LESSON_CONTENT = {
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
- **Puffball:** Must be pure white inside. If Purple/yellow inside, it is old.
- **Field mushroom:** Pink gills turning brown. Avoid yellow stainers.
""",
        "quiz": {
            "question": "If a mushroom has a 'volva' (cup) at the base, what should you do?",
            "options": ["Eat it", "Cut it open", "Leave it (High Poison Risk)", "Smell it"],
            "answer": "Leave it (High Poison Risk)"
        }
    },
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
            "options": ["Yes, if I only take one", "Yes, if it is for dinner", "No, uprooting is illegal without permission"],
            "answer": "No, uprooting is illegal without permission"
        }
    }
}

# --- HELPER FOR AUDIO ---
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

# --- SIDEBAR FUNCTION ---
def render_sidebar():
    # --- LOGO SECTION ---
    try:
        st.sidebar.image("logo.png", width=150)
    except:
        st.sidebar.title("🌿 Rocen Homesteady")

    # --- PLAYER STATS ---
    st.sidebar.markdown(f"**🎓 Rank:** {st.session_state.player_title}")
    st.sidebar.markdown(f"**🌱 Plants ID'd:** {st.session_state.total_plants_identified}")
    st.sidebar.markdown("---")

    # --- SAFETY INFO ---
    st.sidebar.warning("⚠️ **Safety First**")
    st.sidebar.markdown("""
    - Never eat a plant based solely on app ID.
    - Always cross-reference with a field guide.
    - **UK Law:** Only pick for personal use.
    - It is illegal to uproot plants without permission.
    """)

    # --- RESET BUTTON ---
    # Adds a button to clear progress for a new user
    if st.sidebar.button("🔄 Reset Game Stats"):
        # Reset scores
        st.session_state.game_score = 0
        st.session_state.game_lives = 3
        st.session_state.game_streak = 0
        st.session_state.survival_lives = 3
        st.session_state.survival_score = 0
        st.session_state.survival_correct_count = 0
        st.session_state.total_plants_identified = 0
        st.session_state.player_title = "Novice Gatherer"
        st.session_state.season_badge_progress = []
        # Clear specific game states if needed
        st.session_state.village = None
        st.session_state.farm_game = None
        st.sidebar.success("Stats Reset! Refreshing...")
        # Rerun to update the UI immediately
        st.rerun()

    # --- BUSINESS DETAILS ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 12px; line-height: 1.4;">
        <b>Rocen Homesteady LTD</b><br>
        4th Floor<br>
        14 Museum Place, City Centre<br>
        Cardiff<br>
        CF10 3BH
    </div>
    """, unsafe_allow_html=True)