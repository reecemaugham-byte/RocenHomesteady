import streamlit as st
import random
import time
from datetime import datetime

from utils import (init_session_state, apply_brand_theme, render_sidebar,
                   generate_voice, EDGE_TTS_AVAILABLE, clean_text_for_audio,
                   generate_survival_cases, generate_foraging_question,
                   save_game, get_save_data)
from game_config import (ACHIEVEMENTS, HABITAT_ICONS, SEASON_ICONS, SEASON_MONTHS,
                         SURVIVAL_DIFFICULTY)
from plants_data import UK_PLANTS

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
    .market-box div.stButton > button { font-size: 14px !important; white-space: normal !important;
                                          height: auto !important; padding: 5px !important; }
    @media (max-width: 768px) {
        .plant-card { padding: 10px !important; }
        div.grid-game div.stButton > button { font-size: 1em !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- INIT ---
init_session_state()
apply_brand_theme()

# Initialize Achievements if not exists or empty
if 'achievements' not in st.session_state or not st.session_state.achievements:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}

# Initialize cases_solved for survival
if 'survival_cases_solved' not in st.session_state:
    st.session_state.survival_cases_solved = 0

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("🌿 **Rocen Homesteady**")
    st.markdown("---")

    unlocked_count = sum(1 for v in st.session_state.achievements.values() if v)
    total_count = len(ACHIEVEMENTS)
    st.metric("🏆 Achievements", f"{unlocked_count} / {total_count}")

    st.markdown("#### 🌿 Foraging Achievements")
    for key in ["foraging_novice", "foraging_botanist", "foraging_master"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements[key] else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("#### ☠️ Survival Achievements")
    for key in ["survival_scout", "survival_expert", "survival_detective"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements[key] else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("#### 🎲 Quiz Achievements")
    for key in ["quiz_streak", "quiz_challenger"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements[key] else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("---")
    st.caption("📚 Curriculum: Science (Plants, Seasonal Changes), PSHE (Safety)")

    # Reset Button
    st.markdown("---")
    if st.button("🔄 Reset All Games"):
        st.session_state.game_score = 0
        st.session_state.game_lives = 3
        st.session_state.game_streak = 0
        st.session_state.bonus_round = False
        st.session_state.current_question = None
        st.session_state.survival_lives = 3
        st.session_state.survival_score = 0
        st.session_state.survival_correct_count = 0
        st.session_state.survival_level = 1
        st.session_state.survival_cases_solved = 0
        st.session_state.survival_current_case = None
        st.session_state.survival_result = None
        st.session_state.survival_seen = []
        st.session_state.quiz_score = 0
        st.session_state.quiz_q_num = 0
        st.session_state.q_data = None
        st.session_state.daily_streak = 0
        st.session_state.quiz_lives_remaining = 3
        st.session_state.quiz_plants_seen = []
        st.session_state.challenge_completed = False
        st.session_state.total_plants_identified = 0
        st.session_state.player_title = "Novice Gatherer"
        st.session_state.season_badge_progress = []
        st.session_state.master_inventory = {}
        st.session_state.kitchen_inventory = {}
        st.session_state.village = None
        st.session_state.farm_game = None
        st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}
        st.session_state.unlocked_recipes = []
        st.session_state.kitchen_score = 0
        st.session_state.apiary_game = None
        st.success("All Games Reset!")
        st.rerun()

st.title("🎮 Games & Practice")

tab1, tab2, tab3 = st.tabs([
    "🌿 Foraging Quest",
    "☠️ Survival School",
    "🎲 Daily Quiz"
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
        3. Questions rotate through 6 types:
           - 🌍 **Habitat** — Where does it grow?
           - 🔍 **Identification** — What are its key features?
           - ☠️ **Lookalike** — Which is the dangerous lookalike?
           - 🍃 **Parts** — Which part can you eat?
           - 📅 **Season** — When is it best foraged?
           - ⚠️ **Warning** — Is this statement true or false?
        4. **Collect Plants:** Find unique plants to fill your Herbarium.
        5. **Bonus:** Get 5 right in a row to unlock a Bonus Question!
        """)

    st.markdown("### 🗓️ Choose a Season")
    season_cols = st.columns(4)
    seasons = ["Spring", "Summer", "Autumn", "Winter"]

    current_month = datetime.now().strftime("%B")
    default_season = "Summer"
    if current_month in SEASON_MONTHS["Spring"]:
        default_season = "Spring"
    elif current_month in SEASON_MONTHS["Summer"]:
        default_season = "Summer"
    elif current_month in SEASON_MONTHS["Autumn"]:
        default_season = "Autumn"
    else:
        default_season = "Winter"

    if 'active_season' not in st.session_state:
        st.session_state.active_season = default_season

    for i, s in enumerate(seasons):
        is_earned = s in st.session_state.season_badge_progress
        badge_txt = " 🏅" if is_earned else ""
        if season_cols[i].button(f"{SEASON_ICONS[s]} {s}{badge_txt}", key=f"season_{s}", use_container_width=True):
            st.session_state.active_season = s
            st.session_state.current_question = None
            st.rerun()

    st.info(f"**Current Season:** {st.session_state.active_season} {SEASON_ICONS[st.session_state.active_season]}")

    # --- COLLECTION TRACKER ---
    total_edible = len(UK_PLANTS['edible'])
    collection_list = list(st.session_state.master_inventory.keys())
    total_found = len(collection_list)

    st.sidebar.metric("🌿 Species Found", f"{total_found}/{total_edible}")
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
    available_plants = [p for p in UK_PLANTS["edible"]
                         if any(m in SEASON_MONTHS[active_season] for m in p.get("months", []))]

    if not available_plants:
        st.warning(f"Not much grows in {active_season}! Try another season.")
    else:
        # --- BONUS ROUND LOGIC ---
        if (st.session_state.game_streak > 0
                and st.session_state.game_streak % 5 == 0
                and not st.session_state.get('bonus_round')):
            st.session_state.bonus_round = True

        if st.session_state.get('bonus_round'):
            st.markdown("## ⚡ BONUS ROUND!")
            st.markdown("You've identified 5 plants in a row! Answer for **Double Points**.")

            bonus_plant = random.choice(available_plants)
            parts = bonus_plant.get('parts', 'Leaves')
            if isinstance(parts, str):
                parts_list = [p.strip() for p in parts.split(',')]
            else:
                parts_list = parts

            wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark"]
            wrong_options = [p for p in wrong_parts if p not in parts_list]
            bonus_options = parts_list + random.sample(wrong_options, min(2, len(wrong_options)))
            random.shuffle(bonus_options)

            q_text = f"**Bonus:** Which part of **{bonus_plant['name']}** do we usually eat?"
            ans = st.radio(q_text, bonus_options, key="bonus_q")

            if st.button("Submit Bonus", key="submit_bonus"):
                if ans in parts_list:
                    st.session_state.game_score += 20
                    st.success("🎉 Correct! +20 XP!")
                    plant_name = bonus_plant['name']
                    current_count = st.session_state.master_inventory.get(plant_name, 0)
                    st.session_state.master_inventory[plant_name] = current_count + 1
                    st.session_state.total_plants_identified += 1
                else:
                    st.error(f"Incorrect! The answer was: {', '.join(parts_list)}")
                st.session_state.bonus_round = False
                st.session_state.game_streak = 0
                st.session_state.current_question = None
                st.rerun()

        else:
            # --- STANDARD QUESTION (6 TYPES) ---
            if st.session_state.get('current_question') is None:
                plant = random.choice(available_plants)
                question_data = generate_foraging_question(plant)
                question_data['plant'] = plant
                st.session_state.current_question = question_data

            q = st.session_state.current_question

            # Visual Card Layout
            col_vis, col_quiz = st.columns([1, 1.5])

            with col_vis:
                plant_desc = q['plant'].get('description', 'No description available.')
                id_keys = q['plant'].get('id_keys', {})
                if id_keys:
                    keys_html = "<br>".join([f"<b>{k}:</b> {v}" for k, v in list(id_keys.items())[:3]])
                    desc_html = f"<p style='font-size: 0.9em; text-align: left;'>{keys_html}</p>"
                else:
                    desc_html = f"<p><i>{plant_desc[:150]}</i></p>"

                q_type_icons = {
                    'habitat': '🌍', 'identification': '🔍', 'lookalike': '☠️',
                    'parts': '🍃', 'season': '📅', 'warning': '⚠️'
                }
                q_type_names = {
                    'habitat': 'Habitat', 'identification': 'ID Check',
                    'lookalike': 'Lookalike', 'parts': 'Edible Parts',
                    'season': 'Season', 'warning': 'True/False'
                }
                q_icon = q_type_icons.get(q['type'], '🌿')
                q_name = q_type_names.get(q['type'], 'Question')

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
                st.markdown(f"**{q_icon} {q_name} Question** ({q.get('points', 10)} XP)")

                clue_text = ""
                if q['type'] == 'habitat':
                    if id_keys:
                        features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
                        clue_text = "Botanical Clue: " + "; ".join([f"{k} is {v}" for k, v in features])
                    else:
                        clue_text = f"Clue: {q['plant'].get('description', '')[:100]}..."
                elif q['type'] == 'lookalike':
                    clue_text = "⚠️ This plant has a DANGEROUS lookalike. Can you identify it?"
                elif q['type'] == 'warning':
                    clue_text = "⚠️ Safety knowledge check!"
                else:
                    if id_keys:
                        features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
                        clue_text = "Botanical Clue: " + "; ".join([f"{k} is {v}" for k, v in features])
                    else:
                        clue_text = f"Clue: {q['plant'].get('description', '')[:100]}..."

                if clue_text:
                    st.info(f"🕵️ **{clue_text}**")

                if EDGE_TTS_AVAILABLE:
                    clean_clue = clean_text_for_audio(clue_text)
                    if st.button("🔊 Listen to Clue", key=f"audio_{q['plant']['name']}"):
                        audio_bytes = generate_voice(clean_clue)
                        if audio_bytes:
                            st.audio(audio_bytes, format='audio/mp3')

                st.markdown(f"### {q['question']}")

                btn_cols = st.columns(len(q['options']))
                for i, option in enumerate(q['options']):
                    if q['type'] == 'habitat':
                        icon = HABITAT_ICONS.get(option, "❓")
                        label = f"{icon} {option}"
                    else:
                        label = f"👉 {option}"

                    if btn_cols[i].button(label, key=f"opt_{i}", use_container_width=True):
                        if option == q['correct']:
                            points = q.get('points', 10)
                            streak_bonus = st.session_state.game_streak * 2
                            total_points = points + streak_bonus
                            st.session_state.game_score += total_points
                            st.session_state.game_streak += 1
                            st.session_state.total_plants_identified += 1

                            plant_name = q['plant']['name']
                            current_count = st.session_state.master_inventory.get(plant_name, 0)
                            st.session_state.master_inventory[plant_name] = current_count + 1

                            st.success(f"✅ Correct! +{total_points} XP!")
                            st.info(f"💡 {q['explanation']}")

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
                            st.error(f"❌ Not quite! The answer was: **{q['correct']}**")
                            st.info(f"💡 {q['explanation']}")

                        st.session_state.current_question = None
                        time.sleep(0.5)
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

    # --- ACHIEVEMENT DISPLAY ---
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
# GAME TAB 2: SURVIVAL SCHOOL
# ==========================================
with tab2:
    st.header("☠️ Survival School")
    st.caption("📚 Curriculum Link: Science (Plants), PSHE (Safety)")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Read the Case File** carefully. You are looking for the **Safe** plant.
        2. **Study the Clue:** The clue gives you identifying features from the plant's real botanical data.
        3. **Check the Rule:** Each case has a key rule to help you tell safe from dangerous.
        4. **Verdict:** Click the button for the **Safe** plant.
        5. **Progress:** Solve 5 cases in a row to unlock **Level 2 (Fungi & Roots)**.
        6. **Solve 20 cases total** to earn the 🕵️ Detective badge!

        Cases are generated from real plant data — there are dozens of unique scenarios!
        """)

    if 'survival_level' not in st.session_state:
        st.session_state.survival_level = 1
    if 'survival_cases_solved' not in st.session_state:
        st.session_state.survival_cases_solved = 0

    # --- GENERATE CASES FROM PLANT DATA ---
    all_cases = generate_survival_cases()

    # Filter by current level
    if st.session_state.survival_level == 1:
        available_cases = [c for c in all_cases if c['level'] == 1]
    elif st.session_state.survival_level == 2:
        available_cases = [c for c in all_cases if c['level'] <= 2]
    else:
        available_cases = all_cases

    # Fallback if no cases at current level
    if not available_cases:
        available_cases = all_cases

    # Track which cases we've seen to avoid immediate repeats
    if 'survival_seen' not in st.session_state:
        st.session_state.survival_seen = []

    # Pick a case we haven't seen recently
    unseen_cases = [c for c in available_cases
                    if c['safe_plant'] not in st.session_state.survival_seen[-10:]]

    if not unseen_cases:
        unseen_cases = available_cases
        st.session_state.survival_seen = []

    # --- PROGRESS ---
    progress = st.session_state.survival_correct_count / 5
    st.progress(min(progress, 1.0),
                text=f"Level {st.session_state.survival_level} Progress: {st.session_state.survival_correct_count}/5 Cases")

    col1, col2, col3 = st.columns(3)
    col1.metric("❤️ Lives", "❤️" * max(0, st.session_state.survival_lives))
    col2.metric("🌟 Score", st.session_state.survival_score)
    col3.metric("🕵️ Cases Solved", st.session_state.survival_cases_solved)
    st.markdown("---")

    # --- SELECT CURRENT CASE ---
    if st.session_state.survival_current_case is None:
        chosen_case = random.choice(unseen_cases)
        st.session_state.survival_current_case = chosen_case
        st.session_state.survival_result = None
        st.session_state.survival_seen.append(chosen_case['safe_plant'])

    case = st.session_state.survival_current_case

    level_name = SURVIVAL_DIFFICULTY.get(st.session_state.survival_level, "Level 1")
    st.info(f"**{level_name}**")

    # --- DISPLAY CASE ---
    st.info("🔎 **New Case File Found!**")

    with st.container():
        st.markdown(f"**🌿 Safe Plant:** {case['safe_icon']} {case['safe_plant']}")
        st.markdown(f"**☠️ Danger Plant:** {case['danger_icon']} {case['danger_plant']}")
        st.markdown("---")
        st.markdown(f"**📍 Habitat:** {case['safe_habitat']}")
        st.markdown(f"**🔍 Your Observation:** {case['clue']}")
        st.markdown(f"**📋 Rule:** {case['rule']}")

    if EDGE_TTS_AVAILABLE:
        clean_clue = clean_text_for_audio(case['clue'])
        if st.button("🔊 Listen to Clue", key="audio_clue_btn"):
            audio_bytes = generate_voice(clean_clue)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')

    # --- VERDICT ---
    st.markdown("#### ⚠️ VERDICT: Which is the **SAFE** plant?")

    options = [
        {"name": case['safe_plant'], "icon": case['safe_icon'], "is_safe": True},
        {"name": case['danger_plant'], "icon": case['danger_icon'], "is_safe": False}
    ]
    random.shuffle(options)

    if st.session_state.survival_result is None:
        btn_col1, btn_col2 = st.columns(2)

        if btn_col1.button(f"{options[0]['icon']} {options[0]['name']}",
                           key="surv_opt_1", use_container_width=True):
            if options[0]['is_safe']:
                st.session_state.survival_result = "correct"
                st.session_state.survival_score += 20
                st.session_state.survival_correct_count += 1
                st.session_state.total_plants_identified += 1
                st.session_state.survival_cases_solved += 1

                if not st.session_state.achievements['survival_scout']:
                    st.session_state.achievements['survival_scout'] = True
                    st.toast("🏅 Achievement Unlocked: Scout!")
                if (st.session_state.survival_cases_solved >= 20
                        and not st.session_state.achievements['survival_detective']):
                    st.session_state.achievements['survival_detective'] = True
                    st.toast("🏅 Achievement Unlocked: Detective!")
            else:
                st.session_state.survival_result = "wrong"
                st.session_state.survival_lives -= 1
                st.session_state.survival_correct_count = 0
            st.rerun()

        if btn_col2.button(f"{options[1]['icon']} {options[1]['name']}",
                           key="surv_opt_2", use_container_width=True):
            if options[1]['is_safe']:
                st.session_state.survival_result = "correct"
                st.session_state.survival_score += 20
                st.session_state.survival_correct_count += 1
                st.session_state.total_plants_identified += 1
                st.session_state.survival_cases_solved += 1

                if not st.session_state.achievements['survival_scout']:
                    st.session_state.achievements['survival_scout'] = True
                    st.toast("🏅 Achievement Unlocked: Scout!")
                if (st.session_state.survival_cases_solved >= 20
                        and not st.session_state.achievements['survival_detective']):
                    st.session_state.achievements['survival_detective'] = True
                    st.toast("🏅 Achievement Unlocked: Detective!")
            else:
                st.session_state.survival_result = "wrong"
                st.session_state.survival_lives -= 1
                st.session_state.survival_correct_count = 0
            st.rerun()

    else:
        # --- SHOW RESULT ---
        if st.session_state.survival_result == "correct":
            st.success("✅ CASE SOLVED! Great work, Inspector.")
            if (st.session_state.survival_correct_count >= 5
                    and st.session_state.survival_level == 1):
                st.session_state.survival_level = 2
                st.session_state.survival_correct_count = 0
                st.markdown("# 🏆 LEVEL UP!")
                st.write("You have unlocked **Level 2: Fungi & Roots**! Cases now include harder plants and fungi.")
                if not st.session_state.achievements['survival_expert']:
                    st.session_state.achievements['survival_expert'] = True
                    st.toast("🏅 Achievement Unlocked: Graduate!")
        else:
            st.error("☠️ DANGER! That was the wrong choice.")
            st.warning(f"The safe plant was **{case['safe_plant']}**, not {case['danger_plant']}.")

        st.markdown("### 📝 Case File Analysis")
        st.markdown(case['fact'])

        # Show extra detail from plant data
        safe_plant_data = None
        for p in UK_PLANTS['edible']:
            if p['name'] == case['safe_plant']:
                safe_plant_data = p
                break

        if safe_plant_data:
            with st.expander(f"📖 Learn more about {case['safe_plant']}"):
                lookalikes = safe_plant_data.get('lookalikes', [])
                if lookalikes:
                    st.markdown("**Lookalikes:**")
                    for la in lookalikes:
                        danger = la.get('danger', 'Unknown')
                        danger_icon = "☠️" if danger in ["DEADLY", "EXTREME"] else "⚠️" if danger in ["POISONOUS", "HIGH"] else "✅"
                        st.markdown(f"- {danger_icon} **{la['name']}** ({danger}): {la['diff']}")
                warnings = safe_plant_data.get('warnings', '')
                if warnings:
                    st.markdown(f"**⚠️ Warning:** {warnings}")
                confusion = safe_plant_data.get('confusion_notes', '')
                if confusion:
                    st.markdown(f"**🔍 Key ID Note:** {confusion}")

        if st.button("📋 Next Case", key="next_case_btn"):
            st.session_state.survival_current_case = None
            st.session_state.survival_result = None
            st.rerun()

    # --- GAME OVER ---
    if st.session_state.survival_lives <= 0:
        st.markdown("## 🤕 Training Ended")
        st.markdown("Don't worry, even experts make mistakes. Review the case files and try again!")
        st.markdown(f"**Cases solved this session:** {st.session_state.survival_cases_solved}")
        if st.button("🔄 Restart Training", key="restart_survival"):
            st.session_state.survival_lives = 3
            st.session_state.survival_correct_count = 0
            st.session_state.survival_current_case = None
            st.session_state.survival_result = None
            st.session_state.survival_level = 1
            st.rerun()

    # --- ACHIEVEMENT DISPLAY ---
    st.markdown("---")
    with st.expander("🏅 Survival Achievements"):
        for key in ["survival_scout", "survival_expert", "survival_detective"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            progress = ""
            if key == "survival_scout":
                progress = "(1 case)" if st.session_state.achievements[key] else "(0/1)"
            elif key == "survival_expert":
                progress = "(Done)" if st.session_state.achievements[key] else f"({st.session_state.survival_correct_count}/5 this level)"
            elif key == "survival_detective":
                progress = "(Done)" if st.session_state.achievements[key] else f"({st.session_state.survival_cases_solved}/20 total)"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}* {progress}")

        st.caption(f"📊 {len(all_cases)} unique cases available ({len([c for c in all_cases if c['level'] == 1])} Level 1, {len([c for c in all_cases if c['level'] == 2])} Level 2, {len([c for c in all_cases if c['level'] == 3])} Level 3)")

# ==========================================
# GAME TAB 3: DAILY QUIZ
# ==========================================
with tab3:
    st.header("🎯 The Plant Challenge")
    st.caption("📚 Curriculum Link: Science (Plants), Seasonal Changes, PSHE (Safety)")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Categories:** Choose a topic (e.g., Coastal, Trees, Fungi) to focus on.
        2. **Difficulty:**
           - **Beginner:** 3 options per question
           - **Expert:** 4 options per question
        3. **Challenge Mode ⚔️:** Only 1 life! Answer 10 questions correctly to earn the Challenger badge.
        4. **Learn:** Correct answers show the plant card with extra detail.
        5. **Streak:** Build a streak for bonus points!
        """)

    # --- SETTINGS ---
    col_settings1, col_settings2, col_settings3 = st.columns(3)
    with col_settings1:
        quiz_mode = st.selectbox("📚 Category",
            ["All", "Edible Only", "Poisonous Only", "Coastal", "Trees", "Fungi", "Beginner Friendly"])
    with col_settings2:
        difficulty = st.radio("Difficulty", ["Beginner", "Expert"], horizontal=True)
    with col_settings3:
        challenge_mode = st.checkbox("⚔️ Challenge Mode (1 Life, 10 Qs)")

    # --- CHALLENGE MODE CONFIG ---
    if challenge_mode:
        num_options = 4
        max_questions = 10
        lives = 1
    else:
        num_options = 3 if difficulty == "Beginner" else 4
        max_questions = st.session_state.quiz_max
        lives = 3

    st.markdown("---")

    # --- STATS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Streak", f"{st.session_state.daily_streak} Correct")
    col2.metric("🌟 Score", st.session_state.quiz_score)
    col3.metric("❓ Question", f"{st.session_state.quiz_q_num}/{max_questions}")
    st.progress(min(st.session_state.quiz_q_num / max_questions, 1.0))

    # --- BUILD QUESTION POOL ---
    if quiz_mode == "All":
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
    elif quiz_mode == "Edible Only":
        pool = UK_PLANTS['edible']
    elif quiz_mode == "Poisonous Only":
        pool = UK_PLANTS['poisonous']
    elif quiz_mode == "Beginner Friendly":
        pool = [p for p in UK_PLANTS['edible'] if p.get('difficulty', 1) == 1]
    else:
        pool = [p for p in UK_PLANTS['edible'] if p.get('category', '') == quiz_mode]
        pool += [p for p in UK_PLANTS['poisonous'] if p.get('category', '') == quiz_mode]

    if not pool:
        st.warning("No plants found for this category. Try 'All'.")
    else:
        # Initialise lives tracker
        if 'quiz_lives_remaining' not in st.session_state:
            st.session_state.quiz_lives_remaining = lives
        if 'quiz_plants_seen' not in st.session_state:
            st.session_state.quiz_plants_seen = []

        # --- CHALLENGE MODE GAME OVER ---
        if challenge_mode and st.session_state.quiz_lives_remaining <= 0 and st.session_state.quiz_q_num > 0:
            st.error("⚔️ **Challenge Failed!** You ran out of lives.")
            st.markdown(f"**Score:** {st.session_state.quiz_score} | **Questions answered:** {st.session_state.quiz_q_num}")
            if st.button("🔄 Try Challenge Again", key="restart_challenge_fail"):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.session_state.quiz_lives_remaining = 1
                st.session_state.daily_streak = 0
                st.rerun()

        # --- REGULAR GAME OVER ---
        elif st.session_state.quiz_q_num >= max_questions:
            st.balloons()
            if challenge_mode:
                st.success("⚔️ **CHALLENGE COMPLETE!** Incredible!")
                if not st.session_state.achievements['quiz_challenger']:
                    st.session_state.achievements['quiz_challenger'] = True
                    st.toast("🏅 Achievement Unlocked: Challenger!")
            else:
                st.success("🎉 **Challenge Complete!**")

            st.metric("Final Score", st.session_state.quiz_score)

            if st.session_state.quiz_plants_seen:
                with st.expander("📖 Plants You Were Tested On"):
                    for p_name, correct in st.session_state.quiz_plants_seen:
                        icon = "✅" if correct else "❌"
                        st.write(f"{icon} {p_name}")

            if st.button("🔄 Try Again", key="restart_quiz"):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.session_state.quiz_lives_remaining = lives
                st.session_state.quiz_plants_seen = []
                st.rerun()

        # --- ACTIVE QUIZ ---
        else:
            # Show lives in non-challenge mode
            if not challenge_mode:
                st.metric("❤️ Lives", "❤️" * max(0, st.session_state.quiz_lives_remaining))

            # Generate question if needed
            if st.session_state.get('q_data') is None:
                plant = random.choice(pool)

                # Choose question type
                question_types = ['id_check', 'parts_check', 'season_check', 'lookalike_check', 'warning_check']
                q_type = random.choice(question_types)

                # Fallback for plants without necessary data
                if q_type == 'lookalike_check' and not any(
                    la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
                    for la in plant.get('lookalikes', [])
                ):
                    q_type = 'id_check'
                if q_type == 'parts_check' and not plant.get('parts'):
                    q_type = 'id_check'
                if q_type == 'warning_check' and not plant.get('warnings'):
                    q_type = 'id_check'

                question_text = ""
                correct_answer = ""
                options = []
                fun_fact = ""
                is_edible = plant in UK_PLANTS['edible']

                # --- TYPE 1: IS IT EDIBLE? ---
                if q_type == 'id_check':
                    question_text = f"Is **{plant['name']}** safe to eat?"
                    correct_answer = "Edible" if is_edible else "Poisonous"
                    options = ["Edible", "Poisonous"]
                    if is_edible:
                        fun_fact = f"✅ **{plant['name']}** is edible. {plant.get('warnings', 'Always check ID!')}"
                    else:
                        danger = plant.get('danger_tips', {})
                        danger_note = danger.get('danger_zone', plant.get('warnings', 'Extremely dangerous.'))
                        fun_fact = f"☠️ **{plant['name']}** is POISONOUS. {danger_note}"

                # --- TYPE 2: WHICH PART? ---
                elif q_type == 'parts_check':
                    edible_plant = random.choice(UK_PLANTS['edible'])
                    raw_parts = edible_plant.get('parts', 'Leaves')
                    if isinstance(raw_parts, str):
                        parts = [p.strip() for p in raw_parts.split(',')]
                    else:
                        parts = raw_parts
                    if not parts:
                        parts = ['Leaves']

                    correct_answer = parts[0]
                    wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark", "Stem"]
                    wrong_options = [p for p in wrong_parts if p not in parts]
                    question_text = f"Which part of **{edible_plant['name']}** do we usually eat?"
                    options = [correct_answer] + random.sample(wrong_options, min(num_options - 1, len(wrong_options)))
                    fun_fact = f"🍃 **{edible_plant['name']}:** Edible parts are {', '.join(parts)}. {edible_plant.get('warnings', '')}"

                # --- TYPE 3: WHEN TO HARVEST? ---
                elif q_type == 'season_check':
                    edible_plant = random.choice(UK_PLANTS['edible'])
                    correct_months = edible_plant.get('months', ['Summer'])
                    correct_answer = random.choice(correct_months)
                    all_months = ["January", "March", "June", "August", "October", "December"]
                    wrong_months = [m for m in all_months if m not in correct_months]
                    if not wrong_months:
                        wrong_months = ["January", "March", "November"]
                    question_text = f"When is **{edible_plant['name']}** best harvested?"
                    options = [correct_answer] + random.sample(wrong_months, min(num_options - 1, len(wrong_months)))
                    fun_fact = f"📅 **{edible_plant['name']}** is best in {', '.join(correct_months)}. Habitat: {edible_plant.get('habitat', 'Various')}."

                # --- TYPE 4: DANGEROUS LOOKALIKE ---
                elif q_type == 'lookalike_check':
                    dangerous_lookalikes = [
                        la for la in plant.get('lookalikes', [])
                        if la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
                    ]
                    if dangerous_lookalikes:
                        chosen = random.choice(dangerous_lookalikes)
                        correct_answer = chosen['name']
                        question_text = f"**{plant['name']}** has a dangerous lookalike. Which of these is it?"

                        other_names = [p['name'] for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']
                                      if p['name'] != plant['name'] and p['name'] != correct_answer]
                        wrong_options = random.sample(other_names, min(num_options - 1, len(other_names)))
                        options = [correct_answer] + wrong_options

                        confusion = plant.get('confusion_notes', chosen.get('diff', 'Check carefully!'))
                        fun_fact = f"☠️ **Key ID:** {confusion}"
                    else:
                        question_text = f"Is **{plant['name']}** safe to eat?"
                        correct_answer = "Edible" if is_edible else "Poisonous"
                        options = ["Edible", "Poisonous"]
                        fun_fact = plant.get('warnings', '')

                # --- TYPE 5: WARNING CHECK ---
                elif q_type == 'warning_check':
                    warning = plant.get('warnings', '')
                    if warning:
                        if random.random() < 0.6:
                            question_text = f"True or False: {warning}"
                            correct_answer = "True"
                            options = ["True", "False"]
                            fun_fact = f"✅ This is correct: {warning}"
                        else:
                            false_warning = warning
                            swaps = [
                                ("cook", "eat raw"), ("edible", "poisonous"),
                                ("safe", "dangerous"), ("must", "don't need to"),
                                ("hairy", "smooth"), ("round", "flat"),
                                ("never", "always")
                            ]
                            for orig, swap in swaps:
                                if orig.lower() in false_warning.lower():
                                    false_warning = false_warning.lower().replace(orig.lower(), swap.lower())
                                    false_warning = false_warning[0].upper() + false_warning[1:]
                                    break

                            if false_warning != warning:
                                question_text = f"True or False: {false_warning}"
                                correct_answer = "False"
                                options = ["True", "False"]
                                fun_fact = f"❌ That's FALSE. The real warning is: {warning}"
                            else:
                                question_text = f"True or False: {warning}"
                                correct_answer = "True"
                                options = ["True", "False"]
                                fun_fact = f"✅ This is correct: {warning}"
                    else:
                        question_text = f"Is **{plant['name']}** safe to eat?"
                        correct_answer = "Edible" if is_edible else "Poisonous"
                        options = ["Edible", "Poisonous"]
                        fun_fact = plant.get('warnings', '')

                # Ensure we have enough options
                while len(options) < num_options:
                    options.append("None of the above")

                random.shuffle(options)

                st.session_state.q_data = {
                    "plant": plant,
                    "text": question_text,
                    "correct": correct_answer,
                    "options": options,
                    "type": q_type,
                    "fact": fun_fact
                }

            q = st.session_state.q_data

            # Question type icons
            q_type_icons = {
                'id_check': '🔍', 'parts_check': '🍃', 'season_check': '📅',
                'lookalike_check': '☠️', 'warning_check': '⚠️'
            }
            q_type_names = {
                'id_check': 'Identification', 'parts_check': 'Edible Parts',
                'season_check': 'Season', 'lookalike_check': 'Dangerous Lookalike',
                'warning_check': 'Warning'
            }
            q_icon = q_type_icons.get(q['type'], '❓')
            q_name = q_type_names.get(q['type'], 'Question')

            st.markdown(f"### {q_icon} {q_name}")
            st.markdown(f"#### {q['text']}")

            cols = st.columns(len(q['options']))
            for i, opt in enumerate(q['options']):
                if cols[i].button(f"👉 {opt}", key=f"ans_{i}", use_container_width=True):
                    if opt == q['correct']:
                        st.session_state.quiz_score += 1
                        st.session_state.daily_streak += 1
                        st.toast(f"✅ Correct! +1 Point")

                        if 'quiz_plants_seen' in st.session_state:
                            st.session_state.quiz_plants_seen.append((q['plant']['name'], True))

                        if st.session_state.daily_streak >= 5 and not st.session_state.achievements['quiz_streak']:
                            st.session_state.achievements['quiz_streak'] = True
                            st.toast("🏅 Achievement Unlocked: Quick Wit!")

                    else:
                        st.session_state.daily_streak = 0
                        st.session_state.quiz_lives_remaining -= 1
                        st.toast(f"❌ Wrong! The answer was: {q['correct']}")

                        if 'quiz_plants_seen' in st.session_state:
                            st.session_state.quiz_plants_seen.append((q['plant']['name'], False))

                    st.session_state.quiz_q_num += 1
                    st.session_state.q_data = None
                    time.sleep(0.3)
                    st.rerun()

    # --- ACHIEVEMENT DISPLAY ---
    st.markdown("---")
    with st.expander("🏅 Quiz Achievements"):
        for key in ["quiz_streak", "quiz_challenger"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements[key] else "🔒"
            progress = ""
            if key == "quiz_streak":
                progress = f"({st.session_state.daily_streak}/5)" if not st.session_state.achievements[key] else "(Done)"
            elif key == "quiz_challenger":
                progress = "(Done)" if st.session_state.achievements[key] else "(Complete Challenge Mode)"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}* {progress}")

