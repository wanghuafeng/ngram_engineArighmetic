__author__ = 'wanghuafeng'
#coding:utf8
import os
import re
import sys
import math
import time
import copy
import psutil
import itertools
import codecs
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()
MAX_LENGHT = 100
class EngineArithmetic:
    def __init__(self):
        self.real_prefix_set = set()
        self.total_mapping_dic = {}
        self.word_weight_dic = {}
        self._real_prefix_rolenum()
        self._load_mapping_rolenum_wordlist()
        self._load_word_weigh()
        self.start_time = time.time()
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_filename = os.path.join(PATH, '0709modify', 'prefix_if_mapping_role_num.txt')
        with codecs.open(real_prefix_filename, encoding='utf-8') as f:
            self.real_prefix_set = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与权重构成字典'''
        word_weight_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_weight_.txt')
        # word_weight_filename = os.path.join(PATH, '0709modify',  'aaaaaaaaaaaa_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            words_weight_list = [(item.split('\t')[0], int(item.split('\t')[1].strip())) for item in f.readlines()]
            self.word_weight_dic = dict(words_weight_list)
    def handle_key_input_str(self, key_input, top_count=1):
        key_input = key_input.strip()
        matched_route_list = [('#',[],0)]
        prefix_route_list = []
        lenght_key_input = len(key_input)
        key_input_index = 0
        for key in key_input:
            #key是否有mapping匹配
            temp_matched_route_list = []
            temp_prefix_route_list = []
            key_mapping_word_list = self.total_mapping_dic.get(key)

            #如果key有汉字匹配
            if key_mapping_word_list:
                #对matched_route_list的影响
                for mapping_word in key_mapping_word_list:
                    for last_matched_route_param in matched_route_list:
                        #matched_route_list三元组中汉字部分是否为空数组
                        if last_matched_route_param[1]:
                            # bigram_item = ','.join((last_matched_route_param[1][-1], mapping_word))
                            bigram_item = last_matched_route_param[1][-1]+','+ mapping_word
                            # bigram_item = (last_matched_route_param[1][-1], mapping_word)
                            weight = self.word_weight_dic.get(bigram_item)
                            #如果查不到bigram_item对应的weight
                            if not weight:
                                # bigram_item = ','.join((last_matched_route_param[1][-1], '*'))
                                bigram_item = last_matched_route_param[1][-1]+','+ '*'
                                # bigram_item = (last_matched_route_param[1][-1], '*')
                                weight = self.word_weight_dic.get(bigram_item)
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight + last_matched_route_param[-1]
                            # new_matched_route_param = ('#', new_matched_word_list, new_weight)
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                        #key_input_str中的第一个key有匹配
                        else:
                            # bigram_item = ','.join(('BOS', mapping_word))
                            bigram_item = 'BOS'+','+ mapping_word
                            weight = self.word_weight_dic.get(bigram_item)
                            if not weight:
                                # bigram_item = ','.join(('BOS', '*'))
                                bigram_item = 'BOS'+','+'*'
                                weight = self.word_weight_dic.get(bigram_item)
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight + last_matched_route_param[-1]
                            # new_matched_route_param = ('#', new_matched_word_list, new_weight)

                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                ##对prefix_route_list的影响
                for last_matched_route_param in matched_route_list:
                    prefix_route_word_list = last_matched_route_param[1] + []
                    prefix_route_weight = last_matched_route_param[-1]
                    # prefix_route_param = (key, prefix_route_word_list, prefix_route_weight)
                    temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

            #key不匹配mapping_word
            else:
                ##对prefix_route_list的影响
                for last_matched_route_param in matched_route_list:
                    prefix_route_word_list = last_matched_route_param[1] + []
                    prefix_route_weight = last_matched_route_param[-1]
                    # prefix_route_param = (key, prefix_route_word_list, prefix_route_weight)
                    temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

            if len(temp_matched_route_list)>MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                temp_matched_route_list = temp_matched_route_list[:MAX_LENGHT]
            if len(temp_prefix_route_list)>MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                temp_prefix_route_list = temp_prefix_route_list[:MAX_LENGHT]

            #key+old_key_str是否有对应汉字匹配
            for prefix_route_param_tuple in prefix_route_list:
                old_key_str = prefix_route_param_tuple[0]
                new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                # print new_combine_keys
                new_keys_mapping_words_list = self.total_mapping_dic.get(new_combine_keys)
                #如果combine_keys对应有汉字匹配
                if new_keys_mapping_words_list:
                    #对matched_route_list的影响
                    for mapping_word in new_keys_mapping_words_list:
                        #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                        if not prefix_route_param_tuple[1]:
                            # print mapping_word
                            # bigram_item = ','.join(('BOS', mapping_word))
                            bigram_item = 'BOS'+','+mapping_word
                            weight = self.word_weight_dic.get(bigram_item)
                            if not weight:
                                # bigram_item = ','.join(('BOS', '*'))
                                bigram_item = 'BOS'+','+ '*'
                                weight = self.word_weight_dic.get(bigram_item)
                            # new_matched_route_param = ('#', [mapping_word], weight)
                            temp_matched_route_list.append(('#', [mapping_word], weight))
                        #（old_key_str,[],weight）第二个参数不为空
                        else:
                            # bigram_item = ','.join((prefix_route_param_tuple[1][-1], mapping_word))
                            bigram_item = prefix_route_param_tuple[1][-1]+','+ mapping_word
                            # bigram_item = (prefix_route_param_tuple[1][-1], mapping_word)
                            weight = self.word_weight_dic.get(bigram_item)
                            if not weight:
                                # bigram_item = ','.join((prefix_route_param_tuple[1][-1], '*'))
                                bigram_item = prefix_route_param_tuple[1][-1]+','+'*'
                                # bigram_item = (prefix_route_param_tuple[1][-1], '*')
                                weight = self.word_weight_dic.get(bigram_item)
                            new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                            new_weight = weight + prefix_route_param_tuple[-1]
                            # new_matched_route_param = ('#', new_matched_word_list, new_weight)
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                    #对prefix_route_list的影响
                    new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                    new_prefix_route_weight = prefix_route_param_tuple[-1]
                    # new_prefix_route_param_tuple = (new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight)
                    temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                #key+old_key_str是否有对应汉字匹配
                else:
                    if new_combine_keys in self.real_prefix_set:
                        new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

            if len(temp_matched_route_list)>MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                matched_route_list = temp_matched_route_list[:MAX_LENGHT]

            else:
                matched_route_list = temp_matched_route_list[:]
            if len(temp_prefix_route_list)>MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                prefix_route_list = temp_prefix_route_list[:MAX_LENGHT]

            else:
                prefix_route_list = temp_prefix_route_list[:]
            # print len(temp_matched_route_list), len(temp_prefix_route_list)

            ##按键到最后一位时，添加EOS
            key_input_index += 1
            if key_input_index == lenght_key_input:
                final_bigram_weight_list = []
                for matched_route_param in matched_route_list:
                    mapping_word_list = matched_route_param[1]
                    if mapping_word_list:
                        # bigram_item = ','.join((mapping_word_list[-1], 'EOS'))
                        bigram_item = mapping_word_list[-1]+','+'EOS'
                        weight = self.word_weight_dic.get(bigram_item)
                        if not weight:
                            # bigram_item = ','.join((mapping_word_list[-1], '*'))
                            bigram_item = mapping_word_list[-1]+','+ '*'
                            weight = self.word_weight_dic.get(bigram_item)
                        new_matched_word_list = mapping_word_list
                        new_weight = weight + matched_route_param[-1]
                        final_bigram_weight_list.append((' '.join(new_matched_word_list), new_weight))
                return sorted(final_bigram_weight_list, key=lambda x:x[-1])[:top_count]
# ea = EngineArithmetic()
# key_input = '9654684269267426424453926326'
# start_time = time.time()
# top_matched_sentence_weight_list = ea.handle_key_input_str(key_input,5)
# end_time = time.time()
# print end_time - start_time
# # print top_matched_sentence_weight_list
# for param_tuple in top_matched_sentence_weight_list:
#     print param_tuple[0]

def caculate_parameter():
    ea = EngineArithmetic()
    start_time = time.time()
    varify_sample_filename = os.path.join(PATH, '0709modify', 'cuted_varify_sample_pinyin_role_no_repeat.txt')
    checkout_sample_filename_backward = os.path.join(PATH, '0709modify', 'cut_path_lenght_limit_100_delete_2.txt')
    assert os.path.isfile(varify_sample_filename)
    with codecs.open(varify_sample_filename, encoding='utf-8') as f,\
    codecs.open(checkout_sample_filename_backward, mode='a', encoding='utf-8') as wf:
        count = 0
        for line in f.readlines():
            temp_list_for_write = []
            count += 1
            print count
            splited_line = line.split('\t')
            sentence = splited_line[0]
            key_str = splited_line[-1]
            com_str = '*'+sentence+'\n'
            temp_list_for_write.append(com_str)
            top_matched_sentence_weight_list = ['\t'.join((item[0], str(item[1])))+'\n' for item in ea.handle_key_input_str(key_str, 5)]
            temp_list_for_write.extend(top_matched_sentence_weight_list)
            wf.writelines(temp_list_for_write)
    end_time = time.time()
    print end_time-start_time
# caculate_parameter()

class CheckNgramWeight:
    '''检查Ngram的'''
    def __init__(self):
        pass
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与权重构成字典'''
        word_weight_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_weight.txt')
        # word_weight_filename = os.path.join(PATH, '0709modify',  'aaaaaaaaaaaa_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            words_weight_list = [(item.split('\t')[0], item.split('\t')[1].strip()) for item in f.readlines()]
            word_weight_dic = dict(words_weight_list)
            return word_weight_dic
    def check_weight(self):
        item_weight_dic = self._load_word_weigh()
        while 1:
            bigram_item = raw_input('bigram_item:').decode('utf-8')
            item_weight = item_weight_dic.get(bigram_item)
            print 'item_weight:%s'%item_weight
            if not item_weight:
                item_weight = item_weight_dic.get(bigram_item.split(',')[0]+','+'*')
                print 'weight * :%s'%item_weight

    # check_weight()
