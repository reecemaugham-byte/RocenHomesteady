import streamlit as st
import pandas as pd
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar
from auth import render_auth, render_logout_sidebar
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
user = render_auth()
render_logout_sidebar()
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

# --- PAGINATION KEYS ---
if 'plant_pages' not in st.session_state:
    st.session_state.plant_pages = {}

ITEMS_PER_PAGE = 12

st.title("📖 Learning Center")

# --- SEASON FILTER & KIDS MODE ---
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

if st.session_state.season_filter:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a2e1a, #243524); border: 2px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
        <span style="color: var(--green-leaf); font-weight: 600;">📅 Season Filter Active:</span>
        <span style="color: var(--cream);"> Showing plants available in <b>{st.session_state.season_filter}</b></span>
        <span style="color: var(--cream-dim); font-size: 0.85rem;"> — Click the button again to clear.</span>
    </div>
    """, unsafe_allow_html=True)

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

# --- HELPER: RENDER A PLANT CARD ---
def render_plant_card(plant, status, kids_mode, edge_tts_available, card_id="0"):
    """Render a single plant's expander card."""
    icon = "🌿" if status == "Edible" else "☠️"
    cat_badge = plant.get('category', 'Plant')
    difficulty_stars = "🌱" * plant.get('difficulty', 1)

    # Danger zone for poisonous plants
    danger_zone = ""
    if status == "Poisonous":
        danger_tips = plant.get('danger_tips', {})
        danger_zone = danger_tips.get('danger_zone', plant.get('warnings', ''))
        if 'DEADLY' in danger_zone.upper() or 'EXTREME' in danger_zone.upper():
            title_prefix = "☠️ 🔴"
        else:
            title_prefix = "☠️"
    else:
        title_prefix = icon

    title = f"{title_prefix} {plant['name']} ({cat_badge}) {difficulty_stars}"

    with st.expander(title):
        latin_name = plant.get('latin_name', 'Unknown')
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div>
                <span style="color: var(--cream); font-weight: 700; font-size: 1.1rem; font-family: 'Crimson Text', Georgia, serif;">{plant['name']}</span>
                <span style="color: var(--cream-dim); font-style: italic; font-size: 0.9rem; margin-left: 0.5rem;">{latin_name}</span>
            </div>
            <span style="background: {'#ff525220' if status == 'Poisonous' else '#4CAF5020'}; color: {'#ff5252' if status == 'Poisonous' else '#4CAF50'}; padding: 0.15rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; border: 1px solid {'#ff525250' if status == 'Poisonous' else '#4CAF5050'};">
                {status}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Quick info row
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Habitat:** {plant.get('habitat', 'Various')}")
        with c2:
            months = plant.get('months', [])
            months_str = ', '.join(months[:3]) + ('...' if len(months) > 3 else '')
            st.markdown(f"**Months:** {months_str}")
        with c3:
            st.markdown(f"**Difficulty:** {difficulty_stars}")

        # Danger level for poisonous
        if status == "Poisonous":
            danger_tips = plant.get('danger_tips', {})
            danger_zone_text = danger_tips.get('danger_zone', plant.get('warnings', 'Unknown danger level'))
            danger_colour = "#ff5252" if 'DEADLY' in danger_zone_text.upper() or 'EXTREME' in danger_zone_text.upper() else "#FF8F00"
            st.markdown(f"""
            <div style="background: {danger_colour}15; border: 1px solid {danger_colour}; border-radius: 8px; padding: 0.5rem 0.8rem; margin: 0.5rem 0;">
                <span style="color: {danger_colour}; font-weight: 700;">⚠️ Danger Level: {danger_zone_text}</span>
            </div>
            """, unsafe_allow_html=True)

        # Description
        st.markdown(plant.get('description', 'No info available.'))

        # Audio
        if edge_tts_available:
            if st.button(f"🔊 Pronounce {latin_name}", key=f"latin_btn_{card_id}"):
                with st.spinner("Generating pronunciation..."):
                    audio_file = generate_voice(latin_name)
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                    else:
                        st.warning("Could not generate audio.")

        # Identification Keys
        if 'id_keys' in plant:
            st.markdown("#### 🔎 How to Identify")
            for key, value in plant['id_keys'].items():
                st.markdown(f"- **{key}:** {value}")

        # Confusion Notes
        if 'confusion_notes' in plant and plant['confusion_notes']:
            if status == "Poisonous":
                st.markdown(f"""
                <div style="background: #2a1010; border: 1px solid #ff525240; border-radius: 8px; padding: 0.5rem 0.8rem; margin: 0.5rem 0;">
                    <span style="color: #ff5252; font-weight: 700;">⚠️ Critical ID Note:</span>
                    <span style="color: #ff8a80;">{plant['confusion_notes']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #3d2e0a; border: 1px solid #FFC10740; border-radius: 8px; padding: 0.5rem 0.8rem; margin: 0.5rem 0;">
                    <span style="color: #FFC107; font-weight: 700;">🔍 Key ID Note:</span>
                    <span style="color: var(--cream-dim);">{plant['confusion_notes']}</span>
                </div>
                """, unsafe_allow_html=True)

        # Lookalike Showdown
        if 'lookalikes' in plant and isinstance(plant['lookalikes'], list) and len(plant['lookalikes']) > 0:
            st.markdown("#### ⚠️ Lookalike Showdown")
            for lookalike in plant['lookalikes']:
                if isinstance(lookalike, dict):
                    danger = lookalike.get('danger', 'Unknown')
                    danger_icon = "☠️" if danger in ["DEADLY", "EXTREME"] else "⚠️" if danger in ["POISONOUS", "HIGH"] else "✅"
                    danger_colour = "#ff5252" if danger in ["DEADLY", "EXTREME"] else "#FF8F00" if danger in ["POISONOUS", "HIGH"] else "#4CAF50"

                    st.markdown(f"""
                    <div style="background: {danger_colour}10; border-left: 3px solid {danger_colour}; border-radius: 0 8px 8px 0; padding: 0.5rem 0.8rem; margin: 0.3rem 0;">
                        <span style="color: {danger_colour}; font-weight: 700;">{danger_icon} {lookalike['name']}</span>
                        <span style="color: var(--cream-dim);"> ({danger})</span><br>
                        <span style="color: var(--cream-dim); font-size: 0.9rem;">👉 Difference: {lookalike['diff']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Try to find the lookalike plant for comparison
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

        # Full mode: Foraging/Danger Tips
        if not kids_mode:
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

            if 'warnings' in plant and plant['warnings']:
                if status == "Poisonous":
                    st.error(f"⚠️ **Warning:** {plant['warnings']}")
                else:
                    st.warning(f"⚠️ **Caution:** {plant['warnings']}")

        # Kids mode: Key safety info only
        if kids_mode:
            st.markdown("---")
            if status == "Poisonous":
                st.markdown(f"""
                <div style="background: #2a1010; border: 2px solid #ff5252; border-radius: 10px; padding: 1rem; text-align: center;">
                    <div style="font-size: 1.5rem;">🚨</div>
                    <div style="color: #ff5252; font-weight: 700; font-size: 1.1rem;">DO NOT TOUCH OR EAT THIS PLANT</div>
                    {'<div style="color: #ff8a80; font-size: 0.9rem; margin-top: 0.3rem;">Remember: ' + plant['confusion_notes'] + '</div>' if plant.get('confusion_notes') else ''}
                </div>
                """, unsafe_allow_html=True)
            else:
                if 'warnings' in plant and plant['warnings']:
                    st.markdown(f"""
                    <div style="background: #3d2e0a; border: 1px solid #FFC107; border-radius: 10px; padding: 1rem; text-align: center;">
                        <div style="color: #FFC107; font-weight: 700;">⚠️ Important: {plant['warnings']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                if 'confusion_notes' in plant and plant['confusion_notes']:
                    st.info(f"🔍 **Remember:** {plant['confusion_notes']}")

                st.caption("*(More details available in Full Mode — uncheck Simple ID Mode)*")

# --- HELPER: GET FILTERED PLANTS ---
def get_filtered_plants(search="", season_filter=None, edible_only=False, poisonous_only=False, category=None):
    """Get plants matching the current filters."""
    if category and category in UK_PLANTS.get("categories", {}):
        plants_list = UK_PLANTS["categories"][category]
        plants_with_status = []
        for p in plants_list:
            status = "Edible" if p in UK_PLANTS["edible"] else "Poisonous"
            plants_with_status.append((status, p))
        plants = plants_with_status
    elif edible_only:
        plants = [("Edible", p) for p in UK_PLANTS["edible"]]
    elif poisonous_only:
        plants = [("Poisonous", p) for p in UK_PLANTS["poisonous"]]
    else:
        plants = [("Edible", p) for p in UK_PLANTS["edible"]] + [("Poisonous", p) for p in UK_PLANTS["poisonous"]]

    filtered = []
    for status, plant in plants:
        if search and search.lower() not in plant['name'].lower():
            continue
        if season_filter and season_filter not in plant.get('months', []):
            continue
        filtered.append((status, plant))

    return filtered

# --- TABS ---
learn_tab1, learn_tab2 = st.tabs(["🌱 Plant Guide", "🎓 Learning Modules"])

# ==========================================
# SUB-TAB 1: PLANT GUIDE (PAGINATED)
# ==========================================
with learn_tab1:
    st.header("🌱 Plant Guide")

    # --- SEARCH & FILTERS ---
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("🔍 Search Plant", key="plant_search", placeholder="Type a plant name...")
    with col2:
        filter_type = st.selectbox("Type", ["All", "Edible Only", "Poisonous Only"], key="plant_type_filter")

    # --- CATEGORY TABS ---
    category_tabs = st.tabs([
        "🌿 All", "🌳 Trees", "🌱 Plants", "🍄 Fungi",
        "🏖️ Coastal", "🌲 Shrubs", "🥬 Seaweed", "🐚 Shellfish", "☠️ Poisonous"
    ])

    # --- TAB CONFIGS ---
    tab_configs = [
        ("🌿 All", None, False, False),
        ("🌳 Trees", "Tree", False, False),
        ("🌱 Plants", "Plant", False, False),
        ("🍄 Fungi", "Fungi", False, False),
        ("🏖️ Coastal", "Coastal", False, False),
        ("🌲 Shrubs", "Shrub", False, False),
        ("🥬 Seaweed", "Seaweed", False, False),
        ("🐚 Shellfish", "Shellfish", False, False),
        ("☠️ Poisonous", None, False, True),
    ]

    for tab_idx, (tab_name, category, edible_only, poisonous_only) in enumerate(tab_configs):
        with category_tabs[tab_idx]:
            # Determine filter type override for Poisonous tab
            ed_only = edible_only
            po_only = poisonous_only
            if category is None and filter_type == "Edible Only":
                ed_only = True
                po_only = False
            elif category is None and filter_type == "Poisonous Only":
                ed_only = False
                po_only = True

            filtered = get_filtered_plants(
                search=search_term,
                season_filter=st.session_state.season_filter,
                edible_only=ed_only,
                poisonous_only=po_only,
                category=category
            )

            # Count by type
            edible_count = sum(1 for s, p in filtered if s == "Edible")
            poisonous_count = sum(1 for s, p in filtered if s == "Poisonous")

            st.markdown(f"""
            <div style="display: flex; gap: 1rem; margin-bottom: 0.8rem; flex-wrap: wrap;">
                <span style="background: #4CAF5020; color: #4CAF50; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.8rem; border: 1px solid #4CAF5050;">
                    🌿 {edible_count} edible
                </span>
                <span style="background: #ff525220; color: #ff5252; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.8rem; border: 1px solid #ff525250;">
                    ☠️ {poisonous_count} poisonous
                </span>
                <span style="background: var(--bg-card); color: var(--cream-dim); padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.8rem; border: 1px solid #3d5a3d;">
                    {len(filtered)} total
                </span>
            </div>
            """, unsafe_allow_html=True)

            if not filtered:
                st.info("No plants match your filters. Try a different search or season.")
                continue

            # --- PAGINATION ---
            total_pages = max(1, (len(filtered) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
            page_key = f"plant_page_{tab_idx}"
            if page_key not in st.session_state.plant_pages:
                st.session_state.plant_pages[page_key] = 1

            current_page = st.session_state.plant_pages[page_key]
            start_idx = (current_page - 1) * ITEMS_PER_PAGE
            end_idx = start_idx + ITEMS_PER_PAGE
            page_plants = filtered[start_idx:end_idx]

            # --- RENDER PLANTS ON THIS PAGE ---
            for idx, (status, plant) in enumerate(page_plants):
                render_plant_card(plant, status, kids_mode, EDGE_TTS_AVAILABLE, card_id=f"{tab_idx}_{idx}")

            # --- PAGE NAVIGATION ---
            if total_pages > 1:
                nav_cols = st.columns([1, 2, 1])
                with nav_cols[0]:
                    if st.button("⬅️ Previous", key=f"prev_{tab_idx}", disabled=current_page <= 1):
                        st.session_state.plant_pages[page_key] = current_page - 1
                        st.rerun()
                with nav_cols[1]:
                    st.caption(f"Page {current_page} of {total_pages} ({len(filtered)} plants)")
                with nav_cols[2]:
                    if st.button("Next ➡️", key=f"next_{tab_idx}", disabled=current_page >= total_pages):
                        st.session_state.plant_pages[page_key] = current_page + 1
                        st.rerun()

    # --- PLANT COUNT SUMMARY ---
    st.markdown("---")
    total_edible = len(UK_PLANTS['edible'])
    total_poisonous = len(UK_PLANTS['poisonous'])

    st.markdown(f"""
    <div style="display: flex; gap: 1.5rem; justify-content: center; margin: 1rem 0; flex-wrap: wrap;">
        <span style="background: #4CAF5020; color: #4CAF50; padding: 0.3rem 1rem; border-radius: 20px; border: 1px solid #4CAF5050;">
            🌿 {total_edible} Edible Plants
        </span>
        <span style="background: #ff525220; color: #ff5252; padding: 0.3rem 1rem; border-radius: 20px; border: 1px solid #ff525250;">
            ☠️ {total_poisonous} Poisonous Plants
        </span>
        <span style="background: var(--bg-card); color: var(--cream-dim); padding: 0.3rem 1rem; border-radius: 20px; border: 1px solid #3d5a3d;">
            📊 {total_edible + total_poisonous} Total
        </span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# SUB-TAB 2: LEARNING MODULES
# ==========================================
with learn_tab2:
    st.header("🎓 Learning Modules")
    st.caption("Structured learning paths for UK foraging")

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

    st.markdown(f"""
    <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div>
                <span style="color: var(--amber); font-weight: 700; font-size: 1.1rem;">{current_rank_icon} {st.session_state.player_title}</span>
            </div>
            <div>
                <span style="color: var(--cream-dim); font-size: 0.85rem;">Next: {next_rank} at {next_rank_xp} XP</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress_to_next, text=f"{st.session_state.total_xp} / {next_rank_xp} XP to {next_rank}")

    # --- MODULE LIST ---
    modules = {
        "🌱 Beginner": ["Introduction to Foraging", "Easy Plants to Identify", "The Carrot Family", "The Cabbage Family"],
        "🌲 Intermediate": ["Mushroom Foraging", "The Law of the Land"],
        "🏖️ Specialist": ["The Coastal Code", "Winter Foraging"]
    }

    for level, module_list in modules.items():
        st.markdown(f"""
        <div style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; font-size: 1.3rem; font-weight: 700; margin: 1.5rem 0 0.5rem 0;">
            {level}
        </div>
        """, unsafe_allow_html=True)

        for title in module_list:
            if title in LESSON_CONTENT:
                data = LESSON_CONTENT[title]
                is_completed = title in st.session_state.completed_modules
                completion_icon = "✅" if is_completed else "📖"

                with st.expander(f"{completion_icon} {title}"):
                    # Curriculum tags
                    if 'curriculum' in data:
                        curriculum_text = " | ".join(data['curriculum'])
                        st.caption(f"📚 Curriculum: {curriculum_text}")
                    if 'ks2_age' in data:
                        st.caption(f"👦 Recommended Age: {data['ks2_age']}")

                    # Interactive engine
                    if "steps" in data:
                        total_steps = len(data['steps'])
                        progress_key = f"module_progress_{title}"
                        current_step_idx = st.session_state[progress_key]

                        # Show completion message if module already done
                        if is_completed and current_step_idx == 0:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 2px solid var(--green-leaf); border-radius: 10px; padding: 1rem; text-align: center;">
                                <span style="color: var(--green-leaf); font-weight: 700;">✅ Module Completed!</span>
                                <span style="color: var(--cream-dim); font-size: 0.9rem;"> You earned {data['steps'][-1].get('reward', 20)} XP. Click to review.</span>
                            </div>
                            """, unsafe_allow_html=True)

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
                                    st.markdown(f"""
                                    <div class="correct-feedback">
                                        <div style="color: var(--green-leaf); font-weight: 700;">✅ Correct!</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.session_state[progress_key] += 1
                                    st.rerun()
                                else:
                                    st.markdown(f"""
                                    <div class="wrong-feedback">
                                        <div style="color: var(--danger); font-weight: 700;">❌ Incorrect</div>
                                        <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">The answer was: **{step['answer']}**</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                        elif step['type'] == 'plant_card':
                            plant_name = step['plant_name']
                            plant_data = next((p for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']
                                              if p['name'] == plant_name), None)
                            if plant_data:
                                st.markdown(f"#### 🌿 Featured Plant: {plant_name}")

                                if 'id_keys' in plant_data:
                                    st.markdown("**How to Identify:**")
                                    for k, v in plant_data['id_keys'].items():
                                        st.markdown(f"- **{k}:** {v}")

                                st.markdown(f"**Habitat:** {plant_data.get('habitat', 'Various')}")
                                st.markdown(f"**Warning:** {plant_data.get('warnings', 'None')}")
                                st.markdown(plant_data.get('description', ''))

                                if 'lookalikes' in plant_data and plant_data['lookalikes']:
                                    st.markdown("**⚠️ Lookalikes:**")
                                    for la in plant_data['lookalikes']:
                                        if isinstance(la, dict):
                                            danger = la.get('danger', 'Unknown')
                                            st.markdown(f"- **{la['name']}** ({danger}): {la['diff']}")

                                if 'confusion_notes' in plant_data and plant_data['confusion_notes']:
                                    st.warning(f"🔍 **Key ID Note:** {plant_data['confusion_notes']}")

                            else:
                                st.warning(f"Plant {plant_name} not found in database.")

                            if st.button("Next ➡️", key=f"next_plant_{title}_{current_step_idx}"):
                                st.session_state[progress_key] += 1
                                st.rerun()

                        elif step['type'] == 'final_quiz':
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 2px solid var(--green-leaf); border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;">
                                <div style="font-size: 2rem;">🏁</div>
                                <div style="color: var(--green-leaf); font-family: 'Crimson Text', Georgia, serif; font-size: 1.3rem; font-weight: 700;">Module Complete!</div>
                                <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">Take this final quiz to finish the module.</div>
                            </div>
                            """, unsafe_allow_html=True)

                            user_ans = st.radio(step['question'], step['options'], key=f"final_{title}")
                            if st.button("Finish Module", key=f"finish_{title}"):
                                if user_ans == step['answer']:
                                    st.balloons()

                                    xp_reward = step.get('reward', 20)
                                    st.session_state.total_xp += xp_reward

                                    if title not in st.session_state.completed_modules:
                                        st.session_state.completed_modules.append(title)

                                    # Rank Up Logic
                                    current_xp = st.session_state.total_xp
                                    if current_xp >= 300:
                                        st.session_state.player_title = "Master Forager"
                                    elif current_xp >= 150:
                                        st.session_state.player_title = "Expert Gatherer"
                                    elif current_xp >= 50:
                                        st.session_state.player_title = "Junior Forager"
                                    else:
                                        st.session_state.player_title = "Novice Gatherer"

                                    st.markdown(f"""
                                    <div class="correct-feedback">
                                        <div style="color: var(--green-leaf); font-family: 'Crimson Text', Georgia, serif; font-size: 1.3rem; font-weight: 700;">Module Completed!</div>
                                        <div style="color: var(--cream); font-size: 0.95rem; margin-top: 0.3rem;">You earned <b>{xp_reward} XP</b>. Total: {st.session_state.total_xp} XP</div>
                                        <div style="color: var(--amber); font-size: 0.9rem; margin-top: 0.3rem;">📊 Rank: {st.session_state.player_title}</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    st.session_state[progress_key] = 0
                                else:
                                    st.markdown(f"""
                                    <div class="wrong-feedback">
                                        <div style="color: var(--danger); font-weight: 700;">Incorrect</div>
                                        <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">The correct answer was: **{step['answer']}**. Try again!</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                    else:
                        # Old format fallback
                        st.markdown(data.get('text', 'No content.'))
                        st.markdown("### 📝 Quiz")
                        q = data.get('quiz', {})
                        if q:
                            user_ans = st.radio(q.get('question', ''), q.get('options', []), key=f"radio_{title}")
                            if st.button("Submit Answer", key=f"submit_{title}"):
                                if user_ans == q.get('answer'):
                                    st.markdown(f"""
                                    <div class="correct-feedback">
                                        <div style="color: var(--green-leaf); font-weight: 700;">✅ Correct!</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.balloons()
                                    if title not in st.session_state.completed_modules:
                                        st.session_state.completed_modules.append(title)
                                        st.session_state.total_xp += 10
                                else:
                                    st.markdown(f"""
                                    <div class="wrong-feedback">
                                        <div style="color: var(--danger); font-weight: 700;">❌ Incorrect</div>
                                        <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">The correct answer was: **{q.get('answer')}**.</div>
                                    </div>
                                    """, unsafe_allow_html=True)
            else:
                st.warning(f"Content for '{title}' coming soon.")
