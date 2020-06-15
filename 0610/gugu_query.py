# querystring으로 보내는 방법

# http://127.0.0.1:5000/user?id=jone&pass=1234
# 위와 같은 주소로 요청을 할 때 전달되는 query String은
# 서버측에서 request.args로 수신할 수가 있다
# 서버측 콘솔에 request.args 값을 표시해서 확인해보세요.

from flask import Flask, render_template, request

app = Flask(__name__)

# http://127.0.0.1:5000/gg?dan=5
# 위와 같은 주소로 요청하면 화면에 5단이 표시되도록 해보세요.
@app.route('/gg')
def get_gugu():
    dan = int(request.args['dan'])
    res = []
    for i in range(1, 10):
        res.append(f'{dan} * {i} = {dan*i}')
    return render_template('gugu_rendering.html', dan=dan, res=res)