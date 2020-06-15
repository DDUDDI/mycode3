# 웹기반 사원정보 텍스트 CRUD
# 1. emps.txt 파일에 사원 3명의 정보를 저장한다
# - 사번, 이름, 부서, 급여, 근무지, 전화, Email
# 2. 브라우저에 /emps/list로 요청하면 사원정보 리스트를 보여준다

from flask import Flask, render_template, request, redirect
from emp import Emp

app = Flask(__name__)
filepath = r'D:\PythonWeb\emps.txt'

# text file에 저장된 emp 정보를 라인별로 리스트에 저장
# -> 저장된 내용을 split해서 index로 접근할 수 있도록 함
# -> emp 객체를 생성하고 index를 사용해 리스트에 저장된 정보를 객체의 argument로 입력
# -> 생성된 emp 객체를 emplist에 추가

def getlist():
    with open(filepath) as f:
        lines = f.readlines()
        emplist = []
        for line in lines:
            empdata = line.split()
            emp = Emp() # 객체 생성
            emp.empno = int(empdata[0])
            emp.ename = empdata[1]
            emp.dept = int(empdata[2])
            emp.sal = int(empdata[3])
            emp.loc = empdata[4]
            emp.tel = empdata[5]
            emp.email = empdata[6]
            emplist.append(emp)
        return emplist


def getinfo(empno):
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            empdata = line.split()
            if int(empdata[0]) == empno:
                emp = Emp()  # 객체 생성
                emp.empno = int(empdata[0])
                emp.ename = empdata[1]
                emp.dept = int(empdata[2])
                emp.sal = int(empdata[3])
                emp.loc = empdata[4]
                emp.tel = empdata[5]
                emp.email = empdata[6]
                return emp


# 선생님 코드
def update(form):
    with open(filepath) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            empdata = lines[i].split()
            if empdata[0] == form['empno']:
                empdata[2] = form['dept']
                empdata[3] = form['sal']
                empdata[4] = form['loc']
                newline = ''
                for n in range(7): # column 갯수
                    newline += empdata[n]+' '
                lines[i] = newline+'\n'
                break
    with open(filepath, mode='w') as f:
        for line in lines:
            f.write(line)


def delete(empno):
    with open(filepath) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            empdata = lines[i].split()
            if empdata[0] == empno:
                del lines[i]
                break
    with open(filepath, mode='w') as f:
        for line in lines:
            f.write(line)


'''
# 아래 코드 선생님 코드보고 효율적으로 수정하기
def update(form): # 웹브라우저의 form 정보를 받아서
    emplist = getlist()
    for emp in emplist:
        if emp.empno == int(form['empno']):
            emp.ename = form['ename']
            emp.dept = int(form['dept'])
            emp.sal = int(form['sal'])
            emp.loc = form['loc']
            emp.tel = form['tel']
            emp.email = form['email']
    writeinfo(emplist)
    return form['empno']

# 파일 새로 쓰기
def writeinfo(emplist):
    with open(filepath, 'w') as f:
        for emp in emplist:
            # 아래 코드 선생님 코드보고 효율적으로 수정하기
            line = f'{emp.empno} {emp.ename} {emp.dept} {emp.sal} {emp.loc} {emp.tel} {emp.email}'
            f.write(line+'\n')
'''


@app.route('/emp/list')
def show_emplist():
    emplist = getlist()
    return render_template('emps_file_crud.html', emplist=emplist)


@app.route('/emp/info/<int:empno>')
def show_empinfo(empno):
    emp = getinfo(empno)
    return render_template('emp_info.html', emp=emp)


@app.route('/emp/edit/<int:empno>')
def edit_empinfo(empno):
    emp = getinfo(empno)
    return render_template('emp_edit.html', emp=emp)


@app.route('/emp/update', methods=['POST'])
def update_empinfo():
    form = request.form
    update(form)
    #return render_template('emp_update.html', empno=empno, emplist=emplist)
    return redirect('/emp/info/{}'.format(form['empno']))


@app.route('/emp/delete/<empno>') # empno: int로 받으면 안됨
def delete_empinfo(empno):
    delete(empno)
    return redirect('/emp/list')