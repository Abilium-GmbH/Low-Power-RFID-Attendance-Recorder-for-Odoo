import unittest
from odoo.interpreter import Interpreter


class TestInterpreter(unittest.TestCase):

    def setUp(self) -> None:
        self.interpreter = Interpreter()
        self.get_employee= lambda: self.interpreter.getEmployee(1)

    def test_getEmployee(self):
        e = self.get_employee()
        self.assertEqual('Test',
                         e.name)

    def test_checkincheckout1(self):
        e1 = self.get_employee()
        if e1.isCheckedOut:
            self.interpreter.check_in(e1)
            e2 = self.get_employee()
            assert not e2.isCheckedOut
        else:
            self.interpreter.check_out(e1)
            e2 = self.get_employee()
            assert e2.isCheckedOut
    
    def test_checkincheckout2(self):
        self.test_checkincheckout1()




if __name__ == '__main__':
    unittest.main()
