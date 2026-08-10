/* ═══════════════════════════════════════════════════════════════
   ROCEN HOMESTEADY — APIARY MANAGER
   ═══════════════════════════════════════════════════════════════

   TABLE OF CONTENTS
   ────────────────
   1.  Configuration & Constants
   2.  SVG Icon System
   3.  Sound System
   4.  Mentor System
   5.  Utility Functions
   6.  Game State & Defaults
   7.  Core Game Logic (init, render, save)
   8.  Hive Actions (inspect, smoke, feed, treat, etc.)
   9.  Market, Harvest & Processing
   10. Advance Week & Seasonal Events
   11. Achievements & Journal
   12. Visual System (SVG Hives, Gauges, Meadow, Calendar)
   13. Particle Canvas System
   14. Tab Switching & Initialization
   ═══════════════════════════════════════════════════════════════ */


/* ═══════════════════════════════════════════════════════════════
   1. CONFIGURATION & CONSTANTS
   ═══════════════════════════════════════════════════════════════ */

let CONFIG = null;

const SEASON_ICONS = {
    Spring: '🌸',
    Summer: '☀️',
    Autumn: '🍂',
    Winter: '❄️'
};

const HIVE_NAMES = [
    'Willow', 'Oak', 'Birch', 'Hazel', 'Ash', 'Elm',
    'Rowan', 'Holly', 'Ivy', 'Cedar', 'Pine', 'Maple',
    'Linden', 'Sycamore', 'Alder', 'Thorn'
];


/* ═══════════════════════════════════════════════════════════════
   2. SVG ICON SYSTEM
   Replaces emojis with proper inline SVG icons
   ═══════════════════════════════════════════════════════════════ */

const ApiaryIcons = {
    icon(name, size = 16) {
        const icons = {
            hive: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L8 6v4H4v4h4v4h4v4h4v-4h4v-4h-4V6z"/></svg>`,
            bee: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="14" rx="5" ry="6" fill="currentColor" opacity="0.2"/><ellipse cx="12" cy="14" rx="5" ry="6" stroke="currentColor" stroke-width="1.5"/><path d="M7 14h10M7 11.5h10M7 16.5h10" stroke="currentColor" stroke-width="1"/><ellipse cx="9" cy="7" rx="3" ry="4" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="1"/><ellipse cx="15" cy="7" rx="3" ry="4" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="1"/><circle cx="12" cy="13" r="1" fill="currentColor"/></svg>`,
            queen: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 18L7 6l5 8 5-8 4 12H3z" fill="currentColor" opacity="0.2"/><path d="M3 18L7 6l5 8 5-8 4 12H3z"/></svg>`,
            honey: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2h8v4l2 2v10a2 2 0 01-2 2H8a2 2 0 01-2-2V8l2-2V2z" fill="currentColor" opacity="0.2"/><path d="M8 2h8v4l2 2v10a2 2 0 01-2 2H8a2 2 0 01-2-2V8l2-2V2z"/><path d="M8 6h8M7 10h10M7 14h10"/></svg>`,
            varroa: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8" fill="currentColor" opacity="0.2"/><circle cx="12" cy="12" r="8"/><circle cx="10" cy="10" r="1.5" fill="currentColor"/><circle cx="14" cy="10" r="1.5" fill="currentColor"/><path d="M8 15c0 0 2 2 4 2s4-2 4-2" stroke="currentColor" stroke-width="1.5"/></svg>`,
            smoker: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 14l3-3 8 8-3 3z" fill="currentColor" opacity="0.2"/><path d="M4 14l3-3 8 8-3 3z"/><circle cx="18" cy="6" r="3" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M16 8l-3 3" stroke="currentColor" stroke-width="1.5"/><path d="M20 4c1-2 2-3 3-3" stroke="currentColor" stroke-width="1" opacity="0.5"/><path d="M18 2c0-1 0-2 1-2.5" stroke="currentColor" stroke-width="1" opacity="0.5"/></svg>`,
            calendar: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" fill="currentColor" opacity="0.1"/><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M7 13h2M11 13h2M15 13h2M7 17h2M11 17h2"/></svg>`,
            market: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 7l2-4h16l2 4v2H2V7z" fill="currentColor" opacity="0.2"/><path d="M2 7l2-4h16l2 4"/><rect x="3" y="9" width="4" height="11" rx="1"/><rect x="10" y="9" width="4" height="11" rx="1"/><rect x="17" y="9" width="4" height="11" rx="1"/><path d="M2 20h20"/></svg>`,
            warning: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L1 21h22L12 2z" fill="currentColor" opacity="0.2"/><path d="M12 2L1 21h22L12 2z"/><path d="M12 9v5M12 17h.01" stroke-width="2.5"/></svg>`,
            wasp: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="14" rx="4" ry="5" fill="currentColor" opacity="0.2"/><ellipse cx="12" cy="14" rx="4" ry="5"/><path d="M8 12h8M8 14.5h8M8 17h8" stroke="currentColor" stroke-width="1"/><path d="M8 9l-4-3M16 9l4-3" stroke="currentColor" stroke-width="1.5"/><circle cx="9" cy="8" r="2" stroke="currentColor" stroke-width="1"/><circle cx="15" cy="8" r="2" stroke="currentColor" stroke-width="1"/></svg>`,
            heft: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18" stroke="currentColor" stroke-width="2"/><path d="M5 12l1-4h12l1 4" fill="currentColor" opacity="0.15"/><path d="M5 12V9h14v3M5 12v3h14v-3" stroke="currentColor" stroke-width="1.5"/><path d="M4 15h16M7 9V7M17 9V7" stroke="currentColor" stroke-width="1.5"/></svg>`,
            processing: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9" fill="currentColor" opacity="0.1"/><circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2" stroke-width="2"/></svg>`,
            money: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9" fill="currentColor" opacity="0.2"/><circle cx="12" cy="12" r="9"/><text x="12" y="16" text-anchor="middle" font-size="10" font-weight="bold" fill="currentColor" stroke="none">£</text></svg>`,
            level: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 6h6l-5 4 2 6-6-4-6 4 2-6-5-4h6z" fill="currentColor" opacity="0.2"/><path d="M12 2l3 6h6l-5 4 2 6-6-4-6 4 2-6-5-4h6z"/></svg>`,
            population: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="7" cy="5" r="3" fill="currentColor" opacity="0.2"/><circle cx="7" cy="5" r="3"/><circle cx="17" cy="5" r="3" fill="currentColor" opacity="0.2"/><circle cx="17" cy="5" r="3"/><path d="M2 20v-2a4 4 0 014-4h2a4 4 0 014 4v2M12 20v-2a4 4 0 014-4h2a4 4 0 014 4v2" stroke-width="1.5"/></svg>`,
            stores: `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="8" width="18" height="13" rx="2" fill="currentColor" opacity="0.2"/><rect x="3" y="8" width="18" height="13" rx="2"/><path d="M3 8l3-4h12l3 4" stroke-width="1.5"/><path d="M9 8v5M15 8v5" stroke-width="1.5"/></svg>`
        };
        return icons[name] || `<span style="font-size:${size}px">?</span>`;
    }
};


/* ═══════════════════════════════════════════════════════════════
   3. SOUND SYSTEM
   Procedural audio using Web Audio API
   ═══════════════════════════════════════════════════════════════ */

const ApiarySound = {
    ctx: null,
    enabled: true,
    masterGain: null,
    _buzzNodes: null,
    _buzzGains: null,
    _rainNode: null,
    _rainGain: null,
    _windNode: null,
    _windLfo: null,
    _windGain: null,
    _initialized: false,

    /* ── Initialisation ── */

    init() {
        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            this.masterGain = this.ctx.createGain();
            this.masterGain.gain.value = 0.5;
            this.masterGain.connect(this.ctx.destination);
            this._initialized = true;

            const pref = localStorage.getItem('apiary_sound');
            if (pref === 'off') this.enabled = false;

            this.updateSoundButton();
            this._attachActivation();
        } catch (e) {
            console.log('Web Audio not available');
        }
    },

    resume() {
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    },

    _attachActivation() {
        if (!this._initialized) return;
        const activate = () => {
            if (this.ctx && this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
            document.removeEventListener('click', activate);
            document.removeEventListener('touchstart', activate);
            document.removeEventListener('keydown', activate);
            if (this.enabled && typeof apiary !== 'undefined' && apiary.state) {
                this.updateAmbient(apiary.state);
            }
        };
        document.addEventListener('click', activate, { once: true });
        document.addEventListener('touchstart', activate, { once: true });
        document.addEventListener('keydown', activate, { once: true });
    },

    toggle() {
        this.enabled = !this.enabled;
        localStorage.setItem('apiary_sound', this.enabled ? 'on' : 'off');
        if (this.enabled) {
            this.resume();
            if (typeof apiary !== 'undefined' && apiary.state) {
                this.updateAmbient(apiary.state);
            }
            this.playClick();
        } else {
            this.stopAll();
        }
        this.updateSoundButton();
    },

    updateSoundButton() {
        const btn = document.getElementById('sound-toggle');
        if (btn) {
            btn.innerHTML = this.enabled ? '🔊' : '🔇';
            btn.classList.toggle('muted', !this.enabled);
            btn.title = this.enabled ? 'Sound on — click to mute' : 'Sound off — click to enable';
        }
    },

    /* ── Ambient: Bee Buzz ── */

    startBuzz(population = 35000) {
        if (!this._initialized || !this.enabled) return;
        this.stopBuzz();

        const intensity = Math.min(1, population / 60000);
        const t = this.ctx.currentTime;

        // Base drone
        const osc1 = this.ctx.createOscillator();
        osc1.type = 'sawtooth';
        osc1.frequency.value = 120 + intensity * 30;

        // Harmonic
        const osc2 = this.ctx.createOscillator();
        osc2.type = 'sawtooth';
        osc2.frequency.value = 240 + intensity * 40;

        // Modulation
        const modOsc = this.ctx.createOscillator();
        modOsc.type = 'sine';
        modOsc.frequency.value = 3 + Math.random() * 2;
        const modGain = this.ctx.createGain();
        modGain.gain.value = 15;
        modOsc.connect(modGain);
        modGain.connect(osc1.frequency);

        // Noise layer
        const bufSize = this.ctx.sampleRate * 2;
        const noiseBuf = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const noiseData = noiseBuf.getChannelData(0);
        for (let i = 0; i < bufSize; i++) noiseData[i] = (Math.random() * 2 - 1) * 0.3;
        const noise = this.ctx.createBufferSource();
        noise.buffer = noiseBuf;
        noise.loop = true;

        const noiseFilter = this.ctx.createBiquadFilter();
        noiseFilter.type = 'bandpass';
        noiseFilter.frequency.value = 150;
        noiseFilter.Q.value = 2;

        // Mix
        const buzzGain = this.ctx.createGain();
        buzzGain.gain.value = intensity * 0.15;
        const harmGain = this.ctx.createGain();
        harmGain.gain.value = intensity * 0.08;
        const noiseGain = this.ctx.createGain();
        noiseGain.gain.value = intensity * 0.10;

        osc1.connect(buzzGain);
        osc2.connect(harmGain);
        noise.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        buzzGain.connect(this.masterGain);
        harmGain.connect(this.masterGain);
        noiseGain.connect(this.masterGain);

        osc1.start(t);
        osc2.start(t);
        modOsc.start(t);
        noise.start(t);

        this._buzzNodes = [osc1, osc2, modOsc, noise];
        this._buzzGains = [buzzGain, harmGain, noiseGain];
    },

    stopBuzz() {
        if (this._buzzNodes) {
            this._buzzNodes.forEach(n => { try { n.stop(); } catch (e) {} });
            this._buzzNodes = null;
        }
    },

    /* ── Ambient: Rain ── */

    startRain() {
        if (!this._initialized || !this.enabled) return;
        this.stopRain();

        const bufSize = this.ctx.sampleRate * 2;
        const buffer = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;
        noise.loop = true;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 800;
        filter.Q.value = 0.5;

        const gain = this.ctx.createGain();
        gain.gain.value = 0.12;

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.masterGain);
        noise.start();

        this._rainNode = noise;
        this._rainGain = gain;
    },

    stopRain() {
        if (this._rainNode) {
            try { this._rainNode.stop(); } catch (e) {}
            this._rainNode = null;
        }
    },

    /* ── Ambient: Wind ── */

    startWind() {
        if (!this._initialized || !this.enabled) return;
        this.stopWind();

        const bufSize = this.ctx.sampleRate * 3;
        const buffer = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;
        noise.loop = true;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 400;
        filter.Q.value = 0.3;

        const lfo = this.ctx.createOscillator();
        lfo.type = 'sine';
        lfo.frequency.value = 0.15;
        const lfoGain = this.ctx.createGain();
        lfoGain.gain.value = 200;
        lfo.connect(lfoGain);
        lfoGain.connect(filter.frequency);
        lfo.start();

        const gain = this.ctx.createGain();
        gain.gain.value = 0.08;

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.masterGain);
        noise.start();

        this._windNode = noise;
        this._windLfo = lfo;
        this._windGain = gain;
    },

    stopWind() {
        if (this._windNode) {
            try { this._windNode.stop(); } catch (e) {}
            this._windNode = null;
        }
        if (this._windLfo) {
            try { this._windLfo.stop(); } catch (e) {}
            this._windLfo = null;
        }
    },

    /* ── One-shot: Smoker Puff ── */

    playSmoker() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;
        const bufSize = this.ctx.sampleRate * 1.5;
        const buffer = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 600;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0, t);
        gain.gain.linearRampToValueAtTime(0.35, t + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.01, t + 1.5);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.masterGain);
        noise.start(t);
        noise.stop(t + 1.5);
    },

    /* ── One-shot: Achievement Chime ── */

    playAchievement() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;
        const notes = [523.25, 659.25, 783.99, 1046.50]; // C5 E5 G5 C6

        notes.forEach((freq, i) => {
            const osc = this.ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = freq;
            const gain = this.ctx.createGain();
            gain.gain.setValueAtTime(0, t + i * 0.12);
            gain.gain.linearRampToValueAtTime(0.25, t + i * 0.12 + 0.02);
            gain.gain.exponentialRampToValueAtTime(0.001, t + i * 0.12 + 0.5);
            osc.connect(gain);
            gain.connect(this.masterGain);
            osc.start(t + i * 0.12);
            osc.stop(t + i * 0.12 + 0.5);
        });
    },

    /* ── One-shot: Warning ── */

    playWarning() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;
        for (let i = 0; i < 3; i++) {
            const osc = this.ctx.createOscillator();
            osc.type = 'square';
            osc.frequency.value = 440;
            const gain = this.ctx.createGain();
            gain.gain.setValueAtTime(0.2, t + i * 0.25);
            gain.gain.exponentialRampToValueAtTime(0.001, t + i * 0.25 + 0.15);
            osc.connect(gain);
            gain.connect(this.masterGain);
            osc.start(t + i * 0.25);
            osc.stop(t + i * 0.25 + 0.15);
        }
    },

    /* ── One-shot: Harvest Pour ── */

    playHarvest() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;

        // Pouring noise
        const bufSize = this.ctx.sampleRate * 2;
        const buffer = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(2000, t);
        filter.frequency.exponentialRampToValueAtTime(300, t + 1.5);
        filter.Q.value = 1;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.15, t);
        gain.gain.linearRampToValueAtTime(0.25, t + 0.2);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 1.8);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.masterGain);
        noise.start(t);
        noise.stop(t + 2);

        // Sweet chime
        const osc = this.ctx.createOscillator();
        osc.type = 'sine';
        osc.frequency.value = 880;
        const oscGain = this.ctx.createGain();
        oscGain.gain.setValueAtTime(0.15, t + 0.3);
        oscGain.gain.exponentialRampToValueAtTime(0.001, t + 1.5);
        osc.connect(oscGain);
        oscGain.connect(this.masterGain);
        osc.start(t + 0.3);
        osc.stop(t + 1.5);
    },

    /* ── One-shot: Sting ── */

    playSting() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(800, t);
        osc.frequency.exponentialRampToValueAtTime(200, t + 0.3);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.3, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.4);

        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(t);
        osc.stop(t + 0.5);
    },

    /* ── One-shot: Click ── */

    playClick() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        osc.type = 'sine';
        osc.frequency.value = 600;
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.15, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.08);
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(t);
        osc.stop(t + 0.1);
    },

    /* ── One-shot: Inspection Buzz (2 seconds) ── */

    playInspectBuzz() {
        if (!this._initialized || !this.enabled) return;
        this.resume();

        const t = this.ctx.currentTime;

        const osc = this.ctx.createOscillator();
        osc.type = 'sawtooth';
        osc.frequency.value = 140;

        const lfo = this.ctx.createOscillator();
        lfo.type = 'sine';
        lfo.frequency.value = 5;
        const lfoGain = this.ctx.createGain();
        lfoGain.gain.value = 20;
        lfo.connect(lfoGain);
        lfoGain.connect(osc.frequency);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.06, t);
        gain.gain.linearRampToValueAtTime(0.10, t + 0.3);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 2);

        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(t);
        osc.stop(t + 2);
        lfo.start(t);
        lfo.stop(t + 2);
    },

    /* ── Ambient Update (called on render) ── */

    updateAmbient(state) {
        if (!this._initialized || !this.enabled) return;

        const weather = state ? state.weather : '☀️ Sunny';
        const season = ApiaryVisual ? ApiaryVisual.getSeason(state ? state.week : 13) : 'Spring';

        this.stopRain();
        this.stopWind();

        if (weather.includes('Rainy')) {
            this.startRain();
        } else if (weather.includes('Stormy')) {
            this.startRain();
            this.startWind();
        } else if (weather.includes('Cloudy') && season === 'Winter') {
            this.startWind();
        }
    },

    /* ── Stop All ── */

    stopAll() {
        this.stopBuzz();
        this.stopRain();
        this.stopWind();
    }
};
/* ═══════════════════════════════════════════════════════════════
   4. MENTOR SYSTEM
   Contextual tips for new players
   ═══════════════════════════════════════════════════════════════ */

const ApiaryMentor = {
    shownTips: new Set(),

    getTip(state) {
        if (!CONFIG || !CONFIG.mentor_tips) return null;
        const tips = CONFIG.mentor_tips;
        const week = state.week;
        const season = getSeason(getMonth(week));
        const hives = state.hives.filter(h => !h.dead);

        // ── Priority: contextual tips ──

        if (week <= 13 && !this.shownTips.has('first_week')) {
            this.shownTips.add('first_week');
            return tips.first_week;
        }

        if (hives.some(h => h.inspected_week > 0) && !this.shownTips.has('first_inspect')) {
            this.shownTips.add('first_inspect');
            return tips.first_inspect;
        }

        if (hives.some(h => h.temperament === 'defensive') && !this.shownTips.has('aggressive_hive')) {
            this.shownTips.add('aggressive_hive');
            return tips.aggressive_hive;
        }

        if (hives.some(h => h.queen_cells > 0) && !this.shownTips.has('swarm_warning')) {
            this.shownTips.add('swarm_warning');
            return tips.swarm_warning;
        }

        if (hives.some(h => h.varroa_count > 3) && !this.shownTips.has('varroa_warning')) {
            this.shownTips.add('varroa_warning');
            return tips.varroa_warning;
        }

        if (hives.some(h => h.honey_frames < 3) && !this.shownTips.has('low_stores')) {
            this.shownTips.add('low_stores');
            return tips.low_stores;
        }

        if (hives.some(h => h.has_foulbrood) && !this.shownTips.has('first_foulbrood')) {
            this.shownTips.add('first_foulbrood');
            return tips.first_foulbrood;
        }

        // ── Seasonal tips ──

        if (season === 'Spring' && !this.shownTips.has('first_spring')) {
            this.shownTips.add('first_spring');
            return tips.first_spring;
        }
        if (season === 'Summer' && !this.shownTips.has('first_summer')) {
            this.shownTips.add('first_summer');
            return tips.first_summer;
        }
        if (season === 'Autumn' && !this.shownTips.has('first_autumn')) {
            this.shownTips.add('first_autumn');
            return tips.first_autumn;
        }
        if (season === 'Winter' && !this.shownTips.has('first_winter')) {
            this.shownTips.add('first_winter');
            return tips.first_winter;
        }

        // ── Milestone tips ──

        if (state.total_harvests === 0 && hives.some(h => h.has_super && h.super_honey_frames >= 4) && !this.shownTips.has('first_harvest')) {
            this.shownTips.add('first_harvest');
            return tips.first_harvest;
        }

        if (state.level >= 3 && !this.shownTips.has('first_processing')) {
            this.shownTips.add('first_processing');
            return tips.first_processing;
        }

        if (state.level >= 4 && ['May', 'June', 'July'].includes(getMonth(week)) && !this.shownTips.has('first_swarm_catch')) {
            this.shownTips.add('first_swarm_catch');
            return tips.first_swarm_catch;
        }

        return null;
    },

    renderTip(state) {
        const tip = this.getTip(state);
        if (!tip) return '';
        return `
        <div class="mentor-tip" id="mentor-tip">
            <button class="mentor-dismiss" onclick="document.getElementById('mentor-tip').style.display='none'">&times;</button>
            <div class="mentor-content">
                <div class="mentor-avatar">🐝</div>
                <div class="mentor-text">${tip}</div>
            </div>
        </div>`;
    }
};


/* ═══════════════════════════════════════════════════════════════
   5. UTILITY FUNCTIONS
   Helpers for date, weather, storage, and UI
   ═══════════════════════════════════════════════════════════════ */

/* ── Toast Notification ── */

function showToast(msg, dur = 3000) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.remove('hidden');
    setTimeout(() => t.classList.add('hidden'), dur);
}

/* ── Local Storage ── */

function saveState(key, data) {
    try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) {}
}

function loadState(key, defaults) {
    try {
        const s = localStorage.getItem(key);
        if (s) return { ...defaults, ...JSON.parse(s) };
    } catch (e) {}
    return { ...defaults };
}

/* ── Date & Season ── */

function getMonth(week) {
    const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months[((week - 1) % 48) >> 2];
}

function getSeason(month) {
    if (!CONFIG) return 'Spring';
    const seasons = CONFIG.beekeeping_seasons;
    for (const [season, months] of Object.entries(seasons)) {
        if (months.includes(month)) return season;
    }
    return 'Spring';
}

function getWeekInMonth(week) {
    return ((week - 1) % 4) + 1;
}

/* ── Weather ── */

function getWeather(season) {
    if (!CONFIG) return { weather: '☀️ Sunny', temperature: 15 };
    const chances = CONFIG.weather_chances[season] || CONFIG.weather_chances['Spring'];
    const r = Math.random();
    let weather;
    if (r < chances.sunny) weather = '☀️ Sunny';
    else if (r < chances.sunny + chances.cloudy) weather = '⛅ Cloudy';
    else if (r < chances.sunny + chances.cloudy + chances.rainy) weather = '🌧️ Rainy';
    else weather = '⛈️ Stormy';

    const range = CONFIG.temp_range[season] || [10, 20];
    const temperature = Math.floor(Math.random() * (range[1] - range[0] + 1)) + range[0];
    return { weather, temperature };
}

/* ── Inspection Check ── */

function canInspect(weatherStr, temperature) {
    return !weatherStr.includes('Rainy') && !weatherStr.includes('Stormy') && temperature >= 14;
}


/* ═══════════════════════════════════════════════════════════════
   6. GAME STATE & DEFAULTS
   Hive factory, initial state, and save/load
   ═══════════════════════════════════════════════════════════════ */

/* ── Hive Factory ── */

function createHive(name, forceTemperament) {
    const temperaments = ['gentle', 'gentle', 'moderate', 'moderate', 'moderate', 'defensive'];
    const temperament = forceTemperament || temperaments[Math.floor(Math.random() * temperaments.length)];

    return {
        name: name,
        queen: 'present',
        population: 35000 + Math.floor(Math.random() * 8000) - 3000,
        honey_frames: 5,
        brood_frames: 4,
        pollen_frames: 2,
        has_super: false,
        super_honey_frames: 0,
        queen_cells: 0,
        varroa_count: Math.floor(Math.random() * 3) + 1,
        treated_this_year: false,
        fed_spring: false,
        fed_autumn: false,
        inspected_week: 0,
        age_weeks: 0,
        dead: false,
        death_reason: '',
        swarmed: false,
        has_foulbrood: false,
        has_mice_damage: false,
        has_mouse_guard: false,
        disease_free_weeks: 0,
        // Temperament & inspection
        temperament: temperament,
        smoked: false,
        stings_this_week: 0,
        wasp_damage: false,
        queen_mark_colour: null,
        entrance_reduced: false,
        inspection_quality: 1.0
    };
}

/* ── Default State ── */

const apiary = {
    defaults: {
        hives: [createHive('Willow')],
        week: 13,
        money: 100,
        level: 1,
        xp: 0,
        inventory: {},
        events: [],
        weather: '☀️ Sunny',
        temperature: 15,
        total_harvests: 0,
        colonies_overwintered: 0,
        varroa_good_seasons: 0,
        total_processed: 0,
        total_mead: 0,
        swarms_caught: 0,
        hive_names_used: ['Willow'],
        processing_queue: [],
        market_prices: {},
        achievements: {
            apiary_first_harvest: false,
            apiary_overwinter: false,
            apiary_keeper: false,
            apiary_5_hives: false,
            apiary_varroa: false,
            apiary_processor: false,
            apiary_mead_master: false,
            apiary_swarm_catcher: false,
            apiary_5_harvests: false,
            apiary_disease_free: false
        },
        selectedHive: null,
        selectedInspect: null,
        currentTab: 'overview',
        journal: [],
        smoker_used: false,
        _weatherSet: false
    },

    state: null,

    /* ── Computed Properties ── */

    get activeHives() { return this.state.hives.filter(h => !h.dead); },
    get currentMonth() { return getMonth(this.state.week); },
    get currentSeason() { return getSeason(this.currentMonth); },
    get nectarInfo() {
        return (CONFIG && CONFIG.nectar_flow)
            ? CONFIG.nectar_flow[this.currentMonth] || { flow: 0, source: 'None', honey_type: null }
            : { flow: 0, source: 'None', honey_type: null };
    },
    get maxHives() { return this.state.level + 1; },

    /* ── Save ── */

    save() {
        saveState('apiary_state', this.state);
    },

    /* ── Market Prices ── */

    getMarketPrice(product) {
        const base = CONFIG && CONFIG.apiary_products && CONFIG.apiary_products[product]
            ? CONFIG.apiary_products[product].value : 5;
        if (!this.state.market_prices[product]) this.state.market_prices[product] = base;
        return this.state.market_prices[product];
    },

    fluctuatePrices() {
        if (!CONFIG || !CONFIG.apiary_products) return;
        for (const [name, data] of Object.entries(CONFIG.apiary_products)) {
            const base = data.value;
            const current = this.state.market_prices[name] || base;
            const change = (Math.random() - 0.5) * base * 0.3;
            const newPrice = Math.max(
                Math.floor(base * 0.5),
                Math.min(Math.ceil(base * 1.8), Math.round(current + change))
            );
            this.state.market_prices[name] = newPrice;
        }
    },

    /* ── Journal ── */

    addJournal(text, type = 'normal') {
        if (!this.state.journal) this.state.journal = [];
        this.state.journal.push({ week: this.state.week, text, type });
        if (this.state.journal.length > 100) {
            this.state.journal = this.state.journal.slice(-100);
        }
    },

        /* ═══════════════════════════════════════════════════════════
       7. CORE GAME LOGIC
       Initialisation, rendering loop, and state management
       ═══════════════════════════════════════════════════════════ */

    /* ── Initialisation ── */

    init() {
        this.state = loadState('apiary_state', this.defaults);

        // ── State migrations (ensure new properties exist) ──
        for (const key of ['total_harvests', 'colonies_overwintered', 'varroa_good_seasons', 'hive_names_used']) {
            if (!(key in this.state)) {
                this.state[key] = key === 'hive_names_used' ? ['Willow'] : 0;
            }
        }
        if (!this.state.achievements) {
            this.state.achievements = {
                apiary_first_harvest: false, apiary_overwinter: false,
                apiary_keeper: false, apiary_5_hives: false,
                apiary_varroa: false, apiary_processor: false,
                apiary_mead_master: false, apiary_swarm_catcher: false,
                apiary_5_harvests: false, apiary_disease_free: false
            };
        }
        if (!this.state.total_processed) this.state.total_processed = 0;
        if (!this.state.total_mead) this.state.total_mead = 0;
        if (!this.state.swarms_caught) this.state.swarms_caught = 0;
        if (!this.state.processing_queue) this.state.processing_queue = [];
        if (!this.state.market_prices) this.state.market_prices = {};
        if (!this.state.journal) this.state.journal = [];
        if (!this.state.smoker_used) this.state.smoker_used = false;

        // ── Hive property migrations ──
        for (const h of this.state.hives) {
            if (h.has_foulbrood === undefined) h.has_foulbrood = false;
            if (h.has_mice_damage === undefined) h.has_mice_damage = false;
            if (h.has_mouse_guard === undefined) h.has_mouse_guard = false;
            if (h.disease_free_weeks === undefined) h.disease_free_weeks = 0;
            if (h.temperament === undefined) h.temperament = ['gentle', 'moderate', 'moderate'][Math.floor(Math.random() * 3)];
            if (h.smoked === undefined) h.smoked = false;
            if (h.stings_this_week === undefined) h.stings_this_week = 0;
            if (h.wasp_damage === undefined) h.wasp_damage = false;
            if (h.queen_mark_colour === undefined) h.queen_mark_colour = null;
            if (h.entrance_reduced === undefined) h.entrance_reduced = false;
        }

        // ── Sound system ──
        ApiarySound.init();

        // ── Fetch config and render ──
        fetch('/api/games/apiary/config').then(r => r.json()).then(cfg => {
            CONFIG = cfg;

            const month = getMonth(this.state.week);
            const season = getSeason(month);
            if (!this.state._weatherSet) {
                const w = getWeather(season);
                this.state.weather = w.weather;
                this.state.temperature = w.temperature;
                this.state._weatherSet = true;
            }

            this.save();
            this.render();
        });
    },

    /* ── Main Render ── */

    render() {
        this.renderStats();
        this.renderNectar();
        this.renderEvents();
        this.renderWarnings();

        const mentorEl = document.getElementById('mentor-area');
        if (mentorEl) mentorEl.innerHTML = ApiaryMentor.renderTip(this.state);

        this.renderTab(this.state.currentTab || 'overview');
        this.renderAdvance();
        this.renderAchievements();
        this.renderJournal();

        // Visual theming
        const season = ApiaryVisual.getSeason(this.state.week);
        ApiaryVisual.applySeason(season);
        ApiaryVisual.renderWeatherParticles(this.state.weather);
        ApiaryVisual.renderSeasonParticles(season);

        // Sound
        ApiarySound.updateAmbient(this.state);
    },

    /* ── Stats Bar ── */

    renderStats() {
        const s = this.state;
        const month = this.currentMonth;
        const season = this.currentSeason;
        const icon = SEASON_ICONS[season] || '🌸';
        const total = this.activeHives.length;
        const levelUnlocks = CONFIG && CONFIG.level_unlocks ? CONFIG.level_unlocks : {};
        const currentUnlock = levelUnlocks[s.level] || { label: 'Beginner', max_hives: s.level + 1 };

        document.getElementById('apiary-stats').innerHTML = `
            <div class="stat-box season"><div class="stat-label">${icon} SEASON</div><div class="stat-value">${season}</div></div>
            <div class="stat-box weather"><div class="stat-label">📅 Month</div><div class="stat-value">${month.substring(0, 3)} Wk${getWeekInMonth(s.week)}</div></div>
            <div class="stat-box weather"><div class="stat-label">${s.weather}</div><div class="stat-value">${s.temperature}°C</div></div>
            <div class="stat-box hives"><div class="stat-label">🐝 Hives</div><div class="stat-value">${total} alive</div></div>
            <div class="stat-box money"><div class="stat-label">💰 Money</div><div class="stat-value">£${s.money}</div></div>
            <div class="stat-box level"><div class="stat-label">⭐ Level ${s.level}</div><div class="stat-value">${currentUnlock.label} (${s.xp} XP)</div></div>
        `;

        document.getElementById('apiary-season-bar').innerHTML =
            `<div class="season-bar">${icon} ${season} — ${month} Week ${getWeekInMonth(s.week)}</div>`;
    },

    /* ── Nectar Flow ── */

    renderNectar() {
        const el = document.getElementById('apiary-nectar');
        const n = this.nectarInfo;

        if (n.flow > 0) {
            const stars = '⭐'.repeat(n.flow);
            const honeyType = n.honey_type
                ? `<span style="color: var(--amber); margin-left: 0.5rem;">🍯 Honey type: <b>${n.honey_type}</b></span>`
                : '';
            el.innerHTML = `<div class="nectar-box flow"><span style="color: var(--green-leaf); font-weight: 600;">🌸 Nectar Flow:</span> <span style="color: var(--cream);">${n.source} (Strength: ${stars})</span>${honeyType}</div>`;
        } else {
            el.innerHTML = `<div class="nectar-box no-flow"><span style="color: var(--cream-dim);">❄️ No significant nectar flow this month. Bees rely on stores.</span></div>`;
        }
    },

    /* ── Recent Events ── */

    renderEvents() {
        const el = document.getElementById('apiary-events');
        if (this.state.events && this.state.events.length > 0) {
            const recent = this.state.events.slice(-5);
            el.innerHTML = `<div class="events-box"><div style="color: var(--green-light); font-weight: 600; font-size: 0.9rem; margin-bottom: 0.3rem;">📋 Recent Events</div>${recent.map(e => `<div class="ev-item">${e}</div>`).join('')}</div>`;
        } else {
            el.innerHTML = '';
        }
    },

    /* ── Warnings ── */

    renderWarnings() {
        const el = document.getElementById('apiary-warnings');
        const month = this.currentMonth;
        let html = '';

        // Swarm season
        if (['April', 'May', 'June'].includes(month)) {
            html += `<div class="warning-box swarm"><span style="color: var(--amber); font-weight: 600;">⚠️ Swarm Season!</span> <span style="color: var(--cream-dim);">Check for queen cells every week.</span></div>`;
        }

        // Varroa treatment
        if (month === 'August') {
            html += `<div class="warning-box varroa"><span style="color: var(--danger); font-weight: 600;">⚠️ Varroa Treatment Month!</span> <span style="color: var(--cream-dim);">Apply treatment now.</span></div>`;
        }

        // Winter
        if (this.currentSeason === 'Winter') {
            html += `<div class="warning-box winter"><span style="color: #2196F3; font-weight: 600;">❄️ Winter:</span> <span style="color: var(--cream-dim);">No inspections. Heft hives. Apply oxalic acid in December.</span></div>`;
        }

        // Foulbrood
        const foulbroodHives = this.activeHives.filter(h => h.has_foulbrood);
        if (foulbroodHives.length > 0) {
            html += `<div class="warning-box varroa"><span style="color: var(--danger); font-weight: 600;">🦠 Foulbrood!</span> <span style="color: var(--cream-dim);">${foulbroodHives.map(h => h.name).join(', ')} — Treat immediately!</span></div>`;
        }

        // Mice
        const miceHives = this.activeHives.filter(h => h.has_mice_damage);
        if (miceHives.length > 0) {
            html += `<div class="warning-box winter"><span style="color: #FF9800; font-weight: 600;">🐭 Mouse Damage!</span> <span style="color: var(--cream-dim);">${miceHives.map(h => h.name).join(', ')} — Consider fitting mouse guards.</span></div>`;
        }

        // Wasps
        const waspHives = this.activeHives.filter(h => h.wasp_damage);
        if (waspHives.length > 0) {
            html += `<div class="wasp-warning"><span style="font-weight: 600;">${ApiaryIcons.icon('wasp', 16)} Wasp Attack!</span> <span style="color: var(--cream);">${waspHives.map(h => h.name).join(', ')} — Reduce entrance size and check stores.</span></div>`;
        }

        // General wasp warning in late summer
        if (['August', 'September'].includes(month) && waspHives.length === 0) {
            html += `<div class="warning-box" style="background: #3e1a00; border: 1px solid #ff6d00; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;"><span style="color: #ff6d00; font-weight: 600;">${ApiaryIcons.icon('wasp', 16)} Wasp Season!</span> <span style="color: var(--cream-dim);">Wasps are active. Weak hives are at risk — reduce entrances.</span></div>`;
        }

        // Entrance reduced indicator
        const reducedHives = this.activeHives.filter(h => h.entrance_reduced);
        if (reducedHives.length > 0 && ['August', 'September', 'October'].includes(month)) {
            html += `<div class="status-good" style="font-size: 0.85rem;">🪱 Entrance reduced: ${reducedHives.map(h => h.name).join(', ')}</div>`;
        }

        el.innerHTML = html;
    },

    /* ── Tab Rendering ── */

    renderTab(tab) {
        this.state.currentTab = tab;
        document.querySelectorAll('.sub-tab').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.sub-tab-content').forEach(c => c.classList.remove('active'));

        const btn = document.querySelector(`.sub-tab[onclick*="${tab}"]`);
        if (btn) btn.classList.add('active');
        const content = document.getElementById(`tab-${tab}`);
        if (content) content.classList.add('active');

        if (tab === 'overview') ApiaryVisual.renderOverview(this.state);
        else if (tab === 'inspect') ApiaryVisual.renderInspect(this.state);
        else if (tab === 'actions') this.renderActions();
        else if (tab === 'market') this.renderMarket();
        else if (tab === 'meadow') ApiaryVisual.renderMeadow(this.state);
        else if (tab === 'calendar') ApiaryVisual.renderCalendar(this.state);
    },


    /* ═══════════════════════════════════════════════════════════
       8. HIVE ACTIONS
       Inspect, smoke, feed, treat, supers, swarm control
       ═══════════════════════════════════════════════════════════ */

    /* ── Hive Selection ── */

    selectHive(name) {
        this.state.selectedHive = name;
        this.renderTab('inspect');
    },

    actionSelectHive() {
        const sel = document.getElementById('action-hive-select');
        if (sel) this.state.selectedHive = sel.value;
        this.save();
        this.renderActions();
    },

    doInspectSelect() {
        const sel = document.getElementById('inspect-select');
        if (sel) this.state.selectedInspect = sel.value;
        this.save();
        this.renderInspect();
    },

    /* ── Temperament Badge ── */

    _temperamentBadge(temp) {
        const badges = { gentle: '🕊️ Gentle', moderate: '🐝 Moderate', defensive: '😠 Defensive' };
        return badges[temp] || temp;
    },

    /* ── Smoke Hive ── */

    smokeHive(name) {
        const hive = this.state.hives.find(h => h.name === name && !h.dead);
        if (!hive) return;

        const cost = CONFIG && CONFIG.smoker_config ? CONFIG.smoker_config.cost : 2;
        if (this.state.money < cost) { showToast(`Need £${cost} for smoker fuel!`); return; }
        if (hive.smoked) { showToast('Already smoked this week.'); return; }

        this.state.money -= cost;
        hive.smoked = true;
        this.state.smoker_used = true;

        ApiarySound.playSmoker();
        this._showSmokeAnimation(hive.name);

        this.addJournal(`💨 Smoked '${hive.name}' (£${cost})`, 'normal');
        this.state.xp += 1;
        this.save();
        this.render();
        showToast(`💨 Smoker applied to '${hive.name}' — safer inspection! +1 XP`);
    },

    _showSmokeAnimation(hiveName) {
        const cards = document.querySelectorAll('.hive-card-visual, .hive-detail-visual');
        cards.forEach(card => {
            for (let i = 0; i < 5; i++) {
                const puff = document.createElement('div');
                puff.className = 'smoke-puff';
                puff.style.left = (40 + Math.random() * 60) + '%';
                puff.style.top = (30 + Math.random() * 20) + '%';
                puff.style.animationDelay = (i * 0.15) + 's';
                puff.style.transform = `scale(${0.5 + Math.random() * 0.5})`;
                card.style.position = 'relative';
                card.appendChild(puff);
                setTimeout(() => puff.remove(), 3000);
            }
        });
    },

    /* ── Heft Hive (Winter) ── */

    heftHive(name) {
        const hive = this.state.hives.find(h => h.name === name && !h.dead);
        if (!hive) return;

        const totalStores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
        let weightEstimate, storesDesc;

        if (totalStores >= 8) {
            weightEstimate = 'Very heavy';
            storesDesc = 'Plenty of stores — this colony should survive winter.';
        } else if (totalStores >= 5) {
            weightEstimate = 'Heavy';
            storesDesc = 'Adequate stores, but check again in a couple of weeks.';
        } else if (totalStores >= 3) {
            weightEstimate = 'Moderate';
            storesDesc = 'Stores are getting low. Consider feeding fondant or syrup.';
        } else {
            weightEstimate = 'Light — DANGER';
            storesDesc = 'Very light! This colony may not survive without emergency feeding!';
        }

        const noise = Math.floor(Math.random() * 3) - 1;
        const estimatedFrames = Math.max(0, totalStores + noise);

        this.addJournal(
            `⚖️ Hefted '${hive.name}' — feels ${weightEstimate.toLowerCase()}`,
            totalStores < 4 ? 'danger' : 'normal'
        );
        this.state.xp += 1;
        this.save();
        this.render();
        showToast(`⚖️ Hefted '${hive.name}': ${weightEstimate}. ~${estimatedFrames} frames of stores.`);
    },

    /* ── Inspect Hive ── */

    inspectHive(name) {
        const hive = this.state.hives.find(h => h.name === name && !h.dead);
        if (!hive) return;
        if (!canInspect(this.state.weather, this.state.temperature)) {
            showToast('Cannot inspect in this weather!');
            return;
        }

        const smokerConfig = CONFIG && CONFIG.smoker_config ? CONFIG.smoker_config : null;
        const temperConfig = CONFIG && CONFIG.hive_temperaments ? CONFIG.hive_temperaments : {};
        const temp = hive.temperament || 'moderate';
        const tempData = temperConfig[temp] || { label: temp };
        const month = this.currentMonth;

        // ── Sting check ──
        let stung = false;
        if (smokerConfig) {
            const stingChances = hive.smoked
                ? smokerConfig.sting_chance_with_smoke
                : smokerConfig.sting_chance_no_smoke;
            const stingChance = stingChances[temp] || 0.1;
            if (Math.random() < stingChance) {
                stung = true;
                hive.stings_this_week = (hive.stings_this_week || 0) + 1;
                ApiarySound.playSting();
            }
        }

        // ── Inspection quality ──
        if (hive.smoked && smokerConfig) {
            hive.inspection_quality = 1.0 + smokerConfig.inspection_quality_bonus;
        } else {
            hive.inspection_quality = temp === 'gentle' ? 0.9 : temp === 'moderate' ? 0.7 : 0.4;
        }

        hive.inspected_week = this.state.week;
        hive.swarmed = false;

        // ── Queen cells ──
        if (['April', 'May', 'June'].includes(month) && hive.queen === 'present') {
            if (hive.population > 20000 && Math.random() < 0.35) {
                const detected = Math.random() < hive.inspection_quality;
                if (detected) {
                    hive.queen_cells = Math.floor(Math.random() * 4) + 2;
                } else {
                    hive.queen_cells = Math.max(hive.queen_cells, Math.floor(Math.random() * 2) + 1);
                }
            } else {
                hive.queen_cells = Math.max(0, hive.queen_cells - 1);
            }
        }

        // ── Varroa ──
        if (['April', 'May', 'June', 'July', 'August'].includes(month)) {
            if (!hive.treated_this_year) {
                hive.varroa_count = Math.min(15, hive.varroa_count + Math.floor(Math.random() * 3));
            }
        }

        // ── Education fact ──
        let factText = null;
        if (CONFIG && CONFIG.education_facts) {
            const facts = CONFIG.education_facts;
            let factCategory = null;

            if (hive.queen === 'failing') factCategory = 'queen_failing';
            else if (hive.queen === 'present') factCategory = 'queen_present';
            else if (hive.varroa_count > 6) factCategory = 'varroa_high';
            else if (hive.varroa_count > 3) factCategory = 'varroa_low';
            else if (['April', 'May', 'June'].includes(month)) factCategory = 'swarm_season';
            else if (this.currentSeason === 'Winter') factCategory = 'winter';
            else {
                const stores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
                if (stores >= 7) factCategory = 'honey_stores_good';
                else if (stores < 4) factCategory = 'honey_stores_low';
                else if (hive.has_super) factCategory = 'super';
            }

            if (factCategory && facts[factCategory]) {
                factText = facts[factCategory][Math.floor(Math.random() * facts[factCategory].length)];
            }
        }
        this.state._lastEduFact = factText;

        // ── XP ──
        let xpGain = stung ? 1 : 2;
        this.state.xp += xpGain;
        this.state.selectedInspect = name;

        ApiarySound.playInspectBuzz();

        this.addJournal(
            `${stung ? '🩸 ' : '🔍 '}Inspected '${hive.name}' — ${tempData.label || temp} colony${stung ? ' — OUCH! Got stung!' : ''}${hive.smoked ? ' (smoked)' : ' (no smoker)'}`,
            stung ? 'danger' : 'normal'
        );

        this.save();
        this.render();

        if (stung) {
            showToast('🩸 Got stung! Use a smoker next time! +1 XP');
        } else {
            showToast('Hive inspected! +2 XP');
        }
    },

    /* ── Reduce Entrance (wasp defence) ── */

    reduceEntrance(name) {
        const hive = this.state.hives.find(h => h.name === name && !h.dead);
        if (!hive) return;

        hive.entrance_reduced = true;
        this.state.events.push(`🪱 Entrance reduced on '${hive.name}' — wasp defence.`);
        this.addJournal(`🪱 Reduced entrance on '${hive.name}'`, 'important');
        this.state.xp += 1;
        this.save();
        this.render();
        showToast('Entrance reduced — wasps will struggle to enter!');
    },

    /* ── Mouse Guard ── */

    buyMouseGuard() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || hive.has_mouse_guard || this.state.money < 5) return;

        this.state.money -= 5;
        hive.has_mouse_guard = true;
        this.state.events.push(`🐭 Mouse guard fitted on '${hive.name}'.`);
        this.state.xp += 1;
        this.save();
        this.render();
        showToast('Mouse guard fitted! +1 XP');
    },

    /* ── Treat Foulbrood ── */

    treatFoulbrood() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || !hive.has_foulbrood || this.state.money < 25) return;

        this.state.money -= 25;
        hive.has_foulbrood = false;
        hive.brood_frames = Math.max(1, hive.brood_frames - 2);
        this.state.events.push(`🦠 Foulbrood treatment applied to '${hive.name}'. Some brood removed.`);
        this.state.xp += 5;
        this.save();
        this.render();
        showToast('Foulbrood treated! -£25');
    },

    /* ── Add Super ── */

    addSuper() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || hive.has_super || this.state.money < 15) return;

        this.state.money -= 15;
        hive.has_super = true;
        hive.super_honey_frames = 0;
        this.state.events.push(`📦 Super added to '${hive.name}'.`);
        this.save();
        this.render();
        showToast('Super added!');
    },

    /* ── Feeding ── */

    feedSpring() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || this.state.money < 3 || hive.fed_spring || this.currentSeason !== 'Spring') return;

        this.state.money -= 3;
        hive.fed_spring = true;
        hive.honey_frames = Math.min(11, hive.honey_frames + 2);
        this.state.events.push(`🫗 Fed spring syrup to '${hive.name}'. +2 frames stores.`);
        this.save();
        this.render();
        showToast('+2 frames stores');
    },

    feedAutumn() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || this.state.money < 3 || hive.fed_autumn || this.currentSeason !== 'Autumn') return;

        this.state.money -= 3;
        hive.fed_autumn = true;
        hive.honey_frames = Math.min(11, hive.honey_frames + 3);
        this.state.events.push(`🍯 Fed autumn syrup to '${hive.name}'. +3 frames stores.`);
        this.save();
        this.render();
        showToast('+3 frames stores');
    },

    feedFondant() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || this.state.money < 4) return;

        this.state.money -= 4;
        hive.honey_frames = Math.min(11, hive.honey_frames + 1);
        this.state.events.push(`🍬 Fed fondant to '${hive.name}'. +1 frame stores.`);
        this.save();
        this.render();
        showToast('+1 frame stores');
    },

    /* ── Varroa Treatment ── */

    treatVarroa(cost) {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || this.state.money < cost || hive.treated_this_year) return;

        this.state.money -= cost;
        hive.treated_this_year = true;
        hive.varroa_count = Math.max(0, hive.varroa_count - 5);
        this.state.events.push(`💊 Varroa treatment applied to '${hive.name}'.`);
        this.state.xp += 5;

        if (!this.state.achievements.apiary_varroa) {
            this.state.achievements.apiary_varroa = true;
            showToast('🏅 Achievement Unlocked: Mite Fighter!');
        }

        this.save();
        this.render();
    },

    /* ── Swarm Control: Split Colony ── */

    splitColony() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive) return;

        const total = this.activeHives.length;
        if (hive.queen_cells < 2 || hive.population <= 20000 || total >= this.maxHives) return;

        let newName = HIVE_NAMES[Math.floor(Math.random() * HIVE_NAMES.length)];
        while (this.state.hive_names_used.includes(newName)) {
            newName += Math.floor(Math.random() * 9 + 2);
        }
        this.state.hive_names_used.push(newName);

        const newHive = createHive(newName);
        newHive.population = Math.floor(hive.population / 2);
        newHive.queen = 'virgin';
        newHive.honey_frames = 4;
        newHive.brood_frames = 3;

        hive.population = Math.floor(hive.population / 2);
        hive.queen_cells = 0;

        this.state.hives.push(newHive);
        this.state.events.push(`✂️ Split '${hive.name}' → new colony '${newName}'!`);
        this.state.xp += 10;
        this.save();
        this.render();
        showToast(`Split! New colony '${newName}' created!`);
    },

    /* ── Swarm Control: Remove Queen Cells ── */

    removeQueenCells() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || hive.queen_cells <= 0) return;

        hive.queen_cells = 0;
        this.state.events.push(`🔪 Queen cells removed from '${hive.name}'.`);
        this.save();
        this.render();
        showToast('Queen cells removed!');
    },

    /* ── Requeen ── */

    requeen() {
        const hive = this.activeHives.find(h => h.name === this.state.selectedHive);
        if (!hive || this.state.money < 30) return;

        this.state.money -= 30;
        hive.queen = 'present';
        hive.population = Math.max(hive.population, 15000);

        // Mark the new queen with this year's colour
        const year = 2024 + Math.floor((this.state.week - 1) / 48);
        const markColours = CONFIG && CONFIG.queen_mark_colours ? CONFIG.queen_mark_colours : {
            '2024': { colour: '#1E88E5', name: 'Blue' },
            '2025': { colour: '#FDD835', name: 'Yellow' }
        };
        const yearStr = String(year);
        const markData = markColours[yearStr] || { colour: '#E0E0E0', name: 'White' };
        hive.queen_mark_colour = markData.colour;

        this.state.events.push(`👑 New queen introduced to '${hive.name}' (marked ${markData.name}).`);
        this.addJournal(`👑 New queen introduced to '${hive.name}' — marked ${markData.name} (${yearStr})`, 'success');
        this.state.xp += 5;
        ApiarySound.playClick();
        this.save();
        this.render();
        showToast(`New queen introduced! Marked ${markData.name} (${yearStr})`);
    },

    /* ── Remove Dead Hive ── */

    removeDeadHive(name) {
        this.state.hives = this.state.hives.filter(h => h.name !== name);
        this.save();
        this.render();
    },

    /* ── Buy New Hive ── */

    buyHive() {
        const cost = 75;
        if (this.state.money < cost || this.activeHives.length >= this.maxHives) {
            if (this.state.money < cost) showToast('Need £75!');
            else showToast(`Maximum ${this.maxHives} hives at Level ${this.state.level}`);
            return;
        }

        this.state.money -= cost;

        let newName = HIVE_NAMES[Math.floor(Math.random() * HIVE_NAMES.length)];
        while (this.state.hive_names_used.includes(newName)) {
            newName += Math.floor(Math.random() * 9 + 2);
        }
        this.state.hive_names_used.push(newName);

        const newHiveObj = createHive(newName);
        this.state.hives.push(newHiveObj);

        const tempLabel = (CONFIG && CONFIG.hive_temperaments && CONFIG.hive_temperaments[newHiveObj.temperament])
            ? CONFIG.hive_temperaments[newHiveObj.temperament].label
            : newHiveObj.temperament;

        this.state.events.push(`🐝 New colony '${newName}' installed! (${tempLabel})`);
        this.addJournal(`🐝 New colony '${newName}' — ${newHiveObj.temperament} temperament`, 'success');
        this.save();
        this.render();
        showToast(`New hive '${newName}' installed!`);
    },

    /* ── Catch Swarm ── */

    catchSwarm() {
        const total = this.activeHives.length;
        if (total >= this.state.level + 1) {
            showToast(`Maximum ${this.state.level + 1} hives at Level ${this.state.level}`);
            return;
        }

        const chance = 0.4;
        if (Math.random() > chance) {
            this.state.events.push('🪤 Swarm escaped — better luck next time!');
            this.state.xp += 2;
            this.save();
            this.render();
            showToast('The swarm got away! +2 XP for trying');
            return;
        }

        let newName = HIVE_NAMES[Math.floor(Math.random() * HIVE_NAMES.length)];
        while (this.state.hive_names_used.includes(newName)) {
            newName += Math.floor(Math.random() * 9 + 2);
        }
        this.state.hive_names_used.push(newName);

        const newHive = createHive(newName);
        newHive.population = 15000 + Math.floor(Math.random() * 5000);
        newHive.queen = 'virgin';
        newHive.temperament = 'defensive';
        newHive.honey_frames = 3;
        newHive.brood_frames = 2;
        newHive.pollen_frames = 1;

        this.state.hives.push(newHive);
        this.state.swarms_caught++;
        this.state.events.push(`🪤 Caught a swarm! New colony '${newName}' installed!`);
        this.state.xp += 15;

        if (!this.state.achievements.apiary_swarm_catcher) {
            this.state.achievements.apiary_swarm_catcher = true;
            showToast('🏅 Achievement Unlocked: Swarm Catcher!');
        }

        this.save();
        this.render();
        showToast(`Caught a swarm! Welcome '${newName}'!`);
    },
    /* ═══════════════════════════════════════════════════════════
       9. MARKET, HARVEST & PROCESSING
       ═══════════════════════════════════════════════════════════ */

    /* ── Start Processing ── */

    startProcessing(productName) {
        if (!CONFIG || !CONFIG.apiary_processing) { showToast('Processing not available'); return; }

        const recipe = CONFIG.apiary_processing[productName];
        if (!recipe) { showToast('Unknown product'); return; }

        for (const [ingredient, qty] of Object.entries(recipe.ingredients)) {
            if (!this.state.inventory[ingredient] || this.state.inventory[ingredient] < qty) {
                showToast(`Need ${qty}x ${ingredient}`);
                return;
            }
        }

        for (const [ingredient, qty] of Object.entries(recipe.ingredients)) {
            this.state.inventory[ingredient] -= qty;
            if (this.state.inventory[ingredient] <= 0) delete this.state.inventory[ingredient];
        }

        this.state.processing_queue.push({
            product: productName,
            startWeek: this.state.week,
            weeksNeeded: recipe.weeks,
            done: false
        });

        this.state.events.push(`⚗️ Started making ${productName} (${recipe.weeks} weeks)`);
        this.save();
        this.render();
        showToast(`Processing ${productName} — ready in ${recipe.weeks} weeks`);
    },

    /* ── Harvest Honey ── */

    harvest(hiveName) {
        const hive = this.state.hives.find(h => h.name === hiveName && !h.dead);
        if (!hive || !hive.has_super || hive.super_honey_frames < 4) return;

        const nectar = this.nectarInfo;
        const honeyType = nectar.honey_type || 'Summer Wildflower';
        const jars = Math.max(1, Math.floor(hive.super_honey_frames * 1.5));

        this.state.inventory[honeyType] = (this.state.inventory[honeyType] || 0) + jars;
        this.state.inventory['Beeswax'] = (this.state.inventory['Beeswax'] || 0) + Math.max(1, Math.floor(hive.super_honey_frames / 3));

        hive.has_super = false;
        hive.super_honey_frames = 0;
        hive.honey_frames = Math.max(0, hive.honey_frames - 2);

        this.state.total_harvests++;
        this.state.xp += 15;
        this.state.events.push(`🍯 Harvested ${jars} jars of ${honeyType} from '${hive.name}'!`);
        this.addJournal(`🍯 Harvested ${jars} jars of ${honeyType} from '${hive.name}'`, 'success');
        ApiarySound.playHarvest();

        if (!this.state.achievements.apiary_first_harvest) {
            this.state.achievements.apiary_first_harvest = true;
            showToast('🏅 Achievement Unlocked: First Harvest!');
        }
        if (this.state.total_harvests >= 5 && !this.state.achievements.apiary_5_harvests) {
            this.state.achievements.apiary_5_harvests = true;
            showToast('🏅 Achievement Unlocked: Honey Maker!');
        }

        this.save();
        this.render();
    },

    /* ── Sell Product ── */

    sellProduct(item) {
        const products = CONFIG ? CONFIG.apiary_products : {};
        const data = products[item] || { icon: '📦', value: 5 };

        if (!this.state.inventory[item] || this.state.inventory[item] <= 0) return;

        const price = this.getMarketPrice(item);
        this.state.money += price;
        this.state.inventory[item]--;
        if (this.state.inventory[item] <= 0) delete this.state.inventory[item];
        this.state.xp += 2;

        showToast(`Sold ${item} for £${price}`);
        this.save();
        this.render();
    },

    /* ── Render: Market Tab ── */

    renderMarket() {
        const el = document.getElementById('tab-market');
        const hives = this.activeHives;
        const nectar = this.nectarInfo;

        let html = '<h3 class="section-title">🍯 Harvest & Market</h3><div class="market-layout">';

        // ── Harvest Column ──
        html += '<div>';
        html += '<h4 class="market-section-title">🍯 Honey Extraction</h4>';

        const harvestable = hives.filter(h => h.has_super && h.super_honey_frames >= 4);
        if (harvestable.length === 0) {
            html += `<div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2rem;">🍯</div>
                <div style="color: var(--cream-dim); font-size: 0.95rem;">No hives ready for harvest.</div>
                <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">Add supers and wait for the nectar flow!</div>
            </div>`;
        } else {
            for (const hive of harvestable) {
                const frames = hive.super_honey_frames;
                const honeyType = nectar.honey_type || 'Summer Wildflower';
                const jars = Math.max(1, Math.floor(frames * 1.5));
                html += `<div class="harvest-item">
                    <div>
                        <div class="hi-name">🍯 Harvest from '${hive.name}'</div>
                        <div class="hi-detail">${frames} frames → ~${jars} jars of ${honeyType}</div>
                    </div>
                    <button class="sell-btn" onclick="apiary.harvest('${hive.name.replace(/'/g, "\\'")}')">Harvest</button>
                </div>`;
            }
        }
        html += '</div>';

        // ── Sell Column ──
        html += '<div>';
        html += '<h4 class="market-section-title">💰 Sell Products</h4>';

        const inv = this.state.inventory;
        const items = Object.entries(inv).filter(([_, q]) => q > 0);

        if (items.length === 0) {
            html += `<div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1rem; text-align: center;">
                <div style="color: var(--cream-dim);">Nothing to sell. Harvest honey first!</div>
            </div>`;
        } else {
            for (const [item, qty] of items) {
                const products = CONFIG ? CONFIG.apiary_products : {};
                const data = products[item] || { icon: '📦', value: 5, cat: 'raw' };
                const price = this.getMarketPrice(item);
                const priceDiff = price - data.value;
                const priceIndicator = priceDiff > 0 ? '↑' : priceDiff < 0 ? '↓' : '→';
                const priceColor = priceDiff > 0 ? '#4caf50' : priceDiff < 0 ? '#f44336' : 'var(--cream-dim)';
                html += `<div class="sell-item">
                    <div style="color: var(--cream); font-size: 0.9rem;">${data.icon} ${item}: ${qty}</div>
                    <div style="display:flex;gap:0.5rem;align-items:center;">
                        <span style="font-size:0.75rem;color:${priceColor}">£${price} ${priceIndicator}</span>
                        <button class="sell-btn" onclick="apiary.sellProduct('${item.replace(/'/g, "\\'")}')">Sell</button>
                    </div>
                </div>`;
            }
        }
        html += '</div></div>';

        // ── Processing Section ──
        if (CONFIG && CONFIG.apiary_processing) {
            html += '<hr class="game-divider"><h3 class="section-title">⚗️ Processing</h3>';
            html += '<div class="processing-grid">';

            for (const [name, recipe] of Object.entries(CONFIG.apiary_processing)) {
                const canMake = Object.entries(recipe.ingredients).every(
                    ([ing, qty]) => (this.state.inventory[ing] || 0) >= qty
                );
                const ingredientText = Object.entries(recipe.ingredients)
                    .map(([ing, qty]) => `${qty}x ${ing}`).join(', ');

                html += `<div class="process-card${canMake ? '' : ' disabled'}">
                    <div class="process-name">${recipe.icon} ${name}</div>
                    <div class="process-desc">${recipe.desc}</div>
                    <div class="process-ingredients">${ingredientText} • ${recipe.weeks} week${recipe.weeks > 1 ? 's' : ''}</div>
                    <button class="btn-primary process-btn" onclick="apiary.startProcessing('${name}')" ${canMake ? '' : 'disabled'}>Process</button>
                </div>`;
            }
            html += '</div>';

            // Active processing
            if (this.state.processing_queue && this.state.processing_queue.length > 0) {
                html += '<div class="processing-active"><h4 style="color: var(--cream); margin-bottom: 0.5rem;">⏳ In Progress</h4>';
                for (const item of this.state.processing_queue) {
                    const recipe = CONFIG.apiary_processing[item.product] || {};
                    const weeksLeft = item.weeksNeeded - (this.state.week - item.startWeek);
                    html += `<div class="process-progress">${recipe.icon || '⚗️'} ${item.product} — ${weeksLeft > 0 ? weeksLeft + ' week' + (weeksLeft > 1 ? 's' : '') + ' left' : 'Ready!'}</div>`;
                }
                html += '</div>';
            }
        }

        // ── Swarm Catching ──
        const month = this.currentMonth;
        if (['May', 'June', 'July'].includes(month)) {
            const maxHives = this.state.level + 1;
            if (this.activeHives.length < maxHives) {
                html += '<hr class="game-divider"><h3 class="section-title">🪤 Swarm Catching</h3>';
                html += `<div class="swarm-card">
                    <div style="font-size: 1.5rem; text-align: center; margin-bottom: 0.5rem;">🐝</div>
                    <div style="color: var(--cream); text-align: center; margin-bottom: 0.5rem;">A swarm has been spotted nearby!</div>
                    <div style="color: var(--cream-dim); text-align: center; font-size: 0.85rem; margin-bottom: 0.8rem;">40% chance of catching. New colony starts with a virgin queen.</div>
                    <button class="btn-primary btn-full" onclick="apiary.catchSwarm()">🪤 Attempt to Catch Swarm</button>
                </div>`;
            }
        }

        // ── Inventory ──
        html += '<hr class="game-divider"><h4 class="market-section-title">🎒 Inventory</h4>';

        if (items.length === 0) {
            html += `<div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1rem; text-align: center;">
                <span style="color: var(--cream-dim);">Empty — harvest honey to fill your inventory!</span>
            </div>`;
        } else {
            html += '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">';
            for (const [item, qty] of items) {
                html += `<span style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 6px; padding: 0.3rem 0.6rem; color: var(--cream); font-size: 0.85rem;"><b>${item}</b>: ${qty}</span>`;
            }
            html += '</div>';
        }

        el.innerHTML = html;
    },


    /* ═══════════════════════════════════════════════════════════
       10. ACTIONS TAB RENDERER
       ═══════════════════════════════════════════════════════════ */

    renderActions() {
        const el = document.getElementById('tab-actions');
        const hives = this.activeHives;
        const levelUnlocks = CONFIG && CONFIG.level_unlocks ? CONFIG.level_unlocks : {};
        const currentUnlock = levelUnlocks[this.state.level] || { features: ['inspect', 'feed', 'market'], max_hives: this.state.level + 1 };
        const features = currentUnlock.features || [];

        if (hives.length === 0) {
            el.innerHTML = '<p style="color: var(--cream-dim);">No active hives. Buy one from the Overview tab.</p>';
            return;
        }

        let html = '<h3 class="section-title">🛠️ Beekeeping Actions</h3>';

        // ── Hive Selector ──
        html += `<select id="action-hive-select" onchange="apiary.actionSelectHive()" style="background: var(--bg-deep); color: var(--cream); border: 1px solid #3d5a3d; border-radius: 8px; padding: 0.5rem; font-size: 0.95rem; width: 100%; margin-bottom: 1rem;">`;
        for (const h of hives) {
            const sel = h.name === this.state.selectedHive ? ' selected' : '';
            const tempBadge = this._temperamentBadge(h.temperament);
            html += `<option value="${h.name}"${sel}>${h.name} ${tempBadge}</option>`;
        }
        html += '</select>';

        if (!this.state.selectedHive || !hives.find(h => h.name === this.state.selectedHive)) {
            this.state.selectedHive = hives[0].name;
        }

        const hive = hives.find(h => h.name === this.state.selectedHive);
        if (!hive) { el.innerHTML = html; return; }

        const season = this.currentSeason;
        const month = this.currentMonth;
        const temp = hive.temperament || 'moderate';
        const tempConfig = CONFIG && CONFIG.hive_temperaments ? CONFIG.hive_temperaments[temp] : { label: temp };
        const smokerCost = CONFIG && CONFIG.smoker_config ? CONFIG.smoker_config.cost : 2;

        // ── Temperament & Smoker Status ──
        html += '<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; align-items: center;">';
        html += `<span class="temperament-badge ${temp}">${tempConfig.icon || ''} ${tempConfig.label || temp}</span>`;
        if (hive.smoked) {
            html += '<span class="smoked-indicator">💨 Smoked this week</span>';
        }
        if (hive.stings_this_week > 0) {
            html += `<span style="color: #ef9a9a; font-size: 0.8rem; font-weight: 600;">🩸 ${hive.stings_this_week} sting${hive.stings_this_week > 1 ? 's' : ''} this week</span>`;
        }
        html += '</div>';

        if (tempConfig.desc) {
            html += `<div style="color: var(--cream-dim); font-size: 0.8rem; margin-bottom: 0.8rem; font-style: italic;">${tempConfig.desc}</div>`;
        }

        html += '<div class="action-grid">';

        // ── LEFT: Inspection ──
        html += '<div class="action-section"><h4>🔍 Inspection</h4>';

        const canSmoke = this.state.money >= smokerCost && !hive.smoked;
        html += `<button class="action-btn smoker-btn" onclick="apiary.smokeHive('${hive.name.replace(/'/g, "\\'")}') " ${canSmoke ? '' : 'disabled'}>${ApiaryIcons.icon('smoker', 16)} Smoke Hive (£${smokerCost})${hive.smoked ? ' — Already done' : ''}${this.state.money < smokerCost ? ' — Need £' + smokerCost : ''}</button>`;

        if (temp === 'defensive' && !hive.smoked) {
            html += `<div style="color: #ef9a9a; font-size: 0.8rem; margin: 0.3rem 0; padding: 0.3rem 0.5rem; background: #2a1010; border-radius: 6px; border: 1px solid #f44336;">⚠️ Defensive colony — smoke recommended before inspecting!</div>`;
        }

        if (season === 'Winter') {
            html += `<button class="action-btn heft-btn" onclick="apiary.heftHive('${hive.name.replace(/'/g, "\\'")}')">${ApiaryIcons.icon('heft', 16)} Heft Hive (check weight)</button>`;
            html += '<div style="color: var(--cream-dim); font-size: 0.8rem; margin: 0.3rem 0;">Lift the hive to estimate stores without opening it.</div>';
        }

        html += '</div>';

        // ── RIGHT: Feeding & Supers ──
        html += '<div class="action-section"><h4>🍯 Feeding & Supers</h4>';

        // Add Super
        if (features.includes('super') || this.state.level >= 2) {
            if (!hive.has_super) {
                const canAddSuper = season !== 'Winter' && this.state.money >= 15;
                html += `<button class="action-btn success" onclick="apiary.addSuper()" ${canAddSuper ? '' : 'disabled'}>➕ Add Super (£15)${season === 'Winter' ? ' — Not in Winter' : ''}</button>`;
            } else {
                html += '<div class="status-good" style="margin-bottom: 0.5rem;">✅ Super already on hive.</div>';
            }
        } else {
            html += `<div style="color: var(--cream-dim); font-size: 0.8rem; padding: 0.3rem; border: 1px dashed #444; border-radius: 6px;">🔒 Add Super — unlock at Level 2</div>`;
        }

        // Feed Spring
        const canFeedSpring = season === 'Spring' && !hive.fed_spring;
        html += `<button class="action-btn" onclick="apiary.feedSpring()" ${canFeedSpring ? '' : 'disabled'}>🫗 Feed Spring Syrup (1:1) — £3${!canFeedSpring && season !== 'Spring' ? ' — Spring only' : ''}${hive.fed_spring ? ' — Already fed' : ''}</button>`;

        // Feed Autumn
        const canFeedAutumn = season === 'Autumn' && !hive.fed_autumn;
        html += `<button class="action-btn" onclick="apiary.feedAutumn()" ${canFeedAutumn ? '' : 'disabled'}>🍯 Feed Autumn Syrup (2:1) — £3${!canFeedAutumn && season !== 'Autumn' ? ' — Autumn only' : ''}${hive.fed_autumn ? ' — Already fed' : ''}</button>`;

        // Feed Fondant (Winter)
        if (season === 'Winter') {
            html += '<button class="action-btn" onclick="apiary.feedFondant()">🍬 Feed Fondant — £4</button>';
        }

        html += '</div></div>';

        // ── BOTTOM: Health & Swarm Control ──
        html += '<div class="action-grid" style="margin-top: 0.5rem;">';

        // Health
        html += '<div class="action-section"><h4>🛡️ Health</h4>';

        const varroaTreatable = (month === 'August' || month === 'September' || month === 'December') && !hive.treated_this_year;
        if (varroaTreatable) {
            const isAugust = month === 'August' || month === 'September';
            const treatment = isAugust ? 'Apivar Strips (£15)' : 'Oxalic Acid (£10)';
            const cost = isAugust ? 15 : 10;
            html += `<button class="action-btn danger" onclick="apiary.treatVarroa(${cost})">💊 Apply ${treatment}</button>`;
        } else if (hive.treated_this_year) {
            html += '<div class="status-good" style="margin-bottom: 0.5rem;">✅ Already treated this year.</div>';
        } else {
            html += '<p style="color: var(--cream-dim); font-size: 0.85rem;">Treatment in Aug/Sep (Apivar £15) or Dec (Oxalic £10).</p>';
        }

        // Mouse Guard
        if (season === 'Winter' || season === 'Autumn') {
            html += `<button class="action-btn" onclick="apiary.buyMouseGuard()" ${hive.has_mouse_guard ? 'disabled' : ''} ${this.state.money >= 5 ? '' : 'disabled'}>🐭 Mouse Guard (£5)${hive.has_mouse_guard ? ' — Fitted' : ''}</button>`;
        }

        // Reduce Entrance
        if (['August', 'September', 'October'].includes(month) && !hive.entrance_reduced) {
            html += `<button class="action-btn" onclick="apiary.reduceEntrance('${hive.name.replace(/'/g, "\\'")}') " style="border-color: #ff6d00; color: #ffab40;">🪱 Reduce Entrance (wasp defence)</button>`;
        } else if (hive.entrance_reduced) {
            html += '<div class="status-good" style="margin-bottom: 0.5rem; font-size: 0.85rem;">🪱 Entrance reduced — wasp defence active</div>';
        }

        // Foulbrood
        if (hive.has_foulbrood) {
            html += `<button class="action-btn danger" onclick="apiary.treatFoulbrood()" ${this.state.money >= 25 ? '' : 'disabled'}>🦠 Treat Foulbrood (£25)</button>`;
        }

        html += '</div>';

        // Swarm Control
        html += '<div class="action-section"><h4>✂️ Swarm Control</h4>';

        if (features.includes('swarm') || this.state.level >= 4) {
            const canSplit = hive.queen_cells >= 2 && hive.population > 20000 && hives.length < this.state.level + 1 && ['April', 'May', 'June'].includes(month);
            html += `<button class="action-btn" onclick="apiary.splitColony()" ${canSplit ? '' : 'disabled'}>✂️ Split Colony</button>`;
        } else {
            html += `<div style="color: var(--cream-dim); font-size: 0.8rem; padding: 0.3rem; border: 1px dashed #444; border-radius: 6px;">🔒 Split Colony — unlock at Level 4</div>`;
        }

        if (hive.queen_cells > 0) {
            html += `<button class="action-btn danger" onclick="apiary.removeQueenCells()">🔪 Remove ${hive.queen_cells} Queen Cell(s)</button>`;
        }

        if (features.includes('requeen') || this.state.level >= 5) {
            if (hive.queen === 'failing' || hive.queen === 'dead') {
                html += `<button class="action-btn" onclick="apiary.requeen()" ${this.state.money >= 30 ? '' : 'disabled'}>👑 Requeen (£30)</button>`;
            }
        } else if (hive.queen === 'failing' || hive.queen === 'dead') {
            html += `<div style="color: var(--cream-dim); font-size: 0.8rem; padding: 0.3rem; border: 1px dashed #444; border-radius: 6px;">🔒 Requeen — unlock at Level 5</div>`;
        }

        html += '</div></div>';

        // ── Dead Hives ──
        const deadHives = this.state.hives.filter(h => h.dead);
        if (deadHives.length > 0) {
            html += '<hr class="game-divider"><h4 style="color: var(--danger);">🪦 Dead Colonies</h4>';
            for (const dh of deadHives) {
                html += `<div class="dead-hive">
                    <div style="color: var(--danger); font-weight: 700;">💀 ${dh.name}</div>
                    <div style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.3rem;">${dh.death_reason}</div>
                    <button class="btn-danger" style="margin-top: 0.5rem;" onclick="apiary.removeDeadHive('${dh.name.replace(/'/g, "\\'")}')">🗑️ Remove '${dh.name}'</button>
                </div>`;
            }
        }

        el.innerHTML = html;
    },


    /* ═══════════════════════════════════════════════════════════
       11. INSPECTION HELPERS
       Frame layout, dashboard, and health assessment
       ═══════════════════════════════════════════════════════════ */

    /* ── Frame Layout (text version, used in non-visual fallback) ── */

    renderFrameLayout(hive) {
        const hf = hive.honey_frames;
        const pf = hive.pollen_frames;
        const bf = hive.brood_frames;
        const queen = hive.queen === 'present';
        const qc = hive.queen_cells > 0;

        const frameColours = {
            '🍯': '#DAA52020', '🟡': '#FFD70020', '🥚': '#FFFFFF20',
            '🐛': '#F5F5DC20', '🟤': '#8B451320', '⚠️': '#FF444420', '⬜': '#33333320'
        };
        const frameBorders = {
            '🍯': '#DAA520', '🟡': '#FFD700', '🥚': '#FFFFFF',
            '🐛': '#F5F5DC', '🟤': '#8B4513', '⚠️': '#FF4444', '⬜': '#333333'
        };

        // Build brood frames
        const broodFrames = [];
        for (let i = 0; i < 11; i++) {
            if (i < hf) broodFrames.push('🍯');
            else if (i < hf + pf) broodFrames.push('🟡');
            else if (i < hf + pf + bf) {
                const pos = i - hf - pf;
                if (queen && pos < Math.max(1, Math.floor(bf / 3))) broodFrames.push('🥚');
                else if (queen && pos < Math.max(2, Math.floor(bf * 2 / 3))) broodFrames.push('🐛');
                else broodFrames.push('🟤');
            }
            else if (qc && i === hf + pf + bf) broodFrames.push('⚠️');
            else broodFrames.push('⬜');
        }

        let html = '<div class="frame-section"><div class="frame-section-title">🗂️ Brood Box (11 frames):</div>';
        html += '<div class="frame-grid brood">';
        for (const f of broodFrames) {
            html += `<div class="frame-cell" style="background: ${frameColours[f]}; border: 2px solid ${frameBorders[f]};">${f}</div>`;
        }
        html += '</div>';

        // Super
        if (hive.has_super) {
            const sf = Math.min(hive.super_honey_frames, 8);
            const superFrames = Array(sf).fill('🍯').concat(Array(8 - sf).fill('⬜'));
            html += '<div class="frame-section-title" style="margin-top: 0.5rem;">📦 Super (8 frames):</div>';
            html += '<div class="frame-grid super">';
            for (const f of superFrames) {
                const bg = f === '🍯' ? '#DAA52020' : '#33333320';
                const border = f === '🍯' ? '#DAA520' : '#333333';
                html += `<div class="frame-cell" style="background: ${bg}; border: 2px solid ${border};">${f}</div>`;
            }
            html += '</div>';
        }

        // Queen cells
        if (hive.queen_cells > 0) {
            html += `<div class="queen-alert"><span class="qa-title">⚠️ ${hive.queen_cells} Queen Cell(s) Found!</span> <span class="qa-desc">Consider splitting or removing them.</span></div>`;
        } else {
            html += '<div class="status-good">✅ No queen cells found.</div>';
        }

        html += '<div class="frame-legend"><span>🍯 Honey</span><span>🟡 Pollen</span><span>🥚 Eggs</span><span>🐛 Larvae</span><span>🟤 Capped Brood</span><span>⬜ Empty</span><span>⚠️ Queen Cell</span></div>';
        html += '</div>';
        return html;
    },

    /* ── Colony Dashboard ── */

    renderDashboard(hive) {
        const weeksSince = this.state.week - hive.inspected_week;
        const queenMap = {
            present: '👑 Present',
            failing: '⚠️ Failing',
            virgin: '🐣 Virgin',
            dead: '💀 No Queen'
        };
        const queenText = weeksSince <= 1 ? (queenMap[hive.queen] || hive.queen) : '❓ Unknown';
        const pop = hive.population;
        const popDelta = pop > 40000 ? 'Strong' : (pop > 20000 ? 'Medium' : 'Weak');
        const varroa = hive.varroa_count;
        const varroaText = varroa <= 3 ? '✅ Low' : (varroa <= 6 ? '⚠️ Rising' : '🚨 Critical');
        const stores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
        const storesText = stores >= 7 ? '✅ Good' : (stores >= 3 ? '⚠️ Low' : '🚨 Critical');

        return `<hr class="game-divider"><h4 style="color: var(--cream); margin-bottom: 0.5rem;">📊 Colony Dashboard</h4>
        <div class="dashboard-grid">
            <div class="dash-item"><div class="di-label">👑 Queen</div><div class="di-value">${queenText}</div></div>
            <div class="dash-item"><div class="di-label">🐝 Population</div><div class="di-value">${pop.toLocaleString()}</div></div>
            <div class="dash-item"><div class="di-label">🪲 Varroa</div><div class="di-value">${varroa}/300</div></div>
            <div class="dash-item"><div class="di-label">🍯 Stores</div><div class="di-value">${stores} fr</div></div>
        </div>`;
    },

    /* ── Health Assessment ── */

    renderHealthAssessment(hive) {
        const issues = [];
        if (hive.queen === 'failing') issues.push('⚠️ Queen is failing — consider requeening');
        if (hive.queen === 'dead') issues.push('🚨 No queen — colony will die without intervention');
        if (hive.varroa_count > 6) issues.push(`🚨 Varroa levels critical (${hive.varroa_count}/300) — treat immediately`);
        else if (hive.varroa_count > 3) issues.push(`Varroa rising (${hive.varroa_count}/300) — treat in Aug/Sep or Dec`);

        const stores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
        const season = this.currentSeason;
        if (stores < 4 && (season === 'Autumn' || season === 'Winter')) issues.push('🚨 Winter stores dangerously low — feed now!');
        if (hive.population < 15000) issues.push('⚠️ Colony is weak — may not survive winter');

        if (issues.length > 0) {
            return `<div class="health-bad" style="margin-top: 1rem;"><div class="hb-title">Health Issues:</div>${issues.map(i => `<div style="color: var(--cream-dim); font-size: 0.9rem;">• ${i}</div>`).join('')}</div>`;
        }
        return '<div class="health-good" style="margin-top: 1rem;">✅ Colony looks healthy!</div>';
    },


    /* ═══════════════════════════════════════════════════════════
       12. ADVANCE WEEK & SEASONAL EVENTS
       ═══════════════════════════════════════════════════════════ */

    /* ── Advance Week UI ── */

    renderAdvance() {
        const el = document.getElementById('apiary-advance');
        const month = this.currentMonth;
        const nextMonth = getMonth(this.state.week + 1);
        const nextSeason = getSeason(nextMonth);

        el.innerHTML = `
            <div class="advance-info">⏰ This game is turn-based. Inspect your hives, take actions, then advance one week.</div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 0.5rem;">
                <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 8px; padding: 0.5rem 1rem; flex: 1; min-width: 150px;">
                    <div style="color: var(--cream-dim); font-size: 0.85rem;">📅 Current</div>
                    <div style="color: var(--cream); font-size: 0.95rem; font-weight: 600;">${SEASON_ICONS[this.currentSeason] || '🌸'} ${this.currentSeason} — ${month.substring(0, 3)} Wk${getWeekInMonth(this.state.week)}</div>
                </div>
                <div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 8px; padding: 0.5rem 1rem; flex: 1; min-width: 150px;">
                    <div style="color: var(--cream-dim); font-size: 0.85rem;">⏭️ Next week</div>
                    <div style="color: var(--cream); font-size: 0.95rem; font-weight: 600;">${SEASON_ICONS[nextSeason] || '🌸'} ${nextMonth.substring(0, 3)}</div>
                </div>
            </div>
            <button class="btn-primary btn-full" onclick="apiary.advanceWeek()">⏭️ Advance Week</button>
        `;
    },

    /* ── Time-lapse Overlay ── */

    _showTimelapse() {
        const season = getSeason(getMonth(this.state.week + 1));
        const seasonIcons = { Spring: '🌸', Summer: '☀️', Autumn: '🍂', Winter: '❄️' };
        const icon = seasonIcons[season] || '📅';

        const overlay = document.createElement('div');
        overlay.className = 'timelapse-overlay';
        overlay.id = 'timelapse-overlay';
        overlay.innerHTML = `<div class="timelapse-icon">${icon}</div><div class="timelapse-text">Advancing...</div>`;
        document.body.appendChild(overlay);

        setTimeout(() => {
            const el = document.getElementById('timelapse-overlay');
            if (el) el.remove();
        }, 900);
    },

    /* ── Advance Week (core game loop) ── */

    advanceWeek() {
        const game = this.state;

        this._showTimelapse();

        const self = this;
        const advanceDelay = 800;

        setTimeout(() => {
            game.week += 1;
            game.events = [];

            const newMonth = getMonth(game.week);
            const newSeason = getSeason(newMonth);
            const newNectar = CONFIG ? (CONFIG.nectar_flow[newMonth] || { flow: 0, source: 'None', honey_type: null }) : { flow: 0, source: 'None', honey_type: null };

            const weatherData = getWeather(newSeason);
            game.weather = weatherData.weather;
            game.temperature = weatherData.temperature;

            // ── Reset weekly flags ──
            game.smoker_used = false;
            for (const h of game.hives) {
                if (!h.dead) {
                    h.smoked = false;
                    h.stings_this_week = 0;
                }
            }

            // ── Process each hive ──
            for (const hive of game.hives) {
                if (hive.dead) continue;
                hive.age_weeks += 1;

                // Winter
                if (newSeason === 'Winter') {
                    const deaths = Math.floor(hive.population * 0.015);
                    hive.population = Math.max(0, hive.population - deaths);
                    if (hive.honey_frames > 0) {
                        hive.honey_frames -= 1;
                    } else {
                        hive.population = Math.max(0, hive.population - 3000);
                        if (hive.population < 5000) {
                            hive.dead = true;
                            hive.death_reason = 'Starvation — not enough winter stores. Feed fondant in future!';
                            game.events.push(`💀 '${hive.name}' died — starvation!`);
                            self.addJournal(`💀 '${hive.name}' died from starvation`, 'danger');
                        }
                    }
                }
                // Spring / Summer
                else if (newSeason === 'Spring' || newSeason === 'Summer') {
                    const tempMult = hive.temperament === 'defensive' ? 1.02 : hive.temperament === 'gentle' ? 0.98 : 1.0;
                    if (hive.queen === 'present') {
                        const growth = Math.floor(hive.population * 0.03 * (newNectar.flow / 5 + 0.3) * tempMult);
                        hive.population = Math.min(80000, hive.population + growth);
                    }
                    const deaths = Math.floor(hive.population * 0.02);
                    hive.population = Math.max(0, hive.population - deaths);

                    if (newNectar.flow > 0 && !game.weather.includes('Rainy') && !game.weather.includes('Stormy')) {
                        const honeyGain = Math.floor(newNectar.flow * 0.5);
                        if (hive.has_super) {
                            hive.super_honey_frames = Math.min(8, hive.super_honey_frames + honeyGain);
                        } else {
                            hive.honey_frames = Math.min(9, hive.honey_frames + Math.floor(honeyGain * 0.3));
                        }
                    }

                    if (hive.queen === 'virgin' && Math.random() < 0.5) hive.queen = 'present';
                    if (hive.queen === 'present' && hive.age_weeks > 100 && Math.random() < 0.02) hive.queen = 'failing';
                }
                // Autumn
                else if (newSeason === 'Autumn') {
                    const deaths = Math.floor(hive.population * 0.025);
                    hive.population = Math.max(0, hive.population - deaths);
                    if (newNectar.flow > 0 && !game.weather.includes('Rainy')) {
                        const honeyGain = Math.floor(newNectar.flow * 0.2);
                        if (hive.has_super) hive.super_honey_frames = Math.min(8, hive.super_honey_frames + honeyGain);
                    }
                }

                // ── Varroa ──
                if ((newSeason === 'Spring' || newSeason === 'Summer') && !hive.treated_this_year) {
                    hive.varroa_count = Math.min(15, hive.varroa_count + Math.floor(Math.random() * 2));
                }
                if (hive.varroa_count > 10 && newSeason === 'Winter') {
                    hive.dead = true;
                    hive.death_reason = `Varroa infestation (${hive.varroa_count}/300 mites). Treat in August!`;
                    game.events.push(`💀 '${hive.name}' died — varroa infestation!`);
                    self.addJournal(`💀 '${hive.name}' lost to varroa`, 'danger');
                }

                // ── Swarm ──
                if (hive.queen === 'present' && ['April', 'May', 'June'].includes(newMonth) && hive.population > 45000 && hive.queen_cells >= 3 && !hive.swarmed) {
                    const swarmMult = hive.temperament === 'defensive' ? 1.2 : hive.temperament === 'gentle' ? 0.9 : 1.0;
                    if (Math.random() < 0.5 * swarmMult) {
                        const lost = Math.floor(hive.population * 0.5);
                        hive.population -= lost;
                        hive.queen_cells = 0;
                        hive.swarmed = true;
                        game.events.push(`🐝 '${hive.name}' SWARMED! Lost ${lost.toLocaleString()} bees!`);
                        self.addJournal(`🐝 '${hive.name}' swarmed — lost ${lost.toLocaleString()} bees`, 'danger');
                        ApiarySound.playWarning();
                    }
                }

                // ── Wasp Attacks (Aug/Sep) ──
                if (['August', 'September'].includes(newMonth) && !hive.dead) {
                    const waspChance = hive.population < 15000 ? 0.12 : 0.06;
                    if (Math.random() < waspChance && !hive.wasp_damage) {
                        hive.wasp_damage = true;
                        hive.honey_frames = Math.max(0, hive.honey_frames - 2);
                        hive.population = Math.max(0, hive.population - 3000);
                        game.events.push(`🪱 Wasps attacking '${hive.name}'! Stores and bees lost!`);
                        self.addJournal(`🪱 Wasps attacked '${hive.name}'`, 'danger');
                    }
                }

                // ── Foulbrood ──
                if (newSeason === 'Summer' && !hive.has_foulbrood && hive.queen === 'present') {
                    if (Math.random() < 0.03) {
                        hive.has_foulbrood = true;
                        hive.brood_frames = Math.max(0, hive.brood_frames - 1);
                        game.events.push(`🦠 Foulbrood detected in '${hive.name}'! Treat immediately.`);
                        self.addJournal(`🦠 Foulbrood in '${hive.name}'`, 'danger');
                    }
                }
                if (hive.has_foulbrood) {
                    hive.brood_frames = Math.max(0, hive.brood_frames - 1);
                    if (hive.brood_frames === 0 && hive.queen !== 'dead') {
                        hive.queen = 'failing';
                    }
                }

                // ── Mice ──
                if (newSeason === 'Winter' && !hive.has_mouse_guard && !hive.has_mice_damage) {
                    if (Math.random() < 0.08) {
                        hive.has_mice_damage = true;
                        hive.honey_frames = Math.max(0, hive.honey_frames - 2);
                        game.events.push(`🐭 Mouse damage in '${hive.name}'! Consider a mouse guard.`);
                        self.addJournal(`🐭 Mouse damage in '${hive.name}'`, 'important');
                    }
                }

                // ── Disease-free tracking ──
                if (!hive.has_foulbrood && hive.queen === 'present') {
                    hive.disease_free_weeks++;
                    if (hive.disease_free_weeks >= 48 && !game.achievements.apiary_disease_free) {
                        game.achievements.apiary_disease_free = true;
                        ApiarySound.playAchievement();
                        showToast('🏅 Achievement Unlocked: Healthy Colony!');
                    }
                } else {
                    hive.disease_free_weeks = 0;
                }

                // ── Colony death ──
                if (hive.population <= 0 && !hive.dead) {
                    hive.dead = true;
                    hive.death_reason = 'Colony collapsed — population reached zero.';
                    game.events.push(`💀 '${hive.name}' has died.`);
                    self.addJournal(`💀 '${hive.name}' colony collapsed`, 'danger');
                }
            }

            // ── Reset seasonal flags (January) ──
            if (newMonth === 'January') {
                for (const h of game.hives) {
                    h.treated_this_year = false;
                    h.fed_spring = false;
                    h.fed_autumn = false;
                    h.swarmed = false;
                    h.queen_cells = 0;
                    h.has_foulbrood = false;
                    h.has_mice_damage = false;
                    h.wasp_damage = false;
                    h.entrance_reduced = false;
                }
            }

            // ── Process processing queue ──
            for (const item of game.processing_queue) {
                if (!item.done && (game.week - item.startWeek) >= item.weeksNeeded) {
                    item.done = true;
                    game.inventory[item.product] = (game.inventory[item.product] || 0) + 1;
                    game.total_processed++;
                    game.events.push(`✅ ${item.product} is ready!`);
                    self.addJournal(`✅ ${item.product} processing complete`, 'success');

                    if (!game.achievements.apiary_processor) {
                        game.achievements.apiary_processor = true;
                        ApiarySound.playAchievement();
                        showToast('🏅 Achievement Unlocked: Processor!');
                    }
                    if (item.product === 'Mead') {
                        game.total_mead = (game.total_mead || 0) + 1;
                        if (game.total_mead >= 5 && !game.achievements.apiary_mead_master) {
                            game.achievements.apiary_mead_master = true;
                            ApiarySound.playAchievement();
                            showToast('🏅 Achievement Unlocked: Mead Master!');
                        }
                    }
                }
            }
            game.processing_queue = game.processing_queue.filter(i => !i.done);

            // ── Fluctuate prices on month change ──
            const prevMonth = getMonth(game.week - 1);
            if (newMonth !== prevMonth) self.fluctuatePrices();

            // ── Swarm catching opportunity ──
            if (['May', 'June', 'July'].includes(newMonth)) {
                if (Math.random() < 0.1) {
                    game.events.push('🐝 A swarm has been spotted nearby! Go to Market to try catching it.');
                    self.addJournal('🐝 Swarm spotted nearby', 'important');
                }
            }

            // ── Overwinter check (March) ──
            if (newMonth === 'March') {
                const surviving = game.hives.filter(h => !h.dead && h.age_weeks > 20);
                for (const h of surviving) {
                    game.colonies_overwintered++;
                }
                if (surviving.length > 0 && !game.achievements.apiary_overwinter) {
                    game.achievements.apiary_overwinter = true;
                    ApiarySound.playAchievement();
                    showToast('🏅 Achievement Unlocked: Survivor!');
                }
            }

            // ── Achievement checks ──
            const activeCount = game.hives.filter(h => !h.dead).length;
            if (activeCount >= 3 && !game.achievements.apiary_keeper) {
                game.achievements.apiary_keeper = true;
                ApiarySound.playAchievement();
                showToast('🏅 Achievement Unlocked: Beekeeper!');
            }
            if (activeCount >= 5 && !game.achievements.apiary_5_hives) {
                game.achievements.apiary_5_hives = true;
                ApiarySound.playAchievement();
                showToast('🏅 Achievement Unlocked: Apiarist!');
            }

            // ── Level up ──
            const thresholds = { 1: 0, 2: 50, 3: 150, 4: 400, 5: 800 };
            for (const [lvl, xp] of Object.entries(thresholds).sort((a, b) => b[0] - a[0])) {
                if (game.xp >= xp && game.level < parseInt(lvl)) {
                    game.level = parseInt(lvl);
                    game.events.push(`⭐ Level up! Now level ${lvl}!`);
                    self.addJournal(`⭐ Levelled up to Level ${lvl}!`, 'success');
                    ApiarySound.playAchievement();
                    showToast(`⭐ Level Up! You're now Level ${lvl}!`);
                    break;
                }
            }

            self.save();
            self.render();
        }, advanceDelay);
    },
    /* ═══════════════════════════════════════════════════════════
       13. ACHIEVEMENTS & JOURNAL
       ═══════════════════════════════════════════════════════════ */

    /* ── Render Achievements ── */

    renderAchievements() {
        const el = document.getElementById('apiary-achievements');
        if (!el) return;

        const achDefs = [
            { key: 'apiary_first_harvest', name: 'First Harvest', desc: 'Harvest your first honey', progress: () => this.state.achievements.apiary_first_harvest ? '(Done)' : '(0/1)' },
            { key: 'apiary_5_harvests', name: 'Honey Maker', desc: 'Harvest honey 5 times', progress: () => this.state.achievements.apiary_5_harvests ? '(Done)' : `(${this.state.total_harvests}/5)` },
            { key: 'apiary_overwinter', name: 'Survivor', desc: 'Overwinter a colony', progress: () => this.state.achievements.apiary_overwinter ? '(Done)' : `(${this.state.colonies_overwintered}/1)` },
            { key: 'apiary_keeper', name: 'Beekeeper', desc: 'Manage 3+ hives', progress: () => this.state.achievements.apiary_keeper ? '(Done)' : `(${this.activeHives.length}/3)` },
            { key: 'apiary_5_hives', name: 'Apiarist', desc: 'Manage 5+ hives', progress: () => this.state.achievements.apiary_5_hives ? '(Done)' : `(${this.activeHives.length}/5)` },
            { key: 'apiary_varroa', name: 'Mite Fighter', desc: 'Treat for varroa', progress: () => this.state.achievements.apiary_varroa ? '(Done)' : '(0/1)' },
            { key: 'apiary_processor', name: 'Processor', desc: 'Process your first product', progress: () => this.state.achievements.apiary_processor ? '(Done)' : '(0/1)' },
            { key: 'apiary_mead_master', name: 'Mead Master', desc: 'Produce 5 batches of Mead', progress: () => this.state.achievements.apiary_mead_master ? '(Done)' : `(${this.state.total_mead || 0}/5)` },
            { key: 'apiary_swarm_catcher', name: 'Swarm Catcher', desc: 'Catch a swarm', progress: () => this.state.achievements.apiary_swarm_catcher ? '(Done)' : `(${this.state.swarms_caught || 0}/1)` },
            { key: 'apiary_disease_free', name: 'Healthy Colony', desc: 'Keep a colony disease-free for a year', progress: () => this.state.achievements.apiary_disease_free ? '(Done)' : '(0/1)' },
        ];

        el.innerHTML = achDefs.map(a => {
            const unlocked = this.state.achievements[a.key];
            const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
            const bg = unlocked ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)' : 'var(--bg-card)';
            const icon = unlocked ? '✅' : '🔒';
            const nameColor = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';
            return `<div class="achievement-card${unlocked ? ' unlocked' : ''}" style="background: ${bg}; border-color: ${borderColor};">
                <div><div class="ach-left"><span class="ach-icon">${icon}</span><span class="ach-name" style="color: ${nameColor};">${a.name}</span></div><div class="ach-desc">${a.desc}</div></div>
                <span class="ach-progress">${a.progress()}</span>
            </div>`;
        }).join('');
    },

    /* ── Render Journal ── */

    renderJournal() {
        const el = document.getElementById('apiary-journal');
        if (!el) return;

        const journal = this.state.journal || [];
        if (journal.length === 0) {
            el.innerHTML = '<div style="color: var(--cream-dim); font-size: 0.85rem; text-align: center; padding: 1rem;">Your beekeeping journal will record events here.</div>';
            return;
        }

        const recent = journal.slice(-20).reverse();
        el.innerHTML = recent.map(j => {
            let cls = 'journal-entry';
            if (j.type === 'danger') cls += ' danger';
            else if (j.type === 'success') cls += ' success';
            else if (j.type === 'important') cls += ' important';
            return `<div class="${cls}"><span class="journal-week">Wk${j.week}</span> ${j.text}</div>`;
        }).join('');
    },

    /* ── Reset Game ── */

    reset() {
        if (!confirm('Reset apiary progress?')) return;
        this.state = { ...this.defaults, hives: [createHive('Willow')] };
        this.save();
        this.render();
    }
};

/* ── Tab Switching (global) ── */

function apiarySwitchTab(tab) {
    apiary.renderTab(tab);
}


/* ═══════════════════════════════════════════════════════════════
   14. VISUAL SYSTEM
   SVG hives, gauges, meadow view, and calendar
   ═══════════════════════════════════════════════════════════════ */

const ApiaryVisual = {

    /* ════════════════════════════════════════════
       14a. Seasonal Themes
       ════════════════════════════════════════════ */

    themes: {
        Spring: {
            bg: 'linear-gradient(180deg, #d5e8d4 0%, #a8d5a2 40%, #7bc47c 100%)',
            ground: '#4caf50',
            groundDark: '#388e3c',
            sky: ['#dcedc8', '#c5e1a5', '#aed581'],
            accent: '#66bb6a',
            particle: '🌸',
            particleColor: '#f8bbd0',
        },
        Summer: {
            bg: 'linear-gradient(180deg, #fff8e1 0%, #ffe082 40%, #ffd54f 100%)',
            ground: '#8bc34a',
            groundDark: '#689f38',
            sky: ['#fff9c4', '#fff176', '#ffee58'],
            accent: '#ffa726',
            particle: '☀️',
            particleColor: '#ffe082',
        },
        Autumn: {
            bg: 'linear-gradient(180deg, #ffe0b2 0%, #ffcc80 40%, #ffb74d 100%)',
            ground: '#a1887f',
            groundDark: '#8d6e63',
            sky: ['#ffe0b2', '#ffcc80', '#ffa726'],
            accent: '#ef6c00',
            particle: '🍂',
            particleColor: '#ffab40',
        },
        Winter: {
            bg: 'linear-gradient(180deg, #e3f2fd 0%, #bbdefb 40%, #90caf9 100%)',
            ground: '#cfd8dc',
            groundDark: '#b0bec5',
            sky: ['#e3f2fd', '#bbdefb', '#90caf9'],
            accent: '#42a5f5',
            particle: '❄️',
            particleColor: '#e3f2fd',
        }
    },

    /* ════════════════════════════════════════════
       14b. Cell Colour Palette
       ════════════════════════════════════════════ */

    cellColors: {
        honey:      '#DAA520',
        pollen:     '#FFD700',
        egg:        '#FFFFFF',
        larvae:     '#FFF8DC',
        capped:     '#C49A6C',
        queen_cell: '#FF5252',
        empty:      '#2d1f10',
        royal:      '#E8D5B7',
    },

    /* ════════════════════════════════════════════
       14c. Season & Month Helpers
       ════════════════════════════════════════════ */

    getSeason(week) {
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const month = months[((week - 1) % 48) >> 2];
        if (['December', 'January', 'February'].includes(month)) return 'Winter';
        if (['March', 'April', 'May'].includes(month)) return 'Spring';
        if (['June', 'July', 'August'].includes(month)) return 'Summer';
        return 'Autumn';
    },

    getMonth(week) {
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        return months[((week - 1) % 48) >> 2];
    },

    getSeasonByMonth(month) {
        if (['December', 'January', 'February'].includes(month)) return 'Winter';
        if (['March', 'April', 'May'].includes(month)) return 'Spring';
        if (['June', 'July', 'August'].includes(month)) return 'Summer';
        return 'Autumn';
    },

    /* ── Apply Season Theme ── */

    applySeason(season) {
        const theme = this.themes[season] || this.themes.Spring;
        const page = document.querySelector('.apiary-page');
        if (page) {
            page.style.background = theme.bg;
            page.style.transition = 'background 1.5s ease';
        }
        const ground = document.getElementById('apiary-ground');
        if (ground) ground.setAttribute('fill', theme.ground);
        const groundDark = document.getElementById('apiary-ground-dark');
        if (groundDark) groundDark.setAttribute('fill', theme.groundDark);
    },

    /* ── Particle Delegation ── */

    renderWeatherParticles(weather) {
        ParticleCanvas.setWeather(weather);
    },

    renderSeasonParticles(season) {
        ParticleCanvas.setSeason(season);
    },

    /* ════════════════════════════════════════════
       14d. Frame Fill Helpers
       ════════════════════════════════════════════ */

    _getFrameFills(hive, box) {
        const fills = [];
        if (box === 'brood') {
            const hf = hive.honey_frames;
            const pf = hive.pollen_frames;
            const bf = hive.brood_frames;
            const total = hf + pf + bf;
            for (let i = 0; i < 11; i++) {
                if (i < hf) fills.push(this.cellColors.honey);
                else if (i < hf + pf) fills.push(this.cellColors.pollen);
                else if (i < total) fills.push(this.cellColors.capped);
                else if (hive.queen_cells > 0 && i === total) fills.push(this.cellColors.queen_cell);
                else fills.push(this.cellColors.empty);
            }
        } else if (box === 'super') {
            const sf = hive.super_honey_frames;
            for (let i = 0; i < 8; i++) {
                fills.push(i < sf ? this.cellColors.honey : this.cellColors.empty);
            }
        }
        return fills;
    },

    _frameLabel(color) {
        const labels = {};
        labels[this.cellColors.honey] = 'Honey';
        labels[this.cellColors.pollen] = 'Pollen';
        labels[this.cellColors.capped] = 'Brood';
        labels[this.cellColors.queen_cell] = 'Queen Cell!';
        labels[this.cellColors.empty] = 'Empty';
        labels[this.cellColors.egg] = 'Eggs';
        labels[this.cellColors.larvae] = 'Larvae';
        return labels[color] || 'Unknown';
    },

    /* ════════════════════════════════════════════
       14e. Mini Hive SVG (Overview Cards)
       ════════════════════════════════════════════ */

    renderMiniHive(hive) {
        const hasSuper = hive.has_super;
        const healthColor = hive.queen === 'dead' ? '#6d3535' :
                            hive.queen === 'failing' ? '#8B6914' : '#6d4c3d';
        const woodDark = hive.queen === 'dead' ? '#4a2020' :
                         hive.queen === 'failing' ? '#5a4010' : '#3d2e1a';

        const broodFills = this._getFrameFills(hive, 'brood');
        const superFills = hasSuper ? this._getFrameFills(hive, 'super') : [];
        const beeCount = Math.min(7, Math.max(1, Math.floor(hive.population / 7000)));

        // Y positions shift based on super
        const roofY = hasSuper ? 12 : 80;
        const crownY = hasSuper ? 52 : 120;
        const superTopY = hasSuper ? 60 : 0;
        const excluderY = hasSuper ? 152 : 0;
        const broodTopY = hasSuper ? 156 : 126;

        const id = hive.name.replace(/\s/g, '');

        let svg = `<svg viewBox="0 0 200 300" class="mini-hive-svg" xmlns="http://www.w3.org/2000/svg">`;

        // Defs
        svg += `<defs>
            <linearGradient id="woodGrad-${id}" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="${healthColor}"/>
                <stop offset="100%" stop-color="${woodDark}"/>
            </linearGradient>
            <linearGradient id="roofGrad-${id}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#78909c"/>
                <stop offset="100%" stop-color="#546e7a"/>
            </linearGradient>
        </defs>`;

        // Ground
        svg += `<rect x="0" y="278" width="200" height="22" fill="#4caf50" rx="3"/>`;
        svg += `<rect x="0" y="285" width="200" height="15" fill="#388e3c"/>`;
        svg += `<line x1="30" y1="278" x2="28" y2="270" stroke="#66bb6a" stroke-width="1.5"/>`;
        svg += `<line x1="32" y1="278" x2="34" y2="271" stroke="#66bb6a" stroke-width="1"/>`;
        svg += `<line x1="160" y1="278" x2="158" y2="270" stroke="#66bb6a" stroke-width="1.5"/>`;
        svg += `<line x1="162" y1="278" x2="164" y2="272" stroke="#66bb6a" stroke-width="1"/>`;

        // Landing board
        svg += `<rect x="65" y="266" width="70" height="5" fill="#5a3d2b" rx="1"/>`;
        // Floor
        svg += `<rect x="50" y="260" width="100" height="6" fill="#4a3525" rx="1"/>`;
        // Entrance
        svg += `<rect x="78" y="256" width="44" height="6" fill="#1a0f0a" rx="1"/>`;

        // Brood Box
        svg += `<rect x="48" y="${broodTopY}" width="104" height="104" fill="url(#woodGrad-${id})" rx="4"/>`;
        svg += `<rect x="51" y="${broodTopY + 3}" width="98" height="98" fill="#5a3d2b" rx="3"/>`;

        // Brood frames
        svg += this._renderMiniFrames(broodFills, 52, broodTopY + 5, 96, 94, 11);

        // Queen excluder
        const exY = hasSuper ? excluderY : broodTopY - 3;
        svg += `<line x1="50" y1="${broodTopY}" x2="152" y2="${broodTopY}" stroke="#999" stroke-width="2" stroke-dasharray="4,3"/>`;

        // Super
        if (hasSuper) {
            svg += `<rect x="48" y="${superTopY}" width="104" height="96" fill="#8B5E3C" rx="4" stroke="#3d2e1a" stroke-width="1.5"/>`;
            svg += `<rect x="51" y="${superTopY + 3}" width="98" height="90" fill="#7a5235" rx="3"/>`;
            svg += this._renderMiniFrames(superFills, 52, superTopY + 5, 96, 86, 8);
            svg += `<line x1="48" y1="${superTopY}" x2="152" y2="${superTopY}" stroke="#999" stroke-width="1.5" stroke-dasharray="4,3"/>`;
        }

        // Crown board
        svg += `<rect x="49" y="${crownY - 4}" width="102" height="5" fill="#9e9e9e" rx="1"/>`;

        // Roof
        svg += `<rect x="42" y="${roofY}" width="116" height="40" fill="url(#roofGrad-${id})" rx="4"/>`;
        svg += `<rect x="44" y="${roofY + 2}" width="112" height="36" fill="#6d6d6d" rx="3"/>`;
        svg += `<rect x="42" y="${roofY}" width="116" height="4" fill="#90a4ae" rx="2"/>`;

        // Handle
        svg += `<rect x="90" y="${roofY - 3}" width="20" height="5" fill="#78909c" rx="2"/>`;

        // Bees at entrance
        for (let i = 0; i < beeCount; i++) {
            const bx = 72 + (i * 8) + (Math.sin(i * 2.1) * 3);
            const by = 252 + (Math.cos(i * 1.7) * 3);
            svg += `<text x="${bx}" y="${by}" font-size="8" class="bee-anim" style="animation-delay:${i * 0.4}s">🐝</text>`;
        }

        // Dead overlay
        if (hive.dead) {
            svg += `<rect x="48" y="${broodTopY}" width="104" height="104" fill="rgba(0,0,0,0.5)" rx="4"/>`;
            svg += `<text x="100" y="${broodTopY + 55}" text-anchor="middle" font-size="24" fill="#f44336">💀</text>`;
        }

        svg += `</svg>`;
        return svg;
    },

    _renderMiniFrames(fills, x, y, totalWidth, height, count) {
        const frameW = (totalWidth / count) - 1;
        const gap = 1;
        let svg = '';
        for (let i = 0; i < fills.length; i++) {
            const fx = x + i * (frameW + gap);
            svg += `<rect x="${fx}" y="${y}" width="${frameW}" height="${height - 2}" fill="${fills[i]}" rx="1" opacity="0.9">`;
            svg += `<title>Frame ${i + 1}: ${this._frameLabel(fills[i])}</title>`;
            svg += `</rect>`;
        }
        return svg;
    },

    /* ════════════════════════════════════════════
       14f. Detailed Hive SVG (Inspection View)
       ════════════════════════════════════════════ */

    renderDetailedHive(hive, state) {
        const hasSuper = hive.has_super;
        const season = this.getSeason(state.week);
        const theme = this.themes[season] || this.themes.Spring;
        const beeCount = Math.min(12, Math.max(2, Math.floor(hive.population / 5000)));

        // Layout
        const vbW = 660;
        const vbH = hasSuper ? 620 : 520;
        const hiveLeft = 140;
        const hiveW = 380;

        const woodColor = hive.queen === 'dead' ? '#5a3030' :
                          hive.queen === 'failing' ? '#7a5a20' : '#6d4c3d';
        const woodInner = hive.queen === 'dead' ? '#4a2020' :
                          hive.queen === 'failing' ? '#5a4010' : '#5a3d2b';

        // Y positions (bottom-up)
        const groundY = hasSuper ? 590 : 490;
        const floorY = groundY - 18;
        const entranceY = floorY - 8;
        const broodH = 180;
        const broodY = floorY - 8 - broodH;
        const excluderY = broodY - 4;
        const superH = 120;
        const superY = hasSuper ? excluderY - superH - 4 : 0;
        const crownY = hasSuper ? superY - 8 : excluderY - 8;
        const roofH = 38;
        const roofY = crownY - roofH;
        const roofOverhang = 14;

        let svg = `<svg viewBox="0 0 ${vbW} ${vbH}" class="detailed-hive-svg" xmlns="http://www.w3.org/2000/svg">`;

        // ── Defs ──
        svg += `<defs>
            <linearGradient id="woodGradDetail" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="${woodColor}"/>
                <stop offset="100%" stop-color="#3d2e1a"/>
            </linearGradient>
            <linearGradient id="roofGradDetail" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#78909c"/>
                <stop offset="100%" stop-color="#455a64"/>
            </linearGradient>
            <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="${theme.sky[0]}"/>
                <stop offset="50%" stop-color="${theme.sky[1]}"/>
                <stop offset="100%" stop-color="${theme.sky[2]}"/>
            </linearGradient>
            <filter id="hiveShadow" x="-10%" y="-5%" width="120%" height="120%">
                <feDropShadow dx="4" dy="6" stdDeviation="6" flood-opacity="0.3" flood-color="#000"/>
            </filter>
            <filter id="softGlow">
                <feGaussianBlur stdDeviation="2" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <pattern id="combPattern" width="18" height="20.8" patternUnits="userSpaceOnUse" patternTransform="rotate(0)">
                <polygon points="9,0 18,5.2 18,15.6 9,20.8 0,15.6 0,5.2" fill="none" stroke="#5a4010" stroke-width="0.5" opacity="0.3"/>
            </pattern>
        </defs>`;

        // ── Sky ──
        svg += `<rect x="0" y="0" width="${vbW}" height="${vbH}" fill="url(#skyGrad)"/>`;
        svg += `<ellipse cx="100" cy="40" rx="60" ry="18" fill="white" opacity="0.4" class="cloud-drift"/>`;
        svg += `<ellipse cx="130" cy="35" rx="40" ry="14" fill="white" opacity="0.3" class="cloud-drift" style="animation-delay: 2s"/>`;
        svg += `<ellipse cx="450" cy="55" rx="50" ry="15" fill="white" opacity="0.3" class="cloud-drift" style="animation-delay: 4s"/>`;

        // ── Ground ──
        svg += `<rect x="0" y="${groundY}" width="${vbW}" height="${vbH - groundY}" fill="${theme.ground}"/>`;
        svg += `<rect x="0" y="${groundY + 8}" width="${vbW}" height="${vbH - groundY - 8}" fill="${theme.groundDark}"/>`;

        // Grass
        for (let gx = 10; gx < vbW; gx += 25) {
            const gh = 6 + Math.random() * 8;
            svg += `<line x1="${gx}" y1="${groundY}" x2="${gx + (Math.random() * 4 - 2)}" y2="${groundY - gh}" stroke="#66bb6a" stroke-width="1.2" opacity="0.6"/>`;
        }

        // Flowers
        const flowerPositions = [60, 180, 520, 580];
        const flowerColors = ['#ff80ab', '#ffab40', '#69f0ae', '#b388ff'];
        flowerPositions.forEach((fx, i) => {
            svg += `<circle cx="${fx}" cy="${groundY - 3}" r="3" fill="${flowerColors[i]}" opacity="0.7"/>`;
            svg += `<line x1="${fx}" y1="${groundY}" x2="${fx}" y2="${groundY - 8}" stroke="#4caf50" stroke-width="1"/>`;
        });

        // ── Hive Shadow ──
        svg += `<ellipse cx="${hiveLeft + hiveW / 2}" cy="${groundY - 2}" rx="${hiveW / 2 + 15}" ry="6" fill="rgba(0,0,0,0.15)"/>`;

        // ── Landing Board ──
        svg += `<rect x="${hiveLeft + 60}" y="${floorY + 8}" width="${hiveW - 120}" height="6" fill="#5a3d2b" rx="1" filter="url(#hiveShadow)"/>`;

        // ── Floor ──
        svg += `<rect x="${hiveLeft - 4}" y="${floorY + 2}" width="${hiveW + 8}" height="8" fill="#4a3525" rx="2"/>`;

        // ── Entrance ──
        const entW = 70;
        const entX = hiveLeft + (hiveW - entW) / 2;
        svg += `<rect x="${entX}" y="${entranceY}" width="${entW}" height="10" fill="#1a0f0a" rx="2"/>`;
        svg += `<rect x="${entX + 2}" y="${entranceY + 1}" width="${entW - 4}" height="3" fill="#2a1f1a" rx="1"/>`;

        // ── Brood Box ──
        svg += `<rect x="${hiveLeft - 4}" y="${broodY}" width="${hiveW + 8}" height="${broodH + 10}" fill="url(#woodGradDetail)" rx="5" filter="url(#hiveShadow)"/>`;
        svg += `<rect x="${hiveLeft}" y="${broodY + 4}" width="${hiveW}" height="${broodH + 2}" fill="${woodInner}" rx="3"/>`;

        // Brood frames (hex comb)
        svg += this._renderDetailedFrames(hive, 'brood', hiveLeft + 6, broodY + 8, hiveW - 12, broodH - 10, 11);

        // ── Queen Excluder ──
        svg += `<line x1="${hiveLeft - 2}" y1="${excluderY + 2}" x2="${hiveLeft + hiveW + 2}" y2="${excluderY + 2}" stroke="#bbb" stroke-width="3" stroke-dasharray="6,4"/>`;
        svg += `<text x="${hiveLeft + hiveW + 10}" y="${excluderY + 6}" font-size="9" fill="#999" font-family="Inter, sans-serif">queen excluder</text>`;

        // ── Super ──
        if (hasSuper) {
            svg += `<rect x="${hiveLeft - 4}" y="${superY}" width="${hiveW + 8}" height="${superH + 8}" fill="url(#woodGradDetail)" rx="5" filter="url(#hiveShadow)"/>`;
            svg += `<rect x="${hiveLeft}" y="${superY + 4}" width="${hiveW}" height="${superH}" fill="${woodInner}" rx="3"/>`;
            svg += this._renderDetailedFrames(hive, 'super', hiveLeft + 6, superY + 8, hiveW - 12, superH - 12, 8);
            svg += `<text x="${hiveLeft + hiveW + 10}" y="${superY + superH / 2 + 4}" font-size="10" fill="#aaa" font-family="Inter, sans-serif">super</text>`;
        }

        // ── Crown Board ──
        svg += `<rect x="${hiveLeft - 2}" y="${crownY}" width="${hiveW + 4}" height="6" fill="#9e9e9e" rx="1"/>`;

        // ── Roof ──
        svg += `<rect x="${hiveLeft - roofOverhang}" y="${roofY}" width="${hiveW + roofOverhang * 2}" height="${roofH}" fill="url(#roofGradDetail)" rx="5" filter="url(#hiveShadow)"/>`;
        svg += `<rect x="${hiveLeft - roofOverhang + 3}" y="${roofY + 3}" width="${hiveW + roofOverhang * 2 - 6}" height="${roofH - 6}" fill="#6d6d6d" rx="4"/>`;
        svg += `<rect x="${hiveLeft - roofOverhang}" y="${roofY}" width="${hiveW + roofOverhang * 2}" height="4" fill="#90a4ae" rx="2"/>`;
        svg += `<rect x="${hiveLeft + hiveW / 2 - 15}" y="${roofY - 4}" width="30" height="6" fill="#78909c" rx="3"/>`;

        // ── Labels ──
        svg += `<text x="${hiveLeft - 5}" y="${broodY + broodH / 2}" font-size="9" fill="#aaa" font-family="Inter, sans-serif" text-anchor="end" transform="rotate(-90, ${hiveLeft - 10}, ${broodY + broodH / 2})">brood box</text>`;

        // ── Bees at Entrance ──
        for (let i = 0; i < beeCount; i++) {
            const bx = entX + 5 + (i * (entW - 10) / Math.max(1, beeCount - 1));
            const by = entranceY + 4 + (Math.sin(i * 1.3) * 2);
            svg += `<text x="${bx}" y="${by}" font-size="${8 + Math.random() * 3}" class="bee-anim" style="animation-delay:${i * 0.3}s">🐝</text>`;
        }

        // Flying bees
        for (let i = 0; i < Math.min(4, beeCount - 2); i++) {
            const fbx = hiveLeft + 20 + Math.random() * (hiveW - 40);
            const fby = roofY - 15 - Math.random() * 30;
            svg += `<text x="${fbx}" y="${fby}" font-size="${7 + Math.random() * 3}" class="bee-fly" style="animation-delay:${i * 0.7}s">🐝</text>`;
        }

        // ── Queen Mark ──
        if (hive.queen === 'present' && !hive.dead) {
            const crownX = hiveLeft + hiveW / 2;
            const crownY2 = broodY + 20;
            svg += `<text x="${crownX}" y="${crownY2}" font-size="14" text-anchor="middle" filter="url(#softGlow)">👑</text>`;
            if (hive.queen_mark_colour) {
                svg += `<circle cx="${crownX + 12}" cy="${crownY2 - 4}" r="4" fill="${hive.queen_mark_colour}" stroke="white" stroke-width="1" class="queen-mark-dot"/>`;
            }
        } else if (hive.queen === 'failing') {
            svg += `<text x="${hiveLeft + hiveW / 2}" y="${broodY + 20}" font-size="14" text-anchor="middle" opacity="0.7">⚠️</text>`;
        } else if (hive.queen === 'dead' || hive.queen === 'virgin') {
            const label = hive.queen === 'virgin' ? '🐣' : '💀';
            svg += `<text x="${hiveLeft + hiveW / 2}" y="${broodY + 20}" font-size="14" text-anchor="middle">${label}</text>`;
        }

        // ── Queen Cells ──
        if (hive.queen_cells > 0) {
            const qcX = hiveLeft + hiveW + 10;
            const qcY = broodY + broodH - 20;
            svg += `<g class="queen-cell-pulse">`;
            svg += `<rect x="${qcX}" y="${qcY - 2}" width="60" height="20" fill="#3d2e0a" rx="4" stroke="#FF5252" stroke-width="1.5"/>`;
            svg += `<text x="${qcX + 30}" y="${qcY + 12}" font-size="10" text-anchor="middle" fill="#FF5252" font-weight="bold" font-family="Inter, sans-serif">⚠️ ${hive.queen_cells} QC</text>`;
            svg += `</g>`;
        }

        // ── Dead Overlay ──
        if (hive.dead) {
            svg += `<rect x="${hiveLeft - 4}" y="${broodY}" width="${hiveW + 8}" height="${broodH + 10}" fill="rgba(80,20,20,0.6)" rx="5"/>`;
            svg += `<text x="${hiveLeft + hiveW / 2}" y="${broodY + broodH / 2 + 8}" text-anchor="middle" font-size="32" fill="#f44336">💀</text>`;
            svg += `<text x="${hiveLeft + hiveW / 2}" y="${broodY + broodH / 2 + 24}" text-anchor="middle" font-size="10" fill="#ffcdd2" font-family="Inter, sans-serif">COLONY DEAD</text>`;
        }

        // ── Hive Name ──
        svg += `<text x="${hiveLeft + hiveW / 2}" y="${groundY + 16}" text-anchor="middle" font-size="13" fill="var(--cream)" font-weight="700" font-family="'Crimson Text', Georgia, serif">🐝 ${hive.name}</text>`;

        svg += `</svg>`;
        return svg;
    },

    /* ── Detailed Frames (hex comb overlay) ── */

    _renderDetailedFrames(hive, box, x, y, totalWidth, height, count) {
        const fills = this._getFrameFills(hive, box);
        const frameGap = 3;
        const frameW = (totalWidth - (count - 1) * frameGap) / count;
        const hexR = Math.min(frameW / 4, height / 16);
        let svg = '';

        for (let i = 0; i < count; i++) {
            const fx = x + i * (frameW + frameGap);
            const fy = y;
            const fill = fills[i] || this.cellColors.empty;

            // Frame background
            svg += `<rect x="${fx}" y="${fy}" width="${frameW}" height="${height}" fill="${fill}" rx="2" opacity="0.85"/>`;

            // Hex pattern overlay
            const cols = 3;
            const rows = Math.floor(height / (hexR * 1.8));
            for (let row = 0; row < rows; row++) {
                for (let col = 0; col < cols; col++) {
                    const cx = fx + frameW / 2 + (col - 1) * hexR * 1.7;
                    const cy = fy + hexR * 1.5 + row * hexR * 1.8;
                    const offsetX = (row % 2) * hexR * 0.85;

                    let cellColor = fill;
                    let cellOpacity = 0.3;

                    if (fill === this.cellColors.honey) {
                        cellColor = '#FFE082';
                        cellOpacity = 0.4;
                    } else if (fill === this.cellColors.pollen) {
                        cellColor = '#FFF176';
                        cellOpacity = 0.4;
                    } else if (fill === this.cellColors.capped) {
                        const rowRatio = row / rows;
                        if (rowRatio < 0.25 && hive.queen === 'present') {
                            cellColor = '#FFFFFF';
                            cellOpacity = 0.5;
                        } else if (rowRatio < 0.5) {
                            cellColor = '#FFF8DC';
                            cellOpacity = 0.4;
                        } else {
                            cellColor = '#A1887F';
                            cellOpacity = 0.3;
                        }
                    } else if (fill === this.cellColors.queen_cell) {
                        cellColor = '#FF5252';
                        cellOpacity = 0.6;
                    } else {
                        cellColor = '#5a4010';
                        cellOpacity = 0.2;
                    }

                    svg += `<polygon points="${this._hexPoints(cx + offsetX, cy, hexR * 0.7)}" fill="${cellColor}" fill-opacity="${cellOpacity}" stroke="#5a4010" stroke-width="0.3"/>`;
                }
            }

            // Frame border
            svg += `<rect x="${fx}" y="${fy}" width="${frameW}" height="${height}" fill="none" stroke="#3d2e1a" stroke-width="1" rx="2"/>`;
        }

        return svg;
    },

    _hexPoints(cx, cy, r) {
        let pts = [];
        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 180) * (60 * i - 30);
            pts.push(`${(cx + r * Math.cos(angle)).toFixed(1)},${(cy + r * Math.sin(angle)).toFixed(1)}`);
        }
        return pts.join(' ');
    },
    /* ════════════════════════════════════════════
       14g. Visual Gauges
       ════════════════════════════════════════════ */

    renderGauges(hive, state) {
        const totalStores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
        const storeMax = hive.has_super ? 19 : 11;
        const varroaColor = hive.varroa_count > 6 ? '#f44336' : hive.varroa_count > 3 ? '#ff9800' : '#4caf50';
        const popColor = hive.population > 40000 ? '#4caf50' : hive.population > 20000 ? '#ff9800' : '#f44336';
        const storeColor = totalStores >= 7 ? '#DAA520' : totalStores >= 3 ? '#ff9800' : '#f44336';

        return `
        <div class="visual-gauges">
            ${this._renderGauge('🐝 Population', hive.population, 60000, popColor, hive.population.toLocaleString())}
            ${this._renderGauge('🍯 Stores', totalStores, storeMax, storeColor, totalStores + ' frames')}
            ${this._renderGauge('🪲 Varroa', hive.varroa_count, 15, varroaColor, hive.varroa_count + '/300')}
            ${this._renderGauge('👑 Queen', hive.queen === 'present' ? 1 : 0, 1, hive.queen === 'present' ? '#4caf50' : '#f44336', hive.queen === 'present' ? 'Present' : hive.queen === 'failing' ? 'Failing' : 'Missing')}
        </div>`;
    },

    _renderGauge(label, value, max, color, displayValue) {
        const percent = Math.min(100, Math.max(0, (value / max) * 100));
        return `
        <div class="v-gauge">
            <div class="v-gauge-label">${label}</div>
            <div class="v-gauge-track">
                <div class="v-gauge-fill" style="width: ${percent}%; background: ${color};"></div>
            </div>
            <div class="v-gauge-value">${displayValue}</div>
        </div>`;
    },

    /* ════════════════════════════════════════════
       14h. Overview Rendering
       ════════════════════════════════════════════ */

    renderOverview(state) {
        const hives = state.hives.filter(h => !h.dead);
        const el = document.getElementById('tab-overview');
        if (!el) return;

        let html = '<h3 class="section-title">🏠 Your Apiary</h3>';

        if (hives.length === 0) {
            html += `
                <div class="all-dead">
                    <div class="ad-icon">💀</div>
                    <div class="ad-title">All Colonies Have Died</div>
                    <div class="ad-text">Buy a new hive to continue your beekeeping journey.</div>
                    <button class="btn-primary btn-full" style="margin-top: 1rem;" onclick="apiary.buyHive()">🛒 Buy New Hive (£75)</button>
                </div>`;
            el.innerHTML = html;
            return;
        }

        for (const hive of hives) {
            const weeksSince = state.week - hive.inspected_week;
            let inspStatus, inspColor;
            if (weeksSince <= 1 && hive.inspected_week > 0) { inspStatus = '✅ Recent'; inspColor = 'var(--green-leaf)'; }
            else if (weeksSince <= 3) { inspStatus = '⚠️ Overdue'; inspColor = 'var(--amber)'; }
            else { inspStatus = '❓ Unknown'; inspColor = 'var(--danger)'; }

            const totalStores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
            const varroa = hive.varroa_count;
            const varroaLabel = hive.inspected_week > 0 && (state.week - hive.inspected_week) <= 2
                ? (varroa <= 3 ? 'Low' : (varroa <= 6 ? '⚠️ Rising' : '🚨 Critical'))
                : '❓ Unknown';

            const tempKey = hive.temperament || 'moderate';
            const tempConfig = CONFIG && CONFIG.hive_temperaments && CONFIG.hive_temperaments[tempKey];
            const tempBadge = tempConfig
                ? `${tempConfig.icon} ${tempConfig.label}`
                : tempKey;

            html += `
            <div class="hive-card-visual" onclick="apiary.selectHive('${hive.name.replace(/'/g, "\\'")}')">
                <div class="hive-card-svg">${this.renderMiniHive(hive)}</div>
                <div class="hive-card-info">
                    <div class="hive-card-header">
                        <span class="hive-card-name">🐝 ${hive.name}</span>
                        <span class="hive-card-status" style="color: ${inspColor};">${inspStatus}</span>
                    </div>
                    <div class="hive-card-stats">
                        <div class="hive-stat"><div class="hs-label">Population</div><div class="hs-value">${hive.population.toLocaleString()}</div></div>
                        <div class="hive-stat"><div class="hs-label">Stores</div><div class="hs-value">${totalStores} fr</div></div>
                        <div class="hive-stat"><div class="hs-label">Varroa</div><div class="hs-value">${varroaLabel}</div></div>
                        <div class="hive-stat"><div class="hs-label">Queen</div><div class="hs-value">${hive.queen === 'present' ? '👑' : hive.queen === 'failing' ? '⚠️' : hive.queen === 'virgin' ? '🐣' : '💀'}</div></div>
                        <div class="hive-stat"><div class="hs-label">Temperament</div><div class="hs-value"><span class="temperament-badge ${tempKey}" style="font-size:0.75rem">${tempBadge}</span></div></div>
                    </div>
                    ${this._renderMiniGauges(hive)}
                </div>
            </div>`;
        }

        // Buy hive section
        const cost = 75;
        const canBuy = state.money >= cost && hives.length < (state.level + 1);
        html += '<hr class="game-divider"><h3 class="section-title">🛒 Buy New Hive</h3>';
        html += `
        <div class="buy-hive-grid">
            <div class="buy-stat"><div class="stat-label" style="color: var(--amber);">COST</div><div class="stat-value">£${cost}</div></div>
            <div class="buy-stat"><div class="stat-label" style="color: var(--cream-dim);">MAX HIVES</div><div class="stat-value">${state.level + 1} (Level ${state.level})</div></div>
        </div>
        <button class="btn-primary btn-full" onclick="apiary.buyHive()" ${canBuy ? '' : 'disabled'}>🛒 Buy Hive (£${cost})</button>`;

        el.innerHTML = html;
    },

    _renderMiniGauges(hive) {
        const totalStores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
        const storeMax = hive.has_super ? 19 : 11;
        const popPct = Math.min(100, (hive.population / 60000) * 100);
        const storePct = Math.min(100, (totalStores / storeMax) * 100);
        const varroaPct = Math.min(100, (hive.varroa_count / 15) * 100);

        const popColor = hive.population > 40000 ? '#4caf50' : hive.population > 20000 ? '#ff9800' : '#f44336';
        const storeColor = totalStores >= 7 ? '#DAA520' : totalStores >= 3 ? '#ff9800' : '#f44336';
        const varroaColor = hive.varroa_count > 6 ? '#f44336' : hive.varroa_count > 3 ? '#ff9800' : '#4caf50';

        return `
        <div class="mini-gauges">
            <div class="mini-gauge"><div class="mini-gauge-track"><div class="mini-gauge-fill" style="width:${popPct}%; background:${popColor}"></div></div><span class="mini-gauge-label">🐝</span></div>
            <div class="mini-gauge"><div class="mini-gauge-track"><div class="mini-gauge-fill" style="width:${storePct}%; background:${storeColor}"></div></div><span class="mini-gauge-label">🍯</span></div>
            <div class="mini-gauge"><div class="mini-gauge-track"><div class="mini-gauge-fill" style="width:${varroaPct}%; background:${varroaColor}"></div></div><span class="mini-gauge-label">🪲</span></div>
        </div>`;
    },

    /* ════════════════════════════════════════════
       14i. Inspection Rendering
       ════════════════════════════════════════════ */

    renderInspect(state) {
        const el = document.getElementById('tab-inspect');
        const hives = state.hives.filter(h => !h.dead);
        const inspectOk = canInspect(state.weather, state.temperature);

        if (!inspectOk) {
            el.innerHTML = `
                <div class="inspect-blocked">
                    <div class="ib-icon">🚫</div>
                    <div class="ib-title">Cannot Inspect Today</div>
                    <div class="ib-text">Weather: ${state.weather} | Temperature: ${state.temperature}°C<br><span style="font-size: 0.85rem;">(Need ≥14°C and dry)</span></div>
                    <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem; font-style: italic;">In real beekeeping, you should only open the hive on warm, dry days.</div>
                </div>`;
            return;
        }

        let html = '<h3 class="section-title">🔍 Hive Inspection</h3>';
        html += `<div class="inspect-allowed"><span style="color: var(--green-leaf); font-weight: 600;">✅ Good inspection weather!</span> <span style="color: var(--cream);">${state.weather} | ${state.temperature}°C</span></div>`;

        if (hives.length === 0) {
            html += '<p style="color: var(--cream-dim);">No active hives to inspect.</p>';
            el.innerHTML = html;
            return;
        }

        // Hive selector
        html += `<div style="margin-bottom: 1rem;">
            <label style="color: var(--cream); font-weight: 600;">Select Hive:</label>
            <select id="inspect-select" onchange="apiary.doInspectSelect()" style="background: var(--bg-deep); color: var(--cream); border: 1px solid #3d5a3d; border-radius: 8px; padding: 0.5rem; margin-left: 0.5rem; font-size: 0.95rem;">`;
        for (const h of hives) {
            const selected = h.name === state.selectedInspect ? ' selected' : '';
            html += `<option value="${h.name}"${selected}>${h.name}</option>`;
        }
        html += '</select></div>';

        if (!state.selectedInspect || !hives.find(h => h.name === state.selectedInspect)) {
            state.selectedInspect = hives[0].name;
        }

        const hive = hives.find(h => h.name === state.selectedInspect);
        if (!hive) { el.innerHTML = html; return; }

        const weeksSince = state.week - hive.inspected_week;

        // Inspect button
        if (weeksSince > 0 || hive.inspected_week === 0) {
            html += `<div class="inspect-btn-card">
                <div class="inspect-hive-name">🐝 ${hive.name}</div>
                <button class="btn-primary btn-full" onclick="apiary.inspectHive('${hive.name.replace(/'/g, "\\'")}')">🔍 Inspect Hive</button>
            </div>`;
        }

        // Inspection results
        if (hive.inspected_week > 0 && weeksSince <= 2) {
            html += `<p style="color: var(--cream-dim); font-size: 0.85rem; margin-bottom: 1rem;">Last inspected ${weeksSince} week(s) ago</p>`;

            // Detailed hive SVG
            html += `<div class="hive-detail-visual">${this.renderDetailedHive(hive, state)}</div>`;

            // Visual gauges
            html += this.renderGauges(hive, state);

            // Frame legend
            html += `<div class="frame-legend-visual">
                <span class="fl-item"><span class="fl-swatch" style="background:${this.cellColors.honey}"></span> Honey</span>
                <span class="fl-item"><span class="fl-swatch" style="background:${this.cellColors.pollen}"></span> Pollen</span>
                <span class="fl-item"><span class="fl-swatch" style="background:#FFFFFF;border:1px solid #999"></span> Eggs</span>
                <span class="fl-item"><span class="fl-swatch" style="background:${this.cellColors.larvae}"></span> Larvae</span>
                <span class="fl-item"><span class="fl-swatch" style="background:${this.cellColors.capped}"></span> Capped Brood</span>
                <span class="fl-item"><span class="fl-swatch" style="background:${this.cellColors.empty}"></span> Empty</span>
                <span class="fl-item"><span class="fl-swatch" style="background:${this.cellColors.queen_cell}"></span> Queen Cell</span>
            </div>`;

            // Health assessment
            html += this._renderHealthAssessment(hive, state);

            // Education fact
            if (state._lastEduFact) {
                html += `<div class="edu-fact"><div class="edu-label">📚 Did You Know?</div>${state._lastEduFact}</div>`;
            }

            // Temperament & smoker info
            const temp = hive.temperament || 'moderate';
            const tempConfig = CONFIG && CONFIG.hive_temperaments ? CONFIG.hive_temperaments[temp] : { label: temp };
            html += `<div style="margin-top: 0.8rem; display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center;">`;
            html += `<span class="temperament-badge ${temp}">${tempConfig.icon || ''} ${tempConfig.label || temp}</span>`;
            if (hive.smoked) {
                html += '<span class="smoked-indicator">💨 Smoked</span>';
            } else if (temp === 'defensive') {
                html += '<span style="color: #ef9a9a; font-size: 0.8rem; font-weight: 600;">⚠️ Not smoked — higher sting risk!</span>';
            }
            if (hive.stings_this_week > 0) {
                html += `<span style="color: #ef9a9a; font-size: 0.8rem;">🩸 ${hive.stings_this_week} sting${hive.stings_this_week > 1 ? 's' : ''} this inspection</span>`;
            }
            html += '</div>';

        } else if (hive.inspected_week === 0) {
            html += '<p style="color: var(--cream-dim);">🔍 Click <strong>Inspect</strong> to check this hive.</p>';

            const temp = hive.temperament || 'moderate';
            const tempConfig = CONFIG && CONFIG.hive_temperaments ? CONFIG.hive_temperaments[temp] : { label: temp };
            html += `<div style="margin-top: 0.5rem;"><span class="temperament-badge ${temp}">${tempConfig.icon || ''} ${tempConfig.label || temp}</span>`;
            if (temp === 'defensive') {
                html += `<div style="color: #ef9a9a; font-size: 0.85rem; margin-top: 0.3rem;">⚠️ This colony is defensive. Use your smoker before inspecting!</div>`;
            }
            html += '</div>';
        }

        el.innerHTML = html;
    },

    /* ── Health Assessment (visual context version) ── */

    _renderHealthAssessment(hive, state) {
        const issues = [];
        if (hive.queen === 'failing') issues.push('⚠️ Queen is failing — consider requeening');
        if (hive.queen === 'dead') issues.push('🚨 No queen — colony will die without intervention');
        if (hive.varroa_count > 6) issues.push(`🚨 Varroa levels critical (${hive.varroa_count}/300) — treat immediately`);
        else if (hive.varroa_count > 3) issues.push(`Varroa rising (${hive.varroa_count}/300) — treat in Aug/Sep or Dec`);

        const stores = hive.honey_frames + (hive.has_super ? hive.super_honey_frames : 0);
        const season = this.getSeason(state.week);
        if (stores < 4 && (season === 'Autumn' || season === 'Winter')) issues.push('🚨 Winter stores dangerously low — feed now!');
        if (hive.population < 15000) issues.push('⚠️ Colony is weak — may not survive winter');

        if (issues.length > 0) {
            return `<div class="health-bad" style="margin-top: 1rem;"><div class="hb-title">Health Issues:</div>${issues.map(i => `<div style="color: var(--cream-dim); font-size: 0.9rem;">• ${i}</div>`).join('')}</div>`;
        }
        return '<div class="health-good" style="margin-top: 1rem;">✅ Colony looks healthy!</div>';
    },

    /* ════════════════════════════════════════════
       14j. Meadow View
       ════════════════════════════════════════════ */

    renderMeadow(state) {
        const el = document.getElementById('tab-meadow');
        if (!el) return;

        const hives = state.hives.filter(h => !h.dead);
        const deadHives = state.hives.filter(h => h.dead);
        const season = this.getSeason(state.week);
        const theme = this.themes[season] || this.themes.Spring;
        const weather = state.weather || '☀️ Sunny';
        const temperature = state.temperature || 15;

        // Weather settings
        const isRainy = weather.includes('Rainy');
        const isStormy = weather.includes('Stormy');
        const isCloudy = weather.includes('Cloudy');
        const isSunny = weather.includes('Sunny');
        const isWinter = season === 'Winter';

        const beesCanFly = !isRainy && !isStormy && temperature >= 10;
        const highActivity = isSunny && temperature >= 18 && !isWinter;
        const flyingBeeCount = beesCanFly
            ? (highActivity ? Math.min(8, Math.max(2, Math.floor(hives.reduce((s, h) => s + h.population, 0) / 15000))) : Math.min(4, Math.max(1, Math.floor(hives.reduce((s, h) => s + h.population, 0) / 25000))))
            : 0;
        const entranceBees = beesCanFly
            ? Math.min(5, Math.max(1, Math.floor(hives.reduce((s, h) => s + h.population, 0) / 20000)))
            : Math.min(3, Math.floor(hives.reduce((s, h) => s + h.population, 0) / 30000));

        // Sky colours
        let skyStops;
        if (isStormy) skyStops = ['#37474f', '#455a64', '#546e7a'];
        else if (isRainy) skyStops = ['#78909c', '#90a4ae', '#b0bec5'];
        else skyStops = theme.sky;

        const groundWet = isRainy || isStormy;
        const groundColor = groundWet ? this._darkenColor(theme.ground, 0.7) : theme.ground;
        const groundDarkColor = groundWet ? this._darkenColor(theme.groundDark, 0.7) : theme.groundDark;

        let svg = `<svg viewBox="0 0 900 500" class="meadow-svg" xmlns="http://www.w3.org/2000/svg">`;

        // Defs
        svg += `<defs>
            <linearGradient id="meadowSky" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="${skyStops[0]}"/>
                <stop offset="50%" stop-color="${skyStops[1]}"/>
                <stop offset="100%" stop-color="${skyStops[2]}"/>
            </linearGradient>
            <linearGradient id="grassGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="${groundColor}"/>
                <stop offset="100%" stop-color="${groundDarkColor}"/>
            </linearGradient>
        </defs>`;

        // Sky
        svg += `<rect x="0" y="0" width="900" height="320" fill="url(#meadowSky)"/>`;

        // Sun/Moon
        if (isSunny) {
            svg += `<circle cx="780" cy="60" r="35" fill="#FFD54F" opacity="0.9"/>`;
            svg += `<circle cx="780" cy="60" r="42" fill="#FFD54F" opacity="0.15"/>`;
        } else if (isCloudy || isRainy) {
            svg += `<circle cx="780" cy="60" r="30" fill="#FFE082" opacity="0.3"/>`;
        }

        // Clouds
        const cloudCount = isStormy ? 6 : isRainy ? 5 : isCloudy ? 4 : 2;
        const cloudOpacity = isStormy ? 0.8 : isRainy ? 0.6 : 0.4;
        const cloudPositions = [
            { x: 100, y: 40, rx: 70, ry: 22 },
            { x: 140, y: 35, rx: 50, ry: 16 },
            { x: 450, y: 55, rx: 55, ry: 18 },
            { x: 600, y: 30, rx: 65, ry: 20 },
            { x: 700, y: 50, rx: 50, ry: 16 },
            { x: 300, y: 45, rx: 60, ry: 18 }
        ];
        for (let i = 0; i < cloudCount; i++) {
            const c = cloudPositions[i];
            const cloudColor = isStormy ? '#546e7a' : 'white';
            svg += `<ellipse cx="${c.x}" cy="${c.y}" rx="${c.rx}" ry="${c.ry}" fill="${cloudColor}" opacity="${cloudOpacity}" class="cloud-drift" style="animation-delay:${i * 2}s"/>`;
        }

        // Rain
        if (isRainy || isStormy) {
            for (let i = 0; i < (isStormy ? 30 : 15); i++) {
                const rx = Math.random() * 900;
                const ry = Math.random() * 300 + 20;
                svg += `<line x1="${rx}" y1="${ry}" x2="${rx - 3}" y2="${ry + 15}" stroke="${isStormy ? '#90a4ae' : '#b0bec5'}" stroke-width="${isStormy ? 1.5 : 1}" opacity="0.5"/>`;
            }
        }

        // Lightning flash
        if (isStormy) {
            svg += `<rect x="0" y="0" width="900" height="320" fill="white" opacity="0"><animate attributeName="opacity" values="0;0;0;0.3;0;0;0.1;0;0" dur="4s" repeatCount="indefinite"/></rect>`;
        }

        // Distant trees
        if (isWinter) {
            svg += `<line x1="50" y1="240" x2="50" y2="300" stroke="#5d4037" stroke-width="3"/>`;
            svg += `<line x1="80" y1="260" x2="80" y2="300" stroke="#5d4037" stroke-width="2"/>`;
            svg += `<line x1="850" y1="250" x2="850" y2="295" stroke="#5d4037" stroke-width="3"/>`;
        } else {
            svg += `<ellipse cx="50" cy="290" rx="40" ry="60" fill="#2e7d32" opacity="${groundWet ? 0.3 : 0.4}"/>`;
            svg += `<ellipse cx="850" cy="285" rx="35" ry="50" fill="#2e7d32" opacity="${groundWet ? 0.3 : 0.35}"/>`;
            svg += `<ellipse cx="80" cy="295" rx="25" ry="40" fill="#388e3c" opacity="0.3"/>`;
        }

        // Ground
        svg += `<rect x="0" y="300" width="900" height="200" fill="url(#grassGrad)"/>`;
        if (isWinter) {
            svg += `<rect x="0" y="298" width="900" height="200" fill="white" opacity="0.3"/>`;
        }
        svg += `<rect x="0" y="298" width="900" height="4" fill="${groundColor}" opacity="0.5"/>`;

        // Puddles if wet
        if (groundWet) {
            svg += `<ellipse cx="300" cy="370" rx="40" ry="8" fill="#78909c" opacity="0.3"/>`;
            svg += `<ellipse cx="600" cy="390" rx="30" ry="6" fill="#78909c" opacity="0.25"/>`;
            svg += `<ellipse cx="150" cy="400" rx="25" ry="5" fill="#78909c" opacity="0.2"/>`;
        }

        // Path
        const pathColor = groundWet ? '#8d6e63' : '#a1887f';
        svg += `<path d="M0 380 Q200 370 450 380 Q700 390 900 375" fill="${pathColor}" opacity="${groundWet ? 0.2 : 0.3}"/>`;

        // Hives
        const hiveCount = Math.max(hives.length, 1);
        const spacing = Math.min(200, 700 / hiveCount);
        const startX = 100;

        hives.forEach((hive, i) => {
            svg += this._renderMeadowHive(hive, startX + i * spacing, 300, state);
        });

        deadHives.forEach((hive, i) => {
            svg += this._renderMeadowHive(hive, startX + (hives.length + i) * spacing, 300, state);
        });

        // Flowers
        if (!isStormy) {
            const flowerCount = isWinter ? 3 : isRainy ? 5 : 8;
            const flowerColors = ['#ff80ab', '#ffab40', '#69f0ae', '#b388ff', '#ff5252'];
            for (let i = 0; i < flowerCount; i++) {
                let fx, fy;
                do {
                    fx = 20 + Math.random() * 860;
                    fy = 310 + Math.random() * 50;
                } while (fx > startX - 30 && fx < startX + hiveCount * spacing + 30 && fy < 320);

                if (isWinter) {
                    svg += `<circle cx="${fx}" cy="${fy}" r="2" fill="white" opacity="0.7"/>`;
                } else {
                    svg += `<circle cx="${fx}" cy="${fy}" r="3" fill="${flowerColors[Math.floor(Math.random() * flowerColors.length)]}" opacity="${groundWet ? 0.4 : 0.7}"/>`;
                    svg += `<line x1="${fx}" y1="${fy + 2}" x2="${fx}" y2="${fy + 8}" stroke="#4caf50" stroke-width="1" opacity="${groundWet ? 0.3 : 0.5}"/>`;
                }
            }
        }

        // Flying bees
        for (let b = 0; b < flyingBeeCount; b++) {
            const bx = 200 + Math.random() * 500;
            const by = 150 + Math.random() * 120;
            svg += `<text x="${bx}" y="${by}" font-size="${8 + Math.random() * 3}" class="bee-fly" style="animation-delay:${b * 0.7}s">🐝</text>`;
        }

        // Entrance bees
        if (beesCanFly) {
            hives.forEach((hive, i) => {
                const hx = startX + i * spacing;
                const beeCount = Math.min(4, Math.max(1, Math.floor(hive.population / 15000)));
                for (let b = 0; b < beeCount; b++) {
                    const bx = hx - 8 + b * 5;
                    const by = 296 + Math.random() * 3;
                    svg += `<text x="${bx}" y="${by}" font-size="7" class="bee-anim" style="animation-delay:${b * 0.3}s">🐝</text>`;
                }
            });
        } else {
            hives.forEach((hive, i) => {
                if (hive.population > 5000) {
                    const hx = startX + i * spacing;
                    svg += `<text x="${hx - 5}" y="298" font-size="6" opacity="0.6">🐝🐝</text>`;
                }
            });
        }

        // Snow on hive roofs in winter
        if (isWinter) {
            hives.forEach((hive, i) => {
                const hx = startX + i * spacing;
                const roofY = hive.has_super ? 186 : 218;
                svg += `<rect x="${hx - 26}" y="${roofY}" width="52" height="4" fill="white" opacity="0.8" rx="1"/>`;
                svg += `<ellipse cx="${hx}" cy="${roofY}" rx="20" ry="3" fill="white" opacity="0.6"/>`;
            });
        }

        // Wasp indicators (Aug/Sep)
        const month = this.getMonth(state.week);
        if (['August', 'September'].includes(month)) {
            hives.forEach((hive, i) => {
                if (hive.wasp_damage || hive.population < 15000) {
                    const hx = startX + i * spacing;
                    svg += `<text x="${hx + 24}" y="260" font-size="10">🪱</text>`;
                }
            });
        }

        svg += `</svg>`;

        // Weather description
        let html = '<h3 class="section-title">🌿 Apiary Meadow</h3>';
        const weatherDesc = isStormy ? '⛈️ Storm — bees stay inside' : isRainy ? '🌧️ Rain — limited flight' : isCloudy ? '⛅ Cloudy — reduced activity' : '☀️ Good foraging weather';
        html += `<div style="text-align: center; color: var(--cream-dim); font-size: 0.85rem; margin-bottom: 0.5rem;">${weatherDesc} • ${state.temperature}°C</div>`;
        html += `<div class="meadow-container">${svg}</div>`;

        // Summary stats
        const totalPop = hives.reduce((s, h) => s + h.population, 0);
        const totalHoney = hives.reduce((s, h) => s + h.honey_frames + (h.has_super ? h.super_honey_frames : 0), 0);
        html += `<div class="meadow-stats">
            <div class="meadow-stat"><div class="ms-label">🐝 Total Bees</div><div class="ms-value">${totalPop.toLocaleString()}</div></div>
            <div class="meadow-stat"><div class="ms-label">🍯 Total Stores</div><div class="ms-value">${totalHoney} frames</div></div>
            <div class="meadow-stat"><div class="ms-label">🏠 Active Hives</div><div class="ms-value">${hives.length}</div></div>
        </div>`;

        el.innerHTML = html;
    },

    _darkenColor(hex, factor) {
        if (!hex || hex.charAt(0) !== '#') return hex;
        const r = Math.floor(parseInt(hex.slice(1, 3), 16) * factor);
        const g = Math.floor(parseInt(hex.slice(3, 5), 16) * factor);
        const b = Math.floor(parseInt(hex.slice(5, 7), 16) * factor);
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    },

    _renderMeadowHive(hive, x, y, state) {
        const dead = hive.dead;
        const hasSuper = hive.has_super;
        const woodColor = dead ? '#5a3030' : hive.queen === 'failing' ? '#7a5a20' : '#8B6914';
        const roofColor = dead ? '#666' : '#78909c';

        let svg = '';

        // Landing board
        svg += `<rect x="${x - 15}" y="${y + 2}" width="30" height="4" fill="#5a3d2b" rx="1"/>`;
        // Floor
        svg += `<rect x="${x - 22}" y="${y - 3}" width="44" height="5" fill="#4a3525" rx="1"/>`;
        // Entrance
        svg += `<rect x="${x - 10}" y="${y - 8}" width="20" height="5" fill="#1a0f0a" rx="1"/>`;

        // Brood box
        svg += `<rect x="${x - 22}" y="${y - 75}" width="44" height="67" fill="${woodColor}" rx="2" stroke="#3d2e1a" stroke-width="1"/>`;
        const broodFills = this._getFrameFills(hive, 'brood');
        const frameW = 36 / 11;
        for (let i = 0; i < Math.min(broodFills.length, 11); i++) {
            svg += `<rect x="${x - 18 + i * frameW}" y="${y - 72}" width="${frameW - 0.5}" height="60" fill="${broodFills[i]}" rx="0.5" opacity="0.8"/>`;
        }

        // Queen excluder
        svg += `<line x1="${x - 22}" y1="${y - 76}" x2="${x + 22}" y2="${y - 76}" stroke="#999" stroke-width="1.5" stroke-dasharray="3,2"/>`;

        // Super
        if (hasSuper) {
            svg += `<rect x="${x - 22}" y="${y - 115}" width="44" height="38" fill="${woodColor}" rx="2" stroke="#3d2e1a" stroke-width="1"/>`;
            const superFills = this._getFrameFills(hive, 'super');
            const sfW = 36 / 8;
            for (let i = 0; i < Math.min(superFills.length, 8); i++) {
                svg += `<rect x="${x - 18 + i * sfW}" y="${y - 112}" width="${sfW - 0.5}" height="32" fill="${superFills[i]}" rx="0.5" opacity="0.8"/>`;
            }
        }

        // Crown board
        const crownY = hasSuper ? y - 119 : y - 79;
        svg += `<rect x="${x - 21}" y="${crownY}" width="42" height="3" fill="#9e9e9e" rx="0.5"/>`;

        // Roof
        const roofY = crownY - 16;
        svg += `<rect x="${x - 28}" y="${roofY}" width="56" height="16" fill="${roofColor}" rx="2" stroke="#555" stroke-width="0.5"/>`;
        svg += `<rect x="${x - 26}" y="${roofY + 2}" width="52" height="2" fill="#90a4ae" rx="1"/>`;

        // Bees at entrance
        const beeCount = dead ? 0 : Math.min(4, Math.max(1, Math.floor(hive.population / 12000)));
        for (let b = 0; b < beeCount; b++) {
            const bx = x - 8 + b * 5 + Math.random() * 2;
            const by = y - 6 + Math.random() * 3;
            svg += `<text x="${bx}" y="${by}" font-size="7" class="bee-anim" style="animation-delay:${b * 0.4}s">🐝</text>`;
        }

        // Hive name
        svg += `<text x="${x}" y="${y + 20}" text-anchor="middle" font-size="11" fill="${dead ? '#999' : '#e0d5c0'}" font-weight="700" font-family="'Crimson Text', Georgia, serif">${hive.name}</text>`;

        // Dead overlay
        if (dead) {
            svg += `<rect x="${x - 22}" y="${y - 75}" width="44" height="67" fill="rgba(80,20,20,0.5)" rx="2"/>`;
            svg += `<text x="${x}" y="${y - 38}" text-anchor="middle" font-size="16" fill="#f44336">💀</text>`;
        }

        // Foulbrood indicator
        if (hive.has_foulbrood) {
            svg += `<text x="${x + 24}" y="${y - 60}" font-size="12">🦠</text>`;
        }

        // Mice indicator
        if (hive.has_mice_damage) {
            svg += `<text x="${x - 28}" y="${y - 60}" font-size="12">🐭</text>`;
        }

        return svg;
    },

    /* ════════════════════════════════════════════
       14k. Calendar View
       ════════════════════════════════════════════ */

    renderCalendar(state) {
        const el = document.getElementById('tab-calendar');
        if (!el) return;

        const currentMonth = this.getMonth(state.week);
        const currentSeason = this.getSeason(state.week);
        const theme = this.themes[currentSeason] || this.themes.Spring;

        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const seasonIcons = { Spring: '🌸', Summer: '☀️', Autumn: '🍂', Winter: '❄️' };

        const tasks = {
            January: ['Check food stores', 'Heft hives', 'Oxalic acid treatment', 'Order equipment'],
            February: ['Check food stores', 'Heft hives', 'Clear dead bees from entrance', 'Plan the year ahead'],
            March: ['First inspection (if warm)', 'Feed spring syrup (1:1)', 'Remove mouse guards', 'Clean hive floors'],
            April: ['Full inspection', 'Add supers', 'Watch for queen cells', 'Swarm prevention'],
            May: ['Weekly inspections', 'Swarm control', 'Add supers as needed', 'Catch swarms'],
            June: ['Weekly inspections', 'Swarm control continues', 'Add supers', 'First honey harvest possible'],
            July: ['Weekly inspections', 'Harvest spring honey', 'Add supers for summer flow', 'Monitor varroa'],
            August: ['Varroa treatment (Apivar)', 'Harvest summer honey', 'Check queen laying', 'Feed if light'],
            September: ['Continue varroa treatment', 'Remove supers', 'Feed autumn syrup (2:1)', 'Combine weak colonies'],
            October: ['Remove varroa strips', 'Fit mouse guards', 'Reduce entrance', 'Final inspection'],
            November: ['Heft hives', 'Feed fondant if needed', 'Secure roofs', 'Check for mouse damage'],
            December: ['Heft hives', 'Feed fondant', 'Oxalic acid treatment', 'Order next year\'s supplies']
        };

        const currentWeekInMonth = ((state.week - 1) % 4) + 1;

        let html = '<h3 class="section-title">📅 Beekeeping Calendar</h3>';
        html += `<div style="text-align: center; color: var(--cream-dim); font-size: 0.9rem; margin-bottom: 1rem;">${seasonIcons[currentSeason]} ${currentMonth} — Week ${currentWeekInMonth}</div>`;

        html += '<div class="calendar-grid">';
        for (const month of months) {
            const isCurrent = month === currentMonth;
            const mSeason = this.getSeasonByMonth(month);
            const borderColor = isCurrent ? theme.accent : '#3d5a3d';
            const bg = isCurrent ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)' : 'var(--bg-card)';
            const mTasks = tasks[month] || [];
            const icon = seasonIcons[mSeason] || '🌸';

            html += `<div class="cal-month${isCurrent ? ' current' : ''}" style="background: ${bg}; border-color: ${borderColor};">`;
            html += `<div class="cal-month-header">${icon} ${month.substring(0, 3)}</div>`;
            html += '<div class="cal-tasks">';
            for (const task of mTasks) {
                html += `<div class="cal-task">• ${task}</div>`;
            }
            html += '</div></div>';
        }
        html += '</div>';

        el.innerHTML = html;
    },

    /* ── Visual System Init ── */

    init() {
        ParticleCanvas.init();
        if (typeof apiary !== 'undefined' && apiary.state) {
            const season = this.getSeason(apiary.state.week);
            this.applySeason(season);
            this.renderWeatherParticles(apiary.state.weather);
            this.renderSeasonParticles(season);
        }
    }
};


/* ═══════════════════════════════════════════════════════════════
   15. PARTICLE CANVAS SYSTEM
   Seasonal & weather effects rendered on a full-screen canvas
   ═══════════════════════════════════════════════════════════════ */

const ParticleCanvas = {
    canvas: null,
    ctx: null,
    W: 0,
    H: 0,
    particles: [],
    lastTime: 0,
    animRunning: false,
    currentSeason: null,
    currentWeather: null,

    // Wind
    wind: { x: 0, y: 0, gustX: 0, gustTimer: 3, targetGustX: 0 },

    // Spawn timers
    timers: {
        petal: 0, leaf: 0, snow: 0, firefly: 0, rain: 0,
        butterfly: 0, acorn: 0, silk: 0, pollen: 0, breath: 0, shimmer: 0
    },

    // Lightning
    lightningTimer: 6,
    lightningBolts: [],
    lightningFlash: 0,
    screenShake: 0,

    // Frost
    frostCrystals: [],
    frostAlpha: 0,
    frostTarget: 0,

    // Sun rays
    sunRayAlpha: 0,

    /* ── Init ── */

    init() {
        if (this.animRunning) return;
        this.canvas = document.getElementById('particle-canvas');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.lastTime = performance.now();
        this.animRunning = true;
        this.loop();
    },

    resize() {
        this.W = window.innerWidth;
        this.H = window.innerHeight;
        this.canvas.width = this.W;
        this.canvas.height = this.H;
        this.generateFrost();
    },

    /* ── Main Loop ── */

    loop() {
        if (!this.animRunning) return;
        const now = performance.now();
        const dt = Math.min((now - this.lastTime) / 1000, 0.05);
        this.lastTime = now;

        if (!this.currentSeason && typeof apiary !== 'undefined' && apiary.state) {
            this.setSeason(ApiaryVisual.getSeason(apiary.state.week));
            this.setWeather(apiary.state.weather);
        }

        this.updateWind(dt);
        this.update(dt);
        this.spawn(dt);
        this.render();
        requestAnimationFrame(() => this.loop());
    },

    /* ── Wind ── */

    updateWind(dt) {
        const t = performance.now() * 0.001;
        this.wind.x = Math.sin(t * 0.3) * 15 + Math.sin(t * 0.73) * 8;
        this.wind.y = Math.cos(t * 0.2) * 3;

        this.wind.gustTimer -= dt;
        if (this.wind.gustTimer <= 0) {
            this.wind.targetGustX = (Math.random() - 0.3) * 80;
            this.wind.gustTimer = Math.random() * 7 + 3;
        }
        this.wind.gustX += (this.wind.targetGustX - this.wind.gustX) * dt * 0.4;
        this.wind.gustX *= 0.97;
        this.wind.x += this.wind.gustX;

        if (this.currentWeather === 'Stormy') {
            this.wind.x *= 2.5;
            this.wind.y += 5;
        } else if (this.currentWeather && this.currentWeather.includes('Rainy')) {
            this.wind.x *= 1.4;
        }
    },

    /* ── Update All Particles ── */

    update(dt) {
        const t = performance.now() * 0.001;
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.life -= dt;
            if (p.life <= 0 || p.y > this.H + 60 || p.x < -120 || p.x > this.W + 120 || p.y < -120) {
                this.particles.splice(i, 1);
                continue;
            }

            p.x += p.vx * dt + this.wind.x * p.windResp * dt;
            p.y += p.vy * dt + this.wind.y * p.windResp * dt;

            switch (p.type) {
                case 'petal':
                    p.rotation += p.rotSpeed * dt;
                    p.vx += Math.sin(p.y * 0.01 + p.phase) * 25 * dt;
                    if (p.updraft && p.y < this.H * 0.35) p.vy -= 18 * dt;
                    break;
                case 'leaf':
                    p.rotation += p.rotSpeed * dt;
                    p.rotY += p.rotYSpeed * dt;
                    p.vx += Math.sin(p.y * 0.008 + p.phase) * 35 * dt;
                    break;
                case 'snowflake':
                    p.rotation += p.rotSpeed * dt;
                    p.vx += Math.sin(p.y * 0.005 + p.phase) * 12 * dt;
                    break;
                case 'firefly':
                    p.pulsePhase += dt * p.pulseSpeed;
                    p.vx += (Math.sin(t * 0.5 + p.phase) * 18 - p.vx * 0.3) * dt;
                    p.vy += (Math.cos(t * 0.37 + p.phase * 1.3) * 12 - p.vy * 0.3 + 4) * dt;
                    break;
                case 'pollen':
                    p.vx += Math.sin(p.y * 0.012 + p.phase) * 8 * dt;
                    p.vy += Math.cos(p.x * 0.012) * 5 * dt - 3 * dt;
                    break;
                case 'rain':
                    p.x += this.wind.x * 0.25 * dt;
                    break;
                case 'splash':
                    p.radius += p.expandRate * dt;
                    p.alpha -= dt * 2.5;
                    if (p.alpha <= 0) p.life = 0;
                    break;
                case 'acorn':
                    p.rotation += p.rotSpeed * dt;
                    break;
                case 'spiderSilk':
                    p.alpha -= dt * 0.25;
                    if (p.alpha <= 0) p.life = 0;
                    break;
                case 'breathMist':
                    p.radius += 18 * dt;
                    p.alpha -= dt * 0.45;
                    if (p.alpha <= 0) p.life = 0;
                    break;
                case 'butterfly':
                    p.phase += dt * 3.5;
                    p.x += Math.sin(p.phase) * 50 * dt;
                    p.vy = -25 + Math.sin(p.phase * 0.6) * 15;
                    p.wingPhase += dt * 14;
                    p.rotation = Math.sin(p.phase) * 0.3;
                    break;
            }

            // Depth fade near bottom
            if (p.type !== 'firefly' && p.type !== 'splash' && p.type !== 'breathMist') {
                const bottomDist = this.H - p.y;
                p.currentAlpha = bottomDist < 60 ? p.alpha * Math.max(0, bottomDist / 60) : p.alpha;
            } else {
                p.currentAlpha = p.alpha;
            }
        }

        // Lightning
        for (let i = this.lightningBolts.length - 1; i >= 0; i--) {
            this.lightningBolts[i].life -= dt;
            if (this.lightningBolts[i].life <= 0) this.lightningBolts.splice(i, 1);
        }
        if (this.lightningFlash > 0) this.lightningFlash -= dt * 4;
        if (this.screenShake > 0) this.screenShake *= 0.92;
        if (this.screenShake < 0.3) this.screenShake = 0;

        // Frost
        this.frostAlpha += (this.frostTarget - this.frostAlpha) * dt * 0.3;
    },

    /* ── Spawn Particles ── */

    spawn(dt) {
        const season = this.currentSeason;
        const weather = this.currentWeather;

        if (season === 'Spring') {
            this.timers.petal += dt;
            if (this.timers.petal > 0.3 && this.countType('petal') < 40) {
                this.timers.petal = 0;
                this.spawnPetal();
            }
            this.timers.butterfly += dt;
            if (this.timers.butterfly > 8 && this.countType('butterfly') < 2) {
                this.timers.butterfly = 0;
                this.spawnButterfly();
            }
        }

        if (season === 'Summer') {
            this.timers.firefly += dt;
            if (this.timers.firefly > 0.6 && this.countType('firefly') < 28) {
                this.timers.firefly = 0;
                this.spawnFirefly();
            }
            this.timers.pollen += dt;
            if (this.timers.pollen > 0.15 && this.countType('pollen') < 35) {
                this.timers.pollen = 0;
                this.spawnPollen();
            }
            this.sunRayAlpha += (0.12 - this.sunRayAlpha) * dt * 0.5;
        } else {
            this.sunRayAlpha += (0 - this.sunRayAlpha) * dt * 2;
        }

        if (season === 'Autumn') {
            this.timers.leaf += dt;
            if (this.timers.leaf > 0.5 && this.countType('leaf') < 30) {
                this.timers.leaf = 0;
                this.spawnLeaf();
            }
            this.timers.acorn += dt;
            if (this.timers.acorn > 6 && this.countType('acorn') < 2) {
                this.timers.acorn = 0;
                this.spawnAcorn();
            }
            this.timers.silk += dt;
            if (this.timers.silk > 5 && this.countType('spiderSilk') < 4) {
                this.timers.silk = 0;
                this.spawnSpiderSilk();
            }
        }

        if (season === 'Winter') {
            this.timers.snow += dt;
            if (this.timers.snow > 0.06 && this.countType('snowflake') < 90) {
                this.timers.snow = 0;
                this.spawnSnowflake();
            }
            this.timers.breath += dt;
            if (this.timers.breath > 4 && this.countType('breathMist') < 2) {
                this.timers.breath = 0;
                this.spawnBreathMist();
            }
            this.frostTarget = 0.6;
        } else {
            this.frostTarget = 0;
        }

        // Rain
        if (weather && weather.includes('Rainy')) {
            this.timers.rain += dt;
            if (this.timers.rain > 0.015) {
                this.timers.rain = 0;
                for (let i = 0; i < 3; i++) this.spawnRain(false);
                if (Math.random() < dt * 6) this.spawnSplash();
            }
        }

        if (weather && weather.includes('Stormy')) {
            this.timers.rain += dt;
            if (this.timers.rain > 0.008) {
                this.timers.rain = 0;
                for (let i = 0; i < 5; i++) this.spawnRain(true);
                if (Math.random() < dt * 12) this.spawnSplash();
            }
            this.lightningTimer -= dt;
            if (this.lightningTimer <= 0) {
                this.lightningTimer = Math.random() * 6 + 2;
                this.generateLightning();
            }
        }
    },

    countType(type) {
        let c = 0;
        for (const p of this.particles) if (p.type === type) c++;
        return c;
    },

    /* ── Spawn Methods ── */

    spawnPetal() {
        const z = 0.3 + Math.random() * 0.7;
        const colors = ['#FFB6C1', '#FFC0CB', '#FFE4E1', '#FFF0F5', '#FFFFFF'];
        this.particles.push({
            type: 'petal', x: Math.random() * this.W, y: -20 - Math.random() * 40,
            vx: (Math.random() - 0.5) * 20, vy: 30 + Math.random() * 40 + z * 20,
            size: (4 + Math.random() * 6) * (0.4 + z * 0.6),
            rotation: Math.random() * Math.PI * 2, rotSpeed: (Math.random() - 0.5) * 3,
            alpha: (0.5 + Math.random() * 0.4) * (0.4 + z * 0.6),
            color: colors[Math.floor(Math.random() * colors.length)],
            life: 12 + Math.random() * 8, z, windResp: 0.6 + z * 0.4,
            phase: Math.random() * Math.PI * 2, updraft: Math.random() < 0.15,
            rotY: 0, rotYSpeed: 0, pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.5, radius: 0, expandRate: 0
        });
    },

    spawnLeaf() {
        const z = 0.3 + Math.random() * 0.7;
        const subtypes = ['oak', 'maple', 'beech', 'oak', 'maple'];
        const subtype = subtypes[Math.floor(Math.random() * subtypes.length)];
        let color;
        if (subtype === 'oak') color = ['#CD853F', '#D2691E', '#A0522D', '#8B6914'][Math.floor(Math.random() * 4)];
        else if (subtype === 'maple') color = ['#FF6347', '#DC143C', '#B22222', '#FF4500'][Math.floor(Math.random() * 4)];
        else color = ['#DAA520', '#D2B48C', '#CD853F', '#B8860B'][Math.floor(Math.random() * 4)];
        this.particles.push({
            type: 'leaf', x: Math.random() * this.W, y: -30 - Math.random() * 50,
            vx: (Math.random() - 0.5) * 30, vy: 25 + Math.random() * 35 + z * 15,
            size: (8 + Math.random() * 8) * (0.4 + z * 0.6),
            rotation: Math.random() * Math.PI * 2, rotSpeed: (Math.random() - 0.5) * 4,
            alpha: (0.55 + Math.random() * 0.35) * (0.4 + z * 0.6),
            color, subtype, life: 14 + Math.random() * 8, z, windResp: 0.7 + z * 0.3,
            phase: Math.random() * Math.PI * 2, updraft: false,
            rotY: Math.random() * Math.PI * 2, rotYSpeed: (Math.random() - 0.5) * 3,
            pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.5, radius: 0, expandRate: 0
        });
    },

    spawnSnowflake() {
        const z = 0.2 + Math.random() * 0.8;
        const colors = ['#FFFFFF', '#E3F2FD', '#BBDEFB', '#E8EAF6'];
        this.particles.push({
            type: 'snowflake', x: Math.random() * this.W, y: -10 - Math.random() * 30,
            vx: (Math.random() - 0.5) * 10, vy: 15 + Math.random() * 25 + z * 15,
            size: (3 + Math.random() * 7) * (0.3 + z * 0.7),
            rotation: Math.random() * Math.PI * 2, rotSpeed: (Math.random() - 0.5) * 1.5,
            alpha: (0.5 + Math.random() * 0.4) * (0.3 + z * 0.7),
            color: colors[Math.floor(Math.random() * colors.length)],
            life: 15 + Math.random() * 10, z, windResp: 0.4 + z * 0.3,
            phase: Math.random() * Math.PI * 2, updraft: false,
            rotY: 0, rotYSpeed: 0, pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.5, radius: 0, expandRate: 0
        });
    },

    spawnFirefly() {
        const colors = ['#FFFF00', '#FFE082', '#AEEA00', '#FFD54F'];
        this.particles.push({
            type: 'firefly', x: Math.random() * this.W, y: this.H * 0.3 + Math.random() * this.H * 0.5,
            vx: (Math.random() - 0.5) * 20, vy: (Math.random() - 0.5) * 10,
            size: 2 + Math.random() * 3,
            rotation: 0, rotSpeed: 0,
            alpha: 0.8, color: colors[Math.floor(Math.random() * colors.length)],
            life: 8 + Math.random() * 6, z: 0.5 + Math.random() * 0.5, windResp: 0.15,
            phase: Math.random() * Math.PI * 2, updraft: false,
            rotY: 0, rotYSpeed: 0,
            pulsePhase: Math.random() * Math.PI * 2, pulseSpeed: 1.5 + Math.random() * 2,
            wingPhase: 0, currentAlpha: 0.8, radius: 0, expandRate: 0
        });
    },

    spawnPollen() {
        this.particles.push({
            type: 'pollen', x: Math.random() * this.W, y: Math.random() * this.H * 0.7,
            vx: (Math.random() - 0.5) * 8, vy: -5 + Math.random() * 10,
            size: 1 + Math.random() * 2, rotation: 0, rotSpeed: 0,
            alpha: 0.3 + Math.random() * 0.3, color: Math.random() < 0.5 ? '#FFE082' : '#FFD54F',
            life: 6 + Math.random() * 6, z: 0.3 + Math.random() * 0.4, windResp: 0.3,
            phase: Math.random() * Math.PI * 2, updraft: false,
            rotY: 0, rotYSpeed: 0, pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.3, radius: 0, expandRate: 0
        });
    },

    spawnButterfly() {
        const colors = ['#FF80AB', '#CE93D8', '#64B5F6', '#81D4FA', '#FFAB40'];
        this.particles.push({
            type: 'butterfly', x: -30, y: this.H * 0.2 + Math.random() * this.H * 0.4,
            vx: 30 + Math.random() * 40, vy: (Math.random() - 0.5) * 20,
            size: 6 + Math.random() * 4, rotation: 0, rotSpeed: 0,
            alpha: 0.8, color: colors[Math.floor(Math.random() * colors.length)],
            life: 15 + Math.random() * 10, z: 0.6 + Math.random() * 0.4, windResp: 0.4,
            phase: Math.random() * Math.PI * 2, updraft: false,
            rotY: 0, rotYSpeed: 0, pulsePhase: 0, pulseSpeed: 0,
            wingPhase: Math.random() * Math.PI * 2,
            currentAlpha: 0.8, radius: 0, expandRate: 0
        });
    },

    spawnAcorn() {
        this.particles.push({
            type: 'acorn', x: Math.random() * this.W, y: -30,
            vx: (Math.random() - 0.5) * 10, vy: 80 + Math.random() * 40,
            size: 5 + Math.random() * 3, rotation: Math.random() * Math.PI * 2,
            rotSpeed: (Math.random() - 0.5) * 5,
            alpha: 0.85, color: '#8D6E63', life: 5 + Math.random() * 3, z: 0.7,
            windResp: 0.1, phase: 0, updraft: false,
            rotY: 0, rotYSpeed: 0, pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.85, radius: 0, expandRate: 0
        });
    },

    spawnSpiderSilk() {
        const startX = Math.random() * this.W;
        const startY = Math.random() * this.H * 0.3;
        const points = [{ x: startX, y: startY }];
        let cx = startX, cy = startY;
        const segs = 8 + Math.floor(Math.random() * 6);
        for (let i = 0; i < segs; i++) {
            cx += (Math.random() - 0.4) * 30;
            cy += 15 + Math.random() * 25;
            points.push({ x: cx, y: cy });
        }
        this.particles.push({
            type: 'spiderSilk', x: 0, y: 0, vx: 0, vy: 0,
            size: 1, rotation: 0, rotSpeed: 0, alpha: 0.35, color: '#FFFFFF',
            life: 12 + Math.random() * 8, z: 0.5, windResp: 0.5,
            phase: 0, updraft: false, rotY: 0, rotYSpeed: 0,
            pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.35, radius: 0, expandRate: 0,
            points
        });
    },

    spawnBreathMist() {
        this.particles.push({
            type: 'breathMist', x: this.W * 0.3 + Math.random() * this.W * 0.4,
            y: this.H * 0.7 + Math.random() * this.H * 0.15,
            vx: (Math.random() - 0.5) * 5, vy: -8 - Math.random() * 5,
            size: 8, rotation: 0, rotSpeed: 0, alpha: 0.25, color: '#FFFFFF',
            life: 3 + Math.random() * 2, z: 0.6, windResp: 0.2,
            phase: 0, updraft: false, rotY: 0, rotYSpeed: 0,
            pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.25, radius: 5, expandRate: 0
        });
    },

    spawnRain(heavy) {
        const angle = heavy ? 0.4 : 0.2;
        const speed = heavy ? 500 + Math.random() * 200 : 350 + Math.random() * 150;
        this.particles.push({
            type: 'rain', x: Math.random() * (this.W + 200) - 100, y: -20 - Math.random() * 60,
            vx: Math.sin(angle) * speed, vy: Math.cos(angle) * speed,
            size: heavy ? 2 : 1.5, rotation: angle, rotSpeed: 0,
            alpha: heavy ? 0.25 + Math.random() * 0.2 : 0.15 + Math.random() * 0.15,
            color: heavy ? '#90CAF9' : '#BBDEFB',
            life: 2, z: 0.3 + Math.random() * 0.7, windResp: 0.3,
            phase: 0, updraft: false, rotY: 0, rotYSpeed: 0,
            pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.2, radius: 0, expandRate: 0
        });
    },

    spawnSplash() {
        this.particles.push({
            type: 'splash', x: Math.random() * this.W, y: this.H - 10 - Math.random() * 20,
            vx: 0, vy: 0, size: 1, rotation: 0, rotSpeed: 0,
            alpha: 0.5, color: '#90CAF9', life: 0.6, z: 0.5, windResp: 0,
            phase: 0, updraft: false, rotY: 0, rotYSpeed: 0,
            pulsePhase: 0, pulseSpeed: 0, wingPhase: 0,
            currentAlpha: 0.5, radius: 2, expandRate: 25
        });
    },

    /* ── Lightning Generation ── */

    generateLightning() {
        const startX = Math.random() * this.W;
        const bolt = this.createBolt(startX, 0, startX + (Math.random() - 0.5) * 200, this.H * (0.4 + Math.random() * 0.4), 0);
        this.lightningBolts.push({ segments: bolt, life: 0.4, maxLife: 0.4 });
        this.lightningFlash = 0.6;
        this.screenShake = 8;
    },

    createBolt(x1, y1, x2, y2, depth) {
        const segments = [];
        const steps = 8 + Math.floor(Math.random() * 5);
        let prevX = x1, prevY = y1;
        const jitterScale = Math.max(20, 60 / (depth + 1));
        for (let i = 1; i <= steps; i++) {
            const t = i / steps;
            const nx = x1 + (x2 - x1) * t + (i < steps ? (Math.random() - 0.5) * jitterScale : 0);
            const ny = y1 + (y2 - y1) * t + (i < steps ? (Math.random() - 0.5) * jitterScale * 0.3 : 0);
            segments.push({ x1: prevX, y1: prevY, x2: nx, y2: ny });
            if (depth < 2 && Math.random() < 0.35 && i > 1 && i < steps - 1) {
                const branchEndX = nx + (Math.random() - 0.5) * 120;
                const branchEndY = ny + 30 + Math.random() * 80;
                const branch = this.createBolt(nx, ny, branchEndX, branchEndY, depth + 1);
                segments.push(...branch);
            }
            prevX = nx;
            prevY = ny;
        }
        return segments;
    },

    /* ── Frost ── */

    generateFrost() {
        this.frostCrystals = [];
        const edgeCount = 18 + Math.floor(Math.random() * 10);
        for (let i = 0; i < edgeCount; i++) {
            const side = Math.floor(Math.random() * 4);
            let x, y, angle;
            switch (side) {
                case 0: x = Math.random() * this.W; y = Math.random() * 30; angle = Math.PI * 0.5 + (Math.random() - 0.5) * 0.8; break;
                case 1: x = this.W - Math.random() * 30; y = Math.random() * this.H; angle = Math.PI + (Math.random() - 0.5) * 0.8; break;
                case 2: x = Math.random() * this.W; y = this.H - Math.random() * 30; angle = -Math.PI * 0.5 + (Math.random() - 0.5) * 0.8; break;
                default: x = Math.random() * 30; y = Math.random() * this.H; angle = (Math.random() - 0.5) * 0.8; break;
            }
            const branches = [];
            const numBranches = 2 + Math.floor(Math.random() * 3);
            for (let b = 0; b < numBranches; b++) {
                const branchAngle = angle + (Math.random() - 0.5) * 1.2;
                const length = 15 + Math.random() * 40;
                const subBranches = [];
                const numSub = Math.floor(Math.random() * 3);
                for (let s = 0; s < numSub; s++) {
                    const subAngle = branchAngle + (Math.random() - 0.5) * 0.8;
                    const subLen = 5 + Math.random() * 15;
                    subBranches.push({ angle: subAngle, length: subLen, pos: 0.3 + Math.random() * 0.5 });
                }
                branches.push({ angle: branchAngle, length, subBranches });
            }
            this.frostCrystals.push({ x, y, branches, size: 0.5 + Math.random() * 0.5 });
        }
    },

    /* ── Render ── */

    render() {
        const ctx = this.ctx;
        ctx.save();

        if (this.screenShake > 0.5) {
            ctx.translate((Math.random() - 0.5) * this.screenShake, (Math.random() - 0.5) * this.screenShake);
        }

        ctx.clearRect(-10, -10, this.W + 20, this.H + 20);

        // Season background effects
        this.renderSeasonBg(ctx);

        // Particles
        for (const p of this.particles) {
            this.renderParticle(ctx, p);
        }

        // Lightning
        for (const bolt of this.lightningBolts) {
            this.renderLightningBolt(ctx, bolt);
        }

        // Lightning flash
        if (this.lightningFlash > 0.01) {
            ctx.fillStyle = `rgba(200,210,255,${Math.min(this.lightningFlash, 0.5)})`;
            ctx.fillRect(0, 0, this.W, this.H);
        }

        // Frost overlay
        if (this.frostAlpha > 0.01) this.renderFrost(ctx);

        // Storm vignette
        if (this.currentWeather === 'Stormy') this.renderVignette(ctx, 0.45);
        else if (this.currentWeather && this.currentWeather.includes('Rainy')) this.renderVignette(ctx, 0.18);

        // Ground fog
        if (this.currentWeather && (this.currentWeather.includes('Rainy') || this.currentWeather.includes('Stormy'))) {
            this.renderGroundFog(ctx);
        }

        ctx.restore();
    },

    /* ── Season Background ── */

    renderSeasonBg(ctx) {
        if (this.currentSeason === 'Summer' && this.sunRayAlpha > 0.005) {
            this.renderSunRays(ctx);
        }
    },

    renderSunRays(ctx) {
        const cx = this.W - 80, cy = 0;
        const numRays = 8;
        const t = performance.now() * 0.001;
        ctx.save();
        ctx.globalAlpha = this.sunRayAlpha;
        for (let i = 0; i < numRays; i++) {
            const angle = (i / numRays) * Math.PI * 0.8 + Math.sin(t * 0.2 + i) * 0.05;
            const len = this.H * 1.5;
            const width = 30 + Math.sin(t * 0.3 + i * 0.5) * 10;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + Math.cos(angle) * len - Math.sin(angle) * width, cy + Math.sin(angle) * len + Math.cos(angle) * width);
            ctx.lineTo(cx + Math.cos(angle) * len + Math.sin(angle) * width, cy + Math.sin(angle) * len - Math.cos(angle) * width);
            ctx.closePath();
            const grad = ctx.createLinearGradient(cx, cy, cx + Math.cos(angle) * len, cy + Math.sin(angle) * len);
            grad.addColorStop(0, 'rgba(255,248,200,0.3)');
            grad.addColorStop(1, 'rgba(255,248,200,0)');
            ctx.fillStyle = grad;
            ctx.fill();
        }
        ctx.restore();
    },

    /* ── Particle Rendering ── */

    renderParticle(ctx, p) {
        if (p.currentAlpha < 0.01) return;
        switch (p.type) {
            case 'petal': this.drawBlossom(ctx, p); break;
            case 'leaf': this.drawLeaf(ctx, p); break;
            case 'snowflake': this.drawSnowflake(ctx, p); break;
            case 'firefly': this.drawFirefly(ctx, p); break;
            case 'pollen': this.drawPollen(ctx, p); break;
            case 'rain': this.drawRain(ctx, p); break;
            case 'splash': this.drawSplash(ctx, p); break;
            case 'butterfly': this.drawButterfly(ctx, p); break;
            case 'acorn': this.drawAcorn(ctx, p); break;
            case 'spiderSilk': this.drawSpiderSilk(ctx, p); break;
            case 'breathMist': this.drawBreathMist(ctx, p); break;
        }
    },

    /* ── Drawing Methods ── */

    drawBlossom(ctx, p) {
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.globalAlpha = p.currentAlpha;
        const s = p.size;
        ctx.fillStyle = p.color;
        for (let i = 0; i < 5; i++) {
            ctx.save();
            ctx.rotate(i * Math.PI * 2 / 5);
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.bezierCurveTo(s * 0.25, -s * 0.2, s * 0.2, -s * 0.65, 0, -s * 0.85);
            ctx.bezierCurveTo(-s * 0.2, -s * 0.65, -s * 0.25, -s * 0.2, 0, 0);
            ctx.fill();
            ctx.restore();
        }
        ctx.fillStyle = '#FFE082';
        ctx.globalAlpha = p.currentAlpha * 0.8;
        ctx.beginPath();
        ctx.arc(0, 0, s * 0.13, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    },

    drawLeaf(ctx, p) {
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        const ySquash = Math.cos(p.rotY);
        ctx.scale(ySquash, 1);
        ctx.globalAlpha = p.currentAlpha;
        const s = p.size;
        ctx.fillStyle = p.color;
        ctx.strokeStyle = this._darken(p.color, 0.7);
        ctx.lineWidth = 0.5;

        if (p.subtype === 'oak') {
            ctx.beginPath();
            ctx.moveTo(0, -s);
            ctx.lineTo(s * 0.25, -s * 0.75); ctx.lineTo(s * 0.45, -s * 0.65);
            ctx.lineTo(s * 0.2, -s * 0.5); ctx.lineTo(s * 0.4, -s * 0.3);
            ctx.lineTo(s * 0.15, -s * 0.15); ctx.lineTo(s * 0.35, -s * 0.05);
            ctx.lineTo(s * 0.1, s * 0.15); ctx.lineTo(0, s * 0.5);
            ctx.lineTo(-s * 0.1, s * 0.15); ctx.lineTo(-s * 0.35, -s * 0.05);
            ctx.lineTo(-s * 0.15, -s * 0.15); ctx.lineTo(-s * 0.4, -s * 0.3);
            ctx.lineTo(-s * 0.2, -s * 0.5); ctx.lineTo(-s * 0.45, -s * 0.65);
            ctx.lineTo(-s * 0.25, -s * 0.75); ctx.closePath();
            ctx.fill(); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, -s * 0.9); ctx.lineTo(0, s * 0.5);
            ctx.strokeStyle = this._darken(p.color, 0.6); ctx.lineWidth = 1; ctx.stroke();
        } else if (p.subtype === 'maple') {
            ctx.beginPath();
            const pts = 5;
            for (let i = 0; i < pts * 2; i++) {
                const angle = (i * Math.PI / pts) - Math.PI / 2;
                const r = i % 2 === 0 ? s * 0.9 : s * 0.35;
                const px = Math.cos(angle) * r;
                const py = Math.sin(angle) * r;
                if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.closePath(); ctx.fill(); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, s * 0.35); ctx.lineTo(0, s * 1.1);
            ctx.strokeStyle = this._darken(p.color, 0.6); ctx.lineWidth = 1; ctx.stroke();
        } else {
            ctx.beginPath();
            ctx.moveTo(0, -s * 0.9);
            ctx.bezierCurveTo(s * 0.35, -s * 0.5, s * 0.35, s * 0.3, 0, s * 0.7);
            ctx.bezierCurveTo(-s * 0.35, s * 0.3, -s * 0.35, -s * 0.5, 0, -s * 0.9);
            ctx.fill(); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, s * 0.7); ctx.lineTo(0, s * 1.1);
            ctx.strokeStyle = this._darken(p.color, 0.6); ctx.lineWidth = 0.8; ctx.stroke();
        }
        ctx.restore();
    },

    drawSnowflake(ctx, p) {
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.globalAlpha = p.currentAlpha;
        const s = p.size;
        ctx.strokeStyle = p.color;
        ctx.lineWidth = Math.max(0.5, s * 0.08);
        ctx.lineCap = 'round';
        for (let i = 0; i < 6; i++) {
            ctx.save();
            ctx.rotate(i * Math.PI / 3);
            ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -s); ctx.stroke();
            if (s > 4) {
                const branchY = -s * 0.55;
                const branchLen = s * 0.35;
                ctx.beginPath(); ctx.moveTo(0, branchY); ctx.lineTo(branchLen * 0.5, branchY - branchLen * 0.7); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, branchY); ctx.lineTo(-branchLen * 0.5, branchY - branchLen * 0.7); ctx.stroke();
                if (s > 6) {
                    const b2Y = -s * 0.75;
                    const b2Len = s * 0.2;
                    ctx.beginPath(); ctx.moveTo(0, b2Y); ctx.lineTo(b2Len * 0.5, b2Y - b2Len * 0.7); ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(0, b2Y); ctx.lineTo(-b2Len * 0.5, b2Y - b2Len * 0.7); ctx.stroke();
                }
            }
            ctx.restore();
        }
        ctx.fillStyle = p.color;
        ctx.beginPath(); ctx.arc(0, 0, Math.max(0.5, s * 0.1), 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    },

    drawFirefly(ctx, p) {
        const pulse = Math.sin(p.pulsePhase) * 0.5 + 0.5;
        const a = p.currentAlpha * pulse;
        if (a < 0.02) return;
        ctx.save();
        ctx.globalAlpha = a;
        const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 8);
        grad.addColorStop(0, p.color);
        grad.addColorStop(0.3, p.color + '80');
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size * 8, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = Math.min(1, a * 1.5);
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(0.5, p.size * 0.6), 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    },

    drawPollen(ctx, p) {
        ctx.save();
        ctx.globalAlpha = p.currentAlpha;
        ctx.fillStyle = p.color;
        ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(0.5, p.size), 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    },

    drawRain(ctx, p) {
        ctx.save();
        ctx.globalAlpha = p.currentAlpha;
        ctx.strokeStyle = p.color;
        ctx.lineWidth = p.size;
        ctx.lineCap = 'round';
        const len = p.z > 0.5 ? 18 : 12;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x - Math.sin(p.rotation) * len, p.y - Math.cos(p.rotation) * len);
        ctx.stroke();
        ctx.restore();
    },

    drawSplash(ctx, p) {
        ctx.save();
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.strokeStyle = '#90CAF9';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(0.5, p.radius), 0, Math.PI * 2); ctx.stroke();
        ctx.restore();
    },

    drawButterfly(ctx, p) {
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.globalAlpha = p.currentAlpha;
        const s = p.size;
        const wingOpen = Math.cos(p.wingPhase) * 0.7 + 0.3;
        ctx.fillStyle = p.color;
        ctx.save();
        ctx.scale(wingOpen, 1);
        ctx.beginPath(); ctx.ellipse(-s * 0.5, -s * 0.3, s * 0.7, s * 0.5, -0.3, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.ellipse(s * 0.5, -s * 0.3, s * 0.7, s * 0.5, 0.3, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        ctx.save();
        ctx.scale(wingOpen * 0.9, 1);
        ctx.globalAlpha = p.currentAlpha * 0.85;
        ctx.beginPath(); ctx.ellipse(-s * 0.35, s * 0.15, s * 0.45, s * 0.35, -0.2, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.ellipse(s * 0.35, s * 0.15, s * 0.45, s * 0.35, 0.2, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        ctx.fillStyle = '#3E2723';
        ctx.globalAlpha = p.currentAlpha;
        ctx.beginPath(); ctx.ellipse(0, 0, s * 0.1, s * 0.4, 0, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#3E2723'; ctx.lineWidth = 0.5;
        ctx.beginPath(); ctx.moveTo(0, -s * 0.3); ctx.lineTo(-s * 0.15, -s * 0.6);
        ctx.moveTo(0, -s * 0.3); ctx.lineTo(s * 0.15, -s * 0.6); ctx.stroke();
        ctx.restore();
    },

    drawAcorn(ctx, p) {
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        ctx.globalAlpha = p.currentAlpha;
        const s = p.size;
        ctx.fillStyle = '#5D4037';
        ctx.beginPath(); ctx.ellipse(0, -s * 0.15, s * 0.45, s * 0.25, 0, Math.PI, 0); ctx.fill();
        ctx.strokeStyle = '#4E342E'; ctx.lineWidth = 0.5;
        ctx.beginPath(); ctx.moveTo(-s * 0.3, -s * 0.15); ctx.lineTo(-s * 0.3, -s * 0.3);
        ctx.moveTo(0, -s * 0.15); ctx.lineTo(0, -s * 0.35);
        ctx.moveTo(s * 0.3, -s * 0.15); ctx.lineTo(s * 0.3, -s * 0.3); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, -s * 0.35); ctx.lineTo(0, -s * 0.5); ctx.stroke();
        ctx.fillStyle = '#8D6E63';
        ctx.beginPath(); ctx.ellipse(0, s * 0.25, s * 0.35, s * 0.45, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.15)';
        ctx.beginPath(); ctx.ellipse(-s * 0.1, s * 0.15, s * 0.1, s * 0.25, -0.2, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    },

    drawSpiderSilk(ctx, p) {
        if (!p.points || p.points.length < 2) return;
        ctx.save();
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.strokeStyle = p.color; ctx.lineWidth = 0.5;
        ctx.beginPath(); ctx.moveTo(p.points[0].x, p.points[0].y);
        for (let i = 1; i < p.points.length; i++) ctx.lineTo(p.points[i].x, p.points[i].y);
        ctx.stroke();
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        for (let i = 1; i < p.points.length; i += 2) {
            ctx.beginPath(); ctx.arc(p.points[i].x, p.points[i].y + 1, 1, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore();
    },

    drawBreathMist(ctx, p) {
        ctx.save();
        ctx.globalAlpha = Math.max(0, p.alpha);
        const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, Math.max(1, p.radius));
        grad.addColorStop(0, 'rgba(255,255,255,0.15)');
        grad.addColorStop(0.5, 'rgba(255,255,255,0.06)');
        grad.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(1, p.radius), 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    },

    /* ── Lightning Rendering ── */

    renderLightningBolt(ctx, bolt) {
        const alpha = bolt.life / bolt.maxLife;
        ctx.save();
        ctx.shadowColor = '#7986CB'; ctx.shadowBlur = 20;
        ctx.strokeStyle = `rgba(200,210,255,${alpha * 0.9})`;
        ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        ctx.beginPath();
        for (const seg of bolt.segments) { ctx.moveTo(seg.x1, seg.y1); ctx.lineTo(seg.x2, seg.y2); }
        ctx.stroke();
        ctx.shadowBlur = 0;
        ctx.strokeStyle = `rgba(255,255,255,${alpha})`; ctx.lineWidth = 1.5;
        ctx.beginPath();
        for (const seg of bolt.segments) { ctx.moveTo(seg.x1, seg.y1); ctx.lineTo(seg.x2, seg.y2); }
        ctx.stroke();
        ctx.restore();
    },

    /* ── Frost Rendering ── */

    renderFrost(ctx) {
        ctx.save();
        ctx.globalAlpha = this.frostAlpha;
        ctx.strokeStyle = '#E3F2FD'; ctx.lineWidth = 1.5; ctx.lineCap = 'round';
        for (const crystal of this.frostCrystals) {
            for (const branch of crystal.branches) {
                const endX = crystal.x + Math.cos(branch.angle) * branch.length * crystal.size;
                const endY = crystal.y + Math.sin(branch.angle) * branch.length * crystal.size;
                ctx.beginPath(); ctx.moveTo(crystal.x, crystal.y); ctx.lineTo(endX, endY); ctx.stroke();
                for (const sub of branch.subBranches) {
                    const startX2 = crystal.x + Math.cos(branch.angle) * branch.length * crystal.size * sub.pos;
                    const startY2 = crystal.y + Math.sin(branch.angle) * branch.length * crystal.size * sub.pos;
                    const subEndX = startX2 + Math.cos(sub.angle) * sub.length * crystal.size;
                    const subEndY = startY2 + Math.sin(sub.angle) * sub.length * crystal.size;
                    ctx.beginPath(); ctx.moveTo(startX2, startY2); ctx.lineTo(subEndX, subEndY); ctx.stroke();
                }
            }
        }

        // Edge glow
        const edges = [
            { x1: 0, y1: 0, x2: 0, y2: 50, w: this.W },
            { x1: 0, y1: this.H - 50, x2: 0, y2: this.H, w: this.W },
            { x1: 0, y1: 0, w: 50, h: this.H },
            { x1: this.W - 50, y1: 0, w: 50, h: this.H }
        ];
        const grads = [
            ctx.createLinearGradient(0, 0, 0, 50),
            ctx.createLinearGradient(0, this.H, 0, this.H - 50),
            ctx.createLinearGradient(0, 0, 50, 0),
            ctx.createLinearGradient(this.W, 0, this.W - 50, 0)
        ];
        const fills = [
            { x: 0, y: 0, w: this.W, h: 50 },
            { x: 0, y: this.H - 50, w: this.W, h: 50 },
            { x: 0, y: 0, w: 50, h: this.H },
            { x: this.W - 50, y: 0, w: 50, h: this.H }
        ];
        for (let i = 0; i < 4; i++) {
            grads[i].addColorStop(0, 'rgba(200,230,255,0.2)');
            grads[i].addColorStop(1, 'rgba(200,230,255,0)');
            ctx.fillStyle = grads[i];
            ctx.fillRect(fills[i].x, fills[i].y, fills[i].w, fills[i].h);
        }
        ctx.restore();
    },

    /* ── Vignette & Fog ── */

    renderVignette(ctx, alpha) {
        const grad = ctx.createRadialGradient(this.W / 2, this.H / 2, this.H * 0.3, this.W / 2, this.H / 2, this.H * 0.9);
        grad.addColorStop(0, 'rgba(0,0,0,0)');
        grad.addColorStop(1, `rgba(0,0,0,${alpha})`);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, this.W, this.H);
    },

    renderGroundFog(ctx) {
        const fogHeight = 80;
        const grad = ctx.createLinearGradient(0, this.H - fogHeight, 0, this.H);
        grad.addColorStop(0, 'rgba(180,200,210,0)');
        grad.addColorStop(0.5, 'rgba(180,200,210,0.08)');
        grad.addColorStop(1, 'rgba(180,200,210,0.15)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, this.H - fogHeight, this.W, fogHeight);
    },

    /* ── State Setters ── */

    setSeason(season) {
        if (this.currentSeason === season) return;
        this.currentSeason = season;
        this.timers.petal = 0; this.timers.leaf = 0; this.timers.snow = 0;
        this.timers.firefly = 0; this.timers.butterfly = 0; this.timers.acorn = 0;
        this.timers.silk = 0; this.timers.pollen = 0; this.timers.breath = 0;
        if (season === 'Winter') this.generateFrost();
    },

    setWeather(weather) {
        if (this.currentWeather === weather) return;
        this.currentWeather = weather;
        this.timers.rain = 0;
        if (weather && weather.includes('Stormy')) {
            this.lightningTimer = Math.random() * 3 + 1;
        }
    },

    /* ── Utility ── */

    _darken(hex, factor) {
        if (!hex || hex.charAt(0) !== '#') return hex;
        const r = Math.floor(parseInt(hex.slice(1, 3), 16) * factor);
        const g = Math.floor(parseInt(hex.slice(3, 5), 16) * factor);
        const b = Math.floor(parseInt(hex.slice(5, 7), 16) * factor);
        return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
    }
};


/* ═══════════════════════════════════════════════════════════════
   16. INITIALISATION
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    apiary.init();
});

// Start particle system
ParticleCanvas.init();
