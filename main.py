# ═══════════════════════════════════════════════════════════════
# ROCEN HOMESTEADY — MAIN SERVER
# ═══════════════════════════════════════════════════════════════
#
# TABLE OF CONTENTS
# ─────────────────
# 1.  Imports
# 2.  App Setup & Config (CHANGED: lifespan, rate limiter)
# 3.  Helper Functions
# 4.  Page Routes (HTML)
#     4a. Home
#     4b. Learn & Modules
#     4c. Games Listing
#     4d. Individual Game Pages
#     4e. Shop
#     4f. Auth Pages
# 5.  API Routes — Season & Plants
# 6.  API Routes — Games
#     6a. General Config
#     6b. Foraging Quest
#     6c. Survival School
#     6d. Daily Quiz
#     6e. Eco-Village
#     6f. Apiary
#     6g. Kitchen
#     6h. Farm Tycoon
#     6i. Market Garden
# 7.  API Routes — Lessons
# 8.  API Routes — Stats & Health
# 9.  API Routes — Shop
# 10. API Routes — Authentication (CHANGED: async, rate limited, auto-login on register)
# 11. API Routes — Game Progress (CHANGED: async, merge endpoint)
# ═══════════════════════════════════════════════════════════════


# ── 1. Imports ──

import json
from contextlib import asynccontextmanager
from datetime import datetime, date

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

# CHANGED: import async versions + pool setup
import db
from db import init_pool, close_pool, create_tables
from auth import sign_up, log_in, verify_access_token, get_current_user, create_access_token
from progress import save_progress, load_progress, merge_and_save

# CHANGED: rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from data.shop_data import (
    AFFILIATE_PRODUCTS, DIGITAL_PRODUCTS, SEASON_PRODUCTS,
    BMC_URL, SEASON_COLOURS,
)
from data.lessons_data import LESSON_CONTENT, MODULE_METADATA, PATH_INFO
from data.game_config import (
    SEASON_MONTHS, SEASON_ICONS, ACHIEVEMENTS,
    VILLAGE_ITEMS, VILLAGE_BUILDINGS, VILLAGE_PRODUCTION,
    FARM_ICONS, FARM_BUILDINGS, SEED_COST, BASE_PRICES,
    MG_CROPS, MG_COMPANIONS, MG_ANTAGONISTS, MG_MARKET_BASE,
    NECTAR_FLOW, HONEY_TYPES, APIARY_PRODUCTS, BEEKEEPING_SEASONS,
    WEATHER_CHANCES, TEMP_RANGE,
    KITCHEN_RECIPES, BASICS,
    SURVIVAL_DIFFICULTY, HABITAT_ICONS, ECO_BASICS,
    MASTERY_LEVELS, DIFFICULTY_MODES, STREAK_MILESTONES, WINTER_HEAT,
    WRONG_CONSEQUENCES, CORRECT_BENEFITS, EMERGENCY_SCENARIOS,
    APIARY_PROCESSING, APIARY_THREATS,
    SMOKER_CONFIG, HIVE_TEMPERAMENTS, QUEEN_MARK_COLOURS,
    LEVEL_UNLOCKS, APIARY_EDUCATION_FACTS, MENTOR_TIPS,
    FARM_CROP_UNLOCKS, FARM_CROP_SEASONS, FARM_CROP_DAYS,
    FARM_SEASONAL_PRICES, FARM_ROCK_CLEAR_COST, FARM_FISHING,
    FARM_CONTRACTS, FARM_WEATHER_EVENTS, FARM_DIVERSITY_BONUS,
    MG_STARTING_CROPS, MG_CROP_UNLOCKS, MG_PEST_EVENTS, MG_SEASONS,
)

from data.plants_data import UK_PLANTS, PLANT_COUNTS
from data.question_generator import (
    generate_foraging_question, generate_foraging_bonus,
    get_survival_case, get_survival_case_count,
    generate_quiz_question, generate_daily_quiz_questions,
    get_emergency_scenario,
)
from data.quest_config import (
    QUEST_SCENARIOS, QUEST_ACTIONS, QUEST_SHELTER, QUEST_CRAFTING,
    FORAGING_ENCOUNTERS, QUEST_ADDITIONAL_PLANTS,
    QUEST_WEATHER_FLAVOUR, QUEST_DAY_START, QUEST_LOCATION_DISCOVER,
)
from data.quest_generator import get_quest_config, generate_quest_encounter, get_available_plants


# ── 2. App Setup & Config ──

# CHANGED: Lifespan handler for database pool
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create db pool and tables. Shutdown: close pool."""
    pool_ready = await init_pool()
    if pool_ready:
        await create_tables()
        print("✓ Database ready")
    else:
        print("⚠ Database unavailable — auth and progress features disabled")
    yield
    await close_pool()
    print("✓ Database pool closed")


# CHANGED: Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Rocen Homesteady API",
    description="The UK's Ultimate Foraging Companion — API",
    version="0.3.0",
    lifespan=lifespan,
)

# Rate limiting setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

env = Environment(loader=FileSystemLoader("templates"))
env.filters['tojson'] = lambda value: Markup(json.dumps(value, ensure_ascii=False))


# ═══════════════════════════════════════════════════════════════
# 3. HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_current_season():
    """Determine the current season from today's month."""
    current_month = datetime.now().strftime("%B")
    for season, months in SEASON_MONTHS.items():
        if current_month in months:
            return season
    return "Winter"


def get_season_colour(season):
    """Return a theme colour for a given season."""
    colours = {
        "Spring": "#66BB6A",
        "Summer": "#FFA726",
        "Autumn": "#EF6C00",
        "Winter": "#42A5F5",
    }
    return colours.get(season, "#4CAF50")


def get_default_season_context():
    """Return a dict of common season-related context for templates."""
    current_season = get_current_season()
    current_month = datetime.now().strftime("%B")
    return {
        "current_season": current_season,
        "current_month": current_month,
        "season_icon": SEASON_ICONS.get(current_season, "🌸"),
        "season_colour": get_season_colour(current_season),
    }


def get_plants_in_season(month=None):
    """Return edible plants available in a given month."""
    if month is None:
        month = datetime.now().strftime("%B")
    return [p for p in UK_PLANTS["edible"] if month in p.get("months", [])]


def get_dangerous_plants(month=None):
    """Return poisonous plants dangerous in a given month."""
    if month is None:
        month = datetime.now().strftime("%B")
    return [p for p in UK_PLANTS["poisonous"] if month in p.get("months", [])]


# ═══════════════════════════════════════════════════════════════
# 4. PAGE ROUTES (HTML)
# ═══════════════════════════════════════════════════════════════

# ── 4a. Home ──

@app.get("/")
async def home():
    ctx = get_default_season_context()
    plants_in_season = get_plants_in_season()
    dangerous_now = get_dangerous_plants()

    plants_in_season.sort(key=lambda p: p.get("difficulty", 1))
    dangerous_now.sort(
        key=lambda p: 0 if p.get("danger_tips", {}).get("danger_zone", "") in ["DEADLY", "EXTREME"] else 1
    )

    featured_edible = plants_in_season[:3]
    featured_dangerous = dangerous_now[:2]

    safe_match = None
    if featured_dangerous:
        for p in UK_PLANTS["edible"]:
            for la in p.get("lookalikes", []):
                if la.get("name") == featured_dangerous[0]["name"]:
                    safe_match = p
                    break
            if safe_match:
                break

    html = env.get_template("home.html").render(
        season=ctx["current_season"],
        season_icon=ctx["season_icon"],
        season_colour=ctx["season_colour"],
        current_month=ctx["current_month"],
        total_edible=PLANT_COUNTS["total_edible"],
        total_poisonous=PLANT_COUNTS["total_poisonous"],
        total_plants=PLANT_COUNTS["total"],
        total_games=8,
        total_achievements=len(ACHIEVEMENTS),
        featured_edible=featured_edible,
        featured_dangerous=featured_dangerous,
        safe_match=safe_match,
    )
    return HTMLResponse(content=html)


# ── 4b. Learn & Modules ──

@app.get("/learn")
async def learn_page():
    ctx = get_default_season_context()
    html = env.get_template("learn.html").render(
        season=ctx["current_season"],
        season_icon=ctx["season_icon"],
        current_month=ctx["current_month"],
        total_edible=PLANT_COUNTS["total_edible"],
        total_poisonous=PLANT_COUNTS["total_poisonous"],
    )
    return HTMLResponse(content=html)


@app.get("/learn/modules")
async def learn_modules_page():
    ctx = get_default_season_context()

    modules_by_path = {}
    for title, data in LESSON_CONTENT.items():
        meta = MODULE_METADATA.get(title, {"path": "Foraging", "level": "Beginner", "icon": "📖"})
        path = meta["path"]
        path_slug = PATH_INFO.get(path, PATH_INFO["Foraging"])["slug"]

        if path not in modules_by_path:
            modules_by_path[path] = []

        modules_by_path[path].append({
            "title": title,
            "curriculum": data.get("curriculum", []),
            "ks2_age": data.get("ks2_age", ""),
            "level": meta["level"],
            "icon": meta["icon"],
            "path": path,
            "path_slug": path_slug,
            "step_count": len(data.get("steps", [])),
        })

    for path_name in PATH_INFO:
        if path_name not in modules_by_path:
            modules_by_path[path_name] = []

    html = env.get_template("modules.html").render(
        season=ctx["current_season"],
        season_icon=ctx["season_icon"],
        current_month=ctx["current_month"],
        modules_by_path=modules_by_path,
        path_info=PATH_INFO,
        total_modules=len(LESSON_CONTENT),
    )
    return HTMLResponse(content=html)

# ── 4c. Games Listing ──

@app.get("/games")
async def games_page():
    ctx = get_default_season_context()
    edible_count = len(UK_PLANTS.get("edible", []))

    html = env.get_template("games.html").render(
        default_season=json.dumps(ctx["current_season"]),
        season_icons=json.dumps(SEASON_ICONS),
        season_months=json.dumps(SEASON_MONTHS),
        achievements=json.dumps(ACHIEVEMENTS),
        survival_difficulty=json.dumps(SURVIVAL_DIFFICULTY),
        survival_case_count=json.dumps(get_survival_case_count()),
        edible_count=json.dumps(edible_count),
    )
    return HTMLResponse(content=html)


# ── 4d. Individual Game Pages ──

@app.get("/games/foraging-quest")
async def foraging_quest_page():
    ctx = get_default_season_context()
    fq_config = json.dumps({
        "defaultSeason": ctx["current_season"],
        "seasonIcons": SEASON_ICONS,
        "seasonMonths": SEASON_MONTHS,
    })
    html = env.get_template("foraging-quest.html").render(fq_config=fq_config)
    return HTMLResponse(content=html)


@app.get("/games/survival-school")
async def survival_school_page():
    ctx = get_default_season_context()
    html = env.get_template("survival-school.html").render(
        survival_difficulty=SURVIVAL_DIFFICULTY,
        survival_case_count=get_survival_case_count(),
        default_season=ctx["current_season"],
        season_icons=SEASON_ICONS,
        edible_count=len(UK_PLANTS.get("edible", [])),
        achievements=ACHIEVEMENTS,
        difficulty_modes=DIFFICULTY_MODES,
        mastery_levels=MASTERY_LEVELS,
        streak_milestones=STREAK_MILESTONES,
        emergency_scenarios=[
            {"id": s["id"], "scenario": s["scenario"], "setting": s["setting"], "follow_up_types": s["follow_up_types"]}
            for s in EMERGENCY_SCENARIOS
        ],
    )
    return HTMLResponse(content=html)


@app.get("/games/daily-quiz")
async def daily_quiz_page():
    total_plants = len(UK_PLANTS.get("edible", [])) + len(UK_PLANTS.get("poisonous", []))
    html = env.get_template("daily-quiz.html").render(
        edible_count=json.dumps(len(UK_PLANTS.get("edible", []))),
        total_plants=json.dumps(total_plants),
        achievements=json.dumps(ACHIEVEMENTS),
    )
    return HTMLResponse(content=html)


@app.get("/games/homestead")
async def homestead_page():
    ctx = get_default_season_context()
    html = env.get_template("homestead.html").render(
        season_icons=json.dumps(SEASON_ICONS),
        season_months=json.dumps(SEASON_MONTHS),
        default_season=json.dumps(ctx["current_season"]),
        active_game="eco-village",
    )
    return HTMLResponse(content=html)


@app.get("/games/eco-village")
async def eco_village_page():
    ctx = get_default_season_context()
    html = env.get_template("homestead.html").render(
        season_icons=json.dumps(SEASON_ICONS),
        season_months=json.dumps(SEASON_MONTHS),
        default_season=json.dumps(ctx["current_season"]),
        active_game="eco-village",
    )
    return HTMLResponse(content=html)


@app.get("/games/wild-kitchen")
async def wild_kitchen_page():
    ctx = get_default_season_context()
    html = env.get_template("homestead.html").render(
        season_icons=json.dumps(SEASON_ICONS),
        season_months=json.dumps(SEASON_MONTHS),
        default_season=json.dumps(ctx["current_season"]),
        active_game="wild-kitchen",
    )
    return HTMLResponse(content=html)


@app.get("/games/farm")
async def farm_page():
    html = env.get_template("farm.html").render(active_game="farm-tycoon")
    return HTMLResponse(content=html)


@app.get("/games/farm-tycoon")
async def farm_tycoon_page():
    html = env.get_template("farm.html").render(active_game="farm-tycoon")
    return HTMLResponse(content=html)


@app.get("/games/market-garden")
async def market_garden_page():
    html = env.get_template("farm.html").render(active_game="market-garden")
    return HTMLResponse(content=html)


@app.get("/games/apiary")
async def apiary_page():
    html = env.get_template("apiary.html").render(
        season_icons=json.dumps(SEASON_ICONS),
    )
    return HTMLResponse(content=html)


# ── 4e. Shop ──

@app.get("/shop")
async def shop_page():
    ctx = get_default_season_context()
    season_product = SEASON_PRODUCTS.get(ctx["current_season"], SEASON_PRODUCTS["Winter"])

    html = env.get_template("shop.html").render(
        season=ctx["current_season"],
        season_icon=ctx["season_icon"],
        season_colour=ctx["season_colour"],
        season_product=season_product,
        books=AFFILIATE_PRODUCTS["books"],
        gear=AFFILIATE_PRODUCTS["gear"],
        beekeeping=AFFILIATE_PRODUCTS["beekeeping"],
        digital_products=DIGITAL_PRODUCTS,
        bmc_url=BMC_URL,
    )
    return HTMLResponse(content=html)


# ── 4f. Auth Pages ──

@app.get("/login")
async def login_page(request: Request):
    """Login/register page. Redirect to home if already logged in."""
    user = await get_current_user(request)
    if user:
        return RedirectResponse(url="/", status_code=302)
    html = env.get_template("login.html").render()
    return HTMLResponse(content=html)


# ═══════════════════════════════════════════════════════════════
# 5. API ROUTES — SEASON & PLANTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/season")
async def api_season():
    ctx = get_default_season_context()
    return {
        "month": ctx["current_month"],
        "season": ctx["current_season"],
        "icon": ctx["season_icon"],
        "colour": ctx["season_colour"],
    }


@app.get("/api/plants/edible")
async def api_edible_plants(category: str = None, season: str = None):
    plants = UK_PLANTS["edible"]
    if category:
        plants = [p for p in plants if p.get("category", "").lower() == category.lower()]
    if season:
        months = SEASON_MONTHS.get(season, [])
        plants = [p for p in plants if any(m in p.get("months", []) for m in months)]
    return {"count": len(plants), "plants": plants}


@app.get("/api/plants/poisonous")
async def api_poisonous_plants(season: str = None):
    plants = UK_PLANTS["poisonous"]
    if season:
        months = SEASON_MONTHS.get(season, [])
        plants = [p for p in plants if any(m in p.get("months", []) for m in months)]
    return {"count": len(plants), "plants": plants}


@app.get("/api/plants/in-season")
async def api_plants_in_season(month: str = None):
    if month is None:
        month = datetime.now().strftime("%B")
    edible = [p for p in UK_PLANTS["edible"] if month in p.get("months", [])]
    poisonous = [p for p in UK_PLANTS["poisonous"] if month in p.get("months", [])]
    return {
        "month": month,
        "edible_count": len(edible),
        "poisonous_count": len(poisonous),
        "edible": edible,
        "poisonous": poisonous,
    }


# ═══════════════════════════════════════════════════════════════
# 6. API ROUTES — GAMES
# ═══════════════════════════════════════════════════════════════

# ── 6a. General Game Config ──

@app.get("/api/games/config")
async def api_game_config():
    return {
        "achievements": ACHIEVEMENTS,
        "habitat_icons": HABITAT_ICONS,
        "survival_difficulty": SURVIVAL_DIFFICULTY,
        "season_icons": SEASON_ICONS,
        "season_months": SEASON_MONTHS,
    }


# ── 6b. Foraging Quest ──

@app.get("/api/games/foraging-quest/config")
async def foraging_quest_config():
    return get_quest_config()


@app.get("/api/games/foraging-quest/question")
async def foraging_quest_question(season: str = "Summer", preferred_type: str = None, review: str = None):
    review_names = [n.strip() for n in review.split(",") if n.strip()] if review else None
    return generate_foraging_question(season, preferred_type=preferred_type, review_names=review_names)


@app.get("/api/games/foraging-quest/bonus")
async def foraging_quest_bonus(season: str = "Summer"):
    return generate_foraging_bonus(season)


@app.get("/api/games/foraging-quest/encounter")
async def foraging_quest_encounter(scenario: str = "wild_forest", season: str = "Autumn", review: str = ""):
    seen = [n.strip() for n in review.split(",") if n.strip()] if review else None
    return generate_quest_encounter(scenario, season, seen_plants=seen)


@app.get("/api/games/foraging-quest/plants")
async def foraging_quest_plants(scenario: str = "wild_forest", season: str = "Autumn"):
    edible, poisonous = get_available_plants(scenario, season)
    return {
        "scenario": scenario,
        "season": season,
        "edible_count": len(edible),
        "poisonous_count": len(poisonous),
        "edible": [p.get("name", "?") for p in edible],
        "poisonous": [p.get("name", "?") for p in poisonous],
    }


# ── 6c. Survival School ──

@app.get("/api/games/survival-school/case")
async def survival_school_case(level: int = 1, exclude: str = "", review: str = ""):
    exclude_names = [n.strip() for n in exclude.split(",") if n.strip()] if exclude else []
    review_names = [n.strip() for n in review.split(",") if n.strip()] if review else None
    return get_survival_case(level, exclude_names, review_names=review_names)


@app.get("/api/games/survival-school/case-count")
async def survival_case_count():
    return get_survival_case_count()


@app.get("/api/games/survival-school/scenario")
async def survival_school_scenario(season: str = None):
    return get_emergency_scenario(season)


@app.get("/api/games/survival-school/plant-of-the-day")
async def survival_school_plant_of_the_day():
    from data.question_generator import generate_plant_of_the_day
    return generate_plant_of_the_day()


@app.get("/api/games/survival-school/weekly-challenge")
async def survival_school_weekly_challenge():
    from data.question_generator import generate_weekly_challenge
    return generate_weekly_challenge()


# ── 6d. Daily Quiz ──

@app.get("/api/games/daily-quiz/question")
async def daily_quiz_question(category: str = "All", num_options: int = 3, seed: str = None, review: str = ""):
    import random as random_mod
    import hashlib

    rng = None
    if seed:
        seed_int = int(hashlib.md5(seed.encode()).hexdigest(), 16) % (2**32)
        rng = random_mod.Random(seed_int)

    review_names = [n.strip() for n in review.split(",") if n.strip()] if review else None
    return generate_quiz_question(category, num_options, rng=rng, review=review_names)


@app.get("/api/games/daily-quiz/daily")
async def daily_quiz_daily():
    from data.question_generator import generate_daily_quiz_questions
    from datetime import date as date_mod
    return {
        "date": date_mod.today().isoformat(),
        "questions": generate_daily_quiz_questions(num_questions=10, num_options=4),
    }


# ── 6e. Eco-Village ──

@app.get("/api/games/eco-village")
async def api_eco_village():
    return {
        "items": VILLAGE_ITEMS,
        "buildings": VILLAGE_BUILDINGS,
        "production": VILLAGE_PRODUCTION,
    }


@app.get("/api/games/eco-village/config")
async def eco_village_config():
    return {
        "items": VILLAGE_ITEMS,
        "buildings": VILLAGE_BUILDINGS,
        "production": VILLAGE_PRODUCTION,
        "basics": ECO_BASICS,
        "season_icons": SEASON_ICONS,
        "season_months": SEASON_MONTHS,
        "winter_heat": WINTER_HEAT,
    }


# ── 6f. Apiary ──

@app.get("/api/games/apiary")
async def api_apiary():
    return {
        "nectar_flow": NECTAR_FLOW,
        "honey_types": HONEY_TYPES,
        "products": APIARY_PRODUCTS,
        "seasons": BEEKEEPING_SEASONS,
        "weather": WEATHER_CHANCES,
        "temp_range": TEMP_RANGE,
    }


@app.get("/api/games/apiary/config")
async def apiary_config():
    return {
        "nectar_flow": NECTAR_FLOW,
        "honey_types": HONEY_TYPES,
        "apiary_products": APIARY_PRODUCTS,
        "apiary_processing": APIARY_PROCESSING,
        "apiary_threats": APIARY_THREATS,
        "beekeeping_seasons": BEEKEEPING_SEASONS,
        "weather_chances": WEATHER_CHANCES,
        "temp_range": TEMP_RANGE,
        "season_icons": SEASON_ICONS,
        "smoker_config": SMOKER_CONFIG,
        "hive_temperaments": HIVE_TEMPERAMENTS,
        "queen_mark_colours": QUEEN_MARK_COLOURS,
        "level_unlocks": LEVEL_UNLOCKS,
        "education_facts": APIARY_EDUCATION_FACTS,
        "mentor_tips": MENTOR_TIPS,
        "wasp_threat": APIARY_THREATS["wasp_attack"],
    }


# ── 6g. Kitchen ──

@app.get("/api/games/kitchen")
async def api_kitchen():
    return {
        "basics": BASICS,
        "recipes": KITCHEN_RECIPES,
    }


@app.get("/api/games/kitchen/config")
async def kitchen_config():
    return {
        "recipes": KITCHEN_RECIPES,
        "basics": BASICS,
    }


# ── 6h. Farm Tycoon ──

@app.get("/api/games/farm-tycoon")
async def farm_tycoon_config():
    tile_styles = {}
    tile_meta = {
        0: {"label": "Empty", "bg": "#1a2e1a", "border": "#3d5a3d", "text": "#a0a0a0"},
        1: {"label": "Stream", "bg": "#0a1a2e", "border": "#2196F3", "text": "#90CAF9"},
        2: {"label": "Seed", "bg": "#1a2e1a", "border": "#4CAF50", "text": "#81C784"},
        3: {"label": "Growing", "bg": "#1a2e1a", "border": "#66BB6A", "text": "#A5D6A7"},
        4: {"label": "Ready!", "bg": "#2a2a00", "border": "#FFC107", "text": "#FFD54F"},
        5: {"label": "Rock", "bg": "#2a2a2a", "border": "#757575", "text": "#9E9E9E"},
        7: {"label": "Weed", "bg": "#2a1a0a", "border": "#8D6E63", "text": "#BCAAA4"},
        8: {"label": "Barn", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        9: {"label": "Beehive", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        10: {"label": "Scarecrow", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        11: {"label": "Sprinkler", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        12: {"label": "Chicken", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        13: {"label": "Cow", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        14: {"label": "Goat", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        15: {"label": "Cold Frame", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
        16: {"label": "Manor", "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"},
    }
    for tid, icon in FARM_ICONS.items():
        if tid in tile_meta:
            tile_styles[str(tid)] = {"icon": icon, **tile_meta[tid]}
        else:
            tile_styles[str(tid)] = {"icon": icon, "label": icon, "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"}
    for bname, bdata in FARM_BUILDINGS.items():
        bid = str(bdata["id"])
        if bid not in tile_styles:
            tile_styles[bid] = {"icon": bdata.get("icon", "🏠"), "label": bname, "bg": "#1a2e1a", "border": "#4CAF50", "text": "var(--cream)"}

    return {
        "buildings": FARM_BUILDINGS,
        "seed_cost": SEED_COST,
        "base_prices": BASE_PRICES,
        "tile_styles": tile_styles,
        "achievements": {k: v for k, v in ACHIEVEMENTS.items() if k.startswith("farm_")},
        "crop_unlocks": FARM_CROP_UNLOCKS,
        "crop_seasons": FARM_CROP_SEASONS,
        "crop_days": FARM_CROP_DAYS,
        "seasonal_prices": FARM_SEASONAL_PRICES,
        "rock_clear_cost": FARM_ROCK_CLEAR_COST,
        "fishing": FARM_FISHING,
        "contracts": FARM_CONTRACTS,
        "weather_events": FARM_WEATHER_EVENTS,
        "diversity_bonus": FARM_DIVERSITY_BONUS,
    }


# ── 6i. Market Garden ──

@app.get("/api/games/market-garden")
async def market_garden_config():
    companions = {}
    for pair, data in MG_COMPANIONS.items():
        key = ",".join(sorted(pair))
        companions[key] = data
    antagonists = {}
    for pair, desc in MG_ANTAGONISTS.items():
        key = ",".join(sorted(pair))
        antagonists[key] = desc

    return {
        "crops": MG_CROPS,
        "companions": companions,
        "antagonists": antagonists,
        "seasons": MG_SEASONS,
        "market_base": MG_MARKET_BASE,
        "achievements": {k: v for k, v in ACHIEVEMENTS.items() if k.startswith("mg_")},
        "starting_crops": MG_STARTING_CROPS,
        "crop_unlocks": MG_CROP_UNLOCKS,
        "pest_events": MG_PEST_EVENTS,
    }


# ═══════════════════════════════════════════════════════════════
# 7. API ROUTES — LESSONS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/lessons")
async def api_lessons():
    modules = []
    for title, data in LESSON_CONTENT.items():
        meta = MODULE_METADATA.get(title, {"path": "Foraging", "level": "Beginner", "icon": "📖"})
        modules.append({
            "title": title,
            "curriculum": data.get("curriculum", []),
            "ks2_age": data.get("ks2_age", ""),
            "level": meta["level"],
            "icon": meta["icon"],
            "path": meta["path"],
            "step_count": len(data.get("steps", [])),
        })
    return {"count": len(modules), "modules": modules}


@app.get("/api/lessons/{lesson_title}")
async def api_lesson_detail(lesson_title: str):
    if lesson_title not in LESSON_CONTENT:
        return {"error": "Lesson not found"}

    data = LESSON_CONTENT[lesson_title]
    meta = MODULE_METADATA.get(lesson_title, {"path": "Foraging", "level": "Beginner", "icon": "📖"})

    steps = []
    for i, step in enumerate(data.get("steps", [])):
        step_data = {"index": i, "type": step["type"]}
        if step["type"] == "text":
            step_data["content"] = step["content"]
        elif step["type"] == "quiz":
            step_data["question"] = step["question"]
            step_data["options"] = step["options"]
        elif step["type"] == "plant_card":
            step_data["plant_name"] = step["plant_name"]
        elif step["type"] == "final_quiz":
            step_data["question"] = step["question"]
            step_data["options"] = step["options"]
            step_data["reward"] = step.get("reward", 10)
        steps.append(step_data)

    return {
        "title": lesson_title,
        "curriculum": data.get("curriculum", []),
        "ks2_age": data.get("ks2_age", ""),
        "level": meta["level"],
        "icon": meta["icon"],
        "path": meta["path"],
        "total_steps": len(steps),
        "steps": steps,
    }


@app.post("/api/lessons/check-answer")
async def check_answer(payload: dict):
    lesson_title = payload.get("lesson_title")
    step_index = payload.get("step_index")
    user_answer = payload.get("answer")

    if lesson_title not in LESSON_CONTENT:
        return {"error": "Lesson not found"}

    steps = LESSON_CONTENT[lesson_title].get("steps", [])
    if step_index >= len(steps):
        return {"error": "Step not found"}

    step = steps[step_index]
    if step["type"] not in ("quiz", "final_quiz"):
        return {"error": "Not a quiz step"}

    correct_answer = step.get("answer", "")
    is_correct = user_answer == correct_answer

    result = {
        "correct": is_correct,
        "correct_answer": correct_answer if not is_correct else None,
    }

    if step["type"] == "final_quiz" and is_correct:
        result["reward"] = step.get("reward", 10)

    return result


# ═══════════════════════════════════════════════════════════════
# 8. API ROUTES — STATS & HEALTH
# ═══════════════════════════════════════════════════════════════

@app.get("/api/stats")
async def api_stats():
    return {
        "total_edible_plants": PLANT_COUNTS.get("total_edible", 0),
        "total_poisonous_plants": PLANT_COUNTS.get("total_poisonous", 0),
        "total_plants": PLANT_COUNTS.get("total", 0),
        "total_games": 8,
        "total_achievements": len(ACHIEVEMENTS),
        "total_recipes": len(KITCHEN_RECIPES),
        "current_season": get_current_season(),
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "rocen-homesteady",
        "version": "0.3.0",
        "database": "connected" if db.pool else "unavailable",
    }


# ═══════════════════════════════════════════════════════════════
# 9. API ROUTES — SHOP
# ═══════════════════════════════════════════════════════════════

@app.get("/api/shop/products")
async def api_shop_products():
    return {
        "affiliate_products": AFFILIATE_PRODUCTS,
        "digital_products": DIGITAL_PRODUCTS,
        "seasonal_products": SEASON_PRODUCTS,
    }


@app.get("/api/shop/seasonal")
async def api_shop_seasonal():
    current_season = get_current_season()
    return {
        "season": current_season,
        "product": SEASON_PRODUCTS.get(current_season, SEASON_PRODUCTS["Winter"]),
        "colour": SEASON_COLOURS.get(current_season, "#4CAF50"),
    }


# ═══════════════════════════════════════════════════════════════
# 10. API ROUTES — AUTHENTICATION
# ═══════════════════════════════════════════════════════════════

@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def api_login(request: Request):
    """Authenticate user and set JWT cookie."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            content={"success": False, "error": "Invalid request."},
            status_code=400,
        )

    username = body.get("username", "").strip()
    password = body.get("password", "")

    success, result = await log_in(username, password)

    if success:
        response = JSONResponse(content={"success": True, "username": result["username"]})
        response.set_cookie(
            key="access_token",
            value=result["token"],
            httponly=True,
            max_age=60 * 60 * 24 * 7,
            samesite="lax",
            path="/",
        )
        return response
    else:
        return JSONResponse(
            content={"success": False, "error": result.get("error", "Login failed.")},
            status_code=401,
        )


@app.post("/api/auth/register")
@limiter.limit("3/minute")
async def api_register(request: Request):
    """Register a new user and auto-login."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            content={"success": False, "error": "Invalid request."},
            status_code=400,
        )

    username = body.get("username", "").strip()
    password = body.get("password", "")

    success, message = await sign_up(username, password)

    if success:
        # Auto-login after registration
        token = create_access_token(username)

        response = JSONResponse(content={"success": True, "username": username, "message": message})
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=60 * 60 * 24 * 7,
            samesite="lax",
            path="/",
        )
        return response
    else:
        return JSONResponse(
            content={"success": False, "error": message},
            status_code=400,
        )


@app.post("/api/auth/logout")
async def api_logout():
    """Clear JWT cookie to log out."""
    response = JSONResponse(content={"success": True})
    response.delete_cookie(key="access_token", path="/")
    return response


@app.get("/api/auth/me")
async def api_me(request: Request):
    """Check if the current user is authenticated."""
    user = await get_current_user(request)
    if user:
        return JSONResponse(content={"authenticated": True, "username": user["username"]})
    else:
        return JSONResponse(content={"authenticated": False})


# ═══════════════════════════════════════════════════════════════
# 11. API ROUTES — GAME PROGRESS
# ═══════════════════════════════════════════════════════════════

@app.post("/api/progress/save")
async def api_save_progress(request: Request):
    """Save game progress. Requires authentication."""
    user = await get_current_user(request)
    if not user:
        return JSONResponse(
            content={"success": False, "error": "Not authenticated."},
            status_code=401,
        )

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            content={"success": False, "error": "Invalid request."},
            status_code=400,
        )

    progress = body.get("progress", {})
    username = user["username"]

    success = await save_progress(username, progress)
    if success:
        return JSONResponse(content={"success": True, "saved_at": datetime.utcnow().isoformat()})
    else:
        return JSONResponse(
            content={"success": False, "error": "Failed to save progress."},
            status_code=500,
        )


@app.get("/api/progress/load")
async def api_load_progress(request: Request):
    """Load game progress. Requires authentication."""
    user = await get_current_user(request)
    if not user:
        return JSONResponse(
            content={"success": False, "error": "Not authenticated."},
            status_code=401,
        )

    username = user["username"]
    progress = await load_progress(username)

    if progress is not None:
        return JSONResponse(content={"success": True, "progress": progress})
    else:
        return JSONResponse(content={"success": True, "progress": {}})


@app.post("/api/progress/merge")
async def api_merge_progress(request: Request):
    """
    Merge guest progress (from localStorage) into the user's server progress.
    Requires authentication. Called once after login if guest data exists.
    """
    user = await get_current_user(request)
    if not user:
        return JSONResponse(
            content={"success": False, "error": "Not authenticated."},
            status_code=401,
        )

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            content={"success": False, "error": "Invalid request."},
            status_code=400,
        )

    guest_progress = body.get("guest_progress", {})
    if not guest_progress:
        return JSONResponse(content={"success": True, "merged": {}, "message": "No guest data to merge."})

    username = user["username"]
    merged = await merge_and_save(username, guest_progress)

    if merged is not None:
        return JSONResponse(content={"success": True, "merged": merged})
    else:
        return JSONResponse(
            content={"success": False, "error": "Failed to merge progress."},
            status_code=500,
        )


@app.post("/api/progress/reset")
async def api_reset_progress(request: Request):
    """Delete all saved progress. Requires authentication."""
    user = await get_current_user(request)
    if not user:
        return JSONResponse(
            content={"success": False, "error": "Not authenticated."},
            status_code=401,
        )

    from progress import delete_progress
    username = user["username"]
    success = await delete_progress(username)

    if success:
        return JSONResponse(content={"success": True})
    else:
        return JSONResponse(
            content={"success": False, "error": "Failed to reset progress."},
            status_code=500,
        )
