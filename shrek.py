# Open data grabbed from API

from file_recorder.json_parser import open_json
from selector.сonfig import get_config


configuration = get_config()
#penis = configuration.file_paths['path_user']
users = open_json("C:\KEK\KEK_Users.json")
print(3)