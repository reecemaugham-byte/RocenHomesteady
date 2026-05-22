import streamlit as st
import random
import math

from utils import (init_session_state, apply_brand_theme, render_sidebar)
from game_config import (ACHIEVEMENTS, SEASON_ICONS, NECTAR_FLOW, HONEY_TYPES,
                         APIARY_PRODUCTS, BEEKEEPING_SEASONS, WEATHER_CHANCES, TEMP_RANGE)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Apiary Manager - Rocen Homesteady",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .bee-hive-grid div.stButton > button {
        width: 100% !important; height: 60px !important; font-size: 1.5em !important;
        border: 2px solid #444 !important; background-color: #2b2b2b !important;
        color: white !important; border-radius: 8px !important;
    }
    .bee-hive-grid div.stButton > button:hover { border-color: #FFD700 !important; }
    .frame-box {
        border: 2px solid #555; border-radius: 8px; padding: 8px; text-align: center;
        background: #1a1a1a; min-height: 80px;
    }
    .alert-box {
        border: 2px solid #FFD700; border-radius: 10px; padding: 12px;
        background: linear-gradient(145deg, #3d2e00, #1a1a00); margin: 8px 0;
    }
    .dash-metric {
        border: 1px solid #444; border-radius: 8px; padding: 10px;
        text-align: center; background: #1a1a1a;
    }
    @media (max-width: 768px) {
        .bee-hive-grid div.stButton > button { font-size: 1em !important; height: 45px !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- INIT ---
init_session_state()
apply_brand_theme()

if 'achievements' not in st.session_state or not st.session_state.achievements:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}

# --- HELPER FUNCTIONS ---
def get_month(week):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    idx = ((week - 1) % 48) // 4
    return months[idx]

def get_season(month):
    for season, months in BEEKEEPING_SEASONS.items():
        if month in months:
            return season
    return "Spring"

def get_weather(season):
    chances = WEATHER_CHANCES.get(season, WEATHER_CHANCES["Spring"])
    r = random.random()
    if r < chances["sunny"]:
        return "☀️ Sunny"
    elif r < chances["sunny"] + chances["cloudy"]:
        return "⛅ Cloudy"
    elif r < chances["sunny"] + chances["cloudy"] + chances["rainy"]:
        return "🌧️ Rainy"
    else:
        return "⛈️ Stormy"

def get_temperature(season):
    low, high = TEMP_RANGE.get(season, (10, 20))
    return random.randint(low, high)

def can_inspect(weather_str, temperature):
    """Can't inspect in rain/storms, or below 14°C"""
    if "Rainy" in weather_str or "Stormy" in weather_str:
        return False
    if temperature < 14:
        return False
    return True

def get_week_in_month(week):
    return ((week - 1) % 4) + 1

def create_hive(name="Willow"):
    return {
        'name': name,
        'queen': 'present',
        'population': 35000 + random.randint(-3000, 5000),
        'honey_frames': 5,
        'brood_frames': 4,
        'pollen_frames': 2,
        'has_super': False,
        'super_honey_frames': 0,
        'queen_cells': 0,
        'varroa_count': random.randint(1, 3),
        'treated_this_year': False,
        'fed_spring': False,
        'fed_autumn': False,
        'inspected_week': 0,
        'age_weeks': 0,
        'dead': False,
        'death_reason': '',
        'swarmed': False,
    }

# --- GAME STATE INIT ---
if st.session_state.get('apiary_game') is None:
    st.session_state.apiary_game = {
        'hives': [create_hive("Willow")],
        'week': 13,  # Start in April (week 13)
        'money': 100,
        'level': 1,
        'xp': 0,
        'inventory': {},
        'events': [],
        'weather': '☀️ Sunny',
        'temperature': 15,
        'total_harvests': 0,
        'colonies_overwintered': 0,
        'varroa_good_seasons': 0,
        'hive_names_used': ['Willow'],
    }

game = st.session_state.apiary_game

# --- MIGRATIONS ---
for key in ['total_harvests', 'colonies_overwintered', 'varroa_good_seasons', 'hive_names_used']:
    if key not in game:
        if key == 'total_harvests':
            game[key] = 0
        elif key == 'colonies_overwintered':
            game[key] = 0
        elif key == 'varroa_good_seasons':
            game[key] = 0
        elif key == 'hive_names_used':
            game[key] = ['Willow']

# --- DERIVED VALUES ---
current_month = get_month(game['week'])
current_season = get_season(current_month)
nectar_info = NECTAR_FLOW.get(current_month, {"flow": 0, "source": "None", "honey_type": None})
active_hives = [h for h in game['hives'] if not h['dead']]
total_hives = len(active_hives)

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

    st.markdown("#### 🐝 Apiary Achievements")
    for key in ["apiary_first_harvest", "apiary_overwinter", "apiary_keeper", "apiary_5_hives", "apiary_varroa"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("---")
    st.caption("📚 Curriculum: Science (Life Cycles, Ecosystems, Pollination), PSHE (Responsibility)")

# --- MAIN DISPLAY ---
st.title("🐝 Apiary Manager")
st.caption("Manage your hives through the seasons. Inspect regularly, treat for varroa, and harvest liquid gold!")

# --- GUIDE (moved to top so players read it first) ---
with st.expander("📖 Beekeeper's Guide — Read before playing!"):
    st.markdown("""
    **🖱️ Quick Start:**
    1. You start with 1 hive called "Willow" in April
    2. Click **🔍 Inspect** to check your colony
    3. Add a **Super** in spring so bees can store honey
    4. Watch for **⚠️ Queen Cells** in April–June — split or remove them!
    5. **Harvest** honey when the super is full (4+ frames)
    6. **Treat for varroa** in August or your colony may die over winter
    7. **Feed** spring and autumn syrup to keep stores up
    
    **🗓️ Seasonal Calendar:**
    | Season | Key Actions |
    |--------|------------|
    | Spring | Inspect weekly, add supers, swarm control, feed syrup |
    | Summer | Main honey flow, harvest, check for queen cells |
    | Autumn | Varroa treatment, feed heavy syrup, mouse guards |
    | Winter | Heft hives only, feed fondant if light, oxalic acid treatment |
    
    **🔍 Reading Frames:**
    | Symbol | Meaning |
    |--------|---------|
    | 🍯 Honey | Capped = ready to extract |
    | 🟡 Pollen | Different colours = different plants |
    | 🥚 Eggs | Single egg per cell = queen laying well |
    | 🟤 Capped Brood | Solid pattern = good queen |
    | ⚠️ Queen Cell | Swarm preparation! Act fast! |
    
    **🪲 Varroa Thresholds:**
    | Count/300 | Level | Action |
    |-----------|-------|--------|
    | 0–3 | ✅ Low | Monitor, no action needed |
    | 4–6 | ⚠️ Rising | Plan treatment for August |
    | 7+ | 🚨 Critical | Treat immediately! |
    
    **📈 Levels:**
    | Level | Title | Max Hives | XP |
    |-------|-------|-----------|-----|
    | 1 | Beginner | 2 | 0 |
    | 2 | Apprentice | 3 | 50 |
    | 3 | Beekeeper | 5 | 150 |
    | 4 | Master | 7 | 400 |
    | 5 | Apiarist | 10 | 800 |
    """)

st.markdown("---")

# --- TOP STATS ---
s1, s2, s3, s4, s5, s6 = st.columns(6)
s1.metric(f"{SEASON_ICONS.get(current_season, '🌸')} Season", current_season)
s2.metric("📅 Month", f"{current_month[:3]} Wk{get_week_in_month(game['week'])}")
s3.metric(f"{game['weather']}", f"{game['temperature']}°C")
s4.metric("🐝 Hives", f"{total_hives} alive")
s5.metric("💰 Money", f"£{game['money']}")
s6.metric("⭐ Level", f"{game['level']} ({game['xp']} XP)")

# --- CAN INSPECT? ---
inspect_allowed = can_inspect(game['weather'], game['temperature'])

# --- NECTAR FLOW INFO ---
if nectar_info['flow'] > 0:
    st.success(f"🌸 **Nectar Flow:** {nectar_info['source']} (Strength: {'⭐' * nectar_info['flow']})")
    if nectar_info['honey_type']:
        st.info(f"🍯 Honey type this month: **{nectar_info['honey_type']}**")
else:
    st.info("❄️ No significant nectar flow this month. Bees rely on stores.")

# --- EVENTS ---
if game['events']:
    with st.expander("📋 Recent Events", expanded=True):
        for event in game['events'][-5:]:
            st.markdown(event)
    if len(game['events']) > 5:
        st.caption(f"... and {len(game['events']) - 5} more events")

# --- SEASONAL WARNINGS ---
if current_month == "April" or current_month == "May" or current_month == "June":
    st.warning("⚠️ **Swarm Season!** Check for queen cells every week. A swarmed colony loses half its bees.")
if current_month == "August":
    st.warning("⚠️ **Varroa Treatment Month!** Apply treatment now before winter bees are raised.")
if current_season == "Winter":
    st.info("❄️ **Winter:** No inspections. Heft hives to check stores. Apply oxalic acid in December.")

st.markdown("---")

# --- MAIN TABS ---
overview_tab, inspect_tab, actions_tab, market_tab = st.tabs([
    "🏠 Apiary", "🔍 Inspect", "🛠️ Actions", "🍯 Market"
])

# ==========================================
# TAB 1: APIARY OVERVIEW
# ==========================================
with overview_tab:
    st.markdown("### 🏠 Your Apiary")

    if not active_hives:
        st.error("💀 All your colonies have died! Buy a new hive to continue.")
        if st.button("🛒 Buy New Hive (£75)", key="buy_hive_dead"):
            if game['money'] >= 75:
                game['money'] -= 75
                new_name = random.choice(["Oak", "Birch", "Hazel", "Ash", "Elm", "Rowan", "Holly", "Ivy"])
                while new_name in game.get('hive_names_used', []):
                    new_name = random.choice(["Oak", "Birch", "Hazel", "Ash", "Elm", "Rowan", "Holly", "Ivy"])
                game['hive_names_used'].append(new_name)
                game['hives'] = [create_hive(new_name)]
                game['events'] = [f"🐝 New colony '{new_name}' installed!"]
                st.rerun()
            else:
                st.error("Need £75!")
    else:
        for i, hive in enumerate(active_hives):
            weeks_since_inspection = game['week'] - hive['inspected_week']
            inspection_status = "✅ Recent" if weeks_since_inspection <= 1 else ("⚠️ Overdue" if weeks_since_inspection <= 3 else "❌ Unknown")

            with st.expander(f"🐝 {hive['name']} — Pop: {hive['population']:,} | {inspection_status}"):
                col1, col2, col3, col4 = st.columns(4)

                # Queen status
                if weeks_since_inspection <= 1:
                    queen_icon = "👑" if hive['queen'] == 'present' else ("⚠️" if hive['queen'] == 'failing' else "💀")
                    col1.metric("Queen", f"{queen_icon} {hive['queen'].title()}")
                else:
                    col1.metric("Queen", "❓ Unknown")

                # Population
                pop_label = "Strong" if hive['population'] > 40000 else ("Medium" if hive['population'] > 20000 else "Weak")
                col2.metric("Population", f"{hive['population']:,}", pop_label)

                # Stores
                total_stores = hive['honey_frames'] + (hive['super_honey_frames'] if hive['has_super'] else 0)
                stores_label = "Good" if total_stores >= 7 else ("Low" if total_stores >= 3 else "Critical")
                col3.metric("Honey Stores", f"{total_stores} frames", stores_label)

                # Varroa
                if weeks_since_inspection <= 2:
                    varroa_label = "Low" if hive['varroa_count'] <= 3 else ("⚠️ Rising" if hive['varroa_count'] <= 6 else "🚨 Critical")
                    col4.metric("Varroa", f"{hive['varroa_count']}/300", varroa_label)
                else:
                    col4.metric("Varroa", "❓ Unknown")

                # Queen cells alert
                if hive['queen_cells'] > 0 and weeks_since_inspection <= 1:
                    st.warning(f"⚠️ **{hive['queen_cells']} queen cell(s) found!** Swarm risk is HIGH. Consider splitting.")

                # Swarm warning
                if hive['population'] > 40000 and current_month in ["April", "May", "June"]:
                    st.warning("🐝 High population + swarm season = High swarm risk! Inspect weekly.")

                # Winter stores warning
                if current_season in ["Autumn", "Winter"] and total_stores < 5:
                    st.error("❄️ Stores critically low! Feed immediately or colony will starve.")

        # --- BUY HIVE ---
        st.markdown("---")
        st.markdown("#### 🛒 Buy New Hive")
        max_hives = game['level'] + 1
        hive_cost = 75

        col_cost, col_level, col_buy = st.columns(3)
        col_cost.metric("Cost", f"£{hive_cost}")
        col_level.metric("Max Hives", f"{max_hives} (Level {game['level']})")

        can_buy = game['money'] >= hive_cost and total_hives < max_hives
        if col_buy.button(f"Buy Hive (£{hive_cost})", disabled=not can_buy, key="buy_hive_main"):
            game['money'] -= hive_cost
            new_name = random.choice(["Oak", "Birch", "Hazel", "Ash", "Elm", "Rowan", "Holly", "Ivy",
                                       "Cedar", "Pine", "Maple", "Linden", "Sycamore", "Alder", "Thorn"])
            while new_name in game.get('hive_names_used', []):
                new_name += str(random.randint(2, 9))
            game['hive_names_used'].append(new_name)
            game['hives'].append(create_hive(new_name))
            game['events'].append(f"🐝 New colony '{new_name}' installed!")
            st.rerun()

# ==========================================
# TAB 2: INSPECT HIVE
# ==========================================
with inspect_tab:
    st.markdown("### 🔍 Hive Inspection")

    if not inspect_allowed:
        st.error(f"🚫 **Cannot inspect today.** Weather: {game['weather']} | Temp: {game['temperature']}°C (need ≥14°C and dry)")
        st.caption("In real beekeeping, you should only open the hive on warm, dry days to avoid chilling the brood.")
    else:
        st.success(f"✅ **Good inspection weather!** {game['weather']} | {game['temperature']}°C")

    if not active_hives:
        st.warning("No active hives to inspect.")
    else:
        hive_names = [h['name'] for h in active_hives]
        selected_name = st.selectbox("Select Hive", hive_names, key="inspect_hive_select")
        selected_hive = next((h for h in active_hives if h['name'] == selected_name), None)

        if selected_hive:
            weeks_since = game['week'] - selected_hive['inspected_week']

            if not inspect_allowed:
                st.info("❄️ You can only heft the hive (lift one side to estimate stores).")
                total_stores = selected_hive['honey_frames']
                heft = "Heavy" if total_stores >= 7 else ("About right" if total_stores >= 4 else "Light ⚠️")
                st.metric("Heft Check", heft)
                if total_stores < 4:
                    st.error("⚠️ Stores feel light! Feed fondant or syrup.")
            elif weeks_since > 0 or selected_hive['inspected_week'] == 0:
                if st.button(f"🔍 Inspect '{selected_hive['name']}'", key="do_inspect"):
                    selected_hive['inspected_week'] = game['week']
                    selected_hive['swarmed'] = False

                    if current_month in ["April", "May", "June"] and selected_hive['queen'] == 'present':
                        if selected_hive['population'] > 20000 and random.random() < 0.35:
                            selected_hive['queen_cells'] = random.randint(2, 5)
                        else:
                            selected_hive['queen_cells'] = max(0, selected_hive['queen_cells'] - 1)

                    if current_month in ["April", "May", "June", "July", "August"]:
                        if not selected_hive['treated_this_year']:
                            selected_hive['varroa_count'] = min(15, selected_hive['varroa_count'] + random.randint(0, 2))

                    game['xp'] += 2
                    st.rerun()

            if selected_hive['inspected_week'] > 0 and (game['week'] - selected_hive['inspected_week']) <= 2:
                weeks_info = game['week'] - selected_hive['inspected_week']
                st.caption(f"Last inspected {weeks_info} week(s) ago")

                st.markdown("#### 🗂️ Frame Layout")

                # Brood box
                hf = int(selected_hive['honey_frames'])
                pf = int(selected_hive['pollen_frames'])
                bf = int(selected_hive['brood_frames'])
                queen = selected_hive['queen'] == 'present'
                qc = selected_hive['queen_cells'] > 0

                brood_frames = []
                for i in range(11):
                    if i < hf:
                        brood_frames.append("🍯")
                    elif i < hf + pf:
                        brood_frames.append("🟡")
                    elif i < hf + pf + bf:
                        pos = i - hf - pf
                        if queen and pos < max(1, bf // 3):
                            brood_frames.append("🥚")
                        elif queen and pos < max(2, bf * 2 // 3):
                            brood_frames.append("🐛")
                        else:
                            brood_frames.append("🟤")
                    elif qc and i == hf + pf + bf:
                        brood_frames.append("⚠️")
                    else:
                        brood_frames.append("⬜")

                st.markdown("**Brood Box** (11 frames):")
                b_cols = st.columns(11)
                for i, frame in enumerate(brood_frames):
                    with b_cols[i]:
                        st.markdown(f"<div class='frame-box'>{frame}</div>", unsafe_allow_html=True)

                if selected_hive['has_super']:
                    sf = int(min(selected_hive['super_honey_frames'], 8))
                    super_frames = ["🍯"] * sf + ["⬜"] * (8 - sf)
                    st.markdown("**Super** (8 frames):")
                    s_cols = st.columns(8)
                    for i, frame in enumerate(super_frames):
                        with s_cols[i]:
                            st.markdown(f"<div class='frame-box'>{frame}</div>", unsafe_allow_html=True)

                if selected_hive['queen_cells'] > 0:
                    st.warning(f"⚠️ **{selected_hive['queen_cells']} Queen Cell(s) Found!** Consider splitting or removing.")
                else:
                    st.success("✅ No queen cells found.")

                st.caption("🍯 Honey | 🟡 Pollen | 🥚 Eggs | 🐛 Larvae | 🟤 Capped Brood | ⬜ Empty | ⚠️ Queen Cell")

                # Dashboard
                st.markdown("---")
                st.markdown("#### 📊 Colony Dashboard")

                d1, d2, d3, d4 = st.columns(4)
                queen_icon = {"present": "👑 Present", "failing": "⚠️ Failing", "virgin": "🐣 Virgin", "dead": "💀 No Queen"}
                d1.metric("👑 Queen", queen_icon.get(selected_hive['queen'], selected_hive['queen']))

                pop = selected_hive['population']
                pop_delta = "Strong" if pop > 40000 else ("Medium" if pop > 20000 else "Weak")
                d2.metric("🐝 Population", f"{pop:,}", pop_delta)

                varroa = selected_hive['varroa_count']
                varroa_status = "✅ Low" if varroa <= 3 else ("⚠️ Rising" if varroa <= 6 else "🚨 Critical")
                d3.metric("🪲 Varroa", f"{varroa}/300", varroa_status)

                stores = int(selected_hive['honey_frames'] + (selected_hive['super_honey_frames'] if selected_hive['has_super'] else 0))
                stores_status = "✅ Good" if stores >= 7 else ("⚠️ Low" if stores >= 4 else "🚨 Critical")
                d4.metric("🍯 Stores", f"{stores} frames", stores_status)

                # Health assessment
                st.markdown("---")
                health_issues = []
                if selected_hive['queen'] == 'failing':
                    health_issues.append("⚠️ Queen is failing — consider requeening")
                if selected_hive['queen'] == 'dead':
                    health_issues.append("🚨 No queen — colony will die without intervention")
                if selected_hive['varroa_count'] > 6:
                    health_issues.append("🚨 Varroa levels critical — treat immediately")
                elif selected_hive['varroa_count'] > 3:
                    health_issues.append(f"Varroa rising ({selected_hive['varroa_count']}/300) - treat in Aug/Sep or Dec")
                if stores < 4 and current_season in ["Autumn", "Winter"]:
                    health_issues.append("🚨 Winter stores dangerously low — feed now!")
                if selected_hive['population'] < 15000:
                    health_issues.append("⚠️ Colony is weak — may not survive winter")

                if health_issues:
                    st.error("**Health Issues:**")
                    for issue in health_issues:
                        st.markdown(f"- {issue}")
                else:
                    st.success("✅ Colony looks healthy!")

            elif selected_hive['inspected_week'] == 0:
                st.info("🔍 Click **Inspect** to check this hive.")

# ==========================================
# TAB 3: ACTIONS
# ==========================================
with actions_tab:
    st.markdown("### 🛠️ Beekeeping Actions")

    if not active_hives:
        st.warning("No active hives. Buy one from the Apiary tab.")
    else:
        hive_names = [h['name'] for h in active_hives]
        act_hive_name = st.selectbox("Select Hive", hive_names, key="act_hive_select")
        act_hive = next((h for h in active_hives if h['name'] == act_hive_name), None)

        if act_hive:
            a1, a2 = st.columns(2)

            with a1:
                st.markdown("#### 🍯 Feeding & Supers")

                # ADD SUPER
                if not act_hive['has_super']:
                    if st.button("➕ Add Super (£15)", key="add_super", disabled=current_season == "Winter"):
                        if game['money'] >= 15:
                            game['money'] -= 15
                            act_hive['has_super'] = True
                            act_hive['super_honey_frames'] = 0
                            game['events'].append(f"📦 Super added to '{act_hive['name']}'.")
                            st.rerun()
                        else:
                            st.error("Need £25!")
                else:
                    st.info("✅ Super already on hive.")

                # FEED SPRING SYRUP
                can_feed_spring = current_season == "Spring" and not act_hive['fed_spring']
                if st.button("🫗 Feed Spring Syrup (1:1) — £3", key="feed_spring",
                            disabled=not can_feed_spring):
                    if game['money'] >= 3:
                        game['money'] -= 3
                        act_hive['fed_spring'] = True
                        act_hive['honey_frames'] = min(11, act_hive['honey_frames'] + 2)
                        game['events'].append(f"🫗 Fed spring syrup to '{act_hive['name']}'. +2 frames stores.")
                        st.rerun()
                    else:
                        st.error("Need £3!")

                # FEED AUTUMN SYRUP
                can_feed_autumn = current_season == "Autumn" and not act_hive['fed_autumn']
                if st.button("🍯 Feed Autumn Syrup (2:1) — £3", key="feed_autumn",
                            disabled=not can_feed_autumn):
                    if game['money'] >= 3:
                        game['money'] -= 3
                        act_hive['fed_autumn'] = True
                        act_hive['honey_frames'] = min(11, act_hive['honey_frames'] + 3)
                        game['events'].append(f"🍯 Fed autumn syrup to '{act_hive['name']}'. +3 frames stores.")
                        st.rerun()
                    else:
                        st.error("Need £3!")

                # FEED FONDANT (Winter)
                if current_season == "Winter":
                    if st.button("🍬 Feed Fondant — £8", key="feed_fondant"):
                        if game['money'] >= 4:
                            game['money'] -= 4
                            act_hive['honey_frames'] = min(11, act_hive['honey_frames'] + 1)
                            game['events'].append(f"🍬 Fed fondant to '{act_hive['name']}'. +1 frame stores.")
                            st.rerun()
                        else:
                            st.error("Need £4!")

            with a2:
                st.markdown("#### 🛡️ Health & Swarm Control")

                # TREAT FOR VARROA
                varroa_treatable = (current_month in ["August", "September"] or current_month == "December") and not act_hive['treated_this_year']
                if varroa_treatable:
                    treatment = "Apivar Strips (£15)" if current_month in ["August", "September"] else "Oxalic Acid (£10)"
                    cost = 15 if current_month in ["August", "September"] else 10
                    if st.button(f"💊 Apply {treatment}", key="treat_varroa"):
                        if game['money'] >= cost:
                            game['money'] -= cost
                            act_hive['treated_this_year'] = True
                            act_hive['varroa_count'] = max(0, act_hive['varroa_count'] - 5)
                            game['events'].append(f"💊 Varroa treatment applied to '{act_hive['name']}'. Mites reduced.")
                            game['xp'] += 5

                            if not st.session_state.achievements.get('apiary_varroa', False):
                                st.session_state.achievements['apiary_varroa'] = True
                                st.toast("🏅 Achievement Unlocked: Mite Fighter!")

                            st.rerun()
                        else:
                            st.error(f"Need £{cost}!")
                else:
                    if act_hive['treated_this_year']:
                        st.success("✅ Already treated this year.")
                    else:
                        st.caption("Treatment in Aug/Sep (Apivar £15) or Dec (Oxalic £10). Keep advancing weeks!")

                # SPLIT COLONY (swarm control)
                can_split = (act_hive['queen_cells'] >= 2 and
                            act_hive['population'] > 20000 and
                            total_hives < game['level'] + 1 and
                            current_month in ["April", "May", "June"])
                if st.button("✂️ Split Colony (Swarm Control)", key="split_colony", disabled=not can_split):
                    # Create new hive from split
                    new_name = random.choice(["Oak", "Birch", "Hazel", "Ash", "Elm", "Rowan", "Holly", "Ivy",
                                               "Cedar", "Pine", "Maple", "Linden"])
                    while new_name in game.get('hive_names_used', []):
                        new_name += str(random.randint(2, 9))
                    game['hive_names_used'].append(new_name)

                    new_hive = create_hive(new_name)
                    new_hive['population'] = act_hive['population'] // 2
                    new_hive['queen'] = 'virgin'
                    new_hive['honey_frames'] = 4
                    new_hive['brood_frames'] = 3
                    act_hive['population'] = act_hive['population'] // 2
                    act_hive['queen_cells'] = 0

                    game['hives'].append(new_hive)
                    game['events'].append(f"✂️ Split '{act_hive['name']}' → new colony '{new_name}'!")
                    game['xp'] += 10
                    st.rerun()

                # REMOVE QUEEN CELLS (if not wanting to split)
                if act_hive['queen_cells'] > 0:
                    if st.button(f"🔪 Remove {act_hive['queen_cells']} Queen Cell(s)", key="remove_qc"):
                        act_hive['queen_cells'] = 0
                        game['events'].append(f"🔪 Queen cells removed from '{act_hive['name']}'.")
                        st.rerun()

                # REQUEEN
                if act_hive['queen'] in ['failing', 'dead']:
                    if st.button("👑 Requeen (£30)", key="requeen"):
                        if game['money'] >= 30:
                            game['money'] -= 30
                            act_hive['queen'] = 'present'
                            act_hive['population'] = max(act_hive['population'], 15000)
                            game['events'].append(f"👑 New queen introduced to '{act_hive['name']}'.")
                            game['xp'] += 5
                            st.rerun()
                        else:
                            st.error("Need £30!")

    # --- REMOVE DEAD HIVES ---
    dead_hives = [h for h in game['hives'] if h['dead']]
    if dead_hives:
        st.markdown("---")
        st.markdown("#### 🪦 Dead Colonies")
        for dh in dead_hives:
            st.error(f"**{dh['name']}** — {dh['death_reason']}")
            if st.button(f"🗑️ Remove '{dh['name']}'", key=f"remove_{dh['name']}"):
                game['hives'] = [h for h in game['hives'] if h['name'] != dh['name']]
                st.rerun()

# ==========================================
# TAB 4: HARVEST & MARKET
# ==========================================
with market_tab:
    st.markdown("### 🍯 Harvest & Market")

    hm1, hm2 = st.columns(2)

    with hm1:
        st.markdown("#### 🍯 Honey Extraction")
        harvestable = [h for h in active_hives if h['has_super'] and h['super_honey_frames'] >= 4]

        if not harvestable:
            st.info("No hives ready for harvest. Add supers and wait for the nectar flow!")
        else:
            for hive in harvestable:
                frames = hive['super_honey_frames']
                honey_type = nectar_info.get('honey_type', 'Summer Wildflower')
                honey_value = HONEY_TYPES.get(honey_type, HONEY_TYPES['Summer Wildflower'])['value'] if honey_type else HONEY_TYPES['Summer Wildflower']['value']
                jars = max(1, int(frames * 1.5))

                if st.button(f"🍯 Harvest from '{hive['name']}' ({frames} frames → ~{jars} jars of {honey_type})", key=f"harvest_{hive['name']}"):
                    honey_key = honey_type if honey_type else "Summer Wildflower"
                    game['inventory'][honey_key] = game['inventory'].get(honey_key, 0) + jars
                    game['inventory']['Beeswax'] = game['inventory'].get('Beeswax', 0) + max(1, frames // 3)

                    # Remove super
                    hive['has_super'] = False
                    hive['super_honey_frames'] = 0
                    hive['honey_frames'] = max(0, hive['honey_frames'] - 2)

                    game['total_harvests'] += 1
                    game['xp'] += 15
                    game['events'].append(f"🍯 Harvested {jars} jars of {honey_key} from '{hive['name']}'!")

                    if not st.session_state.achievements.get('apiary_first_harvest', False):
                        st.session_state.achievements['apiary_first_harvest'] = True
                        st.toast("🏅 Achievement Unlocked: First Harvest!")

                    st.rerun()

    with hm2:
        st.markdown("#### 💰 Sell Products")
        if not game['inventory']:
            st.info("Nothing to sell. Harvest honey first!")
        else:
            for item, qty in list(game['inventory'].items()):
                if qty <= 0:
                    continue
                product_data = APIARY_PRODUCTS.get(item, {'icon': '📦', 'value': 5})
                price = product_data['value']

                s1, s2 = st.columns([3, 1])
                s1.write(f"{product_data['icon']} **{item}**: {qty} jars/units")
                if s2.button(f"Sell £{price}", key=f"sell_{item}"):
                    game['money'] += price
                    game['inventory'][item] -= 1
                    if game['inventory'][item] <= 0:
                        del game['inventory'][item]
                    game['xp'] += 2
                    st.toast(f"Sold {item} for £{price}")
                    st.rerun()

    # --- INVENTORY ---
    st.markdown("---")
    st.markdown("#### 🎒 Inventory")
    if game['inventory']:
        inv_str = " | ".join([f"**{k}:** {v}" for k, v in game['inventory'].items() if v > 0])
        st.markdown(inv_str)
    else:
        st.info("Empty — harvest honey to fill your inventory!")

# ==========================================
# ADVANCE WEEK (turn-based progression)
# ==========================================
st.markdown("---")
st.info("⏰ **This game is turn-based.** Inspect your hives, take actions, then click below to advance one week.")

week_info_col1, week_info_col2 = st.columns(2)
with week_info_col1:
    st.info(f"📅 **Current:** {SEASON_ICONS.get(current_season, '🌸')} {current_season} — {current_month[:3]} Wk{get_week_in_month(game['week'])}")
with week_info_col2:
    next_month = get_month(game['week'] + 1)
    next_season = get_season(next_month)
    st.info(f"⏭️ **Next week:** {SEASON_ICONS.get(next_season, '🌸')} {next_month[:3]}")

if st.button("⏭️ Advance Week", use_container_width=True, key="advance_week"):
    game['week'] += 1
    game['events'] = []

    new_month = get_month(game['week'])
    new_season = get_season(new_month)
    new_nectar = NECTAR_FLOW.get(new_month, {"flow": 0, "source": "None", "honey_type": None})

    game['weather'] = get_weather(new_season)
    game['temperature'] = get_temperature(new_season)

    for hive in game['hives']:
        if hive['dead']:
            continue

        hive['age_weeks'] += 1

        if new_season == "Winter":
            deaths = int(hive['population'] * 0.015)
            hive['population'] = max(0, hive['population'] - deaths)
            if hive['honey_frames'] > 0:
                hive['honey_frames'] -= 1
            else:
                hive['population'] = max(0, hive['population'] - 3000)
                if hive['population'] < 5000:
                    hive['dead'] = True
                    hive['death_reason'] = "Starvation — not enough winter stores. Feed fondant in future!"
                    game['events'].append(f"💀 '{hive['name']}' died — starvation!")

        elif new_season in ["Spring", "Summer"]:
            if hive['queen'] == 'present':
                growth = int(hive['population'] * 0.03 * (new_nectar['flow'] / 5 + 0.3))
                hive['population'] = min(80000, hive['population'] + growth)

            deaths = int(hive['population'] * 0.02)
            hive['population'] = max(0, hive['population'] - deaths)

            if new_nectar['flow'] > 0 and "Rainy" not in game['weather'] and "Stormy" not in game['weather']:
                honey_gain = int(new_nectar['flow'] * 0.5)
                if hive['has_super']:
                    hive['super_honey_frames'] = min(8, hive['super_honey_frames'] + honey_gain)
                else:
                    hive['honey_frames'] = min(9, hive['honey_frames'] + int(honey_gain * 0.3))

            if hive['queen'] == 'virgin' and random.random() < 0.5:
                hive['queen'] = 'present'

            if hive['queen'] == 'present' and hive['age_weeks'] > 100 and random.random() < 0.02:
                hive['queen'] = 'failing'

        elif new_season == "Autumn":
            deaths = int(hive['population'] * 0.025)
            hive['population'] = max(0, hive['population'] - deaths)

            if new_nectar['flow'] > 0 and "Rainy" not in game['weather']:
                honey_gain = int(new_nectar['flow'] * 0.2)
                if hive['has_super']:
                    hive['super_honey_frames'] = min(8, hive['super_honey_frames'] + honey_gain)

        # Varroa (applies all seasons)
        if new_season in ["Spring", "Summer"] and not hive['treated_this_year']:
            hive['varroa_count'] = min(20, hive['varroa_count'] + random.randint(0, 1))

        if hive['varroa_count'] > 10 and new_season == "Winter":
            hive['dead'] = True
            hive['death_reason'] = f"Varroa infestation ({hive['varroa_count']}/300 mites). Treat in August!"
            game['events'].append(f"💀 '{hive['name']}' died — varroa infestation!")

        # Swarm check
        if (hive['queen'] == 'present' and
            new_month in ["April", "May", "June"] and
            hive['population'] > 45000 and
            hive['queen_cells'] >= 3 and
            not hive.get('swarmed', False)):
            lost = int(hive['population'] * 0.5)
            hive['population'] -= lost
            hive['queen_cells'] = 0
            hive['swarmed'] = True
            game['events'].append(f"🐝 '{hive['name']}' SWARMED! Lost {lost:,} bees!")

        # Colony death
        if hive['population'] <= 0 and not hive['dead']:
            hive['dead'] = True
            hive['death_reason'] = "Colony collapsed — population reached zero."
            game['events'].append(f"💀 '{hive['name']}' has died.")

    # Reset seasonal flags in January
    if new_month == "January":
        for h in game['hives']:
            h['treated_this_year'] = False
            h['fed_spring'] = False
            h['fed_autumn'] = False
            h['swarmed'] = False
            h['queen_cells'] = 0

    # Overwinter check
    if new_month == "March":
        surviving = [h for h in game['hives'] if not h['dead'] and h['age_weeks'] > 20]
        for h in surviving:
            game['colonies_overwintered'] += 1
            if not st.session_state.achievements.get('apiary_overwinter', False):
                st.session_state.achievements['apiary_overwinter'] = True
                st.toast("🏅 Achievement Unlocked: Survivor!")

    # Achievements
    active_count = len([h for h in game['hives'] if not h['dead']])
    if active_count >= 3 and not st.session_state.achievements.get('apiary_keeper', False):
        st.session_state.achievements['apiary_keeper'] = True
        st.toast("🏅 Achievement Unlocked: Beekeeper!")
    if active_count >= 5 and not st.session_state.achievements.get('apiary_5_hives', False):
        st.session_state.achievements['apiary_5_hives'] = True
        st.toast("🏅 Achievement Unlocked: Apiarist!")

    # Level up
    level_thresholds = {1: 0, 2: 50, 3: 150, 4: 400, 5: 800}
    for lvl, xp_needed in sorted(level_thresholds.items(), reverse=True):
        if game['xp'] >= xp_needed:
            if game['level'] < lvl:
                game['level'] = lvl
                game['events'].append(f"⭐ Level up! Now level {lvl}!")
                st.toast(f"⭐ Level Up! You're now Level {lvl}!")
            break

    st.rerun()
