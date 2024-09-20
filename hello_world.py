# import networkx as nx
# import matplotlib.pyplot as plt


# G = nx.Graph()  # undirected graph
# G = nx.DiGraph()		# directed graph
# G = nx.MultiGraph()		# multiple edges between nodes
# G = nx.MultiDiGraph()

# G.add_edge(1, 2)
# G.add_edge(2, 3, weight=0.9)
# G.add_edge("A", "B")
# G.add_node("C")

# import tsplib95

# problem = tsplib95.load("a280.tsp")
# G = problem.get_graph()

# nx.draw_spring(G, with_labels=True)
# nx.draw_kamada_kawai(G, with_labels=True)
# nx.draw(G, with_labels=True)
# nx.draw_spectral(G)
# nx.draw_circular(G)
# plt.show()

from tsp_file_parser_old import TSPParser

TSPParser(filename=".\\data\\a280.tsp", plot_tsp=True)
