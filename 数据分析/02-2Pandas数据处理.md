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
    ```
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
    ```
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
