import json
import heapq
from math import radians, sin, cos, sqrt, atan2
from database.graph_finder import graph
from database.node_finder import node_mode
import copy

with open("./database/all_coords.json", "r") as f:
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

def nearest_nodes(lat, lon, all_coords, k=5, max_radius=1.5):
    distances = []

    for node, (nlat, nlon) in all_coords.items():
        d = haversine(lat, lon, nlat, nlon)

        if d <= max_radius:
            distances.append((d, node))

    distances.sort()

    return [node for _, node in distances[:k]]


def build_weighted_graph(graph, all_coords, node_mode):
    weighted_graph = {}
    for node in graph:
        weighted_graph[node] = []
        lat1, lon1 = all_coords[node]
        for neighbour in graph[node]:
            lat2, lon2 = all_coords[neighbour]
            distance = haversine(lat1, lon1, lat2, lon2)
            distance = max(distance, 0.05)
            weighted_graph[node].append({
                "to": neighbour,
                "distance": distance,
                "cost": distance,
                "mode": node_mode[node]
            })
    return weighted_graph

def add_transfer_edges(weighted_graph, all_coords, node_mode, radius_km=0.25):
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
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance <= radius_km:
                weighted_graph[node_a].append({"to": node_b, "distance": distance, "cost": distance, "mode": "walk"})
                weighted_graph[node_b].append({"to": node_a, "distance": distance, "cost": distance, "mode": "walk"})
                transfer_count += 1
    print("Transfer edges:", transfer_count)
    return weighted_graph

def dijkstra(graph, source, destination):
    distances = {node: float("inf") for node in graph}
    parent = {}
    distances[source] = 0
    pq = [(0, source)]
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > distances[current_node]:
            continue
        if current_node == destination:
            break
        for edge in graph[current_node]:
            neighbour = edge["to"]
            weight = edge["cost"]
            if edge["mode"] == "walk":
                weight = max(edge["cost"], 0.05) * 3
            new_dist = current_dist + weight
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                parent[neighbour] = (current_node, edge)
                heapq.heappush(pq, (new_dist, neighbour))
    if destination not in parent:
        return None
    segments = []
    current = destination
    while current != source:
        prev_node, edge = parent[current]
        segments.append((prev_node, current, edge["mode"], edge["distance"]))
        current = prev_node
    segments.reverse()
    return segments, distances[destination]

def explain_route(segments):
    total_walk = total_bus = total_rail = total_metro = transfers = 0
    previous_mode = None
    print("\nROUTE\n")
    for start, end, mode, distance in segments:
        print(f"{start} -> {end}")
        print(f"Mode: {mode}")
        display_distance = max(distance, 0.05) if mode == "walk" else distance
        print(f"Distance: {display_distance} km\n")
        if previous_mode and previous_mode != mode:
            transfers += 1
        previous_mode = mode
        if mode == "walk":   total_walk  += max(distance, 0.05)
        elif mode == "bus":  total_bus   += distance
        elif mode == "rail": total_rail  += distance
        elif mode == "metro":total_metro += distance
    print("Summary\n-------")
    print("Walking:", round(total_walk, 2), "km")
    print("Bus:",     round(total_bus, 2),  "km")
    print("Rail:",    round(total_rail, 2), "km")
    print("Metro:",   round(total_metro, 2),"km")
    print("Transfers:", transfers)

def route_nodes(segments):
    nodes = [segments[0][0]]
    for _, end, _, _ in segments:
        nodes.append(end)
    return nodes

def get_candidate_routes(weighted_graph, source, destination, k=10):
    graph_copy = copy.deepcopy(weighted_graph)
    routes = []
    for _ in range(k):
        result = dijkstra(graph_copy, source, destination)
        if result is None:
            break
        segments, distance = result
        routes.append((copy.deepcopy(segments), distance))
        path_nodes = route_nodes(segments)
        for i in range(len(path_nodes) - 1):
            a, b = path_nodes[i], path_nodes[i + 1]
            for edge in graph_copy[a]:
                if edge["to"] == b:
                    edge["cost"] *= 1.5
  
    return routes

def find_routes(source_lat, source_lon,
                dest_lat, dest_lon):

    source_candidates = nearest_nodes(
        source_lat,
        source_lon,
        all_coords,
        k=5
    )

    destination_candidates = nearest_nodes(
        dest_lat,
        dest_lon,
        all_coords,
        k=5
    )

    all_routes = []

    for src in source_candidates:
        for dst in destination_candidates:

            routes = get_candidate_routes(
                weighted_graph,
                src,
                dst,
                k=2
            )

            for segments, distance in routes:

                final_lat, final_lon = all_coords[dst]

                destination_error = haversine(
                    final_lat,
                    final_lon,
                    dest_lat,
                    dest_lon
                )

                score = (
                    distance
                    + destination_error * 5
                )

                all_routes.append(
                    (segments, distance, score)
                )

    all_routes.sort(key=lambda x: x[2])

    for candidate in source_candidates:
        print(candidate)

    for candidate in destination_candidates:
        print(candidate)

    return all_routes[:10]

graph["THIRNEERMALAI"] = []
graph["Vadanemili"] = []
weighted_graph = build_weighted_graph(graph, all_coords, node_mode)
weighted_graph = add_transfer_edges(weighted_graph, all_coords, node_mode)

source_lat, source_lon = 12.99, 80.21
dest_lat,   dest_lon   = 12.5,  80.13

source_candidates = nearest_nodes(
    source_lat,
    source_lon,
    all_coords,
    k=5
)

destination_candidates = nearest_nodes(
    dest_lat,
    dest_lon,
    all_coords,
    k=5
)
all_routes = []

for src in source_candidates:
    for dst in destination_candidates:

        routes = get_candidate_routes(
            weighted_graph,
            src,
            dst,
            k=2
        )

        all_routes.extend(routes)

all_routes.sort(key=lambda x: x[1])

routes = all_routes[:10]


for idx, (segments, distance) in enumerate(routes):
    print(f"\nRoute {idx + 1}")
    print("Distance:", round(distance, 2))
    explain_route(segments)


