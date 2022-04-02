from dataclasses import dataclass

@dataclass #like this we don't need a constructor
class Employee():
    id: str
    name: str
    isCheckedOut: bool
    last_attendance_id: str
