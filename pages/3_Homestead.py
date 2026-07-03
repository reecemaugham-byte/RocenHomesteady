import streamlit as st
import random
from datetime import datetime

from utils import init_session_state, apply_brand_theme, render_save_load
from game_config import (ACHIEVEMENTS, SEASON_ICONS, VILLAGE_ITEMS, VILLAGE_BUILDINGS, VILLAGE_PRODUCTION,
                         KITCHEN_RECIPES, BASICS)
from plants_data import UK_PLANTS

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Homestead - Rocen Homesteady",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIT ---
init_session_state()
apply_brand_theme()

if 'achievements' not in st.session_state or not st.session_state.achievements:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}

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

    st.markdown("#### 🏘️ Village Achievements")
    for key in ["eco_survivor", "eco_wealth"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements[key] else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("#### 🍳 Kitchen Achievements")
    for key in ["kitchen_apprentice", "kitchen_master"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements[key] else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("---")
    st.caption("📚 Curriculum: Science (Ecosystems, Sustainability), DT (Cooking & Nutrition)")

st.title("🏘️ Homestead Games")

tab1, tab2 = st.tabs(["🏘️ Eco-Village", "🍳 The Wild Kitchen"])

# ==========================================
# TAB 1: ECO-VILLAGE
# ==========================================
with tab1:
    st.header("🏘️ Eco-Village Builder")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Forage:** Gather resources from the woods or sell items found in **Foraging Games**.
        2. **Build:** Place buildings on your land to produce resources.
        3. **Produce:** Use the 🏭 Production section to turn raw goods into valuable items.
        4. **Market:** Sell items for money. Processed goods are worth much more than raw!
        5. **⚠️ Winter:** Solar panels stop. Nature stops growing. **Stockpile food before winter!**
        6. **Cold Frame 🫧:** Produces +3 Food/day even in winter.
        7. **Smokehouse 🥓:** Cook Smoked Fish and Jerky without needing Power.
        8. **Storage:** Build a Barn to increase your inventory limit.

        **💡 Tip:** Dandelion Tea is worth 25x more than raw Dandelions. Invest in production!
        """)

    # --- GAME STATE INIT ---
    if st.session_state.get('village') is None:
        grid = [['🌲' for _ in range(6)] for _ in range(4)]
        stream_col = random.randint(1, 4)
        for r in range(4):
            grid[r][stream_col] = '🌊'

        st.session_state.village = {
            'grid': grid,
            'stats': {
                'Food': 50, 'Water': 50, 'Power': 0,
                'Stamina': 100, 'Money': 100, 'Max_Power': 20, 'Storage_Limit': 10
            },
            'inventory': {},
            'owned_buildings': {},
            'placing_mode': None,
            'day': 1,
            'season': 'Spring',
            'nature_health': 100,
            'damaged_buildings': []
        }

    game = st.session_state.village

    # --- MIGRATIONS ---
    if 'Storage_Limit' not in game['stats']:
        game['stats']['Storage_Limit'] = 10
    if 'season' not in game:
        game['season'] = 'Spring'
    if 'damaged_buildings' not in game:
        game['damaged_buildings'] = []
    if 'nature_health' not in game:
        game['nature_health'] = 100
    if 'owned_buildings' not in game:
        game['owned_buildings'] = {}
    if 'placing_mode' not in game:
        game['placing_mode'] = None
    if 'Max_Power' not in game['stats']:
        game['stats']['Max_Power'] = 20

    ITEMS = VILLAGE_ITEMS.copy()
    BUILDINGS = VILLAGE_BUILDINGS.copy()
    PRODUCTION = VILLAGE_PRODUCTION.copy()

    for plant in UK_PLANTS['edible']:
        name = plant['name']
        if name not in ITEMS:
            ITEMS[name] = {"icon": "🌿", "rarity": 0.0, "value": 3, "food": 2}

    has_cold_frame = any('🫧' in row for row in game['grid'])
    has_smokehouse = any('🥓' in row for row in game['grid'])

    current_season = game['season']
    current_storage = sum(game['inventory'].values())
    max_storage = game['stats']['Storage_Limit']

    # --- WIN/LOSE ---
    if game['stats']['Money'] >= 5000:
        st.markdown(f"""
        <div class="level-up">
            <div style="font-size: 3rem;">🏆</div>
            <div style="color: var(--amber); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">VILLAGE TYCOON!</div>
            <div style="color: var(--cream); font-size: 1rem; margin-top: 0.5rem;">You've built a thriving community!</div>
        </div>
        """, unsafe_allow_html=True)

    if game['stats']['Food'] <= 0 or game['stats']['Water'] <= 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 3rem;">💀</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">GAME OVER</div>
            <div style="color: var(--cream-dim); font-size: 1rem; margin-top: 0.5rem;">Your village starved. Try again!</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Restart Village", key="restart_village_gameover"):
            st.session_state.village = None
            st.rerun()

    # --- RENDER STATS ---
    s = game['stats']
    season_colour = {"Spring": "#4CAF50", "Summer": "#FFC107", "Autumn": "#FF8F00", "Winter": "#90CAF9"}.get(current_season, "#4CAF50")

    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber-dark); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--amber); font-size: 0.75rem; font-weight: 600;">{SEASON_ICONS.get(current_season, '🌸')} SEASON</div>
            <div style="color: var(--cream); font-size: 1.1rem; font-weight: 700;">{current_season} — Day {game['day']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("🍖 Food", s['Food'])
    c2.metric("💧 Water", s['Water'])
    c3.metric("⚡ Power", f"{s['Power']}/{s['Max_Power']}")
    c4.metric("💰 Money", f"£{s['Money']}")
    nature = game['nature_health']
    c5.metric("🌿 Nature", f"{nature}%")
    c6.metric("📦 Storage", f"{current_storage}/{max_storage}")

    # --- WINTER WARNING ---
    if current_season == "Autumn":
        st.markdown(f"""
        <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem;">
            <span style="color: var(--amber); font-weight: 600;">🍂 AUTUMN WARNING:</span>
            <span style="color: var(--cream-dim);"> Winter is coming! Stockpile food and build a Cold Frame!</span>
        </div>
        """, unsafe_allow_html=True)
    elif current_season == "Winter":
        if has_cold_frame:
            st.markdown(f"""
            <div style="background: var(--info-bg); border: 1px solid #2196F3; border-radius: 10px; padding: 0.8rem 1rem;">
                <span style="color: #2196F3; font-weight: 600;">❄️ WINTER:</span>
                <span style="color: var(--cream-dim);"> Crops protected by Cold Frame! 🫧</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 0.8rem 1rem;">
                <span style="color: var(--danger); font-weight: 600;">❄️ WINTER:</span>
                <span style="color: var(--cream-dim);"> Solar panels offline. Nature dormant. Cold Frame still produces food.</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    map_tab, forage_tab = st.tabs(["🗺️ Village Map", "🎒 Market & Pantry"])

    # ==========================================
    # VILLAGE MAP
    # ==========================================
    with map_tab:
        if game['placing_mode']:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber); border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
                <span style="color: var(--amber); font-weight: 700;">📍 Placing Mode:</span>
                <span style="color: var(--cream-dim);"> Click a 🌲 tile to build <b>{game['placing_mode']}</b>.</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("❌ Cancel Placement", key="cancel_placement"):
                cost = BUILDINGS[game['placing_mode']]['cost']
                game['stats']['Money'] += cost
                game['placing_mode'] = None
                st.rerun()

        st.markdown("#### 🗺️ Your Land")

        for row_idx, row in enumerate(game['grid']):
            cols = st.columns(6)
            for col_idx, tile in enumerate(row):
                current_tile = game['grid'][row_idx][col_idx]
                is_damaged = (row_idx, col_idx) in game['damaged_buildings']

                with cols[col_idx]:
                    st.markdown('<div class="grid-game">', unsafe_allow_html=True)

                    if game['placing_mode'] and current_tile == '🌲':
                        b_name = game['placing_mode']
                        b_icon = BUILDINGS[b_name]['icon']
                        if st.button(f"📍{b_icon}", key=f"v_place_{row_idx}_{col_idx}"):
                            game['grid'][row_idx][col_idx] = b_icon
                            if b_name not in game['owned_buildings']:
                                game['owned_buildings'][b_name] = 0
                            game['owned_buildings'][b_name] += 1
                            if b_name == "Barn":
                                game['stats']['Storage_Limit'] += 20
                            game['placing_mode'] = None
                            st.rerun()

                    elif current_tile == '🌊':
                        disable_fishing = (current_season == "Winter")
                        if st.button("🎣", key=f"v_fish_{row_idx}_{col_idx}", disabled=disable_fishing):
                            if game['stats']['Stamina'] >= 5:
                                game['stats']['Stamina'] -= 5
                                game['inventory']['Fish'] = game['inventory'].get('Fish', 0) + 1
                                st.toast("🎣 Caught Fish!")
                                st.rerun()
                            else:
                                st.error("Need Stamina")

                    elif is_damaged:
                        b_data = next((v for k, v in BUILDINGS.items() if v['icon'] == current_tile), None)
                        repair_cost = b_data['repair'] if b_data else 10
                        if st.button(f"🛠️ £{repair_cost}", key=f"v_rep_{row_idx}_{col_idx}"):
                            if game['stats']['Money'] >= repair_cost:
                                game['stats']['Money'] -= repair_cost
                                game['damaged_buildings'].remove((row_idx, col_idx))
                                st.toast("Repaired!")
                                st.rerun()
                            else:
                                st.error(f"Need £{repair_cost}")

                    else:
                        st.button(tile, key=f"v_view_{row_idx}_{col_idx}", disabled=True)

                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🛠️ Build")

        if not game['placing_mode']:
            build_cols = st.columns(len(BUILDINGS))
            for i, (name, data) in enumerate(BUILDINGS.items()):
                with build_cols[i]:
                    st.caption(data['desc'])
                    if st.button(f"{data['icon']} {name} - £{data['cost']}", key=f"buy_{name}", use_container_width=True):
                        if game['stats']['Money'] >= data['cost']:
                            game['stats']['Money'] -= data['cost']
                            game['placing_mode'] = name
                            st.rerun()
                        else:
                            st.error(f"Need £{data['cost']}")

        # --- END DAY ---
        if st.button("⏭️ End Day (Survive)", use_container_width=True, key="end_day_village"):
            game['day'] += 1

            day_in_cycle = game['day'] % 40
            if day_in_cycle < 10:
                game['season'] = "Spring"
            elif day_in_cycle < 20:
                game['season'] = "Summer"
            elif day_in_cycle < 30:
                game['season'] = "Autumn"
            else:
                game['season'] = "Winter"

            game['stats']['Food'] = max(0, game['stats']['Food'] - 1)
            game['stats']['Water'] = max(0, game['stats']['Water'] - 1)
            game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)

            for r in range(4):
                for c in range(6):
                    tile = game['grid'][r][c]
                    if (r, c) in game['damaged_buildings']:
                        continue

                    current_season_local = game['season']

                    if current_season_local == "Winter":
                        if tile in ['🔋', '☀️']:
                            continue
                        if tile == '🌳':
                            continue

                    if tile == '🏠':
                        game['stats']['Stamina'] = min(100, game['stats']['Stamina'] + 20)
                    elif tile == '🪨':
                        game['stats']['Water'] += 5
                    elif tile == '🐔':
                        game['inventory']['Eggs'] = game['inventory'].get('Eggs', 0) + 1
                    elif tile == '🔋':
                        game['stats']['Power'] = min(game['stats']['Max_Power'], game['stats']['Power'] + 2)
                    elif tile == '☀️':
                        game['stats']['Power'] = min(50, game['stats']['Power'] + 10)
                    elif tile == '🌳':
                        game['nature_health'] = min(100, game['nature_health'] + 10)
                    elif tile == '🌴':
                        game['inventory']['Apple'] = game['inventory'].get('Apple', 0) + 2
                        game['inventory']['Pear'] = game['inventory'].get('Pear', 0) + 2
                        game['inventory']['Orange'] = game['inventory'].get('Orange', 0) + 2
                    elif tile == '🫧':
                        game['stats']['Food'] += 3
                    elif tile == '🥓':
                        if game['nature_health'] >= 2:
                            game['inventory']['Wood'] = game['inventory'].get('Wood', 0) + 1
                            game['nature_health'] = max(0, game['nature_health'] - 2)

            if random.random() < 0.15:
                protected_tiles = ['🌲', '🌊', '🫧', '🥓']
                buildings = [
                    (r, c, game['grid'][r][c])
                    for r in range(4) for c in range(6)
                    if game['grid'][r][c] not in protected_tiles
                    and (r, c) not in game['damaged_buildings']
                ]
                if buildings:
                    r, c, icon = random.choice(buildings)
                    game['damaged_buildings'].append((r, c))
                    b_data = next((v for k, v in BUILDINGS.items() if v['icon'] == icon), {})
                    repair_cost = b_data.get('repair', 10)
                    st.toast(f"⚠️ Building {icon} damaged! Repair for £{repair_cost}")

            if game['day'] >= 30 and not st.session_state.achievements['eco_survivor']:
                st.session_state.achievements['eco_survivor'] = True
                st.toast("🏅 Achievement Unlocked: Settler!")
            if game['stats']['Money'] >= 2000 and not st.session_state.achievements['eco_wealth']:
                st.session_state.achievements['eco_wealth'] = True
                st.toast("🏅 Achievement Unlocked: Eco-Tycoon!")

            st.rerun()

    # ==========================================
    # MARKET & PANTRY
    # ==========================================
    with forage_tab:
        st.markdown("### 🌲 Gather & Market")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 🌿 Actions")
            disable_forage = (current_season == "Winter")

            if game['nature_health'] < 20:
                st.markdown(f"""
                <div style="background: var(--danger-bg); border: 1px solid var(--danger); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                    <span style="color: var(--danger); font-weight: 600;">⚠️ Nature depleted!</span>
                    <span style="color: var(--cream-dim);"> Build a Reserve to restore it.</span>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🌲 Forage in Woods", key="forage_woods", disabled=disable_forage):
                if game['stats']['Stamina'] >= 10:
                    if game['nature_health'] >= 5:
                        game['stats']['Stamina'] -= 10
                        game['nature_health'] = max(0, game['nature_health'] - 5)
                        found = [
                            name for name, data in ITEMS.items()
                            if random.random() < data.get('rarity', 0)
                            and name in ["Wood", "Stone"]
                        ]
                        for f in found:
                            if sum(game['inventory'].values()) < max_storage:
                                game['inventory'][f] = game['inventory'].get(f, 0) + 1
                        if found:
                            st.success(f"Found: {', '.join(found)}")
                        else:
                            st.info("Nothing found this time.")
                        st.rerun()
                    else:
                        st.error("Nature exhausted! Build a Reserve.")
                else:
                    st.error("Need Stamina")

            if current_season in ["Spring", "Summer"]:
                if st.button("🌸 Forage in Meadows", key="forage_meadow"):
                    if game['stats']['Stamina'] >= 10:
                        if game['nature_health'] >= 5:
                            game['stats']['Stamina'] -= 10
                            game['nature_health'] = max(0, game['nature_health'] - 5)
                            seasonal_plants = [
                                p for p in UK_PLANTS['edible']
                                if any(m in SEASON_ICONS and SEASON_MONTHS.get(current_season, []) and m in SEASON_MONTHS[current_season] for m in p.get('months', []))
                            ]
                            if seasonal_plants and random.random() < 0.4:
                                found_plant = random.choice(seasonal_plants)
                                plant_name = found_plant['name']
                                if sum(game['inventory'].values()) < max_storage:
                                    game['inventory'][plant_name] = game['inventory'].get(plant_name, 0) + 1
                                    st.success(f"Found: {plant_name}!")
                                else:
                                    st.warning("Storage full!")
                            else:
                                st.info("Nothing found this time.")
                            st.rerun()
                        else:
                            st.error("Nature exhausted!")
                    else:
                        st.error("Need Stamina")

            if st.button("🎣 Fish at Stream", key="forage_fish"):
                if game['stats']['Stamina'] >= 5:
                    game['stats']['Stamina'] -= 5
                    game['inventory']['Fish'] = game['inventory'].get('Fish', 0) + 1
                    st.toast("🎣 Caught a Fish!")
                    st.rerun()
                else:
                    st.error("Need Stamina")

            st.markdown("##### 🏭 Production")

            for recipe_name, recipe in PRODUCTION.items():
                needs_power = recipe.get('power', 0) > 0
                has_power = game['stats']['Power'] >= recipe.get('power', 0) or not needs_power

                if recipe.get('smokehouse') and has_smokehouse:
                    has_power = True

                has_ingredients = all(
                    game['inventory'].get(ing, 0) >= qty
                    for ing, qty in recipe['ingredients'].items()
                    if ing not in BASICS
                )
                has_space = (sum(game['inventory'].values()) + recipe.get('qty', 1)) <= max_storage

                ing_str = ", ".join([
                    f"{i}x{q}" for i, q in recipe['ingredients'].items()
                ])
                pwr_str = f" ⚡{recipe['power']}" if recipe.get('power', 0) > 0 else ""
                smoke_str = " 🥓" if recipe.get('smokehouse') else ""

                can_craft = has_power and has_ingredients and has_space

                if st.button(
                    f"Make {recipe_name} ({ing_str}{pwr_str}{smoke_str})",
                    disabled=not can_craft,
                    key=f"make_{recipe_name}"
                ):
                    for ing, qty in recipe['ingredients'].items():
                        if ing not in BASICS:
                            game['inventory'][ing] -= qty
                            if game['inventory'][ing] <= 0:
                                del game['inventory'][ing]

                    if recipe.get('power', 0) > 0 and not (recipe.get('smokehouse') and has_smokehouse):
                        game['stats']['Power'] -= recipe['power']

                    out = recipe['output']
                    game['inventory'][out] = game['inventory'].get(out, 0) + recipe.get('qty', 1)
                    st.toast(f"Made {recipe_name}!")
                    st.rerun()

        with col2:
            st.markdown("#### 💰 Market & Pantry")
            st.caption(f"Storage: {current_storage}/{max_storage}")

            combined_inventory = {}
            for item_name, count in game['inventory'].items():
                if count > 0:
                    combined_inventory[item_name] = combined_inventory.get(item_name, 0) + count
            for item_name, count in st.session_state.master_inventory.items():
                if count > 0:
                    combined_inventory[item_name] = combined_inventory.get(item_name, 0) + count

            if not combined_inventory:
                st.markdown(f"""
                <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
                    <div style="color: var(--cream-dim);">Empty — Forage in Foraging Games or produce here!</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                hdr_cols = st.columns([2, 1, 1, 1])
                hdr_cols[0].write("**Item**")
                hdr_cols[1].write("**Qty**")
                hdr_cols[2].write("**Eat**")
                hdr_cols[3].write("**Sell**")

                for item_name, count in sorted(combined_inventory.items()):
                    if count <= 0:
                        continue

                    data = ITEMS.get(item_name, {'value': 3, 'food': 0, 'icon': '❓'})
                    val = data.get('value', 3)
                    food_val = data.get('food', 0)
                    icon = data.get('icon', '❓')

                    row_cols = st.columns([2, 1, 1, 1])
                    row_cols[0].write(f"{icon} {item_name}")
                    row_cols[1].write(f"{count}")

                    if food_val > 0:
                        if row_cols[2].button("🍽️", key=f"eat_{item_name}",
                                              help=f"Restores {food_val} Food"):
                            game['stats']['Food'] += food_val
                            if item_name in game['inventory'] and game['inventory'][item_name] > 0:
                                game['inventory'][item_name] -= 1
                                if game['inventory'][item_name] <= 0:
                                    del game['inventory'][item_name]
                            elif item_name in st.session_state.master_inventory and st.session_state.master_inventory[item_name] > 0:
                                st.session_state.master_inventory[item_name] -= 1
                                if st.session_state.master_inventory[item_name] <= 0:
                                    del st.session_state.master_inventory[item_name]
                            st.toast(f"+{food_val} Food")
                            st.rerun()
                    else:
                        row_cols[2].write("—")

                    if row_cols[3].button(f"£{val}", key=f"sell_btn_{item_name}"):
                        if item_name in game['inventory'] and game['inventory'][item_name] > 0:
                            game['inventory'][item_name] -= 1
                            if game['inventory'][item_name] <= 0:
                                del game['inventory'][item_name]
                        elif item_name in st.session_state.master_inventory and st.session_state.master_inventory[item_name] > 0:
                            st.session_state.master_inventory[item_name] -= 1
                            if st.session_state.master_inventory[item_name] <= 0:
                                del st.session_state.master_inventory[item_name]

                        game['stats']['Money'] += val
                        st.toast(f"Sold {item_name} for £{val}")

                        if game['stats']['Money'] >= 2000 and not st.session_state.achievements['eco_wealth']:
                            st.session_state.achievements['eco_wealth'] = True
                            st.toast("🏅 Achievement Unlocked: Eco-Tycoon!")
                        st.rerun()

    # --- ACHIEVEMENT DISPLAY ---
    st.markdown("---")
    with st.expander("🏅 Eco-Village Achievements"):
        for key in ["eco_survivor", "eco_wealth"]:
            ach = ACHIEVEMENTS[key]
            is_unlocked = st.session_state.achievements[key]
            border_color = "var(--green-leaf)" if is_unlocked else "#444"
            bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"

            progress = ""
            if key == "eco_survivor":
                progress = f"({game['day']}/30 days)" if not is_unlocked else "(Done)"
            elif key == "eco_wealth":
                progress = f"(£{game['stats']['Money']}/£2000)" if not is_unlocked else "(Done)"

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

        # Building summary
        st.markdown("---")
        st.markdown("**🏘️ Your Buildings:**")
        if game.get('owned_buildings'):
            for bname, count in game['owned_buildings'].items():
                if count > 0:
                    bdata = BUILDINGS.get(bname, {})
                    st.write(f"{bdata.get('icon', '🏠')} {bname}: {count}")
        else:
            st.caption("No buildings yet. Start building!")

    # --- RESET ---
    with st.expander("🔄 Reset Village"):
        st.warning("This will delete your entire village progress!")
        if st.button("🗑️ Reset Eco-Village", key="reset_village_btn"):
            st.session_state.village = None
            st.rerun()

# ==========================================
# TAB 2: THE WILD KITCHEN
# ==========================================
with tab2:
    st.header("🍳 The Wild Kitchen")
    st.caption("📚 Process your harvest. Master the prep. Unlock new difficulties!")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Inventory:** Your pantry is filled by **Foraging Games**. Go foraging first!
        2. **Progression:** Unlock **3 Beginner** recipes to access Intermediate.
        3. **Unlocking:** Click a recipe, answer the safety questions, and click "Submit".
        4. **Cooking:** Once unlocked, cook the recipe using ingredients from your Pantry.
        5. **Sell:** Cooked dishes can be sold in **Eco-Village** for good money!
        """)

    # --- PANTRY SETUP ---
    inv = st.session_state.master_inventory
    total_edible = len(UK_PLANTS['edible'])

    if not inv:
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🥗</div>
            <div style="color: var(--cream-dim);">Your Pantry is empty! Go **Foraging in Foraging Games** to find ingredients.</div>
        </div>
        """, unsafe_allow_html=True)

    # --- PROGRESSION LOGIC ---
    beginner_unlocked = len([
        r for r in st.session_state.unlocked_recipes
        if any(x['name'] == r and x['diff'] == 1 for x in KITCHEN_RECIPES)
    ])
    inter_unlocked = len([
        r for r in st.session_state.unlocked_recipes
        if any(x['name'] == r and x['diff'] == 2 for x in KITCHEN_RECIPES)
    ])
    adv_unlocked = len([
        r for r in st.session_state.unlocked_recipes
        if any(x['name'] == r and x['diff'] == 3 for x in KITCHEN_RECIPES)
    ])

    def get_difficulty_stars(diff):
        return "⭐" * diff + "☆" * (3 - diff)

    # --- LAYOUT ---
    col_main, col_side = st.columns([2, 1])

    with col_side:
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <div style="color: var(--amber); font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;">🎒 Pantry</div>
        </div>
        """, unsafe_allow_html=True)

        if not inv:
            st.info("Empty — Forage items in Foraging Games")
        else:
            st.markdown("**Your Ingredients:**")
            for item, qty in sorted(inv.items()):
                if qty > 0:
                    st.write(f"- **{item}:** {qty}")

        st.markdown("---")
        st.markdown("**🔧 Basics (Unlimited)**")
        st.caption(", ".join(BASICS))

        st.markdown("---")
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 12px; padding: 1rem;">
            <div style="color: var(--amber); font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;">🏆 Progress</div>
            <div style="color: var(--cream); font-size: 0.9rem;">Kitchen Score: <b>{st.session_state.kitchen_score}</b></div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">Beginner: {beginner_unlocked}/3 ✅</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem;">Intermediate: {inter_unlocked}/8 🔒</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem;">Advanced: {adv_unlocked}/7 🔒</div>
        </div>
        """, unsafe_allow_html=True)

    with col_main:
        st.markdown("### 📖 Recipe Book")
        r1, r2, r3 = st.tabs(["⭐ Beginner", "⭐⭐ Intermediate", "⭐⭐⭐ Advanced"])

        def render_recipe_tab(recipe_list, container, locked=False, req_count=0):
            if locked:
                st.markdown(f"""
                <div style="background: var(--bg-card); border: 2px dashed #555; border-radius: 12px; padding: 2rem; text-align: center;">
                    <div style="font-size: 2rem;">🔒</div>
                    <div style="color: var(--cream-dim); font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem;">Unlock {req_count} recipes to access this tier.</div>
                    <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">Complete more Beginner recipes to progress!</div>
                </div>
                """, unsafe_allow_html=True)
                return

            for recipe in recipe_list:
                with container:
                    is_unlocked = recipe['name'] in st.session_state.unlocked_recipes
                    has_ingredients = all(
                        inv.get(ing, 0) >= qty
                        for ing, qty in recipe['ingredients'].items()
                        if ing not in BASICS
                    )

                    diff_stars = get_difficulty_stars(recipe['diff'])
                    border_color = "var(--green-leaf)" if is_unlocked else "#555"
                    bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"

                    with st.expander(f"{recipe['icon']} {recipe['name']} {diff_stars}"):
                        st.markdown(f"**{recipe['desc']}**")
                        st.info(f"**Health Benefits:** {recipe.get('benefits', 'Nutritious wild food.')}")
                        st.markdown("---")

                        # Ingredients
                        st.markdown("**Ingredients Needed:**")
                        ing_cols = st.columns(len(recipe['ingredients']))
                        for i, (ing, qty) in enumerate(recipe['ingredients'].items()):
                            current_qty = inv.get(ing, 0)
                            is_basic = ing in BASICS
                            status = "✅" if current_qty >= qty or is_basic else "❌"
                            with ing_cols[i]:
                                st.metric(f"{status} {ing}", f"{current_qty}/{qty}")

                        st.markdown("---")

                        if not is_unlocked:
                            st.markdown(f"""
                            <div style="background: #3d2e0a; border: 1px solid var(--amber); border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                                <div style="color: var(--amber); font-weight: 700;">🔒 Preparation Required</div>
                                <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">
                                    Answer {len(recipe['prep_questions'])} question(s) to unlock this recipe.
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            for i, q_data in enumerate(recipe['prep_questions']):
                                st.radio(f"Q{i+1}: {q_data['q']}", q_data['opts'],
                                        key=f"q_{recipe['name']}_{i}")

                            if st.button("Submit Answers", key=f"submit_{recipe['name']}"):
                                passed = True
                                for i, q_data in enumerate(recipe['prep_questions']):
                                    key = f"q_{recipe['name']}_{i}"
                                    selected = st.session_state.get(key)
                                    if selected != q_data['a']:
                                        passed = False

                                if passed:
                                    st.session_state.unlocked_recipes.append(recipe['name'])

                                    if recipe['diff'] == 1:
                                        count = len([
                                            r for r in st.session_state.unlocked_recipes
                                            if any(x['name'] == r and x['diff'] == 1 for x in KITCHEN_RECIPES)
                                        ])
                                        if count >= 3 and not st.session_state.achievements['kitchen_apprentice']:
                                            st.session_state.achievements['kitchen_apprentice'] = True
                                            st.toast("🏅 Achievement Unlocked: Apprentice!")

                                    if recipe['diff'] == 2:
                                        total_inter = len([r for r in KITCHEN_RECIPES if r['diff'] == 2])
                                        unlocked_inter = len([
                                            r for r in st.session_state.unlocked_recipes
                                            if any(x['name'] == r and x['diff'] == 2 for x in KITCHEN_RECIPES)
                                        ])
                                        if unlocked_inter == total_inter and not st.session_state.achievements['kitchen_master']:
                                            st.session_state.achievements['kitchen_master'] = True
                                            st.toast("🏅 Achievement Unlocked: Master Chef!")

                                    st.success(f"✅ Correct! **{recipe['name']}** Unlocked!")
                                    st.rerun()
                                else:
                                    st.error("❌ Incorrect. Review the safety notes and try again!")

                        else:
                            if has_ingredients:
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 1px solid var(--green-leaf); border-radius: 10px; padding: 0.8rem 1rem; text-align: center; margin: 0.5rem 0;">
                                    <span style="color: var(--green-leaf); font-weight: 600;">✅ Ready to Cook!</span>
                                </div>
                                """, unsafe_allow_html=True)
                                if st.button(f"🍳 Cook {recipe['name']}", key=f"cook_{recipe['name']}"):
                                    for ing, qty in recipe['ingredients'].items():
                                        if ing not in BASICS:
                                            st.session_state.master_inventory[ing] -= qty
                                            if st.session_state.master_inventory[ing] <= 0:
                                                del st.session_state.master_inventory[ing]

                                    result_dish = recipe['name']
                                    st.session_state.master_inventory[result_dish] = (
                                        st.session_state.master_inventory.get(result_dish, 0) + recipe.get('qty', 1)
                                    )

                                    points = recipe['diff'] * 15
                                    st.session_state.kitchen_score += points

                                    st.toast(f"Made {recipe['name']}! +{points} XP")
                                    st.rerun()
                            else:
                                missing = [
                                    f"{ing} ({inv.get(ing, 0)}/{qty})"
                                    for ing, qty in recipe['ingredients'].items()
                                    if ing not in BASICS and inv.get(ing, 0) < qty
                                ]
                                st.markdown(f"""
                                <div style="background: #3d2e0a; border: 1px solid var(--amber-dark); border-radius: 10px; padding: 0.8rem 1rem; margin: 0.5rem 0;">
                                    <div style="color: var(--amber); font-weight: 600;">🧺 Missing Ingredients</div>
                                    <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">{', '.join(missing)}</div>
                                    <div style="color: var(--cream-dim); font-size: 0.8rem; margin-top: 0.3rem;">💡 Go foraging in Foraging Games to find ingredients!</div>
                                </div>
                                """, unsafe_allow_html=True)

        beginner_recipes = [r for r in KITCHEN_RECIPES if r['diff'] == 1]
        inter_recipes = [r for r in KITCHEN_RECIPES if r['diff'] == 2]
        adv_recipes = [r for r in KITCHEN_RECIPES if r['diff'] == 3]

        render_recipe_tab(beginner_recipes, r1, locked=False)

        inter_locked = beginner_unlocked < 3
        render_recipe_tab(inter_recipes, r2, locked=inter_locked, req_count=3)

        adv_locked = inter_unlocked < 3
        render_recipe_tab(adv_recipes, r3, locked=adv_locked, req_count=3)

    # --- ACHIEVEMENT DISPLAY ---
    st.markdown("---")
    with st.expander("🏅 Kitchen Achievements"):
        for key in ["kitchen_apprentice", "kitchen_master"]:
            ach = ACHIEVEMENTS[key]
            is_unlocked = st.session_state.achievements[key]
            border_color = "var(--green-leaf)" if is_unlocked else "#444"
            bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"

            progress = ""
            if key == "kitchen_apprentice":
                progress = f"({beginner_unlocked}/3)" if not is_unlocked else "(Done)"
            elif key == "kitchen_master":
                total_inter = len([r for r in KITCHEN_RECIPES if r['diff'] == 2])
                progress = f"({inter_unlocked}/{total_inter})" if not is_unlocked else "(Done)"

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

        # Recipe collection tracker
        total_recipes = len(KITCHEN_RECIPES)
        total_unlocked = len(st.session_state.unlocked_recipes)
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.8rem 1rem; text-align: center; margin-top: 0.5rem;">
            <span style="color: var(--amber); font-weight: 700;">📖 Recipes Unlocked: {total_unlocked}/{total_recipes}</span>
        </div>
        """, unsafe_allow_html=True)
