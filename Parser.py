import json
from Entities import *


def open_json(path: str):
    with open(path) as f:
        records = json.load(f)
    return records


def get_data_from_json(params: dict):
    records = open_json(params['path_user'])

    department_map = {}
    user_map = {}

    for record in records:
        user_id = record['id']

        user = User(id=user_id, name=record['displayName'], mail=record['mail'], manager_name=record['manager_name'], manager_mail=record['manager_mail'],
                    job_title=record['jobTitle'], location=record['officeLocation'], device_list=[])

        user_map[user_id] = user

        department_name = record['department']

        if department_name in department_map:
            department_map[department_name].user_list.append(user)
        else:
            department_map[department_name] = Department(
                name=department_name, cost_center=0, user_list=[user])

    records = open_json(params['path_device'])

    for record in records:
        if record['usersLoggedOn'] == []:
            continue
        else:
            device_last_checkin_date = record['usersLoggedOn'][0]['lastLogOnDateTime']

        device_enrollment_type = record['deviceEnrollmentType']
        device_os = record['operatingSystem']
        device_group = ""

        if (device_enrollment_type == "windowsAzureADJoin") & (device_os == "Windows"):
            device_group = "AAD_Joined"
        else:
            if (device_enrollment_type == "windowsCoManagement") & (device_os == "Windows"):
                device_group = "Hybrid_Joined"
            else:
                if (device_enrollment_type == "userEnrollment") & (device_os == "macOS"):
                    device_group = "macOS"

        device = Device(id=record['azureActiveDirectoryDeviceId'], name=record['deviceName'], group=device_group,
                        os=device_os, last_checkin_date=device_last_checkin_date)

        device_user_id = record['userId']

        if device_user_id in user_map:
            user_map[device_user_id].device_list.append(device)
        else:
            continue

    return department_map
