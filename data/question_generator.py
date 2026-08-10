"""Question generation for Foraging Quest, Survival School, and Daily Quiz games."""

import random
import hashlib
from datetime import date
from data.plants_data import UK_PLANTS
from data.game_config import WRONG_CONSEQUENCES, CORRECT_BENEFITS
from data.game_config import (
    ACHIEVEMENTS, HABITAT_ICONS, SEASON_ICONS,
    SEASON_MONTHS, SURVIVAL_DIFFICULTY
)


def safe_sample(population, k, rng=None):
    """Safely sample k items from population."""
    if not population or k <= 0:
        return []
    k = min(k, len(population))
    r = rng or random
    return r.sample(population, k)


# ─────────────────────────────────────────────
# FORAGING QUEST — Question Generation
# ─────────────────────────────────────────────

Q_TYPE_ICONS = {
    'habitat': '🌍', 'identification': '🔍', 'lookalike': '☠️',
    'parts': '🍃', 'season': '📅', 'warning': '⚠️'
}
Q_TYPE_NAMES = {
    'habitat': 'Habitat', 'identification': 'ID Check',
    'lookalike': 'Lookalike Danger', 'parts': 'Edible Parts',
    'season': 'Season', 'warning': 'True or False'
}
Q_TYPE_COLOURS = {
    'habitat': '#4CAF50', 'identification': '#2196F3',
    'lookalike': '#ff5252', 'parts': '#FFC107',
    'season': '#FF8F00', 'warning': '#9C27B0'
}


# Category emoji mapping for reveal cards
CATEGORY_EMOJIS = {
    'Tree': '🌳', 'Shrub': '🌿', 'Plant': '🌱', 'Fungi': '🍄',
    'Coastal': '🏖️', 'Seaweed': '🌊', 'Shellfish': '🐚',
    'Flower': '🌸', 'Berry': '🫐', 'Root': '🥕', 'Herb': '🌿',
    'Fruit': '🍎', 'Nut': '🌰', 'Leaf': '🍃',
}


def _plant_summary(plant, is_edible=True):
    """Extract just the fields the frontend needs for display."""
    danger_tips = plant.get('danger_tips', {})
    danger_level = ''
    if not is_edible:
        danger_level = danger_tips.get('danger_zone', 'POISONOUS')

    return {
        'name': plant.get('name', ''),
        'latin': plant.get('latin_name', ''),
        'emoji': CATEGORY_EMOJIS.get(plant.get('category', ''), '🌿'),
        'category': plant.get('category', ''),
        'description': plant.get('description', '')[:200],
        'id_keys': plant.get('id_keys', {}),
        'habitat': plant.get('habitat', ''),
        'seasons': plant.get('months', []),
        'months': plant.get('months', []),
        'parts': plant.get('parts', ''),
        'lookalikes': plant.get('lookalikes', []),
        'warnings': plant.get('warnings', ''),
        'difficulty': plant.get('difficulty', 1),
        'confusion_notes': plant.get('confusion_notes', ''),
        'edible': is_edible,
        'danger_level': danger_level,
    }



def _generate_clue(plant):
    """Generate a botanical clue from a plant's id_keys or description."""
    id_keys = plant.get('id_keys', {})
    if id_keys:
        features = random.sample(list(id_keys.items()), min(2, len(id_keys)))
        return "Botanical Clue: " + "; ".join([f"{k} is {v}" for k, v in features])
    desc = plant.get('description', '')
    if desc:
        return f"Clue: {desc[:100]}..."
    return "Study this plant carefully."


def generate_foraging_question(season: str, preferred_type: str = None, review_names: list = None, force_plant: dict = None) -> dict:
    """Generate a random foraging question for the given season."""
    if force_plant:
        plant = force_plant
    else:
        available = [p for p in UK_PLANTS["edible"]
                     if any(m in SEASON_MONTHS.get(season, []) for m in p.get("months", []))]
        if not available:
            available = UK_PLANTS["edible"]

        # Prioritise review plants if provided
        if review_names:
            review_plants = [p for p in available if p['name'] in review_names]
            if review_plants and random.random() < 0.7:
                plant = random.choice(review_plants)
            else:
                plant = random.choice(available)
        else:
            plant = random.choice(available)


    question_types = ['habitat', 'identification', 'lookalike', 'parts', 'season', 'warning']

    if not plant.get('lookalikes'):
        question_types = [t for t in question_types if t != 'lookalike']
    if not plant.get('parts'):
        question_types = [t for t in question_types if t != 'parts']
    if not plant.get('warnings'):
        question_types = [t for t in question_types if t != 'warning']
    if not question_types:
        question_types = ['habitat', 'identification']

        # Prioritise preferred type or review plants
    if preferred_type and preferred_type in question_types:
        # 60% chance of using preferred type
        if random.random() < 0.6:
            q_type = preferred_type
        else:
            q_type = random.choice(question_types)
    else:
        q_type = random.choice(question_types)

    all_names = [p['name'] for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']]

    if q_type == 'habitat':
        correct = plant.get('habitat', 'Various')
        wrong_habitats = ["Woodlands", "Meadows", "Coastal cliffs", "Riverbanks",
                          "Hedgerows", "Marshes", "Moors", "Gardens", "Wasteland"]
        wrong_options = [h for h in wrong_habitats if h != correct]
        options = [correct] + safe_sample(wrong_options, 3)
        random.shuffle(options)
        return {
            'type': 'habitat', 'type_icon': Q_TYPE_ICONS['habitat'],
            'type_name': Q_TYPE_NAMES['habitat'], 'type_color': Q_TYPE_COLOURS['habitat'],
            'question': f"Where would you most likely find {plant['name']}?",
            'options': options, 'correct': correct,
            'explanation': f"{plant['name']} typically grows in {correct}.",
            'points': 10, 'clue': _generate_clue(plant),
            'plant': _plant_summary(plant),
            'wrong_consequence': WRONG_CONSEQUENCES.get('habitat', 'Knowing where plants grow is essential for safe foraging.'),
            'correct_benefit': CORRECT_BENEFITS.get('habitat', 'Knowing where to find plants means efficient foraging.'),
        }


    elif q_type == 'identification':
        id_keys = plant.get('id_keys', {})
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
                'type': 'identification', 'type_icon': Q_TYPE_ICONS['identification'],
                'type_name': Q_TYPE_NAMES['identification'],
                'type_color': Q_TYPE_COLOURS['identification'],
                'question': f"What is the {feature_key} of {plant['name']}?",
                'options': options, 'correct': correct,
                'explanation': f"The {feature_key} of {plant['name']} is {feature_val}.",
                'points': 10, 'clue': _generate_clue(plant),
                'plant': _plant_summary(plant),
                'wrong_consequence': WRONG_CONSEQUENCES.get('identification', 'Knowing how to identify plants is essential for safe foraging.'),
                'correct_benefit': CORRECT_BENEFITS.get('identification', 'Being able to identify plants ensures safe and efficient foraging.'),
            }
        else:
            correct = plant.get('category', 'Plant')
            categories = ["Plant", "Tree", "Shrub", "Fungi", "Coastal", "Seaweed", "Shellfish"]
            wrong = [c for c in categories if c != correct]
            options = [correct] + safe_sample(wrong, 3)
            random.shuffle(options)
            return {
                'type': 'identification', 'type_icon': Q_TYPE_ICONS['identification'],
                'type_name': Q_TYPE_NAMES['identification'],
                'type_color': Q_TYPE_COLOURS['identification'],
                'question': f"What type of organism is {plant['name']}?",
                'options': options, 'correct': correct,
                'explanation': f"{plant['name']} is a {correct}.",
                'points': 10, 'clue': _generate_clue(plant),
                'plant': _plant_summary(plant),
                'wrong_consequence': WRONG_CONSEQUENCES.get('bonus', 'Bonus rounds test deeper knowledge.'),
                'correct_benefit': CORRECT_BENEFITS.get('bonus', 'Excellent recall under pressure!'),
            }

    elif q_type == 'lookalike':
        lookalikes = plant.get('lookalikes', [])
        dangerous = [la for la in lookalikes
                     if isinstance(la, dict) and la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']]
        if dangerous:
            chosen = random.choice(dangerous)
            correct = chosen['name']
            other_names = [n for n in all_names if n != plant['name'] and n != correct]
            wrong = safe_sample(other_names, 3)
            options = [correct] + wrong
            while len(options) < 4:
                options.append("None of these")
            random.shuffle(options)
            confusion = plant.get('confusion_notes', chosen.get('diff', 'Check carefully!'))
            return {
                'type': 'lookalike', 'type_icon': Q_TYPE_ICONS['lookalike'],
                'type_name': Q_TYPE_NAMES['lookalike'],
                'type_color': Q_TYPE_COLOURS['lookalike'],
                'question': f"Which is the DANGEROUS lookalike of {plant['name']}?",
                'options': options, 'correct': correct,
                'explanation': f"{chosen['name']} is dangerous ({chosen.get('danger', 'Unknown')}): {chosen.get('diff', confusion)}",
                'points': 15,
                'clue': "⚠️ This plant has a DANGEROUS lookalike. Can you identify it?",
                'plant': _plant_summary(plant),
                'wrong_consequence': WRONG_CONSEQUENCES.get('lookalike', 'Be aware of dangerous lookalikes.'),
                'correct_benefit': CORRECT_BENEFITS.get('lookalike', 'Identifying lookalikes ensures safe foraging.'),
            }
        return generate_foraging_question(season)

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
            'type': 'parts', 'type_icon': Q_TYPE_ICONS['parts'],
            'type_name': Q_TYPE_NAMES['parts'], 'type_color': Q_TYPE_COLOURS['parts'],
            'question': f"Which part of {plant['name']} can you eat?",
            'options': options, 'correct': correct,
            'explanation': f"You can eat the {', '.join(parts_list)} of {plant['name']}.",
            'points': 10, 'clue': _generate_clue(plant),
            'plant': _plant_summary(plant),
            'wrong_consequence': WRONG_CONSEQUENCES.get('parts', 'Knowing which parts of plants are edible is essential for safe foraging.'),
            'correct_benefit': CORRECT_BENEFITS.get('parts', 'Being able to identify edible parts ensures safe and efficient foraging.'),
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
            'type': 'season', 'type_icon': Q_TYPE_ICONS['season'],
            'type_name': Q_TYPE_NAMES['season'], 'type_color': Q_TYPE_COLOURS['season'],
            'question': f"When is {plant['name']} best foraged?",
            'options': options, 'correct': correct,
            'explanation': f"{plant['name']} is best in {', '.join(correct_months)}.",
            'points': 10, 'clue': _generate_clue(plant),
            'plant': _plant_summary(plant),
            'wrong_consequence': WRONG_CONSEQUENCES.get('season', 'Knowing the right season for foraging is essential.'),
            'correct_benefit': CORRECT_BENEFITS.get('season', 'Foraging in the right season ensures the best yield.'),
        }

    elif q_type == 'warning':
        warning = plant.get('warnings', '')
        if warning:
            if random.random() < 0.5:
                return {
                    'type': 'warning', 'type_icon': Q_TYPE_ICONS['warning'],
                    'type_name': Q_TYPE_NAMES['warning'],
                    'type_color': Q_TYPE_COLOURS['warning'],
                    'question': f"True or False: {warning}",
                    'options': ["True", "False"], 'correct': "True",
                    'explanation': f"This is a real warning about {plant['name']}.",
                    'points': 10, 'clue': "⚠️ Safety knowledge check!",
                    'plant': _plant_summary(plant),
                    'wrong_consequence': WRONG_CONSEQUENCES.get('warning', 'Pay attention to warnings about plants.'),
                    'correct_benefit': CORRECT_BENEFITS.get('warning', 'Knowing warnings ensures safe foraging.'),
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
                        'type': 'warning', 'type_icon': Q_TYPE_ICONS['warning'],
                        'type_name': Q_TYPE_NAMES['warning'],
                        'type_color': Q_TYPE_COLOURS['warning'],
                        'question': f"True or False: {false_warning}",
                        'options': ["True", "False"], 'correct': "False",
                        'explanation': f"That's FALSE. The real warning is: {warning}",
                        'points': 15, 'clue': "⚠️ Safety knowledge check!",
                        'plant': _plant_summary(plant),
                        'wrong_consequence': WRONG_CONSEQUENCES.get('warning', 'Pay attention to warnings about plants.'),
                        'correct_benefit': CORRECT_BENEFITS.get('warning', 'Knowing warnings ensures safe foraging.'),
                    }
        return generate_foraging_question(season)

    return generate_foraging_question(season)


def generate_foraging_bonus(season: str) -> dict:
    """Generate a bonus question (double points, parts-based)."""
    available = [p for p in UK_PLANTS["edible"]
                 if any(m in SEASON_MONTHS.get(season, []) for m in p.get("months", []))]
    if not available:
        available = UK_PLANTS["edible"]

    # Prioritise review plants if provided
    if review_names is None:
        review_names = []
    if review_names:
        review_plants = [p for p in available if p['name'] in review_names]
        if review_plants and random.random() < 0.7:
            plant = random.choice(review_plants)
        else:
            plant = random.choice(available)
    else:
        plant = random.choice(available)

    raw_parts = plant.get('parts', 'Leaves')
    if isinstance(raw_parts, str):
        parts_list = [p.strip() for p in raw_parts.split(',')]
    else:
        parts_list = raw_parts
    if not parts_list:
        parts_list = ['Leaves']

    correct = parts_list[0]
    wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark"]
    wrong_options = [p for p in wrong_parts if p not in parts_list]
    options = parts_list[:1] + safe_sample(wrong_options, 2)
    random.shuffle(options)

    return {
        'type': 'bonus', 'type_icon': '⚡', 'type_name': 'Bonus Round',
        'type_color': '#FFD700',
        'question': f"Which part of {plant['name']} do we usually eat?",
        'options': options, 'correct': correct,
        'explanation': f"You can eat the {', '.join(parts_list)} of {plant['name']}.",
        'points': 20, 'clue': _generate_clue(plant),
        'plant': _plant_summary(plant)
    }


# ─────────────────────────────────────────────
# SURVIVAL SCHOOL — Case Generation
# ─────────────────────────────────────────────

_ALL_SURVIVAL_CASES = None


def _generate_all_survival_cases():
    """Generate all survival cases from plant data (called once and cached)."""
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
            rule = confusion or (f"Key difference: {diff}" if diff else f"Check carefully — {la['name']} is dangerous!")
            if confusion and diff:
                rule = f"{confusion} Key difference: {diff}"

            fact_parts = [f"**{edible['name']}** is edible."]
            if diff:
                fact_parts.append(f"The dangerous lookalike **{la['name']}** differs: {diff}")
            if confusion:
                fact_parts.append(f"Key ID note: {confusion}")
            fact = " ".join(fact_parts)

            level = 2 if danger in ['DEADLY', 'EXTREME'] else 1

            cases.append({
                'safe_plant': edible['name'], 'safe_icon': '🌿',
                'danger_plant': la['name'], 'danger_icon': '☠️',
                'safe_habitat': edible.get('habitat', 'Various'),
                'clue': clue, 'rule': rule, 'fact': fact, 'level': level
            })

    # Supplement with confusion_notes matches
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
                    danger_zone = poison.get('danger_tips', {}).get('danger_zone', 'dangerous')
                    fact = f"**{edible['name']}** is safe, but **{poison['name']}** is {danger_zone}."
                    if diff:
                        fact += f" Difference: {diff}"
                    level = 2 if danger_zone in ['DEADLY', 'EXTREME'] else 1
                    key = (edible['name'], poison['name'])
                    if not any(c['safe_plant'] == key[0] and c['danger_plant'] == key[1] for c in cases):
                        cases.append({
                            'safe_plant': edible['name'], 'safe_icon': '🌿',
                            'danger_plant': poison['name'], 'danger_icon': '☠️',
                            'safe_habitat': edible.get('habitat', 'Various'),
                            'clue': clue, 'rule': rule, 'fact': fact, 'level': level
                        })
                    break

    # Hard cases from difficulty >= 3 edibles with deadly lookalikes
    hard_edibles = [p for p in UK_PLANTS['edible'] if p.get('difficulty', 1) >= 3]
    for edible in hard_edibles:
        for la in edible.get('lookalikes', []):
            if not isinstance(la, dict):
                continue
            if la.get('danger', '') in ['DEADLY', 'EXTREME']:
                key = (edible['name'], la['name'])
                existing = [c for c in cases if c['safe_plant'] == key[0] and c['danger_plant'] == key[1]]
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
                    'safe_plant': edible['name'], 'safe_icon': '🌿',
                    'danger_plant': la['name'], 'danger_icon': '☠️',
                    'safe_habitat': edible.get('habitat', 'Various'),
                    'clue': clue, 'rule': rule, 'fact': fact, 'level': 3
                })

    # Deduplicate
    seen = set()
    unique = []
    for c in cases:
        key = (c['safe_plant'], c['danger_plant'])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    if not unique:
        unique.append({
            'safe_plant': 'Nettle', 'safe_icon': '🌿',
            'danger_plant': 'Deadly Nightshade', 'danger_icon': '☠️',
            'safe_habitat': 'Hedgerows and wasteland',
            'clue': 'You notice: a tall plant with jagged leaves and stinging hairs.',
            'rule': 'Always check for stinging hairs — Nettle has them, Deadly Nightshade does not.',
            'fact': '**Nettle** is edible when cooked. **Deadly Nightshade** is extremely poisonous.',
            'level': 1
        })

    return unique


def get_survival_cases():
    """Get all cached survival cases, generating if needed."""
    global _ALL_SURVIVAL_CASES
    if _ALL_SURVIVAL_CASES is None:
        _ALL_SURVIVAL_CASES = _generate_all_survival_cases()
    return _ALL_SURVIVAL_CASES


def get_survival_case(level: int = 1, exclude_names: list = None, review_names: list = None) -> dict:
    """Get a random survival case for the given level, excluding recently seen plants."""
    all_cases = get_survival_cases()

    if level == 1:
        pool = [c for c in all_cases if c['level'] == 1]
    elif level == 2:
        pool = [c for c in all_cases if c['level'] <= 2]
    else:
        pool = all_cases

    if not pool:
        pool = all_cases

    # Exclude recently seen
    if exclude_names:
        unseen = [c for c in pool if c['safe_plant'] not in exclude_names[-10:]]
        if unseen:
            pool = unseen

    # Prioritise review plants (plants the user got wrong)
    if review_names:
        review_pool = [c for c in pool if c['safe_plant'] in review_names or c['danger_plant'] in review_names]
        if review_pool:
            # 70% chance of picking a review plant
            if random.random() < 0.7:
                pool = review_pool

    case = random.choice(pool)

    # Enrich with safe plant details for the "Learn more" section
    safe_plant_data = None
    for p in UK_PLANTS['edible']:
        if p['name'] == case['safe_plant']:
            safe_plant_data = p
            break

    result = dict(case)
    if safe_plant_data:
        result['safe_plant_details'] = {
            'lookalikes': safe_plant_data.get('lookalikes', []),
            'warnings': safe_plant_data.get('warnings', ''),
            'confusion_notes': safe_plant_data.get('confusion_notes', ''),
        }

    # ── Consequence text ──
    from data.game_config import WRONG_CONSEQUENCES, CORRECT_BENEFITS

    # Find danger plant data for wrong consequence
    danger_plant_data = None
    for p in UK_PLANTS['poisonous']:
        if p['name'] == case['danger_plant']:
            danger_plant_data = p
            break

    # Wrong answer consequence
    danger_zone = 'POISONOUS'
    symptoms = 'serious illness'
    if danger_plant_data:
        danger_tips = danger_plant_data.get('danger_tips', {})
        danger_zone = danger_tips.get('danger_zone', 'POISONOUS')
        symptoms = danger_tips.get('symptoms', 'serious illness')
        if not symptoms or symptoms == 'Unknown':
            symptoms = 'serious illness'

    consequence_templates = WRONG_CONSEQUENCES['survival']
    if danger_zone in ['DEADLY', 'EXTREME']:
        template = consequence_templates.get('DEADLY', consequence_templates['default'])
    elif danger_zone in ['POISONOUS', 'HIGH']:
        template = consequence_templates.get('POISONOUS', consequence_templates['default'])
    else:
        template = consequence_templates['default']

    result['wrong_consequence'] = template.format(
        danger_plant=case['danger_plant'],
        symptoms=symptoms
    )
    result['correct_benefit'] = CORRECT_BENEFITS['survival']

    # Case number is client-side tracking, not from server
    return result


def get_survival_case_count() -> dict:
    """Return count of cases by level."""
    all_cases = get_survival_cases()
    return {
        'total': len(all_cases),
        'level_1': len([c for c in all_cases if c['level'] == 1]),
        'level_2': len([c for c in all_cases if c['level'] == 2]),
        'level_3': len([c for c in all_cases if c['level'] == 3]),
    }


# ─────────────────────────────────────────────
# DAILY QUIZ — Question Generation
# ─────────────────────────────────────────────

QUIZ_TYPE_ICONS = {
    'id_check': '🔍', 'parts_check': '🍃', 'season_check': '📅',
    'lookalike_check': '☠️', 'warning_check': '⚠️'
}
QUIZ_TYPE_NAMES = {
    'id_check': 'Identification', 'parts_check': 'Edible Parts',
    'season_check': 'Season', 'lookalike_check': 'Dangerous Lookalike',
    'warning_check': 'Safety Check'
}
QUIZ_TYPE_COLOURS = {
    'id_check': '#2196F3', 'parts_check': '#FFC107',
    'season_check': '#FF8F00', 'lookalike_check': '#ff5252',
    'warning_check': '#9C27B0'
}


def generate_quiz_question(category: str = "All", num_options: int = 3, rng=None, review=None):
    """Generate a random quiz question for the Daily Quiz."""
    r = rng or random

    # Map frontend categories to plant pools and preferred question types
    CATEGORY_MAP = {
        "Identification": {"pool": "all", "types": ["id_check"]},
        "Safety": {"pool": "mixed_danger", "types": ["lookalike_check", "warning_check", "id_check"]},
        "Seasons": {"pool": "edible", "types": ["season_check", "id_check"]},
        "Culinary": {"pool": "edible", "types": ["parts_check", "id_check"]},
        "Law": {"pool": "all", "types": ["warning_check", "id_check"]},
    }

    # Build plant pool from category
    if category in CATEGORY_MAP:
        mapping = CATEGORY_MAP[category]
        pool_type = mapping["pool"]
        preferred_types = mapping["types"]

        if pool_type == "edible":
            pool = UK_PLANTS['edible']
        elif pool_type == "poisonous":
            pool = UK_PLANTS['poisonous']
        elif pool_type == "mixed_danger":
            pool = UK_PLANTS['poisonous'] + [p for p in UK_PLANTS['edible']
                                               if any(isinstance(la, dict) and la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
                                                      for la in p.get('lookalikes', []))]
        else:
            pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
    elif category == "All":
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
        preferred_types = ['id_check', 'parts_check', 'season_check', 'lookalike_check', 'warning_check']
    else:
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']
        preferred_types = ['id_check', 'parts_check', 'season_check', 'lookalike_check', 'warning_check']

    if not pool:
        pool = UK_PLANTS['edible'] + UK_PLANTS['poisonous']

    # Spaced repetition: prefer review plants 60% of the time
    if review:
        review_pool = [p for p in pool if p.get('name', '') in review]
        if review_pool and r.random() < 0.6:
            plant = r.choice(review_pool)
        else:
            plant = r.choice(pool)
    else:
        plant = r.choice(pool)

    # Start with preferred types for this category, filter by what the plant supports
    question_types = list(preferred_types)

    has_dangerous_lookalike = any(
        isinstance(la, dict) and la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
        for la in plant.get('lookalikes', [])
    )
    if not has_dangerous_lookalike:
        question_types = [t for t in question_types if t != 'lookalike_check']
    if not plant.get('parts'):
        question_types = [t for t in question_types if t != 'parts_check']
    if not plant.get('warnings'):
        question_types = [t for t in question_types if t != 'warning_check']
    if not question_types:
        question_types = ['id_check']

    q_type = r.choice(question_types)
    is_edible = plant in UK_PLANTS['edible']
    all_names = [p['name'] for p in UK_PLANTS['edible'] + UK_PLANTS['poisonous']]

    if q_type == 'id_check':
        correct = "Edible" if is_edible else "Poisonous"
        options = ["Edible", "Poisonous"]
        if is_edible:
            fact = f"✅ **{plant['name']}** is edible. {plant.get('warnings', 'Always check ID!')}"
        else:
            danger = plant.get('danger_tips', {})
            danger_note = danger.get('danger_zone', plant.get('warnings', 'Extremely dangerous.'))
            fact = f"☠️ **{plant['name']}** is POISONOUS. {danger_note}"
        return {
            'type': q_type, 'type_icon': QUIZ_TYPE_ICONS[q_type],
            'type_name': QUIZ_TYPE_NAMES[q_type], 'type_color': QUIZ_TYPE_COLOURS[q_type],
            'text': f"Is **{plant['name']}** safe to eat?",
            'correct': correct, 'options': options, 'fact': fact,
            'plant': _plant_summary(plant, is_edible)
        }

    elif q_type == 'parts_check':
        edible_plant = r.choice(UK_PLANTS['edible'])
        is_edible_plant = True
        raw_parts = edible_plant.get('parts', 'Leaves')
        if isinstance(raw_parts, str):
            parts = [p.strip() for p in raw_parts.split(',')]
        else:
            parts = raw_parts
        if not parts:
            parts = ['Leaves']
        correct = parts[0]
        wrong_parts = ["Roots", "Berries", "Flowers", "Seeds", "Bark", "Stem"]
        wrong_options = [p for p in wrong_parts if p not in parts]
        options = [correct] + safe_sample(wrong_options, num_options - 1, rng=rng)
        while len(options) < num_options:
            options.append("None of the above")
        r.shuffle(options)
        fact = f"🍃 **{edible_plant['name']}**: Edible parts are {', '.join(parts)}. {edible_plant.get('warnings', '')}"
        return {
            'type': q_type, 'type_icon': QUIZ_TYPE_ICONS[q_type],
            'type_name': QUIZ_TYPE_NAMES[q_type], 'type_color': QUIZ_TYPE_COLOURS[q_type],
            'text': f"Which part of **{edible_plant['name']}** do we usually eat?",
            'correct': correct, 'options': options, 'fact': fact,
            'plant': _plant_summary(edible_plant, is_edible_plant)
        }

    elif q_type == 'season_check':
        edible_plant = r.choice(UK_PLANTS['edible'])
        is_edible_plant = True
        correct_months = edible_plant.get('months', ['Summer'])
        if isinstance(correct_months, str):
            correct_months = [correct_months]
        correct = r.choice(correct_months)
        all_months = ["January", "March", "June", "August", "October", "December"]
        wrong_months = [m for m in all_months if m not in correct_months]
        if not wrong_months:
            wrong_months = ["January", "March", "November"]
        options = [correct] + safe_sample(wrong_months, num_options - 1, rng=rng)
        while len(options) < num_options:
            options.append("None of the above")
        r.shuffle(options)
        fact = f"📅 **{edible_plant['name']}** is best in {', '.join(correct_months)}. Habitat: {edible_plant.get('habitat', 'Various')}."
        return {
            'type': q_type, 'type_icon': QUIZ_TYPE_ICONS[q_type],
            'type_name': QUIZ_TYPE_NAMES[q_type], 'type_color': QUIZ_TYPE_COLOURS[q_type],
            'text': f"When is **{edible_plant['name']}** best harvested?",
            'correct': correct, 'options': options, 'fact': fact,
            'plant': _plant_summary(edible_plant, is_edible_plant)
        }

    elif q_type == 'lookalike_check':
        dangerous_lookalikes = [
            la for la in plant.get('lookalikes', [])
            if isinstance(la, dict) and la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
        ]
        if dangerous_lookalikes:
            chosen = r.choice(dangerous_lookalikes)
            correct = chosen['name']
            other_names = [n for n in all_names if n != plant['name'] and n != correct]
            wrong_options = safe_sample(other_names, num_options - 1, rng=rng)
            options = [correct] + wrong_options
            while len(options) < num_options:
                options.append("None of the above")
            r.shuffle(options)
            confusion = plant.get('confusion_notes', chosen.get('diff', 'Check carefully!'))
            fact = f"☠️ **Key ID:** {confusion}"
            return {
                'type': q_type, 'type_icon': QUIZ_TYPE_ICONS[q_type],
                'type_name': QUIZ_TYPE_NAMES[q_type], 'type_color': QUIZ_TYPE_COLOURS[q_type],
                'text': f"**{plant['name']}** has a dangerous lookalike. Which of these is it?",
                'correct': correct, 'options': options, 'fact': fact,
                'plant': _plant_summary(plant, is_edible)
            }
        # Fallback
        correct = "Edible" if is_edible else "Poisonous"
        return {
            'type': 'id_check', 'type_icon': QUIZ_TYPE_ICONS['id_check'],
            'type_name': QUIZ_TYPE_NAMES['id_check'], 'type_color': QUIZ_TYPE_COLOURS['id_check'],
            'text': f"Is **{plant['name']}** safe to eat?",
            'correct': correct, 'options': ["Edible", "Poisonous"],
            'fact': plant.get('warnings', ''), 'plant': _plant_summary(plant, is_edible)
        }

    elif q_type == 'warning_check':
        warning = plant.get('warnings', '')
        if warning:
            if r.random() < 0.6:
                return {
                    'type': q_type, 'type_icon': QUIZ_TYPE_ICONS[q_type],
                    'type_name': QUIZ_TYPE_NAMES[q_type], 'type_color': QUIZ_TYPE_COLOURS[q_type],
                    'text': f"True or False: {warning}",
                    'correct': "True", 'options': ["True", "False"],
                    'fact': f"✅ This is correct: {warning}",
                    'plant': _plant_summary(plant, is_edible)
                }
            else:
                false_warning = warning
                swaps = [("cook", "eat raw"), ("edible", "poisonous"),
                         ("safe", "dangerous"), ("must", "don't need to"),
                         ("hairy", "smooth"), ("round", "flat"), ("never", "always")]
                for orig, swap in swaps:
                    if orig.lower() in false_warning.lower():
                        false_warning = false_warning.lower().replace(orig.lower(), swap.lower())
                        false_warning = false_warning[0].upper() + false_warning[1:]
                        break
                if false_warning != warning:
                    return {
                        'type': q_type, 'type_icon': QUIZ_TYPE_ICONS[q_type],
                        'type_name': QUIZ_TYPE_NAMES[q_type], 'type_color': QUIZ_TYPE_COLOURS[q_type],
                        'text': f"True or False: {false_warning}",
                        'correct': "False", 'options': ["True", "False"],
                        'fact': f"❌ That's FALSE. The real warning is: {warning}",
                        'plant': _plant_summary(plant, is_edible)
                    }
        # Fallback
        correct = "Edible" if is_edible else "Poisonous"
        return {
            'type': 'id_check', 'type_icon': QUIZ_TYPE_ICONS['id_check'],
            'type_name': QUIZ_TYPE_NAMES['id_check'], 'type_color': QUIZ_TYPE_COLOURS['id_check'],
            'text': f"Is **{plant['name']}** safe to eat?",
            'correct': correct, 'options': ["Edible", "Poisonous"],
            'fact': plant.get('warnings', ''), 'plant': _plant_summary(plant, is_edible)
        }

    # Shouldn't reach here, but just in case
    correct = "Edible" if is_edible else "Poisonous"
    return {
        'type': 'id_check', 'type_icon': QUIZ_TYPE_ICONS['id_check'],
        'type_name': QUIZ_TYPE_NAMES['id_check'], 'type_color': QUIZ_TYPE_COLOURS['id_check'],
        'text': f"Is **{plant['name']}** safe to eat?",
        'correct': correct, 'options': ["Edible", "Poisonous"],
        'fact': '', 'plant': _plant_summary(plant, is_edible)
    }


def generate_daily_seed():
    """Generate a deterministic seed based on today's date."""
    today = date.today().isoformat()
    return int(hashlib.md5(today.encode()).hexdigest(), 16) % (2**32)


def generate_daily_quiz_questions(num_questions=10, num_options=4):
    """Generate the same 10 questions for everyone today (deterministic seed)."""
    seed = generate_daily_seed()
    rng = random.Random(seed)
    categories = ["Identification", "Safety", "Seasons", "Culinary", "Law"]
    questions = []
    for i in range(num_questions):
        cat = rng.choice(categories)
        q = generate_quiz_question(cat, num_options, rng=rng)
        questions.append(q)
    return questions

def get_emergency_scenario(season: str = None) -> dict:
    """Get a random emergency scenario with contextual info."""
    from data.game_config import EMERGENCY_SCENARIOS, SEASON_MONTHS
    from datetime import datetime

    if season is None:
        current_month = datetime.now().strftime("%B")
        for s, months in SEASON_MONTHS.items():
            if current_month in months:
                season = s
                break
        if season is None:
            season = "Summer"

    # Filter scenarios appropriate to season
    if season in ["Winter"]:
        seasonal = [s for s in EMERGENCY_SCENARIOS if "January" in s["setting"] or "cold" in s["setting"].lower() or "freezing" in s["setting"].lower()]
    elif season in ["Spring"]:
        seasonal = [s for s in EMERGENCY_SCENARIOS if "March" in s["setting"] or "May" in s["setting"] or "damp" in s["setting"].lower()]
    elif season in ["Autumn"]:
        seasonal = [s for s in EMERGENCY_SCENARIOS if "September" in s["setting"] or "October" in s["setting"]]
    else:
        seasonal = EMERGENCY_SCENARIOS

    if not seasonal:
        seasonal = EMERGENCY_SCENARIOS

    scenario = random.choice(seasonal)
    return scenario


# ─────────────────────────────────────────────
# PLANT OF THE DAY & WEEKLY CHALLENGE
# ─────────────────────────────────────────────

def generate_plant_of_the_day() -> dict:
    """Generate deterministic Plant of the Day based on today's date."""
    seed = generate_daily_seed()
    rng = random.Random(seed)

    edible = UK_PLANTS["edible"]
    plant = rng.choice(edible)

    available_types = ['habitat', 'identification', 'parts', 'season']
    if any(isinstance(la, dict) and la.get('danger', '') in ['POISONOUS', 'DEADLY', 'HIGH', 'EXTREME']
           for la in plant.get('lookalikes', [])):
        available_types.append('lookalike')
    if plant.get('warnings'):
        available_types.append('warning')

    selected_types = rng.sample(available_types, min(3, len(available_types)))

    questions = []
    for q_type in selected_types:
        question = generate_foraging_question(
            season="Summer",
            preferred_type=q_type,
            force_plant=plant
        )
        questions.append(question)

    return {
        "plant": _plant_summary(plant),
        "date": date.today().isoformat(),
        "questions": questions
    }


def generate_weekly_challenge(num_questions: int = 10) -> dict:
    """Generate deterministic weekly challenge questions based on ISO week number."""
    today = date.today()
    iso_cal = today.isocalendar()
    week_id = f"{iso_cal[0]}-W{iso_cal[1]:02d}"
    seed = int(hashlib.md5(week_id.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)

    categories = ["Identification", "Safety", "Seasons", "Culinary", "Law"]
    questions = []
    for i in range(num_questions):
        cat = rng.choice(categories)
        q = generate_quiz_question(category=cat, num_options=4, rng=rng)
        questions.append(q)

    return {
        "week": week_id,
        "questions": questions
    }

