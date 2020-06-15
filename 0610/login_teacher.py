from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def view_form():
    return render_template('form_teacher.html')

@app.route('/user/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('form_teacher.html')
    elif request.method == 'POST':
        data = request.form
        login = False
        if data['uid'] == 'blake' and data['upwd'] == '1234':
            login = True
        return render_template('result.html', login=login, uid=data['uid'])
    else:
        return render_template('form_teacher.html')

@app.route('/ajax/login', methods=['POST', 'GET'])
def ajaxlogin():
    if request.method == 'POST':
        data = request.form
        msg = '<h3>로그인 실패</h3>'
        if data['uid'] == 'blake' and data['upwd'] == '1234':
            msg = '<h3>로그인 성공</h3>'
    return msg