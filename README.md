# CommuteWise

**CommuteWise** is a public transit route recommendation system for Chennai, India. It helps commuters find the most suitable route between two locations by analyzing metro, suburban rail, and bus options while balancing travel time, cost, reliability, and carbon emissions.

The system uses a **graph-based routing algorithm (Dijkstra's Algorithm)** over a transit network of approximately **1,400 stops** and a trained **Random Forest model** to predict real-time delays based on current weather conditions.

Routes are scored and ranked so users can filter by preference:

- Best Overall
- Fastest
- Greenest
- Cheapest

---

# Tech Stack

## Backend

- Python 3
- FastAPI
- Dijkstra's Algorithm for route computation
- Random Forest Model (`random_reg_model.pkl`) for delay prediction
- Open-Meteo API for live weather data
- Nominatim (Geopy) for address geocoding

## Frontend

- HTML
- CSS
- JavaScript (Vanilla JS)
- Backend communication through `POST /api/routes`

---

# Project Structure

```text
CommuteWise/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database/                # Transit graph data and graph builder scripts
│   ├── routes/
│   │   ├── route_functions.py   # Core routing pipeline
│   │   ├── routes.py            # Route model and scoring
│   │   └── delay_model.py       # ML delay prediction
│   └── location.py              # Geocoding via Nominatim
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js               # UI logic and rendering
│   │   └── data.js              # API calls to backend
│   └── assets/
│
├── ml-models/                   # Training datasets and model file
└── random_reg_model.pkl         # Trained delay prediction model
