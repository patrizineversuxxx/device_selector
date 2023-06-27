import time
import requests
from entities import *
from json_parser import *
from random_device_selector import *


def get_users_from_API(headers):
    start = time.time()
    all_users = []
    
    next_link = r"https://graph.microsoft.com/v1.0/users?$count=true&$filter=onPremisesExtensionAttributes/extensionAttribute11+eq+'Employee'+and+accountEnabled+eq+true&$select=id,displayName,mail,jobTitle,officeLocation,department"

    while next_link:
        response = requests.get(next_link, headers=headers)
        json_data = response.json()
        all_users += json_data["value"]
        next_link = json_data.get("@odata.nextLink")

    counter = 0
    user_count = len(all_users)
    persent = user_count/100
    prev_progress = 0

    for user in all_users:
        if user.get('id'):
            manager_url = r'https://graph.microsoft.com/v1.0/users/' + \
                user['id']+r'/manager?$select=displayName,mail'

            manager_response = requests.get(manager_url, headers=headers)
            manager_data = manager_response.json()

            user['manager_name'] = manager_data.get("displayName")
            user['manager_mail'] = manager_data.get("mail")

            devices_url = r'https://graph.microsoft.com/v1.0/users/' + \
                user['id']+r'/ownedDevices?$select=displayName,id,enrollmentType,operatingSystem,' + \
                r'isManaged,approximateLastSignInDateTime,manufacturer,model'

            devices_response = requests.get(devices_url, headers=headers)
            devices_data = devices_response.json()

            user['devices'] = devices_data.get("value")

            counter += 1
            progress = int(counter/persent)

            if (progress > prev_progress):
                prev_progress = progress
                print(prev_progress, r"% completed")

    end = time.time()
    print("Data grabbing completed!", user_count)
    print("Grabbing process took ", end-start)
    print(start)
    print(end)
    return all_users


def get_intune_devices_from_API(headers, naming_tags):
    all_devices = []

    for naming_tag in naming_tags:
        next_link = r"https://graph.microsoft.com/beta/deviceManagement/managedDevices?$filter=startswith(devicename,'"+naming_tag + \
            r"')&select=devicename,userid,azureActiveDirectoryDeviceId,deviceEnrollmentType,operatingSystem,usersLoggedOn"

        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_devices += json_data['value']
            next_link = json_data.get("@odata.nextLink")

    return all_devices
