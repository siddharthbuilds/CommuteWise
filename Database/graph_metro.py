from data_cleaning_metro import df
from collections import defaultdict
graph = defaultdict(list)
for corridor, group in df.groupby("Corridor Name"):
    stations = group["Station Name"].tolist()
    for i in range(len(stations)-1):
        current = stations[i]
        next_station = stations[i+1]
        graph[current].append(next_station)
        graph[next_station].append(current)
print(graph["Alandur"])