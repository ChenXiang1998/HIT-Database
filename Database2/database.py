import MySQLdb


connect = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='******',
    db='COMPANY',
    charset='utf8'
)
cur = connect.cursor()


def query(number, *args):
    if number == 1:
        pno = args[0]
        sql = 'select distinct ESSN from WORKS_ON where PNO = \'{pno}\''.format(pno=pno)
        a1 = cur.execute(sql)
        info = cur.fetchmany(a1)
        print('参加了项目编号为{pno}的项目的员工编号如下：'.format(pno=pno))
        for i in info:
            for j in i:
                print(j)

    elif number == 2:
        pname = args[0]
        sql = 'select distinct ENAME from EMPLOYEE natural join WORKS_ON natural join PROJECT where PNAME = \'{pname}\''.format(pname=pname)
        a2 = cur.execute(sql)
        info = cur.fetchmany(a2)
        print('参加了项目名为{pname}的项目的员工名字如下：'.format(pname=pname))
        for i in info:
            for j in i:
                print(j)

    elif number == 3:
        dname = args[0]
        sql = 'select distinct ENAME, ADDRESS from EMPLOYEE natural join DEPARTMENT where DNAME = \'{dname}\''.format(dname=dname)
        a3 = cur.execute(sql)
        info = cur.fetchmany(a3)
        print('在{dname}部门工作的员工名和地址如下：'.format(dname=dname))
        for name, address in info:
            print(name, address)

    elif number == 4:
        dname = args[0]
        salary = args[1]
        sql = 'select distinct ENAME, ADDRESS from EMPLOYEE natural join DEPARTMENT where DEPARTMENT.DNAME = \'{dname}\' and EMPLOYEE.SALARY < {salary}'.format(dname=dname, salary=salary)
        a4 = cur.execute(sql)
        info = cur.fetchmany(a4)
        print('在{dname}部门工作且工资低于{salary}的员工名和地址如下：'.format(dname=dname, salary=salary))
        for name, address in info:
            print(name, address)

    elif number == 5:
        pno = args[0]
        sql = 'select distinct ENAME from EMPLOYEE natural join WORKS_ON where PNO <> \'{pno}\''.format(pno=pno)
        a5 = cur.execute(sql)
        info = cur.fetchmany(a5)
        print('没有参加项目编号为{pno}的员工姓名如下：'.format(pno=pno))
        for i in info:
            for j in i:
                print(j)

    elif number == 6:
        ename = args[0]
        sql = 'select EMPLOYEE.ENAME,DNAME from EMPLOYEE natural join DEPARTMENT join EMPLOYEE as LEADER on EMPLOYEE.SUPRESSN = LEADER.ESSN and EMPLOYEE.ESSN <> LEADER.ESSN where LEADER.ENAME = \'{ename}\''.format(ename=ename)
        a6 = cur.execute(sql)
        info = cur.fetchmany(a6)
        print('由{ename}领导的工作人员姓名、所在部门名字如下：'.format(ename=ename))
        for name, department in info:
            print(name, department)

    elif number == 7:
        pno1 = args[0]
        pno2 = args[1]
        sql = 'select distinct a.ESSN from (select ESSN from WORKS_ON where PNO = \'{pno1}\') as a join (select ESSN from WORKS_ON where PNO = \'{pno2}\') as b on a.ESSN = b.ESSN'.format(pno1=pno1, pno2=pno2)
        a7 = cur.execute(sql)
        info = cur.fetchmany(a7)
        print('至少参加了项目编号为{pno1}和{pno2}的员工编号为：'.format(pno1=pno1, pno2=pno2))
        for i in info:
            for j in i:
                print(j)

    elif number == 8:
        salary = args[0]
        sql = 'select DNAME from DEPARTMENT natural join EMPLOYEE group by DNO having avg(SALARY) < {salary}'.format(salary=salary)
        a8 = cur.execute(sql)
        info = cur.fetchmany(a8)
        print('员工平均工资低于{salary}的部门名称有：'.format(salary=salary))
        for i in info:
            for j in i:
                print(j)

    elif number == 9:
        n = args[0]
        hours = args[1]
        sql = 'select ENAME from EMPLOYEE natural join WORKS_ON group by ESSN, ENAME having count(PNO) >= {n} and sum(HOURS) <= {hours}'.format(n=n, hours=hours)
        a9 = cur.execute(sql)
        info = cur.fetchmany(a9)
        print('参加了多于{n}个项目且工作总时间低于{hours}的员工姓名如下：'.format(n=n, hours=hours))
        for i in info:
            for j in i:
                print(j)

    else:
        print('参数错误！')

print('-----------------------------------------')
query(1, 'P1')
print('-----------------------------------------')
query(2, 'SQLProject')
print('-----------------------------------------')
query(3, '财务部')
print('-----------------------------------------')
query(4, '研发部', 3000)
print('-----------------------------------------')
query(5, 'P1')
print('-----------------------------------------')
query(6, '张红')
print('-----------------------------------------')
query(7, 'P1', 'P2')
print('-----------------------------------------')
query(8, 3000)
print('-----------------------------------------')
query(9, 3, 8)
print('-----------------------------------------')