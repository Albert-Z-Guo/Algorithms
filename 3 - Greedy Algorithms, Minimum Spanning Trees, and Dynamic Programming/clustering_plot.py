import os
import time

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()

file_name = 'clustering_plot.txt'
file_directory = os.path.join(os.path.dirname(__file__), file_name)
with open(file_directory, 'r') as file:
    for row in file:
        row = [int(i) for i in row.split()]
        if len(row) != 1:
            G.add_edge(row[0], row[1], weight=row[2])

plt.figure(figsize=(10,6))
position = nx.kamada_kawai_layout(G)
labels = nx.get_edge_attributes(G,'weight')
nx.draw(G, pos=position, with_labels=True, font_weight='bold')
print(nx.draw_networkx_edge_labels(G, pos=position, edge_labels=labels))
plt.show()
