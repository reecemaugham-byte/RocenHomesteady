import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar, UK_PLANTS, generate_voice, EDGE_TTS_AVAILABLE

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Games - Rocen Homesteady",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
init_session_state()
apply_brand_theme()
render_sidebar()

st.title("🎮 Games & Practice")

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
            
            # UPDATED HABITAT MAPPING
            if raw_habitat in ["Woodlands", "Woods", "Wood", "Plantations"]: correct_habitat = "Woodland"
            elif raw_habitat in ["Hedgerows", "Hedgerow", "Roadsides", "Scrub"]: correct_habitat = "Hedgerow"
            elif raw_habitat in ["Meadows", "Grassland", "Fields", "Fields, Gardens", "Lawns"]: correct_habitat = "Meadow"
            elif raw_habitat in ["Coastal", "Coastal Saltmarshes", "Shingle Beaches", "Rocky Coasts", "Sandy/Muddy Beaches", "Estuaries"]: correct_habitat = "Coastal"
            elif raw_habitat in ["Riverbanks", "Wet ground", "Damp Meadows"]: correct_habitat = "Meadow" # Damp meadows often overlap
            else: correct_habitat = "Urban" # Default fallback

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
            {"clue": "A plant with strap-like leaves grows in the woods. You roll the stem between your fingers—it feels **triangular** (like a keel ⛵).", "rule": "✅ **Rule:** A triangular stem is a unique ID feature.", "safe_plant": "Three-Cornered Leek", "danger_plant": "Bluebell", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Bluebell (POISON):** Round stem. Blue bells. All parts toxic.\n- **Three-Cornered Leek (Safe):** Triangular stem. White flowers. Smells like onion/garlic. **Triangle = Tasty.**", "safe_habitat": "Woodland"},
            
            # --- NEW CASES ADDED ---
            {"clue": "You find a mushroom with a honeycomb cap (pitted like a sponge). You cut it open and it is **completely hollow** inside.", "rule": "✅ **Rule:** If it's hollow like a balloon, it might be a Morel.", "safe_plant": "Morel", "danger_plant": "False Morel", "safe_icon": "🍄", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **False Morel (POISON):** Looks brain-like (wrinkled). Inside is chambered/solid (NOT hollow).\n- **Morel (Safe):** Honeycomb cap. Completely hollow inside. **Hollow = Happy.**", "safe_habitat": "Woodland"},
            {"clue": "You are in a dry meadow. You dig up a small tuber. The stem is fine and feathery (like a carrot). The area is **dry and grassy**.", "rule": "✅ **Rule:** Habitat is key. Pignut likes dry ground.", "safe_plant": "Pignut", "danger_plant": "Hemlock Water Dropwort", "safe_icon": "🥔", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Hemlock Water Dropwort (DEADLY):** Grows in WET ground (ditches/rivers). Roots look like fingers.\n- **Pignut (Safe):** Grows in DRY meadows. Single small tuber. **Wet = Worry. Dry = Dig.**", "safe_habitat": "Meadow"},
            {"clue": "You see an evergreen tree. You pick a needle and roll it in your fingers. It feels **round** and comes in a **bundle of two**.", "rule": "✅ **Rule:** Round needles in bundles are Pine. Flat needles are Yew.", "safe_plant": "Pine Needles", "danger_plant": "Yew", "safe_icon": "🌲", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Yew (POISON):** Flat needles. Single, not in bundles. No smell.\n- **Pine (Safe):** Round needles in bundles (2-5). Smells of resin. **Round & Bundles = Safe.**", "safe_habitat": "Woodland"},
            {"clue": "You are on a beach. You see a green, fleshy plant with jointed stems that looks like a mini cactus 🌵.", "rule": "✅ **Rule:** If it looks like a succulent cactus on a mudflat, it's likely Samphire.", "safe_plant": "Marsh Samphire", "danger_plant": "Sea Holm (Unknown)", "safe_icon": "🥒", "danger_icon": "❓", "fact": "🕵️ **Inspector's Report:**\n- **Samphire (Safe):** Green, jointed stems. Crunchy. No dangerous lookalikes on saltmarsh.\n- **Safety:** Just check for mud washing. No poisons look like this.", "safe_habitat": "Coastal"},
            {"clue": "You find a tree with red berries. The berries are in a **cup** (like a little red egg cup).", "rule": "✅ **Rule:** Red berries in a cup are Yew (Poison). Red berries in a spike are Rowan/Hawthorn.", "safe_plant": "Hawthorn", "danger_plant": "Yew", "safe_icon": "🔴", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Yew (POISON):** Red berry is an open cup (aril) with a seed inside.\n- **Hawthorn (Safe):** Red berry is a solid fruit (like a tiny apple). **Cups = Cut it out.**", "safe_habitat": "Hedgerow"}
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
# GAME TAB 4: ECO-VILLAGE
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

    ITEMS_DATA = {
        "Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 2}, 
        "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1}, 
        "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 3}, 
        "Wood": {"icon": "🪵", "rarity": 0.6, "value": 2}, 
        "Stone": {"icon": "🪨", "rarity": 0.4, "value": 2}, 
        "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 5}, 
        "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 10}, 
        "Milk": {"icon": "🥛", "rarity": 0.0, "value": 15},
        # NEW ITEMS
        "Samphire": {"icon": "🥒", "rarity": 0.3, "value": 15},
        "Birch Sap": {"icon": "🥛", "rarity": 0.4, "value": 10},
        "Crab Apple": {"icon": "🍎", "rarity": 0.5, "value": 5}
    }

    BUILDINGS = {
        "House": {"cost": 50, "icon": "🏠", "desc": "Shelter to recover stamina."}, 
        "Well": {"cost": 30, "icon": "🪨", "desc": "Passive water income."}, 
        "Coop": {"cost": 40, "icon": "🐔", "desc": "Hold up to 5 chickens."}
    }

    # FIX: Indentation corrected for the if statement block
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
            if st.button("🥫 Preserve Food (Cost: 10 Food)", key="preserve_btn"):
                if game['stats']['Food'] >= 10:
                    game['stats']['Food'] -= 10
                    game['preserved_food'] += 5
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
