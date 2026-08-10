# ==========================================
# FORAGING QUEST — GAME CONFIG
# ==========================================

# ==========================================
# SCENARIO DEFINITIONS
# ==========================================

QUEST_SCENARIOS = {
    "wild_forest": {
        "id": "wild_forest",
        "name": "Wild Forest",
        "icon": "🌲",
        "difficulty": 2,
        "tagline": "Lost in ancient British woodland",
        "desc": "A hiking accident has left you stranded in dense temperate forest. Days are mild but nights are cold. Rain is common. The woodland is rich with edible plants — but deadly lookalikes grow beside them.",
        "intro": (
            "The last thing you remember is the path winding deeper into thicker trees. "
            "A wrong step, a twisted root, and you tumbled down a steep bank. "
            "By the time you stopped sliding, the path was gone. Just trees in every direction. "
            "Your phone has no signal. The light is fading. "
            "You need shelter, water, and food — and you need to identify what's safe to eat. "
            "The forest is full of life, but not all of it wants you here."
        ),
        "starting": {
            "health": 100,
            "hunger": 80,
            "warmth": 70,
            "morale": 60,
            "water": None
        },
        "decay": {
            "hunger": 12,
            "warmth": 5,
            "morale": 5,
            "water": 0
        },
        "weather_types": {
            "clear": {"warmth_mod": 0, "morale_mod": 2, "desc": "Clear skies through the canopy. Dappled light reaches the forest floor.", "icon": "☀️"},
            "cloudy": {"warmth_mod": -2, "morale_mod": -1, "desc": "Grey clouds hang low between the trees. The air feels damp.", "icon": "☁️"},
            "rain": {"warmth_mod": -8, "morale_mod": -3, "desc": "Rain drips through the canopy. Everything is wet and cold.", "icon": "🌧️"},
            "storm": {"warmth_mod": -15, "morale_mod": -5, "desc": "Thunder rolls. Wind tears at the trees. Branches crack and fall.", "icon": "⛈️"},
            "fog": {"warmth_mod": -3, "morale_mod": -2, "desc": "Thick fog wraps the forest. You can barely see 20 metres.", "icon": "🌫️"},
        },
        "weather_chances": {
            "Spring": {"clear": 0.30, "cloudy": 0.30, "rain": 0.25, "storm": 0.05, "fog": 0.10},
            "Summer": {"clear": 0.45, "cloudy": 0.30, "rain": 0.15, "storm": 0.05, "fog": 0.05},
            "Autumn": {"clear": 0.20, "cloudy": 0.30, "rain": 0.30, "storm": 0.10, "fog": 0.10},
            "Winter": {"clear": 0.15, "cloudy": 0.35, "rain": 0.25, "storm": 0.15, "fog": 0.10},
        },
        "start_season": "Autumn",
        "season_cycle_days": 10,
        "hours_per_day": 12,
        "actions_per_day": 2,
        "bonus_action_morale": 75,
        "plant_habitats": ["Woodland", "Hedgerow", "Damp"],
        "locations": [
            {
                "id": "camp",
                "name": "Your Camp",
                "icon": "⛺",
                "desc": "The clearing where you woke up. Your makeshift shelter is here.",
                "discovered": True,
                "foraging_quality": 0.5,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 0
            },
            {
                "id": "stream",
                "name": "Rocky Stream",
                "icon": "🏞️",
                "desc": "A narrow stream cuts through mossy stones. Fresh water and water-loving plants.",
                "discovered": False,
                "explore_hours": 2,
                "foraging_quality": 0.8,
                "shelter_bonus": False,
                "water_source": True,
                "signal_bonus": 0
            },
            {
                "id": "dense_woodland",
                "name": "Dense Woodland",
                "icon": "🌳",
                "desc": "Thick canopy, barely any light reaches the floor. Rich foraging but easy to get disoriented.",
                "discovered": False,
                "explore_hours": 3,
                "foraging_quality": 1.0,
                "shelter_bonus": False,
                "water_source": False,
                "signal_bonus": 0,
                "lose_chance": 0.15
            },
            {
                "id": "hedgerow",
                "name": "Hedgerow Edge",
                "icon": "🌿",
                "desc": "Where the forest meets open ground. Berry bushes and wild flowers in abundance.",
                "discovered": False,
                "explore_hours": 2,
                "foraging_quality": 0.9,
                "shelter_bonus": False,
                "water_source": False,
                "signal_bonus": 0
            },
            {
                "id": "rocky_ridge",
                "name": "Rocky Ridge",
                "icon": "🪨",
                "desc": "A high point with views across the canopy. Good for signalling, exposed to weather.",
                "discovered": False,
                "explore_hours": 4,
                "foraging_quality": 0.3,
                "shelter_bonus": False,
                "water_source": False,
                "signal_bonus": 2,
                "wind_penalty": True
            },
            {
                "id": "old_bothy",
                "name": "Abandoned Bothy",
                "icon": "🏚️",
                "desc": "A ruined stone shelter. The roof is half-gone but the walls are solid. Possible supplies inside.",
                "discovered": False,
                "explore_hours": 3,
                "foraging_quality": 0.2,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 0,
                "shelter_level": 2
            }
        ],
        "events": [
            {
                "id": "wolf_encounter",
                "name": "Wolf Encounter",
                "icon": "🐺",
                "probability": 0.08,
                "seasons": ["Autumn", "Winter"],
                "min_day": 2,
                "text": "You hear low growling from the undergrowth. A wolf steps into view, watching you with amber eyes. It doesn't approach — but it doesn't leave either.",
                "choices": [
                    {
                        "text": "Build a fire quickly",
                        "icon": "🔥",
                        "hours": 1,
                        "requires": ["wood"],
                        "success": 0.85,
                        "success_text": "You scramble for kindling and strike a spark. The fire crackles to life. The wolf backs away, growling, then vanishes into the trees. The fire keeps you warm too.",
                        "success_fx": {"warmth": 10, "morale": 5},
                        "fail_text": "Your hands shake too much. The kindling is damp. The fire won't catch and the wolf senses your fear. It circles closer before losing interest. You're shaken.",
                        "fail_fx": {"health": -10, "morale": -10}
                    },
                    {
                        "text": "Continue what you were doing",
                        "icon": "🌲",
                        "hours": 0,
                        "requires": [],
                        "success": 0.3,
                        "success_text": "You ignore the wolf and carry on. It watches for a while, then slinks away. Perhaps it was just curious.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You try to ignore it, but the wolf doesn't leave. It circles closer, snarling. You back away slowly, losing precious time and nerve.",
                        "fail_fx": {"health": -15, "morale": -15}
                    },
                    {
                        "text": "Climb the nearest tree",
                        "icon": "🧗",
                        "hours": 2,
                        "requires": [],
                        "success": 0.9,
                        "success_text": "You scramble up an old oak. The wolf paces below for over an hour before losing interest. From up here, you notice landmarks you couldn't see from the ground.",
                        "success_fx": {"morale": -5, "explore_bonus": 1},
                        "fail_text": "The bark is slick with rain. You slip and fall hard. The wolf lunges — you kick out and it retreats, but your ankle is twisted.",
                        "fail_fx": {"health": -30, "morale": -20}
                    },
                    {
                        "text": "Make yourself big and loud",
                        "icon": "🗣️",
                        "hours": 0,
                        "requires": [],
                        "success": 0.65,
                        "success_text": "You stand tall, wave your arms, and shout. The wolf startles, ears flat, and bolts into the undergrowth. It won't be back soon.",
                        "success_fx": {"morale": 8},
                        "fail_text": "You shout and wave, but the wolf isn't intimidated. It stands its ground, hackles raised. You slowly back away, heart pounding. It follows at a distance for hours.",
                        "fail_fx": {"health": -5, "morale": -15}
                    }
                ]
            },
            {
                "id": "heavy_rain",
                "name": "Torrential Rain",
                "icon": "🌧️",
                "probability": 0.12,
                "seasons": ["Spring", "Autumn", "Winter"],
                "min_day": 1,
                "text": "The sky darkens and rain hammers through the canopy. Within minutes, everything is soaked. Your shelter groans under the weight of water.",
                "choices": [
                    {
                        "text": "Reinforce your shelter",
                        "icon": "🏕️",
                        "hours": 2,
                        "requires": ["wood"],
                        "success": 0.8,
                        "success_text": "You work fast, adding branches and leaves to your shelter. It holds. You stay mostly dry while the rain hammers down around you.",
                        "success_fx": {"warmth": 5, "morale": 3},
                        "fail_text": "You try to reinforce the shelter but the rain is too heavy. Materials slip from your hands. At least you tried — the shelter is no worse than before.",
                        "fail_fx": {"warmth": -5, "morale": -3}
                    },
                    {
                        "text": "Wait it out under tree cover",
                        "icon": "🌳",
                        "hours": 1,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You find a large oak with dense canopy and huddle beneath it. The rain drips around you but you stay relatively dry.",
                        "success_fx": {"warmth": -3, "morale": -2},
                        "fail_text": "The tree cover isn't enough. You're soaked through and shivering. The rain seems endless.",
                        "fail_fx": {"warmth": -15, "morale": -8}
                    },
                    {
                        "text": "Use the rain to collect water",
                        "icon": "💧",
                        "hours": 1,
                        "requires": [],
                        "success": 0.75,
                        "success_text": "You rig up leaves to funnel rainwater into your container. Free, clean water. A small victory on a miserable day.",
                        "success_fx": {"morale": 5, "inventory_add": ["water"]},
                        "fail_text": "The rain is too heavy — your improvised collection keeps overflowing. You get soaked trying and barely collect anything.",
                        "fail_fx": {"warmth": -10, "morale": -5}
                    },
                    {
                        "text": "Press on with your tasks regardless",
                        "icon": "🚶",
                        "hours": 0,
                        "requires": [],
                        "success": 0.4,
                        "success_text": "You push through the rain. It's miserable but you get things done. Sometimes you just have to endure.",
                        "success_fx": {"warmth": -8, "morale": -3},
                        "fail_text": "The rain makes everything impossible. You slip, drop things, and end up soaked and exhausted with nothing to show for it.",
                        "fail_fx": {"warmth": -20, "health": -5, "morale": -10}
                    }
                ]
            },
            {
                "id": "animal_tracks",
                "name": "Animal Tracks",
                "icon": "🦌",
                "probability": 0.10,
                "seasons": ["Spring", "Summer", "Autumn"],
                "min_day": 2,
                "text": "You notice fresh tracks in the mud. They're large — deer, maybe, or wild boar. They lead deeper into the forest.",
                "choices": [
                    {
                        "text": "Follow the tracks carefully",
                        "icon": "🧭",
                        "hours": 2,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You follow the tracks to a small clearing where deer have been grazing. You find signs of edible plants they've left behind, and a game trail that leads somewhere useful.",
                        "success_fx": {"morale": 5, "explore_bonus": 2, "hunger": 5},
                        "fail_text": "The tracks lead deeper into thick brush and then disappear. You're disoriented and have to find your way back, wasting time and energy.",
                        "fail_fx": {"morale": -5, "hunger": -5}
                    },
                    {
                        "text": "Set a snare near the tracks",
                        "icon": "🪤",
                        "hours": 2,
                        "requires": ["cordage"],
                        "success": 0.35,
                        "success_text": "You fashion a simple snare from cordage and set it near the tracks. The next morning, you find a rabbit! Fresh protein at last.",
                        "success_fx": {"hunger": 25, "morale": 10, "inventory_add": ["rabbit"]},
                        "fail_text": "You set the snare and wait, but nothing comes. The animals are too wary, or you've placed it wrong. At least the cordage is reusable.",
                        "fail_fx": {"morale": -3}
                    },
                    {
                        "text": "Mark the location and move on",
                        "icon": "📍",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You note the location in your mind. Animal tracks mean game trails, and game trails often lead to water. Useful knowledge for later.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You note the location and continue. Nothing ventured, nothing lost.",
                        "fail_fx": {"morale": 2}
                    },
                    {
                        "text": "Watch from a distance for movement",
                        "icon": "👁️",
                        "hours": 3,
                        "requires": [],
                        "success": 0.45,
                        "success_text": "You wait silently. After an hour, a deer steps into view. You observe its path — it knows where the good grazing is. You've learned something valuable about the landscape.",
                        "success_fx": {"morale": 8, "explore_bonus": 2},
                        "fail_text": "You wait for hours but see nothing. The tracks were old, or the animal has moved on. Time wasted, but the stillness was almost meditative.",
                        "fail_fx": {"morale": -3, "hunger": -3}
                    }
                ]
            },
            {
                "id": "twisted_ankle",
                "name": "Twisted Ankle",
                "icon": "🦶",
                "probability": 0.07,
                "seasons": ["Spring", "Summer", "Autumn", "Winter"],
                "min_day": 3,
                "text": "You step on a hidden root and your ankle twists sharply. Pain shoots up your leg. You can walk, but carefully.",
                "choices": [
                    {
                        "text": "Rest and bind it with leaves",
                        "icon": "🌿",
                        "hours": 2,
                        "requires": [],
                        "success": 0.9,
                        "success_text": "You wrap your ankle with broad leaves and rest. The swelling goes down slightly. You'll be slower, but you can still move.",
                        "success_fx": {"health": -5, "morale": -3},
                        "fail_text": "Even resting doesn't help much. The ankle throbs. You'll need to be very careful from now on.",
                        "fail_fx": {"health": -10, "morale": -8}
                    },
                    {
                        "text": "Look for comfrey or plantain to make a poultice",
                        "icon": "🩹",
                        "hours": 1,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You find plantain leaves and crush them into a poultice. The natural anti-inflammatory properties ease the swelling. Your knowledge of plants pays off beyond food.",
                        "success_fx": {"health": -2, "morale": 5},
                        "fail_text": "You search for medicinal plants but can't find any in your current state. The time spent hobbling around has made it worse.",
                        "fail_fx": {"health": -10, "morale": -5}
                    },
                    {
                        "text": "Push through — you can't afford to rest",
                        "icon": "🚶",
                        "hours": 0,
                        "requires": [],
                        "success": 0.3,
                        "success_text": "You grit your teeth and keep moving. The pain is sharp but you manage. Sometimes survival means pushing through.",
                        "success_fx": {"health": -8, "morale": 2},
                        "fail_text": "You try to push through but your ankle gives way. You fall hard, making it worse. Now you really can't move properly.",
                        "fail_fx": {"health": -20, "morale": -15}
                    },
                    {
                        "text": "Make a simple walking stick",
                        "icon": "🪵",
                        "hours": 1,
                        "requires": ["wood"],
                        "success": 0.85,
                        "success_text": "You find a sturdy branch and fashion a walking stick. It takes weight off your ankle and gives you stability. A small comfort in a hard situation.",
                        "success_fx": {"health": -3, "morale": 3, "inventory_add": ["walking_stick"]},
                        "fail_text": "You find a branch but it's too weak and snaps when you lean on it. Your ankle protests every step.",
                        "fail_fx": {"health": -8, "morale": -5}
                    }
                ]
            },
            {
                "id": "old_campsite",
                "name": "Abandoned Campsite",
                "icon": "🏕️",
                "probability": 0.09,
                "seasons": ["Spring", "Summer", "Autumn"],
                "min_day": 3,
                "text": "You stumble upon an old campsite. A ring of stones, charred wood, and scattered debris. Someone was here — months ago, maybe longer.",
                "choices": [
                    {
                        "text": "Search the campsite thoroughly",
                        "icon": "🔍",
                        "hours": 2,
                        "requires": [],
                        "success": 0.7,
                        "success_text": "You find useful items: a tin can, some cord, and a broken knife with a blade you can salvage. Previous survivors leave gifts for the next.",
                        "success_fx": {"morale": 8, "inventory_add": ["tin_can", "cordage", "knife_blade"]},
                        "fail_text": "You search carefully but find only rubbish and rain-rotted fabric. Whoever was here took everything useful with them.",
                        "fail_fx": {"morale": -5}
                    },
                    {
                        "text": "Use the fire ring for your own fire",
                        "icon": "🔥",
                        "hours": 1,
                        "requires": ["wood"],
                        "success": 0.9,
                        "success_text": "The stone ring draws heat beautifully. Your fire catches fast and burns warm. This was a good spot for a reason.",
                        "success_fx": {"warmth": 12, "morale": 5},
                        "fail_text": "The fire ring is waterlogged. You get some warmth but it's smoky and unsatisfying.",
                        "fail_fx": {"warmth": 3, "morale": -2}
                    },
                    {
                        "text": "Study the site for clues about the area",
                        "icon": "📝",
                        "hours": 1,
                        "requires": [],
                        "success": 0.75,
                        "success_text": "You notice the campsite was positioned near water and on higher ground. The previous occupant knew what they were doing. You learn from their choices.",
                        "success_fx": {"morale": 5, "explore_bonus": 2},
                        "fail_text": "The campsite reveals little. It's too old, too weathered. Whatever stories it held have washed away.",
                        "fail_fx": {"morale": -2}
                    },
                    {
                        "text": "Leave it alone — it feels wrong",
                        "icon": "🚫",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "Something about the place unsettles you. You move on. Perhaps it's superstition, but your instincts have kept you alive so far.",
                        "success_fx": {"morale": -2},
                        "fail_text": "You move on. The campsite fades behind you.",
                        "fail_fx": {"morale": -2}
                    }
                ]
            },
            {
                "id": "strange_mushrooms",
                "name": "Strange Mushrooms",
                "icon": "🍄",
                "probability": 0.09,
                "seasons": ["Summer", "Autumn"],
                "min_day": 2,
                "text": "Cluster of mushrooms growing at the base of an oak tree. Some look familiar. Others... less so. This could be food — or it could be your last meal.",
                "choices": [
                    {
                        "text": "Identify them carefully before touching",
                        "icon": "🔍",
                        "hours": 1,
                        "requires": [],
                        "success": 0.8,
                        "success_text": "You take your time. The ones with the honeycomb caps and hollow stems are chanterelles — delicious. The ones with white gills and a volva at the base are destroying angels — deadly. Knowledge saves lives.",
                        "success_fx": {"morale": 5, "hunger": 10, "foraging_bonus": True},
                        "fail_text": "You examine them carefully but can't be certain. Better to leave them than risk it. Your stomach growls in protest.",
                        "fail_fx": {"morale": -3}
                    },
                    {
                        "text": "Pick them all — you're hungry",
                        "icon": "🧺",
                        "hours": 0,
                        "requires": [],
                        "success": 0.3,
                        "success_text": "You pick everything and it turns out to be safe. Lucky. Very lucky. Don't make this a habit.",
                        "success_fx": {"hunger": 15, "morale": 3},
                        "fail_text": "You pick them greedily. Later, your stomach cramps violently. Some of those were NOT edible. You spend hours retching.",
                        "fail_fx": {"health": -25, "morale": -15}
                    },
                    {
                        "text": "Leave them — not worth the risk",
                        "icon": "🚫",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You back away from the mushrooms. Without certain identification, they could be deadly. Your caution is wise — but your stomach growls.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You leave the mushrooms. A safe choice, even if a hungry one.",
                        "fail_fx": {"morale": 2}
                    },
                    {
                        "text": "Use them as bait for animals instead",
                        "icon": "🪤",
                        "hours": 2,
                        "requires": [],
                        "success": 0.4,
                        "success_text": "You place the mushrooms near a game trail and wait. A rabbit takes the bait — now you have actual food without the risk.",
                        "success_fx": {"hunger": 20, "morale": 8},
                        "fail_text": "Nothing comes for the mushrooms. They wilt in the sun. Wasted time and potential food, though at least you didn't poison yourself.",
                        "fail_fx": {"morale": -5, "hunger": -3}
                    }
                ]
            },
            {
                "id": "dawn_fog",
                "name": "Morning Fog",
                "icon": "🌫️",
                "probability": 0.10,
                "seasons": ["Spring", "Autumn", "Winter"],
                "min_day": 1,
                "text": "You wake to thick fog. The world beyond your shelter has vanished. Every direction looks the same. Navigation will be dangerous today.",
                "choices": [
                    {
                        "text": "Stay at camp and do maintenance",
                        "icon": "🏕️",
                        "hours": 2,
                        "requires": [],
                        "success": 0.85,
                        "success_text": "You use the fog-bound day to improve your shelter, sort supplies, and rest. Sometimes the best move is to stay put. The fog lifts by afternoon.",
                        "success_fx": {"warmth": 5, "morale": 5, "shelter_progress": 1},
                        "fail_text": "You try to do maintenance but the damp makes everything harder. Your fingers are numb and the shelter doesn't improve much.",
                        "fail_fx": {"warmth": -2, "morale": -2}
                    },
                    {
                        "text": "Navigate carefully using landmarks",
                        "icon": "🧭",
                        "hours": 3,
                        "requires": ["compass"],
                        "success": 0.7,
                        "success_text": "Your compass keeps you on course. The fog is disorienting, but you manage to explore nearby without getting lost. You find something useful.",
                        "success_fx": {"morale": 5, "explore_bonus": 1},
                        "fail_text": "Even with the compass, the fog plays tricks. You waste time going in circles and end up back where you started, exhausted.",
                        "fail_fx": {"morale": -5, "hunger": -5}
                    },
                    {
                        "text": "Wait for the fog to lift before exploring",
                        "icon": "⏳",
                        "hours": 2,
                        "requires": [],
                        "success": 0.75,
                        "success_text": "You wait patiently. By midday the fog thins and the forest reveals itself. You explore in the afternoon with better visibility.",
                        "success_fx": {"morale": 3, "explore_bonus": 1},
                        "fail_text": "The fog doesn't lift all day. You've wasted hours waiting. Sometimes patience isn't rewarded.",
                        "fail_fx": {"morale": -5}
                    },
                    {
                        "text": "Mark your camp and explore carefully",
                        "icon": "📍",
                        "hours": 2,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You mark trees around your camp and venture out carefully. The marks guide you back. You discover a new area.",
                        "success_fx": {"morale": 5, "explore_bonus": 1},
                        "fail_text": "You mark your path but the fog is too thick. You lose your marks and stumble around before finding your way back by luck. Never again.",
                        "fail_fx": {"morale": -10, "health": -5}
                    }
                ]
            },
            {
                "id": "bird_alarm",
                "name": "Bird Alarm Call",
                "icon": "🐦",
                "probability": 0.07,
                "seasons": ["Spring", "Summer"],
                "min_day": 2,
                "text": "Birds are alarm-calling nearby — sharp, repetitive calls. In the forest, this often means a predator is close. Or it could mean they've found food and are defending it.",
                "choices": [
                    {
                        "text": "Investigate — it might mean food nearby",
                        "icon": "🧭",
                        "hours": 1,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You follow the calls and find a berry-laden bush the birds were fighting over. Blackberries, ripe and abundant. The birds were right to be territorial.",
                        "success_fx": {"hunger": 15, "morale": 5},
                        "fail_text": "You follow the calls and disturb a fox. It bolts, and you get a face full of brambles for your trouble. The birds were warning you, not inviting you.",
                        "fail_fx": {"health": -5, "morale": -5}
                    },
                    {
                        "text": "Stay alert but continue your tasks",
                        "icon": "👀",
                        "hours": 0,
                        "requires": [],
                        "success": 0.8,
                        "success_text": "You keep one eye on the treeline but carry on. The alarm calls fade after an hour. Whatever the threat was, it moved on.",
                        "success_fx": {"morale": 0},
                        "fail_text": "You try to focus but the alarm calls unsettle you. You keep looking over your shoulder and accomplish less than you hoped.",
                        "fail_fx": {"morale": -5}
                    },
                    {
                        "text": "Climb to a vantage point and scan",
                        "icon": "🧗",
                        "hours": 2,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You climb a slope and scan the canopy. The birds are mobbing a hawk. Below them, you spot a deer trail that leads to water. Useful information.",
                        "success_fx": {"morale": 5, "explore_bonus": 1},
                        "fail_text": "You climb up but see nothing but trees. The alarm calls were about something small — maybe a cat. You've wasted energy climbing for nothing.",
                        "fail_fx": {"morale": -3, "hunger": -3}
                    },
                    {
                        "text": "Freeze and observe silently",
                        "icon": "🤫",
                        "hours": 1,
                        "requires": [],
                        "success": 0.55,
                        "success_text": "You stand perfectly still and watch. After ten minutes, you spot movement — a wildcat stalking something. It hasn't seen you. You memorize its direction and move the opposite way.",
                        "success_fx": {"morale": 3},
                        "fail_text": "You stand still for ages but see nothing. The calls were probably about a snake or weasel — not worth the time you spent.",
                        "fail_fx": {"morale": -2, "hunger": -2}
                    }
                ]
            }
        ],
        "endings": [
            {
                "id": "rescued",
                "name": "Rescued",
                "icon": "🚁",
                "type": "good",
                "condition": {"signal_progress": 7},
                "text": "The sound reaches you before you see it — the distant thrum of rotor blades. A search helicopter banks over the treeline. You wave frantically. The downdraft flattens the grass as it lands. 'Quite a survival story,' the paramedic says, wrapping a blanket around your shoulders. Quite a story indeed.",
                "summary": "You signalled for help and were rescued."
            },
            {
                "id": "found_road",
                "name": "Found the Road",
                "icon": "🛤️",
                "type": "good",
                "condition": {"explore_progress": 12},
                "text": "The trees thin. The ground levels. And there, cutting through the landscape like a scar, is a road. You stumble onto the tarmac, half-expecting it to vanish like a mirage. A car slows. 'Are you alright? We've been looking for you!' You're going home.",
                "summary": "You explored far enough to find civilisation."
            },
            {
                "id": "the_hermit",
                "name": "The Hermit",
                "icon": "🧔",
                "type": "good",
                "condition": {"days_survived": 40, "min_resources": 40},
                "text": "Day {day}. You've lost count, really. The shelter is solid. The stream provides. You know which plants are safe, where the deer trails lead, when the rain will come. The forest doesn't feel like an enemy anymore. It feels like home. Perhaps that should worry you. It doesn't.",
                "summary": "You survived 40+ days with stable resources. You've become one with the forest."
            },
            {
                "id": "seasoned_forager",
                "name": "Seasoned Forager",
                "icon": "🌿",
                "type": "good",
                "condition": {"plants_correct": 20},
                "text": "You can identify every plant you encounter with confidence. Hemlock from wild carrot. Lords and Ladies from wild garlic. The forest's pantry is open to you, and you know which doors to avoid. A search party eventually finds you, but you didn't really need rescuing. The forest was feeding you all along.",
                "summary": "You correctly identified 20+ plants. Your foraging knowledge kept you alive."
            },
            {
                "id": "poisoned",
                "name": "Fatal Mistake",
                "icon": "☠️",
                "type": "bad",
                "condition": {"health": 0, "cause": "poison"},
                "text": "The plant looked so similar. The leaves, the stem, the smell — almost identical. But 'almost' doesn't count in foraging. The poison works quickly. Your vision blurs. Your throat closes. The forest floor rises to meet you. The trees sway overhead, indifferent, as the light fades.",
                "summary": "A misidentified plant ended your journey. In real life, always be 100% certain before eating any wild plant."
            },
            {
                "id": "perished",
                "name": "The Forest Claims You",
                "icon": "🪦",
                "type": "bad",
                "condition": {"health": 0},
                "text": "Your body can't take any more. The cold, the hunger, the injuries — they've worn you down to nothing. The forest doesn't notice. The wind continues. The rain falls. Somewhere, a bird sings. The world goes on without you, as it always has.",
                "summary": "Your health reached zero. The wilderness was too much."
            }
        ]
    },
    "alaska_winter": {
        "id": "alaska_winter",
        "name": "Alaska Winter",
        "icon": "❄️",
        "difficulty": 3,
        "tagline": "Stranded in sub-zero wilderness",
        "desc": "A plane crash in the Alaskan interior. Sub-zero temperatures. Blinding snow. Limited food. This is survival at its most brutal — where warmth is life and every decision matters.",
        "intro": (
            "The impact threw you clear. The plane is a twisted wreck, burning against the white landscape. "
            "You survived. That's the only good news. The temperature is minus twenty. "
            "Wind cuts through your clothes like a blade. Night is coming, and in the Alaskan winter, "
            "night means death if you're not prepared. You have hours, maybe less. "
            "Find shelter. Make fire. Stay alive."
        ),
        "starting": {
            "health": 100,
            "hunger": 85,
            "warmth": 50,
            "morale": 50,
            "water": None
        },
        "decay": {
            "hunger": 10,
            "warmth": 15,
            "morale": 8,
            "water": 0
        },
        "weather_types": {
            "clear": {"warmth_mod": 2, "morale_mod": 3, "desc": "Bitterly cold but clear. Stars blaze at night.", "icon": "☀️"},
            "cloudy": {"warmth_mod": -3, "morale_mod": -2, "desc": "Grey sky, grey snow. No warmth in the light.", "icon": "☁️"},
            "snow": {"warmth_mod": -10, "morale_mod": -3, "desc": "Snow falls steadily. Visibility drops. Cold seeps into everything.", "icon": "🌨️"},
            "blizzard": {"warmth_mod": -25, "morale_mod": -8, "desc": "White-out. Wind howls. You cannot see 10 feet. Do not go outside.", "icon": "🌨️"},
            "freeze": {"warmth_mod": -20, "morale_mod": -5, "desc": "Deep freeze. Minus 40. Exposed skin freezes in minutes.", "icon": "🥶"},
        },
        "weather_chances": {
            "Winter": {"clear": 0.20, "cloudy": 0.25, "snow": 0.30, "blizzard": 0.15, "freeze": 0.10},
            "Spring": {"clear": 0.35, "cloudy": 0.30, "snow": 0.20, "blizzard": 0.10, "freeze": 0.05},
        },
        "start_season": "Winter",
        "season_cycle_days": 15,
        "hours_per_day": 10,
        "actions_per_day": 2,
        "bonus_action_morale": 80,
        "plant_habitats": ["Mountain", "Tundra", "Coniferous"],
        "locations": [
            {
                "id": "crash_site",
                "name": "Crash Site",
                "icon": "✈️",
                "desc": "The twisted wreckage of the plane. Some supplies may be salvageable. Wind whips through the fuselage.",
                "discovered": True,
                "foraging_quality": 0.2,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 1
            },
            {
                "id": "spruce_grove",
                "name": "Spruce Groveve",
                "icon": "🌲",
                "desc": "Dense spruce trees. Wind protection, firewood, and pine tips for tea. The most forgiving place in this frozen hell.",
                "discovered": False,
                "explore_hours": 2,
                "foraging_quality": 0.6,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 0
            },
            {
                "id": "frozen_lake",
                "name": "Frozen Lake",
                "icon": "🧊",
                "desc": "A vast frozen lake. Potential ice fishing if you can make a hole. The ice groans — check thickness carefully.",
                "discovered": False,
                "explore_hours": 3,
                "foraging_quality": 0.3,
                "shelter_bonus": False,
                "water_source": True,
                "signal_bonus": 1
            },
            {
                "id": "ridge",
                "name": "High Ridge",
                "icon": "⛰️",
                "desc": "Exposed, brutal, and visible for miles. The best place for a signal fire. The worst place to be caught in a storm.",
                "discovered": False,
                "explore_hours": 4,
                "foraging_quality": 0.1,
                "shelter_bonus": False,
                "water_source": False,
                "signal_bonus": 3,
                "wind_penalty": True
            },
            {
                "id": "cave",
                "name": "Cave",
                "icon": "🪨",
                "desc": "A natural cave in the hillside. Good shelter, but something might already live here.",
                "discovered": False,
                "explore_hours": 3,
                "foraging_quality": 0.1,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 0,
                "shelter_level": 2
            }
        ],
        "events": [
            {
                "id": "wolf_pack_alaska",
                "name": "Wolf Pack",
                "icon": "🐺",
                "probability": 0.10,
                "seasons": ["Winter", "Spring"],
                "min_day": 2,
                "text": "Not one wolf — three. They move between the trees like ghosts, tracking you. In the Alaskan winter, wolves are desperate too. They're not just curious.",
                "choices": [
                    {
                        "text": "Light your signal fire early",
                        "icon": "🔥",
                        "hours": 1,
                        "requires": ["wood"],
                        "success": 0.75,
                        "success_text": "You light everything you have. The blaze illuminates the treeline and the wolves retreat from the flames. But you've used precious fuel.",
                        "success_fx": {"warmth": 15, "morale": 5, "signal_progress": 1},
                        "fail_text": "Your hands are too cold. The fire won't catch. The wolves circle closer. You shout and wave, buying time, but they're not leaving.",
                        "fail_fx": {"health": -20, "morale": -15}
                    },
                    {
                        "text": "Back away toward your shelter",
                        "icon": "🏕️",
                        "hours": 1,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You move slowly backward, never turning your back. The wolves follow at a distance but your shelter is close. They won't come near the fire.",
                        "success_fx": {"morale": -5, "warmth": 5},
                        "fail_text": "You stumble in the snow. The wolves close the distance. One snaps at your leg. You kick out and scramble backward, but you're bleeding.",
                        "fail_fx": {"health": -25, "morale": -15}
                    },
                    {
                        "text": "Stand your ground and make noise",
                        "icon": "🗣️",
                        "hours": 0,
                        "requires": [],
                        "success": 0.55,
                        "success_text": "You scream into the frozen air, banging rocks together. The noise echoes off the hills. The wolves hesitate, then trot away. Your voice cracks from the cold.",
                        "success_fx": {"morale": 5},
                        "fail_text": "Your shout dies in the wind. The wolves are unimpressed. They fan out, surrounding you. You barely make it to cover, heart hammering.",
                        "fail_fx": {"health": -15, "morale": -20}
                    },
                    {
                        "text": "Climb a spruce tree",
                        "icon": "🌲",
                        "hours": 2,
                        "requires": [],
                        "success": 0.7,
                        "success_text": "You scramble up a spruce, the sharp needles tearing your hands. Below, the wolves pace and howl. After hours, they leave. You're cold but alive.",
                        "success_fx": {"health": -5, "warmth": -10, "morale": -5},
                        "fail_text": "The tree is iced over. Your grip fails. You fall into the snow as the wolves close in. You fight them off with desperate flailing, but not before taking damage.",
                        "fail_fx": {"health": -30, "morale": -20}
                    }
                ]
            },
            {
                "id": "blizzard_warning",
                "name": "Blizzard Incoming",
                "icon": "🌨️",
                "probability": 0.12,
                "seasons": ["Winter"],
                "min_day": 1,
                "text": "The wind shifts. The sky darkens from white to grey to black. Snow starts sideways. A blizzard is coming and you have maybe an hour before it hits hard.",
                "choices": [
                    {
                        "text": "Hunker down and reinforce shelter",
                        "icon": "🏕️",
                        "hours": 2,
                        "requires": ["wood"],
                        "success": 0.85,
                        "success_text": "You bank snow and spruce boughs around your shelter. The blizzard rages outside but your den holds. You ride it out in relative warmth.",
                        "success_fx": {"warmth": 10, "morale": 5, "shelter_progress": 1},
                        "fail_text": "The wind is faster than you. Half your reinforcement blows away before you can secure it. You survive, but the shelter is no better than before.",
                        "fail_fx": {"warmth": -5, "morale": -5}
                    },
                    {
                        "text": "Seek the cave for better shelter",
                        "icon": "🪨",
                        "hours": 2,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You push through the wind and find the cave. It's cold inside but out of the wind. The blizzard can't touch you here.",
                        "success_fx": {"warmth": 8, "morale": 5},
                        "fail_text": "You can't find the cave in the white-out. You stumble blind through the blizzard, losing all sense of direction. You make it back to your shelter by sheer luck.",
                        "fail_fx": {"warmth": -20, "health": -10, "morale": -15}
                    },
                    {
                        "text": "Ration your food and wait it out",
                        "icon": "🍖",
                        "hours": 0,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You eat what you have and curl up in your shelter. The blizzard howls for hours. When it passes, you're cold but alive.",
                        "success_fx": {"hunger": 5, "warmth": -10, "morale": -3},
                        "fail_text": "The blizzard lasts longer than expected. Your food runs out. The cold seeps in. By the time it passes, you're in bad shape.",
                        "fail_fx": {"hunger": -10, "warmth": -25, "morale": -10}
                    },
                    {
                        "text": "Melt snow for water while you can",
                        "icon": "💧",
                        "hours": 1,
                        "requires": [],
                        "success": 0.8,
                        "success_text": "You stock up on water before the blizzard makes it impossible. Melting snow with body heat or a small fire. Hydration is survival.",
                        "success_fx": {"morale": 3, "inventory_add": ["water"]},
                        "fail_text": "You try to melt snow but your fire won't stay lit in the rising wind. The water you make freezes before you can drink it all.",
                        "fail_fx": {"warmth": -8, "morale": -5}
                    }
                ]
            },
            {
                "id": "crack_ice",
                "name": "Ice Cracks",
                "icon": "🧊",
                "probability": 0.08,
                "seasons": ["Winter", "Spring"],
                "min_day": 3,
                "text": "You're near the frozen lake when the ice groans. A crack spreads across the surface like lightning. The ice is shifting.",
                "choices": [
                    {
                        "text": "Get off the ice immediately",
                        "icon": "🏃",
                        "hours": 0,
                        "requires": [],
                        "success": 0.9,
                        "success_text": "You back away from the lake quickly. The ice cracks but doesn't break through. Close call.",
                        "success_fx": {"morale": -3},
                        "fail_text": "You run but the ice gives way beneath your feet. You plunge into freezing water. The shock is immediate and terrible.",
                        "fail_fx": {"health": -30, "warmth": -40, "morale": -20}
                    },
                    {
                        "text": "Cautiously test the ice thickness",
                        "icon": "🧊",
                        "hours": 1,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You carefully chip at the ice. It's thick enough near the shore but thin further out. Good to know — you mark the safe zones for ice fishing later.",
                        "success_fx": {"morale": 3},
                        "fail_text": "The ice shifts while you're testing. You fall through to your waist. The cold is agonising. You pull yourself out, soaking wet and freezing.",
                        "fail_fx": {"health": -20, "warmth": -30, "morale": -15}
                    },
                    {
                        "text": "Use the crack to fish — thin ice means open water",
                        "icon": "🐟",
                        "hours": 2,
                        "requires": [],
                        "success": 0.35,
                        "success_text": "You widen the crack and drop a makeshift line. After an agonising wait, a fish bites. Real food! Protein in the frozen wilderness.",
                        "success_fx": {"hunger": 20, "morale": 10, "inventory_add": ["fish"]},
                        "fail_text": "You try to fish but the crack seals over with fresh ice. Your line freezes. No fish, and you've been standing on ice for hours.",
                        "fail_fx": {"warmth": -15, "morale": -5}
                    },
                    {
                        "text": "Mark the danger zone and leave",
                        "icon": "📍",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You mark the danger zone with spruce branches and retreat. The lake is not safe today. Wisdom is knowing when not to push your luck.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You mark the area and leave. The ice groans behind you. Smart choice.",
                        "fail_fx": {"morale": 2}
                    }
                ]
            },
            {
                "id": "aurora",
                "name": "Aurora Borealis",
                "icon": "🌌",
                "probability": 0.06,
                "seasons": ["Winter"],
                "min_day": 3,
                "text": "You look up and the sky is alive. Green and purple ribbons of light dance across the stars. The aurora borealis. In this frozen hell, something breathtakingly beautiful.",
                "choices": [
                    {
                        "text": "Watch and find peace",
                        "icon": "🌌",
                        "hours": 1,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You stand in the snow and watch. For a moment, the cold doesn't matter. The world is vast and strange and beautiful, and you are part of it. Something in you shifts. You will survive this.",
                        "success_fx": {"morale": 20},
                        "fail_text": "Even the aurora can't lift your spirits tonight. You've seen too much. But you keep watching anyway. It's still beautiful.",
                        "fail_fx": {"morale": 5}
                    },
                    {
                        "text": "Use the clear night to signal",
                        "icon": "📡",
                        "hours": 2,
                        "requires": ["wood"],
                        "success": 0.7,
                        "success_text": "The clear sky that comes with the aurora is perfect for a signal fire. You build it high and bright. If anyone is looking, they'll see this.",
                        "success_fx": {"signal_progress": 2, "morale": 10, "warmth": -5},
                        "fail_text": "The fire burns but no one comes. Still, the aurora above makes you feel less alone. Something out there is watching.",
                        "fail_fx": {"signal_progress": 1, "morale": 5, "warmth": -5}
                    },
                    {
                        "text": "Collect ice for water while it's clear",
                        "icon": "💧",
                        "hours": 1,
                        "requires": [],
                        "success": 0.8,
                        "success_text": "Clear, cold nights mean clean ice. You collect chunks to melt later. Under the dancing lights, even this chore feels meaningful.",
                        "success_fx": {"morale": 5, "inventory_add": ["water"]},
                        "fail_text": "The ice is too hard to break. You chip away at it but make little progress. The aurora is beautiful though.",
                        "fail_fx": {"morale": 3}
                    },
                    {
                        "text": "Stay in shelter — it's too cold to admire the view",
                        "icon": "🏕️",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You stay in your shelter. The aurora is visible through gaps in the roof. You watch from warmth. Beauty doesn't require suffering.",
                        "success_fx": {"morale": 8, "warmth": 3},
                        "fail_text": "You stay warm and catch glimpses of the lights. It's enough.",
                        "fail_fx": {"morale": 5, "warmth": 3}
                    }
                ]
            },
            {
                "id": "frozen_hands",
                "name": "Frostnip Warning",
                "icon": "🥶",
                "probability": 0.10,
                "seasons": ["Winter"],
                "min_day": 2,
                "text": "Your fingers are white and numb. The early stages of frostnip. If you don't warm them soon, frostbite follows — and that means losing fingers.",
                "choices": [
                    {
                        "text": "Warm hands against your body",
                        "icon": "🤲",
                        "hours": 1,
                        "requires": [],
                        "success": 0.85,
                        "success_text": "You tuck your hands under your arms and wait. The pins and needles are agonising as circulation returns, but it means your fingers are alive. You need better gloves.",
                        "success_fx": {"health": -2, "morale": -2},
                        "fail_text": "Your body heat isn't enough. The warmth returns slowly, painfully. Some damage has been done but you still have your fingers. Barely.",
                        "fail_fx": {"health": -10, "morale": -8}
                    },
                    {
                        "text": "Build a fire immediately",
                        "icon": "🔥",
                        "hours": 1,
                        "requires": ["wood"],
                        "success": 0.75,
                        "success_text": "You get a fire going and hold your hands near the flames. The pain is intense but the warmth saves your fingers. Never take hands for granted.",
                        "success_fx": {"warmth": 10, "health": -2, "morale": 3},
                        "fail_text": "Your hands are too numb to manage the kindling. You can't start a fire. You'll have to use body heat instead. Slow, painful warming.",
                        "fail_fx": {"health": -8, "morale": -5}
                    },
                    {
                        "text": "Wrap hands in spare clothing",
                        "icon": "🧤",
                        "hours": 1,
                        "requires": [],
                        "success": 0.7,
                        "success_text": "You tear a strip from your spare clothing and wrap your hands. It's not much but it's enough to stop the cold from progressing. You need to keep moving.",
                        "success_fx": {"health": -3, "morale": -2},
                        "fail_text": "The wrapping isn't enough. Your fingers throb with cold. You need real warmth, not fabric alone.",
                        "fail_fx": {"health": -10, "morale": -8}
                    },
                    {
                        "text": "Keep moving — circulation will save you",
                        "icon": "🏃",
                        "hours": 1,
                        "requires": [],
                        "success": 0.45,
                        "success_text": "You swing your arms, clap your hands, keep moving. The blood flows back to your fingertips. It hurts like hell but it works. You're not losing any digits today.",
                        "success_fx": {"health": -3, "morale": 3, "hunger": -3},
                        "fail_text": "You try to keep moving but exhaustion is catching up with you. Your hands don't warm properly. You need to stop and address this properly.",
                        "fail_fx": {"health": -12, "morale": -10}
                    }
                ]
            },
            {
                "id": "trapper_cabin",
                "name": "Old Trapper's Trail",
                "icon": "👣",
                "probability": 0.08,
                "seasons": ["Winter", "Spring"],
                "min_day": 4,
                "text": "You find a trail — not animal, but human. Boot prints in the snow, days old. Someone has been here before you. The trail leads somewhere.",
                "choices": [
                    {
                        "text": "Follow the trail",
                        "icon": "🧭",
                        "hours": 3,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "The trail leads to a trapper's cabin! Old but intact. Inside: a stove, some supplies, and a radio that might work. You've found sanctuary.",
                        "success_fx": {"morale": 20, "warmth": 15, "explore_bonus": 2, "discover": "cabin"},
                        "fail_text": "The trail fades in the snow. You follow it for hours but it leads nowhere. The tracks are too old and the wind has erased them. You're exhausted and cold.",
                        "fail_fx": {"warmth": -10, "morale": -10, "hunger": -5}
                    },
                    {
                        "text": "Mark it and check the direction later",
                        "icon": "📍",
                        "hours": 1,
                        "requires": [],
                        "success": 0.75,
                        "success_text": "You mark the trail and note the direction. If you explore that way later, you might find where it leads. For now, you conserve energy.",
                        "success_fx": {"morale": 3, "explore_bonus": 1},
                        "fail_text": "You mark the trail but the next snowfall covers your markers. The trail may be lost, but you remember the direction.",
                        "fail_fx": {"morale": -2}
                    },
                    {
                        "text": "Search the immediate area for supplies",
                        "icon": "🔍",
                        "hours": 2,
                        "requires": [],
                        "success": 0.55,
                        "success_text": "Near the trail, you find signs of a camp — a broken snare, some wire, a rusted can. Salvageable materials. The previous occupant was resourceful.",
                        "success_fx": {"morale": 5, "inventory_add": ["wire", "can"]},
                        "fail_text": "The area around the trail is picked clean. Whoever came through here took everything. You find nothing but their footprints.",
                        "fail_fx": {"morale": -5}
                    },
                    {
                        "text": "Ignore it — could be a trap",
                        "icon": "🚫",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You've seen too many movies. Old trails could mean danger. You mark the direction in case you change your mind, then continue your own path.",
                        "success_fx": {"morale": 0},
                        "fail_text": "You ignore the trail and continue. Maybe you missed something useful, but caution keeps you alive.",
                        "fail_fx": {"morale": 0}
                    }
                ]
            }
        ],
        "endings": [
            {
                "id": "rescued_alaska",
                "name": "Rescued",
                "icon": "🚁",
                "type": "good",
                "condition": {"signal_progress": 7},
                "text": "The helicopter appears like a miracle against the grey sky. It lands in a flurry of snow. 'We got your signal!' the pilot shouts over the rotor. They wrap you in a thermal blanket. 'Toughest son of a bitch I've ever seen out here,' the medic says. You don't argue.",
                "summary": "Your signal fire was spotted. Rescue came."
            },
            {
                "id": "long_walk",
                "name": "The Long Walk",
                "icon": "🛤️",
                "type": "good",
                "condition": {"explore_progress": 12},
                "text": "You follow the river valley for what feels like forever. Then — a road. A real road, with tyre tracks in the snow. You stumble onto the tarmac and a truck stops. The driver stares. 'I thought you were dead.' Not yet. Not today.",
                "summary": "You explored far enough to find civilisation."
            },
            {
                "id": "trappers_life",
                "name": "Trapper's Life",
                "icon": "🪓",
                "type": "good",
                "condition": {"days_survived": 35, "min_resources": 40},
                "text": "Day {day}. The cabin is warm. The stove glows. Outside, the snow falls, but you've got firewood enough for weeks. You've learned which pine tips make tea, which tracks mean rabbits, how to read the sky for storms. Alaska tried to kill you. It failed.",
                "summary": "You survived 35+ days in the Alaskan wilderness. You've adapted."
            },
            {
                "id": "frozen",
                "name": "Frozen",
                "icon": "🥶",
                "type": "bad",
                "condition": {"warmth": 0},
                "text": "The cold takes you gently in the end. You stop shivering — that's the dangerous sign, the one they warn you about. Your thoughts slow. The snow feels warm, soft, inviting. Lie down. Just for a moment. The aurora dances above you, beautiful and indifferent.",
                "summary": "Your warmth reached zero. Hypothermia claimed you. In real life, never stop moving if you're cold."
            },
            {
                "id": "wolf_kill_alaska",
                "name": "Wolf Kill",
                "icon": "🐺",
                "type": "bad",
                "condition": {"health": 0, "cause": "wolf"},
                "text": "The wolves were always there, just beyond the treeline. Patient. They knew you'd weaken eventually. The cold, the hunger, the exhaustion — it all led to this. The pack closes in. You were never the predator here.",
                "summary": "The wolves won. In wolf country, always have fire and never turn your back."
            },
            {
                "id": "broken",
                "name": "Broken",
                "icon": "💔",
                "type": "bad",
                "condition": {"health": 0},
                "text": "Your body gave out. Injuries, cold, hunger — too much for too long. The Alaskan winter doesn't forgive weakness. It doesn't negotiate. It simply waits until you can't fight anymore. The snow covers everything eventually.",
                "summary": "Your health reached zero. The wilderness was too much."
            }
        ]
    },
    "desert": {
        "id": "desert",
        "name": "Desert",
        "icon": "🏜️",
        "difficulty": 4,
        "tagline": "Stranded in scorching desert",
        "desc": "Your vehicle broke down on a remote desert track. The nearest settlement is days away. Water is your most precious resource — and it's running out. The desert is beautiful and deadly in equal measure.",
        "intro": (
            "The engine coughs, sputters, and dies. The temperature gauge has been in the red for an hour. "
            "You're miles from the last settlement, on a track that nobody uses anymore. "
            "The sun is brutal. The sand stretches in every direction. "
            "You have half a bottle of water, a broken radio, and a decision: "
            "stay with the vehicle and hope someone comes, or walk. "
            "Either way, the desert doesn't care. It will be 40°C by midday and near freezing tonight."
        ),
        "starting": {
            "health": 100,
            "hunger": 80,
            "warmth": 100,
            "morale": 55,
            "water": 60
        },
        "decay": {
            "hunger": 8,
            "warmth": 0,
            "morale": 6,
            "water": 20
        },
        "weather_types": {
            "scorching": {"water_mod": -15, "morale_mod": -5, "warmth_mod": -10, "desc": "Relentless sun. The air shimmers. The sand burns to touch. Every step costs water.", "icon": "☀️"},
            "hot_clear": {"water_mod": -10, "morale_mod": -2, "warmth_mod": 0, "desc": "Hot and clear. The horizon wavers with heat. Seek shade during midday.", "icon": "🌤️"},
            "windy": {"water_mod": -8, "morale_mod": -3, "warmth_mod": -5, "desc": "A hot wind blows sand and dust. It gets in everything — eyes, mouth, clothes.", "icon": "💨"},
            "cold_night": {"water_mod": 5, "morale_mod": -3, "warmth_mod": -15, "desc": "The temperature plummets. Without shelter, the cold bites harder than the sun.", "icon": "🌙"},
            "sandstorm": {"water_mod": -5, "morale_mod": -10, "warmth_mod": -8, "desc": "A wall of sand approaches. Visibility drops to zero. Sand gets into everything.", "icon": "🏜️"},
        },
        "weather_chances": {
            "Spring": {"scorching": 0.30, "hot_clear": 0.35, "windy": 0.20, "cold_night": 0.10, "sandstorm": 0.05},
            "Summer": {"scorching": 0.45, "hot_clear": 0.30, "windy": 0.10, "cold_night": 0.10, "sandstorm": 0.05},
        },
        "start_season": "Spring",
        "season_cycle_days": 12,
        "hours_per_day": 14,
        "actions_per_day": 2,
        "bonus_action_morale": 75,
        "plant_habitats": ["Desert", "Arid", "Rocky"],
        "locations": [
            {
                "id": "vehicle",
                "name": "Broken Vehicle",
                "icon": "🚗",
                "desc": "Your dead vehicle. Some shade, some metal to work with. The only landmark for miles.",
                "discovered": True,
                "foraging_quality": 0.1,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 2
            },
            {
                "id": "rocky_canyon",
                "name": "Rocky Canyon",
                "icon": "🪨",
                "desc": "Red rock walls carved by ancient water. Shade in the gaps. Possible water trapped in rock pools.",
                "discovered": False,
                "explore_hours": 3,
                "foraging_quality": 0.5,
                "shelter_bonus": True,
                "water_source": False,
                "signal_bonus": 0
            },
            {
                "id": "dry_riverbed",
                "name": "Dry Riverbed",
                "icon": "🏜️",
                "desc": "A cracked riverbed. Dry on the surface, but water may flow beneath. Animal tracks lead here.",
                "discovered": False,
                "explore_hours": 2,
                "foraging_quality": 0.3,
                "shelter_bonus": False,
                "water_source": True,
                "signal_bonus": 0
            },
            {
                "id": "cactus_grove",
                "name": "Cactus Groveve",
                "icon": "🌵",
                "desc": "A cluster of prickly pear and saguaro. The only green for miles. Food and shade, if you know how to harvest safely.",
                "discovered": False,
                "explore_hours": 2,
                "foraging_quality": 0.9,
                "shelter_bonus": False,
                "water_source": False,
                "signal_bonus": 0
            },
            {
                "id": "high_plateau",
                "name": "High Plateau",
                "icon": "⛰️",
                "desc": "A raised flat of rock. Brutal sun during the day, but visible for miles. Best spot for a signal.",
                "discovered": False,
                "explore_hours": 4,
                "foraging_quality": 0.1,
                "shelter_bonus": False,
                "water_source": False,
                "signal_bonus": 3,
                "wind_penalty": True
            }
        ],
        "events": [
            {
                "id": "snake_encounter",
                "name": "Snake!",
                "icon": "🐍",
                "probability": 0.10,
                "seasons": ["Spring", "Summer"],
                "min_day": 2,
                "text": "A rattling sound. A snake coils in your path, triangular head raised, tail buzzing a warning. It's between you and your destination.",
                "choices": [
                    {
                        "text": "Give it a wide berth and go around",
                        "icon": "🚶",
                        "hours": 1,
                        "requires": [],
                        "success": 0.9,
                        "success_text": "You backtrack and circle wide around the snake. It watches you go but doesn't follow. Smart move. In the desert, every snake should be treated as venomous.",
                        "success_fx": {"morale": -2, "water": -3},
                        "fail_text": "You try to go around but the ground is rocky and uneven. By the time you've detoured, you've spent extra water and energy in the heat.",
                        "fail_fx": {"morale": -5, "water": -5}
                    },
                    {
                        "text": "Stand still and wait for it to leave",
                        "icon": "🤫",
                        "hours": 1,
                        "requires": [],
                        "success": 0.7,
                        "success_text": "You freeze. After a tense minute, the snake slowly uncoils and slides away into the rocks. Patience saves you. And possibly your leg.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You wait and wait but the snake holds its ground. After an hour in the sun, you're forced to retreat. Dehydrated and frustrated.",
                        "fail_fx": {"water": -8, "morale": -5}
                    },
                    {
                        "text": "Try to kill it for food",
                        "icon": "🔪",
                        "hours": 1,
                        "requires": [],
                        "success": 0.3,
                        "success_text": "You find a long rock and strike quickly. The snake is dispatched. Snake meat is protein — in the desert, you don't waste food. But the risk was enormous.",
                        "success_fx": {"hunger": 20, "morale": 5},
                        "fail_text": "You lunge but the snake is faster. It strikes, and fangs sink into your ankle. Venom burns through your veins. This is very, very bad.",
                        "fail_fx": {"health": -40, "morale": -20, "water": -10}
                    },
                    {
                        "text": "Throw sand at it to scare it off",
                        "icon": "✋",
                        "hours": 0,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You scoop sand and throw it at the snake. The disturbance startles it and it slides away rapidly. Good instinct.",
                        "success_fx": {"morale": 3},
                        "fail_text": "The sand misses. The snake is now agitated and strikes at you as you jump back. No bite, but you fall hard on the rocks.",
                        "fail_fx": {"health": -10, "morale": -10}
                    }
                ]
            },
            {
                "id": "sandstorm_desert",
                "name": "Sandstorm",
                "icon": "🏜️",
                "probability": 0.10,
                "seasons": ["Spring", "Summer"],
                "min_day": 2,
                "text": "The sky turns orange. A wall of sand approaches from the west, hundreds of feet high. You have minutes to find cover.",
                "choices": [
                    {
                        "text": "Shelter behind your vehicle",
                        "icon": "🚗",
                        "hours": 0,
                        "requires": [],
                        "success": 0.8,
                        "success_text": "You hunker down behind the vehicle, using a door as a windbreak. Sand blasts past. It's in your eyes, your mouth, but the worst misses you. The storm passes in an hour.",
                        "success_fx": {"health": -3, "morale": -3},
                        "fail_text": "The sand finds every gap. You're coated in dust, choking, eyes streaming. The storm lasts hours. Your water is contaminated with sand.",
                        "fail_fx": {"health": -10, "morale": -10, "water": -10}
                    },
                    {
                        "text": "Find the rocky canyon for shelter",
                        "icon": "🪨",
                        "hours": 1,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You sprint for the canyon as the sandstorm hits. You make it just in time. The rock walls protect you. You wait it out in relative comfort.",
                        "success_fx": {"health": -2, "morale": 3, "water": -3},
                        "fail_text": "You can't see the canyon in the sand. You stumble blindly, falling over rocks, mouth full of sand. You eventually find shelter but you're battered.",
                        "fail_fx": {"health": -15, "morale": -10, "water": -8}
                    },
                    {
                        "text": "Cover yourself and lie flat on the ground",
                        "icon": "🧎",
                        "hours": 1,
                        "requires": [],
                        "success": 0.65,
                        "success_text": "You wrap your clothing over your face and lie flat. Sand scourges overhead. It's terrifying but effective. The storm passes and you're still here.",
                        "success_fx": {"health": -2, "morale": -5},
                        "fail_text": "Lying on the ground, sand piles up around you. You're being buried. You thrash free but you've inhaled a lot of dust.",
                        "fail_fx": {"health": -10, "morale": -8}
                    },
                    {
                        "text": "Use the storm to collect condensation",
                        "icon": "💧",
                        "hours": 1,
                        "requires": [],
                        "success": 0.4,
                        "success_text": "In the chaos of the storm, temperature drops create condensation on metal and rock. You collect precious drops of water. A storm that gives instead of only taking.",
                        "success_fx": {"water": 15, "morale": 5},
                        "fail_text": "You try to collect condensation but the sand makes it undrinkable. You waste time and water in the attempt.",
                        "fail_fx": {"water": -5, "morale": -5}
                    }
                ]
            },
            {
                "id": "mirage",
                "name": "Mirage",
                "icon": "🌅",
                "probability": 0.07,
                "seasons": ["Spring", "Summer"],
                "min_day": 3,
                "text": "Shimmering on the horizon — water? Trees? A building? It looks so real. Your parched throat screams at you to run towards it. But is it real?",
                "choices": [
                    {
                        "text": "Walk towards it carefully",
                        "icon": "🚶",
                        "hours": 3,
                        "requires": [],
                        "success": 0.3,
                        "success_text": "You walk for hours. As you get closer, it doesn't disappear. It's real! An oasis — small, but real. You've never been so grateful for water.",
                        "success_fx": {"water": 30, "morale": 15, "discover": "oasis"},
                        "fail_text": "You walk for hours towards the shimmering. As you approach, it vanishes. Mirage. You've wasted precious water and energy on nothing. The desert laughs.",
                        "fail_fx": {"water": -15, "morale": -15, "health": -5}
                    },
                    {
                        "text": "Mark the direction but don't follow",
                        "icon": "📍",
                        "hours": 0,
                        "requires": [],
                        "success": 0.85,
                        "success_text": "You note the direction. If it's real, it'll still be there tomorrow when you're better prepared. If it's a mirage, you've saved yourself a fatal walk.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You mark the direction. Part of you wonders if it could have been real. But caution keeps you alive in the desert.",
                        "fail_fx": {"morale": 0}
                    },
                    {
                        "text": "Send a signal instead — use the energy wisely",
                        "icon": "📡",
                        "hours": 2,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "Instead of chasing a mirage, you use the clear day for a signal fire. Smoke rises in the still air. If anyone is looking, they'll see it.",
                        "success_fx": {"signal_progress": 1, "water": -5, "morale": 3},
                        "fail_text": "The signal fire is smoky but the air is too still. It doesn't rise high enough. At least you didn't chase the mirage.",
                        "fail_fx": {"signal_progress": 0, "water": -5, "morale": -3}
                    },
                    {
                        "text": "Wait and observe for an hour",
                        "icon": "👁️",
                        "hours": 1,
                        "requires": [],
                        "success": 0.6,
                        "success_text": "You watch the shape on the horizon. After an hour, the angle of the sun changes and it wavers — it's a mirage. Good thing you didn't walk for it.",
                        "success_fx": {"morale": 5},
                        "fail_text": "You watch but can't tell if it's real or not. The uncertainty gnaws at you. Water is so close... or isn't there at all.",
                        "fail_fx": {"morale": -5, "water": -2}
                    }
                ]
            },
            {
                "id": "flash_flood",
                "name": "Flash Flood Warning",
                "icon": "🌊",
                "probability": 0.06,
                "seasons": ["Spring"],
                "min_day": 3,
                "text": "The sky darkens. You're in a low area. The ground starts to feel damp. In the desert, rain miles away can send walls of water through dry channels. You have minutes.",
                "choices": [
                    {
                        "text": "Climb to higher ground immediately",
                        "icon": "⛰️",
                        "hours": 1,
                        "requires": [],
                        "success": 0.85,
                        "success_text": "You scramble up the rocky slope just as water thunders through the channel below. It's terrifying and awe-inspiring. And now there are pools of water trapped in the rocks above.",
                        "success_fx": {"water": 20, "morale": 5},
                        "fail_text": "You climb but the water comes faster than expected. A wave catches your legs. You're swept briefly before grabbing a rock. Soaked, shaken, but alive.",
                        "fail_fx": {"health": -15, "water": -5, "morale": -10}
                    },
                    {
                        "text": "Ride it out in the vehicle",
                        "icon": "🚗",
                        "hours": 1,
                        "requires": [],
                        "success": 0.5,
                        "success_text": "You stay in the vehicle. Water rushes around it but the wheels hold. The flood passes. The vehicle is now stuck in mud, but you're alive and dry.",
                        "success_fx": {"morale": -3, "water": -3},
                        "fail_text": "The water rises higher than expected. The vehicle shifts. You barely escape before it's swept away. You've lost your base and some supplies.",
                        "fail_fx": {"health": -10, "morale": -15, "water": -10}
                    },
                    {
                        "text": "Run for the canyon walls",
                        "icon": "🪨",
                        "hours": 1,
                        "requires": [],
                        "success": 0.65,
                        "success_text": "You sprint for the canyon walls. The rock overhangs provide shelter from both water and the debris it carries. You watch the flood rage below, safely elevated.",
                        "success_fx": {"morale": 5},
                        "fail_text": "You run but don't make it to the canyon before the water hits. You're swept off your feet. You grab a rock and hold on until the water subsides.",
                        "fail_fx": {"health": -20, "morale": -15}
                    },
                    {
                        "text": "Use the flood to collect water",
                        "icon": "💧",
                        "hours": 1,
                        "requires": [],
                        "success": 0.45,
                        "success_text": "You position containers and dig channels. The flood water fills everything. It's brown and gritty, but it's water. You'll filter it later. This could save your life.",
                        "success_fx": {"water": 35, "morale": 10},
                        "fail_text": "The water comes too fast. Your containers are swept away. You nearly are too. The flood takes everything it touches.",
                        "fail_fx": {"water": -10, "morale": -15, "health": -10}
                    }
                ]
            },
            {
                "id": "vultures",
                "name": "Vultures Circling",
                "icon": "🦅",
                "probability": 0.06,
                "seasons": ["Spring", "Summer"],
                "min_day": 3,
                "text": "Vultures circle overhead. They're not looking at you — yet. They've found something dead nearby. Where there's death, there might also be salvageable supplies. Or disease.",
                "choices": [
                    {
                        "text": "Investigate what they've found",
                        "icon": "🔍",
                        "hours": 2,
                        "requires": [],
                        "success": 0.45,
                        "success_text": "You find the carcass of a desert animal. Nearby, caught in brush — a discarded water bottle and a sun-bleached backpack with a working lighter inside. One person's tragedy is another's lifeline.",
                        "success_fx": {"water": 10, "morale": 3, "inventory_add": ["lighter", "backpack"]},
                        "fail_text": "You find the carcass but nothing useful. The smell is horrific and flies swarm. You retreat, gagging. The desert gives nothing freely.",
                        "fail_fx": {"morale": -8, "water": -3}
                    },
                    {
                        "text": "Stay away — it could be diseased",
                        "icon": "🚫",
                        "hours": 0,
                        "requires": [],
                        "success": 1.0,
                        "success_text": "You stay clear. Smart move. Dead things in the desert carry disease. The vultures will clean it up. You keep your distance and your health.",
                        "success_fx": {"morale": -2},
                        "fail_text": "You stay away. The vultures continue their grim work. You focus on what's ahead, not what's behind.",
                        "fail_fx": {"morale": -2}
                    },
                    {
                        "text": "Watch where the vultures roost — they know water",
                        "icon": "🦅",
                        "hours": 2,
                        "requires": [],
                        "success": 0.4,
                        "success_text": "You track the vultures to their roosting spot. Nearby, a seep in the rock face collects morning dew. The birds know where the water is. So do you now.",
                        "success_fx": {"water": 20, "morale": 8},
                        "fail_text": "The vultures circle endlessly. You can't find where they roost. Hours of watching and you've only depleted your water supply.",
                        "fail_fx": {"water": -8, "morale": -5}
                    },
                    {
                        "text": "Use the shade of their circling as a time marker",
                        "icon": "⏰",
                        "hours": 0,
                        "requires": [],
                        "success": 0.9,
                        "success_text": "You note the sun's position by the vultures' shadow patterns. It's later than you thought. You adjust your plans accordingly. In the desert, time management is survival.",
                        "success_fx": {"morale": 2},
                        "fail_text": "You try to read the time but the vultures scatter. At least you remembered to check the sun.",
                        "fail_fx": {"morale": 0}
                    }
                ]
            },
            {
                "id": "cold_night_desert",
                "name": "Freezing Night",
                "icon": "🌙",
                "probability": 0.12,
                "seasons": ["Spring", "Summer"],
                "min_day": 2,
                "text": "The sun vanishes and the temperature plummets. Desert nights are brutally cold. Without proper shelter, hypothermia is a real threat.",
                "choices": [
                    {
                        "text": "Build an insulated sleeping spot",
                        "icon": "🏕️",
                        "hours": 2,
                        "requires": ["wood"],
                        "success": 0.8,
                        "success_text": "You pile sand and rock around your sleeping area and start a small fire. The heat reflects off the rocks. It's not comfortable, but you're warm enough to sleep.",
                        "success_fx": {"warmth": 15, "morale": 5},
                        "fail_text": "The fire won't hold. Sand insulates poorly. You shiver through the night, dozing in short bursts. Morning can't come fast enough.",
                        "fail_fx": {"warmth": -10, "morale": -8}
                    },
                    {
                        "text": "Stay in the vehicle for warmth",
                        "icon": "🚗",
                        "hours": 0,
                        "requires": [],
                        "success": 0.7,
                        "success_text": "The vehicle retains some heat from the day. You curl up inside and it's bearable. Not warm, but not freezing. You survive the night.",
                        "success_fx": {"warmth": 5, "morale": 0},
                        "fail_text": "The vehicle has lost all its heat. Metal conducts cold. It's worse inside than out. You shiver violently until dawn.",
                        "fail_fx": {"warmth": -15, "morale": -5}
                    },
                    {
                        "text": "Exercise throughout the night to stay warm",
                        "icon": "🏃",
                        "hours": 4,
                        "requires": [],
                        "success": 0.45,
                        "success_text": "You pace, jog in place, do press-ups. It keeps you warm but uses enormous energy. By dawn you're exhausted but alive. You'll need more food and water today.",
                        "success_fx": {"warmth": 5, "hunger": -10, "water": -8, "morale": -3},
                        "fail_text": "By 3am you can't keep moving. Exhaustion and cold win. You curl up shivering and hope for dawn. The longest night of your life.",
                        "fail_fx": {"warmth": -20, "health": -10, "morale": -15}
                    },
                    {
                        "text": "Use rocks that retain heat from the day",
                        "icon": "🪨",
                        "hours": 1,
                        "requires": [],
                        "success": 0.65,
                        "success_text": "You find large rocks that baked in the sun all day. They radiate warmth as the temperature drops. You arrange them around your sleeping spot. Primitive heating that works.",
                        "success_fx": {"warmth": 8, "morale": 3},
                        "fail_text": "The rocks have already lost their heat. The sun went down hours ago and you missed the window. You're left with cold stone and cold air.",
                        "fail_fx": {"warmth": -10, "morale": -5}
                    }
                ]
            }
        ],
        "endings": [
            {
                "id": "rescued_desert",
                "name": "Rescued",
                "icon": "🚁",
                "type": "good",
                "condition": {"signal_progress": 7},
                "text": "A vehicle appears on the horizon. At first you think it's another mirage — but this one doesn't vanish. A truck bounces across the desert toward you. 'We saw your smoke!' the driver shouts. You've never been so happy to see a stranger.",
                "summary": "Your signal was spotted. Rescue came across the sand."
            },
            {
                "id": "the_oasis",
                "name": "The Oasis",
                "icon": "🌴",
                "type": "good",
                "condition": {"explore_progress": 12},
                "text": "You find water. Not a mirage — real water. A spring seeping from rock, surrounded by green. You drink until you're sick, then drink more. With water, everything is possible. You build shelter, harvest cactus fruit, and wait. Someone will come. You can survive anything now.",
                "summary": "You explored far enough to find an oasis. Water changes everything."
            },
            {
                "id": "riverbed_escape",
                "name": "The Riverbed Path",
                "icon": "🏞️",
                "type": "good",
                "condition": {"explore_progress": 10},
                "text": "You followed the dry riverbed for days. Water erosion cuts through terrain, and eventually, the riverbed led somewhere — a road. A real road with tyre tracks. You stumble onto the tarmac and a truck stops. The driver can't believe you're alive. Neither can you.",
                "summary": "You followed the riverbed to civilisation."
            },
            {
                "id": "dehydration",
                "name": "Dehydration",
                "icon": "💀",
                "type": "bad",
                "condition": {"water": 0},
                "text": "Your lips crack. Your tongue swells. Your vision blurs. The desert takes everything — your water, your strength, your will. The last thing you see is the sun, blazing overhead, indifferent and eternal. The sand will cover your tracks by morning.",
                "summary": "Your water reached zero. Dehydration claimed you. In real life, always prioritise finding water in survival situations."
            },
            {
                "id": "heatstroke",
                "name": "Heatstroke",
                "icon": "🌡️",
                "type": "bad",
                "condition": {"health": 0, "cause": "heat"},
                "text": "The world spins. Your skin burns dry. You stop sweating — that's the dangerous sign. Your body can't cool itself anymore. You collapse into the sand and the sun doesn't care. It never does.",
                "summary": "Heatstroke claimed you. In real life, always avoid exertion during the hottest part of the day in desert conditions."
            },
            {
                "id": "venomous_desert",
                "name": "Venomous Bite",
                "icon": "🐍",
                "type": "bad",
                "condition": {"health": 0, "cause": "poison"},
                "text": "The bite swells within minutes. Venom spreads through your veins. In the desert, hours from help, there's no antivenom. No hospital. No second chance. The snake was just being a snake. You were just being in the wrong place.",
                "summary": "A venomous creature ended your journey. In real life, always give snakes a wide berth and never handle unknown desert creatures."
            },
            {
                "id": "desert_perished",
                "name": "The Desert Claims You",
                "icon": "🪦",
                "type": "bad",
                "condition": {"health": 0},
                "text": "The desert doesn't hate you. It doesn't feel anything at all. That's what makes it so dangerous. It simply exists, and if you're not prepared, it simply removes you. The sand erases all traces. By tomorrow, there's no sign you were ever here.",
                "summary": "Your health reached zero. The desert was too much."
            }
        ]
    }
}

# ==========================================
# ACTION DEFINITIONS (shared across scenarios)
# ==========================================

QUEST_ACTIONS = {
    "forage": {
        "id": "forage",
        "name": "Forage",
        "icon": "🌿",
        "hours": 2,
        "desc": "Search for edible plants. Requires plant identification knowledge.",
        "requires": [],
        "category": "food"
    },
    "explore": {
        "id": "explore",
        "name": "Explore",
        "icon": "🧭",
        "hours": 3,
        "desc": "Search the area for new locations, resources, and paths.",
        "requires": [],
        "category": "discovery"
    },
    "build_shelter": {
        "id": "build_shelter",
        "name": "Build Shelter",
        "icon": "🏕️",
        "hours": 4,
        "desc": "Improve your shelter. Each level provides better protection.",
        "requires": [],
        "category": "survival"
    },
    "gather_wood": {
        "id": "gather_wood",
        "name": "Gather Wood",
        "icon": "🪵",
        "hours": 2,
        "desc": "Collect firewood and building materials.",
        "requires": [],
        "category": "resources",
        "gives": ["wood"]
    },
    "signal": {
        "id": "signal",
        "name": "Signal for Help",
        "icon": "📡",
        "hours": 2,
        "desc": "Build or maintain a signal fire. Progress toward rescue.",
        "requires": ["wood"],
        "category": "rescue"
    },
    "rest": {
        "id": "rest",
        "name": "Rest",
        "icon": "💤",
        "hours": 3,
        "desc": "Recover health and morale. Costs some food.",
        "requires": [],
        "category": "recovery"
    },
    "hunt": {
        "id": "hunt",
        "name": "Hunt / Set Traps",
        "icon": "🪤",
        "hours": 3,
        "desc": "Attempt to catch game. Low success rate without tools.",
        "requires": [],
        "category": "food"
    },
    "find_water": {
        "id": "find_water",
        "name": "Find Water",
        "icon": "💧",
        "hours": 2,
        "desc": "Search for a water source. Essential in the desert.",
        "requires": [],
        "category": "survival"
    },
    "craft": {
        "id": "craft",
        "name": "Craft Tool",
        "icon": "🔨",
        "hours": 2,
        "desc": "Craft a useful tool from available materials.",
        "requires": [],
        "category": "resources"
    }
}

# ==========================================
# SHELTER STAGES (per scenario)
# ==========================================

QUEST_SHELTER = {
    "wild_forest": [
        {"level": 0, "name": "No Shelter", "icon": "🌧️", "desc": "Exposed to the elements.", "warmth_bonus": 0},
        {"level": 1, "name": "Debris Pile", "icon": "🍃", "desc": "Leaves and branches heaped together. Barely better than nothing.", "warmth_bonus": 5},
        {"level": 2, "name": "Lean-to", "icon": "⛺", "desc": "A frame of branches covered in debris. Keeps most rain off.", "warmth_bonus": 10},
        {"level": 3, "name": "Improved Shelter", "icon": "🏕️", "desc": "Thatched roof, raised bed, wind break. A real home in the wild.", "warmth_bonus": 18},
    ],
    "alaska_winter": [
        {"level": 0, "name": "No Shelter", "icon": "🥶", "desc": "Exposed to the frozen wind. You will die without shelter.", "warmth_bonus": 0},
        {"level": 1, "name": "Snow Trench", "icon": "🌨️", "desc": "A dug-out trench in the snow. Blocks wind but freezing inside.", "warmth_bonus": 8},
        {"level": 2, "name": "Spruce Bough Shelter", "icon": "🌲", "desc": "Branches layered over a frame with spruce insulation.", "warmth_bonus": 15},
        {"level": 3, "name": "Insulated Snow Cave", "icon": "🪨", "desc": "Double-walled with snow insulation. Traps body heat.", "warmth_bonus": 25},
    ],
    "desert": [
        {"level": 0, "name": "No Shade", "icon": "☀️", "desc": "Fully exposed to the sun. Water drains fast.", "warmth_bonus": 0},
        {"level": 1, "name": "Sun Shade", "icon": "🫧", "desc": "A basic lean-to providing shade from the midday sun.", "warmth_bonus": 5},
        {"level": 2, "name": "Rock Shelter", "icon": "🪨", "desc": "Rocks arranged for shade and wind break. Cool by day, warmer by night.", "warmth_bonus": 10},
        {"level": 3, "name": "Desert Dwelling", "icon": "🏠", "desc": "Insulated walls, shade cloth, wind break. A desert home.", "warmth_bonus": 15},
    ]
}

# ==========================================
# CRAFTING RECIPES
# ==========================================

QUEST_CRAFTING = {
    "cordage": {
        "name": "Cordage",
        "icon": "🧶",
        "desc": "Rope from plant fibres. Essential for building and traps.",
        "requires": ["foraged_plants"],
        "hours": 2,
        "unlocks": ["snare", "improved_shelter"]
    },
    "snare": {
        "name": "Snare Trap",
        "icon": "🪤",
        "desc": "A simple animal trap. Requires cordage.",
        "requires": ["cordage", "wood"],
        "hours": 2,
        "unlocks": ["hunting_bonus"]
    },
    "spear": {
        "name": "Sharpened Spear",
        "icon": "🗡️",
        "desc": "A pointed stick. Basic weapon and tool.",
        "requires": ["wood"],
        "hours": 1,
        "unlocks": ["hunting_bonus", "defence_bonus"]
    },
    "water_filter": {
        "name": "Water Filter",
        "icon": "🫗",
        "desc": "Sand and charcoal filter for dirty water. Essential in the desert.",
        "requires": ["wood", "charcoal"],
        "hours": 2,
        "unlocks": ["water_purification"]
    },
    "fire_bow": {
        "name": "Fire Bow Kit",
        "icon": "🔥",
        "desc": "Friction fire starting kit. No matches needed.",
        "requires": ["wood", "cordage"],
        "hours": 3,
        "unlocks": ["reliable_fire"]
    },
    "shade_cloth": {
        "name": "Shade Cloth",
        "icon": "🫧",
        "desc": "Woven plant fibres for sun protection. Desert essential.",
        "requires": ["foraged_plants"],
        "hours": 3,
        "unlocks": ["desert_shade"]
    }
}

# ==========================================
# ADDITIONAL PLANTS FOR ALASKA AND DESERT
# (These supplement UK_PLANTS for non-UK scenarios)
# ==========================================

QUEST_ADDITIONAL_PLANTS = {
    "edible": {
        # Alaska plants
        "Spruce Tips": {
            "name": "Spruce Tips",
            "latin_name": "Picea spp.",
            "icon": "🌲",
            "category": "Tree",
            "habitat": ["Mountain", "Coniferous", "Tundra"],
            "months": ["May", "June"],
            "description": "Bright green new growth at the tips of spruce branches. Rich in vitamin C.",
            "parts": ["Tips (new growth)"],
            "taste": "Citrusy, tangy",
            "season_tips": "Harvest in late spring when bright green and tender.",
            "nutrition": "Very high in Vitamin C. Also contains Vitamin A.",
            "danger_tips": {"danger_zone": "SAFE", "warning": "Avoid yew, which looks similar but is deadly."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 8,
                "water_value": 2,
                "health_value": 10,
                "warmth_value": 5,
                "morale_value": 3,
                "desc": "Bright green tips of new growth on spruce trees. A vital source of vitamin C in cold environments.",
                "danger": "SAFE"
            }
        },
        "Rosehips": {
            "name": "Rosehips",
            "latin_name": "Rosa spp.",
            "icon": "🔴",
            "category": "Berry",
            "habitat": ["Mountain", "Hedgerow", "Coastal"],
            "months": ["September", "October", "November", "December", "January"],
            "description": "Red-orange fruit of wild roses. One of the best sources of vitamin C in cold climates.",
            "parts": ["Fruit (outer flesh only)"],
            "taste": "Tart, fruity",
            "season_tips": "Best after first frost when sweeter. Avoid the seeds inside — they cause irritation.",
            "nutrition": "Extremely high in Vitamin C. Contains vitamins A, E, and antioxidants.",
            "danger_tips": {"danger_zone": "CAUTION", "warning": "Seeds inside are hairy and irritate the digestive tract. Only eat outer flesh."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 10,
                "water_value": 5,
                "health_value": 15,
                "warmth_value": 0,
                "morale_value": 5,
                "desc": "Red fruits of wild roses. Packed with vitamin C — essential for preventing scurvy in survival situations.",
                "danger": "CAUTION"
            }
        },
        "Cranberries": {
            "name": "Cranberries",
            "latin_name": "Vaccinium oxycoccos",
            "icon": "🔴",
            "category": "Berry",
            "habitat": ["Mountain", "Damp", "Tundra"],
            "months": ["September", "October", "November"],
            "description": "Small red berries found in boggy tundra areas. Often frozen on the plant.",
            "parts": ["Berries"],
            "taste": "Very tart",
            "season_tips": "Found in boggy areas. Can be eaten raw but very tart. Better cooked.",
            "nutrition": "High in Vitamin C and antioxidants.",
            "danger_tips": {"danger_zone": "SAFE", "warning": "Easy to identify. No dangerous lookalikes."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 12,
                "water_value": 10,
                "health_value": 8,
                "warmth_value": 0,
                "morale_value": 5,
                "desc": "Tart red berries found in boggy ground. Can be eaten frozen — a winter survival food.",
                "danger": "SAFE"
            }
        },
        "Cattail": {
            "name": "Cattail",
            "latin_name": "Typha latifolia",
            "icon": "🌾",
            "category": "Root",
            "habitat": ["Damp", "Wet"],
            "months": ["March", "April", "May", "June", "July", "August", "September"],
            "description": "Tall reed with distinctive brown sausage-like flower head. Nearly every part is edible.",
            "parts": ["Roots", "Young shoots", "Flower spikes (early)"],
            "taste": "Starchy, mild",
            "season_tips": "Roots are best in fall/winter. Young shoots in spring. Flower spikes when green.",
            "nutrition": "High in starch. One of the most calorie-dense wild foods.",
            "danger_tips": {"danger_zone": "SAFE", "warning": "Must be cooked. Roots contain starch that must be extracted."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 20,
                "water_value": 15,
                "health_value": 5,
                "warmth_value": 0,
                "morale_value": 8,
                "desc": "The supermarket of the wild. Roots, shoots, and flower heads are all edible. A major food source if found.",
                "danger": "SAFE"
            }
        },
        "Fireweed": {
            "name": "Fireweed",
            "latin_name": "Chamerion angustifolium",
            "icon": "🌸",
            "category": "Plant",
            "habitat": ["Mountain", "Coniferous"],
            "months": ["June", "July", "August"],
            "description": "Tall plant with pink-purple flowers. Grows in cleared and burned areas — hence the name.",
            "parts": ["Young leaves", "Flowers", "Stems (young)"],
            "taste": "Mild, slightly sweet",
            "season_tips": "Young leaves in spring. Flowers in summer. Older leaves become bitter.",
            "nutrition": "Rich in vitamins A and C.",
            "danger_tips": {"danger_zone": "SAFE", "warning": "Avoid older leaves which are bitter and can cause stomach upset."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 8,
                "water_value": 5,
                "health_value": 5,
                "warmth_value": 0,
                "morale_value": 3,
                "desc": "Pink-purple flowers on tall stalks. Young leaves and flowers are edible. A sign of regrowth after disturbance.",
                "danger": "SAFE"
            }
        },
        "Labrador Tea": {
            "name": "Labrador Tea",
            "latin_name": "Rhododendron groenlandicum",
            "icon": "🍵",
            "category": "Herb",
            "habitat": ["Mountain", "Tundra", "Damp"],
            "months": ["June", "July", "August"],
            "description": "Low-growing evergreen shrub with fuzzy leaf undersides. Makes a warming tea.",
            "parts": ["Leaves (for tea)"],
            "taste": "Earthy, slightly medicinal",
            "season_tips": "Harvest leaves year-round but best in summer. Brew lightly — strong tea can cause stomach upset.",
            "nutrition": "Contains vitamin C and medicinal compounds. Traditional remedy for colds.",
            "danger_tips": {"danger_zone": "CAUTION", "warning": "Brew lightly. Strong concentrations can be toxic. Do NOT confuse with toxic Labrador laurel."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 2,
                "water_value": 10,
                "health_value": 8,
                "warmth_value": 10,
                "morale_value": 5,
                "desc": "A low shrub with fuzzy white undersides to its leaves. Brew into a warming tea — a lifeline in cold survival.",
                "danger": "CAUTION"
            }
        },
        # Desert plants
        "Prickly Pear": {
            "name": "Prickly Pear",
            "latin_name": "Opuntia spp.",
            "icon": "🌵",
            "category": "Cactus",
            "habitat": ["Desert", "Arid", "Rocky"],
            "months": ["March", "April", "May", "June", "July", "August", "September"],
            "description": "Flat-padded cactus with bright flowers and reddish fruit. Both pads and fruit are edible if prepared correctly.",
            "parts": ["Pads (nopales)", "Fruit (tunas)"],
            "taste": "Pads: green bean-like. Fruit: sweet and juicy.",
            "season_tips": "Young pads in spring. Fruits in late summer. MUST remove all spines and glochids before eating.",
            "nutrition": "High in water, vitamin C, and minerals. One of the best desert survival foods.",
            "danger_tips": {"danger_zone": "CAUTION", "warning": "Tiny glochids (hair-like spines) must be completely removed. They cause severe irritation in mouth and throat."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 18,
                "water_value": 25,
                "health_value": 5,
                "warmth_value": 0,
                "morale_value": 5,
                "desc": "Flat cactus pads and red fruit. Both edible if you remove EVERY spine and glochid. A desert lifeline.",
                "danger": "CAUTION"
            }
        },
        "Yucca": {
            "name": "Yucca",
            "latin_name": "Yucca spp.",
            "icon": "🌿",
            "category": "Plant",
            "habitat": ["Desert", "Arid", "Rocky"],
            "months": ["April", "May", "June", "July", "August"],
            "description": "Sharp-leaved desert plant with tall flower stalks. Flowers, fruit, and roots are all edible. Also useful for fibre.",
            "parts": ["Flowers", "Fruit (young)", "Roots (cooked)"],
            "taste": "Flowers: sweet. Fruit: bitter when mature. Roots: starchy when cooked.",
            "season_tips": "Flowers in spring. Young fruit in early summer. Roots must be cooked thoroughly.",
            "nutrition": "Flowers high in vitamin C. Roots are starchy. Fibres make excellent cordage.",
            "danger_tips": {"danger_zone": "CAUTION", "warning": "Roots MUST be cooked thoroughly. Raw roots contain saponins that cause digestive distress."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 10,
                "water_value": 5,
                "health_value": 5,
                "warmth_value": 0,
                "morale_value": 3,
                "desc": "Tall flower stalks on a sharp-leaved plant. Flowers are sweet and edible. Roots must be cooked. Leaves make strong cordage.",
                "danger": "CAUTION"
            }
        },
        "Mesquite": {
            "name": "Mesquite",
            "latin_name": "Prosopis spp.",
            "icon": "🌰",
            "category": "Tree",
            "habitat": ["Desert", "Arid"],
            "months": ["June", "July", "August", "September"],
            "description": "Desert tree with long bean-like pods. Pods can be ground into flour.",
            "parts": ["Pods (ground into flour)", "Seeds"],
            "taste": "Sweet, nutty",
            "season_tips": "Harvest pods when they're dry and brittle on the tree. Green pods are too bitter.",
            "nutrition": "High in protein and carbohydrates. Ground pods make nutritious flour.",
            "danger_tips": {"danger_zone": "SAFE", "warning": "Must be ground. Whole pods are too fibrous to eat."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 15,
                "water_value": 2,
                "health_value": 5,
                "warmth_value": 0,
                "morale_value": 3,
                "desc": "Long bean pods from a desert tree. Dry pods can be ground into sweet, nutritious flour.",
                "danger": "SAFE"
            }
        },
        "Purslane": {
            "name": "Purslane",
            "latin_name": "Portulaca oleracea",
            "icon": "🥬",
            "category": "Plant",
            "habitat": ["Desert", "Arid", "Urban"],
            "months": ["May", "June", "July", "August", "September"],
            "description": "Low-growing succulent with fleshy, paddle-shaped leaves. One of the most nutritious leaf vegetables in the world.",
            "parts": ["Leaves", "Stems"],
            "taste": "Slightly sour, succulent",
            "season_tips": "Grows in disturbed soil and between rocks. Look for it in shaded, damp areas.",
            "nutrition": "More omega-3 fatty acids than any other leafy plant. Rich in vitamins A, C, and E.",
            "danger_tips": {"danger_zone": "SAFE", "warning": "Contains oxalic acid. Safe in moderate amounts."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": True,
                "food_value": 8,
                "water_value": 15,
                "health_value": 8,
                "warmth_value": 0,
                "morale_value": 3,
                "desc": "Fleshy-leaved ground plant. Incredibly nutritious and hydrating. One of the best wild sources of omega-3.",
                "danger": "SAFE"
            }
        }
    },
    "poisonous": {
        "Baneberry": {
            "name": "Baneberry",
            "latin_name": "Actaea spp.",
            "icon": "🔴",
            "category": "Berry",
            "habitat": ["Mountain", "Coniferous", "Woodland"],
            "months": ["July", "August", "September"],
            "description": "Small white or red berries on a plant with divided leaves. Extremely poisonous.",
            "danger_tips": {"danger_zone": "DEADLY", "warning": "Even a few berries can cause cardiac arrest. Do NOT confuse with cranberries or other red berries."},
            "lookalikes": [{"name": "Cranberries", "note": "Cranberries grow in bogs, not on bushes. Baneberry grows on upright stems."}],
            "foraging_quest": {
                "edible": False,
                "danger": "DEADLY",
                "health_damage": 40,
                "desc": "Clusters of white or red berries on an upright plant. Looks tempting. Is deadly. Do NOT eat."
            }
        },
        "Water Hemlock": {
            "name": "Water Hemlock",
            "latin_name": "Cicuta maculata",
            "icon": "🌿",
            "category": "Plant",
            "habitat": ["Damp", "Wet", "Mountain"],
            "months": ["May", "June", "July", "August"],
            "description": "Tall plant with purple-streaked stems growing near water. The most poisonous plant in North America.",
            "danger_tips": {"danger_zone": "DEADLY", "warning": "A single bite can be fatal. Causes violent seizures. Grows exactly where you'd look for water and edible roots."},
            "lookalikes": [{"name": "Cattail", "note": "Cattail has a distinctive brown flower head. Water Hemlock has white umbrella-shaped flowers."}],
            "foraging_quest": {
                "edible": False,
                "danger": "DEADLY",
                "health_damage": 50,
                "desc": "Purple-streaked stems near water. The most toxic plant in North America. A single bite can kill."
            }
        },
        "Monkshood": {
            "name": "Monkshood",
            "latin_name": "Aconitum spp.",
            "icon": "💜",
            "category": "Plant",
            "habitat": ["Mountain", "Coniferous"],
            "months": ["July", "August", "September"],
            "description": "Tall plant with hooded purple-blue flowers. All parts are extremely poisonous.",
            "danger_tips": {"danger_zone": "DEADLY", "warning": "Contains aconitine, which affects the heart. Can be absorbed through skin. Do NOT touch."},
            "lookalikes": [{"name": "Fireweed", "note": "Fireweed has open pink flowers on tall spikes. Monkshood has hooded blue-purple flowers."}],
            "foraging_quest": {
                "edible": False,
                "danger": "DEADLY",
                "health_damage": 45,
                "desc": "Hooded blue-purple flowers on a tall plant. Every part is poisonous, even through skin contact. Do NOT touch."
            }
        },
        "Datura": {
            "name": "Datura",
            "latin_name": "Datura spp.",
            "icon": "📯",
            "category": "Plant",
            "habitat": ["Desert", "Arid", "Rocky"],
            "months": ["May", "June", "July", "August", "September"],
            "description": "Large trumpet-shaped white flowers on a shrubby plant. Spiny seed pods. A powerful hallucinogen that can kill.",
            "danger_tips": {"danger_zone": "EXTREME", "warning": "Causes delirium, hallucinations, and death. Has been used as poison for centuries. No safe dose."},
            "lookalikes": [{"name": "Yucca", "note": "Yucca has white bell-shaped flowers on tall stalks. Datura has large trumpet flowers low on the plant."}],
            "foraging_quest": {
                "edible": False,
                "danger": "EXTREME",
                "health_damage": 40,
                "desc": "Large trumpet-shaped white flowers with spiny seed pods. A powerful hallucinogen that can kill. No part is safe."
            }
        },
        "Oleander": {
            "name": "Oleander",
            "latin_name": "Nerium oleander",
            "icon": "🌸",
            "category": "Shrub",
            "habitat": ["Desert", "Arid"],
            "months": ["March", "April", "May", "June", "July", "August", "September", "October"],
            "description": "Ornamental shrub with clusters of pink, white, or red flowers. Every part is deadly poisonous.",
            "danger_tips": {"danger_zone": "DEADLY", "warning": "Even smoke from burning oleander is toxic. Do NOT use for firewood. Do NOT touch. Do NOT eat."},
            "lookalikes": [],
            "foraging_quest": {
                "edible": False,
                "danger": "DEADLY",
                "health_damage": 50,
                "desc": "Clusters of pink, white, or red flowers on an evergreen shrub. Every part — leaves, flowers, stems — is deadly. Even the smoke is toxic."
            }
        }
    }
}

# ==========================================
# FORAGING ENCOUNTER TEMPLATES
# (Narrative wrappers for plant ID challenges)
# ==========================================

FORAGING_ENCOUNTERS = {
    "wild_forest": [
        "You push through the undergrowth and spot something growing in the {habitat}.",
        "Near the base of an old oak tree, you notice some familiar-looking leaves.",
        "Growing along the stream bank, something catches your eye.",
        "In a patch of dappled sunlight, a plant stands out against the green.",
        "The hedgerow is thick with growth. One plant in particular draws your attention.",
        "Rooting through the leaf litter, you find something that might be edible.",
        "A splash of colour in the undergrowth — berries, or something more dangerous?",
        "The damp forest floor is alive with growth. You focus on one plant.",
    ],
    "alaska_winter": [
        "Poking through the snow, you spot something green and promising.",
        "Against the white landscape, a flash of colour catches your eye.",
        "Growing in the shelter of a spruce tree, something has survived the cold.",
        "Near the frozen stream, a plant clings to life in the icy ground.",
        "Under the snow, roots and stems still hold sustenance. You dig carefully.",
        "A hardy plant pushes through the frost. Is it safe to eat?",
    ],
    "desert": [
        "In the shade of a rock overhang, something green survives the heat.",
        "A cactus stands defiant against the barren landscape. But is it the right kind?",
        "Growing in a crack in the rock, a small plant offers hope.",
        "Near a dry wash, something green persists in the dusty earth.",
        "Under the punishing sun, one plant shows life. You approach carefully.",
        "A flowering plant clings to existence in the sand. Could it provide food or water?",
    ]
}

# ==========================================
# WEATHER DESCRIPTIONS (extra flavour)
# ==========================================

QUEST_WEATHER_FLAVOUR = {
    "wild_forest": {
        "day_start": {
            "clear": "Sunlight streams through the canopy. The forest floor is dappled with gold.",
            "cloudy": "Grey clouds blanket the sky. The forest is dim and still.",
            "rain": "Rain patters through the leaves. Everything is wet and slippery.",
            "storm": "Thunder rumbles. Wind tears at the canopy. Branches creak and fall.",
            "fog": "Thick fog wraps the trees. Sounds are muffled. Directions blur."
        },
        "day_end": {
            "clear": "A clear evening. Stars emerge between the trees. The forest settles into night.",
            "cloudy": "The clouds persist. A grey dusk settles over the trees.",
            "rain": "The rain eases as darkness falls. The forest drips and sighs.",
            "storm": "The storm passes, leaving broken branches and dripping leaves.",
            "fog": "The fog thickens with the dark. You can barely see your hand."
        }
    },
    "alaska_winter": {
        "day_start": {
            "clear": "Bitterly cold but crystal clear. The mountains gleam white against a blue sky.",
            "cloudy": "Grey sky presses down. The snow looks like concrete. Cold but no definition.",
            "snow": "Snow falls steadily. The world shrinks to a white circle around you.",
            "blizzard": "White-out. Wind tears at your face. You cannot see ten feet.",
            "freeze": "Deep freeze. The air hurts to breathe. Exposed skin freezes in minutes."
        },
        "day_end": {
            "clear": "The sun sets orange over white peaks. The temperature plummets immediately.",
            "cloudy": "The grey day fades to grey night. No stars to guide you.",
            "snow": "Snow continues into darkness. The world is muffled and white.",
            "blizzard": "The blizzard howls through the night. You must stay in shelter.",
            "freeze": "The deep freeze continues. Night is worse. Much worse."
        }
    },
    "desert": {
        "day_start": {
            "scorching": "The sun is a hammer. Within an hour, the sand will burn to touch.",
            "hot_clear": "Hot and clear. The horizon shimmers. Seek shade by midday.",
            "windy": "A hot wind blows sand and dust. It gets in everything — eyes, mouth, lungs.",
            "cold_night": "The night was brutally cold. Dawn brings relief, but the heat is coming.",
            "sandstorm": "A wall of sand approaches from the west. Find cover now."
        },
        "day_end": {
            "scorching": "The sun sets in flames. Brief relief before the cold hits.",
            "hot_clear": "The sky turns orange and red. A beautiful sunset over a brutal landscape.",
            "windy": "The wind dies with the sun. The silence is almost worse.",
            "cold_night": "The temperature drops fast. Already you can see your breath.",
            "sandstorm": "The storm passes, leaving sand in everything. You shake it from your clothes."
        }
    }
}

# ==========================================
# LOCATION DISCOVERY TEMPLATES
# ==========================================

QUEST_LOCATION_DISCOVER = {
    "wild_forest": "You push through the undergrowth and find yourself in a new area...",
    "alaska_winter": "Through the snow and ice, you discover a new landmark...",
    "desert": "Over the next ridge, the landscape reveals something new..."
}

# ==========================================
# DAY START TEMPLATES
# ==========================================

QUEST_DAY_START = {
    "wild_forest": [
        "Dawn breaks through the trees. Birds call in the canopy.",
        "The forest wakes slowly. Morning mist hangs between the trees.",
        "You open your eyes to green. Another day in the wild.",
        "Rain drips from leaves. The forest is damp but alive.",
        "Sunlight reaches the forest floor. Time to move.",
    ],
    "alaska_winter": [
        "The cold wakes you before dawn. Your breath freezes instantly.",
        "Another grey morning in the white wilderness. Cold and unforgiving.",
        "Frost covers everything. You shake it from your shelter.",
        "The sun rises reluctantly over the frozen landscape.",
        "Ice crystals hang in the air. Another day of survival begins.",
    ],
    "desert": [
        "The sun rises fast and hot. The sand is already warming.",
        "Dawn brings brief, cool relief. It won't last.",
        "You wake before the heat. These are the precious hours.",
        "Morning in the desert. Pink sky over orange sand.",
        "The desert is beautiful at dawn. Then the sun climbs.",
    ]
}