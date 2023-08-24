from model.entities import *
import typing

# List of virtual machine vendors and models
vm_vendors = ["Parallels International GmbH.",
              "Parallels Software International Inc.", "VMware, Inc."]
vm_models = ["Cloud PC Enterprise", "VirtualBox"]


def is_vip(job_title: str) -> bool:  # nneds to be rewritten to job_titles gotten from config class
    # Convert job title to lowercase for case-insensitive matching
    if not job_title:
        return True
    job_title = job_title.lower()

    # Check if the job title contains any VIP keywords
    if "country manager" in job_title or \
       ("sr" in job_title and "manager" in job_title) or \
       ("senior" in job_title and "manager" in job_title) or \
       "gm" in job_title or \
       "president" in job_title or \
       "director" in job_title or \
            "clinical" in job_title or \
    "vp" in job_title or \
        "emc" in job_title or \
            "Executive Admin Assistant" in job_title:
        return True
    else:
        return False


def parse_affected(affected_groups: typing.Dict):
    """
    Parses the affected users and devices from affected_groups data.

    Args:
        affected_groups: A dictionary containing affected group information.

    Returns:
        A tuple of two dictionaries: affected_users and affected_devices.
    """
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
    """
    Determines whether a device is a virtual machine based on its manufacturer and model.

    Args:
        device_info: A dictionary containing device information.

    Returns:
        A boolean indicating whether the device is a virtual machine.
    """
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


def create_device(device_info, device_affected) -> Device:
    """
    Creates a Device object based on device information.

    Args:
        device_info: A dictionary containing device information.
        device_affected: A string indicating the device's affected group.

    Returns:
        A Device object.
    """
    device_is_managed = device_info['isManaged']
    device_last_checkin_date = device_info['approximateLastSignInDateTime']
    device_enrollment_type = device_info['enrollmentType']

    device_os = device_info['operatingSystem']
    # Right here, device will have
    match device_os:
        # This means, that MacOS device is not managed by organisation and couldn't participate in Pilot groups
        case "MacOS":
            return None
        # This means, that MacOS device is managed by organisation
        case "MacMDM":
            device_type = "Computer"
            device_enrollment_type = "Mac MDM"
            device_group = "Mac MDM"
        # This means, that iOS device is managed by organisation
        case "iOS":
            device_type = "iPhone"
            device_enrollment_type = "MAM"
            device_group = "iPhone MAM"

        case "IPad":
            # This means, that iOS device isn't managed by organisation
            if device_enrollment_type is None:
                return None

            device_type = "iPad"
            device_enrollment_type = "MDM"
            device_group = "iPad MDM"

        case "IPhone":
            # This means, that iOS device isn't managed by organisation
            if device_enrollment_type is None:
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
            # This means, that Windows device isn't managed by organisation
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

            if device_enrollment_type is None:
                device_enrollment_type = "MAM"
                device_group = "Android MAM"
            else:
                device_enrollment_type = "MDM"
                device_group = "Android MDM"

    # Creating Device object after assigning groups and properties
    device = Device(
        id=device_info['id'],
        affected=device_affected,
        name=device_info['displayName'],
        group=device_group,
        enrollment_type=device_enrollment_type,
        os=device_os,
        type=device_type,
        last_checkin_date=device_last_checkin_date
    )

    return device


def get_data_from_json(users: typing.Dict, affected: typing.Dict) -> typing.Dict[str, Department]:
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
        # If user has no devices, this user will be skipped
        if not user_info['devices']:
            continue
        # If user's job title from VIP list, user will be skipped
        if is_vip(user_info['jobTitle']):
            continue

        user_id = user_info['id']
        user_affected = ""

        # If user participates in current Pilot group he will be marked as 'Affected user'
        if user_id in affected[0]:
            user_affected = affected[0][user_id]

        user = User(
            id=user_id,
            affected=user_affected,
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
        # Reading user's devices data
        for device_record in user_info['devices']:
            device_affected = ""
            device_id = device_record['id']
            # If user's device participates in current Pilot group he will be marked as 'Affected deivce'
            if device_id in affected[1]:
                device_affected = affected[1][device_id]

            device = create_device(device_record, device_affected)
            if device is None:
                continue
            user.add_device(device)

        department_name = user_info['department']

        # If Department object was created earlier, User object will be added in it's user_list
        if department_name in department_map:
            department_map[department_name].add_user(user)
        # If Department object wasn't created, it will be created with current User object inside of user_list
        else:
            department_map[department_name] = Department(
                name=department_name,
                user_list=[user]
            )

    return department_map
