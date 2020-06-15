# querystring으로 보내는 방법

# http://127.0.0.1:5000/user?id=jone&pass=1234
# 위와 같은 주소로 요청을 할 때 전달되는 query String은
# 서버측에서 request.args로 수신할 수가 있다
# 서버측 콘솔에 request.args 값을 표시해서 확인해보세요.

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/user')
def get_query():
    str = request.args # 주소로 요청한 query string 받음
    # query string은 dic 형태로 전달되므로
    id = str['id']
    pwd = str['pass']
    print(id, pwd)
    return str # client의 웹 브라우저에 표시