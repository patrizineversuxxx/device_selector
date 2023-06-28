import typing
from file_recorder.json_parser import open_json


class Config:
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
        return self._connection_parameters

    @property
    def file_paths(self) -> typing.Dict[str, str]:
        return self._file_paths

    @property
    def selection_conditions(self) -> typing.Dict:
        return self._selection_conditions


def get_config():
    # Reading all of the configurational files
    connection_parameters = open_json(r"config_files\config.json")
    file_paths = open_json(r"config_files\file_paths.json")
    selection_conditions = open_json(r"config_files\selection_conditions.json")

    # Creating an entity for using configurational parameters
    return Config(
        connection_parameters=connection_parameters,
        file_paths=file_paths,
        selection_conditions=selection_conditions
    )
