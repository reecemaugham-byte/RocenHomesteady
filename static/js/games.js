/* ═══════════════════════════════════════════════════════════════
   ROCEN HOMESTEADY — GAMES PAGE JAVASCRIPT
   Foraging Quest · Survival School · Daily Quiz
   ═══════════════════════════════════════════════════════════════

   TABLE OF CONTENTS
   ─────────────────
   1.  UTILITIES
       1a. Tab Switching
       1b. Toast Notifications
       1c. Local Storage
       1d. Markdown Renderer
       1e. Shared DOM Helpers
   2.  FORAGING QUEST
       2a. Defaults & State
       2b. Initialisation & Persistence
       2c. Season Management
       2d. Stats
       2e. Question Handling
       2f. Answer Handling
       2g. Bonus Round
       2h. Game Over & Restart
       2i. Achievements
   3.  SURVIVAL SCHOOL
       3a. Defaults & State
       3b. Initialisation & Persistence
       3c. UI Updates
       3d. Case Handling
       3e. Answer Handling
       3f. Result Rendering
       3g. Game Flow
       3h. Achievements
   4.  DAILY QUIZ
       4a. Defaults & State
       4b. Initialisation & Persistence
       4c. Game Lifecycle
       4d. UI Updates
       4e. Question Handling
       4f. Answer Handling
       4g. End States
       4h. Restart
       4i. Achievements
   5.  BOOTSTRAP
   ═══════════════════════════════════════════════════════════════ */


/* ───────────────────────────────────────────────────────────────
   1. UTILITIES
   ─────────────────────────────────────────────────────────────── */

/* 1a. Tab Switching ─────────────────────────────────────────── */

function switchTab(tabId) {
    // Hide all containers & deactivate all tab buttons
    document.querySelectorAll('.game-container').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

    // Activate selected
    const container = document.getElementById(tabId);
    if (container) container.classList.add('active');

    const btn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
    if (btn) btn.classList.add('active');

    // Lazy-init: fetch first question if game hasn't started
    if (tabId === 'foraging-quest' && foragingQuest.state.currentQuestion === null) {
        foragingQuest.fetchQuestion();
    }
    if (tabId === 'survival-school' && survivalSchool.state.currentCase === null) {
        survivalSchool.fetchCase();
    }
}

/* 1b. Toast Notifications ────────────────────────────────────── */

function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), duration);
}

/* 1c. Local Storage ─────────────────────────────────────────── */

function saveState(key, data) {
    try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) { /* quota exceeded */ }
}

function loadState(key, defaults) {
    try {
        const saved = localStorage.getItem(key);
        if (saved) return { ...defaults, ...JSON.parse(saved) };
    } catch (e) { /* corrupt data — fall through to defaults */ }
    return { ...defaults };
}

function resetAllGames() {
    if (!confirm('Reset all game progress? This cannot be undone.')) return;
    localStorage.removeItem('fq_state');
    localStorage.removeItem('ss_state');
    localStorage.removeItem('dq_state');
    location.reload();
}

/* 1d. Markdown Renderer ─────────────────────────────────────── */

function renderMarkdown(text) {
    if (!text) return '';
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

/* 1e. Shared DOM Helpers ────────────────────────────────────── */

/** Disable all answer buttons on the page. */
function disableAllAnswerButtons() {
    document.querySelectorAll('.answer-btn').forEach(b => {
        b.disabled = true;
        b.style.pointerEvents = 'none';
    });
}

/** Highlight the button whose encoded onclick value matches `correctAnswer`. */
function highlightCorrectAnswer(correctAnswer) {
    document.querySelectorAll('.answer-btn').forEach(b => {
        try {
            const onclickAttr = b.getAttribute('onclick');
            const match = onclickAttr.match(/'([^']+)'/);
            if (match && decodeURIComponent(match[1]) === correctAnswer) {
                b.classList.add('correct');
            }
        } catch (e) { /* ignore */ }
    });
}


/* ───────────────────────────────────────────────────────────────
   2. FORAGING QUEST
   ─────────────────────────────────────────────────────────────── */

/* 2a. Defaults & State ───────────────────────────────────────── */

const foragingQuest = {

    HABITAT_ICONS: {
        'Woodlands':       '🌲',
        'Meadows':         '🌾',
        'Coastal cliffs':  '🏖️',
        'Riverbanks':      '🏞️',
        'Hedgerows':       '🌿',
        'Marshes':         '🐸',
        'Moors':           '🏔️',
        'Gardens':         '🌻',
        'Wasteland':       '🏚️',
        'Various':         '🌍'
    },

    defaults: {
        score: 0,
        lives: 3,
        streak: 0,
        season: null,           // set from DEFAULT_SEASON on init
        bonusRound: false,
        currentQuestion: null,
        herbarium: {},
        seasonBadges: [],
        totalPlantsIdentified: 0,
        achievements: {
            foraging_novice: false,
            foraging_botanist: false,
            foraging_master: false
        }
    },

    state: null,

/* 2b. Initialisation & Persistence ───────────────────────────── */

    init() {
        this.defaults.season = DEFAULT_SEASON;
        this.state = loadState('fq_state', this.defaults);

        // Ensure achievement keys exist even if saved state is missing them
        for (const key of ['foraging_novice', 'foraging_botanist', 'foraging_master']) {
            if (!(key in this.state.achievements)) {
                this.state.achievements[key] = false;
            }
        }

        this.renderSeasonButtons();
        this.updateStats();
        this.renderAchievements();

        // Resume the correct view based on current state
        if (this.state.lives <= 0) {
            this.showGameOver();
        } else if (this.state.bonusRound) {
            this.fetchBonusQuestion();
        } else if (this.state.currentQuestion === null) {
            this.fetchQuestion();
        } else {
            this.renderQuestion(this.state.currentQuestion);
        }
    },

    save() {
        saveState('fq_state', this.state);
    },

/* 2c. Season Management ──────────────────────────────────────── */

    renderSeasonButtons() {
        const container = document.getElementById('fq-season-buttons');
        const seasons = ['Spring', 'Summer', 'Autumn', 'Winter'];

        let html = '';
        for (const s of seasons) {
            const icon   = SEASON_ICONS[s] || '🌸';
            const badge  = this.state.seasonBadges.includes(s) ? ' 🏅' : '';
            const active  = this.state.season === s ? ' active' : '';
            html += `<button class="season-btn${active}" onclick="foragingQuest.changeSeason('${s}')">${icon} ${s}${badge}</button>`;
        }
        container.innerHTML = html;

        // Update season display
        const display = document.getElementById('fq-season-display');
        const icon = SEASON_ICONS[this.state.season] || '🌸';
        display.innerHTML = `<span>${icon} Active Season: ${this.state.season}</span>`;
    },

    changeSeason(season) {
        this.state.season = season;
        this.state.currentQuestion = null;
        this.state.bonusRound = false;
        this.save();
        this.renderSeasonButtons();
        this.fetchQuestion();
    },

/* 2d. Stats ──────────────────────────────────────────────────── */

    updateStats() {
        const totalFound = Object.keys(this.state.herbarium).length;
        const hearts = '❤️'.repeat(Math.max(0, this.state.lives));
        const fires  = '🔥'.repeat(Math.min(this.state.streak, 5));

        document.getElementById('fq-stats').innerHTML = `
            <div class="stat-box score">
                <div class="stat-label">SCORE</div>
                <div class="stat-value">${this.state.score}</div>
            </div>
            <div class="stat-box lives">
                <div class="stat-label">LIVES</div>
                <div class="stat-value">${hearts || '💔'}</div>
            </div>
            <div class="stat-box streak">
                <div class="stat-label">STREAK</div>
                <div class="stat-value">${fires} ${this.state.streak}</div>
            </div>
            <div class="stat-box herbarium">
                <div class="stat-label">HERBARIUM</div>
                <div class="stat-value">${totalFound}/${EDIBLE_COUNT}</div>
            </div>
        `;
    },

/* 2e. Question Handling ──────────────────────────────────────── */

    async fetchQuestion() {
        const content = document.getElementById('fq-content');
        content.innerHTML = '<div class="loading-spinner">🌿 Loading...</div>';

        try {
            const resp = await fetch(
                `/api/games/foraging-quest/question?season=${encodeURIComponent(this.state.season)}`
            );
            const q = await resp.json();
            this.state.currentQuestion = q;
            this.save();
            this.renderQuestion(q);
        } catch (e) {
            content.innerHTML = `
                <p>Could not load question.
                   <button class="btn-secondary" onclick="foragingQuest.fetchQuestion()">Try again</button>
                </p>`;
        }
    },

    async fetchBonusQuestion() {
        const content = document.getElementById('fq-content');
        content.innerHTML = '<div class="loading-spinner">⚡ Bonus Round!</div>';

        try {
            const resp = await fetch(
                `/api/games/foraging-quest/bonus?season=${encodeURIComponent(this.state.season)}`
            );
            const q = await resp.json();
            this.state.currentQuestion = q;
            this.save();
            this.renderBonusQuestion(q);
        } catch (e) {
            // Fall back to a normal question on error
            this.state.bonusRound = false;
            this.save();
            this.fetchQuestion();
        }
    },

    renderQuestion(q) {
        const content = document.getElementById('fq-content');
        document.getElementById('fq-game-over').classList.add('hidden');

        const isPoisonous = q.type === 'lookalike';
        const cardBorder  = isPoisonous ? 'var(--danger)' : 'var(--green-leaf)';
        const plant       = q.plant;

        // Plant identification keys
        let keysHtml = '';
        if (plant.id_keys && Object.keys(plant.id_keys).length > 0) {
            const entries = Object.entries(plant.id_keys).slice(0, 3);
            keysHtml = entries.map(([k, v]) => `<b>${k}:</b> ${v}`).join('<br>');
        } else if (plant.description) {
            keysHtml = `<i>${plant.description.substring(0, 150)}</i>`;
        }

        // Build answer options
        let optionsHtml = '';
        if (q.options) {
            q.options.forEach((opt) => {
                const label = (q.type === 'habitat')
                    ? `${this.HABITAT_ICONS[opt] || '❓'} ${opt}`
                    : opt;
                optionsHtml += `<button class="answer-btn" onclick="foragingQuest.handleAnswer('${encodeURIComponent(opt)}', this)">${label}</button>`;
            });
        }

        content.innerHTML = `
            <div class="q-type-header" style="border-left-color: ${q.type_color};">
                <div class="q-type-left">
                    <span class="q-type-icon">${q.type_icon}</span>
                    <span class="q-type-name" style="color: ${q.type_color};">${q.type_name}</span>
                </div>
                <span class="q-points" style="background: ${q.type_color}20; color: ${q.type_color}; border-color: ${q.type_color}50;">+${q.points} XP</span>
            </div>

            <div class="question-layout">
                <div>
                    <div class="plant-card${isPoisonous ? ' poisonous' : ''}">
                        <div class="plant-icon">🌿</div>
                        <div class="plant-name">${plant.name}</div>
                        <div class="plant-latin">${plant.latin_name || 'N/A'}</div>
                        <div class="plant-keys">${keysHtml}</div>
                    </div>
                </div>
                <div>
                    ${q.clue ? `
                        <div class="clue-box">
                            <div class="clue-label">🕵️ CLUE</div>
                            <div class="clue-text">${q.clue}</div>
                        </div>
                    ` : ''}
                    <div class="question-text">${renderMarkdown(q.question)}</div>
                    <div class="answer-grid cols-2">
                        ${optionsHtml}
                    </div>
                </div>
            </div>
        `;
    },

/* 2f. Answer Handling ─────────────────────────────────────────── */

    handleAnswer(encodedAnswer, btn) {
        const answer = decodeURIComponent(encodedAnswer);
        const q = this.state.currentQuestion;
        if (!q) return;

        disableAllAnswerButtons();

        const isCorrect = (answer === q.correct);

        // Highlight correct / wrong
        if (isCorrect) {
            btn.classList.add('correct');
        } else {
            btn.classList.add('wrong');
            highlightCorrectAnswer(q.correct);
        }

        // Update state
        if (isCorrect) {
            const streakBonus = this.state.streak * 2;
            const totalPoints  = q.points + streakBonus;
            this.state.score              += totalPoints;
            this.state.streak             += 1;
            this.state.totalPlantsIdentified += 1;

            // Add to herbarium
            const plantName = q.plant.name;
            this.state.herbarium[plantName] = (this.state.herbarium[plantName] || 0) + 1;

            // Season badge
            if (!this.state.seasonBadges.includes(this.state.season)) {
                this.state.seasonBadges.push(this.state.season);
            }

            // Achievement checks
            const totalFound = Object.keys(this.state.herbarium).length;
            if (totalFound >= 1 && !this.state.achievements.foraging_novice) {
                this.state.achievements.foraging_novice = true;
                showToast('🏅 Achievement Unlocked: Novice Forager!');
            }
            if (totalFound >= 25 && !this.state.achievements.foraging_botanist) {
                this.state.achievements.foraging_botanist = true;
                showToast('🏅 Achievement Unlocked: Botanist!');
            }
            if (this.state.seasonBadges.length >= 4 && !this.state.achievements.foraging_master) {
                this.state.achievements.foraging_master = true;
                showToast('🏅 Achievement Unlocked: Seasonal Master!');
            }

            // Check for bonus round trigger
            if (this.state.streak > 0 && this.state.streak % 5 === 0 && !this.state.bonusRound) {
                this.state.bonusRound = true;
            }
        } else {
            this.state.lives  -= 1;
            this.state.streak  = 0;
        }

        this.state.currentQuestion = null;
        this.save();
        this.updateStats();
        this.renderAchievements();
        this.renderSeasonButtons();

        // Show feedback
        this.showFeedback(isCorrect, q);

        // Check game over or load next
        if (this.state.lives <= 0) {
            setTimeout(() => this.showGameOver(), 1500);
            return;
        }

        setTimeout(() => {
            if (this.state.bonusRound) {
                this.fetchBonusQuestion();
            } else {
                this.fetchQuestion();
            }
        }, 1500);
    },

    /** Helper — shows answer feedback appended to the current content. */
    showFeedback(isCorrect, q) {
        const content = document.getElementById('fq-content');
        const feedbackDiv = document.createElement('div');

        if (isCorrect) {
            const streakBonus = this.state.streak > 1
                ? ` (+${(this.state.streak - 1) * 2} streak bonus)`
                : '';
            feedbackDiv.className = 'feedback-correct';
            feedbackDiv.innerHTML = `
                <div class="feedback-icon">🎉</div>
                <div class="feedback-text">CORRECT! +${q.points} XP${streakBonus}</div>
                <div class="feedback-detail">${renderMarkdown(q.explanation)}</div>
            `;
        } else {
            feedbackDiv.className = 'feedback-wrong';
            feedbackDiv.innerHTML = `
                <div class="feedback-icon">❌</div>
                <div class="feedback-text">Incorrect</div>
                <div class="feedback-detail">The answer was: <strong>${q.correct}</strong></div>
            `;
        }

        content.appendChild(feedbackDiv);
    },

/* 2g. Bonus Round ─────────────────────────────────────────────── */

    renderBonusQuestion(q) {
        const content = document.getElementById('fq-content');
        document.getElementById('fq-game-over').classList.add('hidden');

        let optionsHtml = '';
        if (q.options) {
            q.options.forEach((opt) => {
                optionsHtml += `<button class="answer-btn" onclick="foragingQuest.handleBonusAnswer('${encodeURIComponent(opt)}', this)">${opt}</button>`;
            });
        }

        content.innerHTML = `
            <div class="bonus-banner">
                <div class="bonus-icon">⚡</div>
                <div class="bonus-title">BONUS ROUND!</div>
                <div class="bonus-desc">You've identified 5 plants in a row! Answer for <strong>Double Points</strong>.</div>
            </div>
            <div class="question-text">${renderMarkdown(q.question)}</div>
            <div class="answer-grid cols-2">
                ${optionsHtml}
            </div>
        `;
    },

    handleBonusAnswer(encodedAnswer, btn) {
        const answer = decodeURIComponent(encodedAnswer);
        const q = this.state.currentQuestion;
        if (!q) return;

        disableAllAnswerButtons();

        const isCorrect = (answer === q.correct);

        if (isCorrect) {
            btn.classList.add('correct');
        } else {
            btn.classList.add('wrong');
            highlightCorrectAnswer(q.correct);
        }

        this.state.bonusRound = false;

        if (isCorrect) {
            this.state.score += 20;
            this.state.streak = 0;
            this.state.totalPlantsIdentified += 1;
            const plantName = q.plant.name;
            this.state.herbarium[plantName] = (this.state.herbarium[plantName] || 0) + 1;
        } else {
            this.state.streak = 0;
        }

        this.state.currentQuestion = null;
        this.save();
        this.updateStats();

        // Show bonus feedback
        const content = document.getElementById('fq-content');
        const feedbackDiv = document.createElement('div');

        if (isCorrect) {
            feedbackDiv.className = 'feedback-correct';
            feedbackDiv.innerHTML = `
                <div class="feedback-icon">🎉</div>
                <div class="feedback-text">BONUS CORRECT! +20 XP</div>
            `;
        } else {
            feedbackDiv.className = 'feedback-wrong';
            feedbackDiv.innerHTML = `
                <div class="feedback-icon">❌</div>
                <div class="feedback-text">Incorrect!</div>
                <div class="feedback-detail">The answer was: <strong>${q.correct}</strong></div>
            `;
        }

        content.appendChild(feedbackDiv);
        setTimeout(() => this.fetchQuestion(), 1500);
    },

/* 2h. Game Over & Restart ────────────────────────────────────── */

    showGameOver() {
        const content = document.getElementById('fq-content');
        content.innerHTML = '';

        const goDiv = document.getElementById('fq-game-over');
        goDiv.classList.remove('hidden');
        goDiv.innerHTML = `
            <div class="go-icon">🤕</div>
            <div class="go-title">Adventure Over</div>
            <div class="go-text">Even the best explorers need a rest. Try again to learn more!</div>
            <div class="go-score">Final Score: <strong>${this.state.score} XP</strong></div>
            <button class="btn-restart" onclick="foragingQuest.restart()">🔄 Restart Adventure</button>
        `;
    },

    restart() {
        this.state = { ...this.defaults };
        this.state.season = DEFAULT_SEASON;
        this.save();

        document.getElementById('fq-game-over').classList.add('hidden');
        this.renderSeasonButtons();
        this.updateStats();
        this.renderAchievements();
        this.fetchQuestion();
    },

/* 2i. Achievements ──────────────────────────────────────────── */

    renderAchievements() {
        const container = document.getElementById('fq-achievements');
        const totalFound = Object.keys(this.state.herbarium).length;

        const achDefs = [
            {
                key: 'foraging_novice',
                name: 'Novice Forager',
                desc: 'Identify your first plant',
                icon: '🌿',
                progress: () => this.state.achievements.foraging_novice ? '(Done)' : `(${totalFound}/1)`
            },
            {
                key: 'foraging_botanist',
                name: 'Botanist',
                desc: 'Identify 25 unique plants',
                icon: '🍃',
                progress: () => this.state.achievements.foraging_botanist ? '(Done)' : `(${totalFound}/25)`
            },
            {
                key: 'foraging_master',
                name: 'Seasonal Master',
                desc: 'Earn all 4 season badges',
                icon: '🏆',
                progress: () => this.state.achievements.foraging_master ? '(Done)' : `(${this.state.seasonBadges.length}/4)`
            }
        ];

        container.innerHTML = achDefs.map(a => this.renderAchievementCard(a)).join('');
    },

    /** Helper — renders a single achievement card. */
    renderAchievementCard(a) {
        const unlocked    = this.state.achievements[a.key];
        const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
        const bg          = unlocked
            ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)'
            : 'var(--bg-card)';
        const icon      = unlocked ? '✅' : '🔒';
        const nameColor = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

        return `
            <div class="achievement-card${unlocked ? ' unlocked' : ''}"
                 style="background: ${bg}; border-color: ${borderColor};">
                <div>
                    <div class="ach-left">
                        <span class="ach-icon">${icon}</span>
                        <span class="ach-name" style="color: ${nameColor};">${a.name}</span>
                    </div>
                    <div class="ach-desc">${a.desc}</div>
                </div>
                <span class="ach-progress">${a.progress()}</span>
            </div>
        `;
    }
};


/* ───────────────────────────────────────────────────────────────
   3. SURVIVAL SCHOOL
   ─────────────────────────────────────────────────────────────── */

/* 3a. Defaults & State ───────────────────────────────────────── */

const survivalSchool = {

    LEVEL_LABELS: { 1: 'Beginner', 2: 'Intermediate', 3: 'Expert' },
    LEVEL_COLORS: { 1: '#4CAF50',  2: '#FFC107',       3: '#ff5252' },
    LEVEL_BGS:    { 1: '#4CAF5020', 2: '#FFC10720',     3: '#ff525220' },

    defaults: {
        score: 0,
        lives: 3,
        level: 1,
        correctCount: 0,
        casesSolved: 0,
        currentCase: null,
        result: null,
        seenPlants: [],
        achievements: {
            survival_scout: false,
            survival_expert: false,
            survival_detective: false
        }
    },

    state: null,

/* 3b. Initialisation & Persistence ───────────────────────────── */

    init() {
        this.state = loadState('ss_state', this.defaults);

        // Ensure achievement keys exist even if saved state is missing them
        for (const key of ['survival_scout', 'survival_expert', 'survival_detective']) {
            if (!(key in this.state.achievements)) {
                this.state.achievements[key] = false;
            }
        }

        this.updateStats();
        this.updateProgress();
        this.renderAchievements();

        // Resume the correct view based on current state
        if (this.state.lives <= 0) {
            this.showGameOver();
        } else if (this.state.currentCase === null) {
            this.fetchCase();
        } else if (this.state.result !== null) {
            this.renderResult();
        } else {
            this.renderCase(this.state.currentCase);
        }

        // Display case-count blurb
        const countEl = document.getElementById('ss-case-count');
        if (countEl) {
            countEl.textContent = `📊 ${SURVIVAL_CASE_COUNT.total} unique cases available `
                + `(L1: ${SURVIVAL_CASE_COUNT.level_1}, `
                + `L2: ${SURVIVAL_CASE_COUNT.level_2}, `
                + `L3: ${SURVIVAL_CASE_COUNT.level_3})`;
        }
    },

    save() {
        saveState('ss_state', this.state);
    },

/* 3c. UI Updates ──────────────────────────────────────────────── */

    updateStats() {
        const hearts = '❤️'.repeat(Math.max(0, this.state.lives));

        document.getElementById('ss-stats').innerHTML = `
            <div class="stat-box lives">
                <div class="stat-label">LIVES</div>
                <div class="stat-value">${hearts || '💔'}</div>
            </div>
            <div class="stat-box score">
                <div class="stat-label">SCORE</div>
                <div class="stat-value">${this.state.score}</div>
            </div>
            <div class="stat-box cases">
                <div class="stat-label">CASES SOLVED</div>
                <div class="stat-value">${this.state.casesSolved}</div>
            </div>
        `;
    },

    updateProgress() {
        const levelName = SURVIVAL_DIFFICULTY[this.state.level] || 'Level 1';
        const progress  = Math.min(this.state.correctCount / 5, 1.0) * 100;

        document.getElementById('ss-progress').innerHTML = `
            <span class="level-name">🕵️ ${levelName}</span>
            <span class="level-count">Cases to next level: ${this.state.correctCount}/5</span>
        `;

        document.getElementById('ss-progress-bar').innerHTML = `
            <div class="progress-bar-label">Level ${this.state.level} Progress: ${this.state.correctCount}/5 Cases</div>
            <div class="progress-bar">
                <div class="progress-bar-fill" style="width: ${progress}%">${this.state.correctCount}/5</div>
            </div>
        `;
    },

/* 3d. Case Handling ──────────────────────────────────────────── */

    async fetchCase() {
        const content = document.getElementById('ss-content');
        content.innerHTML = '<div class="loading-spinner">☠️ Loading case...</div>';
        document.getElementById('ss-game-over').classList.add('hidden');

        try {
            const exclude = this.state.seenPlants.slice(-10).join(',');
            const resp = await fetch(
                `/api/games/survival-school/case?level=${this.state.level}&exclude=${encodeURIComponent(exclude)}`
            );
            const c = await resp.json();

            this.state.currentCase = c;
            this.state.result = null;
            this.state.seenPlants.push(c.safe_plant);

            // Keep seenPlants to a manageable size
            if (this.state.seenPlants.length > 30) {
                this.state.seenPlants = this.state.seenPlants.slice(-20);
            }

            this.save();
            this.renderCase(c);
        } catch (e) {
            content.innerHTML = `
                <p>Could not load case.
                   <button class="btn-secondary" onclick="survivalSchool.fetchCase()">Try again</button>
                </p>`;
        }
    },

    renderCase(c) {
        const content = document.getElementById('ss-content');
        document.getElementById('ss-game-over').classList.add('hidden');

        const caseNum   = this.state.casesSolved + 1;
        const levelInfo = this.getLevelInfo(c.level);

        // Build and shuffle the two options
        const options = this.shuffleOptions([
            { name: c.safe_plant,   icon: c.safe_icon,   isSafe: true  },
            { name: c.danger_plant, icon: c.danger_icon,  isSafe: false }
        ]);

        const opt0 = options[0];
        const opt1 = options[1];

        content.innerHTML = `
            <div class="case-file">
                <div class="case-file-header">
                    <h3>📋 Case File #${caseNum}</h3>
                    <span class="case-level-badge ${levelInfo.label.toLowerCase()}"
                          style="background: ${levelInfo.bg}; color: ${levelInfo.color}; border-color: ${levelInfo.color}50;">
                        ${levelInfo.label}
                    </span>
                </div>
            </div>

            <div class="case-section" style="background: var(--bg-card); border-left: 4px solid var(--green-leaf); border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.8rem;">
                <span class="case-label">📍 LOCATION</span><br>
                <span class="case-value">${c.safe_habitat}</span>
            </div>

            <div class="case-observation">
                <div class="obs-label">🔍 YOUR OBSERVATION</div>
                <div class="obs-text">${c.clue}</div>
            </div>

            <div class="case-rule">
                <div class="rule-label">⚠️ KEY RULE</div>
                <div class="rule-text">${renderMarkdown(c.rule)}</div>
            </div>

            <hr class="game-divider">

            <div class="verdict-box">
                <div class="verdict-title">⚖️ VERDICT</div>
                <div class="verdict-sub">Which is the <strong>SAFE</strong> plant?</div>
            </div>

            <div class="answer-grid cols-2">
                <button class="answer-btn" onclick="survivalSchool.handleVerdict(${opt0.isSafe}, this)">
                    ${opt0.icon} ${opt0.name}
                </button>
                <button class="answer-btn" onclick="survivalSchool.handleVerdict(${opt1.isSafe}, this)">
                    ${opt1.icon} ${opt1.name}
                </button>
            </div>
        `;
    },

    /** Helper — level metadata for rendering. */
    getLevelInfo(level) {
        return {
            label: this.LEVEL_LABELS[level] || 'Beginner',
            color: this.LEVEL_COLORS[level] || '#4CAF50',
            bg:    this.LEVEL_BGS[level]    || '#4CAF5020'
        };
    },

    /** Helper — Fisher-Yates shuffle for the answer options. */
    shuffleOptions(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    },

/* 3e. Answer Handling ─────────────────────────────────────────── */

    handleVerdict(isSafe, btn) {
        const c = this.state.currentCase;
        if (!c) return;

        disableAllAnswerButtons();

        if (isSafe) {
            btn.classList.add('correct');
            this.state.result        = 'correct';
            this.state.score        += 20;
            this.state.correctCount += 1;
            this.state.casesSolved  += 1;

            // Achievement checks
            if (!this.state.achievements.survival_scout) {
                this.state.achievements.survival_scout = true;
                showToast('🏅 Achievement Unlocked: Scout!');
            }
            if (this.state.casesSolved >= 20 && !this.state.achievements.survival_detective) {
                this.state.achievements.survival_detective = true;
                showToast('🏅 Achievement Unlocked: Detective!');
            }
        } else {
            btn.classList.add('wrong');
            this.state.result        = 'wrong';
            this.state.lives        -= 1;
            this.state.correctCount  = 0;
        }

        this.save();
        this.updateStats();
        this.renderResult();
    },

/* 3f. Result Rendering ───────────────────────────────────────── */

    renderResult() {
        const c = this.state.currentCase;
        if (!c) return;

        const content   = document.getElementById('ss-content');
        const isCorrect = (this.state.result === 'correct');

        // ── Level-up check ──────────────────────────────────────
        let levelUpHtml = '';
        if (isCorrect && this.state.correctCount >= 5 && this.state.level === 1) {
            this.state.level        = 2;
            this.state.correctCount = 0;
            this.save();

            levelUpHtml = `
                <div class="level-up-banner">
                    <div class="lu-icon">🏆</div>
                    <div class="lu-title">LEVEL UP!</div>
                    <div class="lu-text">You've unlocked <b>Level 2: Fungi &amp; Roots</b></div>
                    <div class="lu-sub">Cases now include harder plants and fungi.</div>
                </div>
            `;

            if (!this.state.achievements.survival_expert) {
                this.state.achievements.survival_expert = true;
                showToast('🏅 Achievement Unlocked: Graduate!');
            }
        }

        // ── Feedback banner ──────────────────────────────────────
        const feedbackClass  = isCorrect ? 'feedback-correct' : 'feedback-wrong';
        const feedbackIcon   = isCorrect ? '✅' : '☠️';
        const feedbackText   = isCorrect ? 'CASE SOLVED!' : 'DANGER!';
        const feedbackDetail = isCorrect
            ? 'Great work, Inspector. +20 points.'
            : `That was the wrong choice. The safe plant was <strong>${c.safe_plant}</strong>.`;

        // ── Expandable plant details ────────────────────────────
        const safeDetailsHtml = c.safe_plant_details
            ? this.renderSafePlantDetails(c)
            : '';

        // ── Compose final view ───────────────────────────────────
        content.innerHTML = `
            <div class="${feedbackClass}">
                <div class="feedback-icon">${feedbackIcon}</div>
                <div class="feedback-text">${feedbackText}</div>
                <div class="feedback-detail">${feedbackDetail}</div>
            </div>
            ${levelUpHtml}

            <div class="comparison-grid">
                <div class="safe-card">
                    <div class="card-icon">🌿</div>
                    <div class="card-name">${c.safe_plant}</div>
                    <div class="card-status">✅ SAFE TO EAT</div>
                    <div style="color: var(--cream-dim); font-size: 0.85rem;">${c.safe_habitat}</div>
                </div>
                <div class="danger-card">
                    <div class="card-icon">☠️</div>
                    <div class="card-name">${c.danger_plant}</div>
                    <div class="card-status">⚠️ DANGEROUS</div>
                    <div style="color: var(--cream-dim); font-size: 0.85rem;">Do NOT consume</div>
                </div>
            </div>

            <div class="case-analysis">
                <div class="analysis-label">📝 Case Analysis</div>
                <div class="analysis-text">${renderMarkdown(c.fact)}</div>
            </div>

            ${safeDetailsHtml}

            <button class="btn-next-case" onclick="survivalSchool.nextCase()">📋 Next Case</button>
        `;

        this.updateProgress();
        this.renderAchievements();

        if (this.state.lives <= 0) {
            setTimeout(() => this.showGameOver(), 500);
        }
    },

    /** Helper — renders the expandable safe-plant details section. */
    renderSafePlantDetails(c) {
        const details = c.safe_plant_details;
        let innerHtml = '';

        if (details.lookalikes && details.lookalikes.length > 0) {
            innerHtml += '<p><strong>Lookalikes:</strong></p><ul>';
            innerHtml += details.lookalikes.map(la => {
                if (typeof la !== 'object') return '';
                const danger = la.danger || 'Unknown';
                const icon   = ['DEADLY', 'EXTREME'].includes(danger)   ? '☠️'
                             : ['POISONOUS', 'HIGH'].includes(danger)   ? '⚠️'
                             : '✅';
                return `<li>${icon} <strong>${la.name}</strong> (${danger}): ${la.diff || ''}</li>`;
            }).join('');
            innerHtml += '</ul>';
        }

        if (details.warnings) {
            innerHtml += `<p><strong>⚠️ Warning:</strong> ${details.warnings}</p>`;
        }
        if (details.confusion_notes) {
            innerHtml += `<p><strong>🔍 Key ID Note:</strong> ${details.confusion_notes}</p>`;
        }

        return `
            <details class="learn-more">
                <summary>📖 Learn more about ${c.safe_plant}</summary>
                <div class="learn-more-content">${innerHtml}</div>
            </details>
        `;
    },

/* 3g. Game Flow ──────────────────────────────────────────────── */

    nextCase() {
        this.state.currentCase = null;
        this.state.result      = null;
        this.save();
        this.fetchCase();
    },

    showGameOver() {
        const content = document.getElementById('ss-content');
        content.innerHTML = '';

        const goDiv = document.getElementById('ss-game-over');
        goDiv.classList.remove('hidden');
        goDiv.innerHTML = `
            <div class="go-icon">🤕</div>
            <div class="go-title">Training Ended</div>
            <div class="go-text">Don't worry, even experts make mistakes.</div>
            <div class="go-score">Cases solved this session: <strong>${this.state.casesSolved}</strong></div>
            <button class="btn-restart" onclick="survivalSchool.restart()">🔄 Restart Training</button>
        `;
    },

    restart() {
        this.state = { ...this.defaults };
        this.save();

        document.getElementById('ss-game-over').classList.add('hidden');
        this.updateStats();
        this.updateProgress();
        this.renderAchievements();
        this.fetchCase();
    },

/* 3h. Achievements ───────────────────────────────────────────── */

    renderAchievements() {
        const container = document.getElementById('ss-achievements');

        const achDefs = [
            {
                key: 'survival_scout',
                name: 'Scout',
                desc: 'Solve your first case',
                icon: '🕵️',
                progress: () => this.state.achievements.survival_scout ? '(1 case)' : '(0/1)'
            },
            {
                key: 'survival_expert',
                name: 'Graduate',
                desc: 'Reach Level 2',
                icon: '🎓',
                progress: () => this.state.achievements.survival_expert ? '(Done)' : `(${this.state.correctCount}/5 this level)`
            },
            {
                key: 'survival_detective',
                name: 'Detective',
                desc: 'Solve 20 cases',
                icon: '🔍',
                progress: () => this.state.achievements.survival_detective ? '(Done)' : `(${this.state.casesSolved}/20 total)`
            }
        ];

        container.innerHTML = achDefs.map(a => this.renderAchievementCard(a)).join('');
    },

    /** Helper — renders a single achievement card (shared pattern). */
    renderAchievementCard(a) {
        const unlocked    = this.state.achievements[a.key];
        const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
        const bg          = unlocked
            ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)'
            : 'var(--bg-card)';
        const icon      = unlocked ? '✅' : '🔒';
        const nameColor = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

        return `
            <div class="achievement-card${unlocked ? ' unlocked' : ''}"
                 style="background: ${bg}; border-color: ${borderColor};">
                <div>
                    <div class="ach-left">
                        <span class="ach-icon">${icon}</span>
                        <span class="ach-name" style="color: ${nameColor};">${a.name}</span>
                    </div>
                    <div class="ach-desc">${a.desc}</div>
                </div>
                <span class="ach-progress">${a.progress()}</span>
            </div>
        `;
    }
};


/* ───────────────────────────────────────────────────────────────
   4. DAILY QUIZ
   ─────────────────────────────────────────────────────────────── */

/* 4a. Defaults & State ───────────────────────────────────────── */

const dailyQuiz = {

    defaults: {
        score: 0,
        qNum: 0,
        maxQuestions: 10,
        streak: 0,
        livesRemaining: 3,
        category: 'All',
        difficulty: 'Beginner',
        challengeMode: false,
        currentQuestion: null,
        plantsSeen: [],
        achievements: {
            quiz_streak: false,
            quiz_challenger: false
        },
        gameActive: false
    },

    state: null,

/* 4b. Initialisation & Persistence ───────────────────────────── */

    init() {
        this.state = loadState('dq_state', this.defaults);

        // Ensure achievement keys exist even if saved state is missing them
        for (const key of ['quiz_streak', 'quiz_challenger']) {
            if (!(key in this.state.achievements)) {
                this.state.achievements[key] = false;
            }
        }

        this.renderAchievements();

        if (this.state.gameActive) {
            this.restoreGame();
        }
    },

    save() {
        saveState('dq_state', this.state);
    },

/* 4c. Game Lifecycle ─────────────────────────────────────────── */

    startGame() {
        const category      = document.getElementById('dq-category').value;
        const difficulty    = document.querySelector('input[name="dq-difficulty"]:checked').value;
        const challengeMode = document.getElementById('dq-challenge').checked;

        this.state = {
            ...this.defaults,
            category,
            difficulty,
            challengeMode,
            livesRemaining: challengeMode ? 1 : 3,
            maxQuestions: 10,
            gameActive: true,
            achievements: this.state.achievements || { quiz_streak: false, quiz_challenger: false },
            plantsSeen: []
        };

        this.save();
        document.getElementById('dq-settings').style.display = 'none';

        if (challengeMode) {
            this.showChallengeBanner();
        }

        this.updateStats();
        this.fetchQuestion();
    },

    restoreGame() {
        if (!this.state.gameActive) return;

        document.getElementById('dq-settings').style.display = 'none';

        if (this.state.challengeMode) {
            this.showChallengeBanner();
        }

        if (this.state.livesRemaining <= 0 || this.state.qNum >= this.state.maxQuestions) {
            this.showGameOver();
            return;
        }

        this.updateStats();
        this.fetchQuestion();
    },

    /** Helper — renders the challenge-mode banner. */
    showChallengeBanner() {
        const banner = document.getElementById('dq-challenge-banner');
        banner.classList.remove('hidden');
        banner.innerHTML = `
            <div class="challenge-icon">⚔️</div>
            <div class="challenge-title">CHALLENGE MODE</div>
            <div class="challenge-desc">1 Life · 10 Questions · Can you survive?</div>
        `;
    },

/* 4d. UI Updates ──────────────────────────────────────────────── */

    updateStats() {
        const streakFires = this.state.streak > 0
            ? '🔥'.repeat(Math.min(this.state.streak, 5))
            : '';

        document.getElementById('dq-stats').innerHTML = `
            <div class="stat-box streak">
                <div class="stat-label">STREAK</div>
                <div class="stat-value">${streakFires} ${this.state.streak}</div>
            </div>
            <div class="stat-box score">
                <div class="stat-label">SCORE</div>
                <div class="stat-value">${this.state.score}</div>
            </div>
            <div class="stat-box question-num">
                <div class="stat-label">QUESTION</div>
                <div class="stat-value">${this.state.qNum}/${this.state.maxQuestions}</div>
            </div>
        `;

        const progress = Math.min(this.state.qNum / this.state.maxQuestions, 1.0) * 100;

        document.getElementById('dq-progress-bar').innerHTML = `
            <div class="progress-bar-label">Progress: ${this.state.qNum}/${this.state.maxQuestions}</div>
            <div class="progress-bar">
                <div class="progress-bar-fill" style="width: ${progress}%">${this.state.qNum}/${this.state.maxQuestions}</div>
            </div>
        `;

        this.updateLives();
    },

    /** Helper — updates the lives display based on current mode. */
    updateLives() {
        const livesEl = document.getElementById('dq-lives');

        if (!this.state.challengeMode) {
            livesEl.classList.remove('hidden');
            const hearts = '❤️'.repeat(Math.max(0, this.state.livesRemaining));
            livesEl.innerHTML = `
                <span class="lives-label">Lives:</span>
                <span class="lives-hearts">${hearts || '💔'}</span>
            `;
        } else {
            livesEl.classList.add('hidden');
        }
    },

/* 4e. Question Handling ──────────────────────────────────────── */

    async fetchQuestion() {
        const content = document.getElementById('dq-content');
        content.innerHTML = '<div class="loading-spinner">🎲 Loading...</div>';
        document.getElementById('dq-game-over').classList.add('hidden');

        const numOptions = (this.state.difficulty === 'Expert' || this.state.challengeMode) ? 4 : 3;

        try {
            const resp = await fetch(
                `/api/games/daily-quiz/question?category=${encodeURIComponent(this.state.category)}&num_options=${numOptions}`
            );
            const q = await resp.json();
            this.state.currentQuestion = q;
            this.save();
            this.renderQuestion(q);
        } catch (e) {
            content.innerHTML = `
                <p>Could not load question.
                   <button class="btn-secondary" onclick="dailyQuiz.fetchQuestion()">Try again</button>
                </p>`;
        }
    },

    renderQuestion(q) {
        const content = document.getElementById('dq-content');

        let optionsHtml = '';
        if (q.options) {
            q.options.forEach((opt) => {
                optionsHtml += `<button class="answer-btn" onclick="dailyQuiz.handleAnswer('${encodeURIComponent(opt)}', this)">👉 ${opt}</button>`;
            });
        }

        content.innerHTML = `
            <div class="q-type-header" style="border-left-color: ${q.type_color};">
                <div class="q-type-left">
                    <span class="q-type-icon">${q.type_icon}</span>
                    <span class="q-type-name" style="color: ${q.type_color};">${q.type_name}</span>
                </div>
                <span style="color: var(--cream-dim); font-size: 0.8rem;">Q${this.state.qNum + 1}/${this.state.maxQuestions}</span>
            </div>
            <div class="question-text">${renderMarkdown(q.text)}</div>
            <div class="answer-grid cols-2">
                ${optionsHtml}
            </div>
        `;
    },

/* 4f. Answer Handling ─────────────────────────────────────────── */

    handleAnswer(encodedAnswer, btn) {
        const answer = decodeURIComponent(encodedAnswer);
        const q = this.state.currentQuestion;
        if (!q) return;

        disableAllAnswerButtons();

        const isCorrect = (answer === q.correct);

        // Highlight correct / wrong
        if (isCorrect) {
            btn.classList.add('correct');
        } else {
            btn.classList.add('wrong');
            highlightCorrectAnswer(q.correct);
        }

        // Update state
        if (isCorrect) {
            this.state.score += 1;
            this.state.streak += 1;
            this.state.plantsSeen.push({ name: q.plant.name, correct: true });

            if (this.state.streak >= 5 && !this.state.achievements.quiz_streak) {
                this.state.achievements.quiz_streak = true;
                showToast('🏅 Achievement Unlocked: Quick Wit!');
            }
        } else {
            this.state.streak = 0;
            this.state.livesRemaining -= 1;
            this.state.plantsSeen.push({ name: q.plant.name, correct: false });
        }

        this.state.qNum += 1;
        this.state.currentQuestion = null;
        this.save();

        // Show feedback
        this.showFeedback(isCorrect, q);
        this.updateStats();

        // Check end conditions
        if (this.state.livesRemaining <= 0) {
            setTimeout(() => this.showGameOver(), 2000);
            return;
        }
        if (this.state.qNum >= this.state.maxQuestions) {
            setTimeout(() => this.showComplete(), 2000);
            return;
        }

        setTimeout(() => this.fetchQuestion(), 2000);
    },

    /** Helper — shows answer feedback appended to the current content. */
    showFeedback(isCorrect, q) {
        const content = document.getElementById('dq-content');
        const feedbackDiv = document.createElement('div');

        if (isCorrect) {
            feedbackDiv.className = 'feedback-correct';
            feedbackDiv.innerHTML = `
                <div class="feedback-icon">✅</div>
                <div class="feedback-text">Correct!</div>
                <div class="plant-fact-box">${renderMarkdown(q.fact)}</div>
            `;
        } else {
            feedbackDiv.className = 'feedback-wrong';
            feedbackDiv.innerHTML = `
                <div class="feedback-icon">❌</div>
                <div class="feedback-text">Incorrect</div>
                <div class="feedback-detail">The correct answer was: <strong>${q.correct}</strong></div>
                <div class="plant-fact-box">${renderMarkdown(q.fact)}</div>
            `;
        }

        content.appendChild(feedbackDiv);
    },

/* 4g. End States ─────────────────────────────────────────────── */

    showGameOver() {
        const content = document.getElementById('dq-content');
        content.innerHTML = '';

        const isChallenge = this.state.challengeMode;
        const title    = isChallenge ? '⚔️ CHALLENGE FAILED' : 'Game Over';
        const subtitle = isChallenge ? 'You ran out of lives.' : 'Better luck next time!';

        const goDiv = document.getElementById('dq-game-over');
        goDiv.classList.remove('hidden');
        goDiv.className = 'game-over';
        goDiv.innerHTML = `
            <div class="go-icon">${isChallenge ? '⚔️' : '🤕'}</div>
            <div class="go-title">${title}</div>
            <div class="go-text">${subtitle}</div>
            <div class="go-score">Score: <strong>${this.state.score}</strong> | Questions answered: <strong>${this.state.qNum}</strong></div>
            <button class="btn-restart" onclick="dailyQuiz.restart()">🔄 Try Again</button>
        `;
    },

    showComplete() {
        const content = document.getElementById('dq-content');
        content.innerHTML = '';

        const isChallenge = this.state.challengeMode;
        const title = isChallenge ? '⚔️ CHALLENGE COMPLETE!' : '🎉 QUIZ COMPLETE!';

        if (isChallenge && !this.state.achievements.quiz_challenger) {
            this.state.achievements.quiz_challenger = true;
            this.save();
            showToast('🏅 Achievement Unlocked: Challenger!');
            this.renderAchievements();
        }

        const plantsSeenHtml = this.state.plantsSeen.length > 0
            ? `
                <details class="learn-more" style="margin-top: 1rem;">
                    <summary>📖 Plants You Were Tested On</summary>
                    <div class="learn-more-content plants-seen-list">
                        ${this.state.plantsSeen.map(p => `${p.correct ? '✅' : '❌'} ${p.name}`).join('<br>')}
                    </div>
                </details>
            `
            : '';

        const goDiv = document.getElementById('dq-game-over');
        goDiv.classList.remove('hidden');
        goDiv.className = 'game-over success';
        goDiv.innerHTML = `
            <div class="go-icon">🎉</div>
            <div class="go-title">${title}</div>
            <div class="go-score">Final Score: <strong>${this.state.score}</strong></div>
            ${plantsSeenHtml}
            <button class="btn-restart" onclick="dailyQuiz.restart()">🔄 Try Again</button>
        `;
    },

/* 4h. Restart ─────────────────────────────────────────────────── */

    restart() {
        this.state = {
            ...this.defaults,
            achievements: { quiz_streak: false, quiz_challenger: false },
            plantsSeen: []
        };

        this.save();

        document.getElementById('dq-game-over').classList.add('hidden');
        document.getElementById('dq-settings').style.display = '';
        document.getElementById('dq-challenge-banner').classList.add('hidden');
        document.getElementById('dq-lives').classList.add('hidden');
        document.getElementById('dq-content').innerHTML = '';
        document.getElementById('dq-stats').innerHTML = '';
        document.getElementById('dq-progress-bar').innerHTML = '';

        this.renderAchievements();
    },

/* 4i. Achievements ───────────────────────────────────────────── */

    renderAchievements() {
        const container = document.getElementById('dq-achievements');

        const achDefs = [
            {
                key: 'quiz_streak',
                name: 'Quick Wit',
                desc: 'Build a 5-question streak',
                progress: () => this.state.achievements.quiz_streak ? '(Done)' : `(${this.state.streak}/5)`
            },
            {
                key: 'quiz_challenger',
                name: 'Challenger',
                desc: 'Complete Challenge Mode',
                progress: () => this.state.achievements.quiz_challenger ? '(Done)' : '(Complete Challenge Mode)'
            }
        ];

        container.innerHTML = achDefs.map(a => this.renderAchievementCard(a)).join('');
    },

    /** Helper — renders a single achievement card. */
    renderAchievementCard(a) {
        const unlocked    = this.state.achievements[a.key];
        const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
        const bg          = unlocked
            ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)'
            : 'var(--bg-card)';
        const icon      = unlocked ? '✅' : '🔒';
        const nameColor = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

        return `
            <div class="achievement-card${unlocked ? ' unlocked' : ''}"
                 style="background: ${bg}; border-color: ${borderColor};">
                <div>
                    <div class="ach-left">
                        <span class="ach-icon">${icon}</span>
                        <span class="ach-name" style="color: ${nameColor};">${a.name}</span>
                    </div>
                    <div class="ach-desc">${a.desc}</div>
                </div>
                <span class="ach-progress">${a.progress()}</span>
            </div>
        `;
    }
};


/* ───────────────────────────────────────────────────────────────
   5. BOOTSTRAP
   ─────────────────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
    foragingQuest.init();
    survivalSchool.init();
    dailyQuiz.init();
});
