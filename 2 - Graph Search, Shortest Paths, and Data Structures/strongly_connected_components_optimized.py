import os
import sys
import threading # thread-based parallelism
from collections import defaultdict
from collections import Counter

import numpy as np


'''
The file strongly_connected_components.txt contains the edges of a directed graph.
Vertices are labeled as positive integers from 1 to 875714.
Every row indicates an edge, the vertex label in first column is the tail
and the vertex label in second column is the head
'''


# nodes' marks
explored = {}
# nodes' finishing times
finishing_times ={}
# nodes' leaders
leaders = {}
# number of nodes processed so far
t = 0
# current source node from which _depth_first_search is initiated
source = None
# number of distinct nodes
N = 875714


def depth_first_search_loop(graph):
    # loop through every node
    # (by finishing time from the longest to the shortest)
    for i in np.arange(N, 0, -1):
        if i not in explored:
            global source
            source = i
            _depth_first_search(graph, i)


def _depth_first_search(graph, i):
    global explored
    global leaders
    explored[i] = 1
    leaders[i] = source

    if i in graph:
        for neighbor in graph[i]:
            if neighbor not in explored:
                _depth_first_search(graph, neighbor)

    global t
    t += 1
    global finishing_times
    finishing_times[i] = t


# method to replace all nodes by their finishing times
def replace_node_name(graph):
    graph_new = defaultdict(list)
    for i, neighbors in graph.items():
        for neighbor in neighbors:
            graph_new[finishing_times[i]].append(finishing_times[neighbor])
    return graph_new


def find_component_number():
    leader_counter = Counter(leaders.values())
    component_numbers = list(leader_counter.values())
    component_numbers.sort(reverse=True)
    print(component_numbers[0:5])


def kosaraju():
    graph_original = defaultdict(list)
    graph_reversed = defaultdict(list)

    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), 'strongly_connected_components.txt')

    with open(file_directory, 'r') as input_file:
    	for line in input_file:
    		u = int(line.split()[0])
    		v = int(line.split()[1])
    		graph_original[u].append(v)
    		graph_reversed[v].append(u)

    depth_first_search_loop(graph_reversed)

    # replace all nodes by their finishing times
    graph_new = replace_node_name(graph_original)

    # reset the following global parameters
    global explored
    global leaders
    global t
    global source
    explored.clear()
    leaders.clear()
    t = 0
    source = None

    depth_first_search_loop(graph_new)
    find_component_number()


if __name__ == "__main__":
    sys.setrecursionlimit(2 ** 20) # raise recursion limit
    threading.stack_size(2 ** 26) # raise stack size
    thread = threading.Thread(target=kosaraju)
    thread.start()
