import netifaces

def get_interfaces():

    interfaces = netifaces.interfaces()
    interfaces.remove('lo')

    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs.keys() and 'addr' in addrs[netifaces.AF_INET][0]:
            return addrs[netifaces.AF_INET][0]['addr']
    raise Exception("no internet") # honestly, if this happens you have bigger problems

print(get_interfaces())
