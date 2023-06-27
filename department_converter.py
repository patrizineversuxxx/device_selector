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


def assign_device_group(device_record):
    device_is_managed = device_record['isManaged']
    device_last_checkin_date = device_record['approximateLastSignInDateTime']
    device_enrollment_type = device_record['enrollmentType']

    device_os = device_record['operatingSystem']

    match device_os:
        case "MacOS":
            return None

        case "MacMDM":
            device_type = "Computer"
            device_group = "MacMDM"

        case "iOS":
            device_type = "iPhone"
            device_group = "iPhone MAM"

        case "IPad":
            if device_enrollment_type == "null":
                return None
            device_type = "iPad"
            device_group = "iPad MDM"

        case "IPhone":
            if device_enrollment_type == "null":
                return None
            device_type = "iPhone"
            device_group = "iPhone MDM"

        case "Linux":
            if check_virtual_device(device_record):
                device_type = "Virtual Machine"
                device_group = "Virtual Linux"
            else:
                device_type = "Computer"
                device_group = "Linux"

        case "Windows":
            if device_is_managed == "false":
                return None

            if device_enrollment_type == "OnPremiseCoManaged":
                device_enrollment_type = "Hybrid Joined"
            else:
                device_enrollment_type = "Azure AD Joined"

            if check_virtual_device(device_record):
                device_type = "Virtual Machine"
                device_group = "Virtual Windows" + device_enrollment_type
            else:
                device_type = "Computer"
                device_group = "Windows" + device_enrollment_type

        case _:
            device_type = "Android"

            if device_enrollment_type == "null":
                device_enrollment_type = "MAM"
                device_group = "Android MAM"
            else:
                device_enrollment_type = "MDM"
                device_group = "Android MDM"

    device = Device(id=device_record['id'],
                    name=device_record['displayName'],
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

        if not user_record['devices']:
            continue
        for device_record in user_record['devices']:
            device = assign_device_group(device_record)
            if device is None:
                continue
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
