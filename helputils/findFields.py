from os import environ
def main():
    import xmlrpc.client
    url = environ['ODOO_URL']
    db = environ['ODOO_DB']
    username = environ['ODOO_USERNAME'] 
    password= environ['ODOO_PASSWORD'] 
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # change the model field to whatever you want to know about
    unformated = models.execute_kw(db, uid, password, 'hr.attendance', 'fields_get', [], ).keys()
    print(type(unformated))

    for i in unformated:
        print(i)
    
if __name__ == "__main__":
    main()
