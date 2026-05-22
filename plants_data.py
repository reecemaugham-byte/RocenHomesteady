# plants_data.py

UK_PLANTS = {
    "edible": [
        {
            "name": "Lime (Leaves)",
        "latin_name": "Tilia cordata",
        "category": "Tree",
        "months": ["April", "May", "June", "July"],
        "habitat": "Woodlands, Parks",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Young leaves",
        "warnings": "Older leaves are tough and can be a choking hazard.",
        "description": "**Identification:** Heart-shaped leaves, slightly serrated edges. **Uses:** Excellent salad green (mild, slightly sweet).",
        "id_keys": {
            "Leaves": "Heart-shaped, hairless on top",
            "Bark": "Smooth, grey",
            "Flowers": "Yellow-white clusters"
        },
        "foraging_tips": {
            "where": "Woodlands and parks. Look for low branches.",
            "when": "Best in Spring (April-June) when leaves are young.",
            "sustainable": "Pick a few leaves from each branch, do not strip.",
            "danger_zone": "Safe. No dangerous lookalikes."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Common Lime is a hybrid. All Lime trees have edible leaves."
            }
        ],
        "confusion_notes": "Safe. One of the best tree leaves for eating."
    },
    {
        "name": "Oak (Acorns)",
        "latin_name": "Quercus robur",
        "category": "Tree",
        "months": ["September", "October", "November"],
        "habitat": "Woodlands, Hedgerows",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Nuts (Acorns)",
        "warnings": "MUST BE LEACHED (soaked) to remove tannins. Very bitter raw.",
        "description": "**Identification:** Lobed leaves (like a curved hand). Acorns in rough cups.",
        "id_keys": {
            "Leaves": "Lobed (wavy edges)",
            "Fruit": "Acorn in a rough cup",
            "Bark": "Rough, ridged"
        },
        "foraging_tips": {
            "where": "Woodlands, Hedgerows.",
            "when": "Autumn.",
            "sustainable": "Take only what you need; wildlife depend on them.",
            "danger_zone": "Raw acorns cause stomach upset due to tannins. Must be leached in running water."
        },
        "lookalikes": [
            {
                "name": "Sessile Oak",
                "danger": "EDIBLE",
                "diff": "Sessile Oak acorns have shorter stalks. Both are edible."
            }
        ],
        "confusion_notes": "Safe if processed. Tannins cause stomach upset if eaten raw."
    },
    {
        "name": "Wild Strawberry",
        "latin_name": "Fragaria vesca",
        "category": "Plant",
        "months": ["June", "July", "August"],
        "habitat": "Woodlands, Grassland",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries, Leaves",
        "warnings": "Small yield but intense flavour.",
        "description": "**Identification:** Low growing, trifoliate leaves (3 leaflets), small red berries pointing upwards.",
        "id_keys": {
            "Leaves": "3 leaflets, toothed",
            "Flowers": "White, 5 petals",
            "Fruit": "Small, red, seeds on outside"
        },
        "foraging_tips": {
            "where": "Woodlands, grassland, tracks.",
            "when": "Summer.",
            "sustainable": "Pick ripe berries only.",
            "danger_zone": "Ensure correct identification to avoid Barren Strawberry."
        },
        "lookalikes": [
            {
                "name": "Barren Strawberry",
                "danger": "INEDIBLE",
                "diff": "Barren Strawberry has petals with gaps between them. Wild Strawberry petals overlap."
            }
        ],
        "confusion_notes": "Confused with Barren Strawberry. **Key Diff:** Barren Strawberry has petals spaced apart (gaps show). Wild Strawberry petals overlap."
    },
    {
        "name": "Bilberry (Whortleberry)",
        "latin_name": "Vaccinium myrtillus",
        "category": "Shrub",
        "months": ["July", "August"],
        "habitat": "Moorland, Acid Soils",
        "regions": ["North", "Wales", "Scotland"],
        "difficulty": 2,
        "parts": "Berries",
        "warnings": "Stains fingers/teeth blue! Difficult to wash out.",
        "description": "**Identification:** Small deciduous shrub, blue-black berries (solo, not in clusters).",
        "id_keys": {
            "Berries": "Blue-black, soft, bloom",
            "Leaves": "Small, oval, finely toothed",
            "Habitat": "High moors"
        },
        "foraging_tips": {
            "where": "High moors, acid soils.",
            "when": "Late Summer.",
            "sustainable": "Pick sparingly; birds rely on them.",
            "danger_zone": "CRITICAL: Do not confuse with Deadly Nightshade. Bilberry is a LOW shrub."
        },
        "lookalikes": [
            {
                "name": "Deadly Nightshade",
                "danger": "POISONOUS",
                "diff": "Nightshade is a tall leafy plant with large shiny black berries. Bilberry is a low shrub with small berries."
            }
        ],
        "confusion_notes": "Confused with Deadly Nightshade. **Key Diff:** Nightshade is a tall plant with large shiny black berries. Bilberry is a low shrub with small berries."
    },
    {
        "name": "Meadowsweet",
        "latin_name": "Filipendula ulmaria",
        "category": "Plant",
        "months": ["June", "July", "August"],
        "habitat": "Damp Meadows, Riverbanks",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Flowers, Leaves",
        "warnings": "Contains aspirin-like compounds. Avoid if allergic to aspirin.",
        "description": "**Identification:** Tall, frothy cream-white flower heads. Smells of almond/honey.",
        "id_keys": {
            "Flowers": "Cream, frothy clusters",
            "Smell": "Almond/Honey scent",
            "Leaves": "Compound, white underside"
        },
        "foraging_tips": {
            "where": "Damp meadows, riverbanks.",
            "when": "Summer.",
            "sustainable": "Pick flower heads, leave plenty for pollinators.",
            "danger_zone": "Avoid if allergic to aspirin (salicylates)."
        },
        "lookalikes": [
            {
                "name": "Dropwort",
                "danger": "POISONOUS",
                "diff": "Dropwort grows on DRY ground. Meadowsweet loves DAMP ground."
            }
        ],
        "confusion_notes": "Confused with Dropwort. **Key Diff:** Dropwort is usually on dry ground. Meadowsweet loves damp ground and smells sweet."
    },
    {
        "name": "Chickweed",
        "latin_name": "Stellaria media",
        "category": "Plant",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Gardens, Waste Ground",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Stems",
        "warnings": "Eat raw or cooked. Very mild.",
        "description": "**Identification:** Low growing, small white star flowers, line of hairs on stem.",
        "id_keys": {
            "Stem": "Line of fine hairs (distinctive feature)",
            "Flowers": "Tiny white stars",
            "Leaves": "Oval, opposite pairs"
        },
        "foraging_tips": {
            "where": "Gardens, waste ground, fertile soil.",
            "when": "Year-round.",
            "sustainable": "Common weed, harvest freely.",
            "danger_zone": "Safe. Check for dog fouling in urban areas."
        },
        "lookalikes": [
            {
                "name": "Mouse-ear Chickweed",
                "danger": "EDIBLE",
                "diff": "Mouse-ear is hairy and tough. Chickweed has a line of hairs on one side only."
            }
        ],
        "confusion_notes": "Safe. Very common weed. Hairy mouse-ear chickweed is edible but texture is rough."
    },
    {
        "name": "Sea Purslane",
        "latin_name": "Halimione portulacoides",
        "category": "Coastal",
        "months": ["May", "June", "July", "August", "September"],
        "habitat": "Coastal Saltmarsh, Shingle",
        "regions": ["Coastal"],
        "difficulty": 1,
        "parts": "Leaves",
        "warnings": "Salty! Use as seasoning.",
        "description": "**Identification:** Grey-green fleshy leaves, woody stems. Grows near Samphire.",
        "id_keys": {
            "Leaves": "Succulent, grey-green, oblong",
            "Stem": "Woody at base",
            "Taste": "Very salty"
        },
        "foraging_tips": {
            "where": "Coastal saltmarsh, shingle.",
            "when": "Spring to Autumn.",
            "sustainable": "Pick sparingly in protected areas.",
            "danger_zone": "Safe. Distinctive grey colour."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive grey-green colour and salty taste."
            }
        ],
        "confusion_notes": "Safe. Distinctive grey colour."
    },
    {
        "name": "Burdock (Root)",
        "latin_name": "Arctium lappa",
        "category": "Plant",
        "months": ["September", "October", "November", "December"],
        "habitat": "Hedgerows, Waste Ground",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Root (First year)",
        "warnings": "Requires digging. Look for first-year plants (no burrs/flowers).",
        "description": "**Identification:** Large rhubarb-like leaves, purple thistle-like flowers that turn into sticky burrs.",
        "id_keys": {
            "Leaves": "Large, heart-shaped, rhubarb-like",
            "Flowers": "Purple thistle, sticky burrs",
            "Root": "Long, thin, brown skin"
        },
        "foraging_tips": {
            "where": "Hedgerows, waste ground.",
            "when": "Autumn/Winter (first year roots).",
            "sustainable": "Digging kills the plant. Only dig where abundant.",
            "danger_zone": "Only eat roots from first-year plants (those without flowers/burrs)."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Large leaves and sticky burrs are distinctive."
            }
        ],
        "confusion_notes": "Safe. Identify by the large leaves and sticky burrs. Only eat roots from first-year plants."
    },
    {
        "name": "Pignut",
        "latin_name": "Bunium bulbocastanum",
        "category": "Plant",
        "months": ["May", "June", "July"],
        "habitat": "Grassland, Meadows",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Tubers",
        "warnings": "Dig carefully. Distinctive nutty taste.",
        "description": "**Identification:** Delicate plant with fine, feathery leaves (like carrot). Small white flower umbels.",
        "id_keys": {
            "Leaves": "Feathery, carrot-like, delicate",
            "Flowers": "White umbels",
            "Root": "Small tuber, brown/black skin"
        },
        "foraging_tips": {
            "where": "Dry meadows, grassland.",
            "when": "Late Spring/Summer.",
            "sustainable": "Dig carefully, refill holes.",
            "danger_zone": "CRITICAL: Check ground is DRY. Hemlock Water Dropwort (Deadly) grows in WET ground."
        },
        "lookalikes": [
            {
                "name": "Hemlock Water Dropwort",
                "danger": "DEADLY",
                "diff": "Dropwort grows in WET ground/ditches. Pignut grows in DRY meadows."
            }
        ],
        "confusion_notes": "CRITICAL: Pignut grows in DRY meadows. Hemlock Water Dropwort grows in WET ground. If your feet are wet, STOP digging."
    },
    {
        "name": "Sloe (Blackthorn)",
        "latin_name": "Prunus spinosa",
        "category": "Shrub",
        "months": ["September", "October", "November"],
        "habitat": "Hedgerows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "Very bitter raw! Best after frost or frozen.",
        "description": "**Identification:** Small blue-black berries with a white 'bloom'. Large thorns on black branches.",
        "id_keys": {
            "Fruit": "Small, blue-black, sour",
            "Stem": "Black bark, large sharp thorns",
            "Bush": "Dense, thicket-forming"
        },
        "foraging_tips": {
            "where": "Hedgerows.",
            "when": "Autumn (after frost).",
            "sustainable": "Leave plenty for birds.",
            "danger_zone": "Thorns are sharp and can cause infection."
        },
        "lookalikes": [
            {
                "name": "Bullace",
                "danger": "EDIBLE",
                "diff": "Bullace is larger and less thorny."
            },
            {
                "name": "Damson",
                "danger": "EDIBLE",
                "diff": "Damson is larger and less thorny."
            }
        ],
        "confusion_notes": "Safe. Very sour raw but best after frost. Bullace and Damson are larger and less thorny. All are edible."
    },
    {
        "name": "Crab Apple",
        "latin_name": "Malus sylvestris",
        "category": "Tree",
        "months": ["September", "October"],
        "habitat": "Woodlands, Hedgerows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Fruit",
        "warnings": "Very tart/sour. Best for jams/jellies.",
        "description": "**Identification:** Small, round apples (golf ball size). Yellow/Green/Red. Often spiky look.",
        "id_keys": {
            "Fruit": "Small apples, long stalks",
            "Taste": "Very sour, dry mouth",
            "Leaves": "Oval, serrated"
        },
        "foraging_tips": {
            "where": "Woodlands, hedgerows.",
            "when": "Autumn.",
            "sustainable": "Use fallen fruit or pick sparingly.",
            "danger_zone": "Very tart. May cause stomach upset if eaten raw in quantity."
        },
        "lookalikes": [
            {
                "name": "Cultivated Apples",
                "danger": "EDIBLE",
                "diff": "Cultivated apples are larger and sweeter."
            }
        ],
        "confusion_notes": "Safe. Small, sour apples. All apple-like fruits are edible."
    },
    {
        "name": "Wood Blewit",
        "latin_name": "Clitocybe nuda",
        "category": "Fungi",
        "months": ["September", "October", "November", "December"],
        "habitat": "Woodlands, Gardens",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "Must be cooked. Some people have allergic reaction.",
        "description": "**Identification:** Lilac/Purple cap fading to tan. Lilac gills. Bulbous stem.",
        "id_keys": {
            "Cap": "Lilac turning tan",
            "Gills": "Lilac, crowded",
            "Stem": "Thick, bulbous, lilac"
        },
        "foraging_tips": {
            "where": "Woodlands, gardens (leaf litter).",
            "when": "Autumn.",
            "sustainable": "Cut at base, leave mycelium.",
            "danger_zone": "Must be cooked. Can cause allergic reaction in some people."
        },
        "lookalikes": [
            {
                "name": "Lilac Fibrecap",
                "danger": "POISONOUS",
                "diff": "Fibrecap grows in GRASS. Blewit grows on WOOD/LEAVES."
            }
        ],
        "confusion_notes": "IMPORTANT: Wood Blewit is lilac and grows on wood/leaves. Lilac Fibrecap grows in grass and is POISONOUS. Check where it grows!"
    },
    {
        "name": "Alexanders",
        "latin_name": "Smyrnium olusatrum",
        "category": "Coastal",
        "months": ["March", "April", "May"],
        "habitat": "Coastal, Hedgerows (near sea)",
        "regions": ["Coastal"],
        "difficulty": 2,
        "parts": "Stems, Roots, Flower buds",
        "warnings": "Seasonal - best in Spring.",
        "description": "**Identification:** Tall plant, yellow-green flowers, shiny green leaves. Smells of celery/parsley.",
        "id_keys": {
            "Stem": "Solid, green (not hollow like hemlock)",
            "Flowers": "Yellow-green umbels",
            "Smell": "Celery-like"
        },
        "foraging_tips": {
            "where": "Coastal hedgerows, near sea.",
            "when": "Spring.",
            "sustainable": "Common on coast, rarer inland.",
            "danger_zone": "Check for purple spotted stems (Hemlock)."
        },
        "lookalikes": [
            {
                "name": "Hemlock",
                "danger": "POISONOUS",
                "diff": "Hemlock has purple spots on stem and smells of mouse urine. Alexanders is green and smells of celery."
            }
        ],
        "confusion_notes": "CRITICAL: Alexanders has a solid GREEN stem and smells of celery. Hemlock has PURPLE SPOTS and smells of mouse urine."
    },
    {
        "name": "Garlic Mustard (Jack-by-the-Hedge)",
        "latin_name": "Alliaria petiolata",
        "category": "Plant",
        "months": ["April", "May", "June"],
        "habitat": "Hedgerows, Woodlands, Roadsides",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Flowers, Roots",
        "warnings": "Smells of garlic. Invasive in some areas.",
        "description": "**Identification:** Heart-shaped leaves with toothed edges. White flowers. Smells of garlic when crushed.",
        "id_keys": {
            "Leaves": "Heart-shaped, toothed, garlic smell",
            "Flowers": "White, 4 petals (cross shape)",
            "Height": "Up to 1m"
        },
        "foraging_tips": {
            "where": "Hedgerows, woods, paths.",
            "when": "Spring.",
            "sustainable": "Invasive - pick freely.",
            "danger_zone": "Safe. Distinctive garlic smell."
        },
        "lookalikes": [
            {"name": "None dangerous", "danger": "SAFE", "diff": "Garlic smell is unique."}
        ],
        "confusion_notes": "Safe. The garlic smell is the key identifier. If it smells of garlic, it is likely Garlic Mustard."
    },
    {
        "name": "Cleavers (Goosegrass)",
        "latin_name": "Galium aparine",
        "category": "Plant",
        "months": ["March", "April", "May", "June"],
        "habitat": "Hedgerows, Gardens, Waste Ground",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Stems, Seeds",
        "warnings": "Sticky/hairy texture. Best cooked or strained.",
        "description": "**Identification:** Straggly plant with hooked hairs that stick to clothes. Whorls of narrow leaves.",
        "id_keys": {
            "Texture": "Sticky (cleaves to clothes/fur)",
            "Leaves": "Whorls (circles) of 6-8 narrow leaves",
            "Stem": "Square, sticky"
        },
        "foraging_tips": {
            "where": "Everywhere.",
            "when": "Spring.",
            "sustainable": "Common weed. Pick freely.",
            "danger_zone": "Juice is good for lymphatic system. Cook like spinach."
        },
        "lookalikes": [
            {"name": "None", "danger": "SAFE", "diff": "The sticky texture is unique."}
        ],
        "confusion_notes": "Safe. The sticky texture makes it impossible to mistake. Cleaves to clothes and fur."
    },
    {
        "name": "Ribwort Plantain",
        "latin_name": "Plantago lanceolata",
        "category": "Plant",
        "months": ["March", "April", "May", "June", "July", "August"],
        "habitat": "Grassland, Paths, Lawns",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Seeds",
        "warnings": "Tough veins. Best eaten young.",
        "description": "**Identification:** Long, narrow, lance-shaped leaves with strong parallel veins. Brown flower head on a long stem.",
        "id_keys": {
            "Leaves": "Long, narrow, parallel veins",
            "Flower": "Brown oval/short spike on long stem",
            "Habitat": "Common in grass"
        },
        "foraging_tips": {
            "where": "Lawns, paths, fields.",
            "when": "Spring - Autumn.",
            "sustainable": "Common. Pick young leaves.",
            "danger_zone": "Safe. Seeds can be eaten like porridge."
        },
        "lookalikes": [
            {"name": "Greater Plantain", "danger": "EDIBLE", "diff": "Rounder leaves. Also edible."}
        ],
        "confusion_notes": "Safe. Very common. Long, narrow leaves with strong parallel veins."
    },
    {
        "name": "Common Mallow",
        "latin_name": "Malva sylvestris",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Waste Ground, Roadsides, Gardens",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Flowers, Seeds (Cheeses)",
        "warnings": "Mucilaginous (slimy) texture. Good for thickening.",
        "description": "**Identification:** Large maple-like leaves. Purple flowers with darker stripes. Seeds look like tiny cheeses.",
        "id_keys": {
            "Leaves": "Maple-like, 5-7 lobes",
            "Flowers": "Purple, dark veins/stripes",
            "Seeds": "Flat, round discs (cheeses)"
        },
        "foraging_tips": {
            "where": "Waste ground, fields.",
            "when": "Summer.",
            "sustainable": "Pick leaves and flowers.",
            "danger_zone": "Safe. Mucilage is soothing for digestion."
        },
        "lookalikes": [
            {"name": "None dangerous", "danger": "SAFE", "diff": "Maple-like leaves and purple flowers."}
        ],
        "confusion_notes": "Safe. Maple-like leaves and purple flowers. The 'cheese' shaped seeds are unique."
    },
    {
        "name": "Sweet Violet",
        "latin_name": "Viola odorata",
        "category": "Plant",
        "months": ["February", "March", "April"],
        "habitat": "Woodlands, Hedgerows, Gardens",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Flowers, Leaves",
        "warnings": "Sweet scent. Do not confuse with Dog Violet (scentless).",
        "description": "**Identification:** Heart-shaped leaves. Deep purple (sometimes white) flowers with a sweet scent.",
        "id_keys": {
            "Flowers": "Purple/White, sweet scent",
            "Leaves": "Heart-shaped",
            "Smell": "Sweet, perfumed"
        },
        "foraging_tips": {
            "where": "Woodlands, old gardens.",
            "when": "Early Spring.",
            "sustainable": "Pick a few flowers. Leave leaves.",
            "danger_zone": "Dog Violet has no scent. Safe but tasteless."
        },
        "lookalikes": [
            {"name": "Dog Violet", "danger": "EDIBLE", "diff": "No scent. Safe but not flavourful."}
        ],
        "confusion_notes": "Safe. Use your nose! Sweet Violet has a sweet scent. Dog Violet has no scent — safe but not flavourful."
    },
    {
        "name": "Oyster Mushroom",
        "latin_name": "Pleurotus ostreatus",
        "category": "Fungi",
        "months": ["September", "October", "November", "December"],
        "habitat": "Woodlands (Dead hardwood)",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Whole mushroom",
        "warnings": "Check for bugs. Gills should be white/cream.",
        "description": "**Identification:** Fan-shaped, oyster-like cap. Gills run down the stem (if present). Grows in tiers on wood.",
        "id_keys": {
            "Cap": "Fan/Oyster shaped, grey/brown",
            "Gills": "White, running down stem",
            "Habitat": "On dead wood (stumps/trunks)"
        },
        "foraging_tips": {
            "where": "Dead deciduous trees, stumps.",
            "when": "Autumn/Winter.",
            "sustainable": "Cut stem. Leave small ones.",
            "danger_zone": "Check for bugs. Slice and check inside."
        },
        "lookalikes": [
            {"name": "Angel's Wings", "danger": "POISONOUS", "diff": "Grows on conifers. White, very thin/fragile. Avoid white oysters on conifers."}
        ],
        "confusion_notes": "IMPORTANT: Only eat oyster mushrooms growing on HARDWOOD. White, thin, fragile mushrooms on CONIFERS could be Angel's Wings (POISONOUS)."
    },
    {
        "name": "Giant Puffball",
        "latin_name": "Calvatia gigantea",
        "category": "Fungi",
        "months": ["August", "September", "October"],
        "habitat": "Grassland, Pastures",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Whole mushroom (young)",
        "warnings": "Must be WHITE inside. If yellow/purple, discard.",
        "description": "**Identification:** Huge white ball (football size or bigger). White skin, white flesh inside.",
        "id_keys": {
            "Shape": "Giant white ball",
            "Inside": "Solid white (like cheese)",
            "Size": "Can be huge"
        },
        "foraging_tips": {
            "where": "Fields, pastures.",
            "when": "Late Summer/Autumn.",
            "sustainable": "Cut a slice. Leave small ones.",
            "danger_zone": "Slice open. Must be WHITE inside. If purple/yellow, it is old/spoiled."
        },
        "lookalikes": [
            {"name": "Earthball", "danger": "POISONOUS", "diff": "Earthball has THICK skin and PURPLE/BROWN inside. Giant Puffball is white inside."}
        ],
        "confusion_notes": "CRITICAL: Must be WHITE inside. If the inside is yellow, purple, or brown, it is too old or spoiled. Earthball is POISONOUS and has a THICK skin and PURPLE/BROWN inside."
    },
    {
        "name": "Ground Ivy",
        "latin_name": "Glechoma hederacea",
        "category": "Plant",
        "months": ["March", "April", "May", "June"],
        "habitat": "Woodlands, Hedgerows, Lawns",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves",
        "warnings": "Strong minty aroma. Good for tea.",
        "description": "**Identification:** Creeping plant. Round, scalloped leaves. Purple trumpet flowers. Smells minty.",
        "id_keys": {
            "Leaves": "Round, scalloped, opposite pairs",
            "Stem": "Creeping (square)",
            "Smell": "Minty/Aromatic"
        },
        "foraging_tips": {
            "where": "Lawns, paths, woods.",
            "when": "Spring.",
            "sustainable": "Common. Pick freely.",
            "danger_zone": "Safe. Good tea substitute."
        },
        "lookalikes": [
            {"name": "Dead-Nettle", "danger": "EDIBLE", "diff": "Dead-nettle has heart-shaped leaves. Ground Ivy has round/scalloped."}
        ],
        "confusion_notes": "Safe. The minty smell on a creeping plant is distinct. Dead-Nettle has heart-shaped leaves; Ground Ivy has round/scalloped leaves."
    },
    {
        "name": "Sea Beet",
        "latin_name": "Beta vulgaris maritima",
        "category": "Coastal",
        "months": ["May", "June", "July", "August", "September"],
        "habitat": "Coastal Cliffs, Shingle",
        "regions": ["Coastal"],
        "difficulty": 1,
        "parts": "Leaves",
        "warnings": "Wild ancestor of beetroot. Tasty.",
        "description": "**Identification:** Dark green, shiny leaves (like spinach). Grows on cliffs. Stems often reddish.",
        "id_keys": {
            "Leaves": "Dark green, shiny, triangular/oval",
            "Stem": "Often red/striped",
            "Habitat": "Coastal cliffs"
        },
        "foraging_tips": {
            "where": "Cliffs, shingle, coastal paths.",
            "when": "Spring - Autumn.",
            "sustainable": "Pick young leaves.",
            "danger_zone": "Safe. Wash to remove salt."
        },
        "lookalikes": [
            {"name": "None dangerous", "danger": "SAFE", "diff": "Distinctive coastal habitat."}
        ],
        "confusion_notes": "Safe. Wild ancestor of beetroot. Cook like spinach. Wash to remove salt."
    },
    {
        "name": "St. George's Mushroom",
        "latin_name": "Calocybe gambosa",
        "category": "Fungi",
        "months": ["April", "May"],
        "habitat": "Grassland, Lawns, Roadsides",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "EXPERT ID. Appears in Spring (St George's Day, April 23).",
        "description": "**Identification:** White cap, white gills, white stem. Mealy smell. Forms 'fairy rings' in grass.",
        "id_keys": {
            "Cap": "White, smooth",
            "Gills": "White, crowded",
            "Smell": "Mealy/floury",
            "Time": "Spring (Early)"
        },
        "foraging_tips": {
            "where": "Grassland, lawns.",
            "when": "April - May (Spring).",
            "sustainable": "Cut stem.",
            "danger_zone": "Must be confident. Poisonous Entoloma species look similar."
        },
        "lookalikes": [
            {"name": "Entoloma (Poisonous)", "danger": "POISONOUS", "diff": "Entolomas have PINK spores (check gill colour). St. George's is white throughout."}
        ],
        "confusion_notes": "CRITICAL: Appears in SPRING (April-May). Most poisonous lookalikes appear in AUTUMN. Still requires 100% confidence to eat."
    },
    {
        "name": "Charlock",
        "latin_name": "Sinapis arvensis",
        "category": "Plant",
        "months": ["May", "June", "July", "August"],
        "habitat": "Fields, Waste Ground, Arable Land",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Flowers, Seeds",
        "warnings": "Taste is hot/spicy (mustard). Use in moderation.",
        "description": "**Identification:** Bright yellow flowers (4 petals in a cross). Rough/hairy leaves. Seed pods are like small sausage shapes.",
        "id_keys": {
            "Flowers": "Yellow, 4 petals in a cross (Crucifer)",
            "Leaves": "Rough, hairy, lobed",
            "Stem": "Hairy",
            "Smell": "Hot/Mustardy when crushed"
        },
        "foraging_tips": {
            "where": "Fields, roadsides, arable land.",
            "when": "May - August.",
            "sustainable": "Common weed. Pick freely.",
            "danger_zone": "Can be spicy! Cook like spinach or use as seasoning."
        },
        "lookalikes": [
            {"name": "Rape (Oilseed Rape)", "danger": "EDIBLE", "diff": "Tall, blue-green leaves. Yellow flowers. Edible but bitter."},
            {"name": "Hedge Mustard", "danger": "EDIBLE", "diff": "Has a distinctive 'sauce' smell. Edible."}
        ],
        "confusion_notes": "Safe. The Cabbage family (Brassicaceae) is generally safe in the UK. If it has 4 petals in a cross and smells mustardy, it is likely edible."
    },
    {
        "name": "Shepherd's Purse",
        "latin_name": "Capsella bursa-pastoris",
        "category": "Plant",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Gardens, Fields, Paths, Waste Ground",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Seeds (peppery)",
        "warnings": "Seeds are peppery. Leaves best when young.",
        "description": "**Identification:** Rosette of leaves at base (dandelion-like). Tiny white flowers. Distinctive heart-shaped seed pods (purses).",
        "id_keys": {
            "Leaves": "Lobed, dandelion-like rosette (deep teeth)",
            "Flowers": "Tiny white, 4 petals",
            "Seeds": "Heart-shaped purses (distinctive)",
            "Height": "Low to medium (up to 40cm)"
        },
        "foraging_tips": {
            "where": "Everywhere. Gardens, paths, fields.",
            "when": "Year round (Best in Spring).",
            "sustainable": "Very common weed. Pick freely.",
            "danger_zone": "Seeds can be used as a pepper substitute."
        },
        "lookalikes": [
            {"name": "None dangerous", "danger": "SAFE", "diff": "Distinctive heart-shaped seed pods make it easy to ID."}
        ],
        "confusion_notes": "Safe. One of the most common weeds. Look for the 'purse' shaped seed pods — that is unique."
    },
    {
        "name": "Wild Garlic",
        "latin_name": "Allium ursinum",
        "category": "Plant",
        "months": ["March", "April", "May", "June"],
        "habitat": "Woodlands, Riverbanks",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Flowers, Bulbs",
        "warnings": "Can be confused with poisonous plants if not smelled.",
        "description": "**Identification:** Broad, lance-shaped leaves. White star-like flowers. Smells strongly of garlic.",
        "id_keys": {
            "Leaves": "Lance-shaped, soft, parallel veins",
            "Flowers": "White, 6 petals, star-shaped",
            "Smell": "Strong garlic smell when crushed"
        },
        "foraging_tips": {
            "where": "Damp woodlands, riverbanks.",
            "when": "Spring.",
            "sustainable": "Pick leaves sparingly, leave flowers for bees.",
            "danger_zone": "Safe if it smells of garlic. If no smell, do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Lily of the Valley",
                "danger": "POISONOUS",
                "diff": "Lily of the Valley has leaves that come from a central stem and NO garlic smell."
            },
            {
                "name": "Lords and Ladies",
                "danger": "POISONOUS",
                "diff": "Lords and Ladies has arrow-shaped leaves, often black spots, and NO garlic smell."
            }
        ],
        "confusion_notes": "☠️ CRITICAL: Wild Garlic smells STRONGLY of garlic. If it doesn't smell of garlic, do NOT eat it. Lily of the Valley has NO garlic smell."
    },
    {
        "name": "Nettles",
        "latin_name": "Urtica dioica",
        "category": "Plant",
        "months": ["March", "April", "May", "June"],
        "habitat": "Woodlands, Gardens, Fields",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Young leaves (tops)",
        "warnings": "Must be cooked to destroy stingers. Wear gloves to pick!",
        "description": "**Identification:** Green, heart-shaped leaves with jagged edges. Covered in tiny stinging hairs.",
        "id_keys": {
            "Leaves": "Heart-shaped, heavily toothed, opposite pairs",
            "Stem": "Square stem, stinging hairs",
            "Sting": "Causes immediate burning rash"
        },
        "foraging_tips": {
            "where": "Everywhere (fertile soil).",
            "when": "Spring (young tops).",
            "sustainable": "Cut tops off, plant will regrow.",
            "danger_zone": "Wear gloves! Must be cooked to remove sting."
        },
        "lookalikes": [
            {
                "name": "Dead-Nettle",
                "danger": "EDIBLE",
                "diff": "Dead-Nettles do not sting and have square stems with nettle-like leaves."
            }
        ],
        "confusion_notes": "Safe. Dead-Nettles look similar but are soft and don't sting. If it stings, it's a Nettle (and edible when cooked)."
    },
    {
        "name": "Dandelion",
        "latin_name": "Taraxacum officinale",
        "category": "Plant",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Lawns, Fields, Roadsides",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Flowers, Roots",
        "warnings": "Leaves are bitter. Root makes a coffee substitute.",
        "description": "**Identification:** Rosette of jagged leaves. Yellow flower head on a hollow stem. Milky sap.",
        "id_keys": {
            "Leaves": "Lion's tooth (jagged), rosette at base",
            "Stem": "Hollow, exudes milky sap",
            "Flower": "Bright yellow, single head"
        },
        "foraging_tips": {
            "where": "Lawns, fields, paths.",
            "when": "Spring for leaves, Autumn for roots.",
            "sustainable": "Very common.",
            "danger_zone": "Bitter but safe."
        },
        "lookalikes": [
            {
                "name": "Cat's Ear",
                "danger": "EDIBLE",
                "diff": "Cat's Ear has hairy leaves. Dandelion leaves are hairless."
            }
        ],
        "confusion_notes": "Safe. Most lookalikes are edible. Identify by the hollow stem and milky sap."
    },
    {
        "name": "Wild Carrot (Queen Anne's Lace)",
        "latin_name": "Daucus carota",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Grassland, Roadsides",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Root (1st year), Seeds",
        "warnings": "EXTREME CAUTION. Very easy to confuse with deadly Hemlock.",
        "description": "**Identification:** White lace-like flower head, often with a single red centre. Hairy stems. Carrot smell.",
        "id_keys": {
            "Flowers": "White umbels, flat-topped, red centre dot",
            "Stem": "HAIRY, green, NO purple spots",
            "Smell": "Smells of carrot when crushed"
        },
        "foraging_tips": {
            "where": "Dry grassland, roadsides.",
            "when": "Late Summer/Autumn.",
            "sustainable": "Digging root kills plant.",
            "danger_zone": "☠️ CRITICAL: Must have HAIRY stems and smell of CARROT. If it has purple spots, do NOT touch."
        },
        "lookalikes": [
            {
                "name": "Hemlock",
                "danger": "DEADLY",
                "diff": "Hemlock has SMOOTH stems with PURPLE SPOTS. Wild Carrot has HAIRY stems."
            }
        ],
        "confusion_notes": "☠️ CRITICAL: Hemlock has SMOOTH stems with PURPLE SPOTS. Wild Carrot has HAIRY stems. If you see purple spots, do NOT touch it."
    },
    {
        "name": "Three-Cornered Leek",
        "latin_name": "Allium triquetrum",
        "category": "Plant",
        "months": ["March", "April", "May"],
        "habitat": "Hedgerows, Woodlands, Roadsides",
        "regions": ["South West", "Wales", "Ireland"],
        "difficulty": 1,
        "parts": "Leaves, Flowers, Bulbs",
        "warnings": "Invasive in some areas. Very strong garlic/onion flavour.",
        "description": "**Identification:** Leaves are triangular in cross-section. White bell-shaped flowers with a green stripe.",
        "id_keys": {
            "Stem": "Triangular (3-cornered) in cross-section",
            "Flowers": "White bells with green stripe",
            "Smell": "Strong garlic/onion smell"
        },
        "foraging_tips": {
            "where": "Hedgerows, woodland (South West).",
            "when": "Spring.",
            "sustainable": "Invasive — pick freely where allowed.",
            "danger_zone": "Safe if it smells of garlic/onion."
        },
        "lookalikes": [
            {
                "name": "Bluebell",
                "danger": "POISONOUS",
                "diff": "Bluebell has NO garlic smell and tubular leaves. Three-Cornered Leek smells of garlic."
            }
        ],
        "confusion_notes": "CRITICAL: If it does NOT smell of garlic or onion, do NOT eat it. Bluebell is POISONOUS and has NO garlic smell."
    },
    {
        "name": "Wood Ear (Jelly Ear)",
        "latin_name": "Auricularia auricula-judae",
        "category": "Fungi",
        "months": ["January", "February", "March", "April", "May", "September", "October", "November", "December"],
        "habitat": "Woodlands (Elder trees)",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Whole mushroom",
        "warnings": "Must be cooked. Texture is rubbery.",
        "description": "**Identification:** Brown, ear-shaped, gelatinous fungus. Grows on elder wood.",
        "id_keys": {
            "Shape": "Ear-shaped, cupped",
            "Texture": "Jelly-like, rubbery, gelatinous",
            "Habitat": "Grows on dead Elder wood"
        },
        "foraging_tips": {
            "where": "Elder trees.",
            "when": "Autumn to Spring.",
            "sustainable": "Cut off with a knife.",
            "danger_zone": "Safe. Distinctive texture and host tree."
        },
        "lookalikes": [
            {
                "name": "Other Tree Ears",
                "danger": "EDIBLE",
                "diff": "Most similar-looking fungi on wood are edible, but Wood Ear is most common on Elder."
            }
        ],
        "confusion_notes": "Safe. If it looks like an ear and feels like jelly, it is likely Wood Ear. Does NOT grow on the ground."
    },
    {
        "name": "Sorrel",
        "latin_name": "Rumex acetosa",
        "category": "Plant",
        "months": ["March", "April", "May", "June", "July"],
        "habitat": "Grassland, Meadows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves",
        "warnings": "Contains oxalic acid (like spinach). Eat in moderation.",
        "description": "**Identification:** Large, arrow-shaped leaves. Very sharp lemon flavour.",
        "id_keys": {
            "Leaves": "Arrow-shaped, pointed lobes at base",
            "Taste": "Sharp, lemon/vinegar flavour",
            "Stem": "Tall, ridged, green/reddish"
        },
        "foraging_tips": {
            "where": "Meadows, grassland.",
            "when": "Spring.",
            "sustainable": "Pick outer leaves, leave centre.",
            "danger_zone": "Safe. Eat in moderation due to oxalic acid."
        },
        "lookalikes": [
            {
                "name": "Lords and Ladies",
                "danger": "POISONOUS",
                "diff": "Lords and Ladies BURNS the mouth instantly. Sorrel TASTES of lemon."
            }
        ],
        "confusion_notes": "Safe. Identified by the sharp lemon taste. If it burns your mouth (not lemon), it is NOT Sorrel."
    },
    {
        "name": "Elderflower",
        "latin_name": "Sambucus nigra",
        "category": "Tree",
        "months": ["May", "June"],
        "habitat": "Hedgerows, Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Flowers",
        "warnings": "Do not eat raw berries. Flowers must be cooked/brewed.",
        "description": "**Identification:** Flat-topped clusters of tiny, creamy-white, sweet-smelling flowers on a shrubby tree.",
        "id_keys": {
            "Flowers": "Flat, creamy-white clusters, sweet smell",
            "Leaves": "Compound, 5-7 leaflets, opposite",
            "Bark": "Corky, warty"
        },
        "foraging_tips": {
            "where": "Hedgerows, woods.",
            "when": "Late Spring/Early Summer.",
            "sustainable": "Pick clusters, leave plenty for berries.",
            "danger_zone": "Safe. Smells of sweet summer."
        },
        "lookalikes": [
            {
                "name": "Hemlock",
                "danger": "DEADLY",
                "diff": "Hemlock has white flowers on umbels (spokes) and purple spots on stems. Elder has flat clusters and woody bark."
            }
        ],
        "confusion_notes": "CRITICAL: Hemlock has purple spots on its stem and smells of mouse urine. Elder has woody bark and smells of sweet flowers."
    },
    {
        "name": "Blackberries",
        "latin_name": "Rubus fruticosus",
        "category": "Shrub",
        "months": ["August", "September", "October"],
        "habitat": "Hedgerows, Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "Thorny! Watch out for ticks and leeches.",
        "description": "**Identification:** Bramble shrub with thorny stems. Aggregate fruit (many tiny drupelets) turning from red to black.",
        "id_keys": {
            "Fruit": "Black, aggregate berry",
            "Stem": "Thorny (prickles), arching",
            "Leaves": "Compound, 3-5 leaflets"
        },
        "foraging_tips": {
            "where": "Hedgerows, fields.",
            "when": "Late Summer/Autumn.",
            "sustainable": "Very prolific. Pick freely.",
            "danger_zone": "Safe. Wash well."
        },
        "lookalikes": [
            {
                "name": "None",
                "danger": "SAFE",
                "diff": "All blackberry-like fruits in the UK are edible."
            }
        ],
        "confusion_notes": "Safe. No dangerous lookalikes in the UK. All blackberry-like fruits are edible."
    },
    {
        "name": "Rosehips",
        "latin_name": "Rosa canina",
        "category": "Shrub",
        "months": ["September", "October", "November"],
        "habitat": "Hedgerows, Scrub",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Fruit (Hips)",
        "warnings": "Seeds inside have irritating hairs. Must be strained out!",
        "description": "**Identification:** Red, oval hips on thorny shrubs with compound leaves.",
        "id_keys": {
            "Fruit": "Red, oval hips",
            "Stem": "Thorny shrub",
            "Leaves": "Compound, serrated edges"
        },
        "foraging_tips": {
            "where": "Hedgerows.",
            "when": "Autumn (after frost).",
            "sustainable": "Leave some for birds.",
            "danger_zone": "CRITICAL: Do NOT eat the seeds inside (they are itchy)."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive red hips."
            }
        ],
        "confusion_notes": "Safe. Distinctive red hips. Do NOT eat the seeds inside (they are itchy)."
    },
    {
        "name": "Hawthorn",
        "latin_name": "Crataegus monogyna",
        "category": "Tree",
        "months": ["May", "September", "October"],
        "habitat": "Hedgerows, Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Flowers, Berries (Haws)",
        "warnings": "Flowers smell faintly of almonds. Seeds contain cyanide, do not eat.",
        "description": "**Identification:** Thorny shrub. Deeply lobed leaves. White 'May' flowers. Red haws in autumn.",
        "id_keys": {
            "Leaves": "Deeply lobed (oak-like but smaller)",
            "Flowers": "White, 5 petals, 'May' blossom",
            "Fruit": "Red haws (single seed inside)"
        },
        "foraging_tips": {
            "where": "Hedgerows.",
            "when": "May for flowers, Autumn for haws.",
            "sustainable": "Very common hedgerow plant.",
            "danger_zone": "Safe. Spit out the seeds."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Look for 'May' flower in spring to identify."
            }
        ],
        "confusion_notes": "Safe. Look for 'May' flower in spring to identify. The berries (haws) are edible but don't eat the seeds (pips)."
    },
    {
        "name": "Chanterelle",
        "latin_name": "Cantharellus cibarius",
        "category": "Fungi",
        "months": ["July", "August", "September"],
        "habitat": "Woodlands (Birch, Oak, Beech)",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "Must be cooked. Do not wash, brush clean.",
        "description": "**Identification:** Egg-yolk yellow. Funnel-shaped. Blunt forking ridges (false gills) running down stem. Smells of apricots.",
        "id_keys": {
            "Colour": "Egg-yolk yellow",
            "Gills": "Blunt, forking ridges (false gills)",
            "Smell": "Apricots"
        },
        "foraging_tips": {
            "where": "Woodland floor.",
            "when": "Summer/Autumn.",
            "sustainable": "Cut stem, leave mycelium.",
            "danger_zone": "CRITICAL: Must have blunt ridges and smell of apricots."
        },
        "lookalikes": [
            {
                "name": "False Chanterelle",
                "danger": "POISONOUS",
                "diff": "False Chanterelle has thin, true gills like paper and NO apricot smell."
            },
            {
                "name": "Jack O'Lantern",
                "danger": "POISONOUS",
                "diff": "Grows in clusters on wood. True Chanterelle grows on the ground."
            }
        ],
        "confusion_notes": "CRITICAL: True Chanterelle has RIDGES (not gills) and smells of apricots. False Chanterelle has thin gills like paper and NO apricot smell."
    },
    {
        "name": "Field Mushroom",
        "latin_name": "Agaricus campestris",
        "category": "Fungi",
        "months": ["August", "September", "October"],
        "habitat": "Grassland, Fields",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "EXPERT ID. Yellow Stainer looks similar.",
        "description": "**Identification:** White cap. Pink gills turning dark brown. White stem with ring. Smells of mushroom/anise.",
        "id_keys": {
            "Cap": "White, smooth",
            "Gills": "Pink turning dark brown",
            "Smell": "Mushroom/Anise"
        },
        "foraging_tips": {
            "where": "Open grassland, fields.",
            "when": "Autumn.",
            "sustainable": "Cut stem.",
            "danger_zone": "CRITICAL: Check for yellow staining and bad smell."
        },
        "lookalikes": [
            {
                "name": "Yellow Stainer",
                "danger": "POISONOUS",
                "diff": "Yellow Stainer stains bright yellow when bruised and smells of ink."
            },
            {
                "name": "Death Cap",
                "danger": "DEADLY",
                "diff": "Death Cap has white gills (never pink) and a volva cup at the base."
            }
        ],
        "confusion_notes": "CRITICAL: Yellow Stainer stains bright yellow when bruised and smells of ink. Death Cap has white gills (never pink). If in doubt, do NOT eat."
    },
    {
        "name": "Hazelnut",
        "latin_name": "Corylus avellana",
        "category": "Shrub",
        "months": ["August", "September", "October"],
        "habitat": "Hedgerows, Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Nuts",
        "warnings": "Must be ripe. Green nuts are very astringent.",
        "description": "**Identification:** Shrub with rounded, toothed leaves. Nuts in leafy 'caps' (hats).",
        "id_keys": {
            "Leaves": "Rounded, double-toothed, soft",
            "Nut": "In a leafy, frilly 'hat'",
            "Shrub": "Bendy, multi-stemmed"
        },
        "foraging_tips": {
            "where": "Hedgerows, woods.",
            "when": "Early Autumn.",
            "sustainable": "Leave some for wildlife.",
            "danger_zone": "Safe. Identify by the leafy hat."
        },
        "lookalikes": [
            {
                "name": "Horse Chestnut",
                "danger": "POISONOUS",
                "diff": "Conkers have a smooth/warty green case, not a leafy frilly hat."
            }
        ],
        "confusion_notes": "Safe. Look for the leafy 'hat' on the nut. Horse Chestnut (conkers) has a smooth/warty case — NOT spiky."
    },
    {
        "name": "Sweet Chestnut",
        "latin_name": "Castanea sativa",
        "category": "Tree",
        "months": ["October", "November"],
        "habitat": "Woodlands, Parks",
        "regions": ["Southern"],
        "difficulty": 2,
        "parts": "Nuts",
        "warnings": "Must be cooked. Shell is sharp.",
        "description": "**Identification:** Large tree with long, toothed leaves. Nuts are in VERY SPIKY cases.",
        "id_keys": {
            "Leaves": "Long, narrow, toothed",
            "Nut Case": "VERY SPIKY, like a hedgehog",
            "Nuts": "Pointed, dark brown, often 2-3 per case"
        },
        "foraging_tips": {
            "where": "Southern woods, parks.",
            "when": "Autumn.",
            "sustainable": "Take fallen nuts.",
            "danger_zone": "CRITICAL: Case must be VERY SPIKY."
        },
        "lookalikes": [
            {
                "name": "Horse Chestnut",
                "danger": "POISONOUS",
                "diff": "Conker cases are smooth/warty. Sweet Chestnut cases are VERY SPIKY."
            }
        ],
        "confusion_notes": "CRITICAL: Sweet Chestnut has a VERY SPIKY case. Horse Chestnut (conkers) has a SMOOTH/WARTY case. If the case isn't spiky, it's NOT Sweet Chestnut."
    },
    {
        "name": "Pine Needles",
        "latin_name": "Pinus sylvestris",
        "category": "Tree",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Woodlands, Heathlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Needles",
        "warnings": "Good for tea. High in Vitamin C.",
        "description": "**Identification:** Evergreen tree. Needles are ROUND and in bundles (fascicles) of 2-5.",
        "id_keys": {
            "Needles": "ROUND, in bundles of 2-5",
            "Bark": "Reddish-brown, flaky upper bark",
            "Cones": "Woody, round"
        },
        "foraging_tips": {
            "where": "Coniferous woods.",
            "when": "Year-round (best in Spring).",
            "sustainable": "Snip a few needles.",
            "danger_zone": "CRITICAL: Needles must be ROUND and in bundles."
        },
        "lookalikes": [
            {
                "name": "Yew",
                "danger": "DEADLY",
                "diff": "Yew needles are FLAT and single, not in bundles."
            }
        ],
        "confusion_notes": "CRITICAL: Pine needles are ROUND and in BUNDLES. Yew needles are FLAT and deadly. If the needles are flat, do NOT make tea from them."
    },
    {
        "name": "Silver Birch",
        "latin_name": "Betula pendula",
        "category": "Tree",
        "months": ["March", "April", "May"],
        "habitat": "Woodlands, Heathlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Sap, Leaves",
        "warnings": "Sap must be collected in Spring. Leaves are diuretic.",
        "description": "**Identification:** White, peeling, papery bark. Small, triangular, toothed leaves.",
        "id_keys": {
            "Bark": "White, peeling, papery",
            "Leaves": "Small, triangular, doubly toothed",
            "Catkins": "Pendulous (hanging)"
        },
        "foraging_tips": {
            "where": "Woods, heaths.",
            "when": "Spring for sap, Summer for leaves.",
            "sustainable": "Tapping sap can harm tree. Only tap large trees.",
            "danger_zone": "Safe. Identify by the white peeling bark."
        },
        "lookalikes": [
            {
                "name": "Downy Birch",
                "danger": "EDIBLE",
                "diff": "Downy Birch has hairy twigs and less peeling bark. Also edible."
            }
        ],
        "confusion_notes": "Safe. Identify by the white peeling bark. Downy Birch is also edible."
    },
    {
        "name": "Beech Leaves",
        "latin_name": "Fagus sylvatica",
        "category": "Tree",
        "months": ["April", "May", "June"],
        "habitat": "Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Young leaves",
        "warnings": "Only eat young, transparent leaves. Older leaves are too tough.",
        "description": "**Identification:** Tall tree with smooth grey bark. Leaves are oval with wavy edges and soft hairs.",
        "id_keys": {
            "Bark": "Smooth, grey",
            "Leaves": "Oval, wavy edges, soft hairs when young",
            "Buds": "Pointed, brown"
        },
        "foraging_tips": {
            "where": "Woods.",
            "when": "Spring (only young leaves).",
            "sustainable": "Pick a few leaves from each branch.",
            "danger_zone": "Safe. Best when young and transparent."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive smooth grey bark and oval leaves."
            }
        ],
        "confusion_notes": "Safe. One of the best tree leaves for eating. Only eat young, transparent leaves."
    },
    {
        "name": "Marsh Samphire",
        "latin_name": "Salicornia europaea",
        "category": "Coastal",
        "months": ["June", "July", "August", "September"],
        "habitat": "Coastal Saltmarsh",
        "regions": ["Coastal"],
        "difficulty": 1,
        "parts": "Stems",
        "warnings": "Very salty. Best boiled or steamed. Do not overcook.",
        "description": "**Identification:** Green, jointed, fleshy stems that look like miniature cactus without the spines. Grows on mud.",
        "id_keys": {
            "Stem": "Fleshy, jointed, like a string of beads",
            "Habitat": "Saltmarsh, tidal mud",
            "Taste": "Very salty"
        },
        "foraging_tips": {
            "where": "Coastal saltmarsh.",
            "when": "Summer.",
            "sustainable": "Snip tops off, leave roots.",
            "danger_zone": "Safe. Known as 'Sea Asparagus'."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive jointed fleshy stems."
            }
        ],
        "confusion_notes": "Safe. Known as 'Sea Asparagus'. Very distinctive — grows on saltmarshes and tastes salty."
    },
    {
        "name": "Sea Kale",
        "latin_name": "Crambe maritima",
        "category": "Coastal",
        "months": ["March", "April", "May"],
        "habitat": "Coastal Shingle, Sand",
        "regions": ["Coastal"],
        "difficulty": 2,
        "parts": "Young shoots, Leaves",
        "warnings": "Protected in the wild. Grow from seed or pick sparingly.",
        "description": "**Identification:** Blue-green, waxy leaves. Crinkled edges. Thick shoots.",
        "id_keys": {
            "Leaves": "Blue-green, waxy, large, crinkled",
            "Habitat": "Shingle beaches",
            "Flowers": "White, 4 petals"
        },
        "foraging_tips": {
            "where": "Shingle beaches.",
            "when": "Spring.",
            "sustainable": "PROTECTED. Pick sparingly or grow your own.",
            "danger_zone": "Safe but protected."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive blue-green waxy leaves on shingle."
            }
        ],
        "confusion_notes": "Safe but protected. Identify by the blue-green waxy leaves on shingle beaches."
    },
    {
        "name": "Dulse",
        "latin_name": "Palmaria palmata",
        "category": "Seaweed",
        "months": ["May", "June", "July", "August", "September"],
        "habitat": "Coastal Rocks",
        "regions": ["Coastal"],
        "difficulty": 2,
        "parts": "Fronds",
        "warnings": "Wash well. Eat raw or dried.",
        "description": "**Identification:** Dark red, hand-shaped (palmate) fronds. Leathery texture.",
        "id_keys": {
            "Colour": "Dark red / purplish",
            "Shape": "Hand-shaped (lobes)",
            "Texture": "Leathery, soft when wet"
        },
        "foraging_tips": {
            "where": "Rocky shores (attached to rocks).",
            "when": "Summer.",
            "sustainable": "Snip above holdfast.",
            "danger_zone": "Safe. Wash to remove sand."
        },
        "lookalikes": [
            {
                "name": "Other Red Seaweeds",
                "danger": "EDIBLE",
                "diff": "Most red seaweeds are edible, but Dulse is distinct."
            }
        ],
        "confusion_notes": "Safe. Very distinct — dark red, hand-shaped, leathery texture. Other seaweeds are mostly edible but check ID."
    },
    {
        "name": "Cockles",
        "latin_name": "Cerastoderma edule",
        "category": "Shellfish",
        "months": ["July", "August", "September"],
        "habitat": "Coastal Estuaries, Sand",
        "regions": ["Coastal"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "Must be from clean water. Check for red tide warnings.",
        "description": "**Identification:** Bivalve shell with deep ribs. Heart shape when viewed from end.",
        "id_keys": {
            "Shell": "Ribbed, symmetrical, heart-shaped profile",
            "Colour": "Pale brown/yellow",
            "Habitat": "Sandy/muddy estuaries"
        },
        "foraging_tips": {
            "where": "Sandy estuaries.",
            "when": "Summer.",
            "sustainable": "Only take sizes over 20mm.",
            "danger_zone": "CRITICAL: Check water quality and red tide warnings."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "EDIBLE",
                "diff": "Other similar bivalves (like clams) are edible if from clean water."
            }
        ],
        "confusion_notes": "Safe. Distinctive ribbed shell, heart shape. Check for red tide warnings before collecting."
    },
    {
        "name": "Morel",
        "latin_name": "Morchella esculenta",
        "category": "Fungi",
        "months": ["March", "April", "May"],
        "habitat": "Woodlands, Gardens, Burnt Ground",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "Must be cooked. EXPERT ID. Hollow inside.",
        "description": "**Identification:** Honeycomb cap (pits and ridges). Cap is attached to stem. Hollow inside.",
        "id_keys": {
            "Cap": "Honeycomb pits and ridges",
            "Inside": "Hollow like a balloon",
            "Attachment": "Cap joins stem at the bottom"
        },
        "foraging_tips": {
            "where": "Woodlands, ash, burn sites.",
            "when": "Spring.",
            "sustainable": "Cut stem, leave base.",
            "danger_zone": "CRITICAL: Must be HOLLOW inside."
        },
        "lookalikes": [
            {
                "name": "False Morel",
                "danger": "DEADLY",
                "diff": "False Morel has brain wrinkles (not honeycomb pits) and is SOLID/CHAMBERED inside."
            }
        ],
        "confusion_notes": "CRITICAL: True Morel is HOLLOW inside like a balloon. False Morel is chambered/solid inside. If it is NOT hollow, do NOT eat it."
    },
    {
        "name": "Fat-Hen",
        "latin_name": "Chenopodium album",
        "category": "Plant",
        "months": ["May", "June", "July", "August", "September"],
        "habitat": "Gardens, Arable Land, Waste Ground",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Seeds",
        "warnings": "Contains oxalic acid. Cook before eating.",
        "description": "**Identification:** Diamond/mealy grey-green leaves. White powder on underside. Tall spikes of tiny green flowers.",
        "id_keys": {
            "Leaves": "Diamond-shaped, mealy white powder underneath",
            "Stem": "Streaked with red/purple",
            "Flowers": "Tiny, green, dense spikes"
        },
        "foraging_tips": {
            "where": "Gardens, arable fields.",
            "when": "Summer.",
            "sustainable": "Common weed. Pick freely.",
            "danger_zone": "Safe. Cook like spinach."
        },
        "lookalikes": [
            {
                "name": "Orache",
                "danger": "EDIBLE",
                "diff": "Orache has leaves that are more triangular and often red-tinged."
            }
        ],
        "confusion_notes": "Safe. The mealy white powder on the underside of the leaves is distinctive. Cook like spinach."
    },
    {
        "name": "Hairy Bittercress",
        "latin_name": "Cardamine hirsuta",
        "category": "Plant",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Gardens, Paths",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Stems, Flowers",
        "warnings": "Peppery taste. Don't eat too much raw.",
        "description": "**Identification:** Small rosette of leaflets. Tiny white flowers. Seed pods explode when touched.",
        "id_keys": {
            "Leaves": "Small, round leaflets in a rosette",
            "Flowers": "Tiny, white, 4 petals",
            "Seeds": "Slender pods that explode"
        },
        "foraging_tips": {
            "where": "Gardens, paths, plant pots.",
            "when": "Year-round.",
            "sustainable": "Common garden weed.",
            "danger_zone": "Safe. Great pepper substitute."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive exploding seed pods."
            }
        ],
        "confusion_notes": "Safe. The exploding seed pods make it impossible to mistake."
    },
    {
        "name": "Wild Raspberry",
        "latin_name": "Rubus idaeus",
        "category": "Shrub",
        "months": ["July", "August"],
        "habitat": "Woodlands, Hedgerows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "Thorny canes.",
        "description": "**Identification:** Red/purple berries that pull easily from the plug. White flowers. Pale, prickly canes.",
        "id_keys": {
            "Fruit": "Red, hollow (leaves core behind)",
            "Stem": "Prickly, pale/grey",
            "Leaves": "Compound, white underneath"
        },
        "foraging_tips": {
            "where": "Woodland edges, clearings.",
            "when": "Summer.",
            "sustainable": "Leave plenty for wildlife.",
            "danger_zone": "Safe. Distinctive hollow berry."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "All raspberry-like fruits in the UK are edible."
            }
        ],
        "confusion_notes": "Safe. All raspberry-like fruits in the UK are edible."
    },
    {
        "name": "Elderberry",
        "latin_name": "Sambucus nigra",
        "category": "Tree",
        "months": ["August", "September"],
        "habitat": "Hedgerows, Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "MUST be cooked. Raw berries cause vomiting. Red berries are POISONOUS.",
        "description": "**Identification:** Clusters of small, black/purple berries on red stems. Shrub with corky bark.",
        "id_keys": {
            "Fruit": "Black/purple, small, in flat clusters",
            "Stem": "Red/purple stems holding berries",
            "Bark": "Corky, warty"
        },
        "foraging_tips": {
            "where": "Hedgerows, woods.",
            "when": "Autumn.",
            "sustainable": "Leave some for birds.",
            "danger_zone": "CRITICAL: Must be COOKED. Raw berries cause vomiting."
        },
        "lookalikes": [
            {
                "name": "Dwarf Elder",
                "danger": "POISONOUS",
                "diff": "Dwarf Elder has upright berry clusters and smells unpleasant."
            }
        ],
        "confusion_notes": "CRITICAL: Elderberries MUST be cooked. Raw berries cause vomiting. Red elderberries are POISONOUS."
    },
    {
        "name": "Shaggy Inkcap",
        "latin_name": "Coprinus comatus",
        "category": "Fungi",
        "months": ["August", "September", "October", "November"],
        "habitat": "Grassland, Roadsides, Waste Ground",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Whole mushroom",
        "warnings": "Must be eaten very fresh (within hours). Turns to ink. Do NOT mix with alcohol.",
        "description": "**Identification:** Tall, white, cylindrical cap with shaggy scales. White gills turn pink, then black, then dissolve into ink.",
        "id_keys": {
            "Cap": "White, tall, shaggy scales",
            "Gills": "White -> Pink -> Black -> Ink",
            "Habitat": "Bare soil, roadsides, paths"
        },
        "foraging_tips": {
            "where": "Grass, paths, roads.",
            "when": "Autumn.",
            "sustainable": "Cut stem.",
            "danger_zone": "CRITICAL: Eat within hours of picking. Do NOT drink alcohol."
        },
        "lookalikes": [
            {
                "name": "Common Inkcap",
                "danger": "POISONOUS (with alcohol)",
                "diff": "Common Inkcap is smaller, less shaggy, and causes severe illness if alcohol is consumed."
            }
        ],
        "confusion_notes": "CRITICAL: Must be eaten fresh before it turns to ink. Do NOT consume alcohol with Inkcap mushrooms."
    },
    {
        "name": "Hedgehog Mushroom",
        "latin_name": "Hydnum repandum",
        "category": "Fungi",
        "months": ["August", "September", "October", "November"],
        "habitat": "Woodlands (Beech, Oak)",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Whole mushroom",
        "warnings": "Can be bitter raw. Must be cooked.",
        "description": "**Identification:** Pale cap. Underneath has SPINES (not gills) that look like a hedgehog. Smells peppery.",
        "id_keys": {
            "Cap": "Pale buff/ochre, irregular",
            "Spines": "Under cap, hanging down (not gills)",
            "Smell": "Peppery"
        },
        "foraging_tips": {
            "where": "Woodland (under beech/oak).",
            "when": "Autumn.",
            "sustainable": "Cut stem.",
            "danger_zone": "Safe. Spines instead of gills make it hard to mistake."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "The spines underneath are unique. No dangerous lookalikes."
            }
        ],
        "confusion_notes": "Safe. If it has spines underneath instead of gills, it is a Hedgehog Mushroom. No dangerous lookalikes."
    },
    {
        "name": "Parasol Mushroom",
        "latin_name": "Macrolepiota procera",
        "category": "Fungi",
        "months": ["July", "August", "September", "October"],
        "habitat": "Grassland, Pastures, Open Woods",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Cap",
        "warnings": "Only eat caps. Stems are too tough. Must be cooked.",
        "description": "**Identification:** Very tall. Large brown-scaled cap like a parasol. Brown 'snakeskin' pattern on stem. Moveable ring.",
        "id_keys": {
            "Cap": "Large, brown scales on white background",
            "Stem": "Brown snakeskin pattern",
            "Ring": "Moveable ring on stem"
        },
        "foraging_tips": {
            "where": "Open grassland, paths.",
            "when": "Late Summer/Autumn.",
            "sustainable": "Cut cap, leave stem.",
            "danger_zone": "CRITICAL: Must have snakeskin stem and moveable ring."
        },
        "lookalikes": [
            {
                "name": "Shaggy Parasol",
                "danger": "EDIBLE (some people allergic)",
                "diff": "Shaggy Parasol is smaller and has a white stem, not snakeskin."
            }
        ],
        "confusion_notes": "CRITICAL: True Parasol has a SNAKESKIN pattern on the stem and a moveable ring. If the stem is smooth or white, do NOT eat it."
    },
    {
        "name": "Watercress",
        "latin_name": "Nasturtium officinale",
        "category": "Plant",
        "months": ["March", "April", "May", "June", "July", "August", "September"],
        "habitat": "Clean Streams, Waterways",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Leaves, Stems",
        "warnings": "Must be washed. Do not collect from polluted water (liver fluke risk).",
        "description": "**Identification:** Grows in running water. Small, rounded leaves. White flowers. Peppery taste.",
        "id_keys": {
            "Leaves": "Small, rounded, dark green",
            "Habitat": "Growing IN clean running water",
            "Taste": "Peppery"
        },
        "foraging_tips": {
            "where": "Clean, fast-flowing streams.",
            "when": "Spring - Autumn.",
            "sustainable": "Snip tops, leave roots.",
            "danger_zone": "CRITICAL: Must be from CLEAN water. Risk of liver fluke."
        },
        "lookalikes": [
            {
                "name": "Fool's Watercress",
                "danger": "EDIBLE",
                "diff": "Fool's Watercress has broader leaves and grows in still water. Edible but check water quality."
            }
        ],
        "confusion_notes": "CRITICAL: Only pick from CLEAN, running water. If water is polluted or still, do NOT eat due to liver fluke risk."
    },
    {
        "name": "Yarrow",
        "latin_name": "Achillea millefolium",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Grassland, Meadows, Lawns",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Leaves, Flowers",
        "warnings": "Good for tea. Can be bitter. Avoid if pregnant.",
        "description": "**Identification:** Feathery, fern-like leaves. Flat-topped clusters of white (or pink) flowers.",
        "id_keys": {
            "Leaves": "Feathery, fern-like, divided",
            "Flowers": "Flat-topped clusters, white/pink",
            "Smell": "Aromatic, medicinal"
        },
        "foraging_tips": {
            "where": "Grassland, lawns, paths.",
            "when": "Summer.",
            "sustainable": "Common. Pick leaves and flowers.",
            "danger_zone": "Safe. Avoid if pregnant."
        },
        "lookalikes": [
            {
                "name": "Hemlock",
                "danger": "DEADLY",
                "diff": "Hemlock has SMOOTH stems with PURPLE SPOTS and smells of mouse urine. Yarrow has FEATHERY leaves and smells aromatic."
            }
        ],
        "confusion_notes": "Safe. Distinctive feathery leaves and aromatic smell. Hemlock has purple spotted stems."
    },
    {
        "name": "Rowan",
        "latin_name": "Sorbus aucuparia",
        "category": "Tree",
        "months": ["August", "September", "October"],
        "habitat": "Woodlands, Hillsides, Gardens",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "Very bitter raw. Must be cooked. Contains parasorbic acid (cooked = sorbic acid, safe).",
        "description": "**Identification:** Tree with paired leaflets. Bright orange-red berries in large clusters.",
        "id_keys": {
            "Berries": "Orange-red, large clusters",
            "Leaves": "Paired leaflets, serrated",
            "Buds": "Hairy, sticky buds"
        },
        "foraging_tips": {
            "where": "Hills, woods, gardens.",
            "when": "Autumn.",
            "sustainable": "Leave some for birds.",
            "danger_zone": "CRITICAL: Must be COOKED. Raw berries cause stomach upset."
        },
        "lookalikes": [
            {
                "name": "Whitebeam",
                "danger": "EDIBLE",
                "diff": "Whitebeam has white berries. Rowan has red/orange."
            }
        ],
        "confusion_notes": "CRITICAL: Rowan berries MUST be cooked. Raw they contain parasorbic acid which causes stomach upset. Cooked they are safe."
    },
    {
        "name": "Sweet Cicely",
        "latin_name": "Myrrhis odorata",
        "category": "Plant",
        "months": ["March", "April", "May", "June"],
        "habitat": "Roadsides, Hedgerows, Gardens",
        "regions": ["North", "Scotland", "Wales"],
        "difficulty": 2,
        "parts": "Leaves, Stems, Roots, Seeds",
        "warnings": "Sweet aniseed flavour. Great sugar substitute.",
        "description": "**Identification:** Feathery leaves with white blotches. White umbels. Strong aniseed smell.",
        "id_keys": {
            "Leaves": "Feathery, white blotches on underside",
            "Flowers": "White umbels",
            "Smell": "Strong aniseed"
        },
        "foraging_tips": {
            "where": "Hedgerows, roadsides (North).",
            "when": "Spring.",
            "sustainable": "Pick leaves, leave roots.",
            "danger_zone": "Safe. Smells strongly of aniseed."
        },
        "lookalikes": [
            {
                "name": "Hemlock",
                "danger": "DEADLY",
                "diff": "Hemlock has purple spots and smells of mouse urine. Sweet Cicely has white blotches on leaves and smells of aniseed."
            }
        ],
        "confusion_notes": "CRITICAL: Sweet Cicely smells of ANISEED and has white blotches on leaves. Hemlock smells of MOUSE URINE and has purple spots."
    },
    {
        "name": "Rock Samphire",
        "latin_name": "Crithmum maritimum",
        "category": "Coastal",
        "months": ["May", "June", "July", "August"],
        "habitat": "Coastal Cliffs",
        "regions": ["Coastal"],
        "difficulty": 2,
        "parts": "Leaves, Stems",
        "warnings": "Strong, aromatic flavour. Often pickled.",
        "description": "**Identification:** Fleshy, green, carrot-like leaves growing on sea cliffs. Smells of carrots/aniseed.",
        "id_keys": {
            "Leaves": "Fleshy, divided, carrot-like",
            "Habitat": "Cliff faces, rocks by the sea",
            "Smell": "Carrot/aniseed"
        },
        "foraging_tips": {
            "where": "Cliff faces (DANGER: Do not risk falling).",
            "when": "Summer.",
            "sustainable": "Cut stems, leave roots.",
            "danger_zone": "CRITICAL: Do NOT climb dangerous cliffs for it."
        },
        "lookalikes": [
            {
                "name": "Marsh Samphire",
                "danger": "EDIBLE",
                "diff": "Marsh Samphire grows on mud and has jointed stems. Rock Samphire grows on cliffs."
            }
        ],
        "confusion_notes": "Safe but grows on dangerous cliffs. Distinctive carrot-like leaves and aniseed smell."
    },
    {
        "name": "Sea Aster",
        "latin_name": "Tripolium pannonicum",
        "category": "Coastal",
        "months": ["July", "August", "September"],
        "habitat": "Coastal Saltmarsh",
        "regions": ["Coastal"],
        "difficulty": 1,
        "parts": "Leaves, Flowers",
        "warnings": "Salty. Good raw or cooked.",
        "description": "**Identification:** Looks like a daisy/aster. Lilac petals with yellow centre. Fleshy, linear leaves.",
        "id_keys": {
            "Flowers": "Lilac/blue petals, yellow centre",
            "Leaves": "Fleshy, linear, salty",
            "Habitat": "Saltmarshes"
        },
        "foraging_tips": {
            "where": "Saltmarshes.",
            "when": "Summer/Autumn.",
            "sustainable": "Pick young leaves.",
            "danger_zone": "Safe. Very distinct."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive lilac daisy on saltmarsh."
            }
        ],
        "confusion_notes": "Safe. Distinctive lilac daisy-like flower growing on saltmarshes."
    }
],
    "poisonous": [
        {
            "name": "Deadly Nightshade",
        "latin_name": "Atropa belladonna",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Woodlands, Gardens, Waste Ground",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially berries)",
        "warnings": "EXTREME. Fatal in small doses. Do not handle without gloves.",
        "description": "**Identification:** A tall, bushy perennial. Bell-shaped purple flowers. Shiny black berries the size of cherries. **Danger:** Causes rapid heartbeat, dilated pupils, hallucinations, and death.",
        "id_keys": {
            "Flowers": "Purple, bell-shaped, nodding",
            "Berries": "Shiny black, cherry-sized, solitary",
            "Leaves": "Oval, pointed, large"
        },
        "danger_tips": {
            "where": "Shady, damp woods and calcareous soils.",
            "when": "Berries appear late summer.",
            "sustainable": "Do not pick. Remove carefully if found in gardens.",
            "danger_zone": "☠️ DEADLY. Just 2-3 berries can kill a child. Do NOT touch."
        },
        "lookalikes": [
            {
                "name": "Bilberry",
                "danger": "EDIBLE",
                "diff": "Bilberry is a low shrub with small, matte blue-black berries. Deadly Nightshade is a tall leafy plant with large shiny black berries."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Deadly Nightshade has LARGE shiny black berries (cherry-sized) on a TALL leafy plant. Bilberry is a LOW shrub with SMALL matte blue-black berries. If the berries are cherry-sized on a tall plant, do NOT touch it."
    },
    {
        "name": "Foxglove",
        "latin_name": "Digitalis purpurea",
        "category": "Plant",
        "months": ["June", "July", "August"],
        "habitat": "Gardens, Woodlands, Acid Soils",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "All parts",
        "warnings": "HIGH. Can cause heart failure. Toxins can be absorbed through skin.",
        "description": "**Identification:** Tall spikes of pink/purple trumpet flowers. Large, fuzzy leaves at the base. **Danger:** Contains digitalis which affects heart rate.",
        "id_keys": {
            "Flowers": "Pink/Purple trumpets, spotted inside",
            "Stem": "Tall, green, sturdy spike",
            "Leaves": "Large, rosette at base, soft texture"
        },
        "danger_tips": {
            "where": "Common in gardens, woodland clearings, and heaths.",
            "when": "Flowering in summer.",
            "sustainable": "Admire from a distance. Do NOT touch.",
            "danger_zone": "☠️ HIGH. Can cause heart failure. Toxins can be absorbed through skin."
        },
        "lookalikes": [
            {
                "name": "Comfrey",
                "danger": "EDIBLE",
                "diff": "Comfrey has bell-shaped flowers that hang in loose clusters. Foxglove flowers are distinct trumpets growing up a single tall spike."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Foxglove has tall spikes of PINK/PURPLE trumpet flowers. Comfrey has smaller bell-shaped flowers that hang in loose clusters. Foxglove is a single tall spike with distinct trumpet shapes."
    },
    {
        "name": "Hemlock",
        "latin_name": "Conium maculatum",
        "category": "Plant",
        "months": ["April", "May", "June", "July"],
        "habitat": "Rivers, Damp areas, Roadsides",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "All parts",
        "warnings": "EXTREME. Deadliest plant in the UK. Mistaken for wild celery/parsley.",
        "description": "**Identification:** Tall plant (up to 2m). Smooth stem with distinctive purple spots. Smells of mouse urine. **Danger:** Causes respiratory paralysis.",
        "id_keys": {
            "Stem": "Smooth, hollow, purple spots (critical ID)",
            "Smell": "Unpleasant, mouse urine smell when crushed",
            "Flowers": "White umbels (flat-topped clusters)"
        },
        "danger_tips": {
            "where": "Damp ditches, riverbanks, waste ground.",
            "when": "Spring and early summer.",
            "sustainable": "Never cut or smell closely.",
            "danger_zone": "☠️ DEADLY. Respiratory failure, death. Toxins can be absorbed through skin. Do NOT touch."
        },
        "lookalikes": [
            {
                "name": "Wild Carrot",
                "danger": "EDIBLE",
                "diff": "Wild Carrot has HAIRY stems. Hemlock has SMOOTH stems with purple spots."
            },
            {
                "name": "Cow Parsley",
                "danger": "EDIBLE",
                "diff": "Cow Parsley stems are ridged/grooved and green. Hemlock stems are smooth with purple blotches."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Hemlock has SMOOTH stems with PURPLE SPOTS and smells of MOUSE URINE. Wild Carrot has HAIRY green stems and smells of CARROT. If you see purple spots, do NOT touch it."
    },
    {
        "name": "Hemlock Water Dropwort",
        "latin_name": "Oenanthe crocata",
        "category": "Plant",
        "months": ["April", "May", "June", "July"],
        "habitat": "Riverbanks, Wet ground, Ditches",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "All parts (Roots deadliest)",
        "warnings": "EXTREME. 'Dead Man's Fingers'. Rapid death.",
        "description": "**Identification:** Grows in water/wet mud. White flowers. Roots are tuberous, resembling a cluster of pale fingers. **Danger:** Causes seizures and death rapidly.",
        "id_keys": {
            "Root": "Tubers like fingers (Dead Man's Fingers)",
            "Habitat": "Wet ground, feet in water",
            "Stem": "Grooved, hollow"
        },
        "danger_tips": {
            "where": "Riverbanks, streams, wet ditches.",
            "when": "Spring and Summer.",
            "sustainable": "Never dig roots in wet areas.",
            "danger_zone": "☠️ DEADLY. Rapid onset seizures, coma, death. Do NOT touch."
        },
        "lookalikes": [
            {
                "name": "Wild Parsnip",
                "danger": "EDIBLE",
                "diff": "Wild Parsnip has YELLOW flowers. Dropwort has WHITE flowers."
            },
            {
                "name": "Pignut",
                "danger": "EDIBLE",
                "diff": "Pignut grows in DRY meadows. Dropwort grows in WET ground/ditches. If your feet are wet, stop digging."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Grows in WET ground (feet in water). Roots look like fingers ('Dead Man's Fingers'). Pignut grows in DRY meadows. If your feet are wet, STOP digging."
    },
    {
        "name": "Death Cap",
        "latin_name": "Amanita phalloides",
        "category": "Fungi",
        "months": ["July", "August", "September"],
        "habitat": "Woodlands (especially Oak)",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "EXTREME. Responsible for most mushroom deaths worldwide.",
        "description": "**Identification:** Greenish-yellow cap. White gills. Distinctive white cup (volva) at the base underground. **Danger:** Liver/kidney failure.",
        "id_keys": {
            "Cap": "Green-yellow, sometimes streaked",
            "Gills": "White, free from stem",
            "Base": "Volva (Cup) in ground, ring on stem"
        },
        "danger_tips": {
            "where": "Broadleaf woodland, often under Oak.",
            "when": "Summer and Autumn.",
            "sustainable": "Never pick mushrooms with a volva (cup) at the base.",
            "danger_zone": "☠️ DEADLY. Symptoms delayed 6-24 hours. Fatal liver damage."
        },
        "lookalikes": [
            {
                "name": "Straw Mushroom",
                "danger": "EDIBLE",
                "diff": "Straw Mushroom has PINK gills. Death Cap has WHITE gills."
            },
            {
                "name": "Caesar's Mushroom",
                "danger": "EDIBLE",
                "diff": "Caesar's has a bright orange/red cap. Death Cap is green/yellow."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Death Cap has WHITE gills (never pink) and a volva (cup) at the base underground. Straw Mushroom has PINK gills. If you see a white cup at the base, do NOT pick it."
    },
    {
        "name": "Lords and Ladies",
        "latin_name": "Arum maculatum",
        "category": "Plant",
        "months": ["March", "April", "May", "August", "September"],
        "habitat": "Hedgerows, Woods",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts",
        "warnings": "HIGH. Causes immediate burning pain and blisters.",
        "description": "**Identification:** Arrow-shaped leaves (often with black spots). Orange-red berries on a spike. **Danger:** Calcium oxalate crystals needle the tongue/throat.",
        "id_keys": {
            "Leaves": "Arrow-shaped, often spotted black",
            "Berries": "Bright orange cluster on a spike",
            "Flower": "Pale green 'hood' (spathe)"
        },
        "danger_tips": {
            "where": "Shady hedgerows and woods.",
            "when": "Leaves in Spring, Berries in Autumn.",
            "sustainable": "Do NOT touch or taste.",
            "danger_zone": "☠️ HIGH. Instant burning pain and blisters. Do NOT put in your mouth."
        },
        "lookalikes": [
            {
                "name": "Sorrel",
                "danger": "EDIBLE",
                "diff": "Sorrel leaves are arrow-shaped but smaller, usually unspotted, and taste lemony. Lords & Ladies are large, leathery, and have NO smell."
            },
            {
                "name": "Wild Garlic",
                "danger": "EDIBLE",
                "diff": "Wild Garlic smells strongly of garlic. Lords & Ladies has NO garlic smell and different leaf texture."
            }
        ],
        "confusion_notes": "☠️ DANGER: Lords and Ladies has arrow-shaped leaves (often with black spots) and burns your mouth INSTANTLY. Wild Garlic SMELLS of garlic. Sorrel TASTES of lemon. Lords and Ladies does NEITHER."
    },
    {
        "name": "Yew",
        "latin_name": "Taxus baccata",
        "category": "Tree",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Churchyards, Gardens, Woodlands",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Needles, Seeds",
        "warnings": "EXTREME. All parts deadly except the red berry flesh.",
        "description": "**Identification:** Dark evergreen tree. Flat, dark green needles. Red fleshy 'berries' (arils) with a dark seed inside. **Danger:** Causes cardiac arrest.",
        "id_keys": {
            "Needles": "Flat, dark green, pointed",
            "Fruit": "Red cup (aril) containing a dark seed",
            "Bark": "Reddish-brown, peeling"
        },
        "danger_tips": {
            "where": "Churchyards, gardens, woodlands.",
            "when": "Evergreen all year. Berries in Autumn.",
            "sustainable": "Never eat the seed inside the red berry.",
            "danger_zone": "☠️ DEADLY. Sudden death, no antidote. Do NOT eat any part except the red berry flesh (and even that is risky)."
        },
        "lookalikes": [
            {
                "name": "Pine",
                "danger": "EDIBLE",
                "diff": "Pine needles are ROUND and long. Yew needles are FLAT, short, and darker."
            },
            {
                "name": "Fir",
                "danger": "EDIBLE",
                "diff": "Fir needles are flat but attach to the stem like a suction cup. Yew needles are distinct dark green."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Yew needles are FLAT. Pine needles are ROUND and in bundles. If the needles are flat, do NOT make tea from them. The red berry flesh is the only safe part — the SEED inside is deadly."
    },
    {
        "name": "False Morel",
        "latin_name": "Gyromitra esculenta",
        "category": "Fungi",
        "months": ["March", "April", "May"],
        "habitat": "Woodlands, Sandy Soils",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "EXTREME. Raw or poorly cooked it is deadly.",
        "description": "**Identification:** Brain-like cap (wrinkled, irregular lobes). NOT hollow inside. **Danger:** Contains gyromitrin (converted to rocket fuel in body).",
        "id_keys": {
            "Cap": "Brain-like, irregular lobes, reddish-brown",
            "Inside": "Chambered (not hollow)",
            "Texture": "Wrinkled, not honeycomb pits"
        },
        "danger_tips": {
            "where": "Coniferous woodlands, sandy soil.",
            "when": "Spring.",
            "sustainable": "Do not pick. Vapours can be toxic when cooking.",
            "danger_zone": "☠️ DEADLY. Contains gyromitrin (converted to rocket fuel in body). Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Morel",
                "danger": "EDIBLE",
                "diff": "True Morel is HOLLOW inside like a balloon. False Morel is CHAMBERED/SOLID inside. True Morel has honeycomb pits; False Morel has brain wrinkles."
            }
        ],
        "confusion_notes": "☠️ DEADLY: False Morel is brain-shaped (wrinkled, NOT honeycomb) and is NOT hollow inside. True Morel has HONEYCOMB pits and IS hollow like a balloon. If it is NOT hollow, do NOT eat it."
    },
    {
        "name": "Spindle",
        "latin_name": "Euonymus europaeus",
        "category": "Shrub",
        "months": ["August", "September", "October"],
        "habitat": "Hedgerows, Woods",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries, Bark",
        "warnings": "HIGH. Strong laxative, liver damage.",
        "description": "**Identification:** Shrub with distinctive pink berries that split open to reveal orange seeds. Leaves turn red in autumn.",
        "id_keys": {
            "Fruit": "Pink, 4-lobed, orange seeds inside (distinctive)",
            "Leaves": "Opposite, pointed, serrated, turn red",
            "Twigs": "Green, angular"
        },
        "danger_tips": {
            "where": "Hedgerows and woodland edges.",
            "when": "Berries in Autumn.",
            "sustainable": "Admire the colour, do not eat.",
            "danger_zone": "HIGH. Severe stomach upset, liver and kidney damage."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive bright pink/orange fruits are unique among common hedgerow plants. No edible plant has this fruit structure."
            }
        ],
        "confusion_notes": "Distinctive bright PINK berries with orange seeds inside. No common edible lookalike has this fruit structure. Do NOT eat the berries."
    },
    {
        "name": "Woody Nightshade (Bittersweet)",
        "latin_name": "Solanum dulcamara",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Hedgerows, Woods",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially berries)",
        "warnings": "MEDIUM to HIGH. Poisonous, causes vomiting.",
        "description": "**Identification:** Climbing plant. Purple flowers with yellow centre cone. Bright red, egg-shaped berries.",
        "id_keys": {
            "Flowers": "Purple star, yellow cone centre",
            "Berries": "Red, egg-shaped, in clusters",
            "Leaves": "Arrow-shaped, often with basal lobes"
        },
        "danger_tips": {
            "where": "Hedgerows, scrambling over plants.",
            "when": "Flowers summer, berries autumn.",
            "sustainable": "Remove from gardens if children present.",
            "danger_zone": "HIGH. Vomiting, dizziness, diarrhoea."
        },
        "lookalikes": [
            {
                "name": "Deadly Nightshade",
                "danger": "POISONOUS",
                "diff": "Deadly Nightshade has BLACK berries and purple/yellow BELL flowers. Woody Nightshade has RED egg berries and purple STAR flowers."
            }
        ],
        "confusion_notes": "Woody Nightshade has PURPLE star flowers with a YELLOW cone centre and RED egg-shaped berries. Deadly Nightshade has PURPLE BELL flowers and BLACK shiny berries. Do NOT eat either of them."
    },
    {
        "name": "White Bryony",
        "latin_name": "Bryonia dioica",
        "category": "Plant",
        "months": ["August", "September", "October"],
        "habitat": "Hedgerows, Woodlands",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially berries)",
        "warnings": "HIGH. Severe purgative. Can be fatal.",
        "description": "**Identification:** Climbing plant (creeper). Red berries. Large lobed leaves (ivy-like). Curling tendrils used to climb.",
        "id_keys": {
            "Fruit": "Red berries, size of peas",
            "Leaves": "Lobed, ivy-like, rough texture",
            "Climb": "Climbs using curling tendrils (vital ID)"
        },
        "danger_tips": {
            "where": "Hedgerows, scrambling over bushes.",
            "when": "Berries late summer/autumn.",
            "sustainable": "Do not touch berries.",
            "danger_zone": "HIGH. Severe vomiting, diarrhoea, dehydration."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Distinctive climber with tendrils. No common edible climber has red berries in hedges."
            }
        ],
        "confusion_notes": "Distinctive climber with red berries. No common edible climber has red berries in hedges. Do NOT eat the berries (irritant)."
    },
    {
        "name": "Black Bryony",
        "latin_name": "Tamus communis",
        "category": "Plant",
        "months": ["August", "September", "October"],
        "habitat": "Hedgerows, Woods",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially berries)",
        "warnings": "HIGH. Skin irritant. Poisonous if eaten.",
        "description": "**Identification:** Climbing plant. Shiny black berries. Heart-shaped glossy leaves. Twining stems (no tendrils).",
        "id_keys": {
            "Fruit": "Shiny black berries",
            "Leaves": "Heart-shaped, glossy, shiny",
            "Stem": "Twining climber (wraps around stems)"
        },
        "danger_tips": {
            "where": "Hedgerows, woods, shady places.",
            "when": "Autumn berries.",
            "sustainable": "Avoid skin contact with sap.",
            "danger_zone": "HIGH. Skin irritation, severe stomach pain."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "Shiny black berries and heart-shaped leaves on a twining stem. Unlikely to be confused with edibles."
            }
        ],
        "confusion_notes": "Distinctive climber with shiny black berries and heart-shaped glossy leaves. No common edible climber has shiny black berries. Do NOT touch the berries (skin irritant)."
    },
    {
        "name": "Giant Hogweed",
        "latin_name": "Heracleum mantegazzianum",
        "category": "Plant",
        "months": ["June", "July", "August"],
        "habitat": "Riverbanks, Waste Ground",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Sap (All parts)",
        "warnings": "EXTREME. Sap causes severe burns in sunlight (Phototoxicity).",
        "description": "**Identification:** Massive plant (up to 5m). Thick stems with purple blotches and bristles. Huge flower heads (umbels).",
        "id_keys": {
            "Height": "Giant (3-5m tall)",
            "Stem": "Thick, purple blotches, bristly",
            "Flowers": "Huge white umbels (50cm+)"
        },
        "danger_tips": {
            "where": "Riverbanks, waste ground.",
            "when": "Summer.",
            "sustainable": "Report sightings. Do NOT touch.",
            "danger_zone": "☠️ EXTREME. Sap + Sun = Blisters/Burns. Can cause BLINDNESS if rubbed in eyes. Do NOT touch."
        },
        "lookalikes": [
            {
                "name": "Common Hogweed",
                "danger": "EDIBLE",
                "diff": "Common Hogweed is smaller (1-2m). Stems are green/pale, less blotchy. Giant is HUGE."
            },
            {
                "name": "Alexanders",
                "danger": "EDIBLE",
                "diff": "Alexanders has solid green stems (no purple blotches) and smells of celery."
            }
        ],
        "confusion_notes": "☠️ DANGER: Giant Hogweed is HUGE (3-5m tall) with purple blotches on thick stems. Common Hogweed is smaller (1-2m) with green/pale stems. If it is GIANT with purple spots, do NOT touch it — the sap burns in sunlight."
    },
    {
        "name": "Meadow Saffron",
        "latin_name": "Colchicum autumnale",
        "category": "Plant",
        "months": ["August", "September", "October"],
        "habitat": "Meadows, Woodlands, Damp grassland",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially seeds and corm)",
        "warnings": "EXTREME. Fatal in small doses. No antidote.",
        "description": "**Identification:** Purple, crocus-like flowers appearing in autumn with NO leaves present. Leaves appear in spring. **Danger:** Contains colchicine which causes multi-organ failure.",
        "id_keys": {
            "Flowers": "Purple, crocus-like, 6 petals, no leaves when flowering",
            "Leaves": "Appear in spring, long, lance-shaped",
            "Corm": "Underground bulb, highly toxic"
        },
        "danger_tips": {
            "where": "Damp meadows and woodland clearings.",
            "when": "Flowers in Autumn, leaves in Spring.",
            "sustainable": "Do not pick wild crocus-like flowers.",
            "danger_zone": "☠️ DEADLY. No antidote. Causes organ failure. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Autumn Crocus (Saffron Crocus)",
                "danger": "EDIBLE (Saffron)",
                "diff": "Saffron Crocus has 3 stigmas (red/orange) and leaves appear with flowers. Meadow Saffron has 6 stamens and flowers appear ALONE (no leaves)."
            },
            {
                "name": "Wild Garlic",
                "danger": "EDIBLE",
                "diff": "Wild Garlic has white star flowers and smells strongly of garlic. Meadow Saffron is purple and scentless."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Meadow Saffron flowers appear in AUTUMN with NO LEAVES. Saffron Crocus has leaves and 3 RED stigmas. If a purple crocus-like flower has no leaves, do NOT touch it."
    },
    {
        "name": "Monkshood",
        "latin_name": "Aconitum napellus",
        "category": "Plant",
        "months": ["June", "July", "August"],
        "habitat": "Woodlands, Gardens, Mountain areas",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially roots)",
        "warnings": "EXTREME. Most poisonous plant in UK. Absorbed through skin.",
        "description": "**Identification:** Tall spikes of dark blue/purple hooded flowers. Dark green, glossy, deeply divided leaves. **Danger:** Contains aconitine which affects the heart and nerves.",
        "id_keys": {
            "Flowers": "Blue/Purple, hooded (like a monk's cowl)",
            "Leaves": "Dark green, glossy, palmately lobed",
            "Root": "Tuberous, highly toxic"
        },
        "danger_tips": {
            "where": "Damp woods, stream sides, gardens.",
            "when": "Summer.",
            "sustainable": "Do NOT touch without gloves.",
            "danger_zone": "☠️ DEADLY. Absorbed through skin. Causes heart palpitations and death. Do NOT touch."
        },
        "lookalikes": [
            {
                "name": "Larkspur",
                "danger": "MILDLY TOXIC",
                "diff": "Larkspur flowers have a backward pointing spur. Monkshood has a distinct helmet/hood shape over the top."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Monkshood has BLUE/PURPLE flowers shaped like a HOOD or helmet. Larkspur has a backward pointing spur. Do NOT touch Monkshood, even skin contact is DEADLY."
    },
    {
        "name": "Lily of the Valley",
        "latin_name": "Convallaria majalis",
        "category": "Plant",
        "months": ["May", "June"],
        "habitat": "Woodlands, Gardens",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially red berries)",
        "warnings": "HIGH. Contains cardiac glycosides. Fatal if eaten.",
        "description": "**Identification:** Low growing plant. Two large leaves with curved parallel veins. Drooping bells of white flowers. Orange-red berries in autumn.",
        "id_keys": {
            "Flowers": "White, bell-shaped, drooping on one side of stem",
            "Leaves": "Two large leaves, parallel veins",
            "Berries": "Orange-red, round"
        },
        "danger_tips": {
            "where": "Shady woods, gardens.",
            "when": "Flowers in Spring, Berries in Autumn.",
            "sustainable": "Do not pick for indoor displays.",
            "danger_zone": "☠️ HIGH. Causes heart irregularities and nausea. Do NOT eat the red berries."
        },
        "lookalikes": [
            {
                "name": "Wild Garlic",
                "danger": "EDIBLE",
                "diff": "Wild Garlic has a distinct garlic smell. Lily of the Valley has NO garlic smell and different leaf veins (curved parallel vs straight)."
            },
            {
                "name": "Solomon's Seal",
                "danger": "EDIBLE",
                "diff": "Solomon's Seal has flowers hanging in pairs along the stem underside. Lily of the Valley flowers are clustered on one side."
            }
        ],
        "confusion_notes": "☠️ DANGER: Lily of the Valley has WHITE bells on one side of the stem and NO garlic smell. Wild Garlic SMELLS of garlic. If it doesn't smell of garlic, do NOT eat it."
    },
    {
        "name": "Fool's Parsley",
        "latin_name": "Aethusa cynapium",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Gardens, Arable land, Hedgerows",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "All parts",
        "warnings": "HIGH. Poisonous, causes convulsions.",
        "description": "**Identification:** Looks like flat-leaved parsley. White flowers (umbels). Distinctive long bracts hanging down under the flower head. Smells of mustard/mouse.",
        "id_keys": {
            "Flowers": "White umbels, with long thin bracts underneath",
            "Leaves": "Similar to flat-leaf parsley, but glossy underneath",
            "Smell": "Unpleasant, like mouse or mustard when crushed"
        },
        "danger_tips": {
            "where": "Cultivated ground, gardens, hedgerows.",
            "when": "Summer.",
            "sustainable": "Do not pick wild 'parsley'.",
            "danger_zone": "☠️ HIGH. Burning mouth, vomiting, convulsions. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Cow Parsley",
                "danger": "EDIBLE",
                "diff": "Cow Parsley has hairy stems and no long bracts under the umbel. Fool's Parsley has smooth stems and long dangling bracts."
            },
            {
                "name": "Flat-leaf Parsley",
                "danger": "EDIBLE",
                "diff": "Cultivated parsley smells of fresh parsley. Fool's Parsley smells like mouse/mustard."
            }
        ],
        "confusion_notes": "☠️ DANGER: Fool's Parsley has long green bracts hanging DOWN under the flower umbels and smells of MOUSE URINE. Cow Parsley does NOT have long bracts. If it has dangling bracts, do NOT eat it."
    },
    {
        "name": "Dog's Mercury",
        "latin_name": "Mercurialis perennis",
        "category": "Plant",
        "months": ["February", "March", "April", "May"],
        "habitat": "Woodlands, Hedgerows",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts",
        "warnings": "HIGH. Causes severe vomiting and inflammation.",
        "description": "**Identification:** Low growing, carpeting woodland plant. Dark green, opposite, oval leaves. Separate male and female plants (catkin-like male flowers).",
        "id_keys": {
            "Leaves": "Oval, toothed, opposite, dark green, rough texture",
            "Flowers": "Green, insignificant (male on spikes, female in leaf axils)",
            "Habitat": "Forms large carpets in ancient woodland"
        },
        "danger_tips": {
            "where": "Shady woodland, dominant ground cover.",
            "when": "Spring.",
            "sustainable": "Do not add to wild salads.",
            "danger_zone": "☠️ HIGH. Causes vomiting, dizziness. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Nettle",
                "danger": "EDIBLE",
                "diff": "Nettles have stinging hairs and heart-shaped leaves. Dog's Mercury has smooth, oval, toothed leaves and NO stings."
            },
            {
                "name": "Mint",
                "danger": "EDIBLE",
                "diff": "Mint smells strongly of mint. Dog's Mercury has no distinct mint smell."
            }
        ],
        "confusion_notes": "☠️ DANGER: Dog's Mercury has OVAL, non-stinging leaves and NO mint smell. Nettles STING. Mint SMELLS of mint. If you don't know what it is in a carpet, do NOT eat it."
    },
    {
        "name": "Daffodil",
        "latin_name": "Narcissus pseudonarcissus",
        "category": "Plant",
        "months": ["February", "March", "April"],
        "habitat": "Woodlands, Gardens, Meadows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Bulbs (All parts irritant)",
        "warnings": "MEDIUM to HIGH. Causes severe stomach upset. Bulbs mistaken for onions.",
        "description": "**Identification:** Yellow trumpet flowers. Long, flat, strap-like leaves. Underground bulb.",
        "id_keys": {
            "Flowers": "Yellow trumpet with 6 petals",
            "Leaves": "Flat, strap-like, upright, grey-green",
            "Bulb": "Underground, onion-like"
        },
        "danger_tips": {
            "where": "Gardens, woods, roadsides.",
            "when": "Spring.",
            "sustainable": "Do not dig up wild bulbs.",
            "danger_zone": "HIGH. Severe stomach upset and skin irritation. Do NOT eat bulbs."
        },
        "lookalikes": [
            {
                "name": "Onion/Garlic",
                "danger": "EDIBLE",
                "diff": "Onion/Garlic bulbs smell strongly of onion/garlic. Daffodil bulbs have NO onion/garlic smell."
            },
            {
                "name": "Snowdrop",
                "danger": "MILDLY TOXIC",
                "diff": "Snowdrops are smaller, white, and have distinct green markings inside. Daffodils are large and yellow."
            }
        ],
        "confusion_notes": "☠️ DANGER: Daffodil bulbs do NOT smell like ONION. If a bulb doesn't smell of onion or garlic, it is NOT an onion. Do NOT eat mystery bulbs."
    },
    {
        "name": "Fly Agaric",
        "latin_name": "Amanita muscaria",
        "category": "Fungi",
        "months": ["August", "September", "October"],
        "habitat": "Woodlands (especially Birch)",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Whole mushroom",
        "warnings": "HIGH. Contains ibotenic acid. Psychoactive and toxic.",
        "description": "**Identification:** Iconic red cap with white spots (warts). White gills. White stem with ring and bulbous base.",
        "id_keys": {
            "Cap": "Bright red with white warts/spots (can wash off in rain)",
            "Gills": "White, free from stem",
            "Base": "Bulbous with volva cup"
        },
        "danger_tips": {
            "where": "Birch and pine woodlands.",
            "when": "Autumn.",
            "sustainable": "Admire, do not pick.",
            "danger_zone": "☠️ HIGH. Nausea, hallucinations, delirium. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Blusher",
                "danger": "EDIBLE (if cooked)",
                "diff": "Blusher has a brownish-red cap that turns PINK when bruised. Fly Agaric is bright red with white spots."
            },
            {
                "name": "Caesar's Mushroom",
                "danger": "EDIBLE",
                "diff": "Caesar's Mushroom is bright orange with NO white spots (spots wash off in rain on Fly Agaric, but usually present)."
            }
        ],
        "confusion_notes": "☠️ DANGER: The classic fairy tale RED mushroom with WHITE SPOTS. Do NOT eat it, it causes severe delirium and illness. If it has white spots on a red cap, LEAVE IT ALONE."
    },
    {
        "name": "Yellow Stainer",
        "latin_name": "Agaricus xanthodermus",
        "category": "Fungi",
        "months": ["June", "July", "August", "September"],
        "habitat": "Gardens, Grassland, Woods",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Whole mushroom",
        "warnings": "HIGH. Causes severe gastric distress.",
        "description": "**Identification:** Looks like a field mushroom. Cap turns bright yellow when bruised, especially at the base. Smells of carbolic/ink.",
        "id_keys": {
            "Cap": "White/brown, turns bright yellow when rubbed or cut",
            "Stem": "Turns bright chrome yellow at base when cut",
            "Smell": "Unpleasant, chemical, carbolic, or ink-like"
        },
        "danger_tips": {
            "where": "Lawns, grassland, edges of woods.",
            "when": "Summer to Autumn.",
            "sustainable": "Do not pick white mushrooms that stain yellow.",
            "danger_zone": "☠️ HIGH. Severe vomiting, sweating, stomach cramps. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Field mushroom",
                "danger": "EDIBLE",
                "diff": "Field mushroom smells of pleasant mushroom/anise. Yellow Stainer smells chemical/carbolic and turns bright yellow at the base when cut."
            },
            {
                "name": "Horse Mushroom",
                "danger": "EDIBLE",
                "diff": "Horse mushroom bruises slightly yellow but smells of anise. Yellow Stainer stains bright yellow instantly and smells of ink/carbolic."
            }
        ],
        "confusion_notes": "☠️ DANGER: Yellow Stainer stains bright CHROME YELLOW at the base when cut and smells of CARBOLIC/INK. Field mushrooms do NOT stain bright yellow. If it stains yellow, do NOT eat it."
    },
    {
        "name": "Brown Rollrim",
        "latin_name": "Paxillus involutus",
        "category": "Fungi",
        "months": ["July", "August", "September", "October"],
        "habitat": "Woodlands, Heathlands",
        "regions": ["All"],
        "difficulty": 3,
        "parts": "Whole mushroom",
        "warnings": "EXTREME. Can cause fatal autoimmune destruction of red blood cells.",
        "description": "**Identification:** Brown cap with an inrolled rim (rollrim). Gills run down the stem and bruise brown. Funnel-shaped when older.",
        "id_keys": {
            "Cap": "Brown/yellow-brown, inrolled rim (rollrim)",
            "Gills": "Run down stem, bruise brown, close together",
            "Stem": "Solid, brownish"
        },
        "danger_tips": {
            "where": "Broadleaf and coniferous woods.",
            "when": "Summer to Autumn.",
            "sustainable": "Do not eat. Toxins accumulate over time.",
            "danger_zone": "☠️ DEADLY. Destroys red blood cells over time. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Chanterelle",
                "danger": "EDIBLE",
                "diff": "Chanterelle is YELLOW/EGG-YOLK coloured with FORKING ridges (not true gills). Brown Rollrim is BROWN with true gills."
            },
            {
                "name": "Funnel Cap",
                "danger": "EDIBLE/INEDIBLE",
                "diff": "Funnel caps do not have the distinct inrolled rim (rollrim) and gills are not as easily bruised brown."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Brown Rollrim has true gills that bruise BROWN and an inrolled rim on the cap. Chanterelles are golden yellow with blunt FORKING ridges. If it has an inrolled rim, do NOT eat it."
    },
    {
        "name": "Thornapple",
        "latin_name": "Datura stramonium",
        "category": "Plant",
        "months": ["July", "August", "September", "October"],
        "habitat": "Waste ground, Gardens, Arable",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "All parts (especially seeds)",
        "warnings": "EXTREME. Deliriant and toxic. Can be fatal.",
        "description": "**Identification:** Large, trumpet-shaped white/purple flowers. Prickly seed pods (thornapples). Strong unpleasant smell.",
        "id_keys": {
            "Flowers": "Large, white/purple trumpets, 5-lobed",
            "Fruit": "Spiny, egg-shaped seed pod (thornapple)",
            "Smell": "Strong, rank, unpleasant when crushed"
        },
        "danger_tips": {
            "where": "Disturbed ground, warm areas.",
            "when": "Summer to Autumn.",
            "sustainable": "Do not touch or inhale smoke if burning.",
            "danger_zone": "☠️ DEADLY. Intense delirium, amnesia, death. Do NOT consume."
        },
        "lookalikes": [
            {
                "name": "Angels Trumpet",
                "danger": "POISONOUS",
                "diff": "Angels Trumpet flowers hang DOWN. Thornapple flowers point UP or sideways."
            }
        ],
        "confusion_notes": "☠️ DEADLY: Thornapple has large trumpet flowers and SPIKY seed pods (thornapples). Angels Trumpet flowers hang DOWN. Do NOT touch or eat any part of this plant."
    },
    {
        "name": "Ragwort",
        "latin_name": "Senecio jacobaea",
        "category": "Plant",
        "months": ["June", "July", "August", "September"],
        "habitat": "Grassland, Roadsides, Pastures",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "All parts",
        "warnings": "HIGH. Cumulative liver damage (to livestock and humans).",
        "description": "**Identification:** Tall plant with bright yellow daisy-like flowers in flat-topped clusters. Dark green deeply lobed leaves.",
        "id_keys": {
            "Flowers": "Yellow, daisy-like, 13 petals typically",
            "Leaves": "Deeply lobed, ragged appearance",
            "Stem": "Tall, green/purplish"
        },
        "danger_tips": {
            "where": "Pastures, roadsides, wasteland.",
            "when": "Summer.",
            "sustainable": "Control where livestock graze.",
            "danger_zone": "☠️ HIGH. Cumulative liver damage. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "St John's Wort",
                "danger": "EDIBLE/MEDICINAL",
                "diff": "St John's Wort has 5-petalled yellow flowers with black dots. Ragwort has daisy-like flowers (13 petals)."
            },
            {
                "name": "Goldenrod",
                "danger": "EDIBLE",
                "diff": "Goldenrod has tiny yellow flowers on feathery spikes. Ragwort has daisy-like flower heads."
            }
        ],
        "confusion_notes": "☠️ DANGER: Ragwort has daisy-like YELLOW flowers with 13 petals and ragged, lobed leaves. St John's Wort has 5 petals and black dots. Do NOT eat Ragwort."
    },
    {
        "name": "Snowberry",
        "latin_name": "Symphoricarpos albus",
        "category": "Shrub",
        "months": ["August", "September", "October", "November"],
        "habitat": "Hedgerows, Woods",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "MEDIUM. Causes vomiting and dizziness.",
        "description": "**Identification:** Deciduous shrub. Small pinkish-white bell flowers. Distinctive large, white, soft berries that look like snowballs.",
        "id_keys": {
            "Fruit": "Large, white, soft, globe-shaped (like a snowball)",
            "Leaves": "Small, oval, green, opposite",
            "Flowers": "Small pink-white bells"
        },
        "danger_tips": {
            "where": "Hedgerows, thickets, gardens.",
            "when": "Autumn/Winter.",
            "sustainable": "Do not eat the white berries.",
            "danger_zone": "MEDIUM. Vomiting, dizziness. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "SAFE",
                "diff": "No common edible white soft berries in hedgerows. Very distinctive snowball-like berry."
            }
        ],
        "confusion_notes": "Distinctive large, WHITE, soft berries that look like snowballs. No common edible white soft berries in hedgerows. If you see white snowball berries, do NOT eat them."
    },
    {
        "name": "Holly",
        "latin_name": "Ilex aquifolium",
        "category": "Tree",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Woodlands, Gardens, Hedgerows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries",
        "warnings": "MEDIUM to HIGH. Causes severe vomiting.",
        "description": "**Identification:** Evergreen tree. Dark green, glossy, very prickly leaves. Bright red berries in winter.",
        "id_keys": {
            "Leaves": "Dark green, glossy, spiky/prickly edges",
            "Berries": "Bright red, small, in clusters",
            "Bark": "Smooth, grey"
        },
        "danger_tips": {
            "where": "Woods, hedges, gardens.",
            "when": "Berries in Winter.",
            "sustainable": "Admire the berries, do not eat.",
            "danger_zone": "HIGH. Vomiting, diarrhoea, drowsiness. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Spindle",
                "danger": "POISONOUS",
                "diff": "Spindle berries are pink and have orange seeds inside. Holly berries are simple red berries."
            }
        ],
        "confusion_notes": "☠️ DANGER: Red berries with SPIKY evergreen leaves. Do NOT eat the berries. They are not wild strawberries."
    },
    {
        "name": "Ivy",
        "latin_name": "Hedera helix",
        "category": "Plant",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Woodlands, Hedgerows, Gardens",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "Berries, Leaves",
        "warnings": "MEDIUM to HIGH. Skin irritant, toxic berries.",
        "description": "**Identification:** Evergreen climber. Dark green, glossy, 3-5 lobed leaves. Black berries in late winter.",
        "id_keys": {
            "Leaves": "Dark green, glossy, distinct lobes (arrows/stars)",
            "Berries": "Dark purple/black, globular",
            "Growth": "Climbing/trailing woody vine"
        },
        "danger_tips": {
            "where": "Climbing trees, walls, ground cover.",
            "when": "Berries in Winter.",
            "sustainable": "Important for wildlife, do not destroy.",
            "danger_zone": "HIGH. Skin rash from sap, severe stomach upset from berries. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Black Bryony",
                "danger": "POISONOUS",
                "diff": "Black Bryony has heart-shaped leaves and twining stems. Ivy has distinct lobed leaves and woody climbing roots."
            }
        ],
        "confusion_notes": "☠️ DANGER: Common evergreen climber with LOBED leaves and dark purple/black berries. Do NOT eat the berries (irritant)."
    },
    {
        "name": "Bluebell",
        "latin_name": "Hyacinthoides non-scripta",
        "category": "Plant",
        "months": ["April", "May", "June"],
        "habitat": "Woodlands, Hedgerows",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "All parts (especially bulbs)",
        "warnings": "MEDIUM. Causes severe stomach upset.",
        "description": "**Identification:** Iconic spring flower. Violet-blue, bell-shaped flowers that droop/nod on one side of the stem. Distinctive curl-back tips.",
        "id_keys": {
            "Flowers": "Violet-blue, nodding bells, curl-back petals",
            "Leaves": "Long, narrow, strap-like",
            "Smell": "Sweet fragrance"
        },
        "danger_tips": {
            "where": "Ancient woodland, creating blue carpets.",
            "when": "Spring.",
            "sustainable": "Do not pick (protected species). Do not dig bulbs.",
            "danger_zone": "MEDIUM. Nausea, vomiting, low heart rate. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Lily of the Valley",
                "danger": "POISONOUS",
                "diff": "Lily of the Valley has white bell flowers. Bluebell has blue bell flowers."
            },
            {
                "name": "Spanish Bluebell",
                "danger": "MILDLY TOXIC",
                "diff": "Spanish Bluebells are paler blue, upright, and have broader leaves. Native Bluebells are deep violet, droop, and curl back."
            }
        ],
        "confusion_notes": "☠️ DANGER: Bluebell bulbs do NOT smell like ONION. If a bulb doesn't smell of onion, it is NOT an onion. Do NOT eat bluebell bulbs."
    },
    {
        "name": "Bracken",
        "latin_name": "Pteridium aquilinum",
        "category": "Plant",
        "months": ["May", "June", "July", "August", "September"],
        "habitat": "Woodlands, Heathlands, Hillsides",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "All parts (especially fiddleheads)",
        "warnings": "HIGH. Carcinogenic (cancer-causing).",
        "description": "**Identification:** Large, coarse fern. Triangular fronds that turn rusty brown in autumn. Fiddleheads (crosiers) are hairy and not downy.",
        "id_keys": {
            "Fronds": "Large, triangular, 3 times divided",
            "Fiddleheads": "Hairy, emerge from ground in spring",
            "Colour": "Turns rusty brown in autumn"
        },
        "danger_tips": {
            "where": "Dominates heathlands, hillsides, and woodland edges.",
            "when": "Spring (fiddleheads) to Autumn.",
            "sustainable": "Do not eat fiddleheads or use as bedding.",
            "danger_zone": "☠️ HIGH. Carcinogenic (cancer-causing). Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Ostrich Fern",
                "danger": "EDIBLE",
                "diff": "Ostrich Fern fiddleheads are smooth and have a groove on the stem. Bracken fiddleheads are hairy."
            },
            {
                "name": "Lady Fern",
                "danger": "INEDIBLE",
                "diff": "Lady Fern is more delicate and lacy. Bracken is coarse and large."
            }
        ],
        "confusion_notes": "☠️ DANGER: Bracken fiddleheads are HAIRY. Edible Ostrich Fern fiddleheads are SMOOTH with a groove. If the fiddlehead is hairy, do NOT eat it."
    },
    {
        "name": "Buttercup",
        "latin_name": "Ranunculus species",
        "category": "Plant",
        "months": ["May", "June", "July", "August"],
        "habitat": "Meadows, Gardens, Grassland",
        "regions": ["All"],
        "difficulty": 1,
        "parts": "All parts",
        "warnings": "MEDIUM. Causes blistering and stomach upset.",
        "description": "**Identification:** Glossy yellow cup-shaped flowers. Deeply lobed leaves. Sap is acrid and blistering.",
        "id_keys": {
            "Flowers": "Glossy yellow, 5 petals, cup-shaped",
            "Leaves": "Deeply lobed or cut, hairy",
            "Sap": "Acrid, causes blistering on skin"
        },
        "danger_tips": {
            "where": "Lawns, meadows, wet ground.",
            "when": "Spring and Summer.",
            "sustainable": "Do not eat. Drying destroys the toxin.",
            "danger_zone": "MEDIUM. Blisters in mouth, stomach cramps. Do NOT eat."
        },
        "lookalikes": [
            {
                "name": "Lesser Celandine",
                "danger": "EDIBLE (Roots/Leaves cooked)",
                "diff": "Lesser Celandine has 8-12 petals and is a low-growing plant. Buttercup has exactly 5 petals and is taller."
            }
        ],
        "confusion_notes": "☠️ DANGER: Buttercups have GLOSSY yellow flowers with exactly 5 petals. Lesser Celandine has 8-12 petals. Do NOT eat fresh buttercups, they burn the mouth."
    },
    {
        "name": "Spurge",
        "latin_name": "Euphorbia species",
        "category": "Plant",
        "months": ["April", "May", "June", "July", "August"],
        "habitat": "Gardens, Woodlands, Waste ground",
        "regions": ["All"],
        "difficulty": 2,
        "parts": "Sap (All parts)",
        "warnings": "HIGH. Sap is severely irritant and can cause blindness.",
        "description": "**Identification:** Variable plant. Green/yellow flowers (cyathia). Leaves are alternate or whorled. The key ID is the milky white sap when cut.",
        "id_keys": {
            "Sap": "Milky white sap that flows when cut",
            "Flowers": "Inconspicuous green/yellow, cup-like",
            "Leaves": "Often blue-green, alternate"
        },
        "danger_tips": {
            "where": "Gardens, waste ground, woods.",
            "when": "Spring and Summer.",
            "sustainable": "Do not break stems. Wash hands if sap contacts skin.",
            "danger_zone": "☠️ HIGH. Skin blistering, eye damage. Do NOT touch the sap."
        },
        "lookalikes": [
            {
                "name": "Dog's Mercury",
                "danger": "POISONOUS",
                "diff": "Dog's Mercury does not produce milky white sap. Spurge always exudes white sap when cut."
            }
        ],
        "confusion_notes": "☠️ DANGER: If a plant exudes MILKY WHITE SAP when cut, it is likely Spurge and highly toxic. Do NOT touch the sap, it can cause BLINDNESS."
    }
]
}
