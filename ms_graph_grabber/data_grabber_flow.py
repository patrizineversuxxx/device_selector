# Import statements
from file_recorder.json_parser import save_json
from model.department_converter import parse_affected
from ms_graph_grabber.ms_graph_connector import connect_to_api
from ms_graph_grabber.ms_graph_data_grabber import get_affected_users, get_users_from_API
from selector.сonfig import get_config

def data_grabber_flow():
    """
    This function orchestrates the data grabbing flow from MS Graph API and saving the results.

    It does the following steps:
    1. Reads configuration files using get_config() function.
    2. Establishes a connection to the API using connect_to_api().
    3. Prints a message indicating a successful connection.
    4. Grabs users' information from MS Graph API using get_users_from_API().
    5. Grabs information about users and devices participating in pilots from MS Graph API using get_affected_users().
    6. Parses the affected users and devices using parse_affected().
    7. Saves the users' information into a JSON file specified in the configuration.
    8. Saves the affected users' and devices' information into separate JSON files specified in the configuration.
    """
    # Reading the configuration files
    configuration = get_config()

    # Create request headers
    headers = connect_to_api(
        connection_parameters=configuration.connection_parameters)
    
    # Print a message indicating a successful connection
    print("Connection established!")

    # Grabbing all of the users info from MS Graph
    users = get_users_from_API(headers=headers)
    
    # Grabbing all of the users and devices participating in Pilots from MS Graph
    affected = get_affected_users(headers=headers)
    
    # Creating two dictionaries of affected users and devices
    affected = parse_affected(affected)
    
    # Saving users info into the JSON file
    save_json(data=users, file_path=configuration.file_paths['path_user'])
    
    # Saving affected users and devices info into separate JSON files
    save_json(data=affected, file_path=configuration.file_paths['path_affected'])
