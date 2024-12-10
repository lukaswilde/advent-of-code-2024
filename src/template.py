from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

from input import get_project_root


class Day(ABC):
    @property
    def day_number(self) -> int:
        return int(type(self).__name__[-2:])

    @property
    def base_dir(self) -> Path:
        return get_project_root() / 'src' / f'day{self.day_number:02}'

    @abstractmethod
    def part1(self, file_path: Path) -> int: ...

    @abstractmethod
    def part2(self, file_path: Path) -> int: ...

    def _complete_path(self, file_name: str):
        return self.base_dir / file_name

    def get_solution(self, file_name: str) -> Tuple[int, int]:
        path = self._complete_path(file_name)
        return self.part1(path), self.part2(path)

    def print_solution(self, file_name: str):
        path = self._complete_path(file_name)

        print(f'Result of part 1: {self.part1(path)}')
        print(f'Result of part 2: {self.part2(path)}')
