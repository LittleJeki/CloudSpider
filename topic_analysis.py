import os
import imp
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis.sklearn

if __name__ == '__main__':
    def chinese_word_cut(text):
        return " ".join(jieba.cut(text))

    data = []
    for filename in os.listdir('LRC/许嵩'):
        cc = ''
        with open('LRC/许嵩/'+filename,encoding='utf-8') as f:
            for line in f.readlines():
                line=line.strip('\n')
                cc += line
        cc = chinese_word_cut(cc)
        data.append(cc)

    '''
        文本向量化：将文章中的关键词转换为一个个特征，然后统计关键词个数
    '''
    n_features = 20  # 只提取1000个最重要的关键词
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(data)

    n_topics = 5  # 设定主题个数
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50, learning_method='online', learning_offset=50.,
                                    random_state=0)
    result_topic = lda.fit(tf)
    # print(result_topic)

    # 显示每个主题下的前若干关键词
    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
            print()


    # n_top_words = 20
    # tf_features_names = tf_vectorizer.get_feature_names()
    # print_top_words(lda, tf_features_names, n_top_words)

    # 主题可视化
    vis = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    pyLDAvis.show(vis)