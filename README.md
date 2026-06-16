COMMUTEWISE

CommuteWise is a public transit route recommendation system for Chennai, India. It helps commuters find the most suitable route between two locations by analyzing metro, suburban rail, and bus options while balancing travel time, cost, reliability, and carbon emissions.

The system uses a graph-based routing algorithm (Dijkstra's Algorithm) over a transit network of approximately 1,400 stops and a trained Random Forest model to predict real-time delays based on current weather conditions.

Routes are scored and ranked so users can filter results based on their preferences:
• Best Overall
• Fastest
• Greenest
• Cheapest


TECH STACK

Backend
• Python 3
• FastAPI
• Dijkstra's Algorithm for route computation
• Random Forest Model (random_reg_model.pkl) for delay prediction
• Open-Meteo API for live weather data
• Nominatim (Geopy) for address geocoding

Frontend
• HTML
• CSS
• JavaScript (Vanilla JS)
• Backend communication through POST /api/routes


PROJECT STRUCTURE

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
│   ├── css/style.css
│   ├── js/
│   │   ├── app.js               # UI logic and rendering
│   │   └── data.js              # API calls to backend
│   └── assets/
│
├── ml-models/                   # Training datasets and model file
└── random_reg_model.pkl         # Trained delay prediction model


RUNNING LOCALLY

Prerequisites
• Python 3.10 or later
• pip3
• A modern web browser
• A local HTTP server (Python's built-in one is sufficient)


1. Clone the Repository

git clone https://github.com/siddharthbuilds/CommuteWise.git
cd CommuteWise


2. Install Dependencies

pip3 install fastapi uvicorn geopy requests scikit-learn pandas numpy

On macOS with Python 3.12+, SSL certificate errors from Nominatim can occur. Fix with:

/Applications/Python\ 3.x/Install\ Certificates.command

Replace 3.x with your installed version.


3. Start the Backend

cd backend
python3 -m uvicorn main:app --reload --port 8000

The API will be available at:

http://localhost:8000

Verify with:

curl http://localhost:8000/api/home


4. Start the Frontend

Open a new terminal from the project root:

cd frontend
python3 -m http.server 3000

Then open:

http://localhost:3000


5. Using the App

1. Enter a source and destination (any Chennai address or landmark, e.g. Guindy and Anna Nagar)

2. Select a date and time

3. Click "Find Best Routes"

4. Use the filter panel to sort by preference:
   • Best Overall
   • Fastest
   • Greenest
   • Cheapest

5. Click "View Details" on any route card to see:
   • Full stop-by-stop breakdown
   • Mode transitions
   • Predicted delays
   • Fare information
   • Environmental impact metrics


KEY FEATURES

• Multi-modal transit routing across metro, suburban rail, and bus networks
• Weather-aware delay prediction using a Random Forest model
• Intelligent route scoring based on time, cost, reliability, and emissions
• Personalized route recommendations optimized for speed, sustainability, budget, or overall convenience


FUTURE IMPROVEMENTS

• Real-time vehicle tracking
• GTFS integration
• Traffic-aware bus delay prediction
• User accounts and saved routes
• Mobile application support
• Enhanced fare estimation
