from base import show_data,show_single_data

all_col_name = ['地址', '食堂名称', '菜品名', '价格', '口味']
canteen_col_name = ['地址', '食堂名称', '菜品数量']
food_col_name = ['菜品名', '价格', '口味', '所在食堂']



def search(cursor, db):
    cursor.execute('''
        select * from student where age>=30;
    ''')  # 使用execute()方法执行SQL语句
    data = cursor.fetchall()  # fetchone()方法获取单条数据  fetchall()方法获取所有数据
    show_data(['id', 'name', 'age', 'sex'], data)