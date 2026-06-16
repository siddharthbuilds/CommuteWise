import sys
import os


from djikstra import find_routes,explain_route
from location import locate

[l1,l2] = locate("Phoenix MarketCity Chennai")
[l3,l4] = locate("Chennai International Airport")

# print([l3,l4])

routes = find_routes(l1, l2, l3, l4)

for idx, (segments, distance, score) in enumerate(routes):
    print(f"\nRoute {idx + 1}")
    print("Distance:", round(distance, 2))
    print("Score:", round(score, 2))
    explain_route(segments)