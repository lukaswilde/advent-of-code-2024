from pathlib import Path

from input import read_input

from template import Day


class Stones:
    def __init__(self, repr: str):
        assert len(repr.splitlines()) == 1
        line = repr.splitlines()[0]
        self.values = [int(x) for x in line.split()]
        self.cache = dict()

    def evolve(self, stone: int, blinks_left: int) -> int:
        if stone == 0:
            return self.count_stones(1, blinks_left - 1)

        as_string = str(stone)
        if len(as_string) % 2 == 0:
            pivot = len(as_string) // 2
            return self.count_stones(int(as_string[:pivot]), blinks_left - 1) + self.count_stones(
                int(as_string[pivot:]), blinks_left - 1
            )

        return self.count_stones(stone * 2024, blinks_left - 1)

    def count_stones(self, stone: int, blinks_left: int):
        if blinks_left == 0:
            return 1

        key = (stone, blinks_left)
        if key in self.cache:
            return self.cache[key]

        res = self.evolve(stone, blinks_left)
        self.cache[key] = res
        return res


def extract_stones(file_path: Path) -> Stones:
    input_text = read_input(file_path)
    return Stones(input_text)


class Day11(Day):
    def part1(self, file_path: Path) -> int:
        stones = extract_stones(file_path)
        return sum([stones.count_stones(stone, 25) for stone in stones.values])

    def part2(self, file_path: Path) -> int:
        stones = extract_stones(file_path)
        return sum([stones.count_stones(stone, 75) for stone in stones.values])


if __name__ == '__main__':
    day = Day11()
    day.print_solution('puzzle.txt')
