import xmlrpc.client
import json
from odoo.employee import Employee
from typing import Any 
from datetime import datetime
from os import environ, path
import base64
import cv2

resources = path.join(path.dirname(__file__), "..", "resources")

class Interpreter():
    """
    Interface to interact with an Odoo server (Online or Offline)
    """
    employeeModule= "hr.employee"
    attendanceModule = "hr.attendance"
    
    @staticmethod
    def time() -> str:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self) -> None:
        """
        The connection to Odoo is established here
        """
        url = environ['ODOO_URL']
        user = environ['ODOO_USERNAME']
        self.db = environ['ODOO_DB']
        self.password = environ['ODOO_PASSWORD']
        self.common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url), allow_none=True)
        self.uid = self.common.authenticate(self.db, user, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),
                                                allow_none=True) 

    def execute(self, model_name : str, method_name : str,
                parameters : list, extra_parameters: dict={}) -> Any:
        """
        Executes tasks with the external Odoo API: https://www.odoo.com/documentation/master/developer/misc/api/odoo.html
        """
        return self.models.execute_kw(self.db,
                                      self.uid,
                                      self.password, 
                                      model_name,
                                      method_name,
                                      parameters,
                                      extra_parameters)

    def monthly_hours(self, attendance_ids: list) -> float:
        """
        Sums up the worked hours of an employee in the last month

        Args:
        attendance_ids: A list of attendance ids given by odoo

        Returns:

        Sum of all the worked hours given from the attendance_ids in the current month
        """
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
        """
        Tries to find out which Employee tried to check in or out with a rfid capable token/badge from the barcode saved on token/badge

        Args: 
        barcode: an int saved on a token/badge and stored in Odoo

        Returns: 

        The Employee registered to the barcode

        Raises ValueError if the barcode is unknown
        """
        try:
            found_employee = self.execute(self.employeeModule,
                                          'search_read',
                                          [[['barcode', '=', str(barcode)]]],
                                          {'fields': [
                                                'name'
                                                ,'attendance_state'
                                                ,'attendance_ids'
                                                ,'last_attendance_id'
                                                ,'last_check_in'
                                                ,'hours_today'
                                              ]
                                            }
                                          )[0]
        except IndexError:
            raise ValueError("Bad Badge-id")

        last_attendance = None if not found_employee['last_attendance_id'] else found_employee['last_attendance_id'][0]
            
        return Employee(id= found_employee['id'],
                        name= found_employee['name'],
                        isCheckedOut= ( found_employee['attendance_state'] == 'checked_out'),
                        last_attendance_id= last_attendance,
                        last_check_in= found_employee['last_check_in'],
                        hours_today= found_employee['hours_today'],
                        hours_this_month= self.monthly_hours(found_employee['attendance_ids'])
                        )
    
    def check_in(self, employee: Employee) -> None:
        """
        Checks an employee In on Odoo
        """
        self.execute(self.attendanceModule, 'create',
                     [{'employee_id': employee.id, 'check_in': str(self.time())}])
    
    def check_out(self, employee: Employee) -> None:
        """
        Checks an employee Out on Odoo and updates the hours worked
        """
        try:
            self.execute(self.attendanceModule, 'write',
                     [employee.last_attendance_id, {'check_out': str(self.time())}] )
        except xmlrpc.client.Fault as e:
            pass
        employee.update_hours()
    
    def getLogo(self) -> None:
        """
        Takes the company logo saved in odoo and saves it formated as resizedCompanyLogo.bmp into the resources folder
        """
        unformated = self.execute('res.partner', 'search_read', [[
                                        ['is_company', '=', True],
                                        ['id', '=', 1]
                                   ]],
                                   {    'fields':['image_512']
                                   })           # take the image from odoo
        result = json.dumps(unformated)
        f = open(path.join(resources,"outputLogo.json"), "w")
        f.write(result)
        f.close()
        unf = list(result.split(":"))   #split output 
        b = "\"}]"  #characters to delete
        unf2 = unf[2]   #data with image string
        for char in b:
            unf2 = unf2.replace(char, "")
        unf3 = unf2[1:]
        #imgdata = b'{unf3}'    #doesnt work
        imgdata2 = unf3.encode('utf-8')  # encode the image into utf-8
        with open(path.join(resources,"companyLogo.png"), "wb") as fh:
            fh.write(base64.b64decode(imgdata2)) # decodes it into base64
        self.convertToBW()
        self.resizeImage()

    def convertToBW(self) -> None:
        """
        Convert the logo to black and white
        """
        originalImage = cv2.imread(path.join(resources,"companyLogo.png"))
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(path.join(resources,"BWcompanyLogo.png"), blackAndWhiteImage)

    def resizeImage(self) -> None:
        """
        Resize the image so it can be displayed in odoo
        """
        originalImage = cv2.imread(path.join(resources,"BWcompanyLogo.png"))
        resized = cv2.resize(originalImage, (264,176))
        cv2.imwrite(path.join(resources,"resizedCompanyLogo.bmp"), resized)
