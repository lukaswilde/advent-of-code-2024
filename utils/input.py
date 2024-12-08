import inspect
from pathlib import Path
from typing import List


def read_input(file_name: str) -> str:
    """Returns the text content of an input file given relative to a dayXX folder"""
    file = _correct_calling_directory(file_name)

    with file.open('r') as f:
        return f.read()


def _correct_calling_directory(file_name: str) -> Path:
    # Extract the location of the calling function, to correctly get the absolute puzzle input path
    calling_module = inspect.stack()[-1].filename
    return Path(calling_module).resolve().parent / file_name


def read_split_input(file_name: str) -> List[str]:
    """
    Return the text content of an input file given relative to a dayXX folder.
    The input is expected to be split by two newlines
    """
    file = _correct_calling_directory(file_name)

    with file.open('r') as f:
        return f.read().split('\n\n')
