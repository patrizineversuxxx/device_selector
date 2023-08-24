from model.department_converter import get_data_from_json
from file_recorder.json_parser import *
from file_recorder.xlsx_parser import *
from selector.job_title_selector import *
from selector.random_device_selector import *
from selector.сonfig import *


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
    # Open data grabbed from API
    users = open_json(configuration.file_paths['path_user'])
    affected = open_json(configuration.file_paths['path_affected'])

    # Creating departments from users and devices data
    departments = get_data_from_json(users, affected)

    # Saving records in xlsx table
    save_data_to_xlsx_prepational_step(
        departments, configuration.file_paths['start_file'])

    # Deleting records from previous table, which contains filtered job titles, and saves the result in the another xlsx file
    check_xlsx_for_vip(file_paths=configuration.file_paths)

    # Randomly selecting needed devices using user's conditions
    departments = get_data_from_xlsx(
        path=configuration.file_paths['middle_file'])[0]
    result = random_selection(
        departments=departments, selection_conditions=configuration.selection_conditions,)

    # Saving the result in the xlsx table
    save_data_to_xlsx_prepational_step(
        result, configuration.file_paths['result_file'])
    return 0
