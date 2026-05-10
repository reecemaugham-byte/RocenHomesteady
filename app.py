import streamlit as st
import random
import time
import pandas as pd
from collections import Counter
from datetime import datetime

# ==========================================
# PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="Foraging & Off-Grid Games", 
    page_icon="🌿", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the Theme Function
def apply_forest_theme():
    st.markdown("""
    <style>
    /* Main Background - Cream/Paper Texture */
    .stApp {
        background-color: #F5F5DC;
        background-image: radial-gradient(#E8E8D0 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Text Color - Dark Forest Green */
    .stMarkdown, .stHeader, p, label {
        color: #2E4A3E !important;
    }

    /* Headings - Earthy Brown */
    h1, h2, h3 {
        color: #5D4037 !important;
        font-family: 'Georgia', serif !important;
        border-bottom: 2px solid #A5D6A7;
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
        transition: all 0.3s;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #388E3C;
        transform: scale(1.02);
        box-shadow: 4px 4px 8px rgba(0,0,0,0.2);
    }

    /* Game Cards / Boxes */
    .element-container {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }

    /* Sidebar - Light Sage */
    [data-testid="stSidebar"] {
        background-color: #E8F5E9;
    }

    /* Metric Boxes */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 0 0 1px #C8E6C9;
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

    /* Warning Box */
    .warning-box {
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply the theme immediately
apply_forest_theme()

# ==========================================
# DATA
# ==========================================
UK_PLANTS = {
    "edible": [
        {"name": "Wild Garlic", "months": ["March", "April", "May"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Strong smell helps identification", "lookalikes": ["Lily of the Valley (Poisonous)"], "description": "**Identification:** Broad leaves, white flowers, smells strongly of garlic."},
        {"name": "Nettles", "months": ["February", "March", "April", "May", "June"], "habitat": "Woodlands, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Young leaves", "warnings": "Wear gloves when picking", "lookalikes": ["Dead-nettle (Edible, no sting)"], "description": "**Identification:** Jagged leaves, stinging hairs. **Uses:** Soup, tea. **Warning:** Only eat cooked!"},
        {"name": "Dandelion", "months": ["February", "March", "April", "May", "June", "July"], "habitat": "Everywhere", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers, Roots", "warnings": "Avoid areas with dog waste", "lookalikes": ["Cat's Ear (Edible)"], "description": "**Identification:** Yellow flowers, hollow stems, 'lion's tooth' leaves."},
        {"name": "Three-Cornered Leek", "months": ["January", "February", "March", "April"], "habitat": "Woodlands, Hedgerows", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Leaves, Flowers, Bulbs", "warnings": "Invasive species - pick freely!", "lookalikes": ["Bluebell (Poisonous)"], "description": "**Identification:** Strap-like leaves with a 'keel' (triangular shape). Smells like onion/garlic."},
        {"name": "Wood Ear (Jelly Ear)", "months": ["January", "February", "November", "December"], "habitat": "Woodlands (Elder trees)", "regions": ["All"], "difficulty": 2, "parts": "Fungus", "warnings": "Must be cooked, raw can cause itchiness", "lookalikes": ["Other tree fungi"], "description": "**Identification:** Brown, jelly-like, grows on Elder branches."},
        {"name": "Sorrel", "months": ["April", "May", "June", "July"], "habitat": "Grassland, Meadows", "regions": ["All"], "difficulty": 1, "parts": "Leaves", "warnings": "Contains oxalic acid, eat in moderation", "lookalikes": ["Lords and Ladies (Poisonous)"], "description": "**Identification:** Arrow-shaped leaves, sharp lemon taste."},
        {"name": "Elderflower", "months": ["June", "July"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Flowers", "warnings": "Don't confuse with dwarf elder", "lookalikes": ["Hemlock (Poisonous)"], "description": "**Identification:** Creamy-white flat flower heads."},
        {"name": "Blackberries", "months": ["August", "September"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Berries", "warnings": "Watch for thorns", "lookalikes": ["None dangerous in UK"], "description": "**Identification:** Bramble with thorns and dark purple/black berries."},
        {"name": "Rosehips", "months": ["September", "October", "November", "December"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Fruit", "warnings": "Remove seeds before eating", "lookalikes": ["None dangerous"], "description": "**Identification:** Red, oval hips on wild rose bushes."},
        {"name": "Hawthorn", "months": ["September", "October"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Berries", "warnings": "Pips contain cyanide - spit out", "lookalikes": ["None dangerous"], "description": "**Identification:** Thorny shrub with red berries (Haws)."},
        {"name": "Chanterelle", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 3, "parts": "Whole mushroom", "warnings": "EXPERT ONLY - False gills", "lookalikes": ["False Chanterelle (Inedible)"], "description": "**Identification:** Egg-yolk yellow, false gills (ridges), smells of apricots."},
        {"name": "Field Mushroom", "months": ["August", "September", "October"], "habitat": "Fields, Meadows", "regions": ["All"], "difficulty": 2, "parts": "Whole mushroom", "warnings": "Beware of yellow staining lookalikes", "lookalikes": ["Yellow Stainer (Poisonous)"], "description": "**Identification:** White cap, pink gills turning brown."},
        {"name": "Hazelnut", "months": ["September", "October"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Nuts", "warnings": "Pick before squirrels get them", "lookalikes": ["None dangerous"], "description": "**Identification:** Shrubby tree, nuts in green husks."},
        {"name": "Sweet Chestnut", "months": ["October", "November"], "habitat": "Woodlands", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Nuts", "warnings": "Do not confuse with Horse Chestnut", "lookalikes": ["Horse Chestnut (Poisonous)"], "description": "**Identification:** Pointed nuts, many nuts per case."}
    ],
    "poisonous": [
        {"name": "Deadly Nightshade", "months": ["June", "July", "August", "September"], "habitat": "Woodlands, Gardens", "regions": ["All"], "danger": "EXTREME", "symptoms": "Dilated pupils, hallucinations, death", "lookalikes": ["Bilberry"], "description": "**Identification:** Bell-shaped purple flowers, shiny black berries. **Danger:** Fatal."},
        {"name": "Foxglove", "months": ["June", "July", "August"], "habitat": "Gardens, Woodlands", "regions": ["All"], "danger": "HIGH", "symptoms": "Heart failure, nausea", "lookalikes": ["Comfrey"], "description": "**Identification:** Tall spikes of pink/purple trumpet flowers. **Danger:** All parts toxic."},
        {"name": "Hemlock", "months": ["April", "May", "June", "July"], "habitat": "Rivers, Damp areas", "regions": ["All"], "danger": "EXTREME", "symptoms": "Respiratory failure, death", "lookalikes": ["Wild Carrot", "Cow Parsley"], "description": "**Identification:** Tall, purple-spotted stems, smell of mouse urine."},
        {"name": "Death Cap", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "danger": "EXTREME", "symptoms": "Liver/kidney failure, often fatal", "lookalikes": ["Straw Mushroom"], "description": "**Identification:** Green-yellow cap, white gills, volva at base."},
        {"name": "Lords and Ladies", "months": ["March", "April", "May"], "habitat": "Hedgerows, Woods", "regions": ["All"], "danger": "HIGH", "symptoms": "Mouth blistering, swelling", "lookalikes": ["Sorrel", "Wild Garlic"], "description": "**Identification:** Arrow-shaped leaves, orange berries. **Danger:** Causes burning pain."},
        {"name": "Yew", "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "habitat": "Churchyards, Gardens", "regions": ["All"], "danger": "EXTREME", "symptoms": "Cardiac arrest, death", "lookalikes": ["None"], "description": "**Identification:** Dark evergreen needles, red berry cups (arils). **Danger:** Needles and seeds are deadly."},
        {"name": "Giant Hogweed", "months": ["June", "July", "August"], "habitat": "Riverbanks, Waste ground", "regions": ["England", "Scotland"], "danger": "HIGH", "symptoms": "Severe burns, skin sensitivity", "lookalikes": ["Cow Parsley", "Common Hogweed"], "description": "**Identification:** Huge (3m+), hairy stem with purple blotches. **Danger:** Sap burns skin."},
        {"name": "Dog's Mercury", "months": ["February", "March", "April"], "habitat": "Woodlands", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Vomiting, diarrhoea", "lookalikes": ["Nettles"], "description": "**Identification:** Low growing, jagged leaves. **Danger:** Eaten by mistake as salad green."},
        {"name": "Bluebell", "months": ["April", "May"], "habitat": "Woodlands", "regions": ["All"], "danger": "MEDIUM", "symptoms": "Stomach upset, skin irritation", "lookalikes": ["Three-Cornered Leek"], "description": "**Identification:** Blue, bell-shaped flowers. **Danger:** Bulbs are toxic."}
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
        'survival_result': None, 'daily_streak': 0, 'last_result': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- SIDEBAR ---
st.sidebar.title("🌿 Rocen Homesteady")
st.sidebar.markdown("**Educational Foraging Tools**")

# --- MAIN TABS ---
main_tab1, main_tab2 = st.tabs(["📖 Learning", "🎮 Games"])

# ==========================================
# TAB 1: LEARNING
# ==========================================
with main_tab1:
    st.header("📖 UK Foraging Guide")
    st.markdown("### Your guide to safe foraging")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Search Plant")
    with col2:
        filter_type = st.selectbox("Type", ["All", "Edible Only", "Poisonous Only"])
    with col3:
        region_filter = st.selectbox("Region", ["All", "England", "Scotland", "Wales", "N. Ireland"])
    
    st.markdown("---")
    
    # Filter Logic
    plants = []
    if filter_type == "Edible Only":
        plants = [("Edible", p) for p in UK_PLANTS["edible"]]
    elif filter_type == "Poisonous Only":
        plants = [("Poisonous", p) for p in UK_PLANTS["poisonous"]]
    else:
        plants = [("Edible", p) for p in UK_PLANTS["edible"]] + [("Poisonous", p) for p in UK_PLANTS["poisonous"]]

    # Display
    for status, plant in plants:
        if search_term and search_term.lower() not in plant['name'].lower():
            continue
            
        with st.expander(f"{'🌿' if status == 'Edible' else '☠️'} {plant['name']}"):
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
            
            st.info(plant.get('description', 'No info available.'))

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

        # --- DEFINE DICTIONARY AT THE TOP ---
        habitat_icons = {"Woodland": "🌲", "Hedgerow": "🌿", "Coastal": "🏖️", "Urban": "🏡", "Meadow": "🌾"}

        # --- SEASON SELECTOR ---
        st.markdown("### 🗓️ Choose a Season")
        st.markdown("Pick a season to see what's growing in the UK forests!")
        
        season_cols = st.columns(4)
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        season_icons = {"Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"}
        
        current_month = datetime.now().strftime("%B")
        default_season = "Summer"
        if current_month in ["March", "April", "May"]: default_season = "Spring"
        elif current_month in ["June", "July", "August"]: default_season = "Summer"
        elif current_month in ["September", "October", "November"]: default_season = "Autumn"
        else: default_season = "Winter"

        if 'active_season' not in st.session_state:
            st.session_state.active_season = default_season

        for i, s in enumerate(seasons):
            is_earned = s in st.session_state.season_badge_progress
            badge_txt = "🏅" if is_earned else ""
            
            if season_cols[i].button(f"{season_icons[s]} {s} {badge_txt}", key=f"season_{s}", use_container_width=True):
                st.session_state.active_season = s
                st.session_state.current_question = None
                st.rerun()

        st.info(f"**Current Season:** {st.session_state.active_season} {season_icons[st.session_state.active_season]}")
        
        # --- STATS BAR ---
        col1, col2, col3 = st.columns(3)
        col1.metric("🌟 Score", st.session_state.game_score)
        col2.metric("❤️ Lives", "❤️" * max(0, st.session_state.game_lives))
        progress_count = len(st.session_state.season_badge_progress)
        col3.metric("🏅 Badge", f"{progress_count}/4")

        st.markdown("---")

        # --- GAME LOGIC ---
        active_season = st.session_state.active_season
        season_months = {
            "Spring": ["March", "April", "May"], "Summer": ["June", "July", "August"],
            "Autumn": ["September", "October", "November"], "Winter": ["December", "January", "February"]
        }
        
        available_plants = []
        for p in UK_PLANTS["edible"]:
            if any(m in season_months[active_season] for m in p.get("months", [])):
                available_plants.append(p)

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
                
                st.session_state.current_question = {
                    "plant": plant, "correct": correct_habitat, "options": options
                }

            q = st.session_state.current_question
            
            # --- DISPLAY QUESTION ---
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
                        
                        # Show the warning/fact
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
        
        # --- GAME OVER ---
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
        
        # --- GAME DATA: CASE FILES ---
        CASE_FILES = [
            {"clue": "You find a plant with white umbrella-shaped flowers. The stem is smooth and has **purple spots** on it.", "safe_plant": "Wild Carrot", "danger_plant": "Hemlock", "safe_icon": "🥕", "danger_icon": "☠️", "fact": "Hemlock is deadly! The purple spots and smooth stem are the danger signs. Wild Carrot has a hairy stem.", "safe_habitat": "Meadows"},
            {"clue": "You see a plant with broad green leaves in a damp woodland. You crush a leaf, and it smells strongly of **garlic**.", "safe_plant": "Wild Garlic", "danger_plant": "Lily of the Valley", "safe_icon": "🌿", "danger_icon": "☠️", "fact": "Smell is a great identifier! Wild Garlic smells like garlic. Lily of the Valley has no smell and is poisonous.", "safe_habitat": "Woodland"},
            {"clue": "A bright orange mushroom grows under an oak tree. Under the cap, it has ridges (like false gills) that run down the stem. It smells **fruity**.", "safe_plant": "Chanterelle", "danger_plant": "False Chanterelle", "safe_icon": "🍄", "danger_icon": "🚫", "fact": "Chanterelles have 'false gills' (ridges) and smell of apricots. False Chanterelles have true gills and no smell.", "safe_habitat": "Woodland"},
            {"clue": "You find a bush with dark berries. The leaves are arranged in **pairs** opposite each other on the stem.", "safe_plant": "Elderflower", "danger_plant": "Dwarf Elder", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "Elder leaves are opposite (in pairs). Dwarf Elder (Danewort) looks similar but the flowers stand upright, not drooping.", "safe_habitat": "Hedgerow"},
            {"clue": "A tall plant with white flowers grows by a river. The root smells like a pleasant **carrot/parsnip**, not mouse urine.", "safe_plant": "Wild Parsnip", "danger_plant": "Hemlock Water Dropwort", "safe_icon": "🥬", "danger_icon": "💀", "fact": "Hemlock Water Dropwort is the deadliest plant in the UK. Never eat roots unless 100% sure. Always check the smell!", "safe_habitat": "Riverbanks"},
            {"clue": "You see a patch of green leaves growing on the forest floor. They have **jagged edges** and sting when you touch them.", "safe_plant": "Nettles", "danger_plant": "Dog's Mercury", "safe_icon": "🌿", "danger_icon": "⚠️", "fact": "Nettles sting and are edible when cooked. Dog's Mercury does NOT sting but is poisonous. Always check for the sting (with gloves)!", "safe_habitat": "Woodland"},
            {"clue": "You find a tree with dark green needles and a red berry cup. It grows near a **churchyard**.", "safe_plant": "Juniper Berry", "danger_plant": "Yew", "safe_icon": "🫐", "danger_icon": "💀", "fact": "Yew trees are extremely common in churchyards. **Every part is deadly except the red berry flesh.** Avoid completely.", "safe_habitat": "Churchyards"},
            {"clue": "A plant with strap-like leaves grows in the woods. It has a **distinct triangular shape** in the stem and smells like onions.", "safe_plant": "Three-Cornered Leek", "danger_plant": "Bluebell", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "Three-Cornered Leek is edible and invasive. Bluebells are poisonous. The 'triangle' stem and onion smell are the keys.", "safe_habitat": "Woodland"},
            {"clue": "A huge plant (over 2 meters tall) with white flowers grows by a river. The stem has **bristly hairs**.", "safe_plant": "Common Hogweed", "danger_plant": "Giant Hogweed", "safe_icon": "🌻", "danger_icon": "⚠️", "fact": "Giant Hogweed sap burns skin in sunlight! It is huge and has bristly purple hairs. Common Hogweed is smaller and safe.", "safe_habitat": "Riverbanks"},
            {"clue": "A fungus grows on an **Elder tree**. It is brown, jelly-like, and looks like an ear.", "safe_plant": "Wood Ear", "danger_plant": "Beech Bracket", "safe_icon": "👂", "danger_icon": "🪵", "fact": "Wood Ear grows specifically on Elder trees. Most other brackets on trees are woody and inedible.", "safe_habitat": "Woodland"}
        ]

        # --- UI HEADER ---
        st.markdown("### 🕵️‍♂️ The Safety Inspector")
        progress = st.session_state.survival_correct_count / 5
        st.progress(progress, text=f"Badge Progress: {st.session_state.survival_correct_count}/5 Cases Solved")
        
        col1, col2 = st.columns(2)
        col1.metric("❤️ Lives", "❤️" * max(0, st.session_state.survival_lives))
        col2.metric("🌟 Score", st.session_state.survival_score)
        st.markdown("---")

        # --- GAME LOGIC ---
        if st.session_state.survival_current_case is None:
            st.session_state.survival_current_case = random.choice(CASE_FILES)
            st.session_state.survival_result = None

        case = st.session_state.survival_current_case

        st.info(f"🔎 **New Case File Found!**")
        st.markdown(f"**Habitat:** {case['safe_habitat']}")
        st.markdown(f"**Your Observation:** {case['clue']}")
        st.markdown("#### ⚠️ VERDICT: Is this plant SAFE to touch/harvest?")

        options = [
            {"name": case['safe_plant'], "icon": case['safe_icon'], "is_safe": True},
            {"name": case['danger_plant'], "icon": case['danger_icon'], "is_safe": False}
        ]
        random.shuffle(options)

        if st.session_state.survival_result is None:
            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button(f"{options[0]['icon']} {options[0]['name']}", key="surv_opt_1", use_container_width=True):
                if options[0]['is_safe']:
                    st.session_state.survival_result = "correct"
                    st.session_state.survival_score += 20
                    st.session_state.survival_correct_count += 1
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
                else:
                    st.session_state.survival_result = "wrong"
                    st.session_state.survival_lives -= 1
                    st.session_state.survival_correct_count = 0
                st.rerun()
        else:
            if st.session_state.survival_result == "correct":
                st.success("✅ CASE SOLVED! Great work, Inspector.")
                st.balloons()
            else:
                st.error("☠️ DANGER! That was the wrong choice.")
            
            st.markdown("### 📝 Safety Report")
            st.warning(case['fact'])

            if st.session_state.survival_correct_count >= 5:
                st.markdown("# 🏅 BADGE EARNED: Plant Safety Expert!")
                st.snow()
                st.session_state.survival_correct_count = 0 

            if st.button("📋 Next Case", key="next_case_btn"):
                st.session_state.survival_current_case = None
                st.rerun()

        if st.session_state.survival_lives <= 0:
            st.markdown("## 💀 GAME OVER")
            st.markdown("The forest is dangerous. Remember the rules!")
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

        col1, col2, col3 = st.columns(3)
        col1.metric("🔥 Streak", f"{st.session_state.daily_streak} Days")
        col2.metric("🌟 Score", st.session_state.quiz_score)
        col3.metric("❓ Question", f"{st.session_state.quiz_q_num}/{st.session_state.quiz_max}")
        st.progress(st.session_state.quiz_q_num / st.session_state.quiz_max)

        if st.session_state.quiz_q_num < st.session_state.quiz_max:
            if st.session_state.get('q_data') is None:
                q_type = random.choice(["edible_check", "parts_check", "season_check"])
                plant = random.choice(UK_PLANTS['edible'] + UK_PLANTS['poisonous'])
                
                question_text = ""
                correct_answer = ""
                options = []
                fun_fact = ""

                if q_type == "edible_check":
                    question_text = f"Is **{plant['name']}** safe to eat?"
                    correct_answer = "Edible" if plant in UK_PLANTS['edible'] else "Poisonous"
                    options = ["Edible", "Poisonous"]
                    fun_fact = f"**Warning:** {plant.get('warnings', 'Always double check!')}" if correct_answer == "Edible" else f"**Danger:** {plant.get('symptoms', 'Toxic!')}"
                elif q_type == "parts_check":
                    plant = random.choice(UK_PLANTS['edible']) 
                    parts = plant.get('parts', ['Leaves'])
                    correct_answer = parts[0]
                    wrong_parts = ["Roots", "Berries", "Flowers", "Seeds"]
                    wrong_options = [p for p in wrong_parts if p not in parts]
                    question_text = f"Which part of **{plant['name']}** do we usually eat?"
                    options = [correct_answer] + random.sample(wrong_options, 2)
                    fun_fact = f"**Tip:** {plant.get('warnings', 'Always wash plants before eating.')}"
                elif q_type == "season_check":
                    plant = random.choice(UK_PLANTS['edible'])
                    correct_months = plant.get('months', ['Summer'])
                    correct_answer = correct_months[0]
                    all_months = ["January", "March", "June", "August", "October", "December"]
                    wrong_months = [m for m in all_months if m not in correct_months]
                    question_text = f"When is **{plant['name']}** best harvested?"
                    options = [correct_answer] + random.sample(wrong_months, 2)
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
            final_score = st.session_state.quiz_score
            if final_score == st.session_state.quiz_max: st.success("PERFECT SCORE! You are a Foraging Master!")
            elif final_score >= st.session_state.quiz_max / 2: st.info("Good job! Keep learning.")
            else: st.warning("Keep practicing!")

            if st.button("🔄 Try Again", key="restart_quiz"):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.rerun()

    # ==========================================
    # GAME TAB 4: ECO-VILLAGE
    # ==========================================
    with tab4:
        st.header("🏘️ Eco-Village Builder")
        st.markdown("### Build, Grow, and Protect Nature!")
        
        # --- GAME DATA (Simplified) ---
        ITEMS_DATA = {"Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 2}, "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1}, "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 3}, "Wood": {"icon": "🪵", "rarity": 0.6, "value": 2}, "Stone": {"icon": "🪨", "rarity": 0.4, "value": 2}, "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 5}, "Blackberry": {"icon": "🫐", "rarity": 0.4, "value": 4}, "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 10}, "Milk": {"icon": "🥛", "rarity": 0.0, "value": 15}}
        RECIPES = {"Dandelion Tea": {"ingredients": {"Dandelion": 5, "Water": 1}, "sell": 15}, "Nettle Soup": {"ingredients": {"Nettle": 5, "Water": 1, "Wood": 1}, "sell": 20}, "Blackberry Jam": {"ingredients": {"Blackberry": 10, "Wood": 1}, "sell": 35}}
        BUILDINGS = {"House": {"cost": 50, "icon": "🏠", "desc": "Shelter to recover stamina."}, "Well": {"cost": 30, "icon": "🪨", "desc": "Passive water income."}, "Coop": {"cost": 40, "icon": "🐔", "desc": "Hold up to 5 chickens."}, "Barn": {"cost": 80, "icon": "🐄", "desc": "Hold up to 3 cows."}}

        if st.session_state.get('village') is None:
            st.session_state.village = {'grid': [['🌲' for _ in range(6)] for _ in range(4)], 'stats': {'Food': 50, 'Water': 50, 'Power': 0, 'Stamina': 100, 'Money': 100}, 'inventory': {}, 'animals': [], 'buildings': [], 'day': 1, 'season': 'Spring', 'placement_mode': None, 'nature_health': 100}
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
            st.markdown("---")

        map_tab, forage_tab, market_tab = st.tabs(["🗺️ Map", "🌲 Forage", "🛒 Market"])

        with map_tab:
            st.markdown(f"### 📅 Day {game['day']} | {game['season']}")
            render_stats()
            st.markdown("#### 🛠️ Build Mode")
            options = ["None"] + list(BUILDINGS.keys())
            selected_build = st.selectbox("Select Building", options)
            game['placement_mode'] = selected_build if selected_build != "None" else None
            if game['placement_mode']:
                b = BUILDINGS[game['placement_mode']]
                st.write(f"**Cost:** £{b['cost']} | **Icon:** {b['icon']} | {b['desc']}")
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
                            game['buildings'].append(game['placement_mode'])
                            st.rerun()
                    else:
                        cols[col_idx].markdown(f"<div style='text-align:center; font-size:24px;'>{current_icon}</div>", unsafe_allow_html=True)
            if st.button("⏭️ Next Day", key="vill_next_day"):
                game['stats']['Food'] -= 3
                game['stats']['Water'] -= 2
                game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
                game['nature_health'] = min(100, game['nature_health'] + 10)
                if "Well" in game['buildings']: game['stats']['Water'] += 10
                game['inventory']['Eggs'] = game['inventory'].get('Eggs', 0) + game['animals'].count('Chicken')
                game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + game['animals'].count('Cow')
                game['day'] += 1
                st.rerun()

        with forage_tab:
            st.markdown("### 🌲 Gather Resources")
            render_stats()
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Forage Plants", key="fp1", use_container_width=True):
                    if game['stats']['Stamina'] >= 10:
                        game['stats']['Stamina'] -= 10
                        found = [name for name, data in ITEMS_DATA.items() if random.random() < data['rarity']]
                        for f in found: game['inventory'][f] = game['inventory'].get(f, 0) + 1
                        st.success(f"Found: {', '.join(found[:3])}...")
                        st.rerun()
                    else:
                        st.warning("Not enough stamina!")
            with c2:
                if st.button("Gather Wood", key="fm1", use_container_width=True):
                    game['inventory']['Wood'] = game['inventory'].get('Wood', 0) + 2
                    st.success("Found Wood")
                    st.rerun()
            st.markdown("#### 🎒 Inventory")
            st.write(game['inventory'] if game['inventory'] else "Empty")

        with market_tab:
            st.markdown("### 🛒 Market")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🐔 Chicken (£15)**")
                if st.button("Buy Chicken", key="buy_chick"):
                    if game['stats']['Money'] >= 15:
                        game['stats']['Money'] -= 15
                        game['animals'].append('Chicken')
                        st.rerun()
            with col2:
                st.markdown("**🐄 Cow (£60)**")
                if st.button("Buy Cow", key="buy_cow"):
                    if game['stats']['Money'] >= 60:
                        game['stats']['Money'] -= 60
                        game['animals'].append('Cow')
                        st.rerun()

    # ==========================================
    # GAME TAB 5: FARM TYCOON
    # ==========================================
    with tab5:
        st.header("🚜 Farm Tycoon: Nature Guardians")
        st.markdown("### Build your farm, watch for **Invasive Species**!")
        
        if st.session_state.get('farm_game') is None:
            grid = [[0 for _ in range(6)] for _ in range(5)]
            stream_col = random.randint(1, 4)
            for r in range(5):
                grid[r][stream_col] = 1
                if random.random() > 0.5: stream_col = max(0, min(5, stream_col + random.choice([-1, 1]))); grid[r][stream_col] = 1
            st.session_state.farm_game = {'grid': grid, 'money': 100, 'day': 1, 'season': 'Spring', 'weather': '☀️ Sunny', 'tool': '🥕 Carrot', 'game_over': False, 'invasives_cleared': 0}
        
        game = st.session_state.farm_game
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Day", game['day'])
        col2.metric("💰 Money", f"£{game['money']}")
        col3.metric("🛡️ Guard Badge", game['invasives_cleared'])
        
        if st.button("⏭️ Next Day", key="fd_next"):
            # Growth logic
            for r in range(5):
                for c in range(6):
                    if game['grid'][r][c] == 2: game['grid'][r][c] = 3
                    elif game['grid'][r][c] == 3: game['grid'][r][c] = 4
            # Spawn Invasive
            if random.random() < 0.3:
                empty = [(r,c) for r in range(5) for c in range(6) if game['grid'][r][c] == 0]
                if empty:
                    rr, cc = random.choice(empty)
                    game['grid'][rr][cc] = 7
            game['day'] += 1
            st.rerun()

        # Grid Display
        icons = {0: "🟫", 1: "🌊", 2: "🌱", 3: "🌿", 4: "🌾", 5: "🐔", 6: "🐄", 7: "🔴"}
        st.markdown("### 🗺️ Your Farm")
        for r in range(5):
            cols = st.columns(6)
            for c in range(6):
                val = game['grid'][r][c]
                cols[c].markdown(f"<div style='text-align:center; font-size:24px;'>{icons[val]}</div>", unsafe_allow_html=True)
