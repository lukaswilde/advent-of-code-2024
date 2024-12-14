import pytest

from day14.main import Day14


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', 12, 23),
        ('puzzle.txt', 228410028, 8258),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day14().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
