__author__ = 'wanghuafeng'
#coding:utf-8
import os
import re
import time
import codecs
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()
def remove_repeat():
    filename = os.path.join(PATH, '0709modify', 'cuted_varify_sample.txt')
    with codecs.open(filename, encoding='utf-8') as f:
        line_set =  set(f.readlines())
    codecs.open(filename, mode='wb', encoding='utf-8').writelines(line_set)
# remove_repeat()
def get_average_length_of_line():
    '''求出样本空间中所有句子的平均长度'''
    filename = os.path.join(PATH, '0709modify', 'unigram', 'only_cuted_sentence_varify_sample.txt')
    word_count = 0
    with codecs.open(filename, encoding='utf-8')as f:
        for line in f.readlines():
            splited_line = line.split()
            word_count += len(splited_line)
    print word_count/1356076.0
def get_words_accuracy_top_one():
    '''样本文件中词的准确度AW'''
    from cut_sentence_26 import Cut_Sentence
    matched_words_count = 0
    # total_words_count = 312525.0
    cs = Cut_Sentence()
    correct_sentence_set = set()
    total_top_one_sentence_list = []
    top_one_sentence_list = []
    correct_sentence_list = []
    checkout_filename = os.path.join(PATH, 'data', 'cut_path_lenght_26_keys_limit_100.txt')
    with codecs.open(checkout_filename, encoding='utf-8') as f:
        count = 0
        for line in f.readlines():
            if line.startswith('*'):
                correct_sentence_list.extend(cs.cut_with_weight(line.strip()[1:]))
                correct_sentence_set = cs.cut_with_weight(line.strip()[1:])
                count = 0
            else:
                count += 1
                if count == 1:
                    sentence = line.split('\t')[0]
                    total_top_one_sentence_list.extend(cs.cut_with_weight(sentence))
                    # total_top_one_sentence_list.extend(sentence.split())
                    top_one_sentence_list = cs.cut_with_weight(sentence)
                    for words in top_one_sentence_list:
                        if words in correct_sentence_set:
                            matched_words_count += 1
    print len(total_top_one_sentence_list), len(correct_sentence_list)
    print str(matched_words_count/float(len(total_top_one_sentence_list))*100)+'%'
get_words_accuracy_top_one()
def get_sentence_accuracy_top_n():
    '''样本文件中句子的精确度AS'''
    checkout_filename = os.path.join(PATH, 'data', 'cut_path_lenght_26_keys_limit_100.txt')
    top_n_sentence_list = []
    correct_sentence = ''
    matched_sentence_count = 0
    total_count = 0
    top_count = 5
    with codecs.open(checkout_filename, encoding='utf-8')as f:
        for line in f.readlines():
            if line.startswith('*'):
                total_count += 1
                if correct_sentence in top_n_sentence_list[:top_count]:
                    matched_sentence_count += 1
                top_n_sentence_list[:] = []
                correct_sentence = line.strip()[1:]
            else:
                sentence = line.split('\t')[0].replace(' ','')
                top_n_sentence_list.append(sentence)
    print total_count, matched_sentence_count
    print str(matched_sentence_count/float(total_count)*100)+'%'
# get_sentence_accuracy_top_n()
def get_lenght_of_file():
    '''获取训练语料的句子数目'''
    filename = os.path.join(PATH, 'cuted_linguistic_data.txt')
    f = open(filename)
    count = 1
    while 1:
        line = f.readline()
        if not line:
            count += 1
            print count
            break
        else:
            count += 1
# get_lenght_of_file()
def get_total_count_of_linguistic_sample():
    '''计算训练语料的词数，字数'''
    total_words_count = 0
    total_single_count = 0
    path = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample')
    for file_count in range(1,29):
        print file_count
        filename = os.path.join(path, '%s.txt'%file_count)
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                total_words_count += len(line.split())
                line_without_space = line.replace(' ', '').strip()
                total_single_count += len(line_without_space)
    print total_words_count
    print total_single_count
# get_total_count_of_linguistic_sample()
def get_total_count_of_varify_sample():
    '''计算验证语料的词数，字数'''
    total_words_count = 0
    total_single_count = 0
    filename = os.path.join(PATH, '0709modify', 'unigram', 'only_cuted_sentence_varify_sample.txt')
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            total_words_count += len(line.split())
            line_without_space = line.replace(' ', '').strip()
            total_single_count += len(line_without_space)
    print total_words_count
    print total_single_count
# get_total_count_of_varify_sample()
def bigram_total_freq():
    '''二元模型频度值和'''
    path = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample')
    total_freq_count = 0
    for file_count in range(1,29):
        print file_count
        filename = os.path.join(path, '%s_bigram.txt'%file_count)
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                # print 'num '+line.split('\t')[-1].strip()
                total_freq_count += int(line.split('\t')[-1])
                # print total_freq_count
                # time.sleep(1)
    print total_freq_count
# bigram_total_freq()
def chose_not_top_one():
    '''筛选出不匹配top_one的句子'''
    checkout_filename = os.path.join(PATH, '0709modify', 'checkout.txt')
    top_n_sentence_list = []
    correct_sentence = ''
    matched_sentence_count = 0
    total_count = 0
    top_count = 5
    with codecs.open(checkout_filename, encoding='utf-8')as f:
        for line in f.readlines():
            if line.startswith('*'):
                total_count += 1
                if correct_sentence in top_n_sentence_list[:top_count]:
                    matched_sentence_count += 1
                else:
                    print correct_sentence
                    time.sleep(1)
                top_n_sentence_list[:] = []
                correct_sentence = line.strip()[1:]
            else:
                sentence = line.split('\t')[0].replace(' ','')
                top_n_sentence_list.append(sentence)
# chose_not_top_one()
# from  cut_sentence import Cut_Sentence
# ws = Cut_Sentence()
# word = u'看到医生版的照片'
# print ' '.join(ws.cut_with_weight(word))