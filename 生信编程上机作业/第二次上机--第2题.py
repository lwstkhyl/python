import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 读取Titanic数据集
titanic_data = pd.read_csv('data/titanic.csv')

# 数据预处理：处理缺失值，转换类别变量为数值变量等
for i in range(len(titanic_data)):  # 更改列值
    if titanic_data.loc[i, 'Sex'] == 'male':
        titanic_data.loc[i, 'Sex'] = 0
    else: titanic_data.loc[i, 'Sex'] = 1
titanic_data['Sex'] = pd.to_numeric(titanic_data['Sex'])  # 更改列数据类型

# 划分特征和目标变量
X = titanic_data.drop(['Survived', 'Name'], axis=1)
y = titanic_data['Survived']
# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化并训练逻辑回归模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# 绘制混淆矩阵
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()
