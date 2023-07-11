from file_recorder.json_parser import open_json
import typing

from model.entities import *

vm_vendors = ["Parallels International GmbH.",
              "Parallels Software International Inc.", "VMware, Inc."]
vm_models = ["Cloud PC Enterprise", "VirtualBox"]

def get_affected_users_and_devices():
    affected_groups = open_json("C:\KEK\KEK_Affected_Users.json")
    affected_users = {}
    affected_devices = {}
    for affected_group in affected_groups:
        for member in affected_group['members']:
            if member['@odata.type'] == "#microsoft.graph.user":
                affected_users[member['id']] = affected_group['displayName']
            if member['@odata.type'] == "#microsoft.graph.device":
                affected_devices[member['id']] = affected_group['displayName']
    return affected_users, affected_devices


def is_virtual(device_info: typing.Dict) -> bool:
    device_manufacturer = device_info['manufacturer']
    if device_manufacturer:
        if device_manufacturer in vm_vendors:
            return True
        else:
            device_model = device_info['model']
            if device_model:
                for vm_model in vm_models:
                    if vm_model in device_model:
                        return True
    return False


def create_device(device_info) -> Device:
    device_is_managed = device_info['isManaged']
    device_last_checkin_date = device_info['approximateLastSignInDateTime']
    device_enrollment_type = device_info['enrollmentType']

    device_os = device_info['operatingSystem']

    match device_os:
        case "MacOS":
            return None

        case "MacMDM":
            device_type = "Computer"
            device_enrollment_type = "Mac MDM"
            device_group = "Mac MDM"

        case "iOS":
            device_type = "iPhone"
            device_enrollment_type = "MAM"
            device_group = "iPhone MAM"

        case "IPad":
            if device_enrollment_type == "null":
                return None

            device_type = "iPad"
            device_enrollment_type = "MDM"
            device_group = "iPad MDM"

        case "IPhone":
            if device_enrollment_type == "null":
                return None

            device_type = "iPhone"
            device_enrollment_type = "MDM"
            device_group = "iPhone MDM"

        case "Linux":
            if is_virtual(device_info):
                device_type = "Virtual Machine"
                device_group = "Virtual Linux"
            else:
                device_type = "Computer"
                device_group = "Linux"

        case "Windows":
            if not device_is_managed is True:
                return None

            if device_enrollment_type == "OnPremiseCoManaged":
                device_enrollment_type = "Hybrid Joined"
            else:
                device_enrollment_type = "Azure AD Joined"

            if is_virtual(device_info):
                device_type = "Virtual Machine"
                device_group = "Virtual Windows " + device_enrollment_type
            else:
                device_type = "Computer"
                device_group = "Windows " + device_enrollment_type

        case _:
            device_type = "Android"

            if device_enrollment_type == "null":
                device_enrollment_type = "MAM"
                device_group = "Android MAM"
            else:
                device_enrollment_type = "MDM"
                device_group = "Android MDM"

    device = Device(
        id=device_info['id'],
        name=device_info['displayName'],
        group=device_group,
        enrollment_type=device_enrollment_type,
        os=device_os,
        type=device_type,
        last_checkin_date=device_last_checkin_date
    )

    return device


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
    for user_info in users:
        if not user_info['devices']:
            continue

        user_id = user_info['id']

        user = User(
            id=user_id,
            name=user_info['displayName'],
            mail=user_info['mail'],
            manager_name=user_info['manager_name'],
            manager_mail=user_info['manager_mail'],
            job_title=user_info['jobTitle'],
            location=user_info['officeLocation'],
            cost_center=user_info['cost_center'],
            device_list=[]
        )

        user_map[user_id] = user

        for device_record in user_info['devices']:
            device = create_device(device_record)
            if device is None:
                continue
            user.add_device(device)

        department_name = user_info['department']

        if department_name in department_map:
            department_map[department_name].add_user(user)
        else:
            department_map[department_name] = Department(
                name=department_name,
                user_list=[user]
            )

    return department_map
