import os
import time

import numpy as np


'''
The file clustering.txt describes an implicit distance function.

The distance between two nodes uu and vv in this problem is defined as
the Hamming distance--- the number of differing bits --- between the two
nodes' labels.

It has the following format:

[# of nodes] [# of bits for each node's label]
[first bit of node 1] ... [last bit of node 1]
[first bit of node 2] ... [last bit of node 2]

For example, the Hamming distance between the 24-bit label
of node #2 above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1"
is 3 (since they differ in the 3rd, 7th, and 21st bits).
'''


# global variables
cluster_labels = []
cluster_sizes = []


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    vertex_index_map = {}

    num_vertices = 0
    num_distinct_vertices = 0
    num_vertex_bits = 0

    # read in data as a vertex_index_map
    with open(file_directory, 'r') as file:
        # read the first line
        num_vertices, num_vertex_bits = map(int, file.readline().split())

        # read the following lines
        for row in file:
            vertex_string = ' '.join(row.split())
            # avoid duplicates
            if vertex_string not in vertex_index_map:
                vertex_index_map[vertex_string]= num_distinct_vertices
                num_distinct_vertices += 1

    print('number of vertices:', num_vertices)
    print('number of distinct vertices:', num_distinct_vertices)
    print('number of vertex bits:', num_vertex_bits)

    # initialize clusters' labels and sizes
    global cluster_labels
    global cluster_sizes

    cluster_labels = np.arange(num_distinct_vertices)
    cluster_sizes = np.ones((num_distinct_vertices,), dtype='uint32')

    return vertex_index_map, num_distinct_vertices


def _root(i):
    global cluster_labels

    while (i != cluster_labels[i]):
        # compress paths by making every other node in path point to its grandparent
        cluster_labels[i] = cluster_labels[cluster_labels[i]]
        i = cluster_labels[i]
    return i


def _same_cluster(p, q):
    return _root(p) == _root(q)


def _union(p, q):
    i = _root(p)
    j = _root(q)

    global cluster_labels
    global cluster_sizes

    # merge the smaller tree into the larger tree
    if (cluster_sizes[i] < cluster_sizes[j]):
        cluster_labels[i] = j
        cluster_sizes[j] += cluster_sizes[i]
    else:
        cluster_labels[j] = i
        cluster_sizes[i] += cluster_sizes[j]


def _reverse_digit(digit):
    if digit == 1:
        return 0
    else:
        return 1


def _one_hamming_distance_list(vertex_bits):
    list = []
    for i in np.arange(len(vertex_bits)):
        candidate = vertex_bits.copy()
        candidate[i] = _reverse_digit(candidate[i])
        list.append(candidate)
    return list


def _two_hamming_distance_list(vertex_bits):
    list = []
    for i in np.arange(len(vertex_bits)):
        for j in np.arange(i+1, len(vertex_bits), 1):
            candidate = vertex_bits.copy()
            candidate[i] = _reverse_digit(candidate[i])
            candidate[j] = _reverse_digit(candidate[j])
            list.append(candidate)
    return list


# method to find the number of merging until the minimum hamming distance
# across all vertices pairs is at least 3
def find_num_merging(vertex_index_map, num_distinct_vertices):
    num_merging = 0

    # for each vertex
    for vertex, i in vertex_index_map.items():
        vertex_bits = np.fromstring(vertex, dtype=int, sep=' ')

        # find all possible vertices with one or two hamming distance away
        candidates = _one_hamming_distance_list(vertex_bits) + _two_hamming_distance_list(vertex_bits)
        for candidate in candidates:

            # if the candidate is indeed in the map
            candidate_vertex_string = ' '.join([str(i) for i in candidate])
            if candidate_vertex_string in vertex_index_map:

                # if the two vertices are not in the same cluster
                if not _same_cluster(i, vertex_index_map[candidate_vertex_string]):
                    _union(i, vertex_index_map[candidate_vertex_string])
                    num_merging += 1

    return num_merging


if __name__ == "__main__":
    # estimated running time: 30 min
    start_time = time.time()
    vertex_index_map, num_distinct_vertices = read_file('clustering_big.txt')
    num_merging = find_num_merging(vertex_index_map, num_distinct_vertices)
    print('number of vertices left:', num_distinct_vertices - num_merging)
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
