import pytest

from day06.main import Day06


@pytest.mark.parametrize(
    'input,expected1,expected2', [('example.txt', 41, 6), ('puzzle.txt', 4964, 1740)]
)
def test_input(input, expected1, expected2):
    part1, part2 = Day06().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
