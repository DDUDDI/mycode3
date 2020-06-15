# 링크의 href(QS)

# /gugu 으로 요청하면 요청 링크(2~9)를 가진 gugu.html으로 응답
# gugu.html 파일이 화면에 보여질 때 링크를 누르면 해당 수의 구구단이 화면에 보이도록 해보세요.

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/gugu')
def get_gugu():
    return render_template('review_gugu_link.html')

# dan을 html의 링크 주소로부터 받아와서 show_gugu 함수의 parameter로 전달
@app.route('/gugu/<int:dan>')
def show_gugu(dan):
    str = ''
    for i in range(1, 10):
        str += f'{dan} * {i} = {dan*i}<br>'
    return str