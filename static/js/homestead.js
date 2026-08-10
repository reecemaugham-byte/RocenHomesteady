/* ═══════════════════════════════════════════════════════════
   ROCEN HOMESTEADY — HOMESTEAD GAMES
   Eco-Village Builder · The Wild Kitchen
   ═══════════════════════════════════════════════════════════

   TABLE OF CONTENTS
   ─────────────────
   1.  UTILITIES
       1a. Tab Switching
       1b. Toast Notifications
       1c. Local Storage & Master Inventory
       1d. Markdown Renderer
       1e. Shared Achievements
       1f. Config (loaded from API)
       1g. Season Icons
   2.  VILLAGE SVGS
       2a. Seasonal Palettes
       2b. Building Map & getSVG
       2c. Building SVGs (House, Well, Coop, DIY Solar, Solar Array, Reserve, Barn, Orchard, Cold Frame, Smokehouse)
       2d. Tree Variations (pine, oak, bush, treeCluster)
   3.  ECO-VILLAGE BUILDER
       3a. Defaults & State
       3b. Initialisation & Persistence
       3c. Season & Warnings
       3d. Stats (renderStats, renderParticles)
       3e. Grid & Building (renderGrid, getBuildingData, renderBuildPanel, startPlacement, cancelPlacement, buildTile, fish, repair)
       3f. Day Cycle (endDay, showDayTransition)
       3g. Foraging & Actions (forageWoods, forageMeadow, fishStream, renderActions, craft)
       3h. Market & Pantry (renderPantry, eatItem, sellItem, moveToBarn, takeFromBarn, sellFromBarn)
       3i. Village View (renderVillageView, findStreamColumn, render)
       3j. Achievements & Reset (renderAchievements, renderAchievementCard, reset)
   4.  WILD KITCHEN
       4a. Ingredient Emoji Map
       4b. Cooking Sounds
       4c. Defaults & State
       4d. Initialisation & Persistence
       4e. Inventory
       4f. Page Building & Navigation (buildPages, prevPage, nextPage, goToChapter, flipPage)
       4g. Rendering (render, renderPage, renderChapterPage, renderRecipePage, renderChapters, isCurrentChapter)
       4h. Unlocking & Cooking (submitAnswers, cook)
       4i. Animation (playCookingAnimation, stopAnimationEffects, skipAnimation, wait)
       4j. Kitchen Scene (openBook, closeBook, selectRecipeForCooking, clickCauldron, openPantry, closePantry, renderPantryPopup, renderKitchenScene)
       4k. Sidebar (renderPantry, renderProgress)
       4l. Achievements (renderAchievements, renderAchievementCard)
   5.  SUB-TAB SWITCHING
   6.  BOOTSTRAP

   ═══════════════════════════════════════════════════════════ */


/* ───────────────────────────────────────────────────────────────
   1. UTILITIES
   ─────────────────────────────────────────────────────────────── */

/* 1a. Tab Switching ─────────────────────────────────────────── */

function switchHomesteadTab(tabId) {
    document.querySelectorAll('.game-container').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`.tab-btn[data-tab="${tabId}"]`).classList.add('active');
}

/* 1b. Toast Notifications ────────────────────────────────────── */

function showToast(msg, dur = 3000) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.remove('hidden');
    setTimeout(() => t.classList.add('hidden'), dur);
}

/* 1c. Local Storage & Master Inventory ──────────────────────── */

function saveState(key, data) {
    try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) { /* quota exceeded */ }
}

function loadState(key, defaults) {
    try {
        const s = localStorage.getItem(key);
        if (s) return { ...defaults, ...JSON.parse(s) };
    } catch (e) { /* corrupt data — fall through */ }
    return { ...defaults };
}

function getMasterInventory()  { return loadState('master_inventory', {}); }
function updateMasterInventory(inv) { saveState('master_inventory', inv); }

/* 1d. Markdown Renderer ─────────────────────────────────────── */

function renderMarkdown(text) {
    if (!text) return '';
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

/* 1e. Shared Achievements ────────────────────────────────────── */

function getAchievements() { return loadState('achievements', {}); }
function setAchievement(key) {
    const a = getAchievements();
    a[key] = true;
    saveState('achievements', a);
    showToast('🏅 Achievement Unlocked!');
}

/* 1f. Config (loaded from API) ───────────────────────────────── */

let EV_CONFIG = null;
let WK_CONFIG = null;


/* ═══════════════════════════════════════════════════════════════
   2. VILLAGE SVGS — Suikoden-Style Landscape Generators
   ═══════════════════════════════════════════════════════════════ */

const VillageSVGs = {

    /* ── Seasonal Palettes ─────────────────────────────────────── */

    pal: {
        spring: {
            wall:'#C8B898', roof:'#8B7355', roofDk:'#5D4037', trunk:'#5D4037',
            leaf:'#66BB6A', leafDk:'#388E3C', flwr:'#F8BBD0', grass:'#4CAF50',
            river:'#42A5F5', rivLt:'#90CAF9', gnd:'#66BB6A', gndDk:'#388E3C',
            hill1:'#81C784', hill2:'#66BB6A', sky1:'#87CEEB', sky2:'#C8E6C9',
            moss:'#558B2F', stone:'#8D6E63'
        },
        summer: {
            wall:'#C8B898', roof:'#7B5B3A', roofDk:'#4E342E', trunk:'#4E342E',
            leaf:'#2E7D32', leafDk:'#1B5E20', flwr:'#FFD54F', grass:'#388E3C',
            river:'#1E88E5', rivLt:'#64B5F6', gnd:'#43A047', gndDk:'#2E7D32',
            hill1:'#43A047', hill2:'#2E7D32', sky1:'#4FC3F7', sky2:'#FFF9C4',
            moss:'#33691E', stone:'#795548'
        },
        autumn: {
            wall:'#B8A882', roof:'#6D4C41', roofDk:'#3E2723', trunk:'#3E2723',
            leaf:'#E65100', leafDk:'#BF360C', flwr:'#FF8F00', grass:'#A1887F',
            river:'#546E7A', rivLt:'#78909C', gnd:'#8D6E63', gndDk:'#6D4C41',
            hill1:'#A1887F', hill2:'#8D6E63', sky1:'#90A4AE', sky2:'#FFCC80',
            moss:'#5D4037', stone:'#6D4C41'
        },
        winter: {
            wall:'#B0B0B0', roof:'#CFD8DC', roofDk:'#78909C', trunk:'#6D4C41',
            leaf:'#78909C', leafDk:'#546E7A', flwr:'#ECEFF1', grass:'#CFD8DC',
            river:'#90A4AE', rivLt:'#B0BEC5', gnd:'#E0E0E0', gndDk:'#BDBDBD',
            hill1:'#BDBDBD', hill2:'#9E9E9E', sky1:'#78909C', sky2:'#B0BEC5',
            moss:'#546E7A', stone:'#9E9E9E'
        }
    },

    /* ── Building Map ──────────────────────────────────────────── */

    buildingMap: {
        'House':'house', 'Well':'well', 'Coop':'coop', 'Solar Panel':'solarPanel',
        'Wind Turbine':'windTurbine', 'Reserve':'reserve', 'Barn':'barn',
        'Orchard':'orchard', 'Cold Frame':'coldFrame', 'Smokehouse':'smokehouse',
        'Goat Pen':'goatPen', 'Greenhouse':'greenhouse'
    },


    getSVG(buildingName, season) {
        const fn = this.buildingMap[buildingName];
        return fn && this[fn] ? this[fn](season) : null;
    },

    /* ── House ─────────────────────────────────────────────────── */

    house(s) {
        const c = this.pal[s];
        const snow = s === 'winter'
            ? `<ellipse cx="40" cy="13" rx="34" ry="5" fill="#fff" opacity="0.85"/>
               <ellipse cx="26" cy="18" rx="8" ry="3" fill="#fff" opacity="0.5"/>
               <ellipse cx="56" cy="16" rx="7" ry="2.5" fill="#fff" opacity="0.5"/>`
            : '';
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="12" y="67" width="56" height="5" rx="1" fill="${c.stone}" opacity="0.6"/>
<rect x="15" y="37" width="50" height="33" rx="1" fill="${c.wall}" stroke="${c.roofDk}" stroke-width="1"/>
<line x1="15" y1="46" x2="65" y2="46.5" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.2"/>
<line x1="15" y1="54" x2="65" y2="53.5" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.2"/>
<line x1="15" y1="62" x2="65" y2="62" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.2"/>
<polygon points="6,39 40,8 74,37" fill="${c.roof}" stroke="${c.roofDk}" stroke-width="1.5"/>
<line x1="18" y1="31" x2="62" y2="29" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
<line x1="24" y1="24" x2="56" y2="22" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.25"/>
<line x1="14" y1="37" x2="66" y2="36" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
${snow}
<rect x="33" y="49" width="14" height="23" rx="1" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.8"/>
<line x1="40" y1="49" x2="40" y2="72" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.4"/>
<circle cx="44" cy="61" r="1.2" fill="#8B6914"/>
<rect x="19" y="44" width="10" height="8" rx="1" fill="#FFD54F" opacity="0.75" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="51" y="44" width="10" height="8" rx="1" fill="#FFD54F" opacity="0.75" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="16" y="44" width="3" height="8" rx="0.5" fill="${c.trunk}" opacity="0.5"/>
<rect x="29" y="44" width="3" height="8" rx="0.5" fill="${c.trunk}" opacity="0.5"/>
<rect x="48" y="44" width="3" height="8" rx="0.5" fill="${c.trunk}" opacity="0.5"/>
<rect x="61" y="44" width="3" height="8" rx="0.5" fill="${c.trunk}" opacity="0.5"/>
<rect x="55" y="10" width="7" height="22" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<circle cx="58" cy="13" r="2" fill="${c.moss}" opacity="0.35"/>
</svg>`;
    },

    /* ── Well ──────────────────────────────────────────────────── */

    well(s) {
        const c = this.pal[s];
        return `<svg viewBox="0 0 80 85" class="building-svg">
<ellipse cx="40" cy="58" rx="22" ry="12" fill="${c.stone}" stroke="${c.roofDk}" stroke-width="1.5"/>
<path d="M20,52 Q22,46 26,48 Q30,42 34,46 Q38,40 42,44 Q46,40 50,44 Q54,42 58,48 Q60,46 62,52" fill="${c.stone}" stroke="${c.roofDk}" stroke-width="0.8" opacity="0.7"/>
<ellipse cx="40" cy="54" rx="18" ry="8" fill="${c.river}" opacity="0.5" stroke="${c.roofDk}" stroke-width="0.8"/>
<rect x="20" y="30" width="5" height="28" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="55" y="30" width="5" height="28" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<line x1="23" y1="30" x2="58" y2="30" stroke="${c.trunk}" stroke-width="3.5"/>
<line x1="40" y1="30" x2="40" y2="14" stroke="${c.trunk}" stroke-width="2"/>
<line x1="38" y1="14" x2="42" y2="14" stroke="${c.trunk}" stroke-width="2.5"/>
<line x1="37" y1="28" x2="34" y2="50" stroke="${c.trunk}" stroke-width="0.8" opacity="0.6"/>
<rect x="32" y="48" width="5" height="4" rx="1" fill="${c.stone}" stroke="${c.roofDk}" stroke-width="0.5"/>
<circle cx="22" cy="56" r="2" fill="${c.moss}" opacity="0.3"/>
<circle cx="56" cy="55" r="1.5" fill="${c.moss}" opacity="0.25"/>
</svg>`;
    },

    /* ── Coop ──────────────────────────────────────────────────── */

    coop(s) {
        const c = this.pal[s];
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="22" y="40" width="36" height="28" rx="1" fill="${c.wall}" stroke="${c.roofDk}" stroke-width="1"/>
<polygon points="18,42 40,22 62,42" fill="${c.roof}" stroke="${c.roofDk}" stroke-width="1.2"/>
<line x1="24" y1="35" x2="56" y2="35" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.25"/>
<rect x="34" y="52" width="12" height="16" rx="1" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<ellipse cx="40" cy="52" rx="5" ry="4" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="8" y="66" width="64" height="3" rx="0.5" fill="${c.trunk}" opacity="0.6"/>
<line x1="8" y1="56" x2="8" y2="69" stroke="${c.trunk}" stroke-width="1.5"/>
<line x1="72" y1="56" x2="72" y2="69" stroke="${c.trunk}" stroke-width="1.5"/>
<line x1="8" y1="56" x2="72" y2="56" stroke="${c.trunk}" stroke-width="1"/>
<line x1="8" y1="60" x2="72" y2="60" stroke="${c.trunk}" stroke-width="0.4" opacity="0.35"/>
<line x1="8" y1="63" x2="72" y2="63" stroke="${c.trunk}" stroke-width="0.4" opacity="0.35"/>
<circle cx="15" cy="73" r="1" fill="${c.moss}" opacity="0.2"/>
</svg>`;
    },

    /* ── Solar Panel ───────────────────────────────────────────── */

    solarPanel(s) {
        const c = this.pal[s];
        const pClr = s === 'winter' ? '#B0BEC5' : '#1565C0';
        const frameClr = s === 'winter' ? '#78909C' : '#37474F';
        const glare = s === 'winter' ? '' : `<line x1="28" y1="32" x2="32" y2="22" stroke="#fff" stroke-width="0.6" opacity="0.4"/>
<line x1="30" y1="34" x2="33" y2="26" stroke="#fff" stroke-width="0.3" opacity="0.25"/>`;
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="12" y="60" width="4" height="16" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="64" y="60" width="4" height="16" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="10" y="55" width="60" height="4" rx="1" fill="${frameClr}" stroke="${c.roofDk}" stroke-width="0.5"/>
<polygon points="14,55 66,55 58,20 22,20" fill="${pClr}" stroke="${frameClr}" stroke-width="1.5"/>
<line x1="28" y1="52" x2="31" y2="23" stroke="${frameClr}" stroke-width="0.5" opacity="0.6"/>
<line x1="42" y1="52" x2="43" y2="22" stroke="${frameClr}" stroke-width="0.5" opacity="0.6"/>
<line x1="55" y1="52" x2="54" y2="23" stroke="${frameClr}" stroke-width="0.5" opacity="0.6"/>
<rect x="20" y="30" width="40" height="1" fill="${frameClr}" opacity="0.3"/>
<rect x="22" y="40" width="36" height="1" fill="${frameClr}" opacity="0.25"/>
${glare}
<line x1="40" y1="59" x2="40" y2="76" stroke="${c.trunk}" stroke-width="0.8" opacity="0.5"/>
<circle cx="40" cy="76" r="2" fill="${c.trunk}" opacity="0.4"/>
</svg>`;
    },


    /* ── Wind Turbine ──────────────────────────────────────────── */

    windTurbine(s) {
        const c = this.pal[s];
        const bladeClr = s === 'winter' ? '#CFD8DC' : '#E0E0E0';
        const hubClr = s === 'winter' ? '#90A4AE' : '#78909C';
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="37" y="35" width="6" height="42" rx="1" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.8"/>
<rect x="38.5" y="35" width="3" height="42" rx="0.5" fill="${c.wall}" opacity="0.3"/>
<rect x="30" y="72" width="20" height="5" rx="2" fill="${c.stone}" stroke="${c.roofDk}" stroke-width="0.5"/>
<circle cx="40" cy="32" r="4" fill="${hubClr}" stroke="${c.roofDk}" stroke-width="0.8"/>
<circle cx="40" cy="32" r="1.5" fill="${c.roofDk}" opacity="0.5"/>
<polygon points="40,32 40,8 37,10" fill="${bladeClr}" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.9"/>
<polygon points="40,32 62,44 60,41" fill="${bladeClr}" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.9"/>
<polygon points="40,32 18,44 20,41" fill="${bladeClr}" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.9"/>
<line x1="40" y1="32" x2="40" y2="10" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
<line x1="40" y1="32" x2="61" y2="42" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
<line x1="40" y1="32" x2="19" y2="42" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
</svg>`;
    },


    /* ── Goat Pen ──────────────────────────────────────────────── */

    goatPen(s) {
        const c = this.pal[s];
        const goatClr = s === 'winter' ? '#CFD8DC' : '#E0E0E0';
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="8" y="64" width="64" height="4" rx="1" fill="${c.trunk}" opacity="0.6"/>
<line x1="10" y1="40" x2="10" y2="68" stroke="${c.trunk}" stroke-width="1.5"/>
<line x1="70" y1="40" x2="70" y2="68" stroke="${c.trunk}" stroke-width="1.5"/>
<line x1="10" y1="40" x2="70" y2="40" stroke="${c.trunk}" stroke-width="1"/>
<line x1="10" y1="50" x2="70" y2="50" stroke="${c.trunk}" stroke-width="0.6" opacity="0.4"/>
<line x1="10" y1="57" x2="70" y2="57" stroke="${c.trunk}" stroke-width="0.6" opacity="0.4"/>
<rect x="38" y="48" width="14" height="20" rx="1" fill="${c.wall}" stroke="${c.roofDk}" stroke-width="0.8"/>
<line x1="45" y1="48" x2="45" y2="68" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.4"/>
<ellipse cx="24" cy="58" rx="6" ry="4" fill="${goatClr}" stroke="#9E9E9E" stroke-width="0.5"/>
<circle cx="20" cy="55" r="2.5" fill="${goatClr}" stroke="#9E9E9E" stroke-width="0.4"/>
<line x1="19" y1="52" x2="17" y2="48" stroke="#9E9E9E" stroke-width="0.6"/>
<line x1="21" y1="52" x2="23" y2="48" stroke="#9E9E9E" stroke-width="0.6"/>
<circle cx="19" cy="55" r="0.5" fill="#333"/>
<ellipse cx="58" cy="60" rx="5" ry="3.5" fill="${goatClr}" stroke="#9E9E9E" stroke-width="0.5"/>
<circle cx="55" cy="57" r="2" fill="${goatClr}" stroke="#9E9E9E" stroke-width="0.4"/>
<line x1="54" y1="55" x2="52" y2="51" stroke="#9E9E9E" stroke-width="0.5"/>
<line x1="56" y1="55" x2="57" y2="51" stroke="#9E9E9E" stroke-width="0.5"/>
<circle cx="54.5" cy="57" r="0.4" fill="#333"/>
<rect x="12" y="38" width="56" height="4" rx="1" fill="${c.roofDk}" opacity="0.15"/>
</svg>`;
    },

    /* ── Greenhouse ─────────────────────────────────────────────── */

    greenhouse(s) {
        const c = this.pal[s];
        const glassClr = s === 'winter' ? 'rgba(176,190,197,0.5)' : 'rgba(129,199,132,0.35)';
        const plantClr = s === 'winter' ? '#78909C' : c.leaf;
        const soilClr = s === 'winter' ? '#9E9E9E' : '#5D4037';
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="10" y="60" width="60" height="4" rx="1" fill="${soilClr}" opacity="0.4"/>
<rect x="12" y="40" width="56" height="24" rx="1" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="1"/>
<polygon points="8,42 40,16 72,42" fill="${glassClr}" stroke="${c.roofDk}" stroke-width="1.2"/>
<line x1="24" y1="29" x2="24" y2="42" stroke="${c.roofDk}" stroke-width="0.5" opacity="0.4"/>
<line x1="40" y1="16" x2="40" y2="42" stroke="${c.roofDk}" stroke-width="0.5" opacity="0.4"/>
<line x1="56" y1="29" x2="56" y2="42" stroke="${c.roofDk}" stroke-width="0.5" opacity="0.4"/>
<line x1="16" y1="35" x2="64" y2="35" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.3"/>
<rect x="14" y="42" width="52" height="20" fill="${soilClr}" opacity="0.2"/>
<circle cx="22" cy="56" r="1.5" fill="${plantClr}"/>
<line x1="22" y1="54" x2="22" y2="50" stroke="${plantClr}" stroke-width="0.7"/>
<circle cx="34" cy="54" r="2" fill="${plantClr}"/>
<line x1="34" y1="52" x2="34" y2="47" stroke="${plantClr}" stroke-width="0.7"/>
<circle cx="46" cy="55" r="1.5" fill="${plantClr}"/>
<line x1="46" y1="53" x2="46" y2="49" stroke="${plantClr}" stroke-width="0.7"/>
<circle cx="58" cy="54" r="1.8" fill="${plantClr}"/>
<line x1="58" y1="52" x2="58" y2="47" stroke="${plantClr}" stroke-width="0.7"/>
${s !== 'winter' ? `<circle cx="22" cy="50" r="0.8" fill="#F44336" opacity="0.6"/>
<circle cx="46" cy="49" r="0.8" fill="#FF9800" opacity="0.6"/>` : ''}
</svg>`;
    },

    /* ── Reserve ───────────────────────────────────────────────── */

    reserve(s) {
        const c = this.pal[s];
        if (s === 'winter') {
            return `<svg viewBox="0 0 80 85" class="building-svg">
<line x1="18" y1="72" x2="18" y2="35" stroke="${c.trunk}" stroke-width="2.5"/>
<line x1="18" y1="35" x2="12" y2="22" stroke="${c.trunk}" stroke-width="1.2"/>
<line x1="18" y1="40" x2="25" y2="28" stroke="${c.trunk}" stroke-width="1"/>
<line x1="40" y1="72" x2="40" y2="28" stroke="${c.trunk}" stroke-width="3"/>
<line x1="40" y1="28" x2="32" y2="16" stroke="${c.trunk}" stroke-width="1.3"/>
<line x1="40" y1="34" x2="48" y2="20" stroke="${c.trunk}" stroke-width="1.2"/>
<line x1="40" y1="22" x2="35" y2="12" stroke="${c.trunk}" stroke-width="0.8"/>
<line x1="62" y1="72" x2="62" y2="38" stroke="${c.trunk}" stroke-width="2.5"/>
<line x1="62" y1="38" x2="56" y2="26" stroke="${c.trunk}" stroke-width="1"/>
<line x1="62" y1="44" x2="68" y2="32" stroke="${c.trunk}" stroke-width="1"/>
<ellipse cx="18" cy="20" rx="6" ry="2" fill="#E0E0E0" opacity="0.4"/>
<ellipse cx="40" cy="14" rx="8" ry="2" fill="#E0E0E0" opacity="0.3"/>
<ellipse cx="62" cy="24" rx="6" ry="2" fill="#E0E0E0" opacity="0.35"/>
</svg>`;
        }
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="16" y="50" width="4" height="22" fill="${c.trunk}"/>
<polygon points="18,70 6,42 18,20 30,42" fill="${c.leafDk}" stroke="${c.trunk}" stroke-width="0.3"/>
<polygon points="18,55 10,38 18,28 26,38" fill="${c.leaf}" opacity="0.7"/>
<rect x="38" y="48" width="4" height="24" fill="${c.trunk}"/>
<circle cx="40" cy="28" r="16" fill="${c.leaf}" stroke="${c.leafDk}" stroke-width="0.5"/>
<circle cx="32" cy="22" r="9" fill="${c.leafDk}" opacity="0.65"/>
<circle cx="48" cy="24" r="8" fill="${c.leaf}" opacity="0.6"/>
<rect x="60" y="52" width="4" height="20" fill="${c.trunk}"/>
<polygon points="62,70 52,44 62,26 72,44" fill="${c.leafDk}" stroke="${c.trunk}" stroke-width="0.3"/>
<polygon points="62,55 54,40 62,32 70,40" fill="${c.leaf}" opacity="0.7"/>
<ellipse cx="20" cy="73" rx="6" ry="3" fill="${c.gndDk}" opacity="0.3"/>
<ellipse cx="40" cy="74" rx="7" ry="3" fill="${c.gndDk}" opacity="0.3"/>
<ellipse cx="62" cy="73" rx="5" ry="3" fill="${c.gndDk}" opacity="0.3"/>
</svg>`;
    },

    /* ── Barn ──────────────────────────────────────────────────── */

    barn(s) {
        const c = this.pal[s];
        const barnWall = s === 'winter' ? '#B0B0B0' : '#8B4513';
        const barnAccent = s === 'winter' ? '#90A4AE' : '#6D3A1F';
        const barnDoor = s === 'winter' ? '#78909C' : '#5D2E0F';
        const snow = s === 'winter'
            ? `<ellipse cx="40" cy="14" rx="36" ry="5" fill="#fff" opacity="0.8"/>
               <ellipse cx="68" cy="49" rx="7" ry="2" fill="#fff" opacity="0.4"/>`
            : '';
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="5" y="68" width="70" height="4" rx="1" fill="${c.stone}" opacity="0.5"/>
<rect x="5" y="37" width="70" height="34" rx="1" fill="${barnWall}" stroke="${barnAccent}" stroke-width="1.2"/>
<line x1="20" y1="37" x2="20" y2="71" stroke="${barnAccent}" stroke-width="0.4" opacity="0.25"/>
<line x1="40" y1="37" x2="40" y2="71" stroke="${barnAccent}" stroke-width="0.4" opacity="0.15"/>
<line x1="60" y1="37" x2="60" y2="71" stroke="${barnAccent}" stroke-width="0.4" opacity="0.25"/>
<polygon points="0,39 40,10 80,39" fill="${c.roof}" stroke="${c.roofDk}" stroke-width="1.5"/>
<line x1="15" y1="30" x2="65" y2="28" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
${snow}
<rect x="8" y="44" width="9" height="8" rx="1" fill="#FFD54F" opacity="0.7" stroke="${barnAccent}" stroke-width="0.5"/>
<line x1="8" y1="48" x2="17" y2="48" stroke="${barnAccent}" stroke-width="0.3" opacity="0.5"/>
<line x1="12.5" y1="44" x2="12.5" y2="52" stroke="${barnAccent}" stroke-width="0.3" opacity="0.5"/>
<rect x="63" y="44" width="9" height="8" rx="1" fill="#FFD54F" opacity="0.7" stroke="${barnAccent}" stroke-width="0.5"/>
<line x1="63" y1="48" x2="72" y2="48" stroke="${barnAccent}" stroke-width="0.3" opacity="0.5"/>
<line x1="67.5" y1="44" x2="67.5" y2="52" stroke="${barnAccent}" stroke-width="0.3" opacity="0.5"/>
<rect x="22" y="50" width="36" height="24" rx="1" fill="${barnDoor}" stroke="${barnAccent}" stroke-width="1"/>
<line x1="40" y1="50" x2="40" y2="74" stroke="${barnAccent}" stroke-width="0.6" opacity="0.6"/>
<line x1="22" y1="62" x2="58" y2="62" stroke="${barnAccent}" stroke-width="0.5" opacity="0.5"/>
<circle cx="36" cy="62" r="1.2" fill="#8B6914"/>
<circle cx="44" cy="62" r="1.2" fill="#8B6914"/>
<rect x="24" y="52" width="14" height="8" rx="0.5" fill="#FFD54F" opacity="0.5" stroke="${barnAccent}" stroke-width="0.3"/>
<rect x="42" y="52" width="14" height="8" rx="0.5" fill="#FFD54F" opacity="0.5" stroke="${barnAccent}" stroke-width="0.3"/>
</svg>`;
    },


    /* ── Orchard ───────────────────────────────────────────────── */

    orchard(s) {
        const c = this.pal[s];
        const fruitClr = s === 'spring' ? '#F8BBD0' : s === 'summer' ? '#FFD54F' : s === 'autumn' ? '#FF6D00' : 'none';

        if (s === 'winter') {
            return `<svg viewBox="0 0 80 85" class="building-svg">
<line x1="15" y1="72" x2="15" y2="35" stroke="${c.trunk}" stroke-width="2.5"/>
<line x1="15" y1="35" x2="10" y2="24" stroke="${c.trunk}" stroke-width="1"/>
<line x1="15" y1="40" x2="21" y2="30" stroke="${c.trunk}" stroke-width="1"/>
<line x1="40" y1="72" x2="40" y2="28" stroke="${c.trunk}" stroke-width="3"/>
<line x1="40" y1="28" x2="33" y2="16" stroke="${c.trunk}" stroke-width="1.2"/>
<line x1="40" y1="34" x2="47" y2="22" stroke="${c.trunk}" stroke-width="1.2"/>
<line x1="65" y1="72" x2="65" y2="38" stroke="${c.trunk}" stroke-width="2.5"/>
<line x1="65" y1="38" x2="59" y2="27" stroke="${c.trunk}" stroke-width="1"/>
<line x1="65" y1="42" x2="71" y2="33" stroke="${c.trunk}" stroke-width="1"/>
</svg>`;
        }

        let trees = `<rect x="13" y="50" width="4" height="22" fill="${c.trunk}"/>
<ellipse cx="15" cy="33" rx="12" ry="14" fill="${c.leaf}" stroke="${c.leafDk}" stroke-width="0.4"/>
<ellipse cx="10" cy="28" rx="7" ry="8" fill="${c.leafDk}" opacity="0.6"/>
<rect x="38" y="46" width="4" height="26" fill="${c.trunk}"/>
<ellipse cx="40" cy="25" rx="15" ry="16" fill="${c.leaf}" stroke="${c.leafDk}" stroke-width="0.4"/>
<ellipse cx="33" cy="20" rx="9" ry="10" fill="${c.leafDk}" opacity="0.55"/>
<ellipse cx="47" cy="22" rx="8" ry="9" fill="${c.leaf}" opacity="0.6"/>
<rect x="63" y="52" width="4" height="20" fill="${c.trunk}"/>
<ellipse cx="65" cy="37" rx="11" ry="13" fill="${c.leaf}" stroke="${c.leafDk}" stroke-width="0.4"/>
<ellipse cx="60" cy="33" rx="7" ry="8" fill="${c.leafDk}" opacity="0.55"/>`;

        if (fruitClr !== 'none') {
            trees += `<circle cx="10" cy="36" r="1.8" fill="${fruitClr}"/>
<circle cx="18" cy="30" r="1.5" fill="${fruitClr}"/>
<circle cx="34" cy="22" r="2" fill="${fruitClr}"/>
<circle cx="44" cy="28" r="1.5" fill="${fruitClr}"/>
<circle cx="60" cy="40" r="1.8" fill="${fruitClr}"/>
<circle cx="68" cy="34" r="1.5" fill="${fruitClr}"/>`;
        }

        return `<svg viewBox="0 0 80 85" class="building-svg">${trees}</svg>`;
    },

    /* ── Cold Frame ────────────────────────────────────────────── */

    coldFrame(s) {
        const c = this.pal[s];
        const seedling = s === 'winter' ? '' :
            `<circle cx="25" cy="54" r="1.8" fill="${c.leaf}"/><line x1="25" y1="56" x2="25" y2="60" stroke="${c.leafDk}" stroke-width="0.7"/>
             <circle cx="40" cy="52" r="2.2" fill="${c.leaf}"/><line x1="40" y1="54" x2="40" y2="60" stroke="${c.leafDk}" stroke-width="0.7"/>
             <circle cx="55" cy="55" r="1.8" fill="${c.leaf}"/><line x1="55" y1="57" x2="55" y2="60" stroke="${c.leafDk}" stroke-width="0.7"/>`;
        const snowFrame = s === 'winter' ? `<ellipse cx="40" cy="30" rx="30" ry="4" fill="#fff" opacity="0.5"/>` : '';
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="8" y="62" width="64" height="5" rx="1" fill="${c.gndDk}" opacity="0.3"/>
<rect x="10" y="48" width="60" height="16" rx="1" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="1"/>
<line x1="30" y1="48" x2="30" y2="64" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
<line x1="50" y1="48" x2="50" y2="64" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
<polygon points="10,48 40,28 70,48" fill="#B3E5FC" opacity="0.4" stroke="${c.roofDk}" stroke-width="1"/>
<line x1="25" y1="38" x2="25" y2="48" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.4"/>
<line x1="40" y1="28" x2="40" y2="48" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.4"/>
<line x1="55" y1="38" x2="55" y2="48" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.4"/>
${seedling}${snowFrame}
</svg>`;
    },

    /* ── Smokehouse ───────────────────────────────────────────── */

    smokehouse(s) {
        const c = this.pal[s];
        return `<svg viewBox="0 0 80 85" class="building-svg">
<rect x="15" y="40" width="50" height="30" rx="1" fill="${c.wall}" stroke="${c.roofDk}" stroke-width="1.2"/>
<line x1="30" y1="40" x2="30" y2="70" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.15"/>
<line x1="50" y1="40" x2="50" y2="70" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.15"/>
<polygon points="10,42 40,18 70,42" fill="${c.roof}" stroke="${c.roofDk}" stroke-width="1.5"/>
<line x1="20" y1="34" x2="60" y2="32" stroke="${c.roofDk}" stroke-width="0.3" opacity="0.3"/>
<rect x="30" y="52" width="20" height="18" rx="1" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.8"/>
<line x1="40" y1="52" x2="40" y2="70" stroke="${c.roofDk}" stroke-width="0.4" opacity="0.4"/>
<rect x="55" y="20" width="6" height="18" fill="${c.trunk}" stroke="${c.roofDk}" stroke-width="0.5"/>
<rect x="56" y="22" width="4" height="10" fill="${c.wall}" opacity="0.3"/>
<ellipse cx="58" cy="17" rx="5" ry="3" fill="rgba(200,200,200,0.2)"/>
<ellipse cx="60" cy="13" rx="4" ry="2.5" fill="rgba(200,200,200,0.15)"/>
<ellipse cx="56" cy="10" rx="3" ry="2" fill="rgba(200,200,200,0.1)"/>
<rect x="34" y="55" width="3" height="2" rx="0.5" fill="${c.roofDk}" opacity="0.3"/>
<rect x="42" y="55" width="3" height="2" rx="0.5" fill="${c.roofDk}" opacity="0.3"/>
</svg>`;
    },

    /* ── Tree Variations ───────────────────────────────────────── */

    pine(s) {
        const c = this.pal[s];
        if (s === 'winter') {
            return `<svg viewBox="0 0 30 50" class="tree-svg"><line x1="15" y1="48" x2="15" y2="22" stroke="${c.trunk}" stroke-width="2.5"/>
<line x1="15" y1="22" x2="10" y2="12" stroke="${c.trunk}" stroke-width="1.2"/>
<line x1="15" y1="28" x2="21" y2="18" stroke="${c.trunk}" stroke-width="1"/>
<ellipse cx="15" cy="10" rx="5" ry="2" fill="#E0E0E0" opacity="0.4"/></svg>`;
        }
        return `<svg viewBox="0 0 30 50" class="tree-svg"><rect x="13" y="36" width="4" height="14" fill="${c.trunk}"/>
<polygon points="15,6 4,28 26,28" fill="${c.leafDk}" stroke="${c.trunk}" stroke-width="0.3"/>
<polygon points="15,16 7,32 23,32" fill="${c.leaf}" stroke="${c.trunk}" stroke-width="0.3"/></svg>`;
    },

    oak(s) {
        const c = this.pal[s];
        if (s === 'winter') {
            return `<svg viewBox="0 0 35 50" class="tree-svg"><line x1="17" y1="48" x2="17" y2="22" stroke="${c.trunk}" stroke-width="3"/>
<line x1="17" y1="22" x2="9" y2="12" stroke="${c.trunk}" stroke-width="1.3"/>
<line x1="17" y1="28" x2="26" y2="16" stroke="${c.trunk}" stroke-width="1.2"/>
<line x1="17" y1="18" x2="12" y2="8" stroke="${c.trunk}" stroke-width="0.8"/></svg>`;
        }
        return `<svg viewBox="0 0 35 50" class="tree-svg"><rect x="15" y="34" width="5" height="16" fill="${c.trunk}"/>
<circle cx="17" cy="22" r="12" fill="${c.leaf}" stroke="${c.leafDk}" stroke-width="0.5"/>
<circle cx="10" cy="18" r="7" fill="${c.leafDk}" opacity="0.6"/>
<circle cx="23" cy="20" r="6" fill="${c.leaf}" opacity="0.7"/></svg>`;
    },

    bush(s) {
        const c = this.pal[s];
        if (s === 'winter') {
            return `<svg viewBox="0 0 25 25" class="tree-svg"><ellipse cx="12" cy="16" rx="9" ry="6" fill="${c.leafDk}" opacity="0.4"/>
<line x1="8" y1="22" x2="8" y2="16" stroke="${c.trunk}" stroke-width="1"/>
<line x1="16" y1="22" x2="16" y2="17" stroke="${c.trunk}" stroke-width="1"/></svg>`;
        }
        const flwr = s === 'spring'
            ? `<circle cx="8" cy="9" r="1.5" fill="${c.flwr}"/><circle cx="16" cy="7" r="1.3" fill="${c.flwr}"/><circle cx="20" cy="13" r="1" fill="${c.flwr}" opacity="0.7"/>`
            : '';
        return `<svg viewBox="0 0 25 25" class="tree-svg"><ellipse cx="12" cy="15" rx="10" ry="8" fill="${c.leaf}" stroke="${c.leafDk}" stroke-width="0.3"/>
<ellipse cx="8" cy="13" rx="6" ry="5" fill="${c.leafDk}" opacity="0.55"/>${flwr}</svg>`;
    },

    treeCluster(s, seed) {
        const types = ['pine', 'oak', 'bush'];
        const count = 2 + (seed % 2);
        let html = '<div class="vl-tree-cluster">';
        for (let i = 0; i < count; i++) {
            const type = types[(seed + i) % 3];
            html += this[type](s);
        }
        html += '</div>';
        return html;
    }
};

/* ═══════════════════════════════════════════════════════════════
   3. ECO-VILLAGE BUILDER
   ═══════════════════════════════════════════════════════════════ */

/* 3a. Defaults & State ───────────────────────────────────────── */

const ecoVillage = {

    defaults: {
        grid: null,
        stats: {
            Food: 50, Water: 50, Power: 0, Stamina: 100, Money: 100,
            Max_Power: 20, Storage_Limit: 10, Barn_Capacity: 0
        },
        inventory: {},
        villageStorage: {},
        ownedBuildings: {},
        placingMode: null,
        day: 1,
        season: 'Spring',
        weather: 'Sunny',
        natureHealth: 100,
        damagedBuildings: [],
        achievements: {
            eco_survivor: false, eco_wealth: false, eco_builder: false,
            eco_self_sufficient: false, eco_nature: false, eco_winter_ok: false,
            eco_master: false, eco_full_village: false, eco_green_thumb: false,
            eco_master_chef: false
        }
    },


    state: null,
    _lastPlacedTile: null,

/* 3b. Initialisation & Persistence ────────────────────────────── */

    init() {
        this.state = loadState('ev_state', this.defaults);

        if (!this.state.grid) {
            this.state.grid = this.createGrid();
        }

        // Migrations — ensure newer fields exist on older saves
        if (!this.state.stats.Storage_Limit) this.state.stats.Storage_Limit = 10;
        if (!this.state.stats.Max_Power)   this.state.stats.Max_Power = 20;
        if (!this.state.villageStorage)    this.state.villageStorage = {};
        if (!this.state.stats.Barn_Capacity) this.state.stats.Barn_Capacity = 0;
        if (!this.state.weather)          this.state.weather = 'Sunny';
        if (!this.state.achievements) {
            this.state.achievements = { eco_survivor: false, eco_wealth: false };
        }
        // Add new achievements to existing saves
        const newAch = {
            eco_builder: false, eco_self_sufficient: false, eco_nature: false,
            eco_winter_ok: false, eco_master: false, eco_full_village: false,
            eco_green_thumb: false, eco_master_chef: false
        };
        for (const [k, v] of Object.entries(newAch)) {
            if (this.state.achievements[k] === undefined) this.state.achievements[k] = v;
        }


        // Load config then render
        fetch('/api/games/eco-village/config')
            .then(r => r.json())
            .then(cfg => {
                EV_CONFIG = cfg;
                this.save();
                this.render();
            });
    },

    createGrid() {
        const grid = [];
        const streamCol = Math.floor(Math.random() * 4) + 1;
        for (let r = 0; r < 4; r++) {
            const row = [];
            for (let c = 0; c < 6; c++) {
                row.push(c === streamCol ? '🌊' : '🌲');
            }
            grid.push(row);
        }
        return grid;
    },

    save() {
        saveState('ev_state', this.state);
    },

/* 3c. Season & Warnings ──────────────────────────────────────── */

    applySeasonTheme() {
        const section = document.getElementById('eco-village');
        if (!section) return;
        section.classList.remove('season-spring', 'season-summer', 'season-autumn', 'season-winter');
        section.classList.add('season-' + this.state.season.toLowerCase());
    },

    renderSeason() {
        const icon = HS_ICONS[this.state.season] || '🌸';
        const woodInfo = this.getWinterWoodInfo();
        const wInfo = this.getWeatherInfo(this.state.weather);
        document.getElementById('ev-season-bar').innerHTML = `
            <div class="season-bar">${icon} ${this.state.season} — Day ${this.state.day} <span class="weather-badge ${wInfo.cls}">${wInfo.icon} ${wInfo.label}</span>${woodInfo}</div>
        `;
    },


    /** Helper — computes winter wood info string for the season bar. */
    getWinterWoodInfo() {
        if (this.state.season !== 'Winter') return '';

        const undamaged = this.getUndamagedHouses();
        const woodNeeded = undamaged.length;
        const woodHave = this.state.inventory['Wood'] || 0;

        if (woodNeeded <= 0) return '';

        const woodColour = woodHave >= woodNeeded ? '#4CAF50'
                          : woodHave > 0 ? '#FF9800' : '#f44336';
        return ` <span style="color:${woodColour};">| 🪵 ${woodHave}/${woodNeeded} Wood/day</span>`;
    },

    renderWarning() {
        const el = document.getElementById('ev-warning');
        const undamaged = this.getUndamagedHouses();
        const woodNeeded = undamaged.length;
        const woodHave = this.state.inventory['Wood'] || 0;
        const hasColdFrame = this.state.grid.some(row => row.includes('🫧'));

        // Weather alerts
        let weatherHtml = '';
        if (this.state.weather === 'Stormy') {
            weatherHtml = `<div class="warning-box" style="border-color: #9C27B0; background: rgba(156, 39, 176, 0.1);">
                <span style="color: #CE93D8; font-weight: 600;">⛈️ STORM WARNING:</span>
                <span style="color: var(--cream-dim);"> Solar Panels and Wind Turbines offline today! Buildings have higher damage risk.</span>
            </div>`;
        } else if (this.state.weather === 'Drought') {
            weatherHtml = `<div class="warning-box" style="border-color: #FF5722; background: rgba(255, 87, 34, 0.1);">
                <span style="color: #FF8A65; font-weight: 600;">🏜️ DROUGHT:</span>
                <span style="color: var(--cream-dim);"> Wells produce less water. Foraging yields reduced. Cold Frame output halved.</span>
            </div>`;
        } else if (this.state.weather === 'Cold Snap' && this.state.season === 'Winter') {
            weatherHtml = `<div class="warning-box winter-danger">
                <span style="color: #81D4FA; font-weight: 600;">🥶 COLD SNAP:</span>
                <span style="color: var(--cream-dim);"> Each house needs 2 Wood/day for heating!</span>
            </div>`;
        }

        if (this.state.season === 'Autumn') {

            const totalWoodNeeded = woodNeeded * 10;
            let msg = `<span style="color: var(--amber); font-weight: 600;">🍂 AUTUMN WARNING:</span> `
                + `<span style="color: var(--cream-dim);">Winter is coming! Stockpile food and wood!`;
            if (woodNeeded > 0) {
                msg += ` Each House needs 1 Wood/day in Winter (${woodNeeded} Wood/day, ${totalWoodNeeded} total).`;
            }
            msg += `</span>`;
            el.innerHTML = `<div class="warning-box autumn">${msg}</div>`;
        } else if (this.state.season === 'Winter') {
            let html = '';
            if (woodNeeded > 0 && woodHave < woodNeeded) {
                html = `<div class="warning-box winter-danger">`
                    + `<span style="color: var(--danger); font-weight: 600;">❄️ FROST WARNING:</span> `
                    + `<span style="color: var(--cream-dim);">Need ${woodNeeded} Wood/day for heating. `
                    + `Have ${woodHave}. Unheated homes take damage every 2 days!</span></div>`;
            } else if (woodNeeded > 0) {
                html = `<div class="warning-box winter-safe">`
                    + `<span style="color: #4CAF50; font-weight: 600;">🔥 HEATING:</span> `
                    + `<span style="color: var(--cream-dim);">Using ${woodNeeded} Wood/day for ${undamaged.length} home(s). `
                    + `${woodHave - woodNeeded} Wood remaining.</span></div>`;
            } else {
                html = `<div class="warning-box winter-safe">`
                    + `<span style="color: #2196F3; font-weight: 600;">❄️ WINTER:</span> `
                    + `<span style="color: var(--cream-dim);">No homes to heat. Build a House to shelter from the cold!</span></div>`;
            }
            if (hasColdFrame && !html.includes('winter-safe')) {
                html += `<div class="warning-box winter-safe" style="margin-top: 0.5rem;">`
                    + `<span style="color: #2196F3; font-weight: 600;">🫧</span> `
                    + `<span style="color: var(--cream-dim);">Cold Frame producing +3 Food/day!</span></div>`;
            }
            el.innerHTML = html;
        } else {
            el.innerHTML = weatherHtml;
        }
    },


    /** Determine weather based on season. */
    determineWeather(season) {
        const weatherChances = {
            'Spring':  { 'Sunny': 0.40, 'Rainy': 0.30, 'Stormy': 0.10, 'Windy': 0.20 },
            'Summer':   { 'Sunny': 0.50, 'Rainy': 0.20, 'Stormy': 0.05, 'Drought': 0.15, 'Windy': 0.10 },
            'Autumn':   { 'Sunny': 0.25, 'Rainy': 0.35, 'Stormy': 0.15, 'Windy': 0.25 },
            'Winter':   { 'Sunny': 0.20, 'Rainy': 0.10, 'Stormy': 0.10, 'Cold Snap': 0.25, 'Snowy': 0.35 }
        };
        const chances = weatherChances[season] || weatherChances['Spring'];
        const roll = Math.random();
        let cumulative = 0;
        for (const [weather, chance] of Object.entries(chances)) {
            cumulative += chance;
            if (roll < cumulative) return weather;
        }
        return 'Sunny';
    },

    /** Get weather icon and class. */
    getWeatherInfo(weather) {
        const info = {
            'Sunny':     { icon: '☀️',  cls: 'weather-sunny',     label: 'Sunny' },
            'Rainy':     { icon: '🌧️', cls: 'weather-rainy',     label: 'Rainy' },
            'Stormy':    { icon: '⛈️', cls: 'weather-stormy',    label: 'Stormy' },
            'Drought':   { icon: '🏜️', cls: 'weather-drought',   label: 'Drought' },
            'Cold Snap': { icon: '🥶', cls: 'weather-cold-snap', label: 'Cold Snap' },
            'Snowy':     { icon: '🌨️', cls: 'weather-snowy',     label: 'Snowy' },
            'Windy':     { icon: '💨', cls: 'weather-windy',     label: 'Windy' }
        };
        return info[weather] || info['Sunny'];
    },

    /** Helper — finds all undamaged house tiles on the grid. */
    getUndamagedHouses() {
        const houses = [];
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                if (this.state.grid[r][c] === '🏠'
                    && !this.state.damagedBuildings.some(d => d[0] === r && d[1] === c)) {
                    houses.push([r, c]);
                }
            }
        }
        return houses;
    },

/* 3d. Stats ───────────────────────────────────────────────────── */

    renderStats() {
        const s = this.state.stats;
        const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
        const barnUsed = Object.values(this.state.villageStorage).reduce((a, b) => a + b, 0);
        const barnPct    = s.Barn_Capacity > 0 ? Math.min(100, (barnUsed / s.Barn_Capacity) * 100) : 0;
        const staminaPct = Math.min(100, Math.max(0, s.Stamina));
        const powerPct   = s.Max_Power > 0 ? Math.min(100, (s.Power / s.Max_Power) * 100) : 0;
        const naturePct  = Math.min(100, Math.max(0, this.state.natureHealth));
        const storagePct = s.Storage_Limit > 0 ? Math.min(100, (currentStorage / s.Storage_Limit) * 100) : 0;

        const foodColour    = s.Food > 10 ? '#FF8F00' : s.Food > 5 ? '#FF6D00' : '#f44336';
        const waterColour   = s.Water > 10 ? '#2196F3' : s.Water > 5 ? '#FF9800' : '#f44336';
        const staminaColour = staminaPct > 50 ? '#AB47BC' : staminaPct > 25 ? '#FF9800' : '#f44336';
        const natureColour  = naturePct > 50 ? '#4CAF50' : naturePct > 25 ? '#FF9800' : '#f44336';
        const storageColour = storagePct > 80 ? '#f44336' : storagePct > 50 ? '#FF9800' : '#4CAF50';

        let html = `
            <div class="stat-box food"><div class="stat-label">🍖 Food</div><div class="stat-value">${s.Food}</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${Math.min(100, s.Food * 2)}%;background:${foodColour};"></div></div></div>
            <div class="stat-box water"><div class="stat-label">💧 Water</div><div class="stat-value">${s.Water}</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${Math.min(100, s.Water * 2)}%;background:${waterColour};"></div></div></div>
            <div class="stat-box stamina"><div class="stat-label">⚡ Stamina</div><div class="stat-value">${s.Stamina}</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${staminaPct}%;background:${staminaColour};"></div></div></div>
            <div class="stat-box power"><div class="stat-label">🔌 Power</div><div class="stat-value">${s.Power}/${s.Max_Power}</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${powerPct}%;background:#FFC107;"></div></div></div>
            <div class="stat-box money"><div class="stat-label">💰 Money</div><div class="stat-value">£${s.Money}</div></div>
            <div class="stat-box nature"><div class="stat-label">🌿 Nature</div><div class="stat-value">${this.state.natureHealth}%</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${naturePct}%;background:${natureColour};"></div></div></div>
            <div class="stat-box storage"><div class="stat-label">📦 Storage</div><div class="stat-value">${currentStorage}/${s.Storage_Limit}</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${storagePct}%;background:${storageColour};"></div></div></div>
        `;

        if (s.Barn_Capacity > 0) {
            html += `<div class="stat-box barn"><div class="stat-label">🏗️ Barn</div><div class="stat-value">${barnUsed}/${s.Barn_Capacity}</div><div class="stat-bar"><div class="stat-bar-fill" style="width:${barnPct}%;background:#8B6914;"></div></div></div>`;
        }

        document.getElementById('ev-stats').innerHTML = html;
    },

    renderParticles() {
        const container = document.getElementById('ev-particles');
        if (!container) return;

        const season = this.state.season;
        let html = '';

        if (season === 'Spring') {
            const petals = ['🌸', '🌺', '🌷', '💮'];
            for (let i = 0; i < 12; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 15;
                const duration = 10 + Math.random() * 10;
                const petal = petals[Math.floor(Math.random() * petals.length)];
                html += `<div class="petal-particle" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;">${petal}</div>`;
            }
        } else if (season === 'Summer') {
            for (let i = 0; i < 6; i++) {
                const left = Math.random() * 100;
                const top = Math.random() * 80;
                const delay = Math.random() * 8;
                const duration = 4 + Math.random() * 4;
                html += `<div class="firefly-particle" style="left:${left}%;top:${top}%;animation-delay:${delay}s;animation-duration:${duration}s;"></div>`;
            }
        } else if (season === 'Autumn') {
            const leaves = ['🍂', '🍁', '🍃'];
            for (let i = 0; i < 8; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 12;
                const duration = 8 + Math.random() * 8;
                const leaf = leaves[Math.floor(Math.random() * leaves.length)];
                html += `<div class="leaf-particle" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;">${leaf}</div>`;
            }
        } else if (season === 'Winter') {
            for (let i = 0; i < 15; i++) {
                const left = Math.random() * 100;
                const delay = Math.random() * 10;
                const duration = 6 + Math.random() * 8;
                html += `<div class="snowflake-particle" style="left:${left}%;animation-delay:${delay}s;animation-duration:${duration}s;">❄</div>`;
            }
        }

        container.innerHTML = html;
    },

/* 3e. Grid & Building ─────────────────────────────────────────── */

    renderGrid() {
        const container = document.getElementById('ev-grid');

        const tileStyles = {
            '🌲': { label: 'Empty',         bg: '#1a2e1a', border: '#3d5a3d', text: 'var(--cream-dim)' },
            '🌊': { label: 'Stream',         bg: '#0a1a2e', border: '#2196F3', text: '#90CAF9' },
            '🏠': { label: 'House',          bg: '#1a2a1a', border: '#8D6E63', text: '#BCAAA4' },
            '🪨': { label: 'Well',           bg: '#1a2a1a', border: '#8D6E63', text: '#BCAAA4' },
            '🐔': { label: 'Chickens',       bg: '#1a2a1a', border: '#FF9800', text: '#FFB74D' },
            '🔆': { label: 'Solar Panel',    bg: '#2a2a00', border: '#FFC107', text: '#FFD54F' },
            '💨': { label: 'Wind Turbine',   bg: '#1a2a2a', border: '#78909C', text: '#B0BEC5' },
            '🌳': { label: 'Reserve',        bg: '#0a2a0a', border: '#2E7D32', text: '#66BB6A' },
            '🌴': { label: 'Orchard',        bg: '#0a2a0a', border: '#4CAF50', text: '#81C784' },
            '🫧': { label: 'Cold Frame',     bg: '#0a2a2a', border: '#26C6DA', text: '#80DEEA' },
            '🥓': { label: 'Smokehouse',    bg: '#1a1a0a', border: '#8D6E63', text: '#BCAAA4' },
            '🏡': { label: 'Barn',           bg: '#1a2a1a', border: '#8D6E63', text: '#BCAAA4' },
            '🐐': { label: 'Goat Pen',       bg: '#1a2a1a', border: '#8D6E63', text: '#BCAAA4' },
            '🌱': { label: 'Greenhouse',     bg: '#0a2a1a', border: '#66BB6A', text: '#A5D6A7' },
        };


        // Add dynamic building styles from config
        if (EV_CONFIG && EV_CONFIG.buildings) {
            for (const [bname, bdata] of Object.entries(EV_CONFIG.buildings)) {
                if (!tileStyles[bdata.icon]) {
                    tileStyles[bdata.icon] = {
                        label: bname, bg: '#1a2e1a', border: '#4CAF50', text: 'var(--cream)'
                    };
                }
            }
        }

        // Placing banner
        const placingBanner = document.getElementById('ev-placing-banner');
        if (this.state.placingMode) {
            const bdata = EV_CONFIG.buildings[this.state.placingMode];
            placingBanner.classList.remove('hidden');
            placingBanner.innerHTML = `
                <span style="color: var(--amber); font-weight: 700;">📍 Placing Mode:</span>
                <span style="color: var(--cream-dim);"> Click a <span style="color: var(--green-leaf);">🌲 Empty</span> tile to build <b>${bdata.icon} ${this.state.placingMode}</b>.</span>
                <button class="btn-secondary" style="margin-left: 1rem;" onclick="ecoVillage.cancelPlacement()">❌ Cancel</button>
            `;
        } else {
            placingBanner.classList.add('hidden');
        }

        let html = '';
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                const tile = this.state.grid[r][c];
                const isDamaged = this.state.damagedBuildings.some(d => d[0] === r && d[1] === c);
                const style = tileStyles[tile] || { label: 'Building', bg: '#1a2e1a', border: '#4CAF50', text: 'var(--cream)' };
                const isPlacing = this.state.placingMode && tile === '🌲';

                let tileClass = 'tile';
                if (tile === '🌊') tileClass += ' stream';
                else if (tile === '🌲') tileClass += ' empty';
                if (isDamaged) tileClass += ' damaged';

                const damageBadge = isDamaged ? '<div class="tile-damaged">DAMAGED</div>' : '';

                // Action button
                let actionHtml = '';
                if (isPlacing) {
                    const bdata = EV_CONFIG.buildings[this.state.placingMode];
                    actionHtml = `<button class="tile-action build" onclick="ecoVillage.buildTile(${r},${c})">Build £${bdata.cost}</button>`;
                } else if (tile === '🌊') {
                    const disabled = this.state.season === 'Winter' ? ' disabled' : '';
                    actionHtml = `<button class="tile-action"${disabled} onclick="ecoVillage.fish(${r},${c})">🎣 Fish</button>`;
                } else if (isDamaged) {
                    const bdata = this.getBuildingData(tile);
                    const repairCost = bdata ? bdata.repair : 10;
                    actionHtml = `<button class="tile-action damaged" onclick="ecoVillage.repair(${r},${c})">🛠️ £${repairCost}</button>`;
                } else if (tile !== '🌲' && tile !== '🌊') {
                    actionHtml = `<button class="tile-action" disabled>—</button>`;
                } else {
                    actionHtml = `<button class="tile-action" disabled>—</button>`;
                }

                const popClass = this._lastPlacedTile === `${r},${c}` ? ' pop-in' : '';
                html += `
                    <div class="${tileClass}${popClass}" style="background: ${isDamaged ? 'linear-gradient(135deg, #2a0a0a, #1a0000)' : style.bg}; border: ${isDamaged ? '2px dashed var(--danger)' : `2px solid ${style.border}`};">
                        <div class="tile-season-overlay"></div>
                        <div class="tile-icon" style="position:relative;z-index:2;">${tile}</div>
                        <div class="tile-label" style="color: ${style.text};position:relative;z-index:2;">${style.label}</div>
                        ${damageBadge}
                        ${actionHtml}
                    </div>
                `;
            }
        }
        container.innerHTML = html;
    },

    getBuildingData(icon) {
        if (!EV_CONFIG || !EV_CONFIG.buildings) return null;
        for (const [name, data] of Object.entries(EV_CONFIG.buildings)) {
            if (data.icon === icon) return { name, ...data };
        }
        return null;
    },

    renderBuildPanel() {
        const panel = document.getElementById('ev-build-panel');
        if (!EV_CONFIG || !EV_CONFIG.buildings) { panel.innerHTML = ''; return; }
        if (this.state.placingMode) {
            panel.innerHTML = '<p style="color: var(--cream-dim); text-align: center;">Click an empty tile to place your building.</p>';
            return;
        }

        let html = '';
        for (const [name, data] of Object.entries(EV_CONFIG.buildings)) {
            const canAfford = this.state.stats.Money >= data.cost;
            html += `
                <div class="build-card" style="${canAfford ? '' : 'opacity: 0.5;'}" onclick="${canAfford ? `ecoVillage.startPlacement('${name}')` : ''}">
                    <div class="build-icon">${data.icon}</div>
                    <div class="build-name">${name}</div>
                    <div class="build-cost">£${data.cost}</div>
                    <div class="build-desc">${data.desc.substring(0, 50)}${data.desc.length > 50 ? '...' : ''}</div>
                </div>
            `;
        }
        panel.innerHTML = html;
    },

    startPlacement(name) {
        if (this.state.stats.Money < EV_CONFIG.buildings[name].cost) return;
        this.state.stats.Money -= EV_CONFIG.buildings[name].cost;
        this.state.placingMode = name;
        this.save();
        this.render();
    },

    cancelPlacement() {
        if (this.state.placingMode) {
            this.state.stats.Money += EV_CONFIG.buildings[this.state.placingMode].cost;
            this.state.placingMode = null;
            this.save();
            this.render();
        }
    },

    buildTile(r, c) {
        if (!this.state.placingMode) return;
        const bName = this.state.placingMode;
        const bData = EV_CONFIG.buildings[bName];
        this.state.grid[r][c] = bData.icon;
        if (!this.state.ownedBuildings[bName]) this.state.ownedBuildings[bName] = 0;
        this.state.ownedBuildings[bName]++;

        if (bName === 'Barn') {
            this.state.stats.Storage_Limit += 20;
            this.state.stats.Barn_Capacity += 20;
        }

        this.state.placingMode = null;
        this._lastPlacedTile = `${r},${c}`;
        this.save();
        this.render();
    },

    fish(r, c) {
        if (this.state.stats.Stamina < 5) { showToast('Need Stamina!'); return; }
        this.state.stats.Stamina -= 5;
        this.state.inventory['Fish'] = (this.state.inventory['Fish'] || 0) + 1;
        showToast('🎣 Caught Fish!');
        this.save();
        this.render();
    },

    repair(r, c) {
        const tile = this.state.grid[r][c];
        const bdata = this.getBuildingData(tile);
        const cost = bdata ? bdata.repair : 10;
        if (this.state.stats.Money < cost) { showToast(`Need £${cost} to repair!`); return; }
        this.state.stats.Money -= cost;
        this.state.damagedBuildings = this.state.damagedBuildings.filter(d => !(d[0] === r && d[1] === c));
        showToast('🛠️ Repaired!');
        this.save();
        this.render();
    },

/* 3f. Day Cycle ──────────────────────────────────────────────── */

    endDay() {
        const game = this.state;
        game.day++;

        // ── Season calculation ─────────────────────────────────
        const dayInCycle = game.day % 40;
        if (dayInCycle < 10)      game.season = 'Spring';
        else if (dayInCycle < 20) game.season = 'Summer';
        else if (dayInCycle < 30) game.season = 'Autumn';
        else                      game.season = 'Winter';

        // ── Weather ────────────────────────────────────────────
        const prevWeather = game.weather;
        game.weather = this.determineWeather(game.season);
        const log = [];
        if (game.weather !== prevWeather) {
            const wInfo = this.getWeatherInfo(game.weather);
            log.push({ text: `${wInfo.icon} Weather: ${wInfo.label}`, cls: 'weather' });
        }

        // ── Daily consumption & recovery ────────────────────────
        game.stats.Food    = Math.max(0, game.stats.Food - 1);
        game.stats.Water   = Math.max(0, game.stats.Water - 1);
        game.stats.Stamina = Math.min(100, game.stats.Stamina + 20);

        // Weather bonuses/penalties
        if (game.weather === 'Rainy')    game.stats.Water = Math.min(999, game.stats.Water + 2);
        if (game.weather === 'Drought')   game.stats.Water = Math.max(0, game.stats.Water - 1);

        // ── Building effects ────────────────────────────────────
        const buildingTypes = new Set();
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                const tile = game.grid[r][c];
                if (tile !== '🌲' && tile !== '🌊') buildingTypes.add(tile);

                // Skip damaged buildings
                if (game.damagedBuildings.some(d => d[0] === r && d[1] === c)) continue;

                // Skip solar/wind/reserve in winter
                if (game.season === 'Winter' && (tile === '🔆' || tile === '💨' || tile === '🌳')) continue;

                // Weather overrides
                if (game.weather === 'Stormy' && (tile === '🔆' || tile === '💨')) continue;
                if (game.weather === 'Drought' && tile === '🫧') {
                    game.stats.Food += 1; // reduced output
                    log.push({ text: '🫧 Cold Frame (drought): +1 Food', cls: 'positive' });
                    continue;
                }

                if (tile === '🏠') {
                    game.stats.Stamina = Math.min(100, game.stats.Stamina + 20);
                }
                else if (tile === '🪨') {
                    let waterGain = 5;
                    if (game.weather === 'Rainy') waterGain = 8;
                    game.stats.Water += waterGain;
                }
                else if (tile === '🐔') {
                    game.inventory['Eggs'] = (game.inventory['Eggs'] || 0) + 1;
                }
                else if (tile === '🔆') {
                    game.stats.Power = Math.min(game.stats.Max_Power, game.stats.Power + 2);
                }
                else if (tile === '💨') {
                    game.stats.Power = Math.min(50, game.stats.Power + 10);
                }
                else if (tile === '🌳') {
                    game.natureHealth = Math.min(100, game.natureHealth + 10);
                }
                else if (tile === '🌴') {
                    game.inventory['Apple']  = (game.inventory['Apple']  || 0) + 2;
                    game.inventory['Pear']   = (game.inventory['Pear']   || 0) + 2;
                    game.inventory['Orange'] = (game.inventory['Orange'] || 0) + 2;
                }
                else if (tile === '🫧') {
                    game.stats.Food += 3;
                }
                else if (tile === '🥓' && game.natureHealth >= 2) {
                    game.inventory['Wood'] = (game.inventory['Wood'] || 0) + 1;
                    game.natureHealth = Math.max(0, game.natureHealth - 2);
                }
                else if (tile === '🐐') {
                    game.inventory['Milk'] = (game.inventory['Milk'] || 0) + 1;
                }
                else if (tile === '🌱') {
                    const greenhouseCrops = ['Strawberry', 'Tomato', 'Pepper', 'Cucumber', 'Lettuce'];
                    const crop = greenhouseCrops[Math.floor(Math.random() * greenhouseCrops.length)];
                    game.inventory[crop] = (game.inventory[crop] || 0) + 1;
                    if (game.season !== 'Winter' && game.weather !== 'Drought') {
                        const crop2 = greenhouseCrops[Math.floor(Math.random() * greenhouseCrops.length)];
                        game.inventory[crop2] = (game.inventory[crop2] || 0) + 1;
                    }
                }
            }
        }

        // ── Summary log for building production ──────────────────
        if (buildingTypes.has('🏠'))  log.push({ text: '🏠 Houses: +20 Stamina each', cls: 'positive' });
        if (buildingTypes.has('🪨'))  {
            const wGain = game.weather === 'Rainy' ? 8 : 5;
            log.push({ text: `🪨 Well: +${wGain} Water${game.weather === 'Rainy' ? ' (rainy)' : ''}`, cls: 'positive' });
        }
        if (buildingTypes.has('🐔'))  log.push({ text: '🐔 Coop: +1 Egg', cls: 'positive' });
        if (buildingTypes.has('🔆') && game.season !== 'Winter' && game.weather !== 'Stormy') log.push({ text: '🔆 Solar Panel: +2 Power', cls: 'positive' });
        if (buildingTypes.has('💨') && game.season !== 'Winter' && game.weather !== 'Stormy') log.push({ text: '💨 Wind Turbine: +10 Power', cls: 'positive' });
        if (buildingTypes.has('🌳') && game.season !== 'Winter') log.push({ text: '🌳 Reserve: +10 Nature', cls: 'positive' });
        if (buildingTypes.has('🌴') && game.season !== 'Winter') log.push({ text: '🌴 Orchard: +2 Apple, Pear, Orange', cls: 'positive' });
        if (buildingTypes.has('🫧'))   log.push({ text: '🫧 Cold Frame: +3 Food', cls: 'positive' });
        if (buildingTypes.has('🐐'))   log.push({ text: '🐐 Goat Pen: +1 Milk', cls: 'positive' });
        if (buildingTypes.has('🌱'))   log.push({ text: '🌱 Greenhouse: +1-2 Crops', cls: 'positive' });
        if (buildingTypes.has('🥓'))   log.push({ text: '🥓 Smokehouse: +1 Wood', cls: 'positive' });

        // Weather effects on consumption
        log.push({ text: '🍖 Consumed: −1 Food, −1 Water', cls: 'negative' });
        if (game.weather === 'Rainy')   log.push({ text: '🌧️ Rain: +2 Water', cls: 'weather' });
        if (game.weather === 'Drought') log.push({ text: '🏜️ Drought: −1 extra Water', cls: 'negative' });
        if (game.weather === 'Stormy')  log.push({ text: '⛈️ Storm: Solar & Wind offline!', cls: 'negative' });

        // ── Winter heating ──────────────────────────────────────
        if (game.season === 'Winter') {
            const undamagedHouses = this.getUndamagedHouses();
            let woodPerHouse = 1;
            if (game.weather === 'Cold Snap') woodPerHouse = 2;

            if (undamagedHouses.length > 0) {
                const woodNeeded   = undamagedHouses.length * woodPerHouse;
                const woodAvailable = game.inventory['Wood'] || 0;
                const woodUsed     = Math.min(woodAvailable, woodNeeded);

                // Consume wood: Barn first, then Personal
                let woodRemaining = woodUsed;
                const barnWood  = game.villageStorage['Wood'] || 0;
                const barnUsed  = Math.min(barnWood, woodRemaining);
                if (barnUsed > 0) {
                    game.villageStorage['Wood'] -= barnUsed;
                    if (game.villageStorage['Wood'] <= 0) delete game.villageStorage['Wood'];
                    woodRemaining -= barnUsed;
                }
                if (woodRemaining > 0) {
                    game.inventory['Wood'] = (game.inventory['Wood'] || 0) - woodRemaining;
                    if (game.inventory['Wood'] <= 0) delete game.inventory['Wood'];
                }

                log.push({ text: `🔥 Heating: used ${woodUsed}/${woodNeeded} Wood${woodPerHouse > 1 ? ' (Cold Snap!)' : ''}`, cls: woodUsed >= woodNeeded ? 'positive' : 'negative' });

                // Unheated houses take damage every 2nd day
                const unheatedHouses = undamagedHouses.slice(woodUsed);
                if (unheatedHouses.length > 0) {
                    if (game.day % 2 === 0) {
                        for (const [r, c] of unheatedHouses) {
                            if (!game.damagedBuildings.some(d => d[0] === r && d[1] === c)) {
                                game.damagedBuildings.push([r, c]);
                            }
                        }
                        log.push({ text: `❄️ ${unheatedHouses.length} home(s) damaged by frost!`, cls: 'negative' });
                    } else {
                        log.push({ text: `⚠️ ${unheatedHouses.length} home(s) unheated!`, cls: 'negative' });
                    }
                }
            }
        }

        // ── Random damage event ─────────────────────────────────
        let damageChance = 0.12;
        if (game.weather === 'Stormy') damageChance = 0.25;
        if (game.weather === 'Snowy')  damageChance = 0.18;

        if (Math.random() < damageChance) {
            const protectedTiles = ['🌲', '🌊', '🫧', '🥓', '🌱', '🐐'];
            const buildings = [];
            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 6; c++) {
                    if (!protectedTiles.includes(game.grid[r][c])
                        && !game.damagedBuildings.some(d => d[0] === r && d[1] === c)) {
                        buildings.push([r, c, game.grid[r][c]]);
                    }
                }
            }
            if (buildings.length > 0) {
                const [r, c, icon] = buildings[Math.floor(Math.random() * buildings.length)];
                game.damagedBuildings.push([r, c]);
                const weatherNote = game.weather === 'Stormy' ? ' (storm!)' : '';
                log.push({ text: `⚠️ ${icon} damaged${weatherNote}!`, cls: 'negative' });
            }
        }

        // ── Achievements ────────────────────────────────────────
        if (game.day >= 30 && !game.achievements.eco_survivor) {
            game.achievements.eco_survivor = true;
            setAchievement('eco_survivor');
        }
        if (game.day >= 100 && !game.achievements.eco_master) {
            game.achievements.eco_master = true;
            setAchievement('eco_master');
        }
        if (game.stats.Money >= 2000 && !game.achievements.eco_wealth) {
            game.achievements.eco_wealth = true;
            setAchievement('eco_wealth');
        }
        // Builder: one of each building type
        const allBuildingTypes = ['🏠', '🪨', '🐔', '🔆', '💨', '🌳', '🌴', '🫧', '🥓', '🏡', '🐐', '🌱'];
        const hasAll = allBuildingTypes.every(icon => game.grid.some(row => row.includes(icon)));
        if (hasAll && !game.achievements.eco_builder) {
            game.achievements.eco_builder = true;
            setAchievement('eco_builder');
        }
        // Self-sufficient: producing more food than consuming
        const foodProduced = (game.grid.flat().filter(t => t === '🫧').length * 3) + (game.grid.flat().filter(t => t === '🌱').length * 2);
        if (foodProduced >= 1 && game.stats.Food > 1 && game.stats.Water > 0 && !game.achievements.eco_self_sufficient) {
            game.achievements.eco_self_sufficient = true;
            setAchievement('eco_self_sufficient');
        }
        // Nature lover: nature health >= 90
        if (game.natureHealth >= 90 && !game.achievements.eco_nature) {
            game.achievements.eco_nature = true;
            setAchievement('eco_nature');
        }
        // Winter survivor: survived winter with no damaged buildings
        if (game.season === 'Winter' && game.damagedBuildings.length === 0 && game.day > 30 && !game.achievements.eco_winter_ok) {
            const hasHouses = game.grid.flat().includes('🏠');
            if (hasHouses) {
                game.achievements.eco_winter_ok = true;
                setAchievement('eco_winter_ok');
            }
        }
        // Full village: every non-stream tile built
        if (!game.achievements.eco_full_village) {
            let allBuilt = true;
            for (let r = 0; r < 4; r++) {
                for (let c = 0; c < 6; c++) {
                    if (game.grid[r][c] === '🌲') allBuilt = false;
                }
            }
            if (allBuilt) {
                game.achievements.eco_full_village = true;
                setAchievement('eco_full_village');
            }
        }
        // Green thumb: have 3+ different greenhouse crops
        const ghCrops = ['Strawberry', 'Tomato', 'Pepper', 'Cucumber', 'Lettuce'];
        const ghOwned = ghCrops.filter(c => (game.inventory[c] || 0) > 0).length;
        if (ghOwned >= 3 && !game.achievements.eco_green_thumb) {
            game.achievements.eco_green_thumb = true;
            setAchievement('eco_green_thumb');
        }

        // ── Game over check ─────────────────────────────────────
        if (game.stats.Food <= 0 || game.stats.Water <= 0) {
            log.push({ text: '💀 Game Over! Your village starved.', cls: 'negative' });
            showToast('💀 Game Over! Your village starved.');
        }

        this.save();
        this.showDayTransition(log);
    },


    showDayTransition(dayLog) {
        const overlay = document.getElementById('ev-day-transition');
        if (!overlay) { this.render(); return; }

        const season = this.state.season;
        const icon = HS_ICONS[season] || '🌿';
        const year = Math.floor(this.state.day / 120) + 1;
        const dayInSeason = ((this.state.day - 1) % 30) + 1;
        const wInfo = this.getWeatherInfo(this.state.weather);

        let logHtml = '';
        if (dayLog && dayLog.length > 0) {
            logHtml = '<div class="day-log">' + dayLog.map(e =>
                `<div class="day-log-entry ${e.cls || ''}">${e.text}</div>`
            ).join('') + '</div>';
        }

        overlay.innerHTML = `
            <div class="ev-day-icon">${icon}</div>
            <div class="ev-day-text">Day ${this.state.day}</div>
            <div class="ev-day-sub">${season} — Year ${year}, Day ${dayInSeason} <span class="weather-badge ${wInfo.cls}">${wInfo.icon} ${wInfo.label}</span></div>
            ${logHtml}
        `;
        overlay.classList.remove('hidden');
        overlay.style.animation = 'none';
        overlay.offsetHeight;
        overlay.style.animation = '';

        setTimeout(() => {
            overlay.classList.add('hidden');
            this.render();
        }, 2500);
    },


/* 3g. Foraging & Actions ─────────────────────────────────────── */

    forageWoods() {
        if (this.state.season === 'Winter') { showToast('Cannot forage in winter!'); return; }
        if (this.state.stats.Stamina < 10)  { showToast('Need Stamina!'); return; }
        if (this.state.natureHealth < 5)     { showToast('Nature exhausted! Build a Reserve.'); return; }

        this.state.stats.Stamina   -= 10;
        this.state.natureHealth     = Math.max(0, this.state.natureHealth - 5);

        const items = EV_CONFIG ? EV_CONFIG.items : {};
        const recipeIngredients = this.getRecipeIngredients();
        const found = [];
        const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
        const maxStorage = this.state.stats.Storage_Limit;

        // Seasonal availability — items more common in their season
        const seasonBonus = { 'Spring': ['Dandelion', 'Nettle', 'Wild Garlic', 'Elderflower', 'Chickweed', 'Sorrel', 'Wild Strawberry'],
                              'Summer': ['Blackberry', 'Wild Strawberry', 'Chanterelle', 'Sea Purslane', 'Marsh Samphire', 'Beech Leaves'],
                              'Autumn': ['Hazelnut', 'Sweet Chestnut', 'Crab Apple', 'Hawthorn', 'Rosehips', 'Morel', 'Oak (Acorns)'],
                              'Winter': [] };
        const bonusItems = seasonBonus[this.state.season] || [];

        // Weather effects
        let weatherMult = 1.0;
        if (this.state.weather === 'Rainy')     weatherMult = 1.4;
        if (this.state.weather === 'Stormy')    weatherMult = 0.5;
        if (this.state.weather === 'Drought')    weatherMult = 0.6;

        const maxFinds = this.state.weather === 'Rainy' ? 5 : 4;

        for (const [name, data] of Object.entries(items)) {
            if (found.length >= maxFinds) break;
            if (data.rarity > 0 && currentStorage + found.length < maxStorage) {
                let chance = data.rarity * 0.35 * weatherMult;
                // Boost for recipe-useful items
                if (recipeIngredients.has(name)) chance *= 1.8;
                // Boost for seasonal items
                if (bonusItems.includes(name)) chance *= 1.5;
                if (Math.random() < Math.min(chance, 0.85)) {
                    this.state.inventory[name] = (this.state.inventory[name] || 0) + 1;
                    const icon = INGREDIENT_EMOJIS[name] || data.icon || '❓';
                    found.push(`${icon} ${name}`);
                }
            }
        }

        const weatherNote = this.state.weather === 'Rainy' ? ' 🌧️ Rain bonus!' :
                            this.state.weather === 'Stormy' ? ' ⛈️ Storm limited finds.' :
                            this.state.weather === 'Drought' ? ' 🏜️ Drought limited finds.' : '';
        showToast(found.length > 0 ? `🌲 Found: ${found.join(', ')}${weatherNote}` : `Nothing found this time.${weatherNote}`);
        this.save();
        this.render();
    },

    /** Helper — returns Set of ingredient names used by any recipe (excludes basics). */
    getRecipeIngredients() {
        const ingredients = new Set();
        if (!WK_CONFIG || !WK_CONFIG.recipes) return ingredients;
        const basics = WK_CONFIG.basics || [];
        for (const recipe of WK_CONFIG.recipes) {
            for (const ing of Object.keys(recipe.ingredients || {})) {
                if (!basics.includes(ing)) {
                    ingredients.add(ing);
                }
            }
        }
        return ingredients;
    },


    forageMeadow() {
        if (this.state.season !== 'Spring' && this.state.season !== 'Summer') {
            showToast('Meadow foraging only in Spring/Summer!');
            return;
        }
        if (this.state.stats.Stamina < 10) { showToast('Need Stamina!'); return; }
        if (this.state.natureHealth < 5)   { showToast('Nature exhausted!'); return; }

        this.state.stats.Stamina   -= 10;
        this.state.natureHealth     = Math.max(0, this.state.natureHealth - 5);
        const maxStorage = this.state.stats.Storage_Limit;

        fetch('/api/plants/in-season')
            .then(r => r.json())
            .then(data => {
                const ediblePlants = data.edible || [];
                if (ediblePlants.length > 0) {
                    const numFinds = Math.random() < 0.4 ? 2 : 1;
                    const found = [];
                    for (let i = 0; i < numFinds; i++) {
                        const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
                        if (currentStorage >= maxStorage) break;
                        const plant = ediblePlants[Math.floor(Math.random() * ediblePlants.length)];
                        const plantName = plant.name;
                        this.state.inventory[plantName] = (this.state.inventory[plantName] || 0) + 1;
                        found.push(plantName);
                    }
                    showToast(found.length > 0 ? `🌸 Found: ${found.join(', ')}` : 'Storage full!');
                } else {
                    showToast('Nothing in season right now.');
                }
                this.save();
                this.render();
            })
            .catch(() => {
                showToast('Could not reach plant database.');
                this.save();
                this.render();
            });
    },

    fishStream() {
        if (this.state.stats.Stamina < 5) { showToast('Need Stamina!'); return; }
        this.state.stats.Stamina -= 5;
        this.state.inventory['Fish'] = (this.state.inventory['Fish'] || 0) + 1;
        showToast('🎣 Caught a Fish!');
        this.save();
        this.render();
    },

    renderActions() {
        const el = document.getElementById('ev-actions');
        if (!el) return;

        const season = this.state.season;
        const natureLow = this.state.natureHealth < 20;

        let html = '<h3 class="market-section-title">🌿 Actions</h3>';

        if (natureLow) {
            html += `<div class="warning-box nature-low" style="margin-bottom: 0.5rem;">
                <span style="color: var(--danger); font-weight: 600;">⚠️ Nature depleted!</span>
                <span style="color: var(--cream-dim);"> Build a Reserve to restore it.</span>
            </div>`;
        }

        html += `<button class="action-btn" onclick="ecoVillage.forageWoods()" ${season === 'Winter' ? 'disabled' : ''}>🌲 Forage in Woods (10 Stamina)</button>`;
        if (season === 'Spring' || season === 'Summer') {
            html += `<button class="action-btn" onclick="ecoVillage.forageMeadow()">🌸 Forage in Meadows (10 Stamina)</button>`;
        }
        html += `<button class="action-btn" onclick="ecoVillage.fishStream()">🎣 Fish at Stream (5 Stamina)</button>`;

        // ── Production ──────────────────────────────────────────
        html += '<h4 class="market-section-title" style="margin-top: 1rem;">🏭 Production</h4>';
        if (EV_CONFIG && EV_CONFIG.production) {
            const hasSmokehouse = this.state.grid.some(row => row.includes('🥓'));
            for (const [name, recipe] of Object.entries(EV_CONFIG.production)) {
                const needsPower = (recipe.power || 0) > 0;
                let hasPower = !needsPower || this.state.stats.Power >= (recipe.power || 0);
                if (recipe.smokehouse && hasSmokehouse) hasPower = true;

                const maxStorage = this.state.stats.Storage_Limit;
                const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
                const hasSpace = currentStorage + (recipe.qty || 1) <= maxStorage;

                let hasIngredients = true;
                const ingList = [];
                for (const [ing, qty] of Object.entries(recipe.ingredients || {})) {
                    const isBasic = EV_CONFIG && EV_CONFIG.basics && EV_CONFIG.basics.includes(ing);
                    if (!isBasic && (this.state.inventory[ing] || 0) < qty) hasIngredients = false;
                    ingList.push(`${ing}x${qty}`);
                }

                const canCraft = hasPower && hasIngredients && hasSpace;
                const pwrStr = recipe.power ? ` ⚡${recipe.power}` : '';
                const smokeStr = recipe.smokehouse ? ' 🥓' : '';

                html += `<div class="production-item ${canCraft ? '' : 'disabled'}">
                    <span class="prod-name" onclick="${canCraft ? `ecoVillage.craft('${name}')` : ''}" style="cursor: ${canCraft ? 'pointer' : 'default'};">${name}</span>
                    <span class="prod-cost">${ingList.join(', ')}${pwrStr}${smokeStr}</span>
                </div>`;
            }
        }

        el.innerHTML = html;
    },

    craft(recipeName) {
        if (!EV_CONFIG || !EV_CONFIG.production || !EV_CONFIG.production[recipeName]) return;
        const recipe = EV_CONFIG.production[recipeName];
        const hasSmokehouse = this.state.grid.some(row => row.includes('🥓'));

        // Remove ingredients (Barn first, then Personal)
        for (const [ing, qty] of Object.entries(recipe.ingredients || {})) {
            const isBasic = EV_CONFIG && EV_CONFIG.basics && EV_CONFIG.basics.includes(ing);
            if (!isBasic) {
                let remaining = qty;
                const barnQty = this.state.villageStorage[ing] || 0;
                const barnUsed = Math.min(barnQty, remaining);
                if (barnUsed > 0) {
                    this.state.villageStorage[ing] -= barnUsed;
                    if (this.state.villageStorage[ing] <= 0) delete this.state.villageStorage[ing];
                    remaining -= barnUsed;
                }
                if (remaining > 0) {
                    this.state.inventory[ing] -= remaining;
                    if (this.state.inventory[ing] <= 0) delete this.state.inventory[ing];
                }
            }
        }

        // Remove power
        if ((recipe.power || 0) > 0 && !(recipe.smokehouse && hasSmokehouse)) {
            this.state.stats.Power -= recipe.power;
        }

        // Add output
        const output = recipe.output || recipeName;
        this.state.inventory[output] = (this.state.inventory[output] || 0) + (recipe.qty || 1);

        showToast(`Made ${recipeName}!`);
        this.save();
        this.render();
    },

/* 3h. Market & Pantry ────────────────────────────────────────── */

    renderPantry() {
        const el = document.getElementById('ev-pantry');
        if (!el) return;

        const maxStorage    = this.state.stats.Storage_Limit;
        const barnCapacity  = this.state.stats.Barn_Capacity;
        const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
        const barnStorage   = Object.values(this.state.villageStorage).reduce((a, b) => a + b, 0);
        const hasBarn = barnCapacity > 0;
        const items = EV_CONFIG ? EV_CONFIG.items : {};

        let html = `<h3 class="market-section-title">💰 Market & Pantry</h3>`;
        html += `<p style="color: var(--cream-dim); font-size: 0.85rem; margin-bottom: 0.5rem;">🎒 Personal: ${currentStorage}/${maxStorage}`;
        if (hasBarn) {
            html += ` &nbsp; 🏗️ Barn: ${barnStorage}/${barnCapacity}`;
        }
        html += `</p>`;

        // ── Personal Inventory ───────────────────────────────────
        html += `<div style="margin-bottom: 0.8rem;">`;
        html += `<div style="color: var(--cream); font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem;">🎒 Personal</div>`;

        const personalItems = Object.entries(this.state.inventory)
            .filter(([_, c]) => c > 0)
            .sort((a, b) => a[0].localeCompare(b[0]));

        // Bulk action buttons
        const canSellAll = personalItems.length > 0;
        html += `<div class="bulk-actions">`;
        if (hasBarn) {
            html += `<button class="bulk-btn" onclick="ecoVillage.moveAllToBarn()">📦 Move All → Barn</button>`;
        }
        if (canSellAll) {
            html += `<button class="bulk-btn danger" onclick="ecoVillage.sellAllPersonal()">💰 Sell All</button>`;
        }
        html += `</div>`;

        if (personalItems.length === 0) {
            html += `<div style="color: var(--cream-dim); font-size: 0.85rem; padding: 0.5rem;">Empty</div>`;
        } else {

            html += `<table style="width: 100%; border-collapse: collapse;">
                <tr style="color: var(--cream-dim); font-size: 0.75rem;">
                    <th style="text-align: left;">Item</th><th>Qty</th><th>Eat</th><th>Sell</th>${hasBarn ? '<th>Barn</th>' : ''}
                </tr>`;
            for (const [name, count] of personalItems) {
                const data    = items[name] || { value: 3, food: 0, icon: INGREDIENT_EMOJIS[name] || '❓' };
                const val     = data.value || 3;
                const foodVal = data.food || 0;
                const icon    = data.icon || INGREDIENT_EMOJIS[name] || '❓';
                const escapedName = name.replace(/'/g, "\\'");
                const eatBtn  = foodVal > 0
                    ? `<button class="inv-btn eat" onclick="ecoVillage.eatItem('${escapedName}', ${foodVal})">🍽️</button>`
                    : '—';
                const barnBtn = hasBarn
                    ? `<button class="inv-btn" style="border-color: #8B6914; color: #D4A017;" onclick="ecoVillage.moveToBarn('${escapedName}', 1)" title="Move 1 to Barn">→</button>`
                    : '';
                html += `<tr style="border-bottom: 1px solid #2d4a2d;">
                    <td style="color: var(--cream); font-size: 0.85rem;">${icon} ${name}</td>
                    <td style="color: var(--cream-dim); font-size: 0.85rem; text-align: center;">${count}</td>
                    <td style="text-align: center;">${eatBtn}</td>
                    <td style="text-align: center;"><button class="inv-btn sell" onclick="ecoVillage.sellItem('${escapedName}', ${val})">£${val}</button></td>
                    ${hasBarn ? `<td style="text-align: center;">${barnBtn}</td>` : ''}
                </tr>`;
            }
            html += '</table>';
        }
        html += `</div>`;

        // ── Barn Storage ─────────────────────────────────────────
        if (hasBarn) {
            html += `<div style="margin-top: 0.8rem; padding-top: 0.5rem; border-top: 1px solid #3d5a3d;">`;
            html += `<div style="color: var(--amber); font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem;">🏗️ Barn Storage <span style="color: var(--cream-dim); font-weight: 400;">(${barnStorage}/${barnCapacity})</span></div>`;

            const barnItems = Object.entries(this.state.villageStorage)
                .filter(([_, c]) => c > 0)
                .sort((a, b) => a[0].localeCompare(b[0]));

            html += `<div class="bulk-actions">`;
            if (barnItems.length > 0) {
                html += `<button class="bulk-btn" onclick="ecoVillage.takeAllFromBarn()">🎒 Take All ← Barn</button>`;
                html += `<button class="bulk-btn danger" onclick="ecoVillage.sellAllBarn()">💰 Sell All Barn</button>`;
            }
            html += `</div>`;

            if (barnItems.length === 0) {
                html += `<div style="color: var(--cream-dim); font-size: 0.85rem; padding: 0.5rem;">Empty — move items here for winter stockpiling</div>`;

            } else {
                html += `<table style="width: 100%; border-collapse: collapse;">
                    <tr style="color: var(--cream-dim); font-size: 0.75rem;">
                        <th style="text-align: left;">Item</th><th>Qty</th><th>Take</th><th>Sell</th>
                    </tr>`;
                for (const [name, count] of barnItems) {
                    const data = items[name] || { value: 3, icon: INGREDIENT_EMOJIS[name] || '❓' };
                    const val  = data.value || 3;
                    const icon = data.icon || INGREDIENT_EMOJIS[name] || '❓';
                    const escapedName = name.replace(/'/g, "\\'");
                    html += `<tr style="border-bottom: 1px solid #2d4a2d;">
                        <td style="color: var(--cream); font-size: 0.85rem;">${icon} ${name}</td>
                        <td style="color: var(--cream-dim); font-size: 0.85rem; text-align: center;">${count}</td>
                        <td style="text-align: center;"><button class="inv-btn" style="border-color: #4CAF50; color: #4CAF50;" onclick="ecoVillage.takeFromBarn('${escapedName}', 1)" title="Take 1 to Personal">←</button></td>
                        <td style="text-align: center;"><button class="inv-btn sell" onclick="ecoVillage.sellFromBarn('${escapedName}', ${val})">£${val}</button></td>
                    </tr>`;
                }
                html += '</table>';
            }
            html += `</div>`;
        }

        el.innerHTML = html;
    },

    eatItem(name, foodVal) {
        if (this.state.inventory[name] && this.state.inventory[name] > 0) {
            this.state.inventory[name]--;
            if (this.state.inventory[name] <= 0) delete this.state.inventory[name];
        } else {
            const masterInv = getMasterInventory();
            if (masterInv[name] && masterInv[name] > 0) {
                masterInv[name]--;
                if (masterInv[name] <= 0) delete masterInv[name];
                updateMasterInventory(masterInv);
            } else {
                showToast('Item not available!');
                return;
            }
        }
        this.state.stats.Food += foodVal;
        showToast(`+${foodVal} Food`);
        this.save();
        this.render();
    },

    sellItem(name, value) {
        if (this.state.inventory[name] && this.state.inventory[name] > 0) {
            this.state.inventory[name]--;
            if (this.state.inventory[name] <= 0) delete this.state.inventory[name];
        } else {
            const masterInv = getMasterInventory();
            if (masterInv[name] && masterInv[name] > 0) {
                masterInv[name]--;
                if (masterInv[name] <= 0) delete masterInv[name];
                updateMasterInventory(masterInv);
            } else {
                showToast('Item not available!');
                return;
            }
        }
        this.state.stats.Money += value;
        showToast(`Sold ${name} for £${value}`);

        if (this.state.stats.Money >= 2000 && !this.state.achievements.eco_wealth) {
            this.state.achievements.eco_wealth = true;
            setAchievement('eco_wealth');
        }
        this.save();
        this.render();
    },

    moveToBarn(name, qty) {
        if (!this.state.inventory[name] || this.state.inventory[name] < qty) return;
        const barnTotal = Object.values(this.state.villageStorage).reduce((a, b) => a + b, 0);
        if (barnTotal >= this.state.stats.Barn_Capacity) {
            showToast('🏗️ Barn is full!');
            return;
        }
        this.state.inventory[name] -= qty;
        if (this.state.inventory[name] <= 0) delete this.state.inventory[name];
        this.state.villageStorage[name] = (this.state.villageStorage[name] || 0) + qty;
        this.save();
        this.render();
    },

    takeFromBarn(name, qty) {
        if (!this.state.villageStorage[name] || this.state.villageStorage[name] < qty) return;
        const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
        if (currentStorage >= this.state.stats.Storage_Limit) {
            showToast('🎒 Personal inventory full!');
            return;
        }
        this.state.villageStorage[name] -= qty;
        if (this.state.villageStorage[name] <= 0) delete this.state.villageStorage[name];
        this.state.inventory[name] = (this.state.inventory[name] || 0) + qty;
        this.save();
        this.render();
    },

    sellFromBarn(name, value) {
        if (this.state.villageStorage[name] && this.state.villageStorage[name] > 0) {
            this.state.villageStorage[name]--;
            if (this.state.villageStorage[name] <= 0) delete this.state.villageStorage[name];
            this.state.stats.Money += value;
            showToast(`Sold ${name} for £${value}`);
            if (this.state.stats.Money >= 2000 && !this.state.achievements.eco_wealth) {
                this.state.achievements.eco_wealth = true;
                setAchievement('eco_wealth');
            }
        }
        this.save();
        this.render();
    },

    moveAllToBarn() {
        const items = Object.entries(this.state.inventory).filter(([_, c]) => c > 0);
        if (items.length === 0) { showToast('Nothing to move!'); return; }

        let moved = 0;
        for (const [name, count] of items) {
            const barnTotal = Object.values(this.state.villageStorage).reduce((a, b) => a + b, 0);
            const canMove = Math.min(count, this.state.stats.Barn_Capacity - barnTotal);
            if (canMove > 0) {
                this.state.inventory[name] -= canMove;
                if (this.state.inventory[name] <= 0) delete this.state.inventory[name];
                this.state.villageStorage[name] = (this.state.villageStorage[name] || 0) + canMove;
                moved += canMove;
            }
        }
        showToast(moved > 0 ? `📦 Moved ${moved} items to Barn` : 'Barn is full!');
        this.save();
        this.render();
    },

    takeAllFromBarn() {
        const items = Object.entries(this.state.villageStorage).filter(([_, c]) => c > 0);
        if (items.length === 0) { showToast('Barn is empty!'); return; }

        let moved = 0;
        for (const [name, count] of items) {
            const currentStorage = Object.values(this.state.inventory).reduce((a, b) => a + b, 0);
            const canMove = Math.min(count, this.state.stats.Storage_Limit - currentStorage);
            if (canMove > 0) {
                this.state.villageStorage[name] -= canMove;
                if (this.state.villageStorage[name] <= 0) delete this.state.villageStorage[name];
                this.state.inventory[name] = (this.state.inventory[name] || 0) + canMove;
                moved += canMove;
            }
        }
        showToast(moved > 0 ? `🎒 Took ${moved} items from Barn` : 'Personal inventory full!');
        this.save();
        this.render();
    },

    sellAllPersonal() {
        const items = Object.entries(this.state.inventory).filter(([_, c]) => c > 0);
        if (items.length === 0) { showToast('Nothing to sell!'); return; }

        const itemDefs = EV_CONFIG ? EV_CONFIG.items : {};
        let totalValue = 0;
        let totalItems = 0;
        for (const [name, count] of items) {
            const value = (itemDefs[name] && itemDefs[name].value) || 3;
            totalValue += value * count;
            totalItems += count;
            delete this.state.inventory[name];
        }
        this.state.stats.Money += totalValue;
        showToast(`💰 Sold ${totalItems} items for £${totalValue}`);
        if (this.state.stats.Money >= 2000 && !this.state.achievements.eco_wealth) {
            this.state.achievements.eco_wealth = true;
            setAchievement('eco_wealth');
        }
        this.save();
        this.render();
    },

    sellAllBarn() {
        const items = Object.entries(this.state.villageStorage).filter(([_, c]) => c > 0);
        if (items.length === 0) { showToast('Barn is empty!'); return; }

        const itemDefs = EV_CONFIG ? EV_CONFIG.items : {};
        let totalValue = 0;
        let totalItems = 0;
        for (const [name, count] of items) {
            const value = (itemDefs[name] && itemDefs[name].value) || 3;
            totalValue += value * count;
            totalItems += count;
            delete this.state.villageStorage[name];
        }
        this.state.stats.Money += totalValue;
        showToast(`💰 Sold ${totalItems} barn items for £${totalValue}`);
        if (this.state.stats.Money >= 2000 && !this.state.achievements.eco_wealth) {
            this.state.achievements.eco_wealth = true;
            setAchievement('eco_wealth');
        }
        this.save();
        this.render();
    },

/* 3i. Village View ───────────────────────────────────────────── */

    renderVillageView() {
        const container = document.getElementById('ev-village-scene');
        if (!container) return;

        const grid   = this.state.grid;
        const season = this.state.season.toLowerCase();
        const streamCol = this.findStreamColumn();
        const pal    = VillageSVGs.pal[season];
        const isDamaged = (r, c) => this.state.damagedBuildings.some(d => d[0] === r && d[1] === c);

        // Layout constants
        const colX     = [10, 24, 38, 52, 66, 80];
        const rowY     = [52, 60, 68, 76];
        const rowScale = [0.65, 0.78, 0.9, 1.0];

        // Sky elements
        const sunIcon = { spring: '🌤️', summer: '☀️', autumn: '🍂', winter: '❄️' }[season] || '🌤️';
        const cloudsHtml = [0, 1, 2].map(i =>
            `<div class="vl-cloud" style="top:${5 + i * 12}px; animation-duration:${18 + i * 10}s; animation-delay:${i * 6}s;">☁️</div>`
        ).join('');

        // Hills SVG
        const hillsSvg = `<svg class="vl-hills-svg" viewBox="0 0 1000 300" preserveAspectRatio="none">
            <path d="M0,180 Q120,60 280,140 Q450,20 620,120 Q800,30 1000,100 L1000,300 L0,300 Z" fill="${pal.hill1}" opacity="0.5"/>
            <path d="M0,220 Q180,100 380,180 Q580,80 780,160 Q900,120 1000,180 L1000,300 L0,300 Z" fill="${pal.hill2}" opacity="0.7"/>
        </svg>`;

        // River path
        const rx = colX[streamCol];
        const riverMeadowPath = `M${rx},42 C${rx - 2},50 ${rx + 3},60 ${rx - 1},72 C${rx + 4},82 ${rx - 3},92 ${rx},100`;
        const riverSvg = `<svg class="vl-river-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            <path d="${riverMeadowPath}" fill="none" stroke="${pal.river}" stroke-width="8" opacity="0.45"/>
            <path d="${riverMeadowPath}" fill="none" stroke="${pal.rivLt}" stroke-width="4" opacity="0.25"/>
        </svg>`;

        // Build plots
        let plotsHtml = '';
        let smokePositions = [];
        let chickenPositions = [];

        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                if (c === streamCol) continue;

                const tile    = grid[r][c];
                const x       = colX[c];
                const y       = rowY[r];
                const scale   = rowScale[r];
                const damaged = isDamaged(r, c);
                const isNew   = this._lastPlacedTile === `${r},${c}`;

                let contentHtml = '';
                let plotClass = 'vl-plot';

                if (tile === '🌲') {
                    plotClass += ' vl-plot-tree';
                    const seed = (r * 7 + c * 13) % 5;
                    contentHtml = VillageSVGs.treeCluster(season, seed);
                } else {
                    const buildingData = this.getBuildingData(tile);
                    if (buildingData) {
                        plotClass += ' vl-plot-building';
                        const svgHtml = VillageSVGs.getSVG(buildingData.name, season);
                        contentHtml = svgHtml || `<div style="font-size:2.2rem;filter:drop-shadow(0 2px 3px rgba(0,0,0,0.4));">${tile}</div>`;

                        const labelClass = damaged ? 'vl-building-label damaged' : 'vl-building-label';
                        contentHtml += `<div class="${labelClass}">${buildingData.name}${damaged ? ' ⚠️' : ''}</div>`;

                        if (damaged) {
                            contentHtml += `<div class="vl-damage-overlay"></div>`;
                        }

                        if ((tile === '🏠' || tile === '🥓') && !damaged) {
                            smokePositions.push({ x, y, scale });
                        }
                        if (tile === '🐔' && !damaged) {
                            chickenPositions.push({ x, y, scale });
                        }
                    }
                }

                if (isNew) plotClass += ' vl-plot-pop';
                plotsHtml += `<div class="${plotClass}" data-row="${r}" data-col="${c}" style="left:${x}%; top:${y}%; transform:translate(-50%,-50%) scale(${scale});">${contentHtml}</div>`;
            }
        }

        // Smoke
        const smokeHtml = smokePositions.map(pos =>
            `<div class="vl-smoke-container" style="left:${pos.x}%; top:${pos.y}%; transform:translate(-50%,-80%) scale(${pos.scale});">
                <div class="vl-smoke-puff" style="animation-delay:0s;"></div>
                <div class="vl-smoke-puff" style="animation-delay:1s;"></div>
                <div class="vl-smoke-puff" style="animation-delay:2s;"></div>
            </div>`
        ).join('');

        // Chickens
        const chickenHtml = chickenPositions.map((pos, i) =>
            `<div class="vl-chicken" style="left:${pos.x + 2 + (i % 3) * 3}%; top:${pos.y + 6}%; animation-delay:${i * 1.2}s;">🐔</div>`
        ).join('');

        // Wildflowers (spring only)
        const flowersHtml = season === 'spring' ? '<div class="vl-wildflowers"></div>' : '';

        // Render
        container.innerHTML = `
            <div class="village-landscape season-${season}">
                <div class="vl-sky">
                    <div class="vl-sun">${sunIcon}</div>
                    ${cloudsHtml}
                </div>
                ${hillsSvg}
                <div class="vl-meadow"></div>
                ${riverSvg}
                <div class="vl-plots">
                    ${plotsHtml}
                </div>
                ${smokeHtml}
                ${chickenHtml}
                ${flowersHtml}
                <div class="vl-foreground"></div>
            </div>
        `;

        // Clear pop animation flag
        this._lastPlacedTile = null;
    },

    findStreamColumn() {
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                if (this.state.grid[r][c] === '🌊') return c;
            }
        }
        return 3;
    },

    render() {
        this.applySeasonTheme();
        this.renderStats();
        this.renderSeason();
        this.renderWarning();
        this.renderGrid();
        this.renderBuildPanel();
        this.renderActions();
        this.renderPantry();
        this.renderAchievements();
        this.renderParticles();
        this.renderVillageView();
    },

/* 3j. Achievements & Reset ───────────────────────────────────── */

    renderAchievements() {
        const el = document.getElementById('ev-achievements');
        if (!el) return;

        // Count unique building types on grid
        const uniqueBuildings = new Set();
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                const t = this.state.grid[r][c];
                if (t !== '🌲' && t !== '🌊') uniqueBuildings.add(t);
            }
        }

        // Check if all non-stream tiles are built
        let allBuilt = true;
        for (let r = 0; r < 4; r++) {
            for (let c = 0; c < 6; c++) {
                if (this.state.grid[r][c] === '🌲') allBuilt = false;
            }
        }

        // Greenhouse crops count
        const ghCrops = ['Strawberry', 'Tomato', 'Pepper', 'Cucumber', 'Lettuce'];
        const ghOwned = ghCrops.filter(c => (this.state.inventory[c] || 0) > 0).length;

        const achDefs = [
            { key: 'eco_survivor', name: 'Settler', desc: 'Survive 30 days',
              progress: () => this.state.achievements.eco_survivor ? '(Done)' : `(${this.state.day}/30)` },
            { key: 'eco_master', name: 'Homesteader', desc: 'Survive 100 days',
              progress: () => this.state.achievements.eco_master ? '(Done)' : `(${this.state.day}/100)` },
            { key: 'eco_wealth', name: 'Eco-Tycoon', desc: 'Accumulate £2000',
              progress: () => this.state.achievements.eco_wealth ? '(Done)' : `(£${this.state.stats.Money}/£2000)` },
            { key: 'eco_builder', name: 'Architect', desc: 'Build one of every type',
              progress: () => this.state.achievements.eco_builder ? '(Done)' : `(${uniqueBuildings.size}/12 types)` },
            { key: 'eco_self_sufficient', name: 'Self-Sufficient', desc: 'Produce more Food than you consume in a day',
              progress: () => this.state.achievements.eco_self_sufficient ? '(Done)' : '(Keep Food above consumption)' },
            { key: 'eco_nature', name: 'Nature Guardian', desc: 'Keep Nature Health above 90%',
              progress: () => this.state.achievements.eco_nature ? '(Done)' : `(${Math.round(this.state.natureHealth)}%/90%)` },
            { key: 'eco_winter_ok', name: 'Winter Warrior', desc: 'Survive Winter with no damaged buildings',
              progress: () => this.state.achievements.eco_winter_ok ? '(Done)' : '(Survive a Winter with houses intact)' },
            { key: 'eco_full_village', name: 'Land Baron', desc: 'Build on every tile',
              progress: () => this.state.achievements.eco_full_village ? '(Done)' : (allBuilt ? '(Done!)' : '(Fill all tiles)') },
            { key: 'eco_green_thumb', name: 'Green Thumb', desc: 'Own 3+ different greenhouse crops',
              progress: () => this.state.achievements.eco_green_thumb ? '(Done)' : `(${ghOwned}/3 crops)` },
            { key: 'eco_master_chef', name: 'Master Chef', desc: 'Cook 5 different Kitchen recipes',
              progress: () => {
                  const wkState = loadState('wk_state', {});
                  const unlocked = (wkState.unlockedRecipes || []).length;
                  return this.state.achievements.eco_master_chef ? '(Done)' : `(${unlocked}/5 recipes)`;
              }},
        ];

        el.innerHTML = achDefs.map(a => this.renderAchievementCard(a)).join('');
    },


    /** Helper — renders a single achievement card. */
    renderAchievementCard(a) {
        const unlocked    = this.state.achievements[a.key];
        const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
        const bg          = unlocked ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)' : 'var(--bg-card)';
        const icon      = unlocked ? '✅' : '🔒';
        const nameColor  = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

        return `<div class="achievement-card${unlocked ? ' unlocked' : ''}" style="background: ${bg}; border-color: ${borderColor};">
            <div><div class="ach-left"><span class="ach-icon">${icon}</span><span class="ach-name" style="color: ${nameColor};">${a.name}</span></div><div class="ach-desc">${a.desc}</div></div>
            <span class="ach-progress">${a.progress()}</span>
        </div>`;
    },

    reset() {
        if (!confirm('Delete your entire village progress?')) return;
        this.state = { ...this.defaults, grid: this.createGrid() };
        this.save();
        this.render();
    }
};


/* ── Sub-tab switching for Eco-Village ────────────────────────── */

function evSwitchSubTab(tab) {
    document.querySelectorAll('#eco-village .sub-tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('#eco-village .sub-tab-content').forEach(c => c.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(`ev-tab-${tab}`).classList.add('active');
}

/* ═══════════════════════════════════════════════════════════════
   4. WILD KITCHEN
   ═══════════════════════════════════════════════════════════════ */

/* 4a. Ingredient Emoji Map ────────────────────────────────────── */

const INGREDIENT_EMOJIS = {
    // Wild herbs & greens
    'Nettle': '🌿', 'Wild Garlic': '🧄', 'Dandelion': '🌼', 'Chickweed': '🌱',
    'Sorrel': '🥬', 'Beech Leaves': '🍃', 'Pine Needles': '🌲',
    'Three-Cornered Leek': '🧅', 'Sea Purslane': '🌿', 'Marsh Samphire': '🥦',
    'Burdock (Root)': '🌿', 'Wild Strawberry': '🍓', 'Elderflower': '🌸',
    'Hawthorn': '🔴',
    // Wild fruit & nuts
    'Blackberry': '🫐', 'Rosehips': '🌹', 'Hazelnut': '🌰', 'Sweet Chestnut': '🌰',
    'Oak (Acorns)': '🌰', 'Crab Apple': '🍎', 'Wild Raspberry': '🫐',
    'Wild Plum': '🫐', 'Wild Cherry': '🍒', 'Rowan Berry': '🔴',
    'Sloe': '🫐', 'Elderberry': '🫐', 'Bilberry': '🫐',
    // Wild mushrooms
    'Chanterelle': '🍄', 'Morel': '🍄', 'Wood Ear (Jelly Ear)': '🍄',
    'Field Mushroom': '🍄', 'Oyster Mushroom': '🍄', 'Shaggy Inkcap': '🍄',
    'Porcini': '🍄', 'Hedgehog Mushroom': '🍄',
    // Wild seafood
    'Cockles': '🐚', 'Mussels': '🦪', 'Razor Clam': '🐚',
    'Limpet': '🐚', 'Winkles': '🐚',
    // Farm produce
    'Eggs': '🥚', 'Milk': '🥛', 'Cheese': '🧀', 'Cream': '🥛',
    'Strawberry': '🍓', 'Tomato': '🍅', 'Pepper': '🌶️', 'Cucumber': '🥒',
    'Lettuce': '🥬', 'Potato': '🥔', 'Carrot': '🥕', 'Onion': '🧅',
    'Garlic': '🧄', 'Herbs': '🌿', 'Wool': '🧶', 'Honey': '🍯',
    'Apple': '🍎', 'Pear': '🍐', 'Orange': '🍊', 'Fish': '🐟',
    'Wood': '🪵', 'Smoked Fish': '🐟', 'Smoked Meat': '🥓',
    'Nettle Soup': '🍲', 'Dandelion Salad': '🥗', 'Wild Garlic Pesto': '🫙',
    'Elderflower Cordial': '🍷', 'Blackberry Jam': '🫙', 'Rosehip Syrup': '🍯',
    'Mushroom Risotto': '🍚', 'Chestnut Flour': '🌾', 'Acorn Coffee': '☕',
    'Samphire Stir-fry': '🥘', 'Crab Apple Jelly': '🫙', 'Wood Ear Stir-fry': '🥘',
    'Burdock Root Stew': '🍲', 'Cockle Chowder': '🥣', 'Morel Cream Sauce': '🫙',
    'Wild Salad': '🥗', 'Hawthorn Ketchup': '🫙', 'Sloe Gin': '🥃',
    'Smoked Salmon': '🐟', 'Pickled Samphire': '🫙', 'Wild Herb Focaccia': '🍞',
    'Nettle Tea': '🍵', 'Pine Needle Tea': '🍵', 'Dandelion Coffee': '☕',
    'Wild Fruit Leather': '🍬', 'Goat Cheese': '🧀', 'Goat Milk Yogurt': '🥛',
    // Basics / staples
    'Water': '💧', 'Oil': '🫒', 'Sugar': '🍬', 'Rice': '🍚',
    'Butter': '🧈', 'Vinegar': '🫗', 'Alcohol': '🥃', 'Flour': '🌾',
    'Salt': '🧂', 'Pepper Spice': '🌶️', 'Lemon': '🍋', 'Soy Sauce': '🫙',
    'Bread': '🍞', 'Pasta': '🍝', 'Oats': '🌾', 'Cream Fraiche': '🥛',
    'Mustard': '🟡', 'Egg Yolk': '🥚', 'Stock': '🥣', 'Yeast': '🍞',
    // Catch-all
    'Seeds': '🌱', 'Compost': '♻️',
};


/* 4b. Cooking Sound Effects (Web Audio API) ──────────────────── */

const CookingSounds = {
    ctx: null,

    init() {
        if (!this.ctx) {
            try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { /* not supported */ }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    },

    plop() {
        if (!this.ctx) return;
        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.frequency.setValueAtTime(280, t);
        osc.frequency.exponentialRampToValueAtTime(80, t + 0.12);
        osc.type = 'sine';
        gain.gain.setValueAtTime(0.25, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
        osc.start(t);
        osc.stop(t + 0.15);
    },

    bubble() {
        if (!this.ctx) return;
        const t = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.frequency.setValueAtTime(300 + Math.random() * 200, t);
        osc.frequency.exponentialRampToValueAtTime(100, t + 0.1);
        osc.type = 'sine';
        gain.gain.setValueAtTime(0.08, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
        osc.start(t);
        osc.stop(t + 0.12);
    },

    stir() {
        if (!this.ctx) return;
        const t = this.ctx.currentTime;
        const bufferSize = this.ctx.sampleRate * 0.3;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * 0.03;
        }
        const source = this.ctx.createBufferSource();
        source.buffer = buffer;
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 400;
        const gain = this.ctx.createGain();
        source.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);
        gain.gain.setValueAtTime(0.15, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
        source.start(t);
    },

    chime() {
        if (!this.ctx) return;
        const t = this.ctx.currentTime;
        const notes = [523.25, 659.25, 783.99]; // C5, E5, G5
        notes.forEach((freq, i) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.frequency.value = freq;
            osc.type = 'sine';
            const start = t + (i * 0.12);
            gain.gain.setValueAtTime(0, start);
            gain.gain.linearRampToValueAtTime(0.2, start + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, start + 0.8);
            osc.start(start);
            osc.stop(start + 0.8);
        });
    },

    crackle() {
        if (!this.ctx) return;
        const t = this.ctx.currentTime;
        for (let i = 0; i < 3; i++) {
            const delay = Math.random() * 0.2;
            const bufferSize = this.ctx.sampleRate * 0.05;
            const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let j = 0; j < bufferSize; j++) {
                data[j] = (Math.random() * 2 - 1) * 0.3;
            }
            const source = this.ctx.createBufferSource();
            source.buffer = buffer;
            const gain = this.ctx.createGain();
            source.connect(gain);
            gain.connect(this.ctx.destination);
            gain.gain.setValueAtTime(0.06, t + delay);
            gain.gain.exponentialRampToValueAtTime(0.001, t + delay + 0.05);
            source.start(t + delay);
        }
    }
};

/* 4c. Defaults & State ───────────────────────────────────────── */

const wildKitchen = {

    defaults: {
        kitchenScore: 0,
        unlockedRecipes: [],
        achievements: {
            kitchen_first_cook: false,
            kitchen_apprentice: false,
            kitchen_beginner_complete: false,
            kitchen_intermediate_first: false,
            kitchen_master: false,
            kitchen_advanced_first: false,
            kitchen_grand_master: false,
            kitchen_complete: false,
            kitchen_score_100: false,
            kitchen_score_500: false,
            kitchen_score_1000: false,
            kitchen_pantry: false
        },
        currentPage: 0
    },


    state: null,
    pages: [],
    _bubbleInterval: null,
    _steamInterval: null,
    _cooking: false,
    _cookingResolve: null,
    _selectedRecipe: null,

/* 4d. Initialisation & Persistence ────────────────────────────── */

    init() {
        this.state = loadState('wk_state', this.defaults);

        if (!Array.isArray(this.state.unlockedRecipes)) this.state.unlockedRecipes = [];
        if (!this.state.achievements) this.state.achievements = {};
        if (typeof this.state.currentPage !== 'number') this.state.currentPage = 0;
        // Migrate new achievements
        const defaultAch = {
            kitchen_first_cook: false, kitchen_apprentice: false, kitchen_beginner_complete: false,
            kitchen_intermediate_first: false, kitchen_master: false, kitchen_advanced_first: false,
            kitchen_grand_master: false, kitchen_complete: false, kitchen_score_100: false,
            kitchen_score_500: false, kitchen_score_1000: false, kitchen_pantry: false
        };
        for (const [k, v] of Object.entries(defaultAch)) {
            if (this.state.achievements[k] === undefined) this.state.achievements[k] = v;
        }

        fetch('/api/games/kitchen/config')
            .then(r => r.json())
            .then(cfg => {
                WK_CONFIG = cfg;
                this.buildPages();
                this.render();
            });
    },

    save() {
        saveState('wk_state', this.state);
    },

/* 4e. Inventory ───────────────────────────────────────────────── */

    getInventory() {
        const masterInv = getMasterInventory();
        const combined = {};
        for (const [name, count] of Object.entries(masterInv)) {
            if (count > 0) combined[name] = count;
        }
        const evState = loadState('ev_state', {});
        if (evState.inventory) {
            for (const [name, count] of Object.entries(evState.inventory)) {
                if (count > 0) combined[name] = (combined[name] || 0) + count;
            }
        }
        if (evState.villageStorage) {
            for (const [name, count] of Object.entries(evState.villageStorage)) {
                if (count > 0) combined[name] = (combined[name] || 0) + count;
            }
        }
        return combined;
    },

/* 4f. Page Building & Navigation ──────────────────────────────── */

    buildPages() {
        if (!WK_CONFIG) return;
        const recipes = WK_CONFIG.recipes || [];
        const beginner     = recipes.filter(r => r.diff === 1);
        const intermediate  = recipes.filter(r => r.diff === 2);
        const advanced       = recipes.filter(r => r.diff === 3);

        const beginnerUnlocked = beginner.filter(r => this.state.unlockedRecipes.includes(r.name)).length;
        const interUnlocked    = intermediate.filter(r => this.state.unlockedRecipes.includes(r.name)).length;

        this.pages = [];

        // Chapter 1 — always open
        this.pages.push({
            type: 'chapter', chapter: 1,
            title: '⭐ Beginner',
            desc: 'Simple recipes for new foragers',
            locked: false
        });
        for (const r of beginner) {
            this.pages.push({ type: 'recipe', recipe: r });
        }

        // Chapter 2
        const ch2Locked = beginnerUnlocked < 3;
        this.pages.push({
            type: 'chapter', chapter: 2,
            title: '⭐⭐ Intermediate',
            desc: 'More complex wild recipes',
            locked: ch2Locked,
            requirement: `Unlock 3 Beginner recipes (${beginnerUnlocked}/3)`
        });
        if (!ch2Locked) {
            for (const r of intermediate) {
                this.pages.push({ type: 'recipe', recipe: r });
            }
        }

        // Chapter 3
        const ch3Locked = interUnlocked < 3;
        this.pages.push({
            type: 'chapter', chapter: 3,
            title: '⭐⭐⭐ Advanced',
            desc: 'Expert-level foraging recipes',
            locked: ch3Locked,
            requirement: `Unlock 3 Intermediate recipes (${interUnlocked}/3)`
        });
        if (!ch3Locked) {
            for (const r of advanced) {
                this.pages.push({ type: 'recipe', recipe: r });
            }
        }
    },

    prevPage() {
        if (this.state.currentPage > 0) {
            this.flipPage('backward');
        }
    },

    nextPage() {
        if (this.state.currentPage < this.pages.length - 1) {
            this.flipPage('forward');
        }
    },

    goToChapter(chapter) {
        const idx = this.pages.findIndex(p => p.type === 'chapter' && p.chapter === chapter);
        if (idx >= 0 && !this.pages[idx].locked) {
            const direction = idx > this.state.currentPage ? 'forward' : 'backward';
            this.state.currentPage = idx;
            this.buildPages();
            const pageEl = document.getElementById('wk-page');
            pageEl.classList.add(direction === 'forward' ? 'flip-forward' : 'flip-backward');
            setTimeout(() => {
                this.renderPage();
                pageEl.classList.remove('flip-forward', 'flip-backward');
            }, 300);
        }
    },

    flipPage(direction) {
        const pageEl = document.getElementById('wk-page');
        pageEl.classList.add(direction === 'forward' ? 'flip-forward' : 'flip-backward');

        setTimeout(() => {
            if (direction === 'forward') this.state.currentPage++;
            else this.state.currentPage--;
            this.renderPage();
            pageEl.classList.remove('flip-forward', 'flip-backward');
        }, 300);
    },

/* 4g. Rendering ───────────────────────────────────────────────── */

    render() {
        if (!WK_CONFIG) return;
        this.buildPages();
        if (this.state.currentPage >= this.pages.length) this.state.currentPage = this.pages.length - 1;
        if (this.state.currentPage < 0) this.state.currentPage = 0;
        this.renderPage();
        this.renderPantry();
        this.renderProgress();
        this.renderAchievements();
        this.renderChapters();
        this.renderKitchenScene();
    },

    renderPage() {
        const pageEl = document.getElementById('wk-page');
        const infoEl = document.getElementById('wk-page-info');
        const prevBtn = document.getElementById('wk-prev');
        const nextBtn = document.getElementById('wk-next');

        if (!pageEl || this.pages.length === 0) return;

        const page = this.pages[this.state.currentPage];
        if (!page) return;

        infoEl.textContent = `${this.state.currentPage + 1} / ${this.pages.length}`;
        prevBtn.disabled = this.state.currentPage === 0;
        nextBtn.disabled = this.state.currentPage === this.pages.length - 1;

        if (page.type === 'chapter') {
            pageEl.innerHTML = this.renderChapterPage(page);
        } else if (page.type === 'recipe') {
            pageEl.innerHTML = this.renderRecipePage(page.recipe);
        }

        this.save();
    },

    renderChapterPage(page) {
        if (page.locked) {
            return `
                <div class="page-locked-chapter">
                    <div class="wax-seal">🔒</div>
                    <h2 class="chapter-title locked">${page.title}</h2>
                    <p class="chapter-desc" style="color:#999;">${page.desc}</p>
                    <div class="chapter-divider-line"></div>
                    <div class="lock-notice-page">
                        <div class="lock-title">🔒 Chapter Locked</div>
                        <div class="lock-desc">${page.requirement}</div>
                    </div>
                </div>
            `;
        }
        return `
            <div class="page-chapter">
                <div class="chapter-ornament">✦ ✦ ✦</div>
                <h2 class="chapter-title">${page.title}</h2>
                <div class="chapter-divider-line"></div>
                <p class="chapter-desc">${page.desc}</p>
                <div class="chapter-ornament">✦ ✦ ✦</div>
            </div>
        `;
    },

    renderRecipePage(recipe) {
        const isUnlocked = this.state.unlockedRecipes.includes(recipe.name);
        const inv = this.getInventory();
        const basics = WK_CONFIG.basics || [];
        const hasIngredients = Object.entries(recipe.ingredients || {}).every(([ing, qty]) => {
            return basics.includes(ing) || (inv[ing] || 0) >= qty;
        });

        const stars = '⭐'.repeat(recipe.diff) + '☆'.repeat(3 - recipe.diff);
        const benefitTags = (recipe.benefit_tags || []).map(t => `<span class="benefit-tag">${t}</span>`).join('');
        const benefitDetail = recipe.benefit_detail || recipe.benefits || '';

        let html = `<div class="page-recipe ${isUnlocked ? 'unlocked' : 'locked-recipe'}">`;

        // Header
        html += `
            <div class="recipe-page-header">
                <span class="recipe-page-icon">${recipe.icon}</span>
                <h3 class="recipe-page-name">${recipe.name}</h3>
                <span class="recipe-page-stars">${stars}</span>
            </div>
            <p class="recipe-page-desc">${recipe.desc}</p>
        `;

        // Benefit box
        html += `
            <div class="benefit-box">
                <div class="benefit-title">🌿 Why It's Good For You</div>
                <div class="benefit-detail">${benefitDetail}</div>
                <div class="benefit-tags">${benefitTags}</div>
            </div>
        `;

        // Ingredients
        html += `
            <div class="recipe-ingredients-section">
                <h4 class="ingredients-title">📋 Ingredients</h4>
                <div class="ingredients-list">
        `;
        for (const [ing, qty] of Object.entries(recipe.ingredients || {})) {
            const isBasic = basics.includes(ing);
            const currentQty = inv[ing] || 0;
            const has = isBasic || currentQty >= qty;
            const statusClass = has ? 'has' : (isBasic ? 'basic' : 'missing');
            const statusIcon = has ? '✅' : (isBasic ? '∞' : '❌');
            const emoji = INGREDIENT_EMOJIS[ing] || '🍽️';
            html += `
                <div class="ingredient-item ${statusClass}">
                    <span class="ing-status">${statusIcon}</span>
                    <span class="ing-name">${emoji} ${ing}</span>
                    <span class="ing-qty">${isBasic ? '∞' : currentQty + '/' + qty}</span>
                </div>
            `;
        }
        html += `</div></div>`;

        // Action area
        if (!isUnlocked) {
            html += `<div class="unlock-section">`;
            html += `
                <div class="lock-notice">
                    <div class="lock-title">🔒 Preparation Required</div>
                    <div class="lock-desc">Answer ${recipe.prep_questions.length} question(s) to unlock this recipe.</div>
                </div>
            `;
            for (let i = 0; i < (recipe.prep_questions || []).length; i++) {
                const q = recipe.prep_questions[i];
                html += `
                    <div class="question-block">
                        <div class="q-text">Q${i + 1}: ${q.q}</div>
                        ${q.opts.map(opt => `<label><input type="radio" name="wk_q_${recipe.name.replace(/\s/g, '_')}_${i}" value="${opt}"> ${opt}</label>`).join('')}
                    </div>
                `;
            }
            const escapedName = recipe.name.replace(/'/g, "\\'");
            html += `<button class="btn-primary btn-full" onclick="wildKitchen.submitAnswers('${escapedName}')">Submit Answers</button>`;
            html += `</div>`;
        } else if (hasIngredients) {
            const escapedName = recipe.name.replace(/'/g, "\\'");
            html += `
                <div class="ready-notice">✅ Ready to Cook!</div>
                <button class="btn-primary btn-full cook-btn" onclick="wildKitchen.selectRecipeForCooking('${escapedName}')">🍳 Cook ${recipe.name}</button>
            `;
        } else {
            const missing = Object.entries(recipe.ingredients || {})
                .filter(([ing, qty]) => !basics.includes(ing) && (inv[ing] || 0) < qty)
                .map(([ing, qty]) => `${ing} (${inv[ing] || 0}/${qty})`);
            html += `
                <div class="missing-notice">
                    <div class="missing-title">🧺 Missing Ingredients</div>
                    <div class="missing-items">${missing.join(', ')}</div>
                    <div style="color: var(--cream-dim); font-size: 0.8rem; margin-top: 0.3rem;">💡 Go foraging in Foraging Games to find ingredients!</div>
                </div>
            `;
        }

        html += `</div>`; // close page-recipe
        return html;
    },

    renderChapters() {
        const el = document.getElementById('wk-chapters');
        if (!el) return;

        const chapters = this.pages.filter(p => p.type === 'chapter');
        let html = '';
        for (const ch of chapters) {
            const isCurrentChapter = this.isCurrentChapter(ch.chapter);
            const classes = ['book-chapter-tab'];
            if (isCurrentChapter) classes.push('active');
            if (ch.locked) classes.push('locked');
            html += `<button class="${classes.join(' ')}" ${ch.locked ? 'disabled' : `onclick="wildKitchen.goToChapter(${ch.chapter})"`}>${ch.title}</button>`;
        }
        el.innerHTML = html;
    },

    isCurrentChapter(chapter) {
        let chapterStart = -1;
        let chapterEnd = -1;
        let currentChapter = 0;
        for (let i = 0; i < this.pages.length; i++) {
            if (this.pages[i].type === 'chapter') {
                currentChapter = this.pages[i].chapter;
                chapterStart = i;
            }
            if (currentChapter === chapter) {
                if (chapterEnd === -1 || i >= chapterEnd) chapterEnd = i;
            }
        }
        return this.state.currentPage >= chapterStart && this.state.currentPage <= chapterEnd;
    },

/* 4h. Unlocking & Cooking ──────────────────────────────────────── */

    submitAnswers(recipeName) {
        const recipe = WK_CONFIG.recipes.find(r => r.name === recipeName);
        if (!recipe || !recipe.prep_questions) return;

        let passed = true;
        for (let i = 0; i < recipe.prep_questions.length; i++) {
            const q = recipe.prep_questions[i];
            const radioName = `wk_q_${recipeName.replace(/\s/g, '_')}_${i}`;
            const selected = document.querySelector(`input[name="${radioName}"]:checked`);
            if (!selected || selected.value !== q.a) {
                passed = false;
                break;
            }
        }

        if (passed) {
            this.state.unlockedRecipes.push(recipeName);
            this.checkKitchenAchievements();

            showToast(`✅ ${recipeName} Unlocked!`);
            this.buildPages();
            this.render();
        } else {
            showToast('❌ Incorrect. Review the safety notes and try again!');
        }

    },

        /** Check and award all Kitchen achievements based on current state. */
    checkKitchenAchievements() {
        if (!WK_CONFIG || !WK_CONFIG.recipes) return;
        const recipes = WK_CONFIG.recipes;
        const unlocked = this.state.unlockedRecipes;
        const score = this.state.kitchenScore;

        const beginnerRecipes = recipes.filter(r => r.diff === 1);
        const interRecipes = recipes.filter(r => r.diff === 2);
        const advRecipes = recipes.filter(r => r.diff === 3);

        const beginnerUnlocked = beginnerRecipes.filter(r => unlocked.includes(r.name)).length;
        const interUnlocked = interRecipes.filter(r => unlocked.includes(r.name)).length;
        const advUnlocked = advRecipes.filter(r => unlocked.includes(r.name)).length;
        const totalUnlocked = unlocked.length;

        // Apprentice: 3 Beginner recipes
        if (beginnerUnlocked >= 3 && !this.state.achievements.kitchen_apprentice) {
            this.state.achievements.kitchen_apprentice = true;
            setAchievement('kitchen_apprentice');
        }
        // Beginner Complete: all Beginner recipes
        if (beginnerUnlocked >= beginnerRecipes.length && beginnerRecipes.length > 0 && !this.state.achievements.kitchen_beginner_complete) {
            this.state.achievements.kitchen_beginner_complete = true;
            setAchievement('kitchen_beginner_complete');
        }
        // Intermediate First
        if (interUnlocked >= 1 && !this.state.achievements.kitchen_intermediate_first) {
            this.state.achievements.kitchen_intermediate_first = true;
            setAchievement('kitchen_intermediate_first');
        }
        // Master: all Intermediate recipes
        if (interUnlocked >= interRecipes.length && interRecipes.length > 0 && !this.state.achievements.kitchen_master) {
            this.state.achievements.kitchen_master = true;
            setAchievement('kitchen_master');
        }
        // Advanced First
        if (advUnlocked >= 1 && !this.state.achievements.kitchen_advanced_first) {
            this.state.achievements.kitchen_advanced_first = true;
            setAchievement('kitchen_advanced_first');
        }
        // Grand Master: all Advanced recipes
        if (advUnlocked >= advRecipes.length && advRecipes.length > 0 && !this.state.achievements.kitchen_grand_master) {
            this.state.achievements.kitchen_grand_master = true;
            setAchievement('kitchen_grand_master');
        }
        // Complete Cookbook: every recipe
        if (totalUnlocked >= recipes.length && recipes.length > 0 && !this.state.achievements.kitchen_complete) {
            this.state.achievements.kitchen_complete = true;
            setAchievement('kitchen_complete');
        }
        // Score milestones
        if (score >= 100 && !this.state.achievements.kitchen_score_100) {
            this.state.achievements.kitchen_score_100 = true;
            setAchievement('kitchen_score_100');
        }
        if (score >= 500 && !this.state.achievements.kitchen_score_500) {
            this.state.achievements.kitchen_score_500 = true;
            setAchievement('kitchen_score_500');
        }
        if (score >= 1000 && !this.state.achievements.kitchen_score_1000) {
            this.state.achievements.kitchen_score_1000 = true;
            setAchievement('kitchen_score_1000');
        }
        // Pantry: 20+ total items across all inventories
        const inv = this.getInventory();
        const totalItems = Object.values(inv).reduce((a, b) => a + b, 0);
        if (totalItems >= 20 && !this.state.achievements.kitchen_pantry) {
            this.state.achievements.kitchen_pantry = true;
            setAchievement('kitchen_pantry');
        }
    },

    async cook(recipeName) {
        if (this._cooking) return;
        const recipe = WK_CONFIG.recipes.find(r => r.name === recipeName);
        if (!recipe) return;

        // Check ingredients
        const inv = this.getInventory();
        const basics = WK_CONFIG.basics || [];
        for (const [ing, qty] of Object.entries(recipe.ingredients || {})) {
            if (!basics.includes(ing) && (inv[ing] || 0) < qty) {
                showToast('Missing ingredients!');
                return;
            }
        }

        // Remove ingredients: Barn → Personal → Master
        const evState = loadState('ev_state', {});
        const evInv = evState.inventory || {};
        const evBarn = evState.villageStorage || {};
        const masterInv = getMasterInventory();

        for (const [ing, qty] of Object.entries(recipe.ingredients || {})) {
            if (basics.includes(ing)) continue;
            let remaining = qty;

            // Take from Barn first
            if (evBarn[ing] && evBarn[ing] > 0) {
                const take = Math.min(evBarn[ing], remaining);
                evBarn[ing] -= take;
                remaining -= take;
                if (evBarn[ing] <= 0) delete evBarn[ing];
            }
            // Then from Personal
            if (remaining > 0 && evInv[ing] && evInv[ing] > 0) {
                const take = Math.min(evInv[ing], remaining);
                evInv[ing] -= take;
                remaining -= take;
                if (evInv[ing] <= 0) delete evInv[ing];
            }
            // Then from Master
            if (remaining > 0) {
                masterInv[ing] = (masterInv[ing] || 0) - remaining;
                if (masterInv[ing] <= 0) delete masterInv[ing];
            }
        }

        evState.inventory = evInv;
        saveState('ev_state', evState);
        updateMasterInventory(masterInv);

        // Add result
        masterInv[recipeName] = (masterInv[recipeName] || 0) + (recipe.qty || 1);
        updateMasterInventory(masterInv);

        // Score
        const points = (recipe.diff || 1) * 15;
        this.state.kitchenScore += points;

        // First cook achievement
        if (!this.state.achievements.kitchen_first_cook) {
            this.state.achievements.kitchen_first_cook = true;
            setAchievement('kitchen_first_cook');
        }

        // Check all score & pantry achievements
        this.checkKitchenAchievements();

        // Play animation
        await this.playCookingAnimation(recipe, points);


        this.save();
        this.buildPages();
        this.render();
    },

/* 4i. Animation ────────────────────────────────────────────────── */

    async playCookingAnimation(recipe, points) {
        this._cooking = true;

        const overlay     = document.getElementById('wk-cooking-overlay');
        const liquid      = document.getElementById('wk-liquid');
        const ingredientsEl = document.getElementById('wk-ingredients');
        const spoon       = document.getElementById('wk-spoon');
        const steam       = document.getElementById('wk-steam');
        const flash       = document.getElementById('wk-flash');
        const result      = document.getElementById('wk-result');
        const resultIcon  = document.getElementById('wk-result-icon');
        const resultText  = document.getElementById('wk-result-text');
        const resultXp    = document.getElementById('wk-result-xp');
        const skipBtn     = document.getElementById('wk-skip-btn');

        // Reset
        ingredientsEl.innerHTML = '';
        steam.innerHTML = '';
        liquid.style.height = '0%';
        liquid.style.backgroundColor = 'transparent';
        spoon.classList.remove('visible', 'stirring');
        flash.classList.remove('active');
        result.classList.add('hidden');
        skipBtn.classList.remove('hidden');

        // Show overlay
        overlay.classList.remove('hidden');
        CookingSounds.init();

        // Phase 1: Scene fades in
        await this.wait(300);
        CookingSounds.crackle();

        // Phase 2: Liquid rises
        await this.wait(200);
        liquid.style.height = '55%';

        // Phase 3: Ingredients fly in
        const ingredientEntries = Object.entries(recipe.ingredients || {});
        const totalIngTime = 2800;
        const ingDelay = ingredientEntries.length > 1 ? totalIngTime / ingredientEntries.length : 0;

        for (let i = 0; i < ingredientEntries.length; i++) {
            const [ing, qty] = ingredientEntries[i];
            const emoji = INGREDIENT_EMOJIS[ing] || '🍽️';
            const side = i % 2 === 0 ? 'from-left' : 'from-right';

            const flyEl = document.createElement('div');
            flyEl.className = `flying-ingredient ${side}`;
            flyEl.textContent = `${emoji} ${qty}×${ing}`;
            ingredientsEl.appendChild(flyEl);

            CookingSounds.plop();
            await this.wait(Math.max(ingDelay, 500));
        }

        // Clear flying ingredients
        await this.wait(300);
        ingredientsEl.innerHTML = '';

        // Phase 4: Spoon slides in
        spoon.classList.add('visible');
        await this.wait(300);
        spoon.classList.add('stirring');
        CookingSounds.stir();

        // Phase 5: Liquid changes colour
        liquid.style.backgroundColor = recipe.pot_colour || '#4a7c3f';

        // Phase 6: Bubbles start
        this._bubbleInterval = setInterval(() => {
            const bubblesEl = document.getElementById('wk-bubbles');
            if (!bubblesEl) return;
            const bubble = document.createElement('div');
            bubble.className = 'pot-bubble';
            bubble.style.left = (15 + Math.random() * 70) + '%';
            bubble.style.animationDuration = (0.5 + Math.random() * 0.5) + 's';
            bubblesEl.appendChild(bubble);
            setTimeout(() => bubble.remove(), 1200);
            if (Math.random() < 0.3) CookingSounds.bubble();
        }, 300);

        await this.wait(1000);

        // Phase 7: Steam starts
        this._steamInterval = setInterval(() => {
            const wisp = document.createElement('div');
            wisp.className = 'steam-wisp';
            wisp.style.left = (25 + Math.random() * 50) + '%';
            wisp.style.animationDuration = (2 + Math.random()) + 's';
            steam.appendChild(wisp);
            setTimeout(() => wisp.remove(), 3000);
        }, 200);

        await this.wait(2000);

        // Phase 8: Flash!
        flash.classList.add('active');
        CookingSounds.chime();

        // Phase 9: Result
        await this.wait(200);
        result.classList.remove('hidden');
        resultIcon.textContent = recipe.icon;
        resultText.textContent = `${recipe.name} Created!`;
        resultXp.textContent = `+${points} XP`;

        // Phase 10: Hold then fade
        await this.wait(1500);

        // Cleanup
        this.stopAnimationEffects();
        overlay.classList.add('hidden');
        if (skipBtn) skipBtn.classList.add('hidden');
        if (spoon) spoon.classList.remove('visible', 'stirring');
        this._selectedRecipe = null;
        this._cooking = false;
    },

    stopAnimationEffects() {
        if (this._bubbleInterval) { clearInterval(this._bubbleInterval); this._bubbleInterval = null; }
        if (this._steamInterval)  { clearInterval(this._steamInterval); this._steamInterval = null; }

        const bubblesEl = document.getElementById('wk-bubbles');
        if (bubblesEl) bubblesEl.innerHTML = '';

        const steamEl = document.getElementById('wk-steam');
        if (steamEl) steamEl.innerHTML = '';

        const flash = document.getElementById('wk-flash');
        if (flash) flash.classList.remove('active');
    },

    skipAnimation() {
        this.stopAnimationEffects();

        const overlay = document.getElementById('wk-cooking-overlay');
        const skipBtn = document.getElementById('wk-skip-btn');
        if (overlay) overlay.classList.add('hidden');
        if (skipBtn) skipBtn.classList.add('hidden');

        const spoon = document.getElementById('wk-spoon');
        if (spoon) spoon.classList.remove('visible', 'stirring');

        this._selectedRecipe = null;
        this._cooking = false;
    },

    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

/* 4j. Kitchen Scene ────────────────────────────────────────────── */

    openBook() {
        const overlay = document.getElementById('wk-book-overlay');
        overlay.classList.remove('hidden');
        this.render();
    },

    closeBook() {
        const overlay = document.getElementById('wk-book-overlay');
        overlay.classList.add('hidden');
    },

    selectRecipeForCooking(recipeName) {
        const recipe = WK_CONFIG.recipes.find(r => r.name === recipeName);
        if (!recipe) return;
        this._selectedRecipe = recipe;
        this.closeBook();
        this.renderKitchenScene();
        showToast(`🍳 ${recipe.name} selected — click the cauldron to cook!`);
    },

    clickCauldron() {
        if (!this._selectedRecipe) {
            showToast('📖 Open the book and select a recipe first!');
            return;
        }
        if (this._cooking) return;
        const recipeName = this._selectedRecipe.name;
        this._selectedRecipe = null;
        this.cook(recipeName);
    },

    openPantry() {
        const overlay = document.getElementById('wk-pantry-overlay');
        if (!overlay) return;
        overlay.classList.remove('hidden');
        this.renderPantryPopup();
    },

    closePantry() {
        const overlay = document.getElementById('wk-pantry-overlay');
        if (overlay) overlay.classList.add('hidden');
    },

    renderPantryPopup() {
        const el = document.getElementById('wk-pantry-popup');
        if (!el) return;
        const inv = this.getInventory();
        const sorted = Object.entries(inv).filter(([_, c]) => c > 0).sort((a, b) => a[0].localeCompare(b[0]));

        if (sorted.length === 0) {
            el.innerHTML = '<p style="color: #8b7355; font-size: 0.9rem;">Empty — Forage items in Foraging Games to fill your pantry!</p>';
        } else {
            el.innerHTML = sorted.map(([name, count]) => {
                const emoji = INGREDIENT_EMOJIS[name] || '🍽️';
                return `<div class="pantry-popup-row"><span>${emoji} ${name}</span><span>×${count}</span></div>`;
            }).join('');
        }

        const basicsEl = document.getElementById('wk-pantry-basics-popup');
        if (basicsEl && WK_CONFIG) {
            basicsEl.textContent = (WK_CONFIG.basics || []).join(', ');
        }
    },

    renderKitchenScene() {
        const windowScene = document.getElementById('window-scene');
        const cauldronEl  = document.getElementById('kitchen-cauldron');
        const labelEl     = document.getElementById('kitchen-cauldron-label');
        const selectedEl  = document.getElementById('kitchen-selected-recipe');

        if (!windowScene) return;

        const evState = loadState('ev_state', {});
        const season = (evState.season || 'Spring').toLowerCase();
        windowScene.className = 'ks-window-scene window-' + season;

        const sunIcon = { spring: '🌤️', summer: '☀️', autumn: '🍂', winter: '❄️' }[season] || '🌤️';
        windowScene.innerHTML = `<div class="window-sun">${sunIcon}</div>`;

        if (this._selectedRecipe) {
            if (cauldronEl) cauldronEl.classList.add('has-recipe');
            if (labelEl) {
                labelEl.textContent = '🍳 Cook!';
                labelEl.style.color = '#FFD54F';
            }
            if (selectedEl) {
                selectedEl.textContent = `${this._selectedRecipe.icon} ${this._selectedRecipe.name}`;
                selectedEl.classList.add('visible');
            }
            const liquidMini = document.getElementById('cauldron-liquid-mini');
            if (liquidMini) {
                liquidMini.style.height = '40%';
                liquidMini.style.backgroundColor = this._selectedRecipe.pot_colour || '#4a7c3f';
            }
        } else {
            if (cauldronEl) cauldronEl.classList.remove('has-recipe');
            if (labelEl) {
                labelEl.textContent = 'Click to Cook';
                labelEl.style.color = '#e8d5b5';
            }
            if (selectedEl) {
                selectedEl.textContent = '';
                selectedEl.classList.remove('visible');
            }
            const liquidMini = document.getElementById('cauldron-liquid-mini');
            if (liquidMini) {
                liquidMini.style.height = '0%';
                liquidMini.style.backgroundColor = 'transparent';
            }
        }
    },

/* 4k. Sidebar ──────────────────────────────────────────────────── */

    renderPantry() {
        const el = document.getElementById('wk-pantry');
        if (!el) return;

        const inv = this.getInventory();
        const sorted = Object.entries(inv).filter(([_, c]) => c > 0).sort((a, b) => a[0].localeCompare(b[0]));

        if (sorted.length === 0) {
            el.innerHTML = '<p style="color: var(--cream-dim); font-size: 0.85rem;">Empty — Forage items in Foraging Games</p>';
        } else {
            el.innerHTML = sorted.map(([name, count]) => {
                const emoji = INGREDIENT_EMOJIS[name] || '🍽️';
                return `<div class="inv-row"><span class="inv-name">${emoji} ${name}</span><span>${count}</span></div>`;
            }).join('');
        }

        const basicsEl = document.getElementById('wk-basics');
        if (basicsEl && WK_CONFIG) {
            basicsEl.textContent = (WK_CONFIG.basics || []).join(', ');
        }
    },

    renderProgress() {
        const el = document.getElementById('wk-progress');
        if (!el || !WK_CONFIG) return;

        const recipes = WK_CONFIG.recipes || [];
        const beginnerUnlocked = recipes.filter(r => r.diff === 1 && this.state.unlockedRecipes.includes(r.name)).length;
        const interUnlocked     = recipes.filter(r => r.diff === 2 && this.state.unlockedRecipes.includes(r.name)).length;
        const advUnlocked       = recipes.filter(r => r.diff === 3 && this.state.unlockedRecipes.includes(r.name)).length;
        const totalUnlocked     = this.state.unlockedRecipes.length;
        const totalRecipes      = recipes.length;

        el.innerHTML = `
            <div class="progress-title" style="color: var(--amber); font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;">🏆 Progress</div>
            <div style="color: var(--cream); font-size: 0.9rem;">Kitchen Score: <b>${this.state.kitchenScore}</b></div>
            <div style="color: var(--cream-dim); font-size: 0.85rem; margin-top: 0.3rem;">⭐ Beginner: ${beginnerUnlocked}/${recipes.filter(r => r.diff === 1).length}</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem;">⭐⭐ Intermediate: ${interUnlocked}/${recipes.filter(r => r.diff === 2).length}</div>
            <div style="color: var(--cream-dim); font-size: 0.85rem;">⭐⭐⭐ Advanced: ${advUnlocked}/${recipes.filter(r => r.diff === 3).length}</div>
            <div style="border-top: 1px solid #3d5a3d; margin-top: 0.5rem; padding-top: 0.5rem; color: var(--amber); font-weight: 700; font-size: 0.85rem;">📖 Recipes Unlocked: ${totalUnlocked}/${totalRecipes}</div>
        `;
    },

/* 4l. Achievements ────────────────────────────────────────────── */

    renderAchievements() {
        const el = document.getElementById('wk-achievements');
        if (!el || !WK_CONFIG) return;

        const recipes = WK_CONFIG.recipes || [];
        const unlocked = this.state.unlockedRecipes;
        const score = this.state.kitchenScore;

        const beginnerRecipes = recipes.filter(r => r.diff === 1);
        const interRecipes = recipes.filter(r => r.diff === 2);
        const advRecipes = recipes.filter(r => r.diff === 3);

        const beginnerUnlocked = beginnerRecipes.filter(r => unlocked.includes(r.name)).length;
        const interUnlocked = interRecipes.filter(r => unlocked.includes(r.name)).length;
        const advUnlocked = advRecipes.filter(r => unlocked.includes(r.name)).length;
        const totalUnlocked = unlocked.length;

        const inv = this.getInventory();
        const totalItems = Object.values(inv).reduce((a, b) => a + b, 0);

        const achDefs = [
            { key: 'kitchen_first_cook', name: 'First Dish', desc: 'Cook your first recipe',
              progress: () => this.state.achievements.kitchen_first_cook ? '(Done)' : '(Cook any recipe)' },
            { key: 'kitchen_apprentice', name: 'Apprentice', desc: 'Unlock 3 Beginner recipes',
              progress: () => this.state.achievements.kitchen_apprentice ? '(Done)' : `(${beginnerUnlocked}/3)` },
            { key: 'kitchen_beginner_complete', name: 'Beginner Chef', desc: 'Unlock all Beginner recipes',
              progress: () => this.state.achievements.kitchen_beginner_complete ? '(Done)' : `(${beginnerUnlocked}/${beginnerRecipes.length})` },
            { key: 'kitchen_intermediate_first', name: 'Rising Star', desc: 'Unlock your first Intermediate recipe',
              progress: () => this.state.achievements.kitchen_intermediate_first ? '(Done)' : `(${interUnlocked}/1)` },
            { key: 'kitchen_master', name: 'Master Chef', desc: 'Unlock all Intermediate recipes',
              progress: () => this.state.achievements.kitchen_master ? '(Done)' : `(${interUnlocked}/${interRecipes.length})` },
            { key: 'kitchen_advanced_first', name: 'Adventurer', desc: 'Unlock your first Advanced recipe',
              progress: () => this.state.achievements.kitchen_advanced_first ? '(Done)' : `(${advUnlocked}/1)` },
            { key: 'kitchen_grand_master', name: 'Grand Master', desc: 'Unlock all Advanced recipes',
              progress: () => this.state.achievements.kitchen_grand_master ? '(Done)' : `(${advUnlocked}/${advRecipes.length})` },
            { key: 'kitchen_complete', name: 'Complete Cookbook', desc: 'Unlock every recipe in the game',
              progress: () => this.state.achievements.kitchen_complete ? '(Done)' : `(${totalUnlocked}/${recipes.length})` },
            { key: 'kitchen_score_100', name: 'Line Cook', desc: 'Reach a Kitchen Score of 100',
              progress: () => this.state.achievements.kitchen_score_100 ? '(Done)' : `(${score}/100)` },
            { key: 'kitchen_score_500', name: 'Sous Chef', desc: 'Reach a Kitchen Score of 500',
              progress: () => this.state.achievements.kitchen_score_500 ? '(Done)' : `(${score}/500)` },
            { key: 'kitchen_score_1000', name: 'Head Chef', desc: 'Reach a Kitchen Score of 1000',
              progress: () => this.state.achievements.kitchen_score_1000 ? '(Done)' : `(${score}/1000)` },
            { key: 'kitchen_pantry', name: 'Well Stocked', desc: 'Have 20+ items in your pantry',
              progress: () => this.state.achievements.kitchen_pantry ? '(Done)' : `(${totalItems}/20)` },
        ];

        el.innerHTML = achDefs.map(a => this.renderAchievementCard(a)).join('');
    },


    /** Helper — renders a single achievement card. */
    renderAchievementCard(a) {
        const unlocked    = this.state.achievements[a.key];
        const borderColor = unlocked ? 'var(--green-leaf)' : '#444';
        const bg          = unlocked ? 'linear-gradient(135deg, #0a2a0a, #1a3d1a)' : 'var(--bg-card)';
        const icon      = unlocked ? '✅' : '🔒';
        const nameColor  = unlocked ? 'var(--green-leaf)' : 'var(--cream-dim)';

        return `<div class="achievement-card${unlocked ? ' unlocked' : ''}" style="background: ${bg}; border-color: ${borderColor};">
            <div><div class="ach-left"><span class="ach-icon">${icon}</span><span class="ach-name" style="color: ${nameColor};">${a.name}</span></div><div class="ach-desc">${a.desc}</div></div>
            <span class="ach-progress">${a.progress()}</span>
        </div>`;
    }
};


/* ═══════════════════════════════════════════════════════════════
   5. SUB-TAB SWITCHING
   ═══════════════════════════════════════════════════════════════ */

/* (Already defined above as evSwitchSubTab) */


/* ═══════════════════════════════════════════════════════════════
   6. BOOTSTRAP
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    ecoVillage.init();
    wildKitchen.init();
});
