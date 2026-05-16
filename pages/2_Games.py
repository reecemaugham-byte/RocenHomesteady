from utils import init_session_state, apply_brand_theme, render_sidebar, UK_PLANTS, generate_voice, EDGE_TTS_AVAILABLE

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Games - Rocen Homesteady",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
init_session_state() # <--- ENSURE THIS RUNS FIRST
apply_brand_theme()
render_sidebar()

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

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Select a Season** using the buttons at the top.
        2. A plant will appear. Read its name.
        3. Choose the **Habitat** where it grows.
        4. **Collect Plants:** Find unique plants to fill your Herbarium.
        5. **Bonus:** Get 5 right in a row to unlock a Bonus Question!
        """)

    habitat_icons = {"Woodland": "🌲", "Hedgerow": "🌿", "Coastal": "🏖️", "Urban": "🏡", "Meadow": "🌾"}

    st.markdown("### 🗓️ Choose a Season")
    season_cols = st.columns(4)
    seasons = ["Spring", "Summer", "Autumn", "Winter"]
    season_icons = {"Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"}

    # Default Season Logic
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

    # --- SIDEBAR: COLLECTION TRACKER ---
        # Show progress in sidebar
        # FIX: Use .get() to prevent AttributeError if state is missing
        collection_list = st.session_state.get('collection_edible', [])
        total_found = len(collection_list)
        
        st.sidebar.metric("🌿 Species Found", f"{total_found}/50")
        if total_found > 0:
            with st.sidebar.expander("View Collection"):
                # Show last 5 found
                for p in collection_list[-5:]:
                    st.write(f"✅ {p}")

        col1, col2, col3 = st.columns(3)
        # FIX: Also use .get() for score/lives just in case
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
        # Trigger bonus question if streak is 5 (and not already in bonus)
        if st.session_state.game_streak > 0 and st.session_state.game_streak % 5 == 0 and not st.session_state.get('bonus_round'):
            st.session_state.bonus_round = True

        if st.session_state.get('bonus_round'):
            # BONUS QUESTION
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
                    # Add to collection
                    if bonus_plant['name'] not in st.session_state.collection_edible:
                        st.session_state.collection_edible.append(bonus_plant['name'])
                else:
                    st.error("Incorrect!")
                st.session_state.bonus_round = False
                st.session_state.game_streak = 0 # Reset streak after bonus
                st.rerun()

        else:
            # STANDARD QUESTION LOGIC
            if st.session_state.get('current_question') is None:
                plant = random.choice(available_plants)
                raw_habitat = plant['habitat'].split(',')[0].strip()
                
                if raw_habitat in ["Woodlands", "Woods", "Wood"]: correct_habitat = "Woodland"
                elif raw_habitat in ["Hedgerows", "Hedgerow", "Roadsides"]: correct_habitat = "Hedgerow"
                elif raw_habitat in ["Meadows", "Grassland", "Fields", "Fields, Gardens"]: correct_habitat = "Meadow"
                elif raw_habitat in ["Coastal", "Coastal Shingle", "Rocky Coasts", "Sandy/Muddy Beaches", "Estuaries"]: correct_habitat = "Coastal"
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
                        # CORRECT ANSWER
                        st.session_state.game_score += 10 + (st.session_state.game_streak * 2)
                        st.session_state.game_streak += 1
                        st.session_state.total_plants_identified += 1
                        
                        # ADD TO COLLECTION
                        if q['plant']['name'] not in st.session_state.collection_edible:
                            st.session_state.collection_edible.append(q['plant']['name'])
                        
                        # CUSTOM SUCCESS: FALLING LEAVES
                        st.markdown("""
                        <div style="animation: fall 3s linear forwards; position: fixed; top: 0; left: 50%; font-size: 40px; z-index:9999;">🍃</div>
                        <div style="animation: fall 3s linear 0.5s forwards; position: fixed; top: 0; left: 30%; font-size: 40px; z-index:9999;">🍂</div>
                        <div style="animation: fall 3s linear 1s forwards; position: fixed; top: 0; left: 70%; font-size: 40px; z-index:9999;">🌿</div>
                        """, unsafe_allow_html=True)
                        
                        st.success(f"✅ Correct! {q['plant']['name']} loves the {option}!")
                        
                        # EDUCATIONAL DEBRIEF
                        with st.expander("🔎 Foraging Tip", expanded=True):
                            tips = q['plant'].get('foraging_tips', {})
                            if tips:
                                st.write(f"**Where:** {tips.get('where', 'N/A')}")
                                st.write(f"**When:** {tips.get('when', 'N/A')}")
                                st.write(f"**Sustainable:** {tips.get('sustainable', 'N/A')}")
                            else:
                                st.write(q['plant'].get('description', 'No info.'))
                        
                        if active_season not in st.session_state.season_badge_progress:
                            st.session_state.season_badge_progress.append(active_season)
                    else:
                        # WRONG ANSWER
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
            st.session_state.game_streak = 0
            st.rerun()

# ==========================================
# GAME TAB 2: SURVIVAL SCHOOL (WITH AUDIO)
# ==========================================
with tab2:
    st.header("☠️ Survival School")
    st.caption("📚 Curriculum Link: Science (Plants), PSHE (Safety)")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Read the Case File** carefully.
        2. You have two suspects: One is **Safe**, one is **Poisonous**.
        3. Click the **Safe** plant to solve the case.
        4. **Unlock Levels:** Solve 3 cases in a row to unlock the next difficulty level.
        """)

    # --- LEVEL SYSTEM ---
    if 'survival_level' not in st.session_state:
        st.session_state.survival_level = 1
    
    # Progress
    progress = st.session_state.survival_correct_count / 5
    st.progress(progress, text=f"Level {st.session_state.survival_level} Progress: {st.session_state.survival_correct_count}/5 Cases")
    col1, col2 = st.columns(2)
    col1.metric("❤️ Lives", "❤️" * max(0, st.session_state.survival_lives))
    col2.metric("🌟 Score", st.session_state.survival_score)
    st.markdown("---")

    # --- CASE FILES (With Levels) ---
    # Level 1: Plants (Easy)
    # Level 2: Fungi & Roots (Advanced)
    
    CASE_FILES = [
        # --- LEVEL 1: PLANTS ---
        {"level": 1, "clue": "You find a tall plant with white umbrella-shaped flowers ☂️. You check the stem. It is **smooth** (no hairs) and has **purple spots** on it.", "rule": "🚨 **Rule:** In the Carrot family, purple spots usually mean POISON.", "safe_plant": "Wild Carrot", "danger_plant": "Hemlock", "safe_icon": "🥕", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Hemlock (POISON):** Smooth stem with purple spots. Smells like mouse urine.\n- **Wild Carrot (Safe):** Hairy stem. Smells like carrots. **Hairy is Happy, Smooth is Suspicious!**", "safe_habitat": "Meadows"},
        {"level": 1, "clue": "You find a plant with broad green leaves in a damp woodland. You crush a leaf and it smells strongly of **garlic** 🧄.", "rule": "✅ **Rule:** Strong onion/garlic smell is usually a good sign.", "safe_plant": "Wild Garlic", "danger_plant": "Lily of the Valley", "safe_icon": "🌿", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Lily of the Valley (POISON):** Has no garlic smell. Has bell-shaped flowers.\n- **Wild Garlic (Safe):** Smells strongly of garlic. **No smell = Leave it be.**", "safe_habitat": "Woodland"},
        {"level": 1, "clue": "A plant with strap-like leaves grows in the woods. You roll the stem between your fingers—it feels **triangular** (like a keel ⛵).", "rule": "✅ **Rule:** A triangular stem is a unique ID feature.", "safe_plant": "Three-Cornered Leek", "danger_plant": "Bluebell", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Bluebell (POISON):** Round stem. Blue bells. All parts toxic.\n- **Three-Cornered Leek (Safe):** Triangular stem. White flowers. Smells like onion/garlic. **Triangle = Tasty.**", "safe_habitat": "Woodland"},
        {"level": 1, "clue": "You find a bush with dark berries. The leaves are arranged in **pairs** opposite each other on the stem.", "rule": "✅ **Rule:** 'Opposite' leaves (pairs) are safe for Elder. 'Alternate' leaves are dangerous.", "safe_plant": "Elderflower", "danger_plant": "Dwarf Elder", "safe_icon": "🌸", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Dwarf Elder (POISON):** Leaves are alternate (one by one). Flowers stand upright.\n- **Elderflower (Safe):** Leaves are opposite (in pairs). Flowers droop down.", "safe_habitat": "Hedgerow"},
        
        # --- LEVEL 2: FUNGI & ROOTS (Unlock after 5 streak) ---
        {"level": 2, "clue": "A bright orange mushroom grows under an oak tree. Under the cap, it has **ridges** (like false gills) that run down the stem. It smells like **apricots** 🍑.", "rule": "✅ **Rule:** True gills are thin sheets. Ridges are blunt and thick.", "safe_plant": "Chanterelle", "danger_plant": "False Chanterelle", "safe_icon": "🍄", "danger_icon": "🚫", "fact": "🕵️ **Inspector's Report:**\n- **False Chanterelle (Inedible):** Has true gills (thin sheets). No apricot smell.\n- **Chanterelle (Safe):** Has 'false gills' (ridges) and smells fruity. **Ridges = Rewarding.**", "safe_habitat": "Woodland"},
        {"level": 2, "clue": "You find a mushroom with a honeycomb cap (pitted like a sponge). You cut it open and it is **completely hollow** inside.", "rule": "✅ **Rule:** If it's hollow like a balloon, it might be a Morel.", "safe_plant": "Morel", "danger_plant": "False Morel", "safe_icon": "🍄", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **False Morel (POISON):** Looks brain-like (wrinkled). Inside is chambered/solid (NOT hollow).\n- **Morel (Safe):** Honeycomb cap. Completely hollow inside. **Hollow = Happy.**", "safe_habitat": "Woodland"},
        {"level": 2, "clue": "You are in a dry meadow. You dig up a small tuber. The stem is fine and feathery (like a carrot). The area is **dry and grassy**.", "rule": "✅ **Rule:** Habitat is key. Pignut likes dry ground.", "safe_plant": "Pignut", "danger_plant": "Hemlock Water Dropwort", "safe_icon": "🥔", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Hemlock Water Dropwort (DEADLY):** Grows in WET ground (ditches/rivers). Roots look like fingers.\n- **Pignut (Safe):** Grows in DRY meadows. Single small tuber. **Wet = Worry. Dry = Dig.**", "safe_habitat": "Meadow"},
        {"level": 2, "clue": "You see an evergreen tree. You pick a needle and roll it in your fingers. It feels **round** and comes in a **bundle of two**.", "rule": "✅ **Rule:** Round needles in bundles are Pine. Flat needles are Yew.", "safe_plant": "Pine Needles", "danger_plant": "Yew", "safe_icon": "🌲", "danger_icon": "☠️", "fact": "🕵️ **Inspector's Report:**\n- **Yew (POISON):** Flat needles. Single, not in bundles. No smell.\n- **Pine (Safe):** Round needles in bundles (2-5). Smells of resin. **Round & Bundles = Safe.**", "safe_habitat": "Woodland"}
    ]

    # Filter available cases based on level
    available_cases = [c for c in CASE_FILES if c['level'] <= st.session_state.survival_level]

    if st.session_state.survival_current_case is None:
        st.session_state.survival_current_case = random.choice(available_cases)
        st.session_state.survival_result = None

    case = st.session_state.survival_current_case
    
    # Show Level Badge
    level_names = {1: "🌱 Level 1: Plants", 2: "🍄 Level 2: Fungi & Roots"}
    st.info(f"**{level_names.get(st.session_state.survival_level, 'Level 1')}**")

    st.info(f"🔎 **New Case File Found!**")
    st.markdown(f"**Habitat:** {case['safe_habitat']}")
    st.markdown(f"**Your Observation:** {case['clue']}")
    
    # --- AUDIO FEATURE ---
    if EDGE_TTS_AVAILABLE:
        if st.button("🔊 Listen to Clue", key="audio_clue_btn"):
            audio_bytes = generate_voice(case['clue'])
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

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
        # --- RESULT SECTION ---
        if st.session_state.survival_result == "correct":
            st.success("✅ CASE SOLVED! Great work, Inspector.")
            # Check for Level Up (5 streak)
            if st.session_state.survival_correct_count >= 5 and st.session_state.survival_level == 1:
                st.session_state.survival_level = 2
                st.session_state.survival_correct_count = 0
                st.markdown("# 🏆 LEVEL UP!")
                st.write("You have unlocked **Level 2: Fungi & Roots**!")
        else:
            st.error("☠️ DANGER! That was the wrong choice.")

        # Show Inspector's Report
        st.markdown("### 📝 Case File Analysis")
        st.markdown(case['fact'])
        
        # --- AUDIO FEATURE (Report) ---
        if EDGE_TTS_AVAILABLE:
            if st.button("🔊 Listen to Report", key="audio_report_btn"):
                # Clean text for audio (remove markdown bolding)
                clean_fact = case['fact'].replace('**', '')
                audio_bytes = generate_voice(clean_fact)
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')

        # Show ID Keys Table
        plant_name = case['safe_plant'] if st.session_state.survival_result == "correct" else case['danger_plant']
        plant_data = next((p for p in UK_PLANTS['edible'] if p['name'] == plant_name), None)
        if not plant_data:
            plant_data = next((p for p in UK_PLANTS['poisonous'] if p['name'] == plant_name), None)

        if plant_data:
            st.markdown("#### 🔎 Identification Keys")
            id_keys = plant_data.get('id_keys', {})
            if id_keys:
                for key, value in id_keys.items():
                    st.markdown(f"- **{key}:** {value}")

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

# ==========================================
# GAME TAB 3: DAILY QUIZ
# ==========================================
with tab3:
    st.header("🎯 The Daily Challenge")
    st.caption("📚 Curriculum Link: Science (Plants), Seasonal Changes")
    
    with st.expander("📖 How to Play"):
        st.markdown("""
        - **Categories:** Choose a topic (e.g., Coastal, Trees) to study.
        - **Difficulty:** Beginner gives 3 options. Expert gives 4.
        - **Learn:** Correct answers show the Plant Card!
        - **Streak:** Build a streak for bonus points!
        """)

    # --- SETTINGS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        quiz_mode = st.selectbox("📚 Category", ["All", "Edible Only", "Poisonous Only", "Coastal", "Trees", "Fungi"])
    with col2:
        difficulty = st.radio("Difficulty", ["Beginner", "Expert"], horizontal=True)
    with col3:
        challenge_mode = st.checkbox("⚔️ Challenge Mode (1 Life)", value=False)

    st.markdown("---")

    # --- STATS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Streak", f"{st.session_state.daily_streak} Days")
    col2.metric("🌟 Score", st.session_state.quiz_score)
    col3.metric("❓ Question", f"{st.session_state.quiz_q_num}/{st.session_state.quiz_max}")
    st.progress(st.session_state.quiz_q_num / st.session_state.quiz_max)

    # --- QUESTION LOGIC ---
    # Filter plants based on category
    if quiz_mode == "All":
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
    elif quiz_mode == "Edible Only":
        pool = UK_PLANTS['edible']
    elif quiz_mode == "Poisonous Only":
        pool = UK_PLANTS['poisonous']
    else:
        # Filter by category key
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
                        
                        # --- DIAMOND: Show Plant Card on Success ---
                        with st.expander("🔎 Fact Check", expanded=True):
                            st.markdown(f"**{q['fact']}**")
                            if 'id_keys' in q['plant']:
                                st.markdown("Identification Keys:")
                                for k, v in q['plant']['id_keys'].items():
                                    st.markdown(f"- **{k}:** {v}")
                    else:
                        st.session_state.daily_streak = 0
                        st.toast("❌ Oops!")
                    
                    # Progress Logic
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
    
    # --- GAME STATE INIT (MUST BE FIRST) ---
    if st.session_state.get('village') is None:
        grid = [['🌲' for _ in range(6)] for _ in range(4)]
        grid[1][2] = '🌊' # Stream
        grid[1][3] = '🌊' # Stream
        st.session_state.village = {
            'grid': grid,
            'stats': {'Food': 50, 'Water': 50, 'Power': 0, 'Stamina': 100, 'Money': 100, 'Max_Power': 20},
            'inventory': {},
            'buildings': [],
            'owned_buildings': {},
            'placing_mode': None,
            'day': 1,
            'season': 'Spring',
            'nature_health': 100
        }

    game = st.session_state.village

    # --- WIN CONDITION CHECK ---
    if game['stats']['Money'] >= 2000:
        st.balloons()
        st.success("🏆 **VILLAGE MASTER!** You have accumulated £2000! You win!")

    # --- DEFINITIONS ---
    ITEMS_DATA = {
        "Dandelion": {"icon": "🌼", "rarity": 0.8, "value": 2, "type": "Plant"},
        "Nettle": {"icon": "🌿", "rarity": 0.8, "value": 1, "type": "Plant"},
        "Wild Garlic": {"icon": "🌱", "rarity": 0.5, "value": 3, "type": "Plant"},
        "Wood": {"icon": "🪵", "rarity": 0.6, "value": 5, "type": "Material"},
        "Stone": {"icon": "🪨", "rarity": 0.4, "value": 5, "type": "Material"},
        "Elderflower": {"icon": "🌸", "rarity": 0.3, "value": 8, "type": "Plant"},
        "Eggs": {"icon": "🥚", "rarity": 0.0, "value": 10, "type": "Produce"},
        "Fish": {"icon": "🐟", "rarity": 0.0, "value": 12, "type": "Food"},
        "Dandelion Tea": {"icon": "🍵", "rarity": 0.0, "value": 15, "type": "Artisan"}
    }
    
    BUILDINGS = {
        "House": {"cost": 50, "icon": "🏠", "desc": "+20 Stamina/day"},
        "Well": {"cost": 30, "icon": "🪨", "desc": "+5 Water/day"},
        "Coop": {"cost": 40, "icon": "🐔", "desc": "1 Egg/day"},
        "DIY Solar": {"cost": 50, "icon": "🔋", "desc": "+2 Power/day"},
        "Solar Array": {"cost": 300, "icon": "☀️", "desc": "+10 Power/day"},
        "Nature Reserve": {"cost": 150, "icon": "🌳", "desc": "Restores Nature"}
    }

    # --- RENDER STATS ---
    s = game['stats']
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🍖 Food", s['Food'])
    m2.metric("💧 Water", s['Water'])
    m3.metric("⚡ Power", f"{s['Power']}/{s['Max_Power']}")
    m4.metric("💪 Stamina", s['Stamina'])
    m5.metric("💰 Money", f"£{s['Money']}")
    
    nature = game['nature_health']
    nature_icon = "🟢" if nature > 50 else "🟡" if nature > 20 else "🔴"
    st.metric(f"{nature_icon} Nature Health", nature)
    
    if s['Food'] <= 10 or s['Water'] <= 10:
        st.warning("⚠️ Low Resources! Forage or Fish soon.")
    
    st.markdown("---")

    # --- TABS ---
    map_tab, forage_tab = st.tabs(["🗺️ Village Map", "🌲 Gather & Market"])
    
    with map_tab:
        # --- PLACEMENT MODE LOGIC ---
        if game['placing_mode']:
            # If user is in placing mode, show status and cancel button
            st.info(f"📍 **Placing Mode:** Click an empty forest tile (🌲) to place your **{game['placing_mode']}**.")
            # Refund logic
            if st.button("❌ Cancel Placement (Refund Money)"):
                # Find cost and refund
                cost = BUILDINGS[game['placing_mode']]['cost']
                game['stats']['Money'] += cost
                game['placing_mode'] = None
                st.success(f"Placement cancelled. Refunded £{cost}.")
                st.rerun()

        # --- GRID DISPLAY (Interactive) ---
        st.markdown("#### 🗺️ Your Land")
        
        # Custom CSS for Buttons to look like grid cells
        st.markdown("""
        <style>
        /* Make streamlit buttons look like tiles */
        div.stButton > button {
            width: 100%;
            height: 3em;
            background-color: #3A2416; /* Dark Coffee */
            color: white;
            border: 1px solid #B87333; /* Copper */
            font-size: 24px;
            padding: 0;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)

        for row_idx, row in enumerate(game['grid']):
            cols = st.columns(6)
            for col_idx, icon in enumerate(row):
                current_tile = game['grid'][row_idx][col_idx]
                
                # --- 1. PLACING A BUILDING ---
                if game['placing_mode'] and current_tile == '🌲':
                    b_name = game['placing_mode']
                    b_icon = BUILDINGS[b_name]['icon']
                    # This button uses the CSS above to look like a tile
                    if cols[col_idx].button(f"📍\n{b_icon}", key=f"place_{row_idx}_{col_idx}"):
                        game['grid'][row_idx][col_idx] = b_icon
                        if b_name not in game['owned_buildings']: game['owned_buildings'][b_name] = 0
                        game['owned_buildings'][b_name] += 1
                        game['placing_mode'] = None # Exit placing mode
                        st.success(f"{b_name} built!")
                        st.rerun()

                # --- 2. STREAM (FISHING) ---
                elif current_tile == '🌊':
                    # Button just shows the icon, but acts as fishing
                    if cols[col_idx].button("🎣", key=f"fish_{row_idx}_{col_idx}", help="Fish here (-5 Stamina)"):
                        if game['stats']['Stamina'] >= 5:
                            game['stats']['Stamina'] -= 5
                            game['inventory']['Fish'] = game['inventory'].get('Fish', 0) + 1
                            st.success("Caught a Fish! 🐟")
                            st.rerun()
                        else:
                            st.error("Need 5 Stamina to fish.")

                # --- 3. EXISTING BUILDINGS ---
                else:
                    # Just show the icon. 
                    # We use a disabled button to maintain the grid shape/size consistency
                    cols[col_idx].button(icon, key=f"view_{row_idx}_{col_idx}", disabled=True)

        st.markdown("---")

        # --- BUILD MENU (Compact) ---
        st.markdown("#### 🛠️ Build")
        
        # Only show buy options if NOT in placing mode
        if not game['placing_mode']:
            build_cols = st.columns(len(BUILDINGS))
            for i, (name, data) in enumerate(BUILDINGS.items()):
                if build_cols[i].button(f"{data['icon']} {name}\n£{data['cost']}"):
                    if game['stats']['Money'] >= data['cost']:
                        game['stats']['Money'] -= data['cost']
                        game['placing_mode'] = name
                        st.success(f"Bought {name}! Click map to place.")
                        st.rerun()
                    else:
                        st.error("Not enough money!")
        else:
            st.warning("Finish placing your current building or cancel before buying another.")

        # Next Day Button
        if st.button("⏭️ Next Day (Rest & Collect)", key="next_day_village", use_container_width=True):
            game['day'] += 1
            game['stats']['Food'] = max(0, game['stats']['Food'] - 1)
            game['stats']['Water'] = max(0, game['stats']['Water'] - 1)
            game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
            
            for row in game['grid']:
                for tile in row:
                    if tile == '🏠': game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
                    elif tile == '🪨': game['stats']['Water'] += 5
                    elif tile == '🐔': game['inventory']['Eggs'] = game['inventory'].get('Eggs', 0) + 1
                    elif tile == '🔋': game['stats']['Power'] = min(game['stats']['Max_Power'], game['stats']['Power'] + 2)
                    elif tile == '☀️': game['stats']['Power'] = min(game['stats']['Max_Power'], game['stats']['Power'] + 10)
                    elif tile == '🌳': game['nature_health'] = min(100, game['nature_health'] + 10)

            if game['nature_health'] < 100:
                game['nature_health'] = min(100, game['nature_health'] + 5)
            st.rerun()

    with forage_tab:
        st.markdown("### 🌲 Gather & Market")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌿 Actions")
            st.markdown("##### 🌲 Woods")
            st.markdown("_Costs 10 Stamina, reduces Nature Health._")
            if st.button("Forage in Woods", key="forage_woods"):
                if game['stats']['Stamina'] >= 10:
                    if game['nature_health'] >= 5:
                        game['stats']['Stamina'] -= 10
                        game['nature_health'] = max(0, game['nature_health'] - 5)
                        found = [name for name, data in ITEMS_DATA.items() if random.random() < data['rarity'] and name != "Fish"]
                        for f in found:
                            game['inventory'][f] = game['inventory'].get(f, 0) + 1
                        st.success(f"Found: {', '.join(found[:3])}...")
                        st.rerun()
                    else:
                        st.error("Nature Health is too low!")
                else:
                    st.error("Need 10 Stamina!")
            
            st.markdown("##### 🏭 Production")
            has_power = game['stats']['Power'] >= 2
            if st.button("Make Dandelion Tea (5 🌼 + 2 ⚡)", disabled=not has_power):
                if game['inventory'].get('Dandelion', 0) >= 5:
                    game['inventory']['Dandelion'] -= 5
                    game['stats']['Power'] -= 2
                    game['inventory']['Dandelion Tea'] = game['inventory'].get('Dandelion Tea', 0) + 1
                    st.success("Brewed Tea!")
                    st.rerun()
                else:
                    st.error("Not enough Dandelions.")

        with col2:
            st.markdown("#### 💰 Market")
            st.markdown("_Sell items for Money._")
            if not game['inventory']:
                st.info("No items to sell.")
            else:
                for item_name, count in game['inventory'].items():
                    val = ITEMS_DATA.get(item_name, {'value': 5})['value']
                    if st.button(f"Sell {item_name} ({count}) - £{val} each", key=f"sell_{item_name}"):
                        game['stats']['Money'] += (val * count)
                        del game['inventory'][item_name]
                        st.success(f"Sold {count} {item_name}!")
                        st.rerun()

# ==========================================
# GAME TAB 5: FARM TYCOON
# ==========================================
with tab5:
    st.header("🚜 Farm Tycoon: Diamond Edition")
    st.caption("📚 Build, Automate, and Master the Market!")

    with st.expander("📖 Diamond Guide"):
        st.markdown("""
        - **Seasons:** Change every 10 days. Winter stops growth!
        - **Market:** Prices fluctuate. Harvest to Inventory, sell when prices are high!
        - **Automation:** Buy Barns to auto-collect animal products.
        - **Synergy:** Place Beehives next to crops for +50% yield.
        - **Threat:** Invasives spread! Clear them or lose your crops.
        """)

    # --- GAME STATE INIT ---
    if st.session_state.get('farm_game') is None:
        # Generate Stream
        grid = [[0 for _ in range(6)] for _ in range(5)]
        stream_col = random.randint(1, 4)
        for r in range(5):
            grid[r][stream_col] = 1 # 1 is Stream
            if random.random() > 0.5:
                stream_col = max(0, min(5, stream_col + random.choice([-1, 1])))
                grid[r][stream_col] = 1

        st.session_state.farm_game = {
            'grid': grid,
            'money': 150, # Start with a bit more for Diamond
            'day': 1,
            'season': 'Spring',
            'weather': '☀️ Sunny',
            'tool': 'Carrot',
            'inventory': {}, # Stores harvested goods
            'market_prices': {"Carrot": 10, "Wheat": 15, "Corn": 20, "Egg": 25, "Milk": 40, "Honey": 50},
            'game_over': False,
            'invasives_cleared': 0
        }

    game = st.session_state.farm_game

    # --- DEFINITIONS ---
    # Grid IDs: 0=Dirt, 1=Stream, 2=Seed, 3=Growing, 4=Ready
    # 5=Chicken, 6=Cow, 7=Invasive, 8=Barn, 9=Beehive
    ICONS = {
        0: "🟤", 1: "🌊", 2: "🌱", 3: "🌿", 4: "🌾", 
        5: "🐔", 6: "🐄", 7: "🥀", 
        8: "🏠", # Barn
        9: "🐝"  # Beehive
    }

    CROPS = {"Carrot": 10, "Wheat": 15, "Corn": 20} # Base Prices
    ANIMALS = {"Chicken": 50, "Cow": 100}

    # --- HELPERS ---
    def get_season(day):
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        return seasons[(day // 10) % 4]

    def get_adjacent(r, c):
        # Returns valid neighbor coordinates
        neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if 0 <= r+dr < 5 and 0 <= c+dc < 6:
                neighbors.append((r+dr, c+dc))
        return neighbors

    # --- UI HEADER ---
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Day", game['day'])
    col2.metric("🌍 Season", get_season(game['day']))
    col3.metric("💰 Money", f"£{game['money']}")

    st.markdown("---")

    # --- TOOLBOX ---
    st.markdown("### 🛠️ Toolbox")
    tool_cols = st.columns(5)
    # Tools: Crops, Animals, Structures, Clear
    with tool_cols[0]:
        st.selectbox("Crops", ["Carrot", "Wheat", "Corn"], key="crop_tool")
        game['tool'] = st.session_state.crop_tool # Simplistic binding

    with tool_cols[1]:
        st.selectbox("Animals", ["Chicken", "Cow"], key="animal_tool")
        # We handle tools via buttons in this layout for simplicity

    with tool_cols[2]:
        if st.button("🏠 Barn (£300)"):
            game['tool'] = "Barn"
        if st.button("🐝 Beehive (£200)"):
            game['tool'] = "Beehive"

    with tool_cols[3]:
        if st.button("🧹 Clear Invasive"):
            game['tool'] = "Clear"

    with tool_cols[4]:
        if st.button("🛒 Sell All"):
            # Quick sell logic
            for item, count in game['inventory'].items():
                price = game['market_prices'].get(item, 10)
                # Season bonus in Autumn
                if get_season(game['day']) == "Autumn" and item in CROPS:
                    price = int(price * 1.5)
                game['money'] += price * count
            game['inventory'] = {}
            st.success("Sold everything!")
            st.rerun()

    st.markdown("---")

    # --- INVENTORY & MARKET ---
    st.markdown("### 🎒 Inventory & Market")
    inv_cols = st.columns(len(game['market_prices']))
    for i, (item, price) in enumerate(game['market_prices'].items()):
        count = game['inventory'].get(item, 0)
        # Price Fluctuation Indicator
        base = CROPS.get(item, ANIMALS.get(item, 20))
        indicator = "📈" if price > base else ("📉" if price < base else "➡️")
        
        with inv_cols[i]:
            st.metric(f"{item}", f"{count} pcs", f"£{price} {indicator}")
            if st.button(f"Sell {item}", key=f"sell_{item}"):
                if count > 0:
                    game['money'] += price * count
                    game['inventory'][item] = 0
                    st.success(f"Sold {count} {item}!")
                    st.rerun()

    st.markdown("---")

    # --- THE GRID ---
    st.markdown("### 🗺️ Your Farm")
    st.info(f"Current Tool: **{game['tool']}** | Select an action above.")

    for r in range(5):
        cols = st.columns(6)
        for c in range(6):
            tile_val = game['grid'][r][c]
            icon = ICONS.get(tile_val, "❓")
            
            # Determine if we show a button or just the icon
            # Logic for interactions:
            # 1. Planting/Placing (On Empty 0)
            # 2. Harvesting (On 4)
            # 3. Collecting (On 5/6)
            # 4. Clearing (On 7)
            
            is_interactive = False
            btn_label = ""
            action = None
            
            if tile_val == 0: # Empty
                if game['tool'] in CROPS:
                    cost = CROPS[game['tool']]
                    btn_label = f"Plant £{cost}"
                    is_interactive = True
                    action = "plant"
                elif game['tool'] in ANIMALS:
                    cost = ANIMALS[game['tool']]
                    btn_label = f"Place £{cost}"
                    is_interactive = True
                    action = "place_animal"
                elif game['tool'] == "Barn":
                    btn_label = "Build £300"
                    is_interactive = True
                    action = "build_structure"
                elif game['tool'] == "Beehive":
                    btn_label = "Build £200"
                    is_interactive = True
                    action = "build_structure"
            
            elif tile_val == 4: # Ready Crop
                btn_label = "🌾 Harvest"
                is_interactive = True
                action = "harvest"
                
            elif tile_val == 5: # Chicken
                btn_label = "🐔 Collect"
                is_interactive = True
                action = "collect"
                
            elif tile_val == 6: # Cow
                btn_label = "🐄 Collect"
                is_interactive = True
                action = "collect"
                
            elif tile_val == 7: # Invasive
                if game['tool'] == "Clear":
                    btn_label = "🧹 Clear"
                    is_interactive = True
                    action = "clear"

            if is_interactive:
                # We use a small visual representation above the button for clarity
                # But here we put the icon inside the button for compactness
                if cols[c].button(f"{icon} {btn_label.split(' ')[0]}", key=f"{r}_{c}"):
                    # EXECUTE ACTIONS
                    cost = 0
                    if action == "plant": 
                        cost = CROPS[game['tool']]
                    elif action == "place_animal":
                        cost = ANIMALS[game['tool']]
                    elif action == "build_structure":
                        cost = 300 if game['tool'] == "Barn" else 200
                    
                    if game['money'] >= cost:
                        if action == "plant":
                            game['grid'][r][c] = 2 # Seed
                            game['money'] -= cost
                        elif action == "place_animal":
                            game['grid'][r][c] = 5 if game['tool'] == "Chicken" else 6
                            game['money'] -= cost
                        elif action == "build_structure":
                            game['grid'][r][c] = 8 if game['tool'] == "Barn" else 9
                            game['money'] -= cost
                        elif action == "harvest":
                            # Check for Beehive Bonus
                            bonus = 0
                            for nr, nc in get_adjacent(r, c):
                                if game['grid'][nr][nc] == 9: # Beehive
                                    bonus = 1
                                    break
                            crop_type = "Wheat" # Default logic for simplicity
                            # In a real app, we'd store what crop was planted.
                            # For Diamond, let's randomize or assume wheat for now, 
                            # OR we track crop types in a separate matrix.
                            # Simplification: Harvest gives "Crops" generic item
                            # But let's try to track...
                            # For now, let's just give 'Wheat' as placeholder
                            game['inventory']['Wheat'] = game['inventory'].get('Wheat', 0) + 1 + bonus
                            game['grid'][r][c] = 0
                        elif action == "collect":
                            # Check if near Barn (Auto-collect happens in next_day, but allow manual)
                            prod = "Egg" if tile_val == 5 else "Milk"
                            game['inventory'][prod] = game['inventory'].get(prod, 0) + 1
                            # We don't remove animal, just collect
                        elif action == "clear":
                            game['grid'][r][c] = 0
                            game['invasives_cleared'] += 1
                        st.rerun()
                    else:
                        st.error("Not enough money!")
            else:
                # Just show the icon
                cols[c].markdown(f"<div style='text-align:center; font-size:24px;'>{icon}</div>", unsafe_allow_html=True)

    # --- NEXT DAY LOGIC ---
    if st.button("⏭️ Next Day"):
        # 1. Market Fluctuation
        for item in game['market_prices']:
            # Prices fluctuate 50% up or down
            change = random.uniform(0.7, 1.3)
            game['market_prices'][item] = max(1, int(game['market_prices'][item] * change))
        
        # 2. Crop Growth & Animal Production
        season = get_season(game['day'])
        
        # Grid Scan for Logic
        for r in range(5):
            for c in range(6):
                tile = game['grid'][r][c]
                
                # Crop Growth
                if tile == 2 or tile == 3:
                    # Winter stops growth
                    if season != "Winter":
                        # Check Sprinkler/Beehive logic? 
                        # Beehive increases yield, doesn't speed growth. Sprinkler speeds growth.
                        # Let's assume Sprinkler (ID 10) logic later.
                        # Simple growth:
                        if tile == 2: game['grid'][r][c] = 3
                        elif tile == 3: game['grid'][r][c] = 4
                
                # Animal Production (Auto if near Barn)
                if tile in [5, 6]: # Chicken or Cow
                    # Check adjacent for Barn
                    has_barn = False
                    for nr, nc in get_adjacent(r, c):
                        if game['grid'][nr][nc] == 8: # Barn
                            has_barn = True
                            break
                    
                    if has_barn:
                        prod = "Egg" if tile == 5 else "Milk"
                        game['inventory'][prod] = game['inventory'].get(prod, 0) + 1
                
                # Invasive Spread Logic
                if tile == 7:
                    # Spread to adjacent crops
                    if random.random() < 0.3: # 30% chance to spread
                        targets = get_adjacent(r, c)
                        for nr, nc in targets:
                            if game['grid'][nr][nc] in [2, 3, 4]: # Kill crops
                                game['grid'][nr][nc] = 7
                                
        # 3. Events
        if random.random() < 0.2:
            st.toast(f"📉 Market News: Prices shifted!")
            
        game['day'] += 1
        st.rerun()

# ==========================================
# GAME TAB 6: THE WILD KITCHEN
# ==========================================
with tab6:
    st.header("🍳 The Wild Kitchen")
    st.caption("📚 Process your harvest. Master the prep. Unlock 30+ recipes!")
    
    # --- GAME STATE INIT ---
    if 'kitchen_inventory' not in st.session_state:
        # Sync with Tab 1 Collection OR give starter kit
        if 'collection_edible' in st.session_state and st.session_state.collection_edible:
            inv = {}
            for plant in st.session_state.collection_edible:
                inv[plant] = inv.get(plant, 0) + 1
            st.session_state.kitchen_inventory = inv
        else:
            # Expanded Starter Kit for immediate play
            st.session_state.kitchen_inventory = {
                "Nettle": 10, "Dandelion": 10, "Wild Garlic": 5, "Blackberries": 5,
                "Pine Needles": 10, "Hazelnut": 5, "Sorrel": 5, "Chickweed": 5
            }
        
        st.session_state.kitchen_score = 0
        st.session_state.unlocked_recipes = [] 
    
    # --- RECIPE DATABASE ---
    RECIPES = [
        # ==========================
        # ⭐ BEGINNER (1 Question)
        # ==========================
        {
            "name": "Nettle Soup",
            "ingredients": {"Nettle": 5, "Water": 1},
            "prep_questions": [
                {"q": "Why must nettles be cooked or dried?", "opts": ["To remove the sting", "To make them sweet", "To change color"], "a": "To remove the sting"}
            ],
            "icon": "🥣", "desc": "A rich, green soup full of vitamins.", "diff": 1
        },
        {
            "name": "Wild Garlic Pesto",
            "ingredients": {"Wild Garlic": 10, "Oil": 1},
            "prep_questions": [
                {"q": "Which part of Wild Garlic is edible?", "opts": ["Only the flowers", "Leaves, flowers, and bulbs", "Only the roots"], "a": "Leaves, flowers, and bulbs"}
            ],
            "icon": "🥗", "desc": "A fragrant pesto for pasta.", "diff": 1
        },
        {
            "name": "Dandelion Salad",
            "ingredients": {"Dandelion": 5},
            "prep_questions": [
                {"q": "When is best to harvest Dandelion leaves?", "opts": ["When the flower is yellow", "Before the flower opens (young)", "In winter"], "a": "Before the flower opens (young)"}
            ],
            "icon": "🥗", "desc": "Young leaves are less bitter.", "diff": 1
        },
        {
            "name": "Three-Cornered Leek Omelette",
            "ingredients": {"Three-Cornered Leek": 5, "Eggs": 2},
            "prep_questions": [
                {"q": "How to ID Three-Cornered Leek?", "opts": ["Smells of garlic, triangular stem", "Blue flowers, round stem", "Yellow flowers, spiky"], "a": "Smells of garlic, triangular stem"}
            ],
            "icon": "🍳", "desc": "A forager's breakfast.", "diff": 1
        },
        {
            "name": "Pine Needle Tea",
            "ingredients": {"Pine Needles": 10, "Water": 1},
            "prep_questions": [
                {"q": "How do you identify SAFE Pine needles?", "opts": ["Flat needles (Yew)", "Round needles in bundles", "Blue needles"], "a": "Round needles in bundles"}
            ],
            "icon": "🍵", "desc": "High in Vitamin C.", "diff": 1
        },
        {
            "name": "Beech Leaf Liqueur",
            "ingredients": {"Beech Leaves": 20, "Sugar": 1, "Alcohol": 1},
            "prep_questions": [
                {"q": "When should you pick Beech leaves?", "opts": ["Autumn (Brown)", "Spring (Young/Transparent)", "Winter"], "a": "Spring (Young/Transparent)"}
            ],
            "icon": "🥃", "desc": "A sweet, gin-based liquor.", "diff": 1
        },
        {
            "name": "Lime Leaf Salad",
            "ingredients": {"Lime (Leaves)": 10},
            "prep_questions": [
                {"q": "What do Lime (Basswood) leaves taste like?", "opts": ["Bitter", "Mild and slightly sweet", "Spicy"], "a": "Mild and slightly sweet"}
            ],
            "icon": "🥗", "desc": "Excellent fresh salad green.", "diff": 1
        },
        {
            "name": "Chickweed Salad",
            "ingredients": {"Chickweed": 10},
            "prep_questions": [
                {"q": "How do you identify Chickweed?", "opts": ["Line of hairs on stem", "Purple spots on stem", "Blue flowers"], "a": "Line of hairs on stem"}
            ],
            "icon": "🥗", "desc": "A mild, nutritious weed.", "diff": 1
        },
        {
            "name": "Wild Strawberry Jam",
            "ingredients": {"Wild Strawberry": 20, "Sugar": 1},
            "prep_questions": [
                {"q": "How do wild strawberries differ from barren strawberry?", "opts": ["Barren has petals with gaps", "Wild has blue flowers", "Barren has hairy leaves"], "a": "Barren has petals with gaps"}
            ],
            "icon": "🍯", "desc": "Tiny but intense flavor.", "diff": 1
        },
        {
            "name": "Roasted Hazelnuts",
            "ingredients": {"Hazelnut": 10},
            "prep_questions": [
                {"q": "What indicates a ripe Hazelnut?", "opts": ["Green husk", "Brown shell and leafy husk", "No leaves"], "a": "Brown shell and leafy husk"}
            ],
            "icon": "🌰", "desc": "Autumn treat.", "diff": 1
        },
        {
            "name": "Sea Purslane Salad",
            "ingredients": {"Sea Purslane": 10},
            "prep_questions": [
                {"q": "What is the main precaution with Sea Purslane?", "opts": ["It is very salty", "It is poisonous raw", "It has thorns"], "a": "It is very salty"}
            ],
            "icon": "🥗", "desc": "Salty coastal green.", "diff": 1
        },

        # ==============================
        # ⭐⭐ INTERMEDIATE (2 Questions)
        # ==============================
        {
            "name": "Dandelion Coffee",
            "ingredients": {"Dandelion": 20},
            "prep_questions": [
                {"q": "Which part is used for coffee?", "opts": ["Leaves", "Flowers", "Roots"], "a": "Roots"},
                {"q": "How must the roots be prepared?", "opts": ["Eaten raw", "Roasted and ground", "Boiled whole"], "a": "Roasted and ground"}
            ],
            "icon": "☕", "desc": "A caffeine-free coffee substitute.", "diff": 2
        },
        {
            "name": "Elderflower Cordial",
            "ingredients": {"Elderflower": 10, "Sugar": 1},
            "prep_questions": [
                {"q": "Why should you not wash Elderflowers?", "opts": ["Loses pollen (flavor)", "Becomes poisonous", "Petals fall off"], "a": "Loses pollen (flavor)"},
                {"q": "What must you check for before cooking?", "opts": ["Spiders", "Bugs/Maggots", "Birds"], "a": "Bugs/Maggots"}
            ],
            "icon": "🥤", "desc": "A sweet summery drink.", "diff": 2
        },
        {
            "name": "Blackberry Jam",
            "ingredients": {"Blackberries": 20, "Sugar": 1},
            "prep_questions": [
                {"q": "What must you check for when picking?", "opts": ["Check for bugs", "Check if they are red", "Check for thorns"], "a": "Check for bugs"},
                {"q": "What helps the jam set (thicken)?", "opts": ["Water", "Pectin (naturally in fruit)", "Oil"], "a": "Pectin (naturally in fruit)"}
            ],
            "icon": "🍯", "desc": "Preserved summer in a jar.", "diff": 2
        },
        {
            "name": "Rosehip Syrup",
            "ingredients": {"Rosehips": 15, "Sugar": 1},
            "prep_questions": [
                {"q": "Why remove the seeds?", "opts": ["Bitter", "Itchy irritation", "Poisonous"], "a": "Itchy irritation"},
                {"q": "What vitamin are Rosehips famous for?", "opts": ["Vitamin A", "Vitamin C", "Vitamin D"], "a": "Vitamin C"}
            ],
            "icon": "🧴", "desc": "Rich in Vitamin C.", "diff": 2
        },
        {
            "name": "Sorrel Soup",
            "ingredients": {"Sorrel": 15, "Water": 1},
            "prep_questions": [
                {"q": "What gives Sorrel its sour taste?", "opts": ["Sugar", "Oxalic Acid", "Citrus"], "a": "Oxalic Acid"},
                {"q": "Who should avoid large amounts?", "opts": ["Children", "People with kidney issues", "Elderly"], "a": "People with kidney issues"}
            ],
            "icon": "🥣", "desc": "Tangy and refreshing.", "diff": 2
        },
        {
            "name": "Hawthorn Ketchup",
            "ingredients": {"Hawthorn": 30, "Sugar": 1},
            "prep_questions": [
                {"q": "What do Hawthorn berries look like?", "opts": ["Blue pods", "Small red berries", "Blackberries"], "a": "Small red berries"},
                {"q": "What should you avoid when eating?", "opts": ["The skin", "The seeds (pips)", "The stem"], "a": "The seeds (pips)"}
            ],
            "icon": "🍅", "desc": "A tomato ketchup alternative.", "diff": 2
        },
        {
            "name": "Sweet Chestnut Roast",
            "ingredients": {"Sweet Chestnut": 20},
            "prep_questions": [
                {"q": "How does the case differ from Horse Chestnut?", "opts": ["Smooth/Warty", "Very spiky", "Green"], "a": "Very spiky"},
                {"q": "What must you do before roasting?", "opts": ["Peel them", "Score the shell", "Boil for 1 hour"], "a": "Score the shell"}
            ],
            "icon": "🌰", "desc": "Roasting over an open fire.", "diff": 2
        },
        {
            "name": "Marsh Samphire Sauté",
            "ingredients": {"Marsh Samphire": 15, "Butter": 1},
            "prep_questions": [
                {"q": "Where does Samphire grow?", "opts": ["Dry Meadows", "Saltmarshes/Mud", "Trees"], "a": "Saltmarshes/Mud"},
                {"q": "How do you harvest sustainably?", "opts": ["Pull up roots", "Cut top 2 inches", "Dig with trowel"], "a": "Cut top 2 inches"}
            ],
            "icon": "🥦", "desc": "Sea asparagus.", "diff": 2
        },
        {
            "name": "Sea Kale Steam",
            "ingredients": {"Sea Kale": 10, "Butter": 1},
            "prep_questions": [
                {"q": "Why is Sea Kale rare in some areas?", "opts": ["Over-harvested", "Poisonous", "Invasive"], "a": "Over-harvested"},
                {"q": "What does it taste like?", "opts": ["Cabbage/Asparagus", "Fish", "Sweet"], "a": "Cabbage/Asparagus"}
            ],
            "icon": "🥬", "desc": "Pick sparingly.", "diff": 2
        },
        {
            "name": "Dulse Crisps",
            "ingredients": {"Dulse": 10, "Oil": 1},
            "prep_questions": [
                {"q": "What is Dulse?", "opts": ["A mushroom", "A seaweed", "A berry"], "a": "A seaweed"},
                {"q": "How do you eat it?", "opts": ["Raw", "Fried or dried", "Boiled only"], "a": "Fried or dried"}
            ],
            "icon": "🥢", "desc": "Salty snack.", "diff": 2
        },
        {
            "name": "Bilberry Pie",
            "ingredients": {"Bilberry": 25, "Sugar": 1},
            "prep_questions": [
                {"q": "Where do Bilberries grow?", "opts": ["Low shrubs on moors", "High trees", "Gardens"], "a": "Low shrubs on moors"},
                {"q": "What is the lookalike danger?", "opts": ["Blueberries", "Deadly Nightshade", "Cherries"], "a": "Deadly Nightshade"}
            ],
            "icon": "🥧", "desc": "Wild blueberry pie.", "diff": 2
        },
        {
            "name": "Meadowsweet Cordial",
            "ingredients": {"Meadowsweet": 15, "Sugar": 1},
            "prep_questions": [
                {"q": "What does Meadowsweet smell like?", "opts": ["Garlic", "Almond/Honey", "Mint"], "a": "Almond/Honey"},
                {"q": "Who should avoid Meadowsweet?", "opts": ["Children", "People with Aspirin allergy", "Diabetics"], "a": "People with Aspirin allergy"}
            ],
            "icon": "🥤", "desc": "Floral and sweet.", "diff": 2
        },
        {
            "name": "Pignut Roast",
            "ingredients": {"Pignut": 15, "Oil": 1},
            "prep_questions": [
                {"q": "Where do Pignuts grow?", "opts": ["Wet ditches", "Dry meadows", "Trees"], "a": "Dry meadows"},
                {"q": "What is the deadly lookalike?", "opts": ["Hemlock Water Dropwort", "Potato", "Parsnip"], "a": "Hemlock Water Dropwort"}
            ],
            "icon": "🥔", "desc": "Nutty tuber.", "diff": 2
        },
        {
            "name": "Alexanders Stew",
            "ingredients": {"Alexanders": 15, "Water": 1},
            "prep_questions": [
                {"q": "What part is eaten?", "opts": ["Roots", "Stems", "Flowers"], "a": "Stems"},
                {"q": "What is the lookalike danger?", "opts": ["Hemlock (Purple spots)", "Wild Carrot", "Celery"], "a": "Hemlock (Purple spots)"}
            ],
            "icon": "🍲", "desc": "Coastal celery.", "diff": 2
        },

        # ============================
        # ⭐⭐⭐ ADVANCED (3 Questions)
        # ============================
        {
            "name": "Acorn Coffee",
            "ingredients": {"Acorn": 20},
            "prep_questions": [
                {"q": "Why not eat raw?", "opts": ["Too hard", "Contain tannins (bitter)", "Protected"], "a": "Contain tannins (bitter)"},
                {"q": "How to remove tannins?", "opts": ["Leaching (soaking)", "Freezing", "Burning"], "a": "Leaching (soaking)"},
                {"q": "When to harvest?", "opts": ["Green", "Brown (ripe)", "White"], "a": "Brown (ripe)"}
            ],
            "icon": "☕", "desc": "Must be leached first.", "diff": 3
        },
        {
            "name": "Chanterelle Risotto",
            "ingredients": {"Chanterelle": 10, "Rice": 1},
            "prep_questions": [
                {"q": "How to ID Chanterelle?", "opts": ["True gills (sheets)", "False gills (ridges)", "Sponge"], "a": "False gills (ridges)"},
                {"q": "What does it smell like?", "opts": ["Aniseed/Apricot", "Mud", "Nothing"], "a": "Aniseed/Apricot"},
                {"q": "Danger lookalike?", "opts": ["False Chanterelle", "Death Cap", "Field Mushroom"], "a": "False Chanterelle"}
            ],
            "icon": "🍚", "desc": "A gourmet wild meal.", "diff": 3
        },
        {
            "name": "Crab Apple Jelly",
            "ingredients": {"Crab Apple": 25, "Sugar": 1},
            "prep_questions": [
                {"q": "Why not eat raw?", "opts": ["Poisonous", "Too tart/sour", "Too hard"], "a": "Too tart/sour"},
                {"q": "Why is it good for jelly?", "opts": ["High Pectin", "Red Color", "Soft skin"], "a": "High Pectin"},
                {"q": "What to remove?", "opts": ["Skin", "Seeds and stems", "Nothing"], "a": "Seeds and stems"}
            ],
            "icon": "🍯", "desc": "High pectin, good for setting.", "diff": 3
        },
        {
            "name": "Wood Ear Stir-fry",
            "ingredients": {"Wood Ear": 10, "Oil": 1},
            "prep_questions": [
                {"q": "Where does it grow?", "opts": ["Ground", "Elder trees", "Pine trees"], "a": "Elder trees"},
                {"q": "Texture?", "opts": ["Soft", "Jelly/Rubbery", "Crunchy"], "a": "Jelly/Rubbery"},
                {"q": "Must be cooked?", "opts": ["Yes", "No", "Only if old"], "a": "Yes"}
            ],
            "icon": "🥡", "desc": "Jelly fungus.", "diff": 3
        },
        {
            "name": "Morel Risotto",
            "ingredients": {"Morel": 10, "Rice": 1},
            "prep_questions": [
                {"q": "Cap texture?", "opts": ["Smooth", "Honeycomb pits", "Wrinkled brain"], "a": "Honeycomb pits"},
                {"q": "Inside?", "opts": ["Solid", "Chambered", "Hollow"], "a": "Hollow"},
                {"q": "Danger lookalike?", "opts": ["True Morel", "False Morel", "Chanterelle"], "a": "False Morel"}
            ],
            "icon": "🍚", "desc": "Spring delicacy.", "diff": 3
        },
        {
            "name": "Burdock Root Stew",
            "ingredients": {"Burdock (Root)": 10, "Water": 1},
            "prep_questions": [
                {"q": "Which root to dig?", "opts": ["Flowering plant", "First year plant", "Any"], "a": "First year plant"},
                {"q": "Legal issue?", "opts": ["None", "Uprooting illegal without permission", "Poisonous"], "a": "Uprooting illegal without permission"},
                {"q": "Taste?", "opts": ["Sweet", "Earthy/Artichoke", "Bitter"], "a": "Earthy/Artichoke"}
            ],
            "icon": "🍲", "desc": "Requires digging.", "diff": 3
        },
        {
            "name": "Wood Blewit Stew",
            "ingredients": {"Wood Blewit": 10, "Butter": 1},
            "prep_questions": [
                {"q": "Color?", "opts": ["White", "Lilac/Purple", "Yellow"], "a": "Lilac/Purple"},
                {"q": "Habitat?", "opts": ["Grass", "Wood/Leaves", "Sand"], "a": "Wood/Leaves"},
                {"q": "Danger lookalike?", "opts": ["Lilac Fibrecap", "Amethyst Deceiver", "Field Mushroom"], "a": "Lilac Fibrecap"}
            ],
            "icon": "🍄", "desc": "Late autumn mushroom.", "diff": 3
        },
        {
            "name": "Cockles in Vinegar",
            "ingredients": {"Cockles": 20, "Vinegar": 1},
            "prep_questions": [
                {"q": "Shell shape?", "opts": ["Smooth", "Ribbed/Ridged", "Spiral"], "a": "Ribbed/Ridged"},
                {"q": "Safety check?", "opts": ["Red tide/Pollution", "Size", "Color"], "a": "Red tide/Pollution"},
                {"q": "Cooking?", "opts": ["Eat raw", "Steam until open", "Fry"], "a": "Steam until open"}
            ],
            "icon": "🥣", "desc": "Coastal shellfish.", "diff": 3
        },
        {
            "name": "Silver Birch Sap Wine",
            "ingredients": {"Silver Birch": 10, "Sugar": 1},
            "prep_questions": [
                {"q": "How to get sap?", "opts": ["Cut leaves", "Tap tree", "Dig roots"], "a": "Tap tree"},
                {"q": "When to tap?", "opts": ["Autumn", "Spring", "Winter"], "a": "Spring"},
                {"q": "After tapping?", "opts": ["Leave open", "Plug hole", "Cut tree down"], "a": "Plug hole"}
            ],
            "icon": "🍷", "desc": "Spring sap wine.", "diff": 3
        }
    ]

    # --- HELPER FUNCTIONS ---
    def get_difficulty_stars(diff):
        return "⭐" * diff + "☆" * (3 - diff)

    # --- UI LAYOUT ---
    col_main, col_side = st.columns([2, 1])

    with col_side:
        st.markdown("### 🎒 Pantry")
        inv = st.session_state.kitchen_inventory
        
        if not inv:
            st.info("Pantry empty!")
        else:
            # Compact Grid Layout
            p_cols1, p_cols2 = st.columns(2)
            count = 0
            # Sort items alphabetically for cleaner look
            sorted_items = sorted(inv.items())
            
            for item, qty in sorted_items:
                if qty <= 0: continue
                # Display logic
                line = f"**{item}**: {qty}"
                if count % 2 == 0:
                    p_cols1.markdown(line)
                else:
                    p_cols2.markdown(line)
                count += 1
            
            st.markdown("---")
            st.markdown("### 🔧 Basics")
            st.markdown("_Water, Sugar, Oil, Rice, Butter, Eggs, Vinegar, Alcohol are unlimited._")

    with col_main:
        st.markdown("### 📖 Recipe Book")
        
        r1, r2, r3 = st.tabs(["⭐ Beginner", "⭐⭐ Intermediate", "⭐⭐⭐ Advanced"])
        
        def render_recipe_tab(recipe_list, container):
            for recipe in recipe_list:
                with container:
                    is_unlocked = recipe['name'] in st.session_state.unlocked_recipes
                    has_ingredients = all(st.session_state.kitchen_inventory.get(ing, 0) >= qty for ing, qty in recipe['ingredients'].items() if ing not in ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"])
                    
                    # Header
                    with st.expander(f"{recipe['icon']} {recipe['name']} - {get_difficulty_stars(recipe['diff'])}"):
                        st.markdown(f"**{recipe['desc']}**")
                        st.markdown("---")
                        
                        # Ingredients
                        st.markdown(f"**Ingredients Needed:**")
                        ing_cols = st.columns(len(recipe['ingredients']))
                        for i, (ing, qty) in enumerate(recipe['ingredients'].items()):
                            current_qty = st.session_state.kitchen_inventory.get(ing, 0)
                            status = "✅" if current_qty >= qty or ing in ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"] else "❌"
                            ing_cols[i].metric(f"{ing}", f"{current_qty}/{qty}")
                        
                        st.markdown("---")

                        # Logic
                        if not is_unlocked:
                            st.warning(f"🔒 **Preparation Required:** Answer {len(recipe['prep_questions'])} questions to unlock.")
                            
                            # Iterate through questions
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
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("One or more answers incorrect. Try again!")

                        else: # Unlocked
                            if has_ingredients:
                                st.success("✅ Ready to Cook!")
                                if st.button(f"🍳 Cook {recipe['name']}", key=f"cook_{recipe['name']}"):
                                    # Deduct Ingredients
                                    for ing, qty in recipe['ingredients'].items():
                                        if ing not in ["Water", "Sugar", "Oil", "Rice", "Butter", "Eggs", "Vinegar", "Alcohol"]:
                                            st.session_state.kitchen_inventory[ing] -= qty
                                    
                                    points = recipe['diff'] * 15
                                    st.session_state.kitchen_score += points
                                    st.toast(f"Made {recipe['name']}! +{points} XP")
                                    st.rerun()
                            else:
                                st.warning("Missing ingredients! Go foraging in Tab 1.")

        # Render Tabs
        beginner_recipes = [r for r in RECIPES if r['diff'] == 1]
        inter_recipes = [r for r in RECIPES if r['diff'] == 2]
        adv_recipes = [r for r in RECIPES if r['diff'] == 3]

        render_recipe_tab(beginner_recipes, r1)
        render_recipe_tab(inter_recipes, r2)
        render_recipe_tab(adv_recipes, r3)

        st.markdown("---")
        st.metric("🏆 Kitchen Score", st.session_state.kitchen_score)
