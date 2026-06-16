CommuteWise
CommuteWise is a public transit route recommendation system for Chennai, India. It helps commuters find the most suitable route between two locations by analysing metro, suburban rail, and bus options — balancing travel time, cost, reliability, and carbon emissions.
The system uses a graph-based routing algorithm (Dijkstra's) over a transit network of approximately 1,400 stops and a trained Random Forest model to predict real-time delays based on current weather conditions. Routes are scored and ranked so users can filter by preference: best overall, fastest, greenest, or cheapest.

Tech Stack
Backend
Python 3 with FastAPI
Dijkstra's algorithm over a Chennai transit graph (metro, suburban rail, bus)
Random Forest model (random_reg_model.pkl) for delay prediction
Open-Meteo API for live weather data
Nominatim (geopy) for address geocoding
Frontend
Plain HTML, CSS, and JavaScript — no frameworks
Communicates with the backend via POST /api/routes

Project Structure
CommuteWise/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database/                # Transit graph data and graph builder scripts
│   ├── routes/
│   │   ├── route_functions.py   # Core routing pipeline
│   │   ├── routes.py            # Route model and scoring
│   │   └── delay_model.py       # ML delay prediction
│   └── location.py              # Geocoding via Nominatim
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   ├── js/
│   │   ├── app.js               # UI logic and rendering
│   │   └── data.js              # API calls to backend
│   └── assets/
├── ml-models/                   # Training datasets and model file
└── random_reg_model.pkl         # Trained delay prediction model


Running Locally
Prerequisites
Python 3.10 or later
pip3
A modern web browser
A local HTTP server (Python's built-in one is sufficient)
1. Clone the repository
git clone https://github.com/siddharthbuilds/CommuteWise.git
cd CommuteWise

2. Install Python dependencies
pip3 install fastapi uvicorn geopy requests scikit-learn pandas numpy

On macOS with Python 3.12+, SSL certificate errors from Nominatim can occur. Fix with:
/Applications/Python\ 3.x/Install\ Certificates.command

Replace 3.x with your installed version.
3. Start the backend
cd backend
python3 -m uvicorn main:app --reload --port 8000

The API will be available at http://localhost:8000. Verify with:
curl http://localhost:8000/api/home

4. Start the frontend
Open a new terminal from the project root:
cd frontend
python3 -m http.server 3000

Then open http://localhost:3000 in your browser.
5. Using the app
Enter a source and destination (any Chennai address or landmark, e.g. Guindy and Anna Nagar)
Select a date and time
Click Find Best Routes
Use the filter panel to sort by preference
Click View Details on any route card to see the full stop-by-stop breakdown
