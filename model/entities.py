from dataclasses import dataclass, field
from typing import List


@dataclass(unsafe_hash=True)
class Device:
    """
    Represents a device and its attributes.
    """
    id: str = field(hash=True)
    affected: str = field(hash=True)
    name: str = field(hash=True)
    group: str = field(hash=True)
    enrollment_type: str = field(hash=True)
    os: str = field(hash=True)
    type: str = field(hash=True)
    last_checkin_date: str = field(hash=True)


@dataclass(unsafe_hash=True)
class User:
    """
    Represents a user and associated attributes.
    """
    id: str = field(hash=True)
    affected: str = field(hash=True)
    name: str = field(hash=True)
    mail: str = field(hash=True)
    manager_name: str = field(hash=True)
    manager_mail: str = field(hash=True)
    job_title: str = field(hash=True)
    location: str = field(hash=True)
    cost_center: int = field(hash=True)
    device_list: List[Device] = field(default_factory=list, init=True, compare=False, hash=False)

    def add_device(self, device: Device):
        """
        Adds a device to the user's device list.
        """
        self.device_list.append(device)


@dataclass(unsafe_hash=True)
class Department:
    """
    Represents a department and its attributes.
    """
    name: str = field(hash=True)
    user_list: List[User] = field(default_factory=list, init=True, compare=False, hash=False)

    def add_user(self, user: User):
        """
        Adds a user to the department's user list.
        """
        self.user_list.append(user)
