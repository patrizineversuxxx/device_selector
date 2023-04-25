import json
import typing
from Entities import *


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


def get_data_from_json(users: typing.Dict, devices: typing.Dict) -> typing.Dict[str, Department]:
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
        user_id = record['id']

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

        department_name = user_record['department']

        if department_name in department_map:
            department_map[department_name].user_list.append(user)
        else:
            department_map[department_name] = Department(
                name=department_name,
                cost_center=0,
                user_list=[user]
            )

    # Read all of the device records in the file
    for device_record in devices:
        if not device_record['usersLoggedOn']:
            continue
        else:
            device_last_checkin_date = device_record['usersLoggedOn'][0]['lastLogOnDateTime']

        device_enrollment_type = device_record['deviceEnrollmentType']
        device_os = device_record['operatingSystem']

        if device_enrollment_type == "windowsAzureADJoin" and device_os == "Windows":
            device_group = "AAD_Joined"
        elif device_enrollment_type == "windowsCoManagement" and device_os == "Windows":
            device_group = "Hybrid_Joined"
        elif device_enrollment_type == "userEnrollment" and device_os == "macOS":
            device_group = "macOS"
        else:
            continue

        device = Device(id=device_record['azureActiveDirectoryDeviceId'],
                        name=device_record['deviceName'],
                        group=device_group,
                        os=device_os,
                        last_checkin_date=device_last_checkin_date
                        )

        device_user_id = device_record['userId']

        if device_user_id in user_map:
            user_map[device_user_id].device_list.append(device)
        else:
            continue

    return department_map
