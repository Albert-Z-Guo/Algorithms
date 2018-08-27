import os
import time
import random

import numpy as np


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as adjacency_list
    adjacency_list = []
    with open(file_directory, 'r') as file:
        for row in file:
            row = np.array([int(i) for i in row.split()])
            adjacency_list.append(row)
    file.closed

    # sort each row in adjacency_list by vertex label
    adjacency_list.sort(key=lambda row: row[0])
    return adjacency_list


# Karger's Minimum Cut algorithm
def calculate_min_cut(adjacency_list):
    # initialize the minimum cut value
    min_cut = 100

    # iteration = int(np.square(200) * np.log(200))
    for i in range(20): # set iteraton to only 20 due to speed limit
        # if i % 500 == 0:
            # print('iteration:', i)
        adjacency_list_reduced = [row[1:] for row in adjacency_list]
        vertices_remained = np.array([row[0] for row in adjacency_list])

        # reset random seed
        random.seed(i)

        # run Karger's Minimum Cut algorithm until only 2 vertices left
        while (len(vertices_remained) != 2):
            # choose an edge formed by vertices v and v_adj randomly
            # random.choice(seq) returns a random element from a non-empty sequence seq
            v = random.choice(vertices_remained)
            v_adj = random.choice(adjacency_list_reduced[v-1])

            # merge two vertices v and v_adj and keep v only
            # step 1: move connections to v_adj to v
            vertices_to_be_redirected = adjacency_list_reduced[v_adj-1]
            for i in vertices_to_be_redirected:
                tmp = np.array(adjacency_list_reduced[i-1])
                np.place(tmp, tmp==v_adj, v)
                adjacency_list_reduced[i-1] = tmp

            # step 2: move connections from v_adj to v
            adjacency_list_reduced[v-1] = np.r_[adjacency_list_reduced[v-1], adjacency_list_reduced[v_adj-1]]

            # remove selfloops of v if there is any
            while (v in adjacency_list_reduced[v-1]):
                adjacency_list_reduced[v-1] = np.delete(adjacency_list_reduced[v-1], np.where(adjacency_list_reduced[v-1] == v)[0], axis=0)

            vertices_remained = np.delete(vertices_remained, np.where(vertices_remained == v_adj)[0], axis=0)
            # test
            # print(vertices_remained)

        cut = len(adjacency_list_reduced[vertices_remained[0]-1])
        print('cut:', cut)
        if cut < min_cut:
            min_cut = cut

    return min_cut


if __name__ == "__main__":
    start_time = time.time()
    adjacency_list = read_file('mincut.txt')
    print('min_cut:', calculate_min_cut(adjacency_list))
    print('total running time: {0:.2} seconds'.format(time.time() - start_time))
