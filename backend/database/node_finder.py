from database.data_cleaning_bus import df_bus
from database.data_cleaning_electric_train import df_rail
from database.data_cleaning_metro import df
import json
with open("./database/all_coords.json", "r") as f:
    all_coords = json.load(f)
bus_nodes = set(
    df_bus["stop_name"].dropna().str.strip()
)

# Rail stations
rail_nodes = set(
    df_rail["Station"].dropna().str.strip()
)

# Metro stations
metro_nodes = set(
    df["Station Name"].dropna().str.strip()
)
node_mode = {}

for station in metro_nodes:
    node_mode[station] = "metro"

for station in rail_nodes:
    node_mode[station] = "rail"

for stop in bus_nodes:
    node_mode[stop] = "bus"
node_mode["THIRNEERMALAI"] = "bus"
node_mode["Vadanemili"] = "bus"
