import pytest

from day11.main import Day11


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [('example.txt', 55312, 65601038650482), ('puzzle.txt', 217812, 259112729857522)],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day11().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
