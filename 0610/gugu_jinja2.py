# REST 서비스 	예) /gugu/5

# client가 url로 dan 요청
# -> 입력 받은 dan으로 함수 돌림
# -> backend에서 처리한 결과를 html 문서의 '원하는 위치'에 '원하는 형식'으로 출력

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/gugu<int:dan>')
def get_gugu(dan):
    res = []
    for i in range(1, 10):
        res.append(f'{dan} * {i} = {dan*i}')
    return render_template('gugu_rendering.html', dan=dan, res=res)