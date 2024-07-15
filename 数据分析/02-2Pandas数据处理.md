<a id="mulu">目录</a>
<a href="#mulu" class="back">回到目录</a>
<style>
    .back{width:40px;height:40px;display:inline-block;line-height:20px;font-size:20px;background-color:lightyellow;position: fixed;bottom:50px;right:50px;z-index:999;border:2px solid pink;opacity:0.3;transition:all 0.3s;color:green;}
    .back:hover{color:red;opacity:1}
    img{vertical-align:bottom;}
</style>

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [层次化索引](#层次化索引)
    - [创建](#创建)
      - [隐式构造](#隐式构造)
      - [显式构造](#显式构造)
    - [取索引](#取索引)
      - [series的索引](#series的索引)
      - [DataFrame的索引](#dataframe的索引)
    - [切片](#切片)
      - [series的切片](#series的切片)
      - [DataFrame的切片](#dataframe的切片)
    - [索引的堆叠](#索引的堆叠)

<!-- /code_chunk_output -->

<!-- 打开侧边预览：f1->Markdown Preview Enhanced: open...
只有打开侧边预览时保存才自动更新目录 -->

### 层次化索引
![层次化索引](./md-image/层次化索引.png "层次化索引"){:width=200 height=200}
其中最外层的"期中"、"期末"以及"1班"、"2班"就是层次化索引
##### 创建
###### 隐式构造
最常用的方法是给df构造函数的index/columns参数传递一个二维数组，数组中每个元素为对应行/列的索引，这样每行/列就有多个行名/列名
```py
row = 4
col = 5
df = pd.DataFrame(
    data=np.array(range(col*row)).reshape(row, col),
    index=[['第一组行', '第一组行', '第二组行', '第二组行'], ['行1', '行2', '行3', '行4']],
    columns=[['第一组列', '第一组列', '第二组列', '第二组列', '第二组列'], ['列1', '列2', '列3', '列4', '列5']]
)
print(df)
```
```
             第一组列    第二组列        
             列1  列2   列3  列4  列5
第一组行 行1    0   1    2   3   4
        行2    5   6    7   8   9
第二组行 行3   10   11   12  13  14
        行4   15   16   17  18  19
```
series也可创建多层索引：
```py
s = pd.Series(data=np.array(range(row)), index=df.index)
print(s)
```
```
第一组行  行1    0
         行2    1
第二组行  行3    2
         行4    3
dtype: int32
```
###### 显式构造
`pd.MultiIndex`系列方法
- 使用**数组**
    ```py
    index = pd.MultiIndex.from_arrays([
    ['第一组行', '第一组行', '第二组行', '第二组行'],
    ['行1', '行2', '行3', '行4']])
    columns = pd.MultiIndex.from_arrays([
        ['第一组列', '第一组列', '第二组列', '第二组列', '第二组列'],
        ['列1', '列2', '列3', '列4', '列5']])
    df = pd.DataFrame(
        data=np.array(range(col*row)).reshape(row, col),
        index=index,
        columns=columns
    )
    ```
    这种方式与上面的隐式构造没有差别，`pd.MultiIndex.from_arrays`写不写都可以
- 使用**元组**：`pd.MultiIndex.from_tuples()`需要传入一个元组集合，里面的每个元素是一个元组，表示每行/每列拥有的索引名
    ```py
    index = pd.MultiIndex.from_tuples(
        (
            ('第一组行', '行1'), ('第一组行', '行2'), ('第二组行', '行3'), ('第二组行', '行4')
        )
    )
    columns = pd.MultiIndex.from_tuples(
        (
            ('第一组列', '列1'), ('第一组列', '列2'), ('第二组列', '列3'), ('第二组列', '列4'), ('第二组列', '列5')
        )
    )
    df = pd.DataFrame(
        data=np.array(range(col*row)).reshape(row, col),
        index=index,
        columns=columns
    )
    ```
- **笛卡尔积**：`(a,b)*(c,d)`=>`[(a,c),(a,d),(b,c),(b,d)]`
    `pd.MultiIndex.from_product()`接收一个二维数组，它产生的结果可类比上面的使用元组创建：`pd.MultiIndex.from_product([[a,b],[c,d]])`等同于`pd.MultiIndex.from_tuples(((a,c),(a,d),(b,c),(b,d)))`，即对二维数组中的元素进行笛卡尔积运算
    ```py
    index = pd.MultiIndex.from_product([
        ['第一组行', '第二组行'],
        ['行1', '行2']
    ])
    columns = pd.MultiIndex.from_product([
        ['第一组列'],
        ['列1', '列2', '列3', '列4', '列5']
    ])
    df = pd.DataFrame(
        data=np.array(range(col*row)).reshape(row, col),
        index=index,
        columns=columns
    )
    ```
    ```
                 第一组列                
                列1  列2  列3 列4 列5
    第一组行 行1   0   1   2   3   4
            行2   5   6   7   8   9
    第二组行 行1   10  11  12  13  14
            行2   15  16  17  18  19
    ```
    注意这种方式涉及到每层索引的依次组合，比较适用于：
    ![层次化索引](./md-image/层次化索引.png "层次化索引"){:width=150 height=150}这种情况

这几种方式可以混合使用，比如index用`from_product()`，columns用`from_tuples()`
##### 取索引
###### series的索引
```
第一组行  行1    0
         行2    1
第二组行  行3    2
         行4    3
dtype: int32
```
**显式索引：**
根据外层索引取值：
```py
print(s['第一组行'])  # 或
print(s.loc['第一组行'])
```
```
行1    0
行2    1
dtype: int32
```
保留外层索引：
```py
print(s[['第一组行']])  # 也可以
print(s[['第一组行', '第二组行']])  # 同时取多个外层索引
```
```
第一组行  行1    0
         行2    1
第二组行  行3    2
         行4    3
dtype: int32
```
根据外层和内层索引：
```py
print(s['第一组行', '行1'])  # 也可以
print(s['第一组行']['行1'])  # 0
```
注意：根据显式索引取值时，当有外层索引时，不能直接使用之前的方法取内层索引，必须先说明外层索引，再在其中去取
```py
print(s['行1'])  # 报错
print(s.loc['行1'])  # 报错
```
---

**隐式索引：**
直接取的是内层索引的序号
```py
print(s[0])  # 0
print(s.iloc[1])  # 1
print(s.iloc[[1, 2]])
```
```
第一组行  行2    1
第二组行  行3    2
dtype: int32
```
###### DataFrame的索引
```
             第一组列    第二组列        
             列1  列2   列3  列4  列5
第一组行 行1    0   1    2   3   4
        行2    5   6    7   8   9
第二组行 行3   10   11   12  13  14
        行4   15   16   17  18  19
```
只需记住：df是按`df[外层列索引][内层列索引][外层行索引][内层行索引]`的顺序进行取值即可
df的隐式索引与series的隐式索引一样，直接取的是内层索引的序号
```py
print(df['第一组列'])
```
```
            列1  列2
第一组行 行1   0   1
        行2   5   6
第二组行 行3  10  11
        行4  15  16
```
```py
print(df['第一组列']['列1'])
```
```
第一组行  行1     0
         行2     5
第二组行  行3    10
         行4    15
Name: 列1, dtype: int32
```
```py
print(df['第一组列']['列1']['第一组行'])
```
```
行1    0
行2    5
Name: 列1, dtype: int32
```
```py
print(df['第一组列']['列1']['第一组行']['行1'])  # 0
```
当然，这种方法中`[[行/列]]`、`[行/列]`、`[行,列]`、`df.列名`、`loc`、`iloc`都可以混用（`[[]]`就是保留外层索引）
一些例子：
```py
df['第一组列', '列1']
df.第一组列.列1
df.iloc[:, 2]  # 取第三列
df.iloc[:, [2, 1]]  # 取第三、二列
df.loc[:, ('第一组列', '列1')]  # 取第一组列中的列1
df.loc['第一组行'].loc['行1']  # 取第一组行中的行1，也可以
df.loc[('第一组行', '行1')]
df.iloc[0]  # 取第一行
df.iloc[[0, 1]]  # 取第一、二行
```
注意特殊写法：`(外层索引, 内层索引)`表示取指定的内层索引，用来代替单索引时的`内层索引`

---

另一种取元素的方式：
```py
print(df.iloc[0, 1])  # 也可以
print(df.loc[('第一组行', '行1'), ('第一组列', '列2')])  # 1
```

##### 切片
###### series的切片
```
第一组行  行1    0
         行2    1
第二组行  行3    2
         行4    3
dtype: int32
```
**显式索引：**
根据外层索引：
```py
print(s['第一组行': '第二组行'])  # 也可以
print(s.loc['第一组行': '第二组行'])
```
```
第一组行  行1    0
         行2    1
第二组行  行3    2
         行4    3
dtype: int32
```
根据外层和内层索引：
```py
print(s.loc['第一组行'][0:2])
```
```
行1    0
行2    1
dtype: int32
```
**隐式索引：**
直接切片的是内层索引的序号
```py
print(s[1: 3])  # 也可以
print(s.iloc[1: 3])
```
```
第一组行  行2    1
第二组行  行3    2
dtype: int32
```
###### DataFrame的切片
```
             第一组列    第二组列        
             列1  列2   列3  列4  列5
第一组行 行1    0   1    2   3   4
        行2    5   6    7   8   9
第二组行 行3   10   11   12  13  14
        行4   15   16   17  18  19
```
一些例子：
```py
# 行切片
df.iloc[1: 5]  # 取第2-5行
df.loc['第一组行':'第二组行']  # 从外层索引第一组行切到第二组行
df.loc[('第一组行', '行1'), ('第二组行', '行2')]  # 从第一组行的行1切到第二组行的行2
# 列切片
df.iloc[:, 1:3]  # 取第2-3列
df.loc[:, '第一组列':'第二组列']  # 取外层的第一组列到第二组列
df.loc[:, ('第一组列', '列2'):('第二组列', '列2')]  # 报错，虽然按前面的逻辑来讲没问题
```
建议切片时使用隐式索引，更简便稳定
##### 索引的堆叠
```
             第一组列   第二组列    
             列1  列2   列1  列2
第一组行 行1    0   1    2   3
        行2    4   5    6   7
第二组行 行1    8   9   10  11
        行2   12   13   14  15
```
`df.stack(level=-1)`将列索引（默认是最内层列索引）变为最内层行索引
- `level`指定改变的是哪层索引，各层索引**从外至内**依次是0-n，-1就表示最内层索引

```py
print(df.stack())
```
```
                第一组列  第二组列
第一组行 行1 列1     0     2
            列2     1     3
        行2 列1     4     6
            列2     5     7
第二组行 行1 列1     8    10
            列2     9    11
        行2 列1    12    14
            列2    13    15
```
```py
print(df.stack(level=0))
```
```
                     列1  列2
第一组行 行1 第一组列   0   1
            第二组列   2   3
        行2 第一组列   4   5
            第二组列   6   7
第二组行 行1 第一组列   8   9
            第二组列  10  11
        行2 第一组列  12  13
            第二组列  14  15
```

---

`df.unstack(level=-1)`将行索引（默认是最内层列索引）变为最内层列索引
```
                第一组列  第二组列
第一组行 行1 列1     0     2
            列2     1     3
        行2 列1     4     6
            列2     5     7
第二组行 行1 列1     8    10
            列2     9    11
        行2 列1    12    14
            列2    13    15
```
```py
print(df2.unstack())
```
```
             第一组列    第二组列    
             列1  列2   列1  列2
第一组行 行1    0   1    2   3
        行2    4   5    6   7
第二组行 行1    8   9   10  11
        行2   12  13   14  15
```
```py
print(df2.unstack(level=0))
```
```
        第一组列          第二组列     
      第一组行 第二组行 第一组行 第二组行
行1 列1    0     8       2      10
    列2    1     9       3      11
行2 列1    4    12       6      14
    列2    5    13       7      15
```
level等于哪层索引，哪层索引就被切换到行/列中

---

可以在unstack函数中设置参数`fill_value`，指定df重排后缺失的值
```
             第一组列    第二组列    
             列1  列2   列1  列2
第一组行 行1    0   1    2   3
        行2    4   5    6   7
第二组行 行1    8   9   10  11
        行3   12  13   14  15
```
```py
print(df.unstack(fill_value=0))
```
```
          第一组列                      第二组列                  
          列1           列2             列1             列2       
          行1 行2  行3 行1 行2  行3   行1 行2  行3  行1 行2  行3
第一组行    0  4    0   1   5    0     2  6    0    3   7    0
第二组行    8  0   12   9   0   13    10  0   14   11   0   15
```
