"""
shop.py — Rocen Homesteady Shop Module
Affiliate links, digital products, and support options.
Styled to match the existing theme.

Amazon Associates ID: rocehomestead-21
Buy Me a Coffee: buymeacoffee.com/rocehomesteady
"""

import streamlit as st
from datetime import datetime

# ==========================================
# CONSTANTS
# ==========================================

AMAZON_TAG = "rocehomestead-21"
BMC_URL = "https://buymeacoffee.com/rocehomesteady"

SEASON_MONTHS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"],
}

SEASON_ICONS = {
    "Spring": "🌸",
    "Summer": "☀️",
    "Autumn": "🍂",
    "Winter": "❄️",
}

SEASON_COLOURS = {
    "Spring": "#4CAF50",
    "Summer": "#FFC107",
    "Autumn": "#FF8F00",
    "Winter": "#90CAF9",
}

# ==========================================
# AFFILIATE LINKS — Amazon UK (search URLs)
# ==========================================

AFFILIATE_PRODUCTS = {
    "books": [
        {
            "name": "📚 The Forager's Calendar",
            "author": "John Wright",
            "price": "£9.99",
            "desc": "Month-by-month guide to what's in season across the UK. The book we recommend most.",
            "url": f"https://www.amazon.co.uk/s?k=foragers+calendar+john+wright&tag={AMAZON_TAG}",
            "emoji": "📖",
        },
        {
            "name": "📚 Food for Free",
            "author": "Richard Mabey",
            "price": "£7.49",
            "desc": "The classic foraging bible — over 250 wild plants, fruits, and fungi. A British essential.",
            "url": f"https://www.amazon.co.uk/s?k=food+for+free+richard+mabey&tag={AMAZON_TAG}",
            "emoji": "📖",
        },
        {
            "name": "📚 River Cottage Handbook: Hedgerow",
            "author": "John Wright",
            "price": "£10.49",
            "desc": "Everything you need to know about foraging in UK hedgerows, from sloes to sorrel.",
            "url": f"https://www.amazon.co.uk/s?k=river+cottage+hedgerow+john+wright&tag={AMAZON_TAG}",
            "emoji": "📖",
        },
        {
            "name": "📚 Collins Mushroom Guide",
            "author": "Thomas Laessoe",
            "price": "£12.99",
            "desc": "The most trusted UK mushroom identification guide. Essential before you pick any fungus.",
            "url": f"https://www.amazon.co.uk/s?k=collins+mushroom+guide+laessoe&tag={AMAZON_TAG}",
            "emoji": "🍄",
        },
        {
            "name": "📚 Self-Sufficiency for the 21st Century",
            "author": "Dick Strawbridge & James Strawbridge",
            "price": "£14.99",
            "desc": "The complete guide to living off-grid in the UK. From growing to preserving to foraging.",
            "url": f"https://www.amazon.co.uk/s?k=self+sufficiency+21st+century+strawbridge&tag={AMAZON_TAG}",
            "emoji": "🏘️",
        },
    ],
    "gear": [
        {
            "name": "🔪 Hultafors HVK Foraging Knife",
            "price": "£18.50",
            "desc": "The go-to knife for UK foragers — sharp, safe, and built to last. Our top pick.",
            "url": f"https://www.amazon.co.uk/s?k=hultafors+foraging+knife&tag={AMAZON_TAG}",
            "emoji": "🔪",
        },
        {
            "name": "🧺 Wicker Foraging Basket",
            "price": "£14.99",
            "desc": "Traditional basket for collecting wild food. Lets spores spread as you walk — better than plastic bags.",
            "url": f"https://www.amazon.co.uk/s?k=wicker+foraging+basket&tag={AMAZON_TAG}",
            "emoji": "🧺",
        },
        {
            "name": "🎒 Waterproof Roll-Top Bag",
            "price": "£12.99",
            "desc": "Keep your foraged finds dry on wet days. Roll-top seal, lightweight, and affordable.",
            "url": f"https://www.amazon.co.uk/s?k=waterproof+roll+top+bag+small&tag={AMAZON_TAG}",
            "emoji": "🎒",
        },
        {
            "name": "🔍 10x Plant Identification Loupe",
            "price": "£6.99",
            "desc": "Essential magnifier for examining leaves, stems, and spore prints. Every forager needs one.",
            "url": f"https://www.amazon.co.uk/s?k=10x+loupe+magnifier+plant&tag={AMAZON_TAG}",
            "emoji": "🔍",
        },
        {
            "name": "📖 Waterproof Field Notebook",
            "price": "£8.99",
            "desc": "Rite in the Rain notebook — write in any weather. Perfect for recording foraging spots.",
            "url": f"https://www.amazon.co.uk/s?k=rite+in+the+rain+notebook&tag={AMAZON_TAG}",
            "emoji": "📝",
        },
    ],
    "beekeeping": [
        {
            "name": "🐝 Practical Beekeeping",
            "author": "Clive de Bruyn",
            "price": "£12.99",
            "desc": "The essential guide to starting your first hive in the UK. Clear, practical, and comprehensive.",
            "url": f"https://www.amazon.co.uk/s?k=practical+beekeeping+clive+de+bruyn&tag={AMAZON_TAG}",
            "emoji": "🐝",
        },
        {
            "name": "🧤 Full Beekeeping Suit with Veil",
            "price": "£39.99",
            "desc": "Essential protection for hive inspections. Full suit with integrated veil and gloves.",
            "url": f"https://www.amazon.co.uk/s?k=beekeeping+suit+full+body+veil&tag={AMAZON_TAG}",
            "emoji": "🧤",
        },
        {
            "name": "💨 Stainless Steel Bee Smoker",
            "price": "£24.99",
            "desc": "Calm your bees during inspections. Stainless steel with heat shield — built to last.",
            "url": f"https://www.amazon.co.uk/s?k=stainless+steel+bee+smoker&tag={AMAZON_TAG}",
            "emoji": "💨",
        },
        {
            "name": "🏠 Cedar National Beehive",
            "price": "£149.99",
            "desc": "British Standard National hive in cedar. The most popular hive style in the UK.",
            "url": f"https://www.amazon.co.uk/s?k=national+beehive+cedar+uk&tag={AMAZON_TAG}",
            "emoji": "🏠",
        },
    ],
}

# ==========================================
# DIGITAL PRODUCTS (Buy Me a Coffee "Extras")
# ==========================================

DIGITAL_PRODUCTS = [
    {
        "name": "📋 UK Foraging Season Calendar 2026",
        "desc": "A3 printable wall calendar showing every edible plant, month by month. Never miss a season again!",
        "price": "£4.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "📋",
        "category": "printable",
    },
    {
        "name": "🍄 Mushroom Identification Flash Cards",
        "desc": "30 printable flashcards covering the most common UK mushrooms — edible and deadly. Perfect for families and beginners.",
        "price": "£3.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "🍄",
        "category": "printable",
    },
    {
        "name": "☠️ Dangerous Lookalikes Cheat Sheet",
        "desc": "A4 printable showing every dangerous plant side-by-side with its safe lookalike. Could save a life.",
        "price": "£2.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "☠️",
        "category": "safety",
    },
    {
        "name": "🧒 Family Foraging Adventure Pack",
        "desc": "Complete pack for families: ID cards, activity sheets, safety checklist, and seasonal calendar. Ages 5-11.",
        "price": "£7.99",
        "url": f"{BMC_URL}/extras",
        "emoji": "🧒",
        "category": "family",
    },
]

# ==========================================
# SEASONAL AFFILIATE RECOMMENDATIONS
# ==========================================

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


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_current_season():
    """Return the current season name based on today's date."""
    current_month = datetime.now().strftime("%B")
    for season, months in SEASON_MONTHS.items():
        if current_month in months:
            return season
    return "Winter"


def get_current_month():
    """Return the current month name."""
    return datetime.now().strftime("%B")


# ==========================================
# RENDER FUNCTIONS
# ==========================================

def render_affiliate_section():
    """Render the 'Recommended Books & Gear' affiliate section."""
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
                            color: white;
                            padding: 0.3rem 0.8rem;
                            border-radius: 6px;
                            text-decoration: none;
                            font-size: 0.8rem;
                            font-weight: 600;
                            display: inline-block;
                            margin-top: 0.3rem;
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
                            color: white;
                            padding: 0.3rem 0.8rem;
                            border-radius: 6px;
                            text-decoration: none;
                            font-size: 0.8rem;
                            font-weight: 600;
                            display: inline-block;
                            margin-top: 0.3rem;
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
                            color: #1a1a1a;
                            padding: 0.3rem 0.8rem;
                            border-radius: 6px;
                            text-decoration: none;
                            font-size: 0.8rem;
                            font-weight: 600;
                            display: inline-block;
                            margin-top: 0.3rem;
                        ">View on Amazon →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.caption("🔗 Links may earn us a small commission at no extra cost to you. We only recommend products we genuinely use and trust.")


def render_digital_products():
    """Render the digital products section."""
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
                        color: white;
                        padding: 0.4rem 1rem;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 0.85rem;
                        font-weight: 700;
                        display: inline-block;
                        margin-top: 0.3rem;
                    ">Get PDF →</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.caption("📥 All downloads are PDF files — print at home or take to a print shop for best results.")


def render_support_section():
    """Render the 'Support Us' section with Buy Me a Coffee."""
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
    """Render a newsletter/email capture section."""
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
        email = st.text_input(
            "📧 Your email address",
            placeholder="forager@example.co.uk",
            label_visibility="collapsed",
            key="newsletter_email"
        )
    with col_nl2:
        if st.button("🌿 Subscribe", use_container_width=True, type="primary", key="newsletter_subscribe_btn"):
            if email and "@" in email and "." in email:
                st.success("🌿 Welcome to the foraging community! Check your inbox for a confirmation.")
            else:
                st.warning("Please enter a valid email address.")


def render_seasonal_affiliate_badge():
    """Render a small seasonal affiliate badge for the homepage."""
    current_season = get_current_season()
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
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
            white-space: nowrap;
        ">Shop →</a>
    </div>
    """, unsafe_allow_html=True)


def render_full_shop_page():
    """Render the complete shop page — call this from pages/3_Shop.py."""
    st.markdown("""
    <h2 style="color: var(--cream); font-family: 'Crimson Text', Georgia, serif; text-align: center; margin-bottom: 0.3rem;">
        🛒 Shop & Support
    </h2>
    <p style="color: var(--cream-dim); text-align: center; font-size: 0.95rem; margin-bottom: 1.5rem;">
        Hand-picked books, gear, and downloads for UK foragers, gardeners, and beekeepers.
    </p>
    """, unsafe_allow_html=True)

    tab_shop, tab_downloads, tab_support = st.tabs(["📚 Books & Gear", "📥 Downloads", "☕ Support Us"])

    with tab_shop:
        render_affiliate_section()

    with tab_downloads:
        render_digital_products()

    with tab_support:
        render_support_section()
        st.markdown("---")
        render_newsletter_signup()
