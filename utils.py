import streamlit as st
import random
import time
import json
import os
from datetime import datetime
from pathlib import Path

# --- DATA IMPORTS ---
from plants_data import UK_PLANTS
from lessons_data import LESSON_CONTENT
from game_config import (ACHIEVEMENTS, HABITAT_ICONS, SEASON_ICONS, SEASON_MONTHS,
                         SURVIVAL_DIFFICULTY, VILLAGE_ITEMS, VILLAGE_BUILDINGS,
                         VILLAGE_PRODUCTION, BASE_PRICES, KITCHEN_RECIPES, BASICS)

# --- SAFE IMPORTS ---
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    Image = None

# ==========================================
# DATABASE (PostgreSQL via DigitalOcean)
# ==========================================
import psycopg2

import os # Make sure this is at the top of utils.py

def get_db_connection():
    """Create a connection to the PostgreSQL database using Environment Variables."""
    try:
        # This looks for the link in DigitalOcean App Platform settings
        uri = os.environ.get("DATABASE_URL") 
        # sslmode="require" is necessary for DigitalOcean Managed Databases
        conn = psycopg2.connect(uri, sslmode="require")
        return conn
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None

def init_db():
    """Create the saves table if it doesn't exist."""
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS saves
                         (username TEXT PRIMARY KEY, data TEXT, last_saved TEXT)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB Init Error: {e}")

def save_game(username, data):
    """Save game data to PostgreSQL."""
    if not username:
        return False
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            # PostgreSQL uses %s instead of ? and ON CONFLICT instead of INSERT OR REPLACE
            c.execute("""INSERT INTO saves (username, data, last_saved) 
                          VALUES (%s, %s, %s) 
                          ON CONFLICT (username) 
                          DO UPDATE SET data = EXCLUDED.data, last_saved = EXCLUDED.last_saved""",
                      (username, json.dumps(data), datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Save Error: {e}")
            return False
    return False

def load_game(username):
    """Load game data from PostgreSQL."""
    if not username:
        return None
    conn = get_db_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT data FROM saves WHERE username=%s", (username,))
            row = c.fetchone()
            conn.close()
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            print(f"Load Error: {e}")
            return None
    return None

def get_save_data():
    """Collect all saveable session state data."""
    keys_to_save = [
        'game_score', 'game_lives', 'game_streak', 'total_plants_identified',
        'player_title', 'total_xp', 'master_inventory', 'achievements',
        'unlocked_recipes', 'kitchen_score', 'kitchen_inventory',
        'season_badge_progress', 'survival_lives', 'survival_score',
        'survival_correct_count', 'survival_level', 'survival_cases_solved',
        'quiz_score', 'daily_streak', 'village', 'farm_game',
        'challenge_completed', 'completed_modules',
    ]
    data = {}
    for key in keys_to_save:
        if key in st.session_state:
            val = st.session_state[key]
            if isinstance(val, set):
                val = list(val)
            data[key] = val

    # Save module progress (dynamic keys)
    for title in LESSON_CONTENT.keys():
        progress_key = f"module_progress_{title}"
        if progress_key in st.session_state:
            data[progress_key] = st.session_state[progress_key]

    return data

def apply_save_data(data):
    """Apply loaded data to session state."""
    if data:
        for key, val in data.items():
            if isinstance(val, list) and key in ['season_badge_progress']:
                val = list(val)
            st.session_state[key] = val

# ==========================================
# SESSION STATE
# ==========================================
def init_session_state():
    defaults = {
        'game_score': 0, 'game_lives': 3, 'game_streak': 0,
        'current_question': None, 'bonus_round': False,
        'village': None, 'farm_game': None,
        'survival_lives': 3, 'survival_score': 0,
        'survival_correct_count': 0, 'survival_level': 1,
        'survival_current_case': None, 'survival_result': None,
        'survival_cases_solved': 0,
        'quiz_score': 0, 'quiz_q_num': 0, 'quiz_max': 5,
        'q_data': None, 'daily_streak': 0,
        'challenge_completed': False,
        'chat_language': 'English', 'messages': [],
        'selected_page': "Home", 'book_content': {}, 'book_outline': "",
        'active_season': "Summer", 'season_badge_progress': [],
        'player_title': "Novice Gatherer",
        'total_plants_identified': 0, 'total_xp': 0,
        'master_inventory': {}, 'kitchen_inventory': {},
        'achievements': {k: False for k in ACHIEVEMENTS.keys()},
        'unlocked_recipes': [], 'kitchen_score': 0,
        'username': '', 'game_loaded': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Initialize DB on first run
    init_db()

# ==========================================
# THEME
# ==========================================
def apply_brand_theme():
    st.markdown("""
    <style>
    /* ─── FONTS ─── */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ─── ROOT COLOURS ─── */
    :root {
        --bg-deep: #0a1a0a;
        --bg-main: #1a2e1a;
        --bg-card: #1e331e;
        --bg-card-hover: #264026;
        --green-leaf: #4CAF50;
        --green-light: #66BB6A;
        --green-dark: #2E7D32;
        --amber: #FFC107;
        --amber-dark: #FF8F00;
        --brown: #5D4037;
        --brown-light: #795548;
        --cream: #F5F0E8;
        --cream-dim: #B8AFA3;
        --danger: #ff5252;
        --danger-bg: #2a1010;
        --info-bg: #0a1a2a;
        --shadow: rgba(0, 0, 0, 0.4);
    }

    /* ─── APP BACKGROUND ─── */
    .stApp {
        background: linear-gradient(180deg, var(--bg-deep) 0%, var(--bg-main) 100%) !important;
        color: var(--cream) !important;
    }

    /* ─── MAIN CONTENT ─── */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* ─── TYPOGRAPHY ─── */
    h1, h2, h3, h4, h5, h6 {
        color: var(--cream) !important;
        font-family: 'Crimson Text', Georgia, serif !important;
    }
    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.6rem !important; border-bottom: 2px solid var(--green-dark) !important; padding-bottom: 0.5rem !important; }
    h3 { font-size: 1.3rem !important; }

    p, span, div, label, .stMarkdown, .stText {
        color: var(--cream) !important;
    }

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1f0d 0%, #142814 100%) !important;
        border-right: 1px solid #2d4a2d !important;
    }
    section[data-testid="stSidebar"] * {
        color: var(--cream) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown hr {
        border-color: #2d4a2d !important;
    }

    /* ─── BUTTONS ─── */
    .stButton > button {
        background: linear-gradient(135deg, var(--green-dark), var(--green-leaf)) !important;
        color: var(--cream) !important;
        border: 1px solid var(--green-light) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--green-leaf), var(--green-light)) !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    .stButton > button:focus {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.4) !important;
    }
    .stButton > button:disabled {
        background: #2a3a2a !important;
        color: #666 !important;
        border-color: #444 !important;
        box-shadow: none !important;
    }

    /* ─── TEXT INPUTS ─── */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        color: var(--cream) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--green-leaf) !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    .stTextInput > div > label {
        color: var(--cream-dim) !important;
    }

    /* ─── SELECTBOXES ─── */
    .stSelectbox > div > div {
        background: var(--bg-card) !important;
        color: var(--cream) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > label {
        color: var(--cream-dim) !important;
    }

    /* ─── CHECKBOXES ─── */
    .stCheckbox > label {
        color: var(--cream) !important;
    }
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] {
        color: var(--cream) !important;
    }

    /* ─── RADIO ─── */
    .stRadio > label {
        color: var(--cream) !important;
    }

    /* ─── EXPANDERS ─── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        color: var(--cream) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderHeader:hover {
        background: var(--bg-card-hover) !important;
        border-color: var(--green-leaf) !important;
    }
    .streamlit-expanderContent {
        border: 1px solid #3d5a3d !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ─── METRICS ─── */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
        border-left: 4px solid var(--green-leaf) !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--cream-dim) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--amber) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        color: var(--green-light) !important;
    }

    /* ─── PROGRESS BARS ─── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--green-dark), var(--green-leaf)) !important;
    }
    .stProgress > div > div > div {
        background: var(--bg-card) !important;
    }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        padding: 0.2rem !important;
        gap: 0.2rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--cream-dim) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--green-dark) !important;
        color: var(--cream) !important;
        border: 1px solid var(--green-leaf) !important;
    }
    .stTabs [aria-selected="false"]:hover {
        background: var(--bg-card-hover) !important;
    }

    /* ─── ALERTS / TOASTS ─── */
    .stAlert {
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    [data-bd-type="success"] {
        background: #1a3d1a !important;
        border: 1px solid var(--green-leaf) !important;
        color: var(--cream) !important;
    }
    [data-bd-type="warning"] {
        background: #3d2e0a !important;
        border: 1px solid var(--amber) !important;
        color: var(--cream) !important;
    }
    [data-bd-type="error"] {
        background: var(--danger-bg) !important;
        border: 1px solid var(--danger) !important;
        color: var(--cream) !important;
    }
    [data-bd-type="info"] {
        background: var(--info-bg) !important;
        border: 1px solid #2196F3 !important;
        color: var(--cream) !important;
    }

    /* ─── DATAFRAMES ─── */
    .stDataFrame {
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar {
        width: 8px !important;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-deep) !important;
    }
    ::-webkit-scrollbar-thumb {
        background: #3d5a3d !important;
        border-radius: 4px !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--green-dark) !important;
    }

    /* ─── HIDE STREAMLIT BRANDING ─── */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }

    /* ─── SEPARATOR LINES ─── */
    hr {
        border-color: #2d4a2d !important;
    }

    /* ─── CONTAINER OVERRIDES ─── */
    .element-container {
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* ─── CAPTION ─── */
    .stCaption {
        color: var(--cream-dim) !important;
        font-size: 0.85rem !important;
    }

    /* ───────────────────────────────────────── */
    /* GAME-SPECIFIC STYLES                      */
    /* ───────────────────────────────────────── */

    /* Case file styling (Survival School) */
    .case-file {
        background: linear-gradient(135deg, #1a1a0a, #2a2a10) !important;
        border: 2px solid var(--amber-dark) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 16px rgba(255, 143, 0, 0.15) !important;
    }
    .case-file h3, .case-file h4 {
        color: var(--amber) !important;
        font-family: 'Crimson Text', Georgia, serif !important;
    }

    /* Safe card */
    .safe-card {
        background: linear-gradient(135deg, #0a2a0a, #1a3d1a) !important;
        border: 2px solid var(--green-leaf) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
    }

    /* Danger card */
    .danger-card {
        background: linear-gradient(135deg, #2a0a0a, #3d1515) !important;
        border: 2px solid var(--danger) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
    }

    /* Feedback boxes */
    .correct-feedback {
        background: linear-gradient(135deg, #0a2a0a, #1a3d1a) !important;
        border: 2px solid var(--green-leaf) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    .wrong-feedback {
        background: linear-gradient(135deg, #2a0a0a, #3d1515) !important;
        border: 2px solid var(--danger) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
    }

    /* Level up banner */
    .level-up {
        background: linear-gradient(135deg, #2a1a00, #3d2e00) !important;
        border: 2px solid var(--amber) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        box-shadow: 0 0 30px rgba(255, 193, 7, 0.3) !important;
    }

    /* Game card */
    .game-card {
        background: var(--bg-card) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
    }

    /* Streak flame */
    .streak-display {
        background: linear-gradient(135deg, #1a0a00, #2a1a00) !important;
        border: 2px solid var(--amber-dark) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.2rem !important;
        text-align: center !important;
    }

    /* Plant card (for Foraging Quest etc.) */
    .plant-card {
        border-radius: 20px !important;
        padding: 20px !important;
        text-align: center !important;
        background: linear-gradient(145deg, var(--bg-card), var(--bg-deep)) !important;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.3) !important;
        margin-bottom: 20px !important;
        border: 1px solid #3d5a3d !important;
    }

    /* Grid game buttons (Eco-Village, Farm) */
    div.grid-game div.stButton > button {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        font-size: 1.5em !important;
        border: 1px solid #3d5a3d !important;
        background-color: var(--bg-card) !important;
        color: var(--cream) !important;
        border-radius: 8px !important;
    }
    div.grid-game div.stButton > button:hover {
        border-color: var(--green-leaf) !important;
        transform: scale(1.05) !important;
    }

    /* Market buttons */
    .market-box div.stButton > button {
        font-size: 14px !important;
        white-space: normal !important;
        height: auto !important;
        padding: 5px !important;
    }

    /* ─── RESPONSIVE ─── */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        .plant-card { padding: 10px !important; }
        div.grid-game div.stButton > button { font-size: 1em !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# AUDIO
# ==========================================
def clean_text_for_audio(text):
    if not text:
        return ""
    text = text.replace("**", "").replace("##", "").replace("*", "")
    icon_map = {
        "🌿": "Plant", "🌲": "Woodland", "☠️": "Poison", "✅": "Correct",
        "❌": "Wrong", "🕵️": "Inspector", "⚡": "Bonus", "🎓": "Graduate",
        "🌱": "Seedling", "🍄": "Mushroom", "🏖️": "Coastal", "🏡": "Urban",
        "🌾": "Meadow", "💧": "Water", "🪨": "Rock", "🌸": "Spring",
        "☀️": "Summer", "🍂": "Autumn", "❄️": "Winter", "🍃": "Leaves",
        "🌳": "Tree", "🐝": "Bee", "🍎": "Apple", "🫧": "Cold frame",
        "🥓": "Smokehouse", "🔋": "Battery", "☀️": "Solar", "🐔": "Chicken",
        "🐄": "Cow", "🐐": "Goat", "🌾": "Wheat", "🥕": "Carrot",
        "🌽": "Corn", "🐟": "Fish", "🥚": "Egg", "🥛": "Milk",
        "🍯": "Honey", "📏": "Rule", "📋": "Case", "🔍": "Observation",
        "⚖️": "Verdict", "🎯": "Target", "🔥": "Streak", "🤕": "Injured",
        "🛡️": "Shield", "🏆": "Trophy", "🏅": "Medal", "⚠️": "Warning",
        "📦": "Package", "💰": "Money", "🏗️": "Building", "🧹": "Clear",
    }
    for icon, word in icon_map.items():
        text = text.replace(icon, word)
    return text.strip()

def generate_voice(text, filename="temp_audio.mp3"):
    if not EDGE_TTS_AVAILABLE:
        return None
    import asyncio
    try:
        communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicate.save(filename))
        loop.close()
        return filename
    except Exception as e:
        print(f"Audio Error: {e}")
        return None

def get_week_in_month(day):
    """Calculates the week of the month (1-5) from the day number."""
    if day is None or day <= 0:
        return 1  # Default to week 1 if something goes wrong
    return (day - 1) // 7 + 1

# ==========================================
# DYNAMIC SURVIVAL CASE GENERATION
# ==========================================
def generate_survival_cases():
    """Generate survival school cases from plant data. Uses KS2-friendly language."""
    cases = []

    # Fallback hardcoded cases (always available)
    fallback_cases = [
        {"level": 1, "clue": "You find a tall plant with white umbrella-shaped flowers. The stem is smooth with purple spots on it. There are no hairs on the stem at all.",
         "rule": "🚨 Rule: In the Carrot family, purple spots usually mean POISON. Hairy stems are usually safe.",
         "safe_plant": "Wild Carrot", "danger_plant": "Hemlock",
         "safe_icon": "🥕", "danger_icon": "☠️",
         "fact": "🕵️ Remember: Hemlock (POISON) has a smooth stem with purple spots and smells like mouse wee. Wild Carrot (Safe) has a hairy stem and smells like carrots.",
         "safe_habitat": "Meadows"},
        {"level": 1, "clue": "You find a plant with big green leaves in a damp woodland. You squash a leaf and it smells really strongly of garlic!",
         "rule": "✅ Rule: A strong garlic or onion smell is usually a good sign — it means the plant is safe to eat.",
         "safe_plant": "Wild Garlic", "danger_plant": "Lily of the Valley",
         "safe_icon": "🌿", "danger_icon": "☠️",
         "fact": "🕵️ Remember: Wild Garlic (Safe) smells of garlic. Lily of the Valley (POISON) has no garlic smell at all. Always use your nose!",
         "safe_habitat": "Woodland"},
        {"level": 2, "clue": "You find an orange mushroom under an oak tree. Under the cap, it has ridges (like blunt, thick lines) instead of thin gills. It smells fruity, like apricots.",
         "rule": "✅ Rule: True gills are thin sheets like paper. Ridges are blunt and thick, like corrugated cardboard.",
         "safe_plant": "Chanterelle", "danger_plant": "False Chanterelle",
         "safe_icon": "🍄", "danger_icon": "🚫",
         "fact": "🕵️ Remember: Chanterelle (Safe) has ridges, not gills, and smells like apricots. False Chanterelle (Not Safe) has thin gills like paper and no apricot smell.",
         "safe_habitat": "Woodland"}
    ]

    # Generate cases from plant data
    for plant in UK_PLANTS['edible']:
        lookalikes = plant.get('lookalikes', [])
        plant_difficulty = plant.get('difficulty', 2)
        id_keys = plant.get('id_keys', {})
        confusion_notes = plant.get('confusion_notes', '')

        for la in lookalikes:
            danger_level = la.get('danger', '')
            if danger_level not in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']:
                continue

            danger_name = la.get('name', 'Unknown')
            danger_diff = la.get('diff', '')
            safe_name = plant['name']

            # Determine level
            if plant.get('category') == 'Fungi' or plant_difficulty >= 3:
                level = 2 if plant_difficulty == 2 else 3
            else:
                level = 1

            # Generate KS2-friendly clue
            if id_keys:
                features = list(id_keys.items())[:3]
                clue_parts = []
                for k, v in features:
                    k_simple = k
                    v_simple = v
                    if k == "Gills":
                        k_simple = "Gills (the lines under the cap)"
                    if k == "Stem":
                        k_simple = "Stem (the stalk)"
                    if k == "Flowers":
                        k_simple = "Flowers"
                    if k == "Smell":
                        k_simple = "Smell"
                    if k == "Fruit":
                        k_simple = "Fruit"
                    clue_parts.append(f"{k_simple}: {v_simple}")
                clue = "You find a plant. " + ". ".join(clue_parts) + "."
            else:
                desc = plant.get('description', 'No description available.')
                clue = f"You find {safe_name}. {desc[:100]}..."

            # Generate KS2-friendly rule
            rule = f"⚠️ Key Difference: {danger_diff}" if danger_diff else f"🚨 Rule: {safe_name} has special identifying features. Check carefully!"

            # Generate KS2-friendly fact
            if confusion_notes:
                fact_text = confusion_notes
                fact_text = fact_text.replace("Key Diff:", "Remember:")
                fact_text = fact_text.replace("CRITICAL:", "⚠️ IMPORTANT:")
                fact = f"🕵️ {fact_text}"
            else:
                fact = f"🕵️ {safe_name} is SAFE. {danger_name} is {danger_level}."

            # Find the safe plant's habitat
            raw_habitat = plant.get('habitat', 'Various').split(',')[0].strip()
            habitat_map = {
                "Woodlands": "Woodland", "Woods": "Woodland", "Wood": "Woodland",
                "Hedgerows": "Hedgerow", "Hedgerow": "Hedgerow", "Roadsides": "Hedgerow",
                "Meadows": "Meadow", "Grassland": "Meadow", "Fields": "Meadow",
                "Coastal": "Coastal", "Shingle": "Coastal", "Rocky": "Coastal",
                "Saltmarsh": "Coastal", "Sandy": "Coastal",
                "Urban": "Urban", "Gardens": "Urban", "Lawns": "Urban",
                "Damp": "Woodland", "Riverbanks": "Woodland", "Wet": "Woodland"
            }
            safe_habitat = habitat_map.get(raw_habitat, "Woodland")

            # Determine icons
            safe_icon = "🌿"
            danger_icon = "☠️" if danger_level in ['DEADLY', 'EXTREME'] else "⚠️"

            # Category-specific icons
            cat = plant.get('category', '')
            if cat == 'Fungi':
                safe_icon = "🍄"
            elif cat == 'Tree':
                safe_icon = "🌲"
            elif cat == 'Coastal':
                safe_icon = "🏖️"
            elif cat == 'Shrub':
                safe_icon = "🌿"

            cases.append({
                "level": level,
                "clue": clue,
                "rule": rule,
                "safe_plant": safe_name,
                "danger_plant": danger_name,
                "safe_icon": safe_icon,
                "danger_icon": danger_icon,
                "fact": fact,
                "safe_habitat": safe_habitat
            })

    # If no cases generated, use fallbacks
    if not cases:
        cases = fallback_cases

    return cases

# ==========================================
# DYNAMIC FORAGING QUESTION GENERATION
# ==========================================
def generate_foraging_question(plant, question_type=None):
    """Generate a foraging question of a random or specified type."""
    all_plants = UK_PLANTS['edible'] + UK_PLANTS['poisonous']

    # Determine question type
    if question_type is None:
        has_danger = any(
            la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
            for la in plant.get('lookalikes', [])
        )
        if has_danger:
            question_type = random.choices(
                ['habitat', 'identification', 'lookalike', 'parts', 'season', 'warning'],
                weights=[3, 3, 3, 2, 2, 1], k=1
            )[0]
        else:
            question_type = random.choices(
                ['habitat', 'identification', 'parts', 'season', 'warning'],
                weights=[3, 3, 2, 2, 1], k=1
            )[0]

    # --- HABITAT QUESTION ---
    if question_type == 'habitat':
        raw_habitat = plant['habitat'].split(',')[0].strip()
        habitat_map = {
            "Woodlands": "Woodland", "Woods": "Woodland", "Wood": "Woodland",
            "Hedgerows": "Hedgerow", "Hedgerow": "Hedgerow", "Roadsides": "Hedgerow",
            "Meadows": "Meadow", "Grassland": "Meadow", "Fields": "Meadow",
            "Coastal": "Coastal", "Shingle": "Coastal", "Rocky": "Coastal",
            "Saltmarsh": "Coastal", "Sandy": "Coastal",
            "Urban": "Urban", "Gardens": "Urban", "Lawns": "Urban",
            "Damp": "Woodland", "Riverbanks": "Woodland", "Wet": "Woodland"
        }
        correct = habitat_map.get(raw_habitat, "Woodland")
        all_habitats = ["Woodland", "Coastal", "Hedgerow", "Urban", "Meadow"]
        wrong = [h for h in all_habitats if h != correct]
        options = [correct] + random.sample(wrong, min(3, len(wrong)))
        random.shuffle(options)

        return {
            'type': 'habitat', 'plant': plant,
            'question': f"Where does {plant['name']} typically grow?",
            'correct': correct, 'options': options,
            'explanation': f"{plant['name']} grows in {plant['habitat']}.",
            'points': 10
        }

    # --- IDENTIFICATION QUESTION ---
    elif question_type == 'identification':
        id_keys = plant.get('id_keys', {})
        if not id_keys:
            return generate_foraging_question(plant, 'habitat')

        correct_key, correct_value = random.choice(list(id_keys.items()))
        wrong_options = []
        used_values = {correct_value}
        for other_plant in random.sample(all_plants, min(len(all_plants), 8)):
            if other_plant['name'] == plant['name']:
                continue
            other_keys = other_plant.get('id_keys', {})
            for k, v in other_keys.items():
                if v not in used_values and len(wrong_options) < 3:
                    wrong_options.append(v)
                    used_values.add(v)
                    break

        while len(wrong_options) < 3:
            wrong_options.append("Unknown feature")

        options = [correct_value] + wrong_options[:3]
        random.shuffle(options)

        return {
            'type': 'identification', 'plant': plant,
            'question': f"Which is a key identifier for {plant['name']}?",
            'correct': correct_value, 'options': options,
            'explanation': f"{plant['name']}: {correct_key} - {correct_value}",
            'points': 12
        }

    # --- LOOKALIKE QUESTION ---
    elif question_type == 'lookalike':
        dangerous_lookalikes = [
            la for la in plant.get('lookalikes', [])
            if la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
        ]
        if not dangerous_lookalikes:
            return generate_foraging_question(plant, 'identification')

        chosen = random.choice(dangerous_lookalikes)
        correct = chosen['name']
        wrong_options = []
        used_names = {correct, plant['name']}
        for other_plant in random.sample(all_plants, min(len(all_plants), 10)):
            if other_plant['name'] not in used_names and len(wrong_options) < 2:
                wrong_options.append(other_plant['name'])
                used_names.add(other_plant['name'])

        while len(wrong_options) < 2:
            wrong_options.append("Unknown plant")

        options = [correct] + wrong_options[:2]
        random.shuffle(options)

        return {
            'type': 'lookalike', 'plant': plant,
            'question': f"Which plant is a DANGEROUS lookalike of {plant['name']}?",
            'correct': correct, 'options': options,
            'explanation': f"{plant.get('confusion_notes', chosen.get('diff', 'Check carefully!'))}",
            'points': 15
        }

    # --- PARTS QUESTION ---
    elif question_type == 'parts':
        raw_parts = plant.get('parts', 'Leaves')
        if isinstance(raw_parts, str):
            parts = [p.strip() for p in raw_parts.split(',')]
        else:
            parts = raw_parts
        if not parts:
            parts = ['Leaves']

        correct = parts[0]
        wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark", "Stem"]
        wrong = [p for p in wrong_parts if p not in parts]
        options = [correct] + random.sample(wrong, min(2, len(wrong)))
        random.shuffle(options)

        return {
            'type': 'parts', 'plant': plant,
            'question': f"Which part of {plant['name']} can you eat?",
            'correct': correct, 'options': options,
            'explanation': f"{plant['name']}: Edible parts are {', '.join(parts)}.",
            'points': 10
        }

    # --- SEASON QUESTION ---
    elif question_type == 'season':
        correct_months = plant.get('months', ['Summer'])
        correct = random.choice(correct_months)
        all_months = ["January", "March", "June", "August", "October", "December"]
        wrong_months = [m for m in all_months if m not in correct_months]
        if not wrong_months:
            wrong_months = ["January", "March"]
        options = [correct] + random.sample(wrong_months, min(2, len(wrong_months)))
        random.shuffle(options)

        return {
            'type': 'season', 'plant': plant,
            'question': f"When is {plant['name']} best harvested?",
            'correct': correct, 'options': options,
            'explanation': f"{plant['name']} is best in {', '.join(correct_months)}.",
            'points': 10
        }

    # --- WARNING QUESTION ---
    elif question_type == 'warning':
        warning = plant.get('warnings', plant.get('description', ''))
        if not warning:
            return generate_foraging_question(plant, 'habitat')

        if random.random() < 0.5:
            return {
                'type': 'warning', 'plant': plant,
                'question': f"True or False: {warning}",
                'correct': "True", 'options': ["True", "False"],
                'explanation': f"This is correct: {warning}",
                'points': 12
            }
        else:
            false_warning = warning
            swaps = [
                ("edible", "poisonous"), ("safe", "dangerous"),
                ("cook", "eat raw"), ("hairy", "smooth"),
                ("round", "flat"), ("garlic", "onion"),
                ("must", "can skip")
            ]
            for orig, swap in swaps:
                if orig.lower() in warning.lower():
                    false_warning = warning.lower().replace(orig.lower(), swap.lower())
                    false_warning = false_warning[0].upper() + false_warning[1:]
                    break

            if false_warning == warning:
                return {
                    'type': 'warning', 'plant': plant,
                    'question': f"True or False: {warning}",
                    'correct': "True", 'options': ["True", "False"],
                    'explanation': f"This is correct: {warning}",
                    'points': 12
                }

            return {
                'type': 'warning', 'plant': plant,
                'question': f"True or False: {false_warning}",
                'correct': "False", 'options': ["True", "False"],
                'explanation': f"The correct warning is: {warning}",
                'points': 12
            }

    # Fallback
    return generate_foraging_question(plant, 'habitat')

# ==========================================
# SIDEBAR
# ==========================================
def render_sidebar():
    """Main sidebar: Auto-saves progress, shows stats, safety info."""
    # --- AUTO-SAVE ---
    # Automatically save progress to the database if the user is logged in
    if st.session_state.get('user') and st.session_state.get('game_loaded'):
        username = st.session_state.user.get('username')
        if username:
            data = get_save_data()
            save_game(username, data)

    # --- LOGO ---
    try:
        st.sidebar.image("logo.png", use_container_width=True)
    except:
        st.sidebar.title("🌿 Rocen Homesteady")

    st.sidebar.markdown("---")

    # --- PLAYER STATS ---
    total_edible = len(UK_PLANTS['edible'])
    collected = len(st.session_state.get('master_inventory', {}))
    st.sidebar.metric("🌱 Species Found", f"{collected}/{total_edible}")

    unlocked_count = sum(1 for v in st.session_state.get('achievements', {}).values() if v)
    total_ach = len(ACHIEVEMENTS)
    st.sidebar.metric("🏆 Achievements", f"{unlocked_count}/{total_ach}")

    unlocked_keys = [k for k, v in st.session_state.get('achievements', {}).items() if v]
    if unlocked_keys:
        st.sidebar.caption("Recently Unlocked:")
        for key in unlocked_keys[-3:]:
            st.sidebar.write(f"✅ {ACHIEVEMENTS[key]['name']}")

    # --- SAFETY ---
    st.sidebar.markdown("---")
    st.sidebar.warning("⚠️ **Safety First**")
    st.sidebar.markdown("""
    - Never eat a plant based solely on an app.
    - Always cross-reference with a field guide.
    - **UK Law:** Only pick for personal use.
    - It is illegal to uproot plants without permission.
    """)

    # --- RESET ---
    if st.sidebar.button("🗑️ Reset All Progress"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # --- BUSINESS ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 12px; line-height: 1.4;">
        <b>Rocen Homesteady LTD</b><br>
        4th Floor, 14 Museum Place<br>
        Cardiff, CF10 3BH
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# THEME
# ==========================================
def apply_brand_theme():
    st.markdown("""
    <style>
    /* ─── FONTS ─── */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ─── ROOT COLOURS ─── */
    :root {
        --bg-deep: #0a1a0a;
        --bg-main: #1a2e1a;
        --bg-card: #1e331e;
        --bg-card-hover: #264026;
        --green-leaf: #4CAF50;
        --green-light: #66BB6A;
        --green-dark: #2E7D32;
        --amber: #FFC107;
        --amber-dark: #FF8F00;
        --brown: #5D4037;
        --brown-light: #795548;
        --cream: #F5F0E8;
        --cream-dim: #B8AFA3;
        --danger: #ff5252;
        --danger-bg: #2a1010;
        --info-bg: #0a1a2a;
        --shadow: rgba(0, 0, 0, 0.4);
    }

    /* ─── APP BACKGROUND ─── */
    .stApp {
        background: linear-gradient(180deg, var(--bg-deep) 0%, var(--bg-main) 100%) !important;
        color: var(--cream) !important;
    }

    /* ─── MAIN CONTENT ─── */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* ─── TYPOGRAPHY ─── */
    h1, h2, h3, h4, h5, h6 {
        color: var(--cream) !important;
        font-family: 'Crimson Text', Georgia, serif !important;
    }
    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.6rem !important; border-bottom: 2px solid var(--green-dark) !important; padding-bottom: 0.5rem !important; }
    h3 { font-size: 1.3rem !important; }

    p, span, div, label, .stMarkdown, .stText {
        color: var(--cream) !important;
    }

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1f0d 0%, #142814 100%) !important;
        border-right: 1px solid #2d4a2d !important;
    }
    section[data-testid="stSidebar"] * {
        color: var(--cream) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown hr {
        border-color: #2d4a2d !important;
    }

    /* ─── BUTTONS ─── */
    .stButton > button {
        background: linear-gradient(135deg, var(--green-dark), var(--green-leaf)) !important;
        color: var(--cream) !important;
        border: 1px solid var(--green-light) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--green-leaf), var(--green-light)) !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    .stButton > button:focus {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.4) !important;
    }
    .stButton > button:disabled {
        background: #2a3a2a !important;
        color: #666 !important;
        border-color: #444 !important;
        box-shadow: none !important;
    }

    /* ─── TEXT INPUTS ─── */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        color: var(--cream) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--green-leaf) !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    .stTextInput > div > label {
        color: var(--cream-dim) !important;
    }

    /* ─── SELECTBOXES ─── */
    .stSelectbox > div > div {
        background: var(--bg-card) !important;
        color: var(--cream) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > label {
        color: var(--cream-dim) !important;
    }

    /* ─── CHECKBOXES ─── */
    .stCheckbox > label {
        color: var(--cream) !important;
    }
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] {
        color: var(--cream) !important;
    }

    /* ─── RADIO ─── */
    .stRadio > label {
        color: var(--cream) !important;
    }

    /* ─── EXPANDERS ─── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        color: var(--cream) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderHeader:hover {
        background: var(--bg-card-hover) !important;
        border-color: var(--green-leaf) !important;
    }
    .streamlit-expanderContent {
        border: 1px solid #3d5a3d !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ─── METRICS ─── */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
        border-left: 4px solid var(--green-leaf) !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--cream-dim) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--amber) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        color: var(--green-light) !important;
    }

    /* ─── PROGRESS BARS ─── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--green-dark), var(--green-leaf)) !important;
    }
    .stProgress > div > div > div {
        background: var(--bg-card) !important;
    }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        padding: 0.2rem !important;
        gap: 0.2rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--cream-dim) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-family: 'Inter', system-ui, sans-serif !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--green-dark) !important;
        color: var(--cream) !important;
        border: 1px solid var(--green-leaf) !important;
    }
    .stTabs [aria-selected="false"]:hover {
        background: var(--bg-card-hover) !important;
    }

    /* ─── ALERTS / TOASTS ─── */
    .stAlert {
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    [data-bd-type="success"] {
        background: #1a3d1a !important;
        border: 1px solid var(--green-leaf) !important;
        color: var(--cream) !important;
    }
    [data-bd-type="warning"] {
        background: #3d2e0a !important;
        border: 1px solid var(--amber) !important;
        color: var(--cream) !important;
    }
    [data-bd-type="error"] {
        background: var(--danger-bg) !important;
        border: 1px solid var(--danger) !important;
        color: var(--cream) !important;
    }
    [data-bd-type="info"] {
        background: var(--info-bg) !important;
        border: 1px solid #2196F3 !important;
        color: var(--cream) !important;
    }

    /* ─── DATAFRAMES ─── */
    .stDataFrame {
        border: 1px solid #3d5a3d !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar {
        width: 8px !important;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-deep) !important;
    }
    ::-webkit-scrollbar-thumb {
        background: #3d5a3d !important;
        border-radius: 4px !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--green-dark) !important;
    }

    /* ─── HIDE STREAMLIT BRANDING ─── */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }

    /* ─── SEPARATOR LINES ─── */
    hr {
        border-color: #2d4a2d !important;
    }

    /* ─── CONTAINER OVERRIDES ─── */
    .element-container {
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* ─── CAPTION ─── */
    .stCaption {
        color: var(--cream-dim) !important;
        font-size: 0.85rem !important;
    }

    /* ───────────────────────────────────────── */
    /* GAME-SPECIFIC STYLES                      */
    /* ───────────────────────────────────────── */

    /* Case file styling (Survival School) */
    .case-file {
        background: linear-gradient(135deg, #1a1a0a, #2a2a10) !important;
        border: 2px solid var(--amber-dark) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 16px rgba(255, 143, 0, 0.15) !important;
    }
    .case-file h3, .case-file h4 {
        color: var(--amber) !important;
        font-family: 'Crimson Text', Georgia, serif !important;
    }

    /* Safe card */
    .safe-card {
        background: linear-gradient(135deg, #0a2a0a, #1a3d1a) !important;
        border: 2px solid var(--green-leaf) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
    }

    /* Danger card */
    .danger-card {
        background: linear-gradient(135deg, #2a0a0a, #3d1515) !important;
        border: 2px solid var(--danger) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
    }

    /* Feedback boxes */
    .correct-feedback {
        background: linear-gradient(135deg, #0a2a0a, #1a3d1a) !important;
        border: 2px solid var(--green-leaf) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    .wrong-feedback {
        background: linear-gradient(135deg, #2a0a0a, #3d1515) !important;
        border: 2px solid var(--danger) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
    }

    /* Level up banner */
    .level-up {
        background: linear-gradient(135deg, #2a1a00, #3d2e00) !important;
        border: 2px solid var(--amber) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        box-shadow: 0 0 30px rgba(255, 193, 7, 0.3) !important;
    }

    /* Game card */
    .game-card {
        background: var(--bg-card) !important;
        border: 1px solid #3d5a3d !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
    }

    /* Streak flame */
    .streak-display {
        background: linear-gradient(135deg, #1a0a00, #2a1a00) !important;
        border: 2px solid var(--amber-dark) !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.2rem !important;
        text-align: center !important;
    }

    /* Plant card (for Foraging Quest etc.) */
    .plant-card {
        border-radius: 20px !important;
        padding: 20px !important;
        text-align: center !important;
        background: linear-gradient(145deg, var(--bg-card), var(--bg-deep)) !important;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.3) !important;
        margin-bottom: 20px !important;
        border: 1px solid #3d5a3d !important;
    }

    /* Grid game buttons (Eco-Village, Farm) */
    div.grid-game div.stButton > button {
        width: 100% !important; height: auto !important; aspect-ratio: 1 / 1 !important;
        padding: 0 !important; font-size: 1.5em !important;
        border: 1px solid #3d5a3d !important;
        background-color: #2b2b2b !important; color: white !important; border-radius: 8px !important;
    }
    div.grid-game div.stButton > button:hover { border-color: #fff !important; transform: scale(1.05) !important; }

    /* Market buttons */
    .market-box div.stButton > button { font-size: 14px !important; white-space: normal !important;
                                          height: auto !important; padding: 5px !important; }

    /* ─── RESPONSIVE ─── */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        .plant-card { padding: 10px !important; }
        div.grid-game div.stButton > button { font-size: 1em !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# AUDIO
# ==========================================
def clean_text_for_audio(text):
    if not text:
        return ""
    text = text.replace("**", "").replace("##", "").replace("*", "")
    icon_map = {
        "🌿": "Plant", "🌲": "Woodland", "☠️": "Poison", "✅": "Correct",
        "❌": "Wrong", "🕵️": "Inspector", "⚡": "Bonus", "🎓": "Graduate",
        "🌱": "Seedling", "🍄": "Mushroom", "🏖️": "Coastal", "🏡": "Urban",
        "🌾": "Meadow", "💧": "Water", "🪨": "Rock", "🌸": "Spring",
        "☀️": "Summer", "🍂": "Autumn", "❄️": "Winter", "🍃": "Leaves",
        "🌳": "Tree", "🐝": "Bee", "🍎": "Apple", "🫧": "Cold frame",
        "🥓": "Smokehouse", "🔋": "Battery", "☀️": "Solar", "🐔": "Chicken",
        "🐄": "Cow", "🐐": "Goat", "🌾": "Wheat", "🥕": "Carrot",
        "🌽": "Corn", "🐟": "Fish", "🥚": "Egg", "🥛": "Milk",
        "🍯": "Honey", "📏": "Rule", "📋": "Case", "🔍": "Observation",
        "⚖️": "Verdict", "🎯": "Target", "🔥": "Streak", "🤕": "Injured",
        "🛡️": "Shield", "🏆": "Trophy", "🏅": "Medal", "⚠️": "Warning",
        "📦": "Package", "💰": "Money", "🏗️": "Building", "🧹": "Clear",
    }
    for icon, word in icon_map.items():
        text = text.replace(icon, word)
    return text.strip()

def generate_voice(text, filename="temp_audio.mp3"):
    if not EDGE_TTS_AVAILABLE:
        return None
    import asyncio
    try:
        communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(communicate.save(filename))
        loop.close()
        return filename
    except Exception as e:
        print(f"Audio Error: {e}")
        return None

def get_week_in_month(day):
    """Calculates the week of the month (1-5) from the day number."""
    if day is None or day <= 0:
        return 1  # Default to week 1 if something goes wrong
    return (day - 1) // 7 + 1
