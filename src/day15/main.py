from pathlib import Path
from typing import List, Tuple

from geometry import Direction, Grid, Vec2d
from input import read_split_input

from template import Day


class Map(Grid):
    def __init__(self, repr: str):
        super().__init__(repr)
        self.robot = self.find_unique('@')
        assert self.robot is not None

    def get_second_loc(self, first_loc: Vec2d) -> Vec2d:
        """Returns the location of the second half of a wide box `[]`"""
        if self[first_loc] == '[':
            return first_loc + Direction.RIGHT.value
        return first_loc + Direction.LEFT.value

    def _move_single(self, location: Vec2d, direction: Direction) -> bool:
        """
        Returns `False` if single move not possible, `True` if possible and the map was changed
        """
        next_location = location + direction.value

        # Should not happen, because map is surrounded by walls (#)
        assert not self.out_of_bounds(next_location)

        if (next_char := self[next_location]) == '#':
            return False
        elif next_char == '.':
            self.swap(location, next_location)
            return True

        assert next_char in 'O[]'

        if not self._move_single(next_location, direction):
            return False
        self.swap(location, next_location)
        return True

    def move(self, direction: Direction):
        """
        Tries to move the robot in the given direction. If there are boxes in the way,
        it tries to push them accordingly. Should this be impossible, doesn't change the map.
        """
        if self._move_single(self.robot, direction):
            self.robot += direction.value

    def move_wide(self, direction: Direction):
        """
        Tries to move the robot in the given direction in a wide setting. If there are boxes in the way,
        it tries to push them accordingly. Should this be impossible, doesn't change the map.
        """

        def move_two(loc1: Vec2d, loc2: Vec2d, dy: Direction, displace: bool = False) -> bool:
            assert dy in [Direction.UP, Direction.DOWN]
            next_loc1, next_loc2 = loc1 + dy.value, loc2 + dy.value

            # Should not happen, because map is surrounded by walls (#)
            assert not self.out_of_bounds(next_loc1)
            assert not self.out_of_bounds(next_loc2)

            next_char1 = self[next_loc1]
            next_char2 = self[next_loc2]

            result = False
            if next_char1 == '.' and next_char2 == '.':
                result = True
            elif next_char1 == '#' or next_char2 == '#':
                result = False
            elif next_char1 == '.' and next_char2 in '[]':
                assert next_char2 == '['
                result = move_two(next_loc2, self.get_second_loc(next_loc2), dy, displace)
            elif next_char1 in '[]' and next_char2 == '.':
                assert next_char1 == ']'
                result = move_two(self.get_second_loc(next_loc1), next_loc1, dy, displace)
            elif next_char1 == '[' and next_char2 == ']':
                result = move_two(next_loc1, next_loc2, dy, displace)
            elif next_char1 == ']' and next_char2 == '[':
                result = move_two(
                    self.get_second_loc(next_loc1), next_loc1, dy, displace
                ) and move_two(next_loc2, self.get_second_loc(next_loc2), dy, displace)

            if displace:
                self.swap(loc1, next_loc1)
                self.swap(loc2, next_loc2)

            return result

        next_loc = self.robot + direction.value

        if direction in [Direction.LEFT, Direction.RIGHT] or self[next_loc] in '#.':
            return self.move(direction)

        first, second = next_loc, self.get_second_loc(next_loc)

        if self[next_loc] == ']':
            first, second = second, first

        if not move_two(first, second, direction, False):
            return

        move_two(first, second, direction, True)
        self[next_loc] = '@'
        self[self.robot] = '.'
        self.robot = next_loc

    def execute_directions(self, directions: List[Direction], wide: bool = False):
        for direction in directions:
            self.move_wide(direction) if wide else self.move(direction)

    def get_gps_score(self) -> int:
        score = 0
        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                if self[point] in 'O[':
                    score += i + 100 * j

        return score


def parse_directions(text: str) -> List[Direction]:
    return [Direction.from_str(char) for char in text]


def extract_sections(file_path: Path) -> Tuple[Map, List[Direction]]:
    input_text = read_split_input(file_path)
    assert len(input_text) == 2

    map_str, dir_str = input_text[0], input_text[1]
    dir_str = dir_str.replace('\n', '')
    return Map(map_str), parse_directions(dir_str)


def extract_sections_wider(file_path: Path) -> Tuple[Map, List[Direction]]:
    input_text = read_split_input(file_path)
    assert len(input_text) == 2

    map_str, dir_str = input_text[0], input_text[1]
    dir_str = dir_str.replace('\n', '')
    map_str = map_str.replace('#', '##')
    map_str = map_str.replace('O', '[]')
    map_str = map_str.replace('.', '..')
    map_str = map_str.replace('@', '@.')
    return Map(map_str), parse_directions(dir_str)


class Day15(Day):
    def part1(self, file_path: Path) -> int:
        map, directions = extract_sections(file_path)
        map.execute_directions(directions)
        return map.get_gps_score()

    def part2(self, file_path: Path) -> int:
        map, directions = extract_sections_wider(file_path)
        map.execute_directions(directions, wide=True)
        return map.get_gps_score()


if __name__ == '__main__':
    day = Day15()
    day.print_solution('puzzle.txt')
