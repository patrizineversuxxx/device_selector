import random
import openpyxl
from Data import *
from Parser import *


def check_department_target(department):
    return int(0.12 * len(department.user_list))+1


path = r'C:\KEK\ID_RANDOM.xlsx'
workbook = openpyxl.load_workbook(path)
spreadsheet = workbook.active

department_list = {}
user_list = {}
device_list = []

target_percent = 0.12
parse_datatable(spreadsheet, department_list, user_list, device_list)

departments = list(department_list.values())
user_list = list(user_list.values())

aad_map = {}
# Selecting AAD_Joined devices
for department in departments:
    device_user = {}
    for user in department.user_list:
        for device in user.device_list:
            if device.group == 'AAD_Joined':
                device_user[user] = device
                aad_map[department] = device_user

result_map = {}

# Selecting 45 AAD_Joined devices for Pilot group
target = 45
count = 0

while count < target:
    department = random.choice(departments)
    if (department in aad_map): 
        temp = list(aad_map[department].items())[0]
        user_device = {}
        user_device[temp[0]]= temp[1]
        aad_map.pop(department)
        result_map[department] = user_device
        count += 1
    departments.remove(department)
    
departments = list(department_list.values())

for department in departments:
    target = int(len(department.user_list) * 0.12)+1
    if department in result_map:
        while len(result_map[department]) < target:
            user = random.choice(department.user_list)
            device = random.choice(user.device_list)
            result_map[department][user]= device
    else:
        user = random.choice(department.user_list)
        device = random.choice(user.device_list)
        result_map[department] = {}
        result_map[department][user] = device


save_result(result_map)