import os
import sys
import threading # thread-based parallelism
from collections import defaultdict


graph_original = defaultdict(list)
graph_reversed = defaultdict(list)
graph_new = defaultdict(list)

node_time_dict = {}
time_leader_dict = {}

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


def depth_first_search_loop(graph):
    # loop through every node
    # (by finishing time from the longest to the shortest)
    for node in _sort_nodes(graph):
        if node not in explored:
            global source
            source = node
            _depth_first_search(graph, node)


def _sort_nodes(graph):
    nodes = {}
    for node, neighbors in graph.items():
        nodes[node] = 1
        for neighbor in neighbors:
            nodes[neighbor] = 1
    nodes = list(nodes.keys())
    nodes.sort(reverse=True)
    return nodes


def _depth_first_search(graph, node):
    global explored
    global leaders
    global source

    explored[node] = 1
    leaders[node] = source

    if node in graph:
        for neighbor in graph[node]:
            if neighbor not in explored:
                _depth_first_search(graph, neighbor)

    global t
    t += 1
    global finishing_times
    finishing_times[node] = t


# method to replace all nodes' names by finishing times
def replace_node_name(graph):
    global graph_new
    graph_new.clear()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            graph_new[finishing_times[node]].append(finishing_times[neighbor])


# Kosaraju's algorithm to find the strongly connected components
def kosaraju():
    # reset parameters when the algorithm is repeatedly called
    global explored
    global leaders
    global finishing_times
    global t
    global source
    explored.clear()
    leaders.clear()
    finishing_times.clear()
    t = 0
    source = None

    depth_first_search_loop(graph_reversed)

    global node_time_dict
    node_time_dict = finishing_times.copy()

    replace_node_name(graph_original)

    # reset parameters
    explored.clear()
    leaders.clear()
    finishing_times.clear()
    t = 0
    source = None

    depth_first_search_loop(graph_new)

    global time_leader_dict
    time_leader_dict = leaders.copy()
