import pymysql


def login():
    """连接到数据库"""
    while 1:
        password = input("请输入数据库密码：")
        database = input("请输入数据库名称：")
        try:
            db = pymysql.connect(host='localhost',  # 主机名
                                 user='root',  # 用户名
                                 password=password,  # 数据库密码
                                 database=database,  # 数据库名称
                                 charset='utf8'  # 指定编码方式
                                 )  # 连接数据库
            print("连接成功！")
            return db
        except:
            print("输入有误，请重新输入！")


def default_login():
    """默认连接（测试）"""
    db = pymysql.connect(host='localhost',  # 主机名
                         user='root',  # 用户名
                         password='wthlyhshpy',  # 数据库密码
                         database='test',  # 数据库名称
                         charset='utf8'  # 指定编码方式
                         )  # 连接数据库
    return db


def confirm() -> bool:
    """确认是否执行操作"""
    while 1:
        conf = input("请确认[y/n]：")
        if conf == 'y':
            return True
        elif conf == 'n':
            return False
        else:
            print("输入应为y或n，请重新输入！")


def show_data(col_name: list, col_val: tuple):
    """
    输出查询结果
    :param col_name: 列名
    :param col_val: 数据（数据列数应等于列名数）
    """
    if col_val is None or len(col_val) == 0:
        print("查找结果为空")
        return
    if len(col_val[0]) != len(col_name):
        print("列名与列值数量不同")
        return
    row_index = 0
    for row in col_val:
        row_index += 1  # 当前输出的是第几行
        print(f"({row_index})", end='')  # 显示第几行
        for val_index in range(len(row)):  # 读取行内数据
            print(f"{col_name[val_index]}:{row[val_index]}   ", end='')
        print('\n', end='')


def do_self(cursor, db):
    command = input("请输入sql语句：")
    try:
        cursor.execute(command)
        db.commit()
        data = cursor.fetchall()
        if data != ():
            print(data)
    except:
        print("输入语句有误")
