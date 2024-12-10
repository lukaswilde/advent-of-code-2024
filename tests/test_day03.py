import pytest

from day03.main import Day03


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [('example.txt', 161, 161), ('example2.txt', 161, 48), ('puzzle.txt', 173529487, 99532691)],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day03().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
