# 导入所需库
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import networkx as nx

# 读取转录组数据集
transcriptome_data = pd.read_excel('C:/Users/33016/Desktop/助教/生物信息Perl编程第二次上机/GSE238099_count.annot_第一题参考数据.xlsx')

transcriptome_data = transcriptome_data.replace(0, np.nan)  # 将0替换为NaN，便于处理缺失值
transcriptome_data.dropna(thresh=6, inplace=True)  # 剔除NaN值超过6个的行
transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6','t-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']] = transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6','t-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']].fillna(transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6','t-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']].mean())

from sklearn.preprocessing import MinMaxScaler
# 数据标准化
scaler = MinMaxScaler()

# 对指定列进行 min-max 归一化
transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6',
                    't-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']] = scaler.fit_transform(
    transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6',
                        't-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']])

# 计算 Ctrl 组和 KD 组的平均值
transcriptome_data['Ctrl_mean'] = transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6']].mean(axis=1)
transcriptome_data['KD_mean'] = transcriptome_data[['t-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']].mean(axis=1)

# 计算 fold change
transcriptome_data['fold_change'] = transcriptome_data['KD_mean'] / transcriptome_data['Ctrl_mean']
p_values = []
transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6',
                    't-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']] = transcriptome_data[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6',
                                                                                                    't-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']].astype(float)
# 定义自由度
df = 6  # 自由度等于样本数减去1
from scipy.stats import t
def calculate_p_value(row):
    ctrl_expr = row[['t-Cont1', 't-Cont2', 't-Cont3', 't-Cont4', 't-Cont5', 't-Cont6']]
    kd_expr = row[['t-KD1', 't-KD2', 't-KD3', 't-KD4', 't-KD5', 't-KD6']]

    # 计算均值和标准差
    ctrl_mean = ctrl_expr.mean()
    kd_mean = kd_expr.mean()
    ctrl_std = ctrl_expr.std(ddof=1)
    kd_std = kd_expr.std(ddof=1)

    # 计算标准误差
    stderr = np.sqrt(ctrl_std ** 2 / len(ctrl_expr) + kd_std ** 2 / len(kd_expr))

    # 计算 t 值
    t_value = (kd_mean - ctrl_mean) / stderr

    # 计算双尾检验的 p 值
    p_value = 2 * t.cdf(-np.abs(t_value), df)

    return p_value


# 使用apply函数按行计算p值
transcriptome_data['p_value'] = transcriptome_data.apply(calculate_p_value, axis=1)
transcriptome_data = transcriptome_data[~transcriptome_data['p_value'].isna()]
# 定义 fold change 阈值
fold_change_threshold = 2

# 筛选差异基因
differentially_expressed_genes = transcriptome_data[(transcriptome_data['fold_change'] >= fold_change_threshold) | (transcriptome_data['fold_change'] <= 0.5)]

# 计算不同样本类型之间基因表达的差异
control_mean = transcriptome_data['Ctrl_mean'].mean()
kd_mean = transcriptome_data['KD_mean'].mean()
differential_genes_count = len(differentially_expressed_genes)

# 输出统计摘要信息
print("Ctrl 组平均表达量:", control_mean)
print("KD 组平均表达量:", kd_mean)
print("差异基因数:", differential_genes_count)

# 设置图形大小
plt.figure(figsize=(10, 6))

# 定义阈值
fold_change_threshold = 2
p_value_threshold = 0.05

# 绘制所有基因的散点图
plt.scatter(transcriptome_data.index, transcriptome_data['fold_change'], color='gray', alpha=0.5, label='All Genes')

# 标记差异基因
diff_genes = transcriptome_data[(transcriptome_data['fold_change'] >= fold_change_threshold) |
                                (transcriptome_data['fold_change'] <= 1/fold_change_threshold)]
transcriptome_data['-log10p_value'] = -np.log10(transcriptome_data['p_value'])

# 计算log2 fold change
transcriptome_data['log2_fold_change'] = np.log2(transcriptome_data['fold_change'])

# 设置图形大小
plt.figure(figsize=(10, 6))

# 绘制火山图
plt.scatter(transcriptome_data['log2_fold_change'], transcriptome_data['-log10p_value'], color='gray', alpha=0.5, label='All Genes')

# 标记差异基因
diff_genes = transcriptome_data[(transcriptome_data['fold_change'] >= fold_change_threshold) |
                                (transcriptome_data['fold_change'] <= 1/fold_change_threshold)]
plt.scatter(diff_genes['log2_fold_change'], diff_genes['-log10p_value'], color='red', label='Differentially Expressed Genes')

# 添加阈值线
plt.axhline(y=-np.log10(p_value_threshold), color='r', linestyle='--', label='-log10p Threshold')

# 添加标题和标签
plt.title('Volcano Plot')
plt.xlabel('log2 Fold Change')
plt.ylabel('-log10p Value')

# 添加图例
plt.legend()

# 显示图形
plt.show()

# 基因关联网络构建
# 这里假设你有基因间的相关性数据，可以根据相关性构建网络
# 这里只提供一个简单的示例
G = nx.Graph()
# 添加节点
G.add_nodes_from(transcriptome_data.columns)
# 添加边
# 以下是一个简单的示例
# for i in range(len(correlation_matrix)):
#     for j in range(i+1, len(correlation_matrix)):
#         if correlation_matrix[i][j] > threshold:
#             G.add_edge(transcriptome_data.columns[i], transcriptome_data.columns[j])

# 绘制网络
nx.draw(G, with_labels=True)
plt.title('Gene Correlation Network')
plt.show()