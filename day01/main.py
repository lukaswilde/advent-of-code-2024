from collections import Counter
from typing import List, Tuple

from input import read_input


def extract_lists(file_name: str) -> Tuple[List[int], List[int]]:
    input_text = read_input(file_name)
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


def part1(file_name: str) -> int:
    lists = extract_lists(file_name)
    return calculate_differences(*lists)


def part2(file_name: str) -> int:
    lists = extract_lists(file_name)
    return calculate_similarity(*lists)


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f'Total distance between the two lists: {result1}')

    result2 = part2('puzzle.txt')
    print(f'Similarity score of the two lists: {result2}')
