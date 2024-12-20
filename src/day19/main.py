from pathlib import Path

from input import read_split_input

from template import Day


def extract_sections(file_path: Path) -> tuple[set[str], list[str]]:
    input_text = read_split_input(file_path)
    assert len(input_text) == 2
    patterns = set([pattern for pattern in input_text[0].replace(' ', '').split(',')])
    designs = [design for design in input_text[1].splitlines()]
    return patterns, designs


def calculate_possible(patterns: set[str], designs: list[str]) -> int:
    def is_possible(design: str) -> bool:
        if design == '':
            return False

        possible = False
        for pattern in patterns:
            if possible:
                return True

            if not design.startswith(pattern):
                continue

            if pattern == design:
                return True

            possible = possible or is_possible(design.removeprefix(pattern))

        return possible

    return sum([is_possible(design) for design in designs])


def calculate_possibilities(patterns: set[str], designs: list[str]) -> int:
    cache: dict[str, int] = dict()

    def num_possibilities(design: str) -> int:
        if design in cache:
            return cache[design]

        if design == '':
            return 0

        count_possible = 0
        for pattern in patterns:
            if not design.startswith(pattern):
                continue

            if pattern == design:
                count_possible += 1

            suffix = design.removeprefix(pattern)
            res = num_possibilities(suffix)
            count_possible += res

            if suffix not in cache:
                cache[suffix] = res

        return count_possible

    return sum([num_possibilities(design) for design in designs])


class Day19(Day):
    def part1(self, file_path: Path) -> float:
        patterns, designs = extract_sections(file_path)
        return calculate_possible(patterns, designs)

    def part2(self, file_path: Path) -> float:
        patterns, designs = extract_sections(file_path)
        return calculate_possibilities(patterns, designs)


if __name__ == '__main__':
    day = Day19()
    day.print_solution('puzzle.txt')
