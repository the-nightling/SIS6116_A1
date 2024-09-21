## 1. Parse TSP file

import os
from modules.tsp_file_parser import TSP

# problemName = "ulysses16.tsp"
problemName = "a280.tsp"
currentFolderPath = os.path.abspath("")
tspFilePath = os.path.join(currentFolderPath, f"data\\{problemName}")
print("Loading .tsp file from path: " + tspFilePath)

tsp = TSP(tspFilePath)
print(tsp.name + " was loaded")


## 2. Plot TSP Graph

import matplotlib.pyplot as plt

x_values = [i[0] for i in tsp.nodeCoords]
y_values = [i[1] for i in tsp.nodeCoords]

plt.plot(x_values, y_values, "r--", zorder=0)  # type: ignore
plt.scatter(x_values, y_values)  # type: ignore

for i in range(tsp.dimension):
    plt.annotate(str(i + 1), (x_values[i], y_values[i]))  # type: ignore

plt.show()  # type: ignore


## 3. Experiment
import math

totalDistance = 0

for i in range(1, tsp.dimension):
    x1 = x_values[i - 1]
    y1 = y_values[i - 1]
    x2 = x_values[i]
    y2 = y_values[i]
    distance: float = math.dist([x1, y1], [x2, y2])  # type: ignore
    print(f"({x1}, {y1}), ({x2}, {y2}) -> {distance}")
    totalDistance = totalDistance + float(distance)  # type: ignore

print(totalDistance)
