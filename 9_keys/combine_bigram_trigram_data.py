__author__ = 'wanghuafeng'
#coding:utf8
import os
import re
import math
import time
import psutil
import codecs

PATH = os.path.dirname(os.path.abspath(__file__))
class CombineFreq:
    def combine_bigram_freq(self):
        combine_bigram_freq_filename = os.path.join(PATH, 'cuted_linguistic_stample', 'combine_bigram_freq_bak.txt')
        com_fileObj = codecs.open(combine_bigram_freq_filename, mode='a', encoding='utf-8')
        for file_count in range(1, 29):
            #28个bigram_filename[1, 28]
            exec "bigram_filename%(bigram_filename_count)s = os.path.join(PATH, 'cuted_linguistic_stample', '%(bigram_inorder)s_bigram_inorder.txt')"%{'bigram_filename_count':file_count, 'bigram_inorder':file_count} in globals(), locals()
            #28个fileobj[1, 28]
            exec "fileObj%(fileObj_count)s = codecs.open(bigram_filename%(bigram_filename_count)s, encoding='utf-8')"%({'fileObj_count':file_count,'bigram_filename_count':file_count}) in globals(), locals()

        bigram_param_list = []
        for fileObj_index in range(1, 29):
            bigram_param_list.append((fileObj_index, eval('next(fileObj%s)'%fileObj_index)))
        #以fileObj的index为key，以bigram_param freq 为value生成字典
        bigram_dic = dict(bigram_param_list)
        file_count = 0
        while 1:
            #按照bigram_param进行排序，返回key（index）值组成的List
            sorted_bigram_dic_keys_list = sorted(bigram_dic.iterkeys(), key=lambda x:bigram_dic[x].split('\t')[0])
            # print sorted_bigram_dic_keys_list

            # print sum([int(item.encode('utf-8').split('\t')[1]) for item in bigram_dic.itervalues()])

            #排序后字典内第一个元素，查找与该元素相等的元素
            if len(sorted_bigram_dic_keys_list) == 0:
                break
            first_index = sorted_bigram_dic_keys_list[0]
            first_item_in_bigram_dic_splited =  bigram_dic[first_index].split('\t')
            first_bigram_param = first_item_in_bigram_dic_splited[0]
            freq_int = int(first_item_in_bigram_dic_splited[1])
            # print first_bigram_param
            # print freq_int

            bigram_dic.pop(first_index)
            try:
                bigram_dic[first_index] = eval('next(fileObj%s)'%first_index)
            except:
                file_count += 1
                print file_count
                if file_count == 28:
                    break
            # count = 0
            for sorted_index in sorted_bigram_dic_keys_list[1:]:
                if first_bigram_param == bigram_dic[sorted_index].split('\t')[0]:
                    # count += 1
                    # print count ,bigram_dic[sorted_index].strip()
                    freq_int += int(bigram_dic[sorted_index].split('\t')[1])
                    bigram_dic.pop(sorted_index)
                    try:
                        bigram_dic[sorted_index] = eval('next(fileObj%s)'%sorted_index)
                    except:
                        file_count += 1
                        print file_count
                        if file_count == 28:
                            break

            com_str = '\t'.join((first_bigram_param, str(freq_int)))
            # print len(bigram_dic)
            com_fileObj.write(com_str+'\n')
            # time.sleep(2)
    # combine_bigram_freq()
    def mk_bigram_inorder(self):
        '''对二元组元素按照第一个汉字进行排序'''
        bigram_freq_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq.txt')
        with codecs.open(bigram_freq_filename, encoding='utf-8') as f:
            sorted_bigram_list = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
        inorder_bigaram_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_inorder.txt')
        codecs.open(inorder_bigaram_filename, mode='wb', encoding='utf-8').writelines(sorted_bigram_list)
    # mk_bigram_inorder()
class GenPercentage:
    '''生成二元组概率'''
    def gen_first_word_total_freq_dic(self):
        '''以第一个元素相同的二元组中元素为key，该元素所有频度之和为value生成字典'''
        start_time = time.time()
        filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
        total_frist_word_freq_dic = {}
        with codecs.open(filename, encoding='utf-8') as cf:
            first_word = ''
            freq_int = 0
            first_word_equal_in_bigram_count = 0
            c = 0
            while 1:
                c += 1
                line = cf.readline()
                if not line:
                    freq_int += 61634
                    total_frist_word_freq_dic[first_word] = freq_int
                    end_time = time.time()
                    print end_time-start_time
                    return total_frist_word_freq_dic
                splited_line = line.split('\t')
                next_word = splited_line[0].split(',')[0]
                if next_word != first_word:
                    if not first_word:
                        first_word_equal_in_bigram_count += 1
                        first_word = next_word
                        freq_int = int(splited_line[1])
                    else:
                        if first_word == 'BOS':
                            freq_int += 61633
                        else:
                            freq_int += 61634
                        total_frist_word_freq_dic[first_word] = freq_int
                        first_word = next_word
                        freq_int = int(splited_line[1])
                        first_word_equal_in_bigram_count = 1
                else:
                    freq_int += int(splited_line[1])
                    first_word_equal_in_bigram_count += 1
    def gen_percentage_of_first_word(self):
        '''求二元组中首元素相同的词频的百分比'''
        total_word_freq_dic = self.gen_first_word_total_freq_dic()
        # first_word_set = set(total_word_freq_dic.keys())
        src_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
        precision_percentage_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_percentage.txt')
        with codecs.open(src_filename, encoding='utf-8') as f,\
        codecs.open(precision_percentage_filename, mode='wb', encoding='utf-8') as wf:
            for line in f.readlines():
                first_word = line.split(',')[0]
                splited_line = line.split('\t')
                word_str = splited_line[0]
                freq = int(splited_line[1]) + 1
                chack_val = total_word_freq_dic.get(first_word)
                if chack_val:
                    freq_percentage = float(freq)/total_word_freq_dic[first_word]
                    com_str = '\t'.join((word_str, str(freq_percentage)))
                    # precision_percentage_str = str(int(math.log10(freq_percentage)*(-20000)))
                    # com_str = '\t'.join((word_str, precision_percentage_str))
                    # time.sleep(1)
                    wf.write(com_str+'\n')
    def add_omited_bigram_param(self):
        '''为不在二元模型中的组合添加权重，赋值1,'''
        total_word_freq_dic = self.gen_first_word_total_freq_dic()
        bigram_weight_list = []
        for (first_word, freq_int) in total_word_freq_dic.iteritems():
            bigram_words = ','.join((first_word, '*'))
            freq_percentage = 1.0/freq_int
            com_str = '\t'.join((bigram_words, str(freq_percentage)))

            # weight = str(int(math.log10(freq_percentage)*(-20000)))
            # com_str = '\t'.join((bigram_words, weight))
            # print com_str
            bigram_weight_list.append(com_str+'\n')
        test_filename = os.path.join(PATH, '0709modify', 'aaa.txt')
        precision_percentage_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_percentage.txt')
        codecs.open(precision_percentage_filename, mode='a', encoding='utf-8').writelines(bigram_weight_list)
# gp = GenPercentage()
# gp.add_omited_bigram_param()

def in_61633_not_in_first_word():
    '''检查在61633文件但是不在二元模型第一个first_word的元素(搐,阂,眙.娠)'''
    src_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
    combine_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000.txt')
    with codecs.open(src_filename, encoding='utf-8') as f:
        first_word_set = set([item.split(',')[0] for item in f.readlines()])
    with codecs.open(combine_filename, encoding='utf-8') as com_f:
        for line in com_f.readlines():
            if line.split('\t')[0] not in first_word_set:
                print line.strip()
# in_61633_not_in_first_word()
