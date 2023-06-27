import json
import typing
from entities import *


def open_json(path: str) -> typing.Dict[str, typing.Any]:
    """
    Opens a JSON file and returns its contents as a dictionary.

    Args:
        path: A string representing the path to the JSON file.

    Returns:
        A dictionary representing the contents of the JSON file.
    """
    with open(path) as file:
        data = json.load(file)
    return data


def save_json(data: typing.Dict, file_path: str):
    """
    A dictionary representing the contents of the needed JSON file

    Args:
        data: A dictionary with needed data
        path: A string representing the path to the JSON file.

    Returns:
        Saves dictionary into the JSON file
    """
    with open(file_path, "w") as file:
        json.dump(data, file)
