from pathlib import Path
from typing import List


def read_input(file_path: Path) -> str:
    with file_path.open('r') as f:
        return f.read()


def read_split_input(file_path: Path) -> List[str]:
    with file_path.open('r') as f:
        return f.read().split('\n\n')


def get_project_root():
    return Path(__file__).resolve().parent.parent
