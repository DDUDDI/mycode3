# client가 웹브라우저에 출력하고 싶은 단을 입력하면
# 그 값을 server에서 받아서 처리한 후, 구구단을 출력하도록 하라

from flask import Flask, render_template
app = Flask(__name__)



@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
    
@app.route('/gugu')
def get_gugu():
    return render_template('gugu_slider.html')

@app.route('/gugu/<int:dan>')
def gugu(dan):
    res = ''
    for i in range(1, 10):
        res += f'{dan}*{i}={dan * i} <br>'
    return res
