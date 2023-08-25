import logging
import typing
import os
from file_recorders.json_recorder import open_json


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        # Joining file paths
        settings_home_path = "config_files"
        connection_settings_path = os.path.join(settings_home_path, "config.json")
        file_paths_settings_path = os.path.join(settings_home_path, "file_paths.json")
        selection_settings_path = os.path.join(settings_home_path, "selection_conditions.json")
        # Reading all of the configurational files
        connection_parameters = open_json(connection_settings_path)
        file_paths = open_json(file_paths_settings_path)
        selection_conditions = open_json(selection_settings_path)

        # Creating an entity for using configurational parameters
        return Config(
            connection_parameters=connection_parameters,
            file_paths=file_paths,
            selection_conditions=selection_conditions
        )
    except FileNotFoundError as e:
        logging.error("Configuration file not found.")
        raise e
    except Exception as e:
        logging.error(f"An error occurred while reading configuration: {e}")
        raise e

if __name__ == "__main__":
    try:
        config = get_config()
        logging.info("Configuration successfully loaded.")
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        exit(1)