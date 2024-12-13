import pytest

from day12.main import Day12


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example1.txt', 140, 80),
        ('example2.txt', 772, 436),
        ('example3.txt', 1930, 1206),
        ('example4.txt', 692, 236),
        ('example5.txt', 1184, 368),
        ('puzzle.txt', 1518548, None),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day12().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
