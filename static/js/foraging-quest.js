// ==========================================
// FORAGING QUEST — GAME ENGINE
// ==========================================
//
// TABLE OF CONTENTS:
// ─────────────────────────────────────────
//  1.  CLASS DEFINITION & CONSTRUCTOR
//  2.  INITIALIZATION
//  3.  STATE MANAGEMENT
//  4.  GAME FLOW (startGame, startDay, chooseAction, etc.)
//  5.  RESOURCE MANAGEMENT
//  5b. HELPER GETTERS & JOURNAL
//  5c. CRITICAL RESOURCE CHECKS
//  5d. INJURY SYSTEM
//  5e. ACHIEVEMENT SYSTEM
//  5f. ANIMATION & DESERT MECHANICS
//  6.  WEATHER & SEASON
//  7.  ACTION RESOLUTION
//  8.  FORAGING SYSTEM
//  9.  EVENT SYSTEM
//  10. ENDINGS & DEATH
//  11. SAVE / LOAD
//  12. UI HELPERS
//  13. RENDER — SCENARIO SELECT
//  14. RENDER — INTRO
//  15. RENDER — GAME SCREEN
//  16. RENDER — DAY START
//  17. RENDER — CHOOSE ACTIONS
//  17b. RENDER — CRAFTING MENU
//  18. RENDER — FORAGING CHALLENGE
//  19. RENDER — FORAGING RESULT
//  20. RENDER — ACTION RESULT
//  21. RENDER — EVENT & EVENT RESULT
//  22. RENDER — DISCOVERY
//  23. RENDER — DAY END
//  24. RENDER — JOURNAL
//  25. RENDER — GAME OVER
//  25b. SURVIVAL STORY GENERATOR
//  26. LOCATION MOVEMENT
//  27. PROGRESS DISPLAYS
//  28. DEBUG HELPERS
//  29. INITIALISATION ON PAGE LOAD
// ─────────────────────────────────────────

class ForagingQuestGame {

    injectCompactStyles() {
        if (document.getElementById('fq-compact-styles')) return;
        const style = document.createElement('style');
        style.id = 'fq-compact-styles';
        style.textContent = `
            .fq-action-btn {
                display: flex;
                flex-direction: column;
                padding: 8px 12px;
                border: 1px solid rgba(255,255,255,0.15);
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.15s ease;
                background: rgba(255,255,255,0.05);
                margin-bottom: 4px;
                gap: 2px;
            }
            .fq-action-btn:hover:not(.fq-action-disabled) {
                background: rgba(255,255,255,0.1);
                border-color: rgba(255,255,255,0.3);
                transform: translateY(-1px);
            }
            .fq-action-btn:active:not(.fq-action-disabled) {
                transform: translateY(0px);
                background: rgba(255,255,255,0.15);
            }
            .fq-action-btn.fq-action-disabled {
                opacity: 0.35;
                cursor: not-allowed;
                filter: grayscale(0.5);
            }
            .fq-action-top {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .fq-action-top .fq-action-icon {
                font-size: 1.2rem;
                line-height: 1;
            }
            .fq-action-top .fq-action-name {
                font-weight: 600;
                font-size: 0.9rem;
                flex: 1;
                line-height: 1.2;
            }
            .fq-action-top .fq-action-hours {
                font-size: 0.7rem;
                color: rgba(255,255,255,0.5);
                background: rgba(255,255,255,0.08);
                padding: 2px 6px;
                border-radius: 3px;
                white-space: nowrap;
            }
            .fq-action-desc {
                font-size: 0.75rem;
                color: rgba(255,255,255,0.55);
                line-height: 1.3;
                margin-top: 2px;
            }
            .fq-action-requires {
                font-size: 0.7rem;
                color: #ff9800;
                margin-top: 2px;
                display: block;
            }
            .fq-action-chance {
                font-size: 0.7rem;
                color: rgba(255,255,255,0.4);
                margin-top: 1px;
                display: block;
            }
            .fq-action-use-item {
                border-color: rgba(76,175,80,0.3) !important;
                background: rgba(76,175,80,0.05) !important;
            }
            .fq-action-use-item:hover:not(.fq-action-disabled) {
                background: rgba(76,175,80,0.12) !important;
                border-color: rgba(76,175,80,0.5) !important;
            }
            #fq-actions {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 6px;
                max-height: 55vh;
                overflow-y: auto;
                padding-right: 4px;
            }
            @media (max-width: 600px) {
                #fq-actions {
                    grid-template-columns: 1fr;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // ==========================================
    // 1. CLASS DEFINITION & CONSTRUCTOR
    // ==========================================

    constructor() {
        this.app = document.getElementById('fq-app');
        this.screens = {};
        this.config = null;
        this.state = null;
        this.encounterData = null;
        this.currentEvent = null;
        this.currentEventResult = null;
        this.currentActionResult = null;
        this.foragingResult = null;
        this.currentEnding = null;
        this.dayEndChanges = null;
        this.currentDiscovery = null;
        this.actionsRemaining = 0;
        this.actionResults = [];
        this.scenarioData = null;
    }

    // ==========================================
    // 2. INITIALIZATION
    // ==========================================

    async init() {
        const ids = [
            'loading', 'select', 'intro', 'game', 'gameover',
            'journal-overlay', 'menu-overlay'
        ];
        ids.forEach(id => {
            this.screens[id] = document.getElementById(`fq-${id}`);
        });

        this.showScreen('loading');
        this.injectCompactStyles();

        try {
            await this.loadConfig();
            this.showScreen('select');
            this.renderScenarioSelect();
            this.bindGlobalEvents();
        } catch (err) {
            console.error('Failed to load game config:', err);
            this.showToast('Failed to load game. Please refresh.', 'danger');
        }
    }

    async loadConfig() {
        const res = await fetch('/static/data/foraging/base.json');
        this.config = await res.json();

        this.defaultSeason = this.config.seasonIcons ? 'Autumn' : (window.FQ_CONFIG?.defaultSeason || 'Autumn');
        this.seasonIcons = this.config.seasonIcons || window.FQ_CONFIG?.seasonIcons || {};
        this.seasonMonths = this.config.seasonMonths || window.FQ_CONFIG?.seasonMonths || {};
        this.scenarioData = null;
    }

    // ==========================================
    // 3. STATE MANAGEMENT
    // ==========================================

    newState(scenarioId) {
        const scenario = this.scenarioData;
        const starting = scenario.starting;
        const hasWater = starting.water !== null && starting.water !== undefined;

        return {
            scenarioId,
            day: 1,
            season: scenario.start_season || 'Autumn',
            weather: null,
            hoursRemaining: scenario.hours_per_day,
            actionsUsed: 0,
            maxActions: scenario.actions_per_day,
            resources: {
                health: starting.health,
                hunger: starting.hunger,
                warmth: starting.warmth,
                morale: starting.morale,
                ...(hasWater ? { water: starting.water } : {})
            },
            maxResources: {
                health: 100,
                hunger: 100,
                warmth: 100,
                morale: 100,
                ...(hasWater ? { water: 100 } : {})
            },
            inventory: [...(scenario.starting_inventory || [])],
            knownLocations: scenario.locations
                .filter(l => l.discovered)
                .map(l => l.id),
            currentLocation: scenario.locations.find(l => l.discovered)?.id || 'camp',
            shelterLevel: 0,
            signalProgress: 0,
            exploreProgress: 0,
            journal: [],
            plantsSeen: [],
            plantsCorrect: 0,
            plantsWrong: 0,
            eventsCompleted: [],
            daysSurvived: 0,
            causeOfDeath: null,
            state: 'day_start',
            pendingActions: [],
            actionLog: [],
            injuries: [],
            injuryFree: true,
            achievements: [],
            itemsCrafted: [],
            huntsSuccessful: 0,
            wildlifeEncounters: [],
            injuriesTreated: 0,
            lastSignalDay: 1,
            warmthBonus: 0,
            // Wild Forest
            forestKarma: 50,
            watcherPhase: 0,
            watcherDaysSinceEvent: 0,
            groveDaysConsecutive: 0,
            hikerPhase: 0,
            // Alaska
            wildRespect: 50,
            mythicEventsCompleted: [],
            wolfStalking: false,
            wolfPhase: 0,
            wolfDaysSinceEvent: 0,
            wolfEncounterCount: 0,
            bearInsteadOfWolf: false,
            cabinDaysConsecutive: 0,
            stormWarning: 0,
            // Desert
            vulturePhase: 0,
            vultureDaysSinceEvent: 0,
            mineDaysConsecutive: 0,
            driverPhase: 0,
            hallucinationCount: 0,
            // Shared
            shelterAtLastLocation: 0,
            movedThisDay: false,
            hasFire: false,
            fireExtinguished: false,
            // Tropical Island
            islandRespect: 50,
            sharkPhase: 0,
            sharkDaysSinceEvent: 0,
            kiriPhase: 0,
            wreckDaysConsecutive: 0,
            tideState: 'low',
            // Overgrown City
            companions: [],
            packPhase: 0,
            packDaysSinceEvent: 0,
            supermarketDaysConsecutive: 0,
            amaraPhase: 0,
            amaraDaysSinceEvent: 0,
            buildingStability: {
                hospital_ruins: 100,
                underground_station: 100,
                school_gym: 100,
                construction_site: 80
            },
            hostileSurvivorsEncountered: 0
        };
    }

    setState(newState) {
        this.state.state = newState;
        this.render();
    }

    async selectScenario(scenarioId) {
        try {
            const res = await fetch(`/static/data/foraging/scenarios/${scenarioId}.json`);
            if (!res.ok) throw new Error('Failed to load scenario');
            this.scenarioData = await res.json();
            this.state = this.newState(scenarioId);
            this.state.state = 'intro';
            this.render();
        } catch (err) {
            console.error('Failed to load scenario:', err);
            this.showToast('Failed to load scenario. Please try again.', 'danger');
        }
    }

    // ==========================================
    // 4. GAME FLOW
    // ==========================================

    startGame() {
        console.log('[FQ] startGame called, state:', this.state);
        this.state.day = 1;
        this.state.daysSurvived = 0;
        console.log('[FQ] about to call startDay');
        this.startDay();
        console.log('[FQ] startDay finished');
    }

    startDay() {
        this.state.weather = this.generateWeather();

        const scenario = this.getScenario();
        this.state.maxActions = scenario.actions_per_day;

        // Morale bonus action
        if (this.state.resources.morale >= (scenario.bonus_action_morale || 75)) {
            this.state.maxActions += 1;
        }

        // Injury modifier: reduce actions for severe injuries
        const severeInjuries = this.state.injuries.filter(i => i.severity === 'severe');
        if (severeInjuries.length > 0) {
            this.state.maxActions = Math.max(1, this.state.maxActions - severeInjuries.length);
            this.addJournalEntry(`⚠️ Your ${severeInjuries.map(i => i.name).join(' and ')} reduce your energy. You have fewer actions today.`);
        }

        this.state.actionsUsed = 0;
        this.state.hoursRemaining = scenario.hours_per_day;
        this.state.actionLog = [];
        this.state.hasFire = false;
        this.state.fireExtinguished = false;
        this.state.movedThisDay = false;
        this.state.dailyMessageShown = [];

        // ── ALASKA: Wolf progression & cabin fever ──
        if (this.state.scenarioId === 'alaska_winter') {
            this.state.wolfDaysSinceEvent = (this.state.wolfDaysSinceEvent || 0) + 1;

            // Auto-advance wolf phase
            if (this.state.wolfPhase === 0 && this.state.day >= 3) {
                this.state.wolfPhase = 1;
                this.addJournalEntry('🐾 You notice large paw prints in the snow near your shelter. Something is watching you.');
                this.state.resources.morale -= 1;
            } else if (this.state.wolfPhase === 1 && this.state.day >= 6) {
                this.state.wolfPhase = 2;
                this.addJournalEntry('🐺 You hear howling in the distance. The wolf is getting closer.');
                this.state.resources.morale -= 2;
            }

            // Wolf stalking effects
            if (this.state.wolfStalking) {
                const moralePenalty = this.state.wolfEncounterCount >= 3 ? -4 : -2;
                this.state.resources.morale -= moralePenalty;

                if (this.state.shelterLevel >= 3) {
                    this.state.resources.morale += 1;
                    this.addJournalEntry('🐺 You feel watched, but your shelter keeps you safe. The wolf is still out there.');
                } else {
                    this.addJournalEntry('🐺 You feel watched. The wolf is still out there.');
                }

                // After many days of stalking with strong shelter, wolf moves on
                if (this.state.shelterLevel >= 3 && this.state.wolfDaysSinceEvent > 7) {
                    this.state.wolfStalking = false;
                    this.state.wolfPhase = 3;
                    this.addJournalEntry('🐺 The howling has stopped. The wolf has moved on to easier prey.');
                    this.state.resources.morale += 3;
                }
            }

            // Cabin fever
            if (this.state.cabinDaysConsecutive >= 3) {
                const drain = Math.min(this.state.cabinDaysConsecutive - 2, 8);
                this.state.resources.morale -= drain;

                if (this.state.cabinDaysConsecutive >= 5) {
                    this.addJournalEntry('🏚️ The cabin walls feel closer than yesterday. You should leave.');
                }
                if (this.state.cabinDaysConsecutive >= 8) {
                    this.addJournalEntry('🏚️ You can\'t remember the last time you went outside. The fire is warm. The door is closed. That\'s fine. That\'s fine...');
                }
            }
        }

        // ── DESERT: Vulture phase & mine effects ──
        if (this.state.scenarioId === 'desert') {
            const water = this.state.resources.water || 50;
            const health = this.state.resources.health;
            let newPhase = 0;

            if (water <= 0 || health <= 10) {
                newPhase = 4;
            } else if (water <= 10 || health <= 20) {
                newPhase = 3;
            } else if (water <= 25 || health <= 35) {
                newPhase = 2;
            } else if (water <= 40 || health <= 50) {
                newPhase = 1;
            }

            // Phase only increases, never decreases
            if (newPhase > this.state.vulturePhase) {
                this.state.vulturePhase = newPhase;
                if (newPhase >= 2) {
                    this.addJournalEntry('🦅 The vultures are circling closer. They can tell you\'re struggling.');
                } else if (newPhase === 1) {
                    this.addJournalEntry('🦅 You spot vultures circling in the distance. They\'re not interested in you. Yet.');
                }
            }

            // Vulture morale penalty
            if (this.state.vulturePhase >= 3) {
                this.state.resources.morale -= 3;
                this.addJournalEntry('🦅 The vultures are directly overhead. Waiting.');
            } else if (this.state.vulturePhase >= 2) {
                this.state.resources.morale -= 1;
            }

            this.state.vultureDaysSinceEvent = (this.state.vultureDaysSinceEvent || 0) + 1;

            // Mine consecutive days effects
            if (this.state.mineDaysConsecutive >= 3) {
                const drain = Math.min(this.state.mineDaysConsecutive - 2, 5);
                this.state.resources.morale -= drain;

                if (this.state.mineDaysConsecutive >= 5) {
                    this.addJournalEntry('⛏️ The darkness of the mine feels safer than the sun. That worries you.');
                }
                if (this.state.mineDaysConsecutive >= 8) {
                    this.addJournalEntry('⛏️ You can\'t remember the last time you saw the sky. Do you want to?');
                }
            }
        }

        // ── OVERGROWN CITY: Companion & pack system ──
        if (this.state.scenarioId === 'overgrown_city') {
            this.state.packDaysSinceEvent = (this.state.packDaysSinceEvent || 0) + 1;
            this.state.amaraDaysSinceEvent = (this.state.amaraDaysSinceEvent || 0) + 1;

            this.processCompanionsDaily();

            // Pack phase progression
            const activeCompanions = this.getActiveCompanions().length;
            if (this.state.packPhase === 0 && this.state.day >= 3) {
                this.state.packPhase = 1;
                this.addJournalEntry('🐕 You hear howling in the distance. Feral dogs are in the area.');
            } else if (this.state.packPhase === 1 && this.state.day >= 6) {
                this.state.packPhase = 2;
                this.addJournalEntry('🐕 You find the remains of an animal. The pack has been hunting here.');
            } else if (this.state.packPhase === 2 && this.state.day >= 9) {
                this.state.packPhase = 3;
                this.addJournalEntry('🐕 Dogs are circling your shelter at night. They know where you are.');
            } else if (this.state.packPhase === 3 && this.state.day >= 12) {
                this.state.packPhase = 4;
                this.addJournalEntry('🐕 The pack is getting aggressive. Being alone is dangerous.');
            }

            // Pack morale penalty
            const packPenalty = [0, -1, -2, -3, -5][this.state.packPhase] || 0;
            const companionReduction = Math.min(activeCompanions * 1, 3);
            this.state.resources.morale += packPenalty + companionReduction;

            // Supermarket consecutive days effects
            if (this.state.supermarketDaysConsecutive >= 3) {
                const drain = Math.min(this.state.supermarketDaysConsecutive - 2, 6);
                this.state.resources.morale -= drain;
                if (this.state.supermarketDaysConsecutive >= 5) {
                    this.addJournalEntry('🛒 The supermarket feels safe. Too safe. The outside world seems harsh by comparison.');
                }
                if (this.state.supermarketDaysConsecutive >= 8) {
                    this.addJournalEntry('🛒 You can\'t remember the last time you went outside. The fluorescent aisles are your whole world. That\'s fine. That\'s fine...');
                }
            }

            // Building stability decay
            if (this.state.buildingStability) {
                for (const [locId, stability] of Object.entries(this.state.buildingStability)) {
                    if (this.state.currentLocation === locId) {
                        this.state.buildingStability[locId] = Math.max(0, stability - 3);
                    } else {
                        this.state.buildingStability[locId] = Math.max(0, stability - 1);
                    }
                }
            }

            // Building collapse warning
            const loc = this.getLocation();
            if (loc && loc.has_stability && this.state.buildingStability[loc.id] !== undefined) {
                if (this.state.buildingStability[loc.id] <= 0) {
                    this.addJournalEntry('🏚️ The building groans dangerously. It could collapse at any moment!');
                } else if (this.state.buildingStability[loc.id] <= 30) {
                    this.addJournalEntry('🏚️ Cracks are widening in the walls. This building isn\'t stable.');
                }
            }

            // Cold snap check
            if (this.state.weather && this.state.weather.type === 'cold_snap') {
                if (this.state.resources.warmth <= 20 && !this.hasInjury('frostbite')) {
                    if (Math.random() < 0.3) {
                        this.addInjury('frostbite');
                    }
                }
            }

            // Rain water collection
            if (this.state.weather && (this.state.weather.type === 'rain' || this.state.weather.type === 'thunderstorm')) {
                const rainBonus = this.state.weather.type === 'thunderstorm' ? 6 : 3;
                this.state.resources.water = Math.min(100, this.state.resources.water + rainBonus);
            }

            // Disease check
            if (this.state.resources.health <= 25 && !this.hasInjury('infection')) {
                if (Math.random() < 0.15) {
                    this.addInjury('infection');
                    this.addJournalEntry('🦠 You feel feverish and weak. Something isn\'t right — you might be getting sick.');
                }
            }

            // Companion risk when player health is very low
            if (this.state.resources.health <= 15) {
                for (const comp of this.getActiveCompanions()) {
                    if (Math.random() < 0.05) {
                        comp.status = 'dead';
                        this.addJournalEntry(`${comp.icon} ${comp.name} didn't survive. The conditions in this city are too harsh.`);
                        this.showToast(`${comp.icon} ${comp.name} has died.`, 'danger');
                        this.state.resources.morale -= (comp.id === 'lily' ? 30 : comp.id === 'mrs_chen' ? 15 : 10);
                        for (const other of this.state.companions) {
                            if (other.status === 'active' && other.id !== comp.id) {
                                other.trust = Math.max(0, other.trust - 10);
                            }
                        }
                        break;
                    }
                }
            }
        }

        // ── TROPICAL ISLAND: Tide, shark & wreck ──
        if (this.state.scenarioId === 'tropical_island') {
            this.state.tideState = (this.state.day % 2 === 1) ? 'low' : 'high';
            this.state.sharkDaysSinceEvent = (this.state.sharkDaysSinceEvent || 0) + 1;

            // Wreck consecutive days tracking (reset if not at wreck)
            if (this.state.currentLocation === 'lagoon_shipwreck') {
                this.state.wreckDaysConsecutive = (this.state.wreckDaysConsecutive || 0) + 1;
            } else {
                this.state.wreckDaysConsecutive = 0;
            }

            const islandRespect = this.state.islandRespect || 50;

            // Shark phase auto-advancement
            let newSharkPhase = this.state.sharkPhase || 0;
            if (newSharkPhase === 0 && this.state.day >= 3) {
                newSharkPhase = 1;
                this.addJournalEntry('🦈 You spot a fin gliding through the lagoon. A reef shark patrols these waters.');
                this.state.resources.morale -= 1;
            } else if (newSharkPhase === 1 && this.state.day >= 5) {
                newSharkPhase = 2;
                if (islandRespect < 40) {
                    this.addJournalEntry('🦈 The shark is circling closer. It seems interested in you.');
                } else {
                    this.addJournalEntry('🦈 The shark circles in the shallows. It watches but keeps its distance.');
                }
            } else if (newSharkPhase === 2 && this.state.day >= 7) {
                newSharkPhase = 3;
                if (islandRespect < 35) {
                    this.addJournalEntry('🦈 The shark bumped you in the water. It\'s testing whether you\'re prey.');
                    this.state.resources.morale -= 3;
                } else {
                    this.addJournalEntry('🦈 The shark is bolder now. It passes close but doesn\'t threaten.');
                }
            }
            this.state.sharkPhase = Math.max(this.state.sharkPhase || 0, newSharkPhase);

            // Shark morale penalty
            if (this.state.sharkPhase >= 3) {
                this.state.resources.morale -= 2;
                this.addJournalEntry('🦈 The shark\'s presence makes you uneasy about entering the water.');
            } else if (this.state.sharkPhase >= 2) {
                this.state.resources.morale -= 1;
            }

            // Wreck trap morale drain
            if (this.state.wreckDaysConsecutive >= 3) {
                const drain = Math.min(this.state.wreckDaysConsecutive - 2, 6);
                this.state.resources.morale -= drain;

                if (this.state.wreckDaysConsecutive >= 5) {
                    this.addJournalEntry('🚢 The wreck feels safe. Too safe. The outside world seems harsh by comparison.');
                }
                if (this.state.wreckDaysConsecutive >= 8) {
                    this.addJournalEntry('🚢 You can hear the hull groaning. Water seeps in. But it\'s still floating. Still safe. Isn\'t it?');
                    this.state.resources.morale -= 3;
                }
            }
        }

        // ── WILD FOREST: Watcher progression ──
        if (this.state.scenarioId === 'wild_forest') {
            this.state.watcherDaysSinceEvent = (this.state.watcherDaysSinceEvent || 0) + 1;

            const karma = this.state.forestKarma || 50;

            // Auto-advance watcher phase
            if (this.state.watcherPhase === 0 && this.state.day >= 3) {
                this.state.watcherPhase = 1;
                this.addJournalEntry('🌿 You feel something watching you from between the trees. The forest is aware of you now.');
            } else if (this.state.watcherPhase === 1 && this.state.day >= 5) {
                this.state.watcherPhase = 2;
                if (karma < 40) {
                    this.addJournalEntry('🕸️ The watching has a weight to it now. Something in the forest doesn\'t trust you.');
                } else if (karma > 60) {
                    this.addJournalEntry('🍃 The watching feels warmer. Something in the forest is curious about you.');
                } else {
                    this.addJournalEntry('🌿 The watching continues. The forest hasn\'t decided what it thinks of you yet.');
                }
            } else if (this.state.watcherPhase === 2 && this.state.day >= 7) {
                this.state.watcherPhase = 3;
                if (karma < 35) {
                    this.addJournalEntry('🕸️ Paths seem to lead in circles. The forest is testing you — and you\'re failing.');
                    this.state.resources.morale -= 3;
                } else if (karma > 65) {
                    this.addJournalEntry('✨ Mushrooms seem to glow faintly along safe paths. The forest is guiding you.');
                    this.state.resources.morale += 3;
                } else {
                    this.addJournalEntry('🌿 The forest is testing you. Your choices matter more than you know.');
                }
            } else if (this.state.watcherPhase === 3 && this.state.day >= 10) {
                this.state.watcherPhase = 4;
                if (karma >= 70) {
                    this.addJournalEntry('🌱 The forest has made its judgement. You belong here. For now.');
                    this.state.resources.morale += 5;
                } else if (karma <= 25) {
                    this.addJournalEntry('🥀 The forest has made its judgement. You are not welcome here.');
                    this.state.resources.morale -= 5;
                } else {
                    this.addJournalEntry('🌿 The forest has made its judgement. The trees seem to lean in, listening.');
                }
            }

            // Watcher daily effects based on karma
            if (this.state.watcherPhase >= 2) {
                if (karma >= 70) {
                    this.state.resources.morale += 2;
                } else if (karma <= 25) {
                    this.state.resources.morale -= 2;
                }
            }

            // Grove consecutive days effects
            if (this.state.groveDaysConsecutive >= 3) {
                const drain = Math.min(this.state.groveDaysConsecutive - 2, 6);
                this.state.resources.morale -= drain;

                if (this.state.groveDaysConsecutive >= 5) {
                    this.addJournalEntry('🍄 The mushroom grove feels welcoming. Too welcoming. You can\'t remember why you\'d want to leave.');
                }
                if (this.state.groveDaysConsecutive >= 8) {
                    this.addJournalEntry('🍄 The mushrooms whisper to you. Their voices are soft and kind. They say you can stay forever.');
                    this.state.resources.morale -= 3;
                }
            }
        }

        this.addJournalEntry(`Day ${this.state.day} begins. Weather: ${this.state.weather.icon} ${this.state.weather.name}.`);

        // Weather animations
        const container = document.body;
        container.classList.remove('anim-heat-shimmer', 'anim-sandstorm');
        if (this.state.weather) {
            if (this.state.weather.type === 'scorching' || this.state.weather.type === 'hot') {
                this.playAnimation('heat');
            } else if (this.state.weather.type === 'sandstorm') {
                this.playAnimation('sandstorm');
            }
        }

        // Process injury healing
        this.processInjuryHealing();

        // Wolf stalking daily effect (Alaska)
        if (this.state.wolfStalking && this.state.scenarioId === 'alaska_winter') {
            this.state.resources.morale -= 2;
            this.addJournalEntry('🐺 You feel watched. The wolf is still out there.');
        }

        this.setState('day_start');
    }

    chooseAction(actionId, craftItemId = null) {
        if (this.state.actionsUsed >= this.state.maxActions) return;

        if (actionId === 'use_item') return;

        if (actionId === 'light_fire') {
            if (this.state.hoursRemaining < 1) {
                this.showToast('Not enough daylight hours remaining', 'danger');
                return;
            }
            this.state.actionsUsed++;
            this.state.hoursRemaining -= 1;
            const result = this.resolveLightFire(this.getLocation(), this.getScenario());
            this.currentActionResult = result;
            this.setState('action_resolve');
            return;
        }

        if (actionId === 'melt_water') {
            if (this.state.hoursRemaining < 1) {
                this.showToast('Not enough daylight hours remaining', 'danger');
                return;
            }
            this.state.actionsUsed++;
            this.state.hoursRemaining -= 1;
            const result = this.resolveMeltWater(this.getLocation(), this.getScenario());
            this.currentActionResult = result;
            this.setState('action_resolve');
            return;
        }

        if (actionId === 'craft') {
            if (craftItemId) {
                if (this.state.hoursRemaining < 2) {
                    this.showToast('Not enough daylight hours remaining', 'danger');
                    return;
                }
                this.state.actionsUsed++;
                this.state.hoursRemaining -= 2;
                const result = this.resolveCraft(this.getLocation(), this.getScenario(), craftItemId);
                this.currentActionResult = result;
                this.setState('action_resolve');
            } else {
                this.craftingMode = true;
                this.renderChooseActions();
            }
            return;
        }

        const action = this.config.actions[actionId];
        if (!action) return;

        // Check prerequisites
        if (action.requires && action.requires.length > 0) {
            const missing = action.requires.filter(r => !this.state.inventory.includes(r));
            if (missing.length > 0) {
                this.showToast(`Requires: ${missing.join(', ')}`, 'danger');
                return;
            }
        }

        const hours = this.getActionHours(actionId);
        if (hours > this.state.hoursRemaining) {
            this.showToast('Not enough daylight hours remaining', 'danger');
            return;
        }

        this.state.pendingActions.push(actionId);
        this.state.actionsUsed++;
        this.state.hoursRemaining -= hours;

        if (actionId === 'forage') {
            this.startForaging();
            return;
        }

        this.resolveAction(actionId);
    }

    handleUseItem(itemId) {
        if (this.state.actionsUsed >= this.state.maxActions) {
            this.showToast('No actions remaining today', 'danger');
            return;
        }
        if (this.state.hoursRemaining < 1) {
            this.showToast('Not enough daylight hours remaining', 'danger');
            return;
        }

        const result = this.resolveUseItem(itemId);
        this.applyEffects(result.effects);

        this.state.actionsUsed++;
        this.state.hoursRemaining -= result.hours;
        this.state.actionLog.push(result);
        this.addJournalEntry(result.text);

        this.currentActionResult = result;
        this.setState('action_resolve');
    }

    afterActionResult() {
        const check = this.checkCriticalResources();
        if (check.dead) return;

        if (check.warnings.length > 0) {
            this.showToast(check.warnings[0], 'danger');
        }

        if (this.state.actionsUsed >= this.state.maxActions || this.state.hoursRemaining <= 0) {
            this.rollForEvent();
        } else {
            this.setState('choose_actions');
        }
    }

        // ==========================================
    // 5. RESOURCE MANAGEMENT
    // ==========================================

    endDay() {
        const scenario = this.getScenario();
        const decay = scenario.decay;
        const changes = {};

        // Hunger decay
        this.state.resources.hunger -= decay.hunger;
        changes.hunger = -decay.hunger;

        // Warmth decay (modified by shelter, weather, passive bonuses, fire)
        let warmthDecay = decay.warmth;
        if (this.state.weather) {
            warmthDecay -= this.state.weather.warmth_mod || 0;
        }
        const shelterData = this.scenarioData?.shelter;
        if (shelterData && shelterData[this.state.shelterLevel]) {
            warmthDecay -= shelterData[this.state.shelterLevel].warmth_bonus || 0;
        }
        const loc = this.getLocation();
        if (loc && loc.shelter_bonus) {
            warmthDecay -= 3;
        }
        if (this.state.warmthBonus) {
            warmthDecay -= this.state.warmthBonus;
        }
        if (this.state.hasFire) {
            warmthDecay -= 5;
        }
        warmthDecay = Math.max(0, warmthDecay);
        this.state.resources.warmth -= warmthDecay;
        changes.warmth = -warmthDecay;

        // Morale decay (modified by weather, fire)
        let moraleDecay = decay.morale;
        if (this.state.weather) {
            moraleDecay -= this.state.weather.morale_mod || 0;
        }
        if (this.state.hasFire) {
            moraleDecay -= 3;
        }
        moraleDecay = Math.max(0, moraleDecay);
        this.state.resources.morale -= moraleDecay;
        changes.morale = -moraleDecay;

        // Water decay (desert only)
        if (decay.water && decay.water > 0) {
            let waterDecay = decay.water;
            if (this.state.weather) {
                if (this.state.weather.water_mod) {
                    waterDecay -= this.state.weather.water_mod;
                }
            }
            waterDecay = Math.max(0, waterDecay);
            this.state.resources.water -= waterDecay;
            changes.water = -waterDecay;
        }

        // ── OVERGROWN CITY: Companion food consumption & effects ──
        if (this.state.scenarioId === 'overgrown_city') {
            const activeCompanions = this.getActiveCompanions();
            for (const comp of activeCompanions) {
                this.state.resources.hunger -= comp.foodConsumption;
                this.state.resources.morale += comp.moraleEffect;

                // Trust drift toward baseline
                if (comp.trust < comp.trustBaseline) {
                    comp.trust = Math.min(comp.trust + 1, comp.trustBaseline);
                } else if (comp.trust > comp.trustBaseline + 10) {
                    comp.trust = Math.max(comp.trust - 1, comp.trustBaseline);
                }

                // Marcus betrayal check
                if (comp.id === 'marcus' && comp.trust < 20 && Math.random() < 0.15) {
                    this.state.resources.hunger -= 20;
                    comp.status = 'betrayed';
                    this.addJournalEntry('🧔 Marcus stole food and left in the night. You can\'t trust everyone.');
                    this.showToast('Marcus stole supplies and left!', 'danger');
                    this.state.resources.morale -= 10;
                }

                // Sam leaving check
                if (comp.id === 'sam' && this.state.resources.morale < 15 && Math.random() < 0.2) {
                    comp.status = 'left';
                    this.addJournalEntry(`👦 Sam couldn't take it anymore. They left, looking for somewhere better.`);
                    this.showToast('Sam left your group.', 'danger');
                    this.state.resources.morale -= 10;
                }

                // Lily death check
                if (comp.id === 'lily' && comp.status === 'active' && this.state.resources.health <= 0) {
                    comp.status = 'dead';
                    this.addJournalEntry('👧 Lily... didn\'t make it. The city is no place for a child. You failed her.');
                    this.showToast('👧 Lily has died.', 'danger');
                    this.state.resources.morale -= 30;
                    for (const other of this.state.companions) {
                        if (other.status === 'active' && other.id !== 'lily') {
                            other.trust = Math.max(0, other.trust - 15);
                        }
                    }
                }
            }

            // Lily prevents morale from hitting rock bottom
            if (this.hasCompanion('lily') && this.state.resources.morale < 10) {
                this.state.resources.morale = 10;
                this.addJournalEntry('👧 Lily squeezes your hand. "It\'s going to be okay." And somehow, you believe her.');
            }

            // Rain water collection
            if (this.state.weather) {
                if (this.state.weather.type === 'rain') {
                    const rainBonus = this.state.shelterLevel >= 2 ? 8 : 4;
                    this.state.resources.water += rainBonus;
                    changes.water = (changes.water || 0) + rainBonus;
                    this.addJournalEntry(`🌧️ The rain collects in containers and puddles. +${rainBonus} water.`);
                } else if (this.state.weather.type === 'thunderstorm') {
                    const stormBonus = this.state.shelterLevel >= 2 ? 12 : 6;
                    this.state.resources.water += stormBonus;
                    changes.water = (changes.water || 0) + stormBonus;
                    this.addJournalEntry(`⛈️ Heavy rain fills every container. +${stormBonus} water.`);
                }
            }
        }

        // ── TROPICAL ISLAND: Rain water collection ──
        if (this.state.scenarioId === 'tropical_island' && this.state.weather) {
            if (this.state.weather.type === 'rain') {
                const rainBonus = this.state.shelterLevel >= 2 ? 10 : 5;
                this.state.resources.water += rainBonus;
                changes.water = (changes.water || 0) + rainBonus;
                this.addJournalEntry(`🌧️ The rain collects in your shelter. +${rainBonus} water.`);
            } else if (this.state.weather.type === 'tropical_storm') {
                const stormBonus = this.state.shelterLevel >= 2 ? 15 : 8;
                this.state.resources.water += stormBonus;
                changes.water = (changes.water || 0) + stormBonus;
                this.addJournalEntry(`⛈️ The storm dumps rainwater everywhere. +${stormBonus} water.`);
            }
        }

        // ── DESERT: Passive craft effects ──
        this.applyPassiveCraftEffects();

        // Injury daily effects
        if (this.state.injuries && this.state.injuries.length > 0) {
            for (const injury of this.state.injuries) {
                if (injury.dailyEffects) {
                    for (const [key, val] of Object.entries(injury.dailyEffects)) {
                        if (this.state.resources[key] !== undefined) {
                            this.state.resources[key] += val;
                            changes[key] = (changes[key] || 0) + val;
                        }
                    }
                }
            }
        }

        // Critical resource penalties
        let healthPenalty = 0;
        const penaltyMessages = [];

        if (this.state.resources.hunger <= 0) {
            healthPenalty += 15;
            penaltyMessages.push('⚠️ Starving! Your health is declining rapidly.');
        }
        if (this.state.resources.warmth <= 0) {
            healthPenalty += 20;
            penaltyMessages.push('⚠️ Freezing! Your health is declining rapidly.');
        }
        if (this.state.resources.water !== undefined && this.state.resources.water <= 0) {
            healthPenalty += 20;
            penaltyMessages.push('⚠️ Dehydrated! Your health is declining rapidly.');
        }

        if (healthPenalty > 0) {
            this.state.resources.health -= healthPenalty;
            changes.health = (changes.health || 0) - healthPenalty;
            penaltyMessages.forEach(msg => this.addJournalEntry(msg));
        }

        // Fire extinguished by storm
        if (this.state.hasFire && this.state.weather) {
            const weatherType = this.state.weather.type;
            if (weatherType === 'blizzard' || weatherType === 'sandstorm') {
                this.state.hasFire = false;
                this.state.fireExtinguished = true;
                this.addJournalEntry('🔥 The storm has extinguished your fire!');
                this.showToast('🔥 Your fire was put out by the storm!', 'danger');
            } else if (weatherType === 'freezing_rain' || weatherType === 'rain') {
                if (Math.random() < 0.3) {
                    this.state.hasFire = false;
                    this.state.fireExtinguished = true;
                    this.addJournalEntry('🔥 The rain has put out your fire.');
                    this.showToast('🔥 Your fire was put out by the rain.', 'warning');
                }
            }
        }

        // Low resource morale penalty
        if (this.state.resources.hunger <= 20 && this.state.resources.hunger > 0) {
            this.state.resources.morale -= 3;
            changes.morale = (changes.morale || 0) - 3;
        }
        if (this.state.resources.warmth <= 20 && this.state.resources.warmth > 0) {
            this.state.resources.morale -= 3;
            changes.morale = (changes.morale || 0) - 3;
        }

        // Injury morale penalty
        if (this.state.injuries && this.state.injuries.length > 0) {
            const injuryMoralePenalty = this.state.injuries.length * 2;
            this.state.resources.morale -= injuryMoralePenalty;
            changes.morale = (changes.morale || 0) - injuryMoralePenalty;
        }

        this.clampResources();

        this.state.daysSurvived = this.state.day;
        this.state.day++;

        // Advance season
        const cycleDays = scenario.season_cycle_days || 10;
        const seasonOrder = scenario.seasons || ['Spring', 'Summer', 'Autumn', 'Winter'];
        const startSeasonName = scenario.start_season;
        const startIdx = seasonOrder.indexOf(startSeasonName) !== -1 ? seasonOrder.indexOf(startSeasonName) : ['Spring', 'Summer', 'Autumn', 'Winter'].indexOf(startSeasonName);
        const currentSeasonIdx = (startIdx + Math.floor((this.state.day - 1) / cycleDays)) % seasonOrder.length;
        this.state.season = seasonOrder[currentSeasonIdx];

        this.dayEndChanges = changes;

        // ── Injury checks (end of day) ──

        // Frostbite check
        const frostbiteCheck = this.scenarioData?.frostbite_check;
        if (frostbiteCheck && this.state.resources.warmth <= frostbiteCheck.warmth_threshold && !this.hasInjury('frostbite') && !this.state.hasFire) {
            if (Math.random() < frostbiteCheck.injury_chance) {
                this.addInjury('frostbite');
            }
        }

        // Hypothermia check
        const hypothermiaCheck = this.scenarioData?.hypothermia_check;
        if (hypothermiaCheck && this.state.resources.warmth <= hypothermiaCheck.warmth_threshold && !this.hasInjury('hypothermia') && !this.state.hasFire) {
            if (Math.random() < hypothermiaCheck.injury_chance) {
                this.addInjury('hypothermia');
            }
        }

        // Desert: Sunstroke check in hot weather with low water
        if (this.state.weather && (this.state.weather.type === 'scorching' || this.state.weather.type === 'hot')) {
            if (this.state.resources.water <= 30 && !this.hasInjury('sunstroke')) {
                if (Math.random() < 0.25) {
                    this.addInjury('sunstroke');
                    this.addJournalEntry('🥵 The relentless sun has given you sunstroke.');
                }
            }
        }

        // Infection check from untreated cuts
        if (this.hasInjury('cut')) {
            if (Math.random() < 0.15) {
                this.removeInjury('cut');
                this.addInjury('infection');
                this.addJournalEntry('🦠 Your untreated cut has become infected.');
            }
        }

        // ── Alaska: Storm warning countdown ──
        if (this.state.scenarioId === 'alaska_winter' && this.state.stormWarning > 0) {
            this.state.stormWarning--;
            if (this.state.stormWarning > 0) {
                this.addJournalEntry(`⚠️ The wind is picking up. The great storm arrives in ${this.state.stormWarning} day${this.state.stormWarning > 1 ? 's' : ''}.`);
            }
        }

        // ── Consecutive days tracking (before death check so trap endings trigger) ──

        // Alaska: Cabin consecutive days
        if (this.state.scenarioId === 'alaska_winter') {
            if (this.state.currentLocation === 'abandoned_cabin') {
                this.state.cabinDaysConsecutive = (this.state.cabinDaysConsecutive || 0) + 1;
            } else {
                this.state.cabinDaysConsecutive = 0;
            }
        }

        // Desert: Mine consecutive days
        if (this.state.scenarioId === 'desert') {
            if (this.state.currentLocation === 'abandoned_mine') {
                this.state.mineDaysConsecutive = (this.state.mineDaysConsecutive || 0) + 1;
            } else {
                this.state.mineDaysConsecutive = 0;
            }
        }

        // Tropical Island: Wreck consecutive days
        if (this.state.scenarioId === 'tropical_island') {
            if (this.state.currentLocation === 'lagoon_shipwreck') {
                this.state.wreckDaysConsecutive = (this.state.wreckDaysConsecutive || 0) + 1;
            } else {
                this.state.wreckDaysConsecutive = 0;
            }
        }

        // Wild Forest: Grove consecutive days
        if (this.state.scenarioId === 'wild_forest') {
            if (this.state.currentLocation === 'mushroom_grove') {
                this.state.groveDaysConsecutive = (this.state.groveDaysConsecutive || 0) + 1;
            } else {
                this.state.groveDaysConsecutive = 0;
            }
        }

        // Overgrown City: Supermarket consecutive days
        if (this.state.scenarioId === 'overgrown_city') {
            if (this.state.currentLocation === 'abandoned_supermarket') {
                this.state.supermarketDaysConsecutive = (this.state.supermarketDaysConsecutive || 0) + 1;
            } else {
                this.state.supermarketDaysConsecutive = 0;
            }
        }

        // ── Desert: Sandstorm displacement ──
        if (this.state.weather && this.state.weather.type === 'sandstorm') {
            const shelterData2 = this.scenarioData?.shelter;
            const shelterBonus = shelterData2 ? shelterData2[this.state.shelterLevel]?.warmth_bonus || 0 : 0;

            if (shelterBonus < 4) {
                if (Math.random() < 0.5) {
                    const lostProgress = Math.floor(Math.random() * 3) + 1;
                    this.state.exploreProgress = Math.max(0, this.state.exploreProgress - lostProgress);
                    this.state.resources.morale -= 8;
                    this.state.resources.water -= 5;
                    this.state.resources.health -= 3;
                    this.addJournalEntry('🏜️ The sandstorm forced you off course. You lost your bearings and wandered for hours before finding shelter.');
                    this.showToast('🏜️ Lost in the sandstorm!', 'danger');
                } else {
                    this.state.resources.morale -= 4;
                    this.state.resources.water -= 3;
                    this.addJournalEntry('🏜️ The sandstorm raged outside. You huddled in what shelter you had, sand getting into everything.');
                }
            }
        }

        // ── Desert: Scorching heat extra water drain ──
        if (this.state.weather && this.state.weather.type === 'scorching') {
            if (this.state.resources.water <= 30) {
                this.state.resources.health -= 3;
                if (!this.hasInjury('sunstroke') && Math.random() < 0.15) {
                    this.addInjury('sunstroke');
                    this.addJournalEntry('🥵 The relentless heat has given you sunstroke.');
                }
            }
        }

        // ── Check achievements ──
        this.checkAchievements();

        // ── Death / ending check ──
        if (this.state.resources.health <= 0) {
            this.state.causeOfDeath = this.determineCauseOfDeath();
            const severeInjury = this.state.injuries?.find(i => i.severity === 'severe');
            if (severeInjury) {
                this.state.causeOfDeath = severeInjury.id;
            }
            this.checkEndings();
            return;
        }

        if (this.checkEndings()) return;

        this.setState('day_end');
    }

    nextDay() {
        this.startDay();
    }

    applyEffects(effects) {
        if (!effects) return;

        const keyMap = {
            'food': 'hunger',
            'hunger_restore': 'hunger',
            'heal': 'health',
            'health_restore': 'health',
            'warmth_restore': 'warmth',
            'heat': 'warmth',
            'morale_restore': 'morale',
            'water_restore': 'water',
            'hydration': 'water'
        };

        for (const [key, value] of Object.entries(effects)) {
            if (key === 'inventory_add') {
                if (Array.isArray(value)) {
                    this.state.inventory.push(...value);
                } else {
                    this.state.inventory.push(value);
                }
                continue;
            }
            if (key === 'shelter_progress') {
                const maxShelter = this.scenarioData?.shelter?.length ? this.scenarioData.shelter.length - 1 : 3;
                this.state.shelterLevel = Math.min(this.state.shelterLevel + value, maxShelter);
                continue;
            }
            if (key === 'signal_progress') {
                this.state.signalProgress += value;
                continue;
            }
            if (key === 'explore_bonus' || key === 'explore_progress') {
                this.state.exploreProgress += value;
                continue;
            }
            if (key === 'signal_override') {
                this.state.signalProgress = value;
                console.log(`[FQ] Signal progress overridden to ${value}`);
                continue;
            }
            if (key === 'forestKarma') {
                this.state.forestKarma = Math.max(0, Math.min(100, (this.state.forestKarma || 50) + value));
                console.log(`[FQ] Forest karma changed by ${value}, now ${this.state.forestKarma}`);
                continue;
            }
            if (key === 'wildRespect') {
                this.state.wildRespect = Math.max(0, Math.min(100, (this.state.wildRespect || 50) + value));
                console.log(`[FQ] Wild respect changed by ${value}, now ${this.state.wildRespect}`);
                continue;
            }
            if (key === 'islandRespect') {
                this.state.islandRespect = Math.max(0, Math.min(100, (this.state.islandRespect || 50) + value));
                console.log(`[FQ] Island respect changed by ${value}, now ${this.state.islandRespect}`);
                continue;
            }

            const mappedKey = keyMap[key] || key;

            if (this.state.resources[mappedKey] !== undefined) {
                this.state.resources[mappedKey] += value;
                console.log(`[FQ] Applied effect: ${mappedKey} ${value > 0 ? '+' : ''}${value} (original key: ${key})`);
            } else {
                console.warn(`[FQ] Unknown effect key: "${key}" (mapped: "${mappedKey}"). Value: ${value}`);
            }
        }

        this.clampResources();
        console.log('[FQ] Resources after effects:', JSON.stringify(this.state.resources));
    }

    clampResources() {
        const max = this.state.maxResources;
        for (const key of Object.keys(max)) {
            if (this.state.resources[key] !== undefined) {
                this.state.resources[key] = Math.max(0, Math.min(max[key], this.state.resources[key]));
            }
        }
    }

    // ==========================================
    // 5b. HELPER GETTERS & JOURNAL
    // ==========================================

    getScenario() {
        return this.scenarioData;
    }

    getLocation() {
        const scenario = this.getScenario();
        if (!scenario) return null;
        return scenario.locations?.find(l => l.id === this.state.currentLocation) || scenario.locations[0];
    }

    getShelterName() {
        const shelterData = this.scenarioData?.shelter;
        if (shelterData && shelterData[this.state.shelterLevel]) {
            return shelterData[this.state.shelterLevel];
        }
        return { name: 'No Shelter', icon: '🌧️', desc: 'No shelter' };
    }

    getSignalProgress() {
        const current = this.state.signalProgress || 0;
        const max = 7;
        const bars = '█'.repeat(Math.floor(current)) + '░'.repeat(max - Math.floor(current));
        return `${bars} ${current}/${max}`;
    }

    getExploreProgress() {
        const scenario = this.getScenario();
        if (!scenario) return '0/?';
        const total = scenario.locations?.length || 0;
        const found = this.state.knownLocations?.length || 0;
        return `${found}/${total}`;
    }

    addJournalEntry(text) {
        if (!this.state.journal) this.state.journal = [];
        this.state.journal.push({
            day: this.state.day,
            text: text
        });
    }

    // ==========================================
    // 5c. CRITICAL RESOURCE CHECKS
    // ==========================================

    checkCriticalResources() {
        const r = this.state.resources;
        const warnings = [];

        if (r.hunger <= 0) {
            r.health -= 5;
            warnings.push('⚠️ You are starving! Health declining.');
            this.addJournalEntry('⚠️ Starving — your health is failing.');
        }
        if (r.warmth <= 0) {
            r.health -= 5;
            warnings.push('⚠️ You are freezing! Health declining.');
            this.addJournalEntry('⚠️ Freezing — your health is failing.');
        }
        if (r.water !== undefined && r.water <= 0) {
            r.health -= 5;
            warnings.push('⚠️ Dehydrated! Health declining.');
            this.addJournalEntry('⚠️ Dehydrated — your health is failing.');
        }

        // Injury daily effects
        if (this.state.injuries && this.state.injuries.length > 0) {
            for (const injury of this.state.injuries) {
                if (injury.dailyEffects) {
                    this.applyEffects(injury.dailyEffects);
                    warnings.push(`${injury.icon} ${injury.name} is affecting you.`);
                }
            }
        }

        // Frostbite check from low warmth
        const scenario = this.scenarioData || this.getScenario?.();
        if (scenario?.frostbite_check) {
            const fc = scenario.frostbite_check;
            if (r.warmth <= fc.warmth_threshold && !this.hasInjury('frostbite')) {
                if (Math.random() < fc.injury_chance) {
                    this.addInjury('frostbite');
                    warnings.push(fc.message);
                    this.addJournalEntry(`🥶 ${fc.message}`);
                }
            }
        }

        // Hypothermia check
        if (scenario?.hypothermia_check) {
            const hc = scenario.hypothermia_check;
            if (r.warmth <= hc.warmth_threshold && !this.hasInjury('hypothermia')) {
                if (Math.random() < hc.injury_chance) {
                    this.addInjury('hypothermia');
                    warnings.push(hc.message);
                    this.addJournalEntry(`❄️ ${hc.message}`);
                }
            }
        }

        // Infection check from untreated cuts
        if (this.hasInjury('cut')) {
            const cutInjury = this.state.injuries.find(i => i.id === 'cut');
            if (cutInjury && cutInjury.daysRemaining >= 2 && Math.random() < 0.15) {
                this.removeInjury('cut');
                this.addInjury('infection');
                warnings.push('🦠 Your cut has become infected!');
                this.addJournalEntry('🦠 Your untreated cut has become infected.');
            }
        }

        // Desert: Sunstroke check in hot weather with low water
        if (this.state.scenarioId === 'desert' && !this.hasInjury('sunstroke')) {
            if (this.state.weather && (this.state.weather.type === 'scorching' || this.state.weather.type === 'hot')) {
                if (r.water !== undefined && r.water <= 25 && Math.random() < 0.3) {
                    this.addInjury('sunstroke');
                    warnings.push('🥵 The relentless sun has given you sunstroke!');
                    this.addJournalEntry('🥵 The heat overwhelms you. Sunstroke sets in.');
                }
            }
        }

        // Desert: Hallucination check when severely dehydrated
        if (this.state.scenarioId === 'desert' && !this.hasInjury('hallucination')) {
            if (r.water !== undefined && r.water <= 10 && this.state.hallucinationCount < 3 && Math.random() < 0.25) {
                this.addInjury('hallucination');
                this.state.hallucinationCount = (this.state.hallucinationCount || 0) + 1;
                warnings.push('😵‍💫 The desert is playing tricks on your mind.');
                this.addJournalEntry('😵‍💫 Your vision swims. You can\'t trust what you see.');
            }
        }

        // Alaska: Storm warning system
        if (this.state.scenarioId === 'alaska_winter') {
            if (this.state.day >= 8 && this.state.stormWarning === 0 && Math.random() < 0.3) {
                this.state.stormWarning = 3;
                this.addJournalEntry('⚠️ The wind shifts. You feel it in your bones — a big storm is coming.');
                this.showToast('⚠️ A great storm approaches...', 'warning');
            }
        }

        // ── TROPICAL ISLAND: Sunstroke check ──
        if (this.state.scenarioId === 'tropical_island' && !this.hasInjury('sunstroke')) {
            const sunstrokeCheck = this.scenarioData?.sunstroke_check;
            if (sunstrokeCheck) {
                const isHot = this.state.weather && (this.state.weather.type === 'hot' || this.state.weather.type === 'clear');
                const isLowWater = this.state.resources.water !== undefined && this.state.resources.water <= (sunstrokeCheck.water_threshold || 25);

                if (isHot && isLowWater) {
                    const chance = this.state.weather.type === 'hot' ? (sunstrokeCheck.hot_weather_chance || 0.25) * 1.5 : (sunstrokeCheck.hot_weather_chance || 0.25);
                    if (Math.random() < chance) {
                        this.addInjury('sunstroke');
                        this.addJournalEntry(`🥵 ${sunstrokeCheck.message}`);
                        warnings.push(`🥵 ${sunstrokeCheck.message}`);
                    }
                }
            }
        }

        this.clampResources();

        if (r.health <= 0) {
            this.state.causeOfDeath = this.determineCauseOfDeath();
            const severeInjury = this.state.injuries?.find(i => i.severity === 'severe');
            if (severeInjury) {
                this.state.causeOfDeath = severeInjury.id;
            }
            this.checkEndings();
            return { dead: true, warnings };
        }

        return { dead: false, warnings };
    }

    // ==========================================
    // 5d. INJURY SYSTEM
    // ==========================================

    addInjury(injuryId) {
        if (this.hasInjury(injuryId)) {
            console.log(`[FQ] Already have injury: ${injuryId}`);
            return false;
        }

        const injuryDef = this.config?.injuries?.[injuryId];
        if (!injuryDef) {
            console.warn(`[FQ] Unknown injury type: ${injuryId}`);
            return false;
        }

        const injury = {
            id: injuryId,
            name: injuryDef.name,
            icon: injuryDef.icon,
            desc: injuryDef.desc,
            severity: injuryDef.severity,
            dailyEffects: injuryDef.daily_effects || {},
            actionModifiers: injuryDef.action_modifiers || {},
            daysRemaining: injuryDef.duration,
            duration: injuryDef.duration,
            treatments: injuryDef.treatments || {}
        };

        this.state.injuries.push(injury);
        this.addJournalEntry(`${injury.icon} New injury: ${injury.name} — ${injury.desc}`);
        console.log(`[FQ] Injury added: ${injuryId}`, injury);

        this.state.injuryFree = false;
        this.showToast(`${injury.icon} Injury: ${injury.name}`, 'danger');

        this.playAnimation('shake', 500);
        this.playAnimation('hit', 1000);

        return true;
    }

    removeInjury(injuryId) {
        const idx = this.state.injuries.findIndex(i => i.id === injuryId);
        if (idx > -1) {
            const removed = this.state.injuries.splice(idx, 1)[0];
            this.addJournalEntry(`${removed.icon} ${removed.name} has healed!`);
            console.log(`[FQ] Injury removed: ${injuryId}`);
            return true;
        }
        return false;
    }

    hasInjury(injuryId) {
        return this.state.injuries?.some(i => i.id === injuryId) || false;
    }

    getInjuryModifier(actionId, modifierType) {
        let totalPenalty = 0;
        if (!this.state.injuries) return 0;

        for (const injury of this.state.injuries) {
            const mod = injury.actionModifiers?.[actionId];
            if (mod && mod[modifierType] !== undefined) {
                totalPenalty += mod[modifierType];
            }
        }
        return totalPenalty;
    }

    treatInjury(injuryId, treatmentItem) {
        const injury = this.state.injuries.find(i => i.id === injuryId);
        if (!injury) return false;

        const treatment = injury.treatments?.[treatmentItem];
        if (!treatment) {
            this.showToast(`${treatmentItem} cannot treat ${injury.name}`, 'warning');
            return false;
        }

        const idx = this.state.inventory.indexOf(treatmentItem);
        if (idx > -1) {
            this.state.inventory.splice(idx, 1);
        }

        if (treatment.days_reduction) {
            injury.daysRemaining -= treatment.days_reduction;
        }
        if (treatment.health_bonus) {
            this.state.resources.health += treatment.health_bonus;
        }

        if (injury.daysRemaining <= 0) {
            this.removeInjury(injuryId);
            this.showToast(`${injury.icon} ${injury.name} fully healed!`, 'success');
        } else {
            this.showToast(`${injury.icon} ${injury.name} improved — ${injury.daysRemaining} days remaining`, 'info');
        }

        this.state.injuriesTreated = (this.state.injuriesTreated || 0) + 1;
        this.clampResources();
        this.checkAchievements();
        return true;
    }

    processInjuryHealing() {
        if (!this.state.injuries || this.state.injuries.length === 0) return;

        const healed = [];
        for (const injury of this.state.injuries) {
            injury.daysRemaining--;
            if (injury.daysRemaining <= 0) {
                healed.push({ id: injury.id, name: injury.name, icon: injury.icon });
            }
        }

        for (const h of healed) {
            this.removeInjury(h.id);
            this.showToast(`${h.icon} ${h.name} has healed naturally!`, 'success');
        }
    }

    // ==========================================
    // 5e. ACHIEVEMENT SYSTEM
    // ==========================================

    checkAchievements() {
        const achievementDefs = this.config?.achievements;
        if (!achievementDefs) return;

        const state = this.state;
        const scenario = this.getScenario();

        for (const [id, ach] of Object.entries(achievementDefs)) {
            if (state.achievements.includes(id)) continue;

            let earned = false;

            switch (ach.type) {
                case 'days':
                    earned = state.day >= ach.threshold;
                    break;
                case 'plants':
                    earned = (state.plantsCorrect || 0) >= ach.threshold;
                    break;
                case 'locations':
                    if (ach.threshold === 'all') {
                        earned = scenario && state.knownLocations.length >= scenario.locations.length;
                    } else {
                        earned = state.knownLocations.length >= ach.threshold;
                    }
                    break;
                case 'crafts':
                    earned = (state.itemsCrafted || []).length >= ach.threshold;
                    break;
                case 'treatments':
                    earned = (state.injuriesTreated || 0) >= ach.threshold;
                    break;
                case 'hunts':
                    earned = (state.huntsSuccessful || 0) >= ach.threshold;
                    break;
                case 'signal':
                    earned = state.signalProgress >= ach.threshold;
                    break;
                case 'shelter':
                    if (ach.threshold === 'max') {
                        const maxShelter = this.scenarioData?.shelter?.length ? this.scenarioData.shelter.length - 1 : 3;
                        earned = state.shelterLevel >= maxShelter;
                    }
                    break;
                case 'no_injuries':
                    earned = (state.injuryFree !== false) && state.day >= ach.threshold;
                    break;
                case 'all_crafts':
                    if (ach.threshold === 'all') {
                        const allRecipes = Object.keys(this.config.crafting || {});
                        earned = allRecipes.every(r => (state.itemsCrafted || []).includes(r));
                    }
                    break;
                case 'companions':
                    const activeComps = (state.companions || []).filter(c => c.status === 'active');
                    earned = activeComps.length >= ach.threshold;
                    break;
                case 'days_city':
                    earned = state.scenarioId === 'overgrown_city' && state.day >= ach.threshold;
                    break;
                case 'pack_driven':
                    earned = state.eventsCompleted && state.eventsCompleted.includes('pack_attack') && state.scenarioId === 'overgrown_city';
                    break;
            }

            if (earned) {
                state.achievements.push(id);
                this.addJournalEntry(`🏆 Achievement Unlocked: ${ach.icon} ${ach.name} — ${ach.desc}`);
                this.showToast(`🏆 ${ach.icon} ${ach.name}!`, 'achievement');
                console.log(`[FQ] Achievement unlocked: ${id}`);
            }
        }
    }

    // ==========================================
    // 5f. ANIMATION & DESERT MECHANICS
    // ==========================================

    playAnimation(type, duration = 1000) {
        if (type === 'eyes_in_dark') {
            const eyesContainer = document.createElement('div');
            eyesContainer.className = 'eyes-in-dark';
            for (let i = 0; i < 5; i++) {
                const pair = document.createElement('div');
                pair.className = 'eye-pair';
                pair.innerHTML = '<div class="eye"></div><div class="eye"></div>';
                eyesContainer.appendChild(pair);
            }
            document.body.appendChild(eyesContainer);
            setTimeout(() => { if (eyesContainer.parentNode) eyesContainer.remove(); }, duration);
            return;
        }

        if (type === 'shake') {
            const container = document.getElementById('game-container') || document.body;
            container.classList.remove('anim-screen-shake');
            void container.offsetWidth;
            container.classList.add('anim-screen-shake');
            setTimeout(() => { container.classList.remove('anim-screen-shake'); }, duration);
            return;
        }

        if (type === 'fairy_glow') {
            const glow = document.createElement('div');
            glow.className = 'anim-fairy-glow';
            glow.innerHTML = '<div class="fairy-light"></div><div class="fairy-light"></div><div class="fairy-light"></div>';
            document.body.appendChild(glow);
            setTimeout(() => { if (glow.parentNode) glow.remove(); }, duration);
            return;
        }

        if (type === 'vultures') {
            const vultures = document.createElement('div');
            vultures.className = 'anim-vultures';
            vultures.innerHTML = '🦅🦅🦅';
            document.body.appendChild(vultures);
            setTimeout(() => { if (vultures.parentNode) vultures.remove(); }, duration);
            return;
        }

        if (type === 'storm_flash') {
            const flash = document.createElement('div');
            flash.className = 'anim-storm-flash';
            document.body.appendChild(flash);
            setTimeout(() => { if (flash.parentNode) flash.remove(); }, 500);
            setTimeout(() => this.playAnimation('shake', 300), 500);
            return;
        }

        if (type === 'discovery') {
            const reveal = document.createElement('div');
            reveal.className = 'anim-discovery-reveal';
            reveal.innerHTML = '📍✨';
            document.body.appendChild(reveal);
            setTimeout(() => { if (reveal.parentNode) reveal.remove(); }, duration);
            return;
        }

        // All other CSS-based animations
        const container = document.body;
        container.classList.remove('anim-screen-shake', 'anim-health-hit', 'anim-despair', 'anim-sandstorm', 'anim-heat-shimmer');
        void container.offsetWidth;

        let specificClass = '';
        switch (type) {
            case 'hit': specificClass = 'anim-health-hit'; break;
            case 'despair': specificClass = 'anim-despair'; break;
            case 'sandstorm': specificClass = 'anim-sandstorm'; break;
            case 'heat': specificClass = 'anim-heat-shimmer'; break;
            case 'plane':
                this.triggerPlaneFlyover();
                return;
        }

        if (specificClass) {
            container.classList.add(specificClass);
            if (type !== 'heat' && type !== 'sandstorm') {
                setTimeout(() => { container.classList.remove(specificClass); }, duration);
            }
        }
    }

    triggerPlaneFlyover() {
        const container = document.body;
        container.classList.add('anim-plane-shadow');

        const plane = document.createElement('div');
        plane.className = 'anim-plane-flyover';
        plane.textContent = '✈️';
        document.body.appendChild(plane);

        setTimeout(() => {
            container.classList.remove('anim-plane-shadow');
            plane.remove();
            this.playAnimation('despair', 3000);
        }, 4000);
    }

    applyDesertWeatherDecay() {
        const weather = this.state.weather;
        if (!weather) return;

        let waterDrain = 0;
        let warmthDrain = 0;

        switch (weather.type) {
            case 'scorching': waterDrain = 10; break;
            case 'hot': waterDrain = 5; break;
            case 'sandstorm': waterDrain = 3; break;
            case 'cool_night': warmthDrain = 5; break;
        }

        if (waterDrain > 0) {
            this.state.resources.water = Math.max(0, this.state.resources.water - waterDrain);
        }
        if (warmthDrain > 0) {
            this.state.resources.warmth = Math.max(0, this.state.resources.warmth - warmthDrain);
        }
    }

    applyPassiveCraftEffects() {
        const inventory = this.state.inventory;
        this.state.dailyMessageShown = this.state.dailyMessageShown || [];

        // Solar Still: Generates water passively
        if (inventory.includes('solar_still')) {
            this.state.resources.water += 8;
            if (!this.state.dailyMessageShown.includes('solar_still')) {
                this.addJournalEntry('🫗 Your solar still collected some condensation. (+8 Water)');
                this.state.dailyMessageShown.push('solar_still');
            }
        }

        // Sun Hat: Reduces water decay in hot weather
        if (inventory.includes('sun_hat')) {
            if (this.state.weather && (this.state.weather.type === 'scorching' || this.state.weather.type === 'hot')) {
                this.state.resources.water += 5;
                if (!this.state.dailyMessageShown.includes('sun_hat')) {
                    this.addJournalEntry('👒 Your sun hat protects you from the worst of the heat.');
                    this.state.dailyMessageShown.push('sun_hat');
                }
            }
        }

        // Fur Wrap: Helpful on cold nights, terrible in the heat
        if (inventory.includes('fur_wrap')) {
            if (this.state.weather && (this.state.weather.type === 'cool_night' || this.state.weather.type === 'sandstorm')) {
                this.state.resources.warmth += 5;
            } else if (this.state.weather && this.state.weather.type === 'scorching') {
                this.state.resources.warmth -= 3;
                if (!this.state.dailyMessageShown.includes('fur_wrap_bad')) {
                    this.addJournalEntry('🧣 Wearing a fur wrap in this heat is suffocating.');
                    this.state.dailyMessageShown.push('fur_wrap_bad');
                }
            }
        }

        // Foxfire Lantern: Morale bonus and prevents "eyes in the dark" events
        if (inventory.includes('foxfire_lantern')) {
            this.state.resources.morale += 5;
            if (!this.state.dailyMessageShown.includes('foxfire_lantern')) {
                this.addJournalEntry('👻 Your foxfire lantern casts an eerie blue glow. The watching eyes keep their distance.');
                this.state.dailyMessageShown.push('foxfire_lantern');
            }
        }
    }

    getLoseChanceReduction() {
        if (this.state.inventory.includes('rowan_talisman')) return 1;
        return 0;
    }

    // ==========================================
    // 6. WEATHER & SEASON
    // ==========================================

    generateWeather() {
        const scenario = this.getScenario();
        const weatherChances = scenario.weather_chances?.[this.state?.season || scenario.start_season];
        if (!weatherChances) {
            return { name: 'Clear', icon: '☀️', desc: 'The weather is clear.', warmth_mod: 0, morale_mod: 0, water_mod: 0 };
        }

        const roll = Math.random();
        let cumulative = 0;
        for (const [type, chance] of Object.entries(weatherChances)) {
            cumulative += chance;
            if (roll <= cumulative) {
                const weatherData = scenario.weather_types[type];
                return {
                    type,
                    name: weatherData.desc?.split('.')[0] || type,
                    ...weatherData
                };
            }
        }

        return { name: 'Clear', icon: '☀️', desc: 'The weather is clear.', warmth_mod: 0, morale_mod: 0, water_mod: 0 };
    }

    applyWeatherEffects() {
        if (!this.state.weather) return;

        if (this.state.weather.warmth_mod) {
            this.state.resources.warmth += this.state.weather.warmth_mod;
        }
        if (this.state.weather.morale_mod) {
            this.state.resources.morale += this.state.weather.morale_mod;
        }
        if (this.state.weather.water_mod) {
            this.state.resources.water = (this.state.resources.water || 0) + this.state.weather.water_mod;
        }
    }

        // ==========================================
    // 7. ACTION RESOLUTION
    // ==========================================

    getActionHours(actionId) {
        const action = this.config.actions[actionId];
        if (!action) return 0;
        return action.hours;
    }

    resolveExplore(location, scenario) {
        const locations = scenario.locations;
        const undiscovered = locations.filter(l => !this.state.knownLocations.includes(l.id));

        const result = {
            actionId: 'explore',
            actionName: 'Explore',
            actionIcon: '🧭',
            hours: 3,
            text: '',
            effects: {},
            discoveries: [],
            success: true,
            loot: []
        };

        // Apply injury modifiers
        const hoursPenalty = this.getInjuryModifier('explore', 'hours_penalty');
        result.hours = 3 + hoursPenalty;
        this.state.hoursRemaining -= hoursPenalty;

        const exploreGain = location?.explore_hours ? 1 : 2;
        result.effects.explore_progress = exploreGain;

        if (undiscovered.length > 0 && Math.random() < 0.6) {
            const newLoc = undiscovered[Math.floor(Math.random() * undiscovered.length)];
            this.state.knownLocations.push(newLoc.id);
            result.discoveries = [newLoc.id];
            result.text = `You push through the terrain and discover a new area: ${newLoc.icon} ${newLoc.name}. ${newLoc.desc}`;
            result.effects.morale = 5;
        } else if (undiscovered.length === 0) {
            result.text = 'You explore but find nothing new. You know this area well now.';
            result.effects.morale = -2;
        } else {
            result.text = 'You spend time exploring but don\'t find anything new today. The landscape stretches on.';
            result.effects.morale = -1;
            result.effects.hunger = -2;
        }

        // Random item finds while exploring
        if (Math.random() < 0.2) {
            const possibleFinds = scenario.id === 'alaska_winter'
                ? ['wire', 'cordage', 'knife_blade']
                : scenario.id === 'desert'
                ? ['cordage', 'tin_can']
                : ['cordage', 'wood', 'medicinal_herbs'];
            const found = possibleFinds[Math.floor(Math.random() * possibleFinds.length)];
            result.loot = [found];
            result.text += ` While exploring, you find: ${this.getItemIcon(found)} ${found.replace(/_/g, ' ')}.`;
        }

        // Medicinal herbs chance
        if (Math.random() < 0.15) {
            result.loot = result.loot || [];
            result.loot.push('medicinal_herbs');
            result.text += ' You notice some useful-looking herbs growing nearby.';
        }

        const loseChance = Math.max(0, (location?.lose_chance || 0) - this.getLoseChanceReduction() + this.getKarmaLoseChanceModifier());
        if (loseChance > 0 && Math.random() < loseChance) {
            result.text += ' You get disoriented and lose your way briefly.';
            result.effects.health = -5;
            result.effects.morale = -3;

            if (Math.random() < 0.3) {
                result.text += ' You twist your ankle on the rough terrain.';
                this.addInjury('sprained_ankle');
            }
        }

        this.checkAchievements();

        if (result.discoveries && result.discoveries.length > 0) {
            this.playAnimation('discovery', 2000);
        }

        return result;
    }

    getItemIcon(itemId) {
        const icons = {
            compass: '🧭', water_bottle: '🍶', wood: '🪵', cordage: '🧶',
            knife_blade: '🔪', tin_can: '🥫', wire: '🔗', fish: '🐟',
            lighter: '🔥', backpack: '🎒', walking_stick: '🦯',
            snare: '🪤', spear: '🗡️', water_filter: '🫗', fire_bow: '🔥',
            shade_cloth: '🫧', rabbit: '🐇', water: '💧',
            raw_meat: '🥩', animal_fur: '🦊', feathers: '🪶',
            medicinal_herbs: '🌿', bandage: '🩹', herbal_tea: '🍵',
            bow: '🏹', fishing_rod: '🎣', fur_wrap: '🧣', splint: '🦴',
            herbal_poultice: '🌿', cooked_food: '🍖',
            glowing_fungi: '✨', berries: '🫐', coins: '🪙',
            sun_hat: '👒', solar_still: '🫗', rowan_talisman: '🪬',
            foxfire_lantern: '👻', offering_bundle: '🍂',
            canned_food: '🥫', med_kit: '🏥', community_meal: '🍲',
            research_notes: '📋'
        };
        return icons[itemId] || '📦';
    }

    effectsToBadges(effects, isGoodContext = true) {
        if (!effects || Object.keys(effects).length === 0) return '';

        const labels = {
            health: '❤️ Health', hunger: '🍖 Hunger', warmth: '🔥 Warmth',
            morale: '💭 Morale', water: '💧 Water', shelter_progress: '🏕️ Shelter',
            signal_progress: '📡 Signal', explore_progress: '🧭 Explore',
            explore_bonus: '🧭 Explore', forestKarma: '🌿 Forest Karma'
        };

        let html = '<div class="fq-effects-badges">';
        for (const [key, val] of Object.entries(effects)) {
            if (val === 0 || key === 'inventory_add') continue;
            const label = labels[key] || key.replace(/_/g, ' ');
            const sign = val > 0 ? '+' : '';
            const cls = val > 0 ? 'fq-badge-positive' : 'fq-badge-negative';
            html += `<span class="fq-effect-badge ${cls}">${label} ${sign}${val}</span>`;
        }
        html += '</div>';
        return html;
    }

    dangerLevelColor(level) {
        const colors = {
            'SAFE': '#4caf50', 'CAUTION': '#ff9800', 'POISONOUS': '#f44336',
            'HIGH': '#d32f2f', 'EXTREME': '#b71c1c', 'DEADLY': '#880e4f'
        };
        return colors[level] || '#ff5722';
    }

    resolveBuildShelter(location, scenario) {
        const shelterData = this.scenarioData?.shelter;
        const currentLevel = this.state.shelterLevel;
        const maxLevel = shelterData ? shelterData.length - 1 : 3;

        const result = {
            actionId: 'build_shelter',
            actionName: 'Build Shelter',
            actionIcon: '🏕️',
            hours: 4,
            text: '',
            effects: {},
            success: true
        };

        if (currentLevel >= maxLevel) {
            result.text = 'Your shelter is already as good as it can be. You spend the time reinforcing it instead.';
            result.effects.warmth = 3;
            result.effects.morale = 2;
            return result;
        }

        if (location?.shelter_level && location.shelter_level > this.state.shelterLevel) {
            this.state.shelterLevel = location.shelter_level;
            result.text = `You discover ${location.name} — it has better natural shelter than your current setup! Your shelter improves to: ${shelterData[this.state.shelterLevel].name}.`;
            result.effects.morale = 8;
            return result;
        }

        this.state.shelterLevel++;
        const newShelter = shelterData ? shelterData[this.state.shelterLevel] : null;

        if (newShelter) {
            result.text = `You work on improving your shelter. It's now: ${newShelter.icon} ${newShelter.name}. ${newShelter.desc}`;
            result.effects.warmth = 5;
            result.effects.morale = 5;
        } else {
            result.text = 'You improve your shelter. It feels more secure now.';
            result.effects.warmth = 5;
            result.effects.morale = 3;
        }

        return result;
    }

    resolveGatherWood(location, scenario) {
        const result = {
            actionId: 'gather_wood',
            actionName: 'Gather Wood',
            actionIcon: '🪵',
            hours: 2,
            text: '',
            effects: {},
            success: true
        };

        this.state.inventory.push('wood');

        if (this.state.inventory.filter(i => i === 'wood').length > 1) {
            result.text = 'You gather more wood. Your stockpile grows.';
            result.effects.warmth = 2;
        } else {
            result.text = 'You gather dry wood and branches. This will be useful for fire and shelter.';
            result.effects.warmth = 2;
            result.effects.morale = 2;
        }

        if (scenario.id === 'wild_forest') {
            result.text = 'The forest provides. You gather an armful of dry wood and fallen branches.';
        } else if (scenario.id === 'alaska_winter') {
            result.text = 'You find dead spruce branches and break frozen wood. It takes effort but you gather enough.';
            result.effects.health = -2;
        } else if (scenario.id === 'desert') {
            result.text = 'Wood is scarce here. You find dried scrub and dead branches. Barely enough, but it\'s something.';
        }

        return result;
    }

    resolveSignal(location, scenario) {
        const result = {
            actionId: 'signal',
            actionName: 'Signal for Help',
            actionIcon: '📡',
            hours: 2,
            text: '',
            effects: {},
            success: true
        };

        if (!this.state.inventory.includes('wood')) {
            result.text = 'You need wood to build a signal fire. Gather wood first.';
            result.effects = {};
            this.state.actionsUsed--;
            this.state.hoursRemaining += 2;
            return result;
        }

        const woodIdx = this.state.inventory.indexOf('wood');
        if (woodIdx > -1) this.state.inventory.splice(woodIdx, 1);

        let signalGain = 1;
        if (location?.signal_bonus) {
            signalGain += location.signal_bonus;
        }

        result.effects.signal_progress = signalGain;

        if (location?.signal_bonus && location.signal_bonus >= 2) {
            result.text = `You build a signal fire at ${location.name}. The elevated position means it can be seen for miles! Progress: ${this.state.signalProgress}/7`;
        } else {
            result.text = `You build and maintain a signal fire. Smoke rises into the sky. Progress: ${this.state.signalProgress}/7`;
        }

        result.effects.morale = 3;
        this.state.lastSignalDay = this.state.day;
        return result;
    }

    resolveRest(location, scenario) {
        const result = {
            actionId: 'rest',
            actionName: 'Rest',
            actionIcon: '💤',
            hours: 3,
            text: '',
            effects: {},
            success: true
        };

        const shelterData = this.scenarioData?.shelter;
        const shelterName = shelterData ? shelterData[this.state.shelterLevel]?.name || 'no shelter' : 'no shelter';

        let healthGain = 5;
        let moraleGain = 8;
        let hungerLoss = 3;

        if (this.state.shelterLevel >= 2) {
            healthGain += 5;
            moraleGain += 3;
        }

        result.effects.health = healthGain;
        result.effects.morale = moraleGain;
        result.effects.hunger = -hungerLoss;

        if (this.state.shelterLevel >= 2) {
            result.text = `You rest in your ${shelterName}. The shelter keeps the worst of the weather out. You wake feeling refreshed.`;
        } else {
            result.text = `You rest as best you can under ${shelterName}. It's not comfortable, but your body needs the recovery time.`;
        }

        // Desert heat penalty while resting
        if (scenario.id === 'desert' && this.state.resources.water !== undefined) {
            const waterLoss = this.state.weather?.type === 'scorching' ? 8 : 5;
            result.effects.water = -waterLoss;
            result.text += ' The heat saps your water even while resting.';
        }

        return result;
    }

    resolveHunt(location, scenario) {
        const result = {
            actionId: 'hunt',
            actionName: 'Hunt / Set Traps',
            actionIcon: '🪤',
            hours: 3,
            text: '',
            effects: {},
            success: true,
            loot: []
        };

        let successRate = 0.25;

        if (this.state.inventory.includes('snare')) successRate += 0.2;
        if (this.state.inventory.includes('spear')) successRate += 0.15;
        if (this.state.inventory.includes('bow')) successRate += 0.25;
        if (this.state.inventory.includes('cordage')) successRate += 0.1;
        if (location?.id === 'dense_woodland' || location?.id === 'spruce_grove') successRate += 0.1;
        if (location?.id === 'bear_den') successRate += 0.15;

        // Sam's scavenging bonus applies to hunting too
        if (this.hasCompanion('sam')) successRate += 0.1;

        const huntPenalty = this.getInjuryModifier('hunt', 'success_penalty');
        successRate = Math.max(0.05, successRate - huntPenalty);

        if (this.state.inventory.includes('fishing_rod') && location?.water_source) {
            successRate += 0.3;
        }

        const roll = Math.random();

        if (roll < successRate) {
            this.state.huntsSuccessful = (this.state.huntsSuccessful || 0) + 1;

            const hasRod = this.state.inventory.includes('fishing_rod') && location?.water_source;
            const hasBow = this.state.inventory.includes('bow');

            if (hasRod && Math.random() < 0.5) {
                result.text = 'You cast your fishing line into the water and wait. A bite! You reel in a fish!';
                result.effects.hunger = 20;
                result.effects.morale = 10;
                result.loot = ['raw_meat', 'fish'];
            } else if (hasBow && Math.random() < 0.4) {
                const prey = scenario.id === 'alaska_winter'
                    ? 'a ptarmigan' : scenario.id === 'desert'
                    ? 'a desert hare' : 'a rabbit';
                result.text = `With your bow, you take down ${prey}. Good hunting!`;
                result.effects.hunger = 15;
                result.effects.morale = 10;
                result.loot = ['raw_meat', 'feathers'];
            } else if (this.state.inventory.includes('snare')) {
                const prey = scenario.id === 'alaska_winter'
                    ? 'a snowshoe hare' : scenario.id === 'desert'
                    ? 'a desert rat' : 'a rabbit';
                result.text = `Your snare has caught ${prey}. It's not much, but it's protein.`;
                result.effects.hunger = 15;
                result.effects.morale = 8;
                result.loot = ['raw_meat'];
            } else {
                result.text = 'You manage to catch a small animal by hand. Lucky break!';
                result.effects.hunger = 10;
                result.effects.morale = 5;
                result.loot = ['raw_meat'];
            }

            if (scenario.id === 'alaska_winter' && !hasBow && !hasRod) {
                result.text = 'Through the snow, you track and catch a ptarmigan. Not much meat, but it\'s protein.';
                result.effects.hunger = 15;
            }
        } else {
            result.text = 'You set traps and wait, but nothing comes. The wildlife is wary today.';
            result.effects.morale = -3;
            result.effects.hunger = -2;
            result.success = false;
        }

        return result;
    }

    resolveFindWater(location, scenario) {
        const result = {
            actionId: 'find_water',
            actionName: 'Find Water',
            actionIcon: '💧',
            hours: 2,
            text: '',
            effects: {},
            success: true
        };

        // If at a known water source location
        if (location?.water_source) {
            if (scenario.id === 'desert') {
                result.text = `You dig into the sand at ${location.name} and find murky, life-giving water. You drink deeply and fill your container.`;
                result.effects.water = 20;
                result.effects.morale = 8;
            } else if (scenario.id === 'tropical_island') {
                if (location?.id === 'stream_valley') {
                    result.text = 'You follow the sound of running water to a clear stream in the valley. Fresh, cool water — the best thing on this island. You drink deeply and fill your container.';
                    result.effects.water = 25;
                    result.effects.morale = 8;
                } else {
                    result.text = `You find water at ${location.name}. The fresh water is a relief in the tropical heat.`;
                    result.effects.water = 20;
                    result.effects.morale = 5;
                }
            } else if (scenario.id === 'overgrown_city') {
                result.text = `You find collected rainwater at ${location.name}. It's not perfectly clean, but it's drinkable. You fill your container.`;
                result.effects.water = 20;
                result.effects.morale = 5;
            } else {
                result.text = `You find water at ${location.name}. You fill your container and drink deeply.`;
                result.effects.water = 25;
                result.effects.morale = 5;
            }
            return result;
        }

        // ── Overgrown City: Water from rain ──
        if (this.state.scenarioId === 'overgrown_city') {
            if (this.state.weather && (this.state.weather.type === 'rain' || this.state.weather.type === 'thunderstorm')) {
                result.text = 'The rain is your ally today. You set out containers and collect what you can from the downpour.';
                result.effects.water = 15;
                result.effects.morale = 3;
            } else {
                result.text = 'You search for water but the city is dry. The taps don\'t work anymore, and you can\'t find any puddles that haven\'t been contaminated.';
                result.effects.morale = -3;
            }
            return result;
        }

        // ── Tropical Island: Water search when not at a source ──
        if (this.state.scenarioId === 'tropical_island') {
            // Check if player knows any water locations
            const waterLocations = scenario.locations.filter(
                l => l.water_source && this.state.knownLocations.includes(l.id)
            );
            if (waterLocations.length > 0 && Math.random() < 0.6) {
                const wl = waterLocations[0];
                result.text = `You remember the water source at ${wl.name} and head there. Fresh water at last.`;
                result.effects.water = 20;
                result.effects.morale = 3;
            } else if (Math.random() < 0.3) {
                result.text = 'You find a coconut still hanging on a palm. The water inside is warm but refreshing.';
                result.effects.water = 10;
                result.effects.morale = 3;
            } else {
                result.text = 'You search the island for water but find nothing fresh. The sea is all around you, but you can\'t drink that.';
                result.effects.morale = -3;
            }
            return result;
        }

        // ── Generic water finding (Alaska, Wild Forest, etc.) ──
        const waterLocations = scenario.locations.filter(
            l => l.water_source && this.state.knownLocations.includes(l.id)
        );

        if (waterLocations.length > 0 && Math.random() < 0.6) {
            const wl = waterLocations[0];
            result.text = `You remember the water source at ${wl.name} and head there. Fresh water at last.`;
            result.effects.water = 20;
            result.effects.morale = 3;
            return result;
        }

        // Random water find chance (much harder in the desert)
        let findChance = 0.3;
        if (scenario.id === 'desert') {
            findChance = 0.1;
        }

        if (Math.random() < findChance) {
            if (scenario.id === 'desert') {
                result.text = 'A miracle! You find a small puddle trapped in the shade of a rock formation. Barely enough, but it keeps you alive.';
                result.effects.water = 10;
                result.effects.morale = 5;
            } else {
                result.text = 'You find a small seep in the rocks. Not much, but enough to keep you going.';
                result.effects.water = 10;
                result.effects.morale = 2;
            }
        } else {
            if (scenario.id === 'desert') {
                result.text = 'You search the cracked earth for hours, but the desert holds onto its water. Your mouth feels like sandpaper.';
                result.effects.morale = -5;
                result.effects.health = -2;
            } else {
                result.text = 'You search for water but find nothing. The landscape is dry.';
                result.effects.morale = -3;
            }
        }

        return result;
    }

    resolveCraft(location, scenario, craftItemId = null) {
        const result = {
            actionId: 'craft',
            actionName: 'Craft Tool',
            actionIcon: '🔨',
            hours: 2,
            text: '',
            effects: {},
            success: true
        };

        const recipes = this.config.crafting;
        const available = [];

        for (const [id, recipe] of Object.entries(recipes || {})) {
            const hasReqs = recipe.requires.every(r => this.state.inventory.includes(r));
            const alreadyHave = this.state.inventory.includes(id);
            const isConsumable = recipe.consumable;
            if (hasReqs && (isConsumable || !alreadyHave)) {
                available.push({ id, ...recipe });
            }
        }

        if (available.length === 0) {
            result.text = 'You don\'t have the materials to craft anything right now. You need to gather resources first.';
            result.success = false;
            this.state.actionsUsed--;
            this.state.hoursRemaining += 2;
            return result;
        }

        let craft;

        if (craftItemId) {
            craft = available.find(a => a.id === craftItemId);
            if (!craft) {
                result.text = `You don't have the materials to craft ${craftItemId.replace(/_/g, ' ')} right now.`;
                result.success = false;
                this.state.actionsUsed--;
                this.state.hoursRemaining += 2;
                return result;
            }
        } else {
            craft = available[0];
        }

        // Check if this item requires a lit fire
        if (craft.requires_fire && !this.state.hasFire) {
            result.text = `You need a lit fire to make ${craft.name}. Light a fire first.`;
            result.success = false;
            this.state.actionsUsed--;
            this.state.hoursRemaining += 2;
            return result;
        }

        // Remove consumed materials
        for (const req of craft.requires) {
            const idx = this.state.inventory.indexOf(req);
            if (idx > -1) {
                this.state.inventory.splice(idx, 1);
            } else {
                console.warn(`[FQ] Could not find required item: ${req}`);
            }
        }

        this.state.inventory.push(craft.id);

        if (!this.state.itemsCrafted) this.state.itemsCrafted = [];
        if (!this.state.itemsCrafted.includes(craft.id)) {
            this.state.itemsCrafted.push(craft.id);
        }

        // Apply passive effects for equipment
        if (craft.passive_effects) {
            let passiveText = '';
            for (const [key, val] of Object.entries(craft.passive_effects)) {
                if (key === 'warmth_bonus') {
                    this.state.warmthBonus = (this.state.warmthBonus || 0) + val;
                    passiveText = ' The extra warmth is immediately noticeable.';
                }
                if (key === 'water_bonus') {
                    passiveText = ' It starts collecting condensation immediately.';
                }
                if (key === 'water_decay_reduction') {
                    passiveText = ' You put it on. The shade provides immediate relief from the sun.';
                }
            }
            result.text = `You craft: ${craft.icon} ${craft.name}. ${craft.desc}${passiveText}`;
        } else {
            result.text = `You craft: ${craft.icon} ${craft.name}. ${craft.desc}`;
        }

        result.effects.morale = 5;
        result.effects.inventory_add = [craft.id];

        this.checkAchievements();
        return result;
    }

    resolveUseItem(itemId) {
        const result = {
            actionId: 'use_item',
            actionName: 'Use Item',
            actionIcon: '📦',
            hours: 1,
            text: '',
            effects: {},
            success: true
        };

        const idx = this.state.inventory.indexOf(itemId);
        if (idx === -1) {
            result.text = `You don't have ${itemId.replace(/_/g, ' ')} in your inventory.`;
            result.success = false;
            return result;
        }

        const itemDef = this.config.crafting?.[itemId];
        if (!itemDef || !itemDef.consumable) {
            result.text = `${itemDef?.name || itemId} is not a usable item.`;
            result.success = false;
            return result;
        }

        this.state.inventory.splice(idx, 1);

        if (itemDef.use_effects) {
            this.applyEffects(itemDef.use_effects);
        }

        if (itemDef.treats_injury) {
            const injuriesToTreat = Array.isArray(itemDef.treats_injury) ? itemDef.treats_injury : [itemDef.treats_injury];
            let treated = false;
            for (const injuryId of injuriesToTreat) {
                if (this.hasInjury(injuryId)) {
                    this.treatInjury(injuryId, itemId);
                    treated = true;
                    break;
                }
            }
            if (!treated && injuriesToTreat.length > 0) {
                result.text = `You use ${itemDef.icon} ${itemDef.name}, but you don't have any injuries it can treat. Still, it's comforting.`;
            } else {
                result.text = `You use ${itemDef.icon} ${itemDef.name}. ${itemDef.desc}`;
            }
        } else {
            result.text = `You use ${itemDef.icon} ${itemDef.name}. ${itemDef.desc}`;
        }

        this.state.hoursRemaining -= result.hours;
        this.checkAchievements();
        return result;
    }

    getUsableItems() {
        const items = [];
        const seen = new Set();
        for (const itemId of this.state.inventory) {
            if (seen.has(itemId)) continue;
            seen.add(itemId);
            const def = this.config.crafting?.[itemId];
            if (def && def.consumable) {
                items.push({ id: itemId, ...def });
            }
        }
        return items;
    }

    resolveLightFire(location, scenario) {
        const result = {
            actionId: 'light_fire',
            actionName: 'Light Fire',
            actionIcon: '🔥',
            hours: 1,
            text: '',
            effects: {},
            success: true
        };

        if (this.state.hasFire) {
            result.text = 'Your fire is already burning. The flames dance and crackle, pushing back the cold.';
            result.success = false;
            this.state.actionsUsed--;
            this.state.hoursRemaining += 1;
            return result;
        }

        if (!this.state.inventory.includes('wood')) {
            result.text = 'You need wood to build a fire. Gather some first.';
            result.success = false;
            this.state.actionsUsed--;
            this.state.hoursRemaining += 1;
            return result;
        }

        const woodIdx = this.state.inventory.indexOf('wood');
        if (woodIdx > -1) this.state.inventory.splice(woodIdx, 1);

        const hasFireBow = this.state.inventory.includes('fire_bow');
        let successChance = hasFireBow ? 1.0 : 0.7;

        if (this.state.weather) {
            if (this.state.weather.type === 'blizzard') successChance -= 0.4;
            else if (this.state.weather.type === 'freezing_rain') successChance -= 0.3;
            else if (this.state.weather.type === 'rain' || this.state.weather.type === 'snow') successChance -= 0.15;
        }
        successChance = Math.max(0.1, successChance);

        if (Math.random() < successChance) {
            this.state.hasFire = true;
            if (hasFireBow) {
                result.text = 'Your fire bow makes short work of the tinder. Flames crackle to life, casting warmth across your shelter. The fire is lit.';
            } else {
                result.text = 'You strike sparks onto the tinder. It catches. Flames crackle to life, casting warmth across your shelter. For a moment, the cold doesn\'t feel quite so absolute.';
            }
            result.effects = { warmth: 5, morale: 3 };
        } else {
            result.text = 'You strike spark after spark, but the tinder won\'t catch. The wood is too damp, or your hands are too cold, or the wind is too strong. You\'ve used the wood and you\'re still without fire.';
            result.effects = { morale: -3 };
        }

        return result;
    }

    resolveMeltWater(location, scenario) {
        const result = {
            actionId: 'melt_water',
            actionName: 'Melt Snow for Water',
            actionIcon: '🫗',
            hours: 1,
            text: '',
            effects: {},
            success: true
        };

        if (!this.state.hasFire) {
            result.text = 'You need a lit fire to melt snow for water. Light a fire first.';
            result.success = false;
            this.state.actionsUsed--;
            this.state.hoursRemaining += 1;
            return result;
        }

        if (this.state.resources.water === undefined || this.state.resources.water === null) {
            result.text = 'There\'s no container to hold water here.';
            result.success = false;
            this.state.actionsUsed--;
            this.state.hoursRemaining += 1;
            return result;
        }

        let waterGain = 15;
        if (location?.id === 'frozen_creek') waterGain = 20;
        if (this.state.season === 'Winter') waterGain += 5;

        result.text = `You melt snow over your fire, filling your container with fresh water. It\'s slow work, but the result is life itself. +${waterGain} water.`;
        result.effects = { water: waterGain, morale: 2 };
        return result;
    }

    resolveScavenge(location, scenario) {
        const result = {
            actionId: 'scavenge',
            actionName: 'Scavenge',
            actionIcon: '🔍',
            hours: 2,
            text: '',
            effects: {},
            discoveries: [],
            success: true,
            loot: []
        };

        const scavengeQuality = location?.scavenging_quality || 0.3;
        let successChance = scavengeQuality;

        if (this.hasCompanion('sam')) successChance += 0.2;
        if (this.hasCompanion('marcus')) successChance += 0.1;

        const roll = Math.random();

        if (roll < successChance) {
            const possibleFinds = {
                common: ['wood', 'cordage', 'bandage'],
                uncommon: ['knife_blade', 'wire', 'tin_can', 'medicinal_herbs'],
                rare: ['raw_meat', 'feathers']
            };

            const found = [];
            const commonItem = possibleFinds.common[Math.floor(Math.random() * possibleFinds.common.length)];
            found.push(commonItem);

            if (Math.random() < 0.4) {
                const uncommonItem = possibleFinds.uncommon[Math.floor(Math.random() * possibleFinds.uncommon.length)];
                found.push(uncommonItem);
            }
            if (Math.random() < 0.15) {
                const rareItem = possibleFinds.rare[Math.floor(Math.random() * possibleFinds.rare.length)];
                found.push(rareItem);
            }

            for (const item of found) {
                this.state.inventory.push(item);
            }

            const foundText = found.map(i => `${this.getItemIcon(i)} ${i.replace(/_/g, ' ')}`).join(', ');

            if (scavengeQuality >= 0.7) {
                result.text = `You search through the debris and find a cache of useful supplies! ${foundText}. This place hasn't been picked clean yet.`;
            } else if (scavengeQuality >= 0.4) {
                result.text = `You carefully search the building and find some useful items: ${foundText}. Not bad for a ruined city.`;
            } else {
                result.text = `You scrounge around but the pickings are slim. You still manage to find: ${foundText}.`;
            }

            result.effects.morale = 5;
            result.loot = found;

            // Building stability damage from scavenging
            if (location?.has_stability && this.state.buildingStability?.[location.id] !== undefined) {
                this.state.buildingStability[location.id] -= 5;
                if (this.state.buildingStability[location.id] <= 20) {
                    result.text += ' The building groans ominously as you search. It\'s not stable.';
                }
            }
        } else {
            if (location?.has_stability && this.state.buildingStability?.[location.id] !== undefined) {
                const stability = this.state.buildingStability[location.id];
                if (stability <= 30 && Math.random() < 0.3) {
                    result.text = 'You\'re searching through the building when a crack echoes through the structure. Debris falls around you! The building is collapsing!';
                    result.effects.health = -10;
                    result.effects.morale = -8;
                    this.state.buildingStability[location.id] -= 20;
                    if (Math.random() < 0.3) {
                        this.addInjury('cut');
                        result.text += ' Falling debris catches your arm. You need to get out!';
                    }
                } else {
                    result.text = 'You search carefully but find nothing useful. The building has been picked clean by other survivors — or the elements have destroyed what was left.';
                    result.effects.morale = -3;
                }
            } else {
                result.text = 'You search thoroughly but find nothing useful. Everything of value has already been taken or destroyed.';
                result.effects.morale = -2;
                result.effects.hunger = -2;
            }
            result.success = false;
        }

        return result;
    }

    // ==========================================
    // 8. FORAGING SYSTEM
    // ==========================================

    async startForaging() {
        this.renderForagingLoading();

        const scenario = this.getScenario();
        if (!scenario || !scenario.plants) {
            console.error('[FQ] No scenario or no plants!');
            this.showToast('No plants found in this area.', 'warning');
            this.state.actionsUsed--;
            this.state.hoursRemaining += 2;
            this.setState('choose_actions');
            return;
        }

        const currentLocation = this.state.currentLocation;
        const currentSeason = this.state.season;
        let availablePlants = scenario.plants.filter(plant => {
            const locationMatch = plant.locations?.includes(currentLocation);
            const seasonMatch = !plant.seasons || plant.seasons.includes(currentSeason);
            const seenToday = this.state.plantsSeen.some(p => p.name === plant.name && p.day === this.state.day);
            return locationMatch && seasonMatch && !seenToday;
        });

        // Fallback: if no plants at current location, pick from any location
        if (availablePlants.length === 0) {
            const fallbackPlants = scenario.plants.filter(plant => {
                const seenToday = this.state.plantsSeen.some(p => p.name === plant.name && p.day === this.state.day);
                return !seenToday;
            });
            if (fallbackPlants.length > 0) {
                availablePlants = [fallbackPlants[Math.floor(Math.random() * fallbackPlants.length)]];
            }
        }

        if (availablePlants.length === 0) {
            this.showToast('Could not find a new plant. Try a different area.', 'warning');
            this.state.actionsUsed--;
            this.state.hoursRemaining += 2;
            this.setState('choose_actions');
            return;
        }

        // ── Wild Forest: Karma-based plant bias ──
        let plantPool = availablePlants;
        if (this.state.scenarioId === 'wild_forest' && availablePlants.length > 1) {
            const karma = this.state.forestKarma || 50;
            if (karma > 65) {
                const edible = availablePlants.filter(p => p.is_edible);
                if (edible.length > 0 && Math.random() < 0.35) {
                    plantPool = [...availablePlants, ...edible];
                }
            } else if (karma < 35) {
                const dangerous = availablePlants.filter(p => !p.is_edible);
                if (dangerous.length > 0 && Math.random() < 0.35) {
                    plantPool = [...availablePlants, ...dangerous];
                }
            }
        }

        const chosenPlant = plantPool[Math.floor(Math.random() * plantPool.length)];

        const encounterTexts = [
            `You search the area and spot something growing.`,
            `Among the rocks and sand, you find a plant.`,
            `Your eyes catch a glimpse of green. You move closer to investigate.`
        ];

        this.encounterData = {
            encounter_text: encounterTexts[Math.floor(Math.random() * encounterTexts.length)],
            plant: chosenPlant,
            question: "Is this plant safe to forage/consume?",
            options: [
                { name: "Safe to consume", icon: "✅" },
                { name: "Dangerous, avoid it", icon: "🚫" }
            ],
            correct_answer: chosenPlant.is_edible ? "Safe to consume" : "Dangerous, avoid it"
        };

        // Chance to find extra medicinal herbs while foraging
        if (Math.random() < 0.15 && !this.state.inventory.includes('medicinal_herbs')) {
            this.state.inventory.push('medicinal_herbs');
            this.addJournalEntry('🌿 You spotted some useful medicinal herbs while foraging.');
        }

        // ── Wild Forest: Mythic bonus drops ──
        if (this.state.scenarioId === 'wild_forest') {
            const currentLoc = this.getLocation();
            if (currentLoc) {
                if (currentLoc.id === 'mushroom_grove' && Math.random() < 0.3) {
                    if (!this.state.inventory.includes('glowing_fungi')) {
                        this.state.inventory.push('glowing_fungi');
                        this.addJournalEntry('✨ In the shadows, you spot an eerie blue glow... you found Glowing Fungi!');
                    }
                }
                if (currentLoc.id === 'berry_patch' && Math.random() < 0.4) {
                    if (!this.state.inventory.includes('berries')) {
                        this.state.inventory.push('berries');
                        this.addJournalEntry('🌿 You gather a handful of wild berries, perfect for an offering.');
                    }
                }
            }
        }

        this.setState('foraging');
    }

    handleForagingAnswer(answer) {
        const data = this.encounterData;
        if (!data) return;

        const plant = data.plant;
        const correctAnswer = data.correct_answer;
        const isCorrect = answer === correctAnswer;

        const consequences = {};
        const quality = this.getLocation()?.foraging_quality || 0.5;

        let resultText = '';

        if (isCorrect) {
            this.state.plantsCorrect = (this.state.plantsCorrect || 0) + 1;

            let foragingQualityBonus = 0;
            if (this.state.scenarioId === 'overgrown_city' && this.hasCompanion('dr_amara')) {
                foragingQualityBonus = 0.25;
            }

            if (plant.safe_yield) {
                for (const [key, value] of Object.entries(plant.safe_yield)) {
                    consequences[key] = Math.round(value * (quality + foragingQualityBonus));
                }
            }

            resultText = plant.desc_safe;

            if (plant.loot && plant.loot.length > 0) {
                for (const item of plant.loot) {
                    if (!this.state.inventory.includes(item)) {
                        this.state.inventory.push(item);
                        resultText += ` You gathered: ${item.replace(/_/g, ' ')}.`;
                    } else {
                        resultText += ` You found more ${item.replace(/_/g, ' ')}, but you already have some.`;
                    }
                }
            }

            this.addJournalEntry(`✅ Correctly identified ${plant.icon} ${plant.name}.`);
        } else {
            this.state.plantsWrong = (this.state.plantsWrong || 0) + 1;

            if (plant.unsafe_yield) {
                Object.assign(consequences, plant.unsafe_yield);
            }

            resultText = plant.unsafe_text;

            if (plant.unsafe_injury) {
                this.addInjury(plant.unsafe_injury);
            } else if (consequences.health && consequences.health < -10) {
                this.playAnimation('shake', 500);
            }

            this.addJournalEntry(`❌ Misidentified ${plant.icon} ${plant.name} (guessed: ${answer}).`);
        }

        this.applyEffects(consequences);

        this.state.plantsSeen.push({
            name: plant.name,
            correct: isCorrect,
            day: this.state.day
        });

        this.foragingResult = {
            correct: isCorrect,
            answer: answer,
            correctAnswer: correctAnswer,
            plant: plant,
            consequences: consequences,
            resultText: resultText,
            dangerLevel: plant.is_edible ? 'SAFE' : 'POISONOUS'
        };

        this.checkAchievements();
        this.renderForagingResult();
    }

    afterForagingResult() {
        const check = this.checkCriticalResources();
        if (check.dead) return;

        if (check.warnings.length > 0) {
            this.showToast(check.warnings[0], 'danger');
        }

        if (this.state.actionsUsed >= this.state.maxActions || this.state.hoursRemaining <= 0) {
            this.rollForEvent();
        } else {
            this.setState('choose_actions');
        }
    }

    getAvailableActions() {
        const scenario = this.getScenario();
        const loc = this.getLocation();
        const actions = ['forage', 'explore', 'rest', 'build_shelter', 'gather_wood'];

        if (this.state.day >= 2) actions.push('signal');
        actions.push('hunt');
        actions.push('light_fire');

        if (this.state.scenarioId === 'alaska_winter') {
            actions.push('melt_water');
            actions.push('find_water');
        } else if (this.state.scenarioId === 'desert') {
            actions.push('find_water');
        } else if (this.state.scenarioId === 'wild_forest') {
            actions.push('find_water');
        } else if (this.state.scenarioId === 'overgrown_city') {
            actions.push('find_water');
            actions.push('scavenge');
        } else if (this.state.scenarioId === 'tropical_island') {
            actions.push('find_water');
        } else if (!loc?.water_source) {
            actions.push('find_water');
        }

        if (this.state.inventory.length > 0) actions.push('craft');

        return actions;
    }

    getKarmaForagingModifier() {
        if (this.state.scenarioId !== 'wild_forest') return 0;
        const karma = this.state.forestKarma || 50;
        if (karma > 80) return 0.2;
        if (karma > 60) return 0.1;
        if (karma < 25) return -0.15;
        if (karma < 40) return -0.05;
        return 0;
    }

        // ==========================================
    // 9. EVENT SYSTEM
    // ==========================================

    rollForEvent() {
        const scenario = this.getScenario();
        const events = scenario.events || [];

        // ── MISSED OPPORTUNITY EVENTS ──
        const missedOpp = this.scenarioData?.missed_opportunity;
        if (missedOpp && this.state.day >= (missedOpp.days_without_signal || 5) + 3) {
            const daysSince = this.state.day - (this.state.lastSignalDay || 1);
            if (daysSince >= missedOpp.days_without_signal && this.state.signalProgress < 7) {
                const moEvent = events.find(e => e.id === missedOpp.event_id);
                if (moEvent && !this.state.eventsCompleted.includes(moEvent.id)) {
                    this.playAnimation('plane');
                    this.currentEvent = moEvent;
                    this.addJournalEntry('🚁 You hear something in the distance...');
                    this.setState('event');
                    return;
                }
            }
        }

        // ── ALASKA: STORM EVENT ──
        if (this.state.scenarioId === 'alaska_winter' && this.state.stormWarning > 0) {
            this.state.stormWarning--;
            if (this.state.stormWarning <= 0) {
                const stormEvent = {
                    id: "great_storm",
                    name: "❄️ The Great Storm",
                    icon: "❄️",
                    text: "The storm you sensed has arrived. A wall of white engulfs you. The wind screams like something alive. This is not a normal blizzard — this is the kind of storm that buries people forever. You have minutes to decide what to do.",
                    min_day: 1,
                    choices: [
                        {
                            icon: "🏕️", text: "Hunker down in your shelter and wait it out",
                            success: 0.7, hours: 4,
                            success_text: "You ride out the storm in your shelter. It rages for hours, but your walls hold. When it passes, the world is transformed — buried in white, but you're alive.",
                            success_fx: { "warmth": -10, "morale": 5 },
                            fail_text: "Your shelter groans under the assault. Snow forces its way through every gap. You spend the worst night of your life, shivering and afraid.",
                            fail_fx: { "warmth": -25, "health": -15, "morale": -10 }
                        },
                        {
                            icon: "🪵", text: "Build up your fire and fortify",
                            requires: ["wood"], success: 0.8, hours: 3,
                            success_text: "You feed the fire everything you have. The flames push back the cold. The storm rages, but you have warmth. When dawn comes, you're still here.",
                            success_fx: { "warmth": 5, "morale": 10 },
                            fail_text: "The wind steals your firewood. The cold closes in. It's a terrible night.",
                            fail_fx: { "warmth": -15, "health": -10, "morale": -5 }
                        },
                        {
                            icon: "🏃", text: "Try to find better ground",
                            success: 0.3, hours: 2,
                            success_text: "Through sheer luck, you stumble upon a rock overhang. Not perfect, but better than open ground. You survive the night pressed against cold stone.",
                            success_fx: { "warmth": -5, "morale": 3, "explore_progress": 2 },
                            fail_text: "You're completely lost in the whiteout. The cold is killing you. By the time you find any cover, you're half-frozen.",
                            fail_fx: { "warmth": -30, "health": -25, "morale": -15 }
                        }
                    ]
                };
                this.currentEvent = stormEvent;
                this.playAnimation('storm_flash', 1500);
                this.addJournalEntry('❄️ The Great Storm arrives!');
                this.setState('event');
                return;
            } else {
                this.addJournalEntry(`⚠️ The wind is getting worse. The storm arrives in ${this.state.stormWarning} day${this.state.stormWarning > 1 ? 's' : ''}.`);
                this.showToast(`⚠️ Storm in ${this.state.stormWarning} day${this.state.stormWarning > 1 ? 's' : ''}`, 'warning');
            }
        }

        // ── ALASKA: WOLF PROGRESSION SYSTEM ──
        if (this.state.scenarioId === 'alaska_winter') {
            const shelterLevel = this.state.shelterLevel;
            const wolfPhase = this.state.wolfPhase || 0;
            const daysSince = this.state.wolfDaysSinceEvent || 0;
            const encounterCount = this.state.wolfEncounterCount || 0;

            let wolfEventChance = 0.35;
            if (shelterLevel >= 2) wolfEventChance -= 0.1;
            if (shelterLevel >= 3) wolfEventChance -= 0.15;

            // Force wolf tracks event
            if (wolfPhase === 1 && daysSince >= 1 && !this.state.eventsCompleted.includes('wolf_tracks')) {
                const wolfTracksEvent = events.find(e => e.id === 'wolf_tracks');
                if (wolfTracksEvent) {
                    this.currentEvent = wolfTracksEvent;
                    this.setState('event');
                    return;
                }
            }

            // Force wolf howl event
            if (wolfPhase === 2 && daysSince >= 1 && !this.state.eventsCompleted.includes('wolf_howl')) {
                const wolfHowlEvent = events.find(e => e.id === 'wolf_howl');
                if (wolfHowlEvent) {
                    this.currentEvent = wolfHowlEvent;
                    this.setState('event');
                    return;
                }
            }

            // Wolf stalking encounters
            if (this.state.wolfStalking && Math.random() < wolfEventChance) {
                const isBear = encounterCount >= 3 && Math.random() < 0.3;

                if (isBear) {
                    const bearEvent = {
                        id: "bear_at_camp", name: "🐻 Bear at Camp", icon: "🐻",
                        text: "You wake to heavy footsteps and a deep, guttural huffing. A grizzly bear is investigating your camp. It's massive — easily 300 kilograms of muscle and claw. It hasn't seen you yet, but the wind could shift at any moment.",
                        min_day: 1,
                        choices: [
                            { icon: "🏃", text: "Back away slowly and quietly", success: 0.6, hours: 1, success_text: "You inch backwards without making a sound. The bear sniffs the air, investigates your fire pit, and eventually wanders off.", success_fx: { "morale": -5 }, fail_text: "You step on a dry branch. The bear whips around and bluff-charges. You scramble backwards, tripping over your own shelter.", fail_fx: { "health": -15, "morale": -15 }, fail_injury: "cut" },
                            { icon: "💪", text: "Make yourself big and make noise", success: 0.5, hours: 1, success_text: "You stand tall, wave your arms, and shout. The bear pauses, snorts, and decides you're more trouble than you're worth.", success_fx: { "morale": 3 }, fail_text: "You shout and wave, but the bear isn't intimidated. It stands up on its hind legs. You freeze. After what feels like an eternity, it drops back down and leaves.", fail_fx: { "morale": -20, "warmth": -5 } },
                            { icon: "🔥", text: "Try to scare it with fire", requires: ["wood"], success: 0.65, hours: 1, success_text: "You grab burning wood from your fire and wave it at the bear. The flames and smoke convince it to leave.", success_fx: { "morale": 5, "warmth": 2 }, fail_text: "You grab burning wood but the bear charges. You throw it and the bear flinches, then rethinks and retreats. Close.", fail_fx: { "morale": -10 } }
                        ]
                    };
                    this.currentEvent = bearEvent;
                    this.addJournalEntry('🐻 A grizzly bear investigated your camp!');
                } else {
                    // Wolf stalking encounter — escalates
                    const encounterTexts = [
                        { text: "The wolf is back. You see it at the edge of your camp, watching. It's been tracking you for days now. This is no longer a chance encounter — it has decided you are prey.", success_text_fire: "You feed the fire high and loud. The wolf circles but won't approach the flames. By morning it's gone — for now.", success_text_spear: "You charge at the wolf with your spear raised and screaming. It flinches, then bolts. You've won this round — but it may come back.", fail_text: "The wolf tests your perimeter all night. You don't sleep. By morning it's gone, but you're exhausted." },
                        { text: "The wolf returns with another. Two sets of eyes reflect your firelight. They're learning your patterns. They know when you sleep. They know when you're weak.", success_text_fire: "You keep the fire blazing until dawn. The wolves circle but won't cross the flames.", success_text_spear: "You stand your ground, spear raised, and they decide you're not worth the risk. Not tonight.", fail_text: "The wolves probe your defences all night. At one point, the larger one comes within arm's reach before you drive it back." },
                        { text: "A wolf pack surrounds your camp. You can see at least three sets of eyes in the darkness. They've been watching you for days. They know your routine. Tonight, they're testing whether you're still dangerous.", success_text_fire: "You build your fire into a wall of flame. The wolves retreat to the tree line. They'll be back, but tonight you're still the apex predator.", success_text_spear: "You fight back with everything you have. The wolves back off — they're smart enough to know that injured prey isn't worth the cost.", fail_text: "The wolves press closer than ever before. One snaps at your leg. You drive it back, but you're bleeding and exhausted." }
                    ];

                    const encounterIndex = Math.min(encounterCount, encounterTexts.length - 1);
                    const encounter = encounterTexts[encounterIndex];

                    const wolfEvent = {
                        id: "wolf_stalking",
                        name: encounterCount >= 2 ? "🐺 Wolf Pack Returns" : "🐺 The Wolf Returns",
                        icon: "🐺", text: encounter.text, min_day: 1,
                        choices: [
                            { icon: "🔥", text: "Keep the fire blazing all night", requires: ["wood"], success: 0.7, hours: 3, success_text: encounter.success_text_fire, success_fx: { "morale": -3, "warmth": 3 }, fail_text: encounter.fail_text, fail_fx: { "morale": -10, "warmth": -2 } },
                            { icon: "🗡️", text: "Stand your ground and confront it", requires: ["spear"], success: 0.5, hours: 2, success_text: encounter.success_text_spear, success_fx: { "morale": 10 }, fail_text: "The wolf doesn't back down. It lunges. You fight it off but take a slash across your arm.", fail_fx: { "health": -20, "morale": -15 }, fail_injury: "cut" },
                            { icon: "🏃", text: "Move camp immediately", success: 0.4, hours: 2, success_text: "You pack up and move. The wolves follow at a distance but eventually lose interest.", success_fx: { "morale": -5, "warmth": -5 } }
                        ]
                    };

                    if ((this.state.wildRespect || 50) >= 70) {
                        wolfEvent.choices.push({
                            icon: "🌿", text: "Make eye contact and stand still — show no fear, no aggression",
                            success: 0.6, hours: 1,
                            success_text: "You lock eyes with the wolf. You don't blink. Something passes between you — recognition. The wolf turns and walks away. In the morning, you find a deer carcass near camp.",
                            success_fx: { "morale": 10, "hunger": 15, "wildRespect": 5 }, success_loot: ["raw_meat"],
                            fail_text: "You try to hold the wolf's gaze, but it senses your uncertainty. It circles closer.",
                            fail_fx: { "morale": -8 }
                        });
                    }

                    this.currentEvent = wolfEvent;
                }

                this.state.wolfEncounterCount = encounterCount + 1;
                this.state.wolfDaysSinceEvent = 0;
                this.setState('event');
                return;
            }

            // Non-stalking wolf encounters (phase 3: first encounter)
            if (wolfPhase >= 2 && !this.state.wolfStalking && daysSince >= 2 && Math.random() < 0.25) {
                const isBear = this.state.day >= 6 && Math.random() < 0.25;
                if (isBear) {
                    const bearEvent = events.find(e => e.id === 'bear_encounter');
                    if (bearEvent) { this.currentEvent = bearEvent; this.setState('event'); return; }
                } else {
                    const wolfEvent = events.find(e => e.id === 'wolf_pack') || events.find(e => e.id === 'wolf_howl');
                    if (wolfEvent) {
                        this.currentEvent = wolfEvent;
                        this.state.wolfPhase = 3;
                        this.state.wolfDaysSinceEvent = 0;
                        this.setState('event');
                        return;
                    }
                }
            }
        }

        // ── DESERT: VULTURE PROGRESSION ──
        if (this.state.scenarioId === 'desert' && this.state.vulturePhase >= 2 && this.state.vultureDaysSinceEvent >= 2) {
            const vultureChance = this.state.vulturePhase >= 4 ? 0.6 : this.state.vulturePhase >= 3 ? 0.4 : 0.2;

            if (this.state.vulturePhase >= 4) {
                const vultureLandEvent = {
                    id: "vultures_landed", name: "🦅 Vultures on the Ground", icon: "🦅",
                    text: "The vultures have landed. Three of them sit on the rocks nearby, watching you with flat, black eyes. They're not circling anymore. They're waiting. Prove them wrong.",
                    min_day: 1,
                    choices: [
                        { icon: "🏃", text: "Stand up and shout at them", success: 0.7, hours: 0, success_text: "You force yourself to your feet and yell. The vultures flap away awkwardly, startled.", success_fx: { "morale": 5, "water": -2 } },
                        { icon: "💪", text: "Ignore them — save your energy", success: 0.5, hours: 0, success_text: "You stare back at them. They watch. You watch. Eventually they shuffle to a further rock.", success_fx: { "morale": -3 } },
                        { icon: "💧", text: "Drink what water you have — prove you're alive", success: 0.6, hours: 0, success_text: "You take a long, deliberate drink. The vultures tilt their heads. You're not dying. Not today.", success_fx: { "morale": 8 }, fail_text: "You reach for your water... and there's almost nothing left. The vultures don't move.", fail_fx: { "morale": -10 } }
                    ]
                };
                this.currentEvent = vultureLandEvent;
                this.state.vultureDaysSinceEvent = 0;
                this.setState('event');
                return;
            }

            if (this.state.vulturePhase >= 3) {
                const vultureLowEvent = events.find(e => e.id === 'vultures_circling_low');
                if (vultureLowEvent) { this.currentEvent = vultureLowEvent; this.state.vultureDaysSinceEvent = 0; this.setState('event'); return; }
            }

            if (Math.random() < vultureChance) {
                const vultureEvent = events.find(e => e.id === 'vultures_circling');
                if (vultureEvent) { this.currentEvent = vultureEvent; this.state.vultureDaysSinceEvent = 0; this.setState('event'); return; }
            }
        }

        // ── DESERT: DRIVER STORY ARC ──
        if (this.state.scenarioId === 'desert') {
            const driverPhase = this.state.driverPhase || 0;
            const driverEvents = ['ray_jacket', 'ray_trail', 'ray_camp', 'ray_body'];

            if (driverPhase < 4) {
                const nextEventId = driverEvents[driverPhase];
                const nextEvent = events.find(e => e.id === nextEventId);

                if (nextEvent && !this.state.eventsCompleted.includes(nextEventId)) {
                    const dayRequirements = [2, 4, 7, 11];
                    if (this.state.day >= dayRequirements[driverPhase]) {
                        const chance = driverPhase === 0 ? 0.6 : 0.4;
                        if (Math.random() < chance || this.state.day >= dayRequirements[driverPhase] + 3) {
                            this.currentEvent = nextEvent;
                            this.setState('event');
                            return;
                        }
                    }
                }
            }
        }

        // ── DESERT: MINE PSYCHOLOGICAL TRAP ──
        if (this.state.scenarioId === 'desert' && this.state.currentLocation === 'abandoned_mine') {
            const mineDays = this.state.mineDaysConsecutive || 0;
            const mineChance = Math.min(0.3 + (mineDays * 0.1), 0.8);

            if (mineDays >= 3 && !this.state.eventsCompleted.includes('mine_sounds') && Math.random() < mineChance) {
                const mineEvent = events.find(e => e.id === 'mine_sounds');
                if (mineEvent) { this.currentEvent = mineEvent; this.setState('event'); return; }
            }
            if (mineDays >= 5 && !this.state.eventsCompleted.includes('mine_darkness') && Math.random() < mineChance) {
                const mineEvent = events.find(e => e.id === 'mine_darkness');
                if (mineEvent) { this.currentEvent = mineEvent; this.setState('event'); return; }
            }
            if (mineDays >= 8 && !this.state.eventsCompleted.includes('mine_resident') && Math.random() < mineChance) {
                const mineEvent = events.find(e => e.id === 'mine_resident');
                if (mineEvent) { this.currentEvent = mineEvent; this.setState('event'); return; }
            }
            if (mineDays >= 10) {
                const mineEnding = scenario.endings?.find(e => e.id === 'the_mine');
                if (mineEnding) { this.triggerEnding(mineEnding); return; }
            }
        }

        // ── ALASKA: CABIN FEVER SYSTEM ──
        if (this.state.scenarioId === 'alaska_winter' && this.state.currentLocation === 'abandoned_cabin') {
            const cabinDays = this.state.cabinDaysConsecutive || 0;
            const cabinEventChance = Math.min(0.3 + (cabinDays * 0.1), 0.9);

            if (cabinDays >= 3 && !this.state.eventsCompleted.includes('cabin_night_sounds') && Math.random() < cabinEventChance) {
                const cabinEvent = events.find(e => e.id === 'cabin_night_sounds');
                if (cabinEvent) { this.currentEvent = cabinEvent; this.setState('event'); return; }
            }
            if (cabinDays >= 5 && !this.state.eventsCompleted.includes('cabin_fever') && Math.random() < cabinEventChance) {
                const cabinEvent = events.find(e => e.id === 'cabin_fever');
                if (cabinEvent) { this.currentEvent = cabinEvent; this.setState('event'); return; }
            }
            if (cabinDays >= 7 && !this.state.eventsCompleted.includes('cabin_scratches') && Math.random() < cabinEventChance) {
                const cabinEvent = events.find(e => e.id === 'cabin_scratches');
                if (cabinEvent) { this.currentEvent = cabinEvent; this.setState('event'); return; }
            }
            if (cabinDays >= 8 && !this.state.eventsCompleted.includes('cabin_resident') && Math.random() < cabinEventChance) {
                const cabinEvent = events.find(e => e.id === 'cabin_resident');
                if (cabinEvent) { this.currentEvent = cabinEvent; this.setState('event'); return; }
            }
            if (cabinDays >= 10) {
                const cabinEnding = scenario.endings?.find(e => e.id === 'the_cabin');
                if (cabinEnding) { this.triggerEnding(cabinEnding); return; }
            }
        }

        // ── OVERGROWN CITY: COMPANION DISCOVERY EVENTS ──
        if (this.state.scenarioId === 'overgrown_city') {
            const companionDefs = this.getCompanionDefs();

            for (const [compId, def] of Object.entries(companionDefs)) {
                if (this.state.companions.some(c => c.id === compId)) continue;
                if (this.state.day < def.discoverMinDay) continue;

                const event = events.find(e => e.id === `${compId}_discovery`);
                if (!event || this.state.eventsCompleted.includes(event.id)) continue;

                const chance = 0.4;
                const maxDay = def.discoverMaxDay || 999;
                if (Math.random() < chance || this.state.day >= maxDay) {
                    this.currentEvent = event;
                    this.setState('event');
                    return;
                }
            }

            // ── Pack events ──
            const packPhase = this.state.packPhase || 0;
            const packDaysSince = this.state.packDaysSinceEvent || 0;
            const activeCompanions = this.getActiveCompanions().length;

            if (packPhase >= 1 && packDaysSince >= 2) {
                let packEventId = null;
                if (packPhase >= 1 && !this.state.eventsCompleted.includes('pack_howls') && Math.random() < 0.4) packEventId = 'pack_howls';
                if (packPhase >= 2 && !this.state.eventsCompleted.includes('pack_kills') && Math.random() < 0.35) packEventId = 'pack_kills';
                if (packPhase >= 3 && !this.state.eventsCompleted.includes('pack_surround') && Math.random() < 0.3) packEventId = 'pack_surround';
                if (packPhase >= 4 && Math.random() < (0.3 - (activeCompanions * 0.05))) packEventId = 'pack_attack';

                if (packEventId) {
                    const packEvent = events.find(e => e.id === packEventId);
                    if (packEvent) { this.currentEvent = packEvent; this.state.packDaysSinceEvent = 0; this.setState('event'); return; }
                }
            }

            // ── Dr. Amara arc ──
            const amaraPhase = this.state.amaraPhase || 0;
            const amaraEvents = ['amara_greenhouse', 'amara_lab', 'amara_camp', 'amara_herself'];
            const amaraDayReqs = [2, 5, 8, 11];

            if (amaraPhase < 4) {
                const nextEventId = amaraEvents[amaraPhase];
                const nextEvent = events.find(e => e.id === nextEventId);
                if (nextEvent && !this.state.eventsCompleted.includes(nextEventId) && this.state.day >= amaraDayReqs[amaraPhase]) {
                    const chance = amaraPhase === 0 ? 0.5 : 0.4;
                    if (Math.random() < chance || this.state.day >= amaraDayReqs[amaraPhase] + 3) {
                        this.currentEvent = nextEvent;
                        this.setState('event');
                        return;
                    }
                }
            }

            // ── Supermarket trap ──
            if (this.state.currentLocation === 'abandoned_supermarket' && this.state.supermarketDaysConsecutive >= 3) {
                const marketDays = this.state.supermarketDaysConsecutive;
                const marketChance = Math.min(0.3 + (marketDays * 0.1), 0.8);

                if (marketDays >= 3 && !this.state.eventsCompleted.includes('supermarket_allure') && Math.random() < marketChance) {
                    const marketEvent = events.find(e => e.id === 'supermarket_allure');
                    if (marketEvent) { this.currentEvent = marketEvent; this.setState('event'); return; }
                }
                if (marketDays >= 5 && !this.state.eventsCompleted.includes('supermarket_comfort') && Math.random() < marketChance) {
                    const marketEvent = events.find(e => e.id === 'supermarket_comfort');
                    if (marketEvent) { this.currentEvent = marketEvent; this.setState('event'); return; }
                }
                if (marketDays >= 7 && !this.state.eventsCompleted.includes('supermarket_forgotten') && Math.random() < marketChance) {
                    const marketEvent = events.find(e => e.id === 'supermarket_forgotten');
                    if (marketEvent) { this.currentEvent = marketEvent; this.setState('event'); return; }
                }
                if (this.state.supermarketDaysConsecutive >= 10) {
                    const marketEnding = scenario.endings?.find(e => e.id === 'the_supermarket');
                    if (marketEnding) { this.triggerEnding(marketEnding); return; }
                }
            }

            // ── Companion events ──
            if (this.hasCompanion('lily') && this.state.day >= 3 && !this.state.eventsCompleted.includes('lily_drawing') && Math.random() < 0.3) {
                const lilyEvent = events.find(e => e.id === 'lily_drawing');
                if (lilyEvent) { this.currentEvent = lilyEvent; this.setState('event'); return; }
            }
            if (this.hasCompanion('sam') && this.state.resources.morale < 30 && this.state.day >= 7 && !this.state.eventsCompleted.includes('sam_wants_to_leave') && Math.random() < 0.3) {
                const samEvent = events.find(e => e.id === 'sam_wants_to_leave');
                if (samEvent) { this.currentEvent = samEvent; this.setState('event'); return; }
            }
            const marcus = this.state.companions.find(c => c.id === 'marcus' && c.status === 'active');
            if (marcus && marcus.trust < 30 && this.state.day >= 8 && !this.state.eventsCompleted.includes('marcus_stealing') && Math.random() < 0.3) {
                const marcusEvent = events.find(e => e.id === 'marcus_stealing');
                if (marcusEvent) { this.currentEvent = marcusEvent; this.setState('event'); return; }
            }
            if (this.getActiveCompanions().length >= 1 && this.state.day >= 5 && !this.state.eventsCompleted.includes('community_meal') && Math.random() < 0.15) {
                const mealEvent = events.find(e => e.id === 'community_meal');
                if (mealEvent) { this.currentEvent = mealEvent; this.setState('event'); return; }
            }

            // ── Building collapse ──
            const currentLoc = this.getLocation();
            if (currentLoc && currentLoc.has_stability && this.state.buildingStability[currentLoc.id] !== undefined) {
                const stability = this.state.buildingStability[currentLoc.id];
                if (stability <= 30 && !this.state.eventsCompleted.includes('building_collapse') && Math.random() < 0.25) {
                    const collapseEvent = events.find(e => e.id === 'building_collapse');
                    if (collapseEvent) { this.currentEvent = collapseEvent; this.setState('event'); return; }
                }
            }

            // ── Mythic events ──
            if (!this.state.mythicEventsCompleted?.includes('city_remembers') && this.state.day >= 8 && Math.random() < 0.1) {
                const mythicEvent = events.find(e => e.id === 'city_remembers');
                if (mythicEvent && !this.state.eventsCompleted.includes('city_remembers')) {
                    this.currentEvent = mythicEvent;
                    this.setState('event');
                    return;
                }
            }
            if (!this.state.mythicEventsCompleted?.includes('nature_reclaims') && this.state.day >= 12 && this.state.resources.morale >= 40 && Math.random() < 0.08) {
                const mythicEvent = events.find(e => e.id === 'nature_reclaims');
                if (mythicEvent && !this.state.eventsCompleted.includes('nature_reclaims')) {
                    this.currentEvent = mythicEvent;
                    this.setState('event');
                    return;
                }
            }
        }

        // ── DESERT: HALLUCINATION EVENTS ──
        if (this.state.scenarioId === 'desert' && this.state.hallucinationCount > 0 && Math.random() < 0.3) {
            const halluEvent = this.getHallucinationEvent();
            if (halluEvent) { this.currentEvent = halluEvent; this.setState('event'); return; }
        }

        // ── WILD FOREST: WATCHER EVENT SYSTEM ──
        if (this.state.scenarioId === 'wild_forest') {
            const watcherPhase = this.state.watcherPhase || 0;
            const karma = this.state.forestKarma || 50;
            const daysSince = this.state.watcherDaysSinceEvent || 0;

            if (watcherPhase >= 1 && daysSince >= 2) {
                let watcherEvent = null;

                if (karma < 30 && watcherPhase >= 2) {
                    const watcherEvents = ['thorny_path', 'wrong_berries', 'eyes_in_dark_event'];
                    const available = watcherEvents.filter(e => !this.state.eventsCompleted.includes(e));
                    if (available.length > 0 && Math.random() < 0.3) {
                        watcherEvent = events.find(e => e.id === available[Math.floor(Math.random() * available.length)]);
                    }
                }

                if (!watcherEvent && karma > 60 && watcherPhase >= 2) {
                    const helpfulEvents = ['helpful_deer', 'glowing_path', 'friendly_fox'];
                    const available = helpfulEvents.filter(e => !this.state.eventsCompleted.includes(e));
                    if (available.length > 0 && Math.random() < 0.25) {
                        watcherEvent = events.find(e => e.id === available[Math.floor(Math.random() * available.length)]);
                    }
                }

                if (!watcherEvent && watcherPhase === 1 && !this.state.eventsCompleted.includes('watcher_sensing') && daysSince >= 1) {
                    watcherEvent = events.find(e => e.id === 'watcher_sensing');
                }
                if (!watcherEvent && watcherPhase === 2 && !this.state.eventsCompleted.includes('watcher_watching') && daysSince >= 1) {
                    watcherEvent = events.find(e => e.id === 'watcher_watching');
                }
                if (!watcherEvent && watcherPhase === 3 && !this.state.eventsCompleted.includes('watcher_testing') && daysSince >= 1) {
                    watcherEvent = events.find(e => e.id === 'watcher_testing');
                }

                if (watcherEvent) {
                    this.state.watcherDaysSinceEvent = 0;
                    this.currentEvent = watcherEvent;
                    this.setState('event');
                    return;
                }
            }

            // ── Hiker arc ──
            const hikerPhase = this.state.hikerPhase || 0;
            const hikerEvents = ['hikers_backpack', 'hikers_trail_marks', 'hikers_shelter', 'hikers_note'];

            if (hikerPhase < 4) {
                const nextEventId = hikerEvents[hikerPhase];
                const nextEvent = events.find(e => e.id === nextEventId);

                if (nextEvent && !this.state.eventsCompleted.includes(nextEventId)) {
                    const dayRequirements = [2, 5, 8, 11];
                    if (this.state.day >= dayRequirements[hikerPhase]) {
                        const chance = hikerPhase === 0 ? 0.5 : 0.4;
                        if (Math.random() < chance || this.state.day >= dayRequirements[hikerPhase] + 3) {
                            this.currentEvent = nextEvent;
                            this.setState('event');
                            return;
                        }
                    }
                }
            }

            // ── Grove trap ──
            if (this.state.currentLocation === 'mushroom_grove') {
                const groveDays = this.state.groveDaysConsecutive || 0;
                const groveChance = Math.min(0.3 + (groveDays * 0.1), 0.8);

                if (groveDays >= 3 && !this.state.eventsCompleted.includes('grove_allure') && Math.random() < groveChance) {
                    const groveEvent = events.find(e => e.id === 'grove_allure');
                    if (groveEvent) { this.currentEvent = groveEvent; this.setState('event'); return; }
                }
                if (groveDays >= 5 && !this.state.eventsCompleted.includes('grove_deeper') && Math.random() < groveChance) {
                    const groveEvent = events.find(e => e.id === 'grove_deeper');
                    if (groveEvent) { this.currentEvent = groveEvent; this.setState('event'); return; }
                }
                if (groveDays >= 8 && !this.state.eventsCompleted.includes('grove_voices') && Math.random() < groveChance) {
                    const groveEvent = events.find(e => e.id === 'grove_voices');
                    if (groveEvent) { this.currentEvent = groveEvent; this.setState('event'); return; }
                }
                if (groveDays >= 10) {
                    const groveEnding = scenario.endings?.find(e => e.id === 'the_grove');
                    if (groveEnding) { this.triggerEnding(groveEnding); return; }
                }
            }
        }

        // ── TROPICAL ISLAND: SHARK, KIRI, WRECK, RESPECT (single consolidated block) ──
        if (this.state.scenarioId === 'tropical_island') {
            const sharkPhase = this.state.sharkPhase || 0;
            const sharkDaysSince = this.state.sharkDaysSinceEvent || 0;

            // Shark phase events
            if (sharkPhase >= 1 && !this.state.eventsCompleted.includes('shark_fin_spotted')) {
                const sharkEvent = events.find(e => e.id === 'shark_fin_spotted');
                if (sharkEvent) { this.currentEvent = sharkEvent; this.state.sharkDaysSinceEvent = 0; this.setState('event'); return; }
            }
            if (sharkPhase >= 2 && !this.state.eventsCompleted.includes('shark_circling')) {
                const sharkEvent = events.find(e => e.id === 'shark_circling');
                if (sharkEvent) { this.currentEvent = sharkEvent; this.state.sharkDaysSinceEvent = 0; this.setState('event'); return; }
            }
            if (sharkPhase >= 3 && !this.state.eventsCompleted.includes('shark_bump')) {
                const sharkEvent = events.find(e => e.id === 'shark_bump');
                if (sharkEvent) { this.currentEvent = sharkEvent; this.state.sharkDaysSinceEvent = 0; this.setState('event'); return; }
            }
            if (sharkPhase >= 4 && !this.state.eventsCompleted.includes('shark_aggressive') && Math.random() < 0.35) {
                const sharkEvent = events.find(e => e.id === 'shark_aggressive');
                if (sharkEvent) { this.currentEvent = sharkEvent; this.state.sharkDaysSinceEvent = 0; this.setState('event'); return; }
            }

            // Kiri arc
            const kiriPhase = this.state.kiriPhase || 0;
            const kiriEvents = ['kiri_tackle_box', 'kiri_shelter', 'kiri_signal_fire', 'kiri_bottle_message'];
            const kiriDayReqs = [2, 5, 8, 11];

            if (kiriPhase < 4) {
                const nextEventId = kiriEvents[kiriPhase];
                const nextEvent = events.find(e => e.id === nextEventId);
                if (nextEvent && !this.state.eventsCompleted.includes(nextEventId) && this.state.day >= kiriDayReqs[kiriPhase]) {
                    const chance = kiriPhase === 0 ? 0.5 : 0.4;
                    if (Math.random() < chance || this.state.day >= kiriDayReqs[kiriPhase] + 3) {
                        this.currentEvent = nextEvent;
                        this.setState('event');
                        return;
                    }
                }
            }

            // Wreck trap
            if (this.state.currentLocation === 'lagoon_shipwreck' && this.state.wreckDaysConsecutive >= 3) {
                const wreckDays = this.state.wreckDaysConsecutive;
                const wreckChance = Math.min(0.3 + (wreckDays * 0.1), 0.8);

                if (wreckDays >= 3 && !this.state.eventsCompleted.includes('wreck_comfort') && Math.random() < wreckChance) {
                    const wreckEvent = events.find(e => e.id === 'wreck_comfort');
                    if (wreckEvent) { this.currentEvent = wreckEvent; this.setState('event'); return; }
                }
                if (wreckDays >= 5 && !this.state.eventsCompleted.includes('wreck_creaking') && Math.random() < wreckChance) {
                    const wreckEvent = events.find(e => e.id === 'wreck_creaking');
                    if (wreckEvent) { this.currentEvent = wreckEvent; this.setState('event'); return; }
                }
                if (wreckDays >= 7 && !this.state.eventsCompleted.includes('wreck_sinking') && Math.random() < wreckChance) {
                    const wreckEvent = events.find(e => e.id === 'wreck_sinking');
                    if (wreckEvent) { this.currentEvent = wreckEvent; this.setState('event'); return; }
                }
                if (this.state.wreckDaysConsecutive >= 10) {
                    const wreckEnding = scenario.endings?.find(e => e.id === 'the_wreck');
                    if (wreckEnding) { this.triggerEnding(wreckEnding); return; }
                }
            }

            // Island respect events
            const islandRespect = this.state.islandRespect || 50;
            if (islandRespect >= 55 && this.state.day >= 4 && !this.state.eventsCompleted.includes('island_spirit_offering') && Math.random() < 0.15) {
                const respectEvent = events.find(e => e.id === 'island_spirit_offering');
                if (respectEvent) { this.currentEvent = respectEvent; this.setState('event'); return; }
            }
            if (islandRespect <= 35 && this.state.day >= 5 && !this.state.eventsCompleted.includes('island_warning') && Math.random() < 0.2) {
                const respectEvent = events.find(e => e.id === 'island_warning');
                if (respectEvent) { this.currentEvent = respectEvent; this.setState('event'); return; }
            }
        }

        // ── STANDARD EVENT ROLL ──
        const eligible = events.filter(e => {
            if (e.min_day && this.state.day < e.min_day) return false;
            if (e.max_day && this.state.day > e.max_day) return false;
            if (e.seasons && !e.seasons.includes(this.state.season)) return false;
            if (this.state.eventsCompleted.includes(e.id)) return false;
            if (e.location && this.state.currentLocation !== e.location) return false;

            if (e.condition) {
                if (e.condition.warmth_below && this.state.resources.warmth >= e.condition.warmth_below) return false;
                if (e.condition.signal_below && this.state.signalProgress >= e.condition.signal_below) return false;
                if (e.condition.water_below && (this.state.resources.water === undefined || this.state.resources.water >= e.condition.water_below)) return false;
                if (e.condition.health_below && this.state.resources.health >= e.condition.health_below) return false;
                if (e.condition.karma_above && (this.state.forestKarma || 50) < e.condition.karma_above) return false;
                if (e.condition.karma_below && (this.state.forestKarma || 50) > e.condition.karma_below) return false;
                if (e.condition.islandRespect_above && (this.state.islandRespect || 50) < e.condition.islandRespect_above) return false;
                if (e.condition.islandRespect_below && (this.state.islandRespect || 50) > e.condition.islandRespect_below) return false;
                if (e.condition.wreck_days_above && (this.state.wreckDaysConsecutive || 0) < e.condition.wreck_days_above) return false;
                if (e.condition.has_item && !this.state.inventory.includes(e.condition.has_item)) return false;
                if (e.condition.no_item && this.state.inventory.includes(e.condition.no_item)) return false;
                if (e.condition.has_fire && !this.state.hasFire) return false;
                if (e.condition.no_fire && this.state.hasFire) return false;
                if (e.condition.requires_event && !this.state.eventsCompleted.includes(e.condition.requires_event)) return false;
                if (e.condition.mythic_not_completed && this.state.mythicEventsCompleted?.includes(e.condition.mythic_not_completed)) return false;
                if (e.condition.has_companion && !this.hasCompanion(e.condition.has_companion)) return false;
                if (e.condition.has_companions_above && this.getActiveCompanions().length < e.condition.has_companions_above) return false;
                if (e.condition.morale_below && this.state.resources.morale >= e.condition.morale_below) return false;
                if (e.condition.supermarket_days_above && (this.state.supermarketDaysConsecutive || 0) < e.condition.supermarket_days_above) return false;
                if (e.condition.pack_above && (this.state.packPhase || 0) < e.condition.pack_above) return false;
                if (e.condition.companion_died && !this.state.companions?.some(c => c.id === e.condition.companion_died && c.status === 'dead')) return false;
            }

            if (e.missed_opportunity) return false;

            if (e.mythic) {
                if (this.state.scenarioId !== 'wild_forest') return false;
                if (this.state.mythicEventsCompleted?.includes(e.id)) return false;
            }

            return true;
        });

        const eventChance = 0.5;
        if (Math.random() > eventChance || eligible.length === 0) {
            this.endDay();
            return;
        }

        const event = eligible[Math.floor(Math.random() * eligible.length)];
        this.currentEvent = event;
        this.setState('event');
    }

    getHallucinationEvent() {
        const halluEvents = [
            {
                id: "hallu_person", name: "👤 Someone Walking", icon: "👤",
                text: "You see a figure in the distance, walking slowly across the sand. They seem real — you can make out their clothing, their stride. But when you blink, they're closer. Much closer. Are they real?",
                choices: [
                    { icon: "🏃", text: "Walk towards them", success: 0.2, hours: 2, success_text: "You stumble towards the figure... and it's a real person! A Bedouin herder, who shares water and points you towards a nearby oasis marker.", success_fx: { "morale": 15, "water": 10, "explore_progress": 2 } },
                    { icon: "🚫", text: "It's not real. Stay where you are.", success: 1.0, hours: 0, success_text: "You close your eyes and count to ten. When you look again, the figure has vanished. There was never anyone there.", success_fx: { "morale": -5 } }
                ]
            },
            {
                id: "hallu_oasis", name: "🌴 The Shimmering Pool", icon: "🌴",
                text: "There it is. Water. Palm trees. An oasis, shimmering in the heat. You can almost taste it. But the last time you saw this... it wasn't real. Is this one different?",
                choices: [
                    { icon: "🏃", text: "Go towards it — this time it might be real", success: 0.25, hours: 2, success_text: "You walk for what feels like hours... and incredibly, it IS real. A small oasis with a muddy but drinkable pool.", success_fx: { "water": 30, "morale": 20, "health": 5 } },
                    { icon: "🧠", text: "Don't trust it. Your mind is lying.", success: 1.0, hours: 0, success_text: "You turn away. The oasis shimmers and fades. Just another mirage. But this time, you're certain you made the right choice. Weren't you?", success_fx: { "morale": -5 } }
                ]
            },
            {
                id: "hallu_bus", name: "🚌 The Bus", icon: "🚌",
                text: "You hear an engine. A bus — YOUR bus — appears on the horizon. The door opens and the driver waves. 'Come on!' he shouts. 'I've been looking for you!' It looks so real.",
                choices: [
                    { icon: "🏃", text: "Run to the bus!", success: 0.05, hours: 2, success_text: "You sprint towards the bus... and it dissolves into heat haze. There was nothing there. You've wasted precious energy and water.", success_fx: { "water": -10, "health": -5, "morale": -15 } },
                    { icon: "👋", text: "Wave back, but don't move", success: 1.0, hours: 0, success_text: "You wave slowly. The driver waves back. Then his face melts into sand. The bus evaporates. You're alone again.", success_fx: { "morale": -8 } }
                ]
            }
        ];

        const available = halluEvents.filter(e => !this.state.eventsCompleted.includes(e.id));
        if (available.length === 0) return null;
        return available[Math.floor(Math.random() * available.length)];
    }

    resolveEventChoice(choiceIndex) {
        const event = this.currentEvent;
        if (!event || !event.choices[choiceIndex]) return;

        const choice = event.choices[choiceIndex];

        if (choice.requires && choice.requires.length > 0) {
            const missing = choice.requires.filter(r => !this.state.inventory.includes(r));
            if (missing.length > 0) {
                this.showToast(`Requires: ${missing.join(', ')}`, 'danger');
                return;
            }
        }

        if (choice.condition_has_companions) {
            const activeCompanions = this.state.scenarioId === 'overgrown_city' ? this.getActiveCompanions().length : 0;
            if (activeCompanions < choice.condition_has_companions) {
                this.showToast(`Requires ${choice.condition_has_companions} companions (you have ${activeCompanions})`, 'danger');
                return;
            }
        }

        if (choice.hours > 0) {
            this.state.hoursRemaining -= choice.hours;
        }

        const roll = Math.random();
        const success = roll < choice.success;

        if (!success) {
            this.playAnimation('shake', 500);
        }

        const result = {
            event, choice, success,
            text: success ? choice.success_text : choice.fail_text,
            effects: success ? choice.success_fx : choice.fail_fx
        };

        this.applyEffects(result.effects);

        // Forest karma changes
        if (choice.karma_mod) {
            this.state.forestKarma = Math.max(0, Math.min(100, this.state.forestKarma + choice.karma_mod));
            this.checkForestKarma();
        }

        // Island respect changes
        if (this.state.scenarioId === 'tropical_island' && choice.islandRespect !== undefined) {
            this.state.islandRespect = Math.max(0, Math.min(100, (this.state.islandRespect || 50) + choice.islandRespect));
        }

        // Overgrown City: Companion join
        if (this.state.scenarioId === 'overgrown_city' && choice.companion_join) {
            this.addCompanion(choice.companion_join);
        }

        // Overgrown City: Companion trust changes
        if (this.state.scenarioId === 'overgrown_city' && choice.companion_trust) {
            for (const [compId, trustChange] of Object.entries(choice.companion_trust)) {
                const comp = this.state.companions.find(c => c.id === compId && c.status === 'active');
                if (comp) {
                    comp.trust = Math.max(0, Math.min(comp.maxTrust, comp.trust + trustChange));
                }
            }
        }

        // Overgrown City: Trust all companions
        if (this.state.scenarioId === 'overgrown_city' && choice.companion_trust_all) {
            const trustChange = choice.companion_trust_all;
            for (const comp of this.getActiveCompanions()) {
                comp.trust = Math.max(0, Math.min(comp.maxTrust, comp.trust + trustChange));
            }
        }

        // Overgrown City: Dr. Amara phase tracking
        if (this.state.scenarioId === 'overgrown_city') {
            if (event.id === 'amara_greenhouse') { this.state.amaraPhase = Math.max(this.state.amaraPhase || 0, 1); this.state.amaraDaysSinceEvent = 0; }
            if (event.id === 'amara_lab') { this.state.amaraPhase = Math.max(this.state.amaraPhase || 0, 2); this.state.amaraDaysSinceEvent = 0; }
            if (event.id === 'amara_camp') { this.state.amaraPhase = Math.max(this.state.amaraPhase || 0, 3); this.state.amaraDaysSinceEvent = 0; }
            if (event.id === 'amara_herself') { this.state.amaraPhase = Math.max(this.state.amaraPhase || 0, 4); this.state.amaraDaysSinceEvent = 0; }
            if (event.id && event.id.startsWith('pack_')) { this.state.packDaysSinceEvent = 0; }
            if (event.id && event.id.startsWith('supermarket_')) { this.state.packDaysSinceEvent = 0; }
            if (event.mythic || choice.mythic_complete) {
                if (!this.state.mythicEventsCompleted) this.state.mythicEventsCompleted = [];
                const mythicId = choice.mythic_complete || event.id;
                if (!this.state.mythicEventsCompleted.includes(mythicId)) { this.state.mythicEventsCompleted.push(mythicId); }
            }
        }

        // Injury from failed choices
        if (!success && choice.fail_injury) {
            const injuries = Array.isArray(choice.fail_injury) ? choice.fail_injury : [choice.fail_injury];
            for (const injuryId of injuries) { this.addInjury(injuryId); }
        }

        // Injury treatment from successful choices
        if (success && choice.treat_injury) {
            if (choice.treat_injury === 'all') {
                this.state.injuries = [];
                this.state.injuryFree = true;
                result.text += ' Your injuries have mysteriously vanished!';
            } else {
                const injuries = Array.isArray(choice.treat_injury) ? choice.treat_injury : [choice.treat_injury];
                for (const injuryId of injuries) {
                    if (this.hasInjury(injuryId)) { this.removeInjury(injuryId); result.text += ' Your injury feels much better!'; }
                }
            }
        }

        // Loot from successful choices
        if (success && choice.success_loot) {
            for (const item of choice.success_loot) { this.state.inventory.push(item); }
            result.text += ` You gained: ${choice.success_loot.map(i => `${this.getItemIcon(i)} ${i.replace(/_/g, ' ')}`).join(', ')}.`;
        }

        // Loot from failed choices
        if (!success && choice.fail_loot) {
            for (const item of choice.fail_loot) { this.state.inventory.push(item); }
        }

        // Consumable items on failure
        if (!success && choice.fail_consume) {
            for (const item of choice.fail_consume) {
                const idx = this.state.inventory.indexOf(item);
                if (idx > -1) { this.state.inventory.splice(idx, 1); }
            }
        }

        // Signal override
        if (success && choice.signal_override) {
            this.state.signalProgress = choice.signal_override;
        }

        // Wildlife encounters (Alaska)
        if (event.wildlife) {
            if (!this.state.wildlifeEncounters) this.state.wildlifeEncounters = [];
            this.state.wildlifeEncounters.push({ species: event.wildlife.species, day: this.state.day, success: success });

            if (this.state.scenarioId === 'alaska_winter') {
                if (event.wildlife.species === 'wolf') {
                    if (!success) {
                        this.state.wolfStalking = true;
                        this.state.wolfPhase = 4;
                        this.state.wolfDaysSinceEvent = 0;
                        this.addJournalEntry('🐺 The wolf will be back. You can feel it watching from the trees.');
                    } else {
                        this.state.wolfDaysSinceEvent = 0;
                        if (this.state.wolfPhase < 3) this.state.wolfPhase = 3;
                        if (this.state.shelterLevel >= 3 && this.state.hasFire) {
                            this.state.wolfStalking = false;
                            this.addJournalEntry('🐺 The wolf has left. With strong shelter and fire, it won\'t bother you again — for now.');
                        } else if (this.state.wolfStalking) {
                            this.addJournalEntry('🐺 The wolf retreated this time. But it\'s still out there.');
                        }
                    }
                }
                if (event.wildlife.species === 'bear') {
                    this.state.wolfDaysSinceEvent = 0;
                }
            }

            if (this.state.scenarioId === 'alaska_winter') {
                if (event.id === 'wolf_tracks') { this.state.wolfPhase = Math.max(this.state.wolfPhase, 1); this.state.wolfDaysSinceEvent = 0; }
                if (event.id === 'wolf_howl') { this.state.wolfPhase = Math.max(this.state.wolfPhase, 2); this.state.wolfDaysSinceEvent = 0; }
                if (event.id === 'wolf_pack') { this.state.wolfPhase = Math.max(this.state.wolfPhase, 3); this.state.wolfDaysSinceEvent = 0; }
                if (event.id === 'wolf_stalking' || event.id === 'bear_at_camp') { this.state.wolfDaysSinceEvent = 0; }
            }
        }

        // Wild Forest: Hiker and Watcher phase tracking
        if (this.state.scenarioId === 'wild_forest') {
            if (event.id === 'hikers_backpack') this.state.hikerPhase = Math.max(this.state.hikerPhase || 0, 1);
            if (event.id === 'hikers_trail_marks') this.state.hikerPhase = Math.max(this.state.hikerPhase || 0, 2);
            if (event.id === 'hikers_shelter') this.state.hikerPhase = Math.max(this.state.hikerPhase || 0, 3);
            if (event.id === 'hikers_note') this.state.hikerPhase = Math.max(this.state.hikerPhase || 0, 4);
            if (event.id === 'watcher_sensing') { this.state.watcherPhase = Math.max(this.state.watcherPhase || 0, 1); this.state.watcherDaysSinceEvent = 0; }
            if (event.id === 'watcher_watching') { this.state.watcherPhase = Math.max(this.state.watcherPhase || 0, 2); this.state.watcherDaysSinceEvent = 0; }
            if (event.id === 'watcher_testing') { this.state.watcherPhase = Math.max(this.state.watcherPhase || 0, 3); this.state.watcherDaysSinceEvent = 0; }
        }

        // Desert: Driver phase tracking
        if (this.state.scenarioId === 'desert') {
            if (event.id === 'ray_jacket') this.state.driverPhase = Math.max(this.state.driverPhase || 0, 1);
            if (event.id === 'ray_trail') this.state.driverPhase = Math.max(this.state.driverPhase || 0, 2);
            if (event.id === 'ray_camp') this.state.driverPhase = Math.max(this.state.driverPhase || 0, 3);
            if (event.id === 'ray_body') this.state.driverPhase = Math.max(this.state.driverPhase || 0, 4);
        }

        // Tropical Island: Kiri & shark phase tracking
        if (this.state.scenarioId === 'tropical_island') {
            if (event.id === 'kiri_tackle_box') this.state.kiriPhase = Math.max(this.state.kiriPhase || 0, 1);
            if (event.id === 'kiri_shelter') this.state.kiriPhase = Math.max(this.state.kiriPhase || 0, 2);
            if (event.id === 'kiri_signal_fire') this.state.kiriPhase = Math.max(this.state.kiriPhase || 0, 3);
            if (event.id === 'kiri_bottle_message') this.state.kiriPhase = Math.max(this.state.kiriPhase || 0, 4);
            if (event.id === 'shark_fin_spotted') { this.state.sharkPhase = Math.max(this.state.sharkPhase || 0, 1); this.state.sharkDaysSinceEvent = 0; }
            if (event.id === 'shark_circling') { this.state.sharkPhase = Math.max(this.state.sharkPhase || 0, 2); this.state.sharkDaysSinceEvent = 0; }
            if (event.id === 'shark_bump') { this.state.sharkPhase = Math.max(this.state.sharkPhase || 0, 3); this.state.sharkDaysSinceEvent = 0; }
            if (event.id === 'shark_aggressive') { this.state.sharkPhase = Math.max(this.state.sharkPhase || 0, 4); this.state.sharkDaysSinceEvent = 0; }
            if (event.id === 'wreck_supplies' || event.id === 'wreck_comfort' || event.id === 'wreck_creaking' || event.id === 'wreck_sinking') {
                this.state.wreckDaysSinceEvent = 0;
            }
        }

        // Track mythic events
        if (event.mythic) {
            if (!this.state.mythicEventsCompleted) this.state.mythicEventsCompleted = [];
            if (!this.state.mythicEventsCompleted.includes(event.id)) { this.state.mythicEventsCompleted.push(event.id); }
        }

        this.state.eventsCompleted.push(event.id);
        this.addJournalEntry(result.text);

        this.currentEventResult = result;
        this.setState('event_result');
    }

    afterEventResult() {
        const check = this.checkCriticalResources();
        if (check.dead) return;

        if (check.warnings.length > 0) {
            this.showToast(check.warnings[0], 'danger');
        }

        this.endDay();
    }

    // ==========================================
    // 10. ENDINGS & DEATH
    // ==========================================

    checkEndings() {
        const scenario = this.getScenario();
        const endings = scenario.endings || [];
        const r = this.state.resources;

        // Check for Victory/Escape endings
        for (const ending of endings) {
            const cond = ending.condition;
            if (!cond) continue;
            let met = true;

            if (cond.signal_progress && this.state.signalProgress < cond.signal_progress) met = false;
            if (cond.explore_progress && this.state.exploreProgress < cond.explore_progress) met = false;
            if (cond.days_survived && this.state.daysSurvived < cond.days_survived) met = false;
            if (cond.plants_correct && this.state.plantsCorrect < cond.plants_correct) met = false;
            if (cond.forestKarma_above && this.state.forestKarma < cond.forestKarma_above) met = false;
            if (cond.forestKarma_below && this.state.forestKarma > cond.forestKarma_below) met = false;
            if (cond.wildRespect_above && (this.state.wildRespect || 50) < cond.wildRespect_above) met = false;
            if (cond.wildRespect_below && (this.state.wildRespect || 50) > cond.wildRespect_below) met = false;
            if (cond.requires_event && !this.state.eventsCompleted.includes(cond.requires_event)) met = false;
            if (cond.has_injury && !this.state.injuries.some(i => i.id === cond.has_injury)) met = false;
            if (cond.injury_count_above && this.state.injuries.length <= cond.injury_count_above) met = false;
            if (cond.max_morale && this.state.resources.morale > cond.max_morale) met = false;
            if (cond.islandRespect_above && (this.state.islandRespect || 50) < cond.islandRespect_above) met = false;
            if (cond.islandRespect_below && (this.state.islandRespect || 50) > cond.islandRespect_below) met = false;
            if (cond.wreck_days_above && (this.state.wreckDaysConsecutive || 0) < cond.wreck_days_above) met = false;
            if (cond.signal_progress_below && this.state.signalProgress >= cond.signal_progress_below) met = false;
            if (cond.companions_above && this.getActiveCompanions().length < cond.companions_above) met = false;
            if (cond.has_companion && !this.hasCompanion(cond.has_companion)) met = false;
            if (cond.has_all_companions && this.state.companions.filter(c => c.status === 'active').length < 5) met = false;
            if (cond.morale_below && this.state.resources.morale >= cond.morale_below) met = false;
            if (cond.supermarket_days_above && (this.state.supermarketDaysConsecutive || 0) < cond.supermarket_days_above) met = false;
            if (cond.pack_above && (this.state.packPhase || 0) < cond.pack_above) met = false;
            if (cond.has_companions_above && this.getActiveCompanions().length < cond.has_companions_above) met = false;
            if (cond.companion_died && !this.state.companions?.some(c => c.id === cond.companion_died && c.status === 'dead')) met = false;

            if (cond.min_resources) {
                for (const [key, min] of Object.entries(cond.min_resources)) {
                    if ((r[key] || 0) < min) met = false;
                }
            }

            if (met && (ending.type === 'good' || ending.type === 'mythic')) {
                this.triggerEnding(ending);
                return true;
            }
        }

        // Trap endings (consecutive days)
        if (this.state.scenarioId === 'desert' && this.state.mineDaysConsecutive >= 10) {
            const mineEnding = endings.find(e => e.id === 'the_mine');
            if (mineEnding) { this.triggerEnding(mineEnding); return true; }
        }
        if (this.state.scenarioId === 'wild_forest' && this.state.groveDaysConsecutive >= 10) {
            const groveEnding = endings.find(e => e.id === 'the_grove');
            if (groveEnding) { this.triggerEnding(groveEnding); return true; }
        }
        if (this.state.scenarioId === 'tropical_island' && this.state.wreckDaysConsecutive >= 10) {
            const wreckEnding = endings.find(e => e.id === 'the_wreck');
            if (wreckEnding) { this.triggerEnding(wreckEnding); return true; }
        }

        // Bittersweet endings
        for (const ending of endings) {
            if (ending.type !== 'bittersweet') continue;
            const cond = ending.condition;
            if (!cond) continue;
            let met = true;

            if (cond.signal_progress && this.state.signalProgress < cond.signal_progress) met = false;
            if (cond.explore_progress && this.state.exploreProgress < cond.explore_progress) met = false;
            if (cond.days_survived && this.state.daysSurvived < cond.days_survived) met = false;
            if (cond.requires_event && !this.state.eventsCompleted.includes(cond.requires_event)) met = false;
            if (cond.has_injury && !this.state.injuries.some(i => i.id === cond.has_injury)) met = false;
            if (cond.injury_count_above && this.state.injuries.length <= cond.injury_count_above) met = false;
            if (cond.max_morale && this.state.resources.morale > cond.max_morale) met = false;
            if (cond.wildRespect_above && (this.state.wildRespect || 50) < cond.wildRespect_above) met = false;
            if (cond.wildRespect_below && (this.state.wildRespect || 50) > cond.wildRespect_below) met = false;
            if (cond.forestKarma_above && (this.state.forestKarma || 50) < cond.forestKarma_above) met = false;
            if (cond.forestKarma_below && (this.state.forestKarma || 50) > cond.forestKarma_below) met = false;

            if (cond.min_resources) {
                for (const [key, min] of Object.entries(cond.min_resources)) {
                    if ((this.state.resources[key] || 0) < min) met = false;
                }
            }

            if (met) { this.triggerEnding(ending); return true; }
        }

        // Overgrown City: Supermarket ending
        if (this.state.scenarioId === 'overgrown_city' && this.state.supermarketDaysConsecutive >= 10) {
            const marketEnding = endings.find(e => e.id === 'the_supermarket');
            if (marketEnding) { this.triggerEnding(marketEnding); return true; }
        }

        // Overgrown City: Pack attack death
        if (this.state.scenarioId === 'overgrown_city' && this.state.packPhase >= 4 && this.getActiveCompanions().length === 0) {
            if (Math.random() < 0.3) {
                this.state.causeOfDeath = 'pack_attack';
                const packEnding = endings.find(e => e.id === 'the_pack');
                if (packEnding) { this.triggerEnding(packEnding); return true; }
            }
        }

        // Overgrown City: Building collapse death
        if (this.state.scenarioId === 'overgrown_city') {
            const currentLoc = this.getLocation();
            if (currentLoc && currentLoc.has_stability && this.state.buildingStability[currentLoc.id] <= 0) {
                if (Math.random() < 0.5) {
                    this.state.causeOfDeath = 'building_collapse';
                    const collapseEnding = endings.find(e => e.id === 'building_collapse');
                    if (collapseEnding) { this.triggerEnding(collapseEnding); return true; }
                }
            }
        }

        // Death endings (health <= 0)
        if (r.health <= 0) {
            this.state.causeOfDeath = this.determineCauseOfDeath();

            const specificDeath = endings.find(e => {
                if (!e.condition) return false;
                if (e.type !== 'bad' && e.type !== 'mythic') return false;

                if (e.condition.cause && e.condition.cause === this.state.causeOfDeath) {
                    if (e.condition.wildRespect_above && (this.state.wildRespect || 50) < e.condition.wildRespect_above) return false;
                    if (e.condition.wildRespect_below && (this.state.wildRespect || 50) > e.condition.wildRespect_below) return false;
                    if (e.condition.forestKarma_above && (this.state.forestKarma || 50) < e.condition.forestKarma_above) return false;
                    if (e.condition.requires_event && !this.state.eventsCompleted.includes(e.condition.requires_event)) return false;
                    return true;
                }

                if (e.condition.warmth !== undefined && e.condition.warmth === 0 && r.warmth <= 0) return true;
                if (e.condition.health !== undefined && e.condition.health === 0 && r.health <= 0) return true;
                if (e.condition.water !== undefined && e.condition.water === 0 && r.water <= 0) return true;

                return false;
            });

            if (specificDeath) {
                this.triggerEnding(specificDeath);
            } else {
                const genericDeath = {
                    id: 'generic_death',
                    name: scenario.id === 'alaska_winter' ? 'Frozen' : scenario.id === 'desert' ? 'Perished' : 'The Wild Claims You',
                    icon: '🪦', type: 'bad',
                    text: 'Your body can no longer endure. The wilderness is indifferent — it simply continues without you.',
                    summary: 'Your health reached zero.'
                };
                this.triggerEnding(genericDeath);
            }
            return true;
        }

        return false;
    }

    triggerEnding(ending) {
        let text = ending.text;
        text = text.replace(/{day}/g, this.state.day);
        text = text.replace(/{days}/g, this.state.day);
        text = text.replace(/{scenario}/g, this.getScenario().name);

        this.currentEnding = { ...ending, text };

        const key = `fq_ending_${this.state.scenarioId}_${ending.id}`;
        const unlocked = JSON.parse(localStorage.getItem('fq_endings') || '[]');
        if (!unlocked.includes(key)) {
            unlocked.push(key);
            localStorage.setItem('fq_endings', JSON.stringify(unlocked));
        }

        this.setState('game_over');
    }

    determineCauseOfDeath() {
        const r = this.state.resources;

        // Scenario-specific death causes
        if (this.state.scenarioId === 'tropical_island') {
            if (r.water !== undefined && r.water <= 0) return 'dehydration';
            if (this.hasInjury('sunstroke')) return 'sunstroke';
            if (r.warmth <= 0) return 'exposure';
        }

        if (this.state.scenarioId === 'overgrown_city') {
            if (r.hunger <= 0) return 'starvation';
            if (r.water !== undefined && r.water <= 0) return 'dehydration';
            if (r.warmth <= 0) return 'cold';
            if (this.hasInjury('infection')) return 'disease';
        }

        if (this.state.scenarioId === 'desert') {
            if (r.water !== undefined && r.water <= 0) return 'dehydration';
            if (this.state.weather && (this.state.weather.type === 'scorching' || this.state.weather.type === 'hot')) return 'heat';
            if (r.warmth <= 0) return 'cold';
        }

        if (this.state.scenarioId === 'alaska_winter') {
            if (r.warmth <= 0) return 'cold';
        }

        // General fallbacks
        if (r.water !== undefined && r.water <= 0) return 'dehydration';
        if (r.warmth <= 0) return 'cold';
        if (r.hunger <= 0) return 'starvation';

        const severeInjury = this.state.injuries?.find(i => i.severity === 'severe');
        if (severeInjury) return severeInjury.id;

        return 'health';
    }

    // ==========================================
    // 11. SAVE / LOAD
    // ==========================================

    saveGame() {
        if (!this.state) return;
        const key = `fq_save_${this.state.scenarioId}`;
        localStorage.setItem(key, JSON.stringify(this.state));
        localStorage.setItem('fq_last_scenario', this.state.scenarioId);
        try {
            const globalAch = JSON.parse(localStorage.getItem('fq_achievements') || '{}');
            globalAch[this.state.scenarioId] = this.state.achievements || [];
            localStorage.setItem('fq_achievements', JSON.stringify(globalAch));
        } catch (e) {
            console.warn('Failed to save achievements:', e);
        }
    }

    async loadGame(scenarioId) {
        const key = `fq_save_${scenarioId}`;
        const data = localStorage.getItem(key);
        if (!data) return false;

        try {
            this.state = JSON.parse(data);

            // Migrate missing fields
            const defaults = {
                injuries: [], injuryFree: true, achievements: [], itemsCrafted: [],
                huntsSuccessful: 0, wildlifeEncounters: [], injuriesTreated: 0,
                lastSignalDay: 1, warmthBonus: 0, wolfPhase: 0, wolfDaysSinceEvent: 0,
                wolfEncounterCount: 0, bearInsteadOfWolf: false, cabinDaysConsecutive: 0,
                vulturePhase: 0, vultureDaysSinceEvent: 0, mineDaysConsecutive: 0,
                driverPhase: 0, watcherPhase: 0, watcherDaysSinceEvent: 0,
                groveDaysConsecutive: 0, hikerPhase: 0,
                companions: [], packPhase: 0, packDaysSinceEvent: 0,
                supermarketDaysConsecutive: 0, amaraPhase: 0, amaraDaysSinceEvent: 0,
                buildingStability: { hospital_ruins: 100, underground_station: 100, school_gym: 100, construction_site: 80 },
                hostileSurvivorsEncountered: 0,
                islandRespect: 50, sharkPhase: 0, sharkDaysSinceEvent: 0,
                kiriPhase: 0, wreckDaysConsecutive: 0, tideState: 'low',
                mythicEventsCompleted: [], hallucinationCount: 0,
                stormWarning: 0, wolfStalking: false, forestKarma: 50,
                wildRespect: 50, actionLog: [], dailyMessageShown: [],
                movedThisDay: false, hasFire: false, fireExtinguished: false,
                shelterAtLastLocation: 0
            };

            for (const [key, val] of Object.entries(defaults)) {
                if (this.state[key] === undefined) {
                    this.state[key] = typeof val === 'object' && !Array.isArray(val) ? JSON.parse(JSON.stringify(val)) : val;
                }
            }

            // Migrate injury objects
            this.state.injuries = this.state.injuries.map(i => {
                if (typeof i === 'string') {
                    const def = this.config?.injuries?.[i];
                    return def ? {
                        id: i, name: def.name, icon: def.icon, desc: def.desc,
                        severity: def.severity, dailyEffects: def.daily_effects || {},
                        actionModifiers: def.action_modifiers || {}, daysRemaining: def.duration,
                        duration: def.duration, treatments: def.treatments || {}
                    } : null;
                }
                return i;
            }).filter(Boolean);

            const res = await fetch(`/static/data/foraging/scenarios/${scenarioId}.json`);
            if (res.ok) {
                this.scenarioData = await res.json();
            }

            return true;
        } catch {
            return false;
        }
    }

    hasSaveGame(scenarioId) {
        return !!localStorage.getItem(`fq_save_${scenarioId}`);
    }

    deleteSaveGame(scenarioId) {
        localStorage.removeItem(`fq_save_${scenarioId}`);
    }

    autoSave() {
        if (!this.state) return;
        try {
            const key = `fq_save_${this.state.scenarioId}`;
            localStorage.setItem(key, JSON.stringify(this.state));
            localStorage.setItem('fq_last_scenario', this.state.scenarioId);
            localStorage.setItem('fq_last_save', new Date().toISOString());
        } catch (e) {
            console.warn('Auto-save failed:', e);
        }
    }

    getUnlockedEndings() {
        try { return JSON.parse(localStorage.getItem('fq_endings') || '[]'); }
        catch { return []; }
    }

    getEndingCountForScenario(scenarioId) {
        const all = this.getUnlockedEndings();
        return all.filter(e => e.startsWith(`fq_ending_${scenarioId}_`)).length;
    }

    getTotalEndingCount() {
        return this.getUnlockedEndings().length;
    }

    // ==========================================
    // 12. UI HELPERS
    // ==========================================

    showScreen(name) {
        Object.values(this.screens).forEach(s => {
            if (s) { s.classList.add('hidden'); s.classList.remove('active'); }
        });
        if (this.screens[name]) {
            this.screens[name].classList.remove('hidden');
            this.screens[name].classList.add('active');
        }
    }

    showToast(msg, type = 'success') {
        if (type === 'achievement') {
            const existingAch = document.querySelector('.fq-achievement-toast');
            if (existingAch) existingAch.remove();

            const achDefs = this.config?.achievements || {};
            const achDef = Object.values(achDefs).find(a => msg.includes(a.name));

            const toast = document.createElement('div');
            toast.className = 'fq-achievement-toast';
            toast.innerHTML = `
                <span class="fq-ach-icon">${achDef ? achDef.icon : '🏆'}</span>
                <span class="fq-ach-title">Achievement Unlocked!</span>
                <span class="fq-ach-desc">${achDef ? achDef.desc : msg}</span>
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3200);
            return;
        }

        const existing = document.querySelector('.fq-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = `fq-toast ${type === 'danger' ? 'fq-toast-danger' : type === 'warning' ? 'fq-toast-warning' : ''}`;
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    bindGlobalEvents() {
        document.getElementById('fq-journal-btn')?.addEventListener('click', () => this.showJournal());
        document.getElementById('fq-journal-close')?.addEventListener('click', () => this.hideJournal());
        document.getElementById('fq-menu-btn')?.addEventListener('click', () => this.showMenu());
        document.getElementById('fq-menu-close')?.addEventListener('click', () => this.hideMenu());
        document.getElementById('fq-menu-resume')?.addEventListener('click', () => this.hideMenu());
        document.getElementById('fq-menu-journal')?.addEventListener('click', () => { this.hideMenu(); this.showJournal(); });
        document.getElementById('fq-menu-save')?.addEventListener('click', () => { this.saveGame(); this.showToast('Game saved!'); });
        document.getElementById('fq-menu-quit')?.addEventListener('click', () => { this.hideMenu(); this.state = null; this.renderScenarioSelect(); });
        document.getElementById('fq-save-btn')?.addEventListener('click', () => { this.saveGame(); this.showToast('Game saved!'); });
    }

    showJournal() {
        this.renderJournal();
        this.screens['journal-overlay']?.classList.remove('hidden');
    }

    hideJournal() {
        this.screens['journal-overlay']?.classList.add('hidden');
    }

    showMenu() {
        this.screens['menu-overlay']?.classList.remove('hidden');
    }

    hideMenu() {
        this.screens['menu-overlay']?.classList.add('hidden');
    }

    checkForestKarma() {
        if (this.state.scenarioId !== 'wild_forest') return;
        const karma = this.state.forestKarma || 50;

        if (karma < 30 && !this.state.inventory.includes('foxfire_lantern')) {
            this.playAnimation('eyes_in_dark');
            this.addJournalEntry('🕸️ You feel a hostile gaze upon you... the forest is watching.');
            this.showToast('The forest feels hostile...', 'danger');
        } else if (karma > 70) {
            this.addJournalEntry('🍃 The woods seem to open up before you, guiding your path.');
        }
    }

    // ── OVERGROWN CITY: COMPANION HELPERS ──

    getCompanionDefs() {
        return {
            sam: { id: 'sam', name: 'Sam', age: 14, role: 'Teenager', skill: 'scavenging', skillBonus: 0.2, trust: 70, maxTrust: 100, trustBaseline: 70, moraleEffect: 5, foodConsumption: 5, status: 'undiscovered', icon: '👦', discoverMinDay: 2, discoverMaxDay: 5 },
            mrs_chen: { id: 'mrs_chen', name: 'Mrs. Chen', age: 52, role: 'Teacher', skill: 'medical', skillBonus: 0.2, trust: 60, maxTrust: 100, trustBaseline: 60, moraleEffect: 8, foodConsumption: 6, status: 'undiscovered', icon: '👩‍🏫', discoverMinDay: 4, discoverMaxDay: 7 },
            marcus: { id: 'marcus', name: 'Marcus', age: 35, role: 'Engineer', skill: 'engineering', skillBonus: 0.15, trust: 40, maxTrust: 100, trustBaseline: 40, moraleEffect: 3, foodConsumption: 7, status: 'undiscovered', icon: '🧔', discoverMinDay: 6, discoverMaxDay: 10 },
            lily: { id: 'lily', name: 'Lily', age: 8, role: 'Child', skill: 'morale', skillBonus: 0, trust: 80, maxTrust: 100, trustBaseline: 80, moraleEffect: 12, foodConsumption: 3, status: 'undiscovered', icon: '👧', discoverMinDay: 5, discoverMaxDay: 9 },
            dr_amara: { id: 'dr_amara', name: 'Dr. Amara', age: 45, role: 'Botanist', skill: 'botany', skillBonus: 0.25, trust: 70, maxTrust: 100, trustBaseline: 70, moraleEffect: 6, foodConsumption: 5, status: 'undiscovered', icon: '👩‍🔬', discoverMinDay: 11, discoverMaxDay: 15 }
        };
    }

    getActiveCompanions() {
        return (this.state.companions || []).filter(c => c.status === 'active');
    }

    getCompanionSkillBonus(skillType) {
        const active = this.getActiveCompanions();
        let bonus = 0;
        for (const comp of active) {
            if (comp.skill === skillType) bonus += comp.skillBonus;
        }
        return bonus;
    }

    hasCompanion(compId) {
        return (this.state.companions || []).some(c => c.id === compId && c.status === 'active');
    }

    addCompanion(compId) {
        const defs = this.getCompanionDefs();
        const def = defs[compId];
        if (!def) return;
        if (this.state.companions.some(c => c.id === compId)) return;

        const companion = { ...def };
        companion.status = 'active';
        companion.discoverDay = this.state.day;
        this.state.companions.push(companion);
        this.addJournalEntry(`${companion.icon} ${companion.name} has joined your group!`);
        this.showToast(`${companion.icon} ${companion.name} joined your group!`, 'success');
        this.checkAchievements();
    }

    processCompanionsDaily() {
        if (this.state.scenarioId !== 'overgrown_city') return;
    }

    // ==========================================
    // 26. LOCATION MOVEMENT
    // ==========================================

    moveToLocation(locationId) {
        const scenario = this.getScenario();
        const loc = scenario.locations.find(l => l.id === locationId);

        if (!loc || !this.state.knownLocations.includes(locationId)) {
            this.showToast('You haven\'t discovered this location yet.', 'warning');
            return;
        }

        // Tropical Island: Tide-gated locations
        if (this.state.scenarioId === 'tropical_island') {
            if (loc.tide_required && this.state.tideState !== loc.tide_required) {
                const tideLabel = this.state.tideState === 'high' ? 'High tide' : 'Low tide';
                const neededLabel = loc.tide_required === 'low' ? 'low tide' : 'high tide';
                this.showToast(`${loc.name} is only accessible at ${neededLabel}. Currently: ${tideLabel}.`, 'warning');
                return;
            }
        }

        const oldShelterLevel = this.state.shelterLevel;

        // Moving locations reduces shelter level
        if (loc.shelter_bonus) {
            this.state.shelterLevel = Math.max(0, this.state.shelterLevel - 1);
            if (oldShelterLevel > 0 && this.state.shelterLevel < oldShelterLevel) {
                this.addJournalEntry(`Moved to ${loc.icon} ${loc.name}. Your shelter isn't as good here — you'll need to rebuild.`);
                this.showToast('Shelter downgraded: you need to rebuild!', 'warning');
            }
        } else if (oldShelterLevel > 0) {
            this.state.shelterLevel = Math.max(0, this.state.shelterLevel - 2);
            this.addJournalEntry(`Moved to ${loc.icon} ${loc.name}. You've left your shelter behind — you'll need to start over.`);
            this.showToast('Shelter lost! You must rebuild.', 'danger');
            this.playAnimation('shake', 500);
        }

        this.state.currentLocation = locationId;
        this.state.movedThisDay = true;
        this.addJournalEntry(`Moved to ${loc.icon} ${loc.name}.`);
        this.renderGameScreen();
        this.showToast(`Moved to ${loc.icon} ${loc.name}`);
    }

        // ==========================================
    // 13. RENDER — SCENARIO SELECT
    // ==========================================

    renderScenarioSelect() {
        this.showScreen('select');
        const container = document.getElementById('fq-scenarios');
        if (!container || !this.config) return;

        let html = '';
        for (const [id, s] of Object.entries(this.config.scenarios)) {
            const diffClass = `fq-diff-${s.difficulty}`;
            const diffLabel = { 1: 'Easy', 2: 'Moderate', 3: 'Hard', 4: 'Extreme' }[s.difficulty] || 'Unknown';
            const diffStars = '★'.repeat(s.difficulty) + '☆'.repeat(Math.max(0, 3 - s.difficulty));
            const hasSave = this.hasSaveGame(id);

            html += `
            <div class="fq-scenario-card ${diffClass}" data-scenario="${id}">
                <span class="fq-scenario-icon">${s.icon}</span>
                <div class="fq-scenario-name">${s.name}</div>
                <div class="fq-scenario-diff ${diffClass}">${diffStars} ${diffLabel}</div>
                <div class="fq-scenario-desc">${s.tagline}</div>
                ${hasSave ? '<div class="fq-scenario-stat" style="color: var(--amber);">💾 Save found</div>' : ''}
            </div>`;
        }

        container.innerHTML = html;

        container.querySelectorAll('.fq-scenario-card').forEach(card => {
            card.addEventListener('click', async () => {
                const id = card.dataset.scenario;
                if (this.hasSaveGame(id)) {
                    if (confirm('A saved game exists for this scenario. Load it?')) {
                        try {
                            const res = await fetch(`/static/data/foraging/scenarios/${id}.json`);
                            this.scenarioData = await res.json();
                        } catch (err) {
                            this.showToast('Failed to load scenario data.', 'danger');
                            return;
                        }
                        this.loadGame(id);
                        this.showScreen('game');
                        this.render();
                        return;
                    }
                }
                this.selectScenario(id);
            });
        });
    }

    // ==========================================
    // 14. RENDER — INTRO
    // ==========================================

    renderIntro() {
        this.showScreen('intro');
        const scenario = this.scenarioData;

        document.getElementById('fq-intro-icon').textContent = scenario.icon;
        document.getElementById('fq-intro-title').textContent = scenario.name;
        document.getElementById('fq-intro-tagline').textContent = scenario.tagline;
        document.getElementById('fq-intro-text').innerHTML = `<p>${scenario.intro}</p>`;

        const resDiv = document.getElementById('fq-intro-resources');
        const r = scenario.starting;
        resDiv.innerHTML = `
            <div class="fq-start-stat"><span class="fq-ss-icon">❤️</span><span class="fq-ss-label">Health</span><span class="fq-ss-value">${r.health}</span></div>
            <div class="fq-start-stat"><span class="fq-ss-icon">🍖</span><span class="fq-ss-label">Hunger</span><span class="fq-ss-value">${r.hunger}</span></div>
            <div class="fq-start-stat"><span class="fq-ss-icon">🔥</span><span class="fq-ss-label">Warmth</span><span class="fq-ss-value">${r.warmth}</span></div>
            <div class="fq-start-stat"><span class="fq-ss-icon">💭</span><span class="fq-ss-label">Morale</span><span class="fq-ss-value">${r.morale}</span></div>
            ${r.water !== null && r.water !== undefined ? `<div class="fq-start-stat"><span class="fq-ss-icon">💧</span><span class="fq-ss-label">Water</span><span class="fq-ss-value">${r.water}</span></div>` : ''}
        `;

        document.getElementById('fq-begin-btn').onclick = () => { this.startGame(); };
        document.getElementById('fq-back-select-btn').onclick = () => { this.state = null; this.scenarioData = null; this.renderScenarioSelect(); };
    }

    // ==========================================
    // 15. RENDER — GAME SCREEN (shared chrome)
    // ==========================================

    renderGameScreen() {
        this.showScreen('game');
        this.renderTopBar();
        this.renderResources();
        this.renderHoursBar();
        this.renderLocationBar();
        this.renderInventoryBar();

        const container = document.body;
        container.classList.remove('anim-heat-shimmer', 'anim-sandstorm');
        if (this.state.weather) {
            if (this.state.weather.type === 'scorching' || this.state.weather.type === 'hot') {
                container.classList.add('anim-heat-shimmer');
            } else if (this.state.weather.type === 'sandstorm') {
                container.classList.add('anim-sandstorm');
            }
        }
    }

    renderTopBar() {
        const scenarioSeasonIcons = this.scenarioData?.seasonIcons || {};
        const baseSeasonIcons = window.FQ_CONFIG?.seasonIcons || {};
        const seasonIcons = { ...baseSeasonIcons, ...scenarioSeasonIcons };

        document.getElementById('fq-day-badge').textContent = `Day ${this.state.day}`;
        document.getElementById('fq-season-badge').textContent = `${seasonIcons[this.state.season] || ''} ${this.state.season}`;

        const weatherBadge = document.getElementById('fq-weather-badge');
        if (this.state.weather) {
            weatherBadge.textContent = `${this.state.weather.icon} ${this.state.weather.type?.charAt(0).toUpperCase() + this.state.weather.type?.slice(1) || ''}`;
        }
    }

    renderResources() {
        const container = document.getElementById('fq-resources');
        const r = this.state.resources;
        const max = this.state.maxResources;
        const hasWater = r.water !== undefined && r.water !== null;

        container.className = `fq-resources${hasWater ? ' fq-5-bars' : ''}`;

        const bars = [
            { key: 'health', icon: '❤️', label: 'Health', fillClass: 'fq-fill-health' },
            { key: 'hunger', icon: '🍖', label: 'Hunger', fillClass: 'fq-fill-hunger' },
            { key: 'warmth', icon: '🔥', label: 'Warmth', fillClass: 'fq-fill-warmth' },
            { key: 'morale', icon: '💭', label: 'Morale', fillClass: 'fq-fill-morale' },
        ];

        if (hasWater) {
            bars.push({ key: 'water', icon: '💧', label: 'Water', fillClass: 'fq-fill-water' });
        }

        container.innerHTML = bars.map(b => {
            const val = r[b.key];
            const maxVal = max[b.key];
            const pct = Math.max(0, Math.min(100, (val / maxVal) * 100));
            const isLow = val <= 25;
            const isCritical = val <= 10;
            const lowClass = isLow ? ' fq-low' : '';
            const criticalClass = isCritical ? ' fq-critical' : '';

            return `
            <div class="fq-resource-bar${lowClass}${criticalClass}">
                <div class="fq-resource-header">
                    <span class="fq-resource-label">${b.icon} ${b.label}</span>
                    <span class="fq-resource-value">${Math.round(val)}/${maxVal}</span>
                </div>
                <div class="fq-resource-track">
                    <div class="fq-resource-fill ${b.fillClass}" style="width: ${pct}%"></div>
                </div>
            </div>`;
        }).join('');
    }

    renderHoursBar() {
        const container = document.getElementById('fq-hours-bar');
        const scenario = this.getScenario();
        const totalHours = scenario.hours_per_day;
        const remaining = this.state.hoursRemaining;
        const used = totalHours - remaining;

        let pipsHtml = '';
        for (let i = 0; i < totalHours; i++) {
            const cls = i < used ? 'fq-spent' : (i === used ? 'fq-current' : '');
            pipsHtml += `<div class="fq-hours-pip ${cls}"></div>`;
        }

        container.innerHTML = `
            <span class="fq-hours-label">☀️ Daylight</span>
            <div class="fq-hours-pips">${pipsHtml}</div>
            <span class="fq-hours-value">${remaining}h remaining</span>
        `;
    }

    renderLocationBar() {
        const container = document.getElementById('fq-location-bar');
        const loc = this.getLocation();
        const scenario = this.getScenario();

        if (loc) {
            container.innerHTML = `
                <span class="fq-location-icon">${loc.icon}</span>
                <span class="fq-location-name">${loc.name}</span>
                <span class="fq-location-desc">${loc.desc}</span>
            `;
        } else {
            const defaultLoc = scenario.locations.find(l => l.id === this.state.currentLocation) || scenario.locations[0];
            container.innerHTML = `
                <span class="fq-location-icon">${defaultLoc.icon}</span>
                <span class="fq-location-name">${defaultLoc.name}</span>
            `;
        }
    }

    renderInventoryBar() {
        const container = document.getElementById('fq-inventory-bar');
        const inv = this.state.inventory;

        if (inv.length === 0) {
            container.innerHTML = '<span class="fq-inv-label">Inventory:</span> <span class="fq-inv-empty">Empty</span>';
            return;
        }

        const counts = {};
        inv.forEach(item => { counts[item] = (counts[item] || 0) + 1; });

        const itemIcons = {
            compass: '🧭', water_bottle: '🍶', wood: '🪵', cordage: '🧶',
            knife_blade: '🔪', tin_can: '🥫', wire: '🔗', fish: '🐟',
            lighter: '🔥', backpack: '🎒', walking_stick: '🦯',
            snare: '🪤', spear: '🗡️', water_filter: '🫗', fire_bow: '🔥',
            shade_cloth: '🫧', rabbit: '🐇', water: '💧',
            raw_meat: '🥩', animal_fur: '🦊', feathers: '🪶',
            medicinal_herbs: '🌿', bandage: '🩹', herbal_tea: '🍵',
            bow: '🏹', fishing_rod: '🎣', fur_wrap: '🧣', splint: '🦴',
            herbal_poultice: '🌿', cooked_food: '🍖',
            glowing_fungi: '✨', berries: '🫐', coins: '🪙',
            sun_hat: '👒', solar_still: '🫗', rowan_talisman: '🪬',
            foxfire_lantern: '👻', offering_bundle: '🍂',
            canned_food: '🥫', med_kit: '🏥', community_meal: '🍲',
            research_notes: '📋'
        };

        const itemOrder = ['compass','water_bottle','knife_blade','lighter','wire','cordage','wood',
            'medicinal_herbs','bandage','splint','herbal_poultice','herbal_tea',
            'snare','spear','bow','fishing_rod','fire_bow','water_filter','fur_wrap',
            'raw_meat','cooked_food','fish','animal_fur','feathers','shade_cloth'];

        let html = '<span class="fq-inv-label">Inventory:</span>';
        const sortedItems = Object.entries(counts).sort((a, b) => {
            const ai = itemOrder.indexOf(a[0]);
            const bi = itemOrder.indexOf(b[0]);
            return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
        });

        for (const [item, count] of sortedItems) {
            const icon = itemIcons[item] || '📦';
            const def = this.config.crafting?.[item];
            const isConsumable = def?.consumable;
            const clickAttr = isConsumable ? `onclick="window.foragingQuest?.resolveUseItem('${item}')"` : '';
            const consumableClass = isConsumable ? ' fq-consumable' : '';
            html += `<span class="fq-inv-item${consumableClass}" ${clickAttr} title="${def?.desc || item.replace(/_/g, ' ')}">${icon}${count > 1 ? ' ×' + count : ''} ${item.replace(/_/g, ' ')}</span>`;
        }
        container.innerHTML = html;
    }

    // ==========================================
    // 16. RENDER — DAY START
    // ==========================================

    renderDayStart() {
        this.renderGameScreen();

        this.renderAtmosphere();

        const scenario = this.getScenario();
        const weather = this.state.weather;
        const seasonFlavour = this.scenarioData?.weather_flavour?.[this.state.scenarioId]?.day_start?.[weather?.type];
        let dayStartFlavour = this.scenarioData?.day_start;
        if (dayStartFlavour && !Array.isArray(dayStartFlavour)) {
            dayStartFlavour = dayStartFlavour[this.state.scenarioId] || dayStartFlavour[Object.keys(dayStartFlavour)[0]];
        }

        let narrative = '';
        if (seasonFlavour) {
            narrative = seasonFlavour;
        } else if (dayStartFlavour && dayStartFlavour.length > 0) {
            narrative = dayStartFlavour[Math.floor(Math.random() * dayStartFlavour.length)];
        } else {
            narrative = `Day ${this.state.day} begins. The ${this.state.season.toLowerCase()} weather ${weather ? 'is ' + weather.type : 'settles'} around you.`;
        }

        const loc = this.getLocation();
        if (loc) {
            narrative += `<br><br><em>You are at ${loc.icon} ${loc.name}.</em>`;
        }

        // Fire status
        if (this.state.hasFire !== undefined) {
            if (this.state.hasFire) {
                narrative += `<div style="background:rgba(255,152,0,0.15);border:1px solid rgba(255,152,0,0.3);border-radius:6px;padding:8px 12px;margin:8px 0;color:#ff9800;">🔥 Your fire is lit. The flames push back the cold.</div>`;
            } else {
                narrative += `<div style="background:rgba(100,181,246,0.1);border:1px solid rgba(100,181,246,0.3);border-radius:6px;padding:8px 12px;margin:8px 0;color:#64b5f6;">❄️ You have no fire. The cold presses in from all sides.</div>`;
            }
        }

        // Low resource warnings
        const warnings = [];
        if (this.state.resources.health <= 25) warnings.push('⚠️ Your health is critical.');
        if (this.state.resources.hunger <= 20) warnings.push('⚠️ You are starving.');
        if (this.state.resources.warmth <= 20) warnings.push('⚠️ You are freezing.');
        if (this.state.resources.morale <= 20) warnings.push('⚠️ Your spirit is failing.');
        if (this.state.resources.water !== undefined && this.state.resources.water <= 20) warnings.push('⚠️ You are dehydrated.');

        if (warnings.length > 0) {
            narrative += `<br><br><span style="color: #ff8a80;">${warnings.join(' ')}</span>`;
        }

        // Injury display
        if (this.state.injuries && this.state.injuries.length > 0) {
            narrative += `<br><br><span style="color: #ff8a80;">`;
            for (const injury of this.state.injuries) {
                const sevLabel = injury.severity === 'severe' ? '🔴' : injury.severity === 'moderate' ? '🟡' : '🟢';
                narrative += `${sevLabel} ${injury.icon} ${injury.name} (${injury.daysRemaining}d) `;
            }
            narrative += `</span>`;
        }

        // ── TROPICAL ISLAND: Tide, shark, respect, wreck (single block, no duplicates) ──
        if (this.state.scenarioId === 'tropical_island') {
            // Tide display
            if (this.state.tideState) {
                const tideIcon = this.state.tideState === 'low' ? '🌊' : '🏖️';
                const tideDesc = this.state.tideState === 'low' ? 'Low tide — rock pools and reef cave are accessible.' : 'High tide — rock pools and reef cave are submerged.';
                const tideColor = this.state.tideState === 'low' ? '#4fc3f7' : '#ff9800';
                narrative += `<div style="background:rgba(79,195,247,0.1);border:1px solid rgba(79,195,247,0.3);border-radius:6px;padding:8px 12px;margin:8px 0;color:${tideColor};">${tideIcon} Tide: ${this.state.tideState === 'low' ? 'Low Tide' : 'High Tide'} — ${tideDesc}</div>`;
            }

            // Shark phase indicator
            if ((this.state.sharkPhase || 0) >= 1) {
                const sharkPhase = this.state.sharkPhase;
                const sharkLabels = ['', 'Spotted', 'Circling', 'Testing', 'Territorial'];
                const sharkIcons = ['', '🦈', '🦈', '🦈', '🦈'];
                const sharkColors = ['', '#8BC34A', '#FFC107', '#FF9800', '#F44336'];
                narrative += `<div style="color: ${sharkColors[sharkPhase]}; margin-top: 0.3rem; font-size: 0.85rem;">${sharkIcons[sharkPhase]} Shark: ${sharkLabels[sharkPhase]}</div>`;
            }

            // Island respect indicator
            if (this.state.islandRespect !== undefined) {
                const respect = this.state.islandRespect;
                const respectLabel = respect >= 70 ? 'Respected' : respect >= 40 ? 'Neutral' : 'Hostile';
                const respectClass = respect >= 70 ? 'karma-friendly' : respect >= 40 ? 'karma-neutral' : 'karma-hostile';
                const respectIcon = respect >= 70 ? '🌴' : respect >= 40 ? '🏝️' : '⛈️';
                narrative += `
                <div class="fq-karma-bar">
                    <span>${respectIcon} Island: ${respectLabel}</span>
                    <div class="fq-karma-track">
                        <div class="fq-karma-fill ${respectClass}" style="width: ${respect}%"></div>
                    </div>
                    <span>${respect}/100</span>
                </div>`;
            }

            // Wreck consecutive days warning
            if (this.state.wreckDaysConsecutive >= 3) {
                const wreckDays = this.state.wreckDaysConsecutive;
                const wreckColor = wreckDays >= 8 ? '#f44336' : wreckDays >= 5 ? '#ff9800' : '#ffc107';
                narrative += `<div style="color: ${wreckColor}; margin-top: 0.5rem; font-size: 0.85rem;">🚢 Days on the wreck: ${wreckDays}${wreckDays >= 5 ? ' — It feels safe here. Too safe.' : ''}${wreckDays >= 8 ? ' The hull groans. Water seeps in.' : ''}</div>`;
            }
        }

        // ── OVERGROWN CITY: Companion display ──
        if (this.state.scenarioId === 'overgrown_city') {
            const activeCompanions = this.getActiveCompanions();

            if (activeCompanions.length > 0) {
                narrative += `<div style="background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.3);border-radius:6px;padding:8px 12px;margin:8px 0;">`;
                narrative += `<div style="font-weight:bold;margin-bottom:4px;">👥 Community (${activeCompanions.length})</div>`;
                for (const comp of activeCompanions) {
                    const trustColor = comp.trust >= 70 ? '#4caf50' : comp.trust >= 40 ? '#ff9800' : '#f44336';
                    const trustBars = '█'.repeat(Math.floor(comp.trust / 10)) + '░'.repeat(10 - Math.floor(comp.trust / 10));
                    narrative += `<div style="display:flex;align-items:center;gap:6px;margin:2px 0;font-size:0.8rem;">`;
                    narrative += `<span>${comp.icon}</span>`;
                    narrative += `<span style="min-width:80px;">${comp.name}</span>`;
                    narrative += `<span style="color:${trustColor};font-size:0.75rem;" title="Trust: ${comp.trust}%">${trustBars} ${comp.trust}%</span>`;
                    narrative += `<span style="color:var(--cream-dim);font-size:0.7rem;">${comp.role}</span>`;
                    narrative += `</div>`;
                }
                narrative += `</div>`;
            } else {
                narrative += `<div style="background:rgba(255,152,0,0.1);border:1px solid rgba(255,152,0,0.3);border-radius:6px;padding:8px 12px;margin:8px 0;color:#ff9800;font-size:0.85rem;">`;
                narrative += `You are alone. Find other survivors to increase your chances.`;
                narrative += `</div>`;
            }

            // Pack phase indicator
            if (this.state.packPhase >= 1) {
                const packPhase = this.state.packPhase;
                const packLabels = ['', 'Howls heard', 'Kills found', 'Surrounding shelter', 'Attacking'];
                const packIcons = ['', '🐕', '🐕', '🐕', '🐕'];
                const packColors = ['', '#8BC34A', '#FFC107', '#FF9800', '#F44336'];
                narrative += `<div style="color: ${packColors[packPhase]}; margin-top: 0.3rem; font-size: 0.85rem;">${packIcons[packPhase]} Dogs: ${packLabels[packPhase]}</div>`;
            }

            // Supermarket days warning
            if (this.state.supermarketDaysConsecutive >= 3) {
                const marketDays = this.state.supermarketDaysConsecutive;
                const marketColor = marketDays >= 8 ? '#f44336' : marketDays >= 5 ? '#ff9800' : '#ffc107';
                narrative += `<div style="color: ${marketColor}; margin-top: 0.3rem; font-size: 0.85rem;">🛒 Days in supermarket: ${marketDays}${marketDays >= 5 ? ' — It feels safe here. Too safe.' : ''}</div>`;
            }
        }

        // ── Alaska: Storm warning ──
        if (this.state.scenarioId === 'alaska_winter' && this.state.stormWarning > 0) {
            narrative += `<div class="fq-storm-alert">⚠️ A great storm is coming in ${this.state.stormWarning} day${this.state.stormWarning > 1 ? 's' : ''}! Prepare now!</div>`;
        }

        // ── Alaska: Wolf stalking warning ──
        if (this.state.scenarioId === 'alaska_winter' && this.state.wolfStalking) {
            narrative += `<div style="color: #ff8a80; margin-top: 0.5rem; font-size: 0.85rem;" class="fq-wolf-stalking">🐺 The wolf is still tracking you. Be careful.</div>`;
        }

        // ── Alaska: Cabin days warning ──
        if (this.state.scenarioId === 'alaska_winter' && this.state.cabinDaysConsecutive >= 3) {
            const cabinDays = this.state.cabinDaysConsecutive;
            const cabinWarningColor = cabinDays >= 8 ? '#f44336' : cabinDays >= 5 ? '#ff9800' : '#ffc107';
            narrative += `<div style="color: ${cabinWarningColor}; margin-top: 0.5rem; font-size: 0.85rem;">🏚️ Days in cabin: ${cabinDays}${cabinDays >= 5 ? ' — The walls feel close.' : ''}${cabinDays >= 8 ? ' You should leave.' : ''}</div>`;
        }

        // ── Desert: Mine days warning ──
        if (this.state.scenarioId === 'desert' && this.state.mineDaysConsecutive >= 3) {
            const mineDays = this.state.mineDaysConsecutive;
            const mineColor = mineDays >= 8 ? '#f44336' : mineDays >= 5 ? '#ff9800' : '#ffc107';
            narrative += `<div style="color: ${mineColor}; margin-top: 0.5rem; font-size: 0.85rem;">⛏️ Days in mine: ${mineDays}${mineDays >= 5 ? ' — The darkness feels safe. That worries you.' : ''}${mineDays >= 8 ? ' Do you even want to leave?' : ''}</div>`;
        }

        // ── Desert: Vulture warning ──
        if (this.state.scenarioId === 'desert' && this.state.vulturePhase >= 2) {
            const vultureText = this.state.vulturePhase >= 4 ? 'landed nearby, watching' : this.state.vulturePhase >= 3 ? 'directly overhead, waiting' : 'circling closer';
            narrative += `<div style="color: #9e9e9e; margin-top: 0.5rem; font-size: 0.85rem;">🦅 Vultures ${vultureText}.</div>`;
        }

        // ── Wild Forest: Karma indicator ──
        if (this.state.scenarioId === 'wild_forest' && this.state.forestKarma !== undefined) {
            const karma = this.state.forestKarma;
            const karmaLabel = karma >= 70 ? 'Friendly' : karma >= 40 ? 'Neutral' : 'Hostile';
            const karmaClass = karma >= 70 ? 'karma-friendly' : karma >= 40 ? 'karma-neutral' : 'karma-hostile';
            const karmaIcon = karma >= 70 ? '🌿' : karma >= 40 ? '🍃' : '🕸️';
            narrative += `
            <div class="fq-karma-bar">
                <span>${karmaIcon} Forest: ${karmaLabel}</span>
                <div class="fq-karma-track">
                    <div class="fq-karma-fill ${karmaClass}" style="width: ${karma}%"></div>
                </div>
                <span>${karma}/100</span>
            </div>`;

            const watcherPhase = this.state.watcherPhase || 0;
            if (watcherPhase >= 1) {
                const watcherLabels = ['', 'Sensing', 'Watching', 'Testing', 'Judging'];
                const watcherIcons = ['', '🌿', '👁️', '🔍', '⚖️'];
                const watcherColors = ['', '#8BC34A', '#FFC107', '#FF9800', '#F44336'];
                narrative += `<div style="color: ${watcherColors[watcherPhase]}; margin-top: 0.3rem; font-size: 0.85rem;">${watcherIcons[watcherPhase]} The Forest: ${watcherLabels[watcherPhase]}</div>`;
            }

            if (this.state.groveDaysConsecutive >= 3) {
                const groveDays = this.state.groveDaysConsecutive;
                const groveColor = groveDays >= 8 ? '#f44336' : groveDays >= 5 ? '#ff9800' : '#ffc107';
                narrative += `<div style="color: ${groveColor}; margin-top: 0.3rem; font-size: 0.85rem;">🍄 Days in the grove: ${groveDays}${groveDays >= 5 ? ' — The mushrooms welcome you.' : ''}${groveDays >= 8 ? ' You don\'t want to leave.' : ''}</div>`;
            }
        }

        // Shelter & progress info
        const shelter = this.getShelterName();
        narrative += `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 1rem; font-size: 0.85rem; color: var(--cream-dim);">
            <div>🏕️ Shelter: <strong style="color: var(--cream)">${shelter.icon} ${shelter.name}</strong></div>
            <div>📡 Signal: ${this.getSignalProgress()}</div>
            <div>🧭 Explore: ${this.getExploreProgress()}</div>
            <div>🌿 Plants ID'd: <strong style="color: var(--green-light)">${this.state.plantsCorrect}</strong></div>
        </div>`;

        document.getElementById('fq-narrative').innerHTML = `<p>${narrative}</p>`;
        document.getElementById('fq-actions').innerHTML = '';
        this.hideAllGamePanels();

        this.checkAchievements();

        document.getElementById('fq-narrative').innerHTML += `<button class="btn-primary fq-btn-continue" id="fq-continue-day">Choose Your Actions</button>`;

        document.getElementById('fq-continue-day')?.addEventListener('click', () => {
            this.setState('choose_actions');
        });
    }

    // ==========================================
    // 17. RENDER — CHOOSE ACTIONS
    // ==========================================

    renderChooseActions() {
        if (this.craftingMode) {
            this.renderCraftingMenu();
            return;
        }

        this.renderGameScreen();

        const scenario = this.getScenario();
        const remaining = this.state.hoursRemaining;
        const actionsLeft = this.state.maxActions - this.state.actionsUsed;

        let narrative = `<p>Day ${this.state.day} — You have <strong>${remaining} hours</strong> of daylight remaining and <strong>${actionsLeft} action${actionsLeft !== 1 ? 's' : ''}</strong> left.</p>`;

        // Active injuries
        if (this.state.injuries && this.state.injuries.length > 0) {
            narrative += `<div class="fq-injury-panel"><div class="fq-injury-panel-title">🩹 Active Injuries</div><div class="fq-injury-bar">`;
            for (const injury of this.state.injuries) {
                const sevClass = `severity-${injury.severity}`;
                narrative += `<span class="fq-injury-tag ${sevClass}">${injury.icon} ${injury.name} <span class="fq-injury-days">(${injury.daysRemaining}d)</span></span>`;
            }
            narrative += `</div></div>`;
        }

        // Usable items hint
        const usableItems = this.getUsableItems();
        if (usableItems.length > 0) {
            narrative += `<p style="color: var(--amber); font-size: 0.85rem;">💊 You have usable items: ${usableItems.map(i => `${i.icon} ${i.name}`).join(', ')}</p>`;
        }

        // Fire status
        if (this.state.hasFire !== undefined) {
            if (this.state.hasFire) {
                narrative += `<div style="background:rgba(255,152,0,0.15);border:1px solid rgba(255,152,0,0.3);border-radius:6px;padding:6px 10px;margin:6px 0;color:#ff9800;font-size:0.9rem;">🔥 Fire lit — +5 warmth, +3 morale, cooking enabled, frostbite prevented</div>`;
            } else {
                narrative += `<div style="background:rgba(100,181,246,0.1);border:1px solid rgba(100,181,246,0.3);border-radius:6px;padding:6px 10px;margin:6px 0;color:#64b5f6;font-size:0.9rem;">❄️ No fire — You are exposed to the cold. Light a fire for warmth, cooking, and water.</div>`;
            }
        }

        narrative += `<p>What will you do?</p>`;

        document.getElementById('fq-narrative').innerHTML = narrative;

        const actionsContainer = document.getElementById('fq-actions');
        const allActions = this.config.actions;
        const availableActions = this.getAvailableActions();
        const loc = this.getLocation();

        // Location selector
        const locSelectorHtml = this.renderLocationSelector();
        let html = locSelectorHtml;

        for (const actionId of availableActions) {
            const action = allActions[actionId];
            if (!action) continue;

            // Special: light_fire
            if (actionId === 'light_fire') {
                const alreadyHasFire = this.state.hasFire;
                const hasWood = this.state.inventory.includes('wood');
                const canAffordHours = 1 <= remaining;
                const canAffordActions = actionsLeft > 0;
                const canDo = canAffordHours && canAffordActions && (hasWood || alreadyHasFire);

                let disabledClass = canDo ? '' : ' fq-action-disabled';
                let reqText = '';

                if (alreadyHasFire) {
                    disabledClass = ' fq-action-disabled';
                    reqText = '<span class="fq-action-requires" style="color:#ff9800;">🔥 Fire already lit</span>';
                } else if (!hasWood) {
                    reqText = '<span class="fq-action-requires">Requires: wood</span>';
                }

                const hasFireBow = this.state.inventory.includes('fire_bow');
                const successChance = alreadyHasFire ? '—' : (hasFireBow ? '100%' : '70%');
                const weatherNote = (this.state.weather?.type === 'blizzard' || this.state.weather?.type === 'freezing_rain') ? ' (worse in this weather)' : '';

                html += `
                <div class="fq-action-btn${disabledClass}" data-action="light_fire">
                    <div class="fq-action-top">
                        <span class="fq-action-icon">${alreadyHasFire ? '🔥' : '🪵'}</span>
                        <span class="fq-action-name">${alreadyHasFire ? 'Fire Lit ✓' : 'Light Fire'}</span>
                        <span class="fq-action-hours">⏱ 1h</span>
                    </div>
                    <span class="fq-action-desc">${alreadyHasFire ? 'Your fire is already burning.' : 'Build a fire for warmth, cooking, and boiling water.'}</span>
                    ${reqText}
                    ${!alreadyHasFire ? `<span class="fq-action-chance">Success: ${successChance}${weatherNote}</span>` : ''}
                </div>`;
                continue;
            }

            // Special: melt_water
            if (actionId === 'melt_water') {
                const hasFire = this.state.hasFire;
                const canAffordHours = 1 <= remaining;
                const canAffordActions = actionsLeft > 0;
                const canDo = canAffordHours && canAffordActions && hasFire;

                let disabledClass = canDo ? '' : ' fq-action-disabled';
                let reqText = '';

                if (!hasFire) {
                    disabledClass = ' fq-action-disabled';
                    reqText = '<span class="fq-action-requires">Requires: lit fire 🔥</span>';
                }

                const waterGain = (this.getLocation()?.id === 'frozen_creek') ? 20 : 15;

                html += `
                <div class="fq-action-btn${disabledClass}" data-action="melt_water">
                    <div class="fq-action-top">
                        <span class="fq-action-icon">🫗</span>
                        <span class="fq-action-name">Melt Snow for Water</span>
                        <span class="fq-action-hours">⏱ 1h</span>
                    </div>
                    <span class="fq-action-desc">Melt snow or ice over a fire for drinking water.</span>
                    ${reqText}
                    <span class="fq-action-chance">+${waterGain} 💧</span>
                </div>`;
                continue;
            }

            const hours = this.getActionHours(actionId);
            const canAfford = hours <= remaining && actionsLeft > 0;

            const missingReqs = (action.requires || []).filter(r => !this.state.inventory.includes(r));
            const hasReqs = missingReqs.length === 0;
            const canDo = canAfford && hasReqs;

            let disabledClass = canDo ? '' : ' fq-action-disabled';
            let reqText = missingReqs.length > 0 ? `<span class="fq-action-requires">Requires: ${missingReqs.join(', ')}</span>` : '';

            // Signal needs wood
            if (actionId === 'signal' && !this.state.inventory.includes('wood')) {
                reqText = '<span class="fq-action-requires">Requires: wood</span>';
                if (canDo) disabledClass = ' fq-action-disabled';
            }

            // Hide find_water if at water source (non-desert, non-alaska)
            if (actionId === 'find_water' && this.state.scenarioId !== 'desert' && this.state.scenarioId !== 'alaska_winter' && loc?.water_source) {
                continue;
            }

            // Scavenging quality hint
            let extraInfo = '';
            if (actionId === 'scavenge' && this.state.scenarioId === 'overgrown_city') {
                const scavengeQuality = loc?.scavenging_quality || 0.3;
                const qualityLabel = scavengeQuality >= 0.7 ? 'Rich' : scavengeQuality >= 0.4 ? 'Moderate' : 'Poor';
                const qualityColor = scavengeQuality >= 0.7 ? '#4caf50' : scavengeQuality >= 0.4 ? '#ff9800' : '#f44336';
                extraInfo = `<span class="fq-action-chance" style="color:${qualityColor}">Scavenging: ${qualityLabel}</span>`;
            }

            html += `
            <div class="fq-action-btn${disabledClass}" data-action="${actionId}">
                <div class="fq-action-top">
                    <span class="fq-action-icon">${action.icon}</span>
                    <span class="fq-action-name">${action.name}</span>
                    <span class="fq-action-hours">⏱ ${hours}h</span>
                </div>
                <span class="fq-action-desc">${action.desc}</span>
                ${reqText}
                ${extraInfo}
            </div>`;
        }

        // Usable item buttons
        if (usableItems.length > 0 && actionsLeft > 0) {
            html += `<div style="grid-column: 1/-1; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 0.5rem; margin-top: 0.3rem;"></div>`;
            for (const item of usableItems) {
                const count = this.state.inventory.filter(i => i === item.id).length;
                const treatedInjury = this.getTreatableInjury(item);
                const treatHint = treatedInjury ? ` → Treats: ${treatedInjury.icon} ${treatedInjury.name}` : '';
                html += `
            <div class="fq-action-btn fq-action-use-item" data-action="use_item" data-item="${item.id}">
                <div class="fq-action-top">
                    <span class="fq-action-icon">${item.icon}</span>
                    <span class="fq-action-name">Use ${item.name}</span>
                    <span class="fq-action-hours">⏱ 1h</span>
                </div>
                <span class="fq-action-desc">${item.desc}${treatHint}${count > 1 ? ` (${count} available)` : ''}</span>
            </div>`;
            }
        }

        // End day early
        const canAffordAny = availableActions.some(aid => {
            const act = allActions[aid];
            return act && this.getActionHours(aid) <= remaining && actionsLeft > 0;
        });

        if (!canAffordAny && usableItems.length === 0) {
            html += `
            <div class="fq-action-btn" data-action="end_day" style="grid-column: 1/-1; border-color: var(--amber); background: rgba(255,193,7,0.1);">
                <div class="fq-action-top">
                    <span class="fq-action-icon">🌙</span>
                    <span class="fq-action-name">End Day Early</span>
                </div>
                <span class="fq-action-desc">Not enough hours for any action. Rest until tomorrow.</span>
            </div>`;
        } else {
            html += `
            <div class="fq-action-btn" data-action="end_day" style="grid-column: 1/-1; opacity: 0.7; border-color: rgba(255,255,255,0.2);">
                <div class="fq-action-top">
                    <span class="fq-action-icon">🌙</span>
                    <span class="fq-action-name">End Day Early</span>
                </div>
                <span class="fq-action-desc">Skip remaining actions and rest until nightfall.</span>
            </div>`;
        }

        // Shelter upgrade hint
        const shelterData = this.scenarioData?.shelter;
        if (shelterData && this.state.shelterLevel < shelterData.length - 1) {
            const nextShelter = shelterData[this.state.shelterLevel + 1];
            html += `<div style="grid-column: 1/-1; text-align: center; color: var(--cream-dim); font-size: 0.8rem; margin-top: 0.3rem;">Next shelter: ${nextShelter.icon} ${nextShelter.name}</div>`;
        }

        actionsContainer.innerHTML = html;
        this.hideAllGamePanels();

        actionsContainer.querySelectorAll('.fq-action-btn:not(.fq-action-disabled)').forEach(btn => {
            btn.addEventListener('click', () => {
                const actionId = btn.dataset.action;
                if (actionId === 'end_day') { this.rollForEvent(); return; }
                if (actionId === 'use_item') {
                    const itemId = btn.dataset.item;
                    if (itemId) { this.handleUseItem(itemId); }
                } else if (actionId === 'craft') {
                    this.craftingMode = true;
                    this.renderChooseActions();
                } else {
                    this.chooseAction(actionId);
                }
            });
        });

        actionsContainer.querySelectorAll('.fq-ls-btn:not([disabled])').forEach(btn => {
            btn.addEventListener('click', () => {
                this.moveToLocation(btn.dataset.loc);
                this.renderChooseActions();
            });
        });
    }

    // ==========================================
    // 17b. RENDER — CRAFTING MENU
    // ==========================================

    renderCraftingMenu() {
        this.renderGameScreen();

        const remaining = this.state.hoursRemaining;
        const actionsLeft = this.state.maxActions - this.state.actionsUsed;
        const recipes = this.config.crafting;
        const available = [];

        for (const [id, recipe] of Object.entries(recipes || {})) {
            const hasReqs = recipe.requires.every(r => this.state.inventory.includes(r));
            const alreadyHave = this.state.inventory.includes(id);
            const isConsumable = recipe.consumable;
            if (hasReqs && (isConsumable || !alreadyHave)) {
                available.push({ id, ...recipe });
            }
        }

        let narrative = `<p>🔨 <strong>Crafting Menu</strong> — Choose an item to craft. (⏱ 2h)</p>`;
        if (available.length === 0) {
            narrative += `<p style="color: var(--danger);">You don't have the materials to craft anything right now.</p>`;
        }

        document.getElementById('fq-narrative').innerHTML = narrative;
        const actionsContainer = document.getElementById('fq-actions');

        let html = `
        <div class="fq-action-btn" data-action="back" style="grid-column: 1/-1; border-color: var(--cream-dim); background: rgba(255,255,255,0.05);">
            <div class="fq-action-top">
                <span class="fq-action-icon">↩️</span>
                <span class="fq-action-name">Back to Actions</span>
            </div>
            <span class="fq-action-desc">Cancel crafting</span>
        </div>`;

        for (const craft of available) {
            const canAffordHours = 2 <= remaining && actionsLeft > 0;
            const disabledClass = canAffordHours ? '' : ' fq-action-disabled';

            const reqsText = craft.requires.length > 0
                ? craft.requires.map(r => {
                    const hasIt = this.state.inventory.includes(r);
                    return `<span style="color: ${hasIt ? 'var(--success)' : 'var(--danger)'}">${r.replace(/_/g, ' ')}</span>`;
                }).join(', ')
                : 'None (built from scratch)';

            const fireReq = craft.requires_fire ? (this.state.hasFire ? '<span style="color:#4caf50;"> 🔥 Fire lit</span>' : '<span style="color:#f44336;"> 🔥 Requires lit fire</span>') : '';
            const fireDisabledClass = (craft.requires_fire && !this.state.hasFire) ? ' fq-action-disabled' : '';

            html += `
            <div class="fq-action-btn${disabledClass}${fireDisabledClass}" data-action="craft" data-item="${craft.id}">
                <div class="fq-action-top">
                    <span class="fq-action-icon">${craft.icon}</span>
                    <span class="fq-action-name">${craft.name}</span>
                    <span class="fq-action-hours">⏱ 2h</span>
                </div>
                <span class="fq-action-desc">${craft.desc}</span>
                <span class="fq-action-requires">Needs: ${reqsText}</span>
                ${fireReq}
            </div>`;
        }

        actionsContainer.innerHTML = html;
        this.hideAllGamePanels();

        actionsContainer.querySelectorAll('.fq-action-btn:not(.fq-action-disabled)').forEach(btn => {
            btn.addEventListener('click', () => {
                const actionId = btn.dataset.action;
                if (actionId === 'back') { this.craftingMode = false; this.renderChooseActions(); return; }
                if (actionId === 'craft') {
                    const craftItemId = btn.dataset.item;
                    this.craftingMode = false;
                    this.chooseAction('craft', craftItemId);
                }
            });
        });
    }

    getTreatableInjury(itemDef) {
        if (!itemDef.treats_injury || !this.state.injuries || this.state.injuries.length === 0) return null;
        const treatable = Array.isArray(itemDef.treats_injury) ? itemDef.treats_injury : [itemDef.treats_injury];
        for (const injuryId of treatable) {
            const injury = this.state.injuries.find(i => i.id === injuryId);
            if (injury) return injury;
        }
        return null;
    }

    renderLocationSelector() {
        const scenario = this.getScenario();
        if (!scenario) return '';
        const knownLocations = this.state.knownLocations || [];
        if (knownLocations.length <= 1) return '';

        const currentLocId = this.state.currentLocation;
        let html = '<div class="fq-location-selector">';
        html += '<span class="fq-ls-label">📍 Move to:</span>';

        for (const locId of knownLocations) {
            const loc = scenario.locations.find(l => l.id === locId);
            if (!loc) continue;
            const isCurrent = locId === currentLocId;
            const disabledAttr = isCurrent ? ' disabled' : '';
            const currentClass = isCurrent ? ' fq-ls-current' : '';
            html += `<button class="fq-ls-btn${currentClass}" data-loc="${locId}"${disabledAttr}>${loc.icon} ${loc.name}</button>`;
        }

        html += '</div>';
        return html;
    }

    // ==========================================
    // 18. RENDER — FORAGING CHALLENGE
    // ==========================================

    renderForagingLoading() {
        this.renderGameScreen();
        document.getElementById('fq-narrative').innerHTML = '<p>🌿 Searching for plants...</p>';
        document.getElementById('fq-actions').innerHTML = '<div class="loading-spinner">Identifying plants</div>';
        this.hideAllGamePanels();
    }

    renderForaging() {
        this.renderGameScreen();
        const data = this.encounterData;
        if (!data) return;

        const loc = this.getLocation();
        const foragingQuality = loc?.foraging_quality || 0.5;

        let narrativeHtml = `<p>${data.encounter_text}</p>`;
        if (foragingQuality >= 0.8) {
            narrativeHtml += `<p><em>This area is rich with plant life.</em></p>`;
        } else if (foragingQuality <= 0.3) {
            narrativeHtml += `<p><em>Plant life is sparse here. You search carefully.</em></p>`;
        }

        // Seasonal hint (Alaska)
        if (this.state.scenarioId === 'alaska_winter') {
            if (this.state.season === 'Winter') {
                narrativeHtml += `<p><em>❄️ Winter has covered the land in snow. Only the hardiest plants can still be found.</em></p>`;
            } else if (this.state.season === 'Spring') {
                narrativeHtml += `<p><em>🌱 New growth is appearing. More plants are becoming available.</em></p>`;
            } else if (this.state.season === 'Autumn') {
                narrativeHtml += `<p><em>🍂 The last harvest before winter. Gather what you can.</em></p>`;
            }
        }

        document.getElementById('fq-narrative').innerHTML = narrativeHtml;

        const plant = data.plant;
        const plantCard = document.getElementById('fq-plant-card');
        plantCard.classList.remove('hidden');

        let clues = `<div><strong>Description:</strong> ${plant.desc_unsafe}</div>`;
        if (plant.category) clues += `<div><strong>Category:</strong> ${plant.category}</div>`;

        plantCard.innerHTML = `
            <div class="fq-plant-card">
                <div class="fq-plant-icon">${plant.icon || '🌿'}</div>
                <div class="fq-plant-name">Unknown Plant</div>
                ${clues ? `<div class="fq-plant-hint">${clues}</div>` : ''}
            </div>
        `;

        document.getElementById('fq-plant-question').textContent = data.question || 'Can you identify this plant?';

        const optionsDiv = document.getElementById('fq-options-grid');
        optionsDiv.innerHTML = data.options.map((opt, i) => `
            <div class="fq-option-btn" data-answer="${opt.name}" data-index="${i}">
                <span class="fq-opt-icon">${opt.icon}</span>
                <span class="fq-opt-name">${opt.name}</span>
            </div>
        `).join('');

        document.getElementById('fq-foraging').classList.remove('hidden');
        document.getElementById('fq-actions').innerHTML = '';
        this.hideAllGamePanels(true);
        document.getElementById('fq-foraging').classList.remove('hidden');
        document.getElementById('fq-forage-result').classList.add('hidden');

        optionsDiv.querySelectorAll('.fq-option-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                optionsDiv.querySelectorAll('.fq-option-btn').forEach(b => b.classList.add('fq-disabled'));
                btn.classList.add(btn.dataset.answer === data.correct_answer ? 'fq-correct' : 'fq-wrong');
                this.handleForagingAnswer(btn.dataset.answer);
            });
        });
    }

    // ==========================================
    // 19. RENDER — FORAGING RESULT
    // ==========================================

    renderForagingResult() {
        this.renderGameScreen();

        const result = this.foragingResult;
        if (!result) return;

        const correct = result.correct;
        const plant = result.plant;
        const consequences = result.consequences;
        const isEdible = plant.is_edible !== undefined ? plant.is_edible : plant.edible;

        // Highlight correct/wrong options
        const optionsDiv = document.getElementById('fq-options-grid');
        if (optionsDiv) {
            optionsDiv.querySelectorAll('.fq-option-btn').forEach(btn => {
                if (btn.dataset.answer === result.correctAnswer) {
                    btn.classList.add('fq-correct');
                } else if (btn.dataset.answer === result.answer && !correct) {
                    btn.classList.add('fq-wrong');
                }
            });
        }

        let html = '';

        if (correct) {
            html += `
            <div class="fq-result-box fq-result-correct">
                <div class="fq-result-icon">✅</div>
                <div class="fq-result-title">Correct Identification!</div>
                <div class="fq-result-text">
                    ${result.resultText || `You correctly identified <span class="fq-result-plant-name">${plant.icon} ${plant.name}</span>.`}
                </div>
                <div class="fq-result-effects">
                    ${this.effectsToBadges(consequences, true)}
                </div>
            </div>`;
        } else {
            const dangerLevel = result.dangerLevel || plant.danger_level || 'POISONOUS';
            const dangerDescriptions = {
                'SAFE': 'This plant is actually safe, but misidentification is still a mistake.',
                'CAUTION': 'This plant requires careful preparation. Eating it raw could cause problems.',
                'POISONOUS': 'This plant is poisonous and can make you seriously ill.',
                'HIGH': 'This plant is highly poisonous. In real life, this could cause permanent damage.',
                'EXTREME': 'This plant is extremely dangerous. In real life, seek immediate medical attention.',
                'DEADLY': 'This plant is DEADLY. In real life, this mistake could be fatal.'
            };

            html += `
            <div class="fq-result-box fq-result-wrong">
                <div class="fq-result-icon">❌</div>
                <div class="fq-result-title">Wrong Identification!</div>
                <div class="fq-result-text">
                    ${result.resultText || `You thought it was <strong>${result.answer}</strong>, but this is actually <span class="fq-result-plant-name">${plant.icon} ${plant.name}</span>.`}
                </div>
                <div class="fq-result-effects">
                    ${this.effectsToBadges(consequences, false)}
                </div>
            </div>`;

            if (dangerDescriptions[dangerLevel]) {
                html += `
                <div class="fq-danger-warning">
                    <strong>⚠️ ${dangerLevel}:</strong> ${dangerDescriptions[dangerLevel]}
                    ${!isEdible && plant.desc_safe ? `<br><em>Real fact: ${plant.desc_safe}</em>` : ''}
                </div>`;
            }
        }

        // Plant detail card
        html += `
        <div class="fq-plant-detail">
            <strong>${plant.icon} ${plant.name}</strong>
            ${plant.latin_name ? ` <em>(${plant.latin_name})</em>` : ''}<br>
            ${isEdible ? '✅ Edible/Safe to use' : '☠️ Not edible / Dangerous'}
            ${plant.category ? ` • ${plant.category}` : ''}
            ${plant.danger_level ? ` • Danger level: <strong style="color: ${this.dangerLevelColor(plant.danger_level)}">${plant.danger_level}</strong>` : ''}
            ${plant.parts && plant.parts.length > 0 ? `<br>Edible parts: ${plant.parts.join(', ')}` : ''}
            ${plant.taste ? `<br>Taste: ${plant.taste}` : ''}
            ${plant.nutrition ? `<br>Nutrition: ${plant.nutrition}` : ''}
        </div>`;

        html += `<button class="btn-primary fq-btn-continue" id="fq-forage-continue">Continue</button>`;

        document.getElementById('fq-forage-result').innerHTML = html;
        document.getElementById('fq-forage-result').classList.remove('hidden');
        document.getElementById('fq-foraging').classList.add('hidden');
        document.getElementById('fq-actions').innerHTML = '';
        document.getElementById('fq-narrative').innerHTML = '';
        document.getElementById('fq-event').classList.add('hidden');
        document.getElementById('fq-action-result').classList.add('hidden');
        document.getElementById('fq-day-end').classList.add('hidden');
        document.getElementById('fq-discovery').classList.add('hidden');

        document.getElementById('fq-forage-continue')?.addEventListener('click', () => {
            this.afterForagingResult();
        });
    }

    // ==========================================
    // 20. RENDER — ACTION RESULT
    // ==========================================

    renderActionResult() {
        this.renderGameScreen();

        const result = this.currentActionResult;
        if (!result) return;

        let html = `
        <div class="fq-action-result-box">
            <div class="fq-action-result-icon">${result.actionIcon}</div>
            <div class="fq-action-result-title">${result.actionName}</div>
            <div class="fq-action-result-text">${result.text}</div>
            ${result.effects && Object.keys(result.effects).length > 0 ? `
                <div class="fq-result-effects">
                    ${this.effectsToBadges(result.effects, result.success !== false)}
                </div>
            ` : ''}
        </div>`;

        if (result.discoveries && result.discoveries.length > 0) {
            const scenario = this.getScenario();
            for (const locId of result.discoveries) {
                const loc = scenario.locations.find(l => l.id === locId);
                if (loc) {
                    html += `
                    <div class="fq-discovery-box">
                        <span class="fq-discovery-icon">${loc.icon}</span>
                        <h3>${loc.name}</h3>
                        <p>${loc.desc}</p>
                    </div>`;
                }
            }
        }

        html += `<button class="btn-primary fq-btn-continue" id="fq-action-continue">Continue</button>`;

        document.getElementById('fq-action-result').innerHTML = html;
        document.getElementById('fq-action-result').classList.remove('hidden');
        document.getElementById('fq-narrative').innerHTML = '';
        document.getElementById('fq-actions').innerHTML = '';
        this.hideAllGamePanels(true);
        document.getElementById('fq-action-result').classList.remove('hidden');

        document.getElementById('fq-action-continue')?.addEventListener('click', () => {
            this.afterActionResult();
        });
    }

    // ==========================================
    // 21. RENDER — EVENT & EVENT RESULT
    // ==========================================

    renderEvent() {
        this.renderGameScreen();

        const event = this.currentEvent;
        if (!event) return;

        const isMythic = event.mythic || false;
        const mythicClass = isMythic ? ' fq-event-mythic' : '';
        const mythicTag = isMythic ? '<span style="color: #90EE90; font-size: 0.75rem; font-weight: normal; margin-left: 0.5rem;">✨ Mythic Event</span>' : '';

        let html = `
        <div class="fq-event-header${mythicClass}">
            <div class="fq-event-icon">${event.icon}</div>
            <div class="fq-event-title">${event.name}${mythicTag}</div>
        </div>
        <div class="fq-event-text">${event.text}</div>
        <div class="fq-event-choices">
            ${event.choices.map((c, i) => `
                <div class="fq-event-choice" data-choice="${i}">
                    <div class="fq-choice-header">
                        <span class="fq-choice-icon">${c.icon}</span>
                        <span class="fq-choice-text">${c.text}</span>
                    </div>
                    ${c.hours > 0 ? `<span class="fq-choice-hours">⏱ ${c.hours}h</span>` : ''}
                    ${c.requires && c.requires.length > 0 ? `<span class="fq-choice-requires">Requires: ${c.requires.join(', ')}</span>` : ''}
                </div>
            `).join('')}
        </div>`;

        document.getElementById('fq-narrative').innerHTML = `<p><strong>⚡ An event occurs!</strong></p>`;
        document.getElementById('fq-event').innerHTML = html;
        document.getElementById('fq-event').classList.remove('hidden');
        document.getElementById('fq-actions').innerHTML = '';
        this.hideAllGamePanels(true);
        document.getElementById('fq-event').classList.remove('hidden');

        if (isMythic) { this.playAnimation('fairy_glow', 3000); }

        document.querySelectorAll('.fq-event-choice').forEach(el => {
            el.addEventListener('click', () => {
                this.resolveEventChoice(parseInt(el.dataset.choice));
            });
        });
    }

    renderEventResult() {
        this.renderGameScreen();

        const result = this.currentEventResult;
        if (!result) return;

        const isSuccess = result.success;
        const cls = isSuccess ? 'fq-result-correct' : 'fq-result-wrong';
        const icon = isSuccess ? '✅' : '❌';

        let html = `
        <div class="fq-result-box ${cls}">
            <div class="fq-result-icon">${icon}</div>
            <div class="fq-result-title">${isSuccess ? 'Success!' : 'Things go wrong...'}</div>
            <div class="fq-result-text">${result.text}</div>
            <div class="fq-result-effects">
                ${this.effectsToBadges(result.effects, isSuccess)}
            </div>
        </div>`;

        html += `<button class="btn-primary fq-btn-continue" id="fq-event-continue">Continue</button>`;

        document.getElementById('fq-event-result').innerHTML = html;
        document.getElementById('fq-event-result').classList.remove('hidden');
        document.getElementById('fq-event').classList.add('hidden');
        document.getElementById('fq-narrative').innerHTML = '';
        document.getElementById('fq-actions').innerHTML = '';
        this.hideAllGamePanels(true);
        document.getElementById('fq-event-result').classList.remove('hidden');

        document.getElementById('fq-event-continue')?.addEventListener('click', () => {
            this.afterEventResult();
        });
    }

    // ==========================================
    // 22. RENDER — DISCOVERY
    // ==========================================

    renderDiscovery() {
        this.renderGameScreen();

        const discovery = this.currentDiscovery;
        if (!discovery) { this.afterActionResult(); return; }

        const scenario = this.getScenario();
        const loc = scenario.locations.find(l => l.id === discovery);

        if (!loc) { this.afterActionResult(); return; }

        document.getElementById('fq-narrative').innerHTML = `<p><strong>📍 New Location Discovered!</strong></p>`;
        document.getElementById('fq-actions').innerHTML = '';

        document.getElementById('fq-discovery').innerHTML = `
            <div class="fq-discovery-box">
                <span class="fq-discovery-icon">${loc.icon}</span>
                <h3>${loc.name}</h3>
                <p>${loc.desc}</p>
                ${loc.water_source ? '<p style="color: #26c6da;">💧 Fresh water source found!</p>' : ''}
                ${loc.signal_bonus ? `<p style="color: #FFC107;">📡 Good position for signalling (+${loc.signal_bonus})</p>` : ''}
                ${loc.shelter_bonus ? '<p style="color: #66BB6A;">🏕️ Natural shelter available</p>' : ''}
                ${loc.foraging_quality >= 0.8 ? '<p style="color: #66BB6A;">🌿 Rich foraging ground</p>' : ''}
            </div>
            <button class="btn-primary fq-btn-continue" id="fq-discovery-continue">Continue</button>
        `;
        document.getElementById('fq-discovery').classList.remove('hidden');
        this.hideAllGamePanels(true);
        document.getElementById('fq-discovery').classList.remove('hidden');

        this.addJournalEntry(`Discovered new location: ${loc.icon} ${loc.name}. ${loc.desc}`);

        document.getElementById('fq-discovery-continue')?.addEventListener('click', () => {
            this.currentDiscovery = null;
            this.afterActionResult();
        });
    }

    // ==========================================
    // 23. RENDER — DAY END
    // ==========================================

    renderDayEnd() {
        this.renderGameScreen();

        const changes = this.dayEndChanges || {};
        const r = this.state.resources;
        const max = this.state.maxResources;

        const labels = {
            health: '❤️ Health', hunger: '🍖 Hunger', warmth: '🔥 Warmth',
            morale: '💭 Morale', water: '💧 Water'
        };

        let changesHtml = '';
        for (const [key, val] of Object.entries(changes)) {
            if (val === 0) continue;
            const label = labels[key] || key;
            const cls = val > 0 ? 'fq-change-positive' : 'fq-change-negative';
            const sign = val > 0 ? '+' : '';
            changesHtml += `<div class="fq-change-item ${cls}">${label}: ${sign}${val}</div>`;
        }

        changesHtml += `
        <div class="fq-change-item fq-change-neutral" style="grid-column: 1/-1; text-align: center; margin-top: 0.5rem;">
            <strong>Current:</strong>
            ❤️ ${Math.round(r.health)}/${max.health}
            🍖 ${Math.round(r.hunger)}/${max.hunger}
            🔥 ${Math.round(r.warmth)}/${max.warmth}
            💭 ${Math.round(r.morale)}/${max.morale}
            ${r.water !== undefined ? ` 💧 ${Math.round(r.water)}/${max.water}` : ''}
        </div>`;

        const todayEntries = this.state.journal.filter(e => e.day === this.state.day);
        const journalText = todayEntries.map(e => e.text).join(' ');

        document.getElementById('fq-day-end-num').textContent = this.state.day;
        document.getElementById('fq-day-end-changes').innerHTML = changesHtml;
        document.getElementById('fq-day-end-journal').innerHTML = journalText || 'A quiet day.';

        document.getElementById('fq-day-end').classList.remove('hidden');
        document.getElementById('fq-narrative').innerHTML = '';
        document.getElementById('fq-actions').innerHTML = '';
        this.hideAllGamePanels(true);
        document.getElementById('fq-day-end').classList.remove('hidden');

        document.getElementById('fq-next-day-btn')?.addEventListener('click', () => {
            this.nextDay();
        });
    }

    // ==========================================
    // 24. RENDER — JOURNAL
    // ==========================================

    renderJournal() {
        if (!this.state) return;

        const statsDiv = document.getElementById('fq-journal-stats');
        const entriesDiv = document.getElementById('fq-journal-entries');
        const plantsDiv = document.getElementById('fq-journal-plants');

        const r = this.state.resources;
        statsDiv.innerHTML = `
            <div class="fq-journal-stat"><span class="fq-js-value">${this.state.day}</span><span class="fq-js-label">Day</span></div>
            <div class="fq-journal-stat"><span class="fq-js-value">${this.state.plantsCorrect}</span><span class="fq-js-label">Plants ID'd</span></div>
            <div class="fq-journal-stat"><span class="fq-js-value">${this.state.knownLocations.length}</span><span class="fq-js-label">Locations</span></div>
            <div class="fq-journal-stat"><span class="fq-js-value">${this.state.shelterLevel}</span><span class="fq-js-label">Shelter</span></div>
            <div class="fq-journal-stat"><span class="fq-js-value">${this.state.injuries?.length || 0}</span><span class="fq-js-label">Injuries</span></div>
            <div class="fq-journal-stat"><span class="fq-js-value">${this.state.achievements?.length || 0}</span><span class="fq-js-label">🏆</span></div>
        `;

        let entriesHtml = '';
        const entries = [...this.state.journal].reverse();
        for (const entry of entries.slice(0, 30)) {
            entriesHtml += `
            <div class="fq-journal-day">
                <div class="fq-journal-day-header">
                    <span class="fq-journal-day-num">Day ${entry.day}</span>
                </div>
                <div class="fq-journal-day-text">${entry.text}</div>
            </div>`;
        }
        entriesDiv.innerHTML = entriesHtml || '<p style="color: var(--cream-dim)">No entries yet.</p>';

        let plantsHtml = '<h4>🌿 Plants Encountered</h4>';
        for (const plant of this.state.plantsSeen) {
            const cls = plant.correct ? 'fq-plant-correct' : 'fq-plant-wrong';
            const icon = plant.correct ? '✅' : '❌';
            plantsHtml += `<span class="fq-plant-seen ${cls}">${icon} ${plant.name}</span>`;
        }

        if (this.state.injuries && this.state.injuries.length > 0) {
            plantsHtml += '<h4 style="margin-top: 1rem;">🩹 Active Injuries</h4><div class="fq-injury-bar">';
            for (const injury of this.state.injuries) {
                const sevClass = `severity-${injury.severity}`;
                plantsHtml += `<span class="fq-injury-tag ${sevClass}">${injury.icon} ${injury.name} <span class="fq-injury-days">(${injury.daysRemaining}d)</span></span>`;
            }
            plantsHtml += '</div>';
        }

        const achDefs = this.config?.achievements || {};
        const earnedAchs = this.state.achievements || [];

        if (earnedAchs.length > 0) {
            plantsHtml += '<h4 style="margin-top: 1rem;">🏆 Achievements Earned</h4><div class="fq-journal-achievements">';
            for (const achId of earnedAchs) {
                const ach = achDefs[achId];
                if (ach) {
                    plantsHtml += `<div class="fq-journal-ach">${ach.icon} <strong>${ach.name}</strong> — ${ach.desc}</div>`;
                }
            }
            plantsHtml += '</div>';
        }

        const lockedAchs = Object.entries(achDefs).filter(([id]) => !earnedAchs.includes(id));
        if (lockedAchs.length > 0) {
            plantsHtml += '<h4 style="margin-top: 1rem;">🔒 Locked Achievements</h4><div class="fq-journal-achievements fq-locked-achievements">';
            for (const [id, ach] of lockedAchs) {
                plantsHtml += `<div class="fq-journal-ach fq-ach-locked">${ach.icon} <em>???</em> — <span style="color: var(--cream-dim)">${ach.desc}</span></div>`;
            }
            plantsHtml += '</div>';
        }

        plantsDiv.innerHTML = plantsHtml;
    }

    // ==========================================
    // ATMOSPHERIC ANIMATIONS
    // ==========================================

    renderAtmosphere() {
        const existing = document.getElementById('fq-atmosphere');
        if (existing) existing.remove();

        const container = document.createElement('div');
        container.id = 'fq-atmosphere';
        container.className = 'fq-atmosphere';

        const scenarioId = this.state.scenarioId;
        const weatherType = this.state.weather?.type;

        if (scenarioId === 'alaska_winter') {
            if (weatherType === 'blizzard') {
                container.innerHTML = this.getBlizzardParticles();
                container.className += ' fq-atmo-blizzard';
            } else if (weatherType === 'snow') {
                container.innerHTML = this.getSnowParticles();
                container.className += ' fq-atmo-snow';
            } else if (weatherType === 'clear' && (this.state.season === 'Autumn' || this.state.season === 'Winter')) {
                container.innerHTML = this.getAuroraHTML();
                container.className += ' fq-atmo-aurora';
            } else if (weatherType === 'freezing_rain') {
                container.innerHTML = this.getRainParticles('freezing');
                container.className += ' fq-atmo-freezing-rain';
            }
        }

        if (scenarioId === 'desert') {
            if (weatherType === 'clear' && this.state.season === 'Summer') {
                container.innerHTML = this.getHeatHazeHTML();
                container.className += ' fq-atmo-heat';
            } else if (weatherType === 'cloudy' || weatherType === 'wind') {
                container.innerHTML = this.getSandParticles();
                container.className += ' fq-atmo-sand';
            }
        }

        if (scenarioId === 'wild_forest') {
            if (weatherType === 'rain' || weatherType === 'freezing_rain') {
                container.innerHTML = this.getRainParticles('normal');
                container.className += ' fq-atmo-rain';
            } else if (weatherType === 'cloudy') {
                container.innerHTML = this.getMistHTML();
                container.className += ' fq-atmo-mist';
            }
        }

        const gameScreen = document.querySelector('.fq-game-screen') || document.getElementById('fq-game-screen');
        if (gameScreen) {
            gameScreen.style.position = 'relative';
            gameScreen.insertBefore(container, gameScreen.firstChild);
        }
    }

    getAuroraHTML() {
        return `<div class="fq-aurora"><div class="fq-aurora-band fq-aurora-1"></div><div class="fq-aurora-band fq-aurora-2"></div><div class="fq-aurora-band fq-aurora-3"></div></div>`;
    }

    getBlizzardParticles() {
        let particles = '';
        for (let i = 0; i < 60; i++) {
            const left = Math.random() * 100;
            const delay = Math.random() * 3;
            const duration = 1 + Math.random() * 2;
            const size = 2 + Math.random() * 4;
            particles += `<div class="fq-snow-particle fq-blizzard-particle" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;width:${size}px;height:${size}px;"></div>`;
        }
        return `<div class="fq-particle-container">${particles}</div>`;
    }

    getSnowParticles() {
        let particles = '';
        for (let i = 0; i < 30; i++) {
            const left = Math.random() * 100;
            const delay = Math.random() * 5;
            const duration = 3 + Math.random() * 4;
            const size = 2 + Math.random() * 3;
            particles += `<div class="fq-snow-particle" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;width:${size}px;height:${size}px;"></div>`;
        }
        return `<div class="fq-particle-container">${particles}</div>`;
    }

    getRainParticles(type) {
        let particles = '';
        const count = type === 'freezing' ? 40 : 35;
        for (let i = 0; i < count; i++) {
            const left = Math.random() * 100;
            const delay = Math.random() * 2;
            const duration = 0.3 + Math.random() * 0.5;
            const height = 8 + Math.random() * 15;
            particles += `<div class="fq-rain-drop${type === 'freezing' ? ' fq-freezing-drop' : ''}" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;height:${height}px;"></div>`;
        }
        return `<div class="fq-particle-container">${particles}</div>`;
    }

    getHeatHazeHTML() {
        return `<div class="fq-heat-haze"></div>`;
    }

    getSandParticles() {
        let particles = '';
        for (let i = 0; i < 25; i++) {
            const top = Math.random() * 100;
            const delay = Math.random() * 4;
            const duration = 2 + Math.random() * 3;
            const size = 1 + Math.random() * 2;
            particles += `<div class="fq-sand-particle" style="top:${top}%;animation-delay:${delay}s;animation-duration:${duration}s;width:${size}px;height:${size}px;"></div>`;
        }
        return `<div class="fq-particle-container">${particles}</div>`;
    }

    getMistHTML() {
        return `<div class="fq-mist"><div class="fq-mist-layer fq-mist-1"></div><div class="fq-mist-layer fq-mist-2"></div></div>`;
    }

    clearAtmosphere() {
        const container = document.getElementById('fq-atmosphere');
        if (container) container.remove();
    }

    // ==========================================
    // 25. RENDER — GAME OVER
    // ==========================================

    renderGameOver() {
        this.showScreen('gameover');

        const ending = this.currentEnding;
        if (!ending) return;

        const isGood = ending.type === 'good' || ending.type === 'mythic';
        const isMythic = ending.type === 'mythic';
        const boxClass = isMythic ? 'fq-ending-mythic' : (isGood ? 'fq-ending-good' : 'fq-ending-bad');

        let statsHtml = `
            <div class="fq-gameover-stat"><span class="fq-gs-value">${this.state.day}</span><span class="fq-gs-label">Days Survived</span></div>
            <div class="fq-gameover-stat"><span class="fq-gs-value">${this.state.plantsCorrect}</span><span class="fq-gs-label">Plants ID'd</span></div>
            <div class="fq-gameover-stat"><span class="fq-gs-value">${this.state.knownLocations.length}</span><span class="fq-gs-label">Locations</span></div>
            <div class="fq-gameover-stat"><span class="fq-gs-value">${this.state.shelterLevel}</span><span class="fq-gs-label">Shelter</span></div>
        `;

        document.getElementById('fq-gameover-box').className = `fq-gameover-box ${boxClass}`;
        const survivalStory = this.generateSurvivalStory();

        document.getElementById('fq-gameover-box').innerHTML = `
            <div class="fq-gameover-icon">${ending.icon}</div>
            <div class="fq-gameover-title">${ending.name}</div>
            <div class="fq-gameover-text">${ending.text}</div>
            <div class="fq-gameover-summary">${ending.summary}</div>
            <div class="fq-gameover-story">${survivalStory}</div>
            <div class="fq-gameover-stats">${statsHtml}</div>
            <div class="fq-gameover-actions">
                <button class="btn-primary" id="fq-restart">🔄 Play Again</button>
                <button class="btn-danger" id="fq-quit">🏠 Main Menu</button>
            </div>
        `;

        document.getElementById('fq-restart')?.addEventListener('click', () => {
            this.selectScenario(this.state.scenarioId);
        });

        document.getElementById('fq-quit')?.addEventListener('click', () => {
            this.state = null;
            this.renderScenarioSelect();
        });
    }

    // ==========================================
    // 25b. SURVIVAL STORY GENERATOR
    // ==========================================

    generateSurvivalStory() {
        const s = this.state;
        const scenario = this.getScenario();
        const ending = this.currentEnding;
        if (!s || !scenario) return '';

        const day = s.day;
        const daysSurvived = s.daysSurvived || day;
        const isGood = ending && (ending.type === 'good' || ending.type === 'mythic');
        const isDead = ending && ending.type === 'bad';

        const openings = {
            'alaska_winter': `The Cessna went down on day one. The pilot vanished into the white. The cold moved in like something alive, and you were alone — truly, completely alone — in the Alaskan wilderness.`,
            'wild_forest': `You stepped off the path to photograph a butterfly. An orange one, with spots on its wings. When you looked up, the path was gone. The forest had swallowed you whole.`,
            'desert': `The tour bus died with a shudder somewhere between Albuquerque and nowhere. The driver went for help and never came back. You had half a litre of warm water and the growing realisation that no one was coming.`
        };

        let story = openings[s.scenarioId] || `You found yourself stranded, alone, with nothing but your wits and the clothes on your back.`;

        // Early actions
        const firstActions = s.actionLog?.slice(0, 3) || [];
        if (firstActions.length > 0) {
            const actionNames = firstActions.map(a => a.actionName?.toLowerCase() || 'something');
            if (actionNames.length === 1) { story += ` Your first instinct was to ${actionNames[0]}.`; }
            else if (actionNames.length === 2) { story += ` You started by ${actionNames[0]} and then ${actionNames[1]}.`; }
            else { story += ` You spent those first desperate hours ${actionNames[0]}, ${actionNames[1]}, and ${actionNames[2]}.`; }
        }

        // Weather & Seasons
        const weathers = [...new Set((s.journal || []).filter(e => e.text?.includes('Weather:')).map(e => {
            const match = e.text.match(/Weather:\s*(.+)/);
            return match ? match[1].trim() : null;
        }).filter(Boolean))];

        if (weathers.length > 0) {
            const weatherLines = {
                '☀️ Clear': 'clear skies that offered no warmth', '☀️ Hot': 'blistering heat that drained the strength from you',
                '🌧️ Rain': 'rain that soaked through everything', '⛈️ Storm': 'storms that raged without mercy',
                '🌨️ Snow': 'snowfall that buried the world in white silence', '❄️ Blizzard': 'a blizzard that nearly ended everything',
                '🌧️ Freezing rain': 'freezing rain that turned the ground to ice', '🌫️ Fog': 'fog so thick you could barely see your own hands',
                '🔥 Scorching': 'scorching heat that made the air shimmer and burn', '💨 Windy': 'winds that whipped sand and stole your warmth',
                '🏜️ Sandstorm': 'sandstorms that blotted out the sky', '🌙 Cool night': 'nights so cold your breath hung in the air',
                '☁️ Cloudy': 'grey skies that pressed down like a lid', '☁️ Overcast': 'grey skies that never seemed to break'
            };
            const described = weathers.map(w => weatherLines[w] || w);
            if (described.length === 1) { story += ` You endured ${described[0]}.`; }
            else { story += ` You endured ${described.slice(0, -1).join(', ')} and ${described[described.length - 1]}.`; }
        }

        // Locations
        const locNames = (s.knownLocations || []).map(id => {
            const loc = scenario.locations?.find(l => l.id === id);
            return loc ? `${loc.icon} ${loc.name}` : null;
        }).filter(Boolean);

        if (locNames.length > 1) { story += ` Over time, you discovered ${locNames.length} locations: ${locNames.slice(0, -1).join(', ')} and ${locNames[locNames.length - 1]}.`; }
        else if (locNames.length === 1) { story += ` You never strayed far from ${locNames[0]}.`; }

        // Foraging
        const plantsCorrect = s.plantsCorrect || 0;
        const plantsWrong = s.plantsWrong || 0;
        const totalPlants = plantsCorrect + plantsWrong;

        if (totalPlants > 0) {
            const plantNames = (s.plantsSeen || []).map(p => p.name);
            const uniquePlants = [...new Set(plantNames)];

            if (plantsWrong === 0) { story += ` Every plant you identified was correct${totalPlants > 3 ? ' — a remarkable display of botanical knowledge' : ''}.`; }
            else if (plantsCorrect > plantsWrong) { story += ` You identified ${plantsCorrect} of ${totalPlants} plants correctly, though ${plantsWrong} mistake${plantsWrong > 1 ? 's' : ''} ${plantsWrong > 1 ? 'cost' : 'cost'} you dearly.`; }
            else if (plantsCorrect > 0) { story += ` The plants were treacherous. You only identified ${plantsCorrect} correctly out of ${totalPlants} attempts.`; }
            else { story += ` You couldn't identify a single plant correctly. The foraging was a constant gamble between nourishment and poison.`; }

            if (uniquePlants.length > 0 && uniquePlants.length <= 5) { story += ` You encountered ${uniquePlants.join(', ')}.`; }
            else if (uniquePlants.length > 5) { story += ` You encountered ${uniquePlants.slice(0, 4).join(', ')} and ${uniquePlants.length - 4} others.`; }
        }

        // Injuries
        if (s.injuries && s.injuries.length > 0) {
            const injuryNames = s.injuries.map(i => `${i.icon} ${i.name}`);
            if (injuryNames.length === 1) { story += ` You suffered ${injuryNames[0]} that made survival even harder.`; }
            else { story += ` You battled ${injuryNames.join(' and ')}.`; }
        }

        // Shelter
        const shelterData = scenario.shelter;
        if (shelterData && s.shelterLevel > 0) {
            const shelter = shelterData[Math.min(s.shelterLevel, shelterData.length - 1)];
            if (shelter) { story += ` You built ${shelter.name || 'a shelter'} to protect yourself from the elements.`; }
        }

        // Key events from journal
        const eventJournal = (s.journal || []).filter(e =>
            e.text?.includes('🚁') || e.text?.includes('🐺') || e.text?.includes('🐻') ||
            e.text?.includes('🦊') || e.text?.includes('🦅') || e.text?.includes('✈️') ||
            e.text?.includes('🧊') || e.text?.includes('🔥') || e.text?.includes('🌪️') ||
            e.text?.includes('🌙') || e.text?.includes('🦌') || e.text?.includes('💀') ||
            e.text?.includes('🦂') || e.text?.includes('💧') ||
            e.text?.includes('🌿') || e.text?.includes('🍄') ||
            e.text?.includes('⚠️') || e.text?.includes('🥵') ||
            e.text?.includes('🪵') || e.text?.includes('✨')
        );

        if (eventJournal.length > 0) {
            const eventShort = eventJournal.slice(0, 3).map(e => {
                let t = e.text.replace(/^Day \d+:\s*/, '');
                if (t.length > 60) t = t.substring(0, 57) + '...';
                return t;
            });

            if (eventShort.length === 1) { story += ` ${eventShort[0]}`; }
            else if (eventShort.length === 2) { story += ` ${eventShort[0]} Then, ${eventShort[1].toLowerCase()}`; }
            else { story += ` ${eventShort[0]} Later, ${eventShort[1].toLowerCase()} And then, ${eventShort[2].toLowerCase()}`; }
        }

        // Crafting
        const crafted = s.itemsCrafted || [];
        if (crafted.length > 0) {
            const craftNames = crafted.map(id => {
                const def = this.config?.crafting?.[id];
                return def ? `${def.icon} ${def.name}` : id.replace(/_/g, ' ');
            });
            if (crafted.length === 1) { story += ` You crafted ${craftNames[0]} from what you could find.`; }
            else if (crafted.length <= 3) { story += ` You crafted ${craftNames.join(' and ')}.`; }
            else { story += ` You crafted ${craftNames.slice(0, 2).join(', ')}, ${craftNames[2]} and ${crafted.length - 3} other tool${crafted.length - 3 > 1 ? 's' : ''}.`; }
        }

        // Karma (Forest only)
        if (s.scenarioId === 'wild_forest' && s.forestKarma !== undefined) {
            if (s.forestKarma >= 80) { story += ` The forest seemed to welcome you, as if the trees themselves were guiding your path. You heard things in the night — whispers, laughter, music that had no source. Whether they were real or not, they kept you company.`; }
            else if (s.forestKarma >= 50) { story += ` The forest watched you, neither friend nor foe, waiting to see what you would become. Some nights you heard things that couldn't be explained. Whether they were helping you or testing you, you never knew.`; }
            else if (s.forestKarma >= 25) { story += ` The forest grew cold towards you. You could feel its distrust in every shadow. Paths seemed to loop back on themselves. The mushrooms you found were always the wrong kind.`; }
            else { story += ` The forest hated you. Eyes watched from every shadow, and every path led you astray. You heard things in the dark that weren't animal sounds. The trees seemed closer in the morning than they'd been at night.`; }
        }

        // Wolf stalking (Alaska)
        if (s.scenarioId === 'alaska_winter' && s.wolfStalking) {
            story += ` The wolf tracked you for days. You could feel its eyes on you in the twilight, hear its howl when the wind died. It had decided you were prey.`;
        }

        // Hallucinations (Desert)
        if (s.scenarioId === 'desert' && s.hallucinationCount > 0) {
            if (s.hallucinationCount === 1) { story += ` The desert played tricks on your mind. You saw things that weren't there — just once, but it was enough to make you question everything.`; }
            else { story += ` The desert broke something in your mind. You saw people who weren't there, water that evaporated when you reached for it, buses that dissolved into heat haze. Reality became negotiable.`; }
        }

        // Watcher (Forest)
        if (s.scenarioId === 'wild_forest' && s.watcherPhase >= 2) {
            const karma = s.forestKarma || 50;
            if (karma >= 70) { story += ` Something in the forest was watching over you. Not menacingly — protectively. Like a guardian you couldn't see but could always feel.`; }
            else if (karma <= 30) { story += ` Something in the forest was watching you. Not protectively — hungrily. Like a predator waiting for you to stumble.`; }
            else { story += ` Something in the forest was watching you. You never knew whether it wanted to help or hurt you. Maybe it was waiting to decide.`; }
        }

        // Grove (Forest)
        if (s.scenarioId === 'wild_forest' && s.groveDaysConsecutive >= 3) {
            story += ` The mushroom grove nearly claimed you. Its pull was almost irresistible — the abundance, the warmth, the sense that you belonged there.`;
        }

        // Mythic events (Forest)
        if (s.scenarioId === 'wild_forest' && s.mythicEventsCompleted && s.mythicEventsCompleted.length > 0) {
            const mythCount = s.mythicEventsCompleted.length;
            if (mythCount === 1) { story += ` Something strange happened in those woods — something you still can't explain. The forest has its own rules, and you brushed against one of them.`; }
            else { story += ` The forest showed you things that shouldn't exist. Lights that moved on their own, voices in the dark, paths that appeared from nowhere. You stopped questioning whether they were real. In the forest, real is whatever the trees decide.`; }
        }

        // Ending
        if (isDead) {
            const deathPhrases = {
                'dehydration': `You died of dehydration. The desert, the cold, the wilderness — they don't care about your plans or your hopes. They simply take, and take, until there's nothing left.`,
                'cold': `You froze. The cold crept in slowly, then all at once. One moment you were shivering, the next you simply... stopped.`,
                'starvation': `You starved. Day by day, your body consumed itself. The wilderness is full of food if you know where to look — but you didn't find enough.`,
                'infection': `The infection spread through your body like poison. Without antibiotics, it was only a matter of time.`,
                'health': `Your body gave out. The wilderness is patient — it has all the time in the world. You did not.`,
                'heat': `The heat overwhelmed you. Your vision blurred, your legs gave way. The last thing you felt was the scorching ground beneath you.`
            };
            story += ` ${deathPhrases[s.causeOfDeath] || deathPhrases['health']}`;
        } else if (isGood) {
            const goodEndings = {
                'rescued': `Against all odds, you were rescued. As the helicopter lifted you away, you looked down at the wilderness that had tested every fibre of your being — and you had passed.`,
                'rescued_desert': `Against all odds, a rescue vehicle found you. As they handed you cold water, you vowed never to take a single drop for granted again.`,
                'found_road': `After ${daysSurvived} days, you stumbled onto a road. Civilisation. A passing vehicle stopped. The driver couldn't believe anyone had survived out there.`,
                'explored_out': `You walked out on your own terms. ${daysSurvived} days of survival, and you found your own way back.`,
                'survived_7': `Seven days. You survived seven days in the wild. Most people wouldn't last one.`,
                'survived_14': `Fourteen days. Two weeks of survival. You proved that with knowledge and will, the human spirit can endure almost anything.`,
                'survived_10': `Ten days in the forest. You came out changed — not defeated, but transformed. The trees would remember you.`,
                'forest_adoption': `The forest didn't let you leave. You didn't want to go. The search helicopter passed overhead, and you simply... didn't look up. The trees were home now. The butterfly landed on your arm and you understood — you are the green man. You are the woods.`
            };
            const endingText = goodEndings[ending?.id] || goodEndings['rescued'] || `You survived. After ${daysSurvived} days, you made it out.`;
            story += ` ${endingText}`;
        } else {
            story += ` After ${daysSurvived} days, your story came to an end.`;
        }

        story += ` ${daysSurvived} day${daysSurvived !== 1 ? 's' : ''}. ${plantsCorrect} plant${plantsCorrect !== 1 ? 's' : ''} identified. ${(s.knownLocations?.length || 0)} location${(s.knownLocations?.length || 0) !== 1 ? 's' : ''} discovered. ${(s.shelterLevel || 0)} shelter improvement${(s.shelterLevel || 0) !== 1 ? 's' : ''}.`;

        return story;
    }

    // ==========================================
    // UTILITY — HIDE ALL GAME PANELS
    // ==========================================

    hideAllGamePanels(keepVisible = false) {
        const panels = [
            'fq-foraging', 'fq-event', 'fq-event-result',
            'fq-action-result', 'fq-day-end', 'fq-discovery', 'fq-forage-result'
        ];
        panels.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden');
        });
    }

    // ==========================================
    // MAIN RENDER DISPATCH
    // ==========================================

    render() {
        if (!this.state) {
            this.renderScenarioSelect();
            return;
        }

        switch (this.state.state) {
            case 'scenario_select': this.renderScenarioSelect(); break;
            case 'intro': this.renderIntro(); break;
            case 'day_start': this.renderDayStart(); break;
            case 'choose_actions': this.renderChooseActions(); break;
            case 'foraging': this.renderForaging(); break;
            case 'foraging_result': this.renderForagingResult(); break;
            case 'action_resolve': this.renderActionResult(); break;
            case 'event': this.renderEvent(); break;
            case 'event_result': this.renderEventResult(); break;
            case 'discovery': this.renderDiscovery(); break;
            case 'day_end': this.renderDayEnd(); break;
            case 'game_over': this.renderGameOver(); break;
            default: this.renderChooseActions();
        }
    }

    // ==========================================
    // COMPLETE GAME RESET
    // ==========================================

    resetGame() {
        if (this.state) {
            this.deleteSaveGame(this.state.scenarioId);
        }
        this.state = null;
        this.scenarioData = null;
        this.encounterData = null;
        this.currentEvent = null;
        this.currentEventResult = null;
        this.currentActionResult = null;
        this.foragingResult = null;
        this.currentEnding = null;
        this.dayEndChanges = null;
        this.currentDiscovery = null;
        this.renderScenarioSelect();
    }

    // ==========================================
    // 28. DEBUG HELPERS
    // ==========================================

    debugSetResources(health, hunger, warmth, morale, water) {
        if (!this.state) return;
        this.state.resources.health = health || 100;
        this.state.resources.hunger = hunger || 100;
        this.state.resources.warmth = warmth || 100;
        this.state.resources.morale = morale || 100;
        if (water !== undefined) this.state.resources.water = water;
        this.clampResources();
        this.render();
    }

    debugAdvanceDay(days) {
        if (!this.state) return;
        for (let i = 0; i < (days || 1); i++) {
            this.endDay();
            if (this.state.resources.health <= 0) break;
        }
    }

    debugUnlockAllLocations() {
        if (!this.state) return;
        const scenario = this.getScenario();
        this.state.knownLocations = scenario.locations.map(l => l.id);
        this.render();
        this.showToast('All locations unlocked!', 'success');
    }

    debugMaxShelter() {
        if (!this.state) return;
        const shelterData = this.scenarioData?.shelter;
        this.state.shelterLevel = shelterData ? shelterData.length - 1 : 3;
        this.render();
        this.showToast('Shelter maxed!', 'success');
    }
}

// ==========================================
// 29. INITIALISATION ON PAGE LOAD
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const game = new ForagingQuestGame();
    window.fqGame = game;

    window.fqDebug = {
        setResources: (h, hu, w, m, wa) => game.debugSetResources(h, hu, w, m, wa),
        advanceDay: (d) => game.debugAdvanceDay(d),
        unlockLocations: () => game.debugUnlockAllLocations(),
        maxShelter: () => game.debugMaxShelter(),
    };

    game.init();
});
