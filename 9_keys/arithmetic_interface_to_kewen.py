#coding:utf-8
import os
import codecs
import itertools
class EngineArithmetic(object):
    def __init__(self):
        self.src_data_path = r'E:\SVN\linguistic_model\N_gram\bigram'
        self.ngram_weight_dic = {}
        self._load_ngram_weight()
    def _load_ngram_weight(self):
        ngram_item_filename = os.path.join(self.src_data_path, 'combine_ngram_weight.txt')
        with codecs.open(ngram_item_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                weight = int(splited_line[-1])
                self.ngram_weight_dic[ngram_item] = weight
    def caculate_weight_of_word_list(self, words_list):
        '''返回每一行测试数据的总概率'''
        words_list_lenght = len(words_list)
        sentence_weight = 0
        for word_index in range(words_list_lenght):
            if word_index == 0:
                ngram_item = words_list[0]
                weight = self.ngram_weight_dic.get(ngram_item, 250000)
                print ngram_item, weight
                sentence_weight += weight
            elif word_index == 1:
                try:
                    ngram_item = words_list[0] + words_list[1]
                    weight = self.ngram_weight_dic[ngram_item]
                except KeyError:
                    ngram_item = words_list[1]
                    weight = self.ngram_weight_dic.get(ngram_item, 150000)+100000
                print ngram_item, weight
                sentence_weight += weight
            elif word_index == 2:
                try:
                    ngram_item = words_list[0] + words_list[1] + words_list[2]
                    weight = self.ngram_weight_dic[ngram_item]
                except KeyError:
                    try:
                        ngram_item = words_list[1] + words_list[2]
                        weight = self.ngram_weight_dic[ngram_item] + 100000
                    except KeyError:
                        ngram_item = words_list[2]
                        weight = self.ngram_weight_dic.get(ngram_item, 100000)+150000
                print ngram_item, weight
                sentence_weight += weight
            elif word_index == 3:
                try:
                    ngram_item = words_list[0] + words_list[1] + words_list[2] + words_list[3]
                    weight = self.ngram_weight_dic[ngram_item]
                except KeyError:
                    try:
                        ngram_item = words_list[1] + words_list[2] + words_list[3]
                        weight = self.ngram_weight_dic[ngram_item] + 50000
                    except KeyError:
                        try:
                            ngram_item = words_list[2] + words_list[3]
                            weight = self.ngram_weight_dic[ngram_item]+100000
                        except KeyError:
                            ngram_item =  words_list[3]
                            weight = self.ngram_weight_dic.get(ngram_item, 100000)+150000
                print ngram_item, weight
                sentence_weight += weight

            else:
                try:
                    ngram_item = ''.join((words_list[word_index-4], words_list[word_index-3], words_list[word_index-2], words_list[word_index-1], words_list[word_index]))
                    weight = self.ngram_weight_dic[ngram_item]
                except KeyError:
                    try:
                        ngram_item = ''.join((words_list[word_index-3], words_list[word_index-2], words_list[word_index-1], words_list[word_index]))
                        weight = self.ngram_weight_dic[ngram_item]+10000
                    except KeyError:
                        try:
                            ngram_item = ''.join((words_list[word_index-2], words_list[word_index-1], words_list[word_index]))
                            weight = self.ngram_weight_dic[ngram_item]+50000
                        except KeyError:
                            try:
                                ngram_item = ''.join((words_list[word_index-1], words_list[word_index]))
                                weight = self.ngram_weight_dic[ngram_item]+100000
                            except KeyError:
                                ngram_item = words_list[word_index]
                                weight = self.ngram_weight_dic.get(ngram_item, 100000)+150000
                print ngram_item, weight
                sentence_weight += weight

        print sentence_weight
        return [(words_list,sentence_weight)]
    def receive_sentence_list(self, prefix_list, candidate_list, max_lenght=1000):
        '''接收sentence的列表，求出相应的权重值，并返回权重值较低的max_length个'''
        sentence_list = [list(''.join(item)) for item in itertools.product(prefix_list, candidate_list)]
        sentence_weight_tuple_list = []
        for word_list in sentence_list:
            sentence_weight_tuple = self.caculate_weight_of_word_list(word_list)
            sentence_weight_tuple_list.append(sentence_weight_tuple)
        return sorted(sentence_weight_tuple_list, key=lambda x:x[-1])[:max_lenght]

ea = EngineArithmetic()
while 1:#计算在没有路径裁剪情况下句子的实际权重
    sentence = raw_input('input your sentence:')
    word_list = [item for item in sentence.decode('utf-8')]
    ea.caculate_weight_of_word_list(word_list)
