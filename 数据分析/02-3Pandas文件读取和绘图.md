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
- [分箱操作](#分箱操作)
    - [等距分箱](#等距分箱)
    - [等距分箱](#等距分箱-1)
- [时间序列](#时间序列)
    - [时间戳](#时间戳)
    - [各种时间数据的转换](#各种时间数据的转换)
    - [时间差](#时间差)
    - [取值与切片](#取值与切片)
    - [常用属性](#常用属性)
    - [常用方法](#常用方法)
      - [移动](#移动)
      - [频率转换](#频率转换)
      - [重采样（最常用）](#重采样最常用)
    - [时区](#时区)
- [绘图](#绘图)

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
### 分箱操作
即将连续型数据离散化，分为等距和等频分箱
可以理解成将数据按指定范围分组
##### 等距分箱
`pd.cut(series, bins=n/list, right=True, labels=list)`表示将series平均分为n组
- `bins`也可以是一个列表`[n1,n2,n3,...]`，表示分成`(n1,n2]` `(n2,n3]` `(n3,...]`的多组
- `right`设置分组区间开闭，默认是左开右闭，可以设置为False即左闭右开
- `labels`设置分组区间名称，是一个字符串列表

```
    A   B   C
a  14  74  29
b  22  12  68
c  65  80  22
d  79  29  19
e  99  89  56
```
```
# print(pd.cut(df['A'], bins=4, right=False))
a      [14.0, 35.25)
b      [14.0, 35.25)
c      [56.5, 77.75)
d    [77.75, 99.085)
e    [77.75, 99.085)
Name: A, dtype: category
Categories (4, interval[float64]): [[14.0, 35.25) < [35.25, 56.5) < [56.5, 77.75) < [77.75, 99.085)]
```
最后一行`Categories`展示了各组的范围，上面的series展示了abcde对应的数据都在哪组
可以看到默认情况下每组的距离相等
```
# print(pd.cut(df['A'], bins=[0, 30, 60, 80, 100], labels=['0-30', '30-60', '60-80', '80-100']))
a      0-30
b      0-30
c     60-80
d     60-80
e    80-100
Name: A, dtype: category
Categories (4, object): ['0-30' < '30-60' < '60-80' < '80-100']
```
这里我们指定了分组的名称
##### 等距分箱
`pd.qcut(series, q=n, labels=list)`表示将series平均分为n组
- `q`设置将数据均分成n等份
- `right`设置分组区间开闭，默认是左开右闭，可以设置为False即左闭右开
- `labels`设置分组区间名称，是一个字符串列表

```
    A   B   C
a  73   1  68
b   8  83  77
c  14  86  90
d  29  95  60
e  54  12  92
```
```
# pd.qcut(df['A'], q=4)
a     (54.0, 73.0]
b    (7.999, 14.0]
c    (7.999, 14.0]
d     (14.0, 29.0]
e     (29.0, 54.0]
Name: A, dtype: category
Categories (4, interval[float64]): [(7.999, 14.0] < (14.0, 29.0] < (29.0, 54.0] < (54.0, 73.0]]
```
可以看到各组中分别有2、1、1、1个数据，因为是5个数据分成4组，无法完全均分，所以就让第一组多一个数据
等距和等频分箱的区别在于：
- 等距分箱只确保每组的距离相等（默认情况下），不管每组中是否有数据
- 等距分箱只确保每组中数据数量尽可能相等，不管每组的具体范围是多少
### 时间序列
##### 时间戳
`pd.Timestamp("Y-M-D hour:minute:second")`创建指定时刻的时间戳，其中年份Y必须指定
``` py
print(pd.Timestamp("2000"))  # 2000-01-01 00:00:00
print(pd.Timestamp("2010-10-10"))  # 2010-10-10 00:00:00
print(pd.Timestamp("2022-12-23 20:30:45"))  # 2022-12-23 20:30:45
```
`pd.Period("Y-M-D", freq='D')`创建时期数据，参数`freq`指定创建的是年Y、月M、日D
```py
print(pd.Period('2010', freq='D'))  # 2010-01-01
print(pd.Period("2010-10-10", freq='M'))  # 2010-10
print(pd.Period("2022-12-23", freq='Y'))  # 2022
```

---

批量生成时刻/时期数据：
**时刻数据**：`pd.date_range('Y.M.D', periods=n, freq='D')`从指定时间开始，连续取n天/月/年，得到一个`DatetimeIndex`对象。特点是最后必须具体到天
**时期数据**：`pd.period_range('Y.M.D', periods=n, freq='D')`从指定时间开始，连续取n天/月/年，得到一个`PeriodIndex`对象。特点是可以只具体到年/月/日
```py
print(pd.date_range('2030.02.13', periods=4, freq='D')) 
# DatetimeIndex(['2030-02-13', '2030-02-14', '2030-02-15', '2030-02-16'], dtype='datetime64[ns]', freq='D')
print(pd.date_range('2030.02.13', periods=4, freq='M'))
# DatetimeIndex(['2030-02-28', '2030-03-31', '2030-04-30', '2030-05-31'], dtype='datetime64[ns]', freq='M')
print(pd.date_range('2030.02.13', periods=4, freq='Y'))
# DatetimeIndex(['2030-12-31', '2031-12-31', '2032-12-31', '2033-12-31'], dtype='datetime64[ns]', freq='A-DEC')
print(pd.period_range('2030.02.13', periods=4, freq='Y'))
# PeriodIndex(['2030', '2031', '2032', '2033'], dtype='period[A-DEC]', freq='A-DEC')
```
可以看到时刻数据中按月取默认是最后一天，按年取默认是最后一月的最后一天

---

时间戳索引：上面创建的时间数据一般不会单独使用，而是作为数据的索引
```py
index = pd.date_range('2010.01.02', periods=5)
print(pd.Series(np.random.randint(0, 10, size=5), index=index))
```
```
2010-01-02    6
2010-01-03    4
2010-01-04    6
2010-01-05    7
2010-01-06    0
Freq: D, dtype: int32
```
##### 各种时间数据的转换
可以将不规则的时间字符串转换成时刻数据
`pd.to_datetime(str)`其中str也可以是一个字符串列表
```py
print(pd.to_datetime('2030-03-14'))
# 2030-03-14 00:00:00
print(pd.to_datetime(['2030-03-14', '2030-3-14', '14/03/2030', '2030/3/14']))
# DatetimeIndex(['2030-03-14', '2030-03-14', '2030-03-14', '2030-03-14'], dtype='datetime64[ns]', freq=None)
```

---

时间戳也可以转换成时刻数据
`pd.to_datetime(时间戳, unit)` 其中`unit`参数指定时间戳的单位
```py
print(pd.to_datetime([1899678987], unit='s'))
# DatetimeIndex(['2030-03-14 00:36:27'], dtype='datetime64[ns]', freq=None)
print(pd.to_datetime(1899678987000, unit='ms'))
# 2030-03-14 00:36:27
```
##### 时间差
`pd.DateOffset(years/months/days/hours/seconds/minutes)`
```py
dt = pd.Timestamp("2022-12-23 20:30:45")
print(dt + pd.DateOffset(years=8))  # 2030-12-23 20:30:45
print(dt + pd.DateOffset(months=-8))  # 2022-04-23 20:30:45
print(dt - pd.DateOffset(days=8))  # 2022-12-15 20:30:45
print(dt + pd.DateOffset(hours=8))  # 2022-12-24 04:30:45
print(dt + pd.DateOffset(seconds=8))  # 2022-12-23 20:30:53
print(dt + pd.DateOffset(minutes=8))  # 2022-12-23 20:38:45
```
表示在基础时间上加减
##### 取值与切片
准备数据：
```py
index = pd.date_range('2010.01.02', periods=100)
ts = pd.Series(range(len(index)), index=index)  # ts表示以DatetimeIndex对象为索引的series
print(ts)
```
```
2010-01-02     0
2010-01-03     1
2010-01-04     2
2010-01-05     3
2010-01-06     4
              ..
2010-04-07    95
2010-04-08    96
2010-04-09    97
2010-04-10    98
2010-04-11    99
Freq: D, Length: 100, dtype: int64
```
根据索引取值：`ts[索引名]`索引名可以不是具体的`2010-04-11`日期，也可以是月/年
```py
print(ts["2010-01-03"])  # 1
print(ts["2010-1-3"])  # 1    可以省略月/日中的0
print(ts["2010-2"])  # 取整个2月的所有数据
```
```
2010-02-01    30
2010-02-02    31
2010-02-03    32
              ..
2010-02-26    55
2010-02-27    56
2010-02-28    57
Freq: D, dtype: int64
```
切片：`ts[索引名1:索引名2]`取[索引名1,索引名2]中的所有数据
```
# ts["2010-1-3":"2010-1-7"]
2010-01-03    1
2010-01-04    2
2010-01-05    3
2010-01-06    4
2010-01-07    5
Freq: D, dtype: int64
```
```
# ts["2010-2":"2010-3"]
2010-02-01    30
2010-02-02    31
2010-02-03    32
              ..
2010-03-29    86
2010-03-30    87
2010-03-31    88
Freq: D, dtype: int64
```

---

时间戳作索引进行取值/切片：`ts[时间戳]`或`ts[时间戳1:时间戳2]`
```py
print(ts[pd.Timestamp("2010-1-3")])  # 1
```

---

`DatetimeIndex`作索引进行切片：`ts[DatetimeIndex]`
```
# ts[pd.date_range('2010.02.03', periods=5, freq='D')]
2010-02-03    32
2010-02-04    33
2010-02-05    34
2010-02-06    35
2010-02-07    36
Freq: D, dtype: int64
```
##### 常用属性
准备数据：
```py
index = pd.date_range('2010.01.29', periods=5)
ts = pd.Series(range(len(index)), index=index)
print(ts)
```
```
2010-01-29    0
2010-01-30    1
2010-01-31    2
2010-02-01    3
2010-02-02    4
Freq: D, dtype: int64
```
- `ts.index`获取该series的索引（`DatetimeIndex`对象）
```
# ts.index
DatetimeIndex(['2010-01-29', '2010-01-30', '2010-01-31', '2010-02-01',
               '2010-02-02'],
              dtype='datetime64[ns]', freq='D')
```
- `ts.index.year`该`DatetimeIndex`对象的日期都是哪年的
```py
print(ts.index.year)
# Int64Index([2010, 2010, 2010, 2010, 2010], dtype='int64')
```
- `ts.index.month`是哪月的
```py 
print(ts.index.month)
# Int64Index([1, 1, 1, 2, 2], dtype='int64')
```
- `ts.index.day`是哪日的
```py 
print(ts.index.day)
# Int64Index([29, 30, 31, 1, 2], dtype='int64')
```
- `ts.index.dayofweek`是星期几的
```py 
print(ts.index.dayofweek)  
# Int64Index([4, 5, 6, 0, 1], dtype='int64')
```
##### 常用方法
###### 移动
`ts.shift(periods=1)`将数据整体往后移一位，若给负数就是往前移
准备数据：
```py
index = pd.date_range('2010.01.29', periods=5)
ts = pd.Series(range(len(index)), index=index)
print(ts)
```
```
2010-01-29    0
2010-01-30    1
2010-01-31    2
2010-02-01    3
2010-02-02    4
Freq: D, dtype: int64
```
```
# ts.shift()
2010-01-29    NaN
2010-01-30    0.0
2010-01-31    1.0
2010-02-01    2.0
2010-02-02    3.0
Freq: D, dtype: float64
```
```
# ts.shift(periods=-3)
2010-01-29    3.0
2010-01-30    4.0
2010-01-31    NaN
2010-02-01    NaN
2010-02-02    NaN
Freq: D, dtype: float64
```
###### 频率转换
即对数据进行抽样
- 由多变少：
  - `ts.asfreq(pd.tseries.offsets.Week())`天->星期
  - `ts.asfreq(pd.tseries.offsets.MonthEnd())`天->月
- 有少变多：用`fill_value`填充
  - `ts.asfreq(pd.tseries.offsets.Hour(), fill_value=0)`天->小时

```
# ts.asfreq(pd.tseries.offsets.Week())
2010-01-29    0
Freq: W, dtype: int64
```
```
# ts.asfreq(pd.tseries.offsets.MonthEnd())
2010-01-31    2
Freq: M, dtype: int64
```
```
# ts.asfreq(pd.tseries.offsets.Hour(), fill_value=0)
2010-01-29 00:00:00    0
2010-01-29 01:00:00    0
2010-01-29 02:00:00    0
                      ..
2010-02-01 22:00:00    0
2010-02-01 23:00:00    0
2010-02-02 00:00:00    4
Freq: H, Length: 97, dtype: int64
```
###### 重采样（最常用）
即对数据按一定间隔进行聚合
`ts.resample('时间间隔').聚合函数()`
- 时间间隔：`数量+S/T/H/D/W/M/Y`表示几秒/分钟/小时/天/周/月/年，如果不写数量默认为1
- 聚合函数：`sum()`、`cumsum()`等

数据：
```py
index = pd.date_range('2010.01.29', periods=365)
ts = pd.Series(range(len(index)), index=index)
```
```
# ts.resample('2D').sum()
2010-01-29      1
2010-01-31      5
2010-02-02      9
             ... 
2011-01-24    721
2011-01-26    725
2011-01-28    364
Freq: 2D, Length: 183, dtype: int64
```
```
# ts.resample('3M').sum().cumsum()
2010-01-31        3
2010-04-30     4186
2010-07-31    16836
2010-10-31    37950
2011-01-31    66430
Freq: 3M, dtype: int64
```

---

**df的重采样**：
`df.resample('时间间隔', on='列名').聚合函数()`
数据：
```py
data = {
    'price': [10, 11, 2, 12, 33, 14, 17],
    'score': [40, 30, 100, 90, 90, 80, 10],
    'week': pd.date_range('2030-3-2', periods=7, freq='W')
}
df = pd.DataFrame(data)
print(df)
```
```
   price  score       week
0     10     40 2030-03-03
1     11     30 2030-03-10
2      2    100 2030-03-17
3     12     90 2030-03-24
4     33     90 2030-03-31
5     14     80 2030-04-07
6     17     10 2030-04-14
```
对week列按月汇总，求和以及平均值：
```
# df.resample('M', on='week').sum() 
            price  score
week                    
2030-03-31     68    350
2030-04-30     31     90
```
```
# df.resample('M', on='week').apply(np.mean)
            price  score
week                    
2030-03-31   13.6   70.0
2030-04-30   15.5   45.0
```
对week列以两周为单位汇总，price求平均值、score求和
```
# df.resample('2W', on='week').agg({'price': np.mean, 'score': np.sum})
            price  score
week                    
2030-03-03   10.0     40
2030-03-17    6.5    130
2030-03-31   22.5    180
2030-04-14   15.5     90
```
上例中使用了`agg`函数，它用于处理resample后的结果，可指定对各列的处理方式
##### 时区
使用
```py
import pytz
print(pytz.common_timezones)
```
可以查看所有常用的时区名称

---

将普通的时间序列转成带有时区的格式：`ts.tz_localize(tz=时区名称)`
```py
index = pd.date_range('2010.01.29', periods=5)
ts = pd.Series(range(len(index)), index=index)
print(ts.tz_localize(tz='UTC'))  # 国际标准时间
```
```
2010-01-29 00:00:00+00:00    0
2010-01-30 00:00:00+00:00    1
2010-01-31 00:00:00+00:00    2
2010-02-01 00:00:00+00:00    3
2010-02-02 00:00:00+00:00    4
Freq: D, dtype: int64
```

---

时区转换：`ts.tz_convert(tz=新时区名称)`
注意这里的ts必须是经过`tz_localize`转换后的
```py
index = pd.date_range('2010.01.29', periods=5)
ts = pd.Series(range(len(index)), index=index)
ts = ts.tz_localize(tz='UTC')
print(ts.tz_convert(tz='Asia/Shanghai'))
```
```
2010-01-29 08:00:00+08:00    0
2010-01-30 08:00:00+08:00    1
2010-01-31 08:00:00+08:00    2
2010-02-01 08:00:00+08:00    3
2010-02-02 08:00:00+08:00    4
Freq: D, dtype: int64
```
### 绘图

