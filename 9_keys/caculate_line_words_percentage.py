__author__ = 'wanghuafeng'
#coding:utf-8
import os
import re
import time
import math
import codecs
PATH = os.path.dirname(os.path.abspath(__file__))

class FiveGram:
    def __init__(self):
        self.src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item'
        self.five_gram_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\five_gram_arithmetic_param'
    def prepare_ngram_data(self):
        '''生成first_word的total count，用以计算n元模型每个元素的的概率'''
        filename = os.path.join(self.src_data_path, 'five_gram_combine_word_freq_cutOff=1.txt')
        total_first_word_freq_dic = {}
        with codecs.open(filename, encoding='utf-8') as f:
            # while 1:
            #     line = f.readline()
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                first_word_part = ','.join(ngram_item.split(',')[:-1])
                try:
                    total_first_word_freq_dic[first_word_part] += freq_int
                except:
                    total_first_word_freq_dic[first_word_part] = freq_int
        first_word_filename = os.path.join(self.five_gram_data_path, 'five_gram_first_word_total_count.txt')
        temp_list_for_write = ['\t'.join((k, str(v)))+'\n' for k,v in total_first_word_freq_dic.items()]
        codecs.open(first_word_filename,mode='wb', encoding='utf-8').writelines(temp_list_for_write)
    # prepare_ngram_data()
    def caculate_percentage_of_each_item(self):
        '''生成每一个n元模型的权重，'''
        first_word_filename = os.path.join(self.five_gram_data_path, 'first_word_total_count.txt')
        first_word_freq_dic = {}
        with codecs.open(first_word_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                first_word_freq_dic[ngram_item] = freq_int
        combine_data_filename = os.path.join(self.src_data_path, 'five_gram_combine_word_freq_cutOff=1.txt')
        com_str_list = []
        with codecs.open(combine_data_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                first_word_of_ngram = ','.join(ngram_item.split(',')[:-1])
                freq_percentage = float(freq_int)/first_word_freq_dic[first_word_of_ngram]
                weight =  str(int(math.log10(freq_percentage)*(-200000)))
                com_str = '\t'.join((ngram_item, weight)) + '\n'
                # com_str = '\t'.join((ngram_item, str(freq_percentage))) + '\n'
                com_str_list.append(com_str)
        word_weight_filename = os.path.join(self.five_gram_data_path, 'five_gram_word_weight.txt')
        codecs.open(word_weight_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
fg = FiveGram()
fg.caculate_percentage_of_each_item()

class KNPerplexity:
    def __init__(self):
        self.src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\five_gram_arithmetic_param'
        self.word_weight_dic = {}
        self._load_word_weight()
    def _load_word_weight(self):
        word_weight_filename = os.path.join(self.src_data_path, 'five_gram_word_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splitd_line = line.split('\t')
                ngram_item = splitd_line[0]
                weight = int(splitd_line[-1])
                self.word_weight_dic[ngram_item] = weight

    def return_percentage_of_each_line(self):
        '''返回每一行测试数据的总概率'''
        varify_sample_filename = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\five_gram_arithmetic_param\varify_sentence.txt'
        sentence_weight_com_list = []
        with codecs.open(varify_sample_filename, encoding='utf-8') as f:
            for line in f.readlines():
                words_list = line.split()
                words_list_lenght = len(words_list)
                sentence_weight = 0
                for word_index in range(words_list_lenght):
                    if word_index < 4:
                        ngram_item = 'BOS' + ',' + ','.join(words_list[:word_index+1])
                        weight = self.word_weight_dic.get(ngram_item, 0)
                        sentence_weight += weight
                    elif words_list_lenght >= 4:
                        ngram_item = ','.join((words_list[word_index-4], words_list[word_index-3], words_list[word_index-2], words_list[word_index-1], words_list[word_index]))
                        weight = self.word_weight_dic.get(ngram_item, 0)
                        sentence_weight += weight
                ngram_item = ','.join((words_list[-4:])) + ',' + 'EOS'
                weight = self.word_weight_dic.get(ngram_item, 0)
                sentence_weight += weight
                com_str = line.strip() + '\t' + str(sentence_weight) + '\n'
                sentence_weight_com_list.append(com_str)
        check_out_filename = os.path.join(self.src_data_path, 'check_out_weight.txt')
        codecs.open(check_out_filename, mode='wb', encoding='utf-8').writelines(sentence_weight_com_list)
# kn = KNPerplexity()
# kn.return_percentage_of_each_line()


def gen_varify_data():
    '''生成测试数据，单字之间用空格隔开'''
    src_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\five_gram_arithmetic_param'
    filename = os.path.join(src_path, 'only_cuted_sentence_varify_sample.txt')
    total_new_line_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        for line in [item.strip().replace(' ', '') for item in f.readlines()]:
            each_line_list = []
            for single_word in line:
                each_line_list.append(single_word)
            new_line = ' '.join(each_line_list) + '\n'
            total_new_line_list.append(new_line)
    new_filename = os.path.join(src_path, 'varify_sentence.txt')
    codecs.open(new_filename, mode='wb', encoding='utf-8').writelines(total_new_line_list)
# gen_varify_data()