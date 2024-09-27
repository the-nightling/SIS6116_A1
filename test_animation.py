import os
from modules.tsp_file_parser.tsp_file_parser import TSP

problem_name = "berlin52.tsp"
currentFolderPath: str = os.path.abspath("")
tspFilePath = os.path.join(currentFolderPath, f"data\\{problem_name}")
print("Loading .tsp file from path: " + tspFilePath)

tsp = TSP(tspFilePath)
print(tsp.name + " was loaded")


import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import random


# Function to update the transparency of specific edges
def update_transparency(frame, lines_dict, edge_transparencies, rates):
    # for i, line in enumerate(lines):
    #     alpha = max(0, edge_transparencies[i] + rates[i] * frame)
    #     if alpha > 1:
    #         alpha = 1
    #     line[1].set_alpha(alpha)

    for i in range(len(x_values)):
        for j in range(len(x_values)):
            if i == j:
                continue

            edge_pheromone_level: float = random.randrange(30)
            edge_alpha: float = edge_pheromone_level / 30
            if edge_alpha > 1:
                edge_alpha = 1

            if (i, j) in lines_dict:
                lines_dict[(i, j)].set_alpha(edge_alpha)
            else:
                lines_dict[(j, i)].set_alpha(edge_alpha)

    return lines_dict.values()


x_values: list[float] = [i[0] for i in tsp.nodeCoords]
y_values: list[float] = [i[1] for i in tsp.nodeCoords]

# Plot the complete graph
G = nx.complete_graph(len(x_values))
pos: dict[int, tuple[float, float]] = {
    i: (x_values[i], y_values[i]) for i in range(len(x_values))
}
fig, ax = plt.subplots()
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=300)

# Get the edges and their corresponding lines
edges = list(G.edges())
# lines = [
#     (
#         (edge[0], edge[1]),
#         ax.plot(
#             [pos[edge[0]][0], pos[edge[1]][0]],
#             [pos[edge[0]][1], pos[edge[1]][1]],
#             color="gray",
#             alpha=0,
#         )[0],
#     )
#     for edge in edges
# ]

lines_dict = {
    (edge[0], edge[1]): ax.plot(
        [pos[edge[0]][0], pos[edge[1]][0]],
        [pos[edge[0]][1], pos[edge[1]][1]],
        color="gray",
        alpha=0,
    )[0]
    for edge in edges
}

# print(lines_dict)

# Define the edges with custom transparency and their rates
custom_edges: list[int] = [0, 1, 2]  # Indices of the edges to modify
edge_transparencies: list[float] = [0.0] * len(edges)  # Initial transparency
rates: list[float] = [0.01] * len(edges)  # Rates at which transparency decreases
rates[1] = 0.02
rates[2] = 0.03

# Create the animation
ani = FuncAnimation(
    fig,
    update_transparency,
    frames=100,
    fargs=(lines_dict, edge_transparencies, rates),
    interval=100,
    blit=True,
)

plt.show()
