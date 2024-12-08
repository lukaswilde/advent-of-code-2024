import re
from typing import List

from input import read_input


def extract_muls(file_name: str) -> List[str]:
    input_text = read_input(file_name)
    pattern = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
    return re.findall(pattern, input_text)


def extract_muls_conditionals(file_name: str) -> List[str]:
    input_text = read_input(file_name)
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


def part1(file_name: str) -> int:
    muls = extract_muls(file_name)
    return calculate_uncorrupted_sum(muls)


def part2(file_name: str) -> int:
    instructions = extract_muls_conditionals(file_name)
    return calculate_uncorrupted_conditional_sum(instructions)


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f'Total sum of uncorrupted multiplications: {result1}')

    result2 = part2('puzzle.txt')
    print(f'Total sum of uncorrupted multiplications and conditionals: {result2}')
