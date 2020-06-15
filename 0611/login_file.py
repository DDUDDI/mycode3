# user.txt 파일에 회원의 id, passwword 5개를 저장하고
# 로그인 폼을 이용하여 로그인 화면 서버측의 users.txt 파일에 있는 명단을 참조하여 인증을 거친 후
# 이용자의 화면에 'xxx님 환영합니다'
# 혹은 '회원 가입하신 후 사용해주세요'라는 메세지가 표시되도록 한다.

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
    return render_template('login.html')

@app.route('/user/flogin', methods=['POST'])
def userlogin():
    usr = request.form
    msg = '회원가입 후 사용해주세요.'
    uid = usr['uid']
    login = authenticate(usr)
    if login:
        msg = f'{uid}님 환영합니다'
        return msg
    return msg
