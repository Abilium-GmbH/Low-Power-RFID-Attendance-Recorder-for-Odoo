from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass() #like this we don't need a constructor
class Employee():
    id: str
    name: str
    isCheckedOut: bool
    last_attendance_id: str
    hours_today: float
    hours_this_month: float
    last_check_in: str

    def update_hours(self):
        timediff = datetime.now() - datetime.strptime(self.last_check_in,"%Y-%m-%d %H:%M:%S")
        hoursdiff = round( timediff.total_seconds() / 3600) 
        self.hours_this_month += hoursdiff
        self.hours_today += hoursdiff
