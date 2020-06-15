# user.txt 파일에 회원의 id, passwword 5개를 저장하고
# 로그인 폼을 이용하여 로그인 화면 서버측의 users.txt 파일에 있는 명단을 참조하여 인증을 거친 후
# 이용자의 화면에 'xxx님 환영합니다'
# 혹은 '회원 가입하신 후 사용해주세요'라는 메세지가 표시되도록 한다.

from flask import Flask, request, render_template

app = Flask(__name__)
filepath = r'C:\PythonWeb\venv\users.txt'


def authenticate(str):
    res = False
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            sp = line.split()
            if str['uid'] == sp[0] and str['upwd'] == sp[1]:
                return True
        return res


@app.route('/')
def view_form():
    return render_template('review_login_file.html')


@app.route('/user/flogin', methods=['POST'])
def login():
    str = request.form
    msg = '회원 가입 후 사용해주세요.'
    uid = str['uid']
    ok = authenticate(str)
    if ok:
        msg = f'{uid}님 환영합니다.'
        return msg
    return msg