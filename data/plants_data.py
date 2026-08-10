# data/plants_data.py — Plant data assembly for Rocen Homesteady
# Imports from category files and combines into UK_PLANTS and PLANT_COUNTS

from .edible_trees import EDIBLE_TREES
from .edible_shrubs import EDIBLE_SHRUBS
from .edible_plants import EDIBLE_PLANTS
from .edible_fungi import EDIBLE_FUNGI
from .edible_coastal import EDIBLE_COASTAL
from .edible_seaweed import EDIBLE_SEAWEED
from .edible_shellfish import EDIBLE_SHELLFISH
from .poisonous_plants import POISONOUS_PLANTS
from .poisonous_fungi import POISONOUS_FUNGI

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
