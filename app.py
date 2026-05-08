import streamlit as st
import random
import time
import pandas as pd
from collections import Counter
from datetime import datetime
from pathlib import Path
import json
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Rocen Homestead - Foraging", page_icon="🌿", layout="wide")

# --- PASSWORD PROTECTION ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("🔒 Please enter the password to access this app.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("🔓 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- DATA (HARDCODED FOR ZERO COST) ---
UK_PLANTS = {
    "edible": [
        {"name": "Wild Garlic", "months": ["March", "April", "May"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers", "warnings": "Strong smell helps identification", "lookalikes": ["Lily of the Valley (Poisonous)"], "description": "Wild garlic has broad leaves and smells strongly of garlic. Found in damp woods. Use in pesto."},
        {"name": "Nettles", "months": ["February", "March", "April", "May", "June"], "habitat": "Woodlands, Gardens", "regions": ["All"], "difficulty": 1, "parts": "Young leaves", "warnings": "Wear gloves", "lookalikes": ["Dead-nettle (Edible)"], "description": "Stinging hairs. High in iron. Good for soup."},
        {"name": "Dandelion", "months": ["March", "April", "May", "June", "July"], "habitat": "Everywhere", "regions": ["All"], "difficulty": 1, "parts": "Leaves, Flowers, Roots", "warnings": "Avoid dog waste areas", "lookalikes": ["Cat's Ear"], "description": "Yellow flowers. All parts edible. Roots can be dried for coffee."},
        {"name": "Elderflower", "months": ["June", "July"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Flowers", "warnings": "Don't confuse with dwarf elder", "lookalikes": ["Hemlock (Poisonous)"], "description": "Creamy white flowers. Famous for cordial."},
        {"name": "Blackberries", "months": ["August", "September"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 1, "parts": "Berries", "warnings": "Thorns!", "lookalikes": ["None dangerous"], "description": "Delicious raw or in crumbles. Very common in UK hedges."},
        {"name": "Rosehips", "months": ["September", "October", "November"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Fruit", "warnings": "Itchy seeds inside", "lookalikes": ["None"], "description": "High Vitamin C. Used for syrup."},
        {"name": "Hawthorn", "months": ["September", "October"], "habitat": "Hedgerows", "regions": ["All"], "difficulty": 2, "parts": "Berries", "warnings": "Pips contain cyanide", "lookalikes": ["None"], "description": "Red berries. Good for heart health (jellies)."},
        {"name": "Hazelnut", "months": ["September", "October"], "habitat": "Hedgerows, Woods", "regions": ["All"], "difficulty": 1, "parts": "Nuts", "warnings": "Race the squirrels", "lookalikes": ["None"], "description": "Familiar nuts in green husks."},
        {"name": "Sweet Chestnut", "months": ["October", "November"], "habitat": "Woodlands", "regions": ["England", "Wales"], "difficulty": 1, "parts": "Nuts", "warnings": "Don't confuse with Horse Chestnut", "lookalikes": ["Horse Chestnut (Poisonous)"], "description": "Pointed nuts. Roast them."},
        {"name": "Chanterelle", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "difficulty": 3, "parts": "Mushroom", "warnings": "Expert Only", "lookalikes": ["False Chanterelle"], "description": "Yellow funnel. Smells of apricots."},
    ],
    "poisonous": [
        {"name": "Deadly Nightshade", "months": ["June", "July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "danger": "EXTREME", "symptoms": "Death", "lookalikes": ["Bilberry"], "description": "Purple flowers, black berries. Fatal."},
        {"name": "Foxglove", "months": ["June", "July", "August"], "habitat": "Gardens, Woods", "regions": ["All"], "danger": "HIGH", "symptoms": "Heart issues", "lookalikes": ["Comfrey"], "description": "Tall pink spikes. Do not touch."},
        {"name": "Hemlock", "months": ["April", "May", "June", "July"], "habitat": "Rivers", "regions": ["All"], "danger": "EXTREME", "symptoms": "Death", "lookalikes": ["Cow Parsley"], "description": "Purple spots on stem. Smells of mouse urine."},
        {"name": "Death Cap", "months": ["July", "August", "September"], "habitat": "Woodlands", "regions": ["All"], "danger": "EXTREME", "symptoms": "Liver failure", "lookalikes": ["Straw Mushroom"], "description": "Green cap. Responsible for most mushroom deaths."},
        {"name": "Lords and Ladies", "months": ["March", "April", "May"], "habitat": "Hedgerows", "regions": ["All"], "danger": "HIGH", "symptoms": "Burning mouth", "lookalikes": ["Sorrel"], "description": "Arrow leaves, orange berries."},
    ]
}

UK_ENVIRONMENTS = {
    "Coastal": ["Marsh Samphire", "Sea Kale"],
    "Woodland": ["Wild Garlic", "Chanterelle", "Sweet Chestnut", "Hazelnut"],
    "Hedgerow": ["Elderflower", "Blackberries", "Rosehips", "Hawthorn"],
    "Urban": ["Dandelion", "Nettles"],
    "Mountain/Moorland": ["Cloudberry", "Blaeberry"]
}

# --- SESSION STATE INIT ---
def init_session_state():
    defaults = {
        'game_score': 0, 'game_lives': 3, 'game_streak': 0, 'current_question': None,
        'village': None, 'farm_game': None, 'survival_lives': 3, 'survival_score': 0,
        'current_survival_pair': None, 'quiz_score': 0, 'quiz_q_num': 0, 'quiz_max': 5,
        'q_data': None, 'daily_streak': 0, 'survival_correct_count': 0,
        'active_season': 'Spring', 'season_badge_progress': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- SIDEBAR ---
st.sidebar.title("🌿 Rocen Homestead")
st.sidebar.markdown("**Educational Foraging Tools**")

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["📖 Learning", "🎮 Games"])

# ==========================================
# TAB 1: LEARNING
# ==========================================
with tab1:
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
        # Simple search filter
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
            
            # Hardcoded Description
            st.info(plant.get('description', 'No info available.'))

# ==========================================
# TAB 2: GAMES
# ==========================================
with tab2:
    st.header("🎮 Foraging Games")
    st.markdown("### Learn by playing!")
    
    g_tab1, g_tab2, g_tab3, g_tab4, g_tab5 = st.tabs([
        "🌿 Quest", "☠️ Survival", "🎯 Quiz", "🏘️ Village", "🚜 Farm"
    ])

    # --- GAME 1: QUEST ---
    with g_tab1:
        st.markdown("#### 🌿 Seasonal Quest")
        # (Condensed Logic for Quest)
        st.metric("Score", st.session_state.game_score)
        if st.button("Start New Quest"):
            st.session_state.game_score = 0
            st.session_state.game_lives = 3
        
        # Pick random plant and ask season
        plant = random.choice(UK_PLANTS['edible'])
        st.write(f"**Find:** {plant['name']}")
        st.write(f"**Habitat:** {plant['habitat']}")
        st.write(f"**Available in:** {', '.join(plant['months'])}")
        
        if st.button("Mark as Found"):
            st.session_state.game_score += 10
            st.balloons()
            st.success("Well done!")

    # --- GAME 2: SURVIVAL ---
    with g_tab2:
        st.markdown("#### ☠️ Survival School")
        st.metric("Lives", st.session_state.survival_lives)
        
        # Pick one safe, one dangerous
        safe = random.choice(UK_PLANTS['edible'])
        danger = random.choice(UK_PLANTS['poisonous'])
        
        st.write(f"Which is SAFE? **{safe['name']}** or **{danger['name']}**?")
        
        c1, c2 = st.columns(2)
        if c1.button(f"🌿 {safe['name']}"):
            st.success("Correct! It is edible.")
        if c2.button(f"☠️ {danger['name']}"):
            st.error("DANGER! That is poisonous.")
            st.session_state.survival_lives -= 1

    # --- GAME 3: QUIZ ---
    with g_tab3:
        st.markdown("#### 🎯 Daily Quiz")
        st.metric("Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_max}")
        
        plant = random.choice(UK_PLANTS['edible'] + UK_PLANTS['poisonous'])
        correct = "Edible" if plant in UK_PLANTS['edible'] else "Poisonous"
        
        st.write(f"Is **{plant['name']}** Edible or Poisonous?")
        c1, c2 = st.columns(2)
        if c1.button("Edible", key="q_ed"):
            if correct == "Edible":
                st.success("Correct!")
                st.session_state.quiz_score += 1
            else:
                st.error("Wrong!")
        if c2.button("Poisonous", key="q_po"):
            if correct == "Poisonous":
                st.success("Correct!")
                st.session_state.quiz_score += 1
            else:
                st.error("Wrong!")

    # --- GAME 4: VILLAGE ---
    with g_tab4:
        st.markdown("#### 🏘️ Eco-Village")
        st.info("Build your village! (Simplified for Public Version)")
        
        if 'village' not in st.session_state or st.session_state.village is None:
            st.session_state.village = {'stats': {'Money': 100}, 'inventory': {}}
        
        game = st.session_state.village
        
        st.metric("Money", game['stats']['Money'])
        
        if st.button("Forage for Resources"):
            found = random.choice(["Wood", "Stone", "Dandelion"])
            game['inventory'][found] = game['inventory'].get(found, 0) + 1
            st.success(f"Found {found}!")
        
        st.write("Inventory:", game['inventory'])

    # --- GAME 5: FARM ---
    with g_tab5:
        st.markdown("#### 🚜 Farm Tycoon")
        st.info("Manage your farm! (Simplified for Public Version)")
        
        if 'farm' not in st.session_state or st.session_state.farm is None:
            st.session_state.farm = {'Money': 50, 'Day': 1}
        
        farm = st.session_state.farm
        st.metric("Day", farm['Day'])
        st.metric("Money", farm['Money'])
        
        if st.button("Next Day"):
            farm['Day'] += 1
            farm['Money'] += 10
            st.success("New Day!")

