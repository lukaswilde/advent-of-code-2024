import inspect
from pathlib import Path


def read_input(file_name: str) -> str:
    """Returns the text content of an input file given relative to a dayXX folder"""

    # Extract the location of the calling function, to correctly get the absolute puzzle input path
    calling_module = inspect.stack()[-1].filename
    file = Path(calling_module).resolve().parent / file_name

    with file.open('r') as f:
        return f.read()
