from enum import Enum


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

    def __eq__(self, other):
        if not isinstance(other, Vec2d):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'Vec2d({self.x},{self.y})'


class Grid:
    def __init__(self, repr: str):
        self.lines = repr.splitlines()
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def out_of_bounds(self, p: Vec2d) -> bool:
        return p.x < 0 or p.y < 0 or p.x >= self.width or p.y >= self.height


class Direction(Enum):
    UP = Vec2d(0, -1)
    DOWN = Vec2d(0, 1)
    LEFT = Vec2d(-1, 0)
    RIGHT = Vec2d(1, 0)

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
