import pytest

from day01.main import Day01


@pytest.mark.parametrize(
    'input,expected1,expected2', [('example.txt', 11, 31), ('puzzle.txt', 2580760, 25358365)]
)
def test_input(input, expected1, expected2):
    part1, part2 = Day01().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
