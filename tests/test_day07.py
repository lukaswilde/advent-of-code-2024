import pytest

from day07.main import Day07


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [('example.txt', 3749, 11387), ('puzzle.txt', 267566105056, 116094961956019)],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day07().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
