import os
import matplotlib.pyplot as plt

file_name = 'tsp.txt'
file_directory = os.path.join(os.path.dirname(__file__), file_name)

x_values = []
y_values = []
labels = []

with open(file_directory, 'r') as file:
    # read the first line
    num_cities = int(file.readline())

    # read the following lines
    i = 1
    for row in file:
        row = row.split()
        x_values.append(float(row[0]))
        y_values.append(float(row[1]))
        labels.append(i)
        i += 1
file.closed

print('number of cities:', num_cities)

plt.figure(figsize=(8,6), dpi=100)
plt.scatter(x_values, y_values, marker='o')

# overlap distances
plt.plot([23883.3333, 24166.6667], [14533.3333, 13250.0000], 'r')

for i, label in enumerate(labels):
    plt.annotate(label, xy=(x_values[i], y_values[i]))
plt.show()
