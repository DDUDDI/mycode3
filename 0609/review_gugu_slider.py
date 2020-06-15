# REST 서비스 예) /gugu/5

# client가 웹브라우저에 출력하고 싶은 단을 입력하면
# 그 값을 server에서 받아서 처리한 후, 구구단을 출력하도록 하라

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/gugu')
def get_gugu():
    return render_template('review_gugu_slider.html')

# /gugu/<int:dan>은 html에서 input한 값에 따라 결정됨
@app.route('/gugu/<int:dan>')
def show_gugu(dan):
    str = ''
    for i in range(1, 10):
        str += f'{dan}*{i}={dan * i} <br>'
    return str