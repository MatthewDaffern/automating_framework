from pythonping import ping
from itertools import filterfalse

def ping_test(address):
    result = ping(address, timeout=1, count=2)
    if 'Reply' in list(result)[0]:
        return True
    return False