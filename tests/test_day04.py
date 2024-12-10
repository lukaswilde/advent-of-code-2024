import pytest

from day04.main import Day04


@pytest.mark.parametrize(
    'input,expected1,expected2', [('example.txt', 18, 9), ('puzzle.txt', 2593, 1950)]
)
def test_input(input, expected1, expected2):
    part1, part2 = Day04().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
