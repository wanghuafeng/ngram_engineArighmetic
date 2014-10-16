__author__ = 'wanghuafeng'
#coding:utf-8
import os
import re
import time
import math
import codecs
PATH = os.path.dirname(os.path.abspath(__file__))
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
        with codecs.open(src_filename, encoding='utf-8') as f, \
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
                    # precision_percentage_str = str(math.log(freq_percentage, 2))
                    # com_str = '\t'.join((word_str, precision_percentage_str))
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
class AdditivePerplexity:
    def __init__(self):
        self.word_weight_dic = {}
    def _load_word_weight(self):
        word_weight_filename = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity\combine_bigram_freq_percentage.txt'
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                percentate = float(splited_line[-1])
                self.word_weight_dic[word] = percentate
    def get_percentage(self, (firstword,secondword)):
        '''生成ngram的频率'''
        ngram_item = firstword + ',' + secondword
        # print ngram_item
        item_percentage = self.word_weight_dic.get(ngram_item)
        if item_percentage:
            return item_percentage
        else:
            return self.word_weight_dic.get(firstword+','+'*')
    def test_line_percentage(self):
        self._load_word_weight()
        ngram_item = (u'堵', u'堵')
        print self.get_percentage(ngram_item)
    def return_percentage_of_each_line(self):
        '''返回每一行测试数据的总概率'''
        self._load_word_weight()
        varify_sample_filename = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity\only_cuted_sentence_varify_sample.txt'
        total_line_percentage_list = []
        with codecs.open(varify_sample_filename, encoding='utf-8') as f:
            for line in f.readlines():
                percentage = 1
                words_list = line.split()
                words_list_lenght = len(words_list)
                # print words_list_lenght
                ngram_item = ('BOS', words_list[0])
                percentage *= self.get_percentage(ngram_item)
                for word_index in range(words_list_lenght):
                    if word_index < words_list_lenght - 1:
                        ngram_item = (words_list[word_index], words_list[word_index+1])
                        percentage *= self.get_percentage(ngram_item)
                ngram_item = (words_list[-1], 'EOS')
                percentage *= self.get_percentage(ngram_item)
                com_str = '\t'.join((line.strip(), str(percentage)))+'\n'
                total_line_percentage_list.append(com_str)
        return total_line_percentage_list
    def write_line_percentage(self):
        '''将每行测试数据的概率写入到本地'''
        total_line_percentage_list = self.return_percentage_of_each_line()
        percentage_path = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity'
        filename = os.path.join(percentage_path, 'line_percentage.txt')
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(total_line_percentage_list)
    def caculate_perplexity(self):
        '''计算交叉熵、困惑度'''
        percentage_path = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity'
        filename = os.path.join(percentage_path, 'line_percentage.txt')
        total_percentage = 1
        splited_word_count = 0
        line_count = 0
        with codecs.open(filename, encoding='utf-8') as f:
            line_list = f.readlines()
            for line in line_list:
                line_count += 1
                splited_line = line.split('\t')
                words = splited_line[0]
                line_words_list = words.split()
                splited_word_count += len(line_words_list)
                item_percentage = float(splited_line[-1])
                try:
                    assert  item_percentage != 0
                except:
                    print
                    break
                total_percentage += math.log(item_percentage, 2)
        print total_percentage, splited_word_count
        cross_entropy = (-1.0/splited_word_count) * total_percentage
        print cross_entropy
        perplexity = 2**cross_entropy
        print perplexity
# vld = VarifyLinguisticData()
# vld.caculate_perplexity()
class KNPerplexity:
    def __init__(self):
        self.bigram_item_total_count = 869788684.0#所有二元模型元素的频度之和
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
        real_prefix_filename = os.path.join(PATH, '0709modify', 'data', 'prefix_if_mapping_role_num.txt')
        with codecs.open(real_prefix_filename, encoding='utf-8') as f:
            self.real_prefix_set = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(PATH, '0709modify', 'data', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_kn_smooth_param(self):
        '''加载kn_smooth参数'''
        kn_smooth_filename = os.path.join(PATH, '0709modify', 'data', 'kn_smooth_param.txt')
        assert os.path.isfile(kn_smooth_filename)
        with codecs.open(kn_smooth_filename, encoding='utf-8') as f:
            self.kn_smooth_param_dic = dict([(item.split('\t')[0], float(item.split('\t')[1])) for item in f.readlines()])
    def _load_second_word_count(self):
        '''二元模型中second_word的total_count与所有二元组元素之和的比例'''
        second_word_filename = os.path.join(PATH, '0709modify', 'data', 'second_word_count.txt')
        assert os.path.isfile(second_word_filename)
        with codecs.open(second_word_filename, encoding='utf-8') as f:
            self.second_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])/self.bigram_item_total_count) for item in f.readlines()])
    def _load_first_word_freq_count(self):
        '''二元模型中first_word的total_count'''
        first_word_filename = os.path.join(PATH, '0709modify', 'data', 'first_word_freq_count.txt')
        assert os.path.isfile(first_word_filename)
        with codecs.open(first_word_filename, encoding='utf-8') as f:
            self.first_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])) for item in f.readlines()])
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与词频成字典'''
        D1 = 0.450975770341
        D2 = 1.07751243308
        D3 = 1.55683887675
        word_weight_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                bigram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                freq = freq_int - (D1 if freq_int == 1 else D2 if freq_int == 2 else D3)
                self.word_weight_dic[bigram_item] = freq
                # words_weight_list = [(item.split('\t')[0], int(item.split('\t')[1])) for item in f.readlines()]
                # self.word_weight_dic = dict(words_weight_list)
    def kn_smooth_percentage(self, (firstword, secondword)):
        ngram_item = firstword + ',' + secondword
        ngram_count = self.word_weight_dic.get(ngram_item, 0)
        percentage = (ngram_count + self.kn_smooth_param_dic.get(firstword)*self.second_word_count_dic.get(
            secondword))/float(self.first_word_count_dic.get(firstword))
        return percentage
    def return_percentage_of_each_line(self):
        '''返回每一行测试数据的总概率'''
        varify_sample_filename = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity\only_cuted_sentence_varify_sample.txt'
        total_line_percentage_list = []
        with codecs.open(varify_sample_filename, encoding='utf-8') as f:
            for line in f.readlines():
                percentage = 1
                words_list = line.split()
                words_list_lenght = len(words_list)
                ngram_item = ('BOS', words_list[0])
                percentage *= self.kn_smooth_percentage(ngram_item)
                # print ngram_item
                for word_index in range(words_list_lenght):
                    if word_index < words_list_lenght - 1:
                        ngram_item = (words_list[word_index], words_list[word_index+1])
                        percentage *= self.kn_smooth_percentage(ngram_item)
                        # print ngram_item
                ngram_item = (words_list[-1], 'EOS')
                percentage *= self.kn_smooth_percentage(ngram_item)
                # print ngram_item
                com_str = '\t'.join((line.strip(), str(percentage)))+'\n'
                total_line_percentage_list.append(com_str)
        return total_line_percentage_list
    def write_percentage_into_file(self):
        total_line_percentage_list = self.return_percentage_of_each_line()
        filename_path = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity\KNPerplexity'
        filename = os.path.join(filename_path, 'line_percentage.txt')
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(total_line_percentage_list)
# knp = KNPerplexity()
# knp.write_percentage_into_file()
def caculate_kn_smooth_perplexity():
    '''计算交叉熵、困惑度'''
    percentage_path = r'E:\SVN\linguistic_model\9_keys\0709modify\perplexity\KNPerplexity'
    filename = os.path.join(percentage_path, 'line_percentage.txt')
    total_percentage = 1
    splited_word_count = 0
    line_count = 0
    with codecs.open(filename, encoding='utf-8') as f:
        line_list = f.readlines()
        for line in line_list:
            line_count += 1
            splited_line = line.split('\t')
            words = splited_line[0]
            line_words_list = words.split()
            splited_word_count += len(line_words_list)
            item_percentage = float(splited_line[-1])
            try:
                assert  item_percentage != 0
            except:
                print
                break
            total_percentage += math.log(item_percentage, 2)
    print total_percentage, splited_word_count
    cross_entropy = (-1.0/splited_word_count) * total_percentage
    print cross_entropy#10.6755658553
    perplexity = 2**cross_entropy
    print perplexity#
# caculate_kn_smooth_perplexity()