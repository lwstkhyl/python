import pymysql
from base import login, default_login, do_self
from search import search
from delete import delete
from change import change
from add import add
if __name__ == '__main__':
    # db = login()
    db = default_login()  # 测试
    cur = db.cursor()  # 获取游标对象
    delete(cur, db)
    # while 1:
    #     print("0-查询 1-增加 2-修改 3-删除 4-自定义操作 -1退出")
    #     do = input("请输入要执行的操作：")
    #     if do == '0':
    #         search(cur, db)
    #     elif do == '1':
    #         add(cur, db)
    #     elif do == '2':
    #         change(cur, db)
    #     elif do == '3':
    #         delete(cur, db)
    #     elif do == '4':
    #         do_self(cur, db)
    #     elif do == '-1':
    #         break
    #     else:
    #         print('输入有误，请重新输入')
    db.close()  # 关闭数据库连接
