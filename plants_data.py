# plants_data.py — Thin loader
# Imports plant data from category files and combines into UK_PLANTS

import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from data.edible_trees import EDIBLE_TREES
from data.edible_shrubs import EDIBLE_SHRUBS
from data.edible_plants import EDIBLE_PLANTS
from data.edible_fungi import EDIBLE_FUNGI
from data.edible_coastal import EDIBLE_COASTAL
from data.edible_seaweed import EDIBLE_SEAWEED
from data.edible_shellfish import EDIBLE_SHELLFISH
from data.poisonous_plants import POISONOUS_PLANTS
from data.poisonous_fungi import POISONOUS_FUNGI

UK_PLANTS = {
    "edible": EDIBLE_TREES + EDIBLE_SHRUBS + EDIBLE_PLANTS + EDIBLE_FUNGI + EDIBLE_COASTAL + EDIBLE_SEAWEED + EDIBLE_SHELLFISH,
    "poisonous": POISONOUS_PLANTS + POISONOUS_FUNGI,
    "categories": {
        "Tree": EDIBLE_TREES + [p for p in POISONOUS_PLANTS if p.get("category") == "Tree"],
        "Shrub": EDIBLE_SHRUBS + [p for p in POISONOUS_PLANTS if p.get("category") == "Shrub"],
        "Plant": EDIBLE_PLANTS + [p for p in POISONOUS_PLANTS if p.get("category") == "Plant"],
        "Fungi": EDIBLE_FUNGI + POISONOUS_FUNGI,
        "Coastal": EDIBLE_COASTAL + [p for p in POISONOUS_PLANTS if p.get("category") == "Coastal"],
        "Seaweed": EDIBLE_SEAWEED,
        "Shellfish": EDIBLE_SHELLFISH,
    }
}

PLANT_COUNTS = {
    "edible_trees": len(EDIBLE_TREES),
    "edible_shrubs": len(EDIBLE_SHRUBS),
    "edible_plants": len(EDIBLE_PLANTS),
    "edible_fungi": len(EDIBLE_FUNGI),
    "edible_coastal": len(EDIBLE_COASTAL),
    "edible_seaweed": len(EDIBLE_SEAWEED),
    "edible_shellfish": len(EDIBLE_SHELLFISH),
    "poisonous_plants": len(POISONOUS_PLANTS),
    "poisonous_fungi": len(POISONOUS_FUNGI),
    "total_edible": len(UK_PLANTS["edible"]),
    "total_poisonous": len(UK_PLANTS["poisonous"]),
    "total": len(UK_PLANTS["edible"]) + len(UK_PLANTS["poisonous"]),
}
