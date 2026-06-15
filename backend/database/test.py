from coords_rail import chennai_stations_coords,df_rail
from coords_metro import metro_coords
from bfs_algo import bfs,graph
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2

geo = Nominatim(user_agent="commutewise")
all_coords = {}

all_coords.update(metro_coords)

for station, data in chennai_stations_coords.items():

    all_coords[station] = (
        data["latitude"],
        data["longitude"]
    )
def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c
def nearest_transit_node(lat, lon):

    nearest_station = None

    min_distance = float("inf")

    for station, (s_lat, s_lon) in all_coords.items():

        distance = haversine(
            lat,
            lon,
            s_lat,
            s_lon
        )

        if distance < min_distance:

            min_distance = distance

            nearest_station = station

    return nearest_station, min_distance
def top5_nearest_nodes(lat, lon):

    distances = []

    for station, (s_lat, s_lon) in all_coords.items():

        distance = haversine(
            lat,
            lon,
            s_lat,
            s_lon
        )

        distances.append(
            (distance, station)
        )

    distances.sort()

    for distance, station in distances[:5]:

        print(
            station,
            round(distance, 2),
            "km"
        )

def place_to_station(place):

    location = geo.geocode(place)

    if not location:

        print("Place not found")

        return None

    station, distance = nearest_transit_node(
        location.latitude,
        location.longitude
    )

    print(place)

    print(
        "Nearest Station:",
        station
    )

    print(
        "Distance:",
        round(distance, 2),
        "km"
    )

    return station
location = geo.geocode(
    "Tambaram Chennai"
)

top5_nearest_nodes(
    location.latitude,
    location.longitude
)
places = [
    "Phoenix Marketcity Chennai",
    "Express Avenue Chennai",
    "Marina Beach Chennai",
    "Tambaram Chennai",
    "Anna University Chennai"
]

for place in places:

    print("\n" + "=" * 50)

    station = place_to_station(
        place
    )

    print(
        "Selected:",
        station
    )
source = place_to_station(
    "Phoenix Marketcity Chennai"
)

destination = place_to_station(
    "Express Avenue Chennai"
)

path = bfs(
    graph,
    source,
    destination
)

print(path)
print("Tambaram RS" in chennai_stations_coords)
for station in sorted(df_rail["Station"].unique()):
    if station not in chennai_stations_coords:
        print(station)