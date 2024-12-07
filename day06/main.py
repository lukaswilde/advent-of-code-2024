import copy
from enum import Enum, auto

from geometry import Direction, Point
from input import read_input
from tqdm import tqdm


class Map:
    class Progress(Enum):
        EXIT = auto()
        CONTINUE = auto()
        CYCLE = auto()

    def __init__(self, repr: str):
        lines = repr.splitlines()
        self.width = len(lines[0])
        self.height = len(lines)

        self.guard_facing = None
        self._guard_pos = None
        self.guard_pos = None
        self._guard_facing = None

        self.obstacle_pos = set()
        self.visited_tiles = set()
        # For part 2, remember whether tile was visited in the same direction before -> cycle
        self.visited_with_position = set()

        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                match char:
                    case '.':
                        continue
                    case '#':
                        self.obstacle_pos.add(Point(j, i))
                    case 'v':
                        self._guard_pos = Point(j, i)
                        self._guard_facing = Direction.DOWN
                    case '>':
                        self._guard_pos = Point(j, i)
                        self._guard_facing = Direction.RIGHT
                    case '<':
                        self._guard_pos = Point(j, i)
                        self._guard_facing = Direction.LEFT
                    case '^':
                        self._guard_pos = Point(j, i)
                        self._guard_facing = Direction.UP

        self.guard_facing = self._guard_facing
        self.guard_pos = self._guard_pos
        self.visited_tiles.add(self.guard_pos)
        self.visited_with_position.add((self.guard_pos, self.guard_facing))

    def dump(self):
        for j in range(self.height):
            line = ''
            for i in range(self.width):
                if Point(i, j) in self.obstacle_pos:
                    line += '#'
                elif Point(i, j) == self.guard_pos:
                    line += str(self.guard_facing)
                else:
                    line += '.'
            print(line)
        print()

    def step(self) -> bool:
        """
        Evolves the map by the guard moving one position
        Returns True if the guard stays inside the grid, False otherwise
        """
        next_position = self.guard_pos + self.guard_facing.value
        if self.out_of_bounds(next_position):
            return False

        if next_position in self.obstacle_pos:
            self.guard_facing = self.guard_facing.rotate_right()
        else:
            self.guard_pos = next_position
            self.visited_tiles.add(next_position)

        return True

    def out_of_bounds(self, p: Point) -> bool:
        return p.x < 0 or p.y < 0 or p.x >= self.width or p.y >= self.height

    def reset(self):
        self.guard_facing = self._guard_facing
        self.guard_pos = self._guard_pos
        self.visited_with_position = {(self.guard_pos, self.guard_facing)}
        self.visited_tiles = {self.guard_pos}

    def is_creating_cycle(self, new_obstacle_pos: Point) -> bool:
        if new_obstacle_pos == self.guard_pos:
            return False
        if new_obstacle_pos in self.obstacle_pos:
            return False

        self.obstacle_pos.add(new_obstacle_pos)

        while (state := self.advanced_step()) == self.Progress.CONTINUE:
            continue

        self.obstacle_pos.remove(new_obstacle_pos)
        self.reset()

        return state == self.Progress.CYCLE

    def advanced_step(self) -> Progress:
        """
        Evolves the map by the guard moving one position
        Returns either CONTINUE, EXIT or CYCLE depending on the evolution
        """
        next_position = self.guard_pos + self.guard_facing.value
        if self.out_of_bounds(next_position):
            return self.Progress.EXIT

        if next_position in self.obstacle_pos:
            self.guard_facing = self.guard_facing.rotate_right()
            self.visited_with_position.add((self.guard_pos, self.guard_facing))
            return self.Progress.CONTINUE

        self.guard_pos = next_position

        if (self.guard_pos, self.guard_facing) in self.visited_with_position:
            return self.Progress.CYCLE

        self.visited_with_position.add((next_position, self.guard_facing))
        return self.Progress.CONTINUE


def calculate_num_visited(map: Map) -> int:
    while map.step():
        # map.dump()
        continue

    return len(map.visited_tiles)


def calculate_cycle_positions(map: Map) -> int:
    # Only try the positions that are visited by the guard
    tmp = copy.deepcopy(map)
    calculate_num_visited(tmp)

    count = 0
    with tqdm(total=len(tmp.visited_tiles)) as pbar:
        for i, p in enumerate(tmp.visited_tiles):
            if map.is_creating_cycle(p):
                count += 1
            pbar.update(1)

    return count


def extract_map(file_name: str) -> Map:
    input_text = read_input(file_name)
    return Map(input_text)


def part1(file_name: str) -> int:
    map = extract_map(file_name)
    return calculate_num_visited(map)


def part2(file_name: str) -> int:
    map = extract_map(file_name)
    return calculate_cycle_positions(map)


if __name__ == '__main__':
    result1 = part1('puzzle.txt')
    print(f'Total number of visited tiles: {result1}')

    result2 = part2('puzzle.txt')
    print(f'Total number of obstacle positions that create a cycle: {result2}')
