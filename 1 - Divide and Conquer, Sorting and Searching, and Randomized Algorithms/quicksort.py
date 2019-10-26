import os
import time
import numpy as np

COMPARISONS = 0

def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as list
    with open(file_directory, 'r') as file:
        list = file.readlines()

    # convert to integer for each element in list
    integer_array = [int(i) for i in list]
    return integer_array


def _swap(A, i, j):
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp


def _choose_pivot(A, l, r):
    '''
    input: array A of n distinct integers, left and right endopoints l, r
    output: an index i
    '''
    # pick the first element
    # return l

    # pick the last element
    # return r

    # pick the median of the firt, middle, and the last elements
    middle = int((l + r)/2)
    median = np.median([A[l], A[middle], A[r]])
    if A[l] == median:
        return l
    if A[middle] == median:
        return middle
    if A[r] == median:
        return r


def _partition(A, l, r):
    '''
    input: array A of n distinct integers, left and right endopoints l, r
    postcondition: elements of the subarrays are partitioned around A
    output: final position of pivot element
    '''
    p = A[l]
    i = l+1
    for j in np.arange(l+1, r+1, 1):
        if A[j] < p:
            _swap(A, i, j)
            i += 1
    _swap(A, l, i-1)
    return i - 1


def quick_sort(A, l, r):
    '''
    input: array A of n distinct integers, left and right endopoints l, r
    postcondition: elements of the subarrays are sorted from smallest to largest
    '''
    global COMPARISONS

    # 0- or 1-element subarray
    if l >= r:
        return

    i = _choose_pivot(A, l ,r)

    # make pivot first
    _swap(A, l, i)

    # j is made the new pivot position
    j = _partition(A, l ,r)

    COMPARISONS += (j-1) - l + 1
    quick_sort(A, l, j-1)

    COMPARISONS += r - (j+1) + 1
    quick_sort(A, j+1, r)


if __name__ == "__main__":
    start_time = time.time()
    integer_array = read_file('quicksort.txt')
    quick_sort(integer_array, 0, len(integer_array)-1)
    print('integer_array_sorted:', integer_array)
    print('COMPARISONS:', COMPARISONS)
    print('total running time: {0:.2} seconds'.format(time.time() - start_time))
