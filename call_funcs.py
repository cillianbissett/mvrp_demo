import numpy as np
import pandas as pd

def data_generator(num_calls, x_lim, y_lim):
    """
    Generates a number of call locations in x-y space.
    """
    # generate x - y data
    x = np.random.randint(0, x_lim, num_calls)
    y = np.random.randint(0, y_lim, num_calls)

    # build data frame
    locations = pd.DataFrame([x,y]).T
    locations.columns = ['x', 'y']
    locations = locations.reset_index(drop = False)
    return locations

def distance_finder(locations):
    """
    Ingests a dataframe with columns corresponding to call index, call x coord, call y coord
    and produces the corresponding distance matrix. 
    """
    # need a distance matrix
    distance_matrix = []

    # this will be replaced with API calls for traffic times
    for i in range(len(locations)):
        i_distances = []
        for j in range(len(locations)):
            # euclidean distance for demo
            distance = int(((locations['x'].iloc[i] - locations['x'].iloc[j])**2 + (locations['y'].iloc[i] - locations['y'].iloc[j])**2)**0.5)
            i_distances.append(distance)
        distance_matrix.append(i_distances)
    return distance_matrix