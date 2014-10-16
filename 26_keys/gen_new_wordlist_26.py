__author__ = 'wanghuafeng'
#coding:utf-8
import codecs
import os
import re
import time
import random

PATH = os.path.dirname(os.path.abspath(__file__))

MSG_FILE_PATH = r'E:\language_model\ghost_weibo\msg'
COMMENT_FILE_PATH = r'E:\language_model\ghost_weibo\comment'


def check_random():
    count = 0
    for i in range(1, 100000):
        k = random.randint(1, 100000)
        if 4000<k<5000:
            count += 1
            print count
def combine_all_src_files():
    '''合并所有comment与msg文件'''
    combine_filename = os.path.join(PATH, 'combine_msg_comment.txt')
    total_filename_list = []
    msg_file_list = [os.path.join(MSG_FILE_PATH, item) for item in os.listdir(MSG_FILE_PATH)]
    total_filename_list.extend(msg_file_list)
    comment_file_list = [os.path.join(COMMENT_FILE_PATH, item) for item in os.listdir(COMMENT_FILE_PATH)]
    total_filename_list.extend(comment_file_list)
    print len(comment_file_list)
    print len(msg_file_list)
    print len(total_filename_list)
    count = 0
    with codecs.open(combine_filename, mode='a', encoding='utf-8') as wf:
        for filename in total_filename_list:
            count += 1
            with codecs.open(filename, encoding='utf-8') as f:
                wf.writelines(f.readlines())
                print count
                # time.sleep(1)
# combine_all_src_files()
def extract_test_and_varify_sample():
    '''从合并文件中抽取测试样本(linguistic_sample)和验证样本(varify_sample)'''
    linguistic_sample_filename = os.path.join(PATH, 'data', 'linguistic_sample.txt')
    varify_sample_filename = os.path.join(PATH, 'data', 'varify_sample.txt')
    combine_filename = os.path.join(PATH, 'combine_msg_comment.txt')
    count = 0
    with codecs.open(combine_filename, encoding='utf-8') as f,\
        codecs.open(linguistic_sample_filename, mode='wb', encoding='utf-8') as linguistic_wf,\
        codecs.open(varify_sample_filename, mode='wb', encoding='utf-8') as varify_wf:
        while True:
            line = f.readline()
            if not line:
                break
            random_num = random.randint(1, 48529884)
            if 0 < random_num < 500000:
                varify_wf.write(line)
                count += 1
                print count
            else:
                linguistic_wf.write(line)
# extract_test_and_varify_sample()
def gen_freq_in_data_sample():
    '''统计样本语料中所有单词在语料中的词频'''
    whole_word_dic = {}
    sample_filename = os.path.join(PATH, 'data', 'linguistic_sample.txt')
    word_freq_filename = os.path.join(PATH, 'word_freq.txt')
    f = codecs.open(sample_filename, encoding='utf-8')
    # with codecs.open(sample_filename, encoding='utf-8') as f:
    while True:
        line  = f.readline()
        if not line:
            break
        for word in line:
            if word in whole_word_dic:
                whole_word_dic[word] += 1
            else:
                whole_word_dic[word] = 1
        # print len(whole_word_dic)
    # for word, freq in whole_word_dic.items():
    word_freq_str_list = ['\t'.join((key,str(value)))+'\n'  for (key,value) in whole_word_dic.items()]
    with codecs.open(word_freq_filename, mode='wb', encoding='utf-8') as wf:
        wf.writelines(word_freq_str_list)
# gen_freq_in_data_sample()
def make_word_freq_sample_inorder():
    '''对统计出的词频语料进行排序'''
    word_freq_sample_filename = os.path.join(PATH, 'word_freq_from_95K.txt')
    with codecs.open(word_freq_sample_filename, encoding='utf-8') as f:
        word_freq_list = []
        for line in f.readlines():
            splited_line = line.split('\t')
            if  len(splited_line) != 2:
                continue
            word = splited_line[0]
            freq = splited_line[1].strip()
            word_freq_list.append((word, freq))
        print len(word_freq_list)
        sorted_word_freq_list = sorted(word_freq_list, key=lambda x: int(x[1]), reverse=True)
        print len(sorted_word_freq_list)
    sorted_word_freq_filename = os.path.join(PATH, 'word_freq_from_95K.txt')
    with codecs.open(sorted_word_freq_filename, mode='wb', encoding='utf-8') as wf:
        temp_list_for_write = ['\t'.join(item)+'\n' for item in sorted_word_freq_list]
        wf.writelines(temp_list_for_write)
# make_word_freq_sample_inorder()
def gen_6000_word_freq_sample():
    '''从排序后的统计词频语料中筛选出词频最高的6000个词汇'''
    sorted_word_freq_filename = os.path.join(PATH, 'sorted_word_freq.txt')
    top_6000_word_freq_filename = os.path.join(PATH, 'top_6000_word_freq.txt')
    count = 0
    character_pattern = re.compile(ur"([\u4E00-\u9FA5]+)", re.U)
    pure_word_freq = []
    with codecs.open(sorted_word_freq_filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            if len(splited_line) != 2:
                continue
            word = splited_line[0]
            freq = splited_line[1]
            if character_pattern.match(word):
                pure_word_freq.append(line)
                count += 1
            if count >= 6000:
                with codecs.open(top_6000_word_freq_filename, mode='wb', encoding='utf-8') as wf:
                    wf.writelines(pure_word_freq)
                    break
# gen_6000_word_freq_sample()
def extract_word_from_95K():
    '''从27万词表中筛选出单字词频在top_6000词表中字（5322个）'''
    src_95K_filename = r'E:\SVN\chocolate_ime\doc\Cizu_komoxo95K.txt'
    extract_95K_from_top_6000_filename = os.path.join(PATH, 'single_word_from_95K.txt')
    top_6000_word_freq_filename = os.path.join(PATH, 'top_6000_word_freq.txt')
    top_6000_word_set = set()
    with codecs.open(top_6000_word_freq_filename, encoding='utf-8') as f:
        for line in f.readlines():
            word = line.split('\t')[0]
            top_6000_word_set.add(word)
    single_word_in_top_6000_set = set()
    with codecs.open(src_95K_filename, encoding='gbk') as src_f:
        for line in src_f.readlines():
            if line.startswith(';'):
                continue
            words = line.split('\t')[0]
            for single_word in words:
                single_word_in_top_6000_set.add(single_word)
    print len(single_word_in_top_6000_set)
    with codecs.open(extract_95K_from_top_6000_filename, mode='wb', encoding='utf-8') as extract_wf:
        temp_list_for_write = [item+'\n' for item in single_word_in_top_6000_set]
        extract_wf.writelines(temp_list_for_write)
# extract_word_from_95K()
def cut_linguistic_sample_into_sentence():
    '''利用字表（5322）去切割原始测试语料，生成句子——字表+原始语料====>>句子语料'''
    linguistic_sample_filename = os.path.join(PATH, 'data', 'linguistic_sample.txt')
    # test_filename = os.path.join(PATH, '0709modify', '2014_01_13_190053_msg.txt')
    cuted_sentence_filename = os.path.join(PATH, '0709modify', 'cuted_sentence.txt')
    word_list_filename = os.path.join(PATH, '0709modify', 'single_word_from_95K.txt')
    format_str = ''.join([item.strip() for item in codecs.open(word_list_filename, encoding='utf-8').readlines()])
    wordlist_pattern =re.compile(ur"([%s]+)"%format_str, re.U)
    with codecs.open(linguistic_sample_filename, encoding='utf-8') as f,\
        codecs.open(cuted_sentence_filename, mode='wb', encoding='utf-8') as wf:
        while 1:
            line = f.readline()
            if not line:
                break
            splited_line_list = wordlist_pattern.split(line)
            for param in splited_line_list:
                if len(param) == 0:
                    continue
                if wordlist_pattern.match(param):
                    wf.write(param+'\n')
# cut_linguistic_sample_into_sentence()

def re_extract_word_list():
    '''构建词表，95K文件中每个词所包含的单字都在新筛选出的字表中'''
    src_95K_filename = r'E:\SVN\chocolate_ime\doc\Cizu_komoxo95K.txt'
    new_single_word_list = os.path.join(PATH, '0709modify', 'single_word_from_95K_5322.txt')
    new_word_list_filename = os.path.join(PATH, '0709modify', 'new_wordlist.txt')
    with codecs.open(new_single_word_list, encoding='utf-8') as single_f:
        single_word_set = set([item.strip() for item in single_f.readlines()])
        print len(single_word_set)#5322
    wordlist_param_list = []
    with codecs.open(src_95K_filename, encoding='gbk') as src_f:
        for line in src_f.readlines():
            if line.startswith(';'):
                continue
            words = line.split('\t')[0]
            for single_word in words:
                if single_word not in single_word_set:
                    print words
                    continue
            wordlist_param_list.append(words)
    print len(set(wordlist_param_list))
    com_set = single_word_set | set(wordlist_param_list)
    print len(com_set)#276000

    temp_list_for_wirte = [item+'\n' for item in com_set]
    with codecs.open(new_word_list_filename, mode='wb', encoding='utf-8') as wordlist_wf:
        wordlist_wf.writelines(temp_list_for_wirte)
# re_extract_word_list()
# l = [('#', [u'\u8f6c', u'\u5927', u'\u5fae', u'\u64ad'], '246798'), ('#', [u'\u8f6c', u'\u5927', u'\u91ce', u'\u6d69'], '248493'), ('#', [u'\u4e13', u'\u6253', u'\u91ce', u'\u6d69'], '249519'), ('#', [u'\u8f6c', u'\u5927', u'\u7ef4', u'\u5965'], '252485'), ('#', [u'\u4e13', u'\u53d1', u'\u5fae', u'\u64ad'], '252581'), ('#', [u'\u8f6c', u'\u6cd5', u'\u4e5f', u'\u9ad8'], '252731'), ('#', [u'\u8f6c', u'\u5927', u'\u7ef4', u'\u5b89'], '252757'), ('#', [u'\u8f6c', u'\u6cd5', u'\u4e5f', u'\u641e'], '253930'), ('#', [u'\u8f6c', u'\u6cd5', u'\u4e3a', u'\u5b89'], '255066'), ('#', [u'\u8f6c', u'\u5927', u'\u7ef4', u'\u6848'], '256882'), ('#', [u'\u8f6c', u'\u6cd5', u'\u4e5f', u'\u5e72'], '257028'), ('#', [u'\u8f6c', u'\u6cd5', u'\u7237', u'\u597d'], '257171'), ('#', [u'\u8d5a', u'\u5927', u'\u5fae', u'\u64ad'], '258256'), ('#', [u'\u8f6c', u'\u6cd5', u'\u672a', u'\u6309'], '259579'), ('#', [u'\u8f6c', u'\u5927', u'\u4e5f', u'\u9ad8'], '259792'), ('#', [u'\u8d5a', u'\u5927', u'\u91ce', u'\u6d69'], '259951'), ('#', [u'\u8f6c', u'\u5927', u'\u8587', u'\u5b89'], '260935'), ('#', [u'\u8f6c', u'\u5927', u'\u4e5f', u'\u641e'], '260991'), ('#', [u'\u8f6c', u'\u642d', u'\u5fae', u'\u64ad'], '261066'), ('#', [u'\u8f6c', u'\u5927', u'\u5a01', u'\u535a'], '261076')]
# for param_tuple in l:
#     print ''.join(param_tuple[1])
def remove_repeat_word():
    word_weight_filename = os.path.join(PATH, '0709modify', 'cuted_varify_sample_pinyin_role.txt')
    word_weight_filename_no_repeat = os.path.join(PATH, '0709modify', 'cuted_varify_sample_pinyin_role_no_repeat.txt')
    with codecs.open(word_weight_filename, encoding='utf-8') as f,\
    codecs.open(word_weight_filename_no_repeat, mode='wb', encoding='utf-8') as wf:
        line_list = f.readlines()
        line_set = set(line_list)
        print len(line_list), len(line_set)
        wf.writelines(line_set)

def get_all_checkout_file():
    '''利用glob获取相关路径'''
    import glob
    glob_path = os.path.join(PATH, '0709modify', 'cuted_varify_sample_pinyin_role_checkout*')
    matched_path_list =  glob.glob(glob_path)
    # print matched_path_list, len(matched_path_list)
    filename_to_write = os.path.join(PATH, '0709modify', 'checkout.txt')
    with codecs.open(filename_to_write, mode='wb', encoding='utf-8') as wf:
        all_content = [wf.writelines(codecs.open(item, encoding='utf-8').readlines()) for item in matched_path_list]
# get_all_checkout_file()
