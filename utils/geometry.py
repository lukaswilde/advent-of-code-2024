from enum import Enum
from typing import Any, Callable, List, Optional


class Vec2d:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vec2d)
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vec2d)
        return self + (-other)

    def __neg__(self):
        return Vec2d(-self.x, -self.y)

    def __mod__(self, other):
        assert isinstance(other, Vec2d)
        return Vec2d(self.x % other.x, self.y % other.y)

    def __eq__(self, other):
        if not isinstance(other, Vec2d):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'Vec2d({self.x},{self.y})'

    def multiply(self, scalar: int):
        return Vec2d(self.x * scalar, self.y * scalar)


class Grid:
    """Class representing a 2D grid. Convention is (x,y) coordinates with (0,0) in the upper left corner"""

    def __init__(self, repr: str):
        self.lines = repr.splitlines()
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        self.values = [[''] * self.width for _ in range(self.height)]

        for i, line in enumerate(self.lines):
            for j, char in enumerate(line):
                self.values[i][j] = char

    def apply_on_values(self, fn: Callable[[str], Any]):
        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                self[point] = fn(self[point])

    def out_of_bounds(self, p: Vec2d) -> bool:
        return p.x < 0 or p.y < 0 or p.x >= self.width or p.y >= self.height

    def generate_neighbors(self, p: Vec2d) -> List[Vec2d]:
        neighbors = []
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            possible_neighbor = p + direction.value
            if not self.out_of_bounds(possible_neighbor):
                neighbors.append(possible_neighbor)

        return neighbors

    def swap(self, loc1: Vec2d, loc2: Vec2d):
        self[loc1], self[loc2] = self[loc2], self[loc1]

    def find_unique(self, target) -> Optional[Vec2d]:
        assert isinstance(target, type(self[Vec2d(0, 0)]))

        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                val = self[point]
                if val == target:
                    return point

    def find_first(self, targets: List) -> Optional[Vec2d]:
        assert all([isinstance(target, type(self[Vec2d(0, 0)])) for target in targets])

        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                val = self[point]
                if val in targets:
                    return point

    def find_all(self, target) -> List[Vec2d]:
        assert isinstance(target, type(self[Vec2d(0, 0)]))

        res = []
        for i in range(self.width):
            for j in range(self.height):
                point = Vec2d(i, j)
                val = self[point]
                if val == target:
                    res.append(point)
        return res

    def __setitem__(self, key: Vec2d, value):
        if self.out_of_bounds(key):
            raise KeyError(
                f'Point {str(key)} is not inside the grid with dimensions {self.width} x {self.height}'
            )
        self.values[key.y][key.x] = value

    def __getitem__(self, item: Vec2d):
        """Return value of the point item(x,y)"""
        if self.out_of_bounds(item):
            return None

        return self.values[item.y][item.x]

    def dump_values(self):
        """Print a representation of the values stored in the grid"""
        for j in range(self.height):
            line = ''
            for i in range(self.width):
                line += str(self[Vec2d(i, j)])
            print(line)


class Direction(Enum):
    UP = Vec2d(0, -1)
    DOWN = Vec2d(0, 1)
    LEFT = Vec2d(-1, 0)
    RIGHT = Vec2d(1, 0)

    @staticmethod
    def from_str(char: str):
        assert len(char) == 1
        assert char in '><v^', f'The char was: {char}'

        match char:
            case 'v':
                return Direction.DOWN
            case '>':
                return Direction.RIGHT
            case '<':
                return Direction.LEFT
            case '^':
                return Direction.UP

    def rotate_right(self):
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

    def __str__(self):
        match self:
            case Direction.UP:
                return '^'
            case Direction.DOWN:
                return 'v'
            case Direction.LEFT:
                return '<'
            case Direction.RIGHT:
                return '>'


ALL_DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
