// ── Swap ───────────────────────────────────────────────────────────────────
function swapLocations() {
  const src = document.getElementById('source');
  const dst = document.getElementById('destination');
  [src.value, dst.value] = [dst.value, src.value];
}

// ── Default datetime ───────────────────────────────────────────────────────
function setDefaultDatetime() {
  const now = new Date();
  now.setHours(8, 0, 0, 0);
  document.getElementById('datetime').value =
    new Date(now - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
}

// ── Badge helpers ──────────────────────────────────────────────────────────
const BADGE_CLASS = { Best: 'badge-best', Fastest: 'badge-fastest', Safest: 'badge-greenest', Cheapest: 'badge-cheapest' };
const BADGE_LABEL = { Best: '🏆 Best', Fastest: '⚡ Fastest', Safest: '🛡️ Safest', Cheapest: '💰 Cheapest' };
const CARD_CLASS  = { Best: 'best', Fastest: 'fastest', Safest: 'greenest', Cheapest: 'cheapest' };

function primaryBadge(badges) {
  for (const b of ['Best', 'Fastest', 'Safest', 'Cheapest']) {
    if (badges.includes(b)) return b;
  }
  return null;
}

// ── Global segment store for modal ────────────────────────────────────────
let _routeStore = [];

function showRouteDetail(idx) {
  const r = _routeStore[idx];
  if (!r) return;
  document.getElementById('pathContent').innerHTML = `
    <div style="display:flex;flex-direction:column;gap:10px;">
      <div class="detail-row"><span class="detail-label">Mode</span><span>${r.mode}</span></div>
      <div class="detail-row"><span class="detail-label">Distance</span><span>${r.distance} km</span></div>
      <div class="detail-row"><span class="detail-label">Duration</span><span>${r.duration} min</span></div>
      <div class="detail-row"><span class="detail-label">Cost</span><span>₹${r.expenditure}</span></div>
      <div class="detail-row"><span class="detail-label">Expected Delay</span><span>${r.timedelay} min</span></div>
      <div class="detail-row"><span class="detail-label">Carbon Rate</span><span>${r.carbonrate} kg CO₂</span></div>
      <div class="detail-row"><span class="detail-label">Rating</span><span>${r.rating}/10</span></div>
      <div class="detail-row"><span class="detail-label">Badges</span><span>${r.badges.length ? r.badges.join(', ') : '—'}</span></div>
    </div>`;
  document.getElementById('pathModal').style.display = 'flex';
}

// ── Render route cards ─────────────────────────────────────────────────────
let currentRoutes = [];
let activeSortKey = 'rating';

function renderCards(routes, sortKey) {
  activeSortKey = sortKey;

  const sorted = [...routes].sort((a, b) => {
    if (sortKey === 'rating')      return b.rating - a.rating;
    if (sortKey === 'duration')    return a.duration - b.duration;
    if (sortKey === 'carbonrate')  return a.carbonrate - b.carbonrate;
    if (sortKey === 'expenditure') return a.expenditure - b.expenditure;
    return 0;
  });

  _routeStore = sorted;

  const maxDur  = Math.max(...routes.map(r => r.duration));
  const maxCO2  = Math.max(...routes.map(r => r.carbonrate));
  const maxCost = Math.max(...routes.map(r => r.expenditure));

  const modeIcon = { Metro: '🚇', Bus: '🚌', Rail: '🚆', Walk: '🚶', Auto: '🛺' };

  document.getElementById('routeCards').innerHTML = sorted.map((r, idx) => {
    const pb = primaryBadge(r.badges);
    const cardCls = pb ? CARD_CLASS[pb] : '';
    const pctLess = Math.round(((2.1 - r.carbonrate) / 2.1) * 100);

    return `
      <div class="route-card ${cardCls}">
        ${pb ? `<span class="card-badge ${BADGE_CLASS[pb]}">${BADGE_LABEL[pb]}</span>` : '<span class="card-badge" style="visibility:hidden">—</span>'}
        <div class="card-mode-row">
          <span class="mode-chip">${modeIcon[r.mode] || '🚌'} ${r.mode}</span>
        </div>
        <div class="card-duration">${r.duration} min</div>

        <div class="card-metric">
          <div class="metric-label">Rating</div>
          <div class="progress-bar"><div class="progress-fill fill-green" style="width:${r.rating * 10}%"></div></div>
          <div class="metric-value">${r.rating}/10</div>
        </div>
        <div class="card-metric">
          <div class="metric-label">Travel Time</div>
          <div class="progress-bar"><div class="progress-fill fill-blue" style="width:${Math.round(r.duration / maxDur * 100)}%"></div></div>
          <div class="metric-value">${r.duration} min</div>
        </div>
        <div class="card-metric">
          <div class="metric-label">CO₂ Emissions</div>
          <div class="progress-bar"><div class="progress-fill fill-green" style="width:${Math.round(r.carbonrate / maxCO2 * 100)}%"></div></div>
          <div class="metric-value">${r.carbonrate} kg 🌿</div>
        </div>
        <div class="card-metric">
          <div class="metric-label">Cost</div>
          <div class="progress-bar"><div class="progress-fill fill-orange" style="width:${Math.round(r.expenditure / maxCost * 100)}%"></div></div>
          <div class="metric-value">₹${r.expenditure}</div>
        </div>

        <div class="card-score">Distance: <span>${r.distance} km</span> · Delay: <span>+${r.timedelay} min</span></div>
        ${r.badges.length ? `<div class="mode-breakdown">${r.badges.map(b => `<span class="mode-tag ${(b).toLowerCase()}">${BADGE_LABEL[b] || b}</span>`).join('')}</div>` : ''}
        <button class="view-btn" onclick="showRouteDetail(${idx})">View Details →</button>
      </div>`;
  }).join('');
}

// ── Render insights ────────────────────────────────────────────────────────
function renderInsights(routes) {
  const best = routes.find(r => r.badges.includes('Best')) || routes[0];
  const fastest = routes.find(r => r.badges.includes('Fastest')) || routes[0];
  const cheapest = routes.find(r => r.badges.includes('Cheapest')) || routes[0];
  const pctLess = Math.round(((2.1 - best.carbonrate) / 2.1) * 100);

  const insights = [
    { icon: 'fa-star',        text: `Best route: ${best.mode}, ${best.duration} min, rated ${best.rating}/10.` },
    { icon: 'fa-bolt',        text: `Fastest option: ${fastest.mode} at ${fastest.duration} min (+${fastest.timedelay} min delay).` },
    { icon: 'fa-indian-rupee-sign', text: `Cheapest option: ${cheapest.mode} at ₹${cheapest.expenditure}.` },
    { icon: 'fa-leaf',        text: `Best route emits ${best.carbonrate} kg CO₂ — ${pctLess > 0 ? pctLess + '% less than driving' : 'comparable to driving'}.` },
  ];

  document.getElementById('insightsList').innerHTML = insights.map(i =>
    `<li><i class="fa-solid ${i.icon}"></i> ${i.text}</li>`
  ).join('');
}

// ── Render impact ──────────────────────────────────────────────────────────
function renderImpact(routes) {
  const best = routes.find(r => r.badges.includes('Best')) || routes[0];
  const pctLess = Math.round(((2.1 - best.carbonrate) / 2.1) * 100);
  const trees = Math.max(1, Math.round((2.1 - best.carbonrate) / 0.35));

  document.getElementById('impactStats').innerHTML = `
    <div>
      <div class="metric-label">Best Route CO₂</div>
      <div class="impact-num">${best.carbonrate} kg</div>
      <div class="metric-label" style="color:#4caf63">via ${best.mode}</div>
    </div>
    <div class="impact-stat-row">
      <div class="metric-label">Compared to Driving</div>
      <div class="impact-compare">↓ ${pctLess > 0 ? pctLess + '%' : '~0%'} less emissions</div>
    </div>
    <div>
      <div class="metric-label">Trees Equivalent</div>
      <div class="impact-num">${trees} Tree${trees !== 1 ? 's' : ''}</div>
      <div class="metric-label">per commute</div>
    </div>`;
}

// ── Filters — set up once ──────────────────────────────────────────────────
document.querySelectorAll('.filter-option').forEach(opt => {
  opt.addEventListener('click', () => {
    if (!currentRoutes.length) return;
    document.querySelectorAll('.filter-option').forEach(o => o.classList.remove('active'));
    opt.classList.add('active');
    renderCards(currentRoutes, opt.dataset.sort);
  });
});

// ── Error / loading ────────────────────────────────────────────────────────
function showError(msg) {
  document.getElementById('errorBanner').textContent = msg;
  document.getElementById('errorBanner').style.display = 'block';
  document.getElementById('resultsSection').style.display = 'none';
  document.getElementById('whySection').style.display = 'block';
}

function setLoading(text) {
  const btn = document.querySelector('.find-btn');
  if (text) {
    btn.textContent = text;
    btn.disabled = true;
  } else {
    btn.innerHTML = 'Find Best Routes <i class="fa-solid fa-arrow-right"></i>';
    btn.disabled = false;
  }
}

// ── Form submit ────────────────────────────────────────────────────────────
document.getElementById('searchForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const srcVal = document.getElementById('source').value.trim();
  const dstVal = document.getElementById('destination').value.trim();
  const dtVal  = document.getElementById('datetime').value;
  if (!srcVal || !dstVal) return;

  const date = dtVal ? dtVal.slice(0, 10) : new Date().toISOString().slice(0, 10);
  const time = dtVal ? dtVal.slice(11, 16) : '08:00';

  document.getElementById('errorBanner').style.display = 'none';
  setLoading('Finding routes…');

  try {
    const data = await fetchRoutes(srcVal, dstVal, date, time);
    setLoading('');

    if (!data.routes || !data.routes.length) {
      showError(`No routes found between "${srcVal}" and "${dstVal}".`);
      return;
    }

    currentRoutes = data.routes;

    // Reset filter to Best Overall
    document.querySelectorAll('.filter-option').forEach(o => o.classList.remove('active'));
    document.querySelector('[data-sort="rating"]').classList.add('active');

    document.getElementById('whySection').style.display = 'none';
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    renderCards(currentRoutes, 'rating');
    renderInsights(currentRoutes);
    renderImpact(currentRoutes);

    // Update map area
    document.querySelector('.map-placeholder').innerHTML = `
      <div class="map-label">Route Overview</div>
      <p style="font-size:0.82rem;color:#444;">${srcVal} → ${dstVal}</p>
      <p style="font-size:0.75rem;color:#888;margin-top:4px;">${data.routes.length} route${data.routes.length !== 1 ? 's' : ''} found · Google Maps integration coming soon</p>`;

  } catch (err) {
    setLoading('');
    if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
      showError('Cannot reach the backend. Make sure the FastAPI server is running at http://localhost:8000');
    } else {
      showError(`Error: ${err.message}`);
    }
  }
});

// ── Modal close ────────────────────────────────────────────────────────────
document.getElementById('pathModal').addEventListener('click', function (e) {
  if (e.target === this) this.style.display = 'none';
});

// ── Init ───────────────────────────────────────────────────────────────────
setDefaultDatetime();
