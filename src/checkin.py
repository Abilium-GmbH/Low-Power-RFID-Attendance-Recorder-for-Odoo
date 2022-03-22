from datetime import datetime
from os import environ

def main():
    import xmlrpc.client
    import json
    url = environ['ODOO_URL']
    db = environ['ODOO_DB']
    username = environ['ODOO_USERNAME'] 
    password= environ['ODOO_PASSWORD'] 
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    time = datetime.utcnow()
    time=  time.strftime("%Y-%m-%d %H:%M:%S")
    print(time)
    unformated = models.execute_kw(db, uid, password, 'hr.attendance', 'create', [{'check_in': str(time)}] )
    result = json.dumps(unformated,indent = 4)
    print(result)

if __name__ == "__main__":
    main()
