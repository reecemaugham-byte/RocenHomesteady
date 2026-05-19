import streamlit as st
import random
import time
import re
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar, UK_PLANTS, LESSON_CONTENT, generate_voice, EDGE_TTS_AVAILABLE, ACHIEVEMENTS

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Games - Rocen Homesteady",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    div.grid-game div.stButton > button {
        width: 100% !important; height: auto !important; aspect-ratio: 1 / 1 !important;
        padding: 0 !important; font-size: 1.5em !important; border: 1px solid #444 !important;
        background-color: #2b2b2b !important; color: white !important; border-radius: 8px !important;
    }
    div.grid-game div.stButton > button:hover { border-color: #fff !important; transform: scale(1.05); }
    .plant-card {
        border-radius: 20px; padding: 20px; text-align: center;
        background: linear-gradient(145deg, #2b2b2b, #1a1a1a);
        box-shadow: 10px 10px 20px #1a1a1a; margin-bottom: 20px; border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTION: AUDIO SANITIZER ---
def clean_text_for_audio(text):
    if not text: return ""
    text = text.replace("**", "").replace("##", "").replace("*", "")
    icon_map = {"🌿": "Plant", "🌲": "Woodland", "☠️": "Poison", "✅": "Correct", "❌": "Wrong"}
    for icon, word in icon_map.items(): text = text.replace(icon, word)
    return text.strip()

# --- INIT ---
init_session_state()
apply_brand_theme()

# Initialize Achievements if not exists or empty
if 'achievements' not in st.session_state or not st.session_state.achievements:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}

# --- SIDEBAR (CUSTOM FOR GAMES) ---
with st.sidebar:
    st.title("Rocen Homesteady")
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("🌿 **Rocen Homesteady**")
    st.markdown("---")
    
    # Hall of Fame
    unlocked_count = sum(1 for v in st.session_state.achievements.values() if v)
    total_count = len(ACHIEVEMENTS)
    st.metric("🏆 Achievements", f"{unlocked_count} / {total_count}")
    
    unlocked_keys = [k for k, v in st.session_state.achievements.items() if v]
    if unlocked_keys:
        st.caption("Recently Unlocked:")
        for key in unlocked_keys[-3:]:
            st.write(f"✅ {ACHIEVEMENTS[key]['name']}")
    
    # Reset Button
    st.markdown("---")
    if st.button("🔄 Reset All Games"):
        # Reset Game Stats
        st.session_state.game_score = 0
        st.session_state.game_lives = 3
        st.session_state.game_streak = 0
        st.session_state.survival_lives = 3
        st.session_state.survival_score = 0
        st.session_state.survival_correct_count = 0
        st.session_state.total_plants_identified = 0
        st.session_state.player_title = "Novice Gatherer"
        st.session_state.season_badge_progress = []
        
        # Reset Inventories
        st.session_state.master_inventory = {}
        st.session_state.village = None
        st.session_state.farm_game = None
        
        # Reset Achievements
        st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}
        
        st.success("All Games Reset!")
        st.rerun()

st.title("🎮 Games & Practice")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌿 Foraging Quest",
    "☠️ Survival School",
    "🎲 Daily Quiz",
    "🏘️ Eco-Village",
    "🚜 Farm Tycoon",
    "🍳 The Wild Kitchen"
])

# ==========================================
# GAME TAB 1: FORAGING QUEST
# ==========================================
with tab1:
    st.header("🌿 The Seasonal Quest")
    st.caption("📚 Curriculum Link: Science (Seasonal Changes, Plants)")

    # --- HOW TO PLAY ---
    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Select a Season** using the buttons at the top.
        2. A plant will appear. Read the **Botanical Clue** carefully.
        3. Identify the plant based on the clue, then choose where it grows.
        4. **Collect Plants:** Find unique plants to fill your Herbarium.
        5. **Bonus:** Get 5 right in a row to unlock a Bonus Question!
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

    # --- COLLECTION TRACKER ---
    collection_list = list(st.session_state.master_inventory.keys())
    total_found = len(collection_list)
    
    st.sidebar.metric("🌿 Species Found", f"{total_found}/50")
    if total_found > 0:
        with st.sidebar.expander("View Collection"):
            for p in collection_list[-5:]:
                st.write(f"✅ {p}")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌟 Score", st.session_state.get('game_score', 0))
    col2.metric("❤️ Lives", "❤️" * max(0, st.session_state.get('game_lives', 3)))
    col3.metric("🔥 Streak", st.session_state.get('game_streak', 0))
    st.markdown("---")

    active_season = st.session_state.active_season
    season_months = {"Spring": ["March", "April", "May"], "Summer": ["June", "July", "August"], "Autumn": ["September", "October", "November"], "Winter": ["December", "January", "February"]}

    available_plants = [p for p in UK_PLANTS["edible"] if any(m in season_months[active_season] for m in p.get("months", []))]

    if not available_plants:
        st.warning(f"Not much grows in {active_season}! Try another season.")
    else:
        # --- BONUS ROUND LOGIC ---
        if st.session_state.game_streak > 0 and st.session_state.game_streak % 5 == 0 and not st.session_state.get('bonus_round'):
            st.session_state.bonus_round = True

        if st.session_state.get('bonus_round'):
            st.markdown("## ⚡ BONUS ROUND!")
            st.markdown("You've identified 5 plants in a row! Answer this for **Double Points**.")
            
            bonus_plant = random.choice(available_plants)
            parts = bonus_plant.get('parts', 'Leaves')
            if isinstance(parts, str): parts_list = [p.strip() for p in parts.split(',')]
            else: parts_list = parts
            
            q_text = f"**Bonus:** Which part of **{bonus_plant['name']}** do we usually eat?"
            ans = st.radio(q_text, parts_list, key="bonus_q")
            
            if st.button("Submit Bonus", key="submit_bonus"):
                if ans in parts_list:
                    st.session_state.game_score += 20
                    st.success("🎉 Correct! +20 XP!")
                    current_count = st.session_state.master_inventory.get(bonus_plant['name'], 0)
                    st.session_state.master_inventory[bonus_plant['name']] = current_count + 1
                else:
                    st.error("Incorrect!")
                st.session_state.bonus_round = False
                st.session_state.game_streak = 0
                st.rerun()

        else:
            # STANDARD QUESTION LOGIC
            if st.session_state.get('current_question') is None:
                plant = random.choice(available_plants)
                raw_habitat = plant['habitat'].split(',')[0].strip()
                
                habitat_map = {
                    "Woodlands": "Woodland", "Woods": "Woodland", "Wood": "Woodland",
                    "Hedgerows": "Hedgerow", "Hedgerow": "Hedgerow", "Roadsides": "Hedgerow",
                    "Meadows": "Meadow", "Grassland": "Meadow", "Fields": "Meadow",
                    "Coastal": "Coastal", "Shingle": "Coastal", "Rocky": "Coastal", "Saltmarsh": "Coastal",
                    "Urban": "Urban", "Gardens": "Urban"
                }
                correct_habitat = habitat_map.get(raw_habitat, "Urban")

                all_habitats = ["Woodland", "Coastal", "Hedgerow", "Urban", "Meadow"]
                wrong_habitats = [h for h in all_habitats if h != correct_habitat]
                options = [correct_habitat] + random.sample(wrong_habitats, min(3, len(wrong_habitats)))
                random.shuffle(options)
                
                st.session_state.current_question = {"plant": plant, "correct": correct_habitat, "options": options}

            q = st.session_state.current_question
            
            # Visual Card Layout
            col_vis, col_quiz = st.columns([1, 1.5])
            
            with col_vis:
                # --- CARD FIX: SHOW FULL DESCRIPTION OR ID KEYS ---
                plant_desc = q['plant'].get('description', 'No description available.')
                
                # If ID keys exist, format them nicely
                id_keys = q['plant'].get('id_keys', {})
                if id_keys:
                    keys_html = "<br>".join([f"<b>{k}:</b> {v}" for k, v in list(id_keys.items())[:3]])
                    desc_html = f"<p style='font-size: 0.9em; text-align: left;'>{keys_html}</p>"
                else:
                    desc_html = f"<p><i>{plant_desc}</i></p>"

                st.markdown(f"""
                <div class='plant-card'>
                    <h1 style='font-size: 4em; margin-bottom: 0px;'>🌿</h1>
                    <h3>{q['plant']['name']}</h3>
                    <p style='color: #aaa;'>Latin: <i>{q['plant'].get('latin_name', 'N/A')}</i></p>
                    <hr>
                    {desc_html}
                </div>
                """, unsafe_allow_html=True)

            with col_quiz:
                # --- CLUE FIX: DESCRIBE THE PLANT, NOT THE HABITAT ---
                # We generate a clue from the plant's ID keys or description
                if id_keys:
                    # Pick 2 random features to hint at
                    features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
                    clue_text = "Botanical Clue: " + "; ".join([f"{k} is {v}" for k, v in features])
                else:
                    # Fallback to first 80 chars of description
                    clue_text = f"Clue: {plant_desc[:80]}..."
                
                st.info(f"🕵️ **{clue_text}**")
                
                if EDGE_TTS_AVAILABLE:
                    clean_clue = clean_text_for_audio(clue_text)
                    if st.button("🔊 Listen to Clue", key=f"audio_{q['plant']['name']}"):
                        audio_bytes = generate_voice(clean_clue)
                        if audio_bytes:
                            st.audio(audio_bytes, format='audio/mp3')

                st.markdown("### Where does it grow?")
                
                btn_cols = st.columns(len(q['options']))
                for i, option in enumerate(q['options']):
                    icon = habitat_icons.get(option, "❓")
                    if btn_cols[i].button(f"{icon} {option}", key=f"opt_{i}", use_container_width=True):
                        if option == q['correct']:
                            st.session_state.game_score += 10 + (st.session_state.game_streak * 2)
                            st.session_state.game_streak += 1
                            st.session_state.total_plants_identified += 1
                            
                            # Update Unified Inventory
                            plant_name = q['plant']['name']
                            current_count = st.session_state.master_inventory.get(plant_name, 0)
                            st.session_state.master_inventory[plant_name] = current_count + 1
                            
                            st.success(f"✅ Correct! {q['plant']['name']} grows in the {option}!")
                            
                            # --- ACHIEVEMENT CHECKS (TAB 1) ---
                            if len(st.session_state.master_inventory) >= 1 and not st.session_state.achievements['foraging_novice']:
                                st.session_state.achievements['foraging_novice'] = True
                                st.toast("🏅 Achievement Unlocked: Novice Forager!")
                            if len(st.session_state.master_inventory) >= 25 and not st.session_state.achievements['foraging_botanist']:
                                st.session_state.achievements['foraging_botanist'] = True
                                st.toast("🏅 Achievement Unlocked: Botanist!")
                            if len(st.session_state.season_badge_progress) == 4 and not st.session_state.achievements['foraging_master']:
                                st.session_state.achievements['foraging_master'] = True
                                st.toast("🏅 Achievement Unlocked: Seasonal Master!")

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
        st.markdown("### 🤕 Adventure Over")
        st.markdown("Even the best explorers need a rest. Try again to learn more!")
        if st.button("🔄 Restart Adventure", key="restart_quest"):
            st.session_state.game_lives = 3
            st.session_state.game_score = 0
            st.session_state.current_question = None
            st.session_state.game_streak = 0
            st.rerun()

    # --- ACHIEVEMENT DISPLAY (TAB 1) ---
    st.markdown("---")
    with st.expander("🏅 Foraging Achievements"):
        for key in ["foraging_novice", "foraging_botanist", "foraging_master"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            progress = ""
            if key == "foraging_novice":
                progress = f"({len(st.session_state.master_inventory)}/1)" if not st.session_state.achievements[key] else "(Done)"
            elif key == "foraging_botanist":
                progress = f"({len(st.session_state.master_inventory)}/25)" if not st.session_state.achievements[key] else "(Done)"
            elif key == "foraging_master":
                prog = len(st.session_state.season_badge_progress)
                progress = f"({prog}/4)" if not st.session_state.achievements[key] else "(Done)"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}* {progress}")

# ==========================================
# GAME TAB 2: SURVIVAL SCHOOL (Unchanged)
# ==========================================
with tab2:
    st.header("☠️ Survival School")
    st.caption("📚 Curriculum Link: Science (Plants), PSHE (Safety)")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Read the Case File** carefully. You are looking for a Safe plant.
        2. **Identify the Danger:** Use the rules provided to spot the Poisonous plant.
        3. **Verdict:** Click the button for the **Safe** plant.
        4. **Progress:** Solve 5 cases in a row to unlock **Level 2 (Fungi & Roots)**.
        """)

    if 'survival_level' not in st.session_state:
        st.session_state.survival_level = 1
    
    progress = st.session_state.survival_correct_count / 5
    st.progress(progress, text=f"Level {st.session_state.survival_level} Progress: {st.session_state.survival_correct_count}/5 Cases")
    col1, col2 = st.columns(2)
    col1.metric("❤️ Lives", "❤️" * max(0, st.session_state.survival_lives))
    col2.metric("🌟 Score", st.session_state.survival_score)
    st.markdown("---")

    CASE_FILES = [
        {"level": 1, "clue": "You find a tall plant with white umbrella-shaped flowers. You check the stem. It is smooth (no hairs) and has purple spots on it.", "rule": "🚨 Rule: In the Carrot family, purple spots usually mean POISON.", "safe_plant": "Wild Carrot", "danger_plant": "Hemlock", "safe_icon": "🥕", "danger_icon": "☠️", "fact": "🕵️ Inspector's Report: Hemlock (POISON) has a smooth stem with purple spots. Wild Carrot (Safe) has a hairy stem.", "safe_habitat": "Meadows"},
        {"level": 1, "clue": "You find a plant with broad green leaves in a damp woodland. You crush a leaf and it smells strongly of garlic.", "rule": "✅ Rule: Strong onion/garlic smell is usually a good sign.", "safe_plant": "Wild Garlic", "danger_plant": "Lily of the Valley", "safe_icon": "🌿", "danger_icon": "☠️", "fact": "🕵️ Inspector's Report: Lily of the Valley (POISON) has no garlic smell. Wild Garlic (Safe) smells strongly of garlic.", "safe_habitat": "Woodland"},
        {"level": 2, "clue": "A bright orange mushroom grows under an oak tree. Under the cap, it has ridges (like false gills) that run down the stem. It smells like apricots.", "rule": "✅ Rule: True gills are thin sheets. Ridges are blunt and thick.", "safe_plant": "Chanterelle", "danger_plant": "False Chanterelle", "safe_icon": "🍄", "danger_icon": "🚫", "fact": "🕵️ Inspector's Report: False Chanterelle has true gills. Chanterelle (Safe) has ridges and smells fruity.", "safe_habitat": "Woodland"}
    ]

    available_cases = [c for c in CASE_FILES if c['level'] <= st.session_state.survival_level]

    if st.session_state.survival_current_case is None:
        st.session_state.survival_current_case = random.choice(available_cases)
        st.session_state.survival_result = None

    case = st.session_state.survival_current_case
    level_names = {1: "🌱 Level 1: Plants", 2: "🍄 Level 2: Fungi & Roots"}
    st.info(f"**{level_names.get(st.session_state.survival_level, 'Level 1')}**")

    st.info(f"🔎 **New Case File Found!**")
    st.markdown(f"**Habitat:** {case['safe_habitat']}")
    st.markdown(f"**Your Observation:** {case['clue']}")
    
    if EDGE_TTS_AVAILABLE:
        clean_clue = clean_text_for_audio(case['clue'])
        if st.button("🔊 Listen to Clue", key="audio_clue_btn"):
            audio_bytes = generate_voice(clean_clue)
            if audio_bytes: st.audio(audio_bytes, format='audio/mp3')

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
                if not st.session_state.achievements['survival_scout']:
                    st.session_state.achievements['survival_scout'] = True
                    st.toast("🏅 Achievement Unlocked: Scout!")
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
                if not st.session_state.achievements['survival_scout']:
                    st.session_state.achievements['survival_scout'] = True
                    st.toast("🏅 Achievement Unlocked: Scout!")
            else:
                st.session_state.survival_result = "wrong"
                st.session_state.survival_lives -= 1
                st.session_state.survival_correct_count = 0
            st.rerun()
    else:
        if st.session_state.survival_result == "correct":
            st.success("✅ CASE SOLVED! Great work, Inspector.")
            if st.session_state.survival_correct_count >= 5 and st.session_state.survival_level == 1:
                st.session_state.survival_level = 2
                st.session_state.survival_correct_count = 0
                st.markdown("# 🏆 LEVEL UP!")
                st.write("You have unlocked **Level 2: Fungi & Roots**!")
                if not st.session_state.achievements['survival_expert']:
                    st.session_state.achievements['survival_expert'] = True
                    st.toast("🏅 Achievement Unlocked: Graduate!")
        else:
            st.error("☠️ DANGER! That was the wrong choice.")

        st.markdown("### 📝 Case File Analysis")
        st.markdown(case['fact'])
        
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
            st.session_state.survival_level = 1
            st.rerun()

    # --- ACHIEVEMENT DISPLAY (TAB 2) ---
    st.markdown("---")
    with st.expander("🏅 Survival Achievements"):
        for key in ["survival_scout", "survival_expert"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}*")

# ==========================================
# GAME TAB 3: DAILY QUIZ (Unchanged)
# ==========================================
with tab3:
    st.header("🎯 The Daily Challenge")
    st.caption("📚 Curriculum Link: Science (Plants), Seasonal Changes")
    
    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Categories:** Choose a topic (e.g., Coastal, Trees) to study.
        2. **Difficulty:** Beginner gives 3 options. Expert gives 4.
        3. **Learn:** Correct answers show the Plant Card!
        4. **Streak:** Build a streak for bonus points!
        """)

    col1, col2, col3 = st.columns(3)
    with col1:
        quiz_mode = st.selectbox("📚 Category", ["All", "Edible Only", "Poisonous Only", "Coastal", "Trees", "Fungi"])
    with col2:
        difficulty = st.radio("Difficulty", ["Beginner", "Expert"], horizontal=True)
    with col3:
        challenge_mode = st.checkbox("⚔️ Challenge Mode (1 Life)", value=False)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Streak", f"{st.session_state.daily_streak} Days")
    col2.metric("🌟 Score", st.session_state.quiz_score)
    col3.metric("❓ Question", f"{st.session_state.quiz_q_num}/{st.session_state.quiz_max}")
    st.progress(st.session_state.quiz_q_num / st.session_state.quiz_max)

    if quiz_mode == "All":
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
    elif quiz_mode == "Edible Only":
        pool = UK_PLANTS['edible']
    elif quiz_mode == "Poisonous Only":
        pool = UK_PLANTS['poisonous']
    else:
        pool = [p for p in UK_PLANTS['edible'] if p.get('category') == quiz_mode]
        pool += [p for p in UK_PLANTS['poisonous'] if p.get('category') == quiz_mode]

    if not pool:
        st.warning("No plants found for this category.")
    else:
        if st.session_state.quiz_q_num < st.session_state.quiz_max:
            if st.session_state.get('q_data') is None:
                q_type = random.choice(["id_check", "parts_check", "season_check"])
                plant = random.choice(pool)
                question_text, correct_answer, options, fun_fact = "", "", [], ""

                if q_type == "id_check":
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
                        
                        if st.session_state.daily_streak >= 5 and not st.session_state.achievements['quiz_streak']:
                            st.session_state.achievements['quiz_streak'] = True
                            st.toast("🏅 Achievement Unlocked: Quick Wit!")

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
            if st.button("🔄 Try Again", key="restart_quiz"):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.rerun()

    # --- ACHIEVEMENT DISPLAY (TAB 3) ---
    st.markdown("---")
    with st.expander("🏅 Quiz Achievements"):
        for key in ["quiz_streak"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            progress = f"({st.session_state.daily_streak}/5)" if not st.session_state.achievements[key] else "(Done)"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}* {progress}")

# ==========================================
# GAME TAB 4: ECO-VILLAGE (With Achievements)
# ==========================================
with tab4:
    st.header("🏘️ Eco-Village Builder")
    
    # --- HOW TO PLAY ---
    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Orchard:** A high-cost building (£200) that produces stable food daily.
        2. **Winter:** Solar panels stop. Nature stops. Stockpile food!
        3. **Storage:** Build a Barn to increase your inventory limit.
        4. **Market:** Sell items you found in **Tab 1 (Foraging)** or produced here.
        """)

    # --- GAME STATE INIT ---
    if st.session_state.get('village') is None:
        grid = [['🌲' for _ in range(6)] for _ in range(4)]
        stream_col = random.randint(1, 4)
        for r in range(4): grid[r][stream_col] = '🌊'
        
        st.session_state.village = {
            'grid': grid,
            'stats': {'Food': 50, 'Water': 50, 'Power': 0, 'Stamina': 100, 'Money': 100, 'Max_Power': 20, 'Storage_Limit': 10},
            'inventory': {}, 'owned_buildings': {}, 'placing_mode': None,
            'day': 1, 'season': 'Spring', 'nature_health': 100,
            'damaged_buildings': [] 
        }
    else:
        # Ensure keys exist for older sessions
        if 'Storage_Limit' not in st.session_state.village['stats']: st.session_state.village['stats']['Storage_Limit'] = 10
        if 'season' not in st.session_state.village: st.session_state.village['season'] = 'Spring'
        if 'damaged_buildings' not in st.session_state.village: st.session_state.village['damaged_buildings'] = []

    game = st.session_state.village

    # --- DEFINITIONS (Items specific to Village) ---
    ITEMS_DATA = {
        "Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 2, "food": 2},
        "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1, "food": 3},
        "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 3, "food": 4},
        "Wood": {"icon": "🪵", "rarity": 0.6, "value": 5, "food": 0},
        "Stone": {"icon": "🪨", "rarity": 0.4, "value": 5, "food": 0},
        "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 8, "food": 1},
        "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 10, "food": 12},
        "Fish": {"icon": "🐟", "rarity": 0.0, "value": 12, "food": 25},
        "Apple": {"icon": "🍎", "rarity": 0.0, "value": 5, "food": 3},
        "Pear": {"icon": "🍐", "rarity": 0.0, "value": 5, "food": 3},
        "Orange": {"icon": "🍊", "rarity": 0.0, "value": 5, "food": 3},
        "Dandelion Tea": {"icon": "🍵", "rarity": 0.0, "value": 15, "food": 0, "stamina": 15},
        "Nettle Soup": {"icon": "🥣", "rarity": 0.0, "value": 20, "food": 18},
        "Smoked Fish": {"icon": "🍣", "rarity": 0.0, "value": 35, "food": 45},
        "Cordial": {"icon": "🍶", "rarity": 0.0, "value": 50, "food": 5, "stamina": 30},
        "Jerky": {"icon": "🥩", "rarity": 0.0, "value": 40, "food": 50},
        "Apple Juice": {"icon": "🧃", "rarity": 0.0, "value": 75, "food": 10},
        "Pear Juice": {"icon": "🧃", "rarity": 0.0, "value": 75, "food": 10},
        "Orange Juice": {"icon": "🧃", "rarity": 0.0, "value": 75, "food": 10}
    }
    
    # Add Foraged Items from Master Inventory to Market Data if not present
    # (This allows selling them in the Market)
    for plant in UK_PLANTS['edible']:
        name = plant['name']
        if name not in ITEMS_DATA:
            ITEMS_DATA[name] = {"icon": "🌿", "rarity": 0.0, "value": 5, "food": 2} # Default value for foraged items

    BUILDINGS = {
        "House": {"cost": 50, "icon": "🏠", "desc": "+20 Stamina", "repair": 10},
        "Well": {"cost": 30, "icon": "🪨", "desc": "+5 Water", "repair": 5},
        "Coop": {"cost": 40, "icon": "🐔", "desc": "1 Egg/day", "repair": 8},
        "DIY Solar": {"cost": 50, "icon": "🔋", "desc": "+2 Power", "repair": 10},
        "Solar Array": {"cost": 300, "icon": "☀️", "desc": "+10 Power", "repair": 50},
        "Reserve": {"cost": 150, "icon": "🌳", "desc": "Restores Nature", "repair": 20},
        "Barn": {"cost": 200, "icon": "🏚️", "desc": "+20 Storage", "repair": 20},
        "Orchard": {"cost": 200, "icon": "🌴", "desc": "Fruits Daily", "repair": 15}
    }

    PRODUCTION_RECIPES = {
        "Dandelion Tea": {"ingredients": {"Dandelion": 5}, "power": 2, "output": "Dandelion Tea", "qty": 1},
        "Nettle Soup": {"ingredients": {"Nettle": 5, "Water": 1}, "power": 0, "output": "Nettle Soup", "qty": 1},
        "Smoked Fish": {"ingredients": {"Fish": 1, "Wood": 1}, "power": 5, "output": "Smoked Fish", "qty": 1},
        "Elderflower Cordial": {"ingredients": {"Elderflower": 10}, "power": 5, "output": "Cordial", "qty": 1},
        "Jerky": {"ingredients": {"Eggs": 3, "Wood": 1}, "power": 3, "output": "Jerky", "qty": 1},
        "Apple Juice": {"ingredients": {"Apple": 10}, "power": 5, "output": "Apple Juice", "qty": 1},
        "Pear Juice": {"ingredients": {"Pear": 10}, "power": 5, "output": "Pear Juice", "qty": 1},
        "Orange Juice": {"ingredients": {"Orange": 10}, "power": 5, "output": "Orange Juice", "qty": 1}
    }

    # --- WIN/LOSE STATE ---
    if game['stats']['Money'] >= 5000:
        st.balloons()
        st.success("🏆 **VILLAGE TYCOON!**")
    
    if game['stats']['Food'] <= 0 or game['stats']['Water'] <= 0:
        st.error("💀 **GAME OVER:** Your village starved. Try again!")
        if st.button("Restart Village"):
            st.session_state.village = None
            st.rerun()

    # --- RENDER STATS ---
    s = game['stats']
    
    season_icons = {"Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"}
    current_season = game['season']
    st.markdown(f"### {season_icons.get(current_season, '🌸')} {current_season} - Day {game['day']}")
    
    cols = st.columns(6)
    cols[0].metric("🍖 Food", s['Food'])
    cols[1].metric("💧 Water", s['Water'])
    cols[2].metric("⚡ Power", f"{s['Power']}/{s['Max_Power']}")
    cols[3].metric("💰 Money", f"£{s['Money']}")
    
    nature = game['nature_health']
    cols[4].progress(nature / 100, text=f"🌿 Nature: {nature}%")
    
    current_storage = sum(game['inventory'].values())
    max_storage = s['Storage_Limit']
    cols[5].metric("📦 Storage", f"{current_storage}/{max_storage}")

    if current_season == "Winter":
        st.warning("❄️ **WINTER WARNING:** Solar panels offline. Nature is dormant.")

    st.markdown("---")

    map_tab, forage_tab = st.tabs(["🗺️ Village Map", "🎒 Market & Pantry"])
    
    with map_tab:
        if game['placing_mode']:
            st.info(f"📍 **Placing Mode:** Click a 🌲 tile to build **{game['placing_mode']}**.")
            if st.button("❌ Cancel"):
                cost = BUILDINGS[game['placing_mode']]['cost']
                game['stats']['Money'] += cost
                game['placing_mode'] = None
                st.rerun()

        st.markdown("#### 🗺️ Your Land")
        
        for row_idx, row in enumerate(game['grid']):
            cols = st.columns(6)
            for col_idx, tile in enumerate(row):
                current_tile = game['grid'][row_idx][col_idx]
                
                with cols[col_idx]:
                    st.markdown('<div class="grid-game">', unsafe_allow_html=True)
                    
                    is_damaged = (row_idx, col_idx) in game['damaged_buildings']
                    
                    if game['placing_mode'] and current_tile == '🌲':
                        b_name = game['placing_mode']
                        b_icon = BUILDINGS[b_name]['icon']
                        if st.button(f"📍{b_icon}", key=f"v_place_{row_idx}_{col_idx}"):
                            game['grid'][row_idx][col_idx] = b_icon
                            if b_name not in game['owned_buildings']: game['owned_buildings'][b_name] = 0
                            game['owned_buildings'][b_name] += 1
                            if b_name == "Barn": game['stats']['Storage_Limit'] += 20
                            game['placing_mode'] = None
                            st.rerun()

                    elif current_tile == '🌊':
                        disable_fishing = (current_season == "Winter")
                        if st.button("🎣", key=f"v_fish_{row_idx}_{col_idx}", disabled=disable_fishing):
                            if game['stats']['Stamina'] >= 5:
                                game['stats']['Stamina'] -= 5
                                game['inventory']['Fish'] = game['inventory'].get('Fish', 0) + 1
                                st.success("Caught Fish!")
                                st.rerun()
                            else: st.error("Need Stamina")

                    elif is_damaged:
                        b_data = next((v for k,v in BUILDINGS.items() if v['icon'] == current_tile), None)
                        repair_cost = b_data['repair'] if b_data else 10
                        if st.button(f"🛠️ {repair_cost}", key=f"v_rep_{row_idx}_{col_idx}"):
                            if game['stats']['Money'] >= repair_cost:
                                game['stats']['Money'] -= repair_cost
                                game['damaged_buildings'].remove((row_idx, col_idx))
                                st.success("Repaired!")
                                st.rerun()

                    else:
                        st.button(tile, key=f"v_view_{row_idx}_{col_idx}", disabled=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🛠️ Build")
        
        if not game['placing_mode']:
            build_cols = st.columns(len(BUILDINGS))
            for i, (name, data) in enumerate(BUILDINGS.items()):
                btn_label = f"{data['icon']} {name}"
                if name == "Reserve": btn_label = f"{data['icon']} Reserve (Nature)"
                if name == "Barn": btn_label = f"{data['icon']} Barn (+Storage)"
                
                if build_cols[i].button(f"{btn_label} - £{data['cost']}", key=f"buy_{name}"):
                    if game['stats']['Money'] >= data['cost']:
                        game['stats']['Money'] -= data['cost']
                        game['placing_mode'] = name
                        st.rerun()
                    else: st.error("Poor")

        # --- END DAY LOGIC (TAB 4) ---
        if st.button("⏭️ End Day (Survive)", use_container_width=True, key="end_day_village"):
            game['day'] += 1
            
            # Season Logic
            day_in_cycle = game['day'] % 40
            if day_in_cycle < 10: game['season'] = "Spring"
            elif day_in_cycle < 20: game['season'] = "Summer"
            elif day_in_cycle < 30: game['season'] = "Autumn"
            else: game['season'] = "Winter"
            
            # Resource Drain
            game['stats']['Food'] = max(0, game['stats']['Food'] - 1)
            game['stats']['Water'] = max(0, game['stats']['Water'] - 1)
            game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
            
            # Building Logic
            for r in range(4):
                for c in range(6):
                    tile = game['grid'][r][c]
                    if (r, c) in game['damaged_buildings']: continue
                    
                    if game['season'] == "Winter":
                        if tile in ['🔋', '☀️']: continue
                        if tile == '🌳': continue
                    
                    if tile == '🏠': game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
                    elif tile == '🪨': game['stats']['Water'] += 5
                    elif tile == '🐔': game['inventory']['Eggs'] = game['inventory'].get('Eggs', 0) + 1
                    elif tile == '🔋': game['stats']['Power'] = min(20, game['stats']['Power'] + 2)
                    elif tile == '☀️': game['stats']['Power'] = min(50, game['stats']['Power'] + 10)
                    elif tile == '🌳': game['nature_health'] = min(100, game['nature_health'] + 10)
                    elif tile == '🌴': 
                        game['inventory']['Apple'] = game['inventory'].get('Apple', 0) + 2
                        game['inventory']['Pear'] = game['inventory'].get('Pear', 0) + 2
                        game['inventory']['Orange'] = game['inventory'].get('Orange', 0) + 2
            
            # Damage Logic
            if random.random() < 0.15:
                buildings = [(r, c, game['grid'][r][c]) for r in range(4) for c in range(6) if game['grid'][r][c] not in ['🌲', '🌊']]
                if buildings:
                    r, c, icon = random.choice(buildings)
                    game['damaged_buildings'].append((r, c))
                    st.toast(f"⚠️ Building {icon} damaged!")

            # --- ACHIEVEMENT CHECKS (TAB 4) ---
            # Survivor (30 Days)
            if game['day'] >= 30 and not st.session_state.achievements['eco_survivor']:
                st.session_state.achievements['eco_survivor'] = True
                st.toast("🏅 Achievement Unlocked: Settler!")
            # Eco-Tycoon (£2000)
            if game['stats']['Money'] >= 2000 and not st.session_state.achievements['eco_wealth']:
                st.session_state.achievements['eco_wealth'] = True
                st.toast("🏅 Achievement Unlocked: Eco-Tycoon!")

            st.rerun()

    with forage_tab:
        st.markdown("### 🌲 Gather & Market")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🌿 Actions")
            disable_forage = (game['season'] == "Winter")
            
            if game['nature_health'] < 20:
                st.error("⚠️ Nature depleted!")
            
            if st.button("Forage in Woods", key="forage_woods", disabled=disable_forage):
                if game['stats']['Stamina'] >= 10:
                    if game['nature_health'] >= 5:
                        game['stats']['Stamina'] -= 10
                        game['nature_health'] = max(0, game['nature_health'] - 5)
                        # Generates Wood/Stone mainly, but also connects to master inventory if needed
                        found = [name for name, data in ITEMS_DATA.items() if random.random() < data.get('rarity', 0) and name in ["Wood", "Stone"]]
                        for f in found:
                             if sum(game['inventory'].values()) < max_storage:
                                game['inventory'][f] = game['inventory'].get(f, 0) + 1
                        st.success(f"Found: {', '.join(found)}")
                        st.rerun()
                    else: st.error("Nature exhausted!")
                else: st.error("Need Stamina")
            
            st.markdown("##### 🏭 Production")
            
            for recipe_name, recipe in PRODUCTION_RECIPES.items():
                has_power = game['stats']['Power'] >= recipe['power']
                has_ingredients = all(game['inventory'].get(ing, 0) >= qty for ing, qty in recipe['ingredients'].items())
                has_space = (sum(game['inventory'].values()) + recipe['qty']) <= max_storage
                
                ing_str = ", ".join([f"{i}x{q}" for i,q in recipe['ingredients'].items()])
                pwr_str = f"⚡{recipe['power']}" if recipe['power'] > 0 else ""
                
                if st.button(f"Make {recipe_name} ({ing_str} {pwr_str})", disabled=not (has_power and has_ingredients and has_space), key=f"make_{recipe_name}"):
                    for ing, qty in recipe['ingredients'].items():
                        game['inventory'][ing] -= qty
                    game['stats']['Power'] -= recipe['power']
                    out = recipe['output']
                    game['inventory'][out] = game['inventory'].get(out, 0) + recipe['qty']
                    st.success(f"Made {recipe_name}!")
                    st.rerun()

        with col2:
            st.markdown("#### 💰 Market & Pantry")
            st.caption(f"Storage: {current_storage}/{max_storage}")
            
            # Combine Village Inventory with Master Inventory (Foraged items)
            # We create a merged view for selling
            combined_inventory = {}
            # Add village specific items
            for item_name, count in game['inventory'].items():
                combined_inventory[item_name] = combined_inventory.get(item_name, 0) + count
            
            # Add foraged items from Master Inventory (Tab 1)
            for item_name, count in st.session_state.master_inventory.items():
                combined_inventory[item_name] = combined_inventory.get(item_name, 0) + count

            if not combined_inventory: 
                st.info("Empty - Forage in Tab 1 or produce in Tab 4")
            else:
                cols = st.columns([2, 1, 1, 1])
                cols[0].write("**Item**")
                cols[1].write("**Qty**")
                cols[2].write("**Eat**")
                cols[3].write("**Sell**")
                
                for item_name, count in list(combined_inventory.items()):
                    if count <= 0: continue
                    
                    data = ITEMS_DATA.get(item_name, {'value': 5, 'food': 0, 'icon': '❓'})
                    val = data['value']
                    food_val = data.get('food', 0)
                    
                    cols = st.columns([2, 1, 1, 1])
                    cols[0].write(f"{data['icon']} {item_name}")
                    cols[1].write(f"{count}")
                    
                    if food_val > 0:
                        if cols[2].button("🍽️", key=f"eat_{item_name}", help=f"Restores {food_val} Food"):
                            game['stats']['Food'] += food_val
                            # Deduct from the correct inventory
                            if item_name in game['inventory'] and game['inventory'][item_name] > 0:
                                game['inventory'][item_name] -= 1
                            elif item_name in st.session_state.master_inventory and st.session_state.master_inventory[item_name] > 0:
                                st.session_state.master_inventory[item_name] -= 1
                            st.toast(f"+{food_val} Food")
                            st.rerun()
                    else:
                        cols[2].write("—")
                    
                    # Selling Logic
                    if cols[3].button(f"£{val}", key=f"sell_btn_{item_name}"):
                        # Deduct from correct inventory
                        if item_name in game['inventory'] and game['inventory'][item_name] > 0:
                            game['inventory'][item_name] -= 1
                        elif item_name in st.session_state.master_inventory and st.session_state.master_inventory[item_name] > 0:
                            st.session_state.master_inventory[item_name] -= 1
                        
                        game['stats']['Money'] += val
                        st.toast(f"Sold {item_name} for £{val}")
                        
                        # Achievement Check (Money)
                        if game['stats']['Money'] >= 2000 and not st.session_state.achievements['eco_wealth']:
                            st.session_state.achievements['eco_wealth'] = True
                            st.toast("🏅 Achievement Unlocked: Eco-Tycoon!")
                        st.rerun()

    # --- ACHIEVEMENT DISPLAY (TAB 4) ---
    st.markdown("---")
    with st.expander("🏅 Eco-Village Achievements"):
        for key in ["eco_survivor", "eco_wealth"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}*")

# ==========================================
# GAME TAB 5: FARM TYCOON (With Achievements)
# ==========================================
with tab5:
    st.header("🚜 Farm Tycoon")
    
    # --- CSS ---
    st.markdown("""
    <style>
    .market-box div.stButton > button { font-size: 14px !important; white-space: normal !important; height: auto !important; padding: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

    # --- HOW TO PLAY ---
    with st.expander("📖 Guide & Progression"):
        st.markdown("""
        **📅 Timeline:**
        - Seasons last **30 Days**.
        - **Year 1:** Focus on crops and bees. Animals are locked.
        - **Year 2+:** Animals (Chickens, Cows) are unlocked.
        
        **🌱 Farming:**
        - Crops take 3 days to grow.
        - **Soil:** Depletes on harvest. Empty plots **regenerate +5 health** per day.
        
        **📦 Feed & Animals:**
        - Animals eat **Feed Bags** (best) or Wheat (fallback).
        - **Recipe:** 1 Wheat + 1 Carrot + 1 Corn = 5 Feed Bags.
        
        **📉 Market:**
        - Random **Shortages** double the price of a crop!
        - Selling large amounts (>10) crashes the price.
        """)

    # --- INIT ---
    if st.session_state.get('farm_game') is None:
        grid = [[0 for _ in range(6)] for _ in range(5)]
        stream_col = random.randint(1, 4)
        for r in range(5): grid[r][stream_col] = 1
        
        st.session_state.farm_game = {
            'grid': grid, 'money': 200, 'day': 1, 
            'inventory': {'Feed': 0}, 
            'market_prices': {"Carrot": 12, "Wheat": 18, "Corn": 25, "Egg": 30, "Milk": 50, "Honey": 60, "Feed": 5},
            'soil_health': [[100 for _ in range(6)] for _ in range(5)],
            'manor_bought': False,
            'fallow_days': [[0 for _ in range(6)] for _ in range(5)],
            'sales_log': {},
            'crop_map': {},
            'last_event': "",
            'market_event': None,
            'total_harvests': 0 
        }

    game = st.session_state.farm_game
    
    # Migration for existing saves
    for k in ["Carrot", "Wheat", "Corn", "Egg", "Milk", "Honey", "Feed"]:
        if k not in game['market_prices']: game['market_prices'][k] = 10
    if 'Feed' not in game['inventory']: game['inventory']['Feed'] = 0
    if 'market_event' not in game: game['market_event'] = None
    if 'last_event' not in game: game['last_event'] = ""
    if 'total_harvests' not in game: game['total_harvests'] = 0

    # --- DEFINITIONS ---
    ICONS = {
        0: "🟤", 1: "🌊", 2: "🌱", 3: "🌿", 4: "🌾", 7: "🥀", 
        8: "🏠", 9: "🐝", 10: "🎃", 11: "💦", 
        12: "🐔", 13: "🐄", 14: "🐐"
    }
    SEED_COST = {"Carrot": 6, "Wheat": 9, "Corn": 12}
    
    BUILDINGS_FARM = {
        "Manor": {"cost": 5000, "icon": "🏛️", "id": 8},
        "Barn": {"cost": 300, "icon": "🏠", "id": 8},
        "Beehive": {"cost": 200, "icon": "🐝", "id": 9},
        "Scarecrow": {"cost": 100, "icon": "🎃", "id": 10},
        "Sprinkler": {"cost": 250, "icon": "💦", "id": 11},
        "Chicken": {"cost": 50, "icon": "🐔", "id": 12},
        "Cow": {"cost": 100, "icon": "🐄", "id": 13},
        "Goat": {"cost": 80, "icon": "🐐", "id": 14}
    }

    def get_year(day): return (day // 120) + 1
    def get_season(day):
        day_in_year = day % 120
        if day_in_year < 30: return "Spring"
        elif day_in_year < 60: return "Summer"
        elif day_in_year < 90: return "Autumn"
        else: return "Winter"

    # --- WIN STATE ---
    if game['manor_bought']:
        st.success("🏆 **FARMING DYNASTY COMPLETE!**")

    # --- EVENT WARNING ---
    if game['last_event']:
        st.warning(f"**Report:** {game['last_event']}")

    if game['market_event']:
        st.info(f"📈 **Market Surge:** {game['market_event']} prices have doubled!")

    # --- STATS ---
    current_year = get_year(game['day'])
    current_season = get_season(game['day'])

    chickens = sum(row.count(12) for row in game['grid'])
    cows = sum(row.count(13) for row in game['grid'])
    goats = sum(row.count(14) for row in game['grid'])
    total_animals = chickens + cows + goats

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Year", f"{current_year} - {current_season}")
    c2.metric("💰 Money", f"£{game['money']}")
    c3.metric("🐔 Chickens", chickens if current_year >= 2 else "🔒 Y2")
    c4.metric("🐄 Cows / 🐐 Goats", f"{cows}/{goats}" if current_year >= 2 else "🔒 Y2")

    # Inventory
    st.markdown("---")
    inv_str = " | ".join([f"**{k}:** {v}" for k,v in game['inventory'].items() if v > 0])
    st.markdown(f"**🎒 Stock:** {inv_str if inv_str else 'Empty'}")
    
    # Toolbox
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        game['tool'] = st.selectbox("🌱 Plant", ["Carrot", "Wheat", "Corn"], key="farm_tool_crops")
    with t2:
        available_buildings = {k: v for k, v in BUILDINGS_FARM.items() if k in ["Manor", "Barn", "Beehive", "Scarecrow", "Sprinkler"] or current_year >= 2}
        build_opts = [f"{name} (£{data['cost']})" for name, data in available_buildings.items()]
        game['build_sel_raw'] = st.selectbox("🏗️ Build", ["None"] + build_opts, key="farm_tool_build")
        if game['build_sel_raw'] != "None":
            game['build_sel'] = game['build_sel_raw'].split(" (")[0]
        else:
            game['build_sel'] = "None"
    with t3:
        if st.button("🧹 Clear Weeds", key="farm_clear_btn"):
            removed = sum(1 for r in range(5) for c in range(6) if game['grid'][r][c] == 7)
            if removed > 0:
                for r in range(5):
                    for c in range(6):
                        if game['grid'][r][c] == 7: game['grid'][r][c] = 0
                st.success(f"Cleared {removed}!"); st.rerun()
    with t4:
        feed_needed = chickens + (cows * 2) + goats
        st.caption(f"Feed Needed: {feed_needed}")

    # --- FEED PRODUCTION ---
    st.markdown("#### 🏭 Feed Production")
    f1, f2 = st.columns(2)
    with f1:
        st.write("**Recipe:** 1 Wheat + 1 Carrot + 1 Corn = 5 Feed")
    with f2:
        has_ing = (game['inventory'].get('Wheat', 0) >= 1 and 
                   game['inventory'].get('Carrot', 0) >= 1 and 
                   game['inventory'].get('Corn', 0) >= 1)
        if st.button("Make Feed Bag", disabled=not has_ing):
            game['inventory']['Wheat'] -= 1
            game['inventory']['Carrot'] -= 1
            game['inventory']['Corn'] -= 1
            game['inventory']['Feed'] = game['inventory'].get('Feed', 0) + 5
            st.success("+5 Feed Bags"); st.rerun()

    # --- END DAY LOGIC (TAB 5) ---
    if st.button("⏭️ End Day", use_container_width=True, key="end_day_farm"):
        game['last_event'] = ""
        
        # Market Logic
        base_prices = {"Carrot": 12, "Wheat": 18, "Corn": 25, "Egg": 30, "Milk": 50, "Honey": 60}
        for item, qty in game['sales_log'].items():
            if qty > 10: game['market_prices'][item] = max(1, int(base_prices[item] * 0.8))
            else: game['market_prices'][item] = min(base_prices[item] + 5, int(base_prices[item] * 1.05))
        game['sales_log'] = {}
        game['market_event'] = None
        
        # Random Market Surge
        if random.random() < 0.2:
            surge_crop = random.choice(["Carrot", "Wheat", "Corn"])
            game['market_event'] = surge_crop
            game['last_event'] += f"📈 {surge_crop} SURGE! "

        # Weather
        is_drought = (current_season == "Summer" and random.random() < 0.3 and not any(11 in row for row in game['grid']))
        is_pest_event = (current_season != "Winter" and random.random() < 0.2 and not any(10 in row for row in game['grid']))
        
        if is_drought: game['last_event'] += "☀️ DROUGHT! "
        if is_pest_event: game['last_event'] += "🐛 PESTS! "

        # Grid Process
        for r in range(5):
            for c in range(6):
                tile = game['grid'][r][c]
                
                # Weeds & Fallow (Soil Regen)
                if tile == 0:
                    game['fallow_days'][r][c] += 1
                    game['soil_health'][r][c] = min(100, game['soil_health'][r][c] + 5)
                    if game['fallow_days'][r][c] > 3 and random.random() < 0.2:
                        game['grid'][r][c] = 7; game['fallow_days'][r][c] = 0
                
                # Crops
                elif tile in [2, 3]:
                    game['fallow_days'][r][c] = 0
                    if current_season == "Winter":
                        game['grid'][r][c] = 0
                        game['crop_map'].pop((r,c), None)
                        game['last_event'] += "❄️ Winter Kill. "
                    elif not is_drought:
                        game['grid'][r][c] = tile + 1
                    
                    if is_pest_event and random.random() < 0.4:
                        game['grid'][r][c] = 0
                        game['crop_map'].pop((r,c), None)

                # Production
                elif tile == 9: # Beehive
                    game['inventory']['Honey'] = game['inventory'].get('Honey', 0) + 1
                
                # Animals
                elif tile == 12: # Chicken
                    if game['inventory'].get('Feed', 0) >= 1:
                        game['inventory']['Feed'] -= 1
                        game['inventory']['Egg'] = game['inventory'].get('Egg', 0) + 1
                    elif game['inventory'].get('Wheat', 0) >= 1:
                        game['inventory']['Wheat'] -= 1
                        game['inventory']['Egg'] = game['inventory'].get('Egg', 0) + 1
                    else: game['last_event'] += "🐔 Hungry! "

                elif tile == 13: # Cow
                    if game['inventory'].get('Feed', 0) >= 2:
                        game['inventory']['Feed'] -= 2
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    elif game['inventory'].get('Wheat', 0) >= 2:
                        game['inventory']['Wheat'] -= 2
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    else: game['last_event'] += "🐄 Hungry! "

                elif tile == 14: # Goat
                    if game['inventory'].get('Feed', 0) >= 1:
                        game['inventory']['Feed'] -= 1
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    elif game['inventory'].get('Wheat', 0) >= 1:
                        game['inventory']['Wheat'] -= 1
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    else: game['last_event'] += "🐐 Hungry! "

        # --- ACHIEVEMENT CHECKS (TAB 5) ---
        if total_animals >= 5 and not st.session_state.achievements['farm_rancher']:
            st.session_state.achievements['farm_rancher'] = True
            st.toast("🏅 Achievement Unlocked: Rancher!")

        game['day'] += 1
        st.rerun()

    # --- GRID ---
    st.markdown("#### 🗺️ Farm")
    
    for r in range(5):
        cols = st.columns(6)
        for c in range(6):
            tile_val = game['grid'][r][c]
            icon = ICONS.get(tile_val, "❓")
            
            with cols[c]:
                if tile_val == 7: # Weeds
                    if st.button("🧹", key=f"fm_w_{r}_{c}"):
                        game['grid'][r][c] = 0; st.rerun()
                elif tile_val == 0: # Empty
                    if game['build_sel'] != "None":
                        b_name = game['build_sel']
                        b_data = BUILDINGS_FARM[b_name]
                        if b_name in ["Chicken", "Cow", "Goat"] and current_year < 2:
                            st.warning("Unlock Y2")
                        else:
                            if st.button("🏗️", key=f"fm_b_{r}_{c}"):
                                if game['money'] >= b_data['cost']:
                                    game['money'] -= b_data['cost']
                                    game['grid'][r][c] = b_data['id']
                                    game['build_sel'] = "None"
                                    st.rerun()
                    else:
                        if st.button("🌱", key=f"fm_p_{r}_{c}"):
                            crop = game['tool']
                            cost = SEED_COST[crop]
                            if game['money'] >= cost:
                                game['money'] -= cost
                                game['grid'][r][c] = 2
                                game['crop_map'][(r,c)] = crop
                                st.rerun()
                elif tile_val == 4: # Ready
                    if st.button("🌾", key=f"fm_h_{r}_{c}"):
                        crop = game['crop_map'].get((r,c), "Carrot")
                        yield_count = 1
                        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                            if 0 <= r+dr < 5 and 0 <= c+dc < 6:
                                if game['grid'][r+dr][c+dc] == 9: yield_count += 1
                        
                        harvested = int(yield_count * (game['soil_health'][r][c] / 100))
                        if harvested == 0: harvested = 1
                        
                        game['inventory'][crop] = game['inventory'].get(crop, 0) + harvested
                        game['grid'][r][c] = 0
                        game['soil_health'][r][c] = max(0, game['soil_health'][r][c] - 10)
                        game['crop_map'].pop((r,c), None)
                        game['total_harvests'] += 1
                        
                        if game['total_harvests'] >= 1 and not st.session_state.achievements['farm_harvest']:
                            st.session_state.achievements['farm_harvest'] = True
                            st.toast("🏅 Achievement Unlocked: Green Thumb!")

                        st.toast(f"+{harvested} {crop}")
                        st.rerun()
                else:
                    st.button(icon, key=f"fm_v_{r}_{c}", disabled=True)
                
                soil = game['soil_health'][r][c]
                st.progress(soil/100)

    st.markdown("---")
    
    # --- MARKET ---
    st.markdown("#### 💰 Market")
    
    st.markdown('<div class="market-box">', unsafe_allow_html=True)
    cols = st.columns(len(game['market_prices']))
    for i, (item, price) in enumerate(game['market_prices'].items()):
        count = game['inventory'].get(item, 0)
        
        current_price = price
        if game['market_event'] == item:
            current_price = price * 2 
        
        crash_msg = ""
        if game['sales_log'].get(item, 0) > 10: 
            crash_msg = "📉"
            current_price = int(current_price * 0.8)
            
        with cols[i]:
            st.markdown(f"**{item}** {crash_msg}")
            st.caption(f"Have: {count}")
            if st.button(f"Sell\n£{current_price}", key=f"sell_{item}_f", disabled=count<=0):
                game['money'] += current_price
                game['inventory'][item] -= 1
                game['sales_log'][item] = game['sales_log'].get(item, 0) + 1
                
                if game['money'] >= 5000:
                     game['manor_bought'] = True # Win condition check

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # --- ACHIEVEMENT DISPLAY (TAB 5) ---
    st.markdown("---")
    with st.expander("🏅 Farm Achievements"):
        for key in ["farm_harvest", "farm_rancher", "farm_winner"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}*")

# ==========================================
# GAME TAB 6: THE WILD KITCHEN (With Achievements)
# ==========================================
with tab6:
    st.header("🍳 The Wild Kitchen")
    st.caption("📚 Process your harvest. Master the prep. Unlock new difficulties!")
    
    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Inventory:** Your pantry is filled by **Tab 1 (Foraging)**.
        2. **Progression:** Unlock **3 Beginner** recipes to access Intermediate.
        3. **Unlocking:** Click a recipe, answer the safety questions, and click "Submit".
        4. **Cooking:** Once unlocked, cook the recipe using ingredients from your Pantry.
        """)

    # --- PANTRY SETUP (UNIFIED INVENTORY) ---
    # The kitchen now reads directly from the Master Inventory (Tab 1)
    inv = st.session_state.master_inventory
    # Add some default basics if empty for new players?
    if not inv:
        st.info("Your Pantry is empty. Go Foraging in Tab 1 to find ingredients!")

    # --- FULL RECIPE DATABASE ---
    RECIPES = [
        # --- BEGINNER ---
        {"name": "Nettle Soup", "ingredients": {"Nettles": 5, "Water": 1}, "prep_questions": [{"q": "Why must nettles be cooked?", "opts": ["To remove the sting", "To make them sweet", "To change color"], "a": "To remove the sting"}], "icon": "🥣", "desc": "A rich, green soup.", "diff": 1, "benefits": "High in Iron."},
        {"name": "Wild Garlic Pesto", "ingredients": {"Wild Garlic": 10, "Oil": 1}, "prep_questions": [{"q": "Which part of Wild Garlic is edible?", "opts": ["Only the flowers", "Leaves, flowers, and bulbs", "Only the roots"], "a": "Leaves, flowers, and bulbs"}], "icon": "🥗", "desc": "A fragrant pesto.", "diff": 1, "benefits": "Antibacterial."},
        {"name": "Dandelion Salad", "ingredients": {"Dandelion": 5}, "prep_questions": [{"q": "When is best to harvest Dandelion leaves?", "opts": ["When the flower is yellow", "Before the flower opens (young)", "In winter"], "a": "Before the flower opens (young)"}], "icon": "🥗", "desc": "Young leaves are less bitter.", "diff": 1, "benefits": "Liver health."},
        {"name": "Three-Cornered Leek Omelette", "ingredients": {"Three-Cornered Leek": 5, "Eggs": 2}, "prep_questions": [{"q": "How to ID Three-Cornered Leek?", "opts": ["Smells of garlic, triangular stem", "Blue flowers, round stem", "Yellow flowers, spiky"], "a": "Smells of garlic, triangular stem"}], "icon": "🍳", "desc": "A forager's breakfast.", "diff": 1, "benefits": "High protein."},
        {"name": "Pine Needle Tea", "ingredients": {"Pine Needles": 10, "Water": 1}, "prep_questions": [{"q": "How do you identify SAFE Pine needles?", "opts": ["Flat needles (Yew)", "Round needles in bundles", "Blue needles"], "a": "Round needles in bundles"}], "icon": "🍵", "desc": "High in Vitamin C.", "diff": 1, "benefits": "Vitamin C boost."},
        {"name": "Beech Leaf Liqueur", "ingredients": {"Beech Leaves": 20, "Sugar": 1, "Alcohol": 1}, "prep_questions": [{"q": "When should you pick Beech leaves?", "opts": ["Autumn (Brown)", "Spring (Young/Transparent)", "Winter"], "a": "Spring (Young/Transparent)"}], "icon": "🥃", "desc": "A sweet, gin-based liquor.", "diff": 1, "benefits": "Traditional tonic."},
        {"name": "Chickweed Salad", "ingredients": {"Chickweed": 10}, "prep_questions": [{"q": "How do you identify Chickweed?", "opts": ["Line of hairs on stem", "Purple spots on stem", "Blue flowers"], "a": "Line of hairs on stem"}], "icon": "🥗", "desc": "A mild, nutritious weed.", "diff": 1, "benefits": "Vitamins."},
        {"name": "Wild Strawberry Jam", "ingredients": {"Wild Strawberry": 20, "Sugar": 1}, "prep_questions": [{"q": "How do wild strawberries differ from barren strawberry?", "opts": ["Barren has petals with gaps", "Wild has blue flowers", "Barren has hairy leaves"], "a": "Barren has petals with gaps"}], "icon": "🍯", "desc": "Tiny but intense flavor.", "diff": 1, "benefits": "Antioxidants."},
        {"name": "Roasted Hazelnuts", "ingredients": {"Hazelnut": 10}, "prep_questions": [{"q": "What indicates a ripe Hazelnut?", "opts": ["Green husk", "Brown shell and leafy husk", "No leaves"], "a": "Brown shell and leafy husk"}], "icon": "🌰", "desc": "Autumn treat.", "diff": 1, "benefits": "Heart health."},
        {"name": "Sea Purslane Salad", "ingredients": {"Sea Purslane": 10}, "prep_questions": [{"q": "What is the main precaution with Sea Purslane?", "opts": ["It is very salty", "It is poisonous raw", "It has thorns"], "a": "It is very salty"}], "icon": "🥗", "desc": "Salty coastal green.", "diff": 1, "benefits": "Minerals."},
        
        # --- INTERMEDIATE ---
        {"name": "Dandelion Coffee", "ingredients": {"Dandelion": 20}, "prep_questions": [{"q": "Which part is used for coffee?", "opts": ["Leaves", "Flowers", "Roots"], "a": "Roots"}, {"q": "How must the roots be prepared?", "opts": ["Eaten raw", "Roasted and ground", "Boiled whole"], "a": "Roasted and ground"}], "icon": "☕", "desc": "Caffeine-free coffee substitute.", "diff": 2, "benefits": "Liver detox."},
        {"name": "Elderflower Cordial", "ingredients": {"Elderflower": 10, "Sugar": 1}, "prep_questions": [{"q": "Why should you not wash Elderflowers?", "opts": ["Loses pollen (flavor)", "Becomes poisonous", "Petals fall off"], "a": "Loses pollen (flavor)"}, {"q": "What must you check for before cooking?", "opts": ["Spiders", "Bugs/Maggots", "Birds"], "a": "Bugs/Maggots"}], "icon": "🥤", "desc": "A sweet summery drink.", "diff": 2, "benefits": "Vitamin C."},
        {"name": "Blackberry Jam", "ingredients": {"Blackberries": 20, "Sugar": 1}, "prep_questions": [{"q": "What must you check for when picking?", "opts": ["Check for bugs", "Check if they are red", "Check for thorns"], "a": "Check for bugs"}, {"q": "What helps the jam set (thicken)?", "opts": ["Water", "Pectin (naturally in fruit)", "Oil"], "a": "Pectin (naturally in fruit)"}], "icon": "🍯", "desc": "Preserved summer in a jar.", "diff": 2, "benefits": "Fiber."},
        {"name": "Rosehip Syrup", "ingredients": {"Rosehips": 15, "Sugar": 1}, "prep_questions": [{"q": "Why remove the seeds?", "opts": ["Bitter", "Itchy irritation", "Poisonous"], "a": "Itchy irritation"}, {"q": "What vitamin are Rosehips famous for?", "opts": ["Vitamin A", "Vitamin C", "Vitamin D"], "a": "Vitamin C"}], "icon": "🧴", "desc": "Rich in Vitamin C.", "diff": 2, "benefits": "Immune boost."},
        {"name": "Sorrel Soup", "ingredients": {"Sorrel": 15, "Water": 1}, "prep_questions": [{"q": "What gives Sorrel its sour taste?", "opts": ["Sugar", "Oxalic Acid", "Citrus"], "a": "Oxalic Acid"}, {"q": "Who should avoid large amounts?", "opts": ["Children", "People with kidney issues", "Elderly"], "a": "People with kidney issues"}], "icon": "🥣", "desc": "Tangy and refreshing.", "diff": 2, "benefits": "Vitamin C."},
        {"name": "Hawthorn Ketchup", "ingredients": {"Hawthorn": 30, "Sugar": 1}, "prep_questions": [{"q": "What do Hawthorn berries look like?", "opts": ["Blue pods", "Small red berries", "Blackberries"], "a": "Small red berries"}, {"q": "What should you avoid when eating?", "opts": ["The skin", "The seeds (pips)", "The stem"], "a": "The seeds (pips)"}], "icon": "🍅", "desc": "Tomato ketchup alternative.", "diff": 2, "benefits": "Heart health."},
        {"name": "Sweet Chestnut Roast", "ingredients": {"Sweet Chestnut": 20}, "prep_questions": [{"q": "How does the case differ from Horse Chestnut?", "opts": ["Smooth/Warty", "Very spiky", "Green"], "a": "Very spiky"}, {"q": "What must you do before roasting?", "opts": ["Peel them", "Score the shell", "Boil for 1 hour"], "a": "Score the shell"}], "icon": "🌰", "desc": "Roasting over an open fire.", "diff": 2, "benefits": "Starch source."},
        {"name": "Marsh Samphire Sauté", "ingredients": {"Marsh Samphire": 15, "Butter": 1}, "prep_questions": [{"q": "Where does Samphire grow?", "opts": ["Dry Meadows", "Saltmarshes/Mud", "Trees"], "a": "Saltmarshes/Mud"}, {"q": "How do you harvest sustainably?", "opts": ["Pull up roots", "Cut top 2 inches", "Dig with trowel"], "a": "Cut top 2 inches"}], "icon": "🥦", "desc": "Sea asparagus.", "diff": 2, "benefits": "Iodine."},
        
        # --- ADVANCED ---
        {"name": "Acorn Coffee", "ingredients": {"Oak (Acorns)": 20}, "prep_questions": [{"q": "Why not eat raw?", "opts": ["Too hard", "Contain tannins (bitter)", "Protected"], "a": "Contain tannins (bitter)"}, {"q": "How to remove tannins?", "opts": ["Leaching (soaking)", "Freezing", "Burning"], "a": "Leaching (soaking)"}, {"q": "When to harvest?", "opts": ["Green", "Brown (ripe)", "White"], "a": "Brown (ripe)"}], "icon": "☕", "desc": "Must be leached first.", "diff": 3, "benefits": "Gluten-free."},
        {"name": "Chanterelle Risotto", "ingredients": {"Chanterelle": 10, "Rice": 1}, "prep_questions": [{"q": "How to ID Chanterelle?", "opts": ["True gills (sheets)", "False gills (ridges)", "Sponge"], "a": "False gills (ridges)"}, {"q": "What does it smell like?", "opts": ["Aniseed/Apricot", "Mud", "Nothing"], "a": "Aniseed/Apricot"}, {"q": "Danger lookalike?", "opts": ["False Chanterelle", "Death Cap", "Field Mushroom"], "a": "False Chanterelle"}], "icon": "🍚", "desc": "A gourmet wild meal.", "diff": 3, "benefits": "Vitamin D."},
        {"name": "Crab Apple Jelly", "ingredients": {"Crab Apple": 25, "Sugar": 1}, "prep_questions": [{"q": "Why not eat raw?", "opts": ["Poisonous", "Too tart/sour", "Too hard"], "a": "Too tart/sour"}, {"q": "Why is it good for jelly?", "opts": ["High Pectin", "Red Color", "Soft skin"], "a": "High Pectin"}, {"q": "What to remove?", "opts": ["Skin", "Seeds and stems", "Nothing"], "a": "Seeds and stems"}], "icon": "🍯", "desc": "High pectin.", "diff": 3, "benefits": "Pectin source."},
        {"name": "Wood Ear Stir-fry", "ingredients": {"Wood Ear (Jelly Ear)": 10, "Oil": 1}, "prep_questions": [{"q": "Where does it grow?", "opts": ["Ground", "Elder trees", "Pine trees"], "a": "Elder trees"}, {"q": "Texture?", "opts": ["Soft", "Jelly/Rubbery", "Crunchy"], "a": "Jelly/Rubbery"}, {"q": "Must be cooked?", "opts": ["Yes", "No", "Only if old"], "a": "Yes"}], "icon": "🥡", "desc": "Jelly fungus.", "diff": 3, "benefits": "Blood circulation."},
        {"name": "Morel Risotto", "ingredients": {"Morel": 10, "Rice": 1}, "prep_questions": [{"q": "Cap texture?", "opts": ["Smooth", "Honeycomb pits", "Wrinkled brain"], "a": "Honeycomb pits"}, {"q": "Inside?", "opts": ["Solid", "Chambered", "Hollow"], "a": "Hollow"}, {"q": "Danger lookalike?", "opts": ["True Morel", "False Morel", "Chanterelle"], "a": "False Morel"}], "icon": "🍚", "desc": "Spring delicacy.", "diff": 3, "benefits": "Vitamin D."},
        {"name": "Burdock Root Stew", "ingredients": {"Burdock (Root)": 10, "Water": 1}, "prep_questions": [{"q": "Which root to dig?", "opts": ["Flowering plant", "First year plant", "Any"], "a": "First year plant"}, {"q": "Legal issue?", "opts": ["None", "Uprooting illegal without permission", "Poisonous"], "a": "Uprooting illegal without permission"}, {"q": "Taste?", "opts": ["Sweet", "Earthy/Artichoke", "Bitter"], "a": "Earthy/Artichoke"}], "icon": "🍲", "desc": "Requires digging.", "diff": 3, "benefits": "Blood purifier."},
        {"name": "Cockles in Vinegar", "ingredients": {"Cockles": 20, "Vinegar": 1}, "prep_questions": [{"q": "Shell shape?", "opts": ["Smooth", "Ribbed/Ridged", "Spiral"], "a": "Ribbed/Ridged"}, {"q": "Safety check?", "opts": ["Red tide/Pollution", "Size", "Color"], "a": "Red tide/Pollution"}, {"q": "Cooking?", "opts": ["Eat raw", "Steam until open", "Fry"], "a": "Steam until open"}], "icon": "🥣", "desc": "Coastal shellfish.", "diff": 3, "benefits": "Protein."}
    ]

    def get_difficulty_stars(diff): return "⭐" * diff + "☆" * (3 - diff)

    # --- PROGRESSION LOGIC ---
    beginner_unlocked = len([r for r in st.session_state.unlocked_recipes if any(x['name'] == r and x['diff']==1 for x in RECIPES)])
    inter_unlocked = len([r for r in st.session_state.unlocked_recipes if any(x['name'] == r and x['diff']==2 for x in RECIPES)])

    # --- LAYOUT ---
    col_main, col_side = st.columns([2, 1])
    
    with col_side:
        st.markdown("### 🎒 Pantry")
        if not inv: st.info("Empty - Forage items in Tab 1")
        else:
            st.markdown("**Your Ingredients:**")
            for item, qty in sorted(inv.items()):
                if qty > 0:
                    st.write(f"- **{item}:** {qty}")
            
            st.markdown("---")
            st.markdown("**🔧 Basics**")
            st.caption("Water, Sugar, Oil, Rice, Butter, Eggs, Vinegar, and Alcohol are considered unlimited basics.")

    with col_main:
        st.markdown("### 📖 Recipe Book")
        r1, r2, r3 = st.tabs(["⭐ Beginner", "⭐⭐ Intermediate", "⭐⭐⭐ Advanced"])
        
        def render_recipe_tab(recipe_list, container, locked=False, req_count=0):
            if locked:
                container.warning(f"🔒 Unlock {req_count} recipes in the previous tier to access this tab.")
                return

            for recipe in recipe_list:
                with container:
                    is_unlocked = recipe['name'] in st.session_state.unlocked_recipes
                    has_ingredients = all(inv.get(ing, 0) >= qty for ing, qty in recipe['ingredients'].items() if ing not in ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"])
                    
                    with st.expander(f"{recipe['icon']} {recipe['name']} - {get_difficulty_stars(recipe['diff'])}"):
                        st.markdown(f"**{recipe['desc']}**")
                        st.info(f"**Health Benefits:** {recipe.get('benefits', 'Nutritious wild food.')}")
                        st.markdown("---")
                        
                        st.markdown(f"**Ingredients Needed:**")
                        ing_cols = st.columns(len(recipe['ingredients']))
                        for i, (ing, qty) in enumerate(recipe['ingredients'].items()):
                            current_qty = inv.get(ing, 0)
                            status = "✅" if current_qty >= qty or ing in ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"] else "❌"
                            ing_cols[i].metric(f"{ing}", f"{current_qty}/{qty}")
                        
                        st.markdown("---")

                        if not is_unlocked:
                            st.warning(f"🔒 **Preparation Required:** Answer {len(recipe['prep_questions'])} questions.")
                            for i, q_data in enumerate(recipe['prep_questions']):
                                st.radio(f"Q{i+1}: {q_data['q']}", q_data['opts'], key=f"q_{recipe['name']}_{i}")
                            
                            if st.button("Submit Answers", key=f"submit_{recipe['name']}"):
                                passed = True
                                for i, q_data in enumerate(recipe['prep_questions']):
                                    key = f"q_{recipe['name']}_{i}"
                                    selected = st.session_state.get(key)
                                    if selected != q_data['a']:
                                        passed = False
                                
                                if passed:
                                    st.session_state.unlocked_recipes.append(recipe['name'])
                                    st.success(f"✅ Correct! {recipe['name']} Unlocked!")
                                    
                                    # Achievement Check (Unlock 3 Beginner)
                                    if recipe['diff'] == 1:
                                        count = len([r for r in st.session_state.unlocked_recipes if any(x['name'] == r and x['diff']==1 for x in RECIPES)])
                                        if count >= 3 and not st.session_state.achievements['kitchen_apprentice']:
                                            st.session_state.achievements['kitchen_apprentice'] = True
                                            st.toast("🏅 Achievement Unlocked: Apprentice!")
                                    
                                    # Achievement Check (Unlock all Intermediate)
                                    if recipe['diff'] == 2:
                                        total_inter = len([r for r in RECIPES if r['diff'] == 2])
                                        unlocked_inter = len([r for r in st.session_state.unlocked_recipes if any(x['name'] == r and x['diff']==2 for x in RECIPES)])
                                        if unlocked_inter == total_inter and not st.session_state.achievements['kitchen_master']:
                                            st.session_state.achievements['kitchen_master'] = True
                                            st.toast("🏅 Achievement Unlocked: Master Chef!")

                                    st.rerun()
                                else:
                                    st.error("Incorrect. Try again!")

                        else:
                            if has_ingredients:
                                st.success("✅ Ready to Cook!")
                                if st.button(f"🍳 Cook {recipe['name']}", key=f"cook_{recipe['name']}"):
                                    for ing, qty in recipe['ingredients'].items():
                                        if ing not in ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"]:
                                            st.session_state.master_inventory[ing] -= qty
                                    # Add result to inventory (Tab 4 Market can sell it)
                                    result_dish = recipe['name']
                                    st.session_state.master_inventory[result_dish] = st.session_state.master_inventory.get(result_dish, 0) + 1
                                    
                                    points = recipe['diff'] * 15
                                    st.session_state.kitchen_score += points
                                    st.toast(f"Made {recipe['name']}! +{points} XP")
                                    st.rerun()
                            else:
                                st.warning("Missing ingredients! Go foraging in Tab 1.")

        beginner_recipes = [r for r in RECIPES if r['diff'] == 1]
        inter_recipes = [r for r in RECIPES if r['diff'] == 2]
        adv_recipes = [r for r in RECIPES if r['diff'] == 3]

        render_recipe_tab(beginner_recipes, r1, locked=False)
        
        inter_locked = False
        if beginner_unlocked < 3: inter_locked = True
        render_recipe_tab(inter_recipes, r2, locked=inter_locked, req_count=3)
        
        adv_locked = False
        if inter_unlocked < 3: adv_locked = True
        render_recipe_tab(adv_recipes, r3, locked=adv_locked, req_count=3)

        st.markdown("---")
        st.metric("🏆 Kitchen Score", st.session_state.kitchen_score)

    # --- ACHIEVEMENT DISPLAY (TAB 6) ---
    st.markdown("---")
    with st.expander("🏅 Kitchen Achievements"):
        for key in ["kitchen_apprentice", "kitchen_master"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}*")
