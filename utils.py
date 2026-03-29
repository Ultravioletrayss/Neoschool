# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 20:17:23 2026

@author: pathouli
"""
# 导入正则表达式模块（用于文本清洗）
import re
def clean_txt(str_in):
    """
    清洗文本函数：移除特殊字符，只保留字母、空格和撇号，并转换为小写
    参数:
        str_in (str): 输入的原始文本字符串
    返回:
        str: 清洗后的文本（小写，只包含字母和空格）
    """
    # 使用正则表达式替换所有非字母和非撇号的字符为空格，然后去除首尾空格并转小写
    cln_txt = re.sub("[^A-Za-z']+", " ", str_in).strip().lower()
    return cln_txt


def file_opener(p_in, f_n):
    """
    文件打开器函数：读取文件内容并进行清洗
    
    参数:
        p_in (str): 文件路径前缀（目录路径）
        f_n (str): 文件名
    
    返回:
        str: 清洗后的文件内容，如果打开失败则返回空字符串
    """
    try:
        l_t = ""  # 初始化变量用于存储文件内容
        # 以只读模式打开文件，编码为 UTF-8
        # f = open(p_in + f_n, "r", encoding="UTF8")
        # # 读取文件全部内容
        # l_t = f.read()
        # # 关闭文件
        # f.close()

        with open(p_in + f_n, 'r', encoding='UTF8') as f:
            l_t = f.read()
        # 使用 clean_txt 函数清洗文本内容
        l_t = clean_txt(l_t)



    except Exception as e:
        # 如果文件打开失败，打印错误信息
        print ("Can't open", p_in + f_n)
        print("Error type:", type(e).__name__)
        print("Error message:", e)
        pass  # 跳过异常，继续执行
    return l_t

def file_crawler(p_in):
    """
    文件爬虫函数：遍历目录下所有文件并提取内容
    
    参数:
        p_in (str): 要遍历的根目录路径
    
    返回:
        pandas.DataFrame: 包含文件内容和标签的数据框
            - body 列：文件的清洗后内容
            - label 列：文件所在目录名作为标签
    """
    # 导入操作系统接口模块
    import os
    # 导入 pandas 数据处理库
    import pandas as pd
    # 初始化空的数据框用于存储结果
    m_pd = pd.DataFrame()
    # 使用 os.walk 遍历目录树（topdown=False 表示从下往上遍历）
    for root, dirs, files in os.walk(p_in, topdown=False):
       # 从完整路径中提取最后一层目录名作为标签
       lab_t = root.split("/")[-1]
       # 构建当前目录的路径
       tmp_p = root + "/"
       # 遍历当前目录下的所有文件
       for name in files:
          # 调用 file_opener 读取并清洗文件内容
          tmp_txt = file_opener(tmp_p, name)
          # 如果读取的内容不为空
          if tmp_txt != "":
              # 创建临时数据框，包含内容（body）和标签（label）
              t_pd = pd.DataFrame(
                  {"body": tmp_txt, "label": lab_t}, index=[0])
              # 将临时数据框拼接到主数据框中
              m_pd = pd.concat([m_pd, t_pd], ignore_index=True)
    # 返回包含所有文件内容和标签的数据框
    return m_pd

def word_freq_redux(c_in):
    """
    词频统计函数：统计输入文本中每个单词的出现频率
    
    参数:
        c_in (str): 输入的文本字符串（单词间用空格分隔）
    
    返回:
        dict: 单词频率字典，键为单词，值为出现次数
    """
    # 导入 collections 模块（用于计数）
    import collections
    # 使用 Counter 统计单词频率，并转换为字典
    print(c_in.split(),type(c_in.split()))
    wrd_frequency_ctr = dict(
        collections.Counter(c_in.split()))
    print(wrd_frequency_ctr,type(wrd_frequency_ctr))
    return wrd_frequency_ctr

def all_dictionary(df_in, col_n):
    # 初始化空字典用于存储结果
    m_dict = dict()
    # 使用 pandas 的 str.cat 方法将指定列的所有文本连接成一个大字符串（用空格分隔）
    c_str = df_in[col_n].str.cat(sep=" ")
    # 调用 word_freq_redux 生成整体词频字典，存入 'all' 键
    m_dict["all"] = word_freq_redux(c_str)
    # 遍历所有唯一的标签（label）
    for top in list(df_in["label"].unique()):
        # 筛选出当前标签对应的所有行
        t_t = df_in[df_in["label"] == top]
        # 生成当前类别的词频字典
        m_dict[top] = word_freq_redux(t_t[col_n].str.cat(sep=" "))
    # 返回包含所有字典的结果
    return m_dict

def rem_sw(str_in):
    """
    移除停用词函数：从文本中移除英语停用词
    
    参数:
        str_in (str): 输入的文本字符串
    
    返回:
        str: 移除了停用词后的文本
    """
    #import nltk
    #nltk.download('stopwords')
    # 从 NLTK 语料库导入停用词列表
    from nltk.corpus import stopwords
    # 获取英语停用词集合并转换为列表（使用 set 去重）
    sw = list(set(stopwords.words('english')))
    # 初始化临时列表用于存储过滤后的单词
    tmp_ar = list()
    # 遍历输入文本中的每个单词
    for w in str_in.split():
        # 如果单词不在停用词列表中
        if w not in sw:
            # 添加到结果列表
            tmp_ar.append(w)
    # 将列表重新连接为字符串（用空格分隔）
    tmp_ar = " ".join(tmp_ar)
    return tmp_ar

def ps_lemma(str_in, sw_in):
    """
    词干提取/词形还原函数：对文本进行词干提取或词形还原处理
    
    参数:
        str_in (str): 输入的文本字符串
        sw_in (str): 选择处理方式，可选值：
            - 'ps': 使用 PorterStemmer 进行词干提取
            - 其他值：使用 WordNetLemmatizer 进行词形还原
    
    返回:
        str: 处理后的文本
    """
    # 从 NLTK 导入词干提取器和词形还原器
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    # 根据参数选择使用哪种处理方式
    if sw_in == "ps":
        # 创建 Porter 词干提取器实例
        ps = PorterStemmer()
    else:
        # 创建 WordNet 词形还原器实例
        ps = WordNetLemmatizer()
    # 初始化临时列表用于存储处理后的单词
    tmp_ar = list()
    # 遍历输入文本中的每个单词
    for c in str_in.split():
        # 根据选择的处理方式调用相应的方法
        if sw_in == "ps":
            # 使用词干提取
            tmp_ar.append(ps.stem(c))
        else:
            # 使用词形还原
            tmp_ar.append(ps.lemmatize(c))
    # 将处理后的单词列表重新连接为字符串
    tmp_ar = " ".join(tmp_ar)
    return tmp_ar
