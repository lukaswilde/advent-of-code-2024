import pytest
from geometry import Vec2d

from day18.main import Day18


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', 22, Vec2d(6, 1)),
        ('puzzle.txt', 326, Vec2d(18, 62)),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day18().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
