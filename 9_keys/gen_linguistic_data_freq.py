#coding:utf8
import os
import re
import sys
import math
import time
import codecs
from cut_sentence import Cut_Sentence
# module_path = 'E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'
# sys.path.append(module_path)
# from  add_words_spell_m import WordsSearch
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

class WordFreq:
    def __init__(self):
        self.src_filename = os.path.join(PATH, '0709modify', 'cuted_sentence.txt')
    def gen_word_freq_from_linguistic_data(self):
        '''词表+句子语料'''
        cs = Cut_Sentence()
        whole_word_freq_dic = {}
        whole_word_freq_set = set()
        with codecs.open(self.src_filename, encoding='utf-8') as f:
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
    def mk_word_freq_inorder_by_freq(self):
        '''将word_freq文件按词频高低进行排列'''
        file_to_convert_filename = os.path.join(PATH, '0709modify', 'word_freq_from_new_wordlist_inorder.txt')
        new_file_to_write_filename = os.path.join(PATH, '0709modify', 'word_freq_in_order_272773.txt')
        with codecs.open(file_to_convert_filename, encoding='utf-8') as f:
            inorder_list = sorted(f.readlines(), key=lambda x: int(x.split('\t')[1]), reverse=True)
        with codecs.open(new_file_to_write_filename, mode='wb', encoding='utf-8') as wf:
            wf.writelines(inorder_list)
    def gen_60000_word_freq_sample(self):
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
    def combine_5233_and_top60000(self):
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
    def caculate_percentage(self):
        '''计算combine_5233_top60000文件的频率'''
        combine_filename = os.path.join(PATH, 'linguistic_data', 'data', 'combine_top60000_and_5041.txt')
        new_file_to_write_filename = os.path.join(PATH, 'linguistic_data', 'data', 'base_wrods_weight.txt')
        with codecs.open(combine_filename, encoding='utf-8') as f,\
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
    def check_exception_in_new_wordlist(self):
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
    def remove_repeat_word(self):
        new_word_list_filename = os.path.join(PATH, 'a.txt')
        with codecs.open(new_word_list_filename, encoding='utf-8') as f:
            temp_list = [item for item in f.readlines()]
            codecs.open(new_word_list_filename, mode='wb', encoding='utf-8').writelines(set(temp_list))
    def make_word_freq_inorder(self):
        '''按照词频进行排序'''
        top_60000_word_freq_filename = os.path.join(PATH, 'top_60000_word_freq.txt')
        with codecs.open(top_60000_word_freq_filename, encoding='utf-8') as f:
            inorder_word_freq_list = sorted(f.readlines(), key=lambda x: int(x.split('\t')[1]), reverse=True)
            codecs.open('a.txt', mode='wb', encoding='utf-8').writelines(inorder_word_freq_list)
    # make_word_freq_inorder()
class SecondCut:
    '''用新词表进行第二次切割'''
    def gen_cuted_linguistic_data(self):
        '''在非词表出进行切割'''
        base_wordlist_filename = os.path.join(PATH, 'linguistic_data', 'data', 'base_wrods_weight.txt')
        cut_filename = os.path.join(PATH, 'data', 'varify_sample.txt')
        format_str = ''.join([item.split('\t')[0] for item in codecs.open(base_wordlist_filename, encoding='utf-8').readlines()])
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
    def cut_linguistic_sample_into_small_part(self):
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
    def cut_lines_into_words(self):
        '''将行（句子）切割成词，其间以空格隔开'''
        from cut_sentence import Cut_Sentence
        cs = Cut_Sentence()
        for file_count in range(26, 29):
            print file_count
            src_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s.txt'%file_count)
            with codecs.open(src_filename, encoding='utf-8') as f:
                cuted_lines_list = [' '.join(cs.cut_with_weight(line))+'\n' for line in f.readlines()]
            codecs.open(src_filename, mode='wb', encoding='utf-8').writelines(cuted_lines_list)
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
    def gen_bigram_trigram_model_data(self):
        '''统计二元、三元组数据'''
        bigram_param_freq_dic = {}
        bigram_param_set = set()
        trigram_param_freq_dic = {}
        trigram_param_set = set()
        for file_count in range(1, 29):
            src_data_filename = os.path.join(PATH, '0709modify',  'cuted_linguistic_stample', '%s.txt'%file_count)
            with codecs.open(src_data_filename, encoding='utf-8') as f:
                for line in f.readlines():
                    splited_list = line.strip().split()
                    if not splited_list:#跳过空白行
                        continue
                    splited_list_length = len(splited_list)
                    # print splited_list_length

                    # #二元组数据
                    # line_bigram_list = []
                    # line_bigram_list.append(('BOS', splited_list[0]))
                    # for i in range(splited_list_length):
                    #     if i < splited_list_length - 1:
                    #         line_bigram_list.append((splited_list[i], splited_list[i+1]))
                    # line_bigram_list.append((splited_list[-1], 'EOS'))
                    # for bigram_tuple in line_bigram_list:
                    #     if bigram_tuple in bigram_param_set:
                    #         bigram_param_freq_dic[bigram_tuple] += 1
                    #     else:
                    #         bigram_param_freq_dic[bigram_tuple] = 1
                    #         bigram_param_set.add(bigram_tuple)

                    ##三元组数据
                    line_trigram_list = []
                    if splited_list_length == 1:
                        line_trigram_list.append(('BOS', splited_list[0]))
                        line_trigram_list.append((splited_list[0], 'EOS'))
                    elif splited_list_length == 2:
                        line_trigram_list.append(('BOS', splited_list[0]))
                        line_trigram_list.append(('BOS', splited_list[0], splited_list[1]))
                        line_trigram_list.append((splited_list[0], splited_list[1], 'EOS'))
                        line_trigram_list.append((splited_list[-1], 'EOS'))
                    else:
                        line_trigram_list.append(('BOS', splited_list[0]))
                        line_trigram_list.append(('BOS', splited_list[0], splited_list[1]))
                        for k in range(splited_list_length):
                            if k < splited_list_length - 2:
                                line_trigram_list.append((splited_list[k], splited_list[k+1], splited_list[k+2]))
                            elif k == splited_list_length - 2:
                                line_trigram_list.append((splited_list[k], splited_list[k+1], 'EOS'))
                            else:
                                line_trigram_list.append((splited_list[-1], 'EOS'))
                    for word in line_trigram_list:
                        print ' '.join(word)
                    print '*'*40
                    time.sleep(1)
                    for trigram_tuple in line_trigram_list:
                        try:
                            trigram_param_freq_dic[trigram_tuple] += 1
                        except:
                            trigram_param_freq_dic[trigram_tuple] = 1
            ## 写入二元组
            # bigram_tuple_freq_list = ['\t'.join((','.join(bigram_tuple), str(freq)))+'\n' for (bigram_tuple, freq) in bigram_param_freq_dic.items()]
            # bigram_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', '%s_bigram.txt'%file_count)
            # codecs.open(bigram_filename, mode='wb', encoding='utf-8').writelines(bigram_tuple_freq_list)
            # bigram_param_set.clear()
            # bigram_param_freq_dic.clear()
            #写入三元组
            trigram_tuple_freq_list = ['\t'.join((','.join(trigram_tuple), str(freq)))+'\n' for (trigram_tuple, freq) in trigram_param_freq_dic.items()]
            bigram_filename = os.path.join(PATH, 'cuted_linguistic_stample', '%s_trigram.txt'%file_count)
            codecs.open(bigram_filename, mode='wb', encoding='utf-8').writelines(trigram_tuple_freq_list)
            del trigram_param_set
            del trigram_param_freq_dic
# sc = SecondCut()
# sc.gen_bigram_trigram_model_data()
class GenNgram:
    '''生成n-gram模型'''
    def __init__(self):
        self.src_data_file_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item'
        self.TOTAL_FILE_COUNT = 28
        self.uninorder_file_pattern = '%s_five_gram.txt'#排序前的N元模型
        self.inorder_file_pattern = '%s_five_gram_inorder.txt'#排序后的N元模型
        self.uncombine_inorder_file_pattern = 'five_gram_inorder.txt'#合并前的N元模型
        self.combine_filename = 'five_gram_combine_word_freq.txt'#合并后的N元模型

    def gen_n_igram_model_data(self, n=4):
        '''统计三元、四元、五元组数据模型'''
        file_name_pattern = 'four' if n==4 else 'five' if n==5 else 'three'
        for file_count in range(1, 29):
            n_gram_param_freq_dic = {}
            # five_gram_param_freq_dic = {}
            print file_count
            src_data_filename = os.path.join(PATH, '0709modify',  'cuted_linguistic_stample', '%s.txt'%file_count)
            with codecs.open(src_data_filename, encoding='utf-8') as f:
                for line in [item.strip().replace(' ', '') for item in f.readlines()]:
                    if not line:
                        continue
                    splited_list_length = len(line)
                    ##四元组数据
                    if n == 4:
                        line_fourgram_list = []
                        if splited_list_length == 1:
                            line_fourgram_list.append(('BOS', line[0]))
                            line_fourgram_list.append((line[0], 'EOS'))
                        elif splited_list_length == 2:
                            line_fourgram_list.append(('BOS', line[0]))
                            line_fourgram_list.append(('BOS', line[0], line[1]))
                            line_fourgram_list.append((line[0], line[1], 'EOS'))
                        elif splited_list_length == 3:
                            line_fourgram_list.append(('BOS', line[0]))
                            line_fourgram_list.append(('BOS', line[0], line[1]))
                            line_fourgram_list.append(('BOS', line[0], line[1], line[2]))
                            line_fourgram_list.append((line[0], line[1], line[2], 'EOS'))
                            line_fourgram_list.append((line[1], line[2], 'EOS'))
                            line_fourgram_list.append((line[2], 'EOS'))
                        else:
                            line_fourgram_list.append(('BOS', line[0]))
                            line_fourgram_list.append(('BOS',line[0], line[1]))
                            line_fourgram_list.append(('BOS', line[0], line[1], line[2]))
                            for k in range(splited_list_length):
                                if k < splited_list_length - 3:
                                    line_fourgram_list.append((line[k], line[k+1], line[k+2], line[k+3]))
                                elif k == splited_list_length - 3:
                                    line_fourgram_list.append((line[-3], line[-2], line[-1], 'EOS'))
                                elif k == splited_list_length - 2:
                                    line_fourgram_list.append((line[-2], line[-1], 'EOS'))
                                elif k == splited_list_length - 1:
                                    line_fourgram_list.append((line[-1], 'EOS'))

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
    def combine_bigram_freq(self, uncombine_file_pattern, combine_freq_filename='combine_word_freq.txt'):
        '''将n个排序后文件的N元模型进行词频叠加'''
        combine_bigram_freq_filename = os.path.join(self.src_data_file_path, combine_freq_filename)
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
    def cut_off_param(self,un_cut_filename='combine_word_freq.txt',cutOff=2):
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

    def put_ngram_item_into_different_file(self):
        '''把ngram语言模型，根据n的值分到不同的文件中'''
        cut_off_filename = os.path.join(self.src_data_file_path, 'five_gram_combine_word_freq_cutOff=1.txt')
        lenght_1_ngram_item_list = []
        lenght_2_ngram_item_list = []
        lenght_3_ngram_item_list = []
        lenght_4_ngram_item_list = []
        lenght_5_ngram_item_list = []
        with codecs.open(cut_off_filename, encoding='utf-8') as f:
            # while 1:
            #     line = f.readline()
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                ngram_item_words_lenght = len(ngram_item.split(','))

                if ngram_item_words_lenght == 1:
                    lenght_1_ngram_item_list.append(line)
                elif ngram_item_words_lenght == 2:
                    lenght_2_ngram_item_list.append(line)
                elif ngram_item_words_lenght == 3:
                    lenght_3_ngram_item_list.append(line)
                elif lenght_4_ngram_item_list == 4:
                    lenght_4_ngram_item_list.append(line)
                else:
                    lenght_5_ngram_item_list.append(line)

                print ngram_item, ngram_item_words_lenght
                time.sleep(.5)
# gn = GenNgram()
# gn.put_ngram_item_into_different_file()
# gn.mk_n_gram_inorder(gn.uninorder_file_pattern, gn.inorder_file_pattern)
# gn.cut_off_param(gn.combine_filename, cutOff=100)
# gn.combine_bigram_freq(gn.uncombine_inorder_file_pattern, gn.combine_filename)
class SmoothArithmeticDataPrepare:
    '''修正的KN平滑算法'''
    def __init__(self):
        self.total_freq_int = 0#所有二元模型频度之和
        self.src_data_file_path = r'E:\SVN\linguistic_model\9_keys\0709modify\bigram'
        self.arithmetic_param_path = r'E:\SVN\linguistic_model\9_keys\0709modify\bigram'
        self.combine_word_freq_cutOff_filename = 'combine_bigram_freq_no_bos.txt'
    def remove_bos_and_eos(self):
        src_data_file_path = r'E:\SVN\linguistic_model\9_keys\0709modify\bigram\data'
        filename = os.path.join(src_data_file_path, self.combine_word_freq_cutOff_filename)
        new_line_list = []
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                if splited_line[0].startswith('BOS') or splited_line[0].endswith('EOS'):
                    continue
                else:
                    new_line_list.append(line)
            no_bos_eos_filename = os.path.join(self.src_data_file_path, 'combine_bigram_freq_no_bos.txt')
            codecs.open(no_bos_eos_filename, mode='wb', encoding='utf-8').writelines(new_line_list)
    def cutoff_combine_word_freq(self, cutoff):
        filename = os.path.join(self.src_data_file_path, self.combine_word_freq_cutOff_filename)
        com_str_list = []
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                bigram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                if bigram_item.startswith('BOS') or bigram_item.endswith('EOS'):
                    continue
                if freq_int > cutoff:
                    freq_int -= cutoff
                    com_str_list.append('%s\t%s\n'%(bigram_item, freq_int))
        cuted_filename = os.path.join(self.src_data_file_path, 'combine_bigram_freq_delete_2_inorder_no_BOS.txt')
        codecs.open(cuted_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def gen_freq_count_of_1_and_2(self):
        '''统计出词频数为1，或者为2的二元模型的数目'''
        total_count = 0#36292642
        n1 = 0#17050532
        n2 = 0#5462655
        n3 = 0
        n4 = 0
        bigram_freq_filename = os.path.join(self.src_data_file_path, self.combine_word_freq_cutOff_filename)
        with codecs.open(bigram_freq_filename, encoding='utf-8') as f:
            for line in f.readlines():
                total_count += 1
                splited_line = line.strip().split('\t')
                if splited_line[-1] == '1':
                    n1 += 1
                elif splited_line[-1] == '2':
                    n2 += 1
                elif splited_line[-1] == '3':
                    n3 += 1
                elif splited_line[-1] == '4':
                    n4 += 1
        Y = float(n1)/(n1+2*n2)
        print 'Y=%s'%Y#Y=n1/(n1+2*n2)
        print 'D1=%s'%(1-2*Y*(float(n2)/n1))#D1=1-2Y(n2/n1)
        print 'D2=%s'%(2-3*Y*(float(n3)/n2))#D2=2-3Y(n3/n2)
        print 'D3=%s'%(3-4*Y*(float(n4)/n3))#D3=3-4Y(n4/n3)
        print 'Please add these D param to smooth'#D参数写入到平滑参数中去
    def gen_first_word_total_freq_dic(self):
        '''以第一个元素相同的二元组中元素为key，该元素所有频度之和为value生成字典'''
        inorder_bigaram_filename = os.path.join(self.src_data_file_path, self.combine_word_freq_cutOff_filename)
        total_frist_word_freq_dic = {}
        with codecs.open(inorder_bigaram_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                splited_first_word_of_unigram = splited_line[0].split(',')
                first_word = splited_first_word_of_unigram[0]
                # print first_word
                # time.sleep(1)
                freq_int = int(splited_line[-1])
                self.total_freq_int += freq_int
                try:
                    total_frist_word_freq_dic[first_word] += freq_int
                except KeyError:
                    total_frist_word_freq_dic[first_word] = freq_int
            # return total_frist_word_freq_dic
        print 'total freq is %s'%self.total_freq_int#1626997356
        print 'total_freq param will be used in EnginArithmetic'
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in total_frist_word_freq_dic.items()]
        first_word_freq_filename = os.path.join(self.arithmetic_param_path, 'first_word_freq_count.txt')
        codecs.open(first_word_freq_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def get_total_freq_int(self):
        '''计算所有二元模型频度之和'''
        inorder_bigaram_filename = os.path.join(self.src_data_file_path, self.combine_word_freq_cutOff_filename)
        total_freq_int = sum([int(item.split('\t')[-1]) for item in codecs.open(inorder_bigaram_filename, encoding='utf-8').readlines()])
        print total_freq_int#1944946999
    def KN_smooth(self):
        '''对词频为1,2,3+的first_word分别做不同处理'''
        D1=0.630999593298
        D2=1.09109751165
        D3=1.46364610581
        KN_smooth_dic = {}
        filename = os.path.join(self.src_data_file_path, self.combine_word_freq_cutOff_filename)
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                # first_word_list = line.split(',')[:-1]
                first_word = line.split(',')[0]
                # print first_word
                # time.sleep(1)
                freq_int = int(line.split('\t')[-1])
                if freq_int == 1:
                    smooth_param = D1
                elif freq_int == 2:
                    smooth_param = D2
                else:
                    smooth_param = D3
                    # smooth_param = D1 if freq_int == 1 else D2 if freq_int == 2 else D3
                try:
                    KN_smooth_dic[first_word] += freq_int*smooth_param
                except KeyError:
                    KN_smooth_dic[first_word] = freq_int*smooth_param
                    # print KN_smooth_dic
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in KN_smooth_dic.items()]
        kn_smooth_param_filename = os.path.join(self.arithmetic_param_path,  'kn_smooth_param.txt')
        codecs.open(kn_smooth_param_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def second_word_count(self):
        '''获取所要查询二元模型的second_word的total_count'''
        filename = os.path.join(self.src_data_file_path, self.combine_word_freq_cutOff_filename)
        second_freq_dic = {}
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                # second_word_list = splited_line[0].split(',')[1:]
                # second_word = ','.join(second_word_list)
                second_word = splited_line[0].split(',')[-1]
                # print second_word
                # time.sleep(1)
                freq_int = int(splited_line[-1])
                try:
                    second_freq_dic[second_word] += freq_int
                except KeyError:
                    second_freq_dic[second_word] = freq_int
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in second_freq_dic.items()]
        second_word_count_filename = os.path.join(self.arithmetic_param_path, 'second_word_count.txt')
        codecs.open(second_word_count_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def second_word_percentage(self):
        '''ngram的second_word除以对应语言模型的total_count'''
        second_word_count_filename = os.path.join(self.arithmetic_param_path, 'second_word_count.txt')
        total_word_percentage_dic = {}
        with codecs.open(second_word_count_filename, encoding='utf-8') as f:
            trigram_word_freq_dic = {}
            fourgram_word_freq_dic = {}
            line_list = f.readlines()
            bigram_count = sum([int(item.split('\t')[-1]) for item in line_list if len(item.split('\t')[0].split(','))==1])
            # bigram_count = 484876471
            for line in line_list:
                splited_line = line.split('\t')
                words_list = splited_line[0].split(',')
                freq_int = int(splited_line[-1])
                word_list_lenght = len(words_list)
                if word_list_lenght == 2:
                    try:
                        trigram_word_freq_dic[words_list[0]] += freq_int
                    except:
                        trigram_word_freq_dic[words_list[0]] = freq_int
                elif word_list_lenght == 3:
                    try:
                        fourgram_word_freq_dic[','.join((words_list[0], words_list[1]))] += freq_int
                    except:
                        fourgram_word_freq_dic[','.join((words_list[0], words_list[1]))] = freq_int
            for line in line_list:
                splited_line = line.split('\t')
                words_list = splited_line[0].split(',')
                freq_float = float(splited_line[-1])
                word_list_lenght = len(words_list)
                if word_list_lenght == 1:
                    total_word_percentage_dic[words_list[0]] = freq_float/bigram_count
                elif word_list_lenght == 2:
                    total_word_percentage_dic[','.join((words_list[0], words_list[1]))] = freq_float/trigram_word_freq_dic[words_list[0]]
                else:
                    total_word_percentage_dic[','.join((words_list[0], words_list[1], words_list[2]))] = freq_float/fourgram_word_freq_dic[','.join((words_list[0], words_list[1]))]
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in total_word_percentage_dic.items()]
        second_word_percentage_filename = os.path.join(self.arithmetic_param_path, 'second_word_percentage.txt')
        codecs.open(second_word_percentage_filename, mode='wb', encoding='utf-8').writelines(com_str_list)

# sa = SmoothArithmeticDataPrepare()
# sa.remove_bos_and_eos()
# sa.gen_freq_count_of_1_and_2()
# sa.gen_first_word_total_freq_dic()
# sa.KN_smooth()
# sa.second_word_count()
# sa.second_word_percentage()
class InputRules:
    '''初始化时，传入待转换文件的路径，调用convert_pinyin_to_rules方法时，传入其文件名，文件可以是\t隔开的第一列是待转换词'''
    def __init__(self, src_path):
        self.src_file_path = src_path
        # self.src_file_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\arithmetic_param'
    def convert_pinyin_to_rules(self, src_filename):
        '''把基础词库中的拼音转换为输入规则（数字序列）'''
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        from add_pinyin_to_single_word import AddPinyin
        addpinyin = AddPinyin()
        base_filename = os.path.join(self.src_file_path, src_filename)
        filename_without_suffix = src_filename.split('.')[0]
        base_file_with_pinyin_role = os.path.join(self.src_file_path, '%s_pinyin_role.txt'%filename_without_suffix)
        with codecs.open(base_filename, encoding='utf-8') as f, \
            codecs.open(base_file_with_pinyin_role, mode='wb', encoding='utf-8') as wf:
            whole_word_list = (item.split('\t')[0] for item in f.readlines())
            for word in whole_word_list:
                # pinyin_str = ' '.join(ws.get_splited_pinyin(word)[0]).replace('*', '')
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
        mapping_base_file_with_pinyin_inorder_filename = os.path.join(self.src_file_path, '%s_mapping.txt'%filename_without_suffix)
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
# roles = InputRules(r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\four_gram_arithmetic_param')
# roles.convert_pinyin_to_rules('single_word_5322.txt')
class KNEngineArithmetic:
    def __init__(self):
        self.MAX_LENGHT = 100
        self.src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\four_gram_arithmetic_param'
        self.bigram_item_total_count = 1626997356.0#所有二元模型元素的频度之和
        self.real_prefix_set = set()#真前缀列表
        self._real_prefix_rolenum()
        self.total_mapping_dic = {}#输入规则的字典
        self._load_mapping_rolenum_wordlist()
        self.kn_smooth_param_dic = {}#低阶平滑参数
        self._load_kn_smooth_param()
        self.second_word_count_dic = {}#二元模型中second_word的total_count与所有二元组元素之和的比例
        self._load_second_word_count()
        self.first_word_count_dic = {}#所有二元模型中first_wrod的total_count
        self._load_first_word_freq_count()
        self.word_weight_dic = {}#二元模型字典
        self._load_word_weigh()
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_filename = os.path.join(self.src_data_path, 'prefix_if_mapping_role_num.txt')
        with codecs.open(real_prefix_filename, encoding='utf-8') as f:
            self.real_prefix_set = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(self.src_data_path, 'single_word_5322_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_kn_smooth_param(self):
        '''加载kn_smooth参数'''
        kn_smooth_filename = os.path.join(self.src_data_path, 'kn_smooth_param.txt')
        assert os.path.isfile(kn_smooth_filename)
        with codecs.open(kn_smooth_filename, encoding='utf-8') as f:
            self.kn_smooth_param_dic = dict([(item.split('\t')[0], float(item.split('\t')[1])) for item in f.readlines()])
    def _load_second_word_count(self):
        '''二元模型中second_word的total_count与所有二元组元素之和的比例'''
        second_word_filename = os.path.join(self.src_data_path, 'second_word_percentage.txt')
        assert os.path.isfile(second_word_filename)
        with codecs.open(second_word_filename, encoding='utf-8') as f:
            self.second_word_count_dic = dict([(item.split('\t')[0], float(item.split('\t')[-1])) for item in f.readlines()])
    def _load_first_word_freq_count(self):
        '''二元模型中first_word的total_count'''
        first_word_filename = os.path.join(self.src_data_path, 'first_word_freq_count.txt')
        assert os.path.isfile(first_word_filename)
        with codecs.open(first_word_filename, encoding='utf-8') as f:
            self.first_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])) for item in f.readlines()])
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与词频成字典'''
        D1 = 0.458632547866
        D2 = 1.08465539019
        D3 = 1.50193792784
        word_weight_filename = os.path.join(os.path.dirname(self.src_data_path),'four_gram_combine_word_freq_cutOff=2.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                bigram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                freq = freq_int - (D1 if freq_int == 1 else D2 if freq_int == 2 else D3)
                self.word_weight_dic[bigram_item] = freq
                # words_weight_list = [(item.split('\t')[0], int(item.split('\t')[1])) for item in f.readlines()]
                # self.word_weight_dic = dict(words_weight_list)
    def handle_key_input_str(self, key_input, top_count=1):
        key_input = key_input.strip()
        matched_route_list = [('#',[],1)]
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
                        if last_matched_route_param[1]:#如果不为空
                            # first_valid_words = last_matched_route_param[1][-1]
                            # second_valid_words = last_matched_route_param[1][-1]+','+mapping_word

                            first_valid_words = ','.join(last_matched_route_param[1][-3:])
                            second_valid_words = ','.join(last_matched_route_param[1][-2:])+','+mapping_word

                            bigram_item = first_valid_words +','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic.get(first_valid_words, 0)*self.second_word_count_dic.get(second_valid_words, 0))/self.first_word_count_dic.get(first_valid_words, 1000000)
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight * last_matched_route_param[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                        #key_input_str中的第一个key有匹配
                        else:
                            bigram_item = 'BOS'+','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic['BOS']*self.second_word_count_dic.get(mapping_word, 0))/self.first_word_count_dic['BOS']
                            new_matched_word_list = [] + [mapping_word]
                            new_weight = weight * last_matched_route_param[-1]
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
            #     temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1], reverse=True)
            #     # print temp_matched_route_list[0]
            #     temp_matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]
            # if len(temp_prefix_route_list)>self.MAX_LENGHT:
            #     # print temp_prefix_route_list[0]
            #     temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1], reverse=True)
            #     temp_prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]

                #key+old_key_str是否有对应汉字匹配
            for prefix_route_param_tuple in prefix_route_list:
                old_key_str = prefix_route_param_tuple[0]
                new_combine_keys = old_key_str + key#新输入的key为最末位
                new_keys_mapping_words_list = self.total_mapping_dic.get(new_combine_keys)
                #如果combine_keys对应有汉字匹配
                if new_keys_mapping_words_list:
                    #对matched_route_list的影响
                    for mapping_word in new_keys_mapping_words_list:
                        #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                        if not prefix_route_param_tuple[1]:
                            bigram_item = 'BOS'+','+mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic['BOS']*self.second_word_count_dic.get(mapping_word, 0))/self.first_word_count_dic['BOS']
                            new_mapping_word_list = [] + [mapping_word]
                            temp_matched_route_list.append(('#', new_mapping_word_list, weight))
                        #（old_key_str,[second_param],weight）第二个参数不为空
                        else:
                            # first_valid_words = ','.join(last_matched_route_param[1][-1])
                            # second_valid_words = last_matched_route_param[1][-1]+','+mapping_word
                            first_valid_words = ','.join(prefix_route_param_tuple[1][-3:])
                            second_valid_words = ','.join(prefix_route_param_tuple[1][-2:])+','+mapping_word
                            # print 'first_valid_words:', first_valid_words, self.first_word_count_dic.get(first_valid_words, 0)
                            # print 'kn_smooth_param:',self.kn_smooth_param_dic.get(first_valid_words, 0)
                            # print 'second_valid_words:', second_valid_words, self.second_word_count_dic.get(second_valid_words, 0)
                            bigram_item = first_valid_words +','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic.get(first_valid_words, 0)*self.second_word_count_dic.get(second_valid_words, 0))/self.first_word_count_dic.get(first_valid_words, 1000000)
                            new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                            new_weight = weight * prefix_route_param_tuple[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                            # print ''.join(new_matched_word_list), new_weight
                        #对prefix_route_list的影响
                    new_prefix_route_list = prefix_route_param_tuple[1] + []
                    new_prefix_route_weight = prefix_route_param_tuple[-1]
                    temp_prefix_route_list.append((new_combine_keys, new_prefix_route_list, new_prefix_route_weight))
                ##对prefix_route_list的影响
                else:
                    #如果是真前缀
                    if new_combine_keys in self.real_prefix_set:
                        new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

            if len(temp_matched_route_list)>self.MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1], reverse=True)
                matched_route_list = temp_matched_route_list[:self.MAX_LENGHT]
                # self.max_weight_in_complete_path = max(matched_route_list, key=lambda x:x[-1])
            else:
                matched_route_list = temp_matched_route_list[:]
            # print matched_route_list[:]
            if len(temp_prefix_route_list)>self.MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1], reverse=True)
                prefix_route_list = temp_prefix_route_list[:self.MAX_LENGHT]
                # self.max_weight_in_incomplete_path = max(prefix_route_list, key=lambda x:x[-1])
            else:
                prefix_route_list = temp_prefix_route_list[:]
            # print temp_prefix_route_list
            ##按键到最后一位时，添加EOS
            key_input_index += 1
            if key_input_index == lenght_key_input:
                final_bigram_weight_list = []
                for matched_route_param in matched_route_list:
                    mapping_word_list = matched_route_param[1]
                    if mapping_word_list:
                        first_valid_words = ','.join(mapping_word_list[-1])
                        second_valid_words = matched_route_param[1][-1] + 'EOS'
                        bigram_item = first_valid_words+','+'EOS'
                        weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic.get(first_valid_words, 0)*self.second_word_count_dic.get(second_valid_words, 0))/self.first_word_count_dic.get(first_valid_words, 1000000)
                        new_matched_word_list = mapping_word_list
                        new_weight = weight * matched_route_param[-1]
                        final_bigram_weight_list.append((' '.join(new_matched_word_list), new_weight))
                return sorted(final_bigram_weight_list, key=lambda x:x[-1], reverse=True)[:top_count]
# ea = KNEngineArithmetic()
# key_str = '92674264244926326'
# matched_word_list = ea.handle_key_input_str(key_str, 5)
# for matched_word in matched_word_list:
#     print matched_word[0], matched_word[-1]
def caculate_another_parameter():
    ea = KNEngineArithmetic()
    start_time = time.time()
    src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify'
    varify_sample_filename = os.path.join(src_data_path, 'cuted_varify_sample_pinyin_role_no_repeat.txt')
    des_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\four_gram_arithmetic_param'
    checkout_sample_filename_backward = os.path.join(des_path, 'Kneser_Ney_smooth_checkout_limit_100_fourgram.txt')
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
def caculate_sougou():
    # ea = KNEngineArithmetic()
    import sogou_cloud_words
    start_time = time.time()
    src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify'
    varify_sample_filename = os.path.join(src_data_path, 'forum_high_freq_sentence.txt')
    des_path = r'E:\SVN\linguistic_model\9_keys\0709modify'
    checkout_sample_filename_backward = os.path.join(des_path, 'forum_high_freq_sentence_sougou_checkout.txt')
    with codecs.open(varify_sample_filename, encoding='utf-8') as f, \
        codecs.open(checkout_sample_filename_backward, mode='wb', encoding='utf-8') as wf:
        count = 0
        for line in f.readlines():
            temp_list_for_write = []
            count += 1
            print count
            splited_line = line.split()
            sentence = splited_line[0]
            key_str = splited_line[-1].strip().encode('utf-8')
            com_str = '*'+sentence+'\n'
            temp_list_for_write.append(com_str)
            top_matched_sentence_weight_list = [item+'\n' for item in sogou_cloud_words.get_cloud_words(key_str)]
            temp_list_for_write.extend(top_matched_sentence_weight_list)
            wf.writelines(temp_list_for_write)
    end_time = time.time()
    print end_time-start_time
# caculate_sougou()

def get_sentence_accuracy_top_n():
    '''样本文件中句子的精确度AS'''
    des_path = r'E:\SVN\linguistic_model\9_keys\0709modify'
    checkout_filename= os.path.join(des_path, 'sougou_checkout.txt')
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
                sentence = line.split('\t')[0].strip().replace(' ','')
                top_n_sentence_list.append(sentence)
    print total_count, matched_sentence_count
    print str(matched_sentence_count/float(total_count)*100)+'%'
# get_sentence_accuracy_top_n()
class TestNgram:
    def __init__(self):
        self.src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify\four_five_gram_item\arithmetic_param'
        self.ngram_item = u'BOS,你,们,EOS'
        self.first_word = u'BOS,你,们'
        self.second_word = u'你,们,EOS'
    def gen_ngram_item(self):
        global src_data_path
        src_data_path = os.path.dirname(self.src_data_path)
        filename = os.path.join(src_data_path, 'combine_word_freq_cutOff=2.txt')
        with codecs.open(filename, encoding='utf8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                if splited_line[0] == self.ngram_item:
                    print line.strip()
    # ngram_item()
    def gen_kn_smooth(self):
        kn_smooth_filename = os.path.join(self.src_data_path, 'kn_smooth_param.txt')
        with codecs.open(kn_smooth_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                if splited_line[0] == self.first_word:
                    print line.strip()
    # kn_smooth()
    def gen_second_word(self):
        second_filename = os.path.join(self.src_data_path, 'second_word_percentage.txt')
        with codecs.open(second_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                if splited_line[0] == self.second_word:
                    print line.strip()
    # second_word()
    def gen_frist_word(self):
        filename = os.path.join(self.src_data_path, 'first_word_freq_count.txt')
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                if splited_line[0] == self.first_word:
                    print line.strip()

