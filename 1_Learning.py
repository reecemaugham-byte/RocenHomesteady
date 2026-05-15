import streamlit as st
import pandas as pd
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar, UK_PLANTS, LESSON_CONTENT, generate_voice, EDGE_TTS_AVAILABLE

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Learning - Rocen Homesteady",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
init_session_state()
apply_brand_theme()
render_sidebar()

st.title("📖 Learning Center")

# --- FEATURE: IN SEASON NOW & KIDS MODE ---
current_month = datetime.now().strftime("%B")

col_season, col_mode = st.columns(2)
with col_season:
    if st.button(f"📅 What's in Season Now? ({current_month})", use_container_width=True):
        st.session_state.season_filter = current_month

with col_mode:
    # Toggle for Kids/Simple Mode
    kids_mode = st.checkbox("🧒 Simple ID Mode (Hide Advanced Details)", value=False)

st.markdown("---")

# --- TABS ---
learn_tab1, learn_tab2 = st.tabs(["🌱 Plant Guide", "🎓 Learning Modules"])

# --- SUB-TAB 1: PLANT GUIDE ---
with learn_tab1:
    # Filter Logic
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Search Plant")
    with col2:
        filter_type = st.selectbox("Type", ["All", "Edible Only", "Poisonous Only"])
    with col3:
        # NEW: Category Filter
        categories = ["All", "Plant", "Tree", "Fungi", "Coastal", "Seaweed", "Shellfish"]
        category_filter = st.selectbox("Category", categories)

    plants = []
    if filter_type == "Edible Only":
        plants = [("Edible", p) for p in UK_PLANTS["edible"]]
    elif filter_type == "Poisonous Only":
        plants = [("Poisonous", p) for p in UK_PLANTS["poisonous"]]
    else:
        plants = [("Edible", p) for p in UK_PLANTS["edible"]] + [("Poisonous", p) for p in UK_PLANTS["poisonous"]]

    for status, plant in plants:
        # Filter Logic
        if search_term and search_term.lower() not in plant['name'].lower():
            continue
        if category_filter != "All" and plant.get('category', 'Plant') != category_filter:
            continue
        # Season Filter Logic
        if 'season_filter' in st.session_state:
            if st.session_state.season_filter not in plant.get('months', []):
                continue

        # Determine Icon
        icon = "🌿" if status == "Edible" else "☠️"
        # Category Badge
        cat_badge = plant.get('category', 'Plant')
        
        with st.expander(f"{icon} {plant['name']} ({cat_badge})"):
            # Header Info
            latin_name = plant.get('latin_name', 'Unknown')
            st.markdown(f"**Latin Name:** *{latin_name}*")
            if EDGE_TTS_AVAILABLE:
                if st.button(f"🔊 Pronounce Latin", key=f"latin_btn_{plant['name']}"):
                    with st.spinner("Generating pronunciation..."):
                        audio_file = generate_voice(latin_name.replace(" ", " "))
                        if audio_file:
                            st.audio(audio_file)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Habitat:** {plant.get('habitat', 'Various')}")
            with c2:
                st.markdown(f"**Months:** {', '.join(plant.get('months', []))}")
            with c3:
                st.markdown(f"**Difficulty:** {'🌱' * plant.get('difficulty', 1)}")
                if status == "Poisonous":
                    st.markdown(f"**Danger:** {plant.get('danger', 'Unknown')}")

            # Description
            st.markdown(plant.get('description', 'No info available.'))

            # --- KIDS MODE CHECK ---
            if not kids_mode:
                # SHOW DETAILED INFO
                
                # Foraging Tips (if available)
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

                # Identification Keys
                if 'id_keys' in plant:
                    st.markdown("#### 🔎 Identification Keys")
                    for key, value in plant['id_keys'].items():
                        st.markdown(f"- **{key}:** {value}")

                # --- LOOKALIKE SHOWDOWN TABLE ---
                if 'lookalikes' in plant and isinstance(plant['lookalikes'], list) and len(plant['lookalikes']) > 0:
                    st.markdown("#### ⚠️ Lookalike Showdown")
                    st.markdown("*Compare the safe plant with its dangerous lookalike:*")
                    
                    # Create a DataFrame for clear comparison
                    # We reconstruct the Safe Plant data for the table
                    safe_keys = plant.get('id_keys', {})
                    
                    for lookalike in plant['lookalikes']:
                        if isinstance(lookalike, dict): # New Format
                            danger_level = lookalike.get('danger', 'Unknown')
                            st.markdown(f"**Confused with:** {lookalike['name']} ({danger_level})")
                            st.markdown(f"👉 *Difference:* {lookalike['diff']}")
                            st.markdown("---")
                        else:
                            # Old format fallback
                            st.markdown(f"**Watch out for:** {lookalike}")

            else:
                # KIDS MODE: SIMPLE VIEW
                st.info("🕵️ **Quick ID:**")
                if 'id_keys' in plant:
                    # Just show the first 2 keys
                    keys = list(plant['id_keys'].items())
                    for k, v in keys[:2]:
                        st.markdown(f"✅ **{k}:** {v}")
                
                if status == "Poisonous":
                    st.error(f"⚠️ **Danger:** {plant.get('danger', 'Unknown')}")
                    st.markdown("*(Switch off 'Simple ID Mode' in the top menu to see more details)*")

    # Clear Season Filter Button
    if 'season_filter' in st.session_state:
        if st.button("Clear Season Filter"):
            del st.session_state.season_filter
            st.rerun()

# --- SUB-TAB 2: LEARNING MODULES ---
with learn_tab2:
    st.header("🎓 Learning Modules")
    st.markdown("### Structured learning paths for UK foraging")

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