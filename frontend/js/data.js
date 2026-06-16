// ── Backend API call ────────────────────────────────────────────────────────
const API_BASE = 'http://localhost:8000';

async function fetchRoutes(source, destination, date, time) {
  const res = await fetch(`${API_BASE}/api/routes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source, destination, date, time })
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();  // { routes: [...] }
}

async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/home`);
    return res.ok;
  } catch {
    return false;
  }
}
