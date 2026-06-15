import json
import heapq
from math import radians, sin, cos, sqrt, atan2
from graph_finder import graph
from node_finder import node_mode
import copy
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

def build_weighted_graph(graph, all_coords, node_mode):
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
            distance = max(distance, 0.05)
            weighted_graph[node].append(
                {
                    "to": neighbour,
                    "distance": distance,
                    "cost":distance,
                    "mode": node_mode[node]
                }
            )
    return weighted_graph

def add_transfer_edges(
        weighted_graph,
        all_coords,
        node_mode,
        radius_km=0.5):

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
                weighted_graph[node_a].append(
                    {
                        "to": node_b,
                        "distance": distance,
                        "cost":distance,
                        "mode": "walk"
                    }
                )
                weighted_graph[node_b].append(
                    {
                        "to": node_a,
                        "distance": distance,
                        "cost":distance,
                        "mode": "walk"
                    }
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
        for edge in graph[current_node]:
            neighbour = edge["to"]
            weight = edge["cost"]
            if edge["mode"] == "walk":
                 effective_walk = max(edge["cost"],0.05)
                 weight = effective_walk * 3
            new_dist = current_dist + weight
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                parent[neighbour] = (
                    current_node,
                    edge
                )
                heapq.heappush(
                    pq,
                    (new_dist, neighbour)
                )
    if destination not in parent:
        return None
    segments = []
    current = destination
    while current != source:
        prev_node, edge = parent[current]
        segments.append(
            (
                prev_node,
                current,
                edge["mode"],
                edge["distance"]
            )
        )
        current = prev_node
    segments.reverse()
    return segments, distances[destination]


def explain_route(segments):
    total_walk = 0
    total_bus = 0
    total_rail = 0
    total_metro = 0
    transfers = 0
    previous_mode = None
    print("\nROUTE\n")
    for start, end, mode, distance in segments:
        print(
            f"{start} -> {end}"
        )
        print(
            f"Mode: {mode}"
        )
        display_distance = distance

        if mode == "walk":
            display_distance = max(
                distance,
                0.05)
        print(
        f"Distance: {display_distance} km\n")
        
        if previous_mode and previous_mode != mode:
            transfers += 1
        previous_mode = mode
        if mode == "walk":
            total_walk += max(distance,0.05)
        elif mode == "bus":
            total_bus += distance
        elif mode == "rail":
            total_rail += distance
        elif mode == "metro":
            total_metro += distance
    print("Summary")
    print("-------")
    print("Walking:", round(total_walk, 2), "km")
    print("Bus:", round(total_bus, 2), "km")
    print("Rail:", round(total_rail, 2), "km")
    print("Metro:", round(total_metro, 2), "km")
    print("Transfers:", transfers)

def route_nodes(segments):
    nodes = [segments[0][0]]
    for _, end, _, _ in segments:
        nodes.append(end)
    return nodes



def get_candidate_routes(
        weighted_graph,
        source,
        destination,
        k=10):
    graph_copy = copy.deepcopy(weighted_graph)
    routes = []
    for _ in range(k):
        result = dijkstra(
            graph_copy,
            source,
            destination
        )
        if result is None:
            break
        segments, distance = result
        routes.append(
            (segments, distance)
        )
        path_nodes = route_nodes(segments)
        for i in range(len(path_nodes)-1):
            a = path_nodes[i]
            b = path_nodes[i+1]
            for edge in graph_copy[a]:
                if edge["to"] == b:
                    edge["cost"] *= 1.5
    return routes



graph["THIRNEERMALAI"] = []
graph["Vadanemili"] = []
weighted_graph = build_weighted_graph(
    graph,
    all_coords,
    node_mode
)
weighted_graph = add_transfer_edges(
    weighted_graph,
    all_coords,
    node_mode
)
routes = get_candidate_routes(
    weighted_graph,
    "Velacherry RS",
    "LIC",
    k=10
)

for idx, (segments, distance) in enumerate(routes):

    print(
        f"\nRoute {idx+1}"
    )

    print(
        "Distance:",
        round(distance, 2)
    )

    explain_route(segments)

