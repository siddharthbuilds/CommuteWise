import pandas as pd
from bfs_algo import bfs
df_bus=pd.read_csv("route_detail (1).csv")
print(df_bus.columns.tolist())
print(df_bus.shape)


route = "1"

print(
    df_bus[df_bus["route_id"] == route]
)
print(df_bus["route_id"].nunique())
print(df_bus["stop_name"].nunique())
from collections import defaultdict

bus_graph = defaultdict(set)

# ensure stop order
df_bus["stop_id"] = df_bus["stop_id"].astype(int)

for route_id, group in df_bus.groupby("route_id"):

    group = group.sort_values("stop_id")

    stops = group["stop_name"].str.strip().tolist()

    for i in range(len(stops) - 1):

        current = stops[i]
        next_stop = stops[i + 1]

        bus_graph[current].add(next_stop)
        bus_graph[next_stop].add(current)
print(len(bus_graph))

print(bus_graph["THIRUVOTRIYUR"])

print(bus_graph["PARRYS"])
path = bfs(
    bus_graph,
    "THIRUVOTRIYUR",
    "THIRUVANMIYUR"
)

print(path)