import random
from model.entities import *
from file_recorder.json_parser import *
from file_recorder.xlsx_parser import *


def check_department_target(department: Department, params: typing.Dict) -> int:
    target_percent = params['target_percent']/100
    return int(target_percent * len(department.user_list))+1


def check_device_count(group: str, needed: typing.Dict, requirements: typing.Dict) -> bool:
    if needed[group] >= requirements[group]:
        return True
    else:
        needed[group] += 1
        return False


def random_selection(selection_conditions: typing.Dict, path: str) -> typing.Dict[Department, typing.Dict[User, Device]]:
    departments = get_data_from_xlsx(path)[0]

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

    requirements = selection_conditions['required']

    needed = {}

    for key in requirements.keys():
        needed[key] = 0

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
