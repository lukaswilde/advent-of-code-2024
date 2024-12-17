import pytest

from day16.main import Day16


@pytest.mark.parametrize(
    'input,expected1,expected2',
    [
        ('example.txt', 7036, 45),
        ('example2.txt', 11048, 64),
        ('puzzle.txt', 123540, 665),
    ],
)
def test_input(input, expected1, expected2):
    part1, part2 = Day16().get_solution(input)
    assert part1 == expected1
    assert part2 == expected2
