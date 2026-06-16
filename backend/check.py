from math import radians, sin, cos, sqrt, atan2
from coords_metro import metro_coords
def haversine(lat1, lon1, lat2, lon2):

    R = 6371  # km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
def nearest_metro(lat, lon):

    nearest_station = None
    min_distance = float("inf")

    for station, (s_lat, s_lon) in metro_coords.items():

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

def top5_nearest_metro(lat, lon):

    distances = []

    for station, (s_lat, s_lon) in metro_coords.items():

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
from geopy.geocoders import Nominatim

geo = Nominatim(
    user_agent="commutewise"
)

location = geo.geocode(
    "Phoenix Marketcity Chennai"
)

print(
    location.latitude,
    location.longitude
)
top5_nearest_metro(
    location.latitude,
    location.longitude
)
places = [
    "Phoenix Marketcity Chennai",
    "Marina Beach Chennai",
    "Express Avenue Chennai",
    "Anna University Chennai",
    "Tambaram Chennai"
]

for place in places:

    location = geo.geocode(place)

    if location:

        station, distance = nearest_metro(
            location.latitude,
            location.longitude
        )

        print("\n", place)
        print("Nearest:", station)
        print("Distance:", round(distance, 2), "km")

