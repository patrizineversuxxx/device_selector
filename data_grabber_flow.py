
# Creating a connection to API and saving requests headers
from json_parser import save_json
from ms_graph_connector import connect_to_api
from ms_graph_data_grabber import get_users_from_API
from сonfig import get_config

# Reading the configuration files
configuration = get_config()

# Create request headers
headers = connect_to_api(
    connection_parameters=configuration.connection_parameters, device_flow=True)

# Grabbing all of the users info from MS Graph
users = get_users_from_API(
    headers=headers, office_locations=configuration.selection_conditions['office_locations'])
#users = get_intune_devices_from_API(headers=headers, naming_tags=["EVN"])
# Saving users info into the JSON file
save_json(data=users, file_path='C:/KEK/kek.json')#file_path=configuration.file_paths['path_user'])
