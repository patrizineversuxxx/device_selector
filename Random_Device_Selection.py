import random
import openpyxl
from Data import *
from Parser import *


def check_department_target(department, params):
    target_percent = params[target_percent]
    return int(target_percent * len(department.user_list))+1


def random_selection(params: dict):
    path = params['middle_file']
    workbook = openpyxl.load_workbook(path)
    spreadsheet = workbook.active

    department_map = {}
    user_map = {}
    device_list = []

    get_data_from_xlsx(spreadsheet, department_map, user_map, device_list)

    departments = list(department_map.values())
    user_map = list(user_map.values())

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
            user_device[temp[0]] = temp[1]
            aad_map.pop(department)
            result_map[department] = user_device
            count += 1
        departments.remove(department)

    departments = list(department_map.values())

    for department in departments:
        target = check_department_target(department, params)
        if department in result_map:
            while len(result_map[department]) < target:
                user = random.choice(department.user_list)
                device = random.choice(user.device_list)
                result_map[department][user] = device
        else:
            user = random.choice(department.user_list)
            device = random.choice(user.device_list)
            result_map[department] = {}
            result_map[department][user] = device

    save_data_to_xlsx(result_map)
