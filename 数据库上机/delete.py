from base import confirm


def del_canteen(cursor, db):
    name = input("请输入食堂名称：")
    command1 = f'delete from canteen where canteen_name = "{name}";'
    command2 = f'delete from food where canteen_name = "{name}";'
    if confirm():
        try:
            cursor.execute(command1)
            db.commit()
            cursor.execute(command2)
            db.commit()
        except:
            print("输入有误，请重新输入！")
            return
        print('操作成功')


def del_food(cursor, db):
    name = input("请输入菜品名称：")
    address = input("请输入所在食堂名称：")
    command1 = f'delete from food where food_name = "{name}" and canteen_name = "{address}";'
    command2 = f'update canteen set food_count = food_count - 1 where canteen_name = "{address}";'
    if confirm():
        try:
            cursor.execute(command1)
            db.commit()
            cursor.execute(command2)
            db.commit()
        except:
            print("输入有误，请重新输入！")
            return
        print('操作成功')


def del_all(cursor, db):
    if confirm():
        cursor.execute('truncate table canteen;')
        db.commit()
        cursor.execute('truncate table food;')
        db.commit()
        print('操作成功')


def delete(cursor, db):
    while 1:
        print("输入1删除食堂，输入2删除菜品，输入3清空所有数据，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        if do == '1':
            del_canteen(cursor, db)
        elif do == '2':
            del_food(cursor, db)
        elif do == '3':
            del_all(cursor, db)
        elif do == '-1':
            break
        else:
            print('输入有误，请重新输入')
