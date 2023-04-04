from Parser import *
from MSGraph_Data_Grabber import *
from JobTitleSelector import *
from Data import *
from Random_Device_Selection import *


def read_config():
    f = open("config.json")
    params = json.load(f)
    f.close()
    return params


params = read_config()
#headers = connect_to_api(params=params)
#user_to_json_grabbing(headers=headers, params=params)
#device_to_json_grabbing(headers=headers, params=params)

save_data_to_xlsx_prepational_step(get_data_from_json(params=params))
check_xlsx_for_vip(params=params)
random_selection(params=params)
