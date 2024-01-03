from flask import *
from markupsafe import escape
from users import *
import secrets
import hashlib
from queries import *

load_user()

app = Flask("admission_simulator")

@app.route("/", methods = ['GET'])
def hello_world():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None:
        return redirect('/login')

    if check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('dashboard/admin/enroll_plan')
    
    if check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'user'):
        return redirect('/dashboard/user')
    return redirect('/login')

@app.route("/login",methods = ['GET'])
def login_page():
    return render_template('login.html')

@app.route("/login",methods = ['POST'])
def login():
    user = request.form.get('user')
    passwd = request.form.get('pass')
    try:
        if user == 'admin' and passwd == ADMIN_PASSWORD_HASH:
            resp = redirect('dashboard/admin/enroll_plan')
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

@app.route("/logout",methods = ['GET'])
def logout():
    resp = redirect('/login')
    resp.delete_cookie('session')
    resp.delete_cookie('expire')
    return resp

@app.route("/dashboard/admin/enroll_plan")
def admin_enrollplain():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    

    data_tables = []
    ft = get_faculties_table()
    st = {}
    st['P'] = '物理'
    st['H'] = '历史'
    st['C'] = '化学'
    st['B'] = '生物'
    st['O'] = '政治'
    st['G'] = '地理'
    st[None] = '无'
    db = get_admin_connection()
    cursor = db.cursor()

    cursor.execute("SELECT m_id,m_name,m_max_enroll,m_faculty,m_group,m_primary,m_secondary FROM majors")

    for i in cursor.fetchall():
        
        rows = (i[0],i[1], i[2],ft[i[3]],i[4],st[i[5]],st[i[6]])
        if i[2] == None:
            rows = (i[0],i[1], '参照国家计划',ft[i[3]],i[4],st[i[5]],st[i[6]])

        data_tables.append(rows)
    
    cursor.close()
    db.close()

    
    resp = make_response(render_template('enroll_plan.html',table_data = data_tables))
    session, expire = issue_session('admin')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp



































@app.route("/dashboard/user")
def hello_user():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'user'):
        return redirect('/login')
    return f"Hello, user!"


































if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)