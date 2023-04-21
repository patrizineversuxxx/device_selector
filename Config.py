import typing


class Config:
    def __init__(
        self,
        connection_parameters: typing.Dict,
        file_paths: typing.Dict[str, str],
        selection_conditions: typing.Dict
    ):
        self._connection_parameters = connection_parameters,
        self._file_paths = file_paths
        self._selection_conditions = selection_conditions

    @property
    def connection_parameters(self) -> typing.Dict[str, str]:
        return self._connection_parameters

    @property
    def file_paths(self) -> typing.Dict[str, str]:
        return self._file_paths

    @property
    def selection_conditions(self) -> typing.Dict[str, str]:
        return self._selection_conditions
