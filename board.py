# /bbs/list으로 요청하면
# 글번호, 글제목, 작성자, 작성일을 보여준다

from flask import Flask, render_template
import pymysql

app = Flask(__name__)


@app.route('/bbs/list')
def show_list():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjouen', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select num, title, author, wdate from bbs;'
        curs.execute(sql)
        rows = curs.fetchall()
        return render_template('board.html', rows=rows)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()

