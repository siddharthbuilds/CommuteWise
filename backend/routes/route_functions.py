def get_all_routes(source,destination):
    all_routes=[]
    return all_routes

def get_max_values(all_routes):
    max_duration = max(r.duration for r in all_routes)
    max_expenditure = max(r.expenditure for r in all_routes)
    max_delay = max(r.timedelay for r in all_routes)
    max_carbon = max(r.carbonrate for r in all_routes)
    max_distance = max(r.distance for r in all_routes)

    max_values = [max_distance,max_duration,max_expenditure,max_delay,max_carbon]
    for routes in all_routes:
        routes.get_rating(max_values)

def get_min_values(all_routes):
    min_duration = min(r.duration for r in all_routes)
    min_expenditure = min(r.expenditure for r in all_routes)
    min_carbon = min(r.carbonrate for r in all_routes)
    return [min_expenditure,min_duration,min_carbon]

def get_badges(all_routes):
    min_values=get_min_values(all_routes)
    sorted_all_routes=sorted(all_routes,key=lambda route: route.rating)
    sorted_all_routes[0].add_badge("best")
    for routes in sorted_all_routes:
        if routes.expenditure==min_values[0]:
            routes.add_badge("cheapest")
        if routes.expenditure==min_values[1]:
            routes.add_badge("fastest")
        if routes.expenditure==min_values[2]:
            routes.add_badge("safest")