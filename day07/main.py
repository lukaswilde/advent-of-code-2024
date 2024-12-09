from typing import List, Tuple

from input import read_input


def extract_equations(file_name: str) -> List[Tuple[int, List[int]]]:
    input_text = read_input(file_name)
    res = []

    for line in input_text.splitlines():
        test, numbers = line.split(':')
        res.append((int(test), [int(val) for val in numbers.split()]))

    return res


def is_satisfiable_addmul(eq: Tuple[int, List[int]]) -> bool:
    test_val, rest = eq

    def is_satisfiable(rest: List[int], acc: int) -> bool:
        if acc > test_val:
            return False
        if len(rest) == 0:
            return test_val == acc
        next_operand = rest[0]
        return is_satisfiable(rest[1:], acc + next_operand) or is_satisfiable(
            rest[1:], acc * next_operand
        )

    assert len(rest) > 1
    return is_satisfiable(rest[1:], rest[0])


def is_satisfiable_addmulconcat(eq: Tuple[int, List[int]]) -> bool:
    test_val, rest = eq

    def is_satisfiable(rest: List[int], acc: int) -> bool:
        if acc > test_val:
            return False
        if len(rest) == 0:
            return test_val == acc
        next_operand = rest[0]
        return (
            is_satisfiable(rest[1:], acc + next_operand)
            or is_satisfiable(rest[1:], acc * next_operand)
            or is_satisfiable(rest[1:], int(str(acc) + str(next_operand)))
        )

    assert len(rest) > 1
    return is_satisfiable(rest[1:], rest[0])


def part1(file_name: str) -> int:
    equations = extract_equations(file_name)
    return sum([eq[0] for eq in equations if is_satisfiable_addmul(eq)])


def part2(file_name: str) -> int:
    equations = extract_equations(file_name)
    return sum([eq[0] for eq in equations if is_satisfiable_addmulconcat(eq)])


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f'The total calibration result is: {result1}')

    result2 = part2('puzzle.txt')
    print(f'The total calibration result with concatenation is: {result2}')
