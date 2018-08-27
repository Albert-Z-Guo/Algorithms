import os
import time

import numpy as np


'''
The following files describe three graphs:

g1.txt
g2.txt
g3.txt

For each graph, the first line indicates the number of vertices and edges, respectively.
Each subsequent line describes an edge (the first two numbers are its tail
and head, respectively) and its length (the third number).
NOTE: some of the edge lengths are negative.
NOTE: These graphs may or may not have negative-cost cycles.
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    with open(file_directory, 'r') as file:
        # read the first line
        num_vertices, num_edges = map(int, file.readline().split())

        # initialize the shortest i-to-j distances that uses k along with
        # possibly other lower-numbered intermediate nodes
        dist = np.full((num_vertices, num_vertices, 2), fill_value=np.inf)

        # read the following lines
        for row in file:
            i, j, cost_ij = map(int, row.split())
            # if a path does not exist
            if dist[i-1][j-1][0] == np.inf:
                # note that a path with non-zero cost from one vertex to itself is allowed
                dist[i-1][j-1][0] = cost_ij
            # if a path exists already
            else:
                # choose the path with smaller cost
                if cost_ij < dist[i-1][j-1][0]:
                    dist[i-1][j-1][0] = cost_ij
    file.closed

    print('number of vertices:', num_vertices)
    print('number of edges:', num_edges)

    return dist, num_vertices


# space-optimized Floyd-Warshall algorithm
def all_pairs_shortest_paths(dist, num_vertices):
    column_0 = 0
    column_1 = 1

    for k in np.arange(1, num_vertices+1, 1):
        # print k in case the running time is long
        # if k % 100 == 0:
        #     print('k:', k)
        for i in np.arange(num_vertices):
            for j in np.arange(num_vertices):

                if i == j and dist[i][j][column_0] < 0:
                    print('negative cycle detected!')
                    return

                dist[i][j][column_1] = min(dist[i][j][column_0], dist[i][k-1][column_0] + dist[k-1][j][column_0])

        # swap column index
        column_0, column_1 = column_1, column_0

    return int(np.amin(dist))


if __name__ == "__main__":
    start_time = time.time()
    # estimated running time: 6 min
    dist, num_vertices = read_file('g1.txt')
    print('shortest of shortest paths:', all_pairs_shortest_paths(dist, num_vertices))

    # estimated running time: 6 min
    # dist, num_vertices = read_file('g2.txt')
    # print('shortest of shortest paths:', all_pairs_shortest_paths(dist, num_vertices))

    # estimated running time: 70 min
    # dist, num_vertices = read_file('g3.txt')
    # print('shortest of shortest paths:', all_pairs_shortest_paths(dist, num_vertices))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
