from location import locate, get_matching_node
from database.djikstra import find_routes
from routes.routes import Routes
from routes.delay_model import predict_delay
def get_max_values(all_routes):
    max_distance = max(r.distance for r in all_routes)
    max_duration = max(r.duration for r in all_routes)
    max_expenditure = max(r.expenditure for r in all_routes)
    max_timedelay = max(r.timedelay for r in all_routes)
    max_carbonrate = max(r.carbonrate for r in all_routes)

    max_values = [max_distance,max_duration,max_expenditure,max_timedelay,max_carbonrate]
    for routes in all_routes:
        routes.get_rating(max_values)

def get_min_values(all_routes):
    min_duration = min(r.duration for r in all_routes)
    min_expenditure = min(r.expenditure for r in all_routes)
    min_carbonrate = min(r.carbonrate for r in all_routes)
    return [min_expenditure,min_duration,min_carbonrate]

def get_badges(all_routes):
    min_values=get_min_values(all_routes)
    sorted_all_routes=sorted(all_routes,key=lambda route: route.rating, reverse=True)
    sorted_all_routes[0].add_badge("Best")
    for routes in sorted_all_routes:
        if routes.expenditure==min_values[0]:
            routes.add_badge("Cheapest")
        if routes.duration==min_values[1]:
            routes.add_badge("Fastest")
        if routes.carbonrate==min_values[2]:
            routes.add_badge("Safest")
    return sorted_all_routes


def get_final_data(sorted_all_routes):
    final_routes=list()
    for routes in sorted_all_routes:
        route_dict={
                    "mode":routes.mode,
                    "distance": routes.distance,
                    "duration":routes.duration,
                    "expenditure":routes.expenditure,
                    "timedelay":routes.timedelay,
                    "carbonrate":routes.carbonrate,
                    "rating":routes.rating,
                    "badges":routes.badges,
                    "stops":routes.stops,
                    "segments":routes.segments   
                    }
        final_routes.append(route_dict)
    return final_routes

def get_all_routes(source,destination,date,time):
    [source_lat,source_lon] = locate(source)
    [dest_lat,dest_lon] = locate(destination)
    source_node = get_matching_node(source)
    dest_node = get_matching_node(destination)
    all_routes=find_routes(source_lat,source_lon,dest_lat,dest_lon,source_node,dest_node)
    route_objects = [Routes.from_dict(route)for route in all_routes]
    stddelay=predict_delay(date,time)
    for route in route_objects:
        route.timedelay=stddelay*(route.distance/20)
        route.duration+=(route.timedelay/60)
        route.timedelay = round(route.timedelay,2)
        route.duration = round(route.duration,2)
        route.distance = round(route.distance,2)
        route.expenditure = round(route.expenditure,2)
        route.carbonrate = round(route.carbonrate,2)
    get_max_values(route_objects)
    sorted_routes= get_badges(route_objects)
    final_routes=get_final_data(sorted_routes)
    return final_routes

