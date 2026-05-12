/* =============================================
   COINPULSE — script.js  v2
   ============================================= */
'use strict';

/* ===========================
   STATE
   =========================== */
const STATE = {
  coins:       [],
  watchlist:   JSON.parse(localStorage.getItem('cp_wl') || '[]'),
  currentCoin: null,
  prevPage:    'dashboard',
  page:        'dashboard',
  market: {
    filter:  'all',
    query:   '',
    sort:    'rank',
    asc:     true,
    pg:      1,
    perPage: 20
  }
};

const miniCharts = {};
let mainChartInst  = null;
let refreshTimer   = null;
let liveTimer      = null;    // strip refresh interval
let liveWs         = null;    // Binance WebSocket
let liveUpdateTimer = null;   // chart update throttle
let isLive         = false;
let currentDays    = '7';
const LIVE_MAX_PTS = 120;     // rolling window size
let livePrices     = [];
let liveLabels     = [];
let pendingPrice   = null;    // latest price from WS (throttled to chart)

/* ===========================
   API
   =========================== */
const API = 'https://api.coingecko.com/api/v3';

async function apiGet(path) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

function fetchCoins()       { return apiGet('/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h'); }
function fetchGlobal()      { return apiGet('/global').then(d => d.data); }
function fetchChart(id, days){ return apiGet(`/coins/${id}/market_chart?vs_currency=usd&days=${days}`); }

/* ===========================
   INIT
   =========================== */
async function init() {
  setupNav();
  setupSearch();
  renderSkeletons();

  try {
    const [coins, global] = await Promise.all([fetchCoins(), fetchGlobal().catch(() => null)]);
    STATE.coins = coins;
    renderTicker(coins.slice(0, 20));
    renderGlobalStats(global);
    renderFeatured(coins.slice(0, 3));
    renderMovers(coins);
    renderMarket();
    renderWatchlist();
    updateBadge();
  } catch (e) {
    toast('Could not load data. Check your internet connection.', 'err');
  }

  refreshTimer = setInterval(refresh, 30000);
}

async function refresh() {
  try {
    const coins = await fetchCoins();
    STATE.coins = coins;
    renderTicker(coins.slice(0, 20));
    renderFeatured(coins.slice(0, 3));
    renderMovers(coins);
    if (STATE.page === 'market')    renderMarket();
    if (STATE.page === 'watchlist') renderWatchlist();
  } catch (_) {}
}

/* ===========================
   TICKER TAPE
   =========================== */
function renderTicker(coins) {
  const inner = document.getElementById('tickerInner');
  if (!inner) return;
  const items = coins.map(c => {
    const chg = c.price_change_percentage_24h || 0;
    return `<div class="ticker-item">
      <img src="${c.image}" alt="" loading="lazy">
      <span class="t-sym">${c.symbol.toUpperCase()}</span>
      <span class="t-price">${fmt(c.current_price)}</span>
      <span class="t-chg ${chg>=0?'pos':'neg'}">${chg>=0?'▲':'▼'}${Math.abs(chg).toFixed(2)}%</span>
    </div>`;
  }).join('');
  inner.innerHTML = items + items;
}

/* ===========================
   GLOBAL STATS
   =========================== */
function renderGlobalStats(g) {
  const el = document.getElementById('globalStats');
  if (!el) return;
  if (!g) { el.innerHTML = ''; return; }

  const mc  = (g.total_market_cap.usd / 1e12).toFixed(2);
  const vol = (g.total_volume.usd / 1e9).toFixed(0);
  const btc = g.market_cap_percentage.btc.toFixed(1);
  const num = g.active_cryptocurrencies.toLocaleString();
  const chg = (g.market_cap_change_percentage_24h_usd || 0).toFixed(2);
  const pos = parseFloat(chg) >= 0;

  el.innerHTML = `
    <div class="stat-card">
      <div class="stat-label">Total Market Cap</div>
      <div class="stat-value">$${mc}T</div>
      <div class="stat-chg" style="color:${pos?'var(--green)':'var(--red)'}">
        ${pos?'▲':'▼'} ${Math.abs(chg)}% 24h
      </div>
    </div>
    <div class="stat-card">
      <div class="stat-label">24h Volume</div>
      <div class="stat-value">$${vol}B</div>
      <div class="stat-chg" style="color:var(--text2);font-weight:400">Total traded</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">BTC Dominance</div>
      <div class="stat-value">${btc}%</div>
      <div class="stat-chg" style="color:var(--text2);font-weight:400">Market share</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Active Coins</div>
      <div class="stat-value">${num}</div>
      <div class="stat-chg" style="color:var(--text2);font-weight:400">Listed globally</div>
    </div>
  `;
}

/* ===========================
   FEATURED + SPARKLINES
   =========================== */
function renderFeatured(coins) {
  const el = document.getElementById('featuredCoins');
  if (!el) return;

  el.innerHTML = coins.map(c => {
    const chg = c.price_change_percentage_24h || 0;
    return `
    <div class="coin-feat" onclick="openCoin('${c.id}')">
      <div class="cf-top">
        <div class="cf-id">
          <img src="${c.image}" class="cf-img" alt="${c.name}" loading="lazy">
          <div>
            <div class="cf-name">${c.name}</div>
            <div class="cf-sym">${c.symbol.toUpperCase()}</div>
          </div>
        </div>
        <div class="cf-rank">#${c.market_cap_rank}</div>
      </div>
      <div class="cf-price">${fmt(c.current_price)}</div>
      <span class="chg-pill ${chg>=0?'pos':'neg'}">${chg>=0?'▲':'▼'} ${Math.abs(chg).toFixed(2)}%</span>
      <div class="cf-mini"><canvas id="sp-${c.id}"></canvas></div>
    </div>`;
  }).join('');

  setTimeout(() => {
    coins.forEach(c => {
      const sp  = c.sparkline_in_7d?.price;
      const ctx = document.getElementById(`sp-${c.id}`);
      if (!sp || !ctx) return;
      const isUp  = (c.price_change_percentage_24h || 0) >= 0;
      const color = isUp ? '#00e87a' : '#ff4466';
      if (miniCharts[c.id]) miniCharts[c.id].destroy();
      miniCharts[c.id] = new Chart(ctx, {
        type: 'line',
        data: {
          labels: sp.map((_,i) => i),
          datasets: [{
            data: sp, borderColor: color, borderWidth: 1.5,
            pointRadius: 0, fill: true,
            backgroundColor: ctx2 => {
              const g = ctx2.chart.ctx.createLinearGradient(0,0,0,56);
              g.addColorStop(0, isUp?'rgba(0,232,122,.22)':'rgba(255,68,102,.22)');
              g.addColorStop(1, 'transparent');
              return g;
            }
          }]
        },
        options: {
          responsive:true, maintainAspectRatio:false,
          plugins:{legend:{display:false},tooltip:{enabled:false}},
          scales:{x:{display:false},y:{display:false}},
          animation:false
        }
      });
    });
  }, 80);
}

/* ===========================
   MOVERS
   =========================== */
function renderMovers(coins) {
  const sorted = [...coins].sort((a,b) =>
    (b.price_change_percentage_24h||0) - (a.price_change_percentage_24h||0)
  );

  const mkList = (arr, isGainer) => arr.map(c => {
    const chg = c.price_change_percentage_24h || 0;
    return `<div class="mover-item" onclick="openCoin('${c.id}')">
      <img src="${c.image}" alt="" loading="lazy">
      <div>
        <div class="mover-name">${c.name}</div>
        <div class="mover-sym">${c.symbol.toUpperCase()}</div>
      </div>
      <div class="mover-chg" style="color:${isGainer?'var(--green)':'var(--red)'}">
        ${chg>=0?'▲':'▼'} ${Math.abs(chg).toFixed(2)}%
      </div>
    </div>`;
  }).join('');

  const g = document.getElementById('gainersList');
  const l = document.getElementById('losersList');
  if (g) g.innerHTML = mkList(sorted.slice(0,5), true);
  if (l) l.innerHTML = mkList(sorted.slice(-5).reverse(), false);
}

/* ===========================
   MARKET TABLE
   =========================== */
function renderMarket() {
  let coins = [...STATE.coins];
  const { filter, query, sort, asc, pg, perPage } = STATE.market;

  if (filter === 'gainers') coins = coins.filter(c => (c.price_change_percentage_24h||0) > 0);
  if (filter === 'losers')  coins = coins.filter(c => (c.price_change_percentage_24h||0) < 0);
  if (filter === 'top10')   coins = coins.slice(0,10);

  if (query) {
    const q = query.toLowerCase();
    coins = coins.filter(c => c.name.toLowerCase().includes(q) || c.symbol.toLowerCase().includes(q));
  }

  coins.sort((a,b) => {
    let av, bv;
    switch (sort) {
      case 'rank':   av=a.market_cap_rank;             bv=b.market_cap_rank; break;
      case 'name':   return asc ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
      case 'price':  av=a.current_price;               bv=b.current_price; break;
      case 'change': av=a.price_change_percentage_24h||0; bv=b.price_change_percentage_24h||0; break;
      case 'cap':    av=a.market_cap;                  bv=b.market_cap; break;
      case 'vol':    av=a.total_volume;                bv=b.total_volume; break;
      default:       av=a.market_cap_rank;             bv=b.market_cap_rank;
    }
    return asc ? av-bv : bv-av;
  });

  const sub = document.getElementById('mktSub');
  if (sub) sub.textContent = `${coins.length} coins`;

  const pages = Math.ceil(coins.length / perPage);
  const slice = coins.slice((pg-1)*perPage, pg*perPage);

  const tbody = document.getElementById('mktTbody');
  if (!tbody) return;
  tbody.innerHTML = slice.map(c => {
    const chg  = c.price_change_percentage_24h || 0;
    const inWl = STATE.watchlist.some(w => w.id === c.id);
    return `<tr onclick="openCoin('${c.id}')">
      <td class="rank-num">${c.market_cap_rank}</td>
      <td>
        <div class="ci-wrap">
          <img src="${c.image}" class="ci-img" alt="" loading="lazy">
          <div>
            <div class="ci-name">${c.name}</div>
            <div class="ci-sym">${c.symbol.toUpperCase()}</div>
          </div>
        </div>
      </td>
      <td class="rt mono">${fmt(c.current_price)}</td>
      <td class="rt"><span class="chg-tag ${chg>=0?'pos':'neg'}">${chg>=0?'▲':'▼'}${Math.abs(chg).toFixed(2)}%</span></td>
      <td class="rt mono col-cap">${fmtK(c.market_cap)}</td>
      <td class="rt mono col-vol">${fmtK(c.total_volume)}</td>
      <td class="rt">
        <button class="star-btn" onclick="event.stopPropagation();toggleWl('${c.id}')"
          title="${inWl?'Remove':'Add to watchlist'}"
          style="color:${inWl?'var(--gold)':'var(--text3)'}">
          ${inWl?'★':'☆'}
        </button>
      </td>
    </tr>`;
  }).join('');

  renderPagination(pages);
}

function sortBy(key) {
  if (STATE.market.sort === key) STATE.market.asc = !STATE.market.asc;
  else { STATE.market.sort = key; STATE.market.asc = true; }
  STATE.market.pg = 1;
  renderMarket();
}

function setFilter(f, btn) {
  STATE.market.filter = f;
  STATE.market.pg = 1;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderMarket();
}

function filterByQuery(q) {
  STATE.market.query = q;
  STATE.market.pg = 1;
  renderMarket();
}

function goPage(n) {
  STATE.market.pg = n;
  renderMarket();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderPagination(pages) {
  const el = document.getElementById('pagination');
  if (!el) return;
  if (pages <= 1) { el.innerHTML = ''; return; }
  const cur = STATE.market.pg;
  let html = `<button class="pg-btn" onclick="goPage(${cur-1})" ${cur===1?'disabled':''}>←</button>`;
  const s = Math.max(1, cur-2), e = Math.min(pages, cur+2);
  if (s > 1) {
    html += `<button class="pg-btn" onclick="goPage(1)">1</button>`;
    if (s > 2) html += `<span class="pg-ellipsis">…</span>`;
  }
  for (let i=s; i<=e; i++)
    html += `<button class="pg-btn ${i===cur?'active':''}" onclick="goPage(${i})">${i}</button>`;
  if (e < pages) {
    if (e < pages-1) html += `<span class="pg-ellipsis">…</span>`;
    html += `<button class="pg-btn" onclick="goPage(${pages})">${pages}</button>`;
  }
  html += `<button class="pg-btn" onclick="goPage(${cur+1})" ${cur===pages?'disabled':''}>→</button>`;
  el.innerHTML = html;
}

/* ===========================
   WATCHLIST
   =========================== */
function renderWatchlist() {
  const el  = document.getElementById('wlContent');
  const sub = document.getElementById('wlSub');
  if (!el) return;

  if (!STATE.watchlist.length) {
    el.innerHTML = `<div class="wl-empty">
      <div class="wl-empty-icon">☆</div>
      <h3>Your watchlist is empty</h3>
      <p>Go to Market and tap ☆ to save coins here</p>
      <button class="go-mkt" onclick="showPage('market')">Browse Market</button>
    </div>`;
    if (sub) sub.textContent = '0 coins saved';
    return;
  }

  const coins = STATE.watchlist.map(w => STATE.coins.find(c => c.id===w.id) || w);
  if (sub) sub.textContent = `${coins.length} coin${coins.length!==1?'s':''} saved`;

  el.innerHTML = `
    <div class="table-wrap">
      <table class="coin-table">
        <thead>
          <tr>
            <th>#</th><th>Coin</th>
            <th class="rt">Price</th><th class="rt">24h %</th>
            <th class="rt col-cap">Mkt Cap</th><th class="rt col-vol">Volume</th>
            <th class="rt">Remove</th>
          </tr>
        </thead>
        <tbody>
          ${coins.map(c => {
            const chg = c.price_change_percentage_24h || 0;
            return `<tr onclick="openCoin('${c.id}')">
              <td class="rank-num">${c.market_cap_rank||'—'}</td>
              <td><div class="ci-wrap">
                <img src="${c.image}" class="ci-img" alt="" loading="lazy">
                <div><div class="ci-name">${c.name}</div><div class="ci-sym">${c.symbol.toUpperCase()}</div></div>
              </div></td>
              <td class="rt mono">${fmt(c.current_price)}</td>
              <td class="rt"><span class="chg-tag ${chg>=0?'pos':'neg'}">${chg>=0?'▲':'▼'}${Math.abs(chg).toFixed(2)}%</span></td>
              <td class="rt mono col-cap">${fmtK(c.market_cap)}</td>
              <td class="rt mono col-vol">${fmtK(c.total_volume)}</td>
              <td class="rt">
                <button class="star-btn" onclick="event.stopPropagation();removeWl('${c.id}')"
                  style="color:var(--red)" title="Remove">✕</button>
              </td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>`;
}

function toggleWl(id) {
  const coin = STATE.coins.find(c => c.id===id);
  if (!coin) return;
  const idx = STATE.watchlist.findIndex(w => w.id===id);
  if (idx > -1) {
    STATE.watchlist.splice(idx,1);
    toast(`${coin.name} removed from watchlist`, 'ok');
  } else {
    STATE.watchlist.push(coin);
    toast(`${coin.name} added ★`, 'ok');
  }
  saveWl();
  renderMarket();
  renderWatchlist();
  updateBadge();
}

function removeWl(id) {
  const idx = STATE.watchlist.findIndex(w => w.id===id);
  if (idx > -1) {
    const name = STATE.watchlist[idx].name;
    STATE.watchlist.splice(idx,1);
    saveWl(); renderWatchlist(); updateBadge();
    toast(`${name} removed`, 'ok');
  }
}

function saveWl()      { localStorage.setItem('cp_wl', JSON.stringify(STATE.watchlist)); }
function updateBadge() {
  const b = document.getElementById('wlBadge');
  const n = STATE.watchlist.length;
  if (b) { b.textContent=n; b.style.display=n?'flex':'none'; }
  // Update sidebar count
  const sc = document.getElementById('sbWlCount');
  if (sc) { sc.textContent=n; sc.style.display=n?'inline-flex':'none'; }
}

/* ===========================
   COIN DETAIL
   =========================== */
function openCoin(id) {
  if (isLive) stopLive();   // reset live when switching coins
  STATE.prevPage    = STATE.page;
  STATE.currentCoin = id;
  showPage('detail');

  const coin = STATE.coins.find(c => c.id===id);
  if (!coin) return;

  const chg  = coin.price_change_percentage_24h || 0;
  const inWl = STATE.watchlist.some(w => w.id===id);

  const hero = document.getElementById('detailHero');
  if (hero) hero.innerHTML = `
    <div class="d-id">
      <img src="${coin.image}" class="d-img" alt="${coin.name}">
      <div>
        <div class="d-name">${coin.name}</div>
        <div class="d-sym">${coin.symbol.toUpperCase()} · Rank #${coin.market_cap_rank}</div>
      </div>
    </div>
    <div class="d-actions">
      <div>
        <div class="d-price">${fmt(coin.current_price)}</div>
        <div style="margin-top:6px">
          <span class="chg-pill ${chg>=0?'pos':'neg'}">${chg>=0?'▲':'▼'} ${Math.abs(chg).toFixed(2)}%</span>
        </div>
      </div>
      <button class="wl-btn ${inWl?'starred':''}" id="detailWlBtn" onclick="toggleDetailWl()">
        ${inWl?'★ Watching':'☆ Watch'}
      </button>
    </div>
  `;

  const ds = document.getElementById('detailStats');
  if (ds) ds.innerHTML = `
    <div class="stat-card">
      <div class="stat-label">Market Cap</div>
      <div class="stat-value" style="font-size:1.05rem">${fmtK(coin.market_cap)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">24h Volume</div>
      <div class="stat-value" style="font-size:1.05rem">${fmtK(coin.total_volume)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">24h High</div>
      <div class="stat-value" style="font-size:1.05rem;color:var(--green)">${fmt(coin.high_24h)}</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">24h Low</div>
      <div class="stat-value" style="font-size:1.05rem;color:var(--red)">${fmt(coin.low_24h)}</div>
    </div>
  `;

  // Reset time buttons — default to 7D
  document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
  const def = document.querySelectorAll('.time-btn')[1]; // index 1 = 7D
  if (def) def.classList.add('active');
  currentDays = '7';
  drawChart('7');
}

function toggleDetailWl() {
  const id   = STATE.currentCoin;
  const coin = STATE.coins.find(c => c.id===id);
  if (!coin) return;
  const idx  = STATE.watchlist.findIndex(w => w.id===id);
  if (idx > -1) { STATE.watchlist.splice(idx,1); toast(`${coin.name} removed`,'ok'); }
  else           { STATE.watchlist.push(coin);    toast(`${coin.name} added ★`,'ok'); }
  saveWl(); updateBadge();
  const inWl = STATE.watchlist.some(w => w.id===id);
  const btn  = document.getElementById('detailWlBtn');
  if (btn) { btn.className=`wl-btn${inWl?' starred':''}`; btn.textContent=inWl?'★ Watching':'☆ Watch'; }
}

/* ===========================
   CHART MODE SWITCHER
   (handles both timeframe buttons and LIVE toggle)
   =========================== */
function setChartMode(days, btn) {
  // Deactivate LIVE when a timeframe button is clicked
  if (isLive) stopLive();

  currentDays = days;
  document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  drawChart(days);
}

/* ===========================
   LIVE MODE — Binance WebSocket
   =========================== */
function toggleLive() {
  if (isLive) stopLive(); else startLive();
}

/* Map CoinGecko coin symbol → Binance USDT pair */
function toBinanceSymbol(symbol) {
  const s = symbol.toUpperCase();
  // Stablecoins / fiat-pegged coins won't stream well — skip
  const skip = ['USDT','USDC','DAI','BUSD','TUSD','USDP','GUSD'];
  if (skip.includes(s)) return null;
  return s + 'USDT';
}

async function startLive() {
  const coin = STATE.coins.find(c => c.id === STATE.currentCoin);
  if (!coin) return;

  const binSym = toBinanceSymbol(coin.symbol);
  if (!binSym) { toast('Live stream not available for stablecoins', 'err'); return; }

  isLive = true;

  // UI: activate button + show strip immediately
  const liveBtn   = document.getElementById('liveBtn');
  const liveStrip = document.getElementById('liveStrip');
  if (liveBtn)   liveBtn.classList.add('on');
  if (liveStrip) liveStrip.classList.add('visible');

  // Deactivate timeframe buttons
  document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));

  // Fill strip immediately with current coin data
  fillStrip(coin);

  // ── STEP 1: Fetch real 1-day price history to seed the chart ──
  // Use CoinGecko minutes-resolution endpoint (days=1 gives per-minute data)
  try {
    const res  = await fetch(
      `https://api.coingecko.com/api/v3/coins/${STATE.currentCoin}/market_chart` +
      `?vs_currency=usd&days=1`
    );
    const json = await res.json();
    const pts  = json.prices || [];

    // Take last LIVE_MAX_PTS points so chart isn't too cluttered
    const slice = pts.slice(-LIVE_MAX_PTS);

    livePrices = slice.map(p => p[1]);
    liveLabels = slice.map(p => {
      const d = new Date(p[0]);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
  } catch (_) {
    // Fallback: seed with just the current price (single point, WebSocket fills in)
    livePrices = [coin.current_price];
    liveLabels = [new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })];
  }

  // ── STEP 2: Build chart with real history ──
  buildLiveChart();

  // ── STEP 3: Strip refreshes every 10 s from CoinGecko ──
  liveTimer = setInterval(() => refreshStrip(), 10000);

  // ── STEP 4: Connect Binance WebSocket — ticks append to real history ──
  openLiveWs(binSym.toLowerCase());
}

function openLiveWs(binSymLower) {
  try {
    liveWs = new WebSocket(`wss://stream.binance.com:9443/ws/${binSymLower}@aggTrade`);

    liveWs.onopen = () => {
      toast('Live stream connected ●', 'ok');
    };

    liveWs.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      // aggTrade: { p: price string, T: trade timestamp ms }
      pendingPrice = { price: parseFloat(msg.p), ts: msg.T };
    };

    liveWs.onerror = () => {
      if (isLive) { toast('Live stream lost', 'err'); stopLive(); }
    };

    liveWs.onclose = () => {
      if (isLive) stopLive();
    };

    let lastLabel = '';   // track last second pushed — avoid duplicate labels

    // Push latest price onto chart every 1 s
    liveUpdateTimer = setInterval(() => {
      if (!pendingPrice || !isLive) return;

      const { price, ts } = pendingPrice;
      pendingPrice = null;

      const label = new Date(ts).toLocaleTimeString([], {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
      });

      // Only push a new point each second (deduplicate same-second ticks)
      if (label === lastLabel) {
        // Same second — just update the last point in place
        if (livePrices.length > 0) {
          livePrices[livePrices.length - 1] = price;
        }
      } else {
        // New second — append a new candle point
        lastLabel = label;
        livePrices.push(price);
        liveLabels.push(label);
        // Rolling window: trim oldest when full
        if (livePrices.length > LIVE_MAX_PTS) {
          livePrices.shift();
          liveLabels.shift();
        }
      }

      // Color: compare latest price to first visible point
      const first = livePrices[0];
      const isUp  = price >= first;
      const color = isUp ? '#00e87a' : '#ff4466';

      if (mainChartInst) {
        mainChartInst.data.labels              = liveLabels.slice();
        mainChartInst.data.datasets[0].data    = livePrices.slice();
        mainChartInst.data.datasets[0].borderColor = color;

        const c2d      = document.getElementById('mainChart').getContext('2d');
        const gradient = c2d.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, isUp ? 'rgba(0,232,122,.2)' : 'rgba(255,68,102,.2)');
        gradient.addColorStop(1, 'transparent');
        mainChartInst.data.datasets[0].backgroundColor = gradient;

        mainChartInst.update('none');
      }

      // Flash price in strip
      const prevPriceEl = document.getElementById('lsPrice');
      const prevRaw     = prevPriceEl ? parseFloat(prevPriceEl.dataset.raw || price) : price;
      const dir         = price > prevRaw ? 'up' : price < prevRaw ? 'dn' : null;
      setLiveVal('lsPrice', fmt(price), dir);
      if (prevPriceEl) prevPriceEl.dataset.raw = price;

      // Flash hero price in detail header
      const heroPrice = document.querySelector('.d-price');
      if (heroPrice) heroPrice.textContent = fmt(price);

      // Clock
      const lsTime = document.getElementById('lsTime');
      if (lsTime) lsTime.textContent = label;

    }, 1000);

  } catch (err) {
    toast('WebSocket unavailable', 'err');
    stopLive();
  }
}

function stopLive() {
  isLive = false;

  clearInterval(liveTimer);
  clearInterval(liveUpdateTimer);
  liveTimer      = null;
  liveUpdateTimer = null;
  pendingPrice   = null;

  if (liveWs) { try { liveWs.close(); } catch(_){} liveWs = null; }

  const liveBtn   = document.getElementById('liveBtn');
  const liveStrip = document.getElementById('liveStrip');
  if (liveBtn)   liveBtn.classList.remove('on');
  if (liveStrip) liveStrip.classList.remove('visible');

  // Restore the normal chart
  drawChart(currentDays);
}

/* Build the live line chart seeded with real historical data */
function buildLiveChart() {
  if (mainChartInst) { mainChartInst.destroy(); mainChartInst = null; }
  const canvas = document.getElementById('mainChart');
  if (!canvas) return;

  // Color based on actual price direction from seeded data
  const first = livePrices[0] || 0;
  const last  = livePrices[livePrices.length - 1] || 0;
  const isUp  = last >= first;
  const color = isUp ? '#00e87a' : '#ff4466';

  const c2d      = canvas.getContext('2d');
  const gradient = c2d.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, isUp ? 'rgba(0,232,122,.2)' : 'rgba(255,68,102,.2)');
  gradient.addColorStop(1, 'transparent');

  mainChartInst = new Chart(c2d, {
    type: 'line',
    data: {
      labels: liveLabels.slice(),
      datasets: [{
        data:             livePrices.slice(),
        borderColor:      color,
        borderWidth:      2,
        pointRadius:      0,
        pointHoverRadius: 4,
        pointHoverBackgroundColor: color,
        fill:             true,
        backgroundColor:  gradient,
        tension:          0.3
      }]
    },
    options: {
      responsive:          true,
      maintainAspectRatio: true,
      animation:           { duration: 0 },
      interaction:         { intersect: false, mode: 'index' },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0c1120',
          borderColor:     'rgba(255,255,255,.1)',
          borderWidth:     1,
          titleColor:      '#8892a4',
          bodyColor:       '#e8edf7',
          bodyFont:        { family: 'Space Mono', size: 11 },
          callbacks: {
            label: ctx => ' $' + ctx.raw.toLocaleString('en-US', {
              minimumFractionDigits: 2, maximumFractionDigits: 8
            })
          }
        }
      },
      scales: {
        x: {
          grid:   { color: 'rgba(255,255,255,.04)' },
          ticks:  { color: '#4e5a6e', font: { family: 'Space Mono', size: 10 }, maxTicksLimit: 6 },
          border: { display: false }
        },
        y: {
          position: 'right',
          grid:   { color: 'rgba(255,255,255,.04)' },
          ticks:  {
            color: '#4e5a6e',
            font:  { family: 'Space Mono', size: 10 },
            callback: v => '$' + v.toLocaleString('en-US', { notation: 'compact', maximumFractionDigits: 4 })
          },
          border: { display: false }
        }
      }
    }
  });
}

/* Fill the live stats strip */
function fillStrip(coin) {
  const chg = coin.price_change_percentage_24h || 0;
  setLiveVal('lsPrice',  fmt(coin.current_price), chg >= 0 ? 'up' : 'dn');
  setLiveVal('lsChange',
    `${chg >= 0 ? '▲' : '▼'} ${Math.abs(chg).toFixed(2)}%`,
    chg >= 0 ? 'up' : 'dn'
  );
  setLiveVal('lsMcap', fmtK(coin.market_cap));
  setLiveVal('lsVol',  fmtK(coin.total_volume));
  const lsPrice = document.getElementById('lsPrice');
  if (lsPrice) lsPrice.dataset.raw = coin.current_price;
}

async function refreshStrip() {
  if (!STATE.currentCoin || !isLive) return;
  try {
    const res  = await fetch(`https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${STATE.currentCoin}`);
    const data = await res.json();
    if (data[0]) fillStrip(data[0]);
  } catch(_) {}
}

function setLiveVal(id, text, dir) {
  const el = document.getElementById(id);
  if (!el) return;
  const prev = el.textContent;
  el.textContent = text;
  if (dir && prev !== text) {
    el.classList.remove('flash-up', 'flash-dn');
    void el.offsetWidth;
    el.classList.add(dir === 'up' ? 'flash-up' : 'flash-dn');
    setTimeout(() => el.classList.remove('flash-up','flash-dn'), 900);
  }
}

async function drawChart(days, btn) {
  if (!STATE.currentCoin) return;
  if (btn) {
    document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  try {
    const data   = await fetchChart(STATE.currentCoin, days);
    const prices = data.prices;
    const labels = prices.map(p => {
      const d = new Date(p[0]);
      if (days <= 1)  return d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
      if (days <= 30) return d.toLocaleDateString([],{month:'short',day:'numeric'});
      return d.toLocaleDateString([],{month:'short',year:'2-digit'});
    });
    const vals  = prices.map(p => p[1]);
    const isUp  = vals[vals.length-1] >= vals[0];
    const color = isUp ? '#00e87a' : '#ff4466';

    if (mainChartInst) { mainChartInst.destroy(); mainChartInst = null; }
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;
    const c2d      = ctx.getContext('2d');
    const gradient = c2d.createLinearGradient(0,0,0,300);
    gradient.addColorStop(0, isUp?'rgba(0,232,122,.2)':'rgba(255,68,102,.2)');
    gradient.addColorStop(1, 'transparent');

    mainChartInst = new Chart(c2d, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          data: vals, borderColor: color, borderWidth: 2,
          pointRadius: 0, pointHoverRadius: 5, pointHoverBackgroundColor: color,
          fill: true, backgroundColor: gradient, tension: 0.3
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: true,
        interaction: { intersect:false, mode:'index' },
        plugins: {
          legend: { display:false },
          tooltip: {
            backgroundColor:'#0c1120', borderColor:'rgba(255,255,255,.1)', borderWidth:1,
            titleColor:'#8892a4', bodyColor:'#e8edf7',
            bodyFont:{ family:'Space Mono',size:11 },
            callbacks:{
              label: ctx => ' $'+ctx.raw.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:8})
            }
          }
        },
        scales: {
          x: {
            grid:  { color:'rgba(255,255,255,.04)' },
            ticks: { color:'#4e5a6e', font:{family:'Space Mono',size:10}, maxTicksLimit:8 },
            border:{ display:false }
          },
          y: {
            position:'right',
            grid:  { color:'rgba(255,255,255,.04)' },
            ticks: { color:'#4e5a6e', font:{family:'Space Mono',size:10},
              callback: v => '$'+v.toLocaleString('en-US',{notation:'compact',maximumFractionDigits:4}) },
            border:{ display:false }
          }
        }
      }
    });
  } catch(e) {
    toast('Chart failed — API rate limited, wait a moment', 'err');
  }
}

/* ===========================
   SKELETON
   =========================== */
function renderSkeletons() {
  const tbody = document.getElementById('mktTbody');
  if (!tbody) return;
  tbody.innerHTML = Array.from({length:10}).map(() => `
    <tr>
      <td><div class="sk" style="width:22px;height:13px"></div></td>
      <td>
        <div style="display:flex;align-items:center;gap:12px">
          <div class="sk sk-circle" style="width:30px;height:30px;flex-shrink:0"></div>
          <div>
            <div class="sk" style="width:90px;height:13px;margin-bottom:5px"></div>
            <div class="sk" style="width:45px;height:11px"></div>
          </div>
        </div>
      </td>
      <td class="rt"><div class="sk" style="width:70px;height:13px;margin-left:auto"></div></td>
      <td class="rt"><div class="sk" style="width:50px;height:13px;margin-left:auto"></div></td>
      <td class="rt col-cap"><div class="sk" style="width:75px;height:13px;margin-left:auto"></div></td>
      <td class="rt col-vol"><div class="sk" style="width:65px;height:13px;margin-left:auto"></div></td>
      <td></td>
    </tr>
  `).join('');
}

/* ===========================
   SEARCH
   =========================== */
function setupSearch() {
  const input = document.getElementById('globalSearch');
  const drop  = document.getElementById('searchDrop');
  if (!input || !drop) return;
  let timer;

  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      const q = input.value.trim().toLowerCase();
      if (!q || !STATE.coins.length) { drop.classList.remove('open'); return; }
      const res = STATE.coins.filter(c =>
        c.name.toLowerCase().includes(q) || c.symbol.toLowerCase().includes(q)
      ).slice(0,8);
      if (!res.length) { drop.classList.remove('open'); return; }
      drop.innerHTML = res.map(c => `
        <div class="sd-item" onclick="pickCoin('${c.id}')">
          <img src="${c.image}" alt="" loading="lazy">
          <div><div class="sdi-n">${c.name}</div><div class="sdi-s">${c.symbol.toUpperCase()}</div></div>
          <div class="sdi-p">${fmt(c.current_price)}</div>
        </div>`).join('');
      drop.classList.add('open');
    }, 200);
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.search-wrap')) drop.classList.remove('open');
  });
}

function pickCoin(id) {
  const input = document.getElementById('globalSearch');
  const drop  = document.getElementById('searchDrop');
  if (input) input.value = '';
  if (drop)  drop.classList.remove('open');
  openCoin(id);
}

/* ===========================
   NAVIGATION SETUP
   =========================== */
function setupNav() {
  const hamburger = document.getElementById('hamburger');
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('sideOverlay');

  if (hamburger && sidebar && overlay) {
    hamburger.addEventListener('click', () => {
      const isOpen = sidebar.classList.contains('open');
      if (isOpen) {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      } else {
        sidebar.classList.add('open');
        overlay.classList.add('open');
        hamburger.setAttribute('aria-expanded', 'true');
      }
    });
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  }
}

function closeSidebar() {
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('sideOverlay');
  const hamburger = document.getElementById('hamburger');
  if (sidebar)   sidebar.classList.remove('open');
  if (overlay)   overlay.classList.remove('open');
  if (hamburger) hamburger.setAttribute('aria-expanded','false');
}

/* ===========================
   PAGE NAVIGATION
   =========================== */
function showPage(name) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById('page-' + name);
  if (target) target.classList.add('active');

  STATE.page = name;

  // Sync all nav buttons (navbar tabs, sidebar buttons, bottom bar)
  document.querySelectorAll('[data-page]').forEach(b => {
    b.classList.toggle('active', b.dataset.page === name);
  });

  closeSidebar();
  window.scrollTo({ top:0, behavior:'smooth' });

  if (name !== 'detail' && isLive) stopLive();
  if (name === 'market')    renderMarket();
  if (name === 'watchlist') renderWatchlist();
}

function goBack() {
  showPage(STATE.prevPage || 'dashboard');
}

/* ===========================
   MANUAL REFRESH
   =========================== */
function manualRefresh() {
  toast('Refreshing prices…','inf');
  refresh();
}

/* ===========================
   FORMATTERS
   =========================== */
function fmt(n) {
  if (n == null) return '—';
  const opts = n >= 1000 ? {minimumFractionDigits:2,maximumFractionDigits:2}
             : n >= 1    ? {minimumFractionDigits:2,maximumFractionDigits:4}
             :              {minimumFractionDigits:2,maximumFractionDigits:8};
  return '$' + n.toLocaleString('en-US', opts);
}
function fmtK(n) {
  if (!n) return '—';
  if (n >= 1e12) return '$'+(n/1e12).toFixed(2)+'T';
  if (n >= 1e9)  return '$'+(n/1e9).toFixed(2)+'B';
  if (n >= 1e6)  return '$'+(n/1e6).toFixed(2)+'M';
  return '$'+n.toLocaleString('en-US');
}

/* ===========================
   TOAST
   =========================== */
function toast(msg, type='inf') {
  const el   = document.getElementById('toast');
  if (!el) return;
  const icon = type==='ok'?'✓':type==='err'?'✕':'ℹ';
  el.className = `toast t-${type} show`;
  el.innerHTML = `<span>${icon}</span>${msg}`;
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 3200);
}

/* ===========================
   BOOT
   =========================== */
document.addEventListener('DOMContentLoaded', init);