import os
import time

import numpy as np


'''
The file contains an adjacency list representation of an undirected weighted
graph with 200 vertices labeled 1 to 200. Each row consists of the node tuples
that are adjacent to that particular vertex along with the length of that edge.

For example, the 6th row has 6 as the first entry indicating that this row
corresponds to the vertex labeled 6. The next entry of this row "141,8200"
indicates that there is an edge between vertex 6 and vertex 141 that has length 8200.
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as adjacency_list
    adjacency_list = []
    with open(file_directory, 'r') as file:
        for row in file:
            adjacency_list.append(np.array([i for i in row.split()]))
    file.closed

    # sort each row in adjacency_list by vertex label
    adjacency_list.sort(key=lambda row: int(row[0]))
    return adjacency_list


# method to return the vertex from tuple
def _vertex(tuple):
    return int(tuple.split(',')[0])


# method to return the distance from tuple
def _dist(tuple):
    return int(tuple.split(',')[1])


# method to return a list of w's neighbors
def _neightbors(graph, w):
    tuples = graph[w-1][1:]
    return [_vertex(tuple) for tuple in tuples]


# method to return the length defined by vetices u and v
def _length(graph, u, v):
    tuples = graph[u-1][1:]
    for tuple in tuples:
        if _vertex(tuple) == v:
            return _dist(tuple)


def find_shortest_path(adjacency_list, source, target):
    # total number of vertices
    N = len(adjacency_list)
    # dist[v] means the source-to-v distance
    dist = np.zeros((N,), dtype='uint32')
    # visited[v] indicates whether v is visted or not
    visited = np.zeros((N,), dtype='uint32')

    for v in np.arange(1, N+1, 1):
        # initialize unknown distance from source to each vertex v
        dist[v-1] = 1000000

    # distance from source to source is 0 trivially
    dist[source-1] = 0
    # mark source as visited
    visited[source-1] = 1

    # while there is still an unvisited vertex
    while np.sum(visited) != N:
        # find the shortest distance to an unvisited adjacent vertex
        w = None
        min_dist = 1000000
        # for each visited vertices
        for v in np.arange(1, N+1, 1):
            if visited[v-1] == 1:
                for tuple in adjacency_list[v-1][1:]:
                    # search any unvisited vertices
                    if visited[_vertex(tuple)-1] == 0:
                        curr_dist = dist[v-1] + _dist(tuple)
                        if curr_dist < min_dist:
                            # update min_dist
                            min_dist = curr_dist
                            w = _vertex(tuple)
                            dist[w-1] = min_dist

        # note that w is None when all nodes have been visited
        if w != None:
            visited[w-1] = 1

            # for each unvisited neighbors of w
            for v in _neightbors(adjacency_list, w):
                if visited[v-1] == 0:
                    alt = dist[w-1] + _length(adjacency_list, w, v)
                    # if a shorter path to v has been found
                    if alt < dist[v-1]:
                        dist[v-1] = alt

    return dist[target-1]


if __name__ == "__main__":
    start_time = time.time()
    source = 1
    targets = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    print('source vertex label:', source)
    print('target vertices labels:', targets)
    print('\ncomputing the shortest paths from source to targets...')
    adjacency_list = read_file('dijkstra.txt')
    distances = []
    for target in targets:
        distances.append(find_shortest_path(adjacency_list, source, target))
    print('source-to-target distances:', distances)
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
