# 로그인폼에서 로그인을 수행하면 그 결과가 새로운 창에 표시되는 것이 아니라
# 현재의 로그인 폼의 상단에 로그인 성공/실패 여부가 표시되도록 한다.
# jQuery AJAX를 통한 비동기 로그인 기능 작성
# - 로그인 실패시 적색으로 경고 표시
# - 로그인 성공시 google.com으로 이동

from flask import Flask, render_template, request

app = Flask(__name__)
filepath = r'/users.txt'

def authenticate(str):
    result = False
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            data = line.split()
            if str['uid'] == data[0] and str['upwd'] == data[1]:
                return True
        return result

@app.route('/')
def show_form():
    return render_template('review_login_file_ajax.html')


@app.route('/ajax/login', methods=['POST'])
def login():
    usr = request.form
    ok = authenticate(usr)
    msg = '로그인 실패'
    if ok:
        msg = '로그인 성공'
        return msg
    return msg
