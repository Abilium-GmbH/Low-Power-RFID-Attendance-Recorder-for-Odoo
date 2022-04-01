import xmlrpc.client
from os import environ
class Interpreter():
    
    def __init__(self) -> None:
        url = environ['ODOO_URL']
        user = environ['ODOO_USER']
        self.db = environ['ODOO_DB']
        self.password = environ['ODOO_PASSWORD']
        self.common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url), allow_none=True)
        self.uid = self.common.authenticate(self.db, user, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),
                                                allow_none=True) 

    def get_
