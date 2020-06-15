# jinja2: Python 웹 프레임워크인 Flask에 내장되어 있는 Template 엔진

# client가 url로 dan 요청
# -> server에서 입력 받은 dan으로 함수 돌림(리스트 사용)
# -> backend에서 처리한 결과를 html 문서의 '원하는 위치'에 '원하는 형식'으로 출력

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/gugu<int:dan>')
def show_gugu(dan):
    gugulist = []
    for i in range(1, 10):
        gugu = f'{dan} * {i} = {dan*i}'
        gugulist.append(gugu)
    return render_template('review_gugu_rendering.html', res=gugulist)

# 위의 내용을 jinja2를 통해 웹브라우저에 예쁜 형태로 출력