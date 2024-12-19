import bisect
from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path
from typing import Optional

from geometry import Grid, Vec2d, manhattan_distance
from input import extract_vectors, read_input

from template import Day


class Map(Grid):
    def __init__(self, repr):
        super().__init__(repr)

        self.start = Vec2d(0, 0)
        self.goal = Vec2d(self.width - 1, self.height - 1)
        self.obstacle_pos = []


def generate_successors(state: Vec2d, map: Map, limit: int):
    return [
        neighbor
        for neighbor in map.generate_neighbors(state)
        if neighbor not in map.obstacle_pos[:limit]
    ]


def a_star(map: Map, num_obstacles_present: int) -> Optional[int | float]:
    """
    Runs A* algorithm on the map. Start position is `map.start`, goal is `map.goal`.
    Returns the cost of a minimum cost path from start to goal. This is guaranteed with an
    admissible heuristic, which the Manhattan Distance is in a grid setting.
    """
    start_state = map.start

    g_score = defaultdict(lambda: float('inf'))
    g_score[start_state] = 0

    frontier = [(0, start_state)]
    closed = set()
    seen = {start_state}

    while len(frontier) > 0:
        f, state = heappop(frontier)
        closed.add(state)

        if state == map.goal:
            assert isinstance(g_score[state], int)
            return g_score[state]

        for successor in generate_successors(state, map, num_obstacles_present):
            if successor in closed:
                assert successor in seen
                continue

            next_g = g_score[state] + 1

            if successor in seen and next_g >= g_score[successor]:
                continue

            seen.add(successor)
            g_score[successor] = next_g
            next_f = next_g + manhattan_distance(successor, map.goal)
            heappush(frontier, (next_f, successor))


def extract_map(file_path: Path) -> Map:
    input_text = read_input(file_path)
    obstacle_pos = [extract_vectors(line)[0] for line in input_text.splitlines()]

    width = max([obstacle.x for obstacle in obstacle_pos]) + 1
    height = max([obstacle.y for obstacle in obstacle_pos]) + 1

    map = Map.from_dimensions(width, height)
    map.obstacle_pos = obstacle_pos

    return map


def bin_search_num_obstacles(map: Map) -> Optional[float]:
    """
    Performs a binary search on the number of obstacles needed to completely block the path in the map.
    Returns this minimal number of obstacles, if there is no way, returns None
    """

    # def bin_search(lower: int, upper: int) -> Optional[float]:
    #     if lower > upper:
    #         return None
    #
    #     if lower == upper:
    #         if a_star(map, lower) is None:
    #             return lower
    #         return None
    #
    #     pivot = (lower + upper) // 2
    #     result = a_star(map, pivot)
    #
    #     if result is None:
    #         return bin_search(lower, pivot - 1)
    #
    #     return bin_search(pivot + 1, upper)
    #
    # coordinate_idx = bin_search(0, len(map.obstacle_pos))

    coordinate_idx = bisect.bisect_left(
        range(len(map.obstacle_pos)), True, key=lambda limit: a_star(map, limit) is None
    )
    return map.obstacle_pos[int(coordinate_idx) - 1]


class Day18(Day):
    def part1(self, file_path: Path) -> float:
        limit = 1024 if 'puzzle' in str(file_path) else 12
        map = extract_map(file_path)
        return a_star(map, limit) or -1

    def part2(self, file_path: Path) -> float:
        map = extract_map(file_path)
        return bin_search_num_obstacles(map) or -1


if __name__ == '__main__':
    day = Day18()
    day.print_solution('puzzle.txt')
