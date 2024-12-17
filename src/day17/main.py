import copy
from pathlib import Path
from typing import List, Optional, Tuple

from input import read_split_input

from template import Day


class Command:
    def __init__(self, opcode: int, operand: int):
        assert 0 <= opcode <= 7
        assert 0 <= operand <= 7
        self.opcode = opcode
        self.operand = operand

    def execute(self, registers: List[int], ic: int) -> Tuple[int, Optional[int]]:
        """
        Executes a command indicated by its opcode. Registers are changed in-place.
        Returns updated instruction counter and optional output of the command
        """
        a, b, c = registers[0], registers[1], registers[2]
        match self.opcode:
            case 0:
                registers[0] = a // (2 ** self.resolve_combo(registers))
            case 1:
                registers[1] = b ^ self.operand
            case 2:
                registers[1] = self.resolve_combo(registers) % 8
            case 3 if a != 0:
                return self.operand, None
            case 4:
                registers[1] = b ^ c
            case 5:
                return ic + 2, self.resolve_combo(registers) % 8
            case 6:
                registers[1] = a // (2 ** self.resolve_combo(registers))
            case 7:
                registers[2] = a // (2 ** self.resolve_combo(registers))

        return ic + 2, None

    def __repr__(self):
        return f'Command({self.opcode},{self.operand})'

    def resolve_combo(self, registers: List[int]) -> int:
        assert 0 <= self.operand <= 6
        if 0 <= self.operand <= 3:
            return self.operand
        return registers[self.operand - 4]


def extract_sections(file_path: Path) -> Tuple[List[int], List[int]]:
    input_text = read_split_input(file_path)
    assert len(input_text) == 2
    registers = [int(line.split(':')[1]) for line in input_text[0].splitlines()]
    numbers = [int(val) for val in input_text[1].split(':')[1].split(',')]
    return registers, numbers


def execute_program(registers: List[int], program: List[int]) -> List[int]:
    regs = copy.deepcopy(registers)
    ic = 0
    output = []
    while ic < len(program) - 1:
        command = Command(program[ic], program[ic + 1])
        ic, out = command.execute(regs, ic)
        if out is not None:
            output.append(out)

    return output


def find_smallest_reproducer(registers: List[int], program: List[int]) -> int:
    """
    Finds the smallest number for register A that reproduces the program.
    We can observe, that output lengths depend on the register A.
    We can find the correct composition of A by matching the back digits of the program
    first and iterating to the front. Since the output length of the program increases
    by one when multiplying A * 8, we can iteratively build A.
    """
    todo = [(1, 0)]
    for i, a in todo:
        for a in range(a, a + 8):
            if execute_program([a, registers[1], registers[2]], program) == program[-i:]:
                todo.append((i + 1, a * 8))
                if i == len(program):
                    return a


class Day17(Day):
    def part1(self, file_path: Path) -> str:
        registers, program = extract_sections(file_path)
        return ','.join([str(num) for num in execute_program(registers, program)])

    def part2(self, file_path: Path) -> int:
        registers, program = extract_sections(file_path)
        return find_smallest_reproducer(registers, program)


if __name__ == '__main__':
    day = Day17()
    day.print_solution('puzzle.txt')
