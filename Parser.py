from Data import *

def parse_datatable(spreadsheet, department_list, user_list, device_list):
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
            devices = [device]
            user = User(name=user_name, manager=user_manager,
                        job_title=user_job_title, location=user_location, device_list=devices)
            user_list[user.name] = user

            if department_name in department_list:
                department_list[department_name].add_user(user)

            else:
                users = [user]
                department = Department(
                    name=department_name, cost_center=department_cost_center, user_list=users)
                department_list[department_name] = department