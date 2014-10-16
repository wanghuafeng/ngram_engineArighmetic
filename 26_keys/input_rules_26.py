__author__ = 'wanghuafeng'
#coding:utf8
import os
import re
import sys
import math
import time
import psutil
import itertools
import codecs

module_path = 'E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'
sys.path.append(module_path)
from  add_words_spell_m import WordsSearch

PATH = os.path.dirname(os.path.abspath(__file__))

def convert_pinyin_to_rules():
    '''把基础词库中的拼音转换为输入规则（数字序列）'''
    coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
    ws = WordsSearch()
    base_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000.txt')
    base_file_with_pinyin = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000_pinyin_role.txt')
    with codecs.open(base_filename, encoding='utf-8') as f,\
    codecs.open(base_file_with_pinyin, mode='wb', encoding='utf-8') as wf:
        whole_word_list = (item.split('\t')[0] for item in f.readlines())
        for word in whole_word_list:
            pinyin_str = ' '.join(ws.get_splited_pinyin(word)[0]).replace('*', '')
            role_num = ''.join([coding_map[letter] for letter in pinyin_str if letter.isalpha()])
            com_str = '\t'.join((word, pinyin_str, role_num))
            wf.write(com_str+'\n')
# convert_pinyin_to_rules()
def mk_base_file_inorder():
    '''基础词库按照输入规则进行排序'''
    base_file_with_pinyin = os.path.join(PATH, 'data', 'combine_5233_and_top60000_pinyin_role.txt')
    base_file_with_pinyin_inorder = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000_pinyin_role_inorder.txt')
    with codecs.open(base_file_with_pinyin, encoding='utf-8') as f,\
    codecs.open(base_file_with_pinyin_inorder, mode='wb', encoding='utf-8') as wf:
        temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[2])
        wf.writelines(temp_list_for_write)
# mk_base_file_inorder()
def remove_white_space_in_pinyin():
    '''去掉拼音之间的空格'''
    base_file_with_pinyin_inorder = os.path.join(PATH, 'data', 'combine_5233_and_top60000_pinyin_role_inorder.txt')
    com_str_list = []
    with codecs.open(base_file_with_pinyin_inorder, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            word = splited_line[0]
            pinyin = splited_line[1].replace(' ', '')
            com_str = '\t'.join((word, pinyin))
            com_str_list.append(com_str+'\n')
    codecs.open(base_file_with_pinyin_inorder, mode='wb', encoding='utf-8').writelines(com_str_list)
# remove_white_space_in_pinyin()
def gen_role_num_words_mapping():
    '''以输入规则（数字序列）为key，该序列对应的多个汉字（逗号隔开）作为value，生成文件'''
    total_mapping_dic = {}
    base_file_with_pinyin_inorder_filename = os.path.join(PATH, 'data', 'combine_5233_and_top60000_pinyin_role_inorder.txt')
    mapping_base_file_with_pinyin_inorder_filename = os.path.join(PATH, 'data', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
    with codecs.open(base_file_with_pinyin_inorder_filename, encoding='utf-8') as f,\
    codecs.open(mapping_base_file_with_pinyin_inorder_filename, mode='wb', encoding='utf-8') as wf:
        for line in f.readlines():
            splited_line = line.split('\t')
            word = splited_line[0]
            role_num = splited_line[-1].strip()
            check_value = total_mapping_dic.get(role_num)
            if not check_value:
                total_mapping_dic[role_num] = [word]
            else:
                total_mapping_dic[role_num].append(word)
    # print total_mapping_dic
        for role_num, word_str_list in total_mapping_dic.iteritems():
            com_str = '\t'.join((role_num, ','.join(word_str_list)))
            wf.write(com_str+'\n')
# gen_role_num_words_mapping()
def mapping_file_inorder():
    '''按照输入规则进行排序'''
    mapping_base_file_with_pinyin_inorder_filename = os.path.join(PATH, 'data', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
    with codecs.open(mapping_base_file_with_pinyin_inorder_filename, encoding='utf-8') as f:
        temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
    with codecs.open(mapping_base_file_with_pinyin_inorder_filename, mode='wb', encoding='utf-8') as wf:
        wf.writelines(temp_list_for_write)
# mapping_file_inorder()
def get_prefix_of_mapping_role():
    '''输出所有输入规则的真前缀'''
    mapping_filename = os.path.join(PATH, 'data', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
    total_profix_set = set()
    with codecs.open(mapping_filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            role_num = splited_line[0]
            if len(role_num) == 1:
                print line.strip()
            for i in range(1, len(role_num)):
                total_profix_set.add(role_num[0:i]+'\n')
    prefix_filename = os.path.join(PATH, 'data', 'prefix_if_mapping_role_num.txt')
    temp_list_for_write = sorted(total_profix_set, key=lambda x:x.strip())
    codecs.open(prefix_filename, mode='wb', encoding='utf-8').writelines(temp_list_for_write)
# get_prefix_of_mapping_role()

class Bigram:
    def __init__(self):
        self.real_prefix_set = set()
        self.total_mapping_dic = {}
        self.word_weight_dic = {}
        self._real_prefix_rolenum()
        self._load_mapping_rolenum_wordlist()
        self._load_word_weigh()
        self.start_time = time.time()

    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与权重构成字典'''
        word_weight_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_weight.txt')
        # word_weight_filename = os.path.join(PATH, '0709modify',  'aaaaaaaaaaaa_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            words_weight_list = [(item.split('\t')[0], item.split('\t')[1].strip()) for item in f.readlines()]
            self.word_weight_dic = dict(words_weight_list)
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_filename = os.path.join(PATH, '0709modify', 'prefix_if_mapping_role_num.txt')
        with codecs.open(real_prefix_filename, encoding='utf-8') as f:
            self.real_prefix_set = set([item.strip() for item in f.readlines()])
    def gen_bigram_pair_weight(self, num_str):
        '''生成各匹配路径的节点（bigram_item, weight）数组'''
        first_word_of_bigram_item_list = ['BOS']
        start_point = 0
        length_of_num_str = len(num_str)
        self.total_bigramlist_weight_tuple_list = []
        self.second_word_list = []
        matched_path_count = 0#匹配输入数字序列的路径条数
        for num_index in range(1, length_of_num_str+1):
            num_str_slice = num_str[start_point:num_index]
            if num_str_slice in self.real_prefix_set and num_index != length_of_num_str:
                #数字序列为真前缀，且没有到达数字序列的结尾
                continue
            else:
                #有词输出的数字序列

                if num_index != length_of_num_str:#非数字序列的结尾
                    bigramlist_weight_tuple_list = []
                    # print start_point,num_index-1
                    matched_num_str = num_str[start_point:num_index-1]
                    print matched_num_str
                    second_word_of_bigram_item_list = self.total_mapping_dic.get(matched_num_str)
                    print second_word_of_bigram_item_list
                    second_words_list_lenght = len(second_word_of_bigram_item_list)
                    self.second_word_list.append(second_word_of_bigram_item_list)
                    # print first_word_of_bigram_item_list, second_word_of_bigram_item_list
                    bigram_item_tuple_list = itertools.product(first_word_of_bigram_item_list, second_word_of_bigram_item_list)
                    for bigram_item_tuple in bigram_item_tuple_list:
                        bigram_item_str = ','.join(bigram_item_tuple)
                        weight = self.word_weight_dic.get(bigram_item_str)
                        if not weight:#若果bigram_item_str在dict中没有weight存在，则查询(first_word_of_bigram_item，*)来获得该低频词的公有权重值（weight）
                            first_word_of_bigram_item = bigram_item_str.split(',')[0]
                            no_weight_bigram_item_str = ','.join((first_word_of_bigram_item, '*'))
                            weight = self.word_weight_dic.get(no_weight_bigram_item_str)
                        # print bigram_item_str, weight
                        bigramlist_weight_tuple_list.append((bigram_item_str, weight))
                    self.total_bigramlist_weight_tuple_list.append(bigramlist_weight_tuple_list)

                    # print len(bigramlist_weight_tuple_list)
                    # new_combine_bigramitem_weight_list = []
                    # matched_path_count = len(last_status_bigramlist_weight_tuple_list)
                    # for bigramitem_weight_tuple_index in range(matched_path_count):
                    #     last_matched_bigramlist_weight_tuple = last_status_bigramlist_weight_tuple_list[bigramitem_weight_tuple_index]
                    #     matched_bigramlist_weight_list = bigramlist_weight_tuple_list[bigramitem_weight_tuple_index*second_words_list_lenght:(bigramitem_weight_tuple_index+1)*second_words_list_lenght]
                    #     # print len(matched_bigramlist_weight_list)
                    #     # print last_matched_bigramlist_weight, matched_bigramlist_weight_list
                    #     # print bigramitem_weight_tuple_index
                    #     new_combine_bigramitem_weight_list.extend([(','.join((last_matched_bigramlist_weight_tuple[0], item[0].split(',')[1])), sum((int(last_matched_bigramlist_weight_tuple[1]), int(item[1])))) for item in matched_bigramlist_weight_list])
                    #     matched_path_count = len(last_matched_bigramlist_weight_tuple)
                    # if new_combine_bigramitem_weight_list:#如果不为空,即并非第一次输入匹配
                    #     last_status_bigramlist_weight_tuple_list = new_combine_bigramitem_weight_list[:]
                    #     # for con in last_status_bigramlist_weight_tuple_list:
                    #     #     print con[0], con[1]
                    # else:#第一次输入匹配
                    #     last_status_bigramlist_weight_tuple_list = bigramlist_weight_tuple_list[:]
                    #     # print last_status_bigramlist_weight_tuple_list
                    # # last_status_bigramlist_weight_tuple_list = new_combine_bigramitem_weight_list[:]
                    # for con in last_status_bigramlist_weight_tuple_list:
                    #     print con[0], con[1]


                #数字序列的结尾;该数字序列中，末尾部分匹配最后汉字输出的数字串要有EOS匹配
                else:
                    bigramlist_weight_tuple_list = []
                    # print start_point,num_index
                    matched_num_str = num_str[start_point:num_index]
                    # print matched_num_str
                    second_word_of_bigram_item_list = self.total_mapping_dic.get(matched_num_str)
                    # print first_word_of_bigram_item_list, second_word_of_bigram_item_list
                    self.second_word_list.append(second_word_of_bigram_item_list)
                    bigram_item_tuple_list = itertools.product(first_word_of_bigram_item_list, second_word_of_bigram_item_list)
                    for bigram_item_tuple in bigram_item_tuple_list:
                        bigram_item_str = ','.join(bigram_item_tuple)
                        weight = self.word_weight_dic.get(bigram_item_str)
                        if not weight:#若果bigram_item_str在dict中没有weight存在，则查询(first_word_of_bigram_item，*)来获得该低频词的公有权重值（weight）
                            # first_word_of_bigram_item = bigram_item_str.split(',')[0]
                            no_weight_bigram_item_str = ','.join((bigram_item_tuple[0], '*'))
                            # print no_weight_bigram_item_str
                            weight = self.word_weight_dic.get(no_weight_bigram_item_str)
                        # print bigram_item_str, weight
                        bigramlist_weight_tuple_list.append((bigram_item_str, weight))
                    self.total_bigramlist_weight_tuple_list.append(bigramlist_weight_tuple_list)

                    bigramlist_weight_tuple_list = []
                    EOS_bigram_item_tuple_list = itertools.product(second_word_of_bigram_item_list, ['EOS'])
                    self.second_word_list.append(['EOS'])
                    for eos_bigram_item_tuple in EOS_bigram_item_tuple_list:
                        eos_bigram_item_str = ','.join(eos_bigram_item_tuple)
                        eos_weight = self.word_weight_dic.get(eos_bigram_item_str)
                        if not eos_weight:#first_word_of_bigram_item,EOS没有weight匹配
                            eos_no_weight_bigram_item_str = ','.join((eos_bigram_item_tuple[0], '*'))
                            eos_weight = self.word_weight_dic.get(eos_no_weight_bigram_item_str)
                        # print eos_bigram_item_str, eos_weight
                        bigramlist_weight_tuple_list.append((eos_bigram_item_str, eos_weight))
                    self.total_bigramlist_weight_tuple_list.append(bigramlist_weight_tuple_list)
            first_word_of_bigram_item_list = second_word_of_bigram_item_list[:]
            start_point = num_index-1
            # print '*'*40
    def handle_bigramitem_weight_list(self, num_str, top_count=1):
        self.gen_bigram_pair_weight(num_str)
        # print self.total_bigramlist_weight_tuple_list, len(self.total_bigramlist_weight_tuple_list)
        # print self.second_word_list, len(self.second_word_list)
        # for bigram_weight_tuple_list in self.total_bigramlist_weight_tuple_list:
        #     for bigram_weight_tuple in bigram_weight_tuple_list:
        #         print bigram_weight_tuple[0], bigram_weight_tuple[1]
        # print '='*40


        total_list_length = len(self.total_bigramlist_weight_tuple_list)

        new_combine_bigramitem_weight_list = self.total_bigramlist_weight_tuple_list[0]
        # this_bigram_weight_match_list = []
        # next_bigram_weight_matched_list = []

        for bigram_weight_list_index in range(total_list_length-1):

            temp_record_new_route_tuple_list = []
            second_word_list = self.second_word_list[bigram_weight_list_index]
            for i in range(len(second_word_list)):
                matched_second_word = second_word_list[i]
                # print matched_second_word

                this_bigram_weight_match_list = [item for item in new_combine_bigramitem_weight_list if item[0].endswith(matched_second_word)]

                next_bigram_weight_matched_list = [item for item in self.total_bigramlist_weight_tuple_list[bigram_weight_list_index+1] if item[0].startswith(matched_second_word)]

                # print  this_bigram_weight_match_list, next_bigram_weight_matched_list
                # time.sleep(1)

                for this_bigram_weight_tuple in this_bigram_weight_match_list:
                    for next_bigram_weight_tuple in next_bigram_weight_matched_list:
                        # print this_bigram_weight_tuple[1], next_bigram_weight_tuple[1]
                        new_route_tuple = (','.join((this_bigram_weight_tuple[0], next_bigram_weight_tuple[0].split(',')[1])), sum((int(this_bigram_weight_tuple[1]), int(next_bigram_weight_tuple[1]))))
                        temp_record_new_route_tuple_list.append(new_route_tuple)
                        # print new_route_tuple[0], new_route_tuple[1]

            new_combine_bigramitem_weight_list = temp_record_new_route_tuple_list
        # print len(new_combine_bigramitem_weight_list)

        inorder_new_route_list = sorted(new_combine_bigramitem_weight_list, key=lambda x:x[1])
        # for new_route_utple in inorder_new_route_list[0:top_count]:
        #     # print new_route_utple
        #     print '\t'.join((new_route_utple[0].encode('utf-8'), str(new_route_utple[1])))
        print len(inorder_new_route_list)
        return inorder_new_route_list[0:top_count]

# num_str = u'2267426327322673622668'
# num_str = '2493426942347426248'
# bg = Bigram()
# bg.handle_bigramitem_weight_list(num_str,5)
#
# end_time = time.time()
# print end_time - bg.start_time
def check_parameter_of_this_arithmetic():
    bg = Bigram()
    filename = os.path.join(PATH, 'cuted_varify_sample_pinyin_role.txt')
    # filename = os.path.join(PATH, '0709modify', 'aaaaaaaaaak.txt')
    total_top_n_count_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            words = splited_line[0]
            role_num = splited_line[-1].strip()
            # print role_num
            total_top_n_count_list.append('\t'.join((words, role_num+'\n')))
            top_count_tuple_list = bg.handle_bigramitem_weight_list(role_num, 5)
            # print top_count_tuple_list
            total_top_n_count_list.extend(['\t'.join((item[0], str(item[1])))+'\n' for item in top_count_tuple_list])
            # print total_top_n_count_list
    file_to_write_filename = os.path.join(PATH, 'cuted_varify_sample_pinyin_role_checkout.txt')
    end_time = time.time()
    print end_time - bg.start_time
    codecs.open(file_to_write_filename, mode='wb', encoding='utf-8').writelines(total_top_n_count_list)
# check_parameter_of_this_arithmetic()

def zip_test():
    x = [1, 2]
    y = [4, 5, 6]
    print zip(x, y)
# zip_test()
def re_combine_data():
    t = (u'BOS,\u8584\u7247', u'111')
    # print type(t[1])
    # print sum((int(t[1]), int(t[1])))
    l = [(u'\u8584\u7247,\u53d1\u70ed', u'1000000000000'), (u'\u8584\u7247,\u5927\u70ed', u'1000000000000'), (u'\u8584\u7247,\u53d1\u8272', u'1000000000000')]
    for i in l:
        print i[0]
    new_l = [(','.join((t[0], item[0])), sum((int(t[1]), int(item[1])))) for item in l]
    print new_l
# re_combine_data()
sum((1,3))
def split_num_str():
    num_str = '2267426'
    start_point = end_point = 0
    lenght_of_num_str = len(num_str)
    print lenght_of_num_str
    for num_index in range(1, lenght_of_num_str+1):
        print num_index
        # num_str_slice = num_str[start_point:num_index]
        # print num_str_slice
# split_num_str()
def gen_decare_value():
    '''产生笛卡尔积'''
    a = {1}
    b = {2, 4, 5}
    import itertools
    for i in itertools.product(a,b):
        print i
# gen_decare_value()

def gen_varify_sample_pinyin_role():
    filename = os.path.join(PATH, 'data', 'src', 'cuted_varify_sample_pinyin_role_no_repeat.txt')
    com_str_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            word = splited_line[0]
            pinyin = splited_line[1].replace(' ', '')
            com_str = '\t'.join((word, pinyin+'\n'))
            com_str_list.append(com_str)
    codecs.open(filename, mode='wb', encoding='utf-8').writelines(com_str_list)
# gen_varify_sample_pinyin_role()