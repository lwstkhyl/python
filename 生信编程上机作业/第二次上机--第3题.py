import wikipedia

# 从指定的txt文件中读取关键字列表
def get_keywords(file_path:str):
    with open(file_path, 'r') as file:  # 以只读方式打开文件
        # txt文件中每个关键词独占一行
        keywords = [line.strip() for line in file.readlines()]
        # 列表生成式，每个元素是txt文件中的一行，strip用于给这行字符去除前后两侧的空格等字符，这样得到的就是一个单词
    return keywords

# 获取关键字的summary，以字典形式
def get_summaries(keywords:list):
    summaries_dict = {}  # 创建空字典
    for keyword in keywords:
        try:
            summary = wikipedia.summary(keyword)  # 获取该关键字的summary
            summaries_dict[keyword] = summary  # 向字典中添加元素
        except wikipedia.exceptions.DisambiguationError as e:  # 如果该关键字有歧义，
            summary = wikipedia.summary(e.options[0])  # 就以第一个搜索结果作为summary的结果？
            summaries_dict[keyword] = summary
        except wikipedia.exceptions.PageError:  # 如果该关键字不存在
            summaries_dict[keyword] = '0'  # 不添加summary，单独设置为'0'标识为不存在
            print(f"Page for '{keyword}' does not exist.")
    return summaries_dict

# 将摘要保存到输出文件中
def save_summaries(summaries_dict:dict, output_file:str):
    with open(output_file, 'w') as file:  # 以覆盖写入方式打开文件
        index = 0  # 关键字序号
        for keyword, summary in summaries_dict.items():  # 遍历字典元素
            index += 1
            if summary == '0':  # 如果该关键字不存在
                file.write(f"({index})Keyword: {keyword}不存在\n\n")
            else:
                file.write(f"({index})Keyword: {keyword}\nSummary:\n{summary}\n\n")  # 将关键字和summary写入文件

# 指定输入和输出文件路径
input_file_path = "D:/python_project/0525/data/input_keywords.txt"
output_file_path = 'D:/python_project/0525/summaries.txt'
keywords = get_keywords(input_file_path)  # 读取关键字列表
#print(keywords)
summaries_dict = get_summaries(keywords)  # 获取摘要
#save_summaries({'a':'bbbbbbbbbbaa','b':'aaaaaaaaa','c':'0','d':'11111111111111','e':"333333333"}, output_file_path)  # 保存到文件中
save_summaries(summaries_dict, output_file_path)  # 保存到文件中
#print(wikipedia.summary('python'))