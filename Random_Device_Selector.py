import random
import openpyxl
from Entities import *
from JSON_Parser import *
from XLSX_Parser import *


def check_department_target(department: Department, params: typing.Dict) -> int:
    target_percent = params['target_percent']/100
    return int(target_percent * len(department.user_list))+1


def get_minimal_group_devices(selection_conditions: typing.Dict, result_map: typing.Dict,
                              department_map: typing.Dict) -> typing.Dict[Department, typing.Dict[User, Device]]:
    minimal_group_map = {}
    # Selecting minimal group devices
    for department in departments:
        device_user = {}
        for user in department.user_list:
            for device in user.device_list:
                if device.group == selection_conditions["minimal_selected_group"]:
                    device_user[user] = device
                    minimal_group_map[department] = device_user

    # Selecting minimal target devices for Pilot group
    minimal_target = selection_conditions['minimal_target']
    count = 0

    while count < minimal_target:
        department = random.choice(departments)
        if (department in minimal_group_map):
            temp = list(minimal_group_map[department].items())[0]
            user_device = {}
            user_device[temp[0]] = temp[1]
            minimal_group_map.pop(department)
            result_map[department] = user_device
            count += 1
        departments.remove(department)

    departments = list(department_map.values())


def check_device_count(group: str, needed: typing.Dict, requerments: typing.Dict) -> bool:
    if needed[group] >= requerments[group]:
        return True
    else:
        needed[group] += 1
        return False


def random_selection(selection_conditions: typing.Dict, path: str) -> typing.Dict[Department, typing.Dict[User, Device]]:
    data = get_data_from_xlsx(path)

    department_map = data[0]
    user_map = data[1]

    departments = list(department_map.values())
    user_map = list(user_map.values())
    result_map = {}

    requerments = selection_conditions['required']
    needed = {"AAD_Joined": 0, "Hybrid_Joined": 0, "macOS": 0}

    # needs to be rewritten because of dict (d, dict) construction
    for department in departments:
        department_target = check_department_target(department, selection_conditions)
        if department in result_map:
            while len(result_map[department]) < department_target:
                user = random.choice(department.user_list)
                device = random.choice(user.device_list)
                if check_device_count(device.group, needed, requerments):
                    continue
                result_map[department][user] = device
        else:
            user = random.choice(department.user_list)
            device = random.choice(user.device_list)
            if check_device_count(device.group, needed, requerments):
                continue
            result_map[department] = {}
            result_map[department][user] = device

    return result_map
