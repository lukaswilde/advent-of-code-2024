from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path
from typing import Optional, Set, Tuple

from geometry import Direction, Grid, Vec2d, manhattan_distance
from input import read_input

from template import Day


class Map(Grid):
    def __init__(self, repr: str):
        super().__init__(repr)
        self.start = self.find_unique('S')
        self.goal = self.find_unique('E')
        assert self.start is not None
        assert self.goal is not None

        self.obstacles = set(self.find_all('#'))


def generate_successors(state: Tuple[Vec2d, Direction], map: Map):
    point, facing = state
    right_rot = facing.rotate_right()
    left_rot = facing.rotate_left()
    successors = [(point, right_rot), (point, left_rot)]

    forward_loc = point + facing.value
    if not map.out_of_bounds(forward_loc) and forward_loc not in map.obstacles:
        successors.append((forward_loc, facing))

    return successors


def a_star(map: Map) -> Optional[int | float]:
    """
    Runs A* algorithm on the map. Start position is `m.start`, goal is `m.goal`.
    Returns the cost of a minimum cost path from start to goal. This is guaranteed with an
    admissible heuristic, which the Manhattan Distance is in a grid setting.
    """
    start_state = (map.start, Direction.RIGHT)

    g_score = defaultdict(lambda: float('inf'))
    g_score[start_state] = 0

    frontier = [(0, *start_state)]
    closed = set()
    seen = {start_state}

    while len(frontier) > 0:
        f, point, direction = heappop(frontier)
        state = (point, direction)
        closed.add(state)

        if state[0] == map.goal:
            assert isinstance(g_score[state], int)
            return g_score[state]

        for successor in generate_successors(state, map):
            if successor in closed:
                assert successor in seen
                continue

            next_g = g_score[state] + (1 if state[1] == successor[1] else 1000)

            if successor in seen and next_g >= g_score[successor]:
                continue

            seen.add(successor)
            g_score[successor] = next_g
            next_f = next_g + manhattan_distance(successor[0], map.goal)
            heappush(frontier, (next_f, *successor))


def cost_limited_dfs(map: Map, max_cost: int) -> Set[Vec2d]:
    """
    Runs an exhausting DFS algorithm on the map. Start position is `m.start`, goal is `m.goal`.
    If the goal is found, we do not abort, but add the visited nodes to a set
    that is returned in the end. All visited nodes across all cheapest paths are accumulated.
    """

    def dfs_helper(
        path: Set[Vec2d],
        node: Tuple[Vec2d, Direction],
        current_cost: int,
        terminated: defaultdict[Vec2d, float],
    ) -> Set[Vec2d]:
        if node[0] == map.goal:
            return path | {node[0]}

        if current_cost >= max_cost:
            return set()

        if current_cost > terminated[node[0]]:
            return set()

        res = set()
        for successor in generate_successors(node, map):
            cost = 1 if successor[1] == node[1] else 1000
            visited = dfs_helper(path | {node[0]}, successor, current_cost + cost, terminated)
            res.update(visited)

        if len(res) == 0:
            terminated[node[0]] = min(terminated[node[0]], current_cost)

        return res

    start_state = (map.start, Direction.RIGHT)
    return dfs_helper(set(), start_state, 0, defaultdict(lambda: float('inf')))


def extract_map(file_path: Path) -> Map:
    input_text = read_input(file_path)
    return Map(input_text)


class Day16(Day):
    def part1(self, file_path: Path) -> int:
        map = extract_map(file_path)
        return a_star(map) or -1

    def part2(self, file_path: Path) -> int:
        map = extract_map(file_path)
        shortest_distance = a_star(map) or -1
        assert shortest_distance > 0
        return len(cost_limited_dfs(map, shortest_distance))


if __name__ == '__main__':
    day = Day16()
    day.print_solution('puzzle.txt')
