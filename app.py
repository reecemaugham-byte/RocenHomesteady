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
# Set page title and try to use logo as favicon
try:
    st.set_page_config(
        page_title="Rocen Homesteady",
        page_icon="logo.png", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
except:
    st.set_page_config(
        page_title="Rocen Homesteady",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded"
    )

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

    /* --- Headings - Golden Yellow --- */
    h1, h2, h3 {
        color: #E5B83E !important; /* Gold */
        font-family: 'Georgia', serif !important;
        border-bottom: 2px solid #6B4226; /* Saddle Brown underline */
        padding-bottom: 10px;
    }

    /* --- Buttons - Saddle Brown --- */
    .stButton > button {
        background-color: #6B4226; /* Saddle Brown */
        color: white !important;
        border-radius: 20px;
        border: 1px solid #E5B83E; /* Gold border */
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #E5B83E; /* Gold Hover */
        color: #3A2416 !important; /* Dark Text */
        transform: scale(1.02);
    }

    /* --- Sidebar - Forest Green --- */
    [data-testid="stSidebar"] {
        background-color: #3F5F2A; /* Deep Forest Green */
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* White text on green */
    }
    
    /* Sidebar specific adjustments */
    [data-testid="stSidebar"] .stMarkdown hr {
        border-color: #E5B83E;
    }

    /* --- Metric Boxes - Wood Brown --- */
    [data-testid="stMetric"] {
        background-color: #6B4226; /* Saddle Brown */
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 0 1px #E5B83E; /* Gold outline */
        border-left: 5px solid #E5B83E; /* Gold left bar */
        color: white;
    }
    [data-testid="stMetric"] label {
        color: #E5B83E !important; /* Gold Label */
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
        background-color: #E5B83E !important; /* Gold active tab */
        color: #3A2416 !important;
        border-bottom: 2px solid #6B4226;
    }

    /* --- Expander --- */
    .streamlit-expanderHeader {
        background-color: #6B4226 !important; /* Saddle Brown */
        border-radius: 10px;
        border-left: 5px solid #E5B83E; /* Gold left bar */
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* --- Input Fields --- */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
        background-color: #3F5F2A !important; /* Green input bg */
        color: #FFFFFF !important;
        border: 1px solid #E5B83E;
    }

    /* --- Custom Warning Box --- */
    .warning-box {
        background-color: #6B4226;
        border-left: 5px solid #E5B83E;
        color: #FFFFFF !important;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    
    /* --- Danger Box --- */
    .danger-box {
        background-color: #6B4226;
        border-left: 5px solid #dc3545;
        color: #EF9A9A !important;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_brand_theme()

# ==========================================
# DATA (Upgraded with Latin Names & ID Keys)
# ==========================================
UK_PLANTS = {
    "edible": [
        {"name": "Wild Garlic", "latin_name": "Allium ursinum", "months": ["March", "April", "May"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Strong smell helps identification", "lookalikes": ["Lily of the Valley (Poisonous)"], "description": "**Identification:** Broad leaves, white flowers, smells strongly of garlic.", "id_keys": {"Smell": "Strong Garlic", "Leaves": "Broad, soft, translucent", "Flowers": "White, star-shaped"}, "confusion_notes": "Confused with Lily of the Valley. **Key Diff:** Lily of the Valley has bell-shaped flowers and NO garlic smell."},
        {"name": "Nettles", "latin_name": "Urtica dioica", "months": ["February", "March", "April", "May", "June"], "habitat": "Woodlands, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Young leaves", "warnings": "Wear gloves when picking", "lookalikes": ["Dead-nettle (Edible, no sting)"], "description": "**Identification:** Jagged leaves, stinging hairs. **Uses:** Soup, tea.", "id_keys": {"Touch": "Stings!", "Leaves": "Jagged, heart-shaped", "Stem": "Green, hairy"}, "confusion_notes": "Confused with Dead-Nettle. **Key Diff:** Dead-nettle does not sting and has white flowers."},
        {"name": "Dandelion", "latin_name": "Taraxacum officinale", "months": ["February", "March", "April", "May", "June", "July"], "habitat": "Everywhere", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers, Roots", "warnings": "Avoid areas with dog waste", "lookalikes": ["Cat's Ear (Edible)"], "description": "**Identification:** Yellow flowers, hollow stems, 'lion's tooth' leaves.", "id_keys": {"Stem": "Hollow, milky sap", "Leaves": "Toothed (Lion's tooth)", "Flowers": "Single yellow flower"}, "confusion_notes": "Confused with Cat's Ear. **Key Diff:** Cat's Ear has branching stems and hairy leaves."},
        {"name": "Three-Cornered Leek", "latin_name": "Allium triquetrum", "months": ["January", "February", "March", "April"], "habitat": "Woodlands, Hedgerows", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Leaves, Flowers, Bulbs", "warnings": "Invasive species - pick freely!", "lookalikes": ["Snowdrop (Inedible)", "Bluebell (Poisonous)"], "description": "**Identification:** Strap-like leaves with a 'keel' (triangular shape like a boat). Smells like onion/garlic.", "id_keys": {"Smell": "Onion/Garlic", "Stem": "Triangular (3-cornered)", "Flowers": "White, bell-shaped"}, "confusion_notes": "Confused with Bluebell. **Key Diff:** Bluebell is blue/pink and smells like hyacinth, NOT garlic."},
        {"name": "Wood Ear (Jelly Ear)", "latin_name": "Auricularia auricula-judae", "months": ["January", "February", "November", "December"], "habitat": "Woodlands (Elder trees)", "regions": ["All"], "difficulty": 2, "parts": "Fungus", "warnings": "Must be cooked, raw can cause itchiness.", "lookalikes": ["Other tree fungi"], "description": "**Identification:** Brown, jelly-like, grows on Elder branches.", "id_keys": {"Texture": "Jelly-like, rubbery", "Shape": "Ear-shaped", "Habitat": "ONLY on Elder trees"}, "confusion_notes": "Confused with other tree fungi. **Key Diff:** Only Jelly Ear is ear-shaped and grows specifically on Elder."},
        {"name": "Sorrel", "latin_name": "Rumex acetosa", "months": ["April", "May", "June", "July"], "habitat": "Grassland, Meadows", "regions": ["All"], "difficulty": 1, "parts": "Leaves", "warnings": "Contains oxalic acid, eat in moderation", "lookalikes": ["Lords and Ladies (Poisonous)"], "description": "**Identification:** Arrow-shaped leaves, sharp lemon taste.", "id_keys": {"Taste": "Sharp Lemon", "Leaves": "Arrow-shaped, pointed", "Flowers": "Tall reddish spikes"}, "confusion_notes": "Confused with Lords and Ladies. **Key Diff:** Lords and Ladies has arrow leaves but spots/spikes and TONGUE-burn (no lemon taste)."},
        {"name": "Elderflower", "latin_name": "Sambucus nigra", "months": ["June", "July"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Flowers", "warnings": "Don't confuse with dwarf elder", "lookalikes": ["Hemlock (Poisonous)", "Cow Parsley"], "description": "**Identification:** Creamy-white flat flower heads.", "id_keys": {"Smell": "Sweet, summery", "Leaves": "Opposite pairs, feather-shaped", "Flowers": "Flat, creamy-white umbels"}, "confusion_notes": "Confused with Hemlock. **Key Diff:** Hemlock has purple spots on stem and smells of mouse urine. Elder has woody bark."},
        {"name": "Blackberries", "latin_name": "Rubus fruticosus", "months": ["August", "September"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Berries", "warnings": "Watch for thorns", "lookalikes": ["None dangerous in UK"], "description": "**Identification:** Bramble with thorns and dark purple/black berries.", "id_keys": {"Fruit": "Black, compound berry", "Stem": "Thorny (bramble)", "Leaves": "5-leaflet, toothed"}, "confusion_notes": "Very safe. Confused with Dewberry (also edible). No dangerous lookalikes in UK."},
        {"name": "Rosehips", "latin_name": "Rosa canina", "months": ["September", "October", "November", "December"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Fruit", "warnings": "Remove seeds before eating", "lookalikes": ["None dangerous"], "description": "**Identification:** Red, oval hips on wild rose bushes.", "id_keys": {"Fruit": "Red, oval hips", "Stem": "Thorny", "Flowers": "Pink/White (Summer)"}, "confusion_notes": "Safe. Ensure not sprayed by roadsides."},
        {"name": "Hawthorn", "latin_name": "Crataegus monogyna", "months": ["September", "October"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Berries", "warnings": "Pips contain cyanide - spit out", "lookalikes": ["None dangerous"], "description": "**Identification:** Thorny shrub with red berries (Haws).", "id_keys": {"Fruit": "Red berries (Haws)", "Leaves": "Lobed (oak-like)", "Thorns": "Sharp, long thorns"}, "confusion_notes": "Safe. Look for the 'May' flower in spring."},
        {"name": "Chanterelle", "latin_name": "Cantharellus cibarius", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 3, "parts": "Whole mushroom", "warnings": "EXPERT ONLY - False gills", "lookalikes": ["False Chanterelle (Inedible)"], "description": "**Identification:** Egg-yolk yellow, false gills (ridges), smells of apricots.", "id_keys": {"Gills": "False (Ridges), forked", "Smell": "Apricots", "Colour": "Egg-yolk yellow"}, "confusion_notes": "Confused with False Chanterelle. **Key Diff:** False Chanterelle has true gills (thin sheets) and no apricot smell."},
        {"name": "Field Mushroom", "latin_name": "Agaricus campestris", "months": ["August", "September", "October"], "habitat": "Fields, Meadows", "regions": ["All"], "difficulty": 2, "parts": "Whole mushroom", "warnings": "Beware of yellow staining lookalikes", "lookalikes": ["Yellow Stainer (Poisonous)"], "description": "**Identification:** White cap, pink gills turning brown.", "id_keys": {"Gills": "Pink turning brown", "Stem": "White ring", "Smell": "Mushroomy"}, "confusion_notes": "Confused with Yellow Stainer. **Key Diff:** Yellow Stainer stains BRIGHT YELLOW when bruised and smells like ink/chemicals."},
        {"name": "Hazelnut", "latin_name": "Corylus avellana", "months": ["September", "October"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Nuts", "warnings": "Pick before squirrels get them", "lookalikes": ["None dangerous"], "description": "**Identification:** Shrubby tree, nuts in green husks.", "id_keys": {"Nut": "In a leafy green husk", "Leaves": "Rounded, hairy"}, "confusion_notes": "Safe. Look for the leafy 'hat' on the nut."},
        {"name": "Sweet Chestnut", "latin_name": "Castanea sativa", "months": ["October", "November"], "habitat": "Woodlands", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Nuts", "warnings": "Do not confuse with Horse Chestnut", "lookalikes": ["Horse Chestnut (Poisonous)"], "description": "**Identification:** Pointed nuts, many nuts per case.", "id_keys": {"Case": "Spiky, long spikes", "Leaf": "Long, toothed"}, "confusion_notes": "Confused with Horse Chestnut. **Key Diff:** Horse Chestnut has WARTY/SMOOTH cases (conkers), Sweet Chestnut has LONG SPIKY cases."},
        {"name": "Pine Needles", "latin_name": "Pinus sylvestris", "months": ["January", "February", "December"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Needles", "warnings": "Avoid Yew (flat needles)", "lookalikes": ["Yew (Poisonous)"], "description": "**Identification:** Long needles in bundles. **Uses:** Tea, rich in Vitamin C.", "id_keys": {"Needles": "Long, in bundles (2-3)", "Smell": "Pine resin"}, "confusion_notes": "Confused with Yew. **Key Diff:** Yew needles are FLAT and have NO smell/resin. Pine needles are round and in bundles."}
    ],
    "poisonous": [
        {"name": "Deadly Nightshade", "latin_name": "Atropa belladonna", "months": ["June", "July", "August", "September"], "habitat": "Woodlands, Gardens", "regions": ["All"], "danger": "EXTREME", "symptoms": "Dilated pupils, hallucinations, death", "lookalikes": ["Bilberry"], "description": "**Identification:** Bell-shaped purple flowers, shiny black berries. **Danger:** Fatal.", "id_keys": {"Flowers": "Purple, bell-shaped", "Berries": "Shiny black, size of cherry", "Leaves": "Large, soft"}, "confusion_notes": "Confused with Bilberry. **Key Diff:** Bilberry is a small shrub with small blue berries. Nightshade is a large leafy plant with large black berries."},
        {"name": "Foxglove", "latin_name": "Digitalis purpurea", "months": ["June", "July", "August"], "habitat": "Gardens, Woodlands", "regions": ["All"], "danger": "HIGH", "symptoms": "Heart failure, nausea", "lookalikes": ["Comfrey"], "description": "**Identification:** Tall spikes of pink/purple trumpet flowers. **Danger:** All parts toxic.", "id_keys": {"Flowers": "Pink/Purple trumpets", "Stem": "Tall, green", "Leaves": "Large, hairy"}, "confusion_notes": "Confused with Comfrey. **Key Diff:** Comfrey has bell flowers that don't point down, and leaves clasp the stem."},
        {"name": "Hemlock", "latin_name": "Conium maculatum", "months": ["April", "May", "June", "July"], "habitat": "Rivers, Damp areas", "regions": ["All"], "danger": "EXTREME", "symptoms": "Respiratory failure, death", "lookalikes": ["Wild Carrot", "Cow Parsley"], "description": "**Identification:** Tall, purple-spotted stems, smell of mouse urine.", "id_keys": {"Stem": "Smooth, Purple Spots", "Smell": "Mouse Urine", "Root": "White, fleshy"}, "confusion_notes": "Confused with Wild Carrot. **Key Diff:** Hemlock has SMOOTH/PURPLE-SPOTTED stems. Wild Carrot is HAIRY and smells of carrot."},
        {"name": "Hemlock Water Dropwort", "latin_name": "Oenanthe crocata", "months": ["April", "May", "June", "July"], "habitat": "Riverbanks, Wet ground", "regions": ["All"], "danger": "EXTREME", "symptoms": "Seizures, death", "lookalikes": ["Wild Parsnip", "Pignut"], "description": "**Identification:** White flowers, tuberous roots (deadliest part). **Danger:** Deadliest plant in UK.", "id_keys": {"Root": "Tubers like fingers (Dead Man's Fingers)", "Stem": "Hollow, grooved", "Habitat": "Wet ground"}, "confusion_notes": "Confused with Wild Parsnip. **Key Diff:** Parsnip has yellow flowers. Dropwort has white flowers and 'finger' roots."},
        {"name": "Fool's Parsley", "latin_name": "Aethusa cynapium", "months": ["May", "June", "July"], "habitat": "Gardens, Waste ground", "regions": ["All"], "danger": "HIGH", "symptoms": "Vomiting, burning mouth", "lookalikes": ["Parsley", "Wild Carrot"], "description": "**Identification:** Looks like Parsley but has a long bract under flower. Smells unpleasant.", "id_keys": {"Bracts": "Long, hanging under flowers", "Smell": "Unpleasant", "Leaves": "Parsley-like"}, "confusion_notes": "Confused with Parsley. **Key Diff:** Fool's Parsley has long bracts (green hairs) hanging under the flower umbrella. Real Parsley does not."},
        {"name": "Death Cap", "latin_name": "Amanita phalloides", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "danger": "EXTREME", "symptoms": "Liver/kidney failure, often fatal", "lookalikes": ["Straw Mushroom"], "description": "**Identification:** Green-yellow cap, white gills, volva (cup) at base. **Danger:** Most mushroom deaths.", "id_keys": {"Cap": "Green-yellow", "Gills": "White", "Base": "Volva (Cup) in ground"}, "confusion_notes": "Confused with Straw Mushroom. **Key Diff:** Straw Mushroom has PINK gills and no volva cup. Death Cap has WHITE gills and a volva."},
        {"name": "Lords and Ladies", "latin_name": "Arum maculatum", "months": ["March", "April", "May"], "habitat": "Hedgerows, Woods", "regions": ["All"], "danger": "HIGH", "symptoms": "Mouth blistering, swelling", "lookalikes": ["Sorrel", "Wild Garlic"], "description": "**Identification:** Arrow-shaped leaves, orange berries. **Danger:** Causes burning pain.", "id_keys": {"Leaves": "Arrow-shaped, often spotted", "Berries": "Orange cluster", "Smell": "Unpleasant"}, "confusion_notes": "Confused with Wild Garlic or Sorrel. **Key Diff:** Wild Garlic smells of garlic. Sorrel tastes of lemon. Lords & Ladies burns the mouth and has no smell."},
        {"name": "Yew", "latin_name": "Taxus baccata", "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "habitat": "Churchyards, Gardens", "regions": ["All"], "danger": "EXTREME", "symptoms": "Cardiac arrest, death", "lookalikes": ["None (Distinctive tree)"], "description": "**Identification:** Dark evergreen needles, red berry cups (arils). **Danger:** Needles and seeds are deadly.", "id_keys": {"Needles": "Flat, dark green", "Fruit": "Red cup (aril)", "Tree": "Evergreen conifer"}, "confusion_notes": "Confused with Pine/Fir. **Key Diff:** Yew needles are FLAT. Pine needles are ROUND and in bundles."},
        {"name": "Giant Hogweed", "latin_name": "Heracleum mantegazzianum", "months": ["June", "July", "August"], "habitat": "Riverbanks, Waste ground", "regions": ["England", "Scotland"], "danger": "HIGH", "symptoms": "Severe burns, skin sensitivity", "lookalikes": ["Cow Parsley", "Common Hogweed"], "description": "**Identification:** Huge (3m+), hairy stem with purple blotches. **Danger:** Sap burns skin.", "id_keys": {"Height": "Giant (3m+)", "Stem": "Purple blotches, hairy", "Leaves": "Huge, jagged"}, "confusion_notes": "Confused with Common Hogweed. **Key Diff:** Common Hogweed is smaller (1-2m). Giant is HUGE and causes burns. Do not touch."},
        {"name": "Dog's Mercury", "latin_name": "Mercurialis perennis", "months": ["February", "March", "April"], "habitat": "Woodlands", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Vomiting, diarrhoea", "lookalikes": ["Nettles", "Good King Henry"], "description": "**Identification:** Low growing, jagged leaves. **Danger:** Eaten by mistake as salad green.", "id_keys": {"Leaves": "Jagged, paired", "Height": "Low (ankle height)", "Flowers": "Green, insignificant"}, "confusion_notes": "Confused with Nettles. **Key Diff:** Dog's Mercury does NOT sting. It carpets the woodland floor early in spring."},
        {"name": "Bluebell", "latin_name": "Hyacinthoides non-scripta", "months": ["April", "May"], "habitat": "Woodlands", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Stomach upset, skin irritation", "lookalikes": ["Three-Cornered Leek"], "description": "**Identification:** Blue, bell-shaped flowers. **Danger:** Bulbs are toxic.", "id_keys": {"Flowers": "Blue, drooping bells", "Leaves": "Long, narrow", "Smell": "Slight sweet scent"}, "confusion_notes": "Confused with Three-Cornered Leek. **Key Diff:** Three-Cornered Leek has WHITE flowers and smells of Garlic. Bluebell is BLUE."},
        {"name": "Fly Agaric", "latin_name": "Amanita muscaria", "months": ["August", "September", "October"], "habitat": "Woodlands", "regions": ["All"], "danger": "HIGH", "symptoms": "Hallucinations, nausea", "lookalikes": ["None distinctive"], "description": "**Identification:** Classic red cap with white spots. Iconic fairy tale mushroom. **Danger:** Psychoactive and toxic.", "id_keys": {"Cap": "Red with white spots", "Stem": "White, skirt"}, "confusion_notes": "Distinctive. No safe lookalikes. Do not touch."},
        {"name": "Monkshood", "latin_name": "Aconitum napellus", "months": ["June", "July"], "habitat": "Woodlands, Stream banks", "regions": ["UK"], "danger": "EXTREME", "symptoms": "Heart failure", "lookalikes": ["Larkspur"], "description": "**Identification:** Purple helmet-shaped flowers. **Danger:** Very toxic, touching sap can be harmful.", "id_keys": {"Flowers": "Purple, helmet shape", "Leaves": "Hand-shaped (palmate)"}, "confusion_notes": "Confused with Larkspur. **Key Diff:** Monkshood flowers are helmet-shaped. Larkspur has a spur."},
        {"name": "Bracken", "latin_name": "Pteridium aquilinum", "months": ["Summer"], "habitat": "Moorland, Woods", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Cancer risk (long term)", "lookalikes": ["Other ferns"], "description": "**Identification:** Large fern. **Danger:** Young shoots (fiddleheads) are carcinogenic if eaten. Avoid.", "id_keys": {"Shape": "Large, triangular fronds", "Spores": "Under edges of leaf"}, "confusion_notes": "Confused with other ferns. **Key Diff:** Bracken is huge (taller than you). Most other ferns are smaller."}
    ]
}

# ==========================================
# STATIC LESSON CONTENT
# ==========================================
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
        'survival_result': None, 'daily_streak': 0, 'quiz_active': False, 'module_questions': None,
        # NEW: Player Profile
        'player_title': "Novice Gatherer",
        'total_plants_identified': 0
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
# --- LOGO SECTION ---
# Attempts to load your logo.png. Falls back to text if file not found.
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

# ==========================================
# TABS
# ==========================================
main_tab1, main_tab2 = st.tabs(["📖 Learning", "🎮 Games"])

# ==========================================
# TAB 1: LEARNING
# ==========================================
with main_tab1:
    st.header("📖 UK Foraging Guide")
    st.info("**Disclaimer:** This guide is for educational purposes. Always consult a local expert before consuming wild plants.")

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

            # Determine Icon
            icon = "🌿" if status == "Edible" else "☠️"
            
            with st.expander(f"{icon} {plant['name']}"):
                # NEW: Latin Name & Audio
                latin_name = plant.get('latin_name', 'Unknown')
                st.markdown(f"**Latin Name:** *{latin_name}*")
                if EDGE_TTS_AVAILABLE:
                    if st.button(f"🔊 Pronounce Latin", key=f"latin_btn_{plant['name']}"):
                        with st.spinner("Generating pronunciation..."):
                            audio_file = generate_voice(latin_name.replace(" ", " "))
                            if audio_file:
                                st.audio(audio_file)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Habitat:** {plant.get('habitat', 'Various')}")
                    st.markdown(f"**Months:** {', '.join(plant.get('months', []))}")
                with c2:
                    if status == "Edible":
                        st.markdown(f"**Parts:** {plant.get('parts', 'Various')}")
                        st.markdown(f"**Difficulty:** {'🌱' * plant.get('difficulty', 1)}")
                    else:
                        st.markdown(f"**Danger:** {plant.get('danger', 'Unknown')}")
                        st.markdown(f"**Symptoms:** {plant.get('symptoms', 'Unknown')}")

                # Description
                st.markdown(plant.get('description', 'No info available.'))

                # NEW: Identification Keys (Spot the Difference)
                if 'id_keys' in plant:
                    st.markdown("#### 🔎 Identification Keys")
                    for key, value in plant['id_keys'].items():
                        st.markdown(f"- **{key}:** {value}")

                # Safety & Lookalikes
                if status == "Edible":
                    warning_text = plant.get('warnings', '')
                    if warning_text:
                        st.warning(f"⚠️ **Warning:** {warning_text}")
                    
                    lookalikes = plant.get('lookalikes', [])
                    if lookalikes:
                        st.error(f"👀 **Watch out for Lookalikes:** {', '.join(lookalikes)}")
                else:
                    st.error(f"☠️ **Toxicity:** {plant.get('symptoms', 'Unknown')}")
                    st.warning(f"🔍 **Confused with:** {', '.join(plant.get('lookalikes', []))}")
                    if 'confusion_notes' in plant:
                        st.markdown(f"**Confusion Note:** {plant['confusion_notes']}")

    # --- SUB-TAB 2: LEARNING MODULES ---
    with learn_tab2:
        st.header("🎓 Learning Modules")
        st.markdown("### Structured learning paths for UK foraging")

        # Static content dictionary defined above...
        modules = {
            "🌱 Beginner": ["Introduction to Foraging", "Easy Plants to Identify", "The Carrot Family"],
            "🌲 Advanced": ["Mushroom Foraging", "The Law of the Land"]
        }

        for level, module_list in modules.items():
            st.markdown(f"### {level}")
            for title in module_list:
                if title in LESSON_CONTENT:
                    data = LESSON_CONTENT[title]
                    with st.expander(f"📚 {title}"):
                        st.markdown(data['text'])
                        
                        # Quiz Section
                        st.markdown("### 📝 Quiz")
                        q = data['quiz']
                        user_ans = st.radio(q['question'], q['options'], key=f"radio_{title}")
                        
                        if st.button("Submit Answer", key=f"submit_{title}"):
                            if user_ans == q['answer']:
                                st.success("✅ Correct!")
                                st.balloons()
                            else:
                                st.error(f"❌ Incorrect. The correct answer was: {q['answer']}.")
                else:
                    st.warning(f"Content for '{title}' coming soon.")

# ==========================================
# TAB 2: GAMES
# ==========================================
with main_tab2:
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

        with st.expander("📖 How to Play"):
            st.markdown("""
            1. **Select a Season** using the buttons at the top.
            2. A plant will appear. Read its name.
            3. Choose the **Habitat** where it grows (e.g., Woodland, Coastal).
            4. Get it right to build a **Streak** for bonus points!
            5. Collect badges for all 4 seasons.
            """)

        habitat_icons = {"Woodland": "🌲", "Hedgerow": "🌿", "Coastal": "🏖️", "Urban": "🏡", "Meadow": "🌾"}

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
                raw_habitat = plant['habitat'].split(',')[0].strip()
                
                if raw_habitat in ["Woodlands", "Woods", "Wood"]: correct_habitat = "Woodland"
                elif raw_habitat in ["Hedgerows", "Hedgerow", "Roadsides"]: correct_habitat = "Hedgerow"
                elif raw_habitat in ["Meadows", "Grassland", "Fields", "Fields, Gardens"]: correct_habitat = "Meadow"
                elif raw_habitat in ["Coastal", "Coastal Shingle"]: correct_habitat = "Coastal"
                else: correct_habitat = "Urban"

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
                        st.session_state.total_plants_identified += 1
                        st.balloons()
                        st.success(f"✅ Correct! {q['plant']['name']} loves the {option}!")
                        if active_season not in st.session_state.season_badge_progress:
                            st.session_state.season_badge_progress.append(active_season)
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
    # GAME TAB 2: SURVIVAL SCHOOL (UPGRADED)
    # ==========================================
    with tab2:
        st.header("☠️ Survival School")
        st.caption("📚 Curriculum Link: Science (Plants), PSHE (Safety)")

        with st.expander("📖 How to Play"):
            st.markdown("""
            1. Read the **Case File** carefully. Look for clues in the description.
            2. You have two suspects: One is **Safe**, one is **Poisonous**.
            3. Click the **Safe** plant to solve the case.
            4. **NEW:** If you get it wrong, study the **Identification Keys** to see why!
            """)

        # Progress
        progress = st.session_state.survival_correct_count / 5
        st.progress(progress, text=f"Badge Progress: {st.session_state.survival_correct_count}/5 Cases Solved")
        col1, col2 = st.columns(2)
        col1.metric("❤️ Lives", "❤️" * max(0, st.session_state.survival_lives))
        col2.metric("🌟 Score", st.session_state.survival_score)
        st.markdown("---")

        # Expanded Case Files
        CASE_FILES = [
            {"clue": "You find a tall plant with white umbrella-shaped flowers ☂️. You check the stem. It is **smooth** (no hairs) and has **purple spots** on it.", "rule": "🚨 **Rule:** In the Carrot family, purple spots usually mean POISON.", "safe_plant": "Wild Carrot", "danger_plant": "Hemlock", "safe_icon": "🥕", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Hemlock (POISON):** Smooth stem with purple spots. Smells like mouse urine.\n- **Wild Carrot (Safe):** Hairy stem. Smells like carrots. **Hairy is Happy, Smooth is Suspicious!**", "safe_habitat": "Meadows"},
            {"clue": "You find a plant with broad green leaves in a damp woodland. You crush a leaf and it smells strongly of **garlic** 🧄.", "rule": "✅ **Rule:** Strong onion/garlic smell is usually a good sign.", "safe_plant": "Wild Garlic", "danger_plant": "Lily of the Valley", "safe_icon": "🌿", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Lily of the Valley (POISON):** Has no garlic smell. Has bell-shaped flowers.\n- **Wild Garlic (Safe):** Smells strongly of garlic. **No smell = Leave it be.**", "safe_habitat": "Woodland"},
            {"clue": "A bright orange mushroom grows under an oak tree. Under the cap, it has **ridges** (like false gills) that run down the stem. It smells like **apricots** 🍑.", "rule": "✅ **Rule:** True gills are thin sheets. Ridges are blunt and thick.", "safe_plant": "Chanterelle", "danger_plant": "False Chanterelle", "safe_icon": "🍄", "danger_icon": "🚫", "fact": "🕵️ **Inspector's Report:**\n- **False Chanterelle (Inedible):** Has true gills (thin sheets). No apricot smell.\n- **Chanterelle (Safe):** Has 'false gills' (ridges) and smells fruity. **Ridges = Rewarding.**", "safe_habitat": "Woodland"},
            {"clue": "You find a bush with dark berries. The leaves are arranged in **pairs** opposite each other on the stem.", "rule": "✅ **Rule:** 'Opposite' leaves (pairs) are safe for Elder. 'Alternate' leaves are dangerous.", "safe_plant": "Elderflower", "danger_plant": "Dwarf Elder", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Dwarf Elder (POISON):** Leaves are alternate (one by one). Flowers stand upright.\n- **Elderflower (Safe):** Leaves are opposite (in pairs). Flowers droop down.", "safe_habitat": "Hedgerow"},
            {"clue": "A plant with strap-like leaves grows in the woods. You roll the stem between your fingers—it feels **triangular** (like a keel ⛵).", "rule": "✅ **Rule:** A triangular stem is a unique ID feature.", "safe_plant": "Three-Cornered Leek", "danger_plant": "Bluebell", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Bluebell (POISON):** Round stem. Blue bells. All parts toxic.\n- **Three-Cornered Leek (Safe):** Triangular stem. White flowers. Smells like onion/garlic. **Triangle = Tasty.**", "safe_habitat": "Woodland"}
        ]

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
                if options[0]['is_safe']:
                    st.session_state.survival_result = "correct"
                    st.session_state.survival_score += 20
                    st.session_state.survival_correct_count += 1
                    st.session_state.total_plants_identified += 1
                else:
                    st.session_state.survival_result = "wrong"
                    st.session_state.survival_lives -= 1
                    st.session_state.survival_correct_count = 0
                st.rerun()
            if btn_col2.button(f"{options[1]['icon']} {options[1]['name']}", key="surv_opt_2", use_container_width=True):
                if options[1]['is_safe']:
                    st.session_state.survival_result = "correct"
                    st.session_state.survival_score += 20
                    st.session_state.survival_correct_count += 1
                    st.session_state.total_plants_identified += 1
                else:
                    st.session_state.survival_result = "wrong"
                    st.session_state.survival_lives -= 1
                    st.session_state.survival_correct_count = 0
                st.rerun()
        else:
            # --- UPGRADED FEEDBACK SECTION ---
            if st.session_state.survival_result == "correct":
                st.success("✅ CASE SOLVED! Great work, Inspector.")
                st.balloons()
                # Show safe plant info
                plant_name = case['safe_plant']
                # Find plant data
                plant_data = next((p for p in UK_PLANTS['edible'] if p['name'] == plant_name), None)
            else:
                st.error("☠️ DANGER! That was the wrong choice.")
                # Show dangerous plant info
                plant_name = case['danger_plant']
                plant_data = next((p for p in UK_PLANTS['poisonous'] if p['name'] == plant_name), None)
            
            st.markdown("### 📝 Case File Analysis")
            
            if plant_data:
                # 1. Latin Name & Audio
                latin = plant_data.get('latin_name', 'Unknown')
                st.markdown(f"**Scientific Name:** *{latin}*")
                if EDGE_TTS_AVAILABLE:
                    if st.button(f"🔊 Pronounce '{latin}'", key=f"survival_audio_{latin}"):
                        with st.spinner("Generating pronunciation..."):
                            audio_file = generate_voice(latin.replace(" ", " "))
                            if audio_file:
                                st.audio(audio_file)
                
                # 2. ID Keys (Spot the Difference)
                st.markdown("#### 🔎 Identification Keys")
                id_keys = plant_data.get('id_keys', {})
                if id_keys:
                    for key, value in id_keys.items():
                        st.markdown(f"- **{key}:** {value}")
                else:
                    st.markdown(plant_data.get('description', 'No description.'))
                
                # 3. Confusion Note
                confusion = plant_data.get('confusion_notes', '')
                if confusion:
                    st.error(f"⚠️ **Confusion Warning:** {confusion}")

            if st.session_state.survival_correct_count >= 5:
                st.markdown("# 🏅 BADGE EARNED: Plant Safety Expert!")
                st.snow()
                st.session_state.survival_correct_count = 0
            
            if st.button("📋 Next Case", key="next_case_btn"):
                st.session_state.survival_current_case = None
                st.session_state.survival_result = None
                st.rerun()

        if st.session_state.survival_lives <= 0:
            st.markdown("## 🤕 Training Ended")
            st.markdown("Don't worry, even experts make mistakes. Review the case files and try again!")
            if st.button("🔄 Restart Training", key="restart_survival"):
                st.session_state.survival_lives = 3
                st.session_state.survival_correct_count = 0
                st.session_state.survival_current_case = None
                st.session_state.survival_result = None
                st.rerun()

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
                    if opt == q['correct']:
                        st.session_state.quiz_score += 1
                        st.session_state.daily_streak += 1
                        st.toast("✅ Correct!")
                    else:
                        st.session_state.daily_streak = 0
                        st.toast("❌ Oops!")
                    st.session_state.quiz_q_num += 1
                    st.session_state.q_data = None
                    time.sleep(0.5)
                    st.rerun()
        else:
            st.balloons()
            st.markdown("## 🎉 Challenge Complete!")
            if st.session_state.quiz_score == st.session_state.quiz_max:
                st.success("PERFECT SCORE!")
            elif st.session_state.quiz_score >= st.session_state.quiz_max / 2:
                st.info("Good job!")
            else:
                st.warning("Keep practicing!")
            if st.button("🔄 Try Again", key="restart_quiz"):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.rerun()

    # ==========================================
    # GAME TAB 4: ECO-VILLAGE (UPGRADED)
    # ==========================================
    with tab4:
        st.header("🏘️ Eco-Village Builder")
        st.caption("📚 Manage resources sustainably!")
        with st.expander("📖 How to Play"):
            st.markdown("""
            - **Forage:** Gather resources (Costs Stamina & Nature).
            - **Build:** Buy buildings on the Map (Costs Money).
            - **Preserve:** Turn seasonal food into winter stores! (New Feature).
            - **Rest:** Click 'Next Day' to recover Stamina.
            - **Goal:** Build a village without destroying the **Nature Health** bar!
            """)

        ITEMS_DATA = {"Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 2}, "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1}, "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 3}, "Wood": {"icon": "🪵", "rarity": 0.6, "value": 2}, "Stone": {"icon": "🪨", "rarity": 0.4, "value": 2}, "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 5}, "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 10}, "Milk": {"icon": "🥛", "rarity": 0.0, "value": 15}}
        BUILDINGS = {"House": {"cost": 50, "icon": "🏠", "desc": "Shelter to recover stamina."}, "Well": {"cost": 30, "icon": "🪨", "desc": "Passive water income."}, "Coop": {"cost": 40, "icon": "🐔", "desc": "Hold up to 5 chickens."}}

        if st.session_state.get('village') is None:
            st.session_state.village = {'grid': [['🌲' for _ in range(6)] for _ in range(4)], 'stats': {'Food': 50, 'Water': 50, 'Power': 0, 'Stamina': 100, 'Money': 100}, 'inventory': {}, 'animals': [], 'buildings': [], 'day': 1, 'season': 'Spring', 'placement_mode': None, 'nature_health': 100, 'preserved_food': 0}

        game = st.session_state.village

        def render_stats():
            s = game['stats']
            cols = st.columns(7)
            cols[0].metric("🍖 Food", s['Food'])
            cols[1].metric("💧 Water", s['Water'])
            cols[2].metric("⚡ Power", s['Power'])
            cols[3].metric("💪 Stamina", s['Stamina'])
            cols[4].metric("💰 Money", f"£{s['Money']}")
            cols[5].metric("🥫 Preserved", game['preserved_food'])
            nature = game['nature_health']
            cols[6].metric(f"{'🟢' if nature > 50 else '🟡' if nature > 20 else '🔴'} Nature", nature)
            if nature < 20:
                st.warning("⚠️ The forest is struggling! Over-harvesting detected.")
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
            if st.button("⏭️ Next Day"):
                game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
                game['day'] += 1
                st.rerun()

        with forage_tab:
            st.markdown("### 🌲 Gather Resources")
            render_stats()
            col_f, col_p = st.columns(2)
            with col_f:
                if st.button("🌿 Forage Plants", key="fp1"):
                    if game['stats']['Stamina'] >= 10:
                        game['stats']['Stamina'] -= 10
                        game['nature_health'] = max(0, game['nature_health'] - 5)
                        found = [name for name, data in ITEMS_DATA.items() if random.random() < data['rarity']]
                        for f in found:
                            game['inventory'][f] = game['inventory'].get(f, 0) + 1
                        st.success(f"Found: {', '.join(found[:3])}...")
                        st.rerun()
                    else:
                        st.error("Not enough stamina! Rest (Next Day) to recover.")
            with col_p:
                # NEW: Preservation Mechanic
                if st.button("🥫 Preserve Food (Cost: 10 Food)", key="preserve_btn"):
                    if game['stats']['Food'] >= 10:
                        game['stats']['Food'] -= 10
                        game['preserved_food'] += 5 # Efficient preservation
                        st.success("Created 5 Preserved Food rations! Safe for winter.")
                        st.rerun()
                    else:
                        st.error("Need 10 Food to preserve.")

    # ==========================================
    # GAME TAB 5: FARM TYCOON
    # ==========================================
    with tab5:
        st.header("🚜 Farm Tycoon: Nature Guardians")
        st.caption("📚 Build your farm, watch for Invasive Species!")

        with st.expander("📖 How to Play"):
            st.markdown("""
            - Select a **Tool** (Crop or Animal) and click the brown soil to place it.
            - Press **Next Day** to let crops grow.
            - Harvest crops when they are ready (Yellow icons).
            - **Watch out!** Invasive plants (🥀) will try to grow. Use the **Clear** tool to remove them!
            """)

        # --- GAME STATE INIT ---
        if st.session_state.get('farm_game') is None:
            grid = [[0 for _ in range(6)] for _ in range(5)]
            stream_col = random.randint(1, 4)
            for r in range(5):
                grid[r][stream_col] = 1
                if random.random() > 0.5:
                    stream_col = max(0, min(5, stream_col + random.choice([-1, 1])))
                    grid[r][stream_col] = 1

            st.session_state.farm_game = {
                'grid': grid,
                'money': 100,
                'day': 1,
                'season': 'Spring',
                'weather': '☀️ Sunny',
                'tool': 'Carrot',
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

        st.markdown("---")

        # --- THE GRID ---
        st.markdown("### 🗺️ Your Farm")
        st.markdown("`🟤` Dirt | `🌊` Stream | `🌱` Seed | `🌿` Growing | `🌾` Ready | `🐔` Chicken | `🐄` Cow | `🥀` **Invasive**")

        icons = {0: "🟤", 1: "🌊", 2: "🌱", 3: "🌿", 4: "🌾", 5: "🐔", 6: "🐄", 7: "🥀"}

        for r in range(5):
            cols = st.columns(6)
            for c in range(6):
                tile_val = game['grid'][r][c]
                icon = icons.get(tile_val, "❓")

                if tile_val == 7 and game['tool'] == "Clear":
                    if cols[c].button("🥀 CLEAR", key=f"{r}_{c}"):
                        game['grid'][r][c] = 0
                        game['invasives_cleared'] += 1
                        st.success("Invasive Removed!")
                        st.rerun()
                elif tile_val == 0 and game['tool'] in ["Carrot", "Wheat", "Corn"]:
                    costs = {"Carrot": 10, "Wheat": 15, "Corn": 20}
                    cost = costs[game['tool']]
                    can_afford = game['money'] >= cost
                    if cols[c].button(f"Plant (£{cost})", key=f"plant_{r}_{c}", disabled=not can_afford):
                        game['money'] -= cost
                        game['grid'][r][c] = 2
                        st.rerun()
                elif tile_val == 0 and game['tool'] in ["Chicken", "Cow"]:
                    costs = {"Chicken": 50, "Cow": 100}
                    animal_ids = {"Chicken": 5, "Cow": 6}
                    cost = costs[game['tool']]
                    can_afford = game['money'] >= cost
                    if cols[c].button(f"Buy (£{cost})", key=f"buy_{r}_{c}", disabled=not can_afford):
                        game['money'] -= cost
                        game['grid'][r][c] = animal_ids[game['tool']]
                        st.rerun()
                elif tile_val == 4:
                    if cols[c].button("🌾 Harvest", key=f"harv_{r}_{c}"):
                        harvest_val = random.randint(15, 30)
                        game['money'] += harvest_val
                        game['grid'][r][c] = 0
                        st.success(f"Harvested! +£{harvest_val}")
                        st.rerun()
                elif tile_val == 5:
                    if cols[c].button("🐔 Sell", key=f"sell_chick_{r}_{c}"):
                        game['money'] += 25
                        game['grid'][r][c] = 0
                        st.success("Sold Chicken! +£25")
                        st.rerun()
                elif tile_val == 6:
                    if cols[c].button("🐄 Sell", key=f"sell_cow_{r}_{c}"):
                        game['money'] += 60
                        game['grid'][r][c] = 0
                        st.success("Sold Cow! +£60")
                        st.rerun()
                else:
                    cols[c].markdown(f"<div style='text-align:center; font-size:24px;'>{icon}</div>", unsafe_allow_html=True)

        st.markdown("---")

        if st.button("⏭️ Next Day", key="next_day_farm"):
            for r in range(5):
                for c in range(6):
                    if game['grid'][r][c] == 2: game['grid'][r][c] = 3
                    elif game['grid'][r][c] == 3: game['grid'][r][c] = 4

            event_roll = random.random()
            if event_roll < 0.2:
                st.toast(f"📈 Market News: Prices fluctuated!")
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
