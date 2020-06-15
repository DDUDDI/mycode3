# 로그인한 사용자만 멤버 추가할 수 있도록 session 사용하기

import json
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
# secretkey 설정
app.config['SECRET_KEY'] = 'This is secret key'
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


def add_user(data):
    result = False
    with open(filepath, mode='a') as f:
        f.write(f"{data['uid']} {data['upwd']}\n")
        result = True


@app.route('/')
def view_form():
    return render_template('login_session.html')


@app.route('/user/jlogin', methods=['POST'])
def userlogin():
    usr = request.form
    # string -> json #
    dic = {}
    dic['ok'] = False
    uid = usr['uid']
    login = authenticate(usr)
    if login:
        dic['ok'] = True
        '''
        # session class로 생성한 dic은 다른 페이지, 기능을 요청하더라도 유효함 #
        session['uid'] = usr['uid']

        # 위의 과정이 없으면 uid key가 없기 때문에 error 발생
        print(session['uid'])

        # uid key를 설정 안했을 때 error 없이 볼 수 있는 방법, 알아서 error 처리
        # return none이면 login 안한 것 -> login form으로 redirect해서 보내기
        session.get('uid')
        '''
    return json.dumps(dic) # json.dumps(): json 읽고 데이터 쓰기

@app.route('/user/add', methods=['POST', 'GET'])
def user_add():
    if not session.get('uid'):
        return redirect('/user/jlogin')
    if request.method == 'GET':
        return render_template('user_addform.html')
    else:
        data = request.form
        ok = add_user(data)
        return '사용자 추가 성공' if ok else '사용자 추가 실패'

