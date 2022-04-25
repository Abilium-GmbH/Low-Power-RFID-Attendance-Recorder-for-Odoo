import xmlrpc.client
from .employee import Employee
from typing import Any 
from datetime import datetime
from os import environ

class Interpreter():
    employeeModule= "hr.employee"
    attendanceModule = "hr.attendance"
    
    @staticmethod
    def time() -> str:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self) -> None:
        url = 'https://rostmytomato.odoo.com'#environ['ODOO_URL']
        user = 'autorfidcard@informee.ch'#environ['ODOO_USERNAME']
        self.db = 'rostmytomato'#environ['ODOO_DB']
        self.password = 'DVAMavtVhIOIvWfIU66d'#environ['ODOO_PASSWORD']
        self.common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url), allow_none=True)
        self.uid = self.common.authenticate(self.db, user, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),
                                                allow_none=True) 

    def execute(self, model_name : str, method_name : str,
                parameters : list, extra_parameters: dict={}) -> Any:

        return self.models.execute_kw(self.db,
                                      self.uid,
                                      self.password, 
                                      model_name,
                                      method_name,
                                      parameters,
                                      extra_parameters)

    def monthly_hours(self, attendance_ids: list) -> float:
        time_query = datetime.now().strftime('%Y-%m-%')
        unprocessed_attendances = self.execute(self.attendanceModule,
                                   'search_read',
                                   [[
                                        ['id', 'in', attendance_ids], 
                                        ['write_date','like',time_query]
                                   ]],
                                   {'fields':['worked_hours']}
                                )
        return sum(attendance['worked_hours'] for attendance in unprocessed_attendances)
    
    def getEmployee(self, barcode : int) -> Employee:
        try:
            found_employee = self.execute(self.employeeModule,
                                          'search_read',
                                          [[['barcode', '=', str(barcode)]]],
                                          {'fields': [
                                                'name'
                                                ,'attendance_state'
                                                ,'attendance_ids'
                                                ,'last_attendance_id'
                                                ,'hours_today'
                                              ]
                                            }
                                          )[0]
        except IndexError:
            raise ValueError("Bad Badge-id")

        return Employee(id= found_employee['id'],
                        name= found_employee['name'],
                        isCheckedOut= ( found_employee['attendance_state'] == 'checked_out'),
                        last_attendance_id= found_employee['last_attendance_id'][0],
                        hours_today= found_employee['hours_today'],
                        hours_this_month= self.monthly_hours(found_employee['attendance_ids'])
                        )
    
    def check_in(self, employee: Employee) -> None:
        self.execute(self.attendanceModule, 'create',
                     [{'employee_id': employee.id, 'check_in': str(self.time())}])
    
    def check_out(self, employee: Employee) -> None:
        try:
            self.execute(self.attendanceModule, 'write',
                     [employee.last_attendance_id, {'check_out': str(self.time())}] )
        except xmlrpc.client.Fault:
            pass
    
