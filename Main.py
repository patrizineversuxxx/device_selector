from Parser import *
from MS_Graph_Data_Grabber import *
from Job_Title_Selector import *
from Entities import *
from Random_Device_Selector import *
from MS_Graph_Connector import *

def read_config():#needs to be rewritten using with statement and creating a config class instance
    f = open("config.json")
    params = json.load(f)
    f.close()
    return params #return config


params = read_config()
headers = connect_to_api(params=params)
users = user_to_json_grabbing(headers=headers, params=params)
save_json(data=users, file_path=params['path_user'])
devices = device_to_json_grabbing(headers=headers, params=params)
save_json(data=users, file_path=params['path_device'])
departmens = get_data_from_json(params=params)
save_data_to_xlsx_prepational_step(departmens,params)
check_xlsx_for_vip(params=params)
result = random_selection(params=params)
save_data_to_xlsx(result, params)