from collections import Counter
from pathlib import Path
from typing import List, Tuple

from input import read_input

from template import Day


def extract_lists(file_path: Path) -> Tuple[List[int], List[int]]:
    input_text = read_input(file_path)
    lists = ([], [])

    for line in input_text.splitlines():
        numbers = list(map(lambda s: int(s), line.split()))
        lists[0].append(numbers[0])
        lists[1].append(numbers[1])

    return lists


def calculate_differences(list1: List[int], list2: List[int]) -> int:
    return sum(map(lambda x: abs(x[0] - x[1]), zip(sorted(list1), sorted(list2))))


def calculate_similarity(list1: List[int], list2: List[int]) -> int:
    occurrences = Counter(list2)
    return sum(map(lambda x: x * occurrences[x], list1))


class Day01(Day):
    def part1(self, file_path: Path) -> int:
        lists = extract_lists(file_path)
        return calculate_differences(*lists)

    def part2(self, file_path: Path) -> int:
        lists = extract_lists(file_path)
        return calculate_similarity(*lists)


if __name__ == '__main__':
    day = Day01()
    print(day.day_number)
    day.print_solution('puzzle.txt')
