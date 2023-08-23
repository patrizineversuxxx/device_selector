import typing
from file_recorder.json_parser import open_json


class Config:
    """
    A configuration class to hold connection parameters, file paths, and selection conditions.

    Attributes:
        connection_parameters (dict): Parameters for establishing a connection.
        file_paths (dict): Paths to various files.
        selection_conditions (dict): Conditions for device selection.
    """
    def __init__(
        self,
        connection_parameters: typing.Dict,
        file_paths: typing.Dict[str, str],
        selection_conditions: typing.Dict,

    ):
        self._connection_parameters = connection_parameters
        self._file_paths = file_paths
        self._selection_conditions = selection_conditions

    @property
    def connection_parameters(self) -> typing.Dict:
        """Get the connection parameters."""
        return self._connection_parameters

    @property
    def file_paths(self) -> typing.Dict[str, str]:
        """Get the file paths."""
        return self._file_paths

    @property
    def selection_conditions(self) -> typing.Dict:
        """Get the selection conditions."""
        return self._selection_conditions


def get_config():
    """
    Reads configuration files and returns a Config object.

    Returns:
        Config: A Config object containing connection parameters, file paths, and selection conditions.
    """
    # Reading all of the configurational files
    connection_parameters = open_json(f"config_files\config.json")
    file_paths = open_json(f"config_files\file_paths.json")
    selection_conditions = open_json(f"config_files\selection_conditions.json")

    # Creating an entity for using configurational parameters
    return Config(
        connection_parameters=connection_parameters,
        file_paths=file_paths,
        selection_conditions=selection_conditions
    )
