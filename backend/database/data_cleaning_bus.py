import pandas as pd
from collections import defaultdict
df_bus=pd.read_csv("./database/route_detail (1).csv")
route = "1"
bus_graph = defaultdict(set)
df_bus["stop_id"] = df_bus["stop_id"].astype(int)
for route_id, group in df_bus.groupby("route_id"):
    group = group.sort_values("stop_id")
    stops = group["stop_name"].str.strip().tolist()
    for i in range(len(stops) - 1):
        current = stops[i]
        next_stop = stops[i + 1]
        bus_graph[current].add(next_stop)
        bus_graph[next_stop].add(current)
if __name__ == "__main__":
    print(df_bus["route_id"].nunique())
    print(df_bus["stop_name"].nunique())
    print(df_bus.columns.tolist())
    print(df_bus.shape)
    print(
    df_bus[df_bus["route_id"] == route])

