import random
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

    def iterate_AS(self):
        self.evaporate_pheromone()

        starting_vertices: list[int] = list(range(self.number_of_nodes))

        for ant in self.ants:
            if (
                not starting_vertices
            ):  # if we have more ants than nodes, place ant on already occupied nodes
                starting_vertices = list(range(self.number_of_nodes))

            start_vertex: int = random.choice(starting_vertices)
            starting_vertices.remove(start_vertex)

            ant.compute_tour_AS(start_vertex)
            ant.compute_tour_cost()

        for ant in self.ants:
            self.add_pheromone(ant.tour, self.q / ant.tour_cost)

            if ant.tour_cost < self.best_tour_cost:
                self.best_tour = ant.tour
                self.best_tour_cost = ant.tour_cost

    # TODO
    def iterate_ACS(self, q_0: float):
        self.evaporate_pheromone()

        starting_vertices: list[int] = list(range(self.number_of_nodes))

        for ant in self.ants:
            if (
                not starting_vertices
            ):  # if we have more ants than nodes, place ant on already occupied nodes
                starting_vertices = list(range(self.number_of_nodes))

            start_vertex: int = random.choice(starting_vertices)
            starting_vertices.remove(start_vertex)

            ant.compute_tour_ACS(start_vertex, q_0)
            ant.compute_tour_cost()

        for ant in self.ants:
            self.add_pheromone(ant.tour, self.q / ant.tour_cost)

            if ant.tour_cost < self.best_tour_cost:
                self.best_tour = ant.tour
                self.best_tour_cost = ant.tour_cost
