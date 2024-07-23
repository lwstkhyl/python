<a id="mulu">目录</a>
<a href="#mulu" class="back">回到目录</a>
<style>
    .back{width:40px;height:40px;display:inline-block;line-height:20px;font-size:20px;background-color:lightyellow;position: fixed;bottom:50px;right:50px;z-index:999;border:2px solid pink;opacity:0.3;transition:all 0.3s;color:green;}
    .back:hover{color:red;opacity:1}
    img{vertical-align:bottom;}
</style>

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [文件读取](#文件读取)
    - [csv/table](#csvtable)
    - [excel](#excel)
    - [sql](#sql)

<!-- /code_chunk_output -->

<!-- 打开侧边预览：f1->Markdown Preview Enhanced: open...
只有打开侧边预览时保存才自动更新目录 -->

写在前面：[资料下载](https://pan.baidu.com/s/1yrr-kvH2PAR7zNI3K81WSA)  提取码：wusa
### 文件读取
##### csv/table
`df.to_csv(存放路径, sep=',', header=True, index=True)`
- `sep`：分隔符，一般csv的都为逗号
- `header`：是否保留列索引
- `index`：是否保留行索引

```
    A   B   C
1  A1  B1  C1
2  A2  B2  C2
3  A3  B3  C3
4  A4  B4  C4
5  A5  B5  C5
```
```py
df.to_csv('data.csv')
```
![to_csv](./md-image/to_csv.png "to_csv"){:width=100 height=100}

---

`pd.read_csv(数据路径, sep=',', header=0, index_col=None)`
- `sep`：分隔符，一般csv的都为逗号
- `header`：指定哪行作为列索引，默认为第一行
- `index_col`：指定哪列作为行索引，默认不读取行索引，都作为元素读取
- `header`和`index_col`都可取整数值/字符串，表示第几行/列或者行/列名；也可取None，表示不读取行/列索引；也可以是一个整数型列表，表示将指定行/列都作为行/列索引（多层索引）

读取上面的数据：
```py
print(pd.read_csv('data.csv', index_col=0))
```
```
    A   B   C
1  A1  B1  C1
2  A2  B2  C2
3  A3  B3  C3
4  A4  B4  C4
5  A5  B5  C5
```

---

`read_table`用法同read_csv，只是分隔符默认为制表符`\t`
没有`to_table`
##### excel
`df.to_excel(存放路径, sheet_name="Sheet1", header=True, index=True)`
- `sheet_name`：工作表名称
- `header`：是否保留列索引
- `index`：是否保留行索引

注：该函数需要安装openpyxl包
```py
df.to_excel('data.xlsx')
```
![to_excel](./md-image/to_excel.png "to_excel"){:width=150 height=150}

---

`pd.read_excel(数据路径, sheet_name=0, header=0, index_col=None, names=None)`
- `sheet_name`：读取哪个工作表。可以是数字，表示读取第几个表；也可以是工作表名称
- `header`和`index_col`参数同[csv/table](#csvtable)
- `names`：设置列名

```
# pd.read_excel('data.xlsx', index_col=0)
    A   B   C
1  A1  B1  C1
2  A2  B2  C2
3  A3  B3  C3
4  A4  B4  C4
5  A5  B5  C5
```
```
# pd.read_excel('data.xlsx', header=0, names=list("abcd"), index_col=0)
    b   c   d
a            
1  A1  B1  C1
2  A2  B2  C2
3  A3  B3  C3
4  A4  B4  C4
5  A5  B5  C5
```
##### sql
需要SQLAlchemy和pymysql包
`create_engine('数据库类型+驱动://用户名:密码@数据库地址:端口号/数据库名')`
以mysql数据库为例：root用户、默认端口号、本地数据库
```py
from sqlalchemy import create_engine
conn = create_engine("mysql+pymysql://root:123456@localhost:3306/test")
```
`df.to_sql(name,con,index=True,if_exists='fail')`
- `name`：数据库中表名
- `con`：数据库连接对象，即上面获取的`conn`
- `index`：是否保存行索引
- `if_exists`：如果表已经存在时的处理方法，如果设为`append`则为追加写入

```py
df.to_sql(
    name='df',  # 保存到df表中
    con=conn,  # 设置连接对象
    index=False,  # 不保存行索引
    if_exists='append'  # 追加写入
)
```
![to_sql](./md-image/to_sql.png "to_sql"){:width=150 height=150}

---

`pd.read_sql(sql,con,index_col=None)`
- `sql`：一般是sql查询语句，将其返回结果进行保存
- `con`：数据库连接对象，即上面获取的`conn`
- `index_col=None`指定哪列作为行索引，默认不设置行索引（行索引为0-n）

```py
print(pd.read_sql(
    sql="select * from df",  # 读取df表的全部数据
    con=conn,  # 设置连接对象
))
```
```
    A   B   C
0  A1  B1  C1
1  A2  B2  C2
2  A3  B3  C3
3  A4  B4  C4
4  A5  B5  C5
```
```py
print(pd.read_sql(
    sql="select * from df",
    con=conn,
    index_col="A"  # 指定A列作行索引
))
```
```
     B   C
A         
A1  B1  C1
A2  B2  C2
A3  B3  C3
A4  B4  C4
A5  B5  C5
```
