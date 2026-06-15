from graph_finder import graph,df,df_rail,df_bus
from collections import deque

def bfs(graph, start, end):

    queue = deque([start])

    visited = set([start])

    parent = {}

    while queue:

        current = queue.popleft()

        if current == end:

            path = []

            while current != start:
                path.append(current)
                current = parent[current]

            path.append(start)

            return path[::-1]

        for neighbour in graph[current]:

            if neighbour not in visited:

                visited.add(neighbour)

                parent[neighbour] = current

                queue.append(neighbour)

    return None
print("Total nodes:", len(graph))
print("Airport exists:", "Chennai Airport" in graph)
print("THIRUVOTRIYUR exists:", "THIRUVOTRIYUR" in graph)
print("Velacherry RS exists:", "Velacherry RS" in graph)
print("Airport neighbours:")
print(graph["Chennai Airport"])
print("THIRUVOTRIYUR neighbours:")
print(graph["THIRUVOTRIYUR"])
metro_nodes = set(df["Station Name"])

rail_nodes = set(df_rail["Station"])

bus_nodes = set(df_bus["stop_name"])

print("Bus-Metro overlap:",
      metro_nodes & bus_nodes)

print("Bus-Rail overlap:",
      rail_nodes & bus_nodes)