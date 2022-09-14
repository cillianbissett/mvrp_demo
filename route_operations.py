from lib2to3.pgen2 import driver
import pandas as pd

def route_cleaner(routes, num_jobs, single_depot):
    """
    Takes in a mulltidimensional array describing a set of routes and cleans output. Used for one-depot case.
    """
    # reference value
    max_index = num_jobs - 1
    
    if single_depot:
        # hold answer
        clean_routes = []

        # clean up first index problem if needed
        for route in routes:
            if route[0] > max_index:
                route = [0] + route[1:]
            else:
                pass
            clean_routes.append(route)
        
    return clean_routes

def fetch_route_detail(routes, locations_df):
    """
    Takes in a list of clean routes & a list of co-ordinates and builds a driver-call dataframe.
    """
    # hold answer
    driver_routes = []

    # want driver, order in which places visited, and index of call
    for i, route in enumerate(routes):
        for j, call_index in enumerate(route):
            driver_routes.append((i , j, call_index))
    
    # now I want a dataframe for nice tabular format
    driver_routes_df = pd.DataFrame(driver_routes, columns = ['driver', 'order', 'index'])
    driver_routes_locations = pd.merge(locations_df, driver_routes_df, on = 'index', how = 'inner')
    driver_routes_locations = driver_routes_locations.sort_values(['driver', 'order'])
    driver_routes_locations = driver_routes_locations.rename({'x':'x_coord',
                                                              'y':'y_coord'}, axis = 1)
    driver_routes_locations = driver_routes_locations.reset_index(drop = True)
    return driver_routes_locations

    

