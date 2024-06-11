import pymysql


def login():
    """连接到数据库"""
    while 1:
        password = input("请输入数据库密码：")
        database = input("请输入数据库名称：")
        if database == '' and password == '':
            return None
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
        conf = input("请确认[y/n]：") or 'n'
        if conf == 'y':
            return True
        elif conf == 'n':
            return False
        else:
            print("输入应为y或n，请重新输入！")


def have_canteen(cursor, address) -> bool:
    """检测该食堂是否存在"""
    if address == 'canteen_name':
        return True
    try:
        cursor.execute(f'select * from canteen where canteen_name = "{address}";')
        if cursor.fetchall() == ():
            print("该食堂不存在，请先添加该食堂")
            return False
        else:
            return True
    except:
        print("输入有误，请重新输入！")
        return False


def get_max_price(cursor) -> int:
    """获取菜品价格最大值"""
    cursor.execute(f'select price from food order by price desc;')
    data = cursor.fetchone()
    return data[0]


def show_data(col_name: list, col_val: tuple):
    """
    输出多行查询结果
    :param col_name: 列名
    :param col_val: 数据（数据列数应等于列名数），是二维元组
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


def show_single_data(data: tuple, head: str = '', seq: str = ','):
    """
    输出单行查询结果
    :param data: 单行数据（每个第二维元组中只有一个数据）
    :param head: 标头，输出为 head:data1,data2,...
    :param seq: 分隔符
    """
    if data is None or data == ():
        print("查找结果为空")
        return
    try:
        if type(data[0]) != tuple:
            print("数据格式有误")
            return
    except:
        print("数据格式有误")
        return
    res = head
    if head != '':
        res += ':'
    for d in data:
        if d != data[len(data)-1]:
            res += (d[0] + seq)
        else:
            res += d[0]
    print(res)


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
        return
    print('操作成功')
