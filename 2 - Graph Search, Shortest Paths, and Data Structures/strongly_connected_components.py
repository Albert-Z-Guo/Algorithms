import os
import sys
import time
import pickle
import threading # thread-based parallelism
import collections # container datatypes

import numpy as np


'''
The file strongly_connected_components.txt contains the edges of a directed graph.
Vertices are labeled as positive integers from 1 to 875714.
Every row indicates an edge, the vertex label in first column is the tail
and the vertex label in second column is the head
'''


# number of distinct nodes
N = 875714


def _remove_indices(adjacency_list_indexed):
    global N
    adjacency_list = []
    for i in np.arange(N):
        adjacency_list.append(np.delete(adjacency_list_indexed[i], 0, axis=0))
    return adjacency_list


def generate_adjacency_lists(file_name):
    if os.path.exists('adjacency_list.pickle') and os.path.exists('adjacency_list_indexed.pickle'):
        with open('adjacency_list.pickle', 'rb') as f:
            adjacency_list = pickle.load(f)

        with open('adjacency_list_indexed.pickle', 'rb') as f:
            adjacency_list_indexed = pickle.load(f)

        print('found previously generated files')
    else:
        print('Loading data from .txt file...')
        file_directory = os.path.join(os.getcwd(), file_name)
        data = np.loadtxt(file_directory, dtype='uint32')

        global N
        adjacency_list_indexed = []
        # index the adjacency list
        for i in np.arange(N):
            adjacency_list_indexed.append(np.array([i]))
        for row in data:
            adjacency_list_indexed[row[0]-1] = np.append(adjacency_list_indexed[row[0]-1], row[1])

        # remove indices
        adjacency_list = _remove_indices(adjacency_list_indexed)

        # save processed files
        with open("adjacency_list.pickle", "wb") as p:
            pickle.dump(adjacency_list, p)

        with open("adjacency_list_indexed.pickle", "wb") as p:
            pickle.dump(adjacency_list_indexed, p)

        # delete data to save memory
        del data

    return adjacency_list, adjacency_list_indexed


def generate_reversed_adjacency_lists(file_name):
    if os.path.exists('adjacency_list_reversed.pickle') and os.path.exists('adjacency_list_indexed_reversed.pickle'):
        with open('adjacency_list_reversed.pickle', 'rb') as f:
            adjacency_list_reversed = pickle.load(f)

        with open('adjacency_list_indexed_reversed.pickle', 'rb') as f:
            adjacency_list_indexed_reversed = pickle.load(f)

        print('found previously generated files')
    else:
        print('Loading data from .txt file...')
        file_directory = os.path.join(os.getcwd(), file_name)
        data = np.loadtxt(file_directory, dtype='uint32')

        global N
        adjacency_list_indexed_reversed = []
        # index the adjacency list
        for i in np.arange(N):
            adjacency_list_indexed_reversed.append(np.array([i]))
        for row in data:
            adjacency_list_indexed_reversed[row[1]-1] = np.append(adjacency_list_indexed_reversed[row[1]-1], row[0])

        # remove indices
        adjacency_list_reversed = _remove_indices(adjacency_list_indexed_reversed)

        # save processed files
        with open("adjacency_list_reversed.pickle", "wb") as p:
            pickle.dump(adjacency_list_reversed, p)

        with open("adjacency_list_indexed_reversed.pickle", "wb") as p:
            pickle.dump(adjacency_list_indexed_reversed, p)

        # delete data to save memory
        del data

    return adjacency_list_reversed, adjacency_list_indexed_reversed


# marks for whether nodes are explored
node_marks = np.zeros((N,), dtype='uint32')
# orders for nodes' finishing times
node_orders = np.zeros((N,), dtype='uint32')
# leaders for nodes
node_leaders = np.zeros((N,), dtype='uint32')
# number of nodes processed so far
t = 0
# current source vertex from which depth_first_search is initiated
s = None


def depth_first_search_loop(graph):
    '''
    graph : adjacency list
    '''
    global N
    global node_marks
    global node_leaders

    # loop through every node in graph
    # (from the one with largest finishing time)
    for i in np.arange(N, 0, -1):
        # if node i is not yet explored
        if node_marks[i-1] == 0:
            # identify source node
            global s
            s = i
            depth_first_search(graph, i)


def depth_first_search(graph, i):
    '''
    graph : adjacency list
    i : node index
    '''
    global node_marks
    global node_leaders
    global s

    # mark node i as explored
    node_marks[i-1] = 1
    # mark node i's leader as s
    node_leaders[i-1] = s

    if len(graph[i-1]) != 0:
        # iterate each arc ij in graph
        for j in graph[i-1]:
            # if node j is not yet explored
            if node_marks[j-1] == 0:
                depth_first_search(graph, j)
    global t
    t += 1
    global node_orders
    node_orders[i-1] = t


# method to replace nodes' names and nodes' adacencies according to node orders
def replace_node_names(adjacency_list_indexed, node_orders):
    global N
    new_adjacency_list_indexed = []
    # index the adjacency list
    for i in np.arange(N):
        new_adjacency_list_indexed.append(np.array([i]))

    # replace indices' names
    for j in np.arange(N):
        new_adjacency_list_indexed[ node_orders[j]-1 ] = adjacency_list_indexed[j]

    # remove indices
    new_adjacency_list = _remove_indices(new_adjacency_list_indexed)

    # replace indices' adjacencies' names
    for k in np.arange(N):
        for l in np.arange(len(new_adjacency_list[k])):
            new_adjacency_list[k][l] = node_orders[ new_adjacency_list[k][l]-1 ]

    return new_adjacency_list


def count_leaders(node_leaders):
    leader_counter = collections.Counter(node_leaders)
    count = list(leader_counter.values())
    count.sort(reverse=True)
    return count[0:5]


def print_running_time_so_far(start_time):
    print('running time so far: {0:.2} minutes\n'.format((time.time() - start_time)/60))


# Kosaraju algorithm implementation
def main():
    start_time = time.time()
    file_name = 'strongly_connected_components.txt'
    print('Generating adjacency lists...')
    adjacency_list, adjacency_list_indexed = generate_adjacency_lists(file_name)
    print_running_time_so_far(start_time)

    print('Generating reversed adjacency lists...')
    adjacency_list_reversed, adjacency_list_indexed_reversed = generate_reversed_adjacency_lists(file_name)
    print_running_time_so_far(start_time)

    print('First depth-first search pass...')
    depth_first_search_loop(adjacency_list_reversed)
    print_running_time_so_far(start_time)

    print('Replacing nodes names by finishing times...')
    global node_orders
    new_adjacency_list = replace_node_names(adjacency_list_indexed, node_orders)
    print_running_time_so_far(start_time)

    # reset parameters
    global node_marks
    global node_leaders
    global t
    global s
    node_marks = np.zeros((N,), dtype='uint32')
    node_orders = np.zeros((N,), dtype='uint32')
    node_leaders = np.zeros((N,), dtype='uint32')
    t = 0
    s = None

    print('Second depth-first search pass...')
    depth_first_search_loop(new_adjacency_list)
    print_running_time_so_far(start_time)

    print('Count leaders...')
    leaders_count = count_leaders(node_leaders)

    print('Top 5 numbers of strongly connected components:', leaders_count)
    print_running_time_so_far(start_time)


if __name__ == "__main__":
    sys.setrecursionlimit(2 ** 20) # raise recursion limit
    threading.stack_size(2 ** 26) # raise stack size
    thread = threading.Thread(target=main)
    thread.start()
