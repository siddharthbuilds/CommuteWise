// ── State ──────────────────────────────────────────────────────────────────
let WEIGHTED_GRAPH = null;
let ALL_COORDS     = null;
let NODE_MODE      = null;
let ALL_STOPS      = [];

async function loadGraphData() {
  if (WEIGHTED_GRAPH) return;
  const [wgRes, coordsRes, modeRes] = await Promise.all([
    fetch('assets/weighted_graph.json'),
    fetch('assets/all_coords.json'),
    fetch('assets/node_mode.json')
  ]);
  WEIGHTED_GRAPH = await wgRes.json();
  ALL_COORDS     = await coordsRes.json();
  NODE_MODE      = await modeRes.json();
  ALL_STOPS      = Object.keys(WEIGHTED_GRAPH).sort();
}

// ── Geocoding (Nominatim — same as geopy) ─────────────────────────────────
async function geocode(query) {
  const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query + ', Chennai')}&format=json&limit=1`;
  const res = await fetch(url, { headers: { 'Accept-Language': 'en' } });
  const data = await res.json();
  if (!data.length) return null;
  return { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
}

// ── Haversine ──────────────────────────────────────────────────────────────
function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 +
            Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// ── Nearest nodes (mirrors djikstra.py nearest_nodes) ─────────────────────
function nearestNodes(lat, lon, k = 5) {
  const distances = Object.entries(ALL_COORDS).map(([node, [nlat, nlon]]) => ({
    node, d: haversine(lat, lon, nlat, nlon)
  }));
  distances.sort((a, b) => a.d - b.d);
  return distances.slice(0, k).map(x => x.node);
}

// ── Dijkstra (mirrors djikstra.py dijkstra + get_candidate_routes) ─────────
function dijkstra(graph, source, destination) {
  if (!graph[source] || !graph[destination]) return null;

  const dist   = {};
  const parent = {};
  const visited = new Set();

  for (const node of Object.keys(graph)) dist[node] = Infinity;
  dist[source] = 0;

  // Min-heap via sorted array (good enough for 1458 nodes)
  const pq = [[0, source]];

  while (pq.length) {
    pq.sort((a, b) => a[0] - b[0]);
    const [curDist, curNode] = pq.shift();

    if (visited.has(curNode)) continue;
    visited.add(curNode);

    if (curNode === destination) break;

    for (const edge of (graph[curNode] || [])) {
      const weight = edge.mode === 'walk'
        ? Math.max(edge.cost, 0.05) * 3
        : edge.cost;
      const newDist = curDist + weight;
      if (newDist < dist[edge.to]) {
        dist[edge.to] = newDist;
        parent[edge.to] = { from: curNode, edge };
        pq.push([newDist, edge.to]);
      }
    }
  }

  if (dist[destination] === Infinity) return null;

  // Reconstruct segments
  const segments = [];
  let cur = destination;
  while (cur !== source) {
    const { from, edge } = parent[cur];
    segments.push({ from, to: cur, mode: edge.mode, distance: edge.distance });
    cur = from;
  }
  segments.reverse();
  return { segments, totalCost: dist[destination] };
}

// ── Get k candidate routes (penalise used edges) ───────────────────────────
function getCandidateRoutes(src, dst, k = 4) {
  // Deep clone only the cost values we'll modify
  const costOverride = {};  // key: "nodeA|nodeB", value: multiplier

  const routes = [];
  for (let i = 0; i < k; i++) {
    // Build graph view with overrides
    const graphView = {};
    for (const [node, edges] of Object.entries(WEIGHTED_GRAPH)) {
      graphView[node] = edges.map(e => {
        const key = `${node}|${e.to}`;
        const mult = costOverride[key] || 1;
        return { ...e, cost: e.cost * mult };
      });
    }

    const result = dijkstra(graphView, src, dst);
    if (!result) break;
    routes.push(result);

    // Penalise edges on this path
    for (const seg of result.segments) {
      const key = `${seg.from}|${seg.to}`;
      costOverride[key] = (costOverride[key] || 1) * 1.5;
    }
  }
  return routes;
}

// ── Find routes from lat/lon pair ──────────────────────────────────────────
function findRoutes(srcLat, srcLon, dstLat, dstLon) {
  const srcCandidates = nearestNodes(srcLat, srcLon, 3);
  const dstCandidates = nearestNodes(dstLat, dstLon, 3);

  const allRoutes = [];
  for (const src of srcCandidates) {
    for (const dst of dstCandidates) {
      const routes = getCandidateRoutes(src, dst, 2);
      allRoutes.push(...routes);
    }
  }
  allRoutes.sort((a, b) => a.totalCost - b.totalCost);
  return allRoutes.slice(0, 4);
}

// ── Summarise segments into route card data ────────────────────────────────
function summariseRoute(result, idx) {
  const { segments } = result;

  let totalDist = 0, walkDist = 0, busDist = 0, railDist = 0, metroDist = 0;
  let transfers = 0;
  let prevMode = null;
  const modes = new Set();

  for (const seg of segments) {
    const d = Math.max(seg.distance, 0.05);
    totalDist += d;
    if (seg.mode === 'walk')  walkDist  += d;
    else if (seg.mode === 'bus')   busDist   += d;
    else if (seg.mode === 'rail')  railDist  += d;
    else if (seg.mode === 'metro') metroDist += d;
    if (seg.mode !== 'walk') modes.add(seg.mode);
    if (prevMode && prevMode !== seg.mode && seg.mode !== 'walk') transfers++;
    prevMode = seg.mode;
  }

  // Mode label
  const modeArr = [];
  if (metroDist > 0) modeArr.push('Metro');
  if (railDist  > 0) modeArr.push('Rail');
  if (busDist   > 0) modeArr.push('Bus');
  const modeLabel = modeArr.length ? modeArr.join(' + ') : 'Bus';

  // Speed assumptions: metro 35 km/h, rail 40 km/h, bus 18 km/h, walk 4 km/h
  const duration = Math.round(
    metroDist/(35/60) + railDist/(40/60) + busDist/(18/60) + walkDist/(4/60)
  );

  const co2 = parseFloat(
    (metroDist*0.04 + railDist*0.03 + busDist*0.08 + walkDist*0).toFixed(2)
  );

  // Cost: metro ₹10-40, rail ₹5-30, bus ₹5-25
  const cost = Math.round(
    metroDist*3.2 + railDist*2.0 + busDist*2.5 + transfers*5 + 10
  );

  const reliability = Math.max(55, 92 - transfers*7 - (busDist > 5 ? 8 : 0));

  const path = [segments[0].from, ...segments.map(s => s.to)];

  const BADGES = ['best','fastest','greenest','cheapest'];
  const badge  = BADGES[idx] || 'best';

  return {
    mode: modeLabel,
    lineCode: modeArr[0] ? modeArr[0].slice(0,3).toUpperCase() : 'BUS',
    duration,
    reliability,
    carbonrate: co2,
    expenditure: cost,
    distance: parseFloat(totalDist.toFixed(1)),
    timedelay: transfers * 3 + 2,
    transfers,
    stops: segments.length,
    path,
    segments,
    badges: [badge],
    modeBreakdown: { walk: walkDist, bus: busDist, rail: railDist, metro: metroDist }
  };
}

// ── Fuzzy autocomplete ─────────────────────────────────────────────────────
function fuzzyMatch(query, limit = 8) {
  const q = query.toLowerCase();
  return ALL_STOPS.filter(s => s.toLowerCase().includes(q)).slice(0, limit);
}
