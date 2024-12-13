from collections import defaultdict
from pathlib import Path
from typing import Set

from geometry import Grid, Vec2d
from input import read_input

from template import Day


class Map(Grid):
    def __init__(self, repr: str):
        super().__init__(repr)

        # Maps chars to a list of regions, represented as a set of their points
        self.regions = defaultdict(list)

        # Already inserted in a region
        covered = set()

        # Set of points to keep track during exploration which points are in the currently
        # looked at region or outside this region
        inside_region = set()
        outside_region = {Vec2d(0, 0)}

        while len(outside_region) > 0:
            next_region_point = outside_region.pop()
            next_region_char = self[next_region_point]
            if next_region_point in covered:
                continue
            self.regions[next_region_char].append(set())
            assert len(inside_region) == 0
            inside_region.add(next_region_point)
            current_char = next_region_char

            while len(inside_region) > 0:
                next_point = inside_region.pop()
                next_char = self[next_point]
                if next_point in covered:
                    continue

                self.regions[next_char][-1].add(next_point)
                covered.add(next_point)

                for neighbor in self.generate_neighbors(next_point):
                    if self[neighbor] != current_char:
                        outside_region.add(neighbor)
                    else:
                        inside_region.add(neighbor)


def calculate_price(map: Map) -> int:
    def get_area(region: Set[Vec2d]) -> int:
        return len(region)

    def get_perimeter(region: Set[Vec2d]) -> int:
        perimeter = get_area(region) * 4

        for point in region:
            char = map[point]
            for neighbor in map.generate_neighbors(point):
                if char == map[neighbor]:
                    perimeter -= 1

        return perimeter

    def calculate_region_price(region: Set[Vec2d]) -> int:
        return get_perimeter(region) * get_area(region)

    return sum(
        [calculate_region_price(region) for regions in map.regions.values() for region in regions]
    )


def extract_map(file_path: Path) -> Map:
    input_text = read_input(file_path)
    return Map(input_text)


class Day12(Day):
    def part1(self, file_path: Path) -> int:
        map = extract_map(file_path)
        return calculate_price(map)

    def part2(self, file_path: Path) -> int:
        ...
        # map = extract_map(file_path)
        # return calculate_price(map)


if __name__ == '__main__':
    day = Day12()
    day.print_solution('example5.txt')
