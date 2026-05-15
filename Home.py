import streamlit as st
from utils import init_session_state, apply_brand_theme, render_sidebar
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Rocen Homesteady",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="auto"  # CHANGED: Collapses on mobile, open on desktop
)

# --- INIT ---
init_session_state()
apply_brand_theme()
render_sidebar()

# --- HOME CONTENT ---
st.title("🌿 Rocen Homesteady")
st.markdown("### The UK's Ultimate Foraging Companion")

# --- DYNAMIC SEASONAL HOOK ---
current_month = datetime.now().strftime("%B")
# You can customize this message based on the month if you like
st.info(f"📅 **Current Season:** It is **{current_month}**. Perfect for finding Wild Garlic, Nettles, and Dandelions!")

st.markdown("---")

# --- KEY STATS ---
col1, col2, col3 = st.columns(3)
col1.metric("🌱 Plants Database", "50+")
col2.metric("⚠️ Safety Warnings", "100+")
col3.metric("🎮 Interactive Games", "5")

# --- MAIN CONTENT COLUMNS ---
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### How to Use")
    st.markdown("""
    1. **Learn:** Study plants, trees, and fungi in the **Learning** tab.
    2. **Play:** Test your skills in the **Games** section.
    3. **Track:** Check your rank and stats in the **Sidebar**.
    """)
    
    st.error("⚠️ **Safety Disclaimer**")
    st.markdown("""
    - **Identification:** Never eat a plant based solely on an app. Cross-reference with a field guide.
    - **Allergies:** Some individuals may react to edible plants. Try small amounts first.
    - **Legal:** Only pick for personal use. It is illegal to uproot plants without permission.
    """)

with right_col:
    st.markdown("### About Us")
    st.markdown("""
    **Rocen Homesteady LTD** is dedicated to reconnecting people with nature through safe, sustainable foraging education.
    
    Based in Cardiff, we provide educational tools for families, schools, and nature enthusiasts across the UK.
    """)
    
    # UPDATED: Business Email
    st.markdown("📧 [Contact Us](mailto:Maughamijelekhai@gmail.com)")

st.markdown("---")
st.caption("© 2026 Rocen Homesteady LTD. All Rights Reserved. Educational Use Only.")