import json
import openpyxl
from Data import *


def get_data_from_xlsx(spreadsheet, department_list, user_list, device_list):
    for row in spreadsheet.iter_rows(2):

        device_name = row[0].value
        device_group = row[1].value
        device_os = row[2].value
        device_last_checkin_date = row[3].value

        user_name = row[4].value
        user_manager = row[5].value
        user_job_title = row[6].value
        user_location = row[7].value

        department_name = row[8].value
        department_cost_center = row[9].value

        device = Device(name=device_name, group=device_group,
                        os=device_os, last_checkin_date=device_last_checkin_date)
        device_list.append(device)

        if user_name in user_list:
            user_list[user_name].add_device(device)

        else:
            user = User(name=user_name, manager=user_manager,
                        job_title=user_job_title, location=user_location, device_list=[])
            user_list[user.name] = user

            if department_name in department_list:
                department_list[department_name].add_user(user)

            else:
                department = Department(
                    name=department_name, cost_center=department_cost_center, user_list=[])
                department_list[department_name] = department


def open_json(path: str):
    f = open(path)
    records = json.load(f)
    f.close()
    return records


def get_data_from_json(params: dict):
    records = open_json(params['path_user'])

    department_map = {}
    user_map = {}

    for record in records:
        department_map[record['department']] = Department(
            name=record['department'], cost_center=0, user_list=[])

    for record in records:
        user_id = record['id']

        user = User(id=user_id, name=record['displayName'], mail=record['mail'], manager=record['manager'],
                    job_title=record['jobTitle'], location=record['officeLocation'], device_list=[])

        user_map[user_id] = user
        department_map[record['department']].user_list.append(user)

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
                if (device_enrollment_type == "userEnrollment") & (device_os == "Windows"):
                    device_group = "macOS"

        device = Device(id=record['azureActiveDirectoryDeviceId'], name=record['deviceName'], group=device_group,
                        os=device_os, last_checkin_date=device_last_checkin_date)

        device_user_id = record['userId']

        if device_user_id in user_map:
            user_map[device_user_id].device_list.append(device)
        else:
            continue

    return department_map


def save_data_to_xlsx(result_map):
    result_book = openpyxl.Workbook()
    result_sheet = result_book.active

    result_sheet.cell(row=1, column=1, value='devicename')
    result_sheet.cell(row=1, column=2, value='group')
    result_sheet.cell(row=1, column=3, value='os')
    result_sheet.cell(row=1, column=4, value='last_checkin_date')
    result_sheet.cell(row=1, column=5, value='username')
    result_sheet.cell(row=1, column=6, value='manager')
    result_sheet.cell(row=1, column=7, value='job_title')
    result_sheet.cell(row=1, column=8, value='location')
    result_sheet.cell(row=1, column=9, value='department name')
    result_sheet.cell(row=1, column=10, value='cost center')

    row_counter = 2

    for department in result_map.keys():

        department_name = department.name
        cost_center = department.cost_center

        # Iterate over the set of user-device tuples
        for user in result_map[department]:
            device = result_map[department][user]
            device_name = device.name
            group = device.group
            os = device.os
            last_checkin_date = device.last_checkin_date
            username = user.name
            manager = user.manager
            job_title = user.job_title
            location = user.location

            result_sheet.cell(row=row_counter, column=1, value=device_name)
            result_sheet.cell(row=row_counter, column=2, value=group)
            result_sheet.cell(row=row_counter, column=3, value=os)
            result_sheet.cell(row=row_counter, column=4,
                              value=last_checkin_date)
            result_sheet.cell(row=row_counter, column=5, value=username)
            result_sheet.cell(row=row_counter, column=6, value=manager)
            result_sheet.cell(row=row_counter, column=7, value=job_title)
            result_sheet.cell(row=row_counter, column=8, value=location)
            result_sheet.cell(row=row_counter, column=9,
                              value=department_name)
            result_sheet.cell(row=row_counter, column=10,
                              value=cost_center)

            row_counter += 1
    result_book.save(r'C:\KEK\test.xlsx')
