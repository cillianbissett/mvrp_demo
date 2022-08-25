import numpy as np
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model(distance_matrix, engineers, num_jobs):
    '''
    Stores the data. 
    
    Note:
        - number of vehicles is equal to number of depots
        - start and end locations are identical... engineers go home after work! 
    '''
    data = {}
    start_end_points = np.random.randint(0, num_jobs, engineers).tolist()
    job_limits = [int(len(distance_matrix) / engineers) + 1 for _ in range(engineers)]
    demands = [1 for _ in range(len(distance_matrix))]
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = engineers
    data['starts'] = start_end_points
    data['ends'] = start_end_points
    data['demands'] = demands
    data['vehicle_capacities'] = job_limits
    return data

def return_solution(data, manager, routing, solution):
    ''' Returns solution found by OR Tools in a nice structure. '''
    print('Total distance: {} units'.format(solution.ObjectiveValue()))
    all_routes = []
    total_distance = 0
    for engineer in range(data['num_vehicles']):
        current_place = routing.Start(engineer)
        plan = 'Engineer {} locations'.format(engineer)
        distance_travelled = 0
        route_indices = []
        while not routing.IsEnd(current_place):
            route_indices.append(current_place)
            plan += ' {} -> '.format(manager.IndexToNode(current_place))
            previous_place = current_place
            current_place = solution.Value(routing.NextVar(current_place))
            distance_travelled += routing.GetArcCostForVehicle(previous_place, current_place, engineer)
        plan += '{}\n'.format(manager.IndexToNode(current_place))
        plan += 'Distance travelled: {} units'.format(distance_travelled)
        print(plan)
        all_routes.append(route_indices)
        total_distance += distance_travelled
    return all_routes

def problem_solver(distance_matrix, engineers, num_jobs, seconds):
    
    # Instantiate the data problem
    data = create_data_model(distance_matrix, engineers, num_jobs)
    len_dist_matrix = int(len(data['distance_matrix']))
    
    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len_dist_matrix,
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(seconds)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    # Print solution on console
    if solution:
        answer = return_solution(data, manager, routing, solution)
    
    return answer, solution.ObjectiveValue()

def solution_printer(data, solution):
    """
    Print the solution to the problem nicely
    """
    driver_routes = []

    for i, route in enumerate(solution):
        for j, location in enumerate(route):
            driver_routes.append((i,j,location))

    driver_routes_df = pd.DataFrame(driver_routes, columns = ['driver', 'order', 'index'])
    driver_routes_locations = pd.merge(data, driver_routes_df, on = 'index', how = 'inner')
    driver_routes_locations = driver_routes_locations.sort_values(['driver', 'order'])
    driver_routes_locations = driver_routes_locations.rename({'x':'x_coord',
                                                              'y':'y_coord'}, axis = 1)
    driver_routes_locations = driver_routes_locations.reset_index(drop = True)
    return driver_routes_locations
