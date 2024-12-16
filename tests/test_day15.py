import pytest

from day15.main import Day15


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', 10092, 9021),
        ('example_small.txt', 2028, 1751),
        ('example_small2.txt', 908, 618),
        ('puzzle.txt', 1479679, 1509780),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day15().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
