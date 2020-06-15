# /gugu 으로 요청하면 요청 링크(2~9)를 가진 gugu.html으로 응답
# gugu.html 파일이 화면에 보여질 때 링크를 누르면 해당 수의 구구단이 화면에 보이도록 해보세요.

from flask import Flask, render_template
app = Flask(__name__)



@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
    
@app.route('/gugu')
def get_gugu():
    return render_template('gugu_link.html')

@app.route('/gugu/<int:dan>')
def gugu(dan):
    res = ''
    for i in range(1, 10):
        res += f'{dan}*{i}={dan * i} <br>'
    return res
