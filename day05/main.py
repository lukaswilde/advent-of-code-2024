import copy
import re
from typing import List, Tuple, Set

from input import read_split_input

class AdjacencyMatrix():

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.matrix = [[0] * dimension for _ in range(dimension)]

    def fill(self, edges: List[Tuple[int, int]]):
        for (x,y) in edges:
            self.matrix[x][y] = 1

    @staticmethod
    def create_and_fill(edges: List[Tuple[int, int]]):
        dimension = max([value for edge in edges for value in edge]) + 1
        matrix = AdjacencyMatrix(dimension)
        matrix.fill(edges)
        return matrix

    def get_submatrix(self, relevant_nodes: List[int]):
        submatrix = AdjacencyMatrix(len(relevant_nodes))
        submatrix.matrix = [[self.matrix[node][idx] for idx in relevant_nodes] for node in relevant_nodes]
        return submatrix

    def get_incoming(self, node: int):
        return [self.matrix[j][node] for j in range(self.dimension)]

    def get_outgoing(self, node:int):
        return self.matrix[node]

    def is_topologically_sorted(self) -> bool:
        for i in range(self.dimension):
            incoming_edges = self.get_incoming(i)
            if any(incoming_edges[i:]):
                return False
        return True

    def get_sources(self) -> Set[int]:
        result = set()
        for i in range(self.dimension):
            if any(self.get_incoming(i)):
                continue
            result.add(i)

        return result

    def sort_topologically(self) -> List[int]:
        """
        Sort indices topologically using Kahn's algorithm.
        Returns a list of indices of the update in correct topological order
        """
        tmp = copy.deepcopy(self)

        result = []
        covered_nodes = set()

        no_incoming_edges = tmp.get_sources()
        covered_nodes.update(no_incoming_edges)

        while len(no_incoming_edges) > 0:
            next_idx = no_incoming_edges.pop()
            result.append(next_idx)
            tmp.matrix[next_idx] = [0] * tmp.dimension
            no_incoming_edges.update(tmp.get_sources() - covered_nodes)
            covered_nodes.update(no_incoming_edges)

        return result


def extract_parts(file_name: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    sections = read_split_input(file_name)
    assert len(sections) == 2
    edge_list, page_list = sections[0], sections[1]

    edges = [tuple(int(node) for node in edge.split("|", 1)) for edge in edge_list.splitlines()]
    pages = [[int(page) for page in update.split(",")] for update in page_list.splitlines()]

    return edges, pages


def calculate_sum_correct_middles(matrix: AdjacencyMatrix, pages: List[List[int]]) -> int:
    result = 0
    for update in pages:
        assert len(update) % 2 == 1
        submatrix = matrix.get_submatrix(update)
        if submatrix.is_topologically_sorted():
            result += update[len(update)//2]

    return result


def calculate_sum_incorrect_middles(matrix: AdjacencyMatrix, pages: List[List[int]]) -> int:
    result = 0
    for update in pages:
        assert len(update) % 2 == 1
        submatrix = matrix.get_submatrix(update)
        if not submatrix.is_topologically_sorted():
            correct_order = submatrix.sort_topologically()
            assert len(correct_order) % 2 == 1
            middle_idx = correct_order[len(correct_order)//2]
            result += update[middle_idx]

    return result


def part1(file_name: str) -> int:
    edges, pages = extract_parts(file_name)
    matrix = AdjacencyMatrix.create_and_fill(edges)
    return calculate_sum_correct_middles(matrix, pages)


def part2(file_name: str) -> int:
    edges, pages = extract_parts(file_name)
    matrix = AdjacencyMatrix.create_and_fill(edges)
    return calculate_sum_incorrect_middles(matrix, pages)


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f'Total sum of middle page numbers in correct updates: {result1}')

    result2 = part2('puzzle.txt')
    print(f'Total sum of middle page numbers after sorting: {result2}')
