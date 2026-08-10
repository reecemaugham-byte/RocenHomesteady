/* ═══════════════════════════════════════════════════════════════
   ROCEN HOMESTEADY — FARM GAMES
   Farm Tycoon · Market Garden
   ═══════════════════════════════════════════════════════════════ */

/* ── TABLE OF CONTENTS ──────────────────────────────────────────
   1.  SHARED HELPERS
       1a. Tab switching & UI
       1b. Toast & float notifications
       1c. State persistence
       1d. Achievement system
       1e. Weather particle renderer (shared)
       1f. Day/time overlay (shared)
   2.  CONFIG (fetched from API)
   3.  FARM TYCOON
       3a. Defaults & state
       3b. Init & save
       3c. Grid creation
       3d. Season / time helpers
       3e. Unlock & forecast logic
       3f. Render methods
       3g. Player actions
       3h. Day advance & weather events
       3i. Reset
   4.  MARKET GARDEN
       4a. Defaults & state
       4b. Init & save
       4c. Month / season helpers
       4d. Soil & companion helpers
       4e. Render methods
       4f. Player actions
       4g. Day advance
       4h. Reset
   5.  INITIALIZATION
   ──────────────────────────────────────────────────────────────── */


// ════════════════════════════════════════════════
// 1. SHARED HELPERS
// ════════════════════════════════════════════════

// ── 1a. Tab switching & UI ──

function switchFarmTab(tabId) {
    document.querySelectorAll('.game-container').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`.tab-btn[data-tab="${tabId}"]`).classList.add('active');
}

function mgSwitchSubTab(tab, evt) {
    document.querySelectorAll('#market-garden .sub-tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('#market-garden .sub-tab-content').forEach(c => c.classList.remove('active'));
    if (evt && evt.target) evt.target.classList.add('active');
    const btn = document.querySelector(`#market-garden .sub-tab[data-tab="${tab}"]`);
    if (btn) btn.classList.add('active');
    const tabEl = document.getElementById(`mg-tab-${tab}`);
    if (tabEl) {
        tabEl.classList.add('active');
    } else {
        console.error('Tab element not found: mg-tab-' + tab);
        return;
    }
    if (tab === 'scene') {
        marketGarden.renderGardenScene();
    }
}


function ftSwitchSubTab(tab, evt) {
    document.querySelectorAll('#farm-tycoon .sub-tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('#farm-tycoon .sub-tab-content').forEach(c => c.classList.remove('active'));

    if (evt && evt.target) evt.target.classList.add('active');

    const tabEl = document.getElementById('ft-tab-' + tab);
    if (tabEl) {
        tabEl.classList.add('active');
    } else {
        console.error('Tab element not found: ft-tab-' + tab + ' — check your HTML has the sub-tab-content divs');
        return;
    }

    if (tab === 'view') {
        farmTycoon.renderFarmScene();
    }
}

function showSceneInfo(evt, el) {
    const panel = document.getElementById('vf-info-panel');
    if (!panel) return;
    const info = el.getAttribute('data-info') || '';
    panel.innerHTML = `<div class="vf-info-detail">${info}</div>`;
    panel.classList.add('visible');

    // Position near the hovered element
    const rect = el.getBoundingClientRect();
    const container = el.closest('.village-farm');
    if (!container) return;
    const containerRect = container.getBoundingClientRect();

    let left = rect.left - containerRect.left + rect.width / 2;
    let top = rect.top - containerRect.top - 10;

    // Keep within bounds
    panel.style.left = left + 'px';
    panel.style.top = top + 'px';
    panel.style.transform = 'translate(-50%, -100%)';
}

function hideSceneInfo() {
    const panel = document.getElementById('vf-info-panel');
    if (panel) panel.classList.remove('visible');
}
function showGardenInfo(evt, el) {
    const panel = document.getElementById('vg-info-panel');
    if (!panel) return;
    const info = el.getAttribute('data-info') || '';
    panel.innerHTML = `<div class="vg-info-detail">${info}</div>`;
    panel.classList.add('visible');
    const rect = el.getBoundingClientRect();
    const container = el.closest('.village-garden');
    if (!container) return;
    const containerRect = container.getBoundingClientRect();
    let left = rect.left - containerRect.left + rect.width / 2;
    let top = rect.top - containerRect.top - 10;
    panel.style.left = left + 'px';
    panel.style.top = top + 'px';
    panel.style.transform = 'translate(-50%, -100%)';
}

function hideGardenInfo() {
    const panel = document.getElementById('vg-info-panel');
    if (panel) panel.classList.remove('visible');
}


// ── 1b. Toast & float notifications ──

function showToast(msg, dur = 3000) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.remove('hidden');
    setTimeout(() => t.classList.add('hidden'), dur);
}

function showFloat(el, text, colour = '#4CAF50') {
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const f = document.createElement('div');
    f.className = 'float-text';
    f.textContent = text;
    f.style.color = colour;
    f.style.left = rect.left + rect.width / 2 + 'px';
    f.style.top = rect.top + 'px';
    document.body.appendChild(f);
    setTimeout(() => f.remove(), 1500);
}

// ── 1c. State persistence ──

function saveState(key, data) {
    try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) { /* quota exceeded */ }
}

function loadState(key, defaults) {
    try {
        const s = localStorage.getItem(key);
        if (s) return { ...defaults, ...JSON.parse(s) };
    } catch (e) { /* parse error */ }
    return { ...defaults };
}

// ── 1d. Achievement system ──

function getAchievements() { return loadState('achievements', {}); }

function setAchievement(key) {
    const a = getAchievements();
    a[key] = true;
    saveState('achievements', a);
    showToast('🏅 Achievement Unlocked!');
}

// ── 1e. Weather particle renderer (shared) ──

function renderWeatherParticles(containerId, season, options = {}) {
    const { isRain = false } = options;
    const container = document.getElementById(containerId);
    if (!container) return;
    let html = '';

    if (season === 'winter') {
        for (let i = 0; i < 25; i++) {
            const left = Math.random() * 100;
            const delay = Math.random() * 8;
            const duration = 6 + Math.random() * 6;
            const size = 4 + Math.random() * 4;
            html += `<div class="snowflake" style="left:${left}%;width:${size}px;height:${size}px;animation-delay:${delay}s;animation-duration:${duration}s;"></div>`;
        }
    }

    if (season === 'autumn') {
        const leaves = ['🍂', '🍁', '🍃'];
        for (let i = 0; i < 8; i++) {
            const left = Math.random() * 100;
            const delay = Math.random() * 10;
            const duration = 8 + Math.random() * 8;
            html += `<div class="leaf-particle" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;">${leaves[i % 3]}</div>`;
        }
    }

    if (isRain) {
        for (let i = 0; i < 30; i++) {
            const left = Math.random() * 100;
            const delay = Math.random() * 2;
            const duration = 0.5 + Math.random() * 0.5;
            const height = 10 + Math.random() * 10;
            html += `<div class="raindrop" style="left:${left}%;height:${height}px;animation-delay:${delay}s;animation-duration:${duration}s;"></div>`;
        }
    }

    if (season === 'summer') {
        for (let i = 0; i < 4; i++) {
            const left = 10 + Math.random() * 80;
            const delay = Math.random() * 6;
            html += `<div class="sun-ray" style="left:${left}%;animation-delay:${delay}s;"></div>`;
        }
    }

    container.innerHTML = html;
}

// ── 1f. Day/time overlay (shared) ──

function getDayTimeClass(day) {
    const d = day % 30;
    if (d < 7) return 'dawn';
    if (d < 15) return 'midday';
    if (d < 22) return 'afternoon';
    if (d < 27) return 'evening';
    return 'night';
}

function updateDayOverlay(overlayId, day) {
    const overlay = document.getElementById(overlayId);
    if (overlay) overlay.className = 'day-overlay ' + getDayTimeClass(day);
}


// ════════════════════════════════════════════════
// 2. CONFIG (fetched from API)
// ════════════════════════════════════════════════

let FT_CONFIG = null;
let MG_CONFIG = null;


// ════════════════════════════════════════════════
// 3. FARM TYCOON
// ════════════════════════════════════════════════

// ═══════════════════════════════════════════════
// FARM SCENE — Palettes & SVG Builders
// ═══════════════════════════════════════════════

const FarmPalettes = {
    spring: {
        sky1:'#87CEEB', sky2:'#B2DFDB', hill1:'#66BB6A', hill2:'#4CAF50',
        meadow:'#81C784', meadowDk:'#66BB6A', river:'#42A5F5', riverLt:'#90CAF9',
        soil:'#795548', soilDk:'#5D4037', soilLt:'#8D6E63',
        trunk:'#5D4037', leaf:'#66BB6A', leafDk:'#4CAF50',
        barn:'#C62828', barnDk:'#8E0000', barnLt:'#EF5350',
        roof:'#D32F2F', roofDk:'#B71C1C',
        stone:'#757575', stoneDk:'#616161',
        accent:'#FFEB3B', accentDk:'#F9A825'
    },
    summer: {
        sky1:'#FFB74D', sky2:'#FFF176', hill1:'#558B2F', hill2:'#33691E',
        meadow:'#689F38', meadowDk:'#558B2F', river:'#1E88E5', riverLt:'#64B5F6',
        soil:'#795548', soilDk:'#5D4037', soilLt:'#8D6E63',
        trunk:'#5D4037', leaf:'#8BC34A', leafDk:'#689F38',
        barn:'#C62828', barnDk:'#8E0000', barnLt:'#EF5350',
        roof:'#D32F2F', roofDk:'#B71C1C',
        stone:'#757575', stoneDk:'#616161',
        accent:'#FFEB3B', accentDk:'#F9A825'
    },
    autumn: {
        sky1:'#FF8A65', sky2:'#FFAB91', hill1:'#BF8C4E', hill2:'#8D6E63',
        meadow:'#A1887F', meadowDk:'#8D6E63', river:'#5C9BD2', riverLt:'#90CAF9',
        soil:'#6D4C41', soilDk:'#4E342E', soilLt:'#8D6E63',
        trunk:'#4E342E', leaf:'#FF9800', leafDk:'#E65100',
        barn:'#8D6E63', barnDk:'#5D4037', barnLt:'#A1887F',
        roof:'#6D4C41', roofDk:'#4E342E',
        stone:'#757575', stoneDk:'#616161',
        accent:'#FFB300', accentDk:'#FF8F00'
    },
    winter: {
        sky1:'#B0BEC5', sky2:'#E0E0E0', hill1:'#CFD8DC', hill2:'#B0BEC5',
        meadow:'#ECEFF1', meadowDk:'#CFD8DC', river:'#90A4AE', riverLt:'#B0BEC5',
        soil:'#6D4C41', soilDk:'#5D4037', soilLt:'#8D6E63',
        trunk:'#5D4037', leaf:'#CFD8DC', leafDk:'#B0BEC5',
        barn:'#8D6E63', barnDk:'#5D4037', barnLt:'#A1887F',
        roof:'#ECEFF1', roofDk:'#CFD8DC',
        stone:'#9E9E9E', stoneDk:'#757575',
        accent:'#E0E0E0', accentDk:'#B0BEC5'
    }
};

const FarmSVGs = {

    empty: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="12" width="36" height="26" rx="3" fill="${p.soil}"/>
        <rect x="4" y="14" width="32" height="22" rx="2" fill="${p.soilDk}"/>
        <line x1="8" y1="20" x2="32" y2="20" stroke="${p.soilLt}" stroke-width="0.5" opacity="0.5"/>
        <line x1="8" y1="26" x2="32" y2="26" stroke="${p.soilLt}" stroke-width="0.5" opacity="0.5"/>
        <line x1="8" y1="32" x2="32" y2="32" stroke="${p.soilLt}" stroke-width="0.5" opacity="0.5"/>
    </svg>`,

    seed: (p, crop) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="12" width="36" height="26" rx="3" fill="${p.soil}"/>
        <rect x="4" y="14" width="32" height="22" rx="2" fill="${p.soilDk}"/>
        <ellipse cx="20" cy="22" rx="2" ry="1.5" fill="${p.soilLt}"/>
        <line x1="20" y1="18" x2="20" y2="21" stroke="${p.leafDk}" stroke-width="1" stroke-linecap="round"/>
        <circle cx="20" cy="17" r="1.5" fill="${p.leaf}"/>
    </svg>`,

    growing: (p, crop) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="12" width="36" height="26" rx="3" fill="${p.soil}"/>
        <rect x="4" y="14" width="32" height="22" rx="2" fill="${p.soilDk}"/>
        <line x1="20" y1="35" x2="20" y2="14" stroke="${p.trunk}" stroke-width="1.5" stroke-linecap="round"/>
        <ellipse cx="14" cy="18" rx="4" ry="2.5" fill="${p.leaf}" transform="rotate(-25 14 18)"/>
        <ellipse cx="26" cy="18" rx="4" ry="2.5" fill="${p.leaf}" transform="rotate(25 26 18)"/>
        <ellipse cx="17" cy="14" rx="3" ry="2" fill="${p.leafDk}" transform="rotate(-15 17 14)"/>
        <ellipse cx="23" cy="14" rx="3" ry="2" fill="${p.leafDk}" transform="rotate(15 23 14)"/>
    </svg>`,

    ready: (p, crop) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="12" width="36" height="26" rx="3" fill="${p.soil}"/>
        <rect x="4" y="14" width="32" height="22" rx="2" fill="${p.soilDk}"/>
        <line x1="20" y1="36" x2="20" y2="8" stroke="${p.trunk}" stroke-width="2" stroke-linecap="round"/>
        <ellipse cx="12" cy="14" rx="5" ry="3" fill="${p.leaf}" transform="rotate(-30 12 14)"/>
        <ellipse cx="28" cy="14" rx="5" ry="3" fill="${p.leaf}" transform="rotate(30 28 14)"/>
        <ellipse cx="15" cy="9" rx="4" ry="2.5" fill="${p.leafDk}" transform="rotate(-15 15 9)"/>
        <ellipse cx="25" cy="9" rx="4" ry="2.5" fill="${p.leafDk}" transform="rotate(15 25 9)"/>
        <circle cx="20" cy="7" r="3.5" fill="${p.accent}" opacity="0.9"/>
        <circle cx="20" cy="7" r="2" fill="${p.accentDk}" opacity="0.6"/>
    </svg>`,

    rock: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="20" cy="32" rx="15" ry="5" fill="rgba(0,0,0,0.15)"/>
        <path d="M8,30 L6,22 L10,16 L16,12 L24,11 L30,14 L34,20 L33,28 L30,31 Z" fill="${p.stone}" stroke="${p.stoneDk}" stroke-width="0.8" stroke-linejoin="round"/>
        <path d="M12,18 L16,14 L22,16 L26,18" fill="none" stroke="${p.stoneDk}" stroke-width="0.5" opacity="0.4"/>
        <path d="M10,24 L14,20 L20,22" fill="none" stroke="${p.stoneDk}" stroke-width="0.5" opacity="0.3"/>
        <ellipse cx="19" cy="19" rx="6" ry="3" fill="white" opacity="0.08"/>
        <path d="M16,26 L22,24 L28,27" fill="none" stroke="${p.stoneDk}" stroke-width="0.4" opacity="0.2"/>
    </svg>`,

    weed: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="12" width="36" height="26" rx="3" fill="${p.soil}"/>
        <rect x="4" y="14" width="32" height="22" rx="2" fill="${p.soilDk}"/>
        <path d="M18,36 Q16,28 14,22 Q12,18 16,16" fill="none" stroke="#4CAF50" stroke-width="1" stroke-linecap="round"/>
        <path d="M22,36 Q24,26 26,20 Q28,16 24,14" fill="none" stroke="#66BB6A" stroke-width="1" stroke-linecap="round"/>
        <path d="M20,36 Q20,30 18,24 Q16,20 20,18" fill="none" stroke="#388E3C" stroke-width="1" stroke-linecap="round"/>
        <circle cx="14" cy="15" r="1.5" fill="#66BB6A" opacity="0.7"/>
        <circle cx="26" cy="13" r="1.5" fill="#4CAF50" opacity="0.7"/>
        <circle cx="20" cy="17" r="1" fill="#388E3C" opacity="0.7"/>
    </svg>`,

    barn: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="4" y="22" width="32" height="16" rx="2" fill="${p.barn}"/>
        <rect x="6" y="24" width="28" height="12" rx="1" fill="${p.barnDk}"/>
        <polygon points="20,8 3,22 37,22" fill="${p.roof}"/>
        <polygon points="20,8 3,22 37,22" fill="none" stroke="${p.roofDk}" stroke-width="0.5"/>
        <rect x="16" y="28" width="8" height="10" rx="1" fill="${p.barn}" stroke="${p.barnDk}" stroke-width="0.5"/>
        <line x1="20" y1="28" x2="20" y2="38" stroke="${p.barnDk}" stroke-width="0.5"/>
        <rect x="8" y="25" width="4" height="4" rx="0.5" fill="#81D4FA" opacity="0.6"/>
        <rect x="28" y="25" width="4" height="4" rx="0.5" fill="#81D4FA" opacity="0.6"/>
    </svg>`,

    beehive: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <line x1="20" y1="38" x2="20" y2="22" stroke="#5D4037" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M11,24 Q11,16 15,12 Q20,8 25,12 Q29,16 29,24 Z" fill="#F9A825" stroke="#E65100" stroke-width="0.8"/>
        <path d="M13,19 Q20,17 27,19" fill="none" stroke="#E65100" stroke-width="1.2" opacity="0.5"/>
        <path d="M12,22 Q20,20 28,22" fill="none" stroke="#E65100" stroke-width="1.2" opacity="0.5"/>
        <ellipse cx="20" cy="24" rx="3.5" ry="2" fill="#5D4037"/>
        <ellipse cx="20" cy="11" rx="5" ry="2.5" fill="#D4A017" stroke="#A07810" stroke-width="0.5"/>
        <circle cx="32" cy="14" r="1.8" fill="#FDD835" stroke="#F9A825" stroke-width="0.3"/>
        <ellipse cx="33.2" cy="14" rx="1.2" ry="1.8" fill="rgba(255,255,255,0.4)" transform="rotate(-20,33.2,14)"/>
        <line x1="30.2" y1="12.5" x2="29" y2="11" stroke="#3E2723" stroke-width="0.4"/>
        <line x1="30.2" y1="15.5" x2="29" y2="17" stroke="#3E2723" stroke-width="0.4"/>
        <circle cx="9" cy="16" r="1.8" fill="#FDD835" stroke="#F9A825" stroke-width="0.3"/>
        <ellipse cx="7.8" cy="16" rx="1.2" ry="1.8" fill="rgba(255,255,255,0.4)" transform="rotate(20,7.8,16)"/>
        <line x1="10.8" y1="14.5" x2="12" y2="13" stroke="#3E2723" stroke-width="0.4"/>
        <line x1="10.8" y1="17.5" x2="12" y2="19" stroke="#3E2723" stroke-width="0.4"/>
        <circle cx="28" cy="10" r="1.5" fill="#FDD835" stroke="#F9A825" stroke-width="0.3"/>
        <ellipse cx="29" cy="10" rx="1" ry="1.5" fill="rgba(255,255,255,0.4)"/>
    </svg>`,

    scarecrow: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <line x1="20" y1="38" x2="20" y2="10" stroke="#5D4037" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="9" y1="19" x2="31" y2="19" stroke="#5D4037" stroke-width="2" stroke-linecap="round"/>
        <circle cx="20" cy="8" r="4.5" fill="#FFCC80" stroke="#5D4037" stroke-width="0.6"/>
        <polygon points="11,7 14,4 26,4 29,7 26,8 20,5 14,8" fill="${p.roof}" stroke="${p.roofDk}" stroke-width="0.4"/>
        <rect x="13" y="6" width="14" height="2.5" rx="0.5" fill="${p.roofDk}"/>
        <path d="M9,19 L6,24" stroke="#C9A94E" stroke-width="2" stroke-linecap="round"/>
        <path d="M31,19 L34,24" stroke="#C9A94E" stroke-width="2" stroke-linecap="round"/>
        <rect x="16" y="15" width="8" height="10" rx="1.5" fill="#C62828" opacity="0.85"/>
        <line x1="20" y1="25" x2="20" y2="38" stroke="#3E2723" stroke-width="1.5"/>
        <circle cx="18" cy="7.5" r="0.7" fill="#3E2723"/>
        <circle cx="22" cy="7.5" r="0.7" fill="#3E2723"/>
        <path d="M18,10 Q20,11.5 22,10" fill="none" stroke="#3E2723" stroke-width="0.6"/>
        <path d="M9,19 L7,17 L9,19 L7,21" stroke="#C9A94E" stroke-width="0.8" fill="none"/>
        <path d="M31,19 L33,17 L31,19 L33,21" stroke="#C9A94E" stroke-width="0.8" fill="none"/>
    </svg>`,

    sprinkler: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="14" width="36" height="24" rx="3" fill="${p.soil}"/>
        <rect x="4" y="16" width="32" height="20" rx="2" fill="${p.soilDk}"/>
        <line x1="20" y1="38" x2="20" y2="20" stroke="#78909C" stroke-width="2"/>
        <circle cx="20" cy="18" r="2.5" fill="#90A4AE" stroke="#546E7A" stroke-width="0.5"/>
        <circle cx="14" cy="12" r="1" fill="#42A5F5" opacity="0.7">
            <animate attributeName="cy" values="12;16;12" dur="1.5s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.7;0.2;0.7" dur="1.5s" repeatCount="indefinite"/>
        </circle>
        <circle cx="26" cy="12" r="1" fill="#42A5F5" opacity="0.7">
            <animate attributeName="cy" values="12;16;12" dur="1.8s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.7;0.2;0.7" dur="1.8s" repeatCount="indefinite"/>
        </circle>
        <circle cx="20" cy="10" r="1" fill="#42A5F5" opacity="0.7">
            <animate attributeName="cy" values="10;14;10" dur="1.3s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.7;0.2;0.7" dur="1.3s" repeatCount="indefinite"/>
        </circle>
    </svg>`,

    coldFrame: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="4" y="20" width="32" height="18" rx="2" fill="${p.soil}"/>
        <rect x="6" y="22" width="28" height="14" rx="1" fill="${p.soilDk}"/>
        <rect x="6" y="16" width="28" height="8" rx="1" fill="#B2EBF2" opacity="0.4" stroke="#26C6DA" stroke-width="0.5"/>
        <line x1="6" y1="20" x2="34" y2="20" stroke="#5D4037" stroke-width="1.5"/>
        <line x1="20" y1="16" x2="20" y2="24" stroke="#5D4037" stroke-width="0.5" opacity="0.4"/>
        <path d="M6,16 L20,12 L34,16" fill="none" stroke="#26C6DA" stroke-width="0.8"/>
    </svg>`,

    manor: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="4" y="22" width="32" height="16" rx="1" fill="#D7CCC8"/>
        <rect x="6" y="24" width="28" height="12" rx="1" fill="#BCAAA4"/>
        <polygon points="20,6 2,22 38,22" fill="${p.roof}" stroke="${p.roofDk}" stroke-width="0.5"/>
        <rect x="14" y="28" width="12" height="10" rx="1" fill="#8D6E63"/>
        <line x1="20" y1="28" x2="20" y2="38" stroke="#5D4037" stroke-width="0.5"/>
        <circle cx="20" cy="33" r="1" fill="#FFD54F" opacity="0.7"/>
        <rect x="8" y="25" width="4" height="4" rx="0.5" fill="#81D4FA" opacity="0.6"/>
        <rect x="28" y="25" width="4" height="4" rx="0.5" fill="#81D4FA" opacity="0.6"/>
        <rect x="8" y="31" width="3" height="3" rx="0.5" fill="#81D4FA" opacity="0.5"/>
        <rect x="29" y="31" width="3" height="3" rx="0.5" fill="#81D4FA" opacity="0.5"/>
        <rect x="16" y="10" width="8" height="4" rx="0.5" fill="#81D4FA" opacity="0.4"/>
    </svg>`,

    chicken: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="14" width="36" height="24" rx="3" fill="${p.soil}"/>
        <rect x="4" y="16" width="32" height="20" rx="2" fill="${p.soilDk}"/>
        <rect x="4" y="14" width="32" height="4" rx="1" fill="#8D6E63" stroke="#5D4037" stroke-width="0.5"/>
        <line x1="6" y1="14" x2="6" y2="18" stroke="#5D4037" stroke-width="1"/>
        <line x1="34" y1="14" x2="34" y2="18" stroke="#5D4037" stroke-width="1"/>
    </svg>`,

    cow: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="14" width="36" height="24" rx="3" fill="${p.soil}"/>
        <rect x="4" y="16" width="32" height="20" rx="2" fill="${p.soilDk}"/>
        <line x1="4" y1="16" x2="36" y2="16" stroke="#6D4C41" stroke-width="1.5"/>
        <line x1="4" y1="38" x2="36" y2="38" stroke="#6D4C41" stroke-width="1.5"/>
        <line x1="4" y1="16" x2="4" y2="38" stroke="#6D4C41" stroke-width="1.5"/>
        <line x1="36" y1="16" x2="36" y2="38" stroke="#6D4C41" stroke-width="1.5"/>
        <rect x="10" y="14" width="8" height="4" rx="1" fill="#8D6E63" stroke="#5D4037" stroke-width="0.5"/>
        <rect x="22" y="14" width="8" height="4" rx="1" fill="#8D6E63" stroke="#5D4037" stroke-width="0.5"/>
    </svg>`,

    goat: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="14" width="36" height="24" rx="3" fill="${p.soil}"/>
        <rect x="4" y="16" width="32" height="20" rx="2" fill="${p.soilDk}"/>
        <line x1="4" y1="16" x2="36" y2="16" stroke="#6D4C41" stroke-width="1.5"/>
        <line x1="4" y1="38" x2="36" y2="38" stroke="#6D4C41" stroke-width="1.5"/>
        <line x1="4" y1="16" x2="4" y2="38" stroke="#6D4C41" stroke-width="1.5"/>
        <line x1="36" y1="16" x2="36" y2="38" stroke="#6D4C41" stroke-width="1.5"/>
        <rect x="14" y="14" width="12" height="4" rx="1" fill="#8D6E63" stroke="#5D4037" stroke-width="0.5"/>
    </svg>`
};
const GardenPalettes = {
    spring: {
        sky1:'#87CEEB', sky2:'#C8E6C9',
        wall:'#D7CCC8', wallDk:'#BCAAA4',
        ground:'#A1887F', groundDk:'#8D6E63',
        soil:'#6D4C41', soilDk:'#4E342E', soilLt:'#8D6E63',
        bed:'#5D4037', bedDk:'#3E2723', bedLt:'#795548',
        bedGood:'#2E7D32', bedFair:'#F57F17', bedPoor:'#C62828',
        stall:'#8D6E63', stallDk:'#5D4037', stallLt:'#A1887F',
        awning1:'#C62828', awning2:'#FFC107',
        plant:'#66BB6A', plantDk:'#388E3C',
        accent:'#FFEB3B', accentDk:'#F9A825',
        pipe:'#78909C', pipeLt:'#B0BEC5'
    },
    summer: {
        sky1:'#FFB74D', sky2:'#FFF176',
        wall:'#EFEBE9', wallDk:'#D7CCC8',
        ground:'#A1887F', groundDk:'#8D6E63',
        soil:'#6D4C41', soilDk:'#4E342E', soilLt:'#8D6E63',
        bed:'#5D4037', bedDk:'#3E2723', bedLt:'#795548',
        bedGood:'#2E7D32', bedFair:'#F57F17', bedPoor:'#C62828',
        stall:'#8D6E63', stallDk:'#5D4037', stallLt:'#A1887F',
        awning1:'#D32F2F', awning2:'#FF8F00',
        plant:'#8BC34A', plantDk:'#558B2F',
        accent:'#FFEB3B', accentDk:'#F9A825',
        pipe:'#78909C', pipeLt:'#B0BEC5'
    },
    autumn: {
        sky1:'#FF8A65', sky2:'#FFAB91',
        wall:'#BCAAA4', wallDk:'#A1887F',
        ground:'#8D6E63', groundDk:'#795548',
        soil:'#5D4037', soilDk:'#3E2723', soilLt:'#795548',
        bed:'#5D4037', bedDk:'#3E2723', bedLt:'#795548',
        bedGood:'#2E7D32', bedFair:'#F57F17', bedPoor:'#C62828',
        stall:'#795548', stallDk:'#4E342E', stallLt:'#8D6E63',
        awning1:'#BF360C', awning2:'#E65100',
        plant:'#FF9800', plantDk:'#E65100',
        accent:'#FFB300', accentDk:'#FF8F00',
        pipe:'#607D8B', pipeLt:'#90A4AE'
    },
    winter: {
        sky1:'#B0BEC5', sky2:'#E0E0E0',
        wall:'#CFD8DC', wallDk:'#B0BEC5',
        ground:'#9E9E9E', groundDk:'#757575',
        soil:'#6D4C41', soilDk:'#4E342E', soilLt:'#8D6E63',
        bed:'#5D4037', bedDk:'#3E2723', bedLt:'#795548',
        bedGood:'#2E7D32', bedFair:'#F57F17', bedPoor:'#C62828',
        stall:'#8D6E63', stallDk:'#5D4037', stallLt:'#A1887F',
        awning1:'#B71C1C', awning2:'#FF6F00',
        plant:'#CFD8DC', plantDk:'#B0BEC5',
        accent:'#E0E0E0', accentDk:'#B0BEC5',
        pipe:'#90A4AE', pipeLt:'#CFD8DC'
    }
};

const GardenSVGs = {

    emptyBed: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="36" height="32" rx="3" fill="${p.bed}"/>
        <rect x="4" y="8" width="32" height="28" rx="2" fill="${p.bedDk}"/>
        <line x1="8" y1="15" x2="32" y2="15" stroke="${p.bedLt}" stroke-width="0.6" opacity="0.5"/>
        <line x1="8" y1="22" x2="32" y2="22" stroke="${p.bedLt}" stroke-width="0.6" opacity="0.5"/>
        <line x1="8" y1="29" x2="32" y2="29" stroke="${p.bedLt}" stroke-width="0.6" opacity="0.5"/>
        <rect x="2" y="6" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.7"/>
        <rect x="2" y="35" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.5"/>
    </svg>`,

    seededBed: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="36" height="32" rx="3" fill="${p.bed}"/>
        <rect x="4" y="8" width="32" height="28" rx="2" fill="${p.bedDk}"/>
        <line x1="8" y1="15" x2="32" y2="15" stroke="${p.bedLt}" stroke-width="0.6" opacity="0.4"/>
        <line x1="8" y1="22" x2="32" y2="22" stroke="${p.bedLt}" stroke-width="0.6" opacity="0.4"/>
        <circle cx="20" cy="20" r="2.5" fill="${p.plant}" opacity="0.8"/>
        <line x1="20" y1="16" x2="20" y2="19" stroke="${p.plantDk}" stroke-width="0.8" stroke-linecap="round"/>
        <rect x="2" y="6" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.7"/>
        <rect x="2" y="35" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.5"/>
    </svg>`,

    growingBed: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="36" height="32" rx="3" fill="${p.bed}"/>
        <rect x="4" y="8" width="32" height="28" rx="2" fill="${p.bedDk}"/>
        <line x1="20" y1="34" x2="20" y2="16" stroke="${p.plantDk}" stroke-width="1.5" stroke-linecap="round"/>
        <ellipse cx="14" cy="19" rx="4" ry="2.5" fill="${p.plant}" transform="rotate(-25 14 19)"/>
        <ellipse cx="26" cy="19" rx="4" ry="2.5" fill="${p.plant}" transform="rotate(25 26 19)"/>
        <ellipse cx="17" cy="14" rx="3" ry="2" fill="${p.plantDk}" transform="rotate(-15 17 14)"/>
        <ellipse cx="23" cy="14" rx="3" ry="2" fill="${p.plantDk}" transform="rotate(15 23 14)"/>
        <rect x="2" y="6" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.7"/>
        <rect x="2" y="35" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.5"/>
    </svg>`,

    readyBed: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="36" height="32" rx="3" fill="${p.bed}"/>
        <rect x="4" y="8" width="32" height="28" rx="2" fill="${p.bedDk}"/>
        <line x1="20" y1="35" x2="20" y2="10" stroke="${p.plantDk}" stroke-width="2" stroke-linecap="round"/>
        <ellipse cx="12" cy="15" rx="5" ry="3" fill="${p.plant}" transform="rotate(-30 12 15)"/>
        <ellipse cx="28" cy="15" rx="5" ry="3" fill="${p.plant}" transform="rotate(30 28 15)"/>
        <ellipse cx="16" cy="10" rx="4" ry="2.5" fill="${p.plantDk}" transform="rotate(-15 16 10)"/>
        <ellipse cx="24" cy="10" rx="4" ry="2.5" fill="${p.plantDk}" transform="rotate(15 24 10)"/>
        <circle cx="20" cy="8" r="3.5" fill="${p.accent}" opacity="0.9"/>
        <circle cx="20" cy="8" r="2" fill="${p.accentDk}" opacity="0.6"/>
        <rect x="2" y="6" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.7"/>
        <rect x="2" y="35" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.5"/>
    </svg>`,

    winterBed: (p) => `<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="6" width="36" height="32" rx="3" fill="${p.bed}"/>
        <rect x="4" y="8" width="32" height="28" rx="2" fill="${p.bedDk}" opacity="0.6"/>
        <ellipse cx="20" cy="20" rx="12" ry="4" fill="white" opacity="0.12"/>
        <ellipse cx="14" cy="26" rx="4" ry="1.5" fill="white" opacity="0.18"/>
        <ellipse cx="28" cy="24" rx="3" ry="1" fill="white" opacity="0.15"/>
        <circle cx="10" cy="18" r="1" fill="white" opacity="0.2"/>
        <circle cx="30" cy="16" r="1.2" fill="white" opacity="0.2"/>
        <rect x="2" y="6" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.4"/>
        <rect x="2" y="35" width="36" height="2.5" rx="1.5" fill="${p.stall}" opacity="0.3"/>
    </svg>`
};


const farmTycoon = {

    // ── 3a. Defaults & state ──

    defaults: {
        grid: null,
        money: 150,
        day: 1,
        inventory: { Feed: 0 },
        market_prices: null,
        soil_health: null,
        manor_bought: false,
        win_shown: false,
        fallow_days: null,
        sales_log: {},
        crop_map: {},
        last_event: "",
        market_event: null,
        total_harvests: 0,
        total_earned: 0,
        placing_mode: null,
        damaged_buildings: [],
        owned_buildings: {},
        tool: "Wheat",
        build_sel: "None",
        achievements: {
            farm_harvest: false,
            farm_rancher: false,
            farm_winner: false,
            farm_fisher: false,
            farm_rockbreaker: false,
            farm_greenhouse: false,
            farm_rich: false,
            farm_mogul: false,
            farm_diverse: false,
            farm_beekeeper: false,
            farm_scarer: false,
            farm_sprinkler: false
        },
        weather_visual: "clear",
        unlocked_crops: ["Wheat", "Carrot", "Corn"],
        active_contract: null,
        contract_progress: 0,
        weather_forecast: null,
        fishing_today: 0,
        harvest_families: {},
    },

    state: null,

    // ── 3b. Init & save ──

    init() {
        this.state = loadState('ft_state', this.defaults);

        // Ensure arrays exist
        if (!this.state.grid || !Array.isArray(this.state.grid) || this.state.grid.length === 0) {
            this.state.grid = this.createGrid();
        }
        if (!this.state.soil_health || !Array.isArray(this.state.soil_health) || this.state.soil_health.length === 0) {
            this.state.soil_health = Array.from({ length: 5 }, () => Array(6).fill(100));
        }
        if (!this.state.fallow_days || !Array.isArray(this.state.fallow_days) || this.state.fallow_days.length === 0) {
            this.state.fallow_days = Array.from({ length: 5 }, () => Array(6).fill(0));
        }

        // Ensure object fields exist
        if (!this.state.market_prices) this.state.market_prices = null;
        if (!this.state.achievements) this.state.achievements = { farm_harvest: false, farm_rancher: false, farm_winner: false };
        if (!this.state.weather_visual) this.state.weather_visual = "clear";
        if (!this.state.damaged_buildings) this.state.damaged_buildings = [];
        if (!this.state.owned_buildings) this.state.owned_buildings = {};
        if (!this.state.unlocked_crops) this.state.unlocked_crops = ["Wheat", "Carrot", "Corn"];
        if (!this.state.active_contract) this.state.active_contract = null;
        if (this.state.contract_progress === undefined) this.state.contract_progress = 0;
        if (!this.state.weather_forecast) this.state.weather_forecast = null;
        if (!this.state.harvest_families) this.state.harvest_families = {};
        if (this.state.total_earned === undefined) this.state.total_earned = 0;

        fetch('/api/games/farm-tycoon').then(r => r.json()).then(cfg => {
            FT_CONFIG = cfg;
            if (!this.state.market_prices) this.state.market_prices = { ...cfg.base_prices };
            for (const [k, v] of Object.entries(cfg.base_prices)) {
                if (!(k in this.state.market_prices)) this.state.market_prices[k] = v;
            }
            if (!this.state.market_prices.Tomato) this.state.market_prices.Tomato = 12;
            if (!this.state.market_prices.Strawberry) this.state.market_prices.Strawberry = 18;

            this.checkUnlocks();
            this.generateForecast();
            this.save();
            this.render();
        });
    },

    save() {
        saveState('ft_state', this.state);
    },

    // ── 3c. Grid creation ──

    createGrid() {
        const grid = Array.from({ length: 5 }, () => Array(6).fill(0));

        // River — enters from a random column, bends 1-2 times
        let riverCol = Math.floor(Math.random() * 3) + 1;
        for (let r = 0; r < 5; r++) {
            grid[r][riverCol] = 1;
            if (r < 4 && Math.random() < 0.45) {
                const bend = Math.random() < 0.5 ? 1 : -1;
                const newCol = riverCol + bend;
                if (newCol >= 1 && newCol <= 4) {
                    riverCol = newCol;
                }
            }
        }

        // Rocks (2-3)
        let rocksPlaced = 0;
        const maxRocks = 2 + Math.floor(Math.random() * 2);
        let attempts = 0;
        while (rocksPlaced < maxRocks && attempts < 30) {
            const r = Math.floor(Math.random() * 5);
            const c = Math.floor(Math.random() * 6);
            if (grid[r][c] === 0) {
                grid[r][c] = 5;
                rocksPlaced++;
            }
            attempts++;
        }

        return grid;
    },

    // ── 3d. Season / time helpers ──

    getSeason(day) {
        const d = day % 120;
        if (d < 30) return "Spring";
        if (d < 60) return "Summer";
        if (d < 90) return "Autumn";
        return "Winter";
    },

    getYear(day) {
        return Math.floor(day / 120) + 1;
    },

    // ── 3e. Unlock & forecast logic ──

    checkUnlocks() {
        if (!FT_CONFIG || !FT_CONFIG.crop_unlocks) return;
        const year = this.getYear(this.state.day);
        const totalHarvests = this.state.total_harvests;

        for (const [crop, req] of Object.entries(FT_CONFIG.crop_unlocks)) {
            if (this.state.unlocked_crops.includes(crop)) continue;
            let unlocked = false;
            if (req.require === 'always') unlocked = true;
            else if (req.require === 'harvest_5' && totalHarvests >= 5) unlocked = true;
            else if (req.require === 'building_Barn' && (this.state.owned_buildings['Barn'] || 0) > 0) unlocked = true;
            else if (req.require === 'building_Beehive' && (this.state.owned_buildings['Beehive'] || 0) > 0) unlocked = true;
            else if (req.require === 'building_Scarecrow' && (this.state.owned_buildings['Scarecrow'] || 0) > 0) unlocked = true;
            else if (req.require === 'year_2' && year >= 2) unlocked = true;

            if (unlocked) {
                this.state.unlocked_crops.push(crop);
                showToast(`🔓 ${crop} unlocked!`);
            }
        }
    },

    generateForecast() {
        const season = this.getSeason(this.state.day);
        const forecasts = {
            "Spring": ["Sunny", "Rainy", "Cloudy", "Late Frost"],
            "Summer": ["Hot & Dry", "Sunny", "Thunderstorm", "Sunny"],
            "Autumn": ["Cloudy", "Rainy", "Windy", "Sunny"],
            "Winter": ["Snow", "Cold & Clear", "Sleet", "Overcast"],
        };
        const options = forecasts[season] || ["Sunny"];
        this.state.weather_forecast = options[Math.floor(Math.random() * options.length)];
    },

    getCropSeason(crop) {
        if (!FT_CONFIG || !FT_CONFIG.crop_seasons) return true;
        const season = this.getSeason(this.state.day);
        const allowed = FT_CONFIG.crop_seasons[crop];
        if (!allowed) return true;
        return allowed.includes(season);
    },

    getCropDays(crop) {
        if (!FT_CONFIG || !FT_CONFIG.crop_days) return 3;
        return FT_CONFIG.crop_days[crop] || 3;
    },

    // ── 3f. Render methods ──

    updateFarmScene() {
        const season = this.getSeason(this.state.day).toLowerCase();
        const scene = document.getElementById('ft-farm-scene');
        if (scene) scene.className = 'farm-scene season-' + season;
        renderWeatherParticles('ft-weather-particles', season, { isRain: this.state.weather_visual === 'rain' });
        updateDayOverlay('ft-day-overlay', this.state.day);
    },

    render() {
        if (this.state.manor_bought) {
            this.renderWin();
        }

        this.renderStats();
        this.renderForecast();
        this.renderWarning();
        this.renderInventory();
        this.renderFeedStatus();
        this.renderToolPanel();
        this.renderFarmScene();
        this.renderGrid();
        this.renderLegend();
        this.renderFeedProduction();
        this.renderMarket();
        this.renderContracts();
        this.renderAchievements();
        this.renderLedger();
        this.updateFarmScene();
    },

    renderStats() {
        const s = this.state;
        const year = this.getYear(s.day);
        const season = this.getSeason(s.day);
        const chickens = s.grid.flat().filter(t => t === 12).length;
        const cows = s.grid.flat().filter(t => t === 13).length;
        const goats = s.grid.flat().filter(t => t === 14).length;
        const seasonIcon = { Spring: "🌸", Summer: "☀️", Autumn: "🍂", Winter: "❄️" }[season] || "🌸";

        document.getElementById('ft-stats').innerHTML = `
            <div class="stat-box year"><div class="stat-label">📅 YEAR</div><div class="stat-value">${year} — ${seasonIcon} ${season}</div></div>
            <div class="stat-box money"><div class="stat-label">💰 MONEY</div><div class="stat-value">£${s.money}</div></div>
            <div class="stat-box"><div class="stat-label">🌾 HARVESTS</div><div class="stat-value">${s.total_harvests}</div></div>
            <div class="stat-box animals"><div class="stat-label">🐔 ANIMALS</div><div class="stat-value">${year >= 2 ? `${chickens}🐔 ${cows}🐄 ${goats}🐐` : '🔒 Year 2'}</div></div>
        `;
    },

    renderForecast() {
        const el = document.getElementById('ft-event');
        let html = '';

        if (this.state.weather_forecast) {
            const fcIcons = {
                "Sunny": "☀️", "Rainy": "🌧️", "Cloudy": "⛅", "Hot & Dry": "🔥",
                "Thunderstorm": "⛈️", "Windy": "💨", "Late Frost": "🥶",
                "Snow": "❄️", "Cold & Clear": "🌤️", "Sleet": "🌨️", "Overcast": "☁️"
            };
            const icon = fcIcons[this.state.weather_forecast] || "🌤️";
            html += `<div class="forecast-box"><span class="forecast-label">🔭 Tomorrow's Weather:</span> <span class="forecast-value">${icon} ${this.state.weather_forecast}</span></div>`;
        }
        if (this.state.last_event) {
            html += `<div class="event-box"><span style="color: var(--amber-dark); font-weight: 600;">📋 Report:</span> <span style="color: var(--cream);"> ${this.state.last_event}</span></div>`;
        }
        if (this.state.market_event) {
            html += `<div class="surge-box"><span style="color: var(--amber); font-weight: 600;">📈 Market Surge:</span> <span style="color: var(--cream);"> ${this.state.market_event} prices doubled!</span></div>`;
        }

        el.innerHTML = html;
    },

    renderWarning() {
        const el = document.getElementById('ft-warning');
        const season = this.getSeason(this.state.day);
        const hasColdFrame = this.state.grid.flat().includes(15);

        if (season === 'Autumn') {
            el.innerHTML = `<div class="warning-box autumn"><span style="color: var(--amber); font-weight: 600;">🍂 AUTUMN WARNING:</span> <span style="color: var(--cream-dim);">Winter approaches! Stockpile feed and build a Cold Frame!</span></div>`;
        } else if (season === 'Winter' && hasColdFrame) {
            el.innerHTML = `<div class="warning-box winter-safe"><span style="color: #2196F3; font-weight: 600;">❄️ WINTER:</span> <span style="color: var(--cream-dim);">Crops protected by Greenhouse! 🌿</span></div>`;
        } else if (season === 'Winter') {
            el.innerHTML = `<div class="warning-box winter-danger"><span style="color: var(--danger); font-weight: 600;">❄️ WINTER:</span> <span style="color: var(--cream-dim);">Crops will die! Build a Greenhouse.</span></div>`;
        } else {
            el.innerHTML = '';
        }
    },

    renderInventory() {
        const el = document.getElementById('ft-inventory');
        const items = Object.entries(this.state.inventory).filter(([_, v]) => v > 0);

        if (items.length > 0) {
            const str = items.map(([k, v]) => `<strong>${k}:</strong> ${v}`).join(' | ');
            el.innerHTML = `<div class="inventory-bar">🎒 ${str}</div>`;
        } else {
            el.innerHTML = `<div class="inventory-bar" style="text-align: center;">🎒 Empty — start farming!</div>`;
        }
    },

    renderFeedStatus() {
        const el = document.getElementById('ft-feed-status');
        const chickens = this.state.grid.flat().filter(t => t === 12).length;
        const cows = this.state.grid.flat().filter(t => t === 13).length;
        const goats = this.state.grid.flat().filter(t => t === 14).length;
        const totalAnimals = chickens + cows + goats;

        if (totalAnimals > 0 && this.getYear(this.state.day) >= 2) {
            const feedNeeded = chickens + cows * 2 + goats;
            const feedHave = this.state.inventory.Feed || 0;
            const colour = feedHave >= feedNeeded ? '🟢' : '🔴';
            el.innerHTML = `<div class="feed-status">${colour} Feed Needed: ${feedNeeded}/day | Stock: ${feedHave}</div>`;
        } else {
            el.innerHTML = '';
        }
    },

    renderToolPanel() {
        const el = document.getElementById('ft-tool-panel');
        if (!FT_CONFIG) { el.innerHTML = ''; return; }

        const year = this.getYear(this.state.day);
        const allCrops = Object.entries(FT_CONFIG.seed_cost);
        const buildings = Object.entries(FT_CONFIG.buildings);
        const availableBuildings = buildings.filter(([name, data]) =>
            ["Manor", "Barn", "Beehive", "Scarecrow", "Sprinkler", "Cold Frame"].includes(name) ||
            (year >= 2 && ["Chicken Coop", "Cow Pasture", "Goat Pen"].includes(name))
        );

        // Crops dropdown with unlock info
        let html = `<div class="tool-group"><label>🌱 Plant</label><select id="ft-tool-crop" onchange="farmTycoon.state.tool = this.value; farmTycoon.render();">`;
        for (const [name, cost] of allCrops) {
            const unlocked = this.state.unlocked_crops.includes(name);
            const inSeason = this.getCropSeason(name);
            const sel = this.state.tool === name ? ' selected' : '';

            if (unlocked && inSeason) {
                html += `<option value="${name}"${sel}>${name} (£${cost})</option>`;
            } else if (unlocked && !inSeason) {
                html += `<option value="${name}"${sel} disabled>🔒 ${name} (out of season)</option>`;
            } else {
                const unlockInfo = FT_CONFIG.crop_unlocks && FT_CONFIG.crop_unlocks[name];
                const desc = unlockInfo ? unlockInfo.desc : 'Locked';
                html += `<option value="${name}" disabled>🔒 ${name} — ${desc}</option>`;
            }
        }
        html += `</select></div>`;

        html += `<div class="tool-group"><label>🏗️ Build</label><select id="ft-tool-build" onchange="farmTycoon.state.build_sel = this.value; farmTycoon.updatePlacingMode();">`;
        html += `<option value="None">None</option>`;
        for (const [name, data] of availableBuildings) {
            const displayName = name === 'Cold Frame' ? 'Greenhouse' : name;
            html += `<option value="${name}">${data.icon || '🏗️'} ${displayName} (£${data.cost})</option>`;
        }
        html += `</select></div>`;

        html += `<div class="tool-group"><label>&nbsp;</label><button class="btn-danger" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;" onclick="farmTycoon.clearAllWeeds()">🧹 Clear Weeds</button></div>`;

        el.innerHTML = html;
    },

    updatePlacingMode() {
        const sel = this.state.build_sel;
        this.state.placing_mode = (sel && sel !== "None") ? sel : null;
        this.save();
        this.render();
    },

    cancelPlacement() {
        this.state.placing_mode = null;
        this.state.build_sel = "None";
        this.save();
        this.render();
    },

    renderGrid() {
        const container = document.getElementById('ft-grid');
        const placingBanner = document.getElementById('ft-placing-banner');

        if (this.state.placing_mode) {
            const bData = FT_CONFIG.buildings[this.state.placing_mode];
            placingBanner.classList.remove('hidden');
            placingBanner.innerHTML = `
                <span style="color: var(--amber); font-weight: 700;">📍 Placing Mode:</span>
                <span style="color: var(--cream-dim);"> Click a <span style="color: var(--green-leaf);">🌱 Empty</span> tile to build <b>${bData.icon} ${this.state.placing_mode}</b>.</span>
                <button class="btn-danger" style="margin-left: 1rem; padding: 0.3rem 0.8rem; font-size: 0.85rem;" onclick="farmTycoon.cancelPlacement()">❌ Cancel</button>
            `;
        } else {
            placingBanner.classList.add('hidden');
        }

        const styles = FT_CONFIG ? FT_CONFIG.tile_styles : {};
        let html = '';

        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 6; c++) {
                const tile = this.state.grid[r][c];
                const isDamaged = this.state.damaged_buildings.some(d => d[0] === r && d[1] === c);
                const soil = this.state.soil_health[r][c];
                const cropName = this.state.crop_map[`${r},${c}`] || "";

                let style = styles[String(tile)] || { icon: "❓", label: String(tile), bg: "#1a1a1a", border: "#555", text: "#aaa" };
                if (typeof style.icon === 'undefined') style.icon = "❓";

                let displayLabel = style.label;
                if ((tile === 2 || tile === 3 || tile === 4) && cropName) displayLabel = cropName;
                if (tile === 15) displayLabel = "Greenhouse";

                let tileClass = 'farm-tile';
                if (tile === 0) tileClass += ' empty';
                if (tile === 5) tileClass += ' tile-rock';
                if (isDamaged) tileClass += ' damaged';
                if ([8, 9, 10, 11, 15, 16].includes(tile)) tileClass += ' tile-building';
                if ([12, 13, 14].includes(tile)) tileClass += ' tile-animal';
                if (tile === 12) tileClass += ' tile-chicken';
                if (tile === 13) tileClass += ' tile-cow';
                if (tile === 14) tileClass += ' tile-goat';
                if (tile === 1) tileClass += ' tile-stream';
                if (tile === 7) tileClass += ' tile-weed';
                if (tile === 9) tileClass += ' tile-beehive';
                if (tile === 10) tileClass += ' tile-scarecrow';
                if (tile === 11) tileClass += ' tile-sprinkler';
                if (tile === 16) tileClass += ' tile-manor';
                if (tile === 2) tileClass += ' crop-seed';
                if (tile === 3) tileClass += ' crop-growing';
                if (tile === 4) tileClass += ' crop-ready';

                // Scarecrow adjacency bonus indicator
                let adjBonus = '';
                if (tile === 4) {
                    for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1]]) {
                        const nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < 5 && nc >= 0 && nc < 6 && this.state.grid[nr][nc] === 10) {
                            adjBonus = '<div class="tile-bonus">🦅+1</div>';
                            break;
                        }
                    }
                }

                // River adjacency
                if (tile === 0 || tile === 2 || tile === 3 || tile === 4) {
                    for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1]]) {
                        const nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < 5 && nc >= 0 && nc < 6 && this.state.grid[nr][nc] === 1) {
                            tileClass += ' river-adjacent';
                            break;
                        }
                    }
                }

                let actionHtml = '';
                if (isDamaged) {
                    actionHtml = `<button class="tile-action-btn" onclick="farmTycoon.repairBuilding(${r},${c})">🔧 Repair £50</button>`;
                } else if (tile === 5) {
                    actionHtml = `<button class="tile-action-btn danger" onclick="farmTycoon.clearRock(${r},${c})">⛏️ £${FT_CONFIG.rock_clear_cost || 50}</button>`;
                } else if (tile === 7) {
                    actionHtml = `<button class="tile-action-btn danger" onclick="farmTycoon.clearWeed(${r},${c})">🧹 Clear</button>`;
                } else if (tile === 0) {
                    if (this.state.placing_mode && this.state.placing_mode !== "None") {
                        const bName = this.state.placing_mode;
                        const bData = FT_CONFIG.buildings[bName];
                        const year = this.getYear(this.state.day);
                        const locked = ["Chicken Coop", "Cow Pasture", "Goat Pen"].includes(bName) && year < 2;
                        if (locked) {
                            actionHtml = `<span style="color: var(--cream-dim); font-size: 0.7rem;">🔒 Year 2</span>`;
                        } else {
                            actionHtml = `<button class="tile-action-btn" onclick="farmTycoon.buildTile(${r},${c})">🏗️ £${bData.cost}</button>`;
                        }
                    } else {
                        const crop = this.state.tool;
                        const cost = FT_CONFIG.seed_cost[crop] || 6;
                        const unlocked = this.state.unlocked_crops.includes(crop);
                        const inSeason = this.getCropSeason(crop);
                        if (!unlocked) {
                            actionHtml = `<span style="color: var(--cream-dim); font-size: 0.7rem;">🔒 Locked</span>`;
                        } else if (!inSeason) {
                            actionHtml = `<span style="color: var(--amber-dark); font-size: 0.7rem;">❌ Out of season</span>`;
                        } else {
                            actionHtml = `<button class="tile-action-btn" onclick="farmTycoon.plantCrop(${r},${c})">🌱 £${cost}</button>`;
                        }
                    }
                } else if (tile === 4) {
                    actionHtml = `<button class="tile-action-btn harvest" onclick="farmTycoon.harvestCrop(${r},${c})">🌾 Harvest</button>`;
                } else if (tile === 1) {
                    const disabled = this.getSeason(this.state.day) === "Winter" ? ' disabled' : '';
                    actionHtml = `<button class="tile-action-btn fish"${disabled} onclick="farmTycoon.fishTile(${r},${c})">🎣 Fish</button>`;
                }

                let soilHtml = '';
                if (tile === 2 || tile === 3 || tile === 4) {
                    const soilColor = soil >= 70 ? '🟢' : (soil >= 40 ? '🟡' : '🔴');
                    soilHtml = `<div class="tile-soil">${soilColor} Soil ${soil}%</div>`;
                }

                const damageHtml = isDamaged ? '<div class="tile-damaged">DAMAGED</div>' : '';

                html += `<div class="${tileClass}" data-r="${r}" data-c="${c}" style="background: ${isDamaged ? 'linear-gradient(135deg, #2a0a0a, #1a0000)' : style.bg}; border: ${isDamaged ? '2px dashed var(--danger)' : `2px solid ${style.border}`}">
                    <div class="tile-icon">${style.icon}</div>
                    <div class="tile-label" style="color: ${style.text};">${displayLabel}</div>
                    ${damageHtml}${soilHtml}${adjBonus}
                    <div class="tile-action">${actionHtml}</div>
                </div>`;
            }
        }
        container.innerHTML = html;
    },

    renderLegend() {
        const el = document.getElementById('ft-legend');
        const items = [
            { icon: "🌱", label: "Empty", bg: "#1a2e1a", border: "#3d5a3d" },
            { icon: "🌊", label: "Stream", bg: "#0a1a2e", border: "#2196F3" },
            { icon: "🪨", label: "Rock", bg: "#2a2a2a", border: "#757575" },
            { icon: "🌱🌿", label: "Growing", bg: "#1a2e1a", border: "#4CAF50" },
            { icon: "🌾", label: "Ready", bg: "#2a2a00", border: "#FFC107" },
            { icon: "🧹", label: "Weed", bg: "#2a1a0a", border: "#8D6E63" },
            { icon: "🫧", label: "Cold Frame", bg: "#0a2a2a", border: "#26C6DA" },
            { icon: "💧", label: "+River Bonus", bg: "#0a2a1a", border: "#26A69A" },
        ];
        el.innerHTML = items.map(i => `<span class="legend-item" style="background: ${i.bg}; border: 1px solid ${i.border};">${i.icon} ${i.label}</span>`).join('');
    },

    renderFeedProduction() {
        const el = document.getElementById('ft-feed-production');
        const inv = this.state.inventory;
        const hasIng = (inv.Wheat || 0) >= 1 && (inv.Carrot || 0) >= 1 && (inv.Corn || 0) >= 1;

        el.innerHTML = `<div class="feed-production">
            <h4>🏭 Feed Production</h4>
            <div class="feed-row">
                <span class="feed-recipe">Recipe: 1 Wheat + 1 Carrot + 1 Corn = 5 Feed</span>
                <button class="btn-primary" style="padding: 0.4rem 1rem; font-size: 0.85rem;" onclick="farmTycoon.makeFeed()" ${hasIng ? '' : 'disabled'}>Make Feed Bag</button>
            </div>
        </div>`;
    },

    renderMarket() {
        const el = document.getElementById('ft-market');
        const prices = this.state.market_prices;
        const inv = this.state.inventory;
        const season = this.getSeason(this.state.day);

        let html = '';
        for (const [item, price] of Object.entries(prices)) {
            let sellPrice = price;
            let surgeHtml = '';
            let crashHtml = '';
            let seasonHtml = '';

            if (this.state.market_event === item) {
                sellPrice = price * 2;
                surgeHtml = '<div class="mi-surge">📈 Surge!</div>';
            }
            if ((this.state.sales_log[item] || 0) > 10) {
                sellPrice = Math.max(1, Math.floor(price * 0.8));
                crashHtml = '<div class="mi-crash">📉 Crashed</div>';
            }
            if (FT_CONFIG && FT_CONFIG.seasonal_prices && FT_CONFIG.seasonal_prices[item]) {
                const mult = FT_CONFIG.seasonal_prices[item][season] || 1;
                if (mult !== 1) {
                    const adj = mult > 1 ? `+${Math.round((mult - 1) * 100)}%` : `${Math.round((mult - 1) * 100)}%`;
                    seasonHtml = `<div class="mi-season ${mult > 1 ? 'season-high' : 'season-low'}">${mult > 1 ? '📈' : '📉'} Season: ${adj}</div>`;
                    sellPrice = Math.round(sellPrice * mult);
                }
            }

            const count = inv[item] || 0;
            const disabled = count <= 0 ? ' disabled' : '';
            html += `<div class="market-item">
                <div class="mi-name">${item}</div>
                <div class="mi-price">£${sellPrice}</div>
                <div class="mi-qty">Have: ${count}</div>
                ${surgeHtml}${crashHtml}${seasonHtml}
                <button class="sell-btn" onclick="farmTycoon.sellItem('${item}')"${disabled}>Sell £${sellPrice}</button>
            </div>`;
        }
        el.innerHTML = html;
    },

    renderContracts() {
        const el = document.getElementById('ft-contracts');
        if (!el) return;

        const contract = this.state.active_contract;
        if (!contract) {
            el.innerHTML = `<div class="contract-card empty">
                <div style="text-align: center; color: var(--cream-dim); padding: 1rem;">
                    <div style="font-size: 1.5rem;">📜</div>
                    <div>No active contract</div>
                    <button class="btn-primary" style="margin-top: 0.5rem;" onclick="farmTycoon.takeContract()">📋 Take Contract</button>
                </div>
            </div>`;
            return;
        }

        const progress = Math.min(this.state.contract_progress, contract.qty);
        const pct = Math.floor(progress / contract.qty * 100);
        el.innerHTML = `<div class="contract-card">
            <div class="contract-header">📜 ${contract.name}</div>
            <div class="contract-desc">${contract.desc}</div>
            <div class="contract-progress">
                <div class="contract-bar"><div class="contract-fill" style="width: ${pct}%"></div></div>
                <span>${progress}/${contract.qty} ${contract.item}</span>
            </div>
            <div class="contract-reward">Reward: £${contract.reward}</div>
            <button class="btn-primary" style="margin-top: 0.3rem; font-size: 0.8rem;" onclick="farmTycoon.fulfillContract()" ${progress >= contract.qty ? '' : 'disabled'}>${progress >= contract.qty ? '✅ Fulfill Contract' : `Need ${contract.qty - progress} more`}</button>
        </div>`;
    },

    renderAchievements() {
        const el = document.getElementById('ft-achievements');
        const chickens = this.state.grid.flat().filter(t => t === 12).length;
        const cows = this.state.grid.flat().filter(t => t === 13).length;
        const goats = this.state.grid.flat().filter(t => t === 14).length;
        const totalAnimals = chickens + cows + goats;

        const achDefs = [
            { key: 'farm_harvest', name: '🌱 Green Thumb', desc: 'Harvest your first crop', progress: () => this.state.achievements.farm_harvest ? '(Done)' : `(${this.state.total_harvests}/1)` },
            { key: 'farm_rancher', name: '🐮 Rancher', desc: 'Own 5 animals', progress: () => this.state.achievements.farm_rancher ? '(Done)' : `(${totalAnimals}/5)` },
            { key: 'farm_winner', name: '🏆 Landowner', desc: 'Build the Manor', progress: () => this.state.achievements.farm_winner ? '(Done)' : '(Build it!)' },
            { key: 'farm_fisher', name: '🐟 Angler', desc: 'Catch 10 fish', progress: () => this.state.achievements.farm_fisher ? '(Done)' : `(${this.state.inventory.Fish || 0}/10)` },
            { key: 'farm_rockbreaker', name: '⛏️ Rockbreaker', desc: 'Clear 5 rocks', progress: () => this.state.achievements.farm_rockbreaker ? '(Done)' : `(${this.state.rocks_cleared || 0}/5)` },
            { key: 'farm_greenhouse', name: '🌿 Green Thumb Pro', desc: 'Build a Greenhouse', progress: () => this.state.achievements.farm_greenhouse ? '(Done)' : '(Build one!)' },
            { key: 'farm_rich', name: '💰 Prosperous', desc: 'Earn £1000 total', progress: () => this.state.achievements.farm_rich ? '(Done)' : `(£${this.state.total_earned}/£1000)` },
            { key: 'farm_mogul', name: '🏦 Mogul', desc: 'Earn £5000 total', progress: () => this.state.achievements.farm_mogul ? '(Done)' : `(£${this.state.total_earned}/£5000)` },
            { key: 'farm_diverse', name: '🌍 Diverse Farmer', desc: 'Sell 5 different crop types', progress: () => this.state.achievements.farm_diverse ? '(Done)' : `(${Object.keys(this.state.inventory).filter(k => this.state.inventory[k] > 0).length}/5)` },
            { key: 'farm_beekeeper', name: '🍯 Beekeeper', desc: 'Own 3 beehives', progress: () => this.state.achievements.farm_beekeeper ? '(Done)' : `(${this.state.grid.flat().filter(t => t === 9).length}/3)` },
            { key: 'farm_scarer', name: '🦅 Bird Scarer', desc: 'Build 3 scarecrows', progress: () => this.state.achievements.farm_scarer ? '(Done)' : `(${this.state.owned_buildings.Scarecrow || 0}/3)` },
            { key: 'farm_sprinkler', name: '💧 Irrigator', desc: 'Build a sprinkler', progress: () => this.state.achievements.farm_sprinkler ? '(Done)' : '(Build one!)' },
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

    renderLedger() {
        const el = document.getElementById('ft-ledger');
        if (!el) return;
        const s = this.state;
        const totalCrops = s.grid.flat().filter(t => [2, 3, 4].includes(t)).length;
        const emptyPlots = s.grid.flat().filter(t => t === 0).length;
        const buildings = s.grid.flat().filter(t => [8, 9, 10, 11, 15].includes(t)).length;
        const animals = s.grid.flat().filter(t => [12, 13, 14].includes(t)).length;

        const rows = [
            { label: '📅 Days Played', value: s.day, cls: '' },
            { label: '💰 Total Earned', value: `£${s.total_earned}`, cls: 'positive' },
            { label: '🌾 Total Harvests', value: s.total_harvests, cls: '' },
            { label: '🌱 Crops Growing', value: totalCrops, cls: '' },
            { label: '🟫 Empty Plots', value: emptyPlots, cls: '' },
            { label: '🏗️ Buildings', value: buildings, cls: '' },
            { label: '🐔 Animals', value: animals, cls: '' },
            { label: '🔓 Crops Unlocked', value: `${s.unlocked_crops.length} / ${Object.keys(FT_CONFIG.seed_cost || {}).length}`, cls: '' },
        ];

        el.innerHTML = `<div class="farm-ledger">
            <h4>📊 Farm Statistics</h4>
            ${rows.map(r => `<div class="ledger-row"><span class="ledger-label">${r.label}</span><span class="ledger-value ${r.cls}">${r.value}</span></div>`).join('')}
        </div>`;
    },

    renderFarmScene() {
        const container = document.getElementById('ft-village-view');
        if (!container) return;

        const grid = this.state.grid;
        const season = this.getSeason(this.state.day).toLowerCase();
        const pal = FarmPalettes[season];
        const isDamaged = (r, c) => this.state.damaged_buildings.some(d => d[0] === r && d[1] === c);

        let streamCol = -1;
        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 6; c++) {
                if (grid[r][c] === 1) { streamCol = c; break; }
            }
            if (streamCol >= 0) break;
        }

        const colX = [6, 22, 42, 62, 78, 92];
        const rowY = [34, 48, 60, 74, 90];

        // Sky
        const sunIcons = { spring:'🌤️', summer:'☀️', autumn:'🍂', winter:'❄️' };
        const sunIcon = sunIcons[season] || '🌤️';
        const cloudsHtml = [0,1,2].map(i =>
            `<div class="vf-cloud" style="top:${6 + i * 9}%; left:${8 + i * 30}%; animation-duration:${20 + i * 12}s; animation-delay:${i * 5}s; font-size:${1.3 + i * 0.4}rem;">☁️</div>`
        ).join('');

        // Hills
        const hillsSvg = `<svg class="vf-hills-svg" viewBox="0 0 1000 300" preserveAspectRatio="none">
            <path d="M0,180 Q120,60 280,140 Q450,20 620,120 Q800,30 1000,100 L1000,300 L0,300 Z" fill="${pal.hill1}" opacity="0.5"/>
            <path d="M0,220 Q180,100 380,180 Q580,80 780,160 Q900,120 1000,180 L1000,300 L0,300 Z" fill="${pal.hill2}" opacity="0.7"/>
        </svg>`;

        // River
        let riverHtml = '';
        if (streamCol >= 0) {
            const rx = colX[streamCol];
            const bend = (streamCol % 2 === 0) ? 5 : -5;
            const riverPath = `M${rx},30 C${rx + bend},45 ${rx - bend},65 ${rx},82 C${rx + bend},90 ${rx - bend},96 ${rx},100`;
            riverHtml = `<svg class="vf-river-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
                <path d="${riverPath}" fill="none" stroke="${pal.river}" stroke-width="8" opacity="0.4" stroke-linecap="round"/>
                <path d="${riverPath}" fill="none" stroke="${pal.riverLt}" stroke-width="4" opacity="0.25" stroke-linecap="round"/>
                <path d="${riverPath}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" stroke-linecap="round">
                    <animate attributeName="stroke-dasharray" values="0,20;10,10;0,20" dur="3s" repeatCount="indefinite"/>
                </path>
            </svg>`;
        }

        // Fence along river
        let fenceHtml = '';
        if (streamCol >= 0) {
            const rx = colX[streamCol];
            const fLeft = rx - 5;
            const fRight = rx + 5;
            const postPositions = [0, 18, 36, 54, 72, 90];

            const fenceSide = (leftPos) => {
                let html = `<div class="vf-fence" style="left:${leftPos}%; top:32%; height:62%;">`;
                html += `<div class="vf-fence-rail" style="top:5%;"></div>`;
                html += `<div class="vf-fence-rail" style="top:50%;"></div>`;
                html += `<div class="vf-fence-rail" style="top:95%;"></div>`;
                for (const p of postPositions) {
                    html += `<div class="vf-fence-post" style="top:${p}%;"></div>`;
                }
                html += `</div>`;
                return html;
            };

            fenceHtml = fenceSide(fLeft) + fenceSide(fRight);
        }

        // Build field patches and buildings
        let patchesHtml = '';
        let buildingsHtml = '';
        let smokePositions = [];
        let animalPositions = [];
        let beehivePositions = [];

        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 6; c++) {
                if (c === streamCol) continue;

                const tile = grid[r][c];
                const x = colX[c];
                const y = rowY[r];
                const damaged = isDamaged(r, c);
                const cropName = this.state.crop_map[`${r},${c}`] || '';
                const soilHealth = this.state.soil_health[r][c];

                let hoverInfo = '';

                if (tile === 0) {
                    hoverInfo = 'Empty plot — switch to 🚜 Farm tab to plant';
                    patchesHtml += `<div class="vf-patch vf-patch-empty" style="left:${x}%; top:${y}%;" data-info="${hoverInfo}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()"></div>`;
                } else if (tile === 2) {
                    hoverInfo = `${cropName || 'Crop'} — Seed | Soil: ${soilHealth}%`;
                    patchesHtml += `<div class="vf-patch vf-patch-seed" style="left:${x}%; top:${y}%;" data-info="${hoverInfo}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()"><div class="vf-seed-dot"></div></div>`;
                } else if (tile === 3) {
                    hoverInfo = `${cropName || 'Crop'} — Growing | Soil: ${soilHealth}%`;
                    patchesHtml += `<div class="vf-patch vf-patch-growing" style="left:${x}%; top:${y}%;" data-info="${hoverInfo}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()"><div class="vf-sprout"></div></div>`;
                } else if (tile === 4) {
                    hoverInfo = `${cropName || 'Crop'} — Ready to harvest! | Soil: ${soilHealth}%`;
                    patchesHtml += `<div class="vf-patch vf-patch-ready" style="left:${x}%; top:${y}%;" data-info="${hoverInfo}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()"><div class="vf-harvest-glow"></div></div>`;
                } else if (tile === 5) {
                    hoverInfo = `Rock — Clear for £${FT_CONFIG ? FT_CONFIG.rock_clear_cost : 50}`;
                    patchesHtml += `<div class="vf-patch vf-patch-rock" style="left:${x}%; top:${y}%;" data-info="${hoverInfo}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()"></div>`;
                } else if (tile === 7) {
                    hoverInfo = 'Weeds — Clear to plant';
                    patchesHtml += `<div class="vf-patch vf-patch-weed" style="left:${x}%; top:${y}%;" data-info="${hoverInfo}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()"></div>`;
                } else if (tile === 8) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Barn${damaged ? ' (damaged)' : ''}" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.barn(pal)}
                        <div class="vf-building-label${damaged ? ' damaged' : ''}">Barn${damaged ? ' ⚠️' : ''}</div>
                    </div>`;
                    if (!damaged) smokePositions.push({ x, y });
                } else if (tile === 9) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Beehive — Produces Honey" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.beehive(pal)}
                        <div class="vf-building-label">Beehive</div>
                    </div>`;
                    beehivePositions.push({ x, y });
                } else if (tile === 10) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Scarecrow — +1 yield to adjacent crops" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.scarecrow(pal)}
                        <div class="vf-building-label">Scarecrow</div>
                    </div>`;
                } else if (tile === 11) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Sprinkler — Protects from drought" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.sprinkler(pal)}
                    </div>`;
                } else if (tile === 12) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Chicken Coop" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.chicken(pal)}
                        <div class="vf-building-label">Chicken Coop</div>
                    </div>`;
                    animalPositions.push({ type: 'chicken', x, y });
                } else if (tile === 13) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Cow Pasture" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.cow(pal)}
                        <div class="vf-building-label">Cow Pasture</div>
                    </div>`;
                    animalPositions.push({ type: 'cow', x, y });
                } else if (tile === 14) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Goat Pen" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.goat(pal)}
                        <div class="vf-building-label">Goat Pen</div>
                    </div>`;
                    animalPositions.push({ type: 'goat', x, y });
                } else if (tile === 15) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Cold Frame — Protects crops in winter" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.coldFrame(pal)}
                        <div class="vf-building-label">Cold Frame</div>
                    </div>`;
                } else if (tile === 16) {
                    buildingsHtml += `<div class="vf-building" style="left:${x}%; top:${y}%;" data-info="Manor — You won!" onmouseenter="showSceneInfo(event, this)" onmouseleave="hideSceneInfo()">
                        ${FarmSVGs.manor(pal)}
                        <div class="vf-building-label" style="color:#FFD54F;">Manor 🏆</div>
                    </div>`;
                }
            }
        }

        // Smoke from barns
        const smokeHtml = smokePositions.map(pos =>
            `<div class="vf-smoke-container" style="left:${pos.x}%; top:${pos.y}%; transform:translate(-50%,-180%);">
                <div class="vf-smoke-puff" style="animation-delay:0s;"></div>
                <div class="vf-smoke-puff" style="animation-delay:1s;"></div>
                <div class="vf-smoke-puff" style="animation-delay:2s;"></div>
            </div>`
        ).join('');

        // Animals
        const animalHtml = animalPositions.map((a, i) => {
            const ox = 3 + (i % 3) * 2;
            const oy = 4 + (i % 2);
            if (a.type === 'chicken') return `<div class="vf-chicken" style="left:${a.x + ox}%; top:${a.y + oy}%;">🐔</div>`;
            if (a.type === 'cow') return `<div class="vf-cow" style="left:${a.x + 3}%; top:${a.y + 4}%;">🐄</div>`;
            if (a.type === 'goat') return `<div class="vf-goat" style="left:${a.x + 2}%; top:${a.y + 4}%;">🐐</div>`;
            return '';
        }).join('');

        // Flying bees near beehives
        let beesHtml = '';
        beehivePositions.forEach((pos, bi) => {
            for (let b = 0; b < 3; b++) {
                const bx = pos.x - 4 + b * 4;
                const by = pos.y - 10 - b * 2;
                beesHtml += `<div class="vf-bee" style="left:${bx}%; top:${by}%; animation-delay:${b * 0.8 + bi * 0.3}s;">🐝</div>`;
            }
        });

        // Weather
        let weatherHtml = '';
        const weather = this.state.weather_visual || 'clear';
        if (weather === 'rain') {
            for (let i = 0; i < 30; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 2;
                const duration = 0.4 + Math.random() * 0.4;
                const height = 10 + Math.random() * 10;
                weatherHtml += `<div class="vf-rain" style="left:${left}%; animation-delay:${delay}s; animation-duration:${duration}s; height:${height}px;"></div>`;
            }
        } else if (weather === 'snow') {
            for (let i = 0; i < 20; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 8;
                const duration = 6 + Math.random() * 6;
                const size = 4 + Math.random() * 4;
                weatherHtml += `<div class="vf-snow" style="left:${left}%; width:${size}px; height:${size}px; animation-delay:${delay}s; animation-duration:${duration}s;"></div>`;
            }
        } else if (weather === 'leaves') {
            const leaves = ['🍂', '🍁', '🍃'];
            for (let i = 0; i < 8; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 10;
                const duration = 8 + Math.random() * 8;
                weatherHtml += `<div class="vf-leaf" style="left:${left}%; animation-delay:${delay}s; animation-duration:${duration}s;">${leaves[i % 3]}</div>`;
            }
        } else if (weather === 'sun') {
            for (let i = 0; i < 3; i++) {
                const left = 10 + Math.random() * 80;
                const delay = Math.random() * 6;
                weatherHtml += `<div class="vf-sunray" style="left:${left}%; animation-delay:${delay}s;"></div>`;
            }
        }

        // Wildflowers in spring
        const flowersHtml = season === 'spring' ? '<div class="vf-wildflowers"></div>' : '';

        // Day/time tint
        const dayTime = getDayTimeClass(this.state.day);

        // Render
        container.innerHTML = `
            <div class="village-farm season-${season}">
                <div class="vf-sky" style="background: linear-gradient(180deg, ${pal.sky1}, ${pal.sky2});">
                    <div class="vf-sun">${sunIcon}</div>
                    ${cloudsHtml}
                </div>
                ${hillsSvg}
                <div class="vf-meadow"></div>
                ${riverHtml}
                ${fenceHtml}
                ${flowersHtml}
                <div style="position:absolute; inset:0; z-index:10;">
                    ${patchesHtml}
                    ${buildingsHtml}
                </div>
                ${smokeHtml}
                ${animalHtml}
                ${beesHtml}
                <div class="vf-foreground" style="background: linear-gradient(0deg, ${pal.meadowDk}, transparent);"></div>
                ${weatherHtml}
                <div class="vf-time-overlay ${dayTime}"></div>
                <div class="vf-info-panel" id="vf-info-panel"></div>
            </div>
        `;
    },

    renderWin() {
        const banner = document.getElementById('ft-win-banner');
        if (!banner) return;
        // Only show the banner once
        if (this.state.win_shown) {
            banner.classList.add('hidden');
            return;
        }
        this.state.win_shown = true;
        this.save();
        banner.classList.remove('hidden');
        banner.innerHTML = `<div class="win-banner">
            <div class="win-icon">🏆</div>
            <div class="win-title">FARMING DYNASTY COMPLETE!</div>
            <div class="win-text">You built the Manor! Money: £${this.state.money} | Days: ${this.state.day} | Harvests: ${this.state.total_harvests}</div>
            <div class="win-sub" style="color: var(--cream-dim); font-size: 0.9rem; margin-top: 0.5rem;">You can keep playing — your farm continues!</div>
        </div>`;
    },

    // ── 3g. Player actions ──

    plantCrop(r, c) {
        const crop = this.state.tool;
        if (!this.state.unlocked_crops.includes(crop)) { showToast('🔒 Crop not unlocked yet!'); return; }
        if (!this.getCropSeason(crop)) { showToast(`❌ ${crop} can't be planted in ${this.getSeason(this.state.day)}!`); return; }
        const cost = FT_CONFIG.seed_cost[crop] || 6;
        if (this.state.money < cost) { showToast(`Need £${cost}!`); return; }
        if (this.state.grid[r][c] !== 0) return;

        this.state.money -= cost;
        this.state.grid[r][c] = 2;
        this.state.crop_map[`${r},${c}`] = crop;
        this.state.fallow_days[r][c] = 0;
        this.save();
        this.render();
    },

    harvestCrop(r, c) {
        if (this.state.grid[r][c] !== 4) return;
        const crop = this.state.crop_map[`${r},${c}`] || "Wheat";
        let yieldCount = 1;

        // Scarecrow adjacency bonus
        for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1]]) {
            const nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < 5 && nc >= 0 && nc < 6 && this.state.grid[nr][nc] === 10) {
                yieldCount += 1;
            }
        }
        // River adjacency bonus
        for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1]]) {
            const nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < 5 && nc >= 0 && nc < 6 && this.state.grid[nr][nc] === 1) {
                yieldCount += 1;
            }
        }

        const harvested = Math.max(1, Math.floor(yieldCount * this.state.soil_health[r][c] / 100));
        this.state.inventory[crop] = (this.state.inventory[crop] || 0) + harvested;
        this.state.grid[r][c] = 0;
        this.state.soil_health[r][c] = Math.max(0, this.state.soil_health[r][c] - 10);
        delete this.state.crop_map[`${r},${c}`];
        this.state.fallow_days[r][c] = 0;
        this.state.total_harvests += 1;

        // Track harvest families for unlocks
        if (!this.state.harvest_families[crop]) this.state.harvest_families[crop] = 0;
        this.state.harvest_families[crop] += 1;

        // Diverse farmer
        const invTypes = Object.keys(this.state.inventory).filter(k => this.state.inventory[k] > 0);
        if (invTypes.length >= 5 && !this.state.achievements.farm_diverse) {
            this.state.achievements.farm_diverse = true;
            setAchievement('farm_diverse');
        }

        const tileEl = document.querySelector(`.farm-tile[data-r="${r}"][data-c="${c}"]`);
        showFloat(tileEl, `+${harvested} ${crop}`);

        this.checkUnlocks();
        this.save();
        this.render();
    },

    buildTile(r, c) {
        if (!this.state.placing_mode || this.state.grid[r][c] !== 0) return;
        const bName = this.state.placing_mode;
        const bData = FT_CONFIG.buildings[bName];
        if (!bData) return;
        const manorCost = 5000;
        const buildCost = bName === 'Manor' ? manorCost : bData.cost;
        if (this.state.money < buildCost) { showToast(`Need £${buildCost}!`); return; }

        this.state.money -= buildCost;
        this.state.grid[r][c] = bData.id;
        this.state.owned_buildings[bName] = (this.state.owned_buildings[bName] || 0) + 1;

        // Win condition: Manor built on the farm
        if (bName === 'Manor') {
            this.state.manor_bought = true;
            this.state.achievements.farm_winner = true;
            setAchievement('farm_winner');
            showToast('🏆 You built the Manor! Farming Dynasty Complete!');
        }

        // Building achievement checks
        if (bName === 'Cold Frame' && !this.state.achievements.farm_greenhouse) {
            this.state.achievements.farm_greenhouse = true;
            setAchievement('farm_greenhouse');
        }
        if (bName === 'Scarecrow') {
            const scarecrowCount = this.state.owned_buildings.Scarecrow || 0;
            if (scarecrowCount >= 3 && !this.state.achievements.farm_scarer) {
                this.state.achievements.farm_scarer = true;
                setAchievement('farm_scarer');
            }
        }
        if (bName === 'Sprinkler' && !this.state.achievements.farm_sprinkler) {
            this.state.achievements.farm_sprinkler = true;
            setAchievement('farm_sprinkler');
        }

        this.state.placing_mode = null;
        this.state.build_sel = "None";
        this.checkUnlocks();
        this.save();
        this.render();
    },

    clearWeed(r, c) {
        if (this.state.grid[r][c] !== 7) return;
        this.state.grid[r][c] = 0;
        this.state.fallow_days[r][c] = 0;
        this.save();
        this.render();
    },

    clearRock(r, c) {
        if (this.state.grid[r][c] !== 5) return;
        const cost = FT_CONFIG.rock_clear_cost || 50;
        if (this.state.money < cost) { showToast(`Need £${cost} to clear rock!`); return; }

        this.state.money -= cost;
        this.state.grid[r][c] = 0;
        this.state.fallow_days[r][c] = 0;
        if (!this.state.rocks_cleared) this.state.rocks_cleared = 0;
        this.state.rocks_cleared += 1;
        if (this.state.rocks_cleared >= 5 && !this.state.achievements.farm_rockbreaker) {
            this.state.achievements.farm_rockbreaker = true;
            setAchievement('farm_rockbreaker');
        }

        showToast(`⛏️ Rock cleared! -£${cost}`);
        this.save();
        this.render();
    },

    clearAllWeeds() {
        let removed = 0;
        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 6; c++) {
                if (this.state.grid[r][c] === 7) {
                    this.state.grid[r][c] = 0;
                    this.state.fallow_days[r][c] = 0;
                    removed++;
                }
            }
        }
        if (removed > 0) showToast(`Cleared ${removed} weeds!`);
        else showToast('No weeds to clear!');
        this.save();
        this.render();
    },

    repairBuilding(r, c) {
        if (!this.state.damaged_buildings.some(d => d[0] === r && d[1] === c)) {
            showToast('This building is not damaged!');
            return;
        }
        const cost = 50;
        if (this.state.money < cost) { showToast(`Need £${cost} to repair!`); return; }
        this.state.money -= cost;
        this.state.damaged_buildings = this.state.damaged_buildings.filter(d => !(d[0] === r && d[1] === c));
        showToast(`🔧 Building repaired! -£${cost}`);
        this.save();
        this.render();
    },

    fishTile(r, c) {
        if (this.state.grid[r][c] !== 1) return;
        if (this.getSeason(this.state.day) === "Winter") { showToast('Too cold to fish in winter!'); return; }
        if (this.state.fishing_today >= 3) { showToast('🎣 No more fishing today! Come back tomorrow.'); return; }
        this.state.fishing_today += 1;

        const tileEl = document.querySelector(`.farm-tile[data-r="${r}"][data-c="${c}"]`);

        // Determine catch
        const roll = Math.random();
        let cumChance = 0;
        let caught = "Fish";
        const fishing = FT_CONFIG.fishing || {};
        for (const [name, data] of Object.entries(fishing)) {
            cumChance += data.chance;
            if (roll < cumChance) {
                caught = name;
                break;
            }
        }

        const fishData = fishing[caught] || { sell: 15, icon: "🐟", desc: "A fish" };

        // Show fishing animation on the tile
        if (tileEl) {
            tileEl.style.position = 'relative';
            const rippleDiv = document.createElement('div');
            rippleDiv.className = 'fishing-ripple';
            rippleDiv.innerHTML = `
                <div class="ripple-ring"></div>
                <div class="ripple-ring"></div>
                <div class="ripple-ring"></div>
                <div class="catch-result">${fishData.icon}</div>
            `;
            tileEl.appendChild(rippleDiv);
            setTimeout(() => rippleDiv.remove(), 2000);
        }

        if (fishData.sell > 0) {
            this.state.inventory[caught] = (this.state.inventory[caught] || 0) + 1;
        }

        if ((this.state.inventory.Fish || 0) >= 10 && !this.state.achievements.farm_fisher) {
            this.state.achievements.farm_fisher = true;
            setAchievement('farm_fisher');
        }

        if (!(caught in this.state.market_prices) && fishData.sell > 0) {
            this.state.market_prices[caught] = fishData.sell;
        }

        setTimeout(() => {
            showToast(`🎣 ${fishData.icon} ${caught}! ${fishData.desc}`);
        }, 800);

        this.save();
        setTimeout(() => this.render(), 1500);
    },

    makeFeed() {
        const inv = this.state.inventory;
        if ((inv.Wheat || 0) < 1 || (inv.Carrot || 0) < 1 || (inv.Corn || 0) < 1) {
            showToast('Need 1 Wheat + 1 Carrot + 1 Corn!');
            return;
        }
        inv.Wheat -= 1;
        inv.Carrot -= 1;
        inv.Corn -= 1;
        if (inv.Wheat <= 0) delete inv.Wheat;
        if (inv.Carrot <= 0) delete inv.Carrot;
        if (inv.Corn <= 0) delete inv.Corn;
        inv.Feed = (inv.Feed || 0) + 5;
        showToast('+5 Feed Bags');
        this.save();
        this.render();
    },

    sellItem(item) {
        const count = this.state.inventory[item] || 0;
        if (count <= 0) return;

        let price = this.state.market_prices[item] || 5;
        const season = this.getSeason(this.state.day);

        // Seasonal price modifier
        if (FT_CONFIG && FT_CONFIG.seasonal_prices && FT_CONFIG.seasonal_prices[item]) {
            const mult = FT_CONFIG.seasonal_prices[item][season] || 1;
            price = Math.round(price * mult);
        }
        // Market surge
        if (this.state.market_event === item) price *= 2;
        // Market crash
        if ((this.state.sales_log[item] || 0) > 10) price = Math.max(1, Math.floor(price * 0.8));
        // Crop diversity bonus
        if (FT_CONFIG && FT_CONFIG.diversity_bonus) {
            const cropTypes = new Set(Object.keys(this.state.inventory).filter(k => this.state.inventory[k] > 0 && FT_CONFIG.seed_cost && FT_CONFIG.seed_cost[k]));
            if (cropTypes.size >= FT_CONFIG.diversity_bonus.min_crops) {
                price = Math.ceil(price * (1 + FT_CONFIG.diversity_bonus.bonus));
            }
        }

        this.state.money += price;
        this.state.total_earned += price;

        if (this.state.total_earned >= 1000 && !this.state.achievements.farm_rich) {
            this.state.achievements.farm_rich = true;
            setAchievement('farm_rich');
        }
        if (this.state.total_earned >= 5000 && !this.state.achievements.farm_mogul) {
            this.state.achievements.farm_mogul = true;
            setAchievement('farm_mogul');
        }

        this.state.inventory[item] -= 1;
        if (this.state.inventory[item] <= 0) delete this.state.inventory[item];
        this.state.sales_log[item] = (this.state.sales_log[item] || 0) + 1;

        // Contract progress
        if (this.state.active_contract && this.state.active_contract.item === item) {
            this.state.contract_progress += 1;
        }

        // Rancher achievement
        const chickens = this.state.grid.flat().filter(t => t === 12).length;
        const cows = this.state.grid.flat().filter(t => t === 13).length;
        const goats = this.state.grid.flat().filter(t => t === 14).length;
        if (chickens + cows + goats >= 5 && !this.state.achievements.farm_rancher) {
            this.state.achievements.farm_rancher = true;
            setAchievement('farm_rancher');
        }

        showToast(`Sold ${item} for £${price}`);
        this.save();
        this.render();
    },

    takeContract() {
        if (this.state.active_contract) { showToast('Already have a contract!'); return; }
        const contracts = FT_CONFIG.contracts || [];
        if (contracts.length === 0) return;

        const contract = contracts[Math.floor(Math.random() * contracts.length)];
        this.state.active_contract = { ...contract };
        this.state.contract_progress = 0;
        showToast(`📜 Contract: ${contract.name}`);
        this.save();
        this.render();
    },

    fulfillContract() {
        if (!this.state.active_contract) return;
        const contract = this.state.active_contract;
        if (this.state.contract_progress < contract.qty) {
            showToast(`Need ${contract.qty - this.state.contract_progress} more ${contract.item}!`);
            return;
        }

        this.state.money += contract.reward;
        this.state.total_earned += contract.reward;
        showToast(`🎉 Contract fulfilled! +£${contract.reward}`);
        this.state.active_contract = null;
        this.state.contract_progress = 0;

        this.save();
        this.render();
    },

    // ── 3h. Day advance & weather events ──

    advanceDay() {
        const oldSeason = this.getSeason(this.state.day);
        this.state.day += 1;
        this.state.last_event = "";
        this.state.market_event = null;

        const newSeason = this.getSeason(this.state.day);

        // Season transition effect
        if (oldSeason !== newSeason) {
            const flash = document.createElement('div');
            flash.className = `season-flash ${newSeason.toLowerCase()}`;
            document.body.appendChild(flash);
            setTimeout(() => flash.remove(), 1500);
            this.state.last_event += (this.state.last_event ? ' | ' : '') + `🌸 ${newSeason} has arrived!`;
        }

        // Weather for visual effects
        const seasonName = newSeason.toLowerCase();
        if (seasonName === 'winter') {
            this.state.weather_visual = 'snow';
        } else if (seasonName === 'autumn') {
            this.state.weather_visual = 'leaves';
        } else if (seasonName === 'summer') {
            this.state.weather_visual = 'sun';
        } else {
            this.state.weather_visual = 'clear';
        }
        if (Math.random() < 0.25 && seasonName !== 'winter') {
            this.state.weather_visual = 'rain';
        }

        // Random market surge
        if (Math.random() < 0.2) {
            const items = Object.keys(FT_CONFIG.base_prices);
            const surgeItem = items[Math.floor(Math.random() * items.length)];
            this.state.market_event = surgeItem;
            this.state.last_event = `📈 ${surgeItem} prices are surging!`;
        }

        // Weather events
        if (FT_CONFIG && FT_CONFIG.weather_events) {
            for (const evt of FT_CONFIG.weather_events) {
                if (evt.seasons.includes(newSeason) && Math.random() < evt.chance) {
                    this.state.last_event += (this.state.last_event ? ' | ' : '') + evt.desc;
                    this.applyWeatherEvent(evt);
                    break;
                }
            }
        }

        // Crop growth
        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 6; c++) {
                const tile = this.state.grid[r][c];
                if (tile === 2) this.state.grid[r][c] = 3;
                else if (tile === 3) this.state.grid[r][c] = 4;
                else if (tile === 0) {
                    this.state.soil_health[r][c] = Math.min(100, this.state.soil_health[r][c] + 5);
                    this.state.fallow_days[r][c] += 1;
                }
            }
        }

        // Animal production
        const year = this.getYear(this.state.day);
        const season = newSeason;
        const chickens = this.state.grid.flat().filter(t => t === 12).length;
        const cows = this.state.grid.flat().filter(t => t === 13).length;
        const goats = this.state.grid.flat().filter(t => t === 14).length;
        const feedNeeded = chickens + cows * 2 + goats;
        const feedHave = this.state.inventory.Feed || 0;

        if (year >= 2 && (chickens + cows + goats) > 0) {
            if (feedHave >= feedNeeded) {
                this.state.inventory.Feed -= feedNeeded;
                if (this.state.inventory.Feed <= 0) delete this.state.inventory.Feed;
                if (chickens > 0) this.state.inventory.Egg = (this.state.inventory.Egg || 0) + chickens;
                if (cows > 0) this.state.inventory.Milk = (this.state.inventory.Milk || 0) + cows;
                if (goats > 0) this.state.inventory.Milk = (this.state.inventory.Milk || 0) + goats;
                this.state.last_event += (this.state.last_event ? ' | ' : '') + `🐔 Produced ${chickens} Egg(s), ${cows + goats} Milk`;
            } else {
                this.state.last_event += (this.state.last_event ? ' | ' : '') + '⚠️ Not enough feed! Animals produced nothing.';
            }
        }

        // Beehive production
        const beehives = this.state.grid.flat().filter(t => t === 9).length;
        if (beehives >= 3 && !this.state.achievements.farm_beekeeper) {
            this.state.achievements.farm_beekeeper = true;
            setAchievement('farm_beekeeper');
        }

        if (beehives > 0 && season !== "Winter") {
            this.state.inventory.Honey = (this.state.inventory.Honey || 0) + beehives;
        }

        // Greenhouse production
        const greenhouses = this.state.grid.flat().filter(t => t === 15).length;
        if (greenhouses > 0) {
            for (let g = 0; g < greenhouses; g++) {
                const roll = Math.random();
                if (roll < 0.5) {
                    this.state.inventory.Tomato = (this.state.inventory.Tomato || 0) + 1;
                    this.state.last_event += (this.state.last_event ? ' | ' : '') + '🌿 Greenhouse grew a Tomato';
                } else {
                    this.state.inventory.Strawberry = (this.state.inventory.Strawberry || 0) + 1;
                    this.state.last_event += (this.state.last_event ? ' | ' : '') + '🌿 Greenhouse grew a Strawberry';
                }
            }
        }

        // Winter crop death
        if (season === "Winter") {
            const hasGreenhouse = this.state.grid.flat().includes(15);
            if (!hasGreenhouse) {
                for (let r = 0; r < 5; r++) {
                    for (let c = 0; c < 6; c++) {
                        if ([2, 3, 4].includes(this.state.grid[r][c])) {
                            this.state.grid[r][c] = 0;
                            delete this.state.crop_map[`${r},${c}`];
                        }
                    }
                }
                this.state.last_event += (this.state.last_event ? ' | ' : '') + '❄️ Winter killed your crops! Build a Cold Frame!';
            }
        }

        // Random weeds
        if (Math.random() < 0.1) {
            const emptyTiles = [];
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 6; c++) {
                    if (this.state.grid[r][c] === 0) emptyTiles.push([r, c]);
                }
            }
            if (emptyTiles.length > 0) {
                const [wr, wc] = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
                this.state.grid[wr][wc] = 7;
                this.state.last_event += (this.state.last_event ? ' | ' : '') + '🌿 Weeds appeared!';
            }
        }

        // Random building damage
        if (Math.random() < 0.05) {
            const buildings = [];
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 6; c++) {
                    if (![0, 1, 2, 3, 4, 5, 7].includes(this.state.grid[r][c]) &&
                        !this.state.damaged_buildings.some(d => d[0] === r && d[1] === c)) {
                        buildings.push([r, c]);
                    }
                }
            }
            if (buildings.length > 0) {
                const [dr, dc] = buildings[Math.floor(Math.random() * buildings.length)];
                this.state.damaged_buildings.push([dr, dc]);
                this.state.last_event += (this.state.last_event ? ' | ' : '') + '⚠️ A building was damaged!';
            }
        }

        // Rancher achievement check
        const totalAnimals = this.state.grid.flat().filter(t => t === 12).length +
                            this.state.grid.flat().filter(t => t === 13).length +
                            this.state.grid.flat().filter(t => t === 14).length;
        if (totalAnimals >= 5 && !this.state.achievements.farm_rancher) {
            this.state.achievements.farm_rancher = true;
            setAchievement('farm_rancher');
        }

        // Market price fluctuations
        if (FT_CONFIG) {
            for (const item of Object.keys(this.state.market_prices)) {
                const base = FT_CONFIG.base_prices[item] || 5;
                if ((this.state.sales_log[item] || 0) > 10) {
                    this.state.market_prices[item] = Math.max(1, Math.floor(base * 0.8));
                } else {
                    this.state.market_prices[item] = Math.min(
                        base + 5,
                        Math.floor(base * (0.9 + Math.random() * 0.2))
                    );
                }
            }
        }
        this.state.fishing_today = 0;
        this.state.sales_log = {};

        // Generate new weather forecast
        this.generateForecast();

        // Check unlocks
        this.checkUnlocks();

        this.save();
        this.render();
    },

    applyWeatherEvent(evt) {
        const type = evt.effect;
        if (type === 'drought') {
            const hasSprinkler = this.state.grid.flat().includes(11);
            if (!hasSprinkler) {
                for (let r = 0; r < 5; r++) {
                    for (let c = 0; c < 6; c++) {
                        if (this.state.grid[r][c] === 3) {
                            this.state.grid[r][c] = 2; // growth reverses
                        }
                    }
                }
            }
        } else if (type === 'storm') {
            const buildings = [];
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 6; c++) {
                    if (![0, 1, 2, 3, 4, 5, 7].includes(this.state.grid[r][c]) &&
                        !this.state.damaged_buildings.some(d => d[0] === r && d[1] === c)) {
                        buildings.push([r, c]);
                    }
                }
            }
            if (buildings.length > 0) {
                const [dr, dc] = buildings[Math.floor(Math.random() * buildings.length)];
                this.state.damaged_buildings.push([dr, dc]);
            }
        } else if (type === 'frost') {
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 6; c++) {
                    if (this.state.grid[r][c] === 2) {
                        this.state.grid[r][c] = 0; // seedlings killed
                        delete this.state.crop_map[`${r},${c}`];
                    }
                }
            }
        } else if (type === 'pest') {
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 6; c++) {
                    if ([2, 3].includes(this.state.grid[r][c])) {
                        let hasScarecrow = false;
                        for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1]]) {
                            const nr = r + dr, nc = c + dc;
                            if (nr >= 0 && nr < 5 && nc >= 0 && nc < 6 && this.state.grid[nr][nc] === 10) {
                                hasScarecrow = true;
                                break;
                            }
                        }
                        if (!hasScarecrow && Math.random() < 0.3) {
                            this.state.grid[r][c] = 7; // becomes weeds
                            delete this.state.crop_map[`${r},${c}`];
                        }
                    }
                }
            }
        } else if (type === 'bountiful') {
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 6; c++) {
                    this.state.soil_health[r][c] = Math.min(100, this.state.soil_health[r][c] + 10);
                }
            }
        }
    },

    // ── 3i. Reset ──

    reset() {
        if (!confirm('Delete your entire farm progress?')) return;
        this.state = {
            ...this.defaults,
            grid: this.createGrid(),
            soil_health: Array.from({ length: 5 }, () => Array(6).fill(100)),
            fallow_days: Array.from({ length: 5 }, () => Array(6).fill(0)),
            market_prices: FT_CONFIG ? { ...FT_CONFIG.base_prices } : {},
            unlocked_crops: ["Wheat", "Carrot", "Corn"],
            harvest_families: {},
        };
        document.getElementById('ft-win-banner').classList.add('hidden');
        this.save();
        this.render();
    }
};


// ════════════════════════════════════════════════
// 4. MARKET GARDEN
// ════════════════════════════════════════════════

const marketGarden = {

    // ── 4a. Defaults & state ──

    defaults: {
        beds: null,
        day: 1,
        money: 80,
        compost: 0,
        inventory: {},
        total_earned: 0,
        level: 1,
        xp: 0,
        weather: '☀️ Sunny',
        market_prices: null,
        sales_log: {},
        events: [],
        companion_count: 0,
        rotation_count: 0,
        total_harvests: 0,
        has_polytunnel: false,
        fertiliser: 0,
        organic_certified: false,
        has_irrigation: false,
        water_saved: 0,
        golden_found: [],
        rare_found: [],
        selected_crop: "",
        unlocked_crops: ["Carrot", "Lettuce", "Potato", "Beans", "Onion", "Peas"],
        harvest_tracker: {},
        achievements: {
            mg_first_harvest: false, mg_companion: false, mg_rotation: false,
            mg_market_master: false, mg_golden: false, mg_rainwater: false, mg_polytunnel: false
        }
    },

    state: null,

    // ── 4b. Init & save ──

    init() {
        this.state = loadState('mg_state', this.defaults);

        if (!this.state.beds || !Array.isArray(this.state.beds) || this.state.beds.length === 0) {
            this.state.beds = [];
            for (let i = 0; i < 12; i++) {
                this.state.beds.push({ crop: null, days: 0, soil_N: 80, soil_P: 80, soil_K: 80, history: [], watered: false });
            }
        }
        if (!this.state.achievements) {
            this.state.achievements = { mg_first_harvest: false, mg_companion: false, mg_rotation: false, mg_market_master: false, mg_golden: false, mg_rainwater: false, mg_polytunnel: false };
        }
        if (!Array.isArray(this.state.golden_found)) this.state.golden_found = [];
        if (!Array.isArray(this.state.rare_found)) this.state.rare_found = [];
        if (!Array.isArray(this.state.events)) this.state.events = [];
        if (!this.state.unlocked_crops) this.state.unlocked_crops = ["Carrot", "Lettuce", "Potato", "Beans", "Onion", "Peas"];
        if (!this.state.harvest_tracker) this.state.harvest_tracker = {};

        fetch('/api/games/market-garden').then(r => r.json()).then(cfg => {
            MG_CONFIG = cfg;
            if (!this.state.market_prices) this.state.market_prices = { ...cfg.market_base };
            for (const [k, v] of Object.entries(cfg.market_base)) {
                if (!(k in this.state.market_prices)) this.state.market_prices[k] = v;
            }
            this.checkMgUnlocks();
            this.save();
            this.render();
        });
    },

    save() {
        saveState('mg_state', this.state);
    },

    // ── 4c. Month / season helpers ──

    getMonth(day) {
        const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
        return months[Math.floor((day - 1) / 4) % 12];
    },

    getSeason(month) {
        if (!MG_CONFIG) return "Spring";
        for (const [season, months] of Object.entries(MG_CONFIG.seasons)) {
            if (months.includes(month)) return season;
        }
        return "Spring";
    },

    checkMgUnlocks() {
        if (!MG_CONFIG || !MG_CONFIG.crop_unlocks) return;
        for (const [crop, req] of Object.entries(MG_CONFIG.crop_unlocks)) {
            if (this.state.unlocked_crops.includes(crop)) continue;
            let unlocked = false;
            if (req.require === 'total_harvests' && this.state.total_harvests >= (req.threshold || 5)) unlocked = true;
            else if (req.require === 'total_earned' && this.state.total_earned >= (req.threshold || 200)) unlocked = true;
            else if (req.require === 'harvest_family' && this.state.harvest_tracker[req.family] >= (req.threshold || 3)) unlocked = true;
            else if (req.require === 'has_polytunnel' && this.state.has_polytunnel) unlocked = true;
            if (unlocked) {
                this.state.unlocked_crops.push(crop);
                showToast(`🔓 ${crop} unlocked!`);
            }
        }
    },

    // ── 4d. Soil & companion helpers ──

    getSoilColor(val) {
        if (val >= 70) return "#4CAF50";
        if (val >= 40) return "#FFC107";
        return "#F44336";
    },

    getSoilEmoji(val) {
        if (val >= 70) return "🟢";
        if (val >= 40) return "🟡";
        return "🔴";
    },

    getCompanionBonus(bedIdx, crop) {
        if (!MG_CONFIG) return { bonuses: [], penalties: [] };
        const bonuses = [];
        const penalties = [];
        const row = Math.floor(bedIdx / 4);
        const col = bedIdx % 4;
        const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];

        for (const [dr, dc] of dirs) {
            const nr = row + dr, nc = col + dc;
            if (nr >= 0 && nr < 3 && nc >= 0 && nc < 4) {
                const adjIdx = nr * 4 + nc;
                const adjCrop = this.state.beds[adjIdx].crop;
                if (adjCrop) {
                    const pair = [crop, adjCrop].sort().join(',');
                    if (MG_CONFIG.companions[pair]) bonuses.push({ crop: adjCrop, data: MG_CONFIG.companions[pair] });
                    if (MG_CONFIG.antagonists[pair]) penalties.push({ crop: adjCrop, desc: MG_CONFIG.antagonists[pair] });
                }
            }
        }
        return { bonuses, penalties };
    },

    // ── 4e. Render methods ──

    updateGardenScene() {
        const month = this.getMonth(this.state.day);
        const season = this.getSeason(month).toLowerCase();
        const scene = document.getElementById('mg-garden-scene');
        if (scene) scene.className = 'mg-scene season-' + season;
        renderWeatherParticles('mg-weather-particles', season, { isRain: this.state.weather.includes('Rainy') });
        updateDayOverlay('mg-day-overlay', this.state.day);
    },

    renderGardenScene() {
        const container = document.getElementById('mg-village-view');
        if (!container) return;
        if (!MG_CONFIG) return;

        const beds = this.state.beds;
        const month = this.getMonth(this.state.day);
        const season = this.getSeason(month).toLowerCase();
        const pal = GardenPalettes[season] || GardenPalettes.spring;
        const isWinter = season === 'winter';
        const isRaining = this.state.weather.includes('Rainy');

        // Bed positions: [bedIdx, left%, top%]
        const bedPositions = [
            [0,  6,  44], [1,  18, 44], [2,  30, 44],
            [3,  6,  62], [4,  18, 62], [5,  30, 62],
            [6,  56, 44], [7,  68, 44], [8,  80, 44],
            [9,  56, 62], [10, 68, 62], [11, 80, 62],
        ];

        // Sky (small strip — it's a market, not open countryside)
        const sunIcons = { spring: '🌤️', summer: '☀️', autumn: '🍂', winter: '❄️' };
        const sunIcon = sunIcons[season] || '🌤️';
        const cloudsHtml = [0, 1].map(i =>
            `<div class="vf-cloud" style="top:${8 + i * 12}%; left:${10 + i * 40}%; animation-duration:${20 + i * 12}s; animation-delay:${i * 5}s; font-size:${1.2 + i * 0.3}rem;">☁️</div>`
        ).join('');

        // Render each bed
        let bedsHtml = '';
        for (const [bedIdx, bedLeft, bedTop] of bedPositions) {
            const bed = beds[bedIdx];
            let patchClass = 'vg-patch';
            let svgContent = '';
            let hoverInfo = '';
            let companionHtml = '';

            // Soil NPK dots
            const nColor = bed.soil_N >= 70 ? '#4CAF50' : (bed.soil_N >= 40 ? '#FFC107' : '#F44336');
            const pColor = bed.soil_P >= 70 ? '#4CAF50' : (bed.soil_P >= 40 ? '#FFC107' : '#F44336');
            const kColor = bed.soil_K >= 70 ? '#4CAF50' : (bed.soil_K >= 40 ? '#FFC107' : '#F44336');
            const soilDotsHtml = `<div class="vg-soil-dots">
                <span class="vg-dot" style="background:${nColor};" title="N:${bed.soil_N}%"></span>
                <span class="vg-dot" style="background:${pColor};" title="P:${bed.soil_P}%"></span>
                <span class="vg-dot" style="background:${kColor};" title="K:${bed.soil_K}%"></span>
            </div>`;

            if (!bed.crop) {
                const soilAvg = (bed.soil_N + bed.soil_P + bed.soil_K) / 3;
                const soilStatus = soilAvg >= 70 ? 'Good' : (soilAvg >= 40 ? 'Fair' : 'Poor');
                const historyStr = bed.history.length ? ' | Previous: ' + bed.history.slice(-2).join(', ') : '';
                hoverInfo = `Bed ${bedIdx + 1}: Empty | Soil: ${soilStatus}${historyStr}`;

                if (isWinter) {
                    svgContent = GardenSVGs.winterBed(pal);
                } else {
                    svgContent = GardenSVGs.emptyBed(pal);
                }
                if (soilAvg < 40) patchClass += ' vg-soil-poor';
                else if (soilAvg < 70) patchClass += ' vg-soil-fair';
            } else {
                const cropData = MG_CONFIG.crops[bed.crop];
                if (!cropData) continue;
                const daysLeft = Math.max(0, cropData.days - bed.days);
                const progress = bed.days / cropData.days;
                const { bonuses, penalties } = this.getCompanionBonus(bedIdx, bed.crop);
                const soilAvg = (bed.soil_N + bed.soil_P + bed.soil_K) / 3;

                if (progress <= 0.25) {
                    svgContent = GardenSVGs.seededBed(pal);
                    hoverInfo = `${cropData.icon} ${bed.crop} — Seed | ${daysLeft} days left | Soil: ${soilAvg.toFixed(0)}%`;
                } else if (progress < 1) {
                    svgContent = GardenSVGs.growingBed(pal);
                    hoverInfo = `${cropData.icon} ${bed.crop} — Growing | ${daysLeft} days left | Soil: ${soilAvg.toFixed(0)}%`;
                } else {
                    svgContent = GardenSVGs.readyBed(pal);
                    hoverInfo = `${cropData.icon} ${bed.crop} — Ready to harvest! | Soil: ${soilAvg.toFixed(0)}%`;
                    patchClass += ' vg-patch-ready';
                }

                if (bonuses.length > 0) {
                    patchClass += ' vg-companion';
                    const companionNames = bonuses.map(b => b.crop).join(', ');
                    companionHtml = `<div class="vg-companion-indicator">🤝 ${companionNames}</div>`;
                }
                if (penalties.length > 0) {
                    patchClass += ' vg-antagonist';
                    const antagonistNames = penalties.map(p => p.crop).join(', ');
                    companionHtml += `<div class="vg-antagonist-indicator">⚠️ ${antagonistNames}</div>`;
                }

                if (soilAvg < 40) patchClass += ' vg-soil-poor';
                else if (soilAvg < 70) patchClass += ' vg-soil-fair';
            }

            bedsHtml += `<div class="${patchClass}" style="left:${bedLeft}%; top:${bedTop}%;" data-info="${hoverInfo.replace(/"/g, '&quot;')}" onmouseenter="showGardenInfo(event, this)" onmouseleave="hideGardenInfo()">${svgContent}${soilDotsHtml}${companionHtml}</div>`;
        }

        // Market produce display
        const inv = this.state.inventory;
        const invItems = Object.entries(inv).filter(([_, v]) => v > 0);
        let leftProduce = '';
        let rightProduce = '';
        const maxPerStall = 6;

        invItems.forEach(([item, qty], idx) => {
            const cropData = MG_CONFIG.crops[item];
            const icon = cropData ? cropData.icon : (item.startsWith('Golden') ? '🌟' : '📦');
            const display = `<div class="vg-produce-item" title="${item}: ${qty}">${icon}<span class="vg-produce-qty">${qty > 99 ? '99+' : qty}</span></div>`;
            if (idx < maxPerStall) leftProduce += display;
            else rightProduce += display;
        });

        // Irrigation
        let irrigationHtml = '';
        if (this.state.has_irrigation) {
            irrigationHtml = `
                <div class="vg-pipe" style="left: 3%; top: 28%; width: 44%;"></div>
                <div class="vg-pipe" style="left: 53%; top: 28%; width: 44%;"></div>
                <div class="vg-pipe" style="left: 3%; top: 58%; width: 44%;"></div>
                <div class="vg-pipe" style="left: 53%; top: 58%; width: 44%;"></div>
                <div class="vg-drip" style="left: 10%; top: 29%;"></div>
                <div class="vg-drip" style="left: 24%; top: 29%; animation-delay: 0.5s;"></div>
                <div class="vg-drip" style="left: 38%; top: 29%; animation-delay: 1s;"></div>
                <div class="vg-drip" style="left: 60%; top: 29%; animation-delay: 0.3s;"></div>
                <div class="vg-drip" style="left: 74%; top: 29%; animation-delay: 0.8s;"></div>
                <div class="vg-drip" style="left: 88%; top: 29%; animation-delay: 1.2s;"></div>
                <div class="vg-drip" style="left: 10%; top: 59%; animation-delay: 0.2s;"></div>
                <div class="vg-drip" style="left: 24%; top: 59%; animation-delay: 0.7s;"></div>
                <div class="vg-drip" style="left: 38%; top: 59%; animation-delay: 1.1s;"></div>
                <div class="vg-drip" style="left: 60%; top: 59%; animation-delay: 0.4s;"></div>
                <div class="vg-drip" style="left: 74%; top: 59%; animation-delay: 0.9s;"></div>
                <div class="vg-drip" style="left: 88%; top: 59%; animation-delay: 1.3s;"></div>`;
        }

        // Weather
        let weatherHtml = '';
        if (season === 'winter') {
            for (let i = 0; i < 20; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 8;
                const duration = 6 + Math.random() * 6;
                const size = 4 + Math.random() * 4;
                weatherHtml += `<div class="vf-snow" style="left:${left}%; width:${size}px; height:${size}px; animation-delay:${delay}s; animation-duration:${duration}s;"></div>`;
            }
        }
        if (season === 'autumn') {
            const leaves = ['🍂', '🍁', '🍃'];
            for (let i = 0; i < 6; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 10;
                const duration = 8 + Math.random() * 8;
                weatherHtml += `<div class="vf-leaf" style="left:${left}%; animation-delay:${delay}s; animation-duration:${duration}s;">${leaves[i % 3]}</div>`;
            }
        }
        if (isRaining) {
            for (let i = 0; i < 25; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 2;
                const duration = 0.5 + Math.random() * 0.5;
                const height = 10 + Math.random() * 10;
                weatherHtml += `<div class="vf-rain" style="left:${left}%; height:${height}px; animation-delay:${delay}s; animation-duration:${duration}s;"></div>`;
            }
        }
        if (season === 'summer') {
            for (let i = 0; i < 3; i++) {
                const left = 10 + Math.random() * 80;
                const delay = Math.random() * 6;
                weatherHtml += `<div class="vf-sunray" style="left:${left}%; animation-delay:${delay}s;"></div>`;
            }
        }

        // Day/time
        const dayTime = getDayTimeClass(this.state.day);

        // Render
        container.innerHTML = `
            <div class="village-garden season-${season}">
                <!-- Sky (small — it's a market, not a field) -->
                <div class="vg-sky" style="background: linear-gradient(180deg, ${pal.sky1}, ${pal.sky2});">
                    <div class="vf-sun">${sunIcon}</div>
                    ${cloudsHtml}
                </div>

                <!-- Brick wall backdrop -->
                <div class="vg-wall" style="background: repeating-linear-gradient(180deg, ${pal.wall}, ${pal.wall} 18px, ${pal.wallDk} 18px, ${pal.wallDk} 20px);"></div>

                <!-- Packed earth / cobblestone ground -->
                <div class="vg-ground" style="background: linear-gradient(180deg, ${pal.ground}, ${pal.groundDk});"></div>

                <!-- Left Stall -->
                <div class="vg-stall" style="left: 3%; top: 30%;">
                    <div class="vg-awning" style="background: repeating-linear-gradient(90deg, ${pal.awning1}, ${pal.awning1} 18px, ${pal.awning2} 18px, ${pal.awning2} 36px);">
                        <div class="vg-awning-scallop"></div>
                    </div>
                    <div class="vg-stall-post" style="left: 0;"></div>
                    <div class="vg-stall-post" style="right: 0;"></div>
                    <div class="vg-stall-sign">NORTH</div>
                    <div class="vg-stall-counter" style="background: ${pal.stall}; border-color: ${pal.stallDk};">
                        ${leftProduce || '<span class="vg-no-produce">Empty stall</span>'}
                    </div>
                </div>

                <!-- Right Stall -->
                <div class="vg-stall" style="left: 53%; top: 30%;">
                    <div class="vg-awning" style="background: repeating-linear-gradient(90deg, ${pal.awning1}, ${pal.awning1} 18px, ${pal.awning2} 18px, ${pal.awning2} 36px);">
                        <div class="vg-awning-scallop"></div>
                    </div>
                    <div class="vg-stall-post" style="left: 0;"></div>
                    <div class="vg-stall-post" style="right: 0;"></div>
                    <div class="vg-stall-sign">SOUTH</div>
                    <div class="vg-stall-counter" style="background: ${pal.stall}; border-color: ${pal.stallDk};">
                        ${rightProduce || '<span class="vg-no-produce">Empty stall</span>'}
                    </div>
                </div>

                <!-- Beds -->
                <div style="position:absolute; inset:0; z-index:15; pointer-events:none;">
                    ${bedsHtml}
                </div>

                ${irrigationHtml}

                <div class="vg-foreground" style="background: linear-gradient(0deg, ${pal.groundDk}, transparent);"></div>
                ${weatherHtml}
                <div class="vg-time-overlay ${dayTime}"></div>
                <div class="vg-info-panel" id="vg-info-panel"></div>
            </div>
            <p style="text-align: center; color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.5rem; padding: 0.8rem; background: var(--bg-card); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                💡 Switch to the 🌱 Garden tab to plant, water, and harvest your crops.
            </p>
        `;
    },


    render() {
        this.renderStats();
        this.renderGolden();
        this.renderEvents();
        this.renderWeather();
        this.renderCropSelect();
        this.renderBeds();
        this.renderActions();
        this.renderMarket();
        this.renderDayInfo();
        this.renderCatalogue();
        this.renderAchievements();
        this.updateGardenScene();
        // Render garden scene if scene tab is active
        const sceneTab = document.getElementById('mg-tab-scene');
        if (sceneTab && sceneTab.classList.contains('active')) {
            this.renderGardenScene();
        }
    },


    renderStats() {
        const s = this.state;
        const month = this.getMonth(s.day);
        const season = this.getSeason(month);
        const seasonIcon = { Spring: "🌸", Summer: "☀️", Autumn: "🍂", Winter: "❄️" }[season] || "🌸";

        document.getElementById('mg-stats').innerHTML = `
            <div class="stat-box year"><div class="stat-label">${seasonIcon} SEASON</div><div class="stat-value">${season}</div></div>
            <div class="stat-box"><div class="stat-label">📅 MONTH</div><div class="stat-value">${month.substring(0, 3)}</div></div>
            <div class="stat-box money"><div class="stat-label">💰 MONEY</div><div class="stat-value">£${s.money}</div></div>
            <div class="stat-box"><div class="stat-label">💧 WATER SAVED</div><div class="stat-value">£${s.water_saved.toFixed(0)}</div></div>
            <div class="stat-box"><div class="stat-label">⭐ LEVEL</div><div class="stat-value">${s.level} (${s.xp} XP)</div></div>
            <div class="stat-box harvests"><div class="stat-label">🌾 HARVESTS</div><div class="stat-value">${s.total_harvests}</div></div>
        `;
    },

    renderGolden() {
        const el = document.getElementById('mg-golden');
        if (this.state.golden_found.length > 0) {
            el.innerHTML = `<div style="background: linear-gradient(135deg, #1a1a00, #2a2a00); border: 2px solid var(--amber); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <span style="color: var(--amber); font-weight: 600;">🌟 Golden Crops Found:</span>
                <span style="color: var(--cream);"> ${this.state.golden_found.join(', ')}</span>
            </div>`;
        } else {
            el.innerHTML = '';
        }
    },

    renderEvents() {
        const el = document.getElementById('mg-events');
        if (this.state.events.length > 0) {
            const recent = this.state.events.slice(-3);
            el.innerHTML = `<div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                <div style="color: var(--green-light); font-weight: 600; margin-bottom: 0.3rem;">📋 Recent Events</div>
                ${recent.map(e => `<div style="color: var(--cream-dim); font-size: 0.85rem;">${e}</div>`).join('')}
            </div>`;
        } else {
            el.innerHTML = '';
        }
    },

    renderWeather() {
        const el = document.getElementById('mg-weather');
        const month = this.getMonth(this.state.day);
        const season = this.getSeason(month);
        const isRaining = this.state.weather.includes('Rainy');

        if (isRaining) {
            el.innerHTML = `<div class="warning-box winter-safe" style="background: linear-gradient(135deg, #0a1a2a, #1a2e3d); border-color: #2196F3;">
                <span style="color: #2196F3; font-weight: 600;">🌧️ It's raining!</span>
                <span style="color: var(--cream-dim);"> All beds watered for free today.</span>
            </div>`;
        } else if (season === "Winter") {
            el.innerHTML = `<div class="warning-box winter-danger">
                <span style="color: var(--danger); font-weight: 600;">❄️ Winter:</span>
                <span style="color: var(--cream-dim);"> No crops can be planted.</span>
            </div>`;
        } else if (season === "Autumn") {
            el.innerHTML = `<div class="warning-box autumn">
                <span style="color: var(--amber); font-weight: 600;">🍂 Autumn:</span>
                <span style="color: var(--cream-dim);"> Fewer crops available. Clear beds for winter.</span>
            </div>`;
        } else {
            el.innerHTML = '';
        }
    },

    renderCropSelect() {
        const el = document.getElementById('mg-crop-select');
        if (!MG_CONFIG) { el.innerHTML = ''; return; }

        const month = this.getMonth(this.state.day);
        const season = this.getSeason(month);
        const unlocked = this.state.unlocked_crops;

        let available = Object.entries(MG_CONFIG.crops)
            .filter(([name]) => unlocked.includes(name))
            .filter(([name, data]) => data.season.includes(season))
            .map(([name]) => name);

        let html = `<div class="crop-select-area">
            <label>🌱 Select crop to plant:</label><br>
            <select id="mg-crop-dropdown" onchange="marketGarden.state.selected_crop = this.value; marketGarden.renderCropSelect();">
                <option value="">— Select a crop —</option>`;
        for (const name of available) {
            const data = MG_CONFIG.crops[name];
            const sel = this.state.selected_crop === name ? ' selected' : '';
            html += `<option value="${name}"${sel}>${data.icon} ${name} (£${data.seed_cost})</option>`;
        }
        // Show locked crops
        const allCrops = Object.keys(MG_CONFIG.crops);
        const lockedCrops = allCrops.filter(n => !unlocked.includes(n));
        for (const name of lockedCrops) {
            const data = MG_CONFIG.crops[name];
            const unlockInfo = MG_CONFIG.crop_unlocks && MG_CONFIG.crop_unlocks[name];
            const desc = unlockInfo ? unlockInfo.desc : 'Locked';
            html += `<option value="${name}" disabled>🔒 ${name} — ${desc}</option>`;
        }
        html += `</select></div>`;

        const crop = this.state.selected_crop;
        if (crop && MG_CONFIG.crops[crop]) {
            let compHtml = '';
            let antHtml = '';
            for (const [pair, data] of Object.entries(MG_CONFIG.companions)) {
                if (pair.includes(crop)) {
                    const other = pair.split(',').find(p => p !== crop) || pair.split(',')[0];
                    compHtml += `<span style="color: var(--green-light);">${MG_CONFIG.crops[other]?.icon || ''} ${other}: ${data.bonus}</span><br>`;
                }
            }
            for (const [pair, desc] of Object.entries(MG_CONFIG.antagonists)) {
                if (pair.includes(crop)) {
                    const other = pair.split(',').find(p => p !== crop) || pair.split(',')[0];
                    antHtml += `<span style="color: #ff8a80;">${MG_CONFIG.crops[other]?.icon || ''} ${other}: ${desc}</span><br>`;
                }
            }
            if (compHtml || antHtml) {
                html += '<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">';
                if (compHtml) html += `<div class="companion-info good" style="flex: 1;">🤝 Companions:<br>${compHtml}</div>`;
                if (antHtml) html += `<div class="companion-info bad" style="flex: 1;">⚠️ Avoid:<br>${antHtml}</div>`;
                html += '</div>';
            }
        }

        el.innerHTML = html;
    },

    renderBeds() {
        const el = document.getElementById('mg-beds');
        if (!MG_CONFIG) { el.innerHTML = ''; return; }

        let html = '';
        for (let i = 0; i < 12; i++) {
            const bed = this.state.beds[i];
            if (bed.crop) {
                const cropData = MG_CONFIG.crops[bed.crop];
                const daysLeft = Math.max(0, cropData.days - bed.days);
                const progress = Math.min(100, Math.floor(bed.days / cropData.days * 100));
                const { bonuses, penalties } = this.getCompanionBonus(i, bed.crop);

                let bedClass = 'mg-bed';
                if (penalties.length > 0) bedClass += ' antagonist';
                else if (bonuses.length > 0) bedClass += ' companion';

                if (bed.crop && daysLeft > 0) {
                    const progressRatio = bed.days / cropData.days;
                    if (progressRatio <= 0.25) bedClass += ' crop-seed';
                    else if (progressRatio <= 0.5) bedClass += ' crop-sprout';
                    else bedClass += ' crop-growing';
                }
                if (bed.crop && daysLeft === 0) bedClass += ' crop-ready';

                const isReady = daysLeft === 0;
                const progressClass = isReady ? ' ready' : '';

                const soilBarHtml = `<div class="bed-soil-bars">
                    <div class="soil-bar"><span class="soil-label">N</span><div class="soil-track"><div class="soil-fill nitrogen" style="width:${bed.soil_N}%"></div></div></div>
                    <div class="soil-bar"><span class="soil-label">P</span><div class="soil-track"><div class="soil-fill phosphorus" style="width:${bed.soil_P}%"></div></div></div>
                    <div class="soil-bar"><span class="soil-label">K</span><div class="soil-track"><div class="soil-fill potassium" style="width:${bed.soil_K}%"></div></div></div>
                </div>`;

                let bonusHtml = '';
                for (const b of bonuses) bonusHtml += `<div class="bed-bonus">🤝 +${Math.round((b.data.yield_bonus - 1) * 100)}% from ${b.crop}</div>`;
                let penaltyHtml = '';
                for (const p of penalties) penaltyHtml += `<div class="bed-penalty">⚠️ ${p.desc}</div>`;

                const wateredText = bed.watered ? '💧 Watered' : (this.state.weather.includes('Rainy') ? '🌧️ Rain' : 'Needs water');

                html += `<div class="${bedClass}">
                    <div class="bed-num">Bed ${i + 1}</div>
                    <div class="bed-crop">${cropData.icon}</div>
                    <div class="bed-name">${bed.crop}</div>
                    <div class="bed-progress">${isReady ? '✅ Ready!' : `${daysLeft} days left`}</div>
                    <div class="mg-progress-bar"><div class="mg-progress-fill${progressClass}" style="width: ${progress}%"></div></div>
                    ${soilBarHtml}
                    ${bonusHtml}${penaltyHtml}
                    <div class="bed-status">${wateredText}</div>
                    ${isReady ? `<button class="tile-action-btn harvest" onclick="marketGarden.harvestBed(${i})">🌾 Harvest</button>` :
                        (!bed.watered && !this.state.weather.includes('Rainy') && !this.state.has_irrigation ?
                            `<button class="tile-action-btn" onclick="marketGarden.waterBed(${i})">💧 Water (50p)</button>` : '')}
                </div>`;
            } else {
                const soilAvg = (bed.soil_N + bed.soil_P + bed.soil_K) / 3;
                const soilStatus = soilAvg >= 60 ? "🟢 Good" : (soilAvg >= 35 ? "🟡 Fair" : "🔴 Poor");
                const crop = this.state.selected_crop;
                const season = this.getSeason(this.getMonth(this.state.day));
                const canPlant = crop && MG_CONFIG.crops[crop] && MG_CONFIG.crops[crop].season.includes(season) && this.state.money >= MG_CONFIG.crops[crop].seed_cost && this.state.unlocked_crops.includes(crop);

                const soilBarHtml = `<div class="bed-soil-bars">
                    <div class="soil-bar"><span class="soil-label">N</span><div class="soil-track"><div class="soil-fill nitrogen" style="width:${bed.soil_N}%"></div></div></div>
                    <div class="soil-bar"><span class="soil-label">P</span><div class="soil-track"><div class="soil-fill phosphorus" style="width:${bed.soil_P}%"></div></div></div>
                    <div class="soil-bar"><span class="soil-label">K</span><div class="soil-track"><div class="soil-fill potassium" style="width:${bed.soil_K}%"></div></div></div>
                </div>`;

                let rotationWarning = '';
                if (crop && bed.history.length > 0) {
                    const lastCrop = bed.history[bed.history.length - 1];
                    if (lastCrop && MG_CONFIG.crops[crop] && MG_CONFIG.crops[lastCrop] &&
                        MG_CONFIG.crops[crop].family === MG_CONFIG.crops[lastCrop].family) {
                        rotationWarning = '<div style="color: var(--danger); font-size: 0.75rem;">⚠️ Same family! -30%</div>';
                    }
                }

                html += `<div class="mg-bed empty">
                    <div class="bed-num">Bed ${i + 1}: Empty</div>
                    <div class="bed-soil">Soil: ${soilStatus}</div>
                    ${soilBarHtml}
                    ${bed.history.length > 0 ? `<div style="font-size: 0.7rem; color: var(--cream-dim);">Previous: ${bed.history.slice(-2).join(', ')}</div>` : ''}
                    ${rotationWarning}
                    ${canPlant ? `<button class="tile-action-btn" onclick="marketGarden.plantInBed(${i})">🌱 Plant £${MG_CONFIG.crops[crop].seed_cost}</button>` : ''}
                    ${this.state.compost > 0 ? `<button class="tile-action-btn" onclick="marketGarden.compostBed(${i})" style="margin-top: 0.2rem;">🧪 Compost (${this.state.compost})</button>` : ''}
                    ${this.state.fertiliser > 0 ? `<button class="tile-action-btn" onclick="marketGarden.fertiliseBed(${i})" style="margin-top: 0.2rem;">🧴 Fertiliser (${this.state.fertiliser})</button>` : ''}
                </div>`;
            }
        }
        el.innerHTML = html;
    },

    renderActions() {
        let el = document.getElementById('mg-tools-content');
        if (!el) el = document.getElementById('mg-actions');
        if (!MG_CONFIG) { el.innerHTML = ''; return; }

        let html = '';

        html += `<div class="action-card">
            <h4>🧪 Compost</h4>
            <div class="ac-desc">Restore +20 NPK to a bed</div>
            <div class="ac-value">Stock: ${this.state.compost}</div>
            <button class="btn-primary" onclick="marketGarden.buyCompost()" ${this.state.money >= 3 ? '' : 'disabled'}>♻️ Make 2 Compost (£3)</button>
        </div>`;

        html += `<div class="action-card">
            <h4>🧴 Fertiliser</h4>
            <div class="ac-desc">Restore +30 NPK to a bed</div>
            <div class="ac-value">Stock: ${this.state.fertiliser}</div>
            <button class="btn-primary" onclick="marketGarden.buyFertiliser()" ${this.state.money >= 5 ? '' : 'disabled'}>Buy Fertiliser (£5)</button>
        </div>`;

        html += `<div class="action-card"><h4>🏗️ Upgrades</h4>`;
        if (!this.state.has_irrigation) {
            html += `<button class="btn-primary" onclick="marketGarden.buyUpgrade('irrigation')" ${this.state.money >= 150 ? '' : 'disabled'} style="margin-bottom: 0.3rem; width: 100%;">💧 Irrigation (£150)</button>
                      <div style="color: var(--cream-dim); font-size: 0.75rem; margin-bottom: 0.5rem;">Auto-water all beds</div>`;
        } else {
            html += `<div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border-radius: 8px; padding: 0.5rem; margin-bottom: 0.5rem;"><span style="color: var(--green-leaf); font-weight: 600;">✅ Irrigation active!</span></div>`;
        }
        html += `</div>`;

        html += `<div class="action-card"><h4>🏷️ Certifications</h4>`;
        if (!this.state.organic_certified) {
            html += `<button class="btn-primary" onclick="marketGarden.buyUpgrade('organic')" ${this.state.money >= 500 ? '' : 'disabled'} style="width: 100%;">🏷️ Organic Cert (£500)</button>
                      <div style="color: var(--cream-dim); font-size: 0.75rem; margin-top: 0.3rem;">+30% sell prices</div>`;
        } else {
            html += `<div style="background: linear-gradient(135deg, #0a2a0a, #1a3d1a); border-radius: 8px; padding: 0.5rem;"><span style="color: var(--green-leaf); font-weight: 600;">✅ Organic Certified! +30%</span></div>`;
        }
        html += `</div>`;

        // Unlock progress card
        const allCrops = MG_CONFIG ? Object.keys(MG_CONFIG.crops) : [];
        const unlockCount = this.state.unlocked_crops.length;
        const totalCrops = allCrops.length;
        html += `<div class="action-card"><h4>🔓 Crop Unlocks</h4>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-bottom: 0.3rem;">${unlockCount} / ${totalCrops} crops unlocked</div>
            <div class="mg-progress-bar"><div class="mg-progress-fill" style="width: ${Math.floor(unlockCount/totalCrops*100)}%"></div></div>
        </div>`;

        el.innerHTML = html;
    },

    renderMarket() {
        const el = document.getElementById('mg-market');
        const inv = this.state.inventory;
        const items = Object.entries(inv).filter(([_, v]) => v > 0);

        if (items.length === 0) {
            el.innerHTML = `<div style="background: var(--bg-card); border: 1px solid #3d5a3d; border-radius: 10px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌾</div>
                <div style="color: var(--cream-dim);">Nothing to sell. Harvest crops first!</div>
            </div>`;
            return;
        }

        let html = '<div class="mg-market-grid">';
        for (const [item, qty] of items) {
            const isGolden = item.startsWith('Golden');
            const cropData = MG_CONFIG && MG_CONFIG.crops[item] ? MG_CONFIG.crops[item] : { icon: isGolden ? '🌟' : '📦', sell: 5 };
            let price = this.state.market_prices[item] || cropData.sell || 5;
            const organicBonus = this.state.organic_certified ? 1.3 : 1.0;
            const totalPrice = Math.floor(price * organicBonus);

            html += `<div class="mg-market-item${isGolden ? ' golden-item' : ''}">
                <div class="mmi-icon">${cropData.icon}</div>
                <div class="mmi-name">${item}</div>
                <div class="mmi-qty">Qty: ${qty}</div>
                <div class="mmi-price">£${totalPrice}/unit${this.state.organic_certified ? ' (+30%)' : ''}</div>
                <button class="sell-btn" onclick="marketGarden.sellAll('${item.replace(/'/g, "\\'")}')">Sell All £${totalPrice * qty}</button>
            </div>`;
        }
        html += '</div>';
        el.innerHTML = html;
    },

    renderDayInfo() {
        const el = document.getElementById('mg-day-info');
        const month = this.getMonth(this.state.day);
        const season = this.getSeason(month);
        const seasonIcon = { Spring: "🌸", Summer: "☀️", Autumn: "🍂", Winter: "❄️" }[season] || "🌸";
        const isRaining = this.state.weather.includes('Rainy');

        el.innerHTML = `<div class="season-bar">${seasonIcon} ${season} — ${month.substring(0, 3)} | Day ${this.state.day} | 💧 Watering: ${isRaining ? 'FREE (rain!)' : '50p/bed'}</div>`;
    },

    renderCatalogue() {
        const el = document.getElementById('mg-catalogue');
        if (!MG_CONFIG) { el.innerHTML = ''; return; }

        const unlocked = this.state.unlocked_crops;
        let html = '';

        for (const [season, months] of Object.entries(MG_CONFIG.seasons)) {
            const seasonCrops = Object.entries(MG_CONFIG.crops).filter(([name, data]) => data.season.includes(season));
            if (seasonCrops.length === 0) continue;
            const seasonIcon = { Spring: "🌸", Summer: "☀️", Autumn: "🍂", Winter: "❄️" }[season] || "🌸";
            html += `<div class="catalogue-season"><h4>${seasonIcon} ${season}</h4><div class="catalogue-crops">`;
            for (const [name, data] of seasonCrops) {
                const isUnlocked = unlocked.includes(name);
                const lockIcon = isUnlocked ? '' : ' 🔒';
                const unlockInfo = MG_CONFIG.crop_unlocks && MG_CONFIG.crop_unlocks[name];
                const unlockDesc = unlockInfo ? unlockInfo.desc : '';
                const nutrientHtml = isUnlocked ? `<div class="sp-nutrients">
                    <span class="sp-n ${data.nutrient_drain.N < 0 ? 'sp-n-pos' : ''}">N${data.nutrient_drain.N > 0 ? '-' : '+'}${Math.abs(data.nutrient_drain.N)}</span>
                    <span class="sp-p">P${data.nutrient_drain.P > 0 ? '-' : '+'}${Math.abs(data.nutrient_drain.P)}</span>
                    <span class="sp-k">K${data.nutrient_drain.K > 0 ? '-' : '+'}${Math.abs(data.nutrient_drain.K)}</span>
                </div>` : '';
                html += `<div class="seed-packet${isUnlocked ? '' : ' locked'}" title="${isUnlocked ? name : unlockDesc}">
                    <div class="sp-tab"></div>
                    <div class="sp-icon">${data.icon}</div>
                    <div class="sp-name">${name}${lockIcon}</div>
                    <div class="sp-cost">£${data.seed_cost}</div>
                    <div class="sp-days">${data.days} days</div>
                    ${nutrientHtml}
                </div>`;
            }
            html += '</div></div>';
        }

        html += '<hr class="game-divider"><h4>🤝 Best Companions</h4>';
        const topCompanions = Object.entries(MG_CONFIG.companions).slice(0, 6);
        for (const [pair, data] of topCompanions) {
            const [a, b] = pair.split(',');
            const iconA = MG_CONFIG.crops[a]?.icon || '🌱';
            const iconB = MG_CONFIG.crops[b]?.icon || '🌱';
            html += `<div style="color: var(--cream-dim); font-size: 0.85rem;">${iconA} ${a} + ${iconB} ${b}: ${data.bonus}</div>`;
        }

        html += '<h4 style="margin-top: 0.5rem;">⚠️ Worst Companions</h4>';
        for (const [pair, desc] of Object.entries(MG_CONFIG.antagonists)) {
            const [a, b] = pair.split(',');
            const iconA = MG_CONFIG.crops[a]?.icon || '🌱';
            const iconB = MG_CONFIG.crops[b]?.icon || '🌱';
            html += `<div style="color: var(--cream-dim); font-size: 0.85rem;">${iconA} ${a} + ${iconB} ${b}: ${desc}</div>`;
        }

        el.innerHTML = html;
    },

    renderAchievements() {
        const el = document.getElementById('mg-achievements');
        const achDefs = [
            { key: 'mg_first_harvest', name: '🌱 First Crop', desc: 'Harvest your first crop', progress: () => this.state.achievements.mg_first_harvest ? '(Done)' : `(${this.state.total_harvests}/1)` },
            { key: 'mg_companion', name: '🤝 Companion', desc: 'Plant a companion pair', progress: () => this.state.achievements.mg_companion ? '(Done)' : `(${this.state.companion_count}/1)` },
            { key: 'mg_rotation', name: '🔄 Rotator', desc: 'Rotate crop families', progress: () => this.state.achievements.mg_rotation ? '(Done)' : '(In progress)' },
            { key: 'mg_market_master', name: '💰 Market Master', desc: 'Earn £500 from sales', progress: () => this.state.achievements.mg_market_master ? '(Done)' : `(£${this.state.total_earned}/£500)` },
            { key: 'mg_golden', name: '🌟 Golden Touch', desc: 'Find a Golden crop', progress: () => this.state.achievements.mg_golden ? '(Done)' : '(1 in 100 chance)' },
            { key: 'mg_rainwater', name: '🌧️ Rain Dancer', desc: 'Save £20 with rain', progress: () => this.state.achievements.mg_rainwater ? '(Done)' : `(£${this.state.water_saved.toFixed(0)}/£20)` },
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

    renderLedger() {
        const el = document.getElementById('mg-ledger');
        if (!el) return;
        const s = this.state;
        const plantedBeds = s.beds.filter(b => b.crop).length;
        const emptyBeds = 12 - plantedBeds;
        const avgSoil = plantedBeds > 0 ? Math.round(s.beds.filter(b => b.crop).reduce((a, b) => a + (b.soil_N + b.soil_P + b.soil_K) / 3, 0) / plantedBeds) : 0;

        const rows = [
            { label: '📅 Days Played', value: s.day, cls: '' },
            { label: '💰 Total Earned', value: `£${s.total_earned}`, cls: 'positive' },
            { label: '🌾 Total Harvests', value: s.total_harvests, cls: '' },
            { label: '🌱 Beds Planted', value: `${plantedBeds} / 12`, cls: '' },
            { label: '🟫 Empty Beds', value: emptyBeds, cls: '' },
            { label: '🔬 Avg Soil Health', value: `${avgSoil}%`, cls: avgSoil >= 60 ? 'positive' : (avgSoil >= 35 ? '' : 'negative') },
            { label: '🔓 Crops Unlocked', value: `${s.unlocked_crops.length} / ${MG_CONFIG ? Object.keys(MG_CONFIG.crops).length : 17}`, cls: '' },
            { label: '⭐ Level', value: s.level, cls: '' },
        ];

        el.innerHTML = `<div class="farm-ledger">
            <h4>📊 Garden Statistics</h4>
            ${rows.map(r => `<div class="ledger-row"><span class="ledger-label">${r.label}</span><span class="ledger-value ${r.cls}">${r.value}</span></div>`).join('')}
        </div>`;
    },

    // ── 4f. Player actions ──

    plantInBed(bedIdx) {
        const crop = this.state.selected_crop;
        if (!crop || !MG_CONFIG.crops[crop]) return;
        if (!this.state.unlocked_crops.includes(crop)) { showToast('🔒 Crop not unlocked yet!'); return; }
        const bed = this.state.beds[bedIdx];
        if (bed.crop) return;
        const season = this.getSeason(this.getMonth(this.state.day));
        if (!MG_CONFIG.crops[crop].season.includes(season)) { showToast('Wrong season!'); return; }
        if (this.state.money < MG_CONFIG.crops[crop].seed_cost) { showToast('Not enough money!'); return; }

        this.state.money -= MG_CONFIG.crops[crop].seed_cost;
        bed.crop = crop;
        bed.days = 0;
        bed.watered = this.state.weather.includes('Rainy');
        this.state.events.push(`🌱 Planted ${crop} in Bed ${bedIdx + 1}`);
        this.save();
        this.render();
    },

    harvestBed(bedIdx) {
        const bed = this.state.beds[bedIdx];
        if (!bed.crop) return;
        const cropData = MG_CONFIG.crops[bed.crop];
        const { bonuses, penalties } = this.getCompanionBonus(bedIdx, bed.crop);

        let yieldMult = 1.0;
        for (const b of bonuses) yieldMult *= b.data.yield_bonus;
        for (const p of penalties) yieldMult *= 0.7;

        // Rotation bonus
        if (bed.history.length > 0 && bed.history[bed.history.length - 1] !== bed.crop) {
            const lastFamily = MG_CONFIG.crops[bed.history[bed.history.length - 1]]?.family;
            if (lastFamily && MG_CONFIG.crops[bed.crop].family !== lastFamily) {
                yieldMult *= 1.1;
            }
        }

        const soilAvg = (bed.soil_N + bed.soil_P + bed.soil_K) / 3;
        if (soilAvg < 40) yieldMult *= 0.7;

        const harvestAmount = Math.max(1, Math.floor(yieldMult * (Math.random() * 2 + 1)));

        // Golden crop chance
        if (Math.random() < 0.01) {
            const goldenName = "Golden " + bed.crop;
            this.state.inventory[goldenName] = (this.state.inventory[goldenName] || 0) + 1;
            this.state.events.push(`🌟 GOLDEN ${bed.crop} FOUND! Worth 10x!`);
            if (!this.state.golden_found.includes(goldenName)) this.state.golden_found.push(goldenName);
            if (!this.state.achievements.mg_golden) {
                this.state.achievements.mg_golden = true;
                setAchievement('mg_golden');
            }
        } else {
            this.state.inventory[bed.crop] = (this.state.inventory[bed.crop] || 0) + harvestAmount;
        }

        this.state.total_harvests += 1;
        this.state.xp += 5;

        // Track harvest family for unlocks
        const family = cropData.family;
        if (!this.state.harvest_tracker[family]) this.state.harvest_tracker[family] = 0;
        this.state.harvest_tracker[family] += 1;

        bed.soil_N = Math.max(0, bed.soil_N - (cropData.nutrient_drain?.N || 0));
        bed.soil_P = Math.max(0, bed.soil_P - (cropData.nutrient_drain?.P || 0));
        bed.soil_K = Math.max(0, bed.soil_K - (cropData.nutrient_drain?.K || 0));

        bed.history.push(bed.crop);
        bed.crop = null;
        bed.days = 0;
        bed.watered = false;

        if (bonuses.length > 0) {
            this.state.companion_count += 1;
            if (!this.state.achievements.mg_companion) {
                this.state.achievements.mg_companion = true;
                setAchievement('mg_companion');
            }
        }

        if (!this.state.achievements.mg_first_harvest) {
            this.state.achievements.mg_first_harvest = true;
            setAchievement('mg_first_harvest');
        }

        showToast(`+${harvestAmount} ${bed.crop || 'crop'}`);
        this.checkMgUnlocks();
        this.save();
        this.render();
    },

    waterBed(bedIdx) {
        const bed = this.state.beds[bedIdx];
        if (!bed.crop || bed.watered) return;
        if (this.state.money < 0.50) { showToast('Not enough money!'); return; }
        this.state.money -= 0.50;
        bed.watered = true;
        this.save();
        this.render();
    },

    compostBed(bedIdx) {
        if (this.state.compost <= 0) return;
        const bed = this.state.beds[bedIdx];
        this.state.compost -= 1;
        bed.soil_N = Math.min(100, bed.soil_N + 20);
        bed.soil_P = Math.min(100, bed.soil_P + 20);
        bed.soil_K = Math.min(100, bed.soil_K + 20);
        showToast(`Composted Bed ${bedIdx + 1}! +20 NPK`);
        this.save();
        this.render();
    },

    fertiliseBed(bedIdx) {
        if (this.state.fertiliser <= 0) return;
        const bed = this.state.beds[bedIdx];
        this.state.fertiliser -= 1;
        bed.soil_N = Math.min(100, bed.soil_N + 30);
        bed.soil_P = Math.min(100, bed.soil_P + 30);
        bed.soil_K = Math.min(100, bed.soil_K + 30);
        showToast(`Fertilised Bed ${bedIdx + 1}! +30 NPK`);
        this.save();
        this.render();
    },

    sellAll(item) {
        const qty = this.state.inventory[item] || 0;
        if (qty <= 0) return;
        const cropData = MG_CONFIG && MG_CONFIG.crops[item] ? MG_CONFIG.crops[item] : { sell: 5 };
        let price = this.state.market_prices[item] || cropData.sell || 5;
        const organicBonus = this.state.organic_certified ? 1.3 : 1.0;
        const total = Math.floor(price * organicBonus) * qty;

        this.state.money += total;
        this.state.total_earned += total;
        this.state.sales_log[item] = (this.state.sales_log[item] || 0) + qty;
        this.state.xp += 2 * qty;
        delete this.state.inventory[item];

        if (this.state.total_earned >= 500 && !this.state.achievements.mg_market_master) {
            this.state.achievements.mg_market_master = true;
            setAchievement('mg_market_master');
        }

        showToast(`Sold ${qty}x ${item} for £${total}`);
        this.checkMgUnlocks();
        this.save();
        this.render();
    },

    buyCompost() {
        if (this.state.money < 3) { showToast('Need £3!'); return; }
        this.state.money -= 3;
        this.state.compost += 2;
        this.state.events.push('♻️ Made 2 compost');
        showToast('+2 Compost (-£3)');
        this.save();
        this.render();
    },

    buyFertiliser() {
        if (this.state.money < 5) { showToast('Need £5!'); return; }
        this.state.money -= 5;
        this.state.fertiliser += 1;
        showToast('+1 Fertiliser');
        this.save();
        this.render();
    },

    buyUpgrade(type) {
        if (type === 'irrigation') {
            if (this.state.money < 150) { showToast('Need £150!'); return; }
            this.state.money -= 150;
            this.state.has_irrigation = true;
            this.state.events.push('💧 Irrigation installed! All beds watered automatically.');
            showToast('💧 Irrigation installed!');
        } else if (type === 'organic') {
            if (this.state.money < 500) { showToast('Need £500!'); return; }
            this.state.money -= 500;
            this.state.organic_certified = true;
            this.state.events.push('🏷️ Organic Certified! All sales +30%');
            showToast('🏷️ Organic Certified!');
        }
        this.checkMgUnlocks();
        this.save();
        this.render();
    },

    // ── 4g. Day advance ──

    advanceDay() {
        const oldMonth = this.getMonth(this.state.day);
        const oldSeason = this.getSeason(oldMonth);

        this.state.day += 1;
        this.state.events = [];

        const newMonth = this.getMonth(this.state.day);
        const newSeason = this.getSeason(newMonth);

        // Season transition effect
        if (oldSeason !== newSeason) {
            const flash = document.createElement('div');
            flash.className = 'season-flash ' + newSeason.toLowerCase();
            document.body.appendChild(flash);
            setTimeout(() => flash.remove(), 1500);
            this.state.events.push('🌸 ' + newSeason + ' has arrived!');
        }

        // Weather
        const weatherRoll = Math.random();
        if (newSeason === "Summer") {
            this.state.weather = weatherRoll < 0.5 ? '☀️ Sunny' : (weatherRoll < 0.75 ? '⛅ Cloudy' : '🌧️ Rainy');
        } else if (newSeason === "Winter") {
            this.state.weather = weatherRoll < 0.4 ? '🌧️ Rainy' : (weatherRoll < 0.7 ? '⛅ Cloudy' : '☀️ Sunny');
        } else {
            this.state.weather = weatherRoll < 0.4 ? '☀️ Sunny' : (weatherRoll < 0.7 ? '⛅ Cloudy' : '🌧️ Rainy');
        }

        const isRaining = this.state.weather.includes('Rainy');

        // Auto-water
        if (this.state.has_irrigation) {
            for (const bed of this.state.beds) bed.watered = true;
        } else if (isRaining) {
            for (const bed of this.state.beds) bed.watered = true;
            this.state.water_saved += 0.50 * this.state.beds.filter(b => b.crop).length;
            if (this.state.water_saved >= 20 && !this.state.achievements.mg_rainwater) {
                this.state.achievements.mg_rainwater = true;
                setAchievement('mg_rainwater');
            }
        }

        // Process beds
        for (let i = 0; i < this.state.beds.length; i++) {
            const bed = this.state.beds[i];
            if (bed.crop && newSeason !== "Winter") {
                if (bed.watered || isRaining || this.state.has_irrigation) {
                    bed.days += 1;
                }
                bed.watered = false;
                // Legumes fix nitrogen
                if (MG_CONFIG.crops[bed.crop] && MG_CONFIG.crops[bed.crop].family === 'Legume') {
                    bed.soil_N = Math.min(100, bed.soil_N + 1);
                }
            } else if (!bed.crop) {
                bed.soil_N = Math.min(100, bed.soil_N + 5);
                bed.soil_P = Math.min(100, bed.soil_P + 5);
                bed.soil_K = Math.min(100, bed.soil_K + 5);
            }

            if (bed.crop && newSeason === "Winter") {
                const cropData = MG_CONFIG.crops[bed.crop];
                if (cropData && cropData.family !== "Herb") {
                    this.state.events.push('❄️ ' + bed.crop + ' in Bed ' + (i + 1) + ' killed by frost!');
                    bed.history.push(bed.crop);
                    bed.crop = null;
                    bed.days = 0;
                }
            }

            if (bed.crop) {
                const soilAvg = (bed.soil_N + bed.soil_P + bed.soil_K) / 3;
                if (soilAvg < 30) {
                    this.state.events.push('⚠️ Bed ' + (i + 1) + ' soil is poor — yields reduced!');
                }
            }
        }

        // Pest events
        if (MG_CONFIG && MG_CONFIG.pest_events && newSeason !== "Winter") {
            for (const pest of MG_CONFIG.pest_events) {
                if (pest.seasons.includes(newSeason) && Math.random() < pest.chance) {
                    this.state.events.push('🐛 ' + pest.name + ': ' + pest.desc);
                    for (let i = 0; i < this.state.beds.length; i++) {
                        const bed = this.state.beds[i];
                        if (bed.crop && MG_CONFIG.crops[bed.crop]) {
                            const family = MG_CONFIG.crops[bed.crop].family;
                            if (pest.affects.includes(family)) {
                                const { bonuses } = this.getCompanionBonus(i, bed.crop);
                                let resistant = false;
                                for (const b of bonuses) {
                                    if (pest.companions_resist && pest.companions_resist.includes(b.crop)) {
                                        resistant = true;
                                        break;
                                    }
                                }
                                if (!resistant) {
                                    bed.days = Math.max(0, bed.days - 1);
                                }
                            }
                        }
                    }
                    break;
                }
            }
        }

        // Random weather events (frost, etc.)
        if (newSeason !== "Winter" && Math.random() < 0.1) {
            const event = Math.random() < 0.5 ? "frost" : "pests";
            if (event === "frost" && newSeason === "Spring") {
                for (const bed of this.state.beds) {
                    if (bed.crop && !bed.watered && !this.state.has_irrigation) {
                        bed.days = Math.max(0, bed.days - 1);
                    }
                }
                this.state.events.push("🥶 Late frost! Unwatered crops lost a day.");
            }
        }

        // Market price fluctuations
        for (const item of Object.keys(this.state.market_prices)) {
            const base = MG_CONFIG.market_base[item] || 3;
            if ((this.state.sales_log[item] || 0) > 10) {
                this.state.market_prices[item] = Math.max(1, Math.floor(base * 0.8));
            } else {
                this.state.market_prices[item] = Math.min(
                    base + 5,
                    Math.floor(base * (0.9 + Math.random() * 0.2))
                );
            }
        }
        this.state.sales_log = {};

        // Level up
        const thresholds = { 1: 0, 2: 30, 3: 100, 4: 250, 5: 500 };
        for (const [lvl, xpNeeded] of Object.entries(thresholds).sort((a, b) => b[0] - a[0])) {
            if (this.state.xp >= xpNeeded && this.state.level < parseInt(lvl)) {
                this.state.level = parseInt(lvl);
                this.state.events.push('⭐ Level up! Now level ' + lvl + '!');
                showToast('⭐ Level Up! Level ' + lvl + '!');
                break;
            }
        }

        this.checkMgUnlocks();
        this.save();
        this.render();
    },

    // ── 4h. Reset ──

    reset() {
        if (!confirm('Delete your garden progress?')) return;
        this.state = {
            beds: null,
            day: 1,
            money: 80,
            compost: 0,
            inventory: {},
            total_earned: 0,
            level: 1,
            xp: 0,
            weather: '☀️ Sunny',
            market_prices: null,
            sales_log: {},
            events: [],
            companion_count: 0,
            rotation_count: 0,
            total_harvests: 0,
            has_polytunnel: false,
            fertiliser: 0,
            organic_certified: false,
            has_irrigation: false,
            water_saved: 0,
            golden_found: [],
            rare_found: [],
            selected_crop: "",
            unlocked_crops: MG_CONFIG ? [...(MG_CONFIG.starting_crops || ["Carrot","Lettuce","Potato","Beans","Onion","Peas"])] : ["Carrot","Lettuce","Potato","Beans","Onion","Peas"],
            harvest_tracker: {},
            achievements: {
                mg_first_harvest: false, mg_companion: false, mg_rotation: false,
                mg_market_master: false, mg_golden: false, mg_rainwater: false, mg_polytunnel: false
            }
        };
        this.state.beds = [];
        for (let i = 0; i < 12; i++) {
            this.state.beds.push({ crop: null, days: 0, soil_N: 90, soil_P: 90, soil_K: 90, history: [], watered: false });
        }
        this.state.market_prices = MG_CONFIG ? { ...MG_CONFIG.market_base } : {};
        this.save();
        this.render();
    }
};


// ════════════════════════════════════════════════
// 5. INITIALIZATION
// ════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    farmTycoon.init();
    marketGarden.init();
});
