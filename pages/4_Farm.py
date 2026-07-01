import streamlit as st
import random
from datetime import datetime

from utils import init_session_state, apply_brand_theme, render_save_load
from auth import render_auth, render_logout_sidebar
from game_config import (ACHIEVEMENTS, SEASON_ICONS, FARM_ICONS, FARM_BUILDINGS,
                         SEED_COST, BASE_PRICES, BASICS, MG_CROPS, MG_COMPANIONS,
                         MG_ANTAGONISTS, MG_SEASONS, MG_MARKET_BASE)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Farm Games - Rocen Homesteady",
    page_icon="🚜",
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
    .market-box div.stButton > button { font-size: 14px !important; white-space: normal !important;
                                          height: auto !important; padding: 5px !important; }
    @media (max-width: 768px) {
        div.grid-game div.stButton > button { font-size: 1em !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- INIT ---
init_session_state()
apply_brand_theme()
user = render_auth()
render_logout_sidebar()

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

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("🌿 **Rocen Homesteady**")
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

for key in ['companion_count', 'rotation_count', 'total_harvests', 'events']:
    if key not in mg:
        mg[key] = 0 if key != 'events' else []

# --- TITLE AND TABS ---
st.title("🚜 Farm Games")
st.caption("Grow crops, raise animals, and master the market!")

farm_tab, garden_tab = st.tabs(["🚜 Farm Tycoon", "🌱 Market Garden"])

# ==========================================
# TAB 1: FARM TYCOON
# ==========================================
with farm_tab:
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
        st.success("🏆 **FARMING DYNASTY COMPLETE!**")
        st.markdown(f"**Final Money:** £{game['money']} | **Days:** {game['day']} | **Harvests:** {game['total_harvests']}")
        if st.button("🔄 Start New Farm", key="restart_farm_win"):
            st.session_state.farm_game = None
            st.rerun()

    if game['last_event']:
        event_str = game['last_event'].strip()
        if event_str:
            st.warning(f"**Report:** {event_str}")

    if game['market_event']:
        st.info(f"📈 **Market Surge:** {game['market_event']} prices have doubled!")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Year", f"{current_year} - {current_season}")
    c2.metric("💰 Money", f"£{game['money']}")
    c3.metric("🐔 Chickens", chickens if current_year >= 2 else "🔒 Y2")
    c4.metric("🐄 Cows / 🐐 Goats", f"{cows}/{goats}" if current_year >= 2 else "🔒 Y2")

    if current_season == "Autumn":
        st.warning("🍂 **AUTUMN:** Winter is coming! Build a Cold Frame to protect crops!")
    elif current_season == "Winter":
        if has_cold_frame:
            st.info("❄️ **WINTER:** Crops protected by Cold Frame! 🫧")
        else:
            st.error("❄️ **WINTER:** Crops will die! Build a Cold Frame next year.")

    inv_str = " | ".join([f"**{k}:** {v}" for k, v in game['inventory'].items() if v > 0])
    st.markdown(f"**🎒 Stock:** {inv_str if inv_str else 'Empty'}")

    feed_needed = chickens + (cows * 2) + goats
    if total_animals > 0:
        feed_color = "🟢" if game['inventory'].get('Feed', 0) >= feed_needed else "🔴"
        st.caption(f"{feed_color} Feed Needed: {feed_needed}/day | Feed in Stock: {game['inventory'].get('Feed', 0)}")

    st.markdown("---")
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

    st.markdown("---")
    st.markdown("#### 🏭 Feed Production")
    f1, f2 = st.columns(2)
    with f1:
        st.write("**Recipe:** 1 Wheat + 1 Carrot + 1 Corn = 5 Feed")
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
            st.success("+5 Feed Bags")
            st.rerun()

    st.markdown("---")
    if st.button("⏭️ End Day", use_container_width=True, key="end_day_farm"):
        game['last_event'] = ""

        for item, qty in game['sales_log'].items():
            if qty > 10:
                game['market_prices'][item] = max(1, int(BASE_PRICES.get(item, 10) * 0.8))
            else:
                game['market_prices'][item] = min(
                    BASE_PRICES.get(item, 10) + 5,
                    int(BASE_PRICES.get(item, 10) * 1.05)
                )
        game['sales_log'] = {}
        game['market_event'] = None

        if random.random() < 0.2:
            surge_crop = random.choice(["Carrot", "Wheat", "Corn"])
            game['market_event'] = surge_crop
            game['last_event'] += f"📈 {surge_crop} SURGE! "

        is_drought = (
            current_season == "Summer"
            and random.random() < 0.3
            and not any(11 in row for row in game['grid'])
        )
        is_pest_event = (
            current_season != "Winter"
            and random.random() < 0.2
            and not any(10 in row for row in game['grid'])
        )

        if is_drought:
            game['last_event'] += "☀️ DROUGHT! "
        if is_pest_event:
            game['last_event'] += "🐛 PESTS! "

        for r in range(5):
            for c in range(6):
                tile = game['grid'][r][c]

                if tile == 0:
                    game['fallow_days'][r][c] += 1
                    game['soil_health'][r][c] = min(100, game['soil_health'][r][c] + 5)
                    if game['fallow_days'][r][c] > 3 and random.random() < 0.2:
                        game['grid'][r][c] = 7
                        game['fallow_days'][r][c] = 0

                elif tile in [2, 3]:
                    game['fallow_days'][r][c] = 0
                    if current_season == "Winter" and not has_cold_frame:
                        game['grid'][r][c] = 0
                        game['crop_map'].pop((r, c), None)
                        game['last_event'] += "❄️ Winter Kill. "
                    elif not is_drought:
                        game['grid'][r][c] = tile + 1

                    if is_pest_event and random.random() < 0.4:
                        game['grid'][r][c] = 0
                        game['crop_map'].pop((r, c), None)

                elif tile == 9:
                    game['inventory']['Honey'] = game['inventory'].get('Honey', 0) + 1

                elif tile == 12:
                    if game['inventory'].get('Feed', 0) >= 1:
                        game['inventory']['Feed'] -= 1
                        game['inventory']['Egg'] = game['inventory'].get('Egg', 0) + 1
                    elif game['inventory'].get('Wheat', 0) >= 1:
                        game['inventory']['Wheat'] -= 1
                        game['inventory']['Egg'] = game['inventory'].get('Egg', 0) + 1
                    else:
                        game['last_event'] += "🐔 Hungry! "

                elif tile == 13:
                    if game['inventory'].get('Feed', 0) >= 2:
                        game['inventory']['Feed'] -= 2
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    elif game['inventory'].get('Wheat', 0) >= 2:
                        game['inventory']['Wheat'] -= 2
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    else:
                        game['last_event'] += "🐄 Hungry! "

                elif tile == 14:
                    if game['inventory'].get('Feed', 0) >= 1:
                        game['inventory']['Feed'] -= 1
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    elif game['inventory'].get('Wheat', 0) >= 1:
                        game['inventory']['Wheat'] -= 1
                        game['inventory']['Milk'] = game['inventory'].get('Milk', 0) + 1
                    else:
                        game['last_event'] += "🐐 Hungry! "

        if game['total_harvests'] >= 1 and not st.session_state.achievements.get('farm_harvest', False):
            st.session_state.achievements['farm_harvest'] = True
            st.toast("🏅 Achievement Unlocked: Green Thumb!")

        if total_animals >= 5 and not st.session_state.achievements.get('farm_rancher', False):
            st.session_state.achievements['farm_rancher'] = True
            st.toast("🏅 Achievement Unlocked: Rancher!")

        if game['money'] >= 5000 and not st.session_state.achievements.get('farm_winner', False):
            st.session_state.achievements['farm_winner'] = True
            st.toast("🏅 Achievement Unlocked: Farming Dynasty!")

        game['day'] += 1
        st.rerun()

    st.markdown("#### 🗺️ Farm")

    for r in range(5):
        cols = st.columns(6)
        for c in range(6):
            tile_val = game['grid'][r][c]
            icon = FARM_ICONS.get(tile_val, "❓")

            with cols[c]:
                if tile_val == 7:
                    if st.button("🧹", key=f"fm_w_{r}_{c}"):
                        game['grid'][r][c] = 0
                        game['fallow_days'][r][c] = 0
                        st.rerun()

                elif tile_val == 0:
                    if game['build_sel'] != "None":
                        b_name = game['build_sel']
                        b_data = FARM_BUILDINGS.get(b_name, None)
                        if b_data:
                            if b_name in ["Chicken Coop", "Cow Pasture", "Goat Pen"] and current_year < 2:
                                st.warning("🔒 Unlock in Year 2")
                            else:
                                if st.button("🏗️", key=f"fm_b_{r}_{c}"):
                                    if game['money'] >= b_data['cost']:
                                        game['money'] -= b_data['cost']
                                        game['grid'][r][c] = b_data['id']
                                        game['build_sel'] = "None"
                                        st.rerun()
                                    else:
                                        st.error(f"Need £{b_data['cost']}")
                    else:
                        if st.button("🌱", key=f"fm_p_{r}_{c}"):
                            crop = game['tool']
                            cost = SEED_COST.get(crop, 6)
                            if game['money'] >= cost:
                                game['money'] -= cost
                                game['grid'][r][c] = 2
                                game['crop_map'][(r, c)] = crop
                                game['fallow_days'][r][c] = 0
                                st.rerun()
                            else:
                                st.error(f"Need £{cost}")

                elif tile_val == 4:
                    if st.button("🌾", key=f"fm_h_{r}_{c}"):
                        crop = game['crop_map'].get((r, c), "Carrot")
                        yield_count = 1
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 5 and 0 <= nc < 6:
                                if game['grid'][nr][nc] == 9:
                                    yield_count += 1

                        harvested = max(1, int(yield_count * (game['soil_health'][r][c] / 100)))

                        game['inventory'][crop] = game['inventory'].get(crop, 0) + harvested
                        game['grid'][r][c] = 0
                        game['soil_health'][r][c] = max(0, game['soil_health'][r][c] - 10)
                        game['crop_map'].pop((r, c), None)
                        game['fallow_days'][r][c] = 0
                        game['total_harvests'] += 1

                        if game['total_harvests'] >= 1 and not st.session_state.achievements.get('farm_harvest', False):
                            st.session_state.achievements['farm_harvest'] = True
                            st.toast("🏅 Achievement Unlocked: Green Thumb!")

                        st.toast(f"+{harvested} {crop}")
                        st.rerun()

                else:
                    if tile_val in [2, 3]:
                        soil = game['soil_health'][r][c]
                        crop_name = game['crop_map'].get((r, c), "?")
                        st.button(icon, key=f"fm_v_{r}_{c}", disabled=True,
                                  help=f"{crop_name} - Soil: {soil}%")
                        st.progress(max(1, soil // 10))
                    else:
                        st.button(icon, key=f"fm_v_{r}_{c}", disabled=True)

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

    st.markdown("---")
    with st.expander("🔄 Reset Farm"):
        st.warning("This will delete your entire farm progress!")
        if st.button("🗑️ Reset Farm Tycoon", key="reset_farm_btn"):
            st.session_state.farm_game = None
            st.rerun()

    with st.expander("🏅 Farm Achievements"):
        for key in ["farm_harvest", "farm_rancher", "farm_winner"]:
            ach = ACHIEVEMENTS[key]
            status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
            progress = ""
            if key == "farm_harvest":
                progress = "(Done)" if st.session_state.achievements.get(key, False) else f"({game['total_harvests']}/1)"
            elif key == "farm_rancher":
                progress = "(Done)" if st.session_state.achievements.get(key, False) else f"({total_animals}/5)"
            elif key == "farm_winner":
                progress = "(Done)" if st.session_state.achievements.get(key, False) else f"(£{game['money']}/£5000)"
            st.markdown(f"**{status} {ach['name']}**\n- *{ach['desc']}* {progress}")

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
            'has_polytunnel': False, 'fertiliser': 0,
            'organic_certified': False, 'has_irrigation': False,
            'water_saved': 0, 'golden_found': [], 'rare_found': [],
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

    # Polytunnel extends spring to include summer crops
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
        st.success(f"🌟 **Golden Crops Found:** {', '.join(golden_found)}")

    # --- EVENTS ---
    if mg['events']:
        with st.expander("📋 Recent Events", expanded=True):
            for event in mg['events'][-5:]:
                st.markdown(event)

    # --- WEATHER ---
    is_raining = "Rainy" in mg.get('weather', '')
    if is_raining:
        st.success("🌧️ **It's raining!** All beds watered for free today.")
    elif mg_season == "Winter":
        st.error("❄️ **Winter:** No crops can be planted. Browse the Seed Catalogue and plan for spring!")
    elif mg_season == "Autumn":
        st.warning("🍂 **Autumn:** Fewer crops available. Clear beds for winter.")

    # --- SEED CATALOGUE (always available, useful in winter) ---
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
            st.success("🤝 **Companions:** " + " | ".join(companions))
        if antagonists:
            st.error("⚠️ **Avoid planting near:** " + " | ".join(antagonists))

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

                    companions, penalties = get_companion_bonus(bed_idx, bed['crop'], mg['beds'])

                    if penalties:
                        st.markdown('<div style="border: 2px solid #f44336; border-radius: 8px; padding: 4px; background: #3a1a1a;">', unsafe_allow_html=True)
                    elif companions:
                        st.markdown('<div style="border: 2px solid #4CAF50; border-radius: 8px; padding: 4px; background: #1a3a1a;">', unsafe_allow_html=True)

                    st.markdown(f"**Bed {bed_idx + 1}: {crop_data['icon']} {bed['crop']}**")
                    st.progress(progress / 100, text=f"{'✅ Ready!' if days_left == 0 else f'{days_left} days left'}")
                    st.caption(f"N:{get_soil_color(bed['soil_N'])}{bed['soil_N']} "
                              f"P:{get_soil_color(bed['soil_P'])}{bed['soil_P']} "
                              f"K:{get_soil_color(bed['soil_K'])}{bed['soil_K']}")

                    if companions:
                        for adj_crop, bonus in companions:
                            st.caption(f"🤝 +{int((bonus['yield_bonus']-1)*100)}% from {adj_crop}")
                    if penalties:
                        for adj_crop, desc in penalties:
                            st.caption(f"⚠️ {desc}")

                    if days_left == 0:
                        if st.button(f"🌾 Harvest", key=f"mg_harvest_{bed_idx}"):
                            yield_mult = 1.0
                            for adj_crop, bonus in companions:
                                yield_mult *= bonus['yield_bonus']
                            for adj_crop, desc in penalties:
                                yield_mult *= 0.7

                            if bed['history'] and bed['crop'] not in bed['history'][-2:]:
                                yield_mult *= 1.1

                            # Soil penalty for low NPK
                            soil_avg = (bed['soil_N'] + bed['soil_P'] + bed['soil_K']) / 3
                            if soil_avg < 40:
                                yield_mult *= 0.7

                            harvest_amount = max(1, int(yield_mult * random.randint(1, 3)))

                            # Golden crop chance (1 in 100)
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

                            if companions:
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

                    if penalties or companions:
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
            st.success("✅ Polytunnel built!")

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
            st.success("✅ Irrigation active!")

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
            st.success("✅ Organic Certified! +30% prices")

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
                if col_idx % 6 == 0 and col_idx > 0:
                    sell_cols = st.columns(6)
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
        st.info("Nothing to sell. Harvest crops first!")

    # --- END DAY ---
    st.markdown("---")
    st.info(f"📅 **Current:** {SEASON_ICONS.get(mg_season, '🌸')} {mg_season} — {mg_month} | 💧 Watering: {'FREE (rain!)' if is_raining else '50p/bed'}")

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
            # Irrigation: auto-water, costs 1 per day total
            water_cost = 1
            for bed in mg['beds']:
                bed['watered'] = True
        elif is_raining:
            # Rain waters everything for free
            water_cost = 0
            for bed in mg['beds']:
                bed['watered'] = True
            mg['water_saved'] = mg.get('water_saved', 0) + 0.50 * sum(1 for b in mg['beds'] if b['crop'])
        else:
            # Manual watering needed
            for bed in mg['beds']:
                if bed['crop'] and not bed['watered']:
                    water_cost += 0.50

        mg['money'] -= water_cost
        if water_cost > 0:
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
                mg['events'].append("🥶 Late frost! Unwatered crops lost a day.")
            elif event == "pests":
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
