from сonfig import *
from json_parser import *
from ms_graph_data_grabber import *
from job_title_selector import *
from entities import *
from random_device_selector import *
from ms_graph_connector import *


# Reading the configuration files
configuration = get_config()
#'''
# Creating a connection to API and saving requests headers
headers = connect_to_api(
    connection_parameters=configuration.connection_parameters)

# Grabbing all of the users info from MS Graph
users = get_users_from_API(
    headers=headers, office_locations=configuration.selection_conditions['office_locations'])
#users = get_intune_devices_from_API(headers=headers, naming_tags=["EVN"])
# Saving users info into the JSON file
save_json(data=users, file_path='C:/KEK/kek.json')#file_path=configuration.file_paths['path_user'])
'''
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
'''