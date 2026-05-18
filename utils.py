import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from openai import OpenAI
import os
import json
import asyncio

# --- DATA IMPORTS ---
# Importing data from the separate files we created
from plants_data import UK_PLANTS
from lessons_data import LESSON_CONTENT
from game_config import ACHIEVEMENTS

# --- SAFE IMPORTS ---
try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import alpaca_trade_api as tradeapi
except ImportError:
    tradeapi = None

try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
except ImportError:
    Image = None

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# --- CONFIGURATION & API ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "sk-proj--" # Placeholder

if not api_key:
    client = None
else:
    try:
        client = OpenAI(api_key=api_key)
    except:
        client = None

# --- SESSION STATE INIT ---
def init_session_state():
    defaults = {
        'game_score': 0, 
        'game_lives': 3, 
        'game_streak': 0, 
        'current_question': None,
        'village': None, 
        'farm_game': None, 
        'survival_lives': 3, 
        'survival_score': 0,
        'current_survival_pair': None, 
        'quiz_score': 0, 
        'quiz_q_num': 0, 
        'quiz_max': 5,
        'q_data': None, 
        'chat_language': 'English', 
        'messages': [], 
        'selected_page': "Home",
        'book_content': {}, 
        'book_outline': "", 
        'active_season': "Summer",
        'season_badge_progress': [], 
        'survival_correct_count': 0, 
        'survival_current_case': None,
        'survival_result': None, 
        'daily_streak': 0, 
        'quiz_active': False, 
        'module_questions': None,
        'player_title': "Novice Gatherer",
        'total_plants_identified': 0,
        'total_xp': 0,
        'completed_modules': [],
        # --- UNIFIED INVENTORY ---
        'master_inventory': {}, # Replaces separate lists
        'kitchen_inventory': {}, # Deprecated but kept for safety
        'collection_edible': [], # Deprecated but kept for safety
        
        'game_streak_bonus': False,
        'achievements': {k: False for k in ACHIEVEMENTS.keys()}, # Initialize achievements
        'unlocked_recipes': [], # For Kitchen game
        'kitchen_score': 0 # For Kitchen game
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# --- THEME FUNCTION ---
def apply_brand_theme():
    st.markdown("""
    <style>
    /* --- Main Background - Dark Earth --- */
    .stApp, section.main > div {
        background-color: #3A2416; /* Dark Coffee */
    }

    /* --- Text Color - White for contrast --- */
    .stMarkdown, .stHeader, p, label, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        color: #FFFFFF !important; 
    }

    /* --- Headings - Copper --- */
    h1, h2, h3 {
        color: #B87333 !important; /* COPPER */
        font-family: 'Georgia', serif !important;
        border-bottom: 2px solid #6B4226; /* Saddle Brown underline */
        padding-bottom: 10px;
    }

    /* --- Buttons - Saddle Brown --- */
    .stButton > button {
        background-color: #6B4226; /* Saddle Brown */
        color: white !important;
        border-radius: 20px;
        border: 1px solid #B87333; /* COPPER border */
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #B87333; /* COPPER Hover */
        color: #FFFFFF !important; 
        transform: scale(1.02);
    }

    /* --- Sidebar - Deep Evergreen --- */
    [data-testid="stSidebar"] {
        background-color: #1B3A28; /* DARKER GREEN */
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* White text on green */
    }
    
    /* Sidebar specific adjustments */
    [data-testid="stSidebar"] .stMarkdown hr {
        border-color: #B87333; /* Copper divider */
    }

    /* --- Metric Boxes - Wood Brown --- */
    [data-testid="stMetric"] {
        background-color: #6B4226; /* Saddle Brown */
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 0 1px #B87333; /* COPPER outline */
        border-left: 5px solid #B87333; /* COPPER left bar */
        color: white;
    }
    [data-testid="stMetric"] label {
        color: #B87333 !important; /* COPPER Label */
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important; /* Value Color */
    }

    /* --- Tabs --- */
    .stTabs [data-badges="badge"] {
        background-color: #3F5F2A;
        color: #FFFFFF;
    }
    button[aria-selected="true"] {
        background-color: #B87333 !important; /* COPPER active tab */
        color: #FFFFFF !important;
        border-bottom: 2px solid #6B4226;
    }

    /* --- Expander --- */
    .streamlit-expanderHeader {
        background-color: #6B4226 !important; /* Saddle Brown */
        border-radius: 10px;
        border-left: 5px solid #B87333; /* COPPER left bar */
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* --- Input Fields --- */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
        background-color: #3F5F2A !important; /* Green input bg */
        color: #FFFFFF !important;
        border: 1px solid #B87333; /* COPPER border */
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FOR AUDIO ---
def generate_voice(text, filename="temp_audio.mp3"):
    if not EDGE_TTS_AVAILABLE:
        return None
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

# --- SIDEBAR FUNCTION ---
def render_sidebar():
    # --- LOGO SECTION ---
    try:
        st.sidebar.image("logo.png", width=150)
    except:
        st.sidebar.title("🌿 Rocen Homesteady")

    # --- PLAYER STATS ---
    st.sidebar.markdown(f"**🎓 Rank:** {st.session_state.player_title}")
    st.sidebar.markdown(f"**🌱 Plants ID'd:** {st.session_state.total_plants_identified}")
    
    # Show Unified Inventory Count
    inv_count = sum(st.session_state.master_inventory.values()) if 'master_inventory' in st.session_state else 0
    st.sidebar.markdown(f"**🎒 Inventory:** {inv_count} items")
    
    st.sidebar.markdown("---")

    # --- SAFETY INFO ---
    st.sidebar.warning("⚠️ **Safety First**")
    st.sidebar.markdown("""
    - Never eat a plant based solely on app ID.
    - Always cross-reference with a field guide.
    - **UK Law:** Only pick for personal use.
    - It is illegal to uproot plants without permission.
    """)

    # --- RESET BUTTON ---
    if st.sidebar.button("🔄 Reset All Progress"):
        # Reset Game Stats
        st.session_state.game_score = 0
        st.session_state.game_lives = 3
        st.session_state.game_streak = 0
        st.session_state.survival_lives = 3
        st.session_state.survival_score = 0
        st.session_state.survival_correct_count = 0
        st.session_state.total_plants_identified = 0
        st.session_state.player_title = "Novice Gatherer"
        st.session_state.season_badge_progress = []
        
        # Reset Inventories
        st.session_state.master_inventory = {}
        st.session_state.village = None
        st.session_state.farm_game = None
        st.session_state.kitchen_inventory = {}
        
        # Reset Achievements
        st.session_state.achievements = {k: False for k in ACHIEVEMENTS.keys()}
        st.session_state.unlocked_recipes = []
        st.session_state.kitchen_score = 0
        
        st.sidebar.success("Progress Reset! Refreshing...")
        st.rerun()

    # --- BUSINESS DETAILS ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 12px; line-height: 1.4;">
        <b>Rocen Homesteady LTD</b><br>
        4th Floor<br>
        14 Museum Place, City Centre<br>
        Cardiff<br>
        CF10 3BH
    </div>
    """, unsafe_allow_html=True)

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    init_session_state()
    apply_brand_theme()
    render_sidebar()
    
    st.title("🌿 Foraging Learning Platform")
    st.write("Welcome! Use the sidebar to navigate or start a lesson below.")
    
    # Basic Example Usage (Placeholder)
    lesson_names = list(LESSON_CONTENT.keys())
    selected_lesson = st.selectbox("Choose a Lesson:", lesson_names)
    
    if st.button("Start Lesson"):
        st.session_state['selected_page'] = selected_lesson
        st.write(f"Loading {selected_lesson}...") # In a full app, this would switch pages/modes
