/* ═══════════════════════════════════════════════════════════════
   ROCEN HOMESTEADY — DAILY QUIZ
   ═══════════════════════════════════════════════════════════════

   TABLE OF CONTENTS
   ─────────────────
   1.  Defaults & State
   2.  Initialisation & Persistence
   3.  Game Lifecycle
       3a. Start Game
       3b. Restore Game
   4.  UI Updates
       4a. Stats & Progress
   5.  Question Handling
       5a. Fetch Question
       5b. Render Question
   6.  Answer Handling
   7.  End States
       7a. Game Over
       7b. Quiz Complete
   8.  Restart
   9.  Achievements
   10. Bootstrap
   ═══════════════════════════════════════════════════════════════ */


/* ───────────────────────────────────────────────────────────────
   1. DEFAULTS & STATE
   ─────────────────────────────────────────────────────────────── */

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


/* ───────────────────────────────────────────────────────────────
   2. INITIALISATION & PERSISTENCE
   ─────────────────────────────────────────────────────────────── */

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


/* ───────────────────────────────────────────────────────────────
   3. GAME LIFECYCLE
   ─────────────────────────────────────────────────────────────── */

    /* 3a. Start Game ──────────────────────────────────────────── */

    startGame() {
        const category      = document.getElementById('dq-category').value;
        const difficulty     = document.querySelector('input[name="dq-difficulty"]:checked').value;
        const challengeMode  = document.getElementById('dq-challenge').checked;
        const timerEnabled   = document.getElementById('dq-timer')
            ? document.getElementById('dq-timer').checked
            : true;

        this.state = Object.assign({}, this.defaults, {
            category,
            difficulty,
            challengeMode,
            livesRemaining: challengeMode ? 1 : 3,
            maxQuestions: 10,
            gameActive: true,
            achievements: this.state.achievements || { quiz_streak: false, quiz_challenger: false },
            plantsSeen: []
        });

        this.save();
        document.getElementById('dq-settings').style.display = 'none';

        if (challengeMode) {
            this.showChallengeBanner();
        }

        this.updateStats();
        this.fetchQuestion();
    },

    /* 3b. Restore Game ────────────────────────────────────────── */

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


/* ───────────────────────────────────────────────────────────────
   4. UI UPDATES
   ─────────────────────────────────────────────────────────────── */

    /* 4a. Stats & Progress ────────────────────────────────────── */

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


/* ───────────────────────────────────────────────────────────────
   5. QUESTION HANDLING
   ─────────────────────────────────────────────────────────────── */

    /* 5a. Fetch Question ──────────────────────────────────────── */

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

    /* 5b. Render Question ─────────────────────────────────────── */

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
            <div class="answer-grid">
                ${optionsHtml}
            </div>
        `;
    },


/* ───────────────────────────────────────────────────────────────
   6. ANSWER HANDLING
   ─────────────────────────────────────────────────────────────── */

    handleAnswer(encodedAnswer, btn) {
        const answer = decodeURIComponent(encodedAnswer);
        const q = this.state.currentQuestion;
        if (!q) return;

        // Disable all answer buttons
        document.querySelectorAll('.answer-btn').forEach(b => {
            b.disabled = true;
            b.style.pointerEvents = 'none';
        });

        const isCorrect = (answer === q.correct);

        // Highlight correct / wrong answers
        if (isCorrect) {
            btn.classList.add('correct');
        } else {
            btn.classList.add('wrong');
            document.querySelectorAll('.answer-btn').forEach(b => {
                try {
                    const onclickAttr = b.getAttribute('onclick');
                    const match = onclickAttr.match(/'([^']+)'/);
                    if (match && decodeURIComponent(match[1]) === q.correct) {
                        b.classList.add('correct');
                    }
                } catch (e) { /* ignore */ }
            });
        }

        // Update state based on correctness
        if (isCorrect) {
            this.state.score   += 1;
            this.state.streak  += 1;
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

        this.state.qNum++;
        this.state.currentQuestion = null;
        this.save();

        // Show feedback
        this.showFeedback(isCorrect, q);

        this.updateStats();

        // Decide next step
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

    /** Helper — renders answer feedback below the question. */
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


/* ───────────────────────────────────────────────────────────────
   7. END STATES
   ─────────────────────────────────────────────────────────────── */

    /* 7a. Game Over ───────────────────────────────────────────── */

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

    /* 7b. Quiz Complete ───────────────────────────────────────── */

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


/* ───────────────────────────────────────────────────────────────
   8. RESTART
   ─────────────────────────────────────────────────────────────── */

    restart() {
        this.state = Object.assign({}, this.defaults, {
            achievements: { quiz_streak: false, quiz_challenger: false },
            plantsSeen: []
        });

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


/* ───────────────────────────────────────────────────────────────
   9. ACHIEVEMENTS
   ─────────────────────────────────────────────────────────────── */

    renderAchievements() {
        const container = document.getElementById('dq-achievements');

        const achDefs = [
            {
                key: 'quiz_streak',
                name: 'Quick Wit',
                desc: 'Build a 5-question streak',
                progress: () => this.state.achievements.quiz_streak
                    ? '(Done)'
                    : `(${this.state.streak}/5)`
            },
            {
                key: 'quiz_challenger',
                name: 'Challenger',
                desc: 'Complete Challenge Mode',
                progress: () => this.state.achievements.quiz_challenger
                    ? '(Done)'
                    : '(Complete Challenge Mode)'
            }
        ];

        container.innerHTML = achDefs.map(a => {
            const unlocked   = this.state.achievements[a.key];
            const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
            const bg          = unlocked
                ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)'
                : 'var(--bg-card)';
            const icon       = unlocked ? '✅' : '🔒';
            const nameColor  = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

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
   10. BOOTSTRAP
   ─────────────────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
    dailyQuiz.init();
});
