# Import statements
import datetime
import logging
from file_recorders.json_recorder import save_json
from model.department_converter import parse_affected
from ms_graph_grabber.api_connector import connect_to_api
from ms_graph_grabber.api_data_grabber import get_affected_users, get_users_from_API
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
        logging.info(f"Data grabbing process started at {datetime.datetime.now()}")
        # Reading the configuration files
        configuration = get_config()
        logging.info(f"Creating access token and adding it to the request headers")
        # Create request headers
        headers = connect_to_api(
            connection_parameters=configuration.connection_parameters)

        # Log a message indicating a successful connection
        logging.info("Connection established!")
        logging.info("Started getting user data")
        # Grab all users' info from MS Graph
        users = get_users_from_API(headers=headers)
        logging.info("Getting user data was completed")
        # Grab info about users and devices participating in Pilots from MS Graph
        logging.info("Started getting affected users data")
        affected = get_affected_users(headers=headers)
        logging.info("Getting affected users data was completed")
        # Create two dictionaries of affected users and devices
        affected = parse_affected(affected)

        # Save users' info into the JSON file
        logging.info("Saving user data")
        save_json(data=users, file_path=configuration.file_paths['path_user'])
        logging.info("Saving user data was completed")
        # Save affected users' and devices' info into separate JSON files
        logging.info("Saving affected user data")
        save_json(data=affected,
                  file_path=configuration.file_paths['path_affected'])
        logging.info("Saving affected user data was completed")

        logging.info(f"Data grabbing process has completed with exit code {0}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
