"""
Foraging Quest encounter generator.
Generates plant identification challenges filtered by scenario and season.
"""

import random
from data.plants_data import UK_PLANTS
from data.quest_config import (
    QUEST_SCENARIOS, QUEST_ADDITIONAL_PLANTS, FORAGING_ENCOUNTERS,
    QUEST_ACTIONS, QUEST_SHELTER, QUEST_CRAFTING,
    QUEST_WEATHER_FLAVOUR, QUEST_DAY_START, QUEST_LOCATION_DISCOVER
)

SEASON_MONTHS = {
    "Spring": ["March", "April", "May"],
    "Summer": ["June", "July", "August"],
    "Autumn": ["September", "October", "November"],
    "Winter": ["December", "January", "February"]
}

DANGER_DAMAGE = {"SAFE": 5, "CAUTION": 10, "POISONOUS": 20, "HIGH": 25, "EXTREME": 35, "DEADLY": 45}


def get_quest_config():
    """Return the full game configuration for the client."""
    return {
        "scenarios": QUEST_SCENARIOS,
        "actions": QUEST_ACTIONS,
        "shelter": QUEST_SHELTER,
        "crafting": QUEST_CRAFTING,
        "encounters": FORAGING_ENCOUNTERS,
        "weather_flavour": QUEST_WEATHER_FLAVOUR,
        "day_start": QUEST_DAY_START,
        "location_discover": QUEST_LOCATION_DISCOVER,
    }


def _plant_matches(plant, habitats, months):
    """Check if a plant matches the given habitats and months."""
    ph = plant.get("habitat", [])
    if isinstance(ph, str):
        ph = [ph]
    pm = plant.get("months", [])
    h_match = any(h in ph for h in habitats) if habitats else True
    s_match = any(m in months for m in pm) if months else True
    return h_match and s_match


def get_available_plants(scenario_id, season):
    """Get edible and poisonous plants available in this scenario and season."""
    scenario = QUEST_SCENARIOS.get(scenario_id)
    if not scenario:
        return list(UK_PLANTS.get("edible", [])), list(UK_PLANTS.get("poisonous", []))

    habitats = scenario.get("plant_habitats", [])
    months = SEASON_MONTHS.get(season, [])
    edible, poisonous = [], []

    for plant in UK_PLANTS.get("edible", []):
        if _plant_matches(plant, habitats, months):
            edible.append(plant)

    for plant in UK_PLANTS.get("poisonous", []):
        if _plant_matches(plant, habitats, months):
            poisonous.append(plant)

    for name, data in QUEST_ADDITIONAL_PLANTS.get("edible", {}).items():
        if _plant_matches(data, habitats, months):
            p = dict(data)
            p["name"] = name
            edible.append(p)

    for name, data in QUEST_ADDITIONAL_PLANTS.get("poisonous", {}).items():
        if _plant_matches(data, habitats, months):
            p = dict(data)
            p["name"] = name
            poisonous.append(p)

    # Fallback if filters too strict
    if not edible and not poisonous:
        edible = list(UK_PLANTS.get("edible", []))[:20]
        poisonous = list(UK_PLANTS.get("poisonous", []))[:10]

    return edible, poisonous


def generate_quest_encounter(scenario_id, season, seen_plants=None):
    """Generate a foraging encounter: narrative + plant ID question + consequences."""
    edible, poisonous = get_available_plants(scenario_id, season)

    if not edible and not poisonous:
        return {"error": "No plants available"}

    if seen_plants is None:
        seen_plants = []

    # 60% edible encounter, 40% poisonous for good tension
    want_edible = random.random() < 0.6

    if want_edible and edible:
        pool = edible
        target_type = "edible"
    elif not want_edible and poisonous:
        pool = poisonous
        target_type = "poisonous"
    elif edible:
        pool = edible
        target_type = "edible"
    else:
        pool = poisonous
        target_type = "poisonous"

    # Prefer unseen plants
    unseen = [p for p in pool if p.get("name") not in seen_plants]
    target = random.choice(unseen if unseen else pool)
    target_name = target.get("name", "Unknown")

    # Build option pool
    all_options = []
    for p in edible:
        all_options.append({
            "name": p.get("name", "?"), "edible": True,
            "icon": p.get("icon", "🌿"),
            "danger": p.get("foraging_quest", {}).get("danger", "SAFE") if p.get("foraging_quest") else "SAFE"
        })
    for p in poisonous:
        fq = p.get("foraging_quest", {})
        danger = fq.get("danger", "") if fq else ""
        if not danger:
            danger = p.get("danger_tips", {}).get("danger_zone", "POISONOUS")
        all_options.append({
            "name": p.get("name", "?"), "edible": False,
            "icon": p.get("icon", "☠️"),
            "danger": danger
        })

    # Pick wrong answers — prefer lookalikes, then random, ensuring at least 1 dangerous
    wrong = []
    for la in target.get("lookalikes", []):
        la_name = la.get("name", "") if isinstance(la, dict) else la
        match = [o for o in all_options if o["name"] == la_name and o["name"] != target_name]
        for m in match:
            if m not in wrong:
                wrong.append(m)

    remaining = [o for o in all_options if o["name"] != target_name and o not in wrong]
    random.shuffle(remaining)

    # Ensure at least 1 poisonous wrong answer for edible targets
    if target_type == "edible":
        poison_opts = [o for o in remaining if not o["edible"]]
        if poison_opts and len(wrong) < 3:
            wrong.append(poison_opts[0])
            remaining.remove(poison_opts[0])

    while len(wrong) < 3 and remaining:
        wrong.append(remaining.pop(0))

    # Generic fallbacks
    generics = [
        {"name": "Unknown Berry", "edible": False, "icon": "🫐", "danger": "CAUTION"},
        {"name": "Mystery Mushroom", "edible": False, "icon": "🍄", "danger": "CAUTION"},
        {"name": "Unidentified Herb", "edible": True, "icon": "🌿", "danger": "SAFE"},
    ]
    gi = 0
    while len(wrong) < 3 and gi < len(generics):
        if generics[gi]["name"] != target_name:
            wrong.append(generics[gi])
        gi += 1
    wrong = wrong[:3]

    correct_option = {
        "name": target_name,
        "edible": target_type == "edible",
        "icon": target.get("icon", "🌿"),
        "danger": target.get("foraging_quest", {}).get("danger",
                target.get("danger_tips", {}).get("danger_zone", "SAFE" if target_type == "edible" else "POISONOUS"))
    }

    options = [correct_option] + wrong
    random.shuffle(options)

    # Narrative text
    templates = FORAGING_ENCOUNTERS.get(scenario_id, FORAGING_ENCOUNTERS.get("wild_forest", []))
    encounter_text = random.choice(templates) if templates else "You spot something growing nearby."
    encounter_text = encounter_text.replace("{habitat}", random.choice(
        ["forest floor", "stream bank", "clearing", "hedgerow", "undergrowth", "rocky crevice", "mossy bank"]))

    # Consequences
    fq = target.get("foraging_quest", {})
    danger_level = fq.get("danger", "") if fq else ""
    if not danger_level:
        danger_level = target.get("danger_tips", {}).get("danger_zone", "SAFE" if target_type == "edible" else "POISONOUS")

    correct_fx = {}
    if target_type == "edible":
        for key, field in [("food", "food_value"), ("health", "health_value"), ("water", "water_value"),
                           ("warmth", "warmth_value"), ("morale", "morale_value")]:
            val = fq.get(field, 0)
            if val > 0:
                correct_fx[key] = val

    wrong_fx = {"health": -(DANGER_DAMAGE.get(danger_level, 15) if target_type == "poisonous" else 8), "morale": -5}

    return {
        "encounter_text": encounter_text,
        "plant": {
            "name": target.get("name", "Unknown"),
            "latin_name": target.get("latin_name", ""),
            "icon": target.get("icon", "🌿"),
            "description": target.get("description", ""),
            "category": target.get("category", ""),
            "edible": target_type == "edible",
            "danger_level": danger_level,
            "parts": target.get("parts", []),
            "taste": target.get("taste", ""),
            "nutrition": target.get("nutrition", ""),
        },
        "question": "Can you identify this plant?",
        "options": options,
        "correct_answer": target_name,
        "consequences": {"correct": correct_fx, "wrong": wrong_fx},
        "scenario": scenario_id,
        "season": season,
    }
