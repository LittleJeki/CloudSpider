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


# 读取定义好的停用词库
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords

def make_wordcloud():
    for folder in os.listdir('LRC'):
        os.chdir('E:\代码\python\CloudSpider')

        # 依次读取文件，分词，生成all_words列表，用停用词检查后生成新的all_words_new
        all_words =[]
        outstr = ''
        for filename in os.listdir('LRC/'+folder):
            with open('LRC/'+folder+'/' +filename,encoding='utf-8') as f:
                lyrics =f.read()
                data =jieba.cut(lyrics)
                all_words.extend(set(data))
        for word in all_words:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        all_words_new= outstr.split(" ")  # 转成列表

        # 对all_words中的词计数，并按照词频排序
        count =Counter(all_words_new)
        result =sorted(count.items(), key=lambda x: x[1], reverse=True)
        for r in result:
            if r[0]=='' or r[0]=='\ufeff':
                result.remove(r)
        for r in result:
            if r[0]=='\n':
                result.remove(r)
        # print(result[0:20])

        # 词云显示
        word_dic =dict(count.items())
        # 使matplotlib模块能显示中文
        mpl.rcParams['font.sans-serif'] = ['SimHei']        # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False          # 解决保存图像是负号'-'显示为方块的问题
        color_mask =imread('bg_love.jpg')                      # 背景图
        cloud =WordCloud(
            font_path='msyh.ttc',                           # 注意选择本机字体文件的地址
            width=600,
            height=480,
            background_color='black',
            mask=color_mask,
            max_words=350,
            max_font_size=150)
        world_cloud =cloud.fit_words(word_dic)
        os.chdir('word_picture')
        world_cloud.to_file(folder+'.jpg')

if __name__ == '__main__':
    stopwords = stopwordslist('stoplist.txt')
    try:
        os.mkdir('word_picture')  # 创建词云图片保存目录
    except:
        pass
    make_wordcloud()
