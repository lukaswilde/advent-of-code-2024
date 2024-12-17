from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path
from typing import Optional, Tuple

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


def a_star(map: Map) -> Optional[int]:
    """
    Runs A* algorithm on the map. Start position is `m.start`, goal is `m.goal`.
    Returns the cost of a minimum cost path from start to goal. This is guaranteed with an
    admissible heuristic, which the Manhattan Distance is in a grid setting.
    """

    def generate_successors(state: Tuple[Vec2d, Direction]):
        point, facing = state
        right_rot = facing.rotate_right()
        left_rot = facing.rotate_left()
        successors = [(point, right_rot), (point, left_rot)]

        forward_loc = point + facing.value
        if not map.out_of_bounds(forward_loc) and forward_loc not in map.obstacles:
            successors.append((forward_loc, facing))

        return successors

    start_state = (map.start, Direction.RIGHT)

    g_score = defaultdict(lambda: float('inf'))
    g_score[start_state] = 0

    frontier = [(0, *start_state)]
    closed = set()
    entries = {start_state}

    while len(frontier) > 0:
        heuristic, *state = heappop(frontier)
        state = tuple(state)
        closed.add(state)

        if state[0] == map.goal:
            assert isinstance(g_score[state], int)
            return g_score[state]

        for successor in generate_successors(state):
            if successor in closed:
                assert successor in entries
                continue

            next_g = g_score[state] + (1 if state[1] == successor[1] else 1000)

            if successor in entries and next_g >= g_score[successor]:
                continue

            entries.add(successor)
            g_score[successor] = next_g
            next_f = next_g + manhattan_distance(successor[0], map.goal)
            heappush(frontier, (next_f, *successor))

    return None


def extract_map(file_path: Path) -> Map:
    input_text = read_input(file_path)
    return Map(input_text)


class Day16(Day):
    def part1(self, file_path: Path) -> int:
        map = extract_map(file_path)
        return a_star(map) or -1

    def part2(self, file_path: Path) -> int:
        ...
        # map, directions = extract_sections_wider(file_path)
        # map.execute_directions(directions, wide=True)
        # return map.get_gps_score()


if __name__ == '__main__':
    day = Day16()
    day.print_solution('example2.txt')
