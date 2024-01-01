
USERS_PATH = '../etc/password'

ADMIN_PASSWORD_HASH = open('../etc/admin_password', 'r').read(128)



def load_user():
    dat = open(USERS_PATH).readlines()
    ret = {}
    for d in dat:
        k, v = d.split(':')

        ret[k] = v
    return ret

def save_user():
    pass

USERS = load_user()