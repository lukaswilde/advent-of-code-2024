import pytest

from day17.main import Day17


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', '4,6,3,5,6,3,5,2,1,0', None),
        ('example2.txt', '5,7,3,0', 117440),
        ('puzzle.txt', '2,1,0,1,7,2,5,0,3', 267265166222235),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day17().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
