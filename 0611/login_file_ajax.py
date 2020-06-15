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

# 로그인폼에서 로그인을 수행하면 그 결과가 새로운 창에 표시되는 것이 아니라
# 현재의 로그인 폼의 상단에 로그인 성공/실패 여부가 표시되도록 한다.
# jQuery AJAX를 통한 비동기 로그인 기능 작성
# - 로그인 실패시 적색으로 경고 표시
# - 로그인 성공시 google.com으로 이동

@app.route('/ajax/login', methods=['POST'])
def ajaxlogin():
    msg = '로그인 실패'
    usr = request.form
    login = authenticate(usr)
    if login:
        msg = '로그인 성공'
    return msg # return 값은 string으로! boolean X

