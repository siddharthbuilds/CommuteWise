from graph_metro import graph
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
route = bfs(
    graph,
    "Chennai Airport",
    "LIC"
)

print(route)
print(bfs(graph,
          "Ekkattuthangal",
          "Washermenpet"))
print(bfs(graph,
          "St Thomas Mount",
          "LIC"))
print(bfs(graph,
          "Chennai Airport",
          "Wimco Nagar"))