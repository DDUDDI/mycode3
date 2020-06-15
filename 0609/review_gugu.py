# 링크의 href(QS)	예) <a href='/gugu/5'>구구단 보기</a>
# REST 서비스 	예) /gugu/5

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/gugu')
def get_gugu():
    return render_template('review_gugu.html')


@app.route('/gugu/<int:dan>')
def gugu(dan):
    res = ''
    for i in range(1, 10):
        res += f'{dan}*{i}={dan * i} <br>'
    return res