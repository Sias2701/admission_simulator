from flask import *
from markupsafe import escape
from users import *
import secrets
import hashlib

load_user()

app = Flask("admission_simulator")

@app.route("/", methods = ['GET'])
def hello_world():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None:
        return redirect('/login')

    if check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/dashboard/admin')
    
    if check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'user'):
        return redirect('/dashboard/user')
    return redirect('/login')

@app.route("/dashboard/admin")
def hello_admin():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    return f"Hello, admin!"
@app.route("/dashboard/user")
def hello_user():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'user'):
        return redirect('/login')
    return f"Hello, user!"

@app.route("/login",methods = ['GET'])
def login_page():
    return render_template('login.html')

@app.route("/login",methods = ['POST'])
def login():
    user = request.form.get('user')
    passwd = request.form.get('pass')
    try:
        if user == 'admin' and passwd == ADMIN_PASSWORD_HASH:
            resp = redirect('/dashboard/admin')
            session, expire = issue_session('admin')
            resp.set_cookie('session', session)
            resp.set_cookie('expire', expire)
            return resp

        if USERS[user] == passwd:
            resp = redirect('/dashboard/user')
            session, expire = issue_session('user')
            resp.set_cookie('session', session)
            resp.set_cookie('expire', expire)
            return resp
        
        return render_template('login.html',error='用户名或密码错误')
    except:
        return render_template('login.html',error='用户名或密码错误')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)