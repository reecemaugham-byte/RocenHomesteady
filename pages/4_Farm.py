import streamlit as st
import random
from datetime import datetime

from utils import init_session_state, apply_brand_theme, render_save_load
from auth import render_auth, render_logout_sidebar
from game_config import (ACHIEVEMENTS, SEASON_ICONS, FARM_ICONS, FARM_BUILDINGS,
                         SEED_COST, BASE_PRICES, BASICS, MG_CROPS, MG_COMPANIONS,
                         MG_ANTAGONISTS, MG_SEASONS, MG_MARKET_BASE)
from plants_data import UK_PLANTS

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Farm Games - Rocen Homesteady",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
init_session_state()
apply_brand_theme()
user = render_auth()

if 'achievements' not in st.session_state or not st.session_state.achievements:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}

# --- HELPER FUNCTIONS ---
def get_year(day):
    return (day // 120) + 1

def get_season(day):
    day_in_year = day % 120
    if day_in_year < 30: return "Spring"
    elif day_in_year < 60: return "Summer"
    elif day_in_year < 90: return "Autumn"
    else: return "Winter"

def get_soil_color(val):
    if val >= 70:
        return "🟢"
    elif val >= 40:
        return "🟡"
    else:
        return "🔴"

def get_companion_bonus(bed_idx, crop, beds):
    bonuses = []
    penalties = []
    row = bed_idx // 4
    col = bed_idx % 4
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 4:
            adj_idx = nr * 4 + nc
            adj_crop = beds[adj_idx]['crop']
            if adj_crop:
                pair = tuple(sorted([crop, adj_crop]))
                if pair in MG_COMPANIONS:
                    bonuses.append((adj_crop, MG_COMPANIONS[pair]))
                if pair in MG_ANTAGONISTS:
                    penalties.append((adj_crop, MG_ANTAGONISTS[pair]))
    return bonuses, penalties

def get_mg_month(day):
    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    return months[(day - 1) % 48 // 4]

def get_mg_season(month):
    for season, months in MG_SEASONS.items():
        if month in months:
            return season
    return "Spring"

# --- TILE DISPLAY HELPER ---
TILE_STYLES = {
    0: {"icon": "🌱", "label": "Empty", "bg": "#1a2e1a", "border": "#3d5a3d", "text": "var(--cream-dim)"},
    1: {"icon": "🌊", "label": "Stream", "bg": "#0a1a2e", "border": "#2196F3", "text": "#90CAF9"},
    2: {"icon": "🌱", "label": "Seed", "bg": "#1a2e1a", "border": "#4CAF50", "text": "#81C784"},
    3: {"icon": "🌿", "label": "Growing", "bg": "#1a2e1a", "border": "#66BB6A", "text": "#A5D6A7"},
    4: {"icon": "🌾", "label": "Ready!", "bg": "#2a2a00", "border": "#FFC107", "text": "#FFD54F"},
    5: {"icon": "🏠", "label": "House", "bg": "#1a2a1a", "border": "#8D6E63", "text": "#BCAAA4"},
    6: {"icon": "🔋", "label": "Generator", "bg": "#1a1a1a", "border": "#FFC107", "text": "#FFD54F"},
    7: {"icon": "🌿", "label": "Weed", "bg": "#2a1a0a", "border": "#8D6E63", "text": "#BCAAA4"},
    8: {"icon": "☀️", "label": "Solar", "bg": "#2a2a00", "border": "#FFC107", "text": "#FFD54F"},
    9: {"icon": "🦅", "label": "Scarecrow", "bg": "#1a1a0a", "border": "#FFC107", "text": "#FFD54F"},
    10: {"icon": "🌳", "label": "Tree", "bg": "#0a2a0a", "border": "#2E7D32", "text": "#66BB6A"},
    11: {"icon": "🌴", "label": "Orchard", "bg": "#0a2a0a", "border": "#4CAF50", "text": "#81C784"},
    12: {"icon": "🐔", "label": "Chickens", "bg": "#1a2a1a", "border": "#FF9800", "text": "#FFB74D"},
    13: {"icon": "🐄", "label": "Cows", "bg": "#1a1a0a", "border": "#8D6E63", "text": "#BCAAA4"},
    14: {"icon": "🐐", "label": "Goats", "bg": "#1a1a0a", "border": "#A1887F", "text": "#D7CCC8"},
    15: {"icon": "🫧", "label": "Cold Frame", "bg": "#0a2a2a", "border": "#26C6DA", "text": "#80DEEA"},
}

# Add building styles from FARM_BUILDINGS
for bname, bdata in FARM_BUILDINGS.items():
    bid = bdata['id']
    if bid not in TILE_STYLES:
        TILE_STYLES[bid] = {
            "icon": bdata.get('icon', '🏠'), # Replace 🏠 with whatever your default fallback icon is
            "label": bname,
            "bg": "#1a2e1a",
            "border": "#4CAF50",
            "text": "var(--cream)"
        }

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("🌿 **Rocen Homesteady**")
    st.markdown("---")

    render_logout_sidebar()
    st.markdown("---")
    render_save_load()
    st.markdown("---")

    unlocked_count = sum(1 for v in st.session_state.achievements.values() if v)
    total_count = len(ACHIEVEMENTS)
    st.metric("🏆 Achievements", f"{unlocked_count} / {total_count}")

    st.markdown("#### 🚜 Farm Achievements")
    for key in ["farm_harvest", "farm_rancher", "farm_winner"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("#### 🌱 Garden Achievements")
    for key in ["mg_first_harvest", "mg_companion", "mg_rotation", "mg_market_master"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("---")
    st.caption("📚 Curriculum: Maths (Money & Resources), Science (Seasons, Life Cycles)")

# --- FARM GAME STATE ---
if st.session_state.get('farm_game') is None:
    grid = [[0 for _ in range(6)] for _ in range(5)]
    stream_col = random.randint(1, 4)
    for r in range(5):
        grid[r][stream_col] = 1

    st.session_state.farm_game = {
        'grid': grid, 'money': 200, 'day': 1,
        'inventory': {'Feed': 0},
        'market_prices': dict(BASE_PRICES),
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

# --- MIGRATIONS ---
for k, v in BASE_PRICES.items():
    if k not in game['market_prices']:
        game['market_prices'][k] = v
if 'Feed' not in game['inventory']:
    game['inventory']['Feed'] = 0
if 'market_event' not in game:
    game['market_event'] = None
if 'last_event' not in game:
    game['last_event'] = ""
if 'total_harvests' not in game:
    game['total_harvests'] = 0
if 'manor_bought' not in game:
    game['manor_bought'] = False
if 'sales_log' not in game:
    game['sales_log'] = {}
if 'crop_map' not in game:
    game['crop_map'] = {}
if 'fallow_days' not in game:
    game['fallow_days'] = [[0 for _ in range(6)] for _ in range(5)]
if 'soil_health' not in game:
    game['soil_health'] = [[100 for _ in range(6)] for _ in range(5)]

# --- FARM DERIVED VALUES ---
current_year = get_year(game['day'])
current_season = get_season(game['day'])
chickens = sum(row.count(12) for row in game['grid'])
cows = sum(row.count(13) for row in game['grid'])
goats = sum(row.count(14) for row in game['grid'])
total_animals = chickens + cows + goats
has_cold_frame = any(15 in row for row in game['grid'])

# --- MARKET GARDEN STATE ---
if st.session_state.get('market_garden') is None:
    mg_beds = []
    for i in range(12):
        mg_beds.append({
            'crop': None, 'days': 0, 'soil_N': 80, 'soil_P': 80, 'soil_K': 80,
            'history': [], 'watered': False
        })
    st.session_state.market_garden = {
        'beds': mg_beds, 'day': 13, 'money': 80, 'compost': 0,
        'inventory': {}, 'total_earned': 0, 'level': 1, 'xp': 0,
        'weather': '☀️ Sunny', 'market_prices': dict(MG_MARKET_BASE),
        'sales_log': {}, 'events': [], 'companion_count': 0,
        'rotation_count': 0, 'total_harvests': 0,
    }

mg = st.session_state.market_garden

for key in ['companion_count', 'rotation_count', 'total_harvests', 'events',
            'has_polytunnel', 'fertiliser', 'organic_certified',
            'has_irrigation', 'water_saved', 'golden_found', 'rare_found']:
    if key not in mg:
        if key in ['companion_count', 'rotation_count', 'total_harvests', 'water_saved']:
            mg[key] = 0
        elif key in ['events', 'golden_found', 'rare_found']:
            mg[key] = []
        elif key in ['fertiliser']:
            mg[key] = 0
        else:
            mg[key] = False

# --- DERIVED VALUES ---
mg_month = get_mg_month(mg['day'])
mg_season = get_mg_season(mg_month)
available_crops = [name for name, data in MG_CROPS.items() if mg_season in data['season']]

if mg.get('has_polytunnel') and mg_season == "Spring":
    summer_crops = [name for name, data in MG_CROPS.items() if "Summer" in data['season'] and name not in available_crops]
    available_crops = available_crops + summer_crops

# --- TITLE AND TABS ---
st.title("🚜 Farm Games")
st.caption("Grow crops, raise animals, and master the market!")

farm_tab, garden_tab = st.tabs(["🚜 Farm Tycoon", "🌱 Market Garden"])

# ==========================================
# TAB 1: FARM TYCOON
# ==========================================
with farm_tab:
    st.header("🚜 Farm Tycoon")

    with st.expander("📖 Guide & Progression"):
        st.markdown("""
        **📅 Timeline:**
        - Seasons last **30 Days** (120 days = 1 Year).
        - **Year 1:** Focus on crops and bees. Animals are locked.
        - **Year 2+:** Animals (Chickens, Cows, Goats) are unlocked.

        **🌱 Farming:**
        - Crops take **3 days** to grow (🌱→🌿→🌾).
        - Empty plots regenerate **+5 soil health** per day.
        - **Cold Frame 🫧** protects ALL crops from winter kill!

        **📦 Feed & Animals:**
        - Animals eat **Feed Bags** (best) or **Wheat** (fallback).
        - **Recipe:** 1 Wheat + 1 Carrot + 1 Corn = **5 Feed Bags**.
        - Unfed animals produce nothing and show a warning.

        **📉 Market:**
        - Random **Surges** double the price of a crop!
        - Selling >10 of one item **crashes** the price by 20%.

        **❄️ Winter:**
        - Crops die (unless you have a Cold Frame).
        - Build a **Cold Frame** before winter to protect your harvest!
        """)

    if game['manor_bought']:
        st.balloons()
        st.markdown(f"""
        <div class="level-up">
            <div style="font-size: 3rem;">🏆</div>
            <div style="color: var(--amber); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">FARMING DYNASTY COMPLETE!</div>
            <div style="color: var(--cream); font-size: 1rem; margin-top: 0.5rem;">Final Money: £{game['money']} | Days: {game['day']} | Harvests: {game['total_harvests']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Start New Farm", key="restart_farm_win"):
            st.session_state.farm_game = None
            st.rerun()

    if game['last_event']:
        event_str = game['last_event'].strip()
        if event_str:
            st.markdown(f"""
            <div style="background: #3d2e0a; border: 1px solid var(--amber-dark); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <span style="color: var(--amber-dark); font-weight: 600;">📋 Report:</span>
                <span style="color: var(--cream);"> {event_str}</span>
            </div>
            """, unsafe_allow_html=True)

    if game['market_event']:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 1px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
            <span style="color: var(--amber); font-weight: 600;">📈 Market Surge:</span>
            <span style="color: var(--cream);"> {game['market_event']} prices have doubled!</span>
        </div>
        """, unsafe_allow_html=True)

    # --- STATS ---
    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber-dark); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--amber-dark); font-size: 0.75rem; font-weight: 600;">📅 YEAR</div>
            <div style="color: var(--cream); font-size: 1.1rem; font-weight: 700;">{current_year} - {current_season}</div>
        </div>
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--amber); font-size: 0.75rem; font-weight: 600;">💰 MONEY</div>
            <div style="color: var(--cream); font-size: 1.1rem; font-weight: 700;">£{game['money']}</div>
        </div>
        <div style="background: var(--bg-card); border: 2px solid #3d5a3d; border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--green-leaf); font-size: 0.75rem; font-weight: 600;">🐔 CHICKENS</div>
            <div style="color: var(--cream); font-size: 1.1rem; font-weight: 700;">{chickens if current_year >= 2 else "🔒 Y2"}</div>
        </div>
        <div style="background: var(--bg-card); border: 2px solid #3d5a3d; border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 100px;">
            <div style="color: var(--green-leaf); font-size: 0.75rem; font-weight: 600;">🐄 COWS / 🐐 GOATS</div>
            <div style="color: var(--cream); font-size: 1.1rem; font-weight: 700;">{cows}/{goats} {"🔒 Y2" if current_year < 2 else ""}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if current_season == "Autumn":
        st.markdown(f"""
        <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
            <span style="color: var(--amber); font-weight: 600;">🍂 AUTUMN WARNING:</span>
            <span style="color: var(--cream-dim);"> Winter is coming! Stockpile food and build a Cold Frame!</span>
        </div>
        """, unsafe_allow_html=True)
    elif current_season == "Winter":
        if has_cold_frame:
            st.markdown(f"""
            <div style="background: var(--info-bg); border: 1px solid #2196F3; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <span style="color: #2196F3; font-weight: 600;">❄️ WINTER:</span>
                <span style="color: var(--cream-dim);"> Crops protected by Cold Frame! 🫧</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <span style="color: var(--danger); font-weight: 600;">❄️ WINTER:</span>
                <span style="color: var(--cream-dim);"> Crops will die! Build a Cold Frame to protect them.</span>
            </div>
            """, unsafe_allow_html=True)

    # --- INVENTORY ---
    inv_str = " | ".join([f"**{k}:** {v}" for k, v in game['inventory'].items() if v > 0])
    if inv_str:
        st.markdown(f"**🎒 Stock:** {inv_str}")
    else:
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.5rem 1rem; text-align: center;">
            <span style="color: var(--cream-dim);">🎒 Empty — start farming!</span>
        </div>
        """, unsafe_allow_html=True)

    feed_needed = chickens + (cows * 2) + goats
    if total_animals > 0:
        feed_colour = "🟢" if game['inventory'].get('Feed', 0) >= feed_needed else "🔴"
        st.caption(f"{feed_colour} Feed Needed: {feed_needed}/day | Feed in Stock: {game['inventory'].get('Feed', 0)}")

    st.markdown("---")

    # --- TOOL SELECTION ---
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        game['tool'] = st.selectbox("🌱 Plant", ["Carrot", "Wheat", "Corn"], key="farm_tool_crops")
    with t2:
        available_buildings = {
            k: v for k, v in FARM_BUILDINGS.items()
            if k in ["Manor", "Barn", "Beehive", "Scarecrow", "Sprinkler", "Cold Frame"]
            or (current_year >= 2 and k in ["Chicken Coop", "Cow Pasture", "Goat Pen"])
        }
        build_opts = ["None"] + [f"{name} (£{data['cost']})" for name, data in available_buildings.items()]
        game['build_sel_raw'] = st.selectbox("🏗️ Build", build_opts, key="farm_tool_build")
        if game['build_sel_raw'] != "None":
            game['build_sel'] = game['build_sel_raw'].split(" (£")[0]
        else:
            game['build_sel'] = "None"
    with t3:
        if st.button("🧹 Clear Weeds", key="farm_clear_btn"):
            removed = 0
            for r in range(5):
                for c in range(6):
                    if game['grid'][r][c] == 7:
                        game['grid'][r][c] = 0
                        removed += 1
            if removed > 0:
                st.success(f"Cleared {removed} weeds!")
                st.rerun()
            else:
                st.info("No weeds to clear!")
    with t4:
        st.caption(f"🌱 Tool: {game['tool']}")

    # --- FEED PRODUCTION ---
    st.markdown("---")
    st.markdown("#### 🏭 Feed Production")
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("**Recipe:** 1 Wheat + 1 Carrot + 1 Corn = 5 Feed")
    with f2:
        has_ing = (
            game['inventory'].get('Wheat', 0) >= 1
            and game['inventory'].get('Carrot', 0) >= 1
            and game['inventory'].get('Corn', 0) >= 1
        )
        if st.button("Make Feed Bag", disabled=not has_ing, key="make_feed_btn"):
            game['inventory']['Wheat'] -= 1
            game['inventory']['Carrot'] -= 1
            game['inventory']['Corn'] -= 1
            game['inventory']['Feed'] = game['inventory'].get('Feed', 0) + 5
            st.toast("+5 Feed Bags")
            st.rerun()

    st.markdown("---")

    # ==========================================
    # UPGRADED FARM GRID
    # ==========================================
    st.markdown("#### 🗺️ Your Farm")

    # Placing mode banner
    if game.get('placing_mode', False):
        b_name = game['placing_mode']
        b_data = FARM_BUILDINGS.get(b_name, {})
        b_icon = b_data.get('icon', '🏗️')
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber); border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
            <span style="color: var(--amber); font-weight: 700;">📍 Placing Mode:</span>
            <span style="color: var(--cream-dim);"> Click a <span style="color: var(--green-leaf);">🌱 Empty</span> tile to build <b>{b_icon} {b_name}</b>.</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("❌ Cancel Placement", key="cancel_placement"):
            cost = FARM_BUILDINGS[b_name]['cost']
            game['money'] += cost
            game['placing_mode'] = None
            st.rerun()

    # Render grid with styled tiles
    for row_idx in range(5):
        row_cols = st.columns(6)
        for col_idx in range(6):
            tile_val = game['grid'][row_idx][col_idx]
            is_damaged = (row_idx, col_idx) in game.get('damaged_buildings', [])
            soil = game['soil_health'][row_idx][col_idx]
            crop_name = game['crop_map'].get((row_idx, col_idx), "")

            with row_cols[col_idx]:
                style = TILE_STYLES.get(tile_val, {"icon": "❓", "label": str(tile_val), "bg": "#1a1a1a", "border": "#555", "text": "#aaa"})

                # Determine display label
                if tile_val in [2, 3] and crop_name:
                    display_label = f"{style['icon']} {crop_name}"
                elif tile_val == 4 and crop_name:
                    display_label = f"🌾 {crop_name}"
                else:
                    display_label = style['icon']

                # Soil indicator for growing/ready crops
                soil_info = ""
                if tile_val in [2, 3, 4]:
                    soil_info = f"<div style='font-size: 0.55rem; color: var(--cream-dim);'>Soil {soil}%</div>"

                # Damage overlay
                damage_badge = ""
                if is_damaged:
                    damage_badge = "<div style='color: var(--danger); font-size: 0.6rem; font-weight: 700; text-transform: uppercase;'>DAMAGED</div>"

                # Background style
                if is_damaged:
                    border_style = "2px dashed var(--danger)"
                    bg_style = "linear-gradient(135deg, #2a0a0a, #1a0000)"
                else:
                    border_style = f"2px solid {style['border']}"
                    bg_style = style['bg']

                # Render visual tile
                st.markdown(f"""
                <div style="
                    background: {bg_style};
                    border: {border_style};
                    border-radius: 10px;
                    padding: 0.4rem;
                    text-align: center;
                    min-height: 80px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="font-size: 1.4rem; line-height: 1;">{style['icon']}</div>
                    <div style="color: {style['text']}; font-size: 0.65rem; font-weight: 600; margin-top: 0.15rem; line-height: 1.2;">{style['label'] if tile_val not in [2, 3, 4] else crop_name}</div>
                    {damage_badge}
                    {soil_info}
                </div>
                """, unsafe_allow_html=True)

                # Interactive buttons below tile
                if tile_val == 7:
                    if st.button("🧹 Clear", key=f"fm_w_{row_idx}_{col_idx}", use_container_width=True):
                        game['grid'][row_idx][col_idx] = 0
                        game['fallow_days'][row_idx][col_idx] = 0
                        st.rerun()

                elif tile_val == 0:
                    # Get the value safely, default to False if it doesn't exist yet
                    placing_mode = game.get('placing_mode', False)

                    # Now check if it's active and not the string "None"
                    if placing_mode and placing_mode != "None":

                        b_name = game['placing_mode']
                        b_data = FARM_BUILDINGS.get(b_name, None)
                        if b_data:
                            if b_name in ["Chicken Coop", "Cow Pasture", "Goat Pen"] and current_year < 2:
                                st.caption("🔒 Year 2")
                            else:
                                if st.button(f"Build £{b_data['cost']}", key=f"fm_b_{row_idx}_{col_idx}", use_container_width=True):
                                    if game['money'] >= b_data['cost']:
                                        game['money'] -= b_data['cost']
                                        game['grid'][row_idx][col_idx] = b_data['id']
                                        if b_name not in game.get('owned_buildings', {}):
                                            game['owned_buildings'] = game.get('owned_buildings', {})
                                        game['owned_buildings'][b_name] = game['owned_buildings'].get(b_name, 0) + 1
                                        if b_name == "Barn":
                                            game['stats']['Storage_Limit'] = game['stats'].get('Storage_Limit', 10) + 20
                                        game['placing_mode'] = None
                                        st.rerun()
                                    else:
                                        st.error(f"Need £{b_data['cost']}")
                    else:
                        crop = game['tool']
                        cost = SEED_COST.get(crop, 6)
                        if st.button(f"🌱 £{cost}", key=f"fm_p_{row_idx}_{col_idx}", use_container_width=True):
                            if game['money'] >= cost:
                                game['money'] -= cost
                                game['grid'][row_idx][col_idx] = 2
                                game['crop_map'][(row_idx, col_idx)] = crop
                                game['fallow_days'][row_idx][col_idx] = 0
                                st.rerun()
                            else:
                                st.error(f"Need £{cost}")

                elif tile_val == 4:
                    if st.button("🌾 Harvest", key=f"fm_h_{row_idx}_{col_idx}", use_container_width=True):
                        crop = game['crop_map'].get((row_idx, col_idx), "Carrot")
                        yield_count = 1
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = row_idx + dr, col_idx + dc
                            if 0 <= nr < 5 and 0 <= nc < 6:
                                if game['grid'][nr][nc] == 9:
                                    yield_count += 1

                        harvested = max(1, int(yield_count * (game['soil_health'][row_idx][col_idx] / 100)))

                        game['inventory'][crop] = game['inventory'].get(crop, 0) + harvested
                        game['grid'][row_idx][col_idx] = 0
                        game['soil_health'][row_idx][col_idx] = max(0, game['soil_health'][row_idx][col_idx] - 10)
                        game['crop_map'].pop((row_idx, col_idx), None)
                        game['fallow_days'][row_idx][col_idx] = 0
                        game['total_harvests'] += 1

                        if game['total_harvests'] >= 1 and not st.session_state.achievements.get('farm_harvest', False):
                            st.session_state.achievements['farm_harvest'] = True
                            st.toast("🏅 Achievement Unlocked: Green Thumb!")

                        st.toast(f"+{harvested} {crop}")
                        st.rerun()

                elif tile_val == 1:
                    disable_fish = (current_season == "Winter")
                    if st.button("🎣 Fish", key=f"fm_fish_{row_idx}_{col_idx}", disabled=disable_fish, use_container_width=True):
                        game['inventory']['Fish'] = game['inventory'].get('Fish', 0) + 1
                        st.toast("🎣 Caught a Fish!")
                        st.rerun()

    # --- LEGEND ---
    st.markdown(f"""
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem; margin-bottom: 0.5rem;">
        <span style="background: #1a2e1a; border: 1px solid #3d5a3d; border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.75rem; color: var(--cream-dim);">🌱 Empty</span>
        <span style="background: #1a2e1a; border: 1px solid #4CAF50; border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.75rem; color: #81C784;">🌱🌿 Growing</span>
        <span style="background: #2a2a00; border: 1px solid #FFC107; border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.75rem; color: #FFD54F;">🌾 Ready</span>
        <span style="background: #0a1a2e; border: 1px solid #2196F3; border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.75rem; color: #90CAF9;">🌊 Stream</span>
        <span style="background: #2a1a0a; border: 1px solid #8D6E63; border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.75rem; color: #BCAAA4;">🌿 Weed</span>
        <span style="background: #0a2a2a; border: 1px solid #26C6DA; border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.75rem; color: #80DEEA;">🫧 Cold Frame</span>
    </div>
    """, unsafe_allow_html=True)

    # --- MARKET ---
    st.markdown("---")
    st.markdown("#### 💰 Market")

    st.markdown('<div class="market-box">', unsafe_allow_html=True)
    market_items = list(game['market_prices'].keys())
    mkt_cols = st.columns(min(len(market_items), 6))
    for i, item in enumerate(market_items):
        col_idx = i % 6
        if i > 0 and i % 6 == 0:
            mkt_cols = st.columns(6)

        price = game['market_prices'][item]
        count = game['inventory'].get(item, 0)

        if game['market_event'] == item:
            price = price * 2
            surge_msg = "📈"
        else:
            surge_msg = ""

        crash_msg = ""
        if game['sales_log'].get(item, 0) > 10:
            crash_msg = "📉"
            price = max(1, int(price * 0.8))

        with mkt_cols[col_idx]:
            st.markdown(f"**{item}** {crash_msg}")
            st.caption(f"Have: {count}")
            if st.button(f"Sell £{price}", key=f"sell_{item}_f", disabled=count <= 0):
                game['money'] += price
                game['inventory'][item] -= 1
                if game['inventory'][item] <= 0:
                    del game['inventory'][item]
                game['sales_log'][item] = game['sales_log'].get(item, 0) + 1

                if game['money'] >= 5000:
                    game['manor_bought'] = True

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # --- RESET ---
    st.markdown("---")
    with st.expander("🔄 Reset Farm"):
        st.warning("This will delete your entire farm progress!")
        if st.button("🗑️ Reset Farm Tycoon", key="reset_farm_btn"):
            st.session_state.farm_game = None
            st.rerun()

    with st.expander("🏅 Farm Achievements"):
        for key in ["farm_harvest", "farm_rancher", "farm_winner"]:
            ach = ACHIEVEMENTS[key]
            is_unlocked = st.session_state.achievements.get(key, False)
            border_color = "var(--green-leaf)" if is_unlocked else "#444"
            bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"

            progress = ""
            if key == "farm_harvest":
                progress = "(Done)" if is_unlocked else f"({game['total_harvests']}/1)"
            elif key == "farm_rancher":
                progress = "(Done)" if is_unlocked else f"({total_animals}/5)"
            elif key == "farm_winner":
                progress = "(Done)" if is_unlocked else f"(£{game['money']}/£5000)"

            st.markdown(f"""
            <div style="background: {bg}; border: 2px solid {border_color}; border-radius: 10px; padding: 0.8rem; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 0.3rem;">{'✅' if is_unlocked else '🔒'}</span>
                        <span style="color: {'var(--green-leaf)' if is_unlocked else 'var(--cream-dim)'}; font-weight: 700;">{ach['name']}</span>
                    </div>
                    <span style="color: var(--cream-dim); font-size: 0.8rem;">{progress}</span>
                </div>
                <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">{ach['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 2: MARKET GARDEN
# ==========================================
with garden_tab:
    st.header("🌱 Market Garden")
    st.caption("📚 Companion planting, crop rotation, and soil health!")

    with st.expander("📖 How to Play — Read First!"):
        st.markdown("""
        **🖱️ Quick Start:**
        1. Select a crop from the dropdown and click an empty bed to plant
        2. **Water** your crops each day (50p per bed) or wait for rain (free!)
        3. Crops are ready when the progress bar hits 100%
        4. **Companion planting** gives yield bonuses — check the guide!
        5. **Rotate crop families** — don't plant the same family in the same bed
        6. Sell at the **Farmers' Market** — use Sell All for speed
        7. **Golden Crops** (1 in 100 chance!) sell for 10x the price 🌟

        **🤝 Companion Planting:**
        - Good companions give yield bonuses (green border)
        - Bad companions reduce yield (red border)
        - Example: Tomato + Basil = +15% yield

        **🔄 Crop Rotation:**
        - Same family in same bed = -30% yield
        - Legumes (Beans, Peas) ADD nitrogen to soil
        - Good rotation: Legume → Brassica → Root → Leaf

        **💧 Water System:**
        - Each watering costs 50p per bed
        - Rain waters ALL beds for free!
        - Build Irrigation to auto-water (upgrade)

        **🌟 Golden Crops:**
        - 1 in 100 chance when harvesting
        - Worth 10x the normal price
        - Collect all 6 Golden varieties!
        """)

    # --- GAME STATE ---
    mg = st.session_state.market_garden

    for key in ['companion_count', 'rotation_count', 'total_harvests', 'events',
                'has_polytunnel', 'fertiliser', 'organic_certified',
                'has_irrigation', 'water_saved', 'golden_found', 'rare_found']:
        if key not in mg:
            if key in ['companion_count', 'rotation_count', 'total_harvests', 'water_saved']:
                mg[key] = 0
            elif key in ['events', 'golden_found', 'rare_found']:
                mg[key] = []
            elif key in ['fertiliser']:
                mg[key] = 0
            else:
                mg[key] = False

    # --- DERIVED VALUES ---
    mg_month = get_mg_month(mg['day'])
    mg_season = get_mg_season(mg_month)
    available_crops = [name for name, data in MG_CROPS.items() if mg_season in data['season']]

    if mg.get('has_polytunnel') and mg_season == "Spring":
        summer_crops = [name for name, data in MG_CROPS.items() if "Summer" in data['season'] and name not in available_crops]
        available_crops = available_crops + summer_crops

    # --- TOP STATS ---
    g1, g2, g3, g4, g5, g6 = st.columns(6)
    g1.metric(f"{SEASON_ICONS.get(mg_season, '🌸')} Season", mg_season)
    g2.metric("📅 Month", f"{mg_month[:3]}")
    g3.metric("💰 Money", f"£{mg['money']}")
    g4.metric("💧 Water Cost", f"£{mg.get('water_saved', 0):.0f} saved")
    g5.metric("⭐ Level", f"{mg['level']} ({mg['xp']} XP)")
    g6.metric("🌾 Harvests", mg['total_harvests'])

    # --- GOLDEN COLLECTION ---
    golden_found = mg.get('golden_found', [])
    if golden_found:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
            <span style="color: var(--amber); font-weight: 600;">🌟 Golden Crops Found:</span>
            <span style="color: var(--cream);"> {', '.join(golden_found)}</span>
        </div>
        """, unsafe_allow_html=True)

    # --- EVENTS ---
    if mg['events']:
        with st.expander("📋 Recent Events", expanded=True):
            for event in mg['events'][-5:]:
                st.markdown(event)
        if len(mg['events']) > 5:
            st.caption(f"... and {len(mg['events']) - 5} more events")

    # --- WEATHER ---
    is_raining = "Rainy" in mg.get('weather', '')
    if is_raining:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0a1a2a, #1a2e3d); border: 1px solid #2196F3; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
            <span style="color: #2196F3; font-weight: 600;">🌧️ It's raining!</span>
            <span style="color: var(--cream-dim);"> All beds watered for free today.</span>
        </div>
        """, unsafe_allow_html=True)
    elif mg_season == "Winter":
        st.markdown(f"""
        <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
            <span style="color: var(--danger); font-weight: 600;">❄️ Winter:</span>
            <span style="color: var(--cream-dim);"> No crops can be planted. Browse the Seed Catalogue and plan for spring!</span>
        </div>
        """, unsafe_allow_html=True)
    elif mg_season == "Autumn":
        st.markdown(f"""
        <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
            <span style="color: var(--amber); font-weight: 600;">🍂 Autumn:</span>
            <span style="color: var(--cream-dim);"> Fewer crops available. Clear beds for winter.</span>
        </div>
        """, unsafe_allow_html=True)

    # --- SEED CATALOGUE ---
    with st.expander("🌱 Seed Catalogue"):
        st.markdown("**Available by Season:**")
        for season in ["Spring", "Summer", "Autumn", "Winter"]:
            season_crops = [name for name, data in MG_CROPS.items() if season in data['season']]
            if season_crops:
                st.markdown(f"**{SEASON_ICONS.get(season, '🌸')} {season}:**")
                crop_str = " | ".join([f"{MG_CROPS[n]['icon']} {n} (£{MG_CROPS[n]['seed_cost']})" for n in season_crops[:6]])
                st.caption(crop_str)
        st.markdown("---")
        st.markdown("**🤝 Best Companions:**")
        top_companions = list(MG_COMPANIONS.items())[:5]
        for pair, data in top_companions:
            st.caption(f"{MG_CROPS[pair[0]]['icon']} {pair[0]} + {MG_CROPS[pair[1]]['icon']} {pair[1]}: {data['bonus']}")
        st.markdown("**⚠️ Worst Companions:**")
        for pair, desc in list(MG_ANTAGONISTS.items())[:3]:
            st.caption(f"{MG_CROPS[pair[0]]['icon']} {pair[0]} + {MG_CROPS[pair[1]]['icon']} {pair[1]}: {desc}")

    st.markdown("---")

    # --- PLANTING ---
    st.markdown("### 🌱 Your Garden (12 Beds)")

    plant_crop = st.selectbox("🌱 Select crop to plant:", [""] + available_crops,
                              format_func=lambda x: f"{MG_CROPS[x]['icon']} {x} (£{MG_CROPS[x]['seed_cost']})" if x else "— Select a crop —",
                              key="mg_plant_select")

    if plant_crop:
        companions = []
        antagonists = []
        for pair, data in MG_COMPANIONS.items():
            if plant_crop in pair:
                other = pair[0] if pair[1] == plant_crop else pair[1]
                companions.append(f"{MG_CROPS[other]['icon']} {other}: {data['bonus']}")
        for pair, desc in MG_ANTAGONISTS.items():
            if plant_crop in pair:
                other = pair[0] if pair[1] == plant_crop else pair[1]
                antagonists.append(f"{MG_CROPS[other]['icon']} {other}: {desc}")
        if companions:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <span style="color: var(--green-leaf); font-weight: 600;">🤝 Companions:</span>
                <span style="color: var(--cream-dim);"> {" | ".join(companions)}</span>
            </div>
            """, unsafe_allow_html=True)
        if antagonists:
            st.markdown(f"""
            <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <span style="color: var(--danger); font-weight: 600;">⚠️ Avoid planting near:</span>
                <span style="color: var(--cream-dim);"> {" | ".join(antagonists)}</span>
            </div>
            """, unsafe_allow_html=True)

    # --- BED GRID ---
    for row in range(3):
        bed_cols = st.columns(4)
        for col_idx in range(4):
            bed_idx = row * 4 + col_idx
            bed = mg['beds'][bed_idx]
            with bed_cols[col_idx]:
                if bed['crop']:
                    crop_data = MG_CROPS[bed['crop']]
                    days_left = max(0, crop_data['days'] - bed['days'])
                    progress = min(100, int(bed['days'] / crop_data['days'] * 100))

                    companions_bed, penalties_bed = get_companion_bonus(bed_idx, bed['crop'], mg['beds'])

                    if penalties_bed:
                        st.markdown('<div style="border: 2px solid #f44336; border-radius: 8px; padding: 4px; background: #3a1a1a;">', unsafe_allow_html=True)
                    elif companions_bed:
                        st.markdown('<div style="border: 2px solid #4CAF50; border-radius: 8px; padding: 4px; background: #1a3a1a;">', unsafe_allow_html=True)

                    st.markdown(f"**Bed {bed_idx + 1}: {crop_data['icon']} {bed['crop']}**")
                    st.progress(progress / 100, text=f"{'✅ Ready!' if days_left == 0 else f'{days_left} days left'}")
                    st.caption(f"N:{get_soil_color(bed['soil_N'])}{bed['soil_N']} "
                              f"P:{get_soil_color(bed['soil_P'])}{bed['soil_P']} "
                              f"K:{get_soil_color(bed['soil_K'])}{bed['soil_K']}")

                    if companions_bed:
                        for adj_crop, bonus in companions_bed:
                            st.caption(f"🤝 +{int((bonus['yield_bonus']-1)*100)}% from {adj_crop}")
                    if penalties_bed:
                        for adj_crop, desc in penalties_bed:
                            st.caption(f"⚠️ {desc}")

                    if days_left == 0:
                        if st.button(f"🌾 Harvest", key=f"mg_harvest_{bed_idx}"):
                            yield_mult = 1.0
                            for adj_crop, bonus in companions_bed:
                                yield_mult *= bonus['yield_bonus']
                            for adj_crop, desc in penalties_bed:
                                yield_mult *= 0.7

                            if bed['history'] and bed['crop'] not in bed['history'][-2:]:
                                yield_mult *= 1.1

                            soil_avg = (bed['soil_N'] + bed['soil_P'] + bed['soil_K']) / 3
                            if soil_avg < 40:
                                yield_mult *= 0.7

                            harvest_amount = max(1, int(yield_mult * random.randint(1, 3)))

                            if random.random() < 0.01:
                                golden_name = f"Golden {bed['crop']}"
                                harvest_amount = 1
                                mg['inventory'][golden_name] = mg['inventory'].get(golden_name, 0) + 1
                                mg['events'] = mg.get('events', [])
                                mg['events'].append(f"🌟 GOLDEN {bed['crop']} FOUND! Worth 10x!")
                                if golden_name not in mg.get('golden_found', []):
                                    mg['golden_found'] = mg.get('golden_found', []) + [golden_name]
                                if not st.session_state.achievements.get('mg_golden', False):
                                    st.session_state.achievements['mg_golden'] = True
                                    st.toast("🌟 Achievement Unlocked: Golden Touch!")
                            else:
                                mg['inventory'][bed['crop']] = mg['inventory'].get(bed['crop'], 0) + harvest_amount

                            mg['total_harvests'] = mg.get('total_harvests', 0) + 1
                            mg['xp'] += 5

                            drain = crop_data['nutrient_drain']
                            bed['soil_N'] = max(0, bed['soil_N'] + drain['N'])
                            bed['soil_P'] = max(0, bed['soil_P'] + drain['P'])
                            bed['soil_K'] = max(0, bed['soil_K'] + drain['K'])

                            bed['history'].append(bed['crop'])
                            bed['crop'] = None
                            bed['days'] = 0
                            bed['watered'] = False

                            mg['events'] = mg.get('events', [])
                            if harvest_amount > 0 and 'Golden' not in str(mg['events'][-1] if mg['events'] else ''):
                                mg['events'].append(f"🌾 Harvested {harvest_amount}x {bed['crop'] if bed['crop'] else 'crop'}!")

                            if companions_bed:
                                mg['companion_count'] = mg.get('companion_count', 0) + 1
                                if not st.session_state.achievements.get('mg_companion', False):
                                    st.session_state.achievements['mg_companion'] = True
                                    st.toast("🏅 Achievement Unlocked: Companion!")

                            if not st.session_state.achievements.get('mg_first_harvest', False):
                                st.session_state.achievements['mg_first_harvest'] = True
                                st.toast("🏅 Achievement Unlocked: First Crop!")

                            st.rerun()
                    else:
                        water_cost = 0.50
                        if not bed['watered'] and not is_raining:
                            if st.button(f"💧 Water (50p)", key=f"mg_water_{bed_idx}"):
                                if mg['money'] >= water_cost:
                                    mg['money'] -= water_cost
                                    bed['watered'] = True
                                    st.toast(f"Watered {crop_data['icon']} {bed['crop']} (50p)")
                                    st.rerun()
                                else:
                                    st.error("Not enough money!")
                        elif is_raining:
                            st.caption("🌧️ Watered by rain")
                            bed['watered'] = True
                        elif bed['watered']:
                            st.caption("💧 Watered today")

                    if penalties_bed or companions_bed:
                        st.markdown('</div>', unsafe_allow_html=True)

                else:
                    # Empty bed
                    soil_avg = (bed['soil_N'] + bed['soil_P'] + bed['soil_K']) / 3
                    soil_status = "🟢 Good" if soil_avg >= 60 else ("🟡 Fair" if soil_avg >= 35 else "🔴 Poor")

                    st.markdown(f"**Bed {bed_idx + 1}: Empty**")
                    st.caption(f"Soil: {soil_status}")

                    if bed['history']:
                        last_crops = bed['history'][-2:]
                        st.caption(f"Previous: {', '.join(last_crops)}")

                    can_plant = plant_crop and mg_season in MG_CROPS[plant_crop]['season'] and mg['money'] >= MG_CROPS[plant_crop]['seed_cost']

                    rotation_warning = ""
                    if plant_crop and bed['history']:
                        last_crop = bed['history'][-1] if bed['history'] else None
                        if last_crop:
                            new_family = MG_CROPS[plant_crop]['family']
                            last_family = MG_CROPS.get(last_crop, {}).get('family', '')
                            if new_family == last_family:
                                rotation_warning = "⚠️ Same family! -30% yield"

                    if rotation_warning:
                        st.warning(rotation_warning)

                    if can_plant and st.button(f"🌱 Plant £{MG_CROPS[plant_crop]['seed_cost']}", key=f"mg_plant_{bed_idx}"):
                        cost = MG_CROPS[plant_crop]['seed_cost']
                        mg['money'] -= cost
                        bed['crop'] = plant_crop
                        bed['days'] = 0
                        bed['watered'] = is_raining
                        mg['events'] = mg.get('events', [])
                        mg['events'].append(f"🌱 Planted {plant_crop} in Bed {bed_idx + 1}")
                        st.rerun()

                    if mg['compost'] > 0 and st.button(f"🧪 Compost ({mg['compost']})", key=f"mg_compost_{bed_idx}"):
                        mg['compost'] -= 1
                        bed['soil_N'] = min(100, bed['soil_N'] + 20)
                        bed['soil_P'] = min(100, bed['soil_P'] + 20)
                        bed['soil_K'] = min(100, bed['soil_K'] + 20)
                        st.toast(f"Composted Bed {bed_idx + 1}! +20 NPK")
                        st.rerun()

                    if mg.get('fertiliser', 0) > 0 and st.button(f"🧴 Fertiliser", key=f"mg_fert_{bed_idx}"):
                        mg['fertiliser'] -= 1
                        bed['soil_N'] = min(100, bed['soil_N'] + 30)
                        bed['soil_P'] = min(100, bed['soil_P'] + 30)
                        bed['soil_K'] = min(100, bed['soil_K'] + 30)
                        st.toast(f"Fertilised Bed {bed_idx + 1}! +30 NPK")
                        st.rerun()

    # --- ACTIONS ---
    st.markdown("---")
    st.markdown("### 🛠️ Actions & Upgrades")

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.markdown("#### 🧪 Compost")
        st.caption("Make from crop waste. Apply to restore NPK.")
        st.metric("Compost", mg['compost'])
        if st.button("♻️ Make Compost (£3)", key="mg_make_compost"):
            if mg['money'] >= 3:
                mg['money'] -= 3
                mg['compost'] += 2
                mg['events'] = mg.get('events', [])
                mg['events'].append("♻️ Made 2 compost")
                st.toast("+2 Compost (-£3)")
                st.rerun()
            else:
                st.error("Need £3!")

    with a2:
        st.markdown("#### 🧴 Fertiliser")
        st.caption("Targeted NPK boost. +30 to one bed.")
        st.metric("Fertiliser", mg.get('fertiliser', 0))
        if st.button("Buy Fertiliser (£5)", key="mg_buy_fert"):
            if mg['money'] >= 5:
                mg['money'] -= 5
                mg['fertiliser'] = mg.get('fertiliser', 0) + 1
                st.toast("+1 Fertiliser")
                st.rerun()
            else:
                st.error("Need £5!")

    with a3:
        st.markdown("#### 🏗️ Upgrades")
        if not mg.get('has_polytunnel'):
            if st.button("🫧 Polytunnel (£200)", key="mg_buy_poly"):
                if mg['money'] >= 200:
                    mg['money'] -= 200
                    mg['has_polytunnel'] = True
                    mg['events'] = mg.get('events', [])
                    mg['events'].append("🫧 Built a polytunnel! Can now grow summer crops in spring.")
                    st.toast("🫧 Polytunnel built! Summer crops available in Spring!")
                    st.rerun()
                else:
                    st.error("Need £200!")
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem;">
                <span style="color: var(--green-leaf); font-weight: 600;">✅ Polytunnel built!</span>
            </div>
            """, unsafe_allow_html=True)

        if not mg.get('has_irrigation'):
            if st.button("💧 Irrigation (£150)", key="mg_buy_irrig"):
                if mg['money'] >= 150:
                    mg['money'] -= 150
                    mg['has_irrigation'] = True
                    mg['events'] = mg.get('events', [])
                    mg['events'].append("💧 Irrigation installed! All beds watered automatically.")
                    st.toast("💧 Irrigation installed!")
                    st.rerun()
                else:
                    st.error("Need £150!")
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem;">
                <span style="color: var(--green-leaf); font-weight: 600;">✅ Irrigation active!</span>
            </div>
            """, unsafe_allow_html=True)

    with a4:
        st.markdown("#### 🏷️ Certifications")
        if not mg.get('organic_certified'):
            if st.button("🏷️ Organic Cert (£500)", key="mg_buy_organic"):
                if mg['money'] >= 500:
                    mg['money'] -= 500
                    mg['organic_certified'] = True
                    mg['events'] = mg.get('events', [])
                    mg['events'].append("🏷️ Organic Certified! All sales +30%")
                    st.toast("🏷️ Organic Certified!")
                    st.rerun()
                else:
                    st.error("Need £500!")
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem;">
                <span style="color: var(--green-leaf); font-weight: 600;">✅ Organic Certified! +30% prices</span>
            </div>
            """, unsafe_allow_html=True)

    # --- MARKET ---
    st.markdown("---")
    st.markdown("### 💰 Farmers' Market")

    if mg['inventory']:
        sell_cols = st.columns(min(len([k for k, v in mg['inventory'].items() if v > 0]), 6))
        col_idx = 0
        for item, qty in list(mg['inventory'].items()):
            if qty <= 0:
                continue
            crop_data = MG_CROPS.get(item, {'icon': '📦', 'sell': 5})
            price = mg['market_prices'].get(item, crop_data['sell'])

            organic_bonus = 1.3 if mg.get('organic_certified') else 1.0
            total_price = int(price * organic_bonus)

            with sell_cols[col_idx % 6]:
                st.markdown(f"**{crop_data['icon']} {item}**")
                st.caption(f"Qty: {qty} | £{total_price}/unit")
                if st.button(f"Sell All £{total_price * qty}", key=f"mg_sell_{item}"):
                    total = total_price * qty
                    mg['money'] += total
                    mg['total_earned'] += total
                    mg['sales_log'][item] = mg['sales_log'].get(item, 0) + qty
                    mg['xp'] += 2 * qty
                    del mg['inventory'][item]
                    st.toast(f"Sold {qty}x {item} for £{total}")
                    if mg['total_earned'] >= 500 and not st.session_state.achievements.get('mg_market_master', False):
                        st.session_state.achievements['mg_market_master'] = True
                        st.toast("🏅 Achievement Unlocked: Market Master!")
                    st.rerun()
            col_idx += 1
    else:
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌾</div>
            <div style="color: var(--cream-dim);">Nothing to sell. Harvest crops first!</div>
        </div>
        """, unsafe_allow_html=True)

    # --- END DAY ---
    st.markdown("---")
    st.markdown(f"""
    <div style="background: var(--info-bg); border: 1px solid #2196F3; border-radius: 10px; padding: 0.8rem 1rem;">
        <span style="color: #2196F3;">⏰</span>
        <span style="color: var(--cream-dim);"> Current: {SEASON_ICONS.get(mg_season, '🌸')} {mg_season} — {mg_month[:3]} Wk{get_week_in_month(mg['day'])} | 💧 Watering: {'FREE (rain!)' if is_raining else '50p/bed'}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⏭️ Advance Day", use_container_width=True, key="mg_advance"):
        mg['day'] += 1
        mg['events'] = []

        new_month = get_mg_month(mg['day'])
        new_season = get_mg_season(new_month)

        # Weather
        weather_roll = random.random()
        if new_season == "Summer":
            mg['weather'] = "☀️ Sunny" if weather_roll < 0.5 else ("⛅ Cloudy" if weather_roll < 0.75 else "🌧️ Rainy")
        elif new_season == "Winter":
            mg['weather'] = "🌧️ Rainy" if weather_roll < 0.4 else ("⛅ Cloudy" if weather_roll < 0.7 else "☀️ Sunny")
        else:
            mg['weather'] = "☀️ Sunny" if weather_roll < 0.4 else ("⛅ Cloudy" if weather_roll < 0.7 else "🌧️ Rainy")

        is_raining = "Rainy" in mg['weather']

        # Calculate water cost
        water_cost = 0
        if mg.get('has_irrigation'):
            water_cost = 1
            for bed in mg['beds']:
                bed['watered'] = True
        elif is_raining:
            water_cost = 0
            for bed in mg['beds']:
                bed['watered'] = True
            mg['water_saved'] = mg.get('water_saved', 0) + 0.50 * sum(1 for b in mg['beds'] if b['crop'])
        else:
            for bed in mg['beds']:
                if bed['crop'] and not bed['watered']:
                    water_cost += 0.50

        mg['money'] -= water_cost
        if water_cost > 0:
            mg['events'] = mg.get('events', [])
            mg['events'].append(f"💧 Watering cost: £{water_cost:.2f}")

        # Process beds
        for bed in mg['beds']:
            if bed['crop'] and new_season != "Winter":
                crop_data = MG_CROPS[bed['crop']]
                if bed['watered'] or is_raining:
                    bed['days'] += 1
                    bed['soil_N'] = min(100, bed['soil_N'] + 1)
                    bed['soil_P'] = min(100, bed['soil_P'] + 1)
                    bed['soil_K'] = min(100, bed['soil_K'] + 1)
                bed['watered'] = False

                soil_avg = (bed['soil_N'] + bed['soil_P'] + bed['soil_K']) / 3
                if soil_avg < 30:
                    mg['events'] = mg.get('events', [])
                    mg['events'].append(f"⚠️ Bed soil is poor — yields reduced!")

            elif bed['crop'] is None:
                bed['soil_N'] = min(100, bed['soil_N'] + 3)
                bed['soil_P'] = min(100, bed['soil_P'] + 3)
                bed['soil_K'] = min(100, bed['soil_K'] + 3)

            # Winter kills non-herb crops
            if bed['crop'] and new_season == "Winter":
                crop_data = MG_CROPS[bed['crop']]
                if crop_data['family'] != 'Herb':
                    bed_idx_pos = mg['beds'].index(bed)
                    mg['events'] = mg.get('events', [])
                    mg['events'].append(f"❄️ {bed['crop']} in Bed {bed_idx_pos+1} killed by frost!")
                    bed['history'].append(bed['crop'])
                    bed['crop'] = None
                    bed['days'] = 0

        # Random weather events
        if new_season != "Winter" and random.random() < 0.1:
            event = random.choice(["frost", "pests", "wind"])
            if event == "frost" and new_season == "Spring":
                for bed in mg['beds']:
                    if bed['crop'] and not bed['watered']:
                        bed['days'] = max(0, bed['days'] - 1)
                mg['events'] = mg.get('events', [])
                mg['events'].append("🥶 Late frost! Unwatered crops lost a day.")
            elif event == "pests":
                mg['events'] = mg.get('events', [])
                mg['events'].append("🐛 Pest outbreak! Companion planting helps protect crops.")

        # Market price fluctuations
        for item in list(mg['market_prices'].keys()):
            if item in mg.get('sales_log', {}) and mg['sales_log'].get(item, 0) > 10:
                mg['market_prices'][item] = max(1, int(MG_MARKET_BASE.get(item, 3) * 0.8))
            else:
                mg['market_prices'][item] = min(
                    MG_MARKET_BASE.get(item, 3) + 5,
                    int(MG_MARKET_BASE.get(item, 3) * random.uniform(0.9, 1.1))
                )
        mg['sales_log'] = {}

        # Level up
        level_thresholds = {1: 0, 2: 30, 3: 100, 4: 250, 5: 500}
        for lvl, xp_needed in sorted(level_thresholds.items(), reverse=True):
            if mg['xp'] >= xp_needed:
                if mg['level'] < lvl:
                    mg['level'] = lvl
                    mg['events'] = mg.get('events', [])
                    mg['events'].append(f"⭐ Level up! Now level {lvl}!")
                    st.toast(f"⭐ Level Up! You're now Level {lvl}!")
                break

        st.rerun()

    # --- RESET ---
    st.markdown("---")
    with st.expander("🔄 Reset Market Garden"):
        st.warning("This will delete your garden progress!")
        if st.button("🗑️ Reset Market Garden", key="reset_mg"):
            st.session_state.market_garden = None
            st.rerun()
