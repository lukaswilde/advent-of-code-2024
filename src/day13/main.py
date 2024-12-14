import re
from pathlib import Path
from typing import List, Tuple

from geometry import Vec2d
from input import read_split_input

from template import Day


def extract_configuration(file_path: Path) -> List[Tuple[Vec2d, Vec2d, Vec2d]]:
    """Returns a list with entries (A x-y increase, B x-y increase, target x-y)"""

    def extract_coords(line: str) -> Vec2d:
        matches = re.findall(r'\d+', line)
        assert len(matches) == 2
        return Vec2d(int(matches[0]), int(matches[1]))

    input_texts = read_split_input(file_path)
    configs = []

    for text in input_texts:
        lines = text.splitlines()
        assert len(lines) == 3
        configs.append(tuple(extract_coords(line) for line in lines))

    return configs


def find_cheapest_win(config) -> int:
    da, db, t = config
    cheapest = [
        3 * i + j
        for i in range(101)
        for j in range(101)
        if i * da.x + j * db.x == t.x and i * da.y + j * db.y == t.y
    ]
    if len(cheapest) == 0:
        return 0
    return min(cheapest)


def find_cheapest_win_modified(config) -> int:
    # We have the following two equations:
    # 1) i * da.x + j * db.x = t.x
    # 2) i * da.y + j * db.y = t.y

    # Solving each for i, we get
    # 1) i = (t.x - j * db.x) / da.x
    # 2) i = (t.y - j * db.y) / da.y

    # Setting them equal we get
    # (t.x - j * db.x) / da.x = (t.y - j * db.y) / da.y

    # Resolving the quotients we have
    # (t.x - j * db.x) * da.y = (t.y - j * db.y) * da.x

    # Solving for j:
    # t.x * da.y - t.y * da.x = - j * db.y * da.x + j * db.x * da.y
    # and then
    # j = (t.x * da.y - t.y * da.x) / (db.x * da.y - db.y * da.x)

    da, db, t = config
    t.x += 10000000000000
    t.y += 10000000000000

    j = (t.x * da.y - t.y * da.x) / (db.x * da.y - db.y * da.x)
    i = (t.x - j * db.x) / da.x

    if i % 1 == 0 and j % 1 == 0:
        return 3 * int(i) + int(j)

    return 0


class Day13(Day):
    def part1(self, file_path: Path) -> int:
        configs = extract_configuration(file_path)
        return sum([find_cheapest_win(config) for config in configs])

    def part2(self, file_path: Path) -> int:
        configs = extract_configuration(file_path)
        return sum([find_cheapest_win_modified(config) for config in configs])


if __name__ == '__main__':
    day = Day13()
    day.print_solution('example.txt')
