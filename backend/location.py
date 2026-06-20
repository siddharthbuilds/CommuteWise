from geopy.geocoders import Nominatim
import json

with open("./database/all_coords.json", "r") as f:
    all_coords = json.load(f)

# Initialize Nominatim API (user_agent is required)
geolocator = Nominatim(user_agent="my_location")
COORD_LOOKUP = {
    place.lower(): coords
    for place, coords in all_coords.items()
}

def get_matching_node(place):
    query = place.strip().lower()

    # Exact match
    for node in all_coords:
        if node.lower() == query:
            return node

    # Partial match
    for node in all_coords:
        node_lower = node.lower()

        if query in node_lower or node_lower in query:
            return node

    return None


def locate(place):
    query = place.strip().lower()

    # Exact match
    if query in COORD_LOOKUP:
        return COORD_LOOKUP[query]

    # Partial match
    for key, coords in COORD_LOOKUP.items():
        if query in key or key in query:
            return coords

    # Geocoder fallback
    location = geolocator.geocode(place)

    if location:
        return [location.latitude, location.longitude]

    return None
   
