/*
 * progress.js — Game progress sync for Rocen Homesteady.
 * 
 * Syncs localStorage game state with the PostgreSQL database when logged in.
 * Games continue to use localStorage directly. This script adds a transparent
 * sync layer on top.
 * 
 * Behaviour:
 *   - On page load: checks auth, loads from DB if logged in, starts auto-save
 *   - If both localStorage and DB have data: merges them (keeps the best of each)
 *   - If DB is empty but localStorage has data: uploads to DB
 *   - Every 60 seconds: syncs localStorage → database
 *   - Shows a small toast on successful save/merge
 * 
 * Include on EVERY page that needs progress persistence:
 *   <script src="/static/js/progress.js"></script>
 */

const ProgressManager = {
    loggedIn: false,
    username: null,
    autoSaveInterval: null,
    lastSaveTime: null,
    saving: false,

    // All localStorage keys that represent game progress
    SAVE_KEYS: [
        'fq_state',       // Foraging Quest
        'ss_state',       // Survival School
        'dq_state',       // Daily Quiz
        'ev_state',       // Eco-Village
        'wk_state',       // Wild Kitchen
        'ft_state',       // Farm Tycoon
        'mg_state',       // Market Garden
        'am_state',       // Apiary Manager
        'master_inventory', // Shared inventory (Eco-Village + Wild Kitchen)
        'achievements',   // Shared achievements (all games)
        'rocen_xp',       // XP points
        'rocen_completed', // Completed modules
        'rocen_progress'  // Module progress
    ],

    // ==========================================
    // INITIALISATION
    // ==========================================

    async init() {
        this.injectStyles();

        try {
            const response = await fetch('/api/auth/me');
            const data = await response.json();

            if (data.authenticated) {
                this.loggedIn = true;
                this.username = data.username;
                await this.loadFromDatabase();
                this.startAutoSave();
            }
        } catch (e) {
            // Not logged in or network error — use localStorage only
            console.log('ProgressManager: Not logged in, using localStorage only.');
        }

        // Dispatch event so games know progress is ready
        window.dispatchEvent(new Event('progressReady'));
    },

    // ==========================================
    // LOAD FROM DATABASE
    // ==========================================

    async loadFromDatabase() {
        try {
            // Collect local data BEFORE loading from DB
            // This is so we can merge if both sources have data
            const localData = this.collectProgress();

            const response = await fetch('/api/progress/load');
            const data = await response.json();

            if (data.success && data.progress && Object.keys(data.progress).length > 0) {
                // DB has data
                const serverData = data.progress;

                if (Object.keys(localData).length > 0 && !sessionStorage.getItem('rocen_merged')) {
                    // Both DB and localStorage have data — merge them
                    // (keeps the best of each: highest scores, union of achievements, etc.)
                    try {
                        const mergeResponse = await fetch('/api/progress/merge', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ guest_progress: localData }),
                        });
                        const mergeResult = await mergeResponse.json();

                        if (mergeResult.success && mergeResult.merged) {
                            // Write merged data to localStorage
                            for (const [key, value] of Object.entries(mergeResult.merged)) {
                                if (this.SAVE_KEYS.includes(key)) {
                                    localStorage.setItem(key, JSON.stringify(value));
                                }
                            }
                            // Clear any keys in localStorage that aren't in the merged data
                            for (const key of this.SAVE_KEYS) {
                                if (!(key in mergeResult.merged)) {
                                    localStorage.removeItem(key);
                                }
                            }
                            sessionStorage.setItem('rocen_merged', 'true');
                            this.showSyncIndicator('✓ Progress merged');
                            console.log('ProgressManager: Merged local and server progress.');
                            return;
                        }
                    } catch (mergeErr) {
                        console.error('ProgressManager: Merge failed, using server data.', mergeErr);
                    }
                }

                // No merge needed, or merge failed — use server data (overwrite localStorage)
                for (const [key, value] of Object.entries(serverData)) {
                    if (this.SAVE_KEYS.includes(key)) {
                        localStorage.setItem(key, JSON.stringify(value));
                    }
                }
                // Clear any keys in localStorage that aren't in the server data
                // (they've been removed on another device)
                for (const key of this.SAVE_KEYS) {
                    if (!(key in serverData)) {
                        localStorage.removeItem(key);
                    }
                }
                sessionStorage.setItem('rocen_merged', 'true');
                this.showSyncIndicator('✓ Progress synced');
                console.log('ProgressManager: Loaded progress from database.');
            } else {
                // Database is empty — this might be a first login
                // Upload any localStorage data to the database
                if (Object.keys(localData).length > 0) {
                    await this.saveToDatabase();
                    sessionStorage.setItem('rocen_merged', 'true');
                    console.log('ProgressManager: Uploaded local progress to database.');
                }
            }
        } catch (e) {
            console.error('ProgressManager: Failed to load from database.', e);
        }
    },

    // ==========================================
    // COLLECT PROGRESS FROM LOCALSTORAGE
    // ==========================================

    collectProgress() {
        const progress = {};
        for (const key of this.SAVE_KEYS) {
            const value = localStorage.getItem(key);
            if (value !== null && value !== undefined) {
                try {
                    progress[key] = JSON.parse(value);
                } catch (e) {
                    progress[key] = value;
                }
            }
        }
        return progress;
    },

    // ==========================================
    // SAVE TO DATABASE
    // ==========================================

    async saveToDatabase() {
        if (!this.loggedIn || this.saving) return false;

        this.saving = true;
        const progress = this.collectProgress();

        // Don't save if there's nothing to save
        if (Object.keys(progress).length === 0) {
            this.saving = false;
            return true;
        }

        try {
            const response = await fetch('/api/progress/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ progress }),
            });
            const data = await response.json();

            if (data.success) {
                this.lastSaveTime = new Date();
                this.showSyncIndicator('✓ Progress saved');
                console.log('ProgressManager: Progress saved to database.');
                return true;
            } else {
                console.error('ProgressManager: Save failed.', data.error);
                this.showSyncIndicator('⚠ Save failed');
                return false;
            }
        } catch (e) {
            console.error('ProgressManager: Save error.', e);
            this.showSyncIndicator('⚠ Save failed');
            return false;
        } finally {
            this.saving = false;
        }
    },

    // ==========================================
    // PUBLIC API
    // ==========================================

    // Call this from game pages for manual saves
    async save() {
        return await this.saveToDatabase();
    },

    // ==========================================
    // AUTO-SAVE
    // ==========================================

    startAutoSave() {
        if (this.autoSaveInterval) return;
        this.autoSaveInterval = setInterval(() => {
            this.saveToDatabase();
        }, 60000); // Save every 60 seconds
        console.log('ProgressManager: Auto-save started (every 60s).');
    },

    stopAutoSave() {
        if (this.autoSaveInterval) {
            clearInterval(this.autoSaveInterval);
            this.autoSaveInterval = null;
            console.log('ProgressManager: Auto-save stopped.');
        }
    },

    // ==========================================
    // SYNC INDICATOR (floating toast)
    // ==========================================

    showSyncIndicator(message) {
        let indicator = document.getElementById('syncIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'syncIndicator';
            indicator.className = 'sync-indicator';
            document.body.appendChild(indicator);
        }
        indicator.textContent = message;
        indicator.classList.add('visible');

        // Hide after 3 seconds
        clearTimeout(this._hideTimeout);
        this._hideTimeout = setTimeout(() => {
            indicator.classList.remove('visible');
        }, 3000);
    },

    // ==========================================
    // INJECT STYLES
    // ==========================================

    injectStyles() {
        if (document.getElementById('sync-indicator-styles')) return;

        const style = document.createElement('style');
        style.id = 'sync-indicator-styles';
        style.textContent = `
            .sync-indicator {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: rgba(30, 51, 30, 0.95);
                color: #66BB6A;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.85rem;
                font-family: 'Inter', system-ui, sans-serif;
                font-weight: 600;
                border: 1px solid rgba(76, 175, 80, 0.3);
                opacity: 0;
                transform: translateY(10px);
                transition: opacity 0.3s ease, transform 0.3s ease;
                z-index: 10000;
                pointer-events: none;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }
            .sync-indicator.visible {
                opacity: 1;
                transform: translateY(0);
            }
            @media (max-width: 768px) {
                .sync-indicator {
                    bottom: 10px;
                    right: 10px;
                    font-size: 0.8rem;
                    padding: 0.4rem 0.8rem;
                }
            }
        `;
        document.head.appendChild(style);
    }
};

// ==========================================
// INITIALISE ON PAGE LOAD
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    ProgressManager.init();
});
