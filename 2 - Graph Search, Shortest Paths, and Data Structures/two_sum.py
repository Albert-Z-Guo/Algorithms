import os
import time

import numpy as np


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as adjacency_list
    list = []
    with open(file_directory, 'r') as file:
        for row in file:
            list.append(int(row))

    return np.array(list)


# method to search for bound index
def find_index(bound, array):
    # if bound is greater than the greatest element of array
    if bound > array[-1]:
        return -1

    # if bound is smaller than the smallest element of array
    if bound < array[0]:
        return 0

    # if array[0] <= bound <= array[-1]
    i = 0
    while array[len(array) // 2] != bound:

        if bound < array[len(array) // 2]:
            array = array[:len(array) // 2]
        else:
            i += len(array) // 2
            array = array[len(array) // 2:]

        # if bound is not found in array
        if len(array) == 1 and array[0] != bound:
            # note that i + 1 satisfy the following two cases:
            #  - true index for lower bound
            #  - true index for upper bound + 1 in convenience for array slicing
            return i + 1

    # if bound is found in array
    return i + 1


def find_unique_targets_num(array):
    # sort array in order from the smallest to the greatest
    # and return unique elements only
    array = np.unique(array)

    valid_sums = []

    for i in np.arange(len(array)):
        # count iterations for testing purpose
        if i % 5000 == 0:
            print('i:', i)

        x = array[i]

        lower_bound = -10000 - x
        upper_bound = 10000 - x

        lower_bound_index = find_index(lower_bound, array)
        upper_bound_index = find_index(upper_bound, array)

        subarray = array[lower_bound_index : upper_bound_index]
        valid_sums = np.append(valid_sums, x + subarray)

    return len(np.unique(valid_sums))


if __name__ == "__main__":
    start_time = time.time()
    array = read_file('two_sum.txt')
    print('number of unique targets:', find_unique_targets_num(array))
    print('total time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
