import logging
import random
from model.entities import *
from file_recorder.json_parser import *
from file_recorder.xlsx_parser import *

# Configure logging to display information with the desired format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def preparing_conditions(required_device_groups: typing.Dict) -> typing.Dict:
    """
    Prepare a dictionary to track the needed count for each device group.

    Args:
        required_device_groups (typing.Dict): Required device counts for each device group.

    Returns:
        typing.Dict: Dictionary with initialized counts for each device group.
    """
    needed = {}

    for group, count in required_device_groups.items():
        if count > 0:
            needed[group] = 0

    return needed


def preparing_departments(departments: typing.Dict, office_locations: typing.Dict) -> typing.Dict:
    """
    Prepare departments by filtering users based on office locations and affected status.

    Args:
        departments (typing.Dict): Dictionary of departments.
        office_locations (typing.Dict): Allowed office locations.

    Returns:
        typing.Dict: Filtered departments.
    """
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
    """
    Calculate the target number of users to select from a department.

    Args:
        department (Department): The department to calculate the target for.
        selection_conditions (typing.Dict): Selection conditions.

    Returns:
        int: Target number of users to select.
    """
    target_percent = selection_conditions['target_percent']/100
    return int(target_percent * len(department.user_list))+1


def is_user_affected(user: User) -> bool:
    """
    Check if a user is affected based on affected status or affected devices.

    Args:
        user (User): The user to check.

    Returns:
        bool: True if user is affected, False otherwise.
    """
    return user.affected is not None or any(device.affected is not None for device in user.device_list)


def check_device_count(group: str, selected_devices: typing.Dict, required_devices: typing.Dict) -> bool:
    """
    Check if the selected device count for a group meets the requirement.

    Args:
        group (str): The device group.
        selected_devices (typing.Dict): Dictionary to track selected devices.
        required_devices (typing.Dict): Required device counts.

    Returns:
        bool: True if device count meets the requirement, False otherwise.
    """
    if selected_devices[group] >= required_devices[group]:
        return True
    else:
        selected_devices[group] += 1
        return False


def select_users_from_department(department: typing.Dict.values, selected_devices: typing.Dict, selection_conditions: typing.Dict) -> List[User]:
    """
    Select users from a department based on selection conditions.

    Args:
        department (Department): The department to select users from.
        selected_devices (typing.Dict): Dictionary to track selected devices.
        selection_conditions (typing.Dict): Selection conditions.

    Returns:
        List[User]: List of selected users.
    """
    # Creating empty selected users list
    selected_users = []
    # Calculating maximal number of affected users in department
    department_target = check_department_target(
        department, selection_conditions)
    # Shuffling user list
    random.shuffle(department.user_list)
    for user in department.user_list:
        # If department already had enough users in pilot groups, stop selecting users
        if len(selected_users) >= department_target:
            break
        # If user already participated in Pilot group, app will check other users
        if user in selected_devices:
            continue
        # Shuffling user's devices
        random.shuffle(user.device_list)
        for device in user.device_list:
            if device.group in selection_conditions['required']:
                if check_device_count(device.group, selected_devices, selection_conditions['required']):
                    continue
                else:
                    user.device_list = [device]
                    selected_users.append(user)
                    break
            else:
                continue

    return selected_users


def random_selection(departments: typing.Dict, selection_conditions: typing.Dict) -> typing.Dict:
    """
    Perform random selection of users based on selection conditions.

    Args:
        departments (typing.Dict): Dictionary of departments.
        selection_conditions (typing.Dict): Selection conditions.

    Returns:
        typing.Dict: Dictionary mapping department names to selected users.
    """
    result_map = {}
    # Creating selected devices dictionary {"type":device_count}
    selected_devices = preparing_conditions(selection_conditions['required'])
    # Removing users and departments based on office location and affected in Pilot groups criteria
    departments = preparing_departments(
        departments, selection_conditions['office_locations'])
    # Shuffling department
    departments = list(departments.items())
    random.shuffle(departments)
    departments = dict(departments)
    # Selecting users for Pilot groups for each department
    for department in departments.values():
        selected_users = select_users_from_department(
            department, selected_devices, selection_conditions)
        if selected_users:
            result_map[department.name] = Department(
                department.name, selected_users)
    # Checking selected and required devices count
    for device_group, value in selected_devices.items():
        if value < selection_conditions['required'][device_group]:
            logging.info(
                f"We coulnd't select {selection_conditions['required'][device_group]} \"{device_group}\" devices: only {value} \"{device_group}\" devices were selected")

    return result_map
