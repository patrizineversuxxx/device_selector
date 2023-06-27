from attr import dataclass


@dataclass
class Device:
    id: str
    name: str
    group: str
    enrollment_type: str
    os: str
    type: str
    last_checkin_date: str


@dataclass
class User:
    id: str
    name: str
    mail: str
    manager_name: str
    manager_mail: str
    job_title: str
    location: str
    cost_center: int
    device_list: list[Device]

    def add_device(self, device: Device):
        self.device_list.append(device)


@dataclass
class Department:
    name: str
    user_list: list[User]

    def add_user(self, user: User):
        self.user_list.append(user)
