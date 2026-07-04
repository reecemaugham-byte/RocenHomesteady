import streamlit as st
import random
import math

from utils import init_session_state, apply_brand_theme, render_sidebar
from auth import render_auth, render_logout_sidebar
from game_config import (ACHIEVEMENTS, SEASON_ICONS, NECTAR_FLOW, HONEY_TYPES,
                         APIARY_PRODUCTS, BEEKEEPING_SEASONS, WEATHER_CHANCES, TEMP_RANGE)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Apiary Manager - Rocen Homesteady",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
init_session_state()
apply_brand_theme()
user = render_auth()
render_logout_sidebar()
render_sidebar()

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
        'week': 13,
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

# --- GAME SIDEBAR STATS ---
st.sidebar.markdown("---")
st.sidebar.markdown("#### 🐝 Apiary Achievements")
for key in ["apiary_first_harvest", "apiary_overwinter", "apiary_keeper", "apiary_5_hives", "apiary_varroa"]:
    ach = ACHIEVEMENTS[key]
    status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
    st.sidebar.caption(f"{status} {ach['name']}")

st.sidebar.markdown("---")
st.sidebar.caption("📚 Curriculum: Science (Life Cycles, Ecosystems, Pollination), PSHE (Responsibility)")

# --- MAIN DISPLAY ---
st.title("🐝 Apiary Manager")
st.caption("Manage your hives through the seasons. Inspect regularly, treat for varroa, and harvest liquid gold!")

# --- GUIDE ---
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

season_colour = {"Spring": "#4CAF50", "Summer": "#FFC107", "Autumn": "#FF8F00", "Winter": "#90CAF9"}.get(current_season, "#4CAF50")

s1.markdown(f"""
<div style="background: var(--bg-card); border-left: 4px solid {season_colour}; border-radius: 0 10px 10px 0; padding: 0.6rem 0.8rem; text-align: center;">
    <div style="color: var(--cream-dim); font-size: 0.75rem; font-weight: 600;">{SEASON_ICONS.get(current_season, '🌸')} SEASON</div>
    <div style="color: var(--cream); font-size: 1.1rem; font-weight: 700;">{current_season}</div>
</div>
""", unsafe_allow_html=True)

s2.metric("📅 Month", f"{current_month[:3]} Wk{get_week_in_month(game['week'])}")
s3.metric(f"{game['weather']}", f"{game['temperature']}°C")
s4.metric("🐝 Hives", f"{total_hives} alive")
s5.metric("💰 Money", f"£{game['money']}")
s6.metric("⭐ Level", f"{game['level']} ({game['xp']} XP)")

# --- CAN INSPECT? ---
inspect_allowed = can_inspect(game['weather'], game['temperature'])

# --- NECTAR FLOW ---
if nectar_info['flow'] > 0:
    flow_stars = "⭐" * nectar_info['flow']
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a2e1a, #243524); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
        <span style="color: var(--green-leaf); font-weight: 600;">🌸 Nectar Flow:</span>
        <span style="color: var(--cream);"> {nectar_info['source']} (Strength: {flow_stars})</span>
        {"<span style='color: var(--amber); margin-left: 0.5rem;'>🍯 Honey type: <b>" + nectar_info['honey_type'] + "</b></span>" if nectar_info.get('honey_type') else ""}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
        <span style="color: var(--cream-dim);">❄️ No significant nectar flow this month. Bees rely on stores.</span>
    </div>
    """, unsafe_allow_html=True)

# --- EVENTS ---
if game['events']:
    with st.expander("📋 Recent Events", expanded=True):
        for event in game['events'][-5:]:
            st.markdown(event)
    if len(game['events']) > 5:
        st.caption(f"... and {len(game['events']) - 5} more events")

# --- SEASONAL WARNINGS ---
if current_month in ["April", "May", "June"]:
    st.markdown(f"""
    <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
        <span style="color: var(--amber); font-weight: 600;">⚠️ Swarm Season!</span>
        <span style="color: var(--cream-dim);"> Check for queen cells every week. A swarmed colony loses half its bees.</span>
    </div>
    """, unsafe_allow_html=True)
if current_month == "August":
    st.markdown(f"""
    <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
        <span style="color: var(--danger); font-weight: 600;">⚠️ Varroa Treatment Month!</span>
        <span style="color: var(--cream-dim);"> Apply treatment now before winter bees are raised.</span>
    </div>
    """, unsafe_allow_html=True)
if current_season == "Winter":
    st.markdown(f"""
    <div style="background: var(--info-bg); border: 1px solid #2196F3; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
        <span style="color: #2196F3; font-weight: 600;">❄️ Winter:</span>
        <span style="color: var(--cream-dim);"> No inspections. Heft hives to check stores. Apply oxalic acid in December.</span>
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 3rem;">💀</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.5rem; font-weight: 700;">All Colonies Have Died</div>
            <div style="color: var(--cream-dim); font-size: 0.95rem; margin-top: 0.5rem;">Buy a new hive to continue your beekeeping journey.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🛒 Buy New Hive (£75)", key="buy_hive_dead", use_container_width=True):
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
            if weeks_since_inspection <= 1:
                inspection_status = "✅ Recent"
                inspection_colour = "var(--green-leaf)"
            elif weeks_since_inspection <= 3:
                inspection_status = "⚠️ Overdue"
                inspection_colour = "var(--amber)"
            else:
                inspection_status = "❌ Unknown"
                inspection_colour = "var(--danger)"

            total_stores = hive['honey_frames'] + (hive['super_honey_frames'] if hive['has_super'] else 0)
            stores_label = "Good" if total_stores >= 7 else ("Low" if total_stores >= 3 else "Critical")

            varroa = hive['varroa_count']
            if weeks_since_inspection <= 2:
                varroa_label = "Low" if varroa <= 3 else ("⚠️ Rising" if varroa <= 6 else "🚨 Critical")
                varroa_colour = "var(--green-leaf)" if varroa <= 3 else ("var(--amber)" if varroa <= 6 else "var(--danger)")
            else:
                varroa_label = "❓ Unknown"
                varroa_colour = "var(--cream-dim)"

            with st.expander(f"🐝 {hive['name']} — Pop: {hive['population']:,} | {inspection_status}"):
                # Quick stats row
                d1, d2, d3, d4 = st.columns(4)

                # Queen status
                if weeks_since_inspection <= 1:
                    queen_icon = {"present": "👑", "failing": "⚠️", "virgin": "🐣", "dead": "💀"}.get(hive['queen'], "❓")
                    queen_label = {"present": "Present", "failing": "Failing", "virgin": "Virgin", "dead": "No Queen"}.get(hive['queen'], "Unknown")
                    d1.metric("Queen", f"{queen_icon} {queen_label}")
                else:
                    d1.metric("Queen", "❓ Unknown")

                # Population
                pop_label = "Strong" if hive['population'] > 40000 else ("Medium" if hive['population'] > 20000 else "Weak")
                d2.metric("Population", f"{hive['population']:,}", pop_label)

                # Stores
                stores_status = "✅ Good" if total_stores >= 7 else ("⚠️ Low" if total_stores >= 3 else "🚨 Critical")
                d3.metric("Honey Stores", f"{total_stores} frames", stores_status)

                # Varroa
                d4.metric("Varroa", f"{varroa}/300", varroa_label)

                # Queen cells alert
                if hive['queen_cells'] > 0 and weeks_since_inspection <= 1:
                    st.markdown(f"""
                    <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 8px; padding: 0.5rem 0.8rem;">
                        <span style="color: var(--amber); font-weight: 600;">⚠️ {hive['queen_cells']} Queen Cell(s) Found!</span>
                        <span style="color: var(--cream-dim);"> Swarm risk is HIGH. Consider splitting.</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Swarm warning
                if hive['population'] > 40000 and current_month in ["April", "May", "June"]:
                    st.markdown(f"""
                    <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 8px; padding: 0.5rem 0.8rem;">
                        <span style="color: var(--danger); font-weight: 600;">🐝 High population + swarm season = High swarm risk!</span>
                        <span style="color: var(--cream-dim);"> Inspect weekly.</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Winter stores warning
                if current_season in ["Autumn", "Winter"] and total_stores < 5:
                    st.markdown(f"""
                    <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 8px; padding: 0.5rem 0.8rem;">
                        <span style="color: var(--danger); font-weight: 600;">❄️ Stores dangerously low! Feed immediately or colony will starve.</span>
                    </div>
                    """, unsafe_allow_html=True)

        # --- BUY HIVE ---
        st.markdown("---")
        st.markdown("#### 🛒 Buy New Hive")
        max_hives = game['level'] + 1
        hive_cost = 75

        st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
            <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.8rem 1rem; text-align: center; flex: 1; min-width: 100px;">
                <div style="color: var(--cream-dim); font-size: 0.8rem; font-weight: 600;">COST</div>
                <div style="color: var(--amber); font-size: 1.3rem; font-weight: 700;">£{hive_cost}</div>
            </div>
            <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.8rem 1rem; text-align: center; flex: 1; min-width: 100px;">
                <div style="color: var(--cream-dim); font-size: 0.8rem; font-weight: 600;">MAX HIVES</div>
                <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{max_hives} (Level {game['level']})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        can_buy = game['money'] >= hive_cost and total_hives < max_hives
        if st.button(f"🛒 Buy Hive (£{hive_cost})", disabled=not can_buy, key="buy_hive_main", use_container_width=True):
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
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 12px; padding: 1.5rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem;">🚫</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.3rem; font-weight: 700;">Cannot Inspect Today</div>
            <div style="color: var(--cream-dim); font-size: 0.95rem; margin-top: 0.5rem;">
                Weather: {game['weather']} | Temperature: {game['temperature']}°C<br>
                <span style="font-size: 0.85rem;">(Need ≥14°C and dry)</span>
            </div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem; font-style: italic;">
                In real beekeeping, you should only open the hive on warm, dry days to avoid chilling the brood.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <span style="color: var(--green-leaf); font-weight: 600;">✅ Good inspection weather!</span>
            <span style="color: var(--cream);"> {game['weather']} | {game['temperature']}°C</span>
        </div>
        """, unsafe_allow_html=True)

    if not active_hives:
        st.warning("No active hives to inspect.")
    else:
        hive_names = [h['name'] for h in active_hives]
        selected_name = st.selectbox("Select Hive", hive_names, key="inspect_hive_select")
        selected_hive = next((h for h in active_hives if h['name'] == selected_name), None)

        if selected_hive:
            weeks_since = game['week'] - selected_hive['inspected_week']

            if not inspect_allowed:
                # Heft check only
                total_stores = selected_hive['honey_frames']
                heft = "Heavy" if total_stores >= 7 else ("About right" if total_stores >= 4 else "Light ⚠️")
                heft_colour = "var(--green-leaf)" if total_stores >= 7 else ("var(--amber)" if total_stores >= 4 else "var(--danger)")
                st.markdown(f"""
                <div style="background: var(--info-bg); border: 1px solid #2196F3; border-radius: 10px; padding: 1rem; text-align: center;">
                    <div style="color: #2196F3; font-size: 0.9rem;">❄️ You can only heft the hive (lift one side to estimate stores).</div>
                    <div style="color: {heft_colour}; font-size: 1.3rem; font-weight: 700; margin-top: 0.5rem;">{heft}</div>
                </div>
                """, unsafe_allow_html=True)
                if total_stores < 4:
                    st.markdown(f"""
                    <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 8px; padding: 0.5rem 0.8rem;">
                        <span style="color: var(--danger); font-weight: 600;">⚠️ Stores feel light! Feed fondant or syrup.</span>
                    </div>
                    """, unsafe_allow_html=True)

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
                        frame_colours = {
                            "🍯": "#DAA520", "🟡": "#FFD700", "🥚": "#FFFFFF",
                            "🐛": "#F5F5DC", "🟤": "#8B4513", "⚠️": "#FF4444", "⬜": "#333333"
                        }
                        bg = frame_colours.get(frame, "#333333")
                        st.markdown(f"""
                        <div style="background: {bg}20; border: 2px solid {bg}; border-radius: 4px; padding: 4px; text-align: center; min-height: 50px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 1.2rem;">{frame}</span>
                        </div>
                        """, unsafe_allow_html=True)

                if selected_hive['has_super']:
                    sf = int(min(selected_hive['super_honey_frames'], 8))
                    super_frames = ["🍯"] * sf + ["⬜"] * (8 - sf)
                    st.markdown("**Super** (8 frames):")
                    s_cols = st.columns(8)
                    for i, frame in enumerate(super_frames):
                        with s_cols[i]:
                            bg = "#DAA52020" if frame == "🍯" else "#33333320"
                            border = "#DAA520" if frame == "🍯" else "#333333"
                            st.markdown(f"""
                            <div style="background: {bg}; border: 2px solid {border}; border-radius: 4px; padding: 4px; text-align: center; min-height: 50px; display: flex; align-items: center; justify-content: center;">
                                <span style="font-size: 1.2rem;">{frame}</span>
                            </div>
                            """, unsafe_allow_html=True)

                # Queen cells
                if selected_hive['queen_cells'] > 0:
                    st.markdown(f"""
                    <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0;">
                        <span style="color: var(--amber); font-weight: 700;">⚠️ {selected_hive['queen_cells']} Queen Cell(s) Found!</span>
                        <span style="color: var(--cream-dim);"> Consider splitting or removing them.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 8px; padding: 0.5rem 0.8rem; margin: 0.5rem 0;">
                        <span style="color: var(--green-leaf); font-weight: 600;">✅ No queen cells found.</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.caption("🍯 Honey | 🟡 Pollen | 🥚 Eggs | 🐛 Larvae | 🟤 Capped Brood | ⬜ Empty | ⚠️ Queen Cell")

                # Dashboard
                st.markdown("---")
                st.markdown("#### 📊 Colony Dashboard")

                d1, d2, d3, d4 = st.columns(4)

                queen_icon_map = {"present": "👑 Present", "failing": "⚠️ Failing", "virgin": "🐣 Virgin", "dead": "💀 No Queen"}
                d1.metric("👑 Queen", queen_icon_map.get(selected_hive['queen'], selected_hive['queen']))

                pop = selected_hive['population']
                pop_delta = "Strong" if pop > 40000 else ("Medium" if pop > 20000 else "Weak")
                d2.metric("🐝 Population", f"{pop:,}", pop_delta)

                varroa = selected_hive['varroa_count']
                varroa_status = "✅ Low" if varroa <= 3 else ("⚠️ Rising" if varroa <= 6 else "🚨 Critical")
                d3.metric("🪲 Varroa", f"{varroa}/300", varroa_status)

                stores = int(selected_hive['honey_frames'] + (selected_hive['super_honey_frames'] if selected_hive['has_super'] else 0))
                stores_status = "✅ Good" if stores >= 7 else ("⚠️ Low" if stores >= 3 else "🚨 Critical")
                d4.metric("🍯 Stores", f"{stores} frames", stores_status)

                # Health assessment
                health_issues = []
                if selected_hive['queen'] == 'failing':
                    health_issues.append("⚠️ Queen is failing — consider requeening")
                if selected_hive['queen'] == 'dead':
                    health_issues.append("🚨 No queen — colony will die without intervention")
                if selected_hive['varroa_count'] > 6:
                    health_issues.append(f"🚨 Varroa levels critical ({selected_hive['varroa_count']}/300) — treat immediately")
                elif selected_hive['varroa_count'] > 3:
                    health_issues.append(f"Varroa rising ({selected_hive['varroa_count']}/300) — treat in Aug/Sep or Dec")
                if stores < 4 and current_season in ["Autumn", "Winter"]:
                    health_issues.append("🚨 Winter stores dangerously low — feed now!")
                if selected_hive['population'] < 15000:
                    health_issues.append("⚠️ Colony is weak — may not survive winter")

                if health_issues:
                    issues_html = "<br>".join([f"<span style='color: var(--cream-dim); font-size: 0.9rem;'>• {issue}</span>" for issue in health_issues])
                    st.markdown(f"""
                    <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 1rem;">
                        <div style="color: var(--danger); font-weight: 700; font-size: 0.95rem; margin-bottom: 0.5rem;">Health Issues:</div>
                        {issues_html}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 1rem;">
                        <span style="color: var(--green-leaf); font-weight: 700;">✅ Colony looks healthy!</span>
                    </div>
                    """, unsafe_allow_html=True)

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
                            st.error("Need £15!")
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                        <span style="color: var(--green-leaf); font-weight: 600;">✅ Super already on hive.</span>
                    </div>
                    """, unsafe_allow_html=True)

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
                    if st.button("🍬 Feed Fondant — £4", key="feed_fondant"):
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
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem;">
                            <span style="color: var(--green-leaf); font-weight: 600;">✅ Already treated this year.</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.caption("Treatment in Aug/Sep (Apivar £15) or Dec (Oxalic £10). Keep advancing weeks!")

                # SPLIT COLONY
                can_split = (act_hive['queen_cells'] >= 2 and
                            act_hive['population'] > 20000 and
                            total_hives < game['level'] + 1 and
                            current_month in ["April", "May", "June"])
                if st.button("✂️ Split Colony (Swarm Control)", key="split_colony", disabled=not can_split):
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

                # REMOVE QUEEN CELLS
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
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 1px solid #555; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                <div style="color: var(--danger); font-weight: 700;">💀 {dh['name']}</div>
                <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">{dh['death_reason']}</div>
            </div>
            """, unsafe_allow_html=True)
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
            st.markdown(f"""
            <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2rem;">🍯</div>
                <div style="color: var(--cream-dim); font-size: 0.95rem;">No hives ready for harvest.</div>
                <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">Add supers and wait for the nectar flow!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for hive in harvestable:
                frames = hive['super_honey_frames']
                honey_type = nectar_info.get('honey_type', 'Summer Wildflower')
                honey_value = HONEY_TYPES.get(honey_type, HONEY_TYPES.get('Summer Wildflower', {})).get('value', 5) if honey_type else HONEY_TYPES.get('Summer Wildflower', {}).get('value', 5)
                jars = max(1, int(frames * 1.5))

                if st.button(f"🍯 Harvest from '{hive['name']}' ({frames} frames → ~{jars} jars of {honey_type})", key=f"harvest_{hive['name']}"):
                    honey_key = honey_type if honey_type else "Summer Wildflower"
                    game['inventory'][honey_key] = game['inventory'].get(honey_key, 0) + jars
                    game['inventory']['Beeswax'] = game['inventory'].get('Beeswax', 0) + max(1, frames // 3)

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
            st.markdown(f"""
            <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
                <div style="color: var(--cream-dim);">Nothing to sell. Harvest honey first!</div>
            </div>
            """, unsafe_allow_html=True)
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
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1rem; text-align: center;">
            <span style="color: var(--cream-dim);">Empty — harvest honey to fill your inventory!</span>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# ADVANCE WEEK
# ==========================================
st.markdown("---")
st.markdown(f"""
<div style="background: var(--info-bg); border: 1px solid #2196F3; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
    <span style="color: #2196F3;">⏰</span>
    <span style="color: var(--cream-dim);"> This game is turn-based. Inspect your hives, take actions, then click below to advance one week.</span>
</div>
""", unsafe_allow_html=True)

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

        # Varroa
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
