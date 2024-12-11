import pytest

from day10.main import Day10


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('score_single.txt', 1, 16),
        ('score_double.txt', 2, 2),
        ('score_branching.txt', 4, 19),
        ('score_two.txt', 3, 6),
        ('rating_small.txt', 1, 3),
        ('rating_medium.txt', 4, 13),
        ('rating_large.txt', 2, 227),
        ('example.txt', 36, 81),
        ('puzzle.txt', 482, 1094),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day10().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
