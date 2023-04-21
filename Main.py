from Config import *
from JSON_Parser import *
from MS_Graph_Data_Grabber import *
from Job_Title_Selector import *
from Entities import *
from Random_Device_Selector import *
from MS_Graph_Connector import *

#Reading all of the configurational files
connection_parameters = open_json("config.json")
file_paths = open_json("file_paths.json")
selection_conditions = open_json("selection_conditions.json")

# Creating an entity for using configurational parameters
config = Config(
        redirect_uri=connection_parameters['client_id'], 
        client_credentials=connection_parameters['client_id'], 
        authority_url=connection_parameters['authority_url'], 
        scopes=connection_parameters['scopes'], 
        file_paths=file_paths, 
        selection_conditions = selection_conditions
    )

# Creating a connection to API and saving requests headers
headers = connect_to_api(params=connection_parameters) #   params['redirect_uri'] params['client_credentials']

# Grabbing all of the users info from MS Graph
users = user_to_json_grabbing(headers=headers, params=connection_parameters)

# Saving users info into the JSON file
save_json(data=users, file_path=connection_parameters['path_user'])

# Grabbing all of the devices info from MS Graph
devices = device_to_json_grabbing(headers=headers, params=connection_parameters)

# Saving devices info into the JSON file
save_json(data=users, file_path=connection_parameters['path_device'])

# Creating departments from users and devices data
departmens = get_data_from_json(params=connection_parameters)

# Saving records in xlsx table
save_data_to_xlsx_prepational_step(departmens, connection_parameters)

# Deleting records from previous table, which contains filtered job titles, and saves the result in the another xlsx file
check_xlsx_for_vip(params=connection_parameters)

# Randomly selecting needed devices using user's conditions
result = random_selection(params=connection_parameters)

# Saving the result in the xlsx table
save_data_to_xlsx(result, connection_parameters)
