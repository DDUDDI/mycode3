from flask import Flask, render_template, redirect, request, session, send_file
import pymysql
import json
from werkzeug.utils import secure_filename
import os
from os import path
from random import *
from boardclass import Board


app = Flask(__name__)
filepath = r'D:\PythonWeb\users.txt'
# secretkey 설정
app.config['SECRET_KEY'] = 'This is secret key'


# 로그인 기능, 인증받은 사용자만 글쓰기 가능
def authenticate(usr):
    result = False
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select uid, upwd from users'
        curs.execute(sql)
        rows = curs.fetchall()
        for r in rows:
            if usr['uid'] == r['uid'] and usr['upwd'] == r['upwd']:
                return True
        return result
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()



# 업로드한 파일의 이름 중복문제 해결 필요
# 서버에서 파일이 업로드될 때 이미 그 이름을 가진 파일이 있다면 덮어쓰기 된다
# 그러므로 그런 파일이 있는지 확인하여 나중에 업로드된 파일의 이름을 변경해서 저장해야 한다
def file_handler(curs):
    # 파일 여러개 받기 #
    file_dic = request.files.to_dict() # form에서 받은 여러개의 file 정보를 dic 형태로 저장
    upload_cnt = len(file_dic)
    print('업로드 파일 수: ', upload_cnt)
    save_cnt = 0
    try:
        curs.execute('select max(num) curnum from bbs;')
        row = curs.fetchone()
        curnum = row['curnum']
        print('현재 글번호: ', curnum)
        for key in file_dic:
            filename = secure_filename(file_dic[key].filename) # 파일 이름 구하기
            c_filename = filename
            fpath = f'static/attach/{filename}'
            b = path.exists(fpath)
            if b:
                c_filename = changefilename(filename)
                fpath = f'static/attach/{c_filename}'
            file_dic[key].save(fpath)
            fsize = float(os.path.getsize('D:/Pythonweb/'+fpath))
            fsize = fsize / 1024
            sql = 'insert into attach (num, fname, fsize, cfname) values(%s, %s, %s, %s);'
            nrow = curs.execute(sql, (curnum, filename, fsize, c_filename))
            save_cnt += nrow
            print('파일 정보 저장: ', save_cnt)
        if save_cnt == upload_cnt:
            return True
        else:
            return False
    except os.error as e:
        print(e)
        return False

    # 파일 한개 받기
    '''
    f = request.files['file1']
    filename = secure_filename(f.filename) #### 코드가 중복되는 것 같은데 고치는 방법있는지 고민 ####
    c_filename = filename
    fpath = f'static/attach/{filename}'
    b = path.exists(fpath) # 기존 파일이 존재하는지 확인하는 방법
    if b:
        c_filename = changefilename(filename)
        fpath = f'static/attach/{c_filename}'
    f.save(fpath)
    try:
        fsize = float(os.path.getsize('D:/PythonWeb/' + fpath))
        fsize = fsize / 1024 # Kbyte
        curs.execute('select max(num) curnum from bbs;')
        row = curs.fetchone()
        curnum = row['curnum']
        sql = 'insert into attach (num, fname, fsize, cfname) values(%s, %s, %s, %s);'
        curs.execute(sql, (curnum, filename, fsize, c_filename))
        return True
    except os.error as e:
        print(e)
        return False
    '''
    # 게시판 글번호 구하기 다른 코드
    # getnum = '''
    # select auto_increment
    # from information_schema.tables
    # where table_schema = 'test'
    # and table_name = 'bbs';
    # '''
    # num = curs.execute(getnum)


def changefilename(filename):
    filenamesplit = filename.split('.')
    i = randint(1, 1000000)
    c_filename = f'{filenamesplit[0]}_{i}.{filenamesplit[1]}'
    return(c_filename)


def getnickname(uid):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select uid, nickname from users'
        curs.execute(sql)
        rows = curs.fetchall()
        for r in rows:
            if uid == r['uid']:
                nickname = r['nickname']
                return nickname
            else:
                return uid
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


# /bbs/list으로 요청하면
# 글번호, 글제목, 작성자, 작성일을 보여준다
# 한 개의 글에 속한 첨부파일 이름을 모두 표시하기
@app.route('/bbs/list')
def show_list():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = '''
               select b.*, a.fname from bbs b
               left outer join attach a
               on b.num=a.num
               order by b.num desc;'''
        curs.execute(sql)
        rows = curs.fetchall()
        boardnum = 0
        boardlist = []
        for r in rows:
            if r['num'] != boardnum:
                board = Board()
                board.num = int(r['num'])
                board.title = r['title']
                board.author = r['author']
                board.wdate = r['wdate']
                board.hitcnt = int(r['hitcnt'])
                board.fname.append(r['fname'] if r.get('fname') else '')
                boardlist.append(board)
            else:
                boardlist[-1].fname.append(r['fname'] if r.get('fname') else '') # 생각하지 못한 코드
            boardnum = r['num']
        return render_template('board.html', boardlist=boardlist)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


# 글 제목을 클릭하면,
# bbs/read/글번호 요청이 서버로 전달되고,
# 글을 읽을 수 있도록 html 페이지에 보여준다
@app.route('/bbs/read/<int:num>')
def show_content(num):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        ''' 파일 한 개 일 때 코드
        sql = 'select * from bbs where num=%s'
        num = int(num)
        curs.execute(sql, num)
        row = curs.fetchone() # rows = curs.fetchall() >> tuple 반환
        # textbox 내 엔터 출력할 수 있도록 하기
        # content_list = row['content'].split('\n') >> html에서 for 문으로 list출력하고 <br> 붙여줌
        row['content'] = row['content'].replace('\n', '<br/>') # 더 간단
        '''

        # 여러개 파일명 출력 #
        sql = '''
        select b.*, a.fid, a.fname, a.fsize from bbs b
        left outer join attach a
        on b.num=a.num
        where b.num=%s'''
        # curs.execute(sql, num)
        sql = 'call getBoardByNum(%s)'
        curs.execute(sql, num) # stored procedure tests
        rows = curs.fetchall()
        filenamelist = []
        for r in rows:
            filenamelist.append({'fid':r['fid'], 'fname':r['fname']})
        rows[0]['content'] = rows[0]['content'].replace('\n', '<br/>')
        # curs.execute('update bbs set hitcnt=hitcnt+1 where num=%s;', num)  # 조회수 올리기
        conn.commit()
        return render_template('board_content.html', rows=rows[0], filenamelist=filenamelist)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


# 글 읽기 페이지에 [목록보기] [글수정] [글삭제] 기능 연결
# 글 수정(/bbs/edit/글번호)
# - 글 제목, 글 내용만 편집 가능한 폼 안에 보여준다.
@app.route('/bbs/edit/<int:num>')
def edit_content(num):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select * from bbs where num=%s'
        curs.execute(sql, num)
        row = curs.fetchone() # rows = curs.fetchall() >> tuple 반환
        return render_template('board_edit.html', row=row)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


@app.route('/bbs/update', methods=['POST'])
def update_content():
    data = request.form
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'update bbs set title=%s, content=%s where num=%s;'
        title = data['title']
        content = data['content']
        n = curs.execute(sql, (title, content, int(data['num'])))
        if n == 1:
            print('사원정보 변경 성공!!!')
            conn.commit() # 수정된 내용이 적용되도록 함
            return redirect('/bbs/read/'+data['num'])
        else:
            print('변경 오류')
            conn.close()
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


@app.route('/bbs/delete/<int:num>')
def delete_content(num):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql1 = 'delete from bbs where num=%s'
        curs.execute(sql1, int(num))
        conn.commit()
        sql2 = 'select * from bbs'
        curs.execute(sql2)
        rows = curs.fetchall()
        return redirect('/bbs/page/1')
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


@app.route('/bbs/write')
def show_write_content():
    if session.get('uid'):
        return render_template('board_write.html')
    else:
        return redirect('/bbs/page/1')


@app.route('/bbs/insert', methods=['POST'])
def write_content():
    data = request.form
    uid = session.get('uid')
    nickname = getnickname(uid)
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        # bbs 테이블에 글 정보 넣기
        sql = 'insert into bbs (title, author, content) values(%s, %s, %s);'
        curs.execute(sql, (data['title'], nickname, data['content']))
        if not request.files['file1']: # 파일이 없으면 종료
            conn.commit()
        else:
            saved = file_handler(curs)
            if saved:
                conn.commit()
            else:
                conn.rollback()
        return redirect('/bbs/page/1')
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


@app.route('/bbs/search', methods=['POST'])
def select_content():
    data = request.form
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        # \': escape, python의 '문법을 해제시키기 위해
        sql = 'select * from bbs where ' + data['field'] + ' like \'%' + data['keyword'] + '%\''
        curs.execute(sql)
        rows = curs.fetchall()
        return render_template('board.html', rows=rows)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()



# Pagination ver1
# 번호를 클릭할 때마다 /bbs/page/3
'''
@app.route('/bbs/page/<int:num>')
def page(num):
    p2 = num * 5
    p1 = p2 - 4
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute('set @ROWNUM:=0') # 변수 선언할 때는 이 문장을 넣어야 함
        sql = '''
'''     select * from 
        (
            select @ROWNUM:=@ROWNUM+1 RN, b.* from bbs b 
            where (@ROWNUM:=0)=0
        ) b1 
        where RN BETWEEN %s and %s;'''
'''     curs.execute(sql, (p1, p2))
        rows = curs.fetchall()
        print(rows)
        return render_template('board.html', rows=rows)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()
'''

'''
# Pagination ver2: limit
@app.route('/bbs/page/<int:num>')
def page(num):
    p2 = 3
    p1 = num * 3 - 3
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select * from bbs limit %s, %s'
        curs.execute(sql, (p1, p2))
        rows = curs.fetchall()
        print(rows)
        return render_template('board.html', rows=rows)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()
'''

# Pagination ver3: 행번호 이용
@app.route('/bbs/page/<int:num>')
def page(num):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute('set @RN:=0')
        sql = '''
        select * from
        (
            select floor((RN-1)/5+1) page, t1.* from
            (
                select @RN:=@RN+1 RN, b.*, a.fname from bbs b 
                left outer join attach a on b.num=a.num
                where (@RN:=0)=0 order by b.num desc
            ) t1
        ) t2
        where page=%s;'''
        curs.execute(sql, num)
        rows = curs.fetchall()
        boardnum = 0
        boardlist = []
        for r in rows:
            if r['num'] != boardnum:
                board = Board()
                board.num = int(r['num'])
                board.title = r['title']
                board.author = r['author']
                board.wdate = r['wdate']
                board.hitcnt = int(r['hitcnt'])
                board.fname.append(r['fname'] if r.get('fname') else '')
                boardlist.append(board)
            else:
                boardlist[-1].fname.append(r['fname'] if r.get('fname') else '')  # 생각하지 못한 코드
            boardnum = r['num']
        return render_template('board.html', boardlist=boardlist)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()


@app.route('/')
def view_form():
    return render_template('login_session.html')


@app.route('/user/login', methods=['POST'])
def userlogin():
    usr = request.form
    ok = authenticate(usr)
    dic= {}
    if ok:
        dic['ok'] = True
        session['uid'] = usr['uid']
        print(session)
    return json.dumps(dic)



# 로그인 및 글 저장시 session으로부터 작성자 이름 구하여 DB에 저장하기
'''
def session_login():
    data = request.form
    ok = authenticate(data)
    if ok:
        dic['ok'] = True
        session['id'] = data['id']
        # session['id'] # 해당 키에 연결된 값이 없으면 오류 발생
        session.get('id') # 해당 키에 연결된 값이 없으면 None 리턴
'''

'''
if session.get('uid'): # 로그인 했는지 확인
if not session.get('uid'): # 로그인 안했는지 확인
'''

'''
uid = session.get('uid')
sql = 'insert into bbs(author, title, content) values (%s, %s, %s) 
curs.execute(sql, (uid, data['title'], data['content']))
'''


@app.route('/user/logout')
def userlogout():
    session['uid'] = None # 세션에 저장된 이용자의 ID 삭제
    print(session)
    return redirect('/bbs/page/1') # 로그아웃 상태에서도 접속 가능한 페이지로 이동


##############################################################################
@app.route('/bbs/download/<int:fid>')
def download_attach(fid):
    if fid:
        try:
            conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql = 'select * from attach where fid=%s'
            curs.execute(sql, fid)
            row = curs.fetchone()
            filename = row['fname']
            file_name = f"static/attach/{row['cfname']}"
            return send_file(file_name,
                             mimetype=None,
                            attachment_filename=filename,
                            as_attachment=True)
        except pymysql.MySQLError as e:
            print(e)
        finally:
            conn.close()

