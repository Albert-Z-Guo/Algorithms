import os
import time
import heapq as minheap
from functools import total_ordering

import numpy as np


'''
The file huffman.txt describes an instance of the problem.

It has the following format:

[number_of_symbols]
[weight of symbol #1]
[weight of symbol #2]
'''


# references: http://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
@total_ordering
class Symbol:
    def __init__(self, weight, index):
        self.weight = weight
        self.index = index
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        if other == None:
            return 0
        return self.weight == other.weight


def read_file(file_name):
    # locate file directory
    file_directory = os.path.join(os.path.dirname(__file__), file_name)

    heap = []
    index = 0

    # read in data as nodes in heap
    with open(file_directory, 'r') as file:
        # read the first line
        num_symbols = int(file.readline())

        # read the following lines
        for row in file:
            node = Symbol(int(row), index)
            minheap.heappush(heap, node)
            index += 1

    print('number of symbols:', num_symbols)

    return heap


def generate_root(heap):
    while len(heap) != 1:
        symbol_1 = minheap.heappop(heap)
        symbol_2 = minheap.heappop(heap)
        node_merged = Symbol(symbol_1.weight + symbol_2.weight, None)
        node_merged.left = symbol_1
        node_merged.right = symbol_2
        minheap.heappush(heap, node_merged)

    return minheap.heappop(heap)


index_code_dict = {}


# method to encode symbols by traversing through the tree from the generated root
def encode(symbol, current_code):

    # if reaching the leaves, which do have indices
    if symbol.index != None:
        index_code_dict[symbol.index] = current_code
        return

    encode(symbol.left, current_code + '0')
    encode(symbol.right, current_code + '1')


if __name__ == "__main__":
    start_time = time.time()
    heap = read_file('huffman.txt')
    root = generate_root(heap)
    encode(root, '')

    code_lengths = []
    for index, code in index_code_dict.items():
        code_lengths.append(len(code))

    print('maximum code length:', max(code_lengths))
    print('minimum code length:', min(code_lengths))
    print('total running time: {0:.2} minutes\n'.format((time.time() - start_time)/60))
