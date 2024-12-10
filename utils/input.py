import inspect
from pathlib import Path
from typing import List
from re import search


def read_input(file_name: str) -> str:
    """Returns the text content of an input file given relative to a dayXX folder"""
    file = _correct_calling_directory(file_name)

    with file.open('r') as f:
        return f.read()

def get_project_root():
    return Path(__file__).resolve().parent.parent

def _correct_calling_directory(file_name: str) -> Path:
    # Extract the location of the calling function, to correctly get the absolute puzzle input path
    for frame in inspect.stack():
        if day := search(r"day\d\d", frame.filename):
            return get_project_root() / day[0] / file_name


def read_split_input(file_name: str) -> List[str]:
    """
    Return the text content of an input file given relative to a dayXX folder.
    The input is expected to be split by two newlines
    """
    file = _correct_calling_directory(file_name)

    with file.open('r') as f:
        return f.read().split('\n\n')
