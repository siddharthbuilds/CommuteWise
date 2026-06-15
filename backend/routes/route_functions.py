def get_all_routes(source,destination):
    all_routes=[]
    return all_routes

def get_max_values(routes):
    max_duration = max(r.duration for r in routes)
    max_cost = max(r.expenditure for r in routes)
    max_delay = max(r.timedelay for r in routes)
    max_carbon = max(r.carbonrate for r in routes)
    max_distance = max(r.distance for r in routes)

    max_values = [max_distance,max_duration,max_cost,max_delay,max_carbon]
    for route in routes:
        route.get_rating(max_values)

def get_badges(all_routes):
    return