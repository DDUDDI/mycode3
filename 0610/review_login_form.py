# form을 통해 전송

# 아이디가 blake이고 암호가 1234인 경우에
# 로그인 성공 메세지가 웹브라우저 화면이 표시되도록 해보세요.
# 그 외에는 로그인 실패

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def view_form():
    return render_template('review_login_form.html')

@app.route('/user/login', methods=['post']) # post 방식으로만 받음 Get 방식 X
def get_userinfo():
    # request.form을 통해 client가 form을 통해 전송한 데이터 받음
    msg = '로그인 실패'
    userinfo = request.form
    uid = userinfo['uid']
    upwd = userinfo['upwd']
    if uid == 'blake' and upwd == '1234':
        msg = '로그인 성공'
        return msg
    return msg