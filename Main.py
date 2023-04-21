from Config import *
from JSON_Parser import *
from MS_Graph_Data_Grabber import *
from Job_Title_Selector import *
from Entities import *
from Random_Device_Selector import *
from MS_Graph_Connector import *

# Creating an entity for using configurational parameters
params = open_json("config.json")
file_paths = open_json("file_paths.json")
config = Config(redirect_uri=params['client_id'], client_credentials=params['client_id'], authority_url=params['authority_url'], scopes=params['scopes'], file_paths=file_paths)

# Creating a connection to API and saving requests headers
headers = connect_to_api(params=params) #   params['redirect_uri'] params['client_credentials']

# Grabbing all of the users info from MS Graph
users = user_to_json_grabbing(headers=headers, params=params)

# Saving users info into the JSON file
save_json(data=users, file_path=params['path_user'])

# Grabbing all of the devices info from MS Graph
devices = device_to_json_grabbing(headers=headers, params=params)

# Saving devices info into the JSON file
save_json(data=users, file_path=params['path_device'])

# Creating departments from users and devices data
departmens = get_data_from_json(params=params)

# Saving records in xlsx table
save_data_to_xlsx_prepational_step(departmens, params)

# Deleting records from previous table, which contains filtered job titles, and saves the result in the another xlsx file
check_xlsx_for_vip(params=params)

# Randomly selecting needed devices using user's conditions
result = random_selection(params=params)

# Saving the result in the xlsx table
save_data_to_xlsx(result, params)
