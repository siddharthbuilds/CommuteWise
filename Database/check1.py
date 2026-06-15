from bfs_algo import bfs,graph
from check import nearest_metro,Nominatim,metro_coords
geo = Nominatim(user_agent="commutewise")

def place_to_station(place):

    location = geo.geocode(place)

    if not location:
        return None

    station, distance = nearest_metro(
        location.latitude,
        location.longitude
    )

    print(f"{place}")
    print(f"Nearest Station: {station}")
    print(f"Distance: {round(distance, 2)} km")

    return station
source_station = place_to_station(
    "Phoenix Marketcity Chennai"
)

destination_station = place_to_station(
    "Express Avenue Chennai"
)

print(source_station)
print(destination_station)
path = bfs(
    graph,
    source_station,
    destination_station
)

print(path)
tests = [
    ("Phoenix Marketcity Chennai",
     "Express Avenue Chennai"),

    ("Anna University Chennai",
     "Marina Beach Chennai"),

    ("Phoenix Marketcity Chennai",
     "Chennai Central Railway Station"),

    ("Tambaram Chennai",
     "Express Avenue Chennai")
]
for src, dst in tests:

    print("\n" + "="*50)

    source_station = place_to_station(src)
    destination_station = place_to_station(dst)

    if source_station and destination_station:

        path = bfs(
            graph,
            source_station,
            destination_station
        )

        print("Route:")
        print(path)