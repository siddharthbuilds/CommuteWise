import json
import heapq
from math import radians, sin, cos, sqrt, atan2
from graph_finder import graph
from node_finder import node_mode
with open("all_coords.json", "r") as f:
    all_coords = json.load(f)
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
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def build_weighted_graph(graph, all_coords):
    weighted_graph = {}
    for node in graph:
        weighted_graph[node] = []
        lat1, lon1 = all_coords[node]
        for neighbour in graph[node]:
            lat2, lon2 = all_coords[neighbour]
            distance = haversine(
                lat1,
                lon1,
                lat2,
                lon2
            )
            weighted_graph[node].append(
                (neighbour, distance)
            )
    return weighted_graph

def add_transfer_edges(
        weighted_graph,
        all_coords,
        node_mode,
        radius_km=0.3,
        walking_penalty=3):
    nodes = list(weighted_graph.keys())
    transfer_count = 0
    for i in range(len(nodes)):
        node_a = nodes[i]
        lat1, lon1 = all_coords[node_a]
        for j in range(i + 1, len(nodes)):
            node_b = nodes[j]
            mode_a = node_mode.get(node_a)
            mode_b = node_mode.get(node_b)
            if mode_a == mode_b:
                continue
            lat2, lon2 = all_coords[node_b]
            distance = haversine(
                lat1,
                lon1,
                lat2,
                lon2
            )
            if distance <= radius_km:

                walking_cost = distance * walking_penalty

                weighted_graph[node_a].append(
                    (node_b, walking_cost)
                )

                weighted_graph[node_b].append(
                    (node_a, walking_cost)
                )

                transfer_count += 1
    print("Transfer edges:", transfer_count)
    return weighted_graph

def dijkstra(graph, source, destination):
    distances = {
        node: float("inf")
        for node in graph
    }
    parent = {}
    distances[source] = 0
    pq = [(0, source)]
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > distances[current_node]:
            continue
        if current_node == destination:
            break
        for neighbour, weight in graph[current_node]:
            new_dist = current_dist + weight
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                parent[neighbour] = current_node
                heapq.heappush(
                    pq,
                    (new_dist, neighbour)
                )
    if source == destination:
        return [source]
    if destination not in parent:
        return None
    path = []
    curr = destination
    while curr != source:
        path.append(curr)
        curr = parent[curr]
    path.append(source)
    path.reverse()
    return path, distances[destination]


graph["THIRNEERMALAI"] = []
graph["Vadanemili"] = []
weighted_graph = build_weighted_graph(
    graph,
    all_coords
)
print(len(weighted_graph))
weighted_graph = add_transfer_edges(
    weighted_graph,
    all_coords,
    node_mode
)
print(
    dijkstra(
        weighted_graph,
        "LIC",
        "Government Estate"
    )
)

route = dijkstra(
    weighted_graph,
    "Velacherry RS",
    "LIC"
)

print(route)