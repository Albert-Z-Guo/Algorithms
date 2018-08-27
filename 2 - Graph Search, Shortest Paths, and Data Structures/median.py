import os
import time
import heapq as minheap

import numpy as np
import maxheap


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as adjacency_list
    list = []
    with open(file_directory, 'r') as file:
        for row in file:
            list.append(int(row))
    file.closed

    return list


def find_medians(list):
    N = len(list)

    # heap that supports max extraction
    heap_low = []
    # heap that supports min extraction
    heap_high = []

    # initialize the numpy array that contains the medians
    medians = np.zeros((N,), dtype='uint')

    # median of just one number is just the number itself
    medians[0] = list[0]

    # median of two numbers is the smaller of the two
    if list[0] < list[1]:
        maxheap.heappush(heap_low, list[0])
        minheap.heappush(heap_high, list[1])
        medians[1] = list[0]
    else:
        maxheap.heappush(heap_low, list[1])
        minheap.heappush(heap_high, list[0])
        medians[1] = list[1]

    # median of more than two numbers...
    for k in np.arange(2, N, 1):
        if list[k] < heap_low[0]:
            maxheap.heappush(heap_low, list[k])
        else:
            minheap.heappush(heap_high, list[k])

        # if two heaps are inbalanced, balace the two heaps
        if abs(len(heap_low) - len(heap_high)) == 2:
            if len(heap_low) > len(heap_high):
                minheap.heappush(heap_high, maxheap.heappop(heap_low))
            else:
                maxheap.heappush(heap_low, minheap.heappop(heap_high))

        # find the median
        if len(heap_low) >= len(heap_high):
            medians[k] = heap_low[0]
        else:
            medians[k] = heap_high[0]

    return medians


if __name__ == "__main__":
    start_time = time.time()
    list = read_file('median.txt')
    medians = find_medians(list)
    print(np.sum(medians) % 10000)
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
