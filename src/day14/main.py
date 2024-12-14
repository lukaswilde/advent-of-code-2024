import os
from pathlib import Path
from typing import List, Tuple

import numpy
from geometry import Vec2d
from input import extract_vectors, get_project_root, read_input
from PIL import Image

from template import Day


def extract_robots(file_path: Path) -> List[Tuple[Vec2d, ...]]:
    input_texts = read_input(file_path)
    return [tuple(extract_vectors(line)) for line in input_texts.splitlines()]


def evolve(robots: List[Tuple[Vec2d, ...]], width: int, height: int, steps: int) -> List[Vec2d]:
    def step(robot: Tuple[Vec2d, Vec2d]) -> Vec2d:
        pos, vel = robot
        return (pos + vel.multiply(steps)) % Vec2d(width, height)

    return [step(robot) for robot in robots]


def calculate_quadrant_prod(positions: List[Vec2d], middle_x: int, middle_y: int) -> int:
    upper_left = len(list(filter(lambda p: p.x < middle_x and p.y < middle_y, positions)))
    upper_right = len(list(filter(lambda p: p.x > middle_x and p.y < middle_y, positions)))
    lower_left = len(list(filter(lambda p: p.x < middle_x and p.y > middle_y, positions)))
    lower_right = len(list(filter(lambda p: p.x > middle_x and p.y > middle_y, positions)))

    return upper_left * upper_right * lower_right * lower_left


def print_step(positions: List[Vec2d], width: int, height: int):
    for j in range(height):
        line = ''
        for i in range(width):
            if Vec2d(i, j) in positions:
                line += '#'
            else:
                line += '.'
        print(line)


def save_img(positions: List[Vec2d], width: int, height: int, step: int):
    arr = numpy.zeros((width, height))
    for position in positions:
        arr[position.x][position.y] = 1
    arr = arr * 255
    img = Image.fromarray(arr).convert('1')
    img.save(DIR / f'{step}.jpeg')


DIR = get_project_root() / 'src' / 'day14' / 'imgs'


class Day14(Day):
    def part1(self, file_path: Path) -> int:
        robots = extract_robots(file_path)
        width = max([vec.x for vectors in robots for vec in vectors]) + 1
        height = max([vec.y for vectors in robots for vec in vectors]) + 1

        positions = evolve(robots, width, height, 100)
        return calculate_quadrant_prod(positions, width // 2, height // 2)

    def part2(self, file_path: Path) -> int:
        robots = extract_robots(file_path)
        width = max([vec.x for vectors in robots for vec in vectors]) + 1
        height = max([vec.y for vectors in robots for vec in vectors]) + 1

        for i in range(width * height):
            positions = evolve(robots, width, height, i + 1)
            save_img(positions, width, height, i + 1)

        # Image with the easter egg should be the most compressible, so it has the smallest file size
        files = os.listdir(DIR)
        smallest_file = min(files, key=lambda f: os.path.getsize(DIR / f))

        return int(Path(smallest_file).stem)


if __name__ == '__main__':
    day = Day14()
    day.print_solution('puzzle.txt')
