# ajax: 비동기 요청, 새로운 요청을 할 때마다 동기화 X

# html에서 dan 입력
# -> 입력 받은 dan으로 함수 돌림
# -> backend에서 처리한 결과를 html 문서에 출력함

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/gugu')
def view():
    return render_template('review_gugu_ajax.html')

# ajax로 데이터가 아니라 url을 받아옴!
@app.route('/gugu/<int:dan>')
def gugu(dan):
    res = ''
    for i in range(1, 10):
        res += f'{dan}*{i}={dan * i} <br>' # html코드 있으므로 jquery에서 html 함수 사용
    return res
