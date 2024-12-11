from pathlib import Path

from geometry import Grid, Vec2d
from input import read_input

from template import Day


class Map(Grid):
    def __init__(self, repr: str):
        super().__init__(repr)

        self.sources = set()
        self.apply_on_values(int)

        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                if self[point] == 0:
                    self.sources.add(point)


def extract_height_map(file_path: Path) -> Map:
    input_text = read_input(file_path)
    return Map(input_text)


def calculate_single_metric(source: Vec2d, map: Map, remember_visited: bool = True):
    # Rating is number of unique trails
    # We can just do a complete search, because there are no cycles in the map
    # (remember that hike trails are increasing, so cycles are naturally impossible)
    # Ignore the visited set, and we will get the rating instead of score

    visited = set()
    queue = [source]
    count = 0

    while len(queue) != 0:
        next_node = queue.pop()
        if map[next_node] == 9:
            count += 1
        if remember_visited:
            visited.add(next_node)

        for neighbor in map.generate_neighbors(next_node):
            if map[neighbor] - map[next_node] != 1:
                continue
            if (not remember_visited) or (neighbor not in visited):
                queue.append(neighbor)

    return count


def calculate_total_score(map: Map) -> int:
    return sum([calculate_single_metric(source, map) for source in map.sources])


def calculate_total_rating(map: Map) -> int:
    return sum([calculate_single_metric(source, map, False) for source in map.sources])


class Day10(Day):
    def part1(self, file_path: Path) -> int:
        map = extract_height_map(file_path)
        return calculate_total_score(map)

    def part2(self, file_path: Path) -> int:
        map = extract_height_map(file_path)
        return calculate_total_rating(map)


if __name__ == '__main__':
    day = Day10()
    day.print_solution('rating_large.txt')
