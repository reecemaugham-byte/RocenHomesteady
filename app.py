import streamlit as st
import base64
from datetime import datetime
from utils import init_session_state, apply_brand_theme, render_sidebar
from auth import render_auth, render_logout_sidebar
from plants_data import UK_PLANTS
from game_config import ACHIEVEMENTS

# ==========================================
# MONETISATION (inline)
# ==========================================
from datetime import datetime as _dt

AMAZON_TAG = "rocehomestead-21"
BMC_URL = "https://buymeacoffee.com/rocehomesteady"

AFFILIATE_PRODUCTS = {
    "books": [
        {
            "name": "📚 The Forager's Calendar",
            "author": "John Wright",
            "price": "£9.99",
            "desc": "Month-by-month guide to what's in season across the UK.",
            "url": f"https://www.amazon.co.uk/s?k=foragers+calendar+john+wright&tag={AMAZON_TAG}",
        },
        {
            "name": "📚 Food for Free",
            "author": "Richard Mabey",
            "price": "£7.49",
            "desc": "The classic foraging bible — over 250 wild plants, fruits, and fungi.",
            "url": f"https://www.amazon.co.uk/s?k=food+for+free+richard+mabey&tag={AMAZON_TAG}",
        },
        {
            "name": "📚 River Cottage Handbook: Hedgerow",
            "author": "John Wright",
            "price": "£10.49",
            "desc": "Everything you need to know about foraging in UK hedgerows.",
            "url": f"https://www.amazon.co.uk/s?k=river+cottage+hedgerow+john+wright&tag={AMAZON_TAG}",
        },
        {
            "name": "📚 Collins Mushroom Guide",
            "author": "Thomas Laessoe",
            "price": "£12.99",
            "desc": "The most trusted UK mushroom identification guide.",
            "url": f"https://www.amazon.co.uk/s?k=collins+mushroom+guide+laessoe&tag={AMAZON_TAG}",
        },
        {
            "name": "📚 Self-Sufficiency for the 21st Century",
            "author": "Dick & James Strawbridge",
            "price": "£14.99",
            "desc": "The complete guide to living off-grid in the UK.",
            "url": f"https://www.amazon.co.uk/s?k=self+sufficiency+21st+century+strawbridge&tag={AMAZON_TAG}",
        },
    ],
    "gear": [
        {
            "name": "🔪 Hultafors HVK Foraging Knife",
            "price": "£18.50",
            "desc": "The go-to knife for UK foragers — sharp, safe, and built to last.",
            "url": f"https://www.amazon.co.uk/s?k=hultafors+foraging+knife&tag={AMAZON_TAG}",
        },
        {
            "name": "🧺 Wicker Foraging Basket",
            "price": "£14.99",
            "desc": "Traditional basket — lets spores spread as you walk.",
            "url": f"https://www.amazon.co.uk/s?k=wicker+foraging+basket&tag={AMAZON_TAG}",
        },
        {
            "name": "🎒 Waterproof Roll-Top Bag",
            "price": "£12.99",
            "desc": "Keep your finds dry on wet foraging days.",
            "url": f"https://www.amazon.co.uk/s?k=waterproof+roll+top+bag+small&tag={AMAZON_TAG}",
        },
        {
            "name": "🔍 10x Plant Identification Loupe",
            "price": "£6.99",
            "desc": "Essential magnifier for examining leaves, stems, and spore prints.",
            "url": f"https://www.amazon.co.uk/s?k=10x+loupe+magnifier+plant&tag={AMAZON_TAG}",
        },
        {
            "name": "📖 Waterproof Field Notebook",
            "price": "£8.99",
            "desc": "Write in any weather. Perfect for recording foraging spots.",
            "url": f"https://www.amazon.co.uk/s?k=rite+in+the+rain+notebook&tag={AMAZON_TAG}",
        },
    ],
    "beekeeping": [
        {
            "name": "🐝 Practical Beekeeping",
            "author": "Clive de Bruyn",
            "price": "£12.99",
            "desc": "The essential guide to starting your first hive in the UK.",
            "url": f"https://www.amazon.co.uk/s?k=practical+beekeeping+clive+de+bruyn&tag={AMAZON_TAG}",
        },
        {
            "name": "🧤 Full Beekeeping Suit with Veil",
            "price": "£39.99",
            "desc": "Essential protection for hive inspections.",
            "url": f"https://www.amazon.co.uk/s?k=beekeeping+suit+full+body+veil&tag={AMAZON_TAG}",
        },
        {
            "name": "💨 Stainless Steel Bee Smoker",
            "price": "£24.99",
            "desc": "Calm your bees during inspections. Stainless steel with heat shield.",
            "url": f"https://www.amazon.co.uk/s?k=stainless+steel+bee+smoker&tag={AMAZON_TAG}",
        },
        {
            "name": "🏠 Cedar National Beehive",
            "price": "£149.99",
            "desc": "British Standard National hive in cedar. The most popular UK hive.",
            "url": f"https://www.amazon.co.uk/s?k=national+beehive+cedar+uk&tag={AMAZON_TAG}",
        },
    ],
}

DIGITAL_PRODUCTS = [
    {
        "name": "📋 UK Foraging Season Calendar 2025",
        "desc": "A3 printable wall calendar — every edible plant, month by month.",
        "price": "£4.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "📋",
    },
    {
        "name": "🍄 Mushroom Identification Flash Cards",
        "desc": "30 printable flashcards — common UK mushrooms, edible and deadly.",
        "price": "£3.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "🍄",
    },
    {
        "name": "☠️ Dangerous Lookalikes Cheat Sheet",
        "desc": "A4 printable — every dangerous plant side-by-side with its safe lookalike.",
        "price": "£2.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "☠️",
    },
    {
        "name": "🧒 Family Foraging Adventure Pack",
        "desc": "Complete family pack: ID cards, activity sheets, safety checklist, calendar. Ages 5-11.",
        "price": "£7.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "🧒",
    },
]

SEASON_PRODUCTS = {
    "Spring": {
        "name": "Spring Foraging Kit",
        "desc": "Everything you need for spring wild garlic and nettles",
        "url": f"https://www.amazon.co.uk/s?k=foraging+knife+basket+spring&tag={AMAZON_TAG}",
        "emoji": "🌸",
    },
    "Summer": {
        "name": "Summer Foraging Kit",
        "desc": "Berry-picking essentials for hedgerow harvests",
        "url": f"https://www.amazon.co.uk/s?k=foraging+bag+basket+summer&tag={AMAZON_TAG}",
        "emoji": "☀️",
    },
    "Autumn": {
        "name": "Autumn Mushroom Kit",
        "desc": "Mushroom hunting gear for the peak fungi season",
        "url": f"https://www.amazon.co.uk/s?k=mushroom+hunting+kit+identification&tag={AMAZON_TAG}",
        "emoji": "🍂",
    },
    "Winter": {
        "name": "Winter Foraging Guide",
        "desc": "What to forage in the cold months — plus a good thermos",
        "url": f"https://www.amazon.co.uk/s?k=winter+foraging+guide+book+uk&tag={AMAZON_TAG}",
        "emoji": "❄️",
    },
}


def render_affiliate_section():
    st.markdown("""
    <h3 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; text-align: center; margin-bottom: 0.3rem;">
        📚 Recommended Books & Gear
    </h3>
    <p style="color: var(--cream-dim); text-align: center; font-size: 0.85rem;">
        Hand-picked by our team. Purchases support the site at no extra cost to you.
    </p>
    """, unsafe_allow_html=True)

    tab_books, tab_gear, tab_bees = st.tabs(["📚 Books", "🔪 Gear", "🐝 Beekeeping"])

    with tab_books:
        for product in AFFILIATE_PRODUCTS["books"]:
            st.markdown(f"""
            <div class="game-card" style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div style="color: var(--green-leaf); font-weight: 700; font-size: 1rem;">{product['name']}</div>
                        <div style="color: var(--cream-dim); font-style: italic; font-size: 0.85rem;">by {product['author']}</div>
                        <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">{product['desc']}</div>
                    </div>
                    <div style="text-align: right; min-width: 90px; margin-left: 1rem;">
                        <div style="color: var(--amber); font-weight: 700; font-size: 1.1rem;">{product['price']}</div>
                        <a href="{product['url']}" target="_blank" rel="noopener noreferrer" style="
                            background: linear-gradient(135deg, #2E7D32, #4CAF50);
                            color: white; padding: 0.3rem 0.8rem; border-radius: 6px;
                            text-decoration: none; font-size: 0.8rem; font-weight: 600;
                            display: inline-block; margin-top: 0.3rem;
                        ">View on Amazon →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_gear:
        for product in AFFILIATE_PRODUCTS["gear"]:
            st.markdown(f"""
            <div class="game-card" style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div style="color: var(--green-leaf); font-weight: 700; font-size: 1rem;">{product['name']}</div>
                        <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">{product['desc']}</div>
                    </div>
                    <div style="text-align: right; min-width: 90px; margin-left: 1rem;">
                        <div style="color: var(--amber); font-weight: 700; font-size: 1.1rem;">{product['price']}</div>
                        <a href="{product['url']}" target="_blank" rel="noopener noreferrer" style="
                            background: linear-gradient(135deg, #2E7D32, #4CAF50);
                            color: white; padding: 0.3rem 0.8rem; border-radius: 6px;
                            text-decoration: none; font-size: 0.8rem; font-weight: 600;
                            display: inline-block; margin-top: 0.3rem;
                        ">View on Amazon →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_bees:
        for product in AFFILIATE_PRODUCTS["beekeeping"]:
            st.markdown(f"""
            <div class="game-card" style="margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div style="color: var(--amber); font-weight: 700; font-size: 1rem;">{product['name']}</div>
                        <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">{product['desc']}</div>
                    </div>
                    <div style="text-align: right; min-width: 90px; margin-left: 1rem;">
                        <div style="color: var(--amber); font-weight: 700; font-size: 1.1rem;">{product['price']}</div>
                        <a href="{product['url']}" target="_blank" rel="noopener noreferrer" style="
                            background: linear-gradient(135deg, #F57C00, #FFC107);
                            color: #1a1a1a; padding: 0.3rem 0.8rem; border-radius: 6px;
                            text-decoration: none; font-size: 0.8rem; font-weight: 600;
                            display: inline-block; margin-top: 0.3rem;
                        ">View on Amazon →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.caption("🔗 Links may earn us a small commission at no extra cost to you. We only recommend products we genuinely use and trust.")


def render_digital_products():
    st.markdown("""
    <h3 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; text-align: center; margin-bottom: 0.3rem;">
        📥 Printable Downloads
    </h3>
    <p style="color: var(--cream-dim); text-align: center; font-size: 0.85rem;">
        Instant PDF downloads to take on your foraging adventures.
    </p>
    """, unsafe_allow_html=True)

    for product in DIGITAL_PRODUCTS:
        st.markdown(f"""
        <div class="game-card" style="margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="color: var(--green-leaf); font-weight: 700; font-size: 1.05rem;">{product['emoji']} {product['name']}</div>
                    <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">{product['desc']}</div>
                </div>
                <div style="text-align: right; min-width: 100px; margin-left: 1rem;">
                    <div style="color: var(--amber); font-weight: 700; font-size: 1.2rem;">{product['price']}</div>
                    <a href="{product['url']}" target="_blank" rel="noopener noreferrer" style="
                        background: linear-gradient(135deg, #2E7D32, #4CAF50);
                        color: white; padding: 0.4rem 1rem; border-radius: 8px;
                        text-decoration: none; font-size: 0.85rem; font-weight: 700;
                        display: inline-block; margin-top: 0.3rem;
                    ">Get PDF →</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.caption("📥 All downloads are PDF files — print at home or take to a print shop for best results.")


def render_support_section():
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a2e1a, #0a1a0a);
        border: 1px solid #3d5a3d;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    ">
        <h3 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; margin: 0 0 0.5rem 0;">
            ☕ Support Rocen Homesteady
        </h3>
        <p style="color: var(--cream-dim); font-size: 0.95rem; max-width: 550px; margin: 0 auto 0.8rem auto; line-height: 1.6;">
            This site is <b>100%% free</b> for everyone. No paywalls, no ads, no premium tiers.
            If it's helped you identify a plant, learn a new skill, or stay safe in the wild —
            consider buying us a coffee. Every penny goes toward keeping the site running and adding new content.
        </p>
        <div style="margin-top: 1rem;">
            <a href="{BMC_URL}" target="_blank" rel="noopener noreferrer" style="
                background: linear-gradient(135deg, #FFDD00, #F5A623);
                color: #1a1a1a;
                padding: 0.7rem 2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 700;
                font-size: 1.1rem;
                display: inline-block;
                box-shadow: 0 4px 15px rgba(245, 166, 35, 0.3);
            ">☕ Buy Me a Coffee</a>
        </div>
        <p style="color: var(--cream-dim); font-size: 0.75rem; margin-top: 0.8rem;">
            🌿 Thank you for supporting independent foraging education.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_newsletter_signup():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0a2a0a, #1a3d1a);
        border: 2px solid var(--green-leaf);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
    ">
        <h3 style="color: var(--green-leaf); font-family: 'Crimson Text', Georgia, serif; margin: 0 0 0.5rem 0;">
            🌿 Free Monthly Foraging Newsletter
        </h3>
        <p style="color: var(--cream-dim); font-size: 0.9rem;">
            Get seasonal foraging tips, new plant guides, and safety alerts delivered to your inbox.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_nl1, col_nl2 = st.columns([3, 1])
    with col_nl1:
        email = st.text_input("📧 Your email address", placeholder="forager@example.co.uk", label_visibility="collapsed", key="newsletter_email")
    with col_nl2:
        if st.button("🌿 Subscribe", use_container_width=True, type="primary", key="newsletter_subscribe_btn"):
            if email and "@" in email and "." in email:
                st.success("🌿 Welcome to the foraging community! Check your inbox for a confirmation.")
            else:
                st.warning("Please enter a valid email address.")


def render_seasonal_affiliate_badge():
    current_month = datetime.now().strftime("%B")
    SEASON_MONTHS = {
        "Spring": ["March", "April", "May"],
        "Summer": ["June", "July", "August"],
        "Autumn": ["September", "October", "November"],
        "Winter": ["December", "January", "February"],
    }
    current_season = "Winter"
    for season, months in SEASON_MONTHS.items():
        if current_month in months:
            current_season = season
            break
    product = SEASON_PRODUCTS.get(current_season, SEASON_PRODUCTS["Winter"])

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, var(--bg-card), var(--bg-deep));
        border: 1px solid #3d5a3d;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0.5rem 0;
    ">
        <div>
            <div style="color: var(--green-leaf); font-weight: 700; font-size: 0.95rem;">
                {product['emoji']} {product['name']}
            </div>
            <div style="color: var(--cream-dim); font-size: 0.8rem;">{product['desc']}</div>
        </div>
        <a href="{product['url']}" target="_blank" rel="noopener noreferrer" style="
            background: linear-gradient(135deg, #2E7D32, #4CAF50);
            color: white; padding: 0.4rem 0.8rem; border-radius: 6px;
            text-decoration: none; font-size: 0.8rem; font-weight: 600;
            white-space: nowrap;
        ">Shop →</a>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Rocen Homesteady",
    page_icon="Blogo.png",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- INIT ---
init_session_state()
apply_brand_theme()
user = render_auth()
render_logout_sidebar()

# --- LOGO ABOVE SIDEBAR NAVIGATION ---
try:
    with open("Blogo.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode("utf-8")
    
    css_logo = """
    <style>
        [data-testid="stSidebarNav"] > span {
            display: none !important;
        }
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
    st.sidebar.warning("Blogo.png not found.")

render_sidebar()

# --- DYNAMIC SEASONAL DATA ---
current_month = datetime.now().strftime("%B")
SEASON_MONTHS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"]
}

current_season = "Winter"
for season, months in SEASON_MONTHS.items():
    if current_month in months:
        current_season = season
        break

SEASON_ICONS = {
    "Spring": "🌸", "Summer": "☀️", "Autumn": "🍂", "Winter": "❄️"
}

SEASON_COLOURS = {
    "Spring": "#4CAF50", "Summer": "#FFC107", "Autumn": "#FF8F00", "Winter": "#90CAF9"
}

# Find plants in season right now
plants_in_season = [p for p in UK_PLANTS['edible']
                    if current_month in p.get('months', [])]
plants_in_season.sort(key=lambda p: p.get('difficulty', 1))

# Featured poisonous plants
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
# HERO SECTION
# ==========================================

try:
    st.image("Blogo.png", width=220)
except:
    st.markdown("# 🌿 Rocen Homesteady")

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0a1a0a 0%, #1a2e1a 40%, {SEASON_COLOURS.get(current_season, '#2E7D32')}22 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin: -0.5rem -1rem 2rem -1rem;
    text-align: center;
    border: 1px solid #2d4a2d;
">
    <h2 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; font-size: 1.8rem; margin: 0 0 0.5rem 0;">
        The UK's Ultimate Foraging Companion
    </h2>
    <p style="color: var(--cream-dim); font-size: 1rem; max-width: 600px; margin: 0 auto;">
        Learn to identify, forage, and appreciate the wild plants around you.
        Your personal field guide to the natural world.
    </p>
    <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <a href="https://discord.gg/S5hwKD3q" target="_blank" style="
            background: linear-gradient(135deg, #5865F2, #7289DA);
            color: white;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            display: inline-block;
        ">💬 Join Our Discord</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SEASONAL SECTION
# ==========================================

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {SEASON_COLOURS.get(current_season, '#4CAF50')}15, var(--bg-card));
    border: 2px solid {SEASON_COLOURS.get(current_season, '#4CAF50')}40;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
">
    <h3 style="color: {SEASON_COLOURS.get(current_season, '#4CAF50')}; font-family: 'Crimson Text', Georgia, serif; margin: 0 0 1rem 0;">
        {SEASON_ICONS.get(current_season, '🌸')} What's in Season — {current_month}
    </h3>
</div>
""", unsafe_allow_html=True)

col_eat1, col_eat2, col_eat3 = st.columns(3)

with col_eat1:
    if plants_in_season:
        p = plants_in_season[0]
        difficulty_stars = "🌱" * min(p.get('difficulty', 1), 3)
        st.markdown(f"""
        <div class="game-card">
            <div style="color: var(--green-leaf); font-weight: 700; font-size: 1.1rem;">🌿 {p['name']}</div>
            <div style="color: var(--cream-dim); font-style: italic; font-size: 0.85rem;">{p.get('latin_name', '')}</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem;">📖 {p.get('description', '')[:100]}...</div>
            <div style="color: var(--amber); font-size: 0.8rem; margin-top: 0.3rem;">{difficulty_stars} Difficulty</div>
        </div>
        """, unsafe_allow_html=True)

with col_eat2:
    if len(plants_in_season) > 1:
        p = plants_in_season[1]
        difficulty_stars = "🌱" * min(p.get('difficulty', 1), 3)
        st.markdown(f"""
        <div class="game-card">
            <div style="color: var(--green-leaf); font-weight: 700; font-size: 1.1rem;">🌿 {p['name']}</div>
            <div style="color: var(--cream-dim); font-style: italic; font-size: 0.85rem;">{p.get('latin_name', '')}</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem;">📖 {p.get('description', '')[:100]}...</div>
            <div style="color: var(--amber); font-size: 0.8rem; margin-top: 0.3rem;">{difficulty_stars} Difficulty</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("More plants available in the Learning Center")

with col_eat3:
    if len(plants_in_season) > 2:
        p = plants_in_season[2]
        difficulty_stars = "🌱" * min(p.get('difficulty', 1), 3)
        st.markdown(f"""
        <div class="game-card">
            <div style="color: var(--green-leaf); font-weight: 700; font-size: 1.1rem;">🌿 {p['name']}</div>
            <div style="color: var(--cream-dim); font-style: italic; font-size: 0.85rem;">{p.get('latin_name', '')}</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem;">📖 {p.get('description', '')[:100]}...</div>
            <div style="color: var(--amber); font-size: 0.8rem; margin-top: 0.3rem;">{difficulty_stars} Difficulty</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("More plants available in the Learning Center")

st.caption(f"📊 {len(plants_in_season)} plants available this month — see the full list in the Learning Center")

# --- Seasonal affiliate recommendation ---
render_seasonal_affiliate_badge()

# ==========================================
# DANGER WARNING
# ==========================================

st.markdown(f"""
<div style="background: var(--danger-bg); border: 2px solid var(--danger); border-radius: 12px; padding: 1rem 1.5rem; margin: 1.5rem 0;">
    <div style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">⚠️ Safety First</div>
    <ul style="color: var(--cream); font-size: 0.9rem; line-height: 1.6; margin: 0; padding-left: 1.2rem;">
        <li><b>Never eat a plant based solely on an app.</b> Always cross-reference with a field guide or expert.</li>
        <li><b>If in doubt, leave it out.</b> This is the #1 rule of foraging.</li>
        <li><b>UK Law:</b> Only pick the Four Fs (Fruit, Foliage, Flowers, Fungi) for personal use.</li>
        <li><b>It is illegal to uproot plants</b> without the landowner's permission.</li>
        <li><b>Scotland has different rules</b> — see our Law lesson for details.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SURVIVAL SCHOOL HERO
# ==========================================

danger1 = dangerous_now[0] if len(dangerous_now) > 0 else UK_PLANTS['poisonous'][0]
danger2 = None
safe_match = None

for p in UK_PLANTS['edible']:
    for la in p.get('lookalikes', []):
        if la.get('name') == danger1['name']:
            safe_match = p
            break
    if safe_match:
        break

if len(dangerous_now) > 1:
    danger2 = dangerous_now[1]

st.markdown("---")

st.markdown(f"""
<div style="background: linear-gradient(135deg, #1a0000, #2a0a0a); border: 2px solid var(--danger); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;">
    <h3 style="color: var(--danger); font-family: 'Crimson Text', Georgia, serif; margin: 0 0 1rem 0;">☠️ Can You Tell Them Apart?</h3>
</div>
""", unsafe_allow_html=True)

hero_col1, hero_col2 = st.columns(2)

with hero_col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border: 2px solid var(--green-leaf); border-radius: 12px; padding: 1rem;">
        <div style="color: var(--green-leaf); font-weight: 700; font-size: 0.9rem; margin-bottom: 0.3rem;">{SEASON_ICONS.get(current_season, '🌸')} IN SEASON NOW</div>
        <div style="color: var(--cream); font-size: 0.95rem;"><b>{len(plants_in_season)} edible plants</b> are available this month.</div>
    </div>
    """, unsafe_allow_html=True)
    if safe_match:
        st.success(f"✅ **{safe_match['name']}** is safe to eat — but watch out for its dangerous lookalike!")
    else:
        st.success(f"✅ Plants like **{plants_in_season[0]['name']}** are available now.")

with hero_col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2a0a0a, #3d1515); border: 2px solid var(--danger); border-radius: 12px; padding: 1rem;">
        <div style="color: var(--danger); font-weight: 700; font-size: 0.9rem; margin-bottom: 0.3rem;">☠️ DANGER THIS MONTH</div>
        <div style="color: var(--cream); font-size: 0.95rem;"><b>{danger1['name']}</b> — {danger1.get('danger_tips', {}).get('danger_zone', 'Dangerous')}</div>
    </div>
    """, unsafe_allow_html=True)
    if danger1.get('confusion_notes'):
        st.warning(f"🔍 {danger1['confusion_notes']}")
    if danger2:
        st.error(f"☠️ **{danger2['name']}** — also dangerous this month")

if st.button("🛡️ Test Your Safety Knowledge — Go to Survival School", use_container_width=True):
    st.switch_page("pages/2_Forage.py")
if st.button("🐝 Manage Your Own Beehive — Go to Apiary Manager", use_container_width=True):
    st.switch_page("pages/5_Apiary.py")

# ==========================================
# FOOD GROUPS
# ==========================================

st.markdown("---")

st.markdown(f"""
<div style="text-align: center; margin-bottom: 1rem;">
    <h2 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif;">🌿🏘️🚜🐝 The Food Groups</h2>
    <p style="color: var(--cream-dim);">Foragers, Off-Grid Dwellers, Farmers, and Beekeepers — four paths, one goal: sustainable food.</p>
</div>
""", unsafe_allow_html=True)

group1, group2, group3, group4 = st.columns(4)

with group1:
    st.markdown(f"""
    <div class="game-card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.3rem;">🌿</div>
        <div style="color: var(--green-leaf); font-weight: 700; font-size: 1rem;">Foragers</div>
        <div style="color: var(--cream-dim); font-size: 0.8rem; text-align: left; margin-top: 0.5rem;">
            <b>Find</b> food in the wild.<br><br>
            • Identify plants safely<br>
            • Know what's in season<br>
            • Spot dangerous lookalikes<br>
            • Respect nature and the law
        </div>
    </div>
    """, unsafe_allow_html=True)

with group2:
    st.markdown(f"""
    <div class="game-card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.3rem;">🏘️</div>
        <div style="color: var(--amber); font-weight: 700; font-size: 1rem;">Off-Grid Dwellers</div>
        <div style="color: var(--cream-dim); font-size: 0.8rem; text-align: left; margin-top: 0.5rem;">
            <b>Preserve</b> food for year-round use.<br><br>
            • Store and preserve harvests<br>
            • Cook with wild ingredients<br>
            • Reduce food waste<br>
            • Live sustainably
        </div>
    </div>
    """, unsafe_allow_html=True)

with group3:
    st.markdown(f"""
    <div class="game-card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.3rem;">🚜</div>
        <div style="color: var(--amber-dark); font-weight: 700; font-size: 1rem;">Farmers</div>
        <div style="color: var(--cream-dim); font-size: 0.8rem; text-align: left; margin-top: 0.5rem;">
            <b>Grow</b> food on the land.<br><br>
            • Plan crops for all seasons<br>
            • Companion planting & rotation<br>
            • Manage resources wisely<br>
            • Work with nature, not against it
        </div>
    </div>
    """, unsafe_allow_html=True)

with group4:
    st.markdown(f"""
    <div class="game-card" style="text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.3rem;">🐝</div>
        <div style="color: var(--amber); font-weight: 700; font-size: 1rem;">Beekeepers</div>
        <div style="color: var(--cream-dim); font-size: 0.8rem; text-align: left; margin-top: 0.5rem;">
            <b>Steward</b> the pollinators.<br><br>
            • Inspect hives weekly<br>
            • Treat for varroa mites<br>
            • Harvest honey sustainably<br>
            • Support biodiversity
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="background: linear-gradient(135deg, var(--bg-card), var(--bg-deep)); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1rem; text-align: center; margin: 1rem 0;">
    <span style="color: var(--green-leaf);">🌿</span> ➡️ 
    <span style="color: var(--amber);">🏘️</span> ➡️ 
    <span style="color: var(--amber-dark);">🚜</span> ➡️ 
    <span style="color: var(--amber);">🐝</span>
    <span style="color: var(--cream-dim); font-size: 0.9rem;"> Foragers find it. Off-Grid Dwellers preserve it. Farmers grow it. Beekeepers protect the pollinators.</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# STATS
# ==========================================

st.markdown("---")
stat1, stat2, stat3 = st.columns(3)
stat1.metric("🌱 Plants Database", f"{len(UK_PLANTS['edible'])}+")
stat2.metric("⚠️ Safety Warnings", f"{len(UK_PLANTS['poisonous'])}+")
stat3.metric("🎮 Interactive Games", "8")

# ==========================================
# GAMES WITH CURRICULUM
# ==========================================

st.markdown("---")
st.markdown(f"""
<h2 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; text-align: center; margin-bottom: 0.5rem;">🎮 Games & Practice</h2>
<p style="color: var(--cream-dim); text-align: center;">Each game links to the National Curriculum. Click a game to start learning!</p>
""", unsafe_allow_html=True)

game_cols = st.columns(3)
game_items = list(GAME_LINKS.items())

for i, (game_name, game_info) in enumerate(game_items):
    with game_cols[i % 3]:
        st.markdown(f"""
        <div class="game-card" style="text-align: center; margin-bottom: 0.8rem;">
            <div style="font-size: 1.3rem; font-weight: 700; color: var(--cream);">{game_name}</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin: 0.3rem 0;">{game_info['desc']}</div>
            <div style="color: var(--amber); font-size: 0.75rem;">📚 {' | '.join(game_info['curriculum'])}</div>
            <div style="color: var(--cream-dim); font-size: 0.75rem;">👦 Age: {game_info['age']}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HOW TO USE & LAW
# ==========================================

st.markdown("---")

left_col, right_col = st.columns(2)

with left_col:
    st.markdown(f"""
    <div class="game-card">
        <h3 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; margin: 0 0 0.8rem 0;">📖 How to Use This App</h3>
        <ol style="color: var(--cream-dim); font-size: 0.9rem; line-height: 1.8; padding-left: 1.2rem;">
            <li><b>Learn:</b> Study plants, trees, and fungi in the <b>Learning</b> section.</li>
            <li><b>Play:</b> Test your skills in the <b>Games</b> section (6 unique games!).</li>
            <li><b>Track:</b> Check your rank and stats in the <b>Sidebar</b>.</li>
        </ol>
        <div style="color: var(--amber); font-size: 0.9rem; margin-top: 0.5rem;"><b>New?</b> Start with ☠️ <b>Survival School</b> — it could save your life.</div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown(f"""
    <div class="game-card">
        <h3 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; margin: 0 0 0.8rem 0;">🏛️ UK Law & Foraging</h3>
        <p style="color: var(--cream-dim); font-size: 0.9rem; line-height: 1.6;">
            <b>The law is different in the UK</b> compared to the US, EU, and Australia.
        </p>
        <ul style="color: var(--cream-dim); font-size: 0.9rem; line-height: 1.8; padding-left: 1.2rem;">
            <li>✅ You CAN pick the Four Fs for personal use</li>
            <li>❌ You CANNOT uproot wild plants without permission</li>
            <li>❌ You CANNOT forage on SSSIs (protected sites)</li>
            <li>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland has stronger right-to-roam laws</li>
        </ul>
        <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem;">📖 Learn the full details in our <b>UK Foraging Law</b> lesson.</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MONETISATION — Books, Gear, Downloads, Support
# ==========================================

st.markdown("---")

tab_shop, tab_downloads, tab_support = st.tabs(["📚 Books & Gear", "📥 Downloads", "☕ Support Us"])

with tab_shop:
    render_affiliate_section()

with tab_downloads:
    render_digital_products()

with tab_support:
    render_support_section()
    st.markdown("---")
    render_newsletter_signup()

# ==========================================
# DISCORD & FOOTER
# ==========================================

st.markdown("---")

st.markdown(f"""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <a href="https://discord.gg/S5hwKD3q" target="_blank" style="
        background: linear-gradient(135deg, #5865F2, #7289DA);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        display: inline-block;
    ">💬 Join Our Discord Community</a>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: var(--cream-dim); font-size: 0.75rem;">© 2026 Rocen Homesteady LTD. All Rights Reserved. Educational Use Only. UK-specific information — check local laws for other countries.</p>
    <p style="color: var(--cream-dim); font-size: 0.75rem;">📧 <a href="mailto:Support@RocenHomesteady.co.uk" style="color: var(--green-leaf); text-decoration: none;">Support@RocenHomesteady.co.uk</a> | 💬 <a href="https://discord.gg/S5hwKD3q" target="_blank" style="color: #5865F2; text-decoration: none;">Discord</a></p>
</div>
""", unsafe_allow_html=True)
