import os
import sys
import time
import threading # thread-based parallelism
from collections import defaultdict

import strongly_connected_components_module as scc


'''
The files 2sat1.txt to 2sat6.txt are as follows.

In each instance, the number of variables and the number of clauses is the same,
and this number is specified on the first line of the file.
Each subsequent line specifies a clause via its two literals, with a number
denoting the variable and a "-" sign denoting logical "not".
For example, the second line of the first data file is "-16808 75250",
which indicates the clause -x_{16808} V x_{75250}.
'''


# reference:
# https://www.geeksforgeeks.org/2-satisfiability-2-sat-problem/

# method to generate Implication Graph from Conjunctive Normal Form
# For example, Conjunctive Normal Form A V B can be expressed as
# -A -> B and -B -> A in Implication Graph.
def read_file(file_name):
    graph_original = defaultdict(list)
    graph_reversed = defaultdict(list)
    nodes = []

    with open(file_name, 'r') as file:
        # read the first line
        num_clauses = int(file.readline())

        # read the following lines
        for row in file:
            x, y = map(int, row.split())
            graph_original[-x].append(y)
            graph_original[-y].append(x)
            graph_reversed[y].append(-x)
            graph_reversed[x].append(-y)
            nodes.append(x)
            nodes.append(y)
    file.closed

    print('number of clauses:', num_clauses)

    return graph_original, graph_reversed, nodes


def check_satisfiability(nodes):
    times = scc.node_time_dict
    leaders = scc.time_leader_dict

    for node in nodes:
        if leaders[times[node]] == leaders[times[-node]]:
            return 0
    return 1


def main():
    for i in range(1, 7):
        file_name = '2sat' + str(i) + '.txt'
        graph_original, graph_reversed, nodes = read_file(file_name)

        scc.graph_original = graph_original
        scc.graph_reversed = graph_reversed
        scc.kosaraju()

        print(check_satisfiability(nodes))


if __name__ == "__main__":
    sys.setrecursionlimit(2 ** 30) # raise recursion limit
    threading.stack_size(2 ** 30) # raise stack size
    thread = threading.Thread(target=main)
    thread.start()
