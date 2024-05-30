import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

plt.rcParams['axes.unicode_minus'] = False  # 解决图中不显示负号的问题
data = pd.read_table("data/GSE5583_series_matrix.txt", comment='!', index_col=0)  # 忽略以!开头的行，并将第一列（即基因名称列）作为行索引
print(data.head())  # 查看data的前5行
data2 = np.log2(data + 0.0001)  # log2标准化
print(data2.head())  # 查看data2的前5行
data2.plot(kind='box', title='GSE5583 Boxplot', rot=90)  # 每个阵列的箱线图
plt.show()
data2.plot(kind='density', title='GSE5583 Density')  # 查看不同样本之间是否有总体差异
plt.show()
wt = data2.loc[:, 'WT.GSM130365': 'WT.GSM130367'].mean(axis=1)  # 每个基因（行）wt样本的表达平均值
ko = data2.loc[:, 'KO.GSM130368': 'KO.GSM130370'].mean(axis=1)  # 每个基因（行）ko样本的表达平均值
fold = ko - wt  # 折叠变化
plt.hist(fold)  # 折叠变化的直方图
plt.title("Histogram of fold-change")
plt.show()
# 查看基因差异的P值分布
p_value = []
number_of_genes = len(data2)  # 基因数量，即data数组的行数
for i in range(0, number_of_genes):
    t_test = stats.ttest_ind(data2.iloc[i, 0:3], data2.iloc[i, 3:6])  # data2.iloc[i,0:3]就是数据的前3列，即wt样本
    p_value.append(t_test[1])
plt.hist(-np.log(p_value))
plt.title("Histogram of p-value")
plt.show()
