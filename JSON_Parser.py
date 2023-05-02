import json
import typing
from entities import *


vm_vendors = ["Parallels International GmbH.",
              "Parallels Software International Inc.", "VMware, Inc."]
vm_models = ["Cloud PC Enterprise", "VirtualBox"]


def check_virtual_device(device_record: typing.Dict):
    device_manufacturer = device_record['manufacturer']
    if device_manufacturer:
        if device_manufacturer in vm_vendors:
            return True
        else:
            device_model = device_record['model']
            for vm_model in vm_models:
                if vm_model in device_model:
                    return True
    return False


def open_json(path: str) -> typing.Dict[str, typing.Any]:
    """
    Opens a JSON file and returns its contents as a dictionary.

    Args:
        path: A string representing the path to the JSON file.

    Returns:
        A dictionary representing the contents of the JSON file.
    """
    with open(path) as file:
        data = json.load(file)
    return data


def save_json(data: typing.Dict, file_path: str):
    """
    A dictionary representing the contents of the needed JSON file

    Args:
        data: A dictionary with needed data
        path: A string representing the path to the JSON file.

    Returns:
        Saves dictionary into the JSON file
    """
    with open(file_path, "w") as file:
        json.dump(data, file)


def get_data_from_json(users: typing.Dict) -> typing.Dict[str, Department]:
    """
    Parses user and device data from JSON files and creates Department objects.

    Args:
        params: A dictionary containing the paths to the user and device JSON files.

    Returns:
        A dictionary containing Department objects indexed by department name.
    """
    department_map = {}
    user_map = {}

    # Read all of the user records in the file
    for user_record in users:
        user_id = user_record['id']

        user = User(id=user_id,
                    name=user_record['displayName'],
                    mail=user_record['mail'],
                    manager_name=user_record['manager_name'],
                    manager_mail=user_record['manager_mail'],
                    job_title=user_record['jobTitle'],
                    location=user_record['officeLocation'],
                    device_list=[]
                    )

        user_map[user_id] = user

        for device_record in user_record['devices']:

            device_last_checkin_date = device_record['approximateLastSignInDateTime']

            device_enrollment_type = device_record['enrollmentType']
            device_os = device_record['operatingSystem']

            if device_os == 'Windows':
                if check_virtual_device(device_record):
                    device_type = "virtual"
                    if device_enrollment_type is None:
                        continue
                    elif device_enrollment_type == "OnPremiseCoManaged":
                        device_enrollment_type = "HybridJoined"
                        device_group = "Virtual HybridJoined"
                    else:
                        device_enrollment_type = "AzureADJoined"
                        device_group = "Virtual AzureADJoined"
                else:
                    device_type = "computer"
                    if device_enrollment_type is None:
                        continue
                    elif device_enrollment_type == "OnPremiseCoManaged":
                        device_enrollment_type = "HybridJoined"
                        device_group = "Computer HybridJoined"
                    else:
                        device_enrollment_type = "AzureADJoined"
                        device_group = "Computer AzureADJoined"
            elif "Mac" in device_os:
                device_group = "MacMDM"
                device_type = "phone"
                device_enrollment_type = "MacMDM"
            elif "Android" in device_os:
                if device_enrollment_type is None:
                    device_group = "Android MAM"
                    device_type = "phone"
                    device_enrollment_type = "MAM"
                else:
                    device_group = "Android MDM"
                    device_type = "phone"
                    device_enrollment_type = "MDM"
            elif "IPad" in device_os:
                device_group = "iPad MDM"
                device_type = "tablet"
                device_enrollment_type = "MDM"
            elif "IPhone" in device_os:
                device_group = "iPhone MDM"
                device_type = "phone"
                device_enrollment_type = "MDM"
            elif "iOS" in device_os:
                device_group = "iPhone MDM"
                device_type = "phone"
                device_enrollment_type = "MDM"

            device = Device(id=device_record['id'],
                            name=device_record['displayName'],
                            group=device_group,
                            enrollment_type=device_enrollment_type,
                            os=device_os,
                            type=device_type,
                            last_checkin_date=device_last_checkin_date
                            )

            user.add_device(device)

        department_name = user_record['department']

        if department_name in department_map:
            department_map[department_name].add_user(user)
        else:
            department_map[department_name] = Department(
                name=department_name,
                cost_center=0,
                user_list=[user]
            )

    return department_map
