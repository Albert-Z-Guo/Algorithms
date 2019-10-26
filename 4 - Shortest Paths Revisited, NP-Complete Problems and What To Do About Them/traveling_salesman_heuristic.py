import os
import time

import numpy as np


'''
The file nn.txt describes a symetric traveling salesman problem.

The first line indicates the number of cities.
Each city is a point in the plane, and each subsequent line indicates
the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --
that is, two cities at locations (x,y) and (z,w) have distance
\sqrt{(x-z)^2 + (y-w)^2} between them.

We implement the nearest neighbor heuristic:
1. Start the tour at the first city.
2. Repeatedly visit the closest city that the tour hasn't visited yet.
    In case of a tie, go to the closest city with the lowest index.
    For example, if both the third and fifth cities have the same distance
    from the first city (and are closer than any other city), then the tour
    should begin by going from the first city to the third city.
3. Once every city has been visited exactly once, return to the first city
    to complete the tour.
'''


# method to load the distance matrix
def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    index_location_dict = {}

    with open(file_directory, 'r') as file:
        # read the first line
        num_cities = int(file.readline())

        # read the following lines
        for row in file:
            row = [float(i) for i in row.split()]
            index_location_dict[int(row[0])] = row[1:]

    print('number of cities:', num_cities)

    return index_location_dict


def _dist_square(location_1, location_2):
    return np.square(location_1[0] - location_2[0]) + np.square(location_1[1] - location_2[1])


def find_traveling_dist(index_location_dict):
    # start the tour at the first city
    source_location = index_location_dict[1]
    del index_location_dict[1]

    total_traveling_dist = 0
    location_processed_num = 0
    start_location = source_location

    # while index_location_dict is not empty
    while bool(index_location_dict) != False:
        if location_processed_num % 500 == 0:
            print('number of processed locations:', location_processed_num)

        # find the nearest neighbor distance squared
        min_neighbor_dist_square = np.inf
        selected_neighbor_index = 1

        for index, location in index_location_dict.items():
            dist_square = _dist_square(start_location, location)
            if dist_square == min_neighbor_dist_square:
                if index < selected_neighbor_index:
                    selected_neighbor_index = index
            if dist_square < min_neighbor_dist_square:
                min_neighbor_dist_square = dist_square
                selected_neighbor_index = index

        location_processed_num += 1

        # update total_traveling_dist
        total_traveling_dist += np.sqrt(min_neighbor_dist_square)

        # update start_location
        start_location = index_location_dict[selected_neighbor_index]
        del index_location_dict[selected_neighbor_index]

    # add the distance from the final city back to the source
    total_traveling_dist += np.sqrt(_dist_square(source_location, start_location))

    return int(np.floor(total_traveling_dist))


if __name__ == "__main__":
    # estimated running time: 40 min
    start_time = time.time()
    index_location_dict = read_file('nn.txt')
    print('distance for traveling salesman:', find_traveling_dist(index_location_dict))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
