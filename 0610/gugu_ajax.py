# ajax: 비동기 요청, 새로운 요청을 할 때마다 동기화 X
# html에서 dan 입력
# -> 입력 받은 dan으로 함수 돌림
# -> backend에서 처리한 결과를 html 문서에 출력함

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/gugu')
def get_gugu():
    return render_template('gugu_ajax.html')


@app.route('/gugu/<int:dan>')
def gugu(dan):
    res = ''
    for i in range(1, 10):
        res += f'{dan}*{i}={dan * i} <br>'
    return res
