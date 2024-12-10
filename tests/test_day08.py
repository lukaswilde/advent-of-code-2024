import pytest

from day08.main import Day08


@pytest.mark.parametrize(
    'input,expected1,expected2', [('example.txt', 14, 34), ('puzzle.txt', 361, 1249)]
)
def test_input(input, expected1, expected2):
    part1, part2 = Day08().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
