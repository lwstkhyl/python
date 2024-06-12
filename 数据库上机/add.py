from base import confirm, have_canteen


def add_canteen(cursor, db):
    address = input("请输入食堂地址：")
    name = input("请输入食堂名称：")
    command = f'insert into canteen values("{address}","{name}",0);'
    if confirm():
        try:
            cursor.execute(command)
            db.commit()
        except:
            print("输入有误/食堂名重复，请重新输入！")
            return
        print('操作成功')


def add_food(cursor, db):
    name = input("请输入菜品名称：")
    price = input("请输入菜品价格：")
    taste = input("请输入菜品口味：")
    address = input("请输入所在食堂地址：")
    if not have_canteen(cursor, address):
        return
    command1 = f'insert into food values("{name}",{price},"{taste}","{address}");'
    command2 = f'update canteen set food_count = food_count + 1 where canteen_name = "{address}";'
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


def add(cursor, db):
    while 1:
        print("输入1添加食堂，输入2添加菜品，输入-1或回车返回")
        do = input("请输入要执行的操作：") or '-1'
        if do == '1':
            add_canteen(cursor, db)
        elif do == '2':
            add_food(cursor, db)
        elif do == '-1':
            break
        else:
            print('输入有误，请重新输入')
