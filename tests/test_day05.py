import pytest

from day05.main import Day05


@pytest.mark.parametrize(
    'input,expected1,expected2', [('example.txt', 143, 123), ('puzzle.txt', 5732, 4716)]
)
def test_input(input, expected1, expected2):
    part1, part2 = Day05().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
