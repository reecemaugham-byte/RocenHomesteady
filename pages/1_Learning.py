import streamlit as st
import pandas as pd
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar
from plants_data import UK_PLANTS
from game_config import ACHIEVEMENTS
from lessons_data import LESSON_CONTENT
from audio_utils import generate_voice, clean_text_for_audio, is_tts_available

# --- TTS CHECK ---
EDGE_TTS_AVAILABLE = is_tts_available()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Learning - Rocen Homesteady",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- INIT ---
init_session_state()
apply_brand_theme()
render_sidebar()

# --- ENSURE PROGRESS KEYS EXIST ---
if 'completed_modules' not in st.session_state:
    st.session_state.completed_modules = []
if 'total_xp' not in st.session_state:
    st.session_state.total_xp = 0
if 'player_title' not in st.session_state:
    st.session_state.player_title = "Novice Gatherer"
if 'season_filter' not in st.session_state:
    st.session_state.season_filter = None

# --- MODULE PROGRESS KEYS ---
for title in LESSON_CONTENT.keys():
    progress_key = f"module_progress_{title}"
    if progress_key not in st.session_state:
        st.session_state[progress_key] = 0

st.title("📖 Learning Center")

# --- FEATURE: IN SEASON NOW & KIDS MODE ---
current_month = datetime.now().strftime("%B")

col_season, col_mode = st.columns(2)
with col_season:
    if st.button(f"📅 What's in Season Now? ({current_month})", use_container_width=True):
        if st.session_state.season_filter == current_month:
            st.session_state.season_filter = None
        else:
            st.session_state.season_filter = current_month
with col_mode:
    kids_mode = st.checkbox("🧒 Simple ID Mode (Key Safety Info Only)", value=False)

# --- SEASON FILTER STATUS ---
if st.session_state.season_filter:
    st.info(f"📅 **Season Filter Active:** Showing plants available in **{st.session_state.season_filter}**. Click the button again to clear.")
    if st.button("❌ Clear Season Filter"):
        st.session_state.season_filter = None
        st.rerun()

st.markdown("---")

# --- XP & RANK DISPLAY ---
rank_colors = {
    "Novice Gatherer": "🟤",
    "Junior Forager": "🔵",
    "Expert Gatherer": "🟣",
    "Master Forager": "🟡"
}
current_rank_icon = rank_colors.get(st.session_state.player_title, "🟤")
st.sidebar.metric("📊 XP", f"{st.session_state.total_xp}")
st.sidebar.metric(f"{current_rank_icon} Rank", st.session_state.player_title)
if st.session_state.completed_modules:
    st.sidebar.caption(f"📚 Modules: {len(st.session_state.completed_modules)}/{len(LESSON_CONTENT)}")

# --- TABS ---
learn_tab1, learn_tab2 = st.tabs(["🌱 Plant Guide", "🎓 Learning Modules"])

# ==========================================
# SUB-TAB 1: PLANT GUIDE
# ==========================================
with learn_tab1:
    # Filter Logic
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Search Plant")
    with col2:
        filter_type = st.selectbox("Type", ["All", "Edible Only", "Poisonous Only"])
    with col3:
        categories = ["All", "Plant", "Tree", "Shrub", "Fungi", "Coastal", "Seaweed", "Shellfish"]
        category_filter = st.selectbox("Category", categories)

    # Build plant list
    plants = []
    if filter_type == "Edible Only":
        plants = [("Edible", p) for p in UK_PLANTS["edible"]]
    elif filter_type == "Poisonous Only":
        plants = [("Poisonous", p) for p in UK_PLANTS["poisonous"]]
    else:
        plants = [("Edible", p) for p in UK_PLANTS["edible"]] + [("Poisonous", p) for p in UK_PLANTS["poisonous"]]

    # Apply filters
    filtered_plants = []
    for status, plant in plants:
        if search_term and search_term.lower() not in plant['name'].lower():
            continue
        if category_filter != "All" and plant.get('category', 'Plant') != category_filter:
            continue
        if st.session_state.season_filter:
            if st.session_state.season_filter not in plant.get('months', []):
                continue
        filtered_plants.append((status, plant))

    st.caption(f"Showing {len(filtered_plants)} plants")

    for status, plant in filtered_plants:
        # Determine Icon and danger level
        icon = "🌿" if status == "Edible" else "☠️"
        cat_badge = plant.get('category', 'Plant')
        difficulty_stars = "🌱" * plant.get('difficulty', 1)

        # Build expander title
        title = f"{icon} {plant['name']} ({cat_badge}) {difficulty_stars}"

        # Highlight poisonous plants
        if status == "Poisonous":
            danger = plant.get('danger_tips', {}).get('danger_zone', plant.get('warnings', ''))
            if 'DEADLY' in danger.upper() or 'EXTREME' in danger.upper():
                title = f"☠️ 🔴 {plant['name']} — DEADLY"

        with st.expander(title):
            # Header Info
            latin_name = plant.get('latin_name', 'Unknown')
            st.markdown(f"**Latin Name:** *{latin_name}*")

             if EDGE_TTS_AVAILABLE:
                if st.button(f"🔊 Pronounce {latin_name}", key=f"latin_btn_{plant['name']}"):
                    with st.spinner("Generating pronunciation..."):
                        audio_file = generate_voice(latin_name)
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
                        else:
                            st.warning("Could not generate audio.")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Habitat:** {plant.get('habitat', 'Various')}")
            with c2:
                st.markdown(f"**Months:** {', '.join(plant.get('months', []))}")
            with c3:
                st.markdown(f"**Difficulty:** {'🌱' * plant.get('difficulty', 1)}")

            if status == "Poisonous":
                danger_tips = plant.get('danger_tips', {})
                danger_zone = danger_tips.get('danger_zone', plant.get('warnings', 'Unknown danger level'))
                st.error(f"⚠️ **Danger Level:** {danger_zone}")

            # Description
            st.markdown(plant.get('description', 'No info available.'))

            # --- ALWAYS SHOW: Identification Keys ---
            if 'id_keys' in plant:
                st.markdown("#### 🔎 How to Identify")
                for key, value in plant['id_keys'].items():
                    st.markdown(f"- **{key}:** {value}")

            # --- ALWAYS SHOW: Confusion Notes (Critical Safety Info) ---
            if 'confusion_notes' in plant and plant['confusion_notes']:
                if status == "Poisonous":
                    st.error(f"⚠️ **Critical ID Note:** {plant['confusion_notes']}")
                else:
                    st.warning(f"🔍 **Key ID Note:** {plant['confusion_notes']}")

            # --- ALWAYS SHOW: Lookalike Showdown ---
            if 'lookalikes' in plant and isinstance(plant['lookalikes'], list) and len(plant['lookalikes']) > 0:
                st.markdown("#### ⚠️ Lookalike Showdown")

                for lookalike in plant['lookalikes']:
                    if isinstance(lookalike, dict):
                        danger = lookalike.get('danger', 'Unknown')
                        danger_icon = "☠️" if danger in ["DEADLY", "EXTREME"] else "⚠️" if danger in ["POISONOUS", "HIGH"] else "✅"
                        st.markdown(f"**{danger_icon} {lookalike['name']}** ({danger})")
                        st.markdown(f"👉 *Difference:* {lookalike['diff']}")

                        # Try to find the lookalike plant in the database for comparison
                        lookalike_data = None
                        for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']:
                            if p['name'] == lookalike['name']:
                                lookalike_data = p
                                break

                        if lookalike_data and not kids_mode:
                            with st.expander(f"🔍 Compare {lookalike['name']}"):
                                if 'id_keys' in lookalike_data:
                                    for k, v in lookalike_data['id_keys'].items():
                                        st.markdown(f"- **{k}:** {v}")
                                if 'confusion_notes' in lookalike_data and lookalike_data['confusion_notes']:
                                    st.warning(f"**Key ID Note:** {lookalike_data['confusion_notes']}")
                    else:
                        st.markdown(f"**Watch out for:** {lookalike}")

            # --- SHOW IN FULL MODE: Foraging Tips & Danger Tips ---
            if not kids_mode:
                # Foraging Tips (Edible plants)
                if status == "Edible" and 'foraging_tips' in plant:
                    st.markdown("### 🧺 Foraging Tips")
                    tips = plant['foraging_tips']
                    tips_data = {
                        "Where to find": tips.get('where', 'N/A'),
                        "Best time": tips.get('when', 'N/A'),
                        "Sustainable Pick": tips.get('sustainable', 'N/A'),
                        "⚠️ Danger Zone": tips.get('danger_zone', 'N/A')
                    }
                    df = pd.DataFrame(tips_data.items(), columns=["Tip", "Details"])
                    st.table(df)

                # Danger Tips (Poisonous plants)
                if status == "Poisonous" and 'danger_tips' in plant:
                    st.markdown("### ☠️ Danger Details")
                    danger_tips = plant['danger_tips']
                    danger_data = {
                        "Where found": danger_tips.get('where', 'N/A'),
                        "When dangerous": danger_tips.get('when', 'N/A'),
                        "What to do": danger_tips.get('sustainable', 'Check immediately'),
                        "⚠️ Danger Zone": danger_tips.get('danger_zone', 'Unknown')
                    }
                    df = pd.DataFrame(danger_data.items(), columns=["Info", "Details"])
                    st.table(df)

                # Warnings
                if 'warnings' in plant and plant['warnings']:
                    if status == "Poisonous":
                        st.error(f"⚠️ **Warning:** {plant['warnings']}")
                    else:
                        st.warning(f"⚠️ **Caution:** {plant['warnings']}")

            # --- KIDS MODE: Show key safety info ---
            if kids_mode:
                st.markdown("---")
                if status == "Poisonous":
                    st.error("🚨 **DO NOT TOUCH OR EAT THIS PLANT**")
                    if 'confusion_notes' in plant and plant['confusion_notes']:
                        st.error(f"**Remember:** {plant['confusion_notes']}")
                else:
                    if 'warnings' in plant and plant['warnings']:
                        st.warning(f"⚠️ **Important:** {plant['warnings']}")
                    if 'confusion_notes' in plant and plant['confusion_notes']:
                        st.info(f"🔍 **Remember:** {plant['confusion_notes']}")

                st.caption("*(More details available in Full Mode — uncheck Simple ID Mode)*")

    # Plant count summary
    st.markdown("---")
    edible_count = len(UK_PLANTS['edible'])
    poison_count = len(UK_PLANTS['poisonous'])
    st.caption(f"📊 Database: {edible_count} edible plants, {poison_count} poisonous plants")

# ==========================================
# SUB-TAB 2: LEARNING MODULES
# ==========================================
with learn_tab2:
    st.header("🎓 Learning Modules")
    st.markdown("### Structured learning paths for UK foraging")

    # --- XP & PROGRESS BAR ---
    xp_for_junior = 50
    xp_for_expert = 150
    xp_for_master = 300

    next_rank = "Junior Forager"
    next_rank_xp = xp_for_junior
    if st.session_state.total_xp >= xp_for_junior:
        next_rank = "Expert Gatherer"
        next_rank_xp = xp_for_expert
    if st.session_state.total_xp >= xp_for_expert:
        next_rank = "Master Forager"
        next_rank_xp = xp_for_master

    progress_to_next = min(1.0, st.session_state.total_xp / next_rank_xp) if next_rank_xp > 0 else 0
    st.progress(progress_to_next, text=f"{current_rank_icon} {st.session_state.player_title} — {st.session_state.total_xp} XP (Next: {next_rank} at {next_rank_xp} XP)")

    # --- MODULE LIST ---
    modules = {
        "🌱 Beginner": ["Introduction to Foraging", "Easy Plants to Identify", "The Carrot Family", "The Cabbage Family"],
        "🌲 Intermediate": ["Mushroom Foraging", "The Law of the Land"],
        "🏖️ Specialist": ["The Coastal Code", "Winter Foraging"]
    }

    for level, module_list in modules.items():
        st.markdown(f"### {level}")
        for title in module_list:
            if title in LESSON_CONTENT:
                data = LESSON_CONTENT[title]
                is_completed = title in st.session_state.completed_modules
                completion_icon = " ✅" if is_completed else ""

                with st.expander(f"📚 {title}{completion_icon}"):
                    # --- CURRICULUM TAGS ---
                    if 'curriculum' in data:
                        curriculum_text = " | ".join(data['curriculum'])
                        st.caption(f"📚 Curriculum: {curriculum_text}")
                    if 'ks2_age' in data:
                        st.caption(f"👦 Recommended Age: {data['ks2_age']}")

                    # --- NEW INTERACTIVE ENGINE ---
                    if "steps" in data:
                        total_steps = len(data['steps'])
                        progress_key = f"module_progress_{title}"
                        current_step_idx = st.session_state[progress_key]

                        # Show completion message if module already done
                        if is_completed and current_step_idx == 0:
                            st.info(f"✅ You've completed this module! You earned **{data['steps'][-1].get('reward', 20)} XP**. Click to review.")

                        # Progress Bar
                        st.progress((current_step_idx + 1) / total_steps,
                                    text=f"Step {current_step_idx + 1} of {total_steps}")

                        # Render current step
                        step = data['steps'][current_step_idx]

                        if step['type'] == 'text':
                            st.markdown(step['content'])
                            if current_step_idx < total_steps - 1:
                                if st.button("Next ➡️", key=f"next_{title}_{current_step_idx}"):
                                    st.session_state[progress_key] += 1
                                    st.rerun()
                            else:
                                st.caption("End of content. Complete the quiz to finish!")

                        elif step['type'] == 'quiz':
                            st.markdown("#### ❓ Quick Check")
                            ans = st.radio(step['question'], step['options'], key=f"quiz_{title}_{current_step_idx}")
                            if st.button("Check Answer", key=f"check_{title}_{current_step_idx}"):
                                if ans == step['answer']:
                                    st.success(step.get('feedback', "Correct!"))
                                    st.session_state[progress_key] += 1
                                    st.rerun()
                                else:
                                    st.error(f"Incorrect. The answer was: **{step['answer']}**")

                        elif step['type'] == 'plant_card':
                            plant_name = step['plant_name']
                            plant_data = next((p for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']
                                              if p['name'] == plant_name), None)
                            if plant_data:
                                st.markdown(f"#### 🌿 Featured Plant: {plant_name}")

                                # Show key identification features
                                if 'id_keys' in plant_data:
                                    st.markdown("**How to Identify:**")
                                    for k, v in plant_data['id_keys'].items():
                                        st.markdown(f"- **{k}:** {v}")

                                st.markdown(f"**Habitat:** {plant_data.get('habitat', 'Various')}")
                                st.markdown(f"**Warning:** {plant_data.get('warnings', 'None')}")
                                st.markdown(plant_data.get('description', ''))

                                # Show lookalikes if present
                                if 'lookalikes' in plant_data and plant_data['lookalikes']:
                                    st.markdown("**⚠️ Lookalikes:**")
                                    for la in plant_data['lookalikes']:
                                        if isinstance(la, dict):
                                            danger = la.get('danger', 'Unknown')
                                            st.markdown(f"- **{la['name']}** ({danger}): {la['diff']}")

                                # Show confusion notes
                                if 'confusion_notes' in plant_data and plant_data['confusion_notes']:
                                    st.warning(f"🔍 **Key ID Note:** {plant_data['confusion_notes']}")

                            else:
                                st.warning(f"Plant {plant_name} not found in database.")

                            if st.button("Next ➡️", key=f"next_plant_{title}_{current_step_idx}"):
                                st.session_state[progress_key] += 1
                                st.rerun()

                        elif step['type'] == 'final_quiz':
                            st.markdown("## 🏁 Module Complete!")
                            st.markdown("Take this final quiz to finish the module.")
                            user_ans = st.radio(step['question'], step['options'], key=f"final_{title}")
                            if st.button("Finish Module", key=f"finish_{title}"):
                                if user_ans == step['answer']:
                                    st.balloons()

                                    # Award XP
                                    xp_reward = step.get('reward', 20)
                                    st.session_state.total_xp += xp_reward

                                    # Add to completed modules
                                    if title not in st.session_state.completed_modules:
                                        st.session_state.completed_modules.append(title)

                                    # Rank Up Logic (achievable thresholds)
                                    current_xp = st.session_state.total_xp
                                    if current_xp >= 300:
                                        st.session_state.player_title = "Master Forager"
                                    elif current_xp >= 150:
                                        st.session_state.player_title = "Expert Gatherer"
                                    elif current_xp >= 50:
                                        st.session_state.player_title = "Junior Forager"
                                    else:
                                        st.session_state.player_title = "Novice Gatherer"

                                    st.success(f"Module Completed! You earned **{xp_reward} XP**. Total: {st.session_state.total_xp} XP")
                                    st.info(f"📊 Rank: {st.session_state.player_title}")

                                    # Reset for next time
                                    st.session_state[progress_key] = 0
                                else:
                                    st.error(f"Incorrect. The correct answer was: **{step['answer']}**. Try again!")

                    else:
                        # --- OLD FORMAT (Fallback) ---
                        st.markdown(data.get('text', 'No content.'))
                        st.markdown("### 📝 Quiz")
                        q = data.get('quiz', {})
                        if q:
                            user_ans = st.radio(q.get('question', ''), q.get('options', []), key=f"radio_{title}")
                            if st.button("Submit Answer", key=f"submit_{title}"):
                                if user_ans == q.get('answer'):
                                    st.success("✅ Correct!")
                                    st.balloons()
                                    if title not in st.session_state.completed_modules:
                                        st.session_state.completed_modules.append(title)
                                        st.session_state.total_xp += 10
                                else:
                                    st.error(f"❌ Incorrect. The correct answer was: {q.get('answer')}.")
            else:
                st.warning(f"Content for '{title}' coming soon.")
