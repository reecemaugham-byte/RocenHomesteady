import streamlit as st
import base64  # Added for logo CSS injection
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar
from plants_data import UK_PLANTS
from game_config import ACHIEVEMENTS

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Rocen Homesteady",
    page_icon="Blogo.png",  # 1. LOGO IN BROWSER TAB
    layout="wide",
    initial_sidebar_state="auto"
)

# --- INIT ---
init_session_state()
apply_brand_theme()

# --- 2. LOGO ABOVE SIDEBAR NAVIGATION ---
try:
    with open("Blogo.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode("utf-8")
    
    # Build the CSS string without using f-strings to avoid curly brace errors
    css_logo = """
    <style>
        /* Hide the default 'Rocen Homesteady' text title */
        [data-testid="stSidebarNav"] > span {
            display: none !important;
        }
        
        /* Add the logo image above the page links */
        [data-testid="stSidebarNav"]::before {
            content: "";
            display: block;
            margin: 20px auto 10px auto;
            width: 80%; 
            height: 120px; 
            background-image: url("data:image/png;base64,""" + logo_data + """");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }
    </style>
    """
    st.markdown(css_logo, unsafe_allow_html=True)
except FileNotFoundError:
    st.sidebar.warning("Blogo.png not found. Make sure it's in the same folder as this script.")

render_sidebar()

# --- DYNAMIC SEASONAL DATA ---
current_month = datetime.now().strftime("%B")
SEASON_MONTHS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"]
}

# Determine current season
current_season = "Winter"
for season, months in SEASON_MONTHS.items():
    if current_month in months:
        current_season = season
        break

SEASON_ICONS = {
    "Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"
}

# Find plants in season right now
plants_in_season = [p for p in UK_PLANTS['edible']
                    if current_month in p.get('months', [])]
# Sort by difficulty (easiest first)
plants_in_season.sort(key=lambda p: p.get('difficulty', 1))

# Featured poisonous plants (the ones most likely to cause harm right now)
dangerous_now = [p for p in UK_PLANTS['poisonous']
                 if current_month in p.get('months', [])]
dangerous_now.sort(key=lambda p: 0 if p.get('danger_tips', {}).get('danger_zone', '') in ['DEADLY', 'EXTREME'] else 1)

# --- GAME CURRICULUM LINKS ---
GAME_LINKS = {
    "🌿 Foraging Quest": {
        "desc": "Identify plants, learn habitats, spot dangers",
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "age": "7-11",
        "tab": "🌿 Foraging Quest"
    },
    "☠️ Survival School": {
        "desc": "Tell safe plants from dangerous ones — could save a life!",
        "curriculum": ["Sc2/1a", "PSHE/H18", "PSHE/R11"],
        "age": "7-11",
        "tab": "☠️ Survival School"
    },
    "🎲 Daily Quiz": {
        "desc": "Test your plant knowledge across 5 categories",
        "curriculum": ["Sc2/1a", "Sc2/3a", "PSHE/H18"],
        "age": "7-11",
        "tab": "🎲 Daily Quiz"
    },
    "🏘️ Eco-Village": {
        "desc": "Build a village, manage resources, survive winter",
        "curriculum": ["Ma2/1a", "Sc2/3b", "PSHE/H18"],
        "age": "9-11",
        "tab": "🏘️ Eco-Village"
    },
    "🍳 The Wild Kitchen": {
        "desc": "Learn to prepare and cook wild food safely",
        "curriculum": ["Sc2/1a", "PSHE/H18", "D&T/2a"],
        "age": "9-11",
        "tab": "🍳 The Wild Kitchen"
    },
    "🚜 Farm Games": {
        "desc": "Grow crops, raise animals, and master companion planting",
        "curriculum": ["Ma2/1a", "Sc2/3b", "Sc2/3a"],
        "age": "9-11",
        "tab": "🚜 Farm Tycoon"
    },
    "🐝 Apiary Manager": {
        "desc": "Manage beehives through the seasons, harvest honey, treat for varroa",
        "curriculum": ["Sc2/1a", "Sc2/3b", "PSHE/H18"],
        "age": "9-11",
        "tab": "🐝 Apiary Manager"
    },
    "🌱 Market Garden": {
        "desc": "Companion planting, crop rotation, and soil health",
        "curriculum": ["Sc2/3b", "Ma2/1a", "Sc2/1a"],
        "age": "9-11",
        "tab": "🌱 Market Garden"
    },
}

# ==========================================
# PAGE CONTENT
# ==========================================

# --- 3. LOGO AT TOP OF MAIN PAGE ---
st.image("Blogo.png", width=250) # You can change 250 to make it bigger/smaller
st.markdown("### The UK's Ultimate Foraging Companion")

# --- DYNAMIC SEASONAL HOOK ---
st.markdown("---")

season_emoji = SEASON_ICONS.get(current_season, "🌸")
st.markdown(f"## {season_emoji} What's in Season — {current_month}")

# Featured edible plants
col_eat1, col_eat2, col_eat3 = st.columns(3)
with col_eat1:
    if plants_in_season:
        p = plants_in_season[0]
        st.markdown(f"**🌿 {p['name']}**")
        st.caption(f"*{p.get('latin_name', '')}*")
        st.markdown(f"📖 {p.get('description', '')[:120]}...")
        st.markdown(f"⚠️ {p.get('warnings', 'Safe when identified')[:80]}")
with col_eat2:
    if len(plants_in_season) > 1:
        p = plants_in_season[1]
        st.markdown(f"**🌿 {p['name']}**")
        st.caption(f"*{p.get('latin_name', '')}*")
        st.markdown(f"📖 {p.get('description', '')[:120]}...")
        st.markdown(f"⚠️ {p.get('warnings', 'Safe when identified')[:80]}")
    else:
        st.info("More plants available in the Learning Center")
with col_eat3:
    if len(plants_in_season) > 2:
        p = plants_in_season[2]
        st.markdown(f"**🌿 {p['name']}**")
        st.caption(f"*{p.get('latin_name', '')}*")
        st.markdown(f"📖 {p.get('description', '')[:120]}...")
        st.markdown(f"⚠️ {p.get('warnings', 'Safe when identified')[:80]}")
    else:
        st.info("More plants available in the Learning Center")

st.caption(f"📊 {len(plants_in_season)} plants available this month — see the full list in the Learning Center")

# --- DANGER WARNING ---
st.markdown("---")
st.error("⚠️ **Safety First**")
st.markdown("""
- **Never eat a plant based solely on an app.** Always cross-reference with a field guide or expert.
- **If in doubt, leave it out.** This is the #1 rule of foraging.
- **UK Law:** Only pick the Four Fs (Fruit, Foliage, Flowers, Fungi) for personal use.
- **It is illegal to uproot plants** without the landowner's permission.
- **Scotland has different rules** — see our Law lesson for details.
""")

# --- SURVIVAL SCHOOL HERO ---
st.markdown("---")
st.markdown("## ☠️ Can You Tell Them Apart?")

danger1 = dangerous_now[0] if len(dangerous_now) > 0 else UK_PLANTS['poisonous'][0]
danger2 = None
safe_match = None

# Try to find the matching safe plant for the first dangerous plant
for p in UK_PLANTS['edible']:
    for la in p.get('lookalikes', []):
        if la.get('name') == danger1['name']:
            safe_match = p
            break
    if safe_match:
        break

if len(dangerous_now) > 1:
    danger2 = dangerous_now[1]

hero_col1, hero_col2 = st.columns(2)

with hero_col1:
    st.markdown(f"### {season_emoji} In Season Now")
    st.markdown(f"**{len(plants_in_season)} edible plants** are available this month.")
    if safe_match:
        st.success(f"✅ **{safe_match['name']}** is safe to eat — but watch out for its dangerous lookalike!")
    else:
        st.success(f"✅ Plants like **{plants_in_season[0]['name']}** are available now.")

with hero_col2:
    st.markdown("### ☠️ Danger This Month")
    st.error(f"☠️ **{danger1['name']}** — {danger1.get('danger_tips', {}).get('danger_zone', 'Dangerous')}")
    if danger1.get('confusion_notes'):
        st.warning(f"🔍 {danger1['confusion_notes']}")
    if danger2:
        st.error(f"☠️ **{danger2['name']}** — also dangerous this month")

if st.button("🛡️ Test Your Safety Knowledge — Go to Survival School", use_container_width=True):
        st.switch_page("pages/2_Forage.py")
if st.button("🐝 Manage Your Own Beehive — Go to Apiary Manager", use_container_width=True):
    st.switch_page("pages/5_Apiary.py")

# --- 3 FOOD GROUPS ---
st.markdown("## 🌿🏘️🚜🐝 The Food Groups")
st.markdown("*Foragers, Off-Grid Dwellers, Farmers, and Beekeepers — four paths, one goal: sustainable food.*")

group1, group2, group3, group4 = st.columns(4)

with group1:
    st.markdown("### 🌿 Foragers")
    st.markdown("""
    **Find** food in the wild.
    
    - Identify plants safely
    - Know what's in season
    - Spot dangerous lookalikes
    - Respect nature and the law
    
    *Foragers find the food that others overlook.*
    """)

with group2:
    st.markdown("### 🏘️ Off-Grid Dwellers")
    st.markdown("""
    **Preserve** food for year-round use.
    
    - Store and preserve harvests
    - Cook with wild ingredients
    - Reduce food waste
    - Live sustainably
    
    *Off-Grid Dwellers make the food last.*
    """)

with group3:
    st.markdown("### 🚜 Farmers")
    st.markdown("""
    **Grow** food on the land.
    
    - Plan crops for all seasons
    - Companion planting & rotation
    - Manage resources wisely
    - Work with nature, not against it
    
    *Farmers grow the food that sustains communities.*
    """)

with group4:
    st.markdown("### 🐝 Beekeepers")
    st.markdown("""
    **Steward** the pollinators.
    
    - Inspect hives weekly
    - Treat for varroa mites
    - Harvest honey sustainably
    - Support biodiversity
    
    *Beekeepers protect the creatures that make it all possible.*
    """)

st.info("🌿➡️🏘️➡️🚜➡️🐝 **Foragers find it. Off-Grid Dwellers preserve it. Farmers grow it. Beekeepers protect the pollinators.**")

# --- KEY STATS ---
st.markdown("---")
stat1, stat2, stat3 = st.columns(3)
stat1.metric("🌱 Plants Database", f"{len(UK_PLANTS['edible'])}+")
stat2.metric("⚠️ Safety Warnings", f"{len(UK_PLANTS['poisonous'])}+")
stat3.metric("🎮 Interactive Games", "8")

# --- GAMES WITH CURRICULUM ---
st.markdown("---")
st.markdown("## 🎮 Games & Practice")
st.markdown("*Each game links to the National Curriculum. Click a game to start learning!*")

game_cols = st.columns(3)
game_items = list(GAME_LINKS.items())

for i, (game_name, game_info) in enumerate(game_items):
    with game_cols[i % 3]:
        st.markdown(f"### {game_name}")
        st.markdown(f"*{game_info['desc']}*")
        st.caption(f"📚 Curriculum: {' | '.join(game_info['curriculum'])}")
        st.caption(f"👦 Age: {game_info['age']}")

# --- MAIN CONTENT COLUMNS ---
st.markdown("---")

left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### 📖 How to Use This App")
    st.markdown("""
    1. **Learn:** Study plants, trees, and fungi in the **Learning** section.
    2. **Play:** Test your skills in the **Games** section (6 unique games!).
    3. **Track:** Check your rank and stats in the **Sidebar**.
    
    **New?** Start with ☠️ **Survival School** — it could save your life.
    """)

with right_col:
    st.markdown("### 🏛️ UK Law & Foraging")
    st.markdown("""
    **The law is different in the UK compared to the US, EU, and Australia.**
    
    - ✅ You CAN pick the Four Fs for personal use
    - ❌ You CANNOT uproot wild plants without permission
    - ❌ You CANNOT forage on SSSIs (protected sites)
    - 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland has stronger right-to-roam laws
    
    📖 Learn the full details in our **UK Foraging Law** lesson.
    """)
    st.markdown("📧 [Contact Us](mailto:Support@RocenHomesteady.co.uk)")

st.markdown("---")
st.caption("© 2026 Rocen Homesteady LTD. All Rights Reserved. Educational Use Only. UK-specific information — check local laws for other countries.")
