# client가 웹 브라우저에서 출력하고 싶은 dan을 선택하면 javascript를 통해 구구단을 출력하라
# server로 요청 X

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/gugu')
def get_gugu():
    return render_template('gugu_range.html')