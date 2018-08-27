import os
import time

import numpy as np


'''
The file mwis.txt describes the weights of the vertices in a path graph
(with the weights listed in the order in which vertices appear in the path).

It has the following format:

[number_of_vertices]
[weight of first vertex]
[weight of second vertex]
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    weight_list = []

    # read in data as nodes in heap
    with open(file_directory, 'r') as file:
        # read the first line
        num_vertices = int(file.readline())

        # read the following lines
        for row in file:
            weight_list.append(int(row))
    file.closed

    print('number of vertices:', num_vertices)

    return weight_list


def find_max_weight_independent_set(weight_list):
    # number of vertices
    N = len(weight_list)

    # A[i] represents sum of the maximum-weight independent set up to ith vertex
    A = []
    # maximum-weight independent set includes the empty set
    A.append(0)
    # maximum-weight independent set includes the set with just a single element
    A.append(weight_list[0])

    # iterate from vertex 2 to vertex N
    for i in np.arange(2, N+1, 1):
        A.append(max(A[i-1], A[i-2] + weight_list[i-1]))

    # set of vertices that comprises the maximum-weight independent set
    S = []
    j = N
    while j >= 1:
        if A[j - 1] >= A[j - 2] + weight_list[j-1]:
            j -= 1
        else:
            S.append(j)
            j -= 2

    return S


def generate_bits(S):
    string = ''
    vertices = [1, 2, 3, 4, 17, 117, 517, 997]
    print('vertices:', vertices)

    for vertex in vertices:
        if vertex in S:
            string += '1'
        else:
            string += '0'

    return string


if __name__ == "__main__":
    start_time = time.time()
    weight_list = read_file('maximum_weight_independent_set.txt')
    S = find_max_weight_independent_set(weight_list)
    print('bits:', generate_bits(S))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
