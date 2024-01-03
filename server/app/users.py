import threading
import time
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SECRET_KEY = bytes.fromhex('d8ccb01a0bc2bb2c643a2660aa81d6d8')

USERS_PATH = '../etc/password'

ADMIN_PASSWORD_HASH = open('../etc/admin_password', 'r').read(128)

USERS = {}

USER_LOCK = threading.Lock()

SESSIONS = {}

SESSION_LOCK = threading.Lock()

EXPIRE_DELTA = 300000000000

def load_user():
    USER_LOCK.acquire()
    dat = open(USERS_PATH).readlines()
    global USERS
    USERS.clear()
    for d in dat:
        k, v = d.split(':')
        USERS[k] = v
    USER_LOCK.release()

def save_user():
    USER_LOCK.acquire()
    global USERS
    f = open(USERS_PATH,'w')
    for k in USERS:
        f.write(f"{k}:{USERS[k]}\n")
    f.close()
    USER_LOCK.release()

def issue_session(user_type):
    iv = secrets.token_bytes(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    info = pad(f'{user_type}:{str(time.clock_gettime_ns(0) + EXPIRE_DELTA)}'.encode(), 16)

    session = iv.hex(), cipher.encrypt(info).hex()

    return session

def check_session(iv, ciphertext, target_type):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    info = unpad(cipher.decrypt(ciphertext), 16).decode()
    user_type = info.split(':')[0]
    timestamp = int(info.split(':')[1])
    if timestamp > time.clock_gettime_ns(0) and user_type == target_type:
        return True

    return False
# def add_session(session_id):
#     SESSION_LOCK.acquire()
#     expire = time.clock_gettime_ns(0) + EXPIRE_DELTA
#     global SESSIONS
#     SESSIONS[session_id] = expire
#     SESSION_LOCK.release()
# 
# def update_session(session_id):
#     SESSION_LOCK.acquire()
#     global SESSIONS
# 
#     for k in SESSIONS:
#         if SESSIONS[session_id] < time.clock_gettime_ns(0):
# 
#     try:
#         if SESSIONS[session_id] > time.clock_gettime_ns(0):
#             expire = time.clock_gettime_ns(0) + EXPIRE_DELTA
#             SESSIONS[session_id] = expire
#     except:
#         SESSION_LOCK.release()
#         return False
# 
#     SESSION_LOCK.release()
#     return True
# 
# def drop_session(session_id):
#     SESSION_LOCK.acquire()
#     global SESSIONS
#     try:
#         SESSIONS.pop(session_id)
#     except:
#         SESSION_LOCK.release()
# 
#     SESSION_LOCK.release()