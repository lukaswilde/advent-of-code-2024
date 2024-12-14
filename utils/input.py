import re
from pathlib import Path
from typing import List

from geometry import Vec2d


def read_input(file_path: Path) -> str:
    with file_path.open('r') as f:
        return f.read()


def read_split_input(file_path: Path) -> List[str]:
    with file_path.open('r') as f:
        return f.read().split('\n\n')


def get_project_root():
    return Path(__file__).resolve().parent.parent


def extract_vectors(line: str) -> List[Vec2d]:
    matches = re.findall(r'[-\d]+', line)
    return [Vec2d(int(matches[i]), int(matches[i + 1])) for i in range(0, len(matches), 2)]
