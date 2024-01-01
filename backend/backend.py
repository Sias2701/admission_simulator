from datetime import timedelta
from pickle import TRUE
import pyodbc
from flask import Flask, flash, redirect, request, jsonify
from flask_jwt_extended import *
from flask_login import *
from flask_cors import CORS
import hashlib
import pandas as pd
import calendar
import glob
import os

admin_passwaord = '123456'

users = {}

users_file = pd.read_csv('user.csv')
for _, row in users_file.iterrows():
    users[row['username']] = hashlib.sha512(row['password'].encode()).hexdigest()

app = Flask(__name__)
CORS(app, resources = '/*')

# token相关配置 #
app.config["JWT_SECRET_KEY"] = 'secret_key'
app.config["JWT_SECRET_KEY"] = timedelta(hours = 1)
app.config["JWT_SECRET_KEY"] = timedelta(days = 30)
jwt = JWTManager(app)

def get_connect(USERNAME, PASSWORD):
    SERVER = '172.16.50.128'
    DATABASE = 'adminssion'
    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    return connectionString

@app.route('/login', methods = ['POST'])
def login():
    username = request.json.get('username', None)
    password  = request.json.get('passward', None)
    users_file = pd.read_csv('user.csv')
    for _, row in users_file.iterrows():
        if(username == row['username'] and password == row['password']):
            access_token = create_access_token(identity = username)
            return jsonify(access_token)
    return jsonify({"msg": "用户名或密码错误"}), 401

@app.route('/register', methods = ['POST'])
def register():
    global users
    users.clear()
    username = request.json.get('username', None)
    password  = request.json.get('passward', None)
    if(username != 'admin' or password != admin_passwaord):
        return jsonify({"msg": "管理员身份认证错误"}), 401
    while(TRUE):
        register_name = request.json.get('register_name', None)
        register_password = request.json.get('register_password', None)
        users_file = pd.read_csv('user.csv')
        for _, row in users_file.iterrows():
            if(register_name == row['username']):
                flash('该用户名已存在，请更换')
                return redirect(url)

def check_file(file, connectionString): #检查文件是否按照格式填写
    try:
        file_table = pd.read_csv(file)
        valid_col = ["c_id", "c_score", "c_rank", "c_adjust", "c_type", "c_primary", "c_secondary", "c_group", "c_enroll1", "c_enroll2", "c_enroll3", "c_enroll4", "c_enroll5", "c_enroll6"]
        valid_cnt = 0
        for i in valid_col:
            if i in file_table.columns.tolist():
                valid_cnt += 1
        if valid_cnt != len(valid_col):
            raise Exception("csv文件格式错误")
        db = pyodbc.connect(connectionString) #检查是否连接
        for _, row in file_table.iterrows():
            try:
                SQL_QUERY = f"insert into candidates 
                (c_id, c_score, c_rank, c_adjust, c_type, c_primary, c_secondary, c_group, c_enroll1, c_enroll2, c_enroll3, c_enroll4, c_enroll5, c_enroll6) 
                values ([{row['c_id']}], [{row['c_score']}], [{row['c_rank']}], [{row['c_adjust']}], [{row['c_type']}], [{row['c_primary']}], [{row['c_secondary']}], [{row['c_group']}],
                [{row['c_enroll1']}], [{row['c_enroll2']}], [{row['c_enroll3']}], [{row['c_enroll4']}], [{row['c_enroll5']}], [{row['c_enroll6']}])"
            except:
                pass
            pass
    except Exception as e:
        print(str(e))
        pass

@app.route('/administrator/update', methods = ['POST'])
def get_file(db): #文件上传
    temp_file = request.files.get('file')
    if(temp_file is None):
        return 3 #文件上传失败
    check_file(temp_file)
    return check_file(temp_file)

@app.route('administrator/inquire', methods = ['POST'])
def admin_inquire(db): #文件查询
    

@app.route('/administrator', methods = ['POST'])
def admin_operate(): 
    if(request.method == "POST"):
        op = request.form.get('chooice')
        if(op == 1): #上传文件操作
            get_file()
        elif(op == 2): #查询操作
            

@app.route('/teacher', methods = ['POST'])
def teacher_operate():
    if(request.method == "POST"):
        op_num1 = request.form.get('academy') #返回院校代码
        op_num2 = request.form .get('sp_num') #返回专业代码