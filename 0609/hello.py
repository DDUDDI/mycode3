#/gugu/<int:dan>으로 요청하면 해당 단수의 구구단이 화면에 표시되도록 해보세요.

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/gugu/<int:dan>')
def gugu(dan):
    print(dan, ' 요청함')
    res = ''
    for i in range(1, 10):
        res += f'{dan}*{i}={dan*i} <br>'
    return res