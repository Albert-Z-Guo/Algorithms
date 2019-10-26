import os
import time
import itertools

import numpy as np


'''
The file traveling_salesman.txt describes a symetric traveling salesman problem.

The first line indicates the number of cities.
Each city is a point in the plane, and each subsequent line indicates
the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --
that is, two cities at locations (x,y) and (z,w) have distance
\sqrt{(x-z)^2 + (y-w)^2} between them.

To solve this problem, traveling_salesman_plot.py is used to visualize all
cities' locations and we decompose tsp.txt into 2 parts:
traveling_salesman_part_1.txt
traveling_salesman_part_2.txt

We compute the optimal paths separately to infer the global optimal path.
'''


# method to find the Euclidean distance between two locations
def _dist(location_1, location_2):
    return np.sqrt(np.square(location_1[0] - location_2[0]) + np.square(location_1[1] - location_2[1]))


# method to load the distance matrix
def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    index_location_dict = {}

    with open(file_directory, 'r') as file:
        # read the first line
        num_cities = int(file.readline())

        # read the following lines
        index = 0
        for row in file:
            index_location_dict[index] = [float(i) for i in row.split()]
            index += 1

    distance_matrix = np.zeros((num_cities, num_cities))
    for i in np.arange(num_cities):
        for j in np.arange(num_cities):
            distance_matrix[i][j] = _dist(index_location_dict[i], index_location_dict[j])

    print('number of cities:', num_cities)

    return distance_matrix


# (subset, destination) to distance dictionary
tuple_dist_dict = {}


# references:
# https://github.com/CarlEkerot/held-karp/blob/master/held-karp.py
# https://www.tutorialspoint.com/python/bitwise_operators_example.htm

# method to find the minimum traveling distance
def find_min_dist(dist):
    # number of cities
    N = dist.shape[0]

    # range starts from 2 since all subsets contain 1
    range = np.arange(2, N+1, 1)

    # permutation_lengths starts from 1 to N - 1
    permutation_len = np.arange(1, N, 1)

    # base case initialization
    # subset S is in bit set representation
    # note that 2 is '10' in binary form, which means only 1 is included in set
    S = 2

    # the distance from the source to itself is 0
    tuple_dist_dict[(S, 1)] = 0

    # set the distance to infinity otherwise
    # since the path cannot both start and end at the source
    for len in permutation_len:
        for subset in itertools.combinations(range, r=len):
            S = 2
            for i in subset:
                S |= 1 << i
                tuple_dist_dict[(S, 1)] = np.inf

    # for each subproblem
    for size in np.arange(1, N+1, 1):
        # for each subset of size
        for subset in itertools.combinations(range, size):
            S = 2
            for i in subset:
                S |= 1 << i

            # for each j in S
            for j in subset:
                # find min{tuple_dist_dict[S - {J}, k] + dist_kj} for all k
                # where k is in S and k != j
                S_reduced = S & ~(1 << j)
                candidates = []
                for k in (1,) + subset:
                    if k != j:
                        candidates.append(tuple_dist_dict[(S_reduced, k)] + dist[k-1][j-1])

                tuple_dist_dict[(S, j)] = min(candidates)

    # find minimum of tuple_dist_dict[{1, 2, ..., n}, j] + dist_j1
    # for j = 2, 3, ... n
    # note that the binary form for 2**(N+1) - 2 is 11...10 with n ones and 1 zero
    S = 2**(N+1) - 2
    candidates = []
    for j in np.arange(2, N+1, 1):
        candidates.append(tuple_dist_dict[(S, j)] + dist[j-1][0])
    return min(candidates)


if __name__ == "__main__":
    start_time = time.time()
    min_dist_part_1 = find_min_dist(read_file('traveling_salesman_part_1.txt'))
    print('minimum distance for part 1:', min_dist_part_1, '\n')

    min_dist_part_2 = find_min_dist(read_file('traveling_salesman_part_2.txt'))
    print('minimum distance for part 2:', min_dist_part_2, '\n')

    # overlap_dist can be visualized by traveling_salesman_plot.py
    overlap_dist = 2*_dist([23883.3333, 14533.3333], [24166.6667, 13250.0000])
    min_dist = int(np.floor(min_dist_part_1 + min_dist_part_2 - overlap_dist))
    print('minimum distance for the traveling salesman:', min_dist)
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
