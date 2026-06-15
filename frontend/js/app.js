// ── Autocomplete ───────────────────────────────────────────────────────────
function setupAutocomplete(inputId) {
  const input = document.getElementById(inputId);
  let dropdown = document.getElementById(inputId + '-suggestions');
  if (!dropdown) {
    dropdown = document.createElement('ul');
    dropdown.id = inputId + '-suggestions';
    dropdown.className = 'autocomplete-list';
    input.parentElement.appendChild(dropdown);
  }
  input.addEventListener('input', () => {
    dropdown.innerHTML = '';
    const q = input.value.trim();
    if (q.length < 2 || !ALL_STOPS.length) return;
    fuzzyMatch(q).forEach(stop => {
      const li = document.createElement('li');
      li.textContent = stop;
      li.addEventListener('mousedown', () => { input.value = stop; dropdown.innerHTML = ''; });
      dropdown.appendChild(li);
    });
  });
  input.addEventListener('blur', () => setTimeout(() => dropdown.innerHTML = '', 150));
}

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

// ── Global segment store (avoids JSON-in-onclick issues) ───────────────────
let _segmentStore = [];

function showPath(idx) {
  const segments = _segmentStore[idx];
  if (!segments) return;
  const modeIcon = { metro: '🚇', rail: '🚆', bus: '🚌', walk: '🚶' };
  const rows = [
    `<div class="path-stop"><span class="path-dot start"></span><span class="path-mode">${modeIcon[segments[0].mode] || '🚌'}</span><span>${segments[0].from}</span></div>`
  ];
  for (const seg of segments) {
    rows.push(`<div class="path-stop"><span class="path-dot"></span><span class="path-mode">${modeIcon[seg.mode] || '🚌'}</span><span>${seg.to}</span></div>`);
  }
  document.getElementById('pathContent').innerHTML = rows.join('');
  document.getElementById('pathModal').style.display = 'flex';
}

// ── Render route cards ─────────────────────────────────────────────────────
let currentRoutes = [];
let activeSortKey = 'rating';

function renderCards(routes, sortKey) {
  activeSortKey = sortKey;
  const sorted = [...routes].sort((a, b) =>
    sortKey === 'rating' ? b.rating - a.rating : a[sortKey] - b[sortKey]
  );

  const maxDur  = Math.max(...routes.map(r => r.duration));
  const maxCO2  = Math.max(...routes.map(r => r.carbonrate));
  const maxCost = Math.max(...routes.map(r => r.expenditure));

  const badgeClass = { best: 'badge-best', fastest: 'badge-fastest', greenest: 'badge-greenest', cheapest: 'badge-cheapest' };
  const cardClass  = { best: 'best', fastest: 'fastest', greenest: 'greenest', cheapest: 'cheapest' };
  const badgeLabel = { best: '🏆 Best Overall', fastest: '⚡ Fastest', greenest: '🌿 Greenest', cheapest: '💰 Cheapest' };

  // Store segments globally; use index in onclick
  _segmentStore = sorted.map(r => r.segments);

  document.getElementById('routeCards').innerHTML = sorted.map((r, idx) => {
    const b = r.badges[0] || 'best';
    const bd = r.modeBreakdown;
    return `
      <div class="route-card ${cardClass[b] || ''}">
        <span class="card-badge ${badgeClass[b] || ''}">${badgeLabel[b] || ''}</span>
        <div class="card-mode-row"><span class="mode-chip">${r.lineCode}</span></div>
        <div class="card-title">${r.mode}</div>
        <div class="card-duration">${r.duration} min</div>
        <div class="card-metric">
          <div class="metric-label">Reliability</div>
          <div class="progress-bar"><div class="progress-fill fill-green" style="width:${r.reliability}%"></div></div>
          <div class="metric-value">${r.reliability}%</div>
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
        <div class="card-score">Score: <span>${r.rating}/100</span></div>
        <div class="card-stops">🚏 ${r.stops} stops · ${r.distance} km · ${r.transfers} transfer${r.transfers !== 1 ? 's' : ''}</div>
        <div class="mode-breakdown">
          ${bd.metro > 0 ? `<span class="mode-tag metro">🚇 Metro ${bd.metro.toFixed(1)}km</span>` : ''}
          ${bd.rail  > 0 ? `<span class="mode-tag rail">🚆 Rail ${bd.rail.toFixed(1)}km</span>`   : ''}
          ${bd.bus   > 0 ? `<span class="mode-tag bus">🚌 Bus ${bd.bus.toFixed(1)}km</span>`      : ''}
          ${bd.walk  > 0 ? `<span class="mode-tag walk">🚶 Walk ${(bd.walk * 1000).toFixed(0)}m</span>` : ''}
        </div>
        <button class="view-btn" onclick="showPath(${idx})">View Stop Details →</button>
      </div>`;
  }).join('');
}

// ── Render insights ────────────────────────────────────────────────────────
function renderInsights(routes) {
  const best = routes[0];
  const bd = best.modeBreakdown;
  const insights = [
    { icon: 'fa-circle-dot',           text: `${best.reliability}% on-time probability based on historical data.` },
    { icon: 'fa-route',                text: `${best.stops} stops, ${best.distance} km via ${best.mode}.` },
  ];
  if (best.transfers > 0)
    insights.push({ icon: 'fa-arrow-right-arrow-left', text: `${best.transfers} transfer${best.transfers > 1 ? 's' : ''} required. Allow 3–5 mins per transfer.` });
  if (bd.walk > 0)
    insights.push({ icon: 'fa-person-walking', text: `~${(bd.walk * 1000).toFixed(0)}m walking included in this route.` });
  insights.push({ icon: 'fa-leaf', text: `This route emits ${best.carbonrate} kg CO₂ — ${Math.round((1 - best.carbonrate / 2.1) * 100)}% less than driving.` });

  document.getElementById('insightsList').innerHTML = insights.map(i =>
    `<li><i class="fa-solid ${i.icon}"></i> ${i.text}</li>`
  ).join('');
}

// ── Render impact ──────────────────────────────────────────────────────────
function renderImpact(routes) {
  const best = routes[0];
  const pctLess = Math.round(((2.1 - best.carbonrate) / 2.1) * 100);
  const trees = Math.max(1, Math.round((2.1 - best.carbonrate) / 0.35));
  document.getElementById('impactStats').innerHTML = `
    <div>
      <div class="metric-label">Your Selected Route</div>
      <div class="impact-num">${best.carbonrate} kg CO₂</div>
      <div class="metric-label" style="color:#4caf63">Low Emission</div>
    </div>
    <div class="impact-stat-row">
      <div class="metric-label">Compared to Driving</div>
      <div class="impact-compare">↓ ${pctLess}% less emissions</div>
    </div>
    <div>
      <div class="metric-label">Trees Equivalent</div>
      <div class="impact-num">${trees} Tree${trees !== 1 ? 's' : ''}</div>
      <div class="metric-label">in one commute</div>
    </div>`;
}

// ── Render map area ────────────────────────────────────────────────────────
function renderMapArea(routes) {
  const best = routes[0];
  const preview = best.path.slice(0, 5).join(' → ') + (best.path.length > 5 ? ` → … (${best.path.length} stops)` : '');
  document.querySelector('.map-placeholder').innerHTML = `
    <div class="map-label">Route Path</div>
    <p style="font-size:0.82rem;padding:0 16px;color:#444;">${preview}</p>
    <p style="font-size:0.75rem;color:#888;margin-top:4px;">Google Maps integration coming soon</p>`;
}

// ── Filters — set up ONCE on page load, delegate via currentRoutes ─────────
document.querySelectorAll('.filter-option').forEach(opt => {
  opt.addEventListener('click', () => {
    if (!currentRoutes.length) return;
    document.querySelectorAll('.filter-option').forEach(o => o.classList.remove('active'));
    opt.classList.add('active');
    renderCards(currentRoutes, opt.dataset.sort);
  });
});

// ── Error / loading helpers ────────────────────────────────────────────────
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

// ── Assign ratings ─────────────────────────────────────────────────────────
function assignRatings(routes) {
  const maxDur  = Math.max(...routes.map(r => r.duration));
  const maxCost = Math.max(...routes.map(r => r.expenditure));
  const maxCO2  = Math.max(...routes.map(r => r.carbonrate));
  routes.forEach(r => {
    const durScore  = (1 - r.duration / maxDur)   * 35;
    const costScore = (1 - r.expenditure / maxCost) * 25;
    const co2Score  = (1 - r.carbonrate / maxCO2)   * 20;
    const relScore  = (r.reliability / 100)          * 20;
    r.rating = Math.round(durScore + costScore + co2Score + relScore);
  });

  // Assign badges based on actual best in each category
  const byDur  = [...routes].sort((a, b) => a.duration - b.duration);
  const byCO2  = [...routes].sort((a, b) => a.carbonrate - b.carbonrate);
  const byCost = [...routes].sort((a, b) => a.expenditure - b.expenditure);
  const byRate = [...routes].sort((a, b) => b.rating - a.rating);

  byRate[0].badges  = ['best'];
  byDur[0].badges   = byDur[0].badges[0]  === 'best' ? ['best']     : ['fastest'];
  byCO2[0].badges   = byCO2[0].badges[0]  === 'best' ? ['best']     : ['greenest'];
  byCost[0].badges  = byCost[0].badges[0] === 'best' ? ['best']     : ['cheapest'];

  // Any remaining without a badge get one
  const used = new Set(routes.map(r => r.badges[0]));
  const fallbacks = ['fastest', 'greenest', 'cheapest'];
  routes.forEach(r => {
    if (!r.badges.length) {
      const fb = fallbacks.find(f => !used.has(f));
      if (fb) { r.badges = [fb]; used.add(fb); }
    }
  });
}

// ── Form submit ────────────────────────────────────────────────────────────
document.getElementById('searchForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const srcVal = document.getElementById('source').value.trim();
  const dstVal = document.getElementById('destination').value.trim();
  if (!srcVal || !dstVal) return;

  document.getElementById('errorBanner').style.display = 'none';
  setLoading('Loading graph…');
  await loadGraphData();

  let srcLat, srcLon, dstLat, dstLon;
  let srcLabel = srcVal, dstLabel = dstVal;

  const exactSrc = ALL_STOPS.find(s => s.toLowerCase() === srcVal.toLowerCase());
  const exactDst = ALL_STOPS.find(s => s.toLowerCase() === dstVal.toLowerCase());

  if (exactSrc) {
    [srcLat, srcLon] = ALL_COORDS[exactSrc];
    srcLabel = exactSrc;
  } else {
    setLoading('Locating origin…');
    const geo = await geocode(srcVal);
    if (!geo) { setLoading(''); showError(`Could not locate "${srcVal}". Try a stop name from the autocomplete.`); return; }
    srcLat = geo.lat; srcLon = geo.lon;
  }

  if (exactDst) {
    [dstLat, dstLon] = ALL_COORDS[exactDst];
    dstLabel = exactDst;
  } else {
    setLoading('Locating destination…');
    const geo = await geocode(dstVal);
    if (!geo) { setLoading(''); showError(`Could not locate "${dstVal}". Try a stop name from the autocomplete.`); return; }
    dstLat = geo.lat; dstLon = geo.lon;
  }

  setLoading('Finding best routes…');
  await new Promise(r => setTimeout(r, 10));
  const rawRoutes = findRoutes(srcLat, srcLon, dstLat, dstLon);
  setLoading('');

  if (!rawRoutes.length) {
    showError(`No route found between "${srcLabel}" and "${dstLabel}".`);
    return;
  }

  currentRoutes = rawRoutes.map((r, i) => summariseRoute(r, i));
  assignRatings(currentRoutes);

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
  renderMapArea(currentRoutes);
});

// ── Modal close ────────────────────────────────────────────────────────────
document.getElementById('pathModal').addEventListener('click', function (e) {
  if (e.target === this) this.style.display = 'none';
});

// ── Init ───────────────────────────────────────────────────────────────────
setDefaultDatetime();
setupAutocomplete('source');
setupAutocomplete('destination');
loadGraphData();
