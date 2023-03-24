import random
import openpyxl
from Data import *
from Parser import *

path = r'C:\KEK\ID_RANDOM.xlsx'
workbook = openpyxl.load_workbook(path)
spreadsheet = workbook.active


department_list = {}
user_list = {}
device_list = []
target_percent = 0.12
parse_datatable(spreadsheet, department_list, user_list, device_list)

selected_users = []
selected_device_list = []
# selecting needed user count for every department


def check_department_target(department):
    return int(0.12 * len(department.user_list))+1


def select_aad_joined_devices(selected_users):
    aad_joined_devices = [
        device for device in device_list if device.group == 'AAD_Joined']

    selected_aad_joined_devices = random.sample(aad_joined_devices, 45)
    for user in user_list.values():
        for device in user.device_list:
            if device in selected_aad_joined_devices:
                selected_users.append(user)
    return selected_aad_joined_devices


flag = True

while (flag):
    kek = False
    print('again')
    selected_aad_joined_devices = select_aad_joined_devices(selected_users)
    for department in department_list.values():
        target_value = check_department_target(department)
        selected_users_count = 0
        for user in department.user_list:
            if user in selected_users:
                selected_users_count += 1
        if target_value < selected_users_count:
            print(
                r'error selected device count more than 12% in department'+department.name)
            selected_users = []
            kek = True
            break
    if (kek == False):
        flag = False
    else:
        continue


