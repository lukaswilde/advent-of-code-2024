from typing import List, Tuple

from input import read_input


def extract_xmas(file_name: str) -> List[str]:
    input_text = read_input(file_name)
    lines = input_text.splitlines()
    width, height = len(lines[0]), len(lines)
    possibilities = []

    # horizontal possibilities
    for j in range(height):
        for i in range(width - 3):
            possibilities.append(lines[j][i : i + 4])

    # vertical possibilities
    for i in range(width):
        for j in range(height - 3):
            possibilities.append(''.join([lines[j + k][i] for k in range(4)]))

    # diagonals from top left to bottom right
    for i in range(width - 3):
        for j in range(height - 3):
            possibilities.append(''.join([lines[j + k][i + k] for k in range(4)]))

    # diagonals from top right to bottom left:
    for i in range(3, width):
        for j in range(height - 3):
            possibilities.append(''.join([lines[j + k][i - k] for k in range(4)]))

    return possibilities


def extract_crosses(file_name: str) -> List[Tuple[str, str]]:
    input_text = read_input(file_name)
    lines = input_text.splitlines()
    width, height = len(lines[0]), len(lines)
    possibilities = []

    for i in range(1, width - 1):
        for j in range(1, height - 1):
            possibilities.append(
                (
                    ''.join([lines[j + k][i + k] for k in [-1, 0, 1]]),
                    ''.join([lines[j + k][i - k] for k in [-1, 0, 1]]),
                ),
            )

    return possibilities


def part1(file_name: str) -> int:
    possibilities = extract_xmas(file_name)
    return len([x for x in possibilities if x in ['XMAS', 'SAMX']])


def part2(file_name: str) -> int:
    possibilities = extract_crosses(file_name)
    return len([(a, b) for (a, b) in possibilities if a in ['MAS', 'SAM'] and b in ['MAS', 'SAM']])


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f"Total number of 'XMAS' in input: {result1}")

    result2 = part2('puzzle.txt')
    print(f"Total number of 'X-MAS' crosses in input: {result2}")
