import pytest

from day19.main import Day19


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', 6, 16),
        ('puzzle.txt', 228, 584553405070389),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day19().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
