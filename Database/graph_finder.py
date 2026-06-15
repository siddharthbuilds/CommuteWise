from data_cleaning_metro import df
from data_cleaning_electric_train import df_rail
from collections import defaultdict
from data_cleaning_bus import bus_graph
graph = defaultdict(set)
for corridor, group in df.groupby("Corridor Name"):
    stations = group["Station Name"].tolist()
    for i in range(len(stations)-1):
        current = stations[i]
        next_station = stations[i+1]
        graph[current].add(next_station)
        graph[next_station].add(current)

for connection, group in df_rail.groupby("Connection"):
    stations = group["Station"].tolist()
    for i in range(len(stations)-1):
        current = stations[i]
        next_station = stations[i+1]
        graph[current].add(next_station)
        graph[next_station].add(current)
transfer_map = {
    "Guindy RS": "Guindy",
    "St Thomas Mount RS": "St Thomas Mount",
    "Tirusulam RS; Airport": "Chennai Airport",
    "Chennai Central MMC": "Chennai Central"
}
for rail, metro in transfer_map.items():
    graph[rail].add(metro)
    graph[metro].add(rail)

for stop, neighbours in bus_graph.items():
    for neighbour in neighbours:
        graph[stop].append(neighbour)
