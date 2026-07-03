import streamlit as st
import random
import time
from datetime import datetime

from utils import init_session_state, apply_brand_theme, render_save_load
from auth import render_auth, render_logout_sidebar
from game_config import (ACHIEVEMENTS, HABITAT_ICONS, SEASON_ICONS, SEASON_MONTHS,
                         SURVIVAL_DIFFICULTY)
from plants_data import UK_PLANTS
from audio_utils import generate_voice, clean_text_for_audio, is_tts_available

# --- TTS CHECK ---
EDGE_TTS_AVAILABLE = is_tts_available()

# --- SAFE RANDOM SAMPLE HELPER ---
def safe_sample(population, k):
    """Safely sample k items from population. Never crashes on empty lists or negative k."""
    if not population or k <= 0:
        return []
    k = min(k, len(population))
    return random.sample(population, k)

# --- HELPER: GENERATE FORAGING QUESTION ---
def generate_foraging_question(plant):
    """Generate one of 6 question types from a plant dict."""
    question_types = ['habitat', 'identification', 'lookalike', 'parts', 'season', 'warning']

    # Fallback if plant lacks data for certain types
    if not plant.get('lookalikes'):
        question_types = [t for t in question_types if t != 'lookalike']
    if not plant.get('parts'):
        question_types = [t for t in question_types if t != 'parts']
    if not plant.get('warnings'):
        question_types = [t for t in question_types if t != 'warning']

    if not question_types:
        question_types = ['habitat', 'identification']

    q_type = random.choice(question_types)
    all_plant_names = [p['name'] for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']]
    id_keys = plant.get('id_keys', {})

    if q_type == 'habitat':
        correct = plant.get('habitat', 'Various')
        wrong_habitats = ["Woodlands", "Meadows", "Coastal cliffs", "Riverbanks",
                          "Hedgerows", "Marshes", "Moors", "Gardens", "Wasteland"]
        wrong_options = [h for h in wrong_habitats if h != correct]
        options = [correct] + safe_sample(wrong_options, 3)
        random.shuffle(options)
        clue = ""
        if id_keys:
            features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
            clue = "; ".join([f"{k} is {v}" for k, v in features])
        elif plant.get('description'):
            clue = plant['description'][:120]
        return {
            'type': 'habitat',
            'question': f"Where would you most likely find **{plant['name']}**?",
            'options': options,
            'correct': correct,
            'explanation': f"{plant['name']} typically grows in {correct}.",
            'points': 10
        }

    elif q_type == 'identification':
        if id_keys:
            key_feature = random.choice(list(id_keys.items()))
            feature_key, feature_val = key_feature
            correct = feature_val
            wrong_options = [v for k, v in id_keys.items() if v != correct]
            other_vals = [v for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']
                         for k, v in p.get('id_keys', {}).items() if v != correct]
            sample_size = max(0, 3 - len(wrong_options))
            wrong_options += safe_sample(other_vals, sample_size)
            wrong_options = list(set(wrong_options))[:3]
            options = [correct] + wrong_options
            while len(options) < 4:
                options.append("None of these")
            random.shuffle(options)
            return {
                'type': 'identification',
                'question': f"What is the **{feature_key}** of **{plant['name']}**?",
                'options': options,
                'correct': correct,
                'explanation': f"The {feature_key} of {plant['name']} is {feature_val}.",
                'points': 10
            }
        else:
            correct = plant.get('category', 'Plant')
            categories = ["Plant", "Tree", "Shrub", "Fungi", "Coastal", "Seaweed", "Shellfish"]
            wrong = [c for c in categories if c != correct]
            options = [correct] + safe_sample(wrong, 3)
            random.shuffle(options)
            return {
                'type': 'identification',
                'question': f"What type of organism is **{plant['name']}**?",
                'options': options,
                'correct': correct,
                'explanation': f"{plant['name']} is a {correct}.",
                'points': 10
            }

    elif q_type == 'lookalike':
        lookalikes = plant.get('lookalikes', [])
        dangerous = [la for la in lookalikes if la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']]
        if dangerous:
            chosen = random.choice(dangerous)
            correct = chosen['name']
            other_names = [n for n in all_plant_names if n != plant['name'] and n != correct]
            wrong = safe_sample(other_names, 3)
            options = [correct] + wrong
            while len(options) < 4:
                options.append("None of these")
            random.shuffle(options)
            confusion = plant.get('confusion_notes', chosen.get('diff', 'Check carefully!'))
            return {
                'type': 'lookalike',
                'question': f"Which is the DANGEROUS lookalike of **{plant['name']}**?",
                'options': options,
                'correct': correct,
                'explanation': f"{chosen['name']} is dangerous ({chosen.get('danger', 'Unknown')}): {chosen.get('diff', confusion)}",
                'points': 15
            }
        else:
            return generate_foraging_question_fallback(plant)

    elif q_type == 'parts':
        raw_parts = plant.get('parts', 'Leaves')
        if isinstance(raw_parts, str):
            parts_list = [p.strip() for p in raw_parts.split(',')]
        else:
            parts_list = raw_parts
        if not parts_list:
            parts_list = ['Leaves']
        correct = parts_list[0]
        wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark", "Stem", "Tubers"]
        wrong = [p for p in wrong_parts if p not in parts_list]
        options = [correct] + safe_sample(wrong, 3)
        while len(options) < 4:
            options.append("None of these")
        random.shuffle(options)
        return {
            'type': 'parts',
            'question': f"Which part of **{plant['name']}** can you eat?",
            'options': options,
            'correct': correct,
            'explanation': f"You can eat the {', '.join(parts_list)} of {plant['name']}.",
            'points': 10
        }

    elif q_type == 'season':
        correct_months = plant.get('months', ['Summer'])
        if isinstance(correct_months, str):
            correct_months = [correct_months]
        correct = random.choice(correct_months)
        all_months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        wrong = [m for m in all_months if m not in correct_months]
        options = [correct] + safe_sample(wrong, 3)
        random.shuffle(options)
        return {
            'type': 'season',
            'question': f"When is **{plant['name']}** best foraged?",
            'options': options,
            'correct': correct,
            'explanation': f"{plant['name']} is best in {', '.join(correct_months)}.",
            'points': 10
        }

    elif q_type == 'warning':
        warning = plant.get('warnings', '')
        if warning:
            if random.random() < 0.5:
                return {
                    'type': 'warning',
                    'question': f"True or False: {warning}",
                    'options': ["True", "False"],
                    'correct': "True",
                    'explanation': f"This is a real warning about {plant['name']}.",
                    'points': 10
                }
            else:
                false_warning = warning
                swaps = [("cook", "eat raw"), ("edible", "poisonous"),
                         ("safe", "dangerous"), ("must", "don't need to"),
                         ("hairy", "smooth"), ("never", "always")]
                for orig, swap in swaps:
                    if orig.lower() in false_warning.lower():
                        false_warning = false_warning.lower().replace(orig.lower(), swap.lower())
                        false_warning = false_warning[0].upper() + false_warning[1:]
                        break
                if false_warning != warning:
                    return {
                        'type': 'warning',
                        'question': f"True or False: {false_warning}",
                        'options': ["True", "False"],
                        'correct': "False",
                        'explanation': f"That's FALSE. The real warning is: {warning}",
                        'points': 15
                    }
        return generate_foraging_question_fallback(plant)

    return generate_foraging_question_fallback(plant)


def generate_foraging_question_fallback(plant):
    """Fallback question when specific type can't be generated."""
    correct = plant.get('habitat', 'Various')
    wrong_habitats = ["Woodlands", "Meadows", "Coastal cliffs", "Riverbanks",
                      "Hedgerows", "Marshes", "Moors"]
    wrong = [h for h in wrong_habitats if h != correct]
    options = [correct] + safe_sample(wrong, 3)
    random.shuffle(options)
    return {
        'type': 'habitat',
        'question': f"Where would you most likely find **{plant['name']}**?",
        'options': options,
        'correct': correct,
        'explanation': f"{plant['name']} typically grows in {correct}.",
        'points': 10
    }


# --- HELPER: GENERATE SURVIVAL CASES ---
def generate_survival_cases():
    """Generate survival cases from real plant data, pairing edibles with poisonous lookalikes."""
    cases = []

    for edible in UK_PLANTS['edible']:
        lookalikes = edible.get('lookalikes', [])
        for la in lookalikes:
            if not isinstance(la, dict):
                continue
            danger = la.get('danger', '')
            if danger not in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']:
                continue

            danger_plant = None
            for p in UK_PLANTS['poisonous']:
                if p['name'] == la['name']:
                    danger_plant = p
                    break

            if not danger_plant:
                continue

            id_keys = edible.get('id_keys', {})
            if id_keys:
                clue_parts = [f"{k}: {v}" for k, v in list(id_keys.items())[:3]]
                clue = "You notice: " + "; ".join(clue_parts) + "."
            else:
                clue = f"You notice a plant growing in {edible.get('habitat', 'the countryside')}."

            confusion = edible.get('confusion_notes', '')
            diff = la.get('diff', '')
            if confusion:
                rule = confusion
            elif diff:
                rule = f"Key difference: {diff}"
            else:
                rule = f"Check carefully — {la['name']} is dangerous!"

            fact_parts = [f"**{edible['name']}** is edible."]
            if diff:
                fact_parts.append(f"The dangerous lookalike **{la['name']}** differs: {diff}")
            if confusion:
                fact_parts.append(f"Key ID note: {confusion}")
            fact = " ".join(fact_parts)

            if danger in ['DEADLY', 'EXTREME']:
                level = 2
            else:
                level = 1

            cases.append({
                'safe_plant': edible['name'],
                'safe_icon': '🌿',
                'danger_plant': la['name'],
                'danger_icon': '☠️',
                'safe_habitat': edible.get('habitat', 'Various'),
                'clue': clue,
                'rule': rule,
                'fact': fact,
                'level': level
            })

    if len(cases) < 10:
        for poison in UK_PLANTS['poisonous']:
            confusion = poison.get('confusion_notes', '')
            if not confusion:
                continue

            for edible in UK_PLANTS['edible']:
                if edible['name'].lower() in confusion.lower():
                    id_keys = edible.get('id_keys', {})
                    if id_keys:
                        clue_parts = [f"{k}: {v}" for k, v in list(id_keys.items())[:3]]
                        clue = "You notice: " + "; ".join(clue_parts) + "."
                    else:
                        clue = f"You notice a plant growing in {edible.get('habitat', 'the countryside')}."

                    diff = ""
                    for la in edible.get('lookalikes', []):
                        if isinstance(la, dict) and la.get('name') == poison['name']:
                            diff = la.get('diff', '')
                            break

                    rule = confusion if confusion else f"Beware: {poison['name']} looks similar!"

                    fact = f"**{edible['name']}** is safe, but **{poison['name']}** is {poison.get('danger_tips', {}).get('danger_zone', 'dangerous')}."
                    if diff:
                        fact += f" Difference: {diff}"

                    danger_level = poison.get('danger_tips', {}).get('danger_zone', '')
                    level = 2 if danger_level in ['DEADLY', 'EXTREME'] else 1

                    existing = [c for c in cases if c['safe_plant'] == edible['name'] and c['danger_plant'] == poison['name']]
                    if not existing:
                        cases.append({
                            'safe_plant': edible['name'],
                            'safe_icon': '🌿',
                            'danger_plant': poison['name'],
                            'danger_icon': '☠️',
                            'safe_habitat': edible.get('habitat', 'Various'),
                            'clue': clue,
                            'rule': rule,
                            'fact': fact,
                            'level': level
                        })
                    break

    if len(cases) < 5:
        for edible in UK_PLANTS['edible'][:10]:
            for poison in UK_PLANTS['poisonous'][:3]:
                existing = [c for c in cases if c['safe_plant'] == edible['name'] and c['danger_plant'] == poison['name']]
                if not existing:
                    id_keys = edible.get('id_keys', {})
                    if id_keys:
                        clue_parts = [f"{k}: {v}" for k, v in list(id_keys.items())[:2]]
                        clue = "You notice: " + "; ".join(clue_parts) + "."
                    else:
                        clue = f"A plant found in {edible.get('habitat', 'the countryside')}."

                    danger_zone = poison.get('danger_tips', {}).get('danger_zone', 'POISONOUS')
                    rule = f"Always double-check: {poison['name']} is {danger_zone}!"
                    fact = f"**{edible['name']}** is edible. **{poison['name']}** is {danger_zone}."
                    level = 2 if danger_zone in ['DEADLY', 'EXTREME'] else 1

                    cases.append({
                        'safe_plant': edible['name'],
                        'safe_icon': '🌿',
                        'danger_plant': poison['name'],
                        'danger_icon': '☠️',
                        'safe_habitat': edible.get('habitat', 'Various'),
                        'clue': clue,
                        'rule': rule,
                        'fact': fact,
                        'level': level
                    })

    hard_edibles = [p for p in UK_PLANTS['edible'] if p.get('difficulty', 1) >= 3]
    for edible in hard_edibles:
        lookalikes = edible.get('lookalikes', [])
        for la in lookalikes:
            if not isinstance(la, dict):
                continue
            if la.get('danger', '') in ['DEADLY', 'EXTREME']:
                existing = [c for c in cases if c['safe_plant'] == edible['name'] and c['danger_plant'] == la['name']]
                if existing:
                    existing[0]['level'] = 3
                    continue

                id_keys = edible.get('id_keys', {})
                if id_keys:
                    clue_parts = [f"{k}: {v}" for k, v in list(id_keys.items())[:3]]
                    clue = "You notice: " + "; ".join(clue_parts) + ". Be very careful."
                else:
                    clue = f"A tricky plant in {edible.get('habitat', 'the countryside')}."

                confusion = edible.get('confusion_notes', la.get('diff', 'Check very carefully!'))
                rule = f"EXPERT LEVEL: {confusion}"
                diff = la.get('diff', '')
                fact = f"**{edible['name']}** is edible but easily confused with **{la['name']}** ({la.get('danger', 'DANGER')})."
                if diff:
                    fact += f" Key difference: {diff}"

                cases.append({
                    'safe_plant': edible['name'],
                    'safe_icon': '🌿',
                    'danger_plant': la['name'],
                    'danger_icon': '☠️',
                    'safe_habitat': edible.get('habitat', 'Various'),
                    'clue': clue,
                    'rule': rule,
                    'fact': fact,
                    'level': 3
                })

    seen = set()
    unique_cases = []
    for c in cases:
        key = (c['safe_plant'], c['danger_plant'])
        if key not in seen:
            seen.add(key)
            unique_cases.append(c)

    if not unique_cases:
        unique_cases.append({
            'safe_plant': 'Nettle',
            'safe_icon': '🌿',
            'danger_plant': 'Deadly Nightshade',
            'danger_icon': '☠️',
            'safe_habitat': 'Hedgerows and wasteland',
            'clue': 'You notice: a tall plant with jagged leaves and stinging hairs.',
            'rule': 'Always check for stinging hairs — Nettle has them, Deadly Nightshade does not.',
            'fact': '**Nettle** is edible when cooked. **Deadly Nightshade** is extremely poisonous.',
            'level': 1
        })

    return unique_cases


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Games - Rocen Homesteady",
    page_icon="🎮",
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
    .plant-card {
        border-radius: 20px; padding: 20px; text-align: center;
        background: linear-gradient(145deg, #2b2b2b, #1a1a1a);
        box-shadow: 10px 10px 20px #1a1a1a; margin-bottom: 20px; border: 1px solid #444;
    }
    .market-box div.stButton > button { font-size: 14px !important; white-space: normal !important;
                                          height: auto !important; padding: 5px !important; }
    @media (max-width: 768px) {
        .plant-card { padding: 10px !important; }
        div.grid-game div.stButton > button { font-size: 1em !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- INIT ---
init_session_state()
apply_brand_theme()
user = render_auth()
render_logout_sidebar()

# Initialize Achievements if not exists or empty
if 'achievements' not in st.session_state or not st.session_state.achievements:
    st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}

# Initialize cases_solved for survival
if 'survival_cases_solved' not in st.session_state:
    st.session_state.survival_cases_solved = 0

# Initialize game state keys if missing
if 'game_score' not in st.session_state:
    st.session_state.game_score = 0
if 'game_lives' not in st.session_state:
    st.session_state.game_lives = 3
if 'game_streak' not in st.session_state:
    st.session_state.game_streak = 0
if 'bonus_round' not in st.session_state:
    st.session_state.bonus_round = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'survival_lives' not in st.session_state:
    st.session_state.survival_lives = 3
if 'survival_score' not in st.session_state:
    st.session_state.survival_score = 0
if 'survival_correct_count' not in st.session_state:
    st.session_state.survival_correct_count = 0
if 'survival_level' not in st.session_state:
    st.session_state.survival_level = 1
if 'survival_current_case' not in st.session_state:
    st.session_state.survival_current_case = None
if 'survival_result' not in st.session_state:
    st.session_state.survival_result = None
if 'survival_seen' not in st.session_state:
    st.session_state.survival_seen = []
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_q_num' not in st.session_state:
    st.session_state.quiz_q_num = 0
if 'q_data' not in st.session_state:
    st.session_state.q_data = None
if 'daily_streak' not in st.session_state:
    st.session_state.daily_streak = 0
if 'quiz_lives_remaining' not in st.session_state:
    st.session_state.quiz_lives_remaining = 3
if 'quiz_plants_seen' not in st.session_state:
    st.session_state.quiz_plants_seen = []
if 'challenge_completed' not in st.session_state:
    st.session_state.challenge_completed = False
if 'total_plants_identified' not in st.session_state:
    st.session_state.total_plants_identified = 0
if 'player_title' not in st.session_state:
    st.session_state.player_title = "Novice Gatherer"
if 'season_badge_progress' not in st.session_state:
    st.session_state.season_badge_progress = []
if 'master_inventory' not in st.session_state:
    st.session_state.master_inventory = {}
if 'quiz_max' not in st.session_state:
    st.session_state.quiz_max = 10

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

    st.markdown("#### 🌿 Foraging Achievements")
    for key in ["foraging_novice", "foraging_botanist", "foraging_master"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("#### ☠️ Survival Achievements")
    for key in ["survival_scout", "survival_expert", "survival_detective"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("#### 🎲 Quiz Achievements")
    for key in ["quiz_streak", "quiz_challenger"]:
        ach = ACHIEVEMENTS[key]
        status = "✅" if st.session_state.achievements.get(key, False) else "🔒"
        st.caption(f"{status} {ach['name']}")

    st.markdown("---")
    st.caption("📚 Curriculum: Science (Plants, Seasonal Changes), PSHE (Safety)")

    # Reset Button
    st.markdown("---")
    if st.button("🔄 Reset All Games"):
        st.session_state.game_score = 0
        st.session_state.game_lives = 3
        st.session_state.game_streak = 0
        st.session_state.bonus_round = False
        st.session_state.current_question = None
        st.session_state.survival_lives = 3
        st.session_state.survival_score = 0
        st.session_state.survival_correct_count = 0
        st.session_state.survival_level = 1
        st.session_state.survival_cases_solved = 0
        st.session_state.survival_current_case = None
        st.session_state.survival_result = None
        st.session_state.survival_seen = []
        st.session_state.quiz_score = 0
        st.session_state.quiz_q_num = 0
        st.session_state.q_data = None
        st.session_state.daily_streak = 0
        st.session_state.quiz_lives_remaining = 3
        st.session_state.quiz_plants_seen = []
        st.session_state.challenge_completed = False
        st.session_state.total_plants_identified = 0
        st.session_state.player_title = "Novice Gatherer"
        st.session_state.season_badge_progress = []
        st.session_state.master_inventory = {}
        st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}
        st.success("All Games Reset!")
        st.rerun()

st.title("🎮 Games & Practice")

tab1, tab2, tab3 = st.tabs([
    "🌿 Foraging Quest",
    "☠️ Survival School",
    "🎲 Daily Quiz"
])

# ==========================================
# GAME TAB 1: FORAGING QUEST
# ==========================================
with tab1:
    st.header("🌿 The Seasonal Quest")
    st.caption("📚 Curriculum Link: Science (Seasonal Changes, Plants)")

    # --- HOW TO PLAY ---
    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Select a Season** using the buttons at the top.
        2. A plant will appear. Read the **Botanical Clue** carefully.
        3. Questions rotate through 6 types:
           - 🌍 **Habitat** — Where does it grow?
           - 🔍 **Identification** — What are its key features?
           - ☠️ **Lookalike** — Which is the dangerous lookalike?
           - 🍃 **Parts** — Which part can you eat?
           - 📅 **Season** — When is it best foraged?
           - ⚠️ **Warning** — Is this statement true or false?
        4. **Collect Plants:** Find unique plants to fill your Herbarium.
        5. **Bonus:** Get 5 right in a row to unlock a Bonus Question!
        """)

    # --- SEASON SELECTION ---
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, var(--green-dark), var(--green-leaf)); border: 2px solid var(--green-light); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; margin-bottom: 0.8rem;">
        <span style="color: var(--cream); font-weight: 700; font-size: 1.1rem;">{SEASON_ICONS.get(st.session_state.active_season, '🌸')} Active Season: {st.session_state.active_season}</span>
    </div>
    """, unsafe_allow_html=True)

    season_cols = st.columns(4)
    seasons = ["Spring", "Summer", "Autumn", "Winter"]

    current_month = datetime.now().strftime("%B")
    default_season = "Summer"
    if current_month in SEASON_MONTHS.get("Spring", []):
        default_season = "Spring"
    elif current_month in SEASON_MONTHS.get("Summer", []):
        default_season = "Summer"
    elif current_month in SEASON_MONTHS.get("Autumn", []):
        default_season = "Autumn"
    elif current_month in SEASON_MONTHS.get("Winter", []):
        default_season = "Winter"

    if 'active_season' not in st.session_state:
        st.session_state.active_season = default_season

    for i, s in enumerate(seasons):
        is_earned = s in st.session_state.season_badge_progress
        badge_txt = " 🏅" if is_earned else ""
        with season_cols[i]:
            if st.button(f"{SEASON_ICONS[s]} {s}{badge_txt}", key=f"season_{s}", use_container_width=True):
                st.session_state.active_season = s
                st.session_state.current_question = None
                st.rerun()

    # --- STATS ROW ---
    total_edible = len(UK_PLANTS['edible'])
    collection_list = list(st.session_state.master_inventory.keys())
    total_found = len(collection_list)

    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber-dark); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--amber); font-size: 0.75rem; font-weight: 600;">SCORE</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{st.session_state.game_score}</div>
        </div>
        <div style="background: var(--danger-bg); border: 2px solid var(--danger); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--danger); font-size: 0.75rem; font-weight: 600;">LIVES</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{"❤️" * max(0, st.session_state.game_lives)}</div>
        </div>
        <div style="background: linear-gradient(135deg, #1a0a00, #2a1a00); border: 2px solid #FF8F00; border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: #FF8F00; font-size: 0.75rem; font-weight: 600;">STREAK</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{"🔥" * min(st.session_state.game_streak, 5)} {st.session_state.game_streak}</div>
        </div>
        <div style="background: var(--bg-card); border: 2px solid var(--green-leaf); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--green-leaf); font-size: 0.75rem; font-weight: 600;">HERBARIUM</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{total_found}/{total_edible}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    active_season = st.session_state.active_season
    available_plants = [p for p in UK_PLANTS["edible"]
                         if any(m in SEASON_MONTHS[active_season] for m in p.get("months", []))]

    if not available_plants:
        st.warning(f"Not much grows in {active_season}! Try another season.")
    else:
        # --- BONUS ROUND LOGIC ---
        if (st.session_state.game_streak > 0
                and st.session_state.game_streak % 5 == 0
                and not st.session_state.bonus_round):
            st.session_state.bonus_round = True

        if st.session_state.bonus_round:
            st.markdown(f"""
            <div class="level-up">
                <div style="font-size: 2rem;">⚡</div>
                <div style="color: var(--amber); font-family: 'Crimson Text', Georgia, serif; font-size: 1.5rem; font-weight: 700;">BONUS ROUND!</div>
                <div style="color: var(--cream); font-size: 0.95rem; margin-top: 0.3rem;">You've identified 5 plants in a row! Answer for <b>Double Points</b>.</div>
            </div>
            """, unsafe_allow_html=True)

            bonus_plant = random.choice(available_plants)
            parts = bonus_plant.get('parts', 'Leaves')
            if isinstance(parts, str):
                parts_list = [p.strip() for p in parts.split(',')]
            else:
                parts_list = parts

            wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark"]
            wrong_options = [p for p in wrong_parts if p not in parts_list]
            bonus_options = parts_list + safe_sample(wrong_options, 2)
            random.shuffle(bonus_options)

            st.markdown(f"### ⚡ Which part of **{bonus_plant['name']}** do we usually eat?")
            ans = st.radio("Select your answer:", bonus_options, key="bonus_q")

            if st.button("Submit Bonus Answer", key="submit_bonus"):
                if ans in parts_list:
                    st.session_state.game_score += 20
                    st.session_state.bonus_round = False
                    st.session_state.game_streak = 0
                    st.session_state.current_question = None
                    plant_name = bonus_plant['name']
                    current_count = st.session_state.master_inventory.get(plant_name, 0)
                    st.session_state.master_inventory[plant_name] = current_count + 1
                    st.session_state.total_plants_identified += 1

                    st.markdown(f"""
                    <div class="correct-feedback">
                        <div style="font-size: 1.5rem;">🎉</div>
                        <div style="color: var(--green-leaf); font-family: 'Crimson Text', Georgia, serif; font-size: 1.3rem; font-weight: 700;">BONUS CORRECT! +20 XP</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.session_state.bonus_round = False
                    st.session_state.game_streak = 0
                    st.session_state.current_question = None

                    st.markdown(f"""
                    <div class="wrong-feedback">
                        <div style="font-size: 1.5rem;">❌</div>
                        <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.3rem; font-weight: 700;">Incorrect!</div>
                        <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">The answer was: {', '.join(parts_list)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()

        else:
            # --- STANDARD QUESTION (6 TYPES) ---
            if st.session_state.current_question is None:
                plant = random.choice(available_plants)
                question_data = generate_foraging_question(plant)
                question_data['plant'] = plant
                st.session_state.current_question = question_data

            q = st.session_state.current_question

            # --- QUESTION TYPE HEADER ---
            q_type_icons = {
                'habitat': '🌍', 'identification': '🔍', 'lookalike': '☠️',
                'parts': '🍃', 'season': '📅', 'warning': '⚠️'
            }
            q_type_names = {
                'habitat': 'Habitat', 'identification': 'ID Check',
                'lookalike': 'Lookalike Danger', 'parts': 'Edible Parts',
                'season': 'Season', 'warning': 'True or False'
            }
            q_type_colours = {
                'habitat': '#4CAF50', 'identification': '#2196F3',
                'lookalike': '#ff5252', 'parts': '#FFC107',
                'season': '#FF8F00', 'warning': '#9C27B0'
            }
            q_icon = q_type_icons.get(q['type'], '🌿')
            q_name = q_type_names.get(q['type'], 'Question')
            q_colour = q_type_colours.get(q['type'], '#4CAF50')
            q_points = q.get('points', 10)

            st.markdown(f"""
            <div style="background: var(--bg-card); border-left: 4px solid {q_colour}; border-radius: 0 10px 10px 0; padding: 0.8rem 1rem; margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 0.3rem;">{q_icon}</span>
                        <span style="color: {q_colour}; font-weight: 700; font-size: 1.1rem;">{q_name}</span>
                    </div>
                    <span style="background: {q_colour}20; color: {q_colour}; padding: 0.15rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; border: 1px solid {q_colour}50;">
                        +{q_points} XP
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- PLANT CARD ---
            plant_desc = q['plant'].get('description', 'No description available.')
            id_keys = q['plant'].get('id_keys', {})
            if id_keys:
                keys_html = "<br>".join([f"<b>{k}:</b> {v}" for k, v in list(id_keys.items())[:3]])
                desc_html = f"<div style='font-size: 0.85rem; text-align: left; color: var(--cream-dim);'>{keys_html}</div>"
            else:
                desc_html = f"<div style='font-size: 0.85rem; text-align: left; color: var(--cream-dim);'><i>{plant_desc[:150]}</i></div>"

            is_poisonous = q['type'] == 'lookalike'
            card_border = "var(--danger)" if is_poisonous else "var(--green-leaf)"

            col_vis, col_quiz = st.columns([1, 1.5])

            with col_vis:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(145deg, var(--bg-card), var(--bg-deep));
                    border: 2px solid {card_border};
                    border-radius: 12px;
                    padding: 1.2rem;
                    text-align: center;
                ">
                    <div style="font-size: 3rem; margin-bottom: 0.3rem;">🌿</div>
                    <div style="color: var(--cream); font-size: 1.2rem; font-weight: 700; font-family: 'Crimson Text', Georgia, serif;">
                        {q['plant']['name']}
                    </div>
                    <div style="color: var(--cream-dim); font-size: 0.9rem; font-style: italic; margin: 0.3rem 0;">
                        {q['plant'].get('latin_name', 'N/A')}
                    </div>
                    <div style="border-top: 1px solid #3d5a3d; margin: 0.5rem 0;"></div>
                    {desc_html}
                </div>
                """, unsafe_allow_html=True)

            with col_quiz:
                # --- CLUE ---
                clue_text = ""
                if q['type'] == 'habitat':
                    if id_keys:
                        features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
                        clue_text = "Botanical Clue: " + "; ".join([f"{k} is {v}" for k, v in features])
                    else:
                        clue_text = f"Clue: {q['plant'].get('description', '')[:100]}..."
                elif q['type'] == 'lookalike':
                    clue_text = "⚠️ This plant has a DANGEROUS lookalike. Can you identify it?"
                elif q['type'] == 'warning':
                    clue_text = "⚠️ Safety knowledge check!"
                else:
                    if id_keys:
                        features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
                        clue_text = "Botanical Clue: " + "; ".join([f"{k} is {v}" for k, v in features])
                    else:
                        clue_text = f"Clue: {q['plant'].get('description', '')[:100]}..."

                if clue_text:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a0a, #2a2a10); border: 1px solid {q_colour}; border-radius: 10px; padding: 0.8rem; margin-bottom: 0.8rem;">
                        <div style="color: {q_colour}; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem;">🕵️ CLUE</div>
                        <div style="color: var(--cream); font-size: 0.95rem;">{clue_text}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # --- AUDIO ---
                if EDGE_TTS_AVAILABLE:
                    if st.button("🔊 Listen to Clue", key=f"audio_{q['plant']['name']}"):
                        with st.spinner("Generating audio..."):
                            audio_file = generate_voice(clue_text)
                            if audio_file:
                                st.audio(audio_file, format="audio/mp3")
                            else:
                                st.warning("Could not generate audio.")

                # --- QUESTION ---
                st.markdown(f"### {q['question']}")

                # --- ANSWER BUTTONS ---
                btn_cols = st.columns(len(q['options']))
                for i, option in enumerate(q['options']):
                    if q['type'] == 'habitat':
                        icon = HABITAT_ICONS.get(option, "❓")
                        label = f"{icon} {option}"
                    else:
                        label = f"{option}"

                    if btn_cols[i].button(label, key=f"opt_{i}", use_container_width=True):
                        if option == q['correct']:
                            points = q.get('points', 10)
                            streak_bonus = st.session_state.game_streak * 2
                            total_points = points + streak_bonus
                            st.session_state.game_score += total_points
                            st.session_state.game_streak += 1
                            st.session_state.total_plants_identified += 1

                            plant_name = q['plant']['name']
                            current_count = st.session_state.master_inventory.get(plant_name, 0)
                            st.session_state.master_inventory[plant_name] = current_count + 1

                            # Achievement checks
                            if len(st.session_state.master_inventory) >= 1 and not st.session_state.achievements['foraging_novice']:
                                st.session_state.achievements['foraging_novice'] = True
                                st.toast("🏅 Achievement Unlocked: Novice Forager!")
                            if len(st.session_state.master_inventory) >= 25 and not st.session_state.achievements['foraging_botanist']:
                                st.session_state.achievements['foraging_botanist'] = True
                                st.toast("🏅 Achievement Unlocked: Botanist!")
                            if len(st.session_state.season_badge_progress) == 4 and not st.session_state.achievements['foraging_master']:
                                st.session_state.achievements['foraging_master'] = True
                                st.toast("🏅 Achievement Unlocked: Seasonal Master!")

                            if active_season not in st.session_state.season_badge_progress:
                                st.session_state.season_badge_progress.append(active_season)

                            st.session_state.current_question = None
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.session_state.game_lives -= 1
                            st.session_state.game_streak = 0
                            st.session_state.current_question = None
                            time.sleep(0.5)
                            st.rerun()

    # --- GAME OVER ---
    if st.session_state.game_lives <= 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 3rem;">🤕</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">Adventure Over</div>
            <div style="color: var(--cream-dim); font-size: 1rem; margin-top: 0.5rem;">Even the best explorers need a rest. Try again to learn more!</div>
            <div style="color: var(--cream); font-size: 0.9rem; margin-top: 0.5rem;">Final Score: <b>{st.session_state.game_score} XP</b></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Restart Adventure", key="restart_quest", use_container_width=True):
            st.session_state.game_lives = 3
            st.session_state.game_score = 0
            st.session_state.current_question = None
            st.session_state.game_streak = 0
            st.rerun()

    # --- ACHIEVEMENT DISPLAY ---
    st.markdown("---")
    with st.expander("🏅 Foraging Achievements"):
        for key in ["foraging_novice", "foraging_botanist", "foraging_master"]:
            ach = ACHIEVEMENTS[key]
            is_unlocked = st.session_state.achievements.get(key, False)
            border_color = "var(--green-leaf)" if is_unlocked else "#444"
            bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"

            progress = ""
            if key == "foraging_novice":
                progress = "(Done)" if is_unlocked else f"({len(st.session_state.master_inventory)}/1)"
            elif key == "foraging_botanist":
                progress = "(Done)" if is_unlocked else f"({len(st.session_state.master_inventory)}/25)"
            elif key == "foraging_master":
                prog = len(st.session_state.season_badge_progress)
                progress = "(Done)" if is_unlocked else f"({prog}/4)"

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
# GAME TAB 2: SURVIVAL SCHOOL
# ==========================================
with tab2:
    st.header("☠️ Survival School")
    st.caption("📚 Curriculum Link: Science (Plants), PSHE (Safety)")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Read the Case File** carefully. You are looking for the **Safe** plant.
        2. **Study the Clue:** The clue gives you identifying features from the plant's real botanical data.
        3. **Check the Rule:** Each case has a key rule to help you tell safe from dangerous.
        4. **Verdict:** Click the button for the **Safe** plant.
        5. **Progress:** Solve 5 cases in a row to unlock **Level 2 (Fungi & Roots)**.
        6. **Solve 20 cases total** to earn the 🕵️ Detective badge!

        Cases are generated from real plant data — there are dozens of unique scenarios!
        """)

    # --- GENERATE CASES FROM PLANT DATA ---
    all_cases = generate_survival_cases()

    # Filter by current level
    if st.session_state.survival_level == 1:
        available_cases = [c for c in all_cases if c['level'] == 1]
    elif st.session_state.survival_level == 2:
        available_cases = [c for c in all_cases if c['level'] <= 2]
    else:
        available_cases = all_cases

    # Fallback if no cases at current level
    if not available_cases:
        available_cases = all_cases

    # Pick a case we haven't seen recently
    unseen_cases = [c for c in available_cases
                    if c['safe_plant'] not in st.session_state.survival_seen[-10:]]

    if not unseen_cases:
        unseen_cases = available_cases
        st.session_state.survival_seen = []

    # --- PROGRESS ---
    progress = st.session_state.survival_correct_count / 5
    level_name = SURVIVAL_DIFFICULTY.get(st.session_state.survival_level, "Level 1")

    st.markdown(f"""
    <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: var(--amber); font-family: 'Crimson Text', Georgia, serif; font-size: 1.1rem; font-weight: 700;">🕵️ {level_name}</span>
            <span style="color: var(--cream-dim); font-size: 0.85rem;">Cases to next level: {st.session_state.survival_correct_count}/5</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(progress, 1.0), text=f"Level {st.session_state.survival_level} Progress: {st.session_state.survival_correct_count}/5 Cases")

    # --- STATS ROW ---
    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <div style="background: var(--danger-bg); border: 2px solid var(--danger); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 100px;">
            <div style="color: var(--danger); font-size: 0.8rem; font-weight: 600;">LIVES</div>
            <div style="color: var(--cream); font-size: 1.4rem; font-weight: 700;">{"❤️" * max(0, st.session_state.survival_lives)}</div>
        </div>
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber-dark); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 100px;">
            <div style="color: var(--amber); font-size: 0.8rem; font-weight: 600;">SCORE</div>
            <div style="color: var(--cream); font-size: 1.4rem; font-weight: 700;">{st.session_state.survival_score}</div>
        </div>
        <div style="background: var(--bg-card); border: 2px solid #3d5a3d; border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 100px;">
            <div style="color: var(--green-leaf); font-size: 0.8rem; font-weight: 600;">CASES SOLVED</div>
            <div style="color: var(--cream); font-size: 1.4rem; font-weight: 700;">{st.session_state.survival_cases_solved}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- SELECT CURRENT CASE ---
    if st.session_state.survival_current_case is None:
        chosen_case = random.choice(unseen_cases)
        st.session_state.survival_current_case = chosen_case
        st.session_state.survival_result = None
        st.session_state.survival_seen.append(chosen_case['safe_plant'])

    case = st.session_state.survival_current_case

    # ─────────────────────────────────────────
    # CASE FILE DISPLAY
    # ─────────────────────────────────────────

    st.markdown(f"""
    <div class="case-file">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <h3 style="margin: 0; color: var(--amber); font-family: 'Crimson Text', Georgia, serif;">📋 Case File #{st.session_state.survival_cases_solved + 1}</h3>
            <span style="background: {'#ff525220' if case['level'] == 1 else '#ff525240' if case['level'] == 2 else '#ff525260'}; color: {'#4CAF50' if case['level'] == 1 else '#FFC107' if case['level'] == 2 else '#ff5252'}; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; border: 1px solid {'#4CAF50' if case['level'] == 1 else '#FFC107' if case['level'] == 2 else '#ff5252'}50;">
                {'Beginner' if case['level'] == 1 else 'Intermediate' if case['level'] == 2 else 'Expert'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── LOCATION & HABITAT ──
    st.markdown(f"""
    <div style="background: var(--bg-card); border-left: 4px solid var(--green-leaf); border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.8rem;">
        <span style="color: var(--cream-dim); font-size: 0.8rem;">📍 LOCATION</span><br>
        <span style="color: var(--cream); font-size: 1rem; font-weight: 600;">{case['safe_habitat']}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── YOUR OBSERVATION (THE CLUE) ──
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a0a, #2a2a10); border: 1px solid var(--amber); border-radius: 10px; padding: 1rem; margin-bottom: 0.8rem;">
        <div style="color: var(--amber); font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem;">🔍 YOUR OBSERVATION</div>
        <div style="color: var(--cream); font-size: 1.05rem; line-height: 1.5;">{case['clue']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── THE RULE ──
    st.markdown(f"""
    <div style="background: #3d2e0a; border: 1px solid var(--amber-dark); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
        <div style="color: var(--amber); font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem;">⚠️ KEY RULE</div>
        <div style="color: var(--cream); font-size: 0.95rem;">{case['rule']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── AUDIO ──
    if EDGE_TTS_AVAILABLE:
        if st.button("🔊 Listen to Clue", key="audio_clue_btn"):
            with st.spinner("Generating audio..."):
                audio_file = generate_voice(case['clue'])
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
                else:
                    st.warning("Could not generate audio.")

    st.markdown("---")

    # ─────────────────────────────────────────
    # VERDICT
    # ─────────────────────────────────────────

    st.markdown(f"""
    <div style="background: var(--bg-card); border: 2px solid var(--amber); border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
        <div style="color: var(--amber); font-family: 'Crimson Text', Georgia, serif; font-size: 1.2rem; font-weight: 700;">⚖️ VERDICT</div>
        <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">Which is the <span style="color: var(--green-leaf); font-weight: 700;">SAFE</span> plant?</div>
    </div>
    """, unsafe_allow_html=True)

    options = [
        {"name": case['safe_plant'], "icon": case['safe_icon'], "is_safe": True},
        {"name": case['danger_plant'], "icon": case['danger_icon'], "is_safe": False}
    ]
    random.shuffle(options)

    if st.session_state.survival_result is None:
        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            opt = options[0]
            border_color = "var(--green-leaf)" if opt['is_safe'] else "var(--danger)"
            bg_color = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if opt['is_safe'] else "linear-gradient(135deg, #2a1010, #3d1515)"
            hover_text = "This looks safe..." if opt['is_safe'] else "This could be dangerous..."

            if st.button(
                f"{opt['icon']} {opt['name']}",
                key="surv_opt_1",
                use_container_width=True
            ):
                if opt['is_safe']:
                    st.session_state.survival_result = "correct"
                    st.session_state.survival_score += 20
                    st.session_state.survival_correct_count += 1
                    st.session_state.total_plants_identified += 1
                    st.session_state.survival_cases_solved += 1

                    if not st.session_state.achievements['survival_scout']:
                        st.session_state.achievements['survival_scout'] = True
                        st.toast("🏅 Achievement Unlocked: Scout!")
                    if (st.session_state.survival_cases_solved >= 20
                            and not st.session_state.achievements['survival_detective']):
                        st.session_state.achievements['survival_detective'] = True
                        st.toast("🏅 Achievement Unlocked: Detective!")
                else:
                    st.session_state.survival_result = "wrong"
                    st.session_state.survival_lives -= 1
                    st.session_state.survival_correct_count = 0
                st.rerun()

        with btn_col2:
            opt = options[1]
            border_color = "var(--green-leaf)" if opt['is_safe'] else "var(--danger)"
            bg_color = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if opt['is_safe'] else "linear-gradient(135deg, #2a1010, #3d1515)"

            if st.button(
                f"{opt['icon']} {opt['name']}",
                key="surv_opt_2",
                use_container_width=True
            ):
                if opt['is_safe']:
                    st.session_state.survival_result = "correct"
                    st.session_state.survival_score += 20
                    st.session_state.survival_correct_count += 1
                    st.session_state.total_plants_identified += 1
                    st.session_state.survival_cases_solved += 1

                    if not st.session_state.achievements['survival_scout']:
                        st.session_state.achievements['survival_scout'] = True
                        st.toast("🏅 Achievement Unlocked: Scout!")
                    if (st.session_state.survival_cases_solved >= 20
                            and not st.session_state.achievements['survival_detective']):
                        st.session_state.achievements['survival_detective'] = True
                        st.toast("🏅 Achievement Unlocked: Detective!")
                else:
                    st.session_state.survival_result = "wrong"
                    st.session_state.survival_lives -= 1
                    st.session_state.survival_correct_count = 0
                st.rerun()

    # ─────────────────────────────────────────
    # RESULT DISPLAY
    # ─────────────────────────────────────────

    elif st.session_state.survival_result == "correct":
        st.markdown(f"""
        <div class="correct-feedback">
            <div style="font-size: 2rem;">✅</div>
            <div style="color: var(--green-leaf); font-family: 'Crimson Text', Georgia, serif; font-size: 1.4rem; font-weight: 700;">CASE SOLVED!</div>
            <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">Great work, Inspector. +20 points.</div>
        </div>
        """, unsafe_allow_html=True)

        # Level up check
        if (st.session_state.survival_correct_count >= 5
                and st.session_state.survival_level == 1):
            st.session_state.survival_level = 2
            st.session_state.survival_correct_count = 0
            st.markdown(f"""
            <div class="level-up">
                <div style="font-size: 2rem;">🏆</div>
                <div style="color: var(--amber); font-family: 'Crimson Text', Georgia, serif; font-size: 1.5rem; font-weight: 700;">LEVEL UP!</div>
                <div style="color: var(--cream); font-size: 1rem; margin-top: 0.3rem;">You've unlocked <b>Level 2: Fungi & Roots</b></div>
                <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">Cases now include harder plants and fungi.</div>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state.achievements['survival_expert']:
                st.session_state.achievements['survival_expert'] = True
                st.toast("🏅 Achievement Unlocked: Graduate!")

    elif st.session_state.survival_result == "wrong":
        st.markdown(f"""
        <div class="wrong-feedback">
            <div style="font-size: 2rem;">☠️</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.4rem; font-weight: 700;">DANGER!</div>
            <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">That was the wrong choice. The safe plant was <b>{case['safe_plant']}</b>.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── SIDE-BY-SIDE COMPARISON ──
    if st.session_state.survival_result is not None:
        comp_col1, comp_col2 = st.columns(2)

        with comp_col1:
            st.markdown(f"""
            <div class="safe-card">
                <div style="font-size: 2rem;">🌿</div>
                <div style="color: var(--green-leaf); font-weight: 700; font-size: 1.1rem; margin: 0.3rem 0;">{case['safe_plant']}</div>
                <div style="color: var(--green-light); font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;">✅ SAFE TO EAT</div>
                <div style="color: var(--cream-dim); font-size: 0.85rem;">{case['safe_habitat']}</div>
            </div>
            """, unsafe_allow_html=True)

        with comp_col2:
            st.markdown(f"""
            <div class="danger-card">
                <div style="font-size: 2rem;">☠️</div>
                <div style="color: var(--danger); font-weight: 700; font-size: 1.1rem; margin: 0.3rem 0;">{case['danger_plant']}</div>
                <div style="color: #ff8a80; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;">⚠️ DANGEROUS</div>
                <div style="color: var(--cream-dim); font-size: 0.85rem;">Do NOT consume</div>
            </div>
            """, unsafe_allow_html=True)

        # ── CASE ANALYSIS ──
        st.markdown(f"""
        <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1rem; margin-top: 1rem;">
            <div style="color: var(--amber); font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">📝 Case Analysis</div>
            <div style="color: var(--cream); font-size: 0.95rem; line-height: 1.6;">{case['fact']}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── EXTRA DETAIL ──
        safe_plant_data = None
        for p in UK_PLANTS['edible']:
            if p['name'] == case['safe_plant']:
                safe_plant_data = p
                break

        if safe_plant_data:
            with st.expander(f"📖 Learn more about {case['safe_plant']}"):
                lookalikes = safe_plant_data.get('lookalikes', [])
                if lookalikes:
                    st.markdown("**Lookalikes:**")
                    for la in lookalikes:
                        if isinstance(la, dict):
                            danger = la.get('danger', 'Unknown')
                            danger_icon = "☠️" if danger in ["DEADLY", "EXTREME"] else "⚠️" if danger in ["POISONOUS", "HIGH"] else "✅"
                            st.markdown(f"- {danger_icon} **{la['name']}** ({danger}): {la['diff']}")
                warnings = safe_plant_data.get('warnings', '')
                if warnings:
                    st.markdown(f"**⚠️ Warning:** {warnings}")
                confusion = safe_plant_data.get('confusion_notes', '')
                if confusion:
                    st.markdown(f"**🔍 Key ID Note:** {confusion}")

        if st.button("📋 Next Case", key="next_case_btn", use_container_width=True):
            st.session_state.survival_current_case = None
            st.session_state.survival_result = None
            st.rerun()

    # ─────────────────────────────────────────
    # GAME OVER
    # ─────────────────────────────────────────

    if st.session_state.survival_lives <= 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 3rem;">🤕</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">Training Ended</div>
            <div style="color: var(--cream-dim); font-size: 1rem; margin-top: 0.5rem;">Don't worry, even experts make mistakes.</div>
            <div style="color: var(--cream); font-size: 0.9rem; margin-top: 0.5rem;">Cases solved this session: <b>{st.session_state.survival_cases_solved}</b></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Restart Training", key="restart_survival", use_container_width=True):
            st.session_state.survival_lives = 3
            st.session_state.survival_correct_count = 0
            st.session_state.survival_current_case = None
            st.session_state.survival_result = None
            st.session_state.survival_level = 1
            st.rerun()

    # ─────────────────────────────────────────
    # ACHIEVEMENTS
    # ─────────────────────────────────────────

    st.markdown("---")
    with st.expander("🏅 Survival Achievements"):
        for key in ["survival_scout", "survival_expert", "survival_detective"]:
            ach = ACHIEVEMENTS[key]
            is_unlocked = st.session_state.achievements.get(key, False)
            border_color = "var(--green-leaf)" if is_unlocked else "#444"
            bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"
            icon = ach.get('icon', '🏅') if is_unlocked else '🔒'

            progress = ""
            if key == "survival_scout":
                progress = "(1 case)" if is_unlocked else "(0/1)"
            elif key == "survival_expert":
                progress = "(Done)" if is_unlocked else f"({st.session_state.survival_correct_count}/5 this level)"
            elif key == "survival_detective":
                progress = "(Done)" if is_unlocked else f"({st.session_state.survival_cases_solved}/20 total)"

            st.markdown(f"""
            <div style="background: {bg}; border: 2px solid {border_color}; border-radius: 10px; padding: 0.8rem; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 0.3rem;">{icon}</span>
                        <span style="color: {'var(--green-leaf)' if is_unlocked else 'var(--cream-dim)'}; font-weight: 700;">{ach['name']}</span>
                    </div>
                    <span style="color: var(--cream-dim); font-size: 0.8rem;">{progress}</span>
                </div>
                <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">{ach['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(f"📊 {len(all_cases)} unique cases available ({len([c for c in all_cases if c['level'] == 1])} Level 1, {len([c for c in all_cases if c['level'] == 2])} Level 2, {len([c for c in all_cases if c['level'] == 3])} Level 3)")

# ==========================================
# GAME TAB 3: DAILY QUIZ
# ==========================================
with tab3:
    st.header("🎯 The Plant Challenge")
    st.caption("📚 Curriculum Link: Science (Plants), Seasonal Changes, PSHE (Safety)")

    with st.expander("📖 How to Play"):
        st.markdown("""
        1. **Categories:** Choose a topic (e.g., Coastal, Trees, Fungi) to focus on.
        2. **Difficulty:**
           - **Beginner:** 3 options per question
           - **Expert:** 4 options per question
        3. **Challenge Mode ⚔️:** Only 1 life! Answer 10 questions correctly to earn the Challenger badge.
        4. **Learn:** Correct answers show the plant card with extra detail.
        5. **Streak:** Build a streak for bonus points!
        """)

    # --- SETTINGS ---
    st.markdown("#### ⚙️ Quiz Settings")
    col_settings1, col_settings2, col_settings3 = st.columns(3)
    with col_settings1:
        quiz_mode = st.selectbox("📚 Category",
            ["All", "Edible Only", "Poisonous Only", "Coastal", "Trees", "Fungi", "Beginner Friendly"])
    with col_settings2:
        difficulty = st.radio("Difficulty", ["Beginner", "Expert"], horizontal=True)
    with col_settings3:
        challenge_mode = st.checkbox("⚔️ Challenge Mode (1 Life, 10 Qs)")

    # --- CHALLENGE MODE CONFIG ---
    if challenge_mode:
        num_options = 4
        max_questions = 10
        lives = 1
    else:
        num_options = 3 if difficulty == "Beginner" else 4
        max_questions = st.session_state.quiz_max
        lives = 3

    # --- CHALLENGE MODE BANNER ---
    if challenge_mode:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2a0a0a, #3d1515); border: 2px solid var(--danger); border-radius: 12px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem;">⚔️</div>
            <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.2rem; font-weight: 700;">CHALLENGE MODE</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">1 Life · 10 Questions · Can you survive?</div>
        </div>
        """, unsafe_allow_html=True)

    # --- STATS ROW ---
    streak_fire = "🔥" * min(st.session_state.daily_streak, 5) if st.session_state.daily_streak > 0 else ""
    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <div style="background: linear-gradient(135deg, #1a0a00, #2a1a00); border: 2px solid #FF8F00; border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: #FF8F00; font-size: 0.75rem; font-weight: 600;">STREAK</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{streak_fire} {st.session_state.daily_streak}</div>
        </div>
        <div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber-dark); border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--amber); font-size: 0.75rem; font-weight: 600;">SCORE</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{st.session_state.quiz_score}</div>
        </div>
        <div style="background: var(--bg-card); border: 2px solid #3d5a3d; border-radius: 10px; padding: 0.6rem 1rem; text-align: center; flex: 1; min-width: 80px;">
            <div style="color: var(--green-leaf); font-size: 0.75rem; font-weight: 600;">QUESTION</div>
            <div style="color: var(--cream); font-size: 1.3rem; font-weight: 700;">{st.session_state.quiz_q_num}/{max_questions}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(st.session_state.quiz_q_num / max_questions, 1.0), text=f"Progress: {st.session_state.quiz_q_num}/{max_questions}")

    # --- BUILD QUESTION POOL ---
    if quiz_mode == "All":
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
    elif quiz_mode == "Edible Only":
        pool = UK_PLANTS['edible']
    elif quiz_mode == "Poisonous Only":
        pool = UK_PLANTS['poisonous']
    elif quiz_mode == "Beginner Friendly":
        pool = [p for p in UK_PLANTS['edible'] if p.get('difficulty', 1) == 1]
    else:
        pool = [p for p in UK_PLANTS['edible'] if p.get('category', '') == quiz_mode]
        pool += [p for p in UK_PLANTS['poisonous'] if p.get('category', '') == quiz_mode]

    if not pool:
        st.warning("No plants found for this category. Try 'All'.")
    else:
        # Initialize lives tracker
        if 'quiz_lives_remaining' not in st.session_state:
            st.session_state.quiz_lives_remaining = lives
        if 'quiz_plants_seen' not in st.session_state:
            st.session_state.quiz_plants_seen = []

        # --- CHALLENGE MODE GAME OVER ---
        if challenge_mode and st.session_state.quiz_lives_remaining <= 0 and st.session_state.quiz_q_num > 0:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;">
                <div style="font-size: 3rem;">⚔️</div>
                <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">CHALLENGE FAILED</div>
                <div style="color: var(--cream-dim); font-size: 1rem; margin-top: 0.5rem;">You ran out of lives.</div>
                <div style="color: var(--cream); font-size: 0.9rem; margin-top: 0.5rem;">Score: <b>{st.session_state.quiz_score}</b> | Questions answered: <b>{st.session_state.quiz_q_num}</b></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Try Challenge Again", key="restart_challenge_fail", use_container_width=True):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.session_state.quiz_lives_remaining = 1
                st.session_state.daily_streak = 0
                st.rerun()

        # --- REGULAR GAME OVER ---
        elif st.session_state.quiz_q_num >= max_questions:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 2px solid var(--green-leaf); border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;">
                <div style="font-size: 3rem;">🎉</div>
                <div style="color: var(--green-leaf); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; font-weight: 700;">
                    {'⚔️ CHALLENGE COMPLETE!' if challenge_mode else 'QUIZ COMPLETE!'}
                </div>
                <div style="color: var(--cream); font-size: 1.2rem; margin-top: 0.5rem;">Final Score: <b>{st.session_state.quiz_score}</b></div>
            </div>
            """, unsafe_allow_html=True)

            if challenge_mode and not st.session_state.achievements.get('quiz_challenger', False):
                st.session_state.achievements['quiz_challenger'] = True
                st.toast("🏅 Achievement Unlocked: Challenger!")

            st.metric("Final Score", st.session_state.quiz_score)

            if st.session_state.quiz_plants_seen:
                with st.expander("📖 Plants You Were Tested On"):
                    for p_name, correct in st.session_state.quiz_plants_seen:
                        icon = "✅" if correct else "❌"
                        st.write(f"{icon} {p_name}")

            if st.button("🔄 Try Again", key="restart_quiz", use_container_width=True):
                st.session_state.quiz_score = 0
                st.session_state.quiz_q_num = 0
                st.session_state.q_data = None
                st.session_state.quiz_lives_remaining = lives
                st.session_state.quiz_plants_seen = []
                st.rerun()

        # --- ACTIVE QUIZ ---
        else:
            # Show lives in non-challenge mode
            if not challenge_mode:
                lives_display = "❤️" * max(0, st.session_state.quiz_lives_remaining)
                st.markdown(f"""
                <div style="background: var(--danger-bg); border: 2px solid var(--danger); border-radius: 10px; padding: 0.5rem 1rem; text-align: center; margin-bottom: 1rem;">
                    <span style="color: var(--danger); font-weight: 600;">Lives:</span>
                    <span style="color: var(--cream); font-size: 1.2rem; font-weight: 700;">{lives_display}</span>
                </div>
                """, unsafe_allow_html=True)

            # Generate question if needed
            if st.session_state.q_data is None:
                plant = random.choice(pool)

                # Choose question type
                question_types = ['id_check', 'parts_check', 'season_check', 'lookalike_check', 'warning_check']
                q_type = random.choice(question_types)

                # Fallback for plants without necessary data
                if q_type == 'lookalike_check' and not any(
                    la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
                    for la in plant.get('lookalikes', [])
                ):
                    q_type = 'id_check'
                if q_type == 'parts_check' and not plant.get('parts'):
                    q_type = 'id_check'
                if q_type == 'warning_check' and not plant.get('warnings'):
                    q_type = 'id_check'

                question_text = ""
                correct_answer = ""
                options = []
                fun_fact = ""
                is_edible = plant in UK_PLANTS['edible']

                # --- TYPE 1: IS IT EDIBLE? ---
                if q_type == 'id_check':
                    question_text = f"Is **{plant['name']}** safe to eat?"
                    correct_answer = "Edible" if is_edible else "Poisonous"
                    options = ["Edible", "Poisonous"]
                    if is_edible:
                        fun_fact = f"✅ **{plant['name']}** is edible. {plant.get('warnings', 'Always check ID!')}"
                    else:
                        danger = plant.get('danger_tips', {})
                        danger_note = danger.get('danger_zone', plant.get('warnings', 'Extremely dangerous.'))
                        fun_fact = f"☠️ **{plant['name']}** is POISONOUS. {danger_note}"

                # --- TYPE 2: WHICH PART? ---
                elif q_type == 'parts_check':
                    edible_plant = random.choice(UK_PLANTS['edible'])
                    raw_parts = edible_plant.get('parts', 'Leaves')
                    if isinstance(raw_parts, str):
                        parts = [p.strip() for p in raw_parts.split(',')]
                    else:
                        parts = raw_parts
                    if not parts:
                        parts = ['Leaves']

                    correct_answer = parts[0]
                    wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark", "Stem"]
                    wrong_options = [p for p in wrong_parts if p not in parts]
                    question_text = f"Which part of **{edible_plant['name']}** do we usually eat?"
                    options = [correct_answer] + safe_sample(wrong_options, num_options - 1)
                    fun_fact = f"🍃 **{edible_plant['name']}:** Edible parts are {', '.join(parts)}. {edible_plant.get('warnings', '')}"

                # --- TYPE 3: WHEN TO HARVEST? ---
                elif q_type == 'season_check':
                    edible_plant = random.choice(UK_PLANTS['edible'])
                    correct_months = edible_plant.get('months', ['Summer'])
                    correct_answer = random.choice(correct_months)
                    all_months = ["January", "March", "June", "August", "October", "December"]
                    wrong_months = [m for m in all_months if m not in correct_months]
                    if not wrong_months:
                        wrong_months = ["January", "March", "November"]
                    question_text = f"When is **{edible_plant['name']}** best harvested?"
                    options = [correct_answer] + safe_sample(wrong_months, num_options - 1)
                    fun_fact = f"📅 **{edible_plant['name']}** is best in {', '.join(correct_months)}. Habitat: {edible_plant.get('habitat', 'Various')}."

                # --- TYPE 4: DANGEROUS LOOKALIKE ---
                elif q_type == 'lookalike_check':
                    dangerous_lookalikes = [
                        la for la in plant.get('lookalikes', [])
                        if la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
                    ]
                    if dangerous_lookalikes:
                        chosen = random.choice(dangerous_lookalikes)
                        correct_answer = chosen['name']
                        question_text = f"**{plant['name']}** has a dangerous lookalike. Which of these is it?"

                        other_names = [p['name'] for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']
                                      if p['name'] != plant['name'] and p['name'] != correct_answer]
                        wrong_options = safe_sample(other_names, num_options - 1)
                        options = [correct_answer] + wrong_options

                        confusion = plant.get('confusion_notes', chosen.get('diff', 'Check carefully!'))
                        fun_fact = f"☠️ **Key ID:** {confusion}"
                    else:
                        question_text = f"Is **{plant['name']}** safe to eat?"
                        correct_answer = "Edible" if is_edible else "Poisonous"
                        options = ["Edible", "Poisonous"]
                        fun_fact = plant.get('warnings', '')

                # --- TYPE 5: WARNING CHECK ---
                elif q_type == 'warning_check':
                    warning = plant.get('warnings', '')
                    if warning:
                        if random.random() < 0.6:
                            question_text = f"True or False: {warning}"
                            correct_answer = "True"
                            options = ["True", "False"]
                            fun_fact = f"✅ This is correct: {warning}"
                        else:
                            false_warning = warning
                            swaps = [
                                ("cook", "eat raw"), ("edible", "poisonous"),
                                ("safe", "dangerous"), ("must", "don't need to"),
                                ("hairy", "smooth"), ("round", "flat"),
                                ("never", "always")
                            ]
                            for orig, swap in swaps:
                                if orig.lower() in false_warning.lower():
                                    false_warning = false_warning.lower().replace(orig.lower(), swap.lower())
                                    false_warning = false_warning[0].upper() + false_warning[1:]
                                    break

                            if false_warning != warning:
                                question_text = f"True or False: {false_warning}"
                                correct_answer = "False"
                                options = ["True", "False"]
                                fun_fact = f"❌ That's FALSE. The real warning is: {warning}"
                            else:
                                question_text = f"True or False: {warning}"
                                correct_answer = "True"
                                options = ["True", "False"]
                                fun_fact = f"✅ This is correct: {warning}"
                    else:
                        question_text = f"Is **{plant['name']}** safe to eat?"
                        correct_answer = "Edible" if is_edible else "Poisonous"
                        options = ["Edible", "Poisonous"]
                        fun_fact = plant.get('warnings', '')

                # Ensure we have enough options
                while len(options) < num_options:
                    options.append("None of the above")

                random.shuffle(options)

                st.session_state.q_data = {
                    "plant": plant,
                    "text": question_text,
                    "correct": correct_answer,
                    "options": options,
                    "type": q_type,
                    "fact": fun_fact
                }

            q = st.session_state.q_data

            # Question type icons and colours
            q_type_icons = {
                'id_check': '🔍', 'parts_check': '🍃', 'season_check': '📅',
                'lookalike_check': '☠️', 'warning_check': '⚠️'
            }
            q_type_names = {
                'id_check': 'Identification', 'parts_check': 'Edible Parts',
                'season_check': 'Season', 'lookalike_check': 'Dangerous Lookalike',
                'warning_check': 'Safety Check'
            }
            q_type_colours = {
                'id_check': '#2196F3', 'parts_check': '#FFC107',
                'season_check': '#FF8F00', 'lookalike_check': '#ff5252',
                'warning_check': '#9C27B0'
            }
            q_icon = q_type_icons.get(q['type'], '❓')
            q_name = q_type_names.get(q['type'], 'Question')
            q_colour = q_type_colours.get(q['type'], '#4CAF50')

            # --- QUESTION TYPE HEADER ---
            st.markdown(f"""
            <div style="background: var(--bg-card); border-left: 4px solid {q_colour}; border-radius: 0 10px 10px 0; padding: 0.8rem 1rem; margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 0.3rem;">{q_icon}</span>
                        <span style="color: {q_colour}; font-weight: 700; font-size: 1.1rem;">{q_name}</span>
                    </div>
                    <span style="color: var(--cream-dim); font-size: 0.8rem;">Q{st.session_state.quiz_q_num + 1}/{max_questions}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- QUESTION ---
            st.markdown(f"### {q['text']}")

            cols = st.columns(len(q['options']))
            for i, opt in enumerate(q['options']):
                if cols[i].button(f"👉 {opt}", key=f"ans_{i}", use_container_width=True):
                    if opt == q['correct']:
                        st.session_state.quiz_score += 1
                        st.session_state.daily_streak += 1

                        if 'quiz_plants_seen' in st.session_state:
                            st.session_state.quiz_plants_seen.append((q['plant']['name'], True))

                        if st.session_state.daily_streak >= 5 and not st.session_state.achievements['quiz_streak']:
                            st.session_state.achievements['quiz_streak'] = True
                            st.toast("🏅 Achievement Unlocked: Quick Wit!")

                    else:
                        st.session_state.daily_streak = 0
                        st.session_state.quiz_lives_remaining -= 1

                        if 'quiz_plants_seen' in st.session_state:
                            st.session_state.quiz_plants_seen.append((q['plant']['name'], False))

                    st.session_state.quiz_q_num += 1
                    st.session_state.q_data = None
                    time.sleep(0.3)
                    st.rerun()

    # --- ACHIEVEMENT DISPLAY ---
    st.markdown("---")
    with st.expander("🏅 Quiz Achievements"):
        for key in ["quiz_streak", "quiz_challenger"]:
            ach = ACHIEVEMENTS[key]
            is_unlocked = st.session_state.achievements.get(key, False)
            border_color = "var(--green-leaf)" if is_unlocked else "#444"
            bg = "linear-gradient(135deg, #0a2a0a, #1a3d1a)" if is_unlocked else "var(--bg-card)"

            progress = ""
            if key == "quiz_streak":
                progress = f"({st.session_state.daily_streak}/5)" if not is_unlocked else "(Done)"
            elif key == "quiz_challenger":
                progress = "(Done)" if is_unlocked else "(Complete Challenge Mode)"

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
