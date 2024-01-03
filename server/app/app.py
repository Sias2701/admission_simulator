from flask import *
from users import *
from queries import *
import pandas as pd
import numpy as np
from tqdm import tqdm

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

@app.route("/dashboard/admin/upload_candidate",methods = ['GET'])
def admin_upload():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    

    resp = make_response(render_template('upload_candidates.html'))
    session, expire = issue_session('admin')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp

@app.route("/dashboard/admin/upload_candidate",methods = ['POST'])
def admin_upload_process():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    try:
        f = request.files['file']
        if f.mimetype != 'text/csv' : raise ValueError
    except ValueError:
        resp = make_response(render_template('upload_candidates.html', error='文件上传失败::格式错误'))
        session, expire = issue_session('admin')
        resp.set_cookie('session', session)
        resp.set_cookie('expire', expire)
        return resp
    except:
        resp = make_response(render_template('upload_candidates.html', error='文件上传失败::未知错误'))
        session, expire = issue_session('admin')
        resp.set_cookie('session', session)
        resp.set_cookie('expire', expire)
        return resp

    try:
        db = get_admin_connection()
        db.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;")
    except:
        db.close()
        resp = make_response(render_template('upload_candidates.html', error='文件上传失败::数据库连接错误'))
        session, expire = issue_session('admin')
        resp.set_cookie('session', session)
        resp.set_cookie('expire', expire)
        return resp
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM accept_enroll;")
        cursor.execute("DELETE FROM reject_enroll;")
        cursor.execute("DELETE FROM candidates;")
        df = pd.read_csv(f,dtype=str)
        df = df.replace(np.nan, None)
        df = df.replace('NULL', None)
        for _, r in tqdm(df.iterrows()):
            id = r["c_id"]
            score = r["c_score"]
            rank = r["c_rank"]
            adjust = r["c_adjust"]
            c_type = r["c_type"]
            primary = r["c_primary"]
            secondary = r["c_secondary"]
            group = r["c_group"]
            enroll1 = r["c_enroll1"]
            enroll2 = r["c_enroll2"]
            enroll3 = r["c_enroll3"]
            enroll4 = r["c_enroll4"]
            enroll5 = r["c_enroll5"]
            enroll6 = r["c_enroll6"]
            cursor.execute("INSERT INTO candidates(c_id, c_score, c_rank, c_adjust, c_type, c_primary, c_secondary, c_group, c_enroll1, c_enroll2, c_enroll3, c_enroll4, c_enroll5, c_enroll6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", id,score,rank,adjust,c_type,primary,secondary,group,enroll1,enroll2,enroll3,enroll4,enroll5,enroll6)

    except Exception as e:
        print(e)
        cursor.rollback()
        db.close()
        resp = make_response(render_template('upload_candidates.html', error='文件上传失败::数据文件错误'))
        session, expire = issue_session('admin')
        resp.set_cookie('session', session)
        resp.set_cookie('expire', expire)
        return resp
    
    cursor.execute("SET NOCOUNT ON; EXEC apply_enroll")
    cursor.commit()
    db.close()
    resp = make_response(render_template('upload_candidates.html', msg='文件上传成功'))
    session, expire = issue_session('admin')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp

@app.route("/dashboard/admin/admission_result")
def admin_admission_result():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')

    data_tables = []
    st = {}
    st['Y'] = '是'
    st['N'] = '否'
    db = get_admin_connection()
    cursor = db.cursor()

    cursor.execute("SELECT c_id, c_group, c_major_name, c_score, c_rank, c_adjust from final_enroll_view_all_n")
    for i in cursor.fetchall():
        rows = (i[0], i[2], i[1], i[3], i[4], st[i[5]])
        data_tables.append(rows)

    cursor.close()
    db.close()

    resp = make_response(render_template('admission_result.html', table_data = data_tables))
    session, expire = issue_session('admin')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp

@app.route("/dashboard/admin/reject_enroll")
def admin_reject_enroll():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    
    data_tables = []
    db = get_admin_connection()
    cursor = db.cursor()
    cursor.execute("SELECT c_id, reject_term from reject_enroll")
    for i in cursor.fetchall(): 
        rows = (i[0], i[1].strip())
        data_tables.append(rows)

    cursor.close()
    db.close()

    resp = make_response(render_template('reject_enroll.html', table_data = data_tables))
    session, expire = issue_session('admin')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp

@app.route("/dashboard/admin/adjustment_enroll")
def admin_adjustment_enroll():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    
    data_tables = []
    db = get_admin_connection()
    cursor = db.cursor()

    cursor.execute("SELECT c_id, c_group, c_major_name, c_score, c_rank from final_accept_adjust_n")
    for i in cursor.fetchall():
        rows = (i[0], i[2], i[1], i[3], i[4])
        data_tables.append(rows)

    cursor.close()
    db.close()

    resp = make_response(render_template('adjustment_enroll.html', table_data = data_tables))
    session, expire = issue_session('admin')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp


@app.route("/dashboard/admin/static")
def admin_static():
    iv = request.cookies.get('session')
    ct = request.cookies.get('expire')
    if iv == None or ct == None or not check_session(bytes.fromhex(iv), bytes.fromhex(ct), 'admin'):
        return redirect('/login')
    
    data_table1 = []
    data_table2 = []
    data_table3 = []
    db = get_admin_connection()
    cursor = db.cursor()

    cursor.execute("EXEC accept_list_stat_all")
    for i in cursor.fetchall():
        rows = (i[0], i[1], i[2], i[3], i[4], i[5])
        data_table1.append(rows)

    cursor.execute("SELECT faculty_id, faculty_name, max_score, min_score, max_rank, min_rank, avg_score FROM accept_list_stat_faculty")
    for i in cursor.fetchall():
        rows = (i[0], i[1], i[2], i[3], i[6], i[4], i[5])
        data_table2.append(rows)

    cursor.execute("SELECT m_id, m_name, max_score, min_score, max_rank, min_rank, avg_score FROM accept_list_stat_major")
    for i in cursor.fetchall():
        rows = (i[0], i[1], i[2], i[3], i[6], i[4], i[5])
        data_table3.append(rows)

    cursor.close()
    db.close()

    resp = make_response(render_template('static.html', table_data1 = data_table1, table_data2 = data_table2, table_data3 = data_table3))
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
    
    data_table1 = []
    data_table2 = []
    data_table3 = []
    db = get_user_connection()
    cursor = db.cursor()

    cursor.execute("EXEC accept_list_stat_all")
    for i in cursor.fetchall():
        rows = (i[0], i[1], i[2], i[3], i[4], i[5])
        data_table1.append(rows)

    cursor.execute("SELECT faculty_id, faculty_name, max_score, min_score, max_rank, min_rank, avg_score FROM accept_list_stat_faculty")
    for i in cursor.fetchall():
        rows = (i[0], i[1], i[2], i[3], i[6], i[4], i[5])
        data_table2.append(rows)

    cursor.execute("SELECT m_id, m_name, max_score, min_score, max_rank, min_rank, avg_score FROM accept_list_stat_major")
    for i in cursor.fetchall():
        rows = (i[0], i[1], i[2], i[3], i[6], i[4], i[5])
        data_table3.append(rows)

    resp = make_response(render_template('user_static.html', table_data1 = data_table1, table_data2 = data_table2, table_data3 = data_table3))
    session, expire = issue_session('user')
    resp.set_cookie('session', session)
    resp.set_cookie('expire', expire)
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)