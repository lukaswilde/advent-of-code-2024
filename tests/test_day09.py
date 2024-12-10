import pytest

from day09.main import Day09


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [('example.txt', 1928, 2858), ('puzzle.txt', 6337367222422, 6361380647183)],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day09().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
