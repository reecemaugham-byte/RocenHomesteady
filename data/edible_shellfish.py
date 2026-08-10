# edible_shellfish.py — Edible shellfish data for Rocen Homesteady
# 30 entries

EDIBLE_SHELLFISH = [
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
        "name": "Winkles",
        "latin_name": "Littorina littorea",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Rocky shores, harbour walls, pier pilings, stony beaches",
        "regions": ["Coastal", "All"],
        "difficulty": 1,
        "parts": "Whole animal (boiled and picked from shell)",
        "warnings": "⚠️ Only collect from clean water sites. Check FSA and local advisories for algal toxins and pollution. Must be purged (soaked in clean salt water) for several hours before cooking. Cook thoroughly — boil for at least 5 minutes. Do not collect after heavy rain near sewage outfalls.",
        "description": "**Identification:** Small, dark grey-black spiral shell, 2-3cm tall. Pointed cone shape with distinct whorls. Dark operculum (trap door) seals the shell when closed. Found in large clusters on rocks and harbour walls. **Uses:** Boil in salted water for 5+ minutes. Pick from shell with a pin or toothpick. Eat with vinegar, pepper, or dipped in butter. Classic British seaside food.",
        "id_keys": {
            "Shell": "Dark grey-black, 2-3cm tall, pointed conical spiral with distinct whorls",
            "Operculum": "Hard dark 'trap door' that seals the shell opening when retracted",
            "Size": "2-3cm — small, no danger of confusing with larger dangerous species",
            "Position": "Found in clusters on rocks, harbour walls, and stony beaches"
        },
        "foraging_tips": {
            "where": "Rocky shores, harbour walls, piers, and stony beaches above the low tide line",
            "when": "Autumn to spring (September to April) — best in cooler months",
            "sustainable": "Take only what you will eat. Leave small winkles and avoid stripping areas. Follow local byelaws on minimum sizes",
            "danger_zone": "⚠️ Check FSA shellfish warnings. Purge in clean salt water for 3-4 hours before cooking. Boil for at least 5 minutes"
        },
        "lookalikes": [
            {
                "name": "Dog Whelks (Nucella lapillus)",
                "danger": "EDIBLE",
                "diff": "Dog whelks are larger with a thicker shell and shorter spire. Winkles are small, thinner-shelled, and more pointed. Both are technically edible but dog whelks taste bitter"
            },
            {
                "name": "Topshells (Gibbula spp.)",
                "danger": "EDIBLE",
                "diff": "Topshells are more rounded and dome-shaped with colourful patterns; winkles are darker and more pointed"
            }
        ],
        "confusion_notes": "Winkles are one of the safest shellfish to identify — small, pointed, dark, and found in clusters. Most similar-looking snails are also edible. The main risk is water quality, not identification."
    },
    {
        "name": "Whelks",
        "latin_name": "Buccinum undatum",
        "category": "Shellfish",
        "months": ["October", "November", "December", "January", "February", "March", "April", "May"],
        "habitat": "Sandy and muddy seabed, subtidal, often found washed up on beaches after storms",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal (boiled and shelled)",
        "warnings": "⚠️ Only collect from clean water sites. Check FSA advisories for algal toxins. Cook thoroughly — boil for at least 8-10 minutes. May accumulate toxins. Only collect live ones (shell tightly closed or operculum responds to touch).",
        "description": "**Identification:** Large, thick, pale grey-buff spiral shell, 6-11cm tall. Distinctively sculptured with ridges. Shell opening has a wide, oval lip. Soft body with a large foot and siphon. Often found in fish markets. **Uses:** Boil for 8-10 minutes in salted water. Remove from shell. Can be eaten with vinegar and pepper, or used in stews, chowders, and stir-fries. Firm, chewy texture with strong sea flavour.",
        "id_keys": {
            "Shell": "Large, thick, pale grey-buff, 6-11cm, with strong spiral ridges",
            "Shape": "Pointed spiral with a wide oval opening at the base",
            "Size": "6-11cm — significantly larger than winkles",
            "Live test": "Live whelks have an operculum (trap door) that responds to touch"
        },
        "foraging_tips": {
            "where": "Subtidal — often caught in pots or found washed ashore after storms. Check tide lines for fresh shells",
            "when": "Autumn to spring — best in cooler months",
            "sustainable": "Minimum size ~45mm shell height. Only take what you will eat. Whelk populations can be overfished",
            "danger_zone": "⚠️ Check FSA shellfish warnings. Cook thoroughly. Only eat live specimens that respond to touch"
        },
        "lookalikes": [
            {
                "name": "Dog Whelk (Nucella lapillus)",
                "danger": "EDIBLE",
                "diff": "Dog Whelks are smaller (3-5cm), thicker-shelled, and feed on barnacles and mussels. Not recommended as food due to bitter taste"
            },
            {
                "name": "Netted Dog Whelk (Hinia reticulata)",
                "danger": "EDIBLE",
                "diff": "Smaller, more delicate shell with net-like pattern. Not traditionally eaten"
            }
        ],
        "confusion_notes": "Common Whelks are large and distinctive. The main concern is water quality and thorough cooking, not identification confusion."
    },
    {
        "name": "Prawns",
        "latin_name": "Palaemon serratus",
        "category": "Shellfish",
        "months": ["May", "June", "July", "August", "September", "October"],
        "habitat": "Rock pools, seagrass beds, shallow coastal waters, harbour walls",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal (head and tail), or peeled tail meat",
        "warnings": "⚠️ Check water quality before collecting. Only collect from clean water. Some people are allergic to crustaceans — prawns are a common allergen. Cook thoroughly if eating raw-caught. Be aware of algal bloom warnings.",
        "description": "**Identification:** Semi-transparent body with greyish-blue stripes and orange spots on the tail. Long rostrum (beak) with teeth. Large claws on front legs. 5-11cm long. Found in rock pools and shallow water. Swims backwards with rapid tail flips. **Uses:** Boil for 2-3 minutes until pink. Can be eaten whole (head-on) or peeled. Excellent in sandwiches, pasta, stir-fries, or simply with lemon and mayonnaise.",
        "id_keys": {
            "Body": "Semi-transparent, greyish with subtle blue stripes and orange tail spots",
            "Rostrum": "Long pointed beak (rostrum) extending forward from between the eyes, with teeth along the upper edge",
            "Size": "5-11cm — larger than shrimp species",
            "Behaviour": "Found in rock pools; swims backwards rapidly when disturbed"
        },
        "foraging_tips": {
            "where": "Rock pools, shallow coastal water, harbour walls, seagrass beds — especially around low tide",
            "when": "May to October — best in summer months when they come inshore",
            "sustainable": "Use a push net or hand net. Return small prawns and egg-carrying females. Follow local byelaws",
            "danger_zone": "⚠️ Check for algal bloom warnings. Allergen risk for some people. Cook thoroughly"
        },
        "lookalikes": [
            {
                "name": "Brown Shrimp (Crangon crangon)",
                "danger": "EDIBLE",
                "diff": "Brown Shrimp is flatter, more mottled brown, smaller, and lacks the long rostrum. Both are edible"
            }
        ],
        "confusion_notes": "Prawns are easy to identify by their long rostrum and semi-transparent body. All UK prawn and shrimp species are edible. The main risks are water quality and shellfish allergies."
    },
    {
        "name": "Edible Crab",
        "latin_name": "Cancer pagurus",
        "category": "Shellfish",
        "months": ["April", "May", "June", "July", "August", "September", "October", "November"],
        "habitat": "Rocky seabed, under large boulders on the lower shore, subtidal",
        "regions": ["Coastal", "All"],
        "difficulty": 3,
        "parts": "White meat (claws and body), brown meat (inside shell)",
        "warnings": "⚠️ ONLY collect from clean water sites. Check FSA advisories. Pinchers can cause painful injury — handle carefully. Must be cooked thoroughly. Do NOT collect berried (egg-carrying) females. Follow local byelaws for minimum sizes (usually 140mm carapace width). Allergen risk for shellfish.",
        "description": "**Identification:** Large, heavy crab with a distinctive pie-crust edge on the oval shell. Red-brown to orange-brown shell with white-tipped massive claws. Shell width up to 25cm. Found under rocks and in crevices on the lower shore. **Uses:** Boil for 15-20 minutes in well-salted water. Crack claws and extract white meat. Brown meat from inside the shell is a delicacy. Use in sandwiches, crab cakes, pasta, or simply with lemon.",
        "id_keys": {
            "Shell": "Oval, red-brown to orange-brown, with a distinctive crinkled 'pie-crust' edge",
            "Claws": "Massive, black-tipped claws — the main source of white meat",
            "Size": "Shell width up to 25cm — the largest common UK shore crab",
            "Colour": "Red-brown to orange-brown shell, white underside"
        },
        "foraging_tips": {
            "where": "Under large boulders and in crevices on the lower rocky shore, or subtidal in pots",
            "when": "April to November — best in late spring and summer",
            "sustainable": "Minimum carapace width 140mm. Never take berried females (egg-carrying). Follow local byelaws. Return undersized crabs",
            "danger_zone": "⚠️ Claws can cause serious pinch injuries. Handle from the rear. Never collect berried females. Check FSA warnings"
        },
        "lookalikes": [
            {
                "name": "Velvet Swimming Crab (Necora puber)",
                "danger": "EDIBLE",
                "diff": "Velvet Crab is smaller, has red eyes, flat paddle-like rear legs, and a velvety shell texture. Edible but less meat"
            },
            {
                "name": "Shore Crab (Carcinus maenas)",
                "danger": "EDIBLE",
                "diff": "Shore Crab is smaller, green-grey, with five teeth behind each eye. Edible but very little meat"
            }
        ],
        "confusion_notes": "The Edible Crab is unmistakable with its large size, pie-crust shell edge, and massive black-tipped claws. The main concern is safe handling and legal size limits, not identification."
    },
    {
        "name": "Razor Clams",
        "latin_name": "Ensis spp.",
        "category": "Shellfish",
        "months": ["June", "July", "August", "September", "October"],
        "habitat": "Sandy beaches, buried deep in sand between low and high tide marks",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal (foot and body meat)",
        "warnings": "⚠️ CRITICAL: Only collect from Class A waters. Check FSA shellfish classification for your area. Razor clams can accumulate toxins and biotoxins. Purge in clean salt water for 12-24 hours before cooking. Cook thoroughly. Do NOT collect from unclassified waters.",
        "description": "**Identification:** Long, thin, straight-edged shell resembling an old-fashioned cut-throat razor. Up to 20cm long. Shiny olive-brown periostracum (skin) on shell. Keyhole-shaped openings visible in the sand at low tide. Lives buried vertically deep in sand. **Uses:** Steam or boil for 3-5 minutes. Can also be grilled with garlic butter. Sweet, tender meat. Popular in Spanish and Portuguese cuisine.",
        "id_keys": {
            "Shell": "Long, thin, straight-edged — like an old cut-throat razor blade. Up to 20cm",
            "Colour": "White/cream shell with olive-brown shiny outer skin (periostracum)",
            "Sand sign": "Keyhole-shaped or figure-of-eight openings visible in wet sand at low tide",
            "Depth": "Buried 30-60cm deep in sand — requires digging or salting to extract"
        },
        "foraging_tips": {
            "where": "Sandy beaches — look for keyhole openings in the sand at low tide",
            "when": "June to October, during low spring tides for best access",
            "sustainable": "Pour salt down the hole to make them rise up — more sustainable than digging. Only take what you will eat. Follow local byelaws",
            "danger_zone": "⚠️ CRITICAL: Only collect from classified waters (check FSA). Purge 12-24 hours in clean salt water. Cook thoroughly. Toxin risk is real"
        },
        "lookalikes": [
            {
                "name": "Pod Razor (Ensis siliqua)",
                "danger": "EDIBLE",
                "diff": "Pod Razor is slightly longer and more curved. Both Ensis species are edible"
            },
            {
                "name": "Jackknife Clam (Ensis ensis)",
                "danger": "EDIBLE",
                "diff": "Slightly curved shell. All UK razor clam species are edible"
            }
        ],
        "confusion_notes": "All UK razor clam species (Ensis spp.) are edible. The main risk is NOT identification — it's water quality and biotoxin accumulation. Only collect from classified and monitored waters."
    },
    {
        "name": "Oysters",
        "latin_name": "Ostrea edulis / Magallana gigas",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Estuaries, sheltered bays, oyster beds, subtidal",
        "regions": ["Coastal", "All"],
        "difficulty": 3,
        "parts": "Whole animal (meat and liquor inside shell)",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Check FSA shellfish classification. Raw oysters carry risk of norovirus and Vibrio bacteria. People with liver conditions, weakened immune systems, or pregnant women should avoid raw oysters. Purge and cook if in any doubt. Follow local byelaws — many areas are protected.",
        "description": "**Identification:** Native Oyster: round, flat shell, grey-white, 6-11cm. Pacific Oyster: larger (8-20cm), elongated, deeply cupped lower shell, rough with flaky layers. Both found on oyster beds, reefs, and estuary beds. **Uses:** Native oysters are traditionally eaten raw with lemon. Pacific oysters can be eaten raw, grilled, baked, or used in stews. Rich, distinctive flavour.",
        "id_keys": {
            "Native Oyster": "Round, flat, grey-white shell, 6-11cm. Smaller and flatter than Pacific",
            "Pacific Oyster": "Larger (8-20cm), elongated, deeply cupped lower shell, rough flaky layers. Much more common",
            "Live test": "Shell should be tightly closed. Tap open shells — live oysters will close",
            "Habitat": "Estuary beds, sheltered bays, oyster reefs"
        },
        "foraging_tips": {
            "where": "Estuary beds, sheltered bays, and designated oyster grounds — check local permissions",
            "when": "September to April (traditionally only in months with an 'R'). Avoid spawning season (May-August)",
            "sustainable": "Follow local byelaws strictly. Many areas require permits. Return undersized oysters. Never take from protected beds",
            "danger_zone": "⚠️ CRITICAL: Only from classified Class A waters. Raw oysters carry real health risks for vulnerable groups. Check FSA classification"
        },
        "lookalikes": [
            {
                "name": "Pacific Oyster (Magallana gigas)",
                "danger": "EDIBLE",
                "diff": "Larger, more elongated, deeper cupped shell with rough flaky layers. Both species are edible"
            }
        ],
        "confusion_notes": "The main risk with oysters is water quality and food safety, NOT identification. Both UK species are edible. Only collect from classified and monitored waters."
    },
    {
        "name": "Scallops",
        "latin_name": "Pecten maximus",
        "category": "Shellfish",
        "months": ["November", "December", "January", "February", "March", "April", "May"],
        "habitat": "Sandy and gravelly seabed, subtidal (5-50m depth)",
        "regions": ["Coastal", "All"],
        "difficulty": 3,
        "parts": "White adductor muscle and orange roe (coral)",
        "warnings": "⚠️ Check FSA classifications before collecting. Dive-caught only (no dredging for foragers). Must be collected from clean waters. People with shellfish allergies should avoid. Cook thoroughly unless from Class A waters.",
        "description": "**Identification:** King Scallop: large (10-15cm), fan-shaped shell with distinct radiating ribs. Upper shell flat, lower shell deeply cupped. Orange roe (coral) and large white adductor muscle inside. Can swim by clapping shells together. **Uses:** Pan-fry the white muscle for 1-2 minutes each side. Roe (coral) is also edible. Wrap in bacon, serve with black pudding, or use in chowder.",
        "id_keys": {
            "Shell": "Fan-shaped, 10-15cm, with distinct radiating ribs. Lower shell is deeply cupped, upper is flat",
            "Colours": "Shell is white/cream to light brown outside. Inside: white adductor muscle and orange roe (coral)",
            "Swimming": "Live scallops can swim by clapping their shells — a distinctive behaviour",
            "Size": "King Scallops 10-15cm; Queen Scallops smaller at 5-8cm"
        },
        "foraging_tips": {
            "where": "Sandy and gravelly seabed — usually requires diving. Found subtidal at 5-50m depth",
            "when": "November to May — closed season during summer spawning months",
            "sustainable": "Minimum size 100mm for King Scallops. Dive-caught only. Do not use dredges. Follow local byelaws",
            "danger_zone": "⚠️ Requires diving to collect. Check FSA water classifications. Never collect from unclassified waters"
        },
        "lookalikes": [
            {
                "name": "Queen Scallop (Aequipecten opercularis)",
                "danger": "EDIBLE",
                "diff": "Smaller (5-8cm), more symmetrical shells, both valves slightly cupped. Equally edible"
            }
        ],
        "confusion_notes": "Scallops are easy to identify by their fan-shaped ribbed shells. The main considerations are diving safety and water quality classification, not identification."
    },
    {
        "name": "Brown Shrimp",
        "latin_name": "Crangon crangon",
        "category": "Shellfish",
        "months": ["May", "June", "July", "August", "September", "October"],
        "habitat": "Sandy seabed, shallow coastal waters, estuaries, intertidal sand flats",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole shrimp (peeled tail meat)",
        "warnings": "⚠️ Only collect from clean water sites. Check FSA advisories. Cook thoroughly. Shellfish allergen risk. Brown shrimps are small and labour-intensive to peel.",
        "description": "**Identification:** Small, flat, mottled brown-grey shrimp, 3-5cm long. Short, flattened body. No long rostrum (unlike prawns). Blends into sand. Found burrowed in sand in shallow water. **Uses:** Boil for 3-5 minutes in salted water. Peel (labour-intensive). Used in potted shrimp, sandwiches, and as a topping. Classic English seaside food, especially in Morecambe Bay.",
        "id_keys": {
            "Body": "Small (3-5cm), flat, mottled brown-grey — perfectly camouflaged on sand",
            "Shape": "Flatter and broader than prawns, no long rostrum",
            "Behaviour": "Buries in sand with only eyes visible; swims short distances when disturbed",
            "Habitat": "Shallow sandy water, estuaries, sand flats"
        },
        "foraging_tips": {
            "where": "Sandy shallows, estuaries, and sand flats — push net through shallow water",
            "when": "May to October — best in summer",
            "sustainable": "Use a push net. Return small shrimp and egg-carrying females. Follow local byelaws",
            "danger_zone": "⚠️ Check water quality advisories. Cook thoroughly. Shellfish allergen risk"
        },
        "lookalikes": [
            {
                "name": "Prawns (Palaemon serratus)",
                "danger": "EDIBLE",
                "diff": "Prawns are larger, semi-transparent with blue stripes and a long rostrum; Brown Shrimp is small, brown, flat, and mottled"
            }
        ],
        "confusion_notes": "Brown Shrimp is easy to identify — small, brown, flat, and sandy. All UK shrimp and prawn species are edible. Water quality is the main concern."
    },
    {
        "name": "Mussels",
        "latin_name": "Mytilus edulis",
        "category": "Shellfish",
        "months": ["September", "October", "November", "January", "February", "March", "April"],
        "habitat": "Coastal Rocks, Estuaries",
        "regions": ["Coastal"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "Must be from clean water. Check for red tide warnings. Cook thoroughly. Only collect in months with an 'R'.",
        "description": "**Identification:** Dark blue/black bivalve shell. Elongated, pointed at one end. Grows in dense clusters on rocks and piers.",
        "id_keys": {
            "Shell": "Dark blue/black, elongated, pointed at one end",
            "Habitat": "Dense clusters on rocks, piers, ropes",
            "Size": "5-10cm long"
        },
        "foraging_tips": {
            "where": "Rocks, piers, ropes in clean water.",
            "when": "Months with an 'R' (Sept-Apr). Avoid summer.",
            "sustainable": "Only take sizes over 5cm. Pull from rocks carefully.",
            "danger_zone": "CRITICAL: Check water quality and red tide warnings. Cook thoroughly."
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "EDIBLE",
                "diff": "Mussels are distinctive. No dangerous shellfish look like mussels in the UK."
            }
        ],
        "confusion_notes": "Safe from clean water. Only collect in months with an 'R'. Check for red tide warnings. Cook thoroughly."
    },
    {
        "name": "Lobster",
        "latin_name": "Homarus gammarus",
        "category": "Shellfish",
        "months": ["April", "May", "June", "July", "August", "September", "October"],
        "habitat": "Rocky seabed, crevices, subtidal",
        "regions": ["Coastal", "All"],
        "difficulty": 3,
        "parts": "Tail meat, claw meat, body meat",
        "warnings": "⚠️ Must be from clean water. Check FSA advisories. Heavy claws can cause serious injury. Follow local byelaws for minimum sizes (87mm carapace). Do NOT collect berried (egg-carrying) females. Allergen risk for shellfish.",
        "description": "**Identification:** Large, blue-black to dark blue-green crustacean with two massive claws — one crusher (broader) and one cutter (narrower). Long antennae. Turns bright red when cooked. Carapace length up to 20cm, total length up to 60cm. **Uses:** Boil for 15-20 minutes per kg. Crack claws and extract meat. Tail meat is the prime cut. Serve with melted butter, lemon, or in rolls.",
        "id_keys": {
            "Colour": "Blue-black to dark blue-green when alive (bright red when cooked)",
            "Claws": "Two massive claws — one broad crusher, one narrow cutter",
            "Antennae": "Long, thick antennae",
            "Size": "Carapace up to 20cm, total length up to 60cm"
        },
        "foraging_tips": {
            "where": "Rocky seabed and crevices — requires diving or pots. Found subtidal",
            "when": "April to October — best in summer months",
            "sustainable": "Minimum carapace 87mm. NEVER take berried females (egg-carrying). V-notch laws apply in some areas. Return undersized lobsters",
            "danger_zone": "⚠️ Claws can cause serious injury. Handle from the rear. Follow local byelaws strictly. Check FSA water quality"
        },
        "lookalikes": [
            {
                "name": "Crawfish (Spiny Lobster)",
                "danger": "EDIBLE",
                "diff": "Crawfish has NO large claws, a spiny body, and long thick antennae. Lobster has two massive claws"
            }
        ],
        "confusion_notes": "Lobsters are unmistakable with their massive claws and blue-black colour. The main concerns are legal size limits and not taking berried females, not identification."
    },
    {
        "name": "Crawfish (Spiny Lobster)",
        "latin_name": "Palinurus elephas",
        "category": "Shellfish",
        "months": ["June", "July", "August", "September", "October"],
        "habitat": "Rocky seabed, subtidal (10-70m depth), mainly SW England and Wales",
        "regions": ["Coastal", "Southwest", "Wales"],
        "difficulty": 3,
        "parts": "Tail meat",
        "warnings": "⚠️ Only collect from clean water. Dive-caught only. Follow local byelaws for minimum sizes. Do NOT collect berried females. Allergen risk for shellfish.",
        "description": "**Identification:** Large, red-brown crustacean with NO large claws. Spiny body and legs. Very long, thick antennae. Prominent supra-orbital horns above the eyes. Turns deeper red when cooked. **Uses:** Boil or steam for 10-15 minutes. Meat is in the tail only. Sweet, firm, lobster-like flavour. Popular in Mediterranean cuisine.",
        "id_keys": {
            "Claws": "NO large claws — this is the KEY difference from lobster",
            "Body": "Spiny, rough, covered in small spines and tubercles",
            "Antennae": "Very long, thick antennae extending well beyond the body",
            "Horns": "Prominent horns above the eyes (supra-orbital horns)"
        },
        "foraging_tips": {
            "where": "Rocky seabed, 10-70m depth. Mainly SW England, Wales, and Scotland. Requires diving",
            "when": "June to October",
            "sustainable": "Minimum carapace length 95mm (varies by region). NEVER take berried females. Follow local byelaws. Dive-caught only",
            "danger_zone": "⚠️ Requires diving to collect. Check FSA water classifications. Follow all local byelaws"
        },
        "lookalikes": [
            {
                "name": "Common Lobster (Homarus gammarus)",
                "danger": "EDIBLE",
                "diff": "Common Lobster has TWO MASSIVE CLAWS. Crawfish has NO large claws and a spiny body"
            }
        ],
        "confusion_notes": "Crawfish (Spiny Lobster) has NO large claws and a spiny body. Common Lobster has two massive claws. Very easy to tell apart."
    },
    {
        "name": "Langoustine (Dublin Bay Prawn)",
        "latin_name": "Nephrops norvegicus",
        "category": "Shellfish",
        "months": ["January", "February", "March", "April", "May", "June", "October", "November", "December"],
        "habitat": "Muddy seabed, subtidal (20-800m depth), burrows in soft mud",
        "regions": ["Coastal", "All"],
        "difficulty": 3,
        "parts": "Tail meat, claws (small amount)",
        "warnings": "⚠️ Check FSA advisories for water quality. Typically caught in pots or trawled — foraging requires diving or pots. Allergen risk for shellfish. Cook thoroughly.",
        "description": "**Identification:** Long, slim, pink-orange crustacean. Large, slender claws with ridges. Two long claws of similar size. Body is thinner and longer than a lobster. Pink-orange colour even when raw. 10-25cm total length. **Uses:** Boil for 2-3 minutes, or grill with garlic butter. Tail meat is sweet and delicate. Classic in risotto, pasta, or simply with lemon and mayonnaise.",
        "id_keys": {
            "Colour": "Pink-orange even when alive (unlike lobster which is blue-black alive)",
            "Claws": "Two long, slender, ridged claws of similar size",
            "Body": "Slim, elongated body — thinner than lobster",
            "Size": "10-25cm total length"
        },
        "foraging_tips": {
            "where": "Muddy seabed, subtidal. Requires pots or diving. More commonly bought from fishmongers",
            "when": "Avoid summer months (spawning season). Best October to May",
            "sustainable": "Check MSC certification. Follow local byelaws. Minimum landing size applies",
            "danger_zone": "⚠️ Typically a commercial species. Foraging requires specialist equipment. Check FSA water quality"
        },
        "lookalikes": [
            {
                "name": "Common Lobster",
                "danger": "EDIBLE",
                "diff": "Lobster is blue-black when alive, much larger, with one massive crusher claw. Langoustine is pink-orange, slim, with two slender equal claws"
            },
            {
                "name": "Squat Lobster",
                "danger": "EDIBLE",
                "diff": "Squat Lobster is much smaller (3-5cm), flatter, and found under rocks in rock pools. Langoustine is larger and lives in deep mud"
            }
        ],
        "confusion_notes": "Langoustine is pink-orange when alive, slim, with two slender equal claws. Not easily confused with other UK shellfish."
    },
    {
        "name": "Velvet Swimming Crab",
        "latin_name": "Necora puber",
        "category": "Shellfish",
        "months": ["May", "June", "July", "August", "September", "October"],
        "habitat": "Rocky shores, under stones, rock pools, subtidal",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "White meat (claws and body)",
        "warnings": "⚠️ Fast and aggressive — will pinch. Handle with care. Only collect from clean water. Cook thoroughly. Less meat than Edible Crab. Allergen risk.",
        "description": "**Identification:** Medium crab, 6-9cm shell width. Distinctive RED EYES. Velvety texture on shell and legs. Rear legs are flattened paddles for swimming. Dark blue-green shell with velvety feel. Very fast and aggressive when handled. **Uses:** Boil for 10-12 minutes in salted water. Less meat than Edible Crab but sweet and flavourful. Use in soups, bisques, or picked for meat.",
        "id_keys": {
            "Eyes": "RED EYES — the most distinctive feature",
            "Texture": "Velvety feel on shell and legs (hence the name)",
            "Rear_legs": "Flattened paddle-like rear legs for swimming",
            "Colour": "Dark blue-green shell, lighter underneath"
        },
        "foraging_tips": {
            "where": "Under stones and in crevices on the lower rocky shore, and in rock pools",
            "when": "May to October — best in warmer months",
            "sustainable": "Return undersized crabs (minimum 65mm in some areas). Check local byelaws. They are fast — catch quickly",
            "danger_zone": "⚠️ Very fast and aggressive. Will pinch. Handle with thick gloves from the rear. Cook thoroughly"
        },
        "lookalikes": [
            {
                "name": "Edible Crab (Cancer pagurus)",
                "danger": "EDIBLE",
                "diff": "Edible Crab is MUCH LARGER, has a pie-crust shell edge, and white-tipped claws. Velvet Crab has RED EYES, velvety texture, and swimming paddles"
            },
            {
                "name": "Shore Crab (Carcinus maenas)",
                "danger": "EDIBLE",
                "diff": "Shore Crab is green-grey, lacks red eyes and swimming paddles. Velvet Crab has RED EYES and flattened swimming legs"
            }
        ],
        "confusion_notes": "Velvet Swimming Crab is easy to identify by its RED EYES and velvety shell texture. Less meat than Edible Crab but still worthwhile."
    },
    {
        "name": "Shore Crab (Green Crab)",
        "latin_name": "Carcinus maenas",
        "category": "Shellfish",
        "months": ["April", "May", "June", "July", "August", "September", "October"],
        "habitat": "Rocky shores, estuaries, mud flats, harbours, under seaweed",
        "regions": ["Coastal", "All"],
        "difficulty": 1,
        "parts": "White meat (small amount from claws and body)",
        "warnings": "⚠️ Can pinch. Only collect from clean water. Cook thoroughly. Very little meat per crab — best for stock/bisque. Allergen risk.",
        "description": "**Identification:** Small crab, 3-6cm shell width. Green to dark green-grey shell. Five distinct teeth behind each eye. Variable colour — can be green, orange, or red. Very common on all UK shores. **Uses:** Best used for crab stock, bisque, or soup rather than picking for meat — very little meat per crab. Boil for 8-10 minutes. Makes excellent fish stock.",
        "id_keys": {
            "Shell": "Green to dark grey-green, 3-6cm wide",
            "Teeth": "Five distinct sharp teeth behind each eye — KEY feature",
            "Colour": "Variable — green, orange, or red depending on age and habitat",
            "Size": "Small — 3-6cm shell width"
        },
        "foraging_tips": {
            "where": "Under seaweed, stones, and in rock pools. Very common on all UK shores",
            "when": "April to October",
            "sustainable": "Very common. Take only what you need. Return undersized crabs. Check local byelaws",
            "danger_zone": "⚠️ Can pinch but small enough to handle safely. Best for stock/bisque rather than meat. Cook thoroughly"
        },
        "lookalikes": [
            {
                "name": "Edible Crab (Cancer pagurus)",
                "danger": "EDIBLE",
                "diff": "Edible Crab is MUCH LARGER, has a pie-crust edge and black-tipped claws. Shore Crab is small, green-grey, with no pie-crust edge"
            }
        ],
        "confusion_notes": "Shore Crab is small, green-grey, with five teeth behind each eye. Very common. Best used for stock rather than picking for meat."
    },
    {
        "name": "Spider Crab",
        "latin_name": "Maja squinado",
        "category": "Shellfish",
        "months": ["April", "May", "June", "July", "August", "September"],
        "habitat": "Rocky seabed, subtidal, shallow kelp beds, sometimes in rock pools",
        "regions": ["Coastal", "Southern", "Southwest", "Wales"],
        "difficulty": 3,
        "parts": "White meat (legs and body)",
        "warnings": "⚠️ Long, spiny legs can cause scratches. Only collect from clean water. Cook thoroughly. Allergen risk. Do NOT collect berried females.",
        "description": "**Identification:** Large, spiny crab with very long, thin legs. Shell (carapace) 8-20cm, spiny and rough. Distinctive pointed snout between the eyes. Reddish-brown to yellowish. Long legs span up to 50cm. **Uses:** Boil for 15-20 minutes in salted water. Sweet, delicate meat from legs and body. Excellent in soups, risottos, or picked for white meat.",
        "id_keys": {
            "Legs": "Very long, thin, spiny legs — span up to 50cm — the most distinctive feature",
            "Shell": "Spiny, rough, reddish-brown, 8-20cm, with a pointed snout between the eyes",
            "Size": "Shell 8-20cm, leg span up to 50cm",
            "Snout": "Distinctive pointed snout between the eyes"
        },
        "foraging_tips": {
            "where": "Rocky seabed and kelp beds, subtidal. Occasionally found in deep rock pools. Mainly SW England and Wales",
            "when": "April to September — they migrate inshore in summer",
            "sustainable": "Minimum carapace size 120mm (varies). NEVER take berried females. Follow local byelaws",
            "danger_zone": "⚠️ Long spiny legs can scratch. Handle with gloves. Cook thoroughly. Check FSA water quality"
        },
        "lookalikes": [
            {
                "name": "Edible Crab (Cancer pagurus)",
                "danger": "EDIBLE",
                "diff": "Edible Crab has short, thick legs, massive claws, and a pie-crust shell edge. Spider Crab has VERY LONG, THIN, spiny legs and a pointed snout"
            }
        ],
        "confusion_notes": "Spider Crab is unmistakable with its very long, thin, spiny legs and pointed snout between the eyes. Very different from other UK crabs."
    },
    {
        "name": "Palourde Clam (Carpet Shell)",
        "latin_name": "Venerupis decussata / Venerupis philippinarum",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Sandy and muddy estuaries, sheltered bays, burrowed just below surface",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Check FSA shellfish classification. Purge in clean salt water for 12-24 hours before cooking. Cook thoroughly. Do NOT collect from unclassified waters.",
        "description": "**Identification:** Oval, thick shell with concentric ridges and radiating lines creating a cross-hatch pattern. 4-7cm. Cream to grey-white shell. Found buried just below the sand/mud surface in estuaries. **Uses:** Steam for 3-5 minutes until shells open. Discard any that don't open. Classic in pasta, risotto, or simply steamed with white wine, garlic, and parsley.",
        "id_keys": {
            "Shell": "Oval, thick, 4-7cm, with both concentric ridges AND radiating lines (cross-hatch pattern)",
            "Colour": "Cream to grey-white, sometimes with darker markings",
            "Habitat": "Buried just below surface in sandy/muddy estuaries",
            "Live test": "Shells should be tightly closed. Tap open shells — live clams will close"
        },
        "foraging_tips": {
            "where": "Sandy and muddy estuaries, sheltered bays. Dig with a rake or trowel just below the surface",
            "when": "Autumn to spring (months with an 'R'). Avoid summer spawning season",
            "sustainable": "Only take what you will eat. Leave small clams. Follow local byelaws on minimum sizes",
            "danger_zone": "⚠️ CRITICAL: Only from classified Class A waters. Purge 12-24 hours in clean salt water. Cook thoroughly. Toxin risk is real"
        },
        "lookalikes": [
            {
                "name": "Quahog (Hard Clam)",
                "danger": "EDIBLE",
                "diff": "Quahog has a more rounded, thicker shell without the cross-hatch pattern. Both are edible"
            }
        ],
        "confusion_notes": "Palourde Clams have a distinctive cross-hatch pattern on the shell (concentric ridges AND radiating lines). Only collect from classified clean waters."
    },
    {
        "name": "Limpet",
        "latin_name": "Patella vulgata",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Rocky shores, clinging to rocks in the intertidal zone",
        "regions": ["Coastal", "All"],
        "difficulty": 1,
        "parts": "Foot meat",
        "warnings": "⚠️ Only collect from clean water. Must be cooked thoroughly. Very tough and chewy — best minced or used in stews. Do NOT eat raw. Check FSA water quality advisories.",
        "description": "**Identification:** Cone-shaped shell, 3-6cm, grey to dark grey. Clings tightly to rocks in the intertidal zone. Shell interior is iridescent. Very common on all UK rocky shores. **Uses:** Boil for 10+ minutes. Very tough and chewy — best minced, used in stews, chowders, or as bait. Traditional coastal food in some areas.",
        "id_keys": {
            "Shell": "Cone-shaped, 3-6cm, grey to dark grey, clings tightly to rocks",
            "Interior": "Iridescent interior (mother-of-pearl sheen)",
            "Position": "Clings tightly to rocks in the intertidal zone — must be popped off quickly",
            "Size": "3-6cm shell diameter"
        },
        "foraging_tips": {
            "where": "On rocks in the intertidal zone. Very common on all UK rocky shores",
            "when": "Autumn to spring — best in cooler months. Avoid summer spawning",
            "sustainable": "Very common. Only take what you will eat. Pop off rocks quickly with a knife or rock",
            "danger_zone": "⚠️ Very tough and chewy. Must be cooked thoroughly — do NOT eat raw. Best minced or in stews. Check water quality"
        },
        "lookalikes": [
            {
                "name": "Keyhole Limpet",
                "danger": "EDIBLE",
                "diff": "Keyhole Limpets have a small hole at the top of the shell. Common Limpets have a solid cone. Both are edible"
            }
        ],
        "confusion_notes": "Limpets are unmistakable — cone-shaped shells clinging tightly to rocks. Very tough meat, best minced or used in stews. Not a prime eating shellfish but abundant."
    },
    {
        "name": "Ormer (Abalone)",
        "latin_name": "Haliotis tuberculata",
        "category": "Shellfish",
        "months": ["January", "February", "March", "April", "May", "September", "October", "November", "December"],
        "habitat": "Rocky seabed, under large boulders, subtidal and very low spring tides",
        "regions": ["Channel Islands", "Southwest"],
        "difficulty": 3,
        "parts": "Foot meat",
        "warnings": "⚠️ STRICTLY regulated in Channel Islands — seasonal limits, size limits, and permits required. Check local byelaws carefully. Only collect from clean water. Very tough — must be tenderised before cooking. Allergen risk.",
        "description": "**Identification:** Large, ear-shaped shell with a row of holes along one edge. Shell is greenish-brown with mother-of-pearl interior. Single, large muscular foot. 7-12cm. Found under large boulders at extreme low water and subtidal. **Uses:** Must be tenderised by beating with a mallet. Fry in butter with garlic, or slow-cook in stews. Considered a delicacy in the Channel Islands (called 'ormering').",
        "id_keys": {
            "Shell": "Ear-shaped, greenish-brown, 7-12cm, with a distinctive row of holes along one edge",
            "Interior": "Beautiful mother-of-pearl (iridescent) interior",
            "Holes": "Row of 5-9 holes along one edge of the shell — KEY feature",
            "Foot": "Large, muscular, single foot that clings tightly to rocks"
        },
        "foraging_tips": {
            "where": "Under large boulders at extreme low spring tides. Mainly Channel Islands. Rarely found on UK mainland",
            "when": "Season varies by location — check local byelaws. Channel Islands have strict seasons",
            "sustainable": "STRICTLY regulated — permits, seasons, and size limits apply in Channel Islands. Check local laws carefully",
            "danger_zone": "⚠️ Must be tenderised (beaten) before cooking or it will be inedibly tough. Check local regulations — heavily protected in some areas"
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "EDIBLE",
                "diff": "The row of holes along one edge of the shell makes Ormers unmistakable."
            }
        ],
        "confusion_notes": "Ormers are unmistakable — ear-shaped shell with a row of holes along one edge and mother-of-pearl interior. Heavily regulated in the Channel Islands."
    },
    {
        "name": "Edible Sea Urchin",
        "latin_name": "Paracentrotus lividus / Echinus esculentus",
        "category": "Shellfish",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "habitat": "Rocky seabed, rock pools, under boulders, kelp forests",
        "regions": ["Coastal", "Southwest", "Scotland", "Ireland"],
        "difficulty": 3,
        "parts": "Gonads (roe) inside",
        "warnings": "⚠️ Sharp spines can pierce skin and break off. Use thick gloves. Check FSA water quality. The edible part is the gonads (roe) inside, not the whole animal. Allergen risk.",
        "description": "**Identification:** Round, spiny ball, 5-10cm diameter. Paracentrotus lividus is dark purple/black. Echinus esculentus is larger, pinkish-red with white-tipped spines. Found on rocky seabeds and in kelp forests. **Uses:** Crack open the shell and scoop out the orange gonads (roe). Eat raw with lemon, or use in pasta, risotto, or on toast. Sweet, briny, umami flavour.",
        "id_keys": {
            "Shape": "Round, spiny ball — like a hedgehog of the sea",
            "Spines": "Sharp, movable spines cover the entire shell",
            "P_lividus": "Paracentrotus lividus: smaller (5cm), dark purple/black spines, found under boulders",
            "E_esculentus": "Echinus esculentus: larger (10-15cm), pinkish-red with white-tipped spines, found on rocky seabeds"
        },
        "foraging_tips": {
            "where": "Rocky seabed, kelp forests, under boulders on low spring tides. P. lividus mainly SW England; E. esculentus all around UK coast",
            "when": "Year-round, but best gonads in spring (before spawning)",
            "sustainable": "Only take what you will eat. Check local regulations — some areas have limits. Pop off rocks carefully",
            "danger_zone": "⚠️ Spines are SHARP and can break off in skin. Use thick gloves. Only the orange gonads (roe) inside are eaten"
        },
        "lookalikes": [
            {
                "name": "Green Sea Urchin (Psammechinus miliaris)",
                "danger": "EDIBLE",
                "diff": "Green Sea Urchin is smaller and green. Also edible but less commonly foraged"
            }
        ],
        "confusion_notes": "Sea urchins are unmistakable — round, spiny balls. Only the orange gonads (roe) inside are eaten. Use thick gloves to handle — spines are sharp."
    },
    {
        "name": "Topshell",
        "latin_name": "Osilinus lineatus / Gibbula spp.",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Rocky shores, rock pools, under stones",
        "regions": ["Coastal", "All"],
        "difficulty": 1,
        "parts": "Whole animal (boiled and picked from shell)",
        "warnings": "⚠️ Only collect from clean water. Check FSA advisories. Purge in clean salt water for several hours. Cook thoroughly — boil for at least 5 minutes. Small and fiddly.",
        "description": "**Identification:** Small, rounded, cone-shaped shell, 1-2cm. Purple Topshell (Osilinus lineatus) has distinctive dark purple stripes. Grey Topshell (Gibbula cineraria) is grey with pink tip. Found on rocky shores and in rock pools. **Uses:** Boil for 5+ minutes. Pick from shell with a pin. Similar to winkles but smaller. Use in soups or eat with vinegar.",
        "id_keys": {
            "Shell": "Small, rounded, cone-shaped, 1-2cm",
            "Purple_Topshell": "Dark purple stripes with a mother-of-pearl inner lip",
            "Grey_Topshell": "Grey with a pink tip, smaller than purple topshell",
            "Habitat": "On rocks and in rock pools, often under seaweed"
        },
        "foraging_tips": {
            "where": "Rocky shores and rock pools, under seaweed and stones",
            "when": "Autumn to spring — best in cooler months",
            "sustainable": "Very common. Take only what you will eat. Small and fiddly — winkles are easier",
            "danger_zone": "⚠️ Purge in clean salt water for 3-4 hours. Boil for at least 5 minutes. Check FSA water quality warnings"
        },
        "lookalikes": [
            {
                "name": "Winkles (Littorina littorea)",
                "danger": "EDIBLE",
                "diff": "Winkles are larger (2-3cm), darker, and more pointed. Topshells are smaller (1-2cm), more rounded, and often colourful"
            }
        ],
        "confusion_notes": "Topshells are small, rounded, and often colourful. Purple Topshell has distinctive dark purple stripes. All UK topshells are edible. Small and fiddly."
    },
    {
        "name": "Tellins",
        "latin_name": "Tellina spp.",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Sandy beaches, buried just below the surface",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Check FSA shellfish classification. Purge in clean salt water for 12-24 hours before cooking. Cook thoroughly. Do NOT collect from unclassified waters.",
        "description": "**Identification:** Thin, flat, delicate bivalve shell. Oval to kidney-shaped. 1-3cm. Pink, white, or yellow. One of the most beautiful beach shells. Found buried just below the sand surface. **Uses:** Steam for 2-3 minutes until shells open. Sweet, delicate flavour. Use in pasta, risotto, or simply steamed with white wine and garlic.",
        "id_keys": {
            "Shell": "Thin, flat, delicate, 1-3cm, oval to kidney-shaped",
            "Colour": "Pink, white, or yellow — often beautifully banded or tinged",
            "Habitat": "Buried just below sand surface on clean sandy beaches",
            "Live_test": "Shells should be tightly closed. Tap open shells — live tellins will close"
        },
        "foraging_tips": {
            "where": "Clean sandy beaches — dig with fingers or a trowel just below the surface",
            "when": "Autumn to spring (months with an 'R'). Avoid summer",
            "sustainable": "Only take what you will eat. Leave small tellins. Follow local byelaws",
            "danger_zone": "⚠️ CRITICAL: Only from classified Class A waters. Purge 12-24 hours. Cook thoroughly. Toxin risk is real"
        },
        "lookalikes": [
            {
                "name": "None dangerous",
                "danger": "EDIBLE",
                "diff": "Other similar small bivalves on sandy beaches are generally edible if from clean water. The main risk is water quality, not identification"
            }
        ],
        "confusion_notes": "Tellins are thin, flat, beautifully coloured bivalves found on sandy beaches. All UK tellin species are edible. The main risk is water quality, not identification."
    },
    {
        "name": "Gaper Clam (Soft-shell Clam)",
        "latin_name": "Mya arenaria",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Muddy estuaries, sand flats, buried deep in mud (15-30cm)",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal (siphon and body)",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Check FSA shellfish classification. Purge in clean salt water for 12-24 hours before cooking. Cook thoroughly. Do NOT collect from unclassified waters.",
        "description": "**Identification:** Large, oval bivalve shell, 7-15cm. Thin, chalky, grey-white. Cannot close its shell fully — the siphon sticks out even when closed (hence 'gaper'). Distinctive large siphon. Buried deep in mud, 15-30cm down. **Uses:** Steam or boil for 5-10 minutes. Sweet, tender meat. The siphon can be sliced and fried. Popular in New England clam chowder.",
        "id_keys": {
            "Shell": "Large, oval, thin, chalky, grey-white, 7-15cm",
            "Gap": "Shell does NOT close fully — the siphon protrudes even when closed (KEY feature)",
            "Siphon": "Large, leathery siphon protrudes from shell",
            "Habitat": "Buried deep in mud (15-30cm down) in estuaries"
        },
        "foraging_tips": {
            "where": "Muddy estuaries and sand flats. Look for siphon holes (keyhole-shaped) in the mud at low tide",
            "when": "Autumn to spring. Avoid summer months",
            "sustainable": "Only take what you will eat. Dig deep — they can be 30cm down. Follow local byelaws",
            "danger_zone": "⚠️ CRITICAL: Only from classified Class A waters. Purge 12-24 hours. Cook thoroughly. Biotoxin risk is real"
        },
        "lookalikes": [
            {
                "name": "Razor Clam (Ensis spp.)",
                "danger": "EDIBLE",
                "diff": "Razor Clams are long, thin, and straight like a razor blade. Gaper Clams are oval and cannot close their shell fully"
            }
        ],
        "confusion_notes": "Gaper Clams are distinctive because their shell does NOT close fully — the siphon always sticks out. Found deep in mud. Only collect from classified clean waters."
    },
    {
        "name": "Queen Scallop",
        "latin_name": "Aequipecten opercularis",
        "category": "Shellfish",
        "months": ["November", "December", "January", "February", "March", "April", "May"],
        "habitat": "Sandy and gravelly seabed, subtidal (10-100m depth)",
        "regions": ["Coastal", "All"],
        "difficulty": 3,
        "parts": "White adductor muscle and orange roe (coral)",
        "warnings": "⚠️ Check FSA water classifications before collecting. Dive-caught or dredged. Cook thoroughly unless from Class A waters. Allergen risk for shellfish.",
        "description": "**Identification:** Smaller than King Scallop, 5-8cm. Fan-shaped shell with radiating ribs. Both valves slightly cupped (unlike King Scallop which has one flat and one cupped). Can swim by clapping shells. Often sold as 'queenies'. **Uses:** Pan-fry whole for 1-2 minutes, or grill with garlic butter. Sweet, delicate flavour. Can be eaten whole (roe and muscle) or just the white meat.",
        "id_keys": {
            "Shell": "Fan-shaped, 5-8cm, both valves slightly cupped (symmetrical)",
            "Colour": "Variable — cream, pink, orange, or patterned",
            "Size": "5-8cm — smaller than King Scallops",
            "Swimming": "Live queen scallops can swim by clapping shells"
        },
        "foraging_tips": {
            "where": "Sandy and gravelly seabed, 10-100m depth. Requires diving or dredging",
            "when": "November to May — closed during summer spawning",
            "sustainable": "Follow local byelaws. Dive-caught is more sustainable than dredged. Minimum size applies",
            "danger_zone": "⚠️ Requires diving to collect. Check FSA water classifications. Never collect from unclassified waters"
        },
        "lookalikes": [
            {
                "name": "King Scallop (Pecten maximus)",
                "danger": "EDIBLE",
                "diff": "King Scallops are LARGER (10-15cm), with one flat valve and one deeply cupped valve. Queen Scallops are SMALLER (5-8cm) with both valves slightly cupped"
            }
        ],
        "confusion_notes": "Queen Scallops are smaller than King Scallops (5-8cm) with both valves slightly cupped. Sweet and delicate. The main concerns are diving safety and water quality."
    },
    {
        "name": "Squat Lobster",
        "latin_name": "Galathea squamifera / Munida rugosa",
        "category": "Shellfish",
        "months": ["April", "May", "June", "July", "August", "September", "October"],
        "habitat": "Rock pools, under stones, subtidal rocky seabed",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Tail meat (small amount)",
        "warnings": "⚠️ Only collect from clean water. Cook thoroughly. Very little meat per animal — best for stock or bisque. Allergen risk.",
        "description": "**Identification:** Small, lobster-like crustacean, 3-5cm body. One long claw larger than the other. Flattened body. Found under stones in rock pools. Greenish-brown with orange tints. Can swim backwards rapidly by flipping tail. **Uses:** Boil for 3-5 minutes. Very little meat — best used for stock, bisque, or added to seafood stews for flavour. Sweet taste but fiddly.",
        "id_keys": {
            "Size": "Small, 3-5cm body — much smaller than lobster",
            "Claws": "One claw larger than the other, but both relatively small",
            "Body": "Flattened, lobster-like shape, tucked under rocks",
            "Colour": "Greenish-brown with orange tints (varies by species)"
        },
        "foraging_tips": {
            "where": "Under stones in rock pools and on the lower rocky shore. Subtidal to 100m+",
            "when": "Spring to autumn",
            "sustainable": "Very common. Take only what you need. Leave small ones",
            "danger_zone": "⚠️ Very little meat per animal. Best for stock/bisque rather than picking for meat. Cook thoroughly"
        },
        "lookalikes": [
            {
                "name": "Langoustine (Nephrops norvegicus)",
                "danger": "EDIBLE",
                "diff": "Langoustine is MUCH LARGER (10-25cm), pink-orange, and lives in deep mud. Squat Lobster is tiny (3-5cm), brown-green, and lives under rocks"
            }
        ],
        "confusion_notes": "Squat Lobsters are small (3-5cm), flattened, and found under stones in rock pools. Much smaller than true lobsters or langoustines. Best for stock, not picking."
    },
    {
        "name": "Surf Clam",
        "latin_name": "Spisula solida",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Sandy beaches, intertidal zone, buried in sand",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Check FSA shellfish classification. Purge in clean salt water for 12-24 hours before cooking. Cook thoroughly. Do NOT collect from unclassified waters.",
        "description": "**Identification:** Thick, triangular shell, 4-6cm. Smooth exterior, white to cream with a yellow-brown periostracum (skin). Rounded at the anterior, more pointed at the posterior. Found buried in sand on exposed beaches. **Uses:** Steam for 3-5 minutes until shells open. Sweet, firm meat. Excellent in chowder, pasta, or simply steamed with white wine.",
        "id_keys": {
            "Shell": "Thick, triangular, 4-6cm, smooth exterior",
            "Colour": "White to cream with a yellow-brown outer skin (periostracum)",
            "Shape": "Rounded at one end, more pointed at the other",
            "Habitat": "Buried in sand on exposed sandy beaches"
        },
        "foraging_tips": {
            "where": "Sandy beaches — dig with feet or hands in the intertidal zone. Often found after storms",
            "when": "Autumn to spring. Often washed up after storms",
            "sustainable": "Only take what you will eat. Follow local byelaws on minimum sizes",
            "danger_zone": "⚠️ CRITICAL: Only from classified Class A waters. Purge 12-24 hours. Cook thoroughly. Biotoxin risk"
        },
        "lookalikes": [
            {
                "name": "Palourde Clam",
                "danger": "EDIBLE",
                "diff": "Palourde has a cross-hatch pattern on the shell. Surf Clam has a SMOOTH shell with a yellow-brown skin"
            }
        ],
        "confusion_notes": "Surf Clams have thick, smooth, triangular shells with a yellow-brown outer skin. Only collect from classified clean waters. Purge and cook thoroughly."
    },
    {
        "name": "Pepper Furrow Shell",
        "latin_name": "Scrobicularia plana",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Muddy estuaries, mud flats, buried deep in mud (10-20cm)",
        "regions": ["Coastal", "All"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Estuary clams are HIGH RISK for pollution and biotoxins. Check FSA classification carefully. Purge in clean salt water for 24 hours. Cook thoroughly. Do NOT collect from unclassified waters.",
        "description": "**Identification:** Thin, flat, round bivalve shell, 4-7cm. Grey-white with a distinctive dark grey periostracum (skin). Lives deep in mud in estuaries. Look for keyhole-shaped holes in the mud at low tide. **Uses:** Steam for 5-8 minutes until shells open. Can be used in chowder, pasta, or simply steamed with garlic and white wine.",
        "id_keys": {
            "Shell": "Thin, flat, round, 4-7cm, grey-white",
            "Skin": "Dark grey periostracum (outer skin) — distinctive feature",
            "Habitat": "Deep in mud in estuaries — look for keyhole-shaped siphon holes",
            "Live_test": "Shells should be tightly closed. Tap open shells — live ones will close"
        },
        "foraging_tips": {
            "where": "Muddy estuaries — look for keyhole-shaped holes in the mud at low tide. Dig 10-20cm deep",
            "when": "Autumn to spring. Avoid summer spawning season",
            "sustainable": "Only take what you will eat. Leave small shells. Follow local byelaws",
            "danger_zone": "⚠️ CRITICAL: Estuary clams are HIGH RISK for pollution. Only from classified Class A waters. Purge 24 hours. Cook thoroughly"
        },
        "lookalikes": [
            {
                "name": "Gaper Clam (Mya arenaria)",
                "danger": "EDIBLE",
                "diff": "Gaper Clam is LARGER (7-15cm) and its shell cannot close fully. Pepper Furrow Shell is smaller (4-7cm) and can close fully"
            }
        ],
        "confusion_notes": "Pepper Furrow Shells are thin, flat, and found deep in estuary mud. HIGH RISK for pollution — only collect from classified clean waters."
    },
    {
        "name": "Cuttlefish",
        "latin_name": "Sepia officinalis",
        "category": "Shellfish",
        "months": ["May", "June", "July", "August", "September", "October"],
        "habitat": "Sandy and muddy seabed, subtidal, shallow coastal waters",
        "regions": ["Coastal", "Southern", "Southwest"],
        "difficulty": 3,
        "parts": "Body (mantle) and tentacles",
        "warnings": "⚠️ Ink can stain permanently. Check FSA water quality. Allergen risk for molluscs. Only collect from clean water. Handle carefully — can ink you.",
        "description": "**Identification:** Broad, oval body (mantle) up to 30cm. Eight short arms and two long tentacles. Changes colour rapidly. Internal cuttlebone (white, oval). Zebra-stripe pattern when swimming. Found near the seabed in shallow water. **Uses:** Clean thoroughly, remove cuttlebone, beak, and ink sac (or use ink in cooking). Score mantle, grill, or slow-cook. Excellent in risotto with ink, or stuffed and baked.",
        "id_keys": {
            "Body": "Broad, oval mantle up to 30cm, can change colour rapidly",
            "Tentacles": "Eight short arms + two long retractable tentacles",
            "Cuttlebone": "White, oval internal shell (cuttlebone) — often found washed up on beaches",
            "Pattern": "Zebra-stripe pattern on body when swimming or agitated"
        },
        "foraging_tips": {
            "where": "Sandy and muddy seabed in shallow coastal water. Often caught in pots or nets. Cuttlebones washed up on beaches are a good sign",
            "when": "May to October — they come inshore to breed in summer",
            "sustainable": "Follow local byelaws. Often caught as bycatch. Minimum size applies in some areas",
            "danger_zone": "⚠️ Ink can stain permanently. Handle carefully. Clean thoroughly before cooking. Check water quality"
        },
        "lookalikes": [
            {
                "name": "Common Squid (Loligo vulgaris)",
                "danger": "EDIBLE",
                "diff": "Squid has a LONG, pointed, streamlined body. Cuttlefish has a BROAD, oval body. Both are edible"
            }
        ],
        "confusion_notes": "Cuttlefish have a BROAD, oval body and an internal cuttlebone. Squid have a LONG, pointed body. Both are edible. Cuttlefish ink is excellent for cooking."
    },
    {
        "name": "Common Squid",
        "latin_name": "Loligo vulgaris / Alloteuthis subulata",
        "category": "Shellfish",
        "months": ["May", "June", "July", "August", "September", "October"],
        "habitat": "Coastal waters, sandy seabed, subtidal",
        "regions": ["Coastal", "Southern", "Southwest"],
        "difficulty": 3,
        "parts": "Body (mantle) and tentacles",
        "warnings": "⚠️ Ink can stain permanently. Check FSA water quality. Allergen risk for molluscs. Handle carefully — can ink you.",
        "description": "**Identification:** Long, pointed, streamlined body (mantle) up to 40cm. Eight short arms and two long tentacles. Translucent with reddish-brown spots. Internal quill (thin, transparent feather-shaped shell). Large eyes. Swims in shoals. **Uses:** Clean thoroughly, remove quill, beak, and ink sac. Score, grill quickly, or fry in rings. Also excellent slow-cooked in stew. Tender if cooked very briefly (2 mins) or very slowly (1+ hour).",
        "id_keys": {
            "Body": "Long, pointed, streamlined mantle up to 40cm",
            "Tentacles": "Eight short arms + two long retractable tentacles",
            "Quill": "Thin, transparent, feather-shaped internal shell (quill)",
            "Colour": "Translucent with reddish-brown spots, can change colour"
        },
        "foraging_tips": {
            "where": "Coastal waters, sandy seabed. Often caught in nets or jigs. Squid jigs work well at night from piers",
            "when": "May to October — they come inshore in warmer months",
            "sustainable": "Use squid jigs for targeted catch. Follow local byelaws",
            "danger_zone": "⚠️ Ink can stain. Clean thoroughly before cooking. Check water quality"
        },
        "lookalikes": [
            {
                "name": "Cuttlefish (Sepia officinalis)",
                "danger": "EDIBLE",
                "diff": "Cuttlefish has a BROAD, oval body and a thick cuttlebone. Squid has a LONG, pointed body and a thin transparent quill"
            }
        ],
        "confusion_notes": "Squid have a LONG, pointed body and a thin transparent quill. Cuttlefish have a BROAD, oval body and a thick cuttlebone. Both are edible."
    },
        {
        "name": "Quahog (Hard Clam)",
        "latin_name": "Mercenaria mercenaria",
        "category": "Shellfish",
        "months": ["September", "October", "November", "December", "January", "February", "March", "April"],
        "habitat": "Sandy and muddy substrates, estuaries, sheltered bays, subtidal",
        "regions": ["Coastal", "Southern", "Eastern"],
        "difficulty": 2,
        "parts": "Whole animal",
        "warnings": "⚠️ CRITICAL: Only collect from classified Class A waters. Check FSA shellfish classification for your area. Purge in clean salt water for 12-24 hours before cooking. Cook thoroughly. Do NOT collect from unclassified waters. Naturalised in UK — not native.",
        "description": "**Identification:** Thick, heavy, rounded bivalve shell, 5-10cm. Grey-white exterior with concentric growth rings. Interior is glossy white with purple/violet stains near the hinge (key feature). Introduced from North America, now naturalised in some UK estuaries. **Uses:** Steam for 5-8 minutes until shells open. Can be eaten raw on the half shell (if from Class A waters), steamed, in chowder, or stuffed and baked. Sweet, firm, clam flavour.",
        "id_keys": {
            "Shell": "Thick, heavy, rounded, 5-10cm, grey-white with concentric growth rings",
            "Interior": "Glossy white with distinctive PURPLE/VIOLET stains near the hinge — KEY feature",
            "Size": "5-10cm — smaller ones are 'littlenecks', medium are 'cherrystones', large are 'chowders'",
            "Habitat": "Buried in sand/mud in estuaries and sheltered bays"
        },
        "foraging_tips": {
            "where": "Estuaries and sheltered bays in southern and eastern England. Dig with a trowel or rake, 5-15cm below the surface",
            "when": "Autumn to spring (months with an 'R'). Avoid summer spawning season",
            "sustainable": "Only take what you will eat. Leave small clams. Follow local byelaws. Naturalised species — check local regulations",
            "danger_zone": "⚠️ CRITICAL: Only from classified Class A waters. Purge 12-24 hours in clean salt water. Cook thoroughly unless from confirmed Class A waters"
        },
        "lookalikes": [
            {
                "name": "Palourde Clam (Venerupis decussata)",
                "danger": "EDIBLE",
                "diff": "Palourde has a cross-hatch pattern on the shell and NO purple stains inside. Quahog has a smooth shell exterior and DISTINCTIVE purple/violet stains inside near the hinge"
            }
        ],
        "confusion_notes": "Quahogs are identified by their THICK, heavy shell and DISTINCTIVE purple/violet stains on the interior near the hinge. Only collect from classified clean waters. Naturalised in the UK from North America.",
    },
]