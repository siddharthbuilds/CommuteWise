from database.coords_bus import chennai_bus_stops_coords
from database.coords_metro import metro_coords
from database.coords_rail import chennai_stations_coords
import json
all_coords = {}

all_coords.update(metro_coords)

for station, data in chennai_stations_coords.items():
    all_coords[station] = (
        data["latitude"],
        data["longitude"]
    )

for stop, data in chennai_bus_stops_coords.items():
    all_coords[stop] = (
        data["latitude"],
        data["longitude"]
    )
with open("./database/all_coords.json", "w") as f:
    json.dump(all_coords, f, indent=4)