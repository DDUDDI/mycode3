# querystring으로 보내는 방법

# http://127.0.0.1:5000/gg?dan=5
# 위와 같은 주소로 요청하면 화면에 5단이 표시되도록 해보세요.

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/gg')
def show_gugu():
    dan = int(request.args['dan'])
    gugulist = []
    for i in range(1, 10):
        gugu = f'{dan} * {i} = {dan*i}'
        gugulist.append(gugu)
    return render_template('review_gugu_jinja2.html', res=gugulist, dan=dan)
    # list 형태는 웹브라우저로 반환할 수 없음


