from .node import Node
from .ant import Ant, Edge
from .utilities import calculate_euclidian_distance


class AntColony:
    def __init__(
        self,
        number_of_ants: int,
        alpha: float,
        beta: float,
        rho: float,
        q: float,
        initial_pheromone_level: float,
        maximum_number_of_iterations: int,
        nodes: list[Node],
    ) -> None:
        self.number_of_ants: int = number_of_ants
        self.alpha: float = alpha
        self.beta: float = beta
        self.rho: float = rho
        self.q: float = q
        self.maximum_number_of_iterations: int = maximum_number_of_iterations
        self.nodes: list[Node] = nodes
        self.number_of_nodes: int = len(nodes)

        self.edges: list[list[Edge]] = [  # type: ignore
            [None for _ in range(self.number_of_nodes)]
            for _ in range(self.number_of_nodes)
        ]
        for i in range(self.number_of_nodes):
            for j in range(self.number_of_nodes):
                edge_cost: float = calculate_euclidian_distance(
                    self.nodes[i], self.nodes[j]
                )
                self.edges[i][j] = self.edges[j][i] = Edge(
                    i, j, edge_cost, initial_pheromone_level
                )

        self.ants: list[Ant] = [
            Ant(self.edges, alpha, beta, self.number_of_nodes)
            for _ in range(self.number_of_ants)
        ]

        self.best_tour: list[int] = []
        self.best_tour_cost: float = float("inf")

    def add_pheromone(self, tour: list[int], heuristic: float):
        for i in range(self.number_of_nodes):
            self.edges[tour[i]][
                tour[(i + 1) % self.number_of_nodes]
            ].pheromone_level += heuristic

    def evaporate_pheromone(self):
        for i in range(self.number_of_nodes):
            for j in range(self.number_of_nodes):
                self.edges[i][j].pheromone_level *= 1 - self.rho

    def iterate(self):
        self.evaporate_pheromone()

        for ant in self.ants:
            tour: list[int] = ant.compute_tour()
            tour_cost: float = ant.compute_tour_cost()
            self.add_pheromone(tour, self.q / tour_cost)

            if ant.tour_cost < self.best_tour_cost:
                self.best_tour = ant.tour
                self.best_tour_cost = ant.tour_cost
