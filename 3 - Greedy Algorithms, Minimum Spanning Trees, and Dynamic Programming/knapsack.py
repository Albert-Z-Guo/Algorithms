import os
import time

import numpy as np


'''
The file knapsack.txt describes a knapsack instanceself.

It has the following format:

[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
'''


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    value_dict = {}
    weight_dict = {}

    # read in data as nodes in heap
    with open(file_directory, 'r') as file:
        # read the first line
        knapsack_size, items_num = map(int, file.readline().split())

        # read the following lines
        i = 1
        for row in file:
            value, weight = map(int, row.split())
            value_dict[i] = value
            weight_dict[i] = weight
            i += 1
    file.closed

    print('knapsack size:', knapsack_size)
    print('number of items:', items_num)

    return value_dict, weight_dict, knapsack_size, items_num


def find_optimal_knapsack(value_dict, weight_dict, knapsack_size, items_num):
    N = items_num
    W = knapsack_size

    # initialization
    # note that if no item is taken, optimal solution is always 0
    value = np.zeros((N+1, W+1), dtype='uint')

    for i in np.arange(1, N+1, 1):
        for w in np.arange(W+1):
            if w - weight_dict[i] < 0:
                value[i][w] = value[i-1][w]
            else:
                value[i][w] = max(value[i-1][w], value[i-1][w-weight_dict[i]] + value_dict[i])

    return value[-1][-1]


if __name__ == "__main__":
    start_time = time.time()
    value_dict, weight_dict, knapsack_size, items_num = read_file('knapsack.txt')
    print('optimal knapsack value:', find_optimal_knapsack(value_dict, weight_dict, knapsack_size, items_num))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
