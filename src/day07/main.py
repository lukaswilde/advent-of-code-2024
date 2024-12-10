from operator import add, mul
from pathlib import Path
from typing import Callable, List, Tuple

from input import read_input

from template import Day


def extract_equations(file_path: Path) -> List[Tuple[int, List[int]]]:
    input_text = read_input(file_path)
    res = []

    for line in input_text.splitlines():
        test, numbers = line.split(':')
        res.append((int(test), [int(val) for val in numbers.split()]))

    return res


def is_satisfiable(
    eq: Tuple[int, List[int]], operators: Tuple[Callable[[int, int], int], ...] = (add, mul)
) -> bool:
    test_val, rest = eq
    assert len(rest) > 1

    def is_satisfiable_helper(rest: List[int], acc: int) -> bool:
        if acc > test_val:
            return False
        if len(rest) == 0:
            return test_val == acc
        next_operand = rest[0]

        # faster than any() with generator expression
        # slower than just checking length of operator tuple and writing them out with 'or'
        for op in operators:
            if is_satisfiable_helper(rest[1:], op(acc, next_operand)):
                return True

    return is_satisfiable_helper(rest[1:], rest[0])


class Day07(Day):
    def part1(self, file_path: Path) -> int:
        equations = extract_equations(file_path)
        return sum([eq[0] for eq in equations if is_satisfiable(eq)])

    def part2(self, file_path: Path) -> int:
        def concat(x: int, y: int) -> int:
            return int(str(x) + str(y))

        equations = extract_equations(file_path)
        operators = (add, mul, concat)
        return sum([eq[0] for eq in equations if is_satisfiable(eq, operators)])


if __name__ == '__main__':
    day = Day07()
    day.print_solution('puzzle.txt')
