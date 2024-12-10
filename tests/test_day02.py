import pytest

from day02.main import Day02


@pytest.mark.parametrize(
    'input,expected1,expected2', [('example.txt', 2, 4), ('puzzle.txt', 411, 465)]
)
def test_input(input, expected1, expected2):
    part1, part2 = Day02().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
