from flask import *
from markupsafe import escape
from users import *
import hashlib

app = Flask("admission_simulator")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/success")
def hello():
    return f"Hello, success!"

@app.route("/login",methods = ['GET'])
def login_page():
    return render_template('login.html')

@app.route("/login",methods = ['POST'])
def login():
    user = request.form['user']
    passwd = request.form['pass']
    try:
        if USERS[user] == hashlib.sha512(passwd.encode()).hexdigest():
            resp = redirect('/success')
            resp.set_cookie('hello')
            return resp
    except:
        return redirect('/login')

    return redirect('/login')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)