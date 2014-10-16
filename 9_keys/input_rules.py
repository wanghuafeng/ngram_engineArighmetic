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
src_file_path = r'E:\SVN\linguistic_model\9_keys\big_linguistic_data\data'
def convert_pinyin_to_rules():
    '''把基础词库中的拼音转换为输入规则（数字序列）'''
    coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
    ws = WordsSearch()
    base_filename = os.path.join(src_file_path, 'combine_top60000_and_5041.txt')
    base_file_with_pinyin = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role.txt')
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
    base_file_with_pinyin = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role.txt')
    base_file_with_pinyin_inorder = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role_inorder.txt')
    with codecs.open(base_file_with_pinyin, encoding='utf-8') as f,\
    codecs.open(base_file_with_pinyin_inorder, mode='wb', encoding='utf-8') as wf:
        temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[2])
        wf.writelines(temp_list_for_write)
# mk_base_file_inorder()
def gen_role_num_words_mapping():
    '''以输入规则（数字序列）为key，该序列对应的多个汉字（逗号隔开）作为value，生成文件'''
    total_mapping_dic = {}
    base_file_with_pinyin_inorder_filename = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role_inorder.txt')
    mapping_base_file_with_pinyin_inorder_filename = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role_inorder_mapping.txt')
    with codecs.open(base_file_with_pinyin_inorder_filename, encoding='utf-8') as f,\
    codecs.open(mapping_base_file_with_pinyin_inorder_filename, mode='wb', encoding='utf-8') as wf:
        for line in f.readlines():
            splited_line = line.split('\t')
            word = splited_line[0]
            role_num = splited_line[2].strip()
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
    mapping_base_file_with_pinyin_inorder_filename = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role_inorder_mapping.txt')
    with codecs.open(mapping_base_file_with_pinyin_inorder_filename, encoding='utf-8') as f:
        temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
    with codecs.open(mapping_base_file_with_pinyin_inorder_filename, mode='wb', encoding='utf-8') as wf:
        wf.writelines(temp_list_for_write)
# mapping_file_inorder()
def get_prefix_of_mapping_role():
    '''输出所有输入规则的真前缀'''
    mapping_filename = os.path.join(src_file_path, 'combine_top60000_and_5041_pinyin_role_inorder_mapping.txt')
    total_profix_set = set()
    with codecs.open(mapping_filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            role_num = splited_line[0]
            if len(role_num) == 1:
                print line.strip()
            for i in range(1, len(role_num)):
                total_profix_set.add(role_num[0:i]+'\n')
    prefix_filename = os.path.join(src_file_path, 'prefix_if_mapping_role_num.txt')
    temp_list_for_write = sorted(total_profix_set, key=lambda x:x.strip())
    codecs.open(prefix_filename, mode='wb', encoding='utf-8').writelines(temp_list_for_write)
# get_prefix_of_mapping_role()

def get_input_rules_from_giving_words(input_words):
    '''输入汉字，输出相应的输入规则'''
    try:
        assert isinstance(input_words, unicode)
    except:
        input_words = input_words.decode('utf-8')
    coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
    ws = WordsSearch()
    pinyin_str = ' '.join(ws.get_splited_pinyin(input_words)[0]).replace('*', '')
    role_num = ''.join([coding_map[letter] for letter in pinyin_str if letter.isalpha()])
    print '\t'.join((words.decode('utf-8'), pinyin_str, role_num))
words = '岷峨喔'
get_input_rules_from_giving_words(words)
