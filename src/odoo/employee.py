from dataclasses import dataclass

@dataclass(frozen=True) #like this we don't need a constructor
class Employee():
    id: str
    name: str
    isCheckedOut: bool
    last_attendance_id: str
    hours_today: str
    hours_this_month: float
