#coding:utf8
import os
import re
import math
import time
import psutil
import codecs
from cut_sentence import Cut_Sentence

PATH = os.path.dirname(os.path.abspath(__file__))
src_filename = os.path.join(PATH, '0709modify', 'cuted_sentence.txt')
# src_filename = os.path.join(PATH, '2014_03_29_231246_comment.txt')
def gen_word_freq_from_linguistic_data():
    '''词表+句子语料'''
    cs = Cut_Sentence()
    whole_word_freq_dic = {}
    whole_word_freq_set = set()
    with codecs.open(src_filename, encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            splited_words_tuple = cs.cut(line)
            if len(splited_words_tuple) == 1:
                if splited_words_tuple[0] in whole_word_freq_set:
                    whole_word_freq_dic[splited_words_tuple[0]] += 1
                else:
                    whole_word_freq_set.add(splited_words_tuple[0])
                    whole_word_freq_dic[splited_words_tuple[0]] = 1
            else:
                for splited_words_param in splited_words_tuple:
                    if splited_words_param in whole_word_freq_set:
                        whole_word_freq_dic[splited_words_param] += 1
                    else:
                        whole_word_freq_set.add(splited_words_param)
                        whole_word_freq_dic[splited_words_param] = 1
    temp_filename = os.path.join(PATH, '0709modify', 'word_freq_from_95K.txt')
    word_freq_str_list = ['\t'.join((key,str(value)))+'\n' for (key,value) in whole_word_freq_dic.items()]
    with codecs.open(temp_filename, mode='wb', encoding='utf-8') as wf:
        wf.writelines(word_freq_str_list)
# gen_word_freq_from_linguistic_data()

def mk_word_freq_inorder_by_freq():
    '''将word_freq文件按词频高低进行排列'''
    file_to_convert_filename = os.path.join(PATH, '0709modify', 'word_freq_from_new_wordlist_inorder.txt')
    new_file_to_write_filename = os.path.join(PATH, '0709modify', 'word_freq_in_order_272773.txt')
    with codecs.open(file_to_convert_filename, encoding='utf-8') as f:
        inorder_list = sorted(f.readlines(), key=lambda x: int(x.split('\t')[1]), reverse=True)
    with codecs.open(new_file_to_write_filename, mode='wb', encoding='utf-8') as wf:
        wf.writelines(inorder_list)
# mk_word_freq_inorder_by_freq()

def gen_60000_word_freq_sample():
    '''从排序后的统计词频语料中筛选出词频最高的60000个词汇'''
    sorted_word_freq_filename = os.path.join(PATH, '0709modify', 'word_freq_in_order_272773.txt')
    top_60000_word_freq_filename = os.path.join(PATH, '0709modify', 'word_freq_inorder_top_60000.txt')
    count = 0
    pure_word_freq = []
    with codecs.open(sorted_word_freq_filename, encoding='utf-8') as f:
        for line in f.readlines():
            count += 1
            pure_word_freq.append(line)
            if count >= 60000:
                with codecs.open(top_60000_word_freq_filename, mode='wb', encoding='utf-8') as wf:
                    wf.writelines(pure_word_freq)
                    break
# gen_60000_word_freq_sample()
def word_in_top_60000_bigger_than_4():
    '''top_60000文件中汉字长度大于4的所有词'''
    total_word_set = set()
    src_95K_filename = r'E:\SVN\chocolate_ime\doc\Cizu_komoxo95K.txt'
    with codecs.open(src_95K_filename, encoding='gbk') as src_f:
        for line in src_f.readlines():
            if line.startswith(';'):
                continue
            words = line.split('\t')[0]
            total_word_set.add(words)
    top_60000_word_freq_filename = os.path.join(PATH, '0709modify', 'word_freq_inorder_top_60000.txt')
    with codecs.open(top_60000_word_freq_filename, encoding='utf-8') as f:
        for line in f.readlines():
            word = line.split('\t')[0]
            if len(word) >= 4 and word in total_word_set:
                # if word not in total_word_set:
                print word
# word_in_top_60000_bigger_than_4()
def check_in_linguistic_sample():
    '''查询某个词在原始语料中出现的次数，与统计的词频做二次校验'''
    linguistic_sample_filename = os.path.join(PATH, 'data', 'linguistic_sample.txt')
    format_str = u'爱护'#13006
    pattern = re.compile(ur"(%s)"%format_str, re.U)
    count = 0
    with codecs.open(linguistic_sample_filename, encoding='utf-8') as f:
        for line in f.readlines():
            match_list = pattern.findall(line)
            if match_list:
                count += len(match_list)
        # while 1:
        #     line = f.readline()
        #     if not line:
        #         break
        #     match_list = pattern.findall(line)
        #     if match_list:
        #         count += len(match_list)
            # splited_line = pattern.split(line)
            # for param in splited_line:
            #     if pattern.match(param):
            #         count += 1
    print count
# check_in_linguistic_sample()
def add_freq_to_5322_file():
    '''从272773文件中取词频添加到5322文件,生成新的文件'''
    src_5322_filename = os.path.join(PATH, '0709modify', 'single_word_from_95K_5322.txt')
    added_freq_filename = os.path.join(PATH, '0709modify', 'single_word_5322_with_freq.txt')
    word_freq_272773_filename = os.path.join(PATH, '0709modify', 'word_freq_in_order_272773.txt')
    with codecs.open(word_freq_272773_filename, encoding='utf-8') as dic_f,\
    codecs.open(src_5322_filename, encoding='utf-8') as src_f,\
    codecs.open(added_freq_filename, mode='wb', encoding='utf-8') as wf:
        total_word_freq_dic = dict([(item.split('\t')[0], item.split('\t')[1]) for item in dic_f.readlines()])
        # for word in src_f.readlines():
        #     if not total_word_freq_dic.get(word.strip()):
        #         print word.strip()
        word_freq_str_list = ['\t'.join((item.strip(), total_word_freq_dic.get(item.strip(), '0\n'))) for item in src_f.readlines()]
        wf.writelines(word_freq_str_list)
# add_freq_to_5322_file()
def combine_5233_and_top60000():
    '''合并5233与top_60000文件(去重后61633)'''
    combine_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000.txt')
    added_freq_filename = os.path.join(PATH, '0709modify', 'single_word_5322_with_freq.txt')
    top60000_filename = os.path.join(PATH, '0709modify', 'word_freq_inorder_top_60000.txt')
    with codecs.open(top60000_filename, encoding='utf-8') as top_f,\
        codecs.open(added_freq_filename, encoding='utf-8') as single_f,\
        codecs.open(combine_filename, mode='wb', encoding='utf-8') as wf:
        top60000_set = set(top_f.readlines())
        combine_set_for_write_set = set([item for item in single_f.readlines() if item not in top60000_set])
        print len(combine_set_for_write_set)
        temp_set = top60000_set|combine_set_for_write_set
        print len(temp_set)
        wf.writelines(temp_set)
# combine_5233_and_top60000()
def caculate_percentage():
    '''计算combine_5233_top60000文件的频率'''
    combine_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000.txt')
    new_file_to_write_filename = os.path.join(PATH, '0709modify', 'wordlist_61633_weight.txt')
    with codecs.open(combine_filename, encoding='utf-8') as f,\
    codecs.open(new_file_to_write_filename, mode='wb', encoding='utf-8') as wf:
        line_list = f.readlines()
        # sum_freq = sum([int(item.split('\t')[1]) for item in line_list])
        sum_freq = 611112178.0
        for line in line_list:
            splited_line = line.split('\t')
            freq_percentage = int(splited_line[1])/sum_freq
            word = splited_line[0]
            weight =  str(int(math.log10(freq_percentage)*(-20000)))
            com_str = '\t'.join((word, weight))
            wf.write(com_str+'\n')
# caculate_percentage()

def check_exception_in_new_wordlist():
    '''检查top_60000中不包含在new_wordlist的元素'''
    top_60000_word_freq_filename = os.path.join(PATH, 'top_60000_word_freq.txt')
    new_word_list_filename = os.path.join(PATH, 'top_60000_with_single_word_freq.txt')
    extract_95K_from_top_6000_filename = os.path.join(PATH, 'single_word_from_95K.txt')
    total_word_list = []
    with codecs.open(extract_95K_from_top_6000_filename, encoding='utf-8') as ef:
        total_word_list.extend(ef.readlines())
    with codecs.open(top_60000_word_freq_filename, encoding='utf-8') as f:
        for line in f.readlines():
            total_word_list.append(line.split('\t')[0]+'\n')
    with codecs.open(new_word_list_filename, mode='wb', encoding='utf-8') as wf:
        wf.writelines(total_word_list)
# check_exception_in_new_wordlist()
def remove_repeat_word():
    new_word_list_filename = os.path.join(PATH, 'a.txt')
    with codecs.open(new_word_list_filename, encoding='utf-8') as f:
        temp_list = [item for item in f.readlines()]
        codecs.open(new_word_list_filename, mode='wb', encoding='utf-8').writelines(set(temp_list))
# remove_repeat_word()
def make_word_freq_inorder():
    '''按照词频进行排序'''
    top_60000_word_freq_filename = os.path.join(PATH, 'top_60000_word_freq.txt')
    with codecs.open(top_60000_word_freq_filename, encoding='utf-8') as f:
        inorder_word_freq_list = sorted(f.readlines(), key=lambda x: int(x.split('\t')[1]), reverse=True)
        codecs.open('a.txt', mode='wb', encoding='utf-8').writelines(inorder_word_freq_list)
# make_word_freq_inorder()

def format_str_regular():
    s = u'索尼（SONY） KDL-60R520A 60英寸 全高清高清网络 LED液晶电视（高黑清色）'
    srt_format = u'高清'
    pattern = re.compile(ur"%s"%srt_format, re.U)
    # print len(pattern.split(s))
    for con in  pattern.findall(s):
        print con
    # for con in pattern.findall(s):
        # if pattern.match(con):
        #     print con
    # base_wordlist_filename = os.path.join(PATH, 'base_word_list.txt')
    # format_str = codecs.open(base_wordlist_filename, encoding=None).read()
    # print type(format_str)
# format_str_regular()
def gen_cuted_linguistic_data():
    '''在非词表出进行切割'''
    base_wordlist_filename = os.path.join(PATH, 'base_word_list.txt')
    cut_filename = os.path.join(PATH, 'data', 'varify_sample.txt')
    # cut_filename = os.path.join(PATH, '2014_01_13_190053_msg.txt')
    format_str = ''.join([item.strip() for item in codecs.open(base_wordlist_filename, encoding='utf-8').readlines()])
    base_wordlist_pattern =re.compile(ur"([%s]+)"%format_str, re.U)
    cuted_linguistic_data_filename = os.path.join(PATH, 'cuted_varify_sample.txt')
    with codecs.open(cut_filename, encoding='utf-8') as f,\
    codecs.open(cuted_linguistic_data_filename, mode='wb', encoding='utf-8') as wf:
        while 1:
            line = f.readline()
            if not line:
                break
            splited_line_list = base_wordlist_pattern.split(line)
            for param in splited_line_list:
                if len(param) == 0:
                    continue
                if base_wordlist_pattern.match(param):
                    wf.write(param+'\n')
# gen_cuted_linguistic_data()

def cut_linguistic_sample_into_small_part():
    '''将按词表切割后的文件分为150M大小的若干个文件'''
    cut_filename = os.path.join(PATH, '0709modify', 'cuted_sentence.txt')
    # varify_stample_filename = r'E:\SVN\language_model\data\varify_sample.txt'
    # print os.path.getsize(varify_stample_filename)#51470527
    sample_filename_int = 1
    with codecs.open(cut_filename, encoding='utf-8') as f:
        while 1:
            line = f.read(51470527)
            if not line:
                break
            stample_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s.txt'%sample_filename_int)
            if  not os.path.exists(stample_filename):
                codecs.open(stample_filename, mode='wb', encoding='utf-8')
            with codecs.open(stample_filename, mode='a', encoding='utf-8') as wf:
                wf.write(line)
            sample_filename_int += 1
# cut_linguistic_sample_into_small_part()

def cut_lines_into_words():
    '''将行（句子）切割成词，其间以空格隔开'''
    from cut_sentence import Cut_Sentence
    cs = Cut_Sentence()
    for file_count in range(26, 29):
        print file_count
        src_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s.txt'%file_count)
        try:
            assert os.path.exists(src_filename)
        except AssertionError:
            print '%s does not exist !!'%src_filename

        with codecs.open(src_filename, encoding='utf-8') as f:
            cuted_lines_list = [' '.join(cs.cut_with_weight(line))+'\n' for line in f.readlines()]
        codecs.open(src_filename, mode='wb', encoding='utf-8').writelines(cuted_lines_list)
# cut_lines_into_words()

def gen_bigram_trigram_model_data():
    '''统计二元、三元组数据'''
    bigram_param_freq_dic = {}
    bigram_param_set = set()
    trigram_param_freq_dic = {}
    trigram_param_set = set()
    for file_count in range(4, 29):
        src_data_filename = os.path.join(PATH, '0709modify',  'cuted_linguistic_stample', '%s.txt'%file_count)
        with codecs.open(src_data_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_list = line.strip().split()
                if not splited_list:#跳过空白行
                    continue
                splited_list_length = len(splited_list)
                # print splited_list_length

                # #二元组数据
                line_bigram_list = []
                line_bigram_list.append(('BOS', splited_list[0]))
                for i in range(splited_list_length):
                    if i < splited_list_length - 1:
                        line_bigram_list.append((splited_list[i], splited_list[i+1]))
                line_bigram_list.append((splited_list[-1], 'EOS'))
                for bigram_tuple in line_bigram_list:
                    if bigram_tuple in bigram_param_set:
                        bigram_param_freq_dic[bigram_tuple] += 1
                    else:
                        bigram_param_freq_dic[bigram_tuple] = 1
                        bigram_param_set.add(bigram_tuple)

                #三元组数据
                # line_trigram_list = []
                # if splited_list_length == 1:
                #     line_trigram_list.append(('BOS', 'BOS', splited_list[0]))
                #     line_trigram_list.append(('BOS', splited_list[0], 'EOS'))
                #     line_trigram_list.append(('EOS', 'EOS', splited_list[-1]))
                # elif splited_list_length == 2:
                #     line_trigram_list.append(('BOS', 'BOS', splited_list[0]))
                #     line_trigram_list.append(('BOS', splited_list[0], splited_list[1]))
                #     line_trigram_list.append((splited_list[0], splited_list[1], 'EOS'))
                #     line_trigram_list.append(('EOS', 'EOS', splited_list[-1]))
                # else:
                #     line_trigram_list.append(('BOS', 'BOS', splited_list[0]))
                #     line_trigram_list.append(('BOS', splited_list[0], splited_list[1]))
                #     for k in range(splited_list_length):
                #         if k < splited_list_length - 2:
                #             line_trigram_list.append((splited_list[k], splited_list[k+1], splited_list[k+2]))
                #         elif k == splited_list_length - 2:
                #             line_trigram_list.append((splited_list[k], splited_list[k+1], 'EOS'))
                #         else:
                #             line_trigram_list.append((splited_list[-1], 'EOS', 'EOS'))
                # for trigram_tuple in line_trigram_list:
                #     if trigram_tuple in trigram_param_set:
                #         trigram_param_freq_dic[trigram_tuple] += 1
                #     else:
                #         trigram_param_freq_dic[trigram_tuple] = 1
                #         trigram_param_set.add(trigram_tuple)
        # 写入二元组
        bigram_tuple_freq_list = ['\t'.join((','.join(bigram_tuple), str(freq)))+'\n' for (bigram_tuple, freq) in bigram_param_freq_dic.items()]
        bigram_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s_bigram.txt'%file_count)
        codecs.open(bigram_filename, mode='wb', encoding='utf-8').writelines(bigram_tuple_freq_list)
        bigram_param_set.clear()
        bigram_param_freq_dic.clear()
        #写入三元组
        # trigram_tuple_freq_list = ['\t'.join((','.join(trigram_tuple), str(freq)))+'\n' for (trigram_tuple, freq) in trigram_param_freq_dic.items()]
        # bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_trigram.txt'%file_count)
        # codecs.open(bigram_filename, mode='wb', encoding='utf-8').writelines(trigram_tuple_freq_list)
        # del trigram_param_set
        # del trigram_param_freq_dic
# gen_bigram_trigram_model_data()
def remove_freq_1():
    '''删除bigram二元组文件中频度为1的所有二元组元素'''
    for file_count in range(1, 29):
        print file_count
        src_data_filename = os.path.join(PATH, '0709modify',  'cuted_linguistic_stample', '%s_bigram.txt'%file_count)
        bigram_freq_remove_1_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s_bigram_remove_freq_1.txt'%file_count)
        remove_freq_list = []
        with codecs.open(src_data_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                freq = splited_line[1].strip()
                if freq != '1':
                    remove_freq_list.append(line)
        codecs.open(bigram_freq_remove_1_filename, mode='wb', encoding='utf-8').writelines(remove_freq_list)
# remove_freq_1()
def comine_bigram_data():
    '''合并二元组数据，相同words元素，词频(freq)进行叠加'''
    # bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_bigram.txt'%file_count)
    total_bigram_dic = {}
    for file_count in range(1, 29):
        print file_count
        bigram_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s_bigram_remove_freq_1.txt'%file_count)
        with codecs.open(bigram_filename, encoding='utf-8') as f:
            bigram_item_freq_tuple_list = ((item.split('\t')[0], int(item.split('\t')[1]))  for item in f.readlines())
            for bigram_item_freq_tuple in bigram_item_freq_tuple_list:
                bigram_item = bigram_item_freq_tuple[0]
                freq_int = bigram_item_freq_tuple[1]
                check_item = total_bigram_dic.get(bigram_item)
                if check_item:
                    total_bigram_dic[bigram_item] += freq_int
                else:
                    total_bigram_dic[bigram_item] = freq_int

    #合并后的二元组数据写入到本地文件中
    bigram_tuple_freq_list = ['\t'.join((bigram_str, str(freq)))+'\n' for (bigram_str, freq) in total_bigram_dic.items()]
    combine_bigram_freq_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq.txt')
    codecs.open(combine_bigram_freq_filename, mode='wb', encoding='utf-8').writelines(bigram_tuple_freq_list)
# comine_bigram_data()
def sorted_bigram_data():
    '''二元组文件排序'''
    for file_count in range(2, 3):
        print file_count
        bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_bigram.txt'%file_count)
        with codecs.open(bigram_filename, encoding='utf-8') as f:
            sorted_bigram_list = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
        inorder_bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_bigram_inorder.txt'%file_count)
        codecs.open(inorder_bigram_filename, mode='wb', encoding='utf-8').writelines(sorted_bigram_list)
# sorted_bigram_data()
def sorted_trigram_data():
    '''三元组文件排序'''
    for file_count in range(1, 29):
        print file_count
        bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_trigram.txt'%file_count)
        with codecs.open(bigram_filename, encoding='utf-8') as f:
            sorted_bigram_list = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
        inorder_bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_trigram_inorder.txt'%file_count)
        codecs.open(inorder_bigram_filename, mode='wb', encoding='utf-8').writelines(sorted_bigram_list)
# sorted_trigram_data()
# print psutil.virtual_memory()[2]
# inorder_bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', 'combine_bigram_freq_5.txt')
# f = codecs.open(inorder_bigram_filename, mode='a', encoding='utf-8')
# print psutil.virtual_memory()[2]
# f.write('a\n')
# print psutil.virtual_memory()[2]
