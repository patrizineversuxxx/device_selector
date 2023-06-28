from file_recorder.json_parser import open_json
from selector.main import device_selector_flow
from selector.сonfig import get_config


# Reading the configuration files
configuration = get_config()
device_selector_flow(configuration)
