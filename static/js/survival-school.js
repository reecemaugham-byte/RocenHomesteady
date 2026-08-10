/* ═══════════════════════════════════════════════════════════════
   ROCEN HOMESTEADY — SURVIVAL SCHOOL
   ═══════════════════════════════════════════════════════════════

   TABLE OF CONTENTS
   ─────────────────
   1.  Defaults & State
   2.  Initialisation & Persistence
   3.  UI Updates
       3a. Stats
       3b. Progress
   4.  Case Handling
       4a. Fetch Case
       4b. Render Case
   5.  Answer Handling
   6.  Result Rendering
   7.  Game Flow
       7a. Next Case
       7b. Game Over
       7c. Restart
   8.  Achievements
   9.  Bootstrap
   ═══════════════════════════════════════════════════════════════ */


/* ───────────────────────────────────────────────────────────────
   1. DEFAULTS & STATE
   ─────────────────────────────────────────────────────────────── */

const survivalSchool = {

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


/* ───────────────────────────────────────────────────────────────
   2. INITIALISATION & PERSISTENCE
   ─────────────────────────────────────────────────────────────── */

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

        // Display the case-count blurb
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


/* ───────────────────────────────────────────────────────────────
   3. UI UPDATES
   ─────────────────────────────────────────────────────────────── */

    /* 3a. Stats ───────────────────────────────────────────────── */

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

    /* 3b. Progress ─────────────────────────────────────────────── */

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


/* ───────────────────────────────────────────────────────────────
   4. CASE HANDLING
   ─────────────────────────────────────────────────────────────── */

    /* 4a. Fetch Case ───────────────────────────────────────────── */

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

            // Keep the seen-plants list from growing unboundedly
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

    /* 4b. Render Case ──────────────────────────────────────────── */

    renderCase(c) {
        const content = document.getElementById('ss-content');
        document.getElementById('ss-game-over').classList.add('hidden');

        const caseNum    = this.state.casesSolved + 1;
        const levelInfo  = this.getLevelInfo(c.level);

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
        const LEVEL_LABELS = { 1: 'Beginner', 2: 'Intermediate', 3: 'Expert' };
        const LEVEL_COLORS = { 1: '#4CAF50', 2: '#FFC107', 3: '#ff5252' };
        const LEVEL_BGS    = { 1: '#4CAF5020', 2: '#FFC10720', 3: '#ff525220' };

        return {
            label: LEVEL_LABELS[level] || 'Beginner',
            color: LEVEL_COLORS[level] || '#4CAF50',
            bg:    LEVEL_BGS[level]    || '#4CAF5020'
        };
    },

    /** Helper — Fisher-Yates shuffle for the two answer options. */
    shuffleOptions(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    },


/* ───────────────────────────────────────────────────────────────
   5. ANSWER HANDLING
   ─────────────────────────────────────────────────────────────── */

    handleVerdict(isSafe, btn) {
        const c = this.state.currentCase;
        if (!c) return;

        // Disable all answer buttons
        document.querySelectorAll('.answer-btn').forEach(b => {
            b.disabled = true;
            b.style.pointerEvents = 'none';
        });

        if (isSafe) {
            btn.classList.add('correct');
            this.state.result       = 'correct';
            this.state.score       += 20;
            this.state.correctCount += 1;
            this.state.casesSolved += 1;

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
            SFX.wrong();
            this.state.result        = 'wrong';
            this.state.lives        -= 1;
            this.state.correctCount  = 0;
        }

        this.save();
        this.updateStats();
        this.renderResult();
    },


/* ───────────────────────────────────────────────────────────────
   6. RESULT RENDERING
   ─────────────────────────────────────────────────────────────── */

    renderResult() {
        const c = this.state.currentCase;
        if (!c) return;

        const content   = document.getElementById('ss-content');
        const isCorrect = (this.state.result === 'correct');

        // ── Level-up check ──────────────────────────────────────
        let levelUpHtml = '';
        if (isCorrect && this.state.correctCount >= 5 && this.state.level === 1) {
            this.state.level        = 2;
            this.state.correctCount  = 0;
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

        // ── Plant details (lookalikes, warnings, confusion notes) ─
        const safeDetailsHtml = c.safe_plant_details ? this.renderSafePlantDetails(c) : '';

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
                             : ['POISONOUS', 'HIGH'].includes(danger) ? '⚠️'
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


/* ───────────────────────────────────────────────────────────────
   7. GAME FLOW
   ─────────────────────────────────────────────────────────────── */

    /* 7a. Next Case ────────────────────────────────────────────── */

    nextCase() {
        this.state.currentCase = null;
        this.state.result      = null;
        this.save();
        this.fetchCase();
    },

    /* 7b. Game Over ────────────────────────────────────────────── */

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

    /* 7c. Restart ──────────────────────────────────────────────── */

    restart() {
        this.state = Object.assign({}, this.defaults);
        this.save();

        document.getElementById('ss-game-over').classList.add('hidden');
        this.updateStats();
        this.updateProgress();
        this.renderAchievements();
        this.fetchCase();
    },


/* ───────────────────────────────────────────────────────────────
   8. ACHIEVEMENTS
   ─────────────────────────────────────────────────────────────── */

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

        container.innerHTML = achDefs.map(a => {
            const unlocked    = this.state.achievements[a.key];
            const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
            const bg          = unlocked
                ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)'
                : 'var(--bg-card)';
            const icon       = unlocked ? '✅' : '🔒';
            const nameColor   = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

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
        }).join('');
    }
};


/* ───────────────────────────────────────────────────────────────
   9. BOOTSTRAP
   ─────────────────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
    survivalSchool.init();
});
