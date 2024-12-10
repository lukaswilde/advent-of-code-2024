import re
from pathlib import Path
from typing import List

from input import read_input

from template import Day


def extract_muls(file_path: Path) -> List[str]:
    input_text = read_input(file_path)
    pattern = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
    return re.findall(pattern, input_text)


def extract_muls_conditionals(file_path: Path) -> List[str]:
    input_text = read_input(file_path)
    pattern = re.compile(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))")
    return re.findall(pattern, input_text)


def calculate_uncorrupted_sum(instructions: List[str]) -> int:
    assert "don't()" not in instructions
    stripped = [
        instruction.replace('mul', '').replace('(', '').replace(')', '').split(',')
        for instruction in instructions
        if instruction != 'do()'
    ]
    assert 'do' not in stripped
    return sum(int(x[0]) * int(x[1]) for x in stripped)


def calculate_uncorrupted_conditional_sum(muls: List[str]) -> int:
    DELIMITER = 'X'
    filtered = re.sub(rf"don't\(\){DELIMITER}.*?do\(\){DELIMITER}", '', DELIMITER.join(muls))
    return calculate_uncorrupted_sum(filtered.split(DELIMITER))


class Day03(Day):
    def part1(self, file_path: Path) -> int:
        muls = extract_muls(file_path)
        return calculate_uncorrupted_sum(muls)

    def part2(self, file_path: Path) -> int:
        instructions = extract_muls_conditionals(file_path)
        return calculate_uncorrupted_conditional_sum(instructions)


if __name__ == '__main__':
    day = Day03()
    day.print_solution('puzzle.txt')
