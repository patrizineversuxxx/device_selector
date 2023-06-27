from department_converter import get_data_from_json
from сonfig import *
from json_parser import *
from ms_graph_data_grabber import *
from job_title_selector import *
from entities import *
from random_device_selector import *
from ms_graph_connector import *


# Reading the configuration files
configuration = get_config()

#Open data grabbed from API
users = open_json(configuration.file_paths['path_user'])

# Creating departments from users and devices data
departmens = get_data_from_json(users)

# Saving records in xlsx table
save_data_to_xlsx_prepational_step(
    departmens, configuration.file_paths["start_file"])

# Deleting records from previous table, which contains filtered job titles, and saves the result in the another xlsx file
check_xlsx_for_vip(file_paths=configuration.file_paths)

# Randomly selecting needed devices using user's conditions
result = random_selection(selection_conditions=configuration.selection_conditions,
                          path=configuration.file_paths['middle_file'])

# Saving the result in the xlsx table
save_data_to_xlsx(result, configuration.file_paths['result_file'])

