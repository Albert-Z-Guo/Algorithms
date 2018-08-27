import os
import time
import random

import numpy as np


'''
The file edges.txt describes an undirected graph with integer edge costs.
It has the format:
[number_of_nodes] [num_edges]
[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    adjacency_list = {}
    num_vertices = 0
    num_edges = 0

    # read in data as adjacency list
    with open(file_directory, 'r') as file:
        # read the first line
        num_vertices, num_edges = map(int, file.readline().split())

        # read the following lines
        for row in file:
            row = [int(i) for i in row.split()]

            # if the vertex is already in adjacency_list
            if row[0] in adjacency_list:
                adjacency_list[row[0]] = adjacency_list[row[0]] + [row[1:]]

                # complement the adjacency_list since the graph is not directed
                if row[1] in adjacency_list:
                    adjacency_list[row[1]] = adjacency_list[row[1]] + [[row[0], row[2]]]
                else:
                    adjacency_list[row[1]] = [[row[0], row[2]]]

            # if the vertex is not in adjacency_list
            else:
                adjacency_list[row[0]] = [row[1:]]

                # complement the adjacency_list since the graph is not directed
                if row[1] in adjacency_list:
                    adjacency_list[row[1]] = adjacency_list[row[1]] + [[row[0], row[2]]]
                else:
                    adjacency_list[row[1]] = [[row[0], row[2]]]
    file.closed

    print('number of vertices:', num_vertices)
    print('number of edges::', num_edges)

    return adjacency_list, num_vertices, num_edges


# Prim's algorithm
def find_min_spanning_tree(adjacency_list, num_vertices):
    # initialize the minimum spanning tree
    minimum_spanning_tree = []

    # number of vertices
    N = num_vertices

    # spanned[v] indicates whether vertex v is spanned or not
    spanned = np.zeros((N,), dtype='uint32')

    # random.randint(a, b) returns a random integer x such that a <= x <= b
    source = random.randint(1, N)
    print('randomly chosen source vertex label:', source)

    # mark source as spanned
    spanned[source - 1] = 1

    # while there is still an unspanned vertex
    while np.sum(spanned) != N:
        # initialize parameters
        min_cost = 1000000
        min_edge = []
        # for each spanned vertices
        for v in np.arange(1, N+1, 1):
            # find the cheapest edge with only one vertex spanned
            if spanned[v-1] == 1:
                for edge in adjacency_list[v]:
                    # if the adjacent vertex is not spanned
                    if spanned[edge[0]-1] != 1:
                        if edge[1] < min_cost:
                            min_cost = edge[1]
                            min_edge = edge

        # append min_edge to the minimum spanning tree
        minimum_spanning_tree.append(min_edge)

        # mark min_edge as spanned
        spanned[min_edge[0]-1] = 1

    return minimum_spanning_tree


def calculate_total_cost(minimum_spanning_tree):
    total_cost = 0
    for edge in minimum_spanning_tree:
        total_cost += edge[1]
    return total_cost


if __name__ == "__main__":
    start_time = time.time()
    adjacency_list, num_vertices, num_edges = read_file('edges.txt')
    minimum_spanning_tree = find_min_spanning_tree(adjacency_list, num_vertices)
    print('overall cost of the minimum spanning tree:', calculate_total_cost(minimum_spanning_tree))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
