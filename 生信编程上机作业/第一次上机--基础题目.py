def find_even():  # 计算并打印出从1到10的所有偶数
    for i in range(1, 11):
        if i % 2 == 0:
            print(i)
    return
def sum():  # 计算输入的两个数字和
    a = int(input("请输入数字1："))
    b = int(input("请输入数字2："))
    print(a+b)
    return a+b
def find_minmax(l:list):  # 找出给定列表中的最大值和最小值
    min = max = l[0]
    for i in l:
        if i < min:
            min = i
        if i > max:
            max = i
    print(f"最大值：{max}")
    print(f"最小值：{min}")
    return max,min
def huiwenstr(s:str):  # 判断输入的字符串是否为回文字符串
    return s[::-1] == s
def shulie(n:int):  # 生成斐波那契数列的前n个数字
    if n <= 0:
        print("输入数据有误")
        return []
    if n == 1:
        return [1]
    n1 = n2 = 1  # 第1和2项都为1
    count = 2  # 已得到的数列元素个数
    res = [1, 1]  # 创建空列表
    while count < n:
        nn = n1 + n2  # 得到下一项的值
        res.append(nn)  # 将下一项添加到结果列表中
        n1 = n2
        n2 = nn  # 更新数值
        count += 1  # 将已得到的数列元素个数+1
    return res

print("1-10的偶数：")
find_even()
print("---------------------------------------")
print("求和：")
sum()
print("---------------------------------------")
l = [3,1,0,-1,5,6,6,7,1]
print(l)
find_minmax(l)
print("---------------------------------------")
print("回文字符串：")
a = input("请输入字符串：")  # abcba
b = input("请输入字符串：")  # abb
print(f"{a}是回文字符串--{huiwenstr(a)}")
print(f"{b}是回文字符串--{huiwenstr(b)}")
print("---------------------------------------")
n = int(input("请输入正整数："))
print(f"前{n}个数是", shulie(n))
n = int(input("请输入正整数："))
print(f"前{n}个数是", shulie(n))