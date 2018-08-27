import os
import sys
import time

import numpy as np

sys.setrecursionlimit(3000)  # raise recursion limit


'''
The file knapsack.txt describes a knapsack instance self.

It has the following format:

[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
'''


# global variables
value_dict = {}
weight_dict = {}
tuple_value_dict = {}


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

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

    return items_num, knapsack_size


# method to find the optimal knapsack value recursively
# optimized with memoization
def find_optimal_knapsack(i, w):
    '''
    i : first i number of items
    w : capacity size
    '''
    # check if find_optimal_knapsack(i, w) is stored
    if (i, w) in tuple_value_dict:
        return tuple_value_dict[(i, w)]

    # if find_optimal_knapsack(i, w) is not stored
    else:
        # if base case
        if i - 1 == 0:
            tuple_value_dict[(i, w)] = 0
            return 0
        # if not base case
        else:
            if weight_dict[i] > w:
                value = find_optimal_knapsack(i - 1, w)
                tuple_value_dict[(i, w)] = value
                return value
            else:
                value = max(find_optimal_knapsack(i - 1, w), find_optimal_knapsack(i - 1, w - weight_dict[i]) + value_dict[i])
                tuple_value_dict[(i, w)] = value
                return value


if __name__ == "__main__":
    start_time = time.time()
    items_num, knapsack_size = read_file('knapsack_big.txt')
    print('optimal knapsack value:', find_optimal_knapsack(items_num, knapsack_size))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time) / 60))
