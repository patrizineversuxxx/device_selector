
# Creating a connection to API and saving requests headers
from file_recorder.json_parser import save_json
from model.department_converter import parse_affected
from ms_graph_grabber.ms_graph_connector import connect_to_api
from ms_graph_grabber.ms_graph_data_grabber import get_affected_users, get_users_from_API
from selector.сonfig import get_config

def data_grabber_flow():
    # Reading the configuration files
    configuration = get_config()

    # Create request headers
    headers = connect_to_api(
        connection_parameters=configuration.connection_parameters)
    # Message to the server
    print("Connection established!")
    
    # Grabbing all of the users info from MS Graph
    users = get_users_from_API(headers=headers)
    # Grabbing all of the users and devices, which participated in Pilots from MS Graph
    affected = get_affected_users(headers=headers)
    # Creating two dictionaries of affected users and devices
    affected = parse_affected(affected)
    # Saving users info into the JSON file
    save_json(data=users, file_path=configuration.file_paths['path_user'])
    save_json(data=affected, file_path=configuration.file_paths['path_affected'])
