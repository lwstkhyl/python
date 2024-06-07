from base import show_data, show_single_data

all_col_name = ['地址', '食堂名称', '菜品名', '价格', '口味']
canteen_col_name = ['地址', '食堂名称', '菜品数量']
food_col_name = ['菜品名', '价格', '口味', '所在食堂']


def ser_canteen(cursor, db):
    while 1:
        print("输入1列出所有食堂的详细信息，输入2列出所有食堂名称，输入3根据食堂名称和地址查询，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        if do == '1':
            cursor.execute('select * from canteen order by food_count desc;')
            data = cursor.fetchall()
            show_data(canteen_col_name, data)
            break
        elif do == '2':
            cursor.execute('select distinct canteen_name from canteen;')
            data = cursor.fetchall()
            show_single_data(data, '食堂名称')
            break
        elif do == '3':
            print("如不想根据此项搜索请按回车")
            name = input("请输入食堂名称：") or 'canteen_name'
            address = input("请输入食堂地址：") or 'address'
            if name != 'canteen_name':
                name = f'"{name}"'
            if address != 'address':
                address = f'"{address}"'
            cursor.execute(f'select * from canteen where canteen_name = {name} and address = {address} order by food_count desc;')
            data = cursor.fetchall()
            show_data(canteen_col_name, data)
            break
        elif do == '-1':
            break
        else:
            print('输入有误，请重新输入')


def ser_food(cursor, db):
    pass


def ser_all(cursor, db):
    pass


def search(cursor, db):
    while 1:
        print("输入1查询食堂信息，输入2查询菜品信息，输入3查询菜品与食堂的所有信息，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        if do == '1':
            ser_canteen(cursor, db)
        elif do == '2':
            ser_food(cursor, db)
        elif do == '3':
            ser_all(cursor, db)
        elif do == '-1':
            break
        else:
            print('输入有误，请重新输入')