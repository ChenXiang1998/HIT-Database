from syntaxtree import SyntaxTree

employee = ["ESSN", "ADDRESS", "SALARY", "SUPERSSN", "ENAME", "DNO"]
department = ["DNO", "DNAME", "DNEMBER", "MGRSSN", "MGRSTARTDATE"]
project = ["PNAME", "PNO", "PLOCATION", "DNO"],
works_on = ["HOURS", "ESSN", "PNO"]


def parse(sql_statement):
    sql = sql_statement.split()
    execute_tree = SyntaxTree()

    index = 0
    while True:
        if index >= len(sql):
            break
        elif sql[index] == 'SELECT' or sql[index] == 'PROJECTION':
            execute_tree.operator = sql[index]
            index += 2  # 从[开始到]里面的全部记录下来
            condition = ''
            while sql[index] != ']':
                condition += sql[index]
                condition += ' '
                index += 1
            index += 1
            execute_tree.condition = condition
        elif sql[index] == 'JOIN':
            # 连接操作需要创建子树，所以分开写
            execute_tree.operator = sql[index]
            execute_tree.left_child = SyntaxTree()
            execute_tree.left_child.attribute = sql[index - 1]
            execute_tree.right_child = SyntaxTree()
            execute_tree.right_child.attribute = sql[index + 1]
            index += 1
        elif sql[index] == '(':
            # 每次遇到这个说明需要创建一棵子树，由于题目中的查询都是只有一个分支，所以可以直接进入下一个子树中
            index += 1
            statement = ''
            while index < len(sql) and sql[index] != ')':
                statement += sql[index]
                statement += ' '
                index += 1
            index += 1
            execute_tree.left_child = parse(statement)
        else:
            index += 1

    return execute_tree


def search(sql):
    sql = sql.split()
    if sql[0] in employee:
        return "EMPLOYEE"
    elif sql[0] in department:
        return "DEPARTMENT"
    elif sql[0] in project:
        return "PROJECT"
    elif sql[0] in works_on:
        return "WORKS_ON"
    return None


def optimize(syntax_tree, sql):
    if syntax_tree.operator == 'SELECT':
        condition = syntax_tree.condition
        sql = condition.split('&')
        relation = []
        for i in range(len(sql)):
            if search(sql[i]) is not None:
                relation.append(search(sql[i]))
        syntax_tree = optimize(syntax_tree.left_child, sql)
    elif syntax_tree.operator == 'PROJECTION':
        syntax_tree.left_child = optimize(syntax_tree.left_child, sql)
    elif syntax_tree.operator == 'JOIN':
        first_tree = SyntaxTree()
        first_tree.operator = 'SELECT'
        first_tree.condition = sql[0]
        first_tree.left_child = syntax_tree.left_child
        syntax_tree.left_child = first_tree
        if len(sql) == 1:
            return syntax_tree
        second_tree = SyntaxTree()
        second_tree.operator = 'SELECT'
        second_tree.condition = sql[1]
        second_tree.right_child = syntax_tree.right_child
        syntax_tree.right_child = second_tree
    return syntax_tree


def print_tree(syntax_tree):
    if syntax_tree.operator != '':
        print(syntax_tree.operator, syntax_tree.condition)
    else:
        print(syntax_tree.attribute)
    if syntax_tree.left_child is not None:
        print_tree(syntax_tree.left_child)
    if syntax_tree.right_child is not None:
        print_tree(syntax_tree.right_child)


if __name__ == '__main__':
    sql1 = "SELECT [ ENAME = ’Mary’ & DNAME = ’Research’ ] ( EMPLOYEE JOIN DEPARTMENT )"
    sql2 = "PROJECTION [ BDATE ] ( SELECT [ ENAME = ’John’ & DNAME = ’ Research’ ] ( EMPLOYEE JOIN DEPARTMENT) )"
    sql3 = "SELECT [ ESSN = ’01’ ] ( PROJECTION [ ESSN, PNAME ] ( WORKS_ON JOIN PROJECT ) )"

    print('--------------------------------------------')
    etree1 = parse(sql1)
    print_tree(etree1)
    print('--------------------------------------------')
    otree1 = optimize(etree1, '')
    print_tree(otree1)
    print('--------------------------------------------')
    print('--------------------------------------------')
    etree2 = parse(sql2)
    print_tree(etree2)
    print('--------------------------------------------')
    otree2 = optimize(etree2, '')
    print_tree(otree2)
    print('--------------------------------------------')
    print('--------------------------------------------')
    etree3 = parse(sql3)
    print_tree(etree3)
    print('--------------------------------------------')
    otree3 = optimize(etree3, '')
    print_tree(otree3)
    print('--------------------------------------------')