<a id="mulu">目录</a>
<a href="#mulu" class="back">回到目录</a>
<style>
    .back{width:40px;height:40px;display:inline-block;line-height:20px;font-size:20px;background-color:lightyellow;position: fixed;bottom:50px;right:50px;z-index:999;border:2px solid pink;opacity:0.3;transition:all 0.3s;color:green;}
    .back:hover{color:red;opacity:1}
    img{vertical-align:bottom;}
</style>

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [numpy的基础](#numpy的基础)
    - [数据类型](#数据类型)
- [ndarray数组](#ndarray数组)
    - [创建](#创建)
      - [列表直接创建](#列表直接创建)
      - [使用np函数创建](#使用np函数创建)
    - [常用属性](#常用属性)
    - [常用操作](#常用操作)
      - [索引](#索引)
      - [切片](#切片)
      - [应用：翻转](#应用翻转)
      - [变形](#变形)
      - [级联（合并）](#级联合并)

<!-- /code_chunk_output -->

<!-- 打开侧边预览：f1->Markdown Preview Enhanced: open...
只有打开侧边预览时保存才自动更新目录 -->

>import numpy as np
### numpy的基础
##### 数据类型
数组中常见的数据类型：
- int--int8 uint8 int16 int32 int64
- float--float16 float32 float64
- str字符串

如果需要将数据类型传入函数，就使用`np.int8`这种形式表示
### ndarray数组
##### 创建
###### 列表直接创建
`np.array(列表)`
```
lst = [1,2,3,4,5]
nd = np.array(lst)
print(nd) #[1 2 3 4 5]
print(type(nd)) #<class 'numpy.ndarray'>
```
注意：因为numpy默认ndarray中所有元素类型相同，如果传入的列表中有不同类型，则会**自动转换为同一类型**，优先级`str>float>int`
```
print(np.array([3.1,2,"string"])) #['3.1' '2' 'string']
print(np.array([3.1,3])) #[3.1 3. ]
```
###### 使用np函数创建
1. `np.ones(shape,dtype=None,order='C')`创建一个所有元素都为1的多维数组。
`shape=(m,[n,...])`控制创建m行n列的多维数组；`dtype`接收数据类型（可以是numpy的，也可以是python自带的int等）；`order`控制内存存储方式。一般只给第一个参数即可
```
n = np.ones(shape=(3,)) #创建有3个元素的一维数组
print(n) #[1. 1. 1.] 默认使用浮点数
n = np.ones(shape=(3,4),dtype=np.int8) #创建3行4列的二维数组，指定int类型
print(n) #[[1 1 1 1],[1 1 1 1],[1 1 1 1]]
#还可以有更高维，如shape=(3,4,5)
```
2. `np.zeros(shape,dtype=None,order='C')`创建一个所有元素都为0的多维数组。使用方式同上
3. `np.full(shape,fill_value,dtype=None,order='C')`创建一个所有元素都为`fill_value`的多维数组。使用方式同上
4. `np.eye(row,col,k=0,dtype=None,order='C')`创建row行col列的、主对角线（左上-右下）位置为1 其它位置为0的二维数组。其中col默认=row；k指定向右偏移k个位置，若为负数就是向左偏移
`np.eye(3,3,dtype=np.int8)`
```
[[1 0 0]
[0 1 0]
[0 0 1]]
```
`np.eye(3,5,k=2,dtype=np.int8)`
```
[[0 0 1 0 0]
[0 0 0 1 0]
[0 0 0 0 1]]
```
5. `np.linspace(start,stop,num=50,endpoint=True,retstep=False,dtype=None)`创建从start到stop的等差数列，该数列有num个数，步长根据这3个值自动进行计算；endpoint控制该数列是否包含结束值stop；retstep决定是否返回步长
```
n = np.linspace(0,10,num=6,dtype=np.int16) #默认包含结束值
print(n) #[ 0  2  4  6  8  10]
n = np.linspace(0,10,num=5,dtype=np.int16,endpoint=False,retstep=True) #设置不包含结束值
print(n) #(array([0, 2, 4, 6, 8], dtype=int16), 2.0) 可以看到结果中包含步长
```
6. `np.arrange(start=0,stop,step=1,dtype=None)`创建`[start,stop)`的步长为`step`的数组，类似于python中的`range()`。注意它**不包含结束值**
```
n1 = np.arange(10) #[0 1 2 3 4 5 6 7 8 9]
n2 = np.arange(2,10) #[2 3 4 5 6 7 8 9]
n3 = np.arange(2,10,2) #[2 4 6 8]
```
7. **重点：**`np.random.randint(low,high=None,size=None,dtype=None)`创建一个包含随机整数的多维数组：
   - 当`high=None`时，生成数范围为`[0,low)`，如果给定high值，就生成`[low,high)`的数；
   - `size`指定数组维数：`size=6`生成包含6个元素的一维数组，`size=(3,4)`生成3行4列的二维数组，更高维数也使用`(x,y,z,...)`形式创建
```
n1 = np.random.randint(10) #生成1个[0,10)的随机整数
n2 = np.random.randint(-10,11) #生成1个[-10,11)的随机整数
n3 = np.random.randint(3,size=5) #生成5个[0,3)的随机整数
n4 = np.random.randint(-2,high=3,size=(2,2)) #生成2*2的二维数组，元素取值为[-2,3)
```
8. `np.random.randn(d0,d1,...,dn)`创建一个服从标准正态分布的多维数组
```
n1 = np.random.randn() #产生一个随机数，该数服从标准正态分布
n2 = np.random.randn(10) #产生含有10个元素的一维数组，元素服从标准正态分布
n3 = np.random.randn(3,4) #产生3行4列的二维数组，元素服从标准正态分布
```
9. `np.random.normal(loc=0,scale=1,size=None)`创建一个服从正态分布的多维数组，可以指定均值和标准差
    - loc指定均值，即正态分布的中心
    - scale指定标准差，对应分布的宽度，该值越大则曲线越矮胖
    - `size`指定数组维数，同`randint`函数（`size=6`生成包含6个元素的一维数组，`size=(3,4)`生成3行4列的二维数组，更高维数也使用`(x,y,z,...)`形式创建）
```
n1 = np.random.normal(loc=100,scale=10) #产生一个随机数，该数服从正态分布，均值为100，标准差为10
n2 = np.random.normal(loc=100,size=10) #产生含有10个元素的一维数组，元素服从正态分布，均值为100，标准差为1
```
10.  `np.random.random(size=None)`创建一个元素为[0,1)的随机数的多维数组
   - `size`指定数组维数，同randint函数（`size=6`生成包含6个元素的一维数组，`size=(3,4)`生成3行4列的二维数组，更高维数也使用`(x,y,z,...)`形式创建）
```
n1 = np.random.random() #产生一个[0,1)随机数
n2 = np.random.random(size=10) #产生含有10个元素的一维数组，元素取值为[0,1)
```
11.  `np.random.rand(d0,d1,...,dn)`创建一个元素为[0,1)的随机数的多维数组，与`random`类似，参数使用同`randn`
```
n1 = np.random.rand() #产生一个随机数，该数取值为[0,1)
n2 = np.random.rand(10) #产生含有10个元素的一维数组，元素，该数取值为[0,1)
n3 = np.random.rand(3,4) #产生3行4列的二维数组，元素，该数取值为[0,1)
```
##### 常用属性
- `ndim`维度
- `shape`形状--各维度的长度
- `size`总长度
- `dtype`元素类型
```
n = np.random.rand(3,4)
print(n.ndim) #2 表示2维数组
print(n.shape) #(3, 4) 表示3行4列（第一个维度长度为3，第二个为4）
print(n.size) #3*4=12 各维度长度相乘
print(n.dtype) #float64
```
##### 常用操作
###### 索引
一维时与列表相同：
```
n = np.array([0,1,2,3,4,5])
print(n[0]) #第一个元素0
print(n[-1]) #最后一个元素5
```
多维时类似列表：
```
n = np.array([[1,2,3],[4,5,6]])
print(n[0]) #第一行[1 2 3]
print(n[0][1]) #第一行第二个数2
print(n[0,1]) #是n[0][1]简写，也可以接收负数表示倒数第x行
```
就多了一个简写方式`[1][2][-3]`->`[1,2,-3]`
使用索引也可以直接对ndarray中的数据进行修改，如：
```
n = np.array([[1,2,3],[4,5,6]])
n[0] = [10,20,30] #修改第一行为[10,20,30]
n[1] = 100 #修改第二行为[100,100,100]
print(n) #[[ 10  20  30] [100 100 100]]
```
###### 切片
与列表的切片相同，都可使用`[start:end:step]`的方式，因为一维ndarray切片与列表切片完全相同，以下展示二维的切片方法。
- 取行：
    - 取一行--`n[行索引]`
    - 取连续多行--`n[开始行索引:结束行索引]`注意是左闭右开区间
    - 取不连续的多行--`n[[行索引1,行索引2,...]]`，其中行索引可以重复，注意有两层中括号

    若取的是多行就返回一个新的二维数组，单行就返回一维数组
    ```
    n = np.array([[11,12,13],[21,22,23],[31,32,33],[41,42,43],[51,52,53]])
    n1 = n[0] #取第一行 [11 12 13]
    n2 = n[1:3] #第2-3行 [[21 22 23] [31 32 33]]
    n3 = n[[1,4,2,2]] #第2 5 3 3行 [[21 22 23] [51 52 53] [31 32 33] [31 32 33]]
    ```
- 取列：
  - 取一列--`n[:,列索引]`表示取指定列的所有行
  - 取连续的多列--`n[:,开始列索引:结束列索引]`
  - 取不连续的多列--`n[:,[列索引1,列索引2,...]]`

  若取的是多列就返回一个新的二维数组，单列就返回一维数组
  ```
  n = np.array([[11,12,13],[21,22,23],[31,32,33],[41,42,43],[51,52,53]])
  n1 = n[:,0] #取第一列 [11 21 31 41 51]
  n2 = n[:,0:2] #第1-2列 [[11 12] [21 22] [31 32] [41 42] [51 52]]
  n3 = n[:,[1,0,0]] #第2 1 1列 [[12 11 11] [22 21 21] [32 31 31] [42 41 41] [52 51 51]]
  ```
- 取行列：就是把上面两个合起来，中间用`,`隔开
  ```
  n = np.array([[11,12,13],[21,22,23],[31,32,33],[41,42,43],[51,52,53]])
  n1 = n[1:3,0] #取第2-3行的第一列 [21 31]
  n2 = n[1,0:2] #第2行第1-2列 [21 22]
  n3 = n[[1,3],[0,2]] #第2 4行的第1 3列 [21 43]
  ```
  注意最后一行代码的实际意思是取`第2行第一列+第4行第3列`，而不是取`第2行第1 3列+第4行第1 3列`
###### 应用：翻转
>`n = np.array([[11,12,13],[21,22,23],[31,32,33],[41,42,43],[51,52,53]])`
```
[[11 12 13]
 [21 22 23]
 [31 32 33]
 [41 42 43]
 [51 52 53]]
```
行翻转：`n1 = n[::-1]`
```
[[51 52 53]
 [41 42 43]
 [31 32 33]
 [21 22 23]
 [11 12 13]]
```
列翻转：`n2 = n[:,::-1]` 
```
[[13 12 11]
 [23 22 21]
 [33 32 31]
 [43 42 41]
 [53 52 51]]
```
***
例：对一张图片进行翻转
```
import numpy as np
import matplotlib.pyplot as plt
pic = plt.imread('active.png')
print(pic.shape) #(32, 102, 4) pic是一个三维数组，前两个维度分别是宽度，第三个维度是颜色
pic = pic[::-1] #上下翻转
pic = pic[:,::-1] #左右翻转
pic = pic[:,:,::-1] #翻转第三个维度（无实际意义），将会改变图片整体的配色
pic = pic[::10,::10] #隔10像素取一个值，对图片作模糊处理
plt.imshow(pic) #显示图片
```
###### 变形
使用reshape改变数组形状
```
n = np.arange(1,21)
print(n) #[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20]
print(n.shape) #(20,)
```
默认状态下n是长度为20的一维数组
```
n2 = n.reshape((4,5)) #将n变为4行5列的二维数组
print(n2)
[[ 1  2  3  4  5]
 [ 6  7  8  9 10]
 [11 12 13 14 15]
 [16 17 18 19 20]]
n3 = n2.reshape(20) #变成长度为20的一维数组
print(n3) #[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20]
n4 = n2.reshape((5,4)) #变成5行4列的二维数组
print(n4) 
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]
 [13 14 15 16]
 [17 18 19 20]]
```
若变形后的size不等于原size会报错：
```
n = n3.reshape(19) #新size较小，报错
n = n3.reshape((5,5)) #新size较大，报错
```
***
使用-1表示任意剩余维度长度
```
n = np.arange(1,21)
n2 = n.reshape(4,-1) #表示第一个维度为4，第二个维度根据size进行自动补齐，最后生成4行5列的数组
n3 = n.reshape(-1,5) #指定5列->4行5列的二维数组
print(n2)
[[ 1  2  3  4  5]
 [ 6  7  8  9 10]
 [11 12 13 14 15]
 [16 17 18 19 20]]
print(n3)
[[ 1  2  3  4  5]
 [ 6  7  8  9 10]
 [11 12 13 14 15]
 [16 17 18 19 20]]
n4 = n2.reshape(-1)
print(n4) #[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20]
```
注意reshape中只允许出现一个-1
```
n4 = n2.reshape(3,-1) #报错，20不能被3整除，无法生成3行n列的数组
n4 = n2.reshape(-1,-1) #报错
```
###### 级联（合并）
`np.concatenate((n1,n2),axis=0)`将n1和n2合并
- axis控制按哪个维度合并，默认为0（第一个维度）；对于二维数组，第一个维度为行，第二个为列

```
n1 = np.arange(1,21).reshape(4,-1)
n2 = np.arange(21,41).reshape(4,-1)
print(n1)
[[ 1  2  3  4  5]
 [ 6  7  8  9 10]
 [11 12 13 14 15]
 [16 17 18 19 20]]
print(n2)
[[21 22 23 24 25]
 [26 27 28 29 30]
 [31 32 33 34 35]
 [36 37 38 39 40]]
```
```
print(np.concatenate((n1,n2))) #默认按行合并（上下合并）
[[ 1  2  3  4  5]
 [ 6  7  8  9 10]
 [11 12 13 14 15]
 [16 17 18 19 20]
 [21 22 23 24 25]
 [26 27 28 29 30]
 [31 32 33 34 35]
 [36 37 38 39 40]]
```
```
print(np.concatenate((n1,n2),axis=1)) #按列合并（左右合并）
[[ 1  2  3  4  5 21 22 23 24 25]
 [ 6  7  8  9 10 26 27 28 29 30]
 [11 12 13 14 15 31 32 33 34 35]
 [16 17 18 19 20 36 37 38 39 40]]
```
注意合并时对应方向的行数/列数要相同（np包不支持用NaN补齐）
***
`np.hstack((n1,n2))`水平级联（左右合并），相当于上面的`
np.concatenate((n1,n2))`
`np.vstack((n1,n2))`垂直级联（上下合并），相当于上面的`
np.concatenate((n1,n2),axis=1)`
