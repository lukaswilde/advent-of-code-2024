from collections import Counter
from typing import List
import re

from input import read_input


def extract_muls(file_name: str) -> List[str]:
    input_text = read_input(file_name)
    pattern = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
    return re.findall(pattern, input_text)


def calculate_uncorrupted_sum(muls: List[str]) -> int:
    stripped = [mul.replace("mul", "").replace("(", "").replace(")", "").split(',') for mul in muls]
    return sum(int(x[0]) * int(x[1]) for x in stripped)


# def calculate_similarity(list1: List[int], list2: List[int]) -> int:
#     occurrences = Counter(list2)
#     return sum(map(lambda x: x * occurrences[x], list1))


def part1(file_name: str) -> int:
    muls = extract_muls(file_name)
    return calculate_uncorrupted_sum(muls)
    # return calculate_differences(*lists)


# def part2(file_name: str) -> int:
#     lists = extract_muls(file_name)
#     return calculate_similarity(*lists)
#

if __name__ == "__main__":
    result1 = part1("puzzle.txt")
    print(f"Total sum of uncorrupted multiplications: {result1}")

    # result2 = part2("puzzle.txt")
    # print(f"Similarity score of the two lists: {result2}")
