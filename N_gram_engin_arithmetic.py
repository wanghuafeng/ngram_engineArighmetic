__author__ = 'wanghuafeng'
#coding:utf-8
import os
import re
import sys
import math
import glob
import codecs
import itertools
import time

# module_path = 'E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'
# sys.path.append(module_path)
# from  add_words_spell_m import WordsSearch

PATH = os.path.dirname(os.path.abspath(__file__))

class WordList(object):
    def __init__(self):
        pass
    def add_word_pinyin(self):
        '''为单字进行标音'''
        ws = WordsSearch()
        pinyin_set = set()
        single_word_filename = os.path.join(PATH, 'data', 'single_word_5322_with_freq.txt')
        com_str_list = []
        with codecs.open(single_word_filename, encoding='utf8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                pinyin = ' '.join(ws.get_splited_pinyin(word)[0]).replace('*', '')
                com_str = '\t'.join((word, pinyin)) + '\n'
                com_str_list.append(com_str)
        print len(pinyin_set)#402
        new_filename = os.path.join(PATH, 'data', 'single_word_5322_with_pinyin.txt')
        codecs.open(new_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    class AddOmitPinyin:
        '''27万词表中统计出的单字拼音与所有汉字拼音的差集'''
        def gen_single_word_pinyin_set(self):
            single_word_pinyin_filename = os.path.join(PATH, 'data', 'single_word_5322_with_pinyin.txt')
            single_pinyin_set = set()
            with codecs.open(single_word_pinyin_filename, encoding='utf-8') as f:
                for line in f.readlines():
                    spilted_line = line.split('\t')
                    word = spilted_line[0]
                    pinyin = spilted_line[-1].strip()
                    single_pinyin_set.add(pinyin)
                print len(single_pinyin_set)
                return single_pinyin_set
        def total_pinyin_set(self):
            HZout_NoTone_filename = os.path.join(PATH, 'data', 'HZout_NoTone.txt')
            notone_pinyin_set = set()
            with codecs.open(HZout_NoTone_filename, encoding='utf16') as f:
                for line in f.readlines():
                    splited_line = line.split('\t')
                    word = splited_line[0]
                    pinyin = splited_line[1]
                    notone_pinyin_set.add(pinyin)
                print len(notone_pinyin_set)#413
                return notone_pinyin_set
        def get_omit_pinyin(self):
            single_pinyin_set = self.gen_single_word_pinyin_set()
            notone_pinyin_set = self.total_pinyin_set()
            print notone_pinyin_set-single_pinyin_set
    def add_freq_to_single_word(self):
        whole_word_freq_dic = {}
        word_freq_filename = os.path.join(PATH, 'data', 'word_freq_unsorted_from_orginal_data.txt')
        with codecs.open(word_freq_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                freq = splited_line[-1]
                whole_word_freq_dic[word] = freq
        single_word_filename = os.path.join(PATH, 'data', 'single_word_from_95K_5322.txt')
        com_str_list = []
        with codecs.open(single_word_filename, encoding='utf-8') as f:
            for line in f.readlines():
                word = line.strip()
                freq = whole_word_freq_dic.get(word, '0\n')
                com_str = u'\t'.join((word, freq))
                # print com_str
                com_str_list.append(com_str)
        codecs.open(single_word_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def caculate_word_weight(self):
        '''计算词表文件的频率'''
        combine_filename = os.path.join(PATH, 'data', 'single_word_5329.txt')
        new_file_to_write_filename = os.path.join(PATH, 'data', 'single_word_weight_5329.txt')
        with codecs.open(combine_filename, encoding='utf-8') as f, \
            codecs.open(new_file_to_write_filename, mode='wb', encoding='utf-8') as wf:
            line_list = f.readlines()
            sum_freq = sum([int(item.split('\t')[1]) for item in line_list])
            print sum_freq
            for line in line_list:
                splited_line = line.split('\t')
                freq_percentage = int(splited_line[1])/float(sum_freq)
                word = splited_line[0]
                weight =  str(int(math.log10(freq_percentage)*(-20000)))
                com_str = '\t'.join((word, weight))
                wf.write(com_str+'\n')
# wl = WordList()
# wl.caculate_word_weight()
class CutLinguisticData(object):
    '''用新词表进行第二次切割'''
    def gen_cuted_linguistic_data(self):
        '''在非词表出进行切割'''
        src_data_path = r'E:\SVN\linguistic_model\data'
        base_wordlist_filename = os.path.join(PATH,  'data', 'single_word_5329.txt')
        cut_filename = os.path.join(src_data_path, 'linguistic_sample.txt')
        format_str = ''.join([item.split('\t')[0] for item in codecs.open(base_wordlist_filename, encoding='utf-8').readlines()])
        base_wordlist_pattern =re.compile(ur"([%s]+)"%format_str, re.U)
        cuted_linguistic_data_filename = os.path.join(PATH, 'cuted_linguistic_data.txt')
        with codecs.open(cut_filename, encoding='utf-8') as f, \
            codecs.open(cuted_linguistic_data_filename, mode='wb', encoding='utf-8') as wf:
            for line in f.readlines():
                splited_line_list = base_wordlist_pattern.split(line)
                for param in splited_line_list:
                    if len(param) == 0:
                        continue
                    if base_wordlist_pattern.match(param):
                        wf.write(param+'\n')
    def cut_linguistic_sample_into_small_part(self):
        '''将按词表切割后的文件分为150M大小的若干个文件'''
        cuted_filename = os.path.join(PATH, 'cuted_linguistic_data.txt')
        sample_filename_int = 1
        with codecs.open(cuted_filename, encoding='utf-8') as f:
            while 1:
                line = f.read(51470527)
                if not line:
                    break
                stample_filename = os.path.join(PATH, 'splited_linguistic_data', '%s.txt'%sample_filename_int)
                with codecs.open(stample_filename, mode='wb', encoding='utf-8') as wf:
                    wf.write(line)
                sample_filename_int += 1
    def cut_lines_into_words(self):
        '''将行（句子）切割成词，其间以空格隔开'''
        for file_count in range(1, 29):
            total_line_list = []
            print file_count
            src_filename = os.path.join(PATH, 'splited_linguistic_data', '%s.txt'%file_count)
            with codecs.open(src_filename, encoding='utf-8') as f:
                # cuted_lines_list = [' '.join(cs.cut_with_weight(line))+'\n' for line in f.readlines()]
                for line in f.readlines():
                    line_list = []
                    for single_word in line.strip():
                        line_list.append(single_word)
                    new_line = ' '.join(line_list) + '\n'
                    total_line_list.append(new_line)
            codecs.open(src_filename, mode='wb', encoding='utf-8').writelines(total_line_list)
    def cut_sentence_into_words(self):
        '''将行（句子）切割成词，其间以空格隔开'''
        from cut_sentence import Cut_Sentence
        cs = Cut_Sentence()
        src_path = r'F:\linguistic_data\original_data_cuted'
        file_list = os.listdir(src_path)
        for file_name in file_list:
            print file_name
            filename = os.path.join(src_path, file_name)
            with codecs.open(filename, encoding='utf-8') as f:
                cuted_lines_list = [' '.join(cs.cut_with_weight(line))+'\n' for line in f.readlines()]
            codecs.open(filename, mode='wb', encoding='utf-8').writelines(cuted_lines_list)
            # cut_sentence_into_words()
# cs = CutLinguisticData()
# cs.cut_lines_into_words()
class GenNgram(object):
    '''生成n-gram模型'''
    def __init__(self):
        self.src_data_file_path = r'E:\SVN\linguistic_model\N_gram\splited_linguistic_data'
        self.TOTAL_FILE_COUNT = 28
        self.uninorder_file_pattern = '%s_four_gram.txt'#排序前的N元模型
        self.inorder_file_pattern = '%s_four_gram_inorder.txt'#排序后的N元模型
        self.uncombine_inorder_file_pattern = 'four_gram_inorder.txt'#合并前的N元模型
        self.combine_filename = 'four_gram_combine_word_freq.txt'#合并后的N元模型
    def gen_bigram_data(self, ngram='bigram'):
        '''统计二、三元模型'''
        src_data_path = r'E:\SVN\linguistic_model\N_gram'
        des_path = r'E:\SVN\linguistic_model\N_gram\bigram'
        src_data_filename = os.path.join(src_data_path, 'cuted_linguistic_data.txt')
        bigram_freq_dic = {}
        trigram_param_freq_dic = {}
        with codecs.open(src_data_filename, encoding='utf-8') as f:
            for line in (item.strip() for item in f.readlines()):
                if not line:
                    continue
                lenght_of_line = len(line)

                if ngram == 'bigram':
                    # #二元组数据
                    line_bigram_list = []
                    line_bigram_list.append('BOS'+line[0])
                    for i in range(lenght_of_line):
                        if i < lenght_of_line - 1:
                            line_bigram_list.append(line[i]+line[i+1])
                    line_bigram_list.append(line[-1]+'EOS')
                    for bigram_item in line_bigram_list:
                        try:
                            bigram_freq_dic[bigram_item] += 1
                        except:
                            bigram_freq_dic[bigram_item] = 1

                elif ngram == 'trigram':
                        ##三元组数据
                    line_trigram_list = []
                    if lenght_of_line == 2:
                        line_trigram_list.append('BOS'+ line[0]+ line[1])
                        line_trigram_list.append(line[0]+line[1]+'EOS')
                    elif lenght_of_line > 2:
                        line_trigram_list.append('BOS'+line[0]+line[1])
                        for k in range(lenght_of_line):
                            if k < lenght_of_line - 2:
                                line_trigram_list.append(line[k]+line[k+1]+line[k+2])
                            elif k == lenght_of_line - 2:
                                line_trigram_list.append(line[k]+line[k+1]+'EOS')
                    for trigram_item in line_trigram_list:
                        try:
                            trigram_param_freq_dic[trigram_item] += 1
                        except:
                            trigram_param_freq_dic[trigram_item] = 1
        if ngram == 'bigram':
            bigram_tuple_freq_list = ['\t'.join((bigram_item, str(freq)))+'\n' for (bigram_item, freq) in bigram_freq_dic.items()]
            bigram_filename = os.path.join(des_path, 'bigram_combine_freq.txt')
            codecs.open(bigram_filename, mode='wb', encoding='utf-8').writelines(bigram_tuple_freq_list)
        elif ngram == 'trigram':
            trigram_tuple_freq_list = ['\t'.join((trigram_item, str(freq)))+'\n' for (trigram_item, freq) in trigram_param_freq_dic.items()]
            trigram_filename = os.path.join(des_path, 'trigram_combine_freq.txt')
            codecs.open(trigram_filename, mode='wb', encoding='utf-8').writelines(trigram_tuple_freq_list)
    def gen_n_igram_model_data(self, n=4):
        '''统计三元、四元、五元组数据模型'''
        file_name_pattern = 'four' if n==4 else 'five' if n==5 else 'three'
        for file_count in range(1, 29):
            n_gram_param_freq_dic = {}
            # five_gram_param_freq_dic = {}
            print file_count
            src_data_filename = os.path.join(PATH, 'splited_linguistic_data', '%s.txt'%file_count)
            with codecs.open(src_data_filename, encoding='utf-8') as f:
                for line in [item.strip().replace(' ', '') for item in f.readlines()]:
                    if not line:
                        continue
                    splited_list_length = len(line)
                    ###四元组数据
                    if n == 4:
                        line_fourgram_list = []
                        if splited_list_length == 1:
                            # line_fourgram_list.append(('BOS', line[0]))
                            # line_fourgram_list.append((line[0], 'EOS'))
                            continue
                        elif splited_list_length == 2:
                            # line_fourgram_list.append(('BOS', line[0]))
                            # line_fourgram_list.append(('BOS', line[0], line[1]))
                            # line_fourgram_list.append((line[0], line[1], 'EOS'))
                            continue
                        elif splited_list_length == 3:
                            # line_fourgram_list.append(('BOS', line[0]))
                            # line_fourgram_list.append(('BOS', line[0], line[1]))
                            line_fourgram_list.append(('BOS', line[0], line[1], line[2]))
                            line_fourgram_list.append((line[0], line[1], line[2], 'EOS'))
                            # line_fourgram_list.append((line[1], line[2], 'EOS'))
                            # line_fourgram_list.append((line[2], 'EOS'))
                        else:
                            # line_fourgram_list.append(('BOS', line[0]))
                            # line_fourgram_list.append(('BOS',line[0], line[1]))
                            line_fourgram_list.append(('BOS', line[0], line[1], line[2]))
                            for k in range(splited_list_length):
                                if k < splited_list_length - 3:
                                    line_fourgram_list.append((line[k], line[k+1], line[k+2], line[k+3]))
                                elif k == splited_list_length - 3:
                                    line_fourgram_list.append((line[-3], line[-2], line[-1], 'EOS'))
                                # elif k == splited_list_length - 2:
                                #     line_fourgram_list.append((line[-2], line[-1], 'EOS'))
                                # elif k == splited_list_length - 1:
                                #     line_fourgram_list.append((line[-1], 'EOS'))

                                    # for bigram_item in line_fourgram_list:
                                    #     print bigram_item[0], bigram_item[1], bigram_item[2], bigram_item[3]
                                    # time.sleep(1)
                        for fourgram_tuple in line_fourgram_list:
                            try:
                                n_gram_param_freq_dic[fourgram_tuple] += 1
                            except:
                                n_gram_param_freq_dic[fourgram_tuple] = 1

                    # ##五元组数据
                    if n == 5:
                        line_fivegram_list = []
                        if splited_list_length == 1:
                            line_fivegram_list.append(('BOS', line[0]))
                            line_fivegram_list.append((line[0], 'EOS'))
                        elif splited_list_length == 2:
                            line_fivegram_list.append(('BOS', line[0]))
                            line_fivegram_list.append(('BOS', line[0], line[1]))
                            line_fivegram_list.append((line[0], line[1], 'EOS'))
                            line_fivegram_list.append((line[1], 'EOS'))
                        elif splited_list_length == 3:
                            line_fivegram_list.append(('BOS', line[0]))
                            line_fivegram_list.append(('BOS', line[0], line[1]))
                            line_fivegram_list.append(('BOS', line[0], line[1], line[2]))
                            line_fivegram_list.append((line[0], line[1], line[2], 'EOS'))
                            line_fivegram_list.append((line[1], line[2], 'EOS'))
                            line_fivegram_list.append((line[2], 'EOS'))
                        elif splited_list_length == 4:
                            line_fivegram_list.append(('BOS', line[0]))
                            line_fivegram_list.append(('BOS', line[0], line[1]))
                            line_fivegram_list.append(('BOS', line[0], line[1], line[2]))
                            line_fivegram_list.append(('BOS', line[0], line[1], line[2], line[3]))
                            line_fivegram_list.append((line[0], line[1], line[2], line[3], 'EOS'))
                            line_fivegram_list.append((line[1], line[2], line[3], 'EOS'))
                            line_fivegram_list.append((line[2], line[3], 'EOS'))
                            line_fivegram_list.append((line[3], 'EOS'))
                        else:
                            line_fivegram_list.append(('BOS', line[0]))
                            line_fivegram_list.append(('BOS', line[0], line[1]))
                            line_fivegram_list.append(('BOS', line[0], line[1], line[2]))
                            line_fivegram_list.append(('BOS', line[0], line[1], line[2], line[3]))
                            for k in range(splited_list_length):
                                if k < splited_list_length - 4:
                                    line_fivegram_list.append((line[k], line[k+1], line[k+2], line[k+3], line[k+4]))
                                elif k == splited_list_length - 4:
                                    line_fivegram_list.append((line[-4], line[-3], line[-2], line[-1], 'EOS'))
                                elif k == splited_list_length - 3:
                                    line_fivegram_list.append((line[-3], line[-2], line[-1], 'EOS'))
                                elif k == splited_list_length - 2:
                                    line_fivegram_list.append((line[-2], line[-1], 'EOS'))
                                elif k == splited_list_length - 1:
                                    line_fivegram_list.append((line[-1], 'EOS'))
                            # for bigram_item in line_fivegram_list:
                        #     print bigram_item[0], bigram_item[1], bigram_item[2], bigram_item[3], bigram_item[4]
                        # time.sleep(1)
                        for fivegram_tuple in line_fivegram_list:
                            try:
                                n_gram_param_freq_dic[fivegram_tuple] += 1
                            except:
                                n_gram_param_freq_dic[fivegram_tuple] = 1

                # # 写入N元组
                n_gram_com_str_list = ('\t'.join((','.join(n_gram_tuple), str(freq)))+'\n' for (n_gram_tuple, freq) in n_gram_param_freq_dic.items())
                n_gram_filename = os.path.join(self.src_data_file_path, '%(file_count)s_%(file_name_pattern)s_gram.txt'%({'file_count':file_count, 'file_name_pattern':file_name_pattern}))
                codecs.open(n_gram_filename, mode='wb', encoding='utf-8').writelines(n_gram_com_str_list)
                # #写入五元组
                # fivegram_com_str_list = ('\t'.join((','.join(fivegram_tuple), str(freq)))+'\n' for (fivegram_tuple, freq) in n_gram_param_freq_dic.items())
                # n_gram_filename = os.path.join(PATH, '0709modify', 'four_five_gram_item', '%s_five_gram.txt'%file_count)
                # codecs.open(n_gram_filename, mode='wb', encoding='utf-8').writelines(fivegram_com_str_list)
    def mk_n_gram_inorder(self, uninorder_file_pattern, inorder_file_pattern):
        '''N元组文件排序'''
        for file_count in range(1, self.TOTAL_FILE_COUNT+1):
            print file_count
            ngram_filename = os.path.join(self.src_data_file_path, uninorder_file_pattern%file_count)
            with codecs.open(ngram_filename, encoding='utf-8') as f:
                sorted_bigram_list = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
            inorder_bigram_filename = os.path.join(self.src_data_file_path, inorder_file_pattern%file_count)
            codecs.open(inorder_bigram_filename, mode='wb', encoding='utf-8').writelines(sorted_bigram_list)
    def combine_bigram_freq(self, uncombine_file_pattern, combine_filename='combine_word_freq.txt'):
        '''将n个排序后文件的N元模型进行词频叠加'''
        combine_bigram_freq_filename = os.path.join(self.src_data_file_path, combine_filename)
        com_fileObj = codecs.open(combine_bigram_freq_filename, mode='a', encoding='utf-8')
        for file_count in range(1, self.TOTAL_FILE_COUNT+1):
            #28个bigram_filename[1, 28]
            exec "bigram_filename%(bigram_filename_count)s = os.path.join(self.src_data_file_path, '%(bigram_inorder)s_{}'.format(uncombine_file_pattern))"%{'bigram_filename_count':file_count, 'bigram_inorder':file_count} in globals(), locals()
            #28个fileobj[1, 28]
            exec "fileObj%(fileObj_count)s = codecs.open(bigram_filename%(bigram_filename_count)s, encoding='utf-8')"%({'fileObj_count':file_count,'bigram_filename_count':file_count}) in globals(), locals()
        bigram_param_list = []
        for fileObj_index in range(1, self.TOTAL_FILE_COUNT+1):
            bigram_param_list.append((fileObj_index, eval('next(fileObj%s)'%fileObj_index)))
            #以fileObj的index为key，以bigram_param freq 为value生成字典
        bigram_dic = dict(bigram_param_list)
        file_count = 0
        while 1:
            #按照bigram_param进行排序，返回key（index）值组成的List
            sorted_bigram_dic_keys_list = sorted(bigram_dic.iterkeys(), key=lambda x:bigram_dic[x].split('\t')[0])
            # print sum([int(item.encode('utf-8').split('\t')[1]) for item in bigram_dic.itervalues()])
            #排序后字典内第一个元素，查找与该元素相等的元素
            if len(sorted_bigram_dic_keys_list) == 0:
                break
            first_index = sorted_bigram_dic_keys_list[0]
            first_item_in_bigram_dic_splited =  bigram_dic[first_index].split('\t')
            first_bigram_param = first_item_in_bigram_dic_splited[0]
            freq_int = int(first_item_in_bigram_dic_splited[1])
            bigram_dic.pop(first_index)
            try:
                bigram_dic[first_index] = eval('next(fileObj%s)'%first_index)
            except:
                file_count += 1
                print file_count
                if file_count == self.TOTAL_FILE_COUNT:
                    break
            for sorted_index in sorted_bigram_dic_keys_list[1:]:
                if first_bigram_param == bigram_dic[sorted_index].split('\t')[0]:
                    freq_int += int(bigram_dic[sorted_index].split('\t')[1])
                    bigram_dic.pop(sorted_index)
                    try:
                        bigram_dic[sorted_index] = eval('next(fileObj%s)'%sorted_index)
                    except:
                        file_count += 1
                        print file_count
                        if file_count == self.TOTAL_FILE_COUNT:
                            break
            com_str = '\t'.join((first_bigram_param, str(freq_int)))
            com_fileObj.write(com_str+'\n')
    def cut_off_param(self,un_cut_filename='combine_word_freq.txt',cutOff=1):
        '''按cutOff设定值进行裁剪'''
        cut_off_set= set([item for item in range(1, 1+cutOff)])
        un_cut_off_filename = os.path.join(self.src_data_file_path, un_cut_filename)
        assert os.path.isfile(un_cut_off_filename)
        cuted_filename = un_cut_filename.split('.')[0] + '_cutOff=%s.txt'%cutOff
        cuted_off_filename = os.path.join(self.src_data_file_path, cuted_filename)
        read_file_with_readlines = False
        with codecs.open(un_cut_off_filename, encoding='utf-8') as f, \
            codecs.open(cuted_off_filename, mode='wb', encoding='utf-8') as wf:
            if not read_file_with_readlines:#如果数据比较大，则逐行读取数据
                while 1:
                    line = f.readline()
                    if not line:
                        break
                    splited_line = line.split('\t')
                    n_gram_item = splited_line[0]
                    freq = int(splited_line[-1])

                    if freq in cut_off_set:
                        continue
                    else:
                        freq -= cutOff
                        com_str = '\t'.join((n_gram_item, str(freq))) + '\n'
                        wf.write(com_str)
            else:#如果数据在内存允许范围之内，则一次性读取到内存中，速度是逐行读取的10倍
                for line in f.readlines():
                    splited_line = line.split('\t')
                    n_gram_item = splited_line[0]
                    freq = int(splited_line[-1])
                    if freq in cut_off_set:
                        continue
                    else:
                        freq -= cutOff
                        com_str = '\t'.join((n_gram_item, str(freq))) + '\n'
                        wf.write(com_str)
    def put_ngram_item_into_different_file(self, combine_filename):
        '''把ngram语言模型，根据n的值分到不同的文件中'''
        cut_off_filename = os.path.join(self.src_data_file_path, combine_filename)
        bigram_fileanme = os.path.join(self.src_data_file_path, 'n_gram_filename', 'bigram_from_fivegram_item.txt')
        trigram_filename = os.path.join(self.src_data_file_path, 'n_gram_filename', 'trigram_from_fivegram_item.txt')
        fourgram_fileanme = os.path.join(self.src_data_file_path,  'n_gram_filename', 'fourgram_from_fivegram_item.txt')
        fivegram_fileanme = os.path.join(self.src_data_file_path, 'n_gram_filename', 'fivegram_from_fivegram_item.txt')
        lenght_2_ngram_item_list = []
        lenght_3_ngram_item_list = []
        lenght_4_ngram_item_list = []
        lenght_5_ngram_item_list = []
        with codecs.open(cut_off_filename, encoding='utf-8') as f,\
        codecs.open(fivegram_fileanme, mode='wb', encoding='utf-8')as wf:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                ngram_item_words_lenght = len(ngram_item.split(','))
                if ngram_item_words_lenght == 2:
                    lenght_2_ngram_item_list.append(line)
                elif ngram_item_words_lenght == 3:
                    lenght_3_ngram_item_list.append(line)
                elif ngram_item_words_lenght == 4:
                    lenght_4_ngram_item_list.append(line)
                else:
                    wf.write(line)
                    # lenght_5_ngram_item_list.append(line)
        codecs.open(bigram_fileanme, mode='wb', encoding='utf-8').writelines(lenght_2_ngram_item_list)
        codecs.open(trigram_filename, mode='wb', encoding='utf-8').writelines(lenght_3_ngram_item_list)
        codecs.open(fourgram_fileanme, mode='wb', encoding='utf-8').writelines(lenght_4_ngram_item_list)
        # codecs.open(fivegram_fileanme, mode='wb', encoding='utf-8').writelines(lenght_5_ngram_item_list)

# gn = GenNgram()
# gn.gen_bigram_data(ngram='trigram')
# gn.gen_n_igram_model_data(n=4)
# gn.mk_n_gram_inorder(gn.uninorder_file_pattern, gn.inorder_file_pattern)
# gn.combine_bigram_freq(gn.uncombine_inorder_file_pattern, gn.combine_filename)
# gn.cut_off_param(gn.combine_filename, cutOff=1)
# gn.put_ngram_item_into_different_file('five_gram_combine_word_freq.txt')

class CutoffNgramGenWeight(object):
    def __init__(self):
        self.src_data_file_path = r'E:\SVN\linguistic_model\N_gram'
    def mk_n_gram_inorder(self, uninorder_filename):
        '''N元组文件排序'''
        ngram_filename = os.path.join(self.src_data_file_path, uninorder_filename)
        with codecs.open(ngram_filename, encoding='utf-8') as f:
            sorted_bigram_list = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
        inorder_filename = uninorder_filename.split('.')[0] + '_inorder.txt'
        inorder_bigram_filename = os.path.join(self.src_data_file_path, inorder_filename)
        codecs.open(inorder_bigram_filename, mode='wb', encoding='utf-8').writelines(sorted_bigram_list)
    def cut_off_ngram_file(self, ngram_filename, cutoff=1, line_count=0):
        '''二、三、四、五元模型文件
           ngram_filename:待裁剪的文件
           cutoff:裁剪值
           line_count:裁剪后要保留行数
           若设置了裁剪值，则所得文件为比该行数小的最靠近line_count的文件'''
        ngram_file_path = os.path.join(self.src_data_file_path, 'bigram')
        filename = os.path.join(ngram_file_path, ngram_filename)
        pure_cutoff_filename = ngram_filename.split('.')[0]+'_cutoff=%s.txt'%cutoff
        cutoff_filename = os.path.join(ngram_file_path, pure_cutoff_filename)
        cutoff_line_list = []
        total_line_count = 0
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                #除去BOS的项
                if line.startswith('BOS'):
                    continue
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                #除去EOS的项
                if ngram_item.endswith('EOS'):
                    continue
                freq_int = int(splited_line[-1])
                if freq_int > cutoff:
                    total_line_count += 1
                    cutoff_line_list.append(line)
        if line_count:#如果设置了裁剪后数据的行数
            if total_line_count > line_count:#文件行数大于设定值，cutoff值自增1，递归主函数做二次裁剪
                new_cutoff_value = cutoff + 1
                print 'total_line_count:%s cutoff_value:%s'%(total_line_count,new_cutoff_value)
                cutoff_line_list[:] = []
                self.cut_off_ngram_file(ngram_filename, new_cutoff_value, line_count)
            else:#文件行数小宇设定值，则写入本地
                codecs.open(cutoff_filename, mode='wb', encoding='utf-8').writelines(cutoff_line_list)
        else:#若没有设定裁剪数据行数，则按照cutoff值，将裁剪的数据写入本地
            codecs.open(cutoff_filename, mode='wb', encoding='utf-8').writelines(cutoff_line_list)
    def unigram_weight(self):
        filename = os.path.join(self.src_data_file_path, 'bigram', 'unigram_combine_word_freq.txt')
        total_line_list = []
        with codecs.open(filename, encoding='utf-8') as f:
            line_list = f.readlines()
            total_freq = sum([int(item.split('\t')[-1]) for item in line_list])
            print total_freq
            time.sleep(4)
        for line in line_list:
            splited_line = line.split('\t')
            ngram_item = splited_line[0]
            freq_int = int(splited_line[-1])
            percentage = freq_int/float(total_freq)
            weight =  str(int(math.log10(percentage)*(-20000)))
            com_str = ngram_item + '\t' + weight + '\n'
            total_line_list.append(com_str)
        filename_to_write = os.path.join(self.src_data_file_path, 'bigram', 'unigram_item_weight.txt')
        codecs.open(filename_to_write, mode='wb', encoding='utf-8').writelines(total_line_list)
    def bigram_weight(self):
        '''计算二元模型中各个元素出现的概率'''
        filename = os.path.join(self.src_data_file_path, 'bigram', 'bigram_combine_freq_inorder_cutoff=1.txt')
        bos_count = 0
        eos_count = 0
        bigram_item_freq_dic = {}
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    bos_count += freq_int
                elif ngram_item.endswith('EOS'):
                    eos_count += freq_int
                else:
                    try:
                        bigram_item_freq_dic[ngram_item[0]] += freq_int
                    except:
                        bigram_item_freq_dic[ngram_item[0]] = freq_int
        # bigram_item_freq_dic['BOS'] = bos_count
        # bigram_item_freq_dic['EOS'] = eos_count
        total_line_list = []
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    # first_word = ngram_item.split(',')[0]
                    percentage = freq_int/float(bos_count)
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    # com_str = ngram_item + '\t' + str(percentage) + '\n'
                    total_line_list.append(com_str)
                elif ngram_item.endswith('EOS'):
                    percentage = freq_int/float(eos_count)
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    # com_str = ngram_item + '\t' + str(percentage) + '\n'
                    total_line_list.append(com_str)
                else:
                    percentage = float(freq_int)/bigram_item_freq_dic[ngram_item[0]]
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
        filename = os.path.join(self.src_data_file_path, 'bigram', 'bigram_item_weight.txt')
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(total_line_list)
    def trigram_weight(self):
        '''计算三元模型个元素的概率'''
        trigram_filename = os.path.join(self.src_data_file_path, 'bigram', 'trigram_combine_freq_inorder_cutoff=18.txt')
        eos_count = 0
        first_word_freq_dic = {}
        with codecs.open(trigram_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    try:
                        first_word_freq_dic[ngram_item[:-1]] += freq_int
                    except:
                        first_word_freq_dic[ngram_item[:-1]] = freq_int
                #若以EOS结尾，则求解EOS发生的情况下，item为first_word_of_bigram_item的概率
                elif ngram_item.endswith('EOS'):
                    eos_count += freq_int
                else:
                    try:
                        first_word_freq_dic[ngram_item[:-1]] += freq_int
                    except:
                        first_word_freq_dic[ngram_item[:-1]] = freq_int
        total_line_list = []
        with codecs.open(trigram_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith(u'BOS'):
                    percentage = freq_int/float(first_word_freq_dic[ngram_item[:-1]])
                    # percentage = freq_int/float(bos_count)
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
                elif ngram_item.endswith('EOS'):
                    percentage = freq_int/float(eos_count)
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    # com_str = ngram_item + '\t' + str(percentage) + '\n'
                    total_line_list.append(com_str)
                else:
                    percentage = float(freq_int)/first_word_freq_dic[ngram_item[:-1]]
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
        filename = os.path.join(self.src_data_file_path, 'bigram', 'trigram_item_weight.txt')
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(total_line_list)
    def four_gram_weight(self, first_word_count=3):
        '''计算四元模型个元素的概率'''
        trigram_filename = os.path.join(self.src_data_file_path, 'bigram', 'four_gram_combine_word_freq_cutoff=17.txt')
        eos_count = 0
        first_word_freq_dic = {}
        with codecs.open(trigram_filename, encoding='utf-8') as f:
            for line in [item.replace(',', '') for item in f.readlines()]:
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    try:
                        first_word_freq_dic[ngram_item[:-1]] += freq_int
                    except:
                        first_word_freq_dic[ngram_item[:-1]] = freq_int
                elif ngram_item.endswith('EOS'):
                    eos_count += freq_int
                else:
                    try:
                        first_word_freq_dic[ngram_item[:-1]] += freq_int
                    except:
                        first_word_freq_dic[ngram_item[:-1]] = freq_int
        total_line_list = []
        with codecs.open(trigram_filename, encoding='utf-8') as f:
            for line in (item.replace(',', '') for item in f.readlines()):
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    percentage = freq_int/float(first_word_freq_dic[ngram_item[:-1]])
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
                elif ngram_item.endswith('EOS'):
                    percentage = freq_int/float(eos_count)
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
                else:
                    percentage = float(freq_int)/first_word_freq_dic[ngram_item[:-1]]
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
        filename = os.path.join(self.src_data_file_path, 'bigram', 'fourgram_item_weight.txt')
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(total_line_list)
    def five_gram_weight(self, first_word_count=4):
        '''计算五元模型个元素的概率'''
        trigram_filename = os.path.join(self.src_data_file_path, 'bigram', 'fivegram_combine_word_freq_cutoff=53.txt')
        eos_count = 0
        first_word_freq_dic = {}
        with codecs.open(trigram_filename, encoding='utf-8') as f:
            for line in [item.replace(',','') for item in f.readlines()]:
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    try:
                        first_word_freq_dic[ngram_item[:-1]] += freq_int
                    except:
                        first_word_freq_dic[ngram_item[:-1]] = freq_int
                elif ngram_item.endswith('EOS'):
                    eos_count += freq_int
                else:
                    try:
                        first_word_freq_dic[ngram_item[:-1]] += freq_int
                    except:
                        first_word_freq_dic[ngram_item[:-1]] = freq_int
        total_line_list = []
        with codecs.open(trigram_filename, encoding='utf-8') as f:
            for line in (item.replace(',','') for item in f.readlines()):
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if ngram_item.startswith('BOS'):
                    percentage = freq_int/float(first_word_freq_dic[ngram_item[:-1]])
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
                elif ngram_item.endswith('EOS'):
                    percentage = freq_int/float(eos_count)
                    weight =  str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
                else:
                    percentage = float(freq_int)/first_word_freq_dic[ngram_item[:-1]]
                    weight = str(int(math.log10(percentage)*(-20000)))
                    com_str = ngram_item + '\t' + weight + '\n'
                    total_line_list.append(com_str)
        filename = os.path.join(self.src_data_file_path, 'bigram', 'fivegram_item_weight.txt')
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(total_line_list)
    def re_combine_weigh_file(self):
        filepattern = '*weight.txt'
        glob_path = os.path.join(self.src_data_file_path, 'bigram', filepattern)
        filename_list = glob.glob(glob_path)
        print filename_list
        combine_line_list = []
        for filename in filename_list:
            with codecs.open(filename, encoding='utf-8') as f:
                for line in f.readlines():
                    combine_line_list.append(line)
        combine_filename = os.path.join(self.src_data_file_path, 'bigram', 'combine_ngram_weight.txt')
        codecs.open(combine_filename, mode='wb', encoding='utf-8').writelines(combine_line_list)
    def max_weight(self, ngram_weight_filename):
        filename = os.path.join(self.src_data_file_path, 'bigram', ngram_weight_filename)
        weight_set = set()
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                weight = int(splited_line[-1])
                weight_set.add(weight)
        print max(weight_set)#167426

cutoff = CutoffNgramGenWeight()
# cutoff.mk_n_gram_inorder('trigram_combine_freq.txt')
# cutoff.cut_off_ngram_file('bigram_combine_freq_inorder.txt', cutoff=2, line_count=25000000)
# cutoff.cut_off_ngram_file('trigram_combine_freq_inorder.txt', cutoff=18, line_count=5000000)
# cutoff.cut_off_ngram_file('four_gram_combine_word_freq.txt', cutoff=17, line_count=5300000)
# cutoff.cut_off_ngram_file('fivegram_combine_word_freq.txt', cutoff=53, line_count=800000)
# cutoff.unigram_weight()
# cutoff.bigram_weight()
# cutoff.trigram_weight()
# cutoff.four_gram_weight()
# cutoff.five_gram_weight()
# cutoff.re_combine_weigh_file()
# cutoff.max_weight('bigram_item_weight.txt')

# module_path = 'E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'
# sys.path.append(module_path)
# from  add_words_spell_m import WordsSearch
class Key9_InputRules(object):
    '''初始化时，传入待转换文件的路径，调用convert_pinyin_to_rules方法时，传入其文件名，文件可以是\t隔开的第一列是待转换词'''
    def __init__(self, src_path):
        self.src_file_path = src_path
        # self.src_filename = 'single_word_5329.txt'
        # self.src_file_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\arithmetic_param'
    def convert_pinyin_to_rules(self, src_filename):
        '''把基础词库中的拼音转换为输入规则（数字序列）'''
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        from add_pinyin_to_single_word import AddPinyin
        addpinyin = AddPinyin()
        base_filename = os.path.join(self.src_file_path, src_filename)
        filename_without_suffix = src_filename.split('.')[0]
        base_file_with_pinyin_role = os.path.join(self.src_file_path, '%s_pinyin_role'
                                                                      '.txt'%filename_without_suffix)
        with codecs.open(base_filename, encoding='utf-8') as f, \
            codecs.open(base_file_with_pinyin_role, mode='wb', encoding='utf-8') as wf:
            whole_word_list = (item.split('\t')[0] for item in f.readlines())
            for word in whole_word_list:
                pinyin_str = addpinyin.get_pinyin(word)
                role_num = ''.join([coding_map[letter] for letter in pinyin_str if letter.isalpha()])
                com_str = '\t'.join((word, pinyin_str, role_num))
                wf.write(com_str+'\n')
        self.mk_base_file_inorder(base_file_with_pinyin_role)
    def mk_base_file_inorder(self, file_with_pinyin_roles):
        '''基础词库按照输入规则进行排序'''
        base_file_with_pinyin = os.path.join(self.src_file_path, file_with_pinyin_roles)
        filename_without_suffix = base_file_with_pinyin.split('.')[0]
        base_file_with_pinyin_inorder = os.path.join(self.src_file_path, '%s_inorder.txt'%filename_without_suffix)
        with codecs.open(base_file_with_pinyin, encoding='utf-8') as f, \
            codecs.open(base_file_with_pinyin_inorder, mode='wb', encoding='utf-8') as wf:
            temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[2])
            wf.writelines(temp_list_for_write)
        self.gen_role_num_words_mapping(base_file_with_pinyin_inorder)
        os.remove(os.path.join(self.src_file_path, file_with_pinyin_roles))
    def gen_role_num_words_mapping(self, file_with_pinyin_inorder):
        '''以输入规则（数字序列）为key，该序列对应的多个汉字（逗号隔开）作为value，生成文件'''
        total_mapping_dic = {}
        base_file_with_pinyin_inorder_filename = os.path.join(self.src_file_path, file_with_pinyin_inorder)
        filename_without_suffix = file_with_pinyin_inorder.split('.')[0]
        mapping_base_file_with_pinyin_inorder_filename = os.path.join(self.src_file_path, '%s_mapping_9key.txt'%filename_without_suffix)
        with codecs.open(base_file_with_pinyin_inorder_filename, encoding='utf-8') as f, \
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
            for role_num, word_str_list in total_mapping_dic.iteritems():
                com_str = '\t'.join((role_num, ','.join(word_str_list)))
                wf.write(com_str+'\n')
        self.mapping_file_inorder(mapping_base_file_with_pinyin_inorder_filename)
        os.remove(os.path.join(self.src_file_path, file_with_pinyin_inorder))
    def mapping_file_inorder(self, mapping_file):
        '''按照输入规则进行排序'''
        mapping_base_file_with_pinyin_inorder_filename = os.path.join(self.src_file_path, mapping_file)
        with codecs.open(mapping_base_file_with_pinyin_inorder_filename, encoding='utf-8') as f:
            temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
        with codecs.open(mapping_base_file_with_pinyin_inorder_filename, mode='wb', encoding='utf-8') as wf:
            wf.writelines(temp_list_for_write)
        self.get_prefix_of_mapping_role(mapping_file)
    def get_prefix_of_mapping_role(self, mapping_file):
        '''输出所有输入规则的真前缀'''
        mapping_filename = os.path.join(self.src_file_path, mapping_file)
        total_profix_set = set()
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                role_num = splited_line[0]
                for i in range(1, len(role_num)):
                    total_profix_set.add(role_num[0:i]+'\n')
        prefix_filename = os.path.join(self.src_file_path, 'prefix_if_mapping_role_num.txt')
        temp_list_for_write = sorted(total_profix_set, key=lambda x:x.strip())
        codecs.open(prefix_filename, mode='wb', encoding='utf-8').writelines(temp_list_for_write)
# roles = Key9_InputRules(r'E:\SVN\linguistic_model\N_gram\data')
# roles.convert_pinyin_to_rules('single_word_5329.txt')
# roles.mk_base_file_inorder('single_word_5329_pinyin_role_9key.txt')
class Key26_InputRules(object):
    def __init__(self):
        pass
    def convert_pinyin_to_rules(self):
        '''把基础词库中的拼音转换为输入规则（数字序列）'''
        from add_pinyin_to_single_word import AddPinyin
        addpinyin = AddPinyin()
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        base_filename = os.path.join(PATH, 'data', 'single_word_5329.txt')
        base_file_with_pinyin = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_26key.txt')
        with codecs.open(base_filename, encoding='utf-8') as f, \
            codecs.open(base_file_with_pinyin, mode='wb', encoding='utf-8') as wf:
            whole_word_list = (item.split('\t')[0] for item in f.readlines())
            for word in whole_word_list:
                pinyin_str = addpinyin.get_pinyin(word)
                com_str = '\t'.join((word, pinyin_str))
                wf.write(com_str+'\n')
    def mk_base_file_inorder(self):
        '''基础词库按照输入规则进行排序'''
        base_file_with_pinyin = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_26key.txt')
        base_file_with_pinyin_inorder = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_26key.txt')
        with codecs.open(base_file_with_pinyin, encoding='utf-8') as f, \
            codecs.open(base_file_with_pinyin_inorder, mode='wb', encoding='utf-8') as wf:
            temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[-1])
            wf.writelines(temp_list_for_write)
    def gen_role_num_words_mapping(self):
        '''以输入规则（数字序列）为key，该序列对应的多个汉字（逗号隔开）作为value，生成文件'''
        total_mapping_dic = {}
        base_file_with_pinyin_inorder_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_26key.txt')
        mapping_base_file_with_pinyin_inorder_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_26key.txt')
        with codecs.open(base_file_with_pinyin_inorder_filename, encoding='utf-8') as f, \
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
    def mapping_file_inorder(self):
        '''按照输入规则进行排序'''
        mapping_base_file_with_pinyin_inorder_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_26key.txt')
        with codecs.open(mapping_base_file_with_pinyin_inorder_filename, encoding='utf-8') as f:
            temp_list_for_write = sorted(f.readlines(), key=lambda x:x.split('\t')[0])
        with codecs.open(mapping_base_file_with_pinyin_inorder_filename, mode='wb', encoding='utf-8') as wf:
            wf.writelines(temp_list_for_write)
    def get_prefix_of_mapping_role(self):
        '''输出所有输入规则的真前缀'''
        mapping_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_26key.txt')
        total_profix_set = set()
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                role_num = splited_line[0]
                if len(role_num) == 1:
                    print line.strip()
                for i in range(1, len(role_num)):
                    total_profix_set.add(role_num[0:i]+'\n')
        prefix_filename = os.path.join(PATH, 'data', 'prefix_if_mapping_role_num_26key.txt')
        temp_list_for_write = sorted(total_profix_set, key=lambda x:x.strip())
        codecs.open(prefix_filename, mode='wb', encoding='utf-8').writelines(temp_list_for_write)
    # get_prefix_of_mapping_role()
# key26 = Key26_InputRules()
# key26.convert_pinyin_to_rules()
# key26.mk_base_file_inorder()
# key26.gen_role_num_words_mapping()
# key26.get_prefix_of_mapping_role()
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
            if word_index < 4:
                ngram_item = 'BOS' + ''.join(words_list[:word_index+1])
                weight = self.ngram_weight_dic.get(ngram_item, 200000)
                print ngram_item, weight
                sentence_weight += weight

            # if word_index == 0:
            #     ngram_item = 'BOS' + words_list[0]
            #     weight = self.ngram_weight_dic.get(ngram_item, 200000)
            # elif word_index == 1:
            #     try:
            #         ngram_item = 'BOS' + ''.join(words_list[:word_index+1])#BOS,0,1三元模型
            #         weight = self.ngram_weight_dic[ngram_item]
            #     except:
            #         ngram_item = 'BOS' + ''.join(words_list[1:word_index+1])#退至BOS,
            #         weight = self.ngram_weight_dic.get(ngram_item, )

            elif words_list_lenght >= 4:
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
                            ngram_item = ''.join((words_list[word_index-1], words_list[word_index]))
                            weight = self.ngram_weight_dic.get(ngram_item, 100000)+100000
                print ngram_item, weight
                sentence_weight += weight
        try:
            ngram_item = ''.join(words_list[-4:]) + 'EOS'
            weight = self.ngram_weight_dic[ngram_item]
        except KeyError:#若五元模型不存在该元素，则退至四元模型
            try:
                ngram_item = ''.join(words_list[-3:])+ 'EOS'
                weight = self.ngram_weight_dic[ngram_item]+10000
            except KeyError:
                try:
                    ngram_item = ''.join(words_list[-2:]) + 'EOS'
                    weight = self.ngram_weight_dic[ngram_item]+50000
                except KeyError:
                    ngram_item = ''.join(words_list[-1:]) + 'EOS'
                    weight = self.ngram_weight_dic.get(ngram_item, 100000)+100000
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

# ea = EngineArithmetic()
# while 1:#计算在没有路径裁剪情况下句子的实际权重
#     sentence = raw_input('input your sentence:')
#     word_list = [item for item in sentence.decode('utf-8')]
#     ea.caculate_weight_of_word_list(word_list)

class AliEngineArithmetic(object):
    def __init__(self):
        self.MAX_LENGHT = 50
        self.real_prefix_set_9key = set()
        self.real_prefix_set_26key = set()
        self.total_mapping_dic_9key = {}
        self.total_mapping_dic_26key = {}
        self.word_weight_dic = {}
        self._real_prefix_rolenum()
        self._load_mapping_rolenum_wordlist()
        self._load_word_weigh()
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_9key_filename = os.path.join(PATH, 'data', 'prefix_if_mapping_role_num_9key.txt')
        real_prefix_26key_filename = os.path.join(PATH, 'data', 'prefix_if_mapping_role_num_26key.txt')
        with codecs.open(real_prefix_9key_filename, encoding='utf-8') as f:
            self.real_prefix_set_9key = set([item.strip() for item in f.readlines()])
        with codecs.open(real_prefix_26key_filename, encoding='utf-8') as f:
            self.real_prefix_set_26key = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_9key_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_9key.txt')
        mapping_26key_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_26key.txt')
        with codecs.open(mapping_9key_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic_9key = dict(role_num_words)
        with codecs.open(mapping_26key_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic_26key = dict(role_num_words)
    def _load_word_weigh(self):
        '''加载N元组模型，以N元组元素为key，与权重构成字典'''
        word_weight_filename = os.path.join(PATH, 'bigram', 'combine_ngram_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            # while True:
            #     line = f.readline()
            #     if not line:
            #         break
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                weight = int(splited_line[-1])
                self.word_weight_dic[ngram_item] = weight
    def handle_key_input_str(self, key_input, top_count=3):
        key_input = key_input.strip()
        matched_route_list = [('#',[],0)]
        prefix_route_list = []
        lenght_key_input = len(key_input)
        key_input_index = 0
        if key_input.isdigit():
            for key in key_input:
                #key是否有mapping匹配
                temp_matched_route_list = []
                temp_prefix_route_list = []
                key_mapping_word_list = self.total_mapping_dic_9key.get(key)

                #如果key有汉字匹配
                if key_mapping_word_list:
                    #对matched_route_list的影响
                    for mapping_word in key_mapping_word_list:
                        for last_matched_route_param in matched_route_list:
                            #matched_route_list三元组中汉字部分是否为空数组
                            if last_matched_route_param[1]:
                                # if len(last_matched_route_param[1]) < 4:
                                #     # ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-3:]), mapping_word)
                                #     # weight = self.word_weight_dic.get(ngram_item, 200000)
                                #     try:
                                #         ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-3:]), mapping_word)
                                #         weight = self.word_weight_dic[ngram_item]+10000
                                #     except:
                                #         # ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-2:]),
                                #         #                          mapping_word)
                                #         # weight = self.word_weight_dic.get(ngram_item, 200000)
                                #         try:
                                #             ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-2:]),
                                #                                      mapping_word)
                                #             weight = self.word_weight_dic[ngram_item]+50000
                                #         except:
                                #             ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-1:]),mapping_word)
                                #             weight = self.word_weight_dic.get(ngram_item, 100000)+100000
                                history_route_lenght = len(last_matched_route_param[1])
                                if history_route_lenght == 1:#二元模型
                                    ngram_item = u'BOS%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                    weight = self.word_weight_dic.get(ngram_item, 200000)
                                elif history_route_lenght == 2:#三元模型
                                    try:
                                        ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-2:]),mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#退回到二元
                                        ngram_item = u'%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                        weight = self.word_weight_dic.get(ngram_item, 100000)+100000
                                elif history_route_lenght == 3:#四元模型
                                    try:
                                        ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-3:]),
                                                                 mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#退回到三元
                                        try:
                                            ngram_item = u'%s%s'%(''.join(last_matched_route_param[1][-2:]),mapping_word)
                                            weight = self.word_weight_dic[ngram_item] + 50000
                                        except:#退回到二元
                                            ngram_item = u'%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                            weight = self.word_weight_dic.get(ngram_item, 100000) + 100000

                                else:
                                    try:
                                        ngram_item = ''.join(last_matched_route_param[1][-4:])+mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(last_matched_route_param[1][-3:])+mapping_word
                                            weight = self.word_weight_dic[ngram_item]+10000
                                        except:
                                            # ngram_item = ''.join(last_matched_route_param[1][-2:])+mapping_word
                                            # weight = self.word_weight_dic.get(ngram_item, 200000)
                                            try:
                                                ngram_item = ''.join(last_matched_route_param[1][-2:])+mapping_word
                                                weight = self.word_weight_dic[ngram_item]+50000
                                            except:
                                                ngram_item = ''.join(last_matched_route_param[1][-1:])+mapping_word
                                                weight = self.word_weight_dic.get(ngram_item, 100000)+100000

                                #如果查不到bigram_item对应的weight
                                # if not weight:
                                #     bigram_item = last_matched_route_param[1][-1]+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                            #key_input_str中的第一个key有匹配
                            else:
                                ngram_item = 'BOS'+ mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # if not weight:
                                #     bigram_item = 'BOS'+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                        ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                #key不匹配mapping_word
                else:
                    ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                # if len(temp_matched_route_list)>self.MAX_LENGHT:
                #     temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                #     temp_matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]
                # if len(temp_prefix_route_list)>self.MAX_LENGHT:
                #     temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                #     temp_prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]

                #key+old_key_str是否有对应汉字匹配
                for prefix_route_param_tuple in prefix_route_list:
                    old_key_str = prefix_route_param_tuple[0]
                    new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                    new_keys_mapping_words_list = self.total_mapping_dic_9key.get(new_combine_keys)
                    #如果combine_keys对应有汉字匹配
                    if new_keys_mapping_words_list:
                        #对matched_route_list的影响
                        for mapping_word in new_keys_mapping_words_list:
                            #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                            if not prefix_route_param_tuple[1]:
                                ngram_item = 'BOS'+mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # if not weight:
                                #     bigram_item = 'BOS'+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                temp_matched_route_list.append(('#', [mapping_word], weight))
                            #（old_key_str,[],weight）第二个参数不为空
                            else:
                                # bigram_item = prefix_route_param_tuple[1][-1]+','+ mapping_word
                                if len(prefix_route_param_tuple[1]) < 4:
                                    # ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-3:]), mapping_word)
                                    # weight = self.word_weight_dic.get(ngram_item, 200000)
                                    #
                                    # try:
                                    #     ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-3:]), mapping_word)
                                    #     weight = self.word_weight_dic[ngram_item]+10000
                                    # except:
                                    #     # ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),
                                    #     #                         mapping_word)
                                    #     # weight = self.word_weight_dic.get(ngram_item, 200000)
                                    #     try:
                                    #         ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),
                                    #                                 mapping_word)
                                    #         weight = self.word_weight_dic[ngram_item]+50000
                                    #     except:
                                    #         ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-1:]),
                                    #                                 mapping_word)
                                    #         weight = self.word_weight_dic.get(ngram_item, 100000)+100000
                                    # print ngram_item, weight
                                    history_route_lenght = len(prefix_route_param_tuple[1])
                                    if history_route_lenght == 1:#二元模型
                                        ngram_item = u'BOS%s%s'%(prefix_route_param_tuple[1][-1],mapping_word)
                                        weight = self.word_weight_dic.get(ngram_item, 200000)
                                    elif history_route_lenght == 2:#三元模型
                                        try:
                                            ngram_item = u'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),mapping_word)
                                            weight = self.word_weight_dic[ngram_item]
                                        except:#退回到二元
                                            ngram_item = u'%s%s'%(prefix_route_param_tuple[1][-1],mapping_word)
                                            weight = self.word_weight_dic.get(ngram_item, 100000)+100000
                                    elif history_route_lenght == 3:#四元模型
                                        try:
                                            ngram_item = u'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-3:]),
                                                                     mapping_word)
                                            weight = self.word_weight_dic[ngram_item]
                                        except:#退回到三元
                                            try:
                                                ngram_item = u'%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),mapping_word)
                                                weight = self.word_weight_dic[ngram_item] + 50000
                                            except:#退回到二元
                                                ngram_item = u'%s%s'%(prefix_route_param_tuple[1][-1],mapping_word)
                                                weight = self.word_weight_dic.get(ngram_item, 100000) + 100000

                                else:
                                    try:
                                        ngram_item = ''.join(prefix_route_param_tuple[1][-4:]) + mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(prefix_route_param_tuple[1][-3:]) + mapping_word
                                            weight = self.word_weight_dic[ngram_item]+10000
                                        except:
                                            # ngram_item = ''.join(prefix_route_param_tuple[1][-2:]) + mapping_word
                                            # weight = self.word_weight_dic.get(ngram_item, 200000)
                                            try:
                                                ngram_item = ''.join(prefix_route_param_tuple[1][-2:]) + mapping_word
                                                weight = self.word_weight_dic[ngram_item]+50000
                                            except:
                                                ngram_item = ''.join(prefix_route_param_tuple[1][-1:]) + mapping_word
                                                weight = self.word_weight_dic.get(ngram_item, 100000)+100000
                                # if not weight:
                                #     bigram_item = prefix_route_param_tuple[1][-1]+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                                new_weight = weight + prefix_route_param_tuple[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                            #对prefix_route_list的影响
                        new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                    #key+old_key_str是否有对应汉字匹配
                    else:
                        if new_combine_keys in self.real_prefix_set_9key:
                            new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                            new_prefix_route_weight = prefix_route_param_tuple[-1]
                            temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

                if len(temp_matched_route_list)>self.MAX_LENGHT:
                    temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                    matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]

                else:
                    matched_route_list = temp_matched_route_list[:]

                # matched_route_list = temp_matched_route_list[:]

                if len(temp_prefix_route_list)>self.MAX_LENGHT:
                    temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                    prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]
                else:
                    prefix_route_list = temp_prefix_route_list[:]

                # prefix_route_list = temp_prefix_route_list[:]
                ##按键到最后一位时，添加EOS
                key_input_index += 1
                if key_input_index == lenght_key_input:
                    final_bigram_weight_list = []
                    for matched_route_param in matched_route_list:
                        mapping_word_list = matched_route_param[1]
                        if mapping_word_list:
                            try:
                                ngram_item = u'%sEOS'%''.join(mapping_word_list[-4:])
                                weight = self.word_weight_dic[ngram_item]
                            except:
                                try:
                                    ngram_item = u'%sEOS'%''.join(mapping_word_list[-3:])
                                    weight = self.word_weight_dic[ngram_item]+10000
                                except:
                                    # ngram_item = u'%sEOS'%''.join(mapping_word_list[-2:])
                                    # weight = self.word_weight_dic.get(ngram_item, 200000)
                                    try:
                                        ngram_item = u'%sEOS'%''.join(mapping_word_list[-2:])
                                        weight = self.word_weight_dic[ngram_item]+50000
                                    except:
                                        ngram_item = u'%sEOS'%mapping_word_list[-1]
                                        weight = self.word_weight_dic.get(ngram_item, 100000)+100000
                            new_matched_word_list = mapping_word_list
                            new_weight = weight + matched_route_param[-1]
                            final_bigram_weight_list.append((''.join(new_matched_word_list), new_weight))
                    return sorted(final_bigram_weight_list, key=lambda x:x[-1])[:top_count]
        #二十六键输入规则
        elif key_input.isalpha():
            for key in key_input:
                #key是否有mapping匹配
                temp_matched_route_list = []
                temp_prefix_route_list = []
                key_mapping_word_list = self.total_mapping_dic_26key.get(key)

                #如果key有汉字匹配
                if key_mapping_word_list:
                    #对matched_route_list的影响
                    for mapping_word in key_mapping_word_list:
                        for last_matched_route_param in matched_route_list:
                            #matched_route_list三元组中汉字部分是否为空数组
                            if last_matched_route_param[1]:
                                if len(last_matched_route_param[1]) < 4:
                                    try:
                                        ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-3:]), mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-2:]),mapping_word)
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            ngram_item = u'BOS%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                            weight = self.word_weight_dic.get(ngram_item, 200000)
                                else:
                                    try:
                                        ngram_item = ''.join(last_matched_route_param[1][-4:])+mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(last_matched_route_param[1][-3:])+mapping_word
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            try:
                                                ngram_item = ''.join(last_matched_route_param[1][-2:])+mapping_word
                                                weight = self.word_weight_dic[ngram_item]
                                            except:
                                                ngram_item = last_matched_route_param[1][-1]+mapping_word
                                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # bigram_item = last_matched_route_param[1][-1]+','+ mapping_word
                                # weight = self.word_weight_dic.get(bigram_item)
                                #如果查不到bigram_item对应的weight
                                # if not weight:
                                #     bigram_item = last_matched_route_param[1][-1]+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                            #key_input_str中的第一个key有匹配
                            else:
                                ngram_item = 'BOS'+ mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # if not weight:
                                #     bigram_item = 'BOS'+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                                ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                #key不匹配mapping_word
                else:
                    ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                # if len(temp_matched_route_list)>self.MAX_LENGHT:
                #     temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                #     temp_matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]
                # if len(temp_prefix_route_list)>self.MAX_LENGHT:
                #     temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                #     temp_prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]

                #key+old_key_str是否有对应汉字匹配
                for prefix_route_param_tuple in prefix_route_list:
                    old_key_str = prefix_route_param_tuple[0]
                    new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                    new_keys_mapping_words_list = self.total_mapping_dic_26key.get(new_combine_keys)
                    #如果combine_keys对应有汉字匹配
                    if new_keys_mapping_words_list:
                        #对matched_route_list的影响
                        for mapping_word in new_keys_mapping_words_list:
                            #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                            if not prefix_route_param_tuple[1]:
                                ngram_item = 'BOS'+mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # if not weight:
                                #     bigram_item = 'BOS'+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                temp_matched_route_list.append(('#', [mapping_word], weight))
                            #（old_key_str,[],weight）第二个参数不为空
                            else:
                                # bigram_item = prefix_route_param_tuple[1][-1]+','+ mapping_word
                                if len(prefix_route_param_tuple[1]) < 4:
                                    try:
                                        ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-3:]), mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),
                                                                    mapping_word)
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-1:]),
                                                                    mapping_word)
                                            weight = self.word_weight_dic.get(ngram_item, 200000)
                                else:
                                    try:
                                        ngram_item = ''.join(prefix_route_param_tuple[1][-4:]) + mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(prefix_route_param_tuple[1][-3:]) + mapping_word
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            try:
                                                ngram_item = ''.join(prefix_route_param_tuple[1][-2:]) + mapping_word
                                                weight = self.word_weight_dic[ngram_item]
                                            except:
                                                ngram_item = prefix_route_param_tuple[1][-1] + mapping_word
                                                weight = self.word_weight_dic.get(ngram_item, 200000)
                                    # if not weight:
                                #     bigram_item = prefix_route_param_tuple[1][-1]+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                                new_weight = weight + prefix_route_param_tuple[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                                #对prefix_route_list的影响
                        new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                    #key+old_key_str是否有对应汉字匹配
                    else:
                        if new_combine_keys in self.real_prefix_set_26key:
                            new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                            new_prefix_route_weight = prefix_route_param_tuple[-1]
                            temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

                if len(temp_matched_route_list)>self.MAX_LENGHT:
                    temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                    matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]

                else:
                    matched_route_list = temp_matched_route_list[:]

                # matched_route_list = temp_matched_route_list[:]

                if len(temp_prefix_route_list)>self.MAX_LENGHT:
                    temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                    prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]
                else:
                    prefix_route_list = temp_prefix_route_list[:]

                # prefix_route_list = temp_prefix_route_list[:]
                ##按键到最后一位时，添加EOS
                key_input_index += 1
                if key_input_index == lenght_key_input:
                    final_bigram_weight_list = []
                    for matched_route_param in matched_route_list:
                        mapping_word_list = matched_route_param[1]
                        if mapping_word_list:
                            try:
                                ngram_item = u'%sEOS'%''.join(mapping_word_list[-4:])
                                weight = self.word_weight_dic[ngram_item]
                            except:
                                try:
                                    ngram_item = u'%sEOS'%''.join(mapping_word_list[-3:])
                                    weight = self.word_weight_dic[ngram_item]
                                except:
                                    try:
                                        ngram_item = u'%sEOS'%''.join(mapping_word_list[-2:])
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        ngram_item = u'%sEOS'%mapping_word_list[-1]
                                        weight = self.word_weight_dic.get(ngram_item, 200000)
                            new_matched_word_list = mapping_word_list
                            new_weight = weight + matched_route_param[-1]
                            final_bigram_weight_list.append((''.join(new_matched_word_list), new_weight))
                    return sorted(final_bigram_weight_list, key=lambda x:x[-1])[:top_count]

# ea = AliEngineArithmetic()
# key_input = '6464842622484269363893663926463'
# list_ngram = ea.handle_key_input_str(key_input, 5)
# for ngram_tuple in list_ngram:
#     print ngram_tuple[0], ngram_tuple[-1]
class EngineArithmetic_No_BOS(object):
    def __init__(self):
        self.MAX_LENGHT = 50
        self.real_prefix_set_9key = set()
        self.real_prefix_set_26key = set()
        self.total_mapping_dic_9key = {}
        self.total_mapping_dic_26key = {}
        self.word_weight_dic = {}
        self._real_prefix_rolenum()
        self._load_mapping_rolenum_wordlist()
        self._load_word_weigh()
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_9key_filename = os.path.join(PATH, 'data', 'prefix_if_mapping_role_num_9key.txt')
        real_prefix_26key_filename = os.path.join(PATH, 'data', 'prefix_if_mapping_role_num_26key.txt')
        with codecs.open(real_prefix_9key_filename, encoding='utf-8') as f:
            self.real_prefix_set_9key = set([item.strip() for item in f.readlines()])
        with codecs.open(real_prefix_26key_filename, encoding='utf-8') as f:
            self.real_prefix_set_26key = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_9key_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_9key.txt')
        mapping_26key_filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_26key.txt')
        with codecs.open(mapping_9key_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic_9key = dict(role_num_words)
        with codecs.open(mapping_26key_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic_26key = dict(role_num_words)
    def _load_word_weigh(self):
        '''加载N元组模型，以N元组元素为key，与权重构成字典'''
        word_weight_filename = os.path.join(PATH, 'bigram', 'combine_ngram_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            # while True:
            #     line = f.readline()
            #     if not line:
            #         break
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                weight = int(splited_line[-1])
                self.word_weight_dic[ngram_item] = weight
    def handle_key_input_str(self, key_input, top_count=3):
        key_input = key_input.strip()
        matched_route_list = [('#',[],0)]
        prefix_route_list = []
        lenght_key_input = len(key_input)
        key_input_index = 0
        if key_input.isdigit():
            for key in key_input:
                #key是否有mapping匹配
                temp_matched_route_list = []
                temp_prefix_route_list = []
                key_mapping_word_list = self.total_mapping_dic_9key.get(key)

                #如果key有汉字匹配
                if key_mapping_word_list:
                    #对matched_route_list的影响
                    for mapping_word in key_mapping_word_list:
                        for last_matched_route_param in matched_route_list:
                            #matched_route_list三元组中汉字部分是否为空数组
                            if last_matched_route_param[1]:
                                history_route_lenght = len(last_matched_route_param[1])
                                if history_route_lenght == 1:#二元模型
                                    try:
                                        ngram_item = u'%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#回退到一元模型
                                        weight = self.word_weight_dic.get(mapping_word, 150000)+100000
                                elif history_route_lenght == 2:#三元模型
                                    try:
                                        ngram_item = u'%s%s'%(''.join(last_matched_route_param[1][-2:]),mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#退回到二元
                                        try:
                                            ngram_item = u'%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                            weight = self.word_weight_dic[ngram_item]+ 100000
                                        except:#退回到一元
                                            weight = self.word_weight_dic.get(mapping_word, 150000)+100000
                                elif history_route_lenght == 3:#四元模型
                                    try:
                                        ngram_item = u'%s%s'%(''.join(last_matched_route_param[1][-3:]),mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#退回到三元
                                        try:
                                            ngram_item = u'%s%s'%(''.join(last_matched_route_param[1][-2:]),mapping_word)
                                            weight = self.word_weight_dic[ngram_item] + 50000
                                        except:#退回到二元
                                            try:
                                                ngram_item = u'%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                                weight = self.word_weight_dic[ngram_item]+100000
                                            except:# 退回到一元模型
                                                weight = self.word_weight_dic.get(mapping_word, 150000)+100000
                                else:
                                    try:
                                        ngram_item = ''.join(last_matched_route_param[1][-4:])+mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(last_matched_route_param[1][-3:])+mapping_word
                                            weight = self.word_weight_dic[ngram_item]+10000
                                        except:
                                            try:
                                                ngram_item = ''.join(last_matched_route_param[1][-2:])+mapping_word
                                                weight = self.word_weight_dic[ngram_item]+50000
                                            except:
                                                try:
                                                    ngram_item = ''.join(last_matched_route_param[1][-1:])+mapping_word
                                                    weight = self.word_weight_dic[ngram_item]+100000
                                                except:
                                                    weight = self.word_weight_dic.get(mapping_word, 150000)+100000

                                #如果查不到bigram_item对应的weight
                                # if not weight:
                                #     bigram_item = last_matched_route_param[1][-1]+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                            #key_input_str中的第一个key有匹配
                            else:
                                ngram_item = mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 250000)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                                ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                #key不匹配mapping_word
                else:
                    ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                # if len(temp_matched_route_list)>self.MAX_LENGHT:
                #     temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                #     temp_matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]
                # if len(temp_prefix_route_list)>self.MAX_LENGHT:
                #     temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                #     temp_prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]

                #key+old_key_str是否有对应汉字匹配
                for prefix_route_param_tuple in prefix_route_list:
                    old_key_str = prefix_route_param_tuple[0]
                    new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                    new_keys_mapping_words_list = self.total_mapping_dic_9key.get(new_combine_keys)
                    #如果combine_keys对应有汉字匹配
                    if new_keys_mapping_words_list:
                        #对matched_route_list的影响
                        for mapping_word in new_keys_mapping_words_list:
                            #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                            if not prefix_route_param_tuple[1]:
                                ngram_item = mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 250000)
                                temp_matched_route_list.append(('#', [mapping_word], weight))
                            #（old_key_str,[],weight）第二个参数不为空
                            else:
                                history_route_lenght = len(prefix_route_param_tuple[1])
                                if history_route_lenght == 1:#二元模型
                                    try:
                                        ngram_item = u'%s%s'%(prefix_route_param_tuple[1][-1],mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#回退到一元模型
                                        weight = self.word_weight_dic.get(mapping_word, 150000)+100000
                                elif history_route_lenght == 2:#三元模型
                                    try:
                                        ngram_item = u'%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#退回到二元
                                        try:
                                            ngram_item = u'%s%s'%(prefix_route_param_tuple[1][-1],mapping_word)
                                            weight = self.word_weight_dic[ngram_item]+100000
                                        except:#回退到一元模型
                                            weight = self.word_weight_dic.get(mapping_word, 150000)+100000
                                elif history_route_lenght == 3:#四元模型
                                    try:
                                        ngram_item = u'%s%s'%(''.join(prefix_route_param_tuple[1][-3:]),mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:#退回到三元
                                        try:
                                            ngram_item = u'%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),mapping_word)
                                            weight = self.word_weight_dic[ngram_item] + 50000
                                        except:#退回到二元
                                            try:
                                                ngram_item = u'%s%s'%(prefix_route_param_tuple[1][-1],mapping_word)
                                                weight = self.word_weight_dic[ngram_item]+100000
                                            except:#回退到一元模型
                                                weight = self.word_weight_dic.get(mapping_word, 150000)+100000
                                else:
                                    try:
                                        ngram_item = ''.join(prefix_route_param_tuple[1][-4:]) + mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(prefix_route_param_tuple[1][-3:]) + mapping_word
                                            weight = self.word_weight_dic[ngram_item]+10000
                                        except:
                                            try:
                                                ngram_item = ''.join(prefix_route_param_tuple[1][-2:]) + mapping_word
                                                weight = self.word_weight_dic[ngram_item]+50000
                                            except:
                                                try:
                                                    ngram_item = ''.join(prefix_route_param_tuple[1][-1:]) + mapping_word
                                                    weight = self.word_weight_dic[ngram_item]+100000
                                                except:
                                                    ngram_item = mapping_word
                                                    weight = self.word_weight_dic.get(ngram_item, 150000)+100000
                                    # if not weight:
                                #     bigram_item = prefix_route_param_tuple[1][-1]+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                                new_weight = weight + prefix_route_param_tuple[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                                #对prefix_route_list的影响
                        new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                    #key+old_key_str是否有对应汉字匹配
                    else:
                        if new_combine_keys in self.real_prefix_set_9key:
                            new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                            new_prefix_route_weight = prefix_route_param_tuple[-1]
                            temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

                if len(temp_matched_route_list)>self.MAX_LENGHT:
                    temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                    matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]

                else:
                    matched_route_list = temp_matched_route_list[:]

                # matched_route_list = temp_matched_route_list[:]

                if len(temp_prefix_route_list)>self.MAX_LENGHT:
                    temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                    prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]
                else:
                    prefix_route_list = temp_prefix_route_list[:]

                # prefix_route_list = temp_prefix_route_list[:]
                ##按键到最后一位时，添加EOS
                key_input_index += 1
                if key_input_index == lenght_key_input:
                    output_inorder_list = sorted(matched_route_list, key=lambda x:x[-1])[:top_count]
                    sentence_weight_tuple_list = []
                    for items in output_inorder_list:
                        mark, word_list, weight = items
                        output_tuple = (''.join(word_list), weight)
                        sentence_weight_tuple_list.append(output_tuple)
                    return sentence_weight_tuple_list
        #二十六键输入规则
        elif key_input.isalpha():
            for key in key_input:
                #key是否有mapping匹配
                temp_matched_route_list = []
                temp_prefix_route_list = []
                key_mapping_word_list = self.total_mapping_dic_26key.get(key)

                #如果key有汉字匹配
                if key_mapping_word_list:
                    #对matched_route_list的影响
                    for mapping_word in key_mapping_word_list:
                        for last_matched_route_param in matched_route_list:
                            #matched_route_list三元组中汉字部分是否为空数组
                            if last_matched_route_param[1]:
                                if len(last_matched_route_param[1]) < 4:
                                    try:
                                        ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-3:]), mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = u'BOS%s%s'%(''.join(last_matched_route_param[1][-2:]),mapping_word)
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            ngram_item = u'BOS%s%s'%(last_matched_route_param[1][-1],mapping_word)
                                            weight = self.word_weight_dic.get(ngram_item, 200000)
                                else:
                                    try:
                                        ngram_item = ''.join(last_matched_route_param[1][-4:])+mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(last_matched_route_param[1][-3:])+mapping_word
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            try:
                                                ngram_item = ''.join(last_matched_route_param[1][-2:])+mapping_word
                                                weight = self.word_weight_dic[ngram_item]
                                            except:
                                                ngram_item = last_matched_route_param[1][-1]+mapping_word
                                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # bigram_item = last_matched_route_param[1][-1]+','+ mapping_word
                                # weight = self.word_weight_dic.get(bigram_item)
                                #如果查不到bigram_item对应的weight
                                # if not weight:
                                #     bigram_item = last_matched_route_param[1][-1]+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                            #key_input_str中的第一个key有匹配
                            else:
                                ngram_item = 'BOS'+ mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # if not weight:
                                #     bigram_item = 'BOS'+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                                new_weight = weight + last_matched_route_param[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))

                                ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                #key不匹配mapping_word
                else:
                    ##对prefix_route_list的影响
                    for last_matched_route_param in matched_route_list:
                        prefix_route_word_list = last_matched_route_param[1] + []
                        prefix_route_weight = last_matched_route_param[-1]
                        temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))

                # if len(temp_matched_route_list)>self.MAX_LENGHT:
                #     temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                #     temp_matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]
                # if len(temp_prefix_route_list)>self.MAX_LENGHT:
                #     temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                #     temp_prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]

                #key+old_key_str是否有对应汉字匹配
                for prefix_route_param_tuple in prefix_route_list:
                    old_key_str = prefix_route_param_tuple[0]
                    new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                    new_keys_mapping_words_list = self.total_mapping_dic_26key.get(new_combine_keys)
                    #如果combine_keys对应有汉字匹配
                    if new_keys_mapping_words_list:
                        #对matched_route_list的影响
                        for mapping_word in new_keys_mapping_words_list:
                            #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                            if not prefix_route_param_tuple[1]:
                                ngram_item = 'BOS'+mapping_word
                                weight = self.word_weight_dic.get(ngram_item, 200000)

                                # if not weight:
                                #     bigram_item = 'BOS'+','+ '*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                temp_matched_route_list.append(('#', [mapping_word], weight))
                            #（old_key_str,[],weight）第二个参数不为空
                            else:
                                # bigram_item = prefix_route_param_tuple[1][-1]+','+ mapping_word
                                if len(prefix_route_param_tuple[1]) < 4:
                                    try:
                                        ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-3:]), mapping_word)
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-2:]),
                                                                    mapping_word)
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            ngram_item = 'BOS%s%s'%(''.join(prefix_route_param_tuple[1][-1:]),
                                                                    mapping_word)
                                            weight = self.word_weight_dic.get(ngram_item, 200000)
                                else:
                                    try:
                                        ngram_item = ''.join(prefix_route_param_tuple[1][-4:]) + mapping_word
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        try:
                                            ngram_item = ''.join(prefix_route_param_tuple[1][-3:]) + mapping_word
                                            weight = self.word_weight_dic[ngram_item]
                                        except:
                                            try:
                                                ngram_item = ''.join(prefix_route_param_tuple[1][-2:]) + mapping_word
                                                weight = self.word_weight_dic[ngram_item]
                                            except:
                                                ngram_item = prefix_route_param_tuple[1][-1] + mapping_word
                                                weight = self.word_weight_dic.get(ngram_item, 200000)
                                                # if not weight:
                                    #     bigram_item = prefix_route_param_tuple[1][-1]+','+'*'
                                #     weight = self.word_weight_dic.get(bigram_item)
                                new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                                new_weight = weight + prefix_route_param_tuple[-1]
                                temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                                #对prefix_route_list的影响
                        new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                    #key+old_key_str是否有对应汉字匹配
                    else:
                        if new_combine_keys in self.real_prefix_set_26key:
                            new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                            new_prefix_route_weight = prefix_route_param_tuple[-1]
                            temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

                if len(temp_matched_route_list)>self.MAX_LENGHT:
                    temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1])
                    matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]

                else:
                    matched_route_list = temp_matched_route_list[:]

                # matched_route_list = temp_matched_route_list[:]

                if len(temp_prefix_route_list)>self.MAX_LENGHT:
                    temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1])
                    prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]
                else:
                    prefix_route_list = temp_prefix_route_list[:]

                # prefix_route_list = temp_prefix_route_list[:]
                ##按键到最后一位时，添加EOS
                key_input_index += 1
                if key_input_index == lenght_key_input:
                    final_bigram_weight_list = []
                    for matched_route_param in matched_route_list:
                        mapping_word_list = matched_route_param[1]
                        if mapping_word_list:
                            try:
                                ngram_item = u'%sEOS'%''.join(mapping_word_list[-4:])
                                weight = self.word_weight_dic[ngram_item]
                            except:
                                try:
                                    ngram_item = u'%sEOS'%''.join(mapping_word_list[-3:])
                                    weight = self.word_weight_dic[ngram_item]
                                except:
                                    try:
                                        ngram_item = u'%sEOS'%''.join(mapping_word_list[-2:])
                                        weight = self.word_weight_dic[ngram_item]
                                    except:
                                        ngram_item = u'%sEOS'%mapping_word_list[-1]
                                        weight = self.word_weight_dic.get(ngram_item, 200000)
                            new_matched_word_list = mapping_word_list
                            new_weight = weight + matched_route_param[-1]
                            final_bigram_weight_list.append((''.join(new_matched_word_list), new_weight))
                    return sorted(final_bigram_weight_list, key=lambda x:x[-1])[:top_count]
# ea = EngineArithmetic_No_BOS()
# key_input = '426742647444267426494333689446464'
# list_ngram = ea.handle_key_input_str(key_input, 5)
# for ngram_tuple in list_ngram:
#     print ngram_tuple[0], ngram_tuple[-1]

def caculate_another_parameter():
    ea = EngineArithmetic_No_BOS()
    start_time = time.time()
    src_data_path = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun'
    varify_sample_filename = os.path.join(src_data_path, 'forum_high_freq_sentence_sougou_checkout.txt')
    des_path = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun'
    checkout_sample_filename_backward = os.path.join(des_path,'forum_high_freq_sentence_checkout.txt')
    with codecs.open(varify_sample_filename, encoding='utf-8') as f, \
        codecs.open(checkout_sample_filename_backward, mode='wb', encoding='utf-8') as wf:
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
# caculate_another_parameter()
def get_sentence_accuracy_top_n():
    '''样本文件中句子的精确度AS'''
    des_path = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun'
    checkout_filename= os.path.join(des_path, 'forum_high_freq_sentence_checkout.txt')
    top_n_sentence_list = []
    correct_sentence = ''
    matched_sentence_count = 0
    total_count = 0
    top_count = 1
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
