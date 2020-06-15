from flask import Flask
import json

from flask import Flask, render_template, request
app = Flask(__name__)
filepath = r'D:\PythonWeb\users.txt'


def authenticate(usr):
    result = False
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            fdata = line.split()
            if usr['uid'] == fdata[0] and usr['upwd'] == fdata[1]:
                return True
    return result


@app.route('/')
def view_form():
    return render_template('login_json.html')


@app.route('/user/jlogin', methods=['POST'])
def userlogin():
    usr = request.form
    # string -> json #
    dic = {}
    dic['ok'] = False
    # msg = '회원가입 후 사용해주세요.'
    uid = usr['uid']
    login = authenticate(usr)
    if login:
        # msg = f'{uid}님 환영합니다'
        dic['ok'] = True
    return json.dumps(dic) # json.dumps(): json 읽고 데이터 쓰기
