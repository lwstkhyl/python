from base import confirm, have_canteen


def change_food(cursor, db):
    name = input("请输入菜品名称：")
    address = input("请输入所在食堂名称：")
    print("如不想更改此项请按回车")
    new_name = input("请输入菜品新名称：") or 'food_name'
    new_price = input("请输入菜品新价格：") or 'price'
    new_taste = input("请输入菜品新口味：") or 'taste'
    new_address = input("请输入新所在食堂名称：") or 'canteen_name'
    if not have_canteen(cursor, address):
        return
    if new_name != 'food_name':
        new_name = f'"{new_name}"'
    if new_price != 'price':
        new_price = f'"{new_price}"'
    if new_taste != 'taste':
        new_taste = f'"{new_taste}"'
    if confirm():
        try:
            command = f'''update food set price = {new_price} where food_name = "{name}" and canteen_name = "{address}";'''
            cursor.execute(command)
            db.commit()
            command = f'''update food set taste = {new_taste} where food_name = "{name}" and canteen_name = "{address}";'''
            cursor.execute(command)
            db.commit()
            if address != new_address and new_address != 'canteen_name':  # 如果地址发生改变
                command = f'''update food set canteen_name = "{new_address}" where food_name = "{name}" and canteen_name = "{address}";'''
                cursor.execute(command)
                db.commit()
                command = f'''update canteen set food_count = food_count + 1 where canteen_name = "{new_address}";'''
                cursor.execute(command)
                db.commit()
                command = f'''update canteen set food_count = food_count - 1 where canteen_name = "{address}";'''
                cursor.execute(command)
                db.commit()
            # 最后改名字，因为前面的更改以名字为查找标识
            command = f'''update food set food_name = {new_name} where food_name = "{name}" and canteen_name = "{address}";'''
            cursor.execute(command)
            db.commit()
        except:
            print("输入有误，请重新输入！")
            return
        print('操作成功')


def change_canteen(cursor, db):
    name = input("请输入食堂名称：")
    address = input("请输入食堂地址：")
    new_name = input("请输入食堂新名称：") or 'canteen_name'
    new_address = input("请输入新食堂地址：") or address
    if new_name != 'canteen_name':
        new_name = f'"{new_name}"'
    if confirm():
        try:
            command = f'''update canteen set address = '{new_address}' where canteen_name = "{name}" and address = "{address}";'''
            cursor.execute(command)
            db.commit()
            if new_name != name and new_name != 'canteen_name':  # 如果名字发生改变
                command = f'''update canteen set canteen_name = {new_name} where canteen_name = "{name}" and address = "{new_address}";'''
                cursor.execute(command)
                db.commit()
                command = f'''update food set canteen_name = {new_name} where canteen_name = "{name}";'''
                cursor.execute(command)
                db.commit()
        except:
            print("输入有误，请重新输入！")
            return
        print('操作成功')


def change(cursor, db):
    while 1:
        print("输入1更改食堂，输入2更改菜品，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        if do == '1':
            change_canteen(cursor, db)
        elif do == '2':
            change_food(cursor, db)
        elif do == '-1':
            break
        else:
            print('输入有误，请重新输入')
