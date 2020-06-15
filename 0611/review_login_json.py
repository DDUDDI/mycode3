# json 데이터 주고 받기


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
    return render_template('review_login_json.html')


# json값을 return 하면 더 효율적인 프로그램을 만들 수 있음
@app.route('/user/jlogin', methods=['POST'])
def userlogin():
    usr = request.form
    dic = {}
    dic['ok'] = False
    ok = authenticate(usr)
    if ok:
        dic['ok'] = True
    # python dictionary -> json string
    return json.dumps(dic) # json.dumps(): python의 객체를 json 문자열로 변환