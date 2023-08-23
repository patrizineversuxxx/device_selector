# Import statements
import logging
from file_recorder.json_parser import save_json
from model.department_converter import parse_affected
from ms_graph_grabber.ms_graph_connector import connect_to_api
from ms_graph_grabber.ms_graph_data_grabber import get_affected_users, get_users_from_API
from selector.сonfig import get_config

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def data_grabber_flow():
    """
    Orchestrate the data grabbing flow from MS Graph API and save the results.

    Steps:
    1. Read configuration files using get_config() function.
    2. Establish a connection to the API using connect_to_api().
    3. Log a message indicating a successful connection.
    4. Grab users' information from MS Graph API using get_users_from_API().
    5. Grab information about users and devices participating in pilots from MS Graph API using get_affected_users().
    6. Parse the affected users and devices using parse_affected().
    7. Save the users' information into a JSON file specified in the configuration.
    8. Save the affected users' and devices' information into separate JSON files specified in the configuration.
    """
    try:
        # Reading the configuration files
        configuration = get_config()

        # Create request headers
        headers = connect_to_api(
            connection_parameters=configuration.connection_parameters)

        # Log a message indicating a successful connection
        logging.info("Connection established!")

        # Grab all users' info from MS Graph
        users = get_users_from_API(headers=headers)

        # Grab info about users and devices participating in Pilots from MS Graph
        affected = get_affected_users(headers=headers)

        # Create two dictionaries of affected users and devices
        affected = parse_affected(affected)

        # Save users' info into the JSON file
        save_json(data=users, file_path=configuration.file_paths['path_user'])

        # Save affected users' and devices' info into separate JSON files
        save_json(data=affected,
                  file_path=configuration.file_paths['path_affected'])

        logging.info("Data grabbing and saving completed!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
