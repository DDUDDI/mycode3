# Flask와 MySQL 연동
# 로컬 시스템에 있는 MySQL test 데이터베이스에 접속하여
# 임의이 테이블의 전체 내용을 화면에 표시해보세요
# 웹브라우저로 접속했을 때 임의의 테이블의 전체 내용이 화면에 표시되도록 하세요

import pymysql
import sys
from flask import Flask, render_template, request, redirect
from emp import Emp

app = Flask(__name__)
'''
# mysql 연결
def conn_mysql():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        print('MySQL DB에 접속 성공 !!')
        return conn, curs
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()
        return None

# 테이블 출력을 위한 객체 생성
def get_list():
    (conn, curs) = conn_mysql()
    sql = 'select * from emp'
    curs.execute(sql)
    tp = curs.fetchall()
    conn.close()
    if tp:
        emplist = []
        for d in tp:
            emp = Emp()
            emp.empno = int(d['empno'])
            emp.ename = d['ename']
            emp.salary = int(d['salary'])
            emp.deptno = int(d['deptno'])
            emplist.append(emp)
        return emplist
    else:
        return None

'''
@app.route('/mysql/emp/list')
def show_emplist():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='tjoeun', db='test', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'select * from emp'
        curs.execute(sql)
        emplist = curs.fetchall()
        return render_template('mysql_crud.html', emplist=emplist)
    except pymysql.MySQLError as e:
        print(e)
    finally:
        conn.close()