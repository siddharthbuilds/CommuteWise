from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_location")
location = geolocator.geocode("Cali")
coords=[location.latitude,location.longitude]
#print(coords)
