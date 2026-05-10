import streamlit as st
import random
import time
import pandas as pd
from collections import Counter
from datetime import datetime
from openai import OpenAI
import os
import json
import asyncio
import edge_tts

# --- SAFE IMPORTS ---
try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import alpaca_trade_api as tradeapi
except ImportError:
    tradeapi = None

# Handle PIL deprecation
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    Image = None

# ==========================================
# CONFIGURATION
# ==========================================
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "sk-proj--"

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
        background-color: #C8D6C8; /* Darker than before */
        background-image: radial-gradient(#A8BCA8 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Text Color - Deep Jungle Green */
    .stMarkdown, .stHeader, p, label {
        color: #1B4D3E !important;
    }

    /* Headings - Darker Brown */
    h1, h2, h3 {
        color: #3E2723 !important; /* Darker brown */
        font-family: 'Georgia', serif !important;
        border-bottom: 2px solid #8FBC8F; /* Softer green border */
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
        background-color: #A8C0A8; /* Darker Sage */
    }

    /* Metric Boxes - Soft Off-White */
    [data-testid="stMetric"] {
        background-color: #F5F9F5; /* Not pure white */
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
        background-color: #F5F9F5; /* Soft off-white */
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

apply_forest_theme()

# ==========================================
# DATA (Expanded)
# ==========================================
UK_PLANTS = {
    "edible": [
        {"name": "Wild Garlic", "months": ["March", "April", "May"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Strong smell helps identification", "lookalikes": ["Lily of the Valley (Poisonous)"], "description": "**Identification:** Broad leaves, white flowers, smells strongly of garlic."},
        {"name": "Nettles", "months": ["February", "March", "April", "May", "June"], "habitat": "Woodlands, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Young leaves", "warnings": "Wear gloves when picking", "lookalikes": ["Dead-nettle (Edible, no sting)"], "description": "**Identification:** Jagged leaves, stinging hairs. **Uses:** Soup, tea."},
        {"name": "Dandelion", "months": ["February", "March", "April", "May", "June", "July"], "habitat": "Everywhere", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers, Roots", "warnings": "Avoid areas with dog waste", "lookalikes": ["Cat's Ear (Edible)"], "description": "**Identification:** Yellow flowers, hollow stems, 'lion's tooth' leaves."},
        {"name": "Three-Cornered Leek", "months": ["January", "February", "March", "April"], "habitat": "Woodlands, Hedgerows", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Leaves, Flowers, Bulbs", "warnings": "Invasive species - pick freely!", "lookalikes": ["Snowdrop (Inedible)", "Bluebell (Poisonous)"], "description": "**Identification:** Strap-like leaves with a 'keel' (triangular shape). Smells like onion/garlic."},
        {"name": "Wood Ear (Jelly Ear)", "months": ["January", "February", "November", "December"], "habitat": "Woodlands (Elder trees)", "regions": ["All"], "difficulty": 2, "parts": "Fungus", "warnings": "Must be cooked, raw can cause itchiness", "lookalikes": ["Other tree fungi"], "description": "**Identification:** Brown, jelly-like, grows on Elder branches."},
        {"name": "Sorrel", "months": ["April", "May", "June", "July"], "habitat": "Grassland, Meadows", "regions": ["All"], "difficulty": 1, "parts": "Leaves", "warnings": "Contains oxalic acid, eat in moderation", "lookalikes": ["Lords and Ladies (Poisonous)"], "description": "**Identification:** Arrow-shaped leaves, sharp lemon taste."},
        {"name": "Elderflower", "months": ["June", "July"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Flowers", "warnings": "Don't confuse with dwarf elder", "lookalikes": ["Hemlock (Poisonous)", "Cow Parsley"], "description": "**Identification:** Creamy-white flat flower heads."},
        {"name": "Blackberries", "months": ["August", "September"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Berries", "warnings": "Watch for thorns", "lookalikes": ["None dangerous in UK"], "description": "**Identification:** Bramble with thorns and dark purple/black berries."},
        {"name": "Rosehips", "months": ["September", "October", "November", "December"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Fruit", "warnings": "Remove seeds before eating", "lookalikes": ["None dangerous"], "description": "**Identification:** Red, oval hips on wild rose bushes."},
        {"name": "Hawthorn", "months": ["September", "October"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Berries", "warnings": "Pips contain cyanide - spit out", "lookalikes": ["None dangerous"], "description": "**Identification:** Thorny shrub with red berries (Haws)."},
        {"name": "Chanterelle", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 3, "parts": "Whole mushroom", "warnings": "EXPERT ONLY - False gills", "lookalikes": ["False Chanterelle (Inedible)"], "description": "**Identification:** Egg-yolk yellow, false gills (ridges), smells of apricots."},
        {"name": "Field Mushroom", "months": ["August", "September", "October"], "habitat": "Fields, Meadows", "regions": ["All"], "difficulty": 2, "parts": "Whole mushroom", "warnings": "Beware of yellow staining lookalikes", "lookalikes": ["Yellow Stainer (Poisonous)"], "description": "**Identification:** White cap, pink gills turning brown."},
        {"name": "Hazelnut", "months": ["September", "October"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Nuts", "warnings": "Pick before squirrels get them", "lookalikes": ["None dangerous"], "description": "**Identification:** Shrubby tree, nuts in green husks."},
        {"name": "Sweet Chestnut", "months": ["October", "November"], "habitat": "Woodlands", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Nuts", "warnings": "Do not confuse with Horse Chestnut", "lookalikes": ["Horse Chestnut (Poisonous)"], "description": "**Identification:** Pointed nuts, many nuts per case."},
        # --- NEW ADDITIONS ---
        {"name": "Shepherd's Purse", "months": ["January", "February", "March", "April", "May", "June"], "habitat": "Fields, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Seeds", "warnings": "Best when young, peppery", "lookalikes": ["Thale Cress"], "description": "**Identification:** Heart-shaped seed pods (purses). Rosette of lobed leaves."},
        {"name": "Garlic Mustard", "months": ["April", "May", "June"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Smells of garlic when crushed", "lookalikes": ["None dangerous"], "description": "**Identification:** Heart-shaped leaves, white flowers, tall stems."},
        {"name": "Ground Elder", "months": ["March", "April", "May"], "habitat": "Gardens, Woodlands", "regions": ["All"], "difficulty": 2, "parts": "Young leaves", "warnings": "Can be invasive, pick young", "lookalikes": ["Elder (poisonous bark, different leaves)"], "description": "**Identification:** Leaflets in groups of three, celery smell."},
        {"name": "Wild Carrot", "months": ["June", "July", "August"], "habitat": "Grassland, Meadows", "regions": ["All"], "difficulty": 3, "parts": "Root (young)", "warnings": "EXPERT ONLY. Check for hairy stem. Smells of carrot.", "lookalikes": ["Hemlock (Poisonous)"], "description": "**Identification:** White flat-topped flower, one central red flower (often), hairy stem."},
        {"name": "Pignut", "months": ["May", "June"], "habitat": "Meadows, Hedgerows", "regions": ["All"], "difficulty": 3, "parts": "Tubers", "warnings": "EXPERT ONLY. Difficult to identify.", "lookalikes": ["Other umbellifers"], "description": "**Identification:** Delicate white flower, finely divided leaves. Tubers taste like chestnuts."},
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
        {"name": "Death Cap", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "danger": "EXTREME", "symptoms": "Liver/kidney failure, often fatal", "lookalikes": ["Straw Mushroom"], "description": "**Identification:** Green-yellow cap, white gills, volva at base. **Danger:** Most mushroom deaths."},
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
        'survival_result': None, 'daily_streak': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Helper for AI generation
def generate_text(prompt):
    if client is None:
        return "⚠️ AI Content Unavailable (Library not installed)."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Helper for Audio
def generate_voice(text, filename="temp_audio.mp3"):
    try:
        communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicate.save(filename))
        loop.close()
        return filename
    except Exception as e:
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

            with st.expander(f"{'🌿' if status == 'Edible' else '☠️'} {plant['name']}"):
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
                
                st.info(plant.get('description', 'No info available.'))
                
                # Accessibility: Read Aloud Button
                if st.button(f"🔊 Read Aloud", key=f"read_{plant['name']}"):
                    with st.spinner("Generating audio..."):
                        text_to_read = f"{plant['name']}. {plant.get('description', '')}"
                        audio_file = generate_voice(text_to_read)
                        if audio_file:
                            st.audio(audio_file)

    # --- SUB-TAB 2: LEARNING MODULES ---
    with learn_tab2:
        st.header("🎓 Learning Modules")
        st.markdown("### Structured learning paths for UK foraging")
        
        modules = {
            "🌱 Beginner": [
                {"title": "Introduction to Foraging", "duration": "30 min", "topics": ["Safety basics", "UK Foraging Laws (Countryside Act)", "Essential equipment"]},
                {"title": "Easy Plants to Identify", "duration": "45 min", "topics": ["Dandelions", "Nettles", "Blackberries", "Sorrel"]},
                {"title": "Foraging Ethics", "duration": "20 min", "topics": ["Sustainable harvesting", "Leave no trace", "Sharing knowledge"]},
            ],
            "🌿 Intermediate": [
                {"title": "Seasonal Foraging", "duration": "60 min", "topics": ["Spring greens", "Summer berries", "Autumn nuts", "Winter roots"]},
                {"title": "Coastal Foraging", "duration": "60 min", "topics": ["Seaweeds (Laver)", "Shellfish regulations", "Coastal plants (Samphire)"]},
                {"title": "The Carrot Family", "duration": "45 min", "topics": ["Identifying the Carrot family", "Hemlock vs Wild Carrot", "Pignut identification"]},
            ],
            "🌲 Advanced": [
                {"title": "Mushroom Foraging", "duration": "90 min", "topics": ["Identification keys", "Spore prints", "Common lookalikes (Death Cap)"]},
                {"title": "The Umbellifer Challenge", "duration": "60 min", "topics": ["Identifying the Carrot family", "Hemlock vs Cow Parsley", "Hogweed safety"]},
            ],
            "⚖️ UK Law & Land": [
                {"title": "The Law of the Land", "duration": "45 min", "topics": ["Theft Act 1968", "Countryside Act 1981", "Roadside Verges", "Public Rights of Way"]},
                {"title": "Access Rights", "duration": "30 min", "topics": ["Scotland vs England Laws", "Landowner permissions", "Byelaws"]},
            ]
        }
        
        for level, module_list in modules.items():
            st.markdown(f"### {level}")
            for module in module_list:
                with st.expander(f"📚 {module['title']} ({module['duration']})"):
                    st.markdown("**Topics Covered:**")
                    for topic in module['topics']:
                        st.markdown(f"- {topic}")
                    
                    btn_key = f"module_{module['title']}".replace(" ", "_")
                    
                    # 1. Start Module Button
                    if st.button(f"Start Module: {module['title']}", key=btn_key):
                        with st.spinner("Generating module content..."):
                            prompt = (
                                f"Create a comprehensive foraging lesson on: {module['title']} specifically for the UK. "
                                f"Include specific UK laws (Wildlife and Countryside Act 1981, Theft Act 1968). "
                                f"CRITICAL: Clearly distinguish between 'Picking for Personal Use' vs 'Commercial Sale'. "
                                f"Explain the 'Uprooting' rule. Structure it for a KS2/KS3 student."
                            )
                            content = generate_text(prompt)
                            st.session_state['current_lesson_text'] = content
                            st.session_state['current_lesson_title'] = module['title']
                            # Reset quiz state
                            st.session_state['quiz_active'] = False
                            st.session_state['module_questions'] = None
                            st.rerun()
                    
                    # 2. Display Lesson & Actions (if generated)
                    if st.session_state.get('current_lesson_title') == module['title']:
                        st.markdown("---")
                        st.markdown(st.session_state['current_lesson_text'])
                        
                        # Read Aloud Button
                        if st.button("🔊 Read Aloud", key=f"read_{btn_key}"):
                            with st.spinner("Generating audio..."):
                                audio_file = generate_voice(st.session_state['current_lesson_text'])
                                if audio_file:
                                    st.audio(audio_file)
                        
                        st.markdown("---")
                        
                        # 3. Quiz Logic
                        if not st.session_state.get('quiz_active'):
                            if st.button("📝 Take Quiz", key=f"start_quiz_{btn_key}"):
                                st.session_state['quiz_active'] = True
                                st.rerun()
                        else:
                            # Generate Quiz Question (JSON format for reliability)
                            if 'module_questions' not in st.session_state or st.session_state.get('module_title_quiz') != module['title']:
                                with st.spinner("Generating quiz question..."):
                                    q_prompt = (
                                        f"Based on the following lesson: '{st.session_state['current_lesson_text']}', "
                                        f"create ONE multiple choice question. "
                                        f"Return ONLY valid JSON: {{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\"], \"answer\": \"A\"}}."
                                    )
                                    q_text = generate_text(q_prompt)
                                    
                                    # Simple JSON parser
                                    try:
                                        import json
                                        # Find JSON content
                                        start = q_text.find('{')
                                        end = q_text.rfind('}') + 1
                                        json_str = q_text[start:end]
                                        q_data = json.loads(json_str)
                                        st.session_state['module_questions'] = q_data
                                        st.session_state['module_title_quiz'] = module['title']
                                        st.session_state['quiz_score_mod'] = 0
                                    except Exception as e:
                                        st.error("Error generating quiz. Please try again.")
                                        st.session_state['quiz_active'] = False

                            # Display Quiz
                            if 'module_questions' in st.session_state:
                                q = st.session_state['module_questions']
                                st.markdown("### ❓ Quiz Question:")
                                st.write(q['question'])
                                
                                user_ans = st.radio("Select your answer:", q['options'], key=f"radio_{btn_key}")
                                
                                if st.button("Submit Answer", key=f"submit_ans_{btn_key}"):
                                    if user_ans == q['answer']:
                                        st.success("✅ Correct! You have completed this module.")
                                        st.balloons()
                                        st.session_state['quiz_active'] = False
                                        
                                        # CERTIFICATE LOGIC
                                        st.markdown("### 🏆 Claim your Certificate")
                                        cert_name = st.text_input("Enter your name:", key=f"name_{btn_key}")
                                        if st.button("Download Certificate", key=f"dl_{btn_key}"):
                                            if cert_name:
                                                cert_text = f"""
CERTIFICATE OF COMPLETION
------------------------
Student: {cert_name}
Module: {module['title']}
Date: {datetime.now().strftime("%Y-%m-%d")}
Platform: Rocen Homesteady
Status: PASSED
"""
                                                st.download_button("📥 Download Certificate (.txt)", cert_text, file_name=f"certificate_{module['title'].replace(' ', '_')}.txt")
                                            else:
                                                st.warning("Please enter your name.")
                                    else:
                                        st.error(f"❌ Incorrect. The correct answer was {q['answer']}. Please review the lesson and try again.")
                                        st.session_state['quiz_active'] = False
                                        st.rerun()

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
                correct_habitat = plant['habitat'].split(',')[0].strip()
                if correct_habitat == "Woodlands": correct_habitat = "Woodland"
                if correct_habitat == "Hedgerows": correct_habitat = "Hedgerow"
                
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
            st.markdown("### 💀 GAME OVER")
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
        CASE_FILES = [
            {"clue": "You find a plant with white umbrella-shaped flowers. The stem is smooth and has **purple spots** on it.", "safe_plant": "Wild Carrot", "danger_plant": "Hemlock", "safe_icon": "🥕", "danger_icon": "☠️", "fact": "Hemlock is deadly! The purple spots and smooth stem are the danger signs. Wild Carrot has a hairy stem.", "safe_habitat": "Meadows"},
            {"clue": "You see a plant with broad green leaves in a damp woodland. You crush a leaf, and it smells strongly of **garlic**.", "safe_plant": "Wild Garlic", "danger_plant": "Lily of the Valley", "safe_icon": "🌿", "danger_icon": "☠️", "fact": "Smell is a great identifier! Wild Garlic smells like garlic. Lily of the Valley has no smell and is poisonous.", "safe_habitat": "Woodland"},
            {"clue": "A bright orange mushroom grows under an oak tree. Under the cap, it has ridges (like false gills) that run down the stem. It smells **fruity**.", "safe_plant": "Chanterelle", "danger_plant": "False Chanterelle", "safe_icon": "🍄", "danger_icon": "🚫", "fact": "Chanterelles have 'false gills' (ridges) and smell of apricots. False Chanterelles have true gills and no smell.", "safe_habitat": "Woodland"},
            {"clue": "You find a bush with dark berries. The leaves are arranged in **pairs** opposite each other on the stem.", "safe_plant": "Elderflower", "danger_plant": "Dwarf Elder", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "Elder leaves are opposite (in pairs). Dwarf Elder (Danewort) looks similar but the flowers stand upright, not drooping.", "safe_habitat": "Hedgerow"},
            {"clue": "A tall plant with white flowers grows by a river. The root smells like a pleasant **carrot/parsnip**, not mouse urine.", "safe_plant": "Wild Parsnip", "danger_plant": "Hemlock Water Dropwort", "safe_icon": "🥬", "danger_icon": "💀", "fact": "Hemlock Water Dropwort is the deadliest plant in the UK. Never eat roots unless 100% sure. Always check the smell!", "safe_habitat": "Riverbanks"},
            {"clue": "You see a patch of green leaves growing on the forest floor. They have **jagged edges** and sting when you touch them.", "safe_plant": "Nettles", "danger_plant": "Dog's Mercury", "safe_icon": "🌿", "danger_icon": "⚠️", "fact": "Nettles sting and are edible when cooked. Dog's Mercury does NOT sting but is poisonous. Always check for the sting (with gloves)!", "safe_habitat": "Woodland"},
            {"clue": "You find a tree with dark green needles and a red berry cup. It grows near a **churchyard**.", "safe_plant": "Juniper Berry", "danger_plant": "Yew", "safe_icon": "🫐", "danger_icon": "💀", "fact": "Yew trees are extremely common in churchyards. **Every part is deadly except the red berry flesh.** Avoid completely.", "safe_habitat": "Churchyards"},
            {"clue": "A plant with strap-like leaves grows in the woods. It has a **triangular stem** and smells like onions.", "safe_plant": "Three-Cornered Leek", "danger_plant": "Bluebell", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "Three-Cornered Leek is edible and invasive. Bluebells are poisonous. The 'triangle' stem and onion smell are the keys.", "safe_habitat": "Woodland"},
            {"clue": "A huge plant (over 2 meters tall) with white flowers grows by a river. The stem has **bristly hairs**.", "safe_plant": "Common Hogweed", "danger_plant": "Giant Hogweed", "safe_icon": "🌻", "danger_icon": "⚠️", "fact": "Giant Hogweed sap burns skin in sunlight! It is huge and has bristly purple hairs. Common Hogweed is smaller and safe.", "safe_habitat": "Riverbanks"},
            {"clue": "A fungus grows on an **Elder tree**. It is brown, jelly-like, and looks like an ear.", "safe_plant": "Wood Ear", "danger_plant": "Beech Bracket", "safe_icon": "👂", "danger_icon": "🪵", "fact": "Wood Ear grows specifically on Elder trees. Most other brackets on trees are woody and inedible.", "safe_habitat": "Woodland"}
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
            st.markdown("## 💀 GAME OVER")
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
                    found = [name for name, data in ITEMS_DATA.items() if random.random() < data['rarity']]
                    for f in found: game['inventory'][f] = game['inventory'].get(f, 0) + 1
                    st.success(f"Found: {', '.join(found[:3])}...")
                    st.rerun()

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

        if st.session_state.get('farm_game') is None:
            grid = [[0 for _ in range(6)] for _ in range(5)]
            stream_col = random.randint(1, 4)
            for r in range(5):
                grid[r][stream_col] = 1
                if random.random() > 0.5: stream_col = max(0, min(5, stream_col + random.choice([-1, 1]))); grid[r][stream_col] = 1
            st.session_state.farm_game = {'grid': grid, 'money': 100, 'day': 1, 'tool': 'Carrot', 'invasives_cleared': 0}
        
        game = st.session_state.farm_game
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Day", game['day'])
        col2.metric("💰 Money", f"£{game['money']}")
        col3.metric("🛡️ Guard Badge", game['invasives_cleared'])
        
        tools = {"🥕 Carrot (£10)": "Carrot", "🧹 Clear Invasive (Free)": "Clear"}
        tool_cols = st.columns(len(tools))
        for i, (label, val) in enumerate(tools.items()):
            if tool_cols[i].button(label, key=f"tool_{val}"): game['tool'] = val; st.rerun()
            if game['tool'] == val: tool_cols[i].markdown("**✅ Selected**")

        icons = {0: "🟤", 1: "🌊", 2: "🌱", 3: "🌿", 4: "🌾", 7: "🥀"}
        st.markdown("`🟤` Dirt | `🌊` Stream | `🌱` Seed | `🌿` Growing | `🌾` Ready | `🥀` **Invasive**")
        
        for r in range(5):
            cols = st.columns(6)
            for c in range(6):
                val = game['grid'][r][c]
                icon = icons.get(val, "❓")
                if val == 7 and game['tool'] == "Clear":
                    if cols[c].button("🥀 CLEAR", key=f"{r}_{c}"):
                        game['grid'][r][c] = 0
                        game['invasives_cleared'] += 1
                        st.success("Invasive Removed!")
                        st.rerun()
                elif val == 0 and game['tool'] == "Carrot":
                    can_afford = game['money'] >= 10
                    if cols[c].button(f"Plant (£10)", key=f"plant_{r}_{c}", disabled=not can_afford):
                        game['money'] -= 10
                        game['grid'][r][c] = 2
                        st.rerun()
                elif val == 4:
                    if cols[c].button("🌾 Harvest", key=f"harv_{r}_{c}"):
                        game['money'] += 15
                        game['grid'][r][c] = 0
                        st.success("Sold Crop! +£15")
                        st.rerun()
                else:
                    cols[c].markdown(f"<div style='text-align:center; font-size:24px;'>{icon}</div>", unsafe_allow_html=True)

         if st.button("⏭️ Next Day", key="next_day_farm"):
            # 1. Crop Growth
            for r in range(5):
                for c in range(6):
                    if game['grid'][r][c] == 2: game['grid'][r][c] = 3
                    elif game['grid'][r][c] == 3: game['grid'][r][c] = 4

            # 2. RANDOM EVENTS (Weather & Market)
            event_roll = random.random()
            
            # Event: Market Prices (20% chance)
            if event_roll < 0.2:
                market_item = random.choice(["Carrot", "Wheat", "Corn"])
                price_change = random.choice([-5, +10])
                if price_change > 0:
                    st.toast(f"📈 Good News! {market_item} prices are UP! Sell now for bonus.")
                    game['money'] += 5 # Simplified bonus
                else:
                    st.toast(f"📉 Bad News! {market_item} prices crashed.")

            # Event: Weather Storm (10% chance)
            elif event_roll < 0.3:
                st.toast("🌧️ Heavy Rain! Some crops were washed away.")
                crops = [(r,c) for r in range(5) for c in range(6) if game['grid'][r][c] in [2, 3]]
                if crops:
                    rr, cc = random.choice(crops)
                    game['grid'][rr][cc] = 0

            # 3. INVASIVE SPECIES EVENT (Educational)
            elif event_roll < 0.6: # 30% chance
                # Pick a real invasive species
                invasives = [
                    {"name": "Japanese Knotweed", "fact": "Damages foundations! Very hard to remove."},
                    {"name": "Himalayan Balsam", "fact": "Outcompetes native flowers."},
                    {"name": "Giant Hogweed", "fact": "Sap causes burns! Avoid touching."},
                    {"name": "Rhododendron", "fact": "Toxic soil, prevents trees growing."}
                ]
                invasive = random.choice(invasives)
                
                empty_spots = [(r,c) for r in range(5) for c in range(6) if game['grid'][r][c] == 0]
                if empty_spots:
                    rr, cc = random.choice(empty_spots)
                    game['grid'][rr][cc] = 7
                    st.toast(f"⚠️ {invasive['name']} spotted! {invasive['fact']}")

            game['day'] += 1
            st.rerun()
