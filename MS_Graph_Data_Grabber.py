import requests
import json
from Entities import *
from JSON_Parser import *
from Random_Device_Selector import *


def user_to_json_grabbing(headers, params):
    all_users = []

    office_locations = params['office_locations']

    for office_location in office_locations:
        next_link = r"https://graph.microsoft.com/v1.0/users?$count=true&$filter=officeLocation+eq+'" + office_location + \
            r"'+and+onPremisesExtensionAttributes/extensionAttribute11+eq+'Employee'+and+accountEnabled+eq+true&$select=id,displayName,mail,jobTitle,officeLocation,department"
        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_users += json_data['value']
            next_link = json_data.get("@odata.nextLink")

    for user in all_users:
        if user.get('id'):
            manager_url = r'https://graph.microsoft.com/v1.0/users/' + \
                user["id"]+r'/manager?$select=displayName,mail'
            manager_response = requests.get(manager_url, headers=headers)
            manager_data = manager_response.json()
            user['manager_name'] = manager_data.get('displayName')
            user['manager_mail'] = manager_data.get('mail')

    return all_users


def device_to_json_grabbing(headers, params):
    all_devices = []

    naming_tags = params['naming_tags']
    for naming_tag in naming_tags:
        next_link = r"https://graph.microsoft.com/beta/deviceManagement/managedDevices?$filter=startswith(devicename,'"+naming_tag + \
            r"')&select=devicename,userid,azureActiveDirectoryDeviceId,deviceEnrollmentType,operatingSystem,usersLoggedOn"

        while next_link:
            response = requests.get(next_link, headers=headers)
            json_data = response.json()
            all_devices += json_data['value']
            next_link = json_data.get("@odata.nextLink")

    return all_devices
