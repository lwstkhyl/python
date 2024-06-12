from base import show_data, show_single_data, get_max_price, get_canteen_address

all_col_name = ['地址', '食堂名称', '菜品名', '价格', '口味']
canteen_col_name = ['地址', '食堂名称', '菜品数量']
food_col_name = ['菜品名', '价格', '口味', '所在食堂']


def ser_canteen(cursor, db):
    while 1:
        print("输入1列出所有食堂的详细信息，输入2列出所有食堂名称，输入3根据食堂名称和地址查询，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        try:
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
                if name != 'canteen_name':
                    name = f'"{name}"'
                cursor.execute(f'select * from canteen where canteen_name = {name} order by food_count desc;')
                data = cursor.fetchall()
                show_data(canteen_col_name, data)
                break
            elif do == '-1':
                break
            else:
                print('输入有误，请重新输入')
        except:
            print("输入有误，请重新输入！")
            return


def ser_food(cursor, db):
    name = input("请输入食堂名称：") or 'canteen_name'
    if name != 'canteen_name':
        name = f'"{name}"'
    try:
        cursor.execute(f'select * from food where canteen_name = {name} order by price desc;')
        data = cursor.fetchall()
        show_data(food_col_name, data)
    except:
        print("输入有误，请重新输入！")
        return


def ser_all(cursor, db):
    while 1:
        print("输入1根据菜品名称查询，输入2根据菜品口味查询，输入3根据菜品价格查询，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        try:
            if do == '1':
                name = input("请输入菜品名称：") or 'food_name'
                if name != 'food_name':
                    name = f'"{name}"'
                cursor.execute(f'''
                    select canteen.address,canteen.canteen_name,food.food_name,food.price,food.taste 
                    from canteen,food where food.food_name = {name} and 
                    food.canteen_name = canteen.canteen_name;
                ''')
                data = cursor.fetchall()
                show_data(all_col_name, data)
                break
            elif do == '2':
                taste = input("请输入菜品口味：") or 'taste'
                if taste != 'taste':
                    taste = f'"%{taste}%"'
                cursor.execute(f'''
                    select canteen.address,canteen.canteen_name,food.food_name,food.price,food.taste 
                    from canteen,food where food.taste like {taste} and 
                    food.canteen_name = canteen.canteen_name;
                ''')
                data = cursor.fetchall()
                show_data(all_col_name, data)
                break
            elif do == '3':
                print("如不想设置此项请按回车，查询价格为[min,max]")
                min_price = input("min：") or 0
                max_price = input("max：") or get_max_price(cursor)
                cursor.execute(f'''
                    select canteen.address,canteen.canteen_name,food.food_name,food.price,food.taste 
                    from canteen,food where food.price between {min_price} and {max_price} and 
                    food.canteen_name = canteen.canteen_name;
                ''')
                data = cursor.fetchall()
                show_data(all_col_name, data)
                break
            elif do == '-1':
                break
            else:
                print('输入有误，请重新输入')
        except:
            print("输入有误，请重新输入！")
            return


def search(cursor, db):
    while 1:
        print("输入1查询食堂信息，输入2根据食堂查询菜品信息，输入3查询菜品的所有信息，输入-1或回车返回")
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
