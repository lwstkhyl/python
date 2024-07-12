<a id="mulu">目录</a>
<a href="#mulu" class="back">回到目录</a>
<style>
    .back{width:40px;height:40px;display:inline-block;line-height:20px;font-size:20px;background-color:lightyellow;position: fixed;bottom:50px;right:50px;z-index:999;border:2px solid pink;opacity:0.3;transition:all 0.3s;color:green;}
    .back:hover{color:red;opacity:1}
    img{vertical-align:bottom;}
</style>

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [数据结构](#数据结构)
    - [series](#series)
      - [创建](#创建)
      - [values和index](#values和index)
      - [取值](#取值)
      - [切片](#切片)
      - [基本属性和方法](#基本属性和方法)
      - [运算](#运算)
    - [DataFrame](#dataframe)
      - [创建](#创建-1)
      - [基本属性和方法](#基本属性和方法-1)

<!-- /code_chunk_output -->

<!-- 打开侧边预览：f1->Markdown Preview Enhanced: open...
只有打开侧边预览时保存才自动更新目录 -->

> import pandas as pd

### 数据结构
pandas中数据结构主要有series和dataframe
- series类似于一维数组，可以看成是一个有序的字典结构
- dataframe是一种有行/列的表格型数据结构，可以看成是由series组成的字典
##### series
由values和index组成
- values：一组数据（ndarray类型）
- index：相关的数据索引标签
###### 创建
**第一种方式**：由列表/np数组创建：`pd.Series(l)`
```
l = [10, 20, 30, 40, 50]
s = pd.Series(l)
s = pd.Series(np.array(l))
print(s)
```
输出：
```
0    10
1    20
2    30
3    40
4    50
dtype: int32
```
其中第一列01234是索引，第二列是值

---

**第二种方式**：由字典创建，字典的键为索引名，值为值
```
d = {'a': 1, 'b': 2, 'c': 3}
s = pd.Series(d)
print(s)
```
输出：
```
a    1
b    2
c    3
dtype: int64
```

---

注意：series中的值不仅可以是单个数，也可以是数组等多值
```
d = {'a': [1, 10, 100], 'b': 2, 'c': 3}
s = pd.Series(d)
print(s.a[1])  # 10
```

---

pd.Series的其它参数
- index：创建时指定索引名
- name：为创建的series起一个名字
- dtype：指定数据类型

```
s = pd.Series([1, 2, 3], index=list('abc'), name="number", dtype=float)
```
```
a    1.0
b    2.0
c    3.0
Name: number, dtype: float64
```
###### values和index
通过`series.values`和`series.index`获取
```
s = pd.Series([10, 20, 30, 40, 50])
print(s.values)  # [10 20 30 40 50]
print(s.index)  # RangeIndex(start=0, stop=5, step=1)
print(list(s.index))  # [0, 1, 2, 3, 4]
```

---

索引可被修改：`series.index = 新值`，注意新值的长度要与原索引长度相等
```
s.index = ['a', 'b', 'c', 'd', 'e']  # 等效于
s.index = list('abcde')  # list函数会将字符串拆开成单个字符作为元素存储
print(s)
```
```
a    10
b    20
c    30
d    40
e    50
dtype: int64
```
###### 取值
既可以用索引名来取值，也可以用索引序号(0,1,2,...)来取值
**显式索引：索引名**
- `series.索引名`或`series['索引名']`返回索引名对应的value
    注意：如果索引名是数字，就不能使用`series.索引名`获取，必须通过`series['索引名']`
    ```
    print(s.a)  # 10
    print(s.A)  # 报错，区分大小写
    s.a = 1
    print(s['a'])  # 1
    ```
    也可同时取多个值`series[['索引名1','索引名2',...]]`，返回一个新的series。这种方法也可只取一个值，也返回series
    ```
    s = pd.Series([1, 2, 3], index=list('abc'))
    print(s[['b', 'a']])
    ```
    ```
    b    2
    a    1
    dtype: int64
    ```
- `series.loc['索引名']`或`series.loc[['索引名1','索引名2',...]]`
    ```
    print(s.loc['a'])  # 1
    print(s.loc[['a', 'b']])
    ```
    ```
    a    1
    b    2
    dtype: int64
    ```
    ```
    print(s.loc[['a']])
    ```
    ```
    a    1
    dtype: int64
    ```

---

**隐式索引：索引序号（下标）**
- `series['整数下标']`或`series[['下标1','下标2',...]]`规则同上
    ```
    s = pd.Series([1, 2, 3], index=list('abc'))
    print(s[0])  # 1
    print(s[[1, 2]])
    ```
    ```
    b    2
    c    3
    dtype: int64
    ```
    ```
    print(s[[0]])
    ```
    ```
    a    1
    dtype: int64
    ```
- `series.iloc['整数下标']`或`series.iloc[['下标1','下标2',...]]`规则也同上
    ```
    print(s.iloc[0])  # 1
    print(s.iloc[[1, 2]])
    print(s.iloc[[0]])
    ```
    输出同上

注意：loc和iloc不能交换使用，必须分别对应索引名和索引下标

---

**特殊：bool值索引**
`s[[bool值1,bool值2,...]]`取bool值为True的元素
```
s = pd.Series(range(5))
print(s[[True, False, True, False, True]])  
```
```
0    0
2    2
4    4
dtype: int64
```
第1、3、5个bool值为True，就取s中第1、3、5个元素，返回一个新series
###### 切片
同取值，既可以用索引名来切片（**显式切片**），也可以用索引序号(0,1,2,...)来切片（**隐式切片**）
```
a    0
b    1
c    2
d    3
e    4
f    5
g    6
h    7
i    8
k    9
```
隐式切片的方式与列表类似：
```
print(s[1:4])  # 等效于
print(s.iloc[1:4])  # 左闭右开
```
```
b    1
c    2
d    3
dtype: int64
```
可以设置步长、取负数
```
print(s[1:-1:2])
```
```
b    1
d    3
f    5
h    7
dtype: int64
```
---
显式切片：`series[索引名start:索引名end]`或`series.loc[索引名start:索引名end]`，注意是左闭右闭区间，也可以设置步长
```
print(s['b':'e'])  # 等效于
print(s.loc['b':'e'])  # 左闭右闭
```
```
b    1
c    2
d    3
e    4
dtype: int64
```
###### 基本属性和方法
- shape：形状
- size：长度
- index：索引
- values：值
- name：名字

```
s = pd.Series(range(3), index=list('abc'))
print(s.shape)  # (3,) 一维，长度为3
print(s.size)  # 3
print(s.index)  # Index(['a', 'b', 'c'], dtype='object')
print(s.values)  # [0 1 2]
print(s.name)  # None
```
---
- 查看数据：
    - head(n=5)：查看前n条数据
    - tail(n=5)：查看后n条数据
    ```
    s = pd.Series(range(7), index=list('abcdefg'))
    print(s.head(1))  # (3,) 一维，长度为3
    ```
    ```
    a    0
    dtype: int64
    ```
    ```
    print(s.tail())  # 3
    ```
    ```
    c    2
    d    3
    e    4
    f    5
    g    6
    dtype: int64
    ```
- 检测缺失数据
  - `pd.isnull(s)`和`pd.notnull(s)`
  - `s.isnull()`和`s.notnull()`
  
  检测series中的元素是否为空，返回一个series。它们返回的结果相同，只是调用方式有差异
    ```
    s = pd.Series([1, 2, 3, np.nan])
    ```
    ```
    0    1.0
    1    2.0
    2    3.0
    3    NaN
    dtype: float64
    ```
    ```
    print(pd.isnull(s))  # 等效于
    print(s.isnull())
    ```
    ```
    0    False
    1    False
    2    False
    3     True
    dtype: bool
    ```
    notnull()就是上面结果的取反
    ```
    print(s.notnull())  # 等效于
    print(pd.notnull(s))  # 等效于
    print(~s.isnull())  # 取反运算符，对所有values取反
    ```

    ---

    应用：过滤掉数据中的空值
    ```
    s = pd.Series([1, 2, 3, np.nan, 4, np.nan, 5])
    print(s[~s.isnull()])  # 等效于
    print(s[s.notnull()])
    ```
    ```
    0    1.0
    1    2.0
    2    3.0
    4    4.0
    6    5.0
    dtype: float64
    ```
###### 运算
因为pd基于np实现，所以适用于np的数组运算大多数也适用于series（+-*/等等）
两个series之间的运算：根据索引来计算，如`s1+s2`就是将s1中索引为0的数与s2中索引为0的数相加，保存在结果series中索引为0的位置，而不是简单的将s1的第一个数与s2的第一个数相加
- 在运算中自动对齐索引，如果索引不对应，则补NAN
- 没有广播机制

```
s1 = pd.Series([1, 2, 3], index=[0, 1, 2])
s2 = pd.Series([2, 1, 3, 4], index=[1, 0, 2, 3])
print(s1+s2)
```
```
0    2.0
1    4.0
2    6.0
3    NaN
dtype: float64
```
虽然s2的第一个数为2，但索引为0的还是1，所以结果中索引为0的值是1+1=2。s2中有索引为3的值，但s1中没有，因此结果中索引为0的值是nan

---

如果想设置自动补值，就使用`s1.add(s2,fill_value=nan)`代替`s1+s2`，其中fill_value是补充的值，如不指定fill_value，结果同`s1+s2`
```
print(s1.add(s2, fill_value = 0))
```
```
0    2.0
1    4.0
2    6.0
3    4.0
dtype: float64
```
`res[3] = 4 + 0`其中0就是为s1补充的值（用0将s1补充到与s2同行，再相加）
##### DataFrame
由按一定顺序排列的多列数据组成，将series从一维拓展到多维，既有行索引也有列索引
- 行索引：index
- 列索引：columns
- 值：values（是np的二维数组）
###### 创建
最常用的方法是传递一个字典，以字典键作为列名，值（一个数组）作为列值，pd会自动加上每行的索引
注意：传入的每个数组（列值）长度必须相等，若不相等则报错
```
d = {
    'name': ['abc', 'bcd', 'cde'],
    'age': [11, 12, 13]
}
df = pd.DataFrame(d)
print(df)
```
```
  name  age
0  abc   11
1  bcd   12
2  cde   13
```
创建时指定行、列索引：`pd.DataFrame(d, index=行索引, columns=列索引)`
使用二维数组创建：
```
df = pd.DataFrame(
    data=np.random.randint(1, 10, size=(2, 3)),  # 两行三列
)
print(df)
```
```
   0  1  2
0  2  2  4
1  9  4  8
```
```
df = pd.DataFrame(
    data=np.random.randint(1, 10, size=(2, 3)),  # 两行三列
    index=['行1', '行2'],
    columns=['列1', '列2', '列3']
)
print(df)
```
```
    列1  列2  列3
行1   6   4   9
行2   7   8   3
```
- 列索引会优先使用字典的键，如不指定就是0,1,2,...
- 行索引如不指定也是0,1,2,...
###### 基本属性和方法
- `df.values`：二维np数组（数组中的每个元素是df中的一行数据
- `df.columns`：列索引
- `df.index`：行索引
- `df.shape`：形状
- `df.head(n=5)`：查看前n条数据
- `df.tail(n=5)`：查看后n条数据

```
print(df.values)  # [['abc' 11],['bcd' 12],['cde' 13]]
print(df.columns)  # Index(['name', 'age'], dtype='object')
df.index = ['第一列', '第二列', '第三列']  # 和np一样，columns和index都可用同种方式修改
print(df.index)  # Index(['第一列', '第二列', '第三列'], dtype='object')
print(df.shape)  # (3, 2) 表示有三行两列
print(df)
```
```
    name  age
第一列  abc   11
第二列  bcd   12
第三列  cde   13
```
```
print(df.head(2))
```
```
    name  age
第一列  abc   11
第二列  bcd   12
```