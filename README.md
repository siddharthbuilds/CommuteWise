# CommuteWise 

## Smart Public Transit Route Recommendation System for Chennai

CommuteWise is an intelligent public transportation route recommendation system designed to help commuters navigate Chennai's transit network efficiently. The system integrates Chennai Metro, Suburban Rail, and Bus networks into a unified graph-based model and recommends optimal routes based on multiple user preferences.

Unlike traditional route planners that focus solely on shortest travel time, CommuteWise evaluates routes using travel duration, fare cost, reliability, and environmental impact to provide more meaningful recommendations.

To improve real-world usability, the system incorporates a Machine Learning model that predicts transit delays using live weather conditions.

---

## Key Features

### Multi-Modal Transit Routing

* Chennai Metro Network
* Chennai Suburban Rail Network
* MTC Bus Network

### Intelligent Route Recommendations

Users can choose routes based on:

*  Best Overall
*  Fastest
*  Cheapest
*  Greenest

### Real-Time Delay Estimation

* Live weather data from Open-Meteo
* Delay prediction using Random Forest Regression

### Geospatial Processing

* Address geocoding using Nominatim
* Nearest transit stop detection
* Coordinate-based route planning

### Route Scoring Engine

Each generated route is evaluated using:

* Travel Time
* Fare Cost
* Predicted Delay
* Carbon Emissions

---

# System Architecture

```text
User
 │
 ▼
Frontend (HTML/CSS/JavaScript)
 │
 ▼
POST /api/routes
 │
 ▼
FastAPI Backend
 │
 ├── Geocoding (Nominatim)
 ├── Weather API (Open-Meteo)
 ├── Delay Prediction (Random Forest)
 └── Route Computation (Dijkstra)
            │
            ▼
      Route Scoring
            │
            ▼
      Ranked Results
            │
            ▼
         Frontend
```

---

# Technology Stack

## Backend

* Python 3
* FastAPI
* Geopy
* Scikit-Learn
* Pickle
* Open-Meteo API

## Algorithms

* Dijkstra's Algorithm
* Graph-Based Routing
* Route Ranking System

## Machine Learning

* Random Forest Regressor
* Weather-Based Delay Prediction

## Frontend

* HTML5
* CSS3
* Vanilla JavaScript

## Data Sources

* Chennai Metro Rail Data
* Chennai Suburban Rail Data
* Chennai Bus Route Data
* Open-Meteo Weather API

---

# Project Structure

```text
CommuteWise/
│
├── README.md
├── random_reg_model.pkl
│
├── backend/
│   │
│   ├── main.py
│   ├── location.py
│   ├── testing.py
│   │
│   ├── routes/
│   │   ├── route_functions.py
│   │   ├── routes.py
│   │   ├── delay_model.py
│   │   └── random_reg_model.pkl
│   │
│   └── database/
│       ├── djikstra.py
│       ├── graph_finder.py
│       ├── node_finder.py
│       ├── master_dict.py
│       │
│       ├── all_coords.json
│       ├── bus_coords.json
│       ├── metro_coords.json
│       ├── rail_coords.json
│       │
│       └── Transit datasets and preprocessing scripts
│
├── frontend/
│   │
│   ├── index.html
│   ├── about.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   └── data.js
│   │
│   └── assets/
│       ├── logo.svg
│       └── hero-illustration.svg
│
└── ml-models/
    ├── Public Delay Dataset/
    └── Trial Dataset/
```

---

# How It Works

## Step 1: User Input

The commuter enters a source and destination location through the web interface.

---

## Step 2: Geocoding

The entered locations are converted into geographic coordinates using Nominatim.

```python
Source Address → Latitude/Longitude
Destination Address → Latitude/Longitude
```

---

## Step 3: Stop Identification

The system identifies the nearest transit nodes from the transit network using coordinate matching.

---

## Step 4: Weather Retrieval

Current weather conditions are fetched from Open-Meteo.

Collected parameters may include:

* Temperature
* Humidity
* Rainfall
* Wind Speed

---

## Step 5: Delay Prediction

Weather features are passed into a trained Random Forest model.

```text
Weather Data
      │
      ▼
Random Forest Model
      │
      ▼
Predicted Transit Delay
```

---

## Step 6: Route Computation

The transit network is represented as a weighted graph.

### Graph Representation

* Nodes → Transit Stops
* Edges → Connections Between Stops
* Weights → Travel Cost Metrics

Dijkstra's Algorithm computes the shortest path between the source and destination nodes.

---

## Step 7: Route Scoring

Every generated route is evaluated using:

```text
Score =
Travel Time
+ Fare Cost
+ Delay Penalty
+ Carbon Impact
```

The scoring system allows multiple route preferences.

---

## Step 8: Recommendation Generation

Routes are ranked and categorized into:

* Best Overall
* Fastest
* Cheapest
* Greenest

The results are returned to the frontend and displayed to the user.

---

# Algorithm Details

## Dijkstra's Algorithm

CommuteWise uses Dijkstra's Algorithm to compute the optimal path across Chennai's transit network.

### Complexity

```text
Time Complexity:
O((V + E) log V)

Where:

V = Number of Stops
E = Number of Connections
```

### Network Scale

```text
Approximate Transit Stops : 1400+
Transit Modes            : 3
```

---

# Machine Learning Model

## Random Forest Regressor

The delay prediction module uses a Random Forest Regression model trained on transportation and weather-related datasets.

### Input Features

* Temperature
* Humidity
* Rainfall
* Wind Speed
* Other Weather Attributes

### Output

```text
Predicted Delay (minutes)
```

### Model File

```text
random_reg_model.pkl
```

---

# API Documentation

## Generate Routes

### Endpoint

```http
POST /api/routes
```

### Request

```json
{
  "source": "Tambaram",
  "destination": "Chennai Central",
  "date": "2026-06-16",
  "time":"09:00"
}
```

### Response

```json
{ "routes": 
      [ 
        {   "mode": "Metro + Bus", 
            "distance": 21.34, 
            "duration": 58.42, 
            "expenditure": 46.75, 
            "timedelay": 6.42, 
            "carbonrate": 0.94, 
            "rating": 8.76, 
            "badges": [ "Best", "Fastest" ], 
            "stops": [ "GUINDY", "ALANDUR", "TAMBARAM" ], 
            "segments": 
            [ 
                  { 
                        "from": "GUINDY", 
                        "to": "ALANDUR",
                        "mode": "metro", 
                        "distance": 2.15 
                  }, 
                  { 
                        "from": "ALANDUR", 
                        "to": "TAMBARAM", 
                        "mode": "bus", 
                        "distance": 19.19 
                  } 
            ] 
        } 
      ]  
}
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/CommuteWise.git
cd CommuteWise
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Start Backend

Navigate to the backend directory:

```bash
cd backend
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Start Frontend

Open:

```text
frontend/index.html
```

Or serve locally:

```bash
python -m http.server 5500
```

Then visit:

```text
http://localhost:5500
```

---

# Future Enhancements

* GTFS Real-Time Integration
* Live Vehicle Tracking
* Crowding Prediction
* Route Caching
* A* Pathfinding Optimization
* Mobile Application
* User Profiles and Saved Routes
* Dynamic Fare Prediction

---



# License

This project is intended for educational and research purposes.
