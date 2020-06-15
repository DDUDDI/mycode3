# 원하는 위치에 file upload를 하기 위한 python 코드

from flask import Flask, render_template, request
# file upload
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    # get: form 전송, post: 파일 수신
    if request.method == 'GET':
        return render_template('fileupload.html')
    if request.method == 'POST':
        f = request.files['file1'] # file1은 html에서 넘어오는 name
        f.save(f'uploads/{secure_filename(f.filename)}') # 보안상 위험한 파일명이 오지 않도록
        return 'File uploaded'
    return 'Error'



# 이용자들이 file list를 볼 수 있어야함
# 올린 날짜, 올린 사람의 id, 파일 크기, 파일 명이 txt 파일에 저장되도록 해보세요
'''
f.mimetype
f.content_type
f.headers
'''