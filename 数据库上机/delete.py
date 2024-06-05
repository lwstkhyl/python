import pymysql
from base import confirm


def del_canteen(cursor, db):
    address = input("请输入食堂地址：")
    name = input("请输入食堂名称：")
    command = f'insert into canteen values("{address}","{name}",0);'
    try:
        cursor.execute(command)
        db.commit()
    except:
        print("输入有误，请重新输入！")


def del_food(cursor, db):
    name = input("请输入菜品名称：")
    price = input("请输入菜品价格：")
    taste = input("请输入菜品口味：")
    address = input("请输入所在食堂地址：")
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


def delete(cursor, db):
    while 1:
        do = input("输入1删除食堂，输入2删除菜品，输入-1返回：")
        if do == '1':
            del_canteen(cursor, db)
        elif do == '2':
            del_food(cursor, db)
        elif do == '-1':
            break
        else:
            print('输入有误，请重新输入')
