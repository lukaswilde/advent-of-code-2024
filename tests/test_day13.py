import pytest

from day13.main import Day13


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', 480, 459236326669),
        ('puzzle.txt', 33427, 91649162972270),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day13().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
