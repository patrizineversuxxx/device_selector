import datetime
from model.department_converter import get_data_from_json
from file_recorder.json_parser import *
from file_recorder.xlsx_parser import *
from selector.job_title_selector import *
from selector.random_device_selector import *
from selector.сonfig import *

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def device_selector_flow(configuration: Config):
    """
    Orchestrates the device selection process.

    This function performs the following steps:
    1. Opens user and affected device data from JSON files.
    2. Creates departments from the user and device data.
    3. Saves the department records in a preparation XLSX table.
    4. Filters job titles, deletes records from a previous table, and saves the result in another XLSX file.
    5. Randomly selects devices based on user conditions.
    6. Saves the result of the device selection in an XLSX table.

    Args:
        configuration (Config): A configuration object containing file paths and selection conditions.

    Returns:
        int: 0 indicating successful completion.
    """
    logging.info(
        f"Device selection process started at {datetime.datetime.now()}")
    # Open data grabbed from API
    logging.info(f"Reading users data")
    users = open_json(configuration.file_paths['path_user'])
    logging.info(f"Reading users data was completed")
    logging.info(f"Reading affected users and devices data")
    affected = open_json(configuration.file_paths['path_affected'])
    logging.info(f"Reading affected users and devices data was completed")

    # Creating departments from users and devices data
    logging.info(f"Converting users data into objects")
    departments = get_data_from_json(users, affected)
    logging.info(f"Converting users data into objects was completed")

    # Starting device selection process
    logging.info(f"Starting device selection process")
    result = random_selection(
        departments=departments, selection_conditions=configuration.selection_conditions,)
    logging.info(f"Device selection process was completed")

    # Saving the result in the xlsx table
    logging.info(f"Saving processed data into XLSX table")
    save_data_to_xlsx_prepational_step(
        result, configuration.file_paths['result_file'])
    logging.info(f"Saving processed data was completed")
    return 0
