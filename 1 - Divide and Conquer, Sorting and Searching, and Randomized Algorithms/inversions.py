import os
import time

import numpy as np


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    # read in data as list
    with open(file_directory, 'r') as file:
        list = file.readlines()

    # convert to integer for each element in list
    integer_array = [int(i) for i in list]
    return integer_array


def merge_and_count_split_inv(C, D):
    '''
    input: sorted arrays C and D (length n/2 each)
    output: sorted array B (length n) and the number of
            split inversions
    '''
    i = 0
    j = 0
    split_inv = 0
    n = len(C) + len(D) # note that C and D may have different lengths
    B = []

    for k in np.arange(n):
        if i < len(C) and j < len(D) and C[i] < D[j]:
            B.append(C[i])
            i += 1

        if i < len(C) and j < len(D) and C[i] >= D[j]:
            B.append(D[j])
            j += 1
            split_inv += len(C) - i

        # if all elements in C are copied already
        # copy all elements in D
        if i == len(C):
            while j < len(D):
                B.append(D[j])
                j += 1

        # if all elements in D are copied already
        # copy all elements in C
        if j == len(D):
            while i < len(C):
                B.append(C[i])
                i += 1

    return B, split_inv


def sort_and_count_inv(A):
    '''
    input: array A of n distinct integers
    output: sorted array B with the same integers, and
            the number of inversions of A
    '''
    n = len(A)
    if n == 0 or n == 1:
        return A, 0
    else:
        C, left_inv = sort_and_count_inv(A[:int(len(A) / 2)])
        D, right_inv = sort_and_count_inv(A[int(len(A) / 2):])
        B, split_inv = merge_and_count_split_inv(C, D)
        return B, left_inv + right_inv + split_inv


if __name__ == "__main__":
    start_time = time.time()
    integer_array = read_file('inversions.txt')
    # integer_array = [6, 5, 4, 3, 2, 1] # test
    integer_array_sorted, inversions = sort_and_count_inv(integer_array)

    print('integer_array_sorted:', integer_array_sorted)
    print('inversions:', inversions)
    print('total running time: {0:.2} seconds'.format(time.time() - start_time))
