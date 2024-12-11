from collections import defaultdict
from pathlib import Path
from typing import List, Tuple

from geometry import Grid, Vec2d
from input import read_input

from template import Day


class Map(Grid):
    def __init__(self, repr: str):
        super().__init__(repr)

        self.antennas = defaultdict(list)

        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                char = self[point]
                if char != '.':
                    self.antennas[char].append(point)

        self.combinations = self._calculate_combinations()

    def _calculate_combinations(self) -> List[Tuple[Vec2d, Vec2d]]:
        res = []
        for same_type in self.antennas.values():
            for i, pos1 in enumerate(same_type):
                for pos2 in same_type[i + 1 :]:
                    res.append((pos1, pos2))

        return res


def calculate_unique_antinodes(map: Map) -> int:
    unique_antinodes = set()

    for pos1, pos2 in map.combinations:
        difference = pos1 - pos2
        if not map.out_of_bounds(antinode := pos1 + difference):
            unique_antinodes.add(antinode)
        if not map.out_of_bounds(antinode := pos2 - difference):
            unique_antinodes.add(antinode)

    return len(unique_antinodes)


def calculate_resonant_antinodes(map: Map) -> int:
    resonant_antinodes = set()

    for pos1, pos2 in map.combinations:
        resonant_antinodes.add(pos1)
        resonant_antinodes.add(pos2)

        difference = pos1 - pos2
        next_node = pos1 + difference

        while not map.out_of_bounds(next_node):
            resonant_antinodes.add(next_node)
            next_node += difference

        next_node = pos2 - difference
        while not map.out_of_bounds(next_node):
            resonant_antinodes.add(next_node)
            next_node -= difference

    return len(resonant_antinodes)


def extract_antenna_map(file_path: Path) -> Map:
    input_text = read_input(file_path)
    return Map(input_text)


class Day08(Day):
    def part1(self, file_path: Path) -> int:
        map = extract_antenna_map(file_path)
        return calculate_unique_antinodes(map)

    def part2(self, file_path: Path) -> int:
        map = extract_antenna_map(file_path)
        return calculate_resonant_antinodes(map)


if __name__ == '__main__':
    day = Day08()
    day.print_solution('puzzle.txt')
