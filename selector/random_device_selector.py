import random
from model.entities import *
from file_recorder.json_parser import *
from file_recorder.xlsx_parser import *


def preparing_conditions(required_device_groups):

    needed = {}

    for group, count in required_device_groups.items():
        if count > 0:
            needed[group] = 0

    return needed


def preparing_departments(departments: typing.Dict, office_locations: typing.Dict) -> typing.Dict:
    toRemove = []

    for department in departments.values():
        i = 0
        while (i < len(department.user_list)):
            is_affected = False

            if not department.user_list[i].location in office_locations:
                department.user_list.pop(i)
                continue
            if not department.user_list[i].affected is None:
                department.user_list.pop(i)
                continue
            else:
                for device in department.user_list[i].device_list:
                    if not device.affected is None:
                        department.user_list.pop(i)
                        is_affected = True
                        break
                if (is_affected):
                    continue
            i += 1
        if len(department.user_list) == 0:
            toRemove.append(department.name)

    for key in toRemove:
        departments.pop(key)
    return departments


def check_department_target(department: Department, selection_conditions: typing.Dict) -> int:
    target_percent = selection_conditions['target_percent']/100
    return int(target_percent * len(department.user_list))+1


def is_user_affected(user):
    return user.affected is not None or any(device.affected is not None for device in user.device_list)


def check_device_count(group: str, selected_devices: typing.Dict, required_devices: typing.Dict) -> bool:
    if selected_devices[group] >= required_devices[group]:
        return True
    else:
        selected_devices[group] += 1
        return False


def select_users_from_department(department: typing.Dict.values, selected_devices: typing.Dict, selection_conditions: typing.Dict):
    selected_users = {}
    department_target = check_department_target(
        department, selection_conditions)

    while len(selected_users) < department_target:
        user = random.choice(department.user_list)

        if user in selected_devices:
            continue

        device = random.choice(user.device_list)
        if device.group in selection_conditions['required']:
            if check_device_count(device.group, selected_devices, selection_conditions['required']):
                continue
        else:
            continue

        selected_users[user] = device

    return selected_users


def random_selection(departments: typing.Dict, selection_conditions: typing.Dict) -> typing.Dict:
    result_map = {}
    selected_devices = preparing_conditions(selection_conditions['required'])
    departments = preparing_departments(
        departments, selection_conditions['office_locations'])

    for department in departments.values():
        selected_users = select_users_from_department(
            department, selected_devices, selection_conditions)
        if selected_users:
            result_map[department] = selected_users

    return result_map


'''def legacy_random_selection(departments: typing.Dict, selection_conditions: typing.Dict, path: str) -> typing.Dict[Department, typing.Dict[User, Device]]:

    toRemove = []

    for department in departments.values():
        i = 0
        while (i < len(department.user_list)):
            is_affected = False

            if not department.user_list[i].location in selection_conditions['office_locations']:
                department.user_list.pop(i)
                continue
            if not department.user_list[i].affected is None:
                department.user_list.pop(i)
                continue
            else:
                for device in department.user_list[i].device_list:
                    if not device.affected is None:
                        department.user_list.pop(i)
                        is_affected = True
                        break
                if (is_affected):
                    continue
            i += 1
        if len(department.user_list) == 0:
            toRemove.append(department.name)

    for key in toRemove:
        departments.pop(key)

    result_map = {}

    # needs to be rewritten because of dict (d, dict) construction
    for department in departments.values():
        department_target = check_department_target(
            department, selection_conditions)

        if department in result_map:
            while len(result_map[department]) < department_target:
                user = random.choice(department.user_list)
                device = random.choice(user.device_list)

                if device.group in needed:
                    if check_device_count(device.group, needed, requirements):
                        continue
                else:
                    continue

                result_map[department][user] = device
        else:
            user = random.choice(department.user_list)
            device = random.choice(user.device_list)

            if device.group in needed:
                if check_device_count(device.group, needed, requirements):
                    continue
            else:
                continue

            result_map[department] = {}
            result_map[department][user] = device

    return result_map
    '''
