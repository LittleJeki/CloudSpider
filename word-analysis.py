#IR-project3-sometimes
#2018-6-12 update
#author:dzj_manhao

#part-3 word-analysis

import os
from collections import Counter
import  jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
from pylab import mpl


# 第一步：定义停用词库
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords

stopwords =stopwordslist('stoplist.txt')

# 第二步：读取文件，分词，生成all_words列表，用停用词检查后生成新的all_words_new
all_words =[]
outstr = ''
for filename in os.listdir('LRC/张杰'):
    with open('LRC/张杰/' +filename,encoding='utf-8') as f:
        lyrics =f.read()
        data =jieba.cut(lyrics)
        all_words.extend(set(data))
for word in all_words:
    if word not in stopwords:
        if word != '\t':
            outstr += word
            outstr += " "
all_words_new= outstr.split(" ")  # 转成列表

# 第三步：对all_words中的词计数，并按照词频排序
count =Counter(all_words_new)
result =sorted(count.items(), key=lambda x: x[1], reverse=True)
# print(result)

# 第四步，词云显示
# 将频率变成字典
word_dic =dict(count.items())
# 使matplotlib模块能显示中文
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
color_mask =imread('love.jpg')  # 背景图
cloud =WordCloud(
    font_path='msyh.ttc',
    width=600,
    height=480,
    background_color='black',
    mask=color_mask,
    max_words=350,
    max_font_size=150)
world_cloud =cloud.fit_words(word_dic)
world_cloud.to_file('zhangjie.jpg')