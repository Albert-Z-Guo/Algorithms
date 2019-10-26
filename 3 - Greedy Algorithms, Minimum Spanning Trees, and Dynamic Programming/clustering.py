import os
import time

import numpy as np


'''
The file clustering.txt describes a distance function (equivalently, a complete
graph with edge costs). It has the following format:

[number_of_nodes]
[edge 1 node 1] [edge 1 node 2] [edge 1 cost]
[edge 2 node 1] [edge 2 node 2] [edge 2 cost]
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    edge_list = []
    num_vertices = 0
    num_edges = 0

    # read in data as an edge list
    with open(file_directory, 'r') as file:
        # read the first line
        num_vertices = int(file.readline().split()[0])

        # read the following lines
        for row in file:
            row = np.array([int(i) for i in row.split()])
            num_edges += 1
            edge_list.append(row)

    return edge_list, num_vertices, num_edges


# method to check whether the two vertices in edge are clustered
def _is_clustered(edge, vertex_cluster_labels):
    return vertex_cluster_labels[edge[0]-1] != vertex_cluster_labels[edge[1]-1]


def find_maximum_space_of_k_clustering(edge_list, num_vertices):
    # final clusters number
    K = 4

    # initial cluster labels for each vertex
    vertex_cluster_labels = np.arange(1, num_vertices+1, 1)

    # while the final clusters number is not reached
    while len(set(vertex_cluster_labels)) != K:
        # initialize parameters
        min_cost = 1000000
        chosen_vertex_pair = []
        # search for the closest vertex pair
        for edge in edge_list:
            # if the pair is not clustered
            if _is_clustered(edge, vertex_cluster_labels):
                if edge[2] < min_cost:
                    # update min_cost
                    min_cost = edge[2]
                    chosen_vertex_pair = edge

        # merge the chosen vertex pair (p, q) into a single cluster
        # by relabelling all q labels to p label
        p = chosen_vertex_pair[0]
        q = chosen_vertex_pair[1]
        pair_label = vertex_cluster_labels[q-1]
        for i in np.arange(len(vertex_cluster_labels)):
            if vertex_cluster_labels[i] == pair_label:
                vertex_cluster_labels[i] = vertex_cluster_labels[p-1]

    # search for the maximum spacing of a K-clustering
    min_cost = 1000000
    # search for the closest vertex pair (p, q)
    for edge in edge_list:
        # if the pair is not clustered
        if _is_clustered(edge, vertex_cluster_labels):
            if edge[2] < min_cost:
                # update min_cost
                min_cost = edge[2]

    return min_cost


if __name__ == "__main__":
    start_time = time.time()
    edge_list, num_vertices, num_edges = read_file('clustering.txt')
    print('number of vertices:', num_vertices)
    print('number of edges:', num_edges)
    print('max_spacing:', find_maximum_space_of_k_clustering(edge_list, num_vertices))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
