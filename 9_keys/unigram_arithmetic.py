__author__ = 'wanghuafeng'
#coding:utf-8
import codecs
import os
import re
import time
import random

PATH = os.path.dirname(os.path.abspath(__file__))

def cuted_varify_sample():
    '''利用weight值对varify_sample文件进行切割'''
    from cut_sentence import Cut_Sentence
    ws = Cut_Sentence()
    word_input_role_dic = {}

    def _load_input_role():
        '''加载汉61633基础词库词为key与输入规则为value的字典'''
        input_role_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000_pinyin_role.txt')
        with codecs.open(input_role_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                input_role = splited_line[-1].strip()
                word_input_role_dic[word] = input_role
    # _load_input_role()

    varify_sample_filename = os.path.join(PATH, '0709modify', 'cuted_varify_sample.txt')
    output_filename = os.path.join(PATH, '0709modify', 'unigram', 'only_cuted_sentence_varify_sample.txt')
    with codecs.open(varify_sample_filename, encoding='utf-8')as f,\
    codecs.open(output_filename, mode='wb', encoding='utf-8') as wf:
        for line in f.readlines():
            word_list = ws.cut_with_weight(line.strip())
            cuted_sentence = ' '.join(word_list)
            # input_role_list = [word_input_role_dic[item] for item in word_list]
            # input_role_str = ' '.join(input_role_list)
            # com_str = '\t'.join((line.strip(),input_role_str))

            wf.write(cuted_sentence+'\n')
            # print ' '.join(ws.cut_with_weight(word))
# cuted_varify_sample()

class Unibram_Arithmetic:
    def __init__(self):
        ''''''
        self.total_mapping_dic = {}
        self.word_weight_dic = {}
        self._load_mapping_rolenum_wordlist()
        self._load_word_weigh()
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(PATH, '0709modify', 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_word_weigh(self):
        '''加载一元组模型，以一元组元素为key，与权重构成字典'''
        word_weight_filename = os.path.join(PATH, '0709modify', 'wordlist_61633_weight.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            words_weight_list = [(item.split('\t')[0], int(item.split('\t')[1].strip())) for item in f.readlines()]
            self.word_weight_dic = dict(words_weight_list)
    def handle_key_input_str(self, key_str):
        key_str = key_str.strip()
        # key_str = '54674 884543'
        min_weight_word_list = []
        for key in key_str.split():
            word_weight_tuple_list = min([(item, self.word_weight_dic[item]) for item in self.total_mapping_dic[key]], key=lambda x:x[-1])
            # print word_weight_tuple_list
            min_weight_word_list.append(word_weight_tuple_list[0])
        # print ''.join(min_weight_word_list)
        return min_weight_word_list

    def unigram_as_output(self):
        src_filename = os.path.join(PATH, '0709modify', 'unigram', 'unigram_varify_sample_with_cuted_input_role.txt')
        new_gen_sentence_filename = os.path.join(PATH, '0709modify', 'unigram', 'unigram_new_gen_sentence.txt')
        with codecs.open(src_filename, encoding='utf-8') as f,\
        codecs.open(new_gen_sentence_filename, mode='wb', encoding='utf-8') as wf:
            for line in f.readlines():
                key_str = line.split('\t')[-1]
                new_gen_sentence = ''.join(self.handle_key_input_str(key_str))
                wf.write(new_gen_sentence+'\n')

    def check_word_accuracy(self):
        '''计算词的准确度(0.660572977396)'''
        output_filename = os.path.join(PATH, '0709modify', 'unigram', 'only_cuted_sentence_varify_sample.txt')
        src_filename = os.path.join(PATH, '0709modify', 'unigram', 'unigram_varify_sample_with_cuted_input_role.txt')
        total_min_weight_word_list = []
        src_total_word_list = []
        matched_word_count = 0
        with codecs.open(src_filename, encoding='utf-8') as src_f,\
        codecs.open(output_filename, encoding='utf-8') as cuted_f:
            for line in src_f.readlines():
                key_str = line.split('\t')[-1]
                min_weight_word_list = self.handle_key_input_str(key_str)
                total_min_weight_word_list.extend(min_weight_word_list)
            for line in cuted_f.readlines():
                line_words_list = line.strip().split()
                src_total_word_list.extend(line_words_list)
        min_weight_list_length = len(total_min_weight_word_list)
        src_word_list_lenght = len(src_total_word_list)
        assert min_weight_list_length == src_word_list_lenght
        for i in range(min_weight_list_length):
            if total_min_weight_word_list[i] == src_total_word_list[i]:
                matched_word_count += 1
        print matched_word_count/float(5787244)#0.660572977396

# ua = Unibram_Arithmetic()
# ua.check_word_accuracy()

def check_unigram_accuracy():
    '''计算句子准确率'''
    src_filename = os.path.join(PATH, '0709modify', 'unigram', 'unigram_varify_sample_with_cuted_input_role.txt')
    new_gen_sentence_filename = os.path.join(PATH, '0709modify', 'unigram', 'unigram_new_gen_sentence.txt')
    matched_sencetence_count = 0
    with codecs.open(src_filename, encoding='utf-8') as src_f,\
        codecs.open(new_gen_sentence_filename, encoding='utf-8') as new_f:
        src_sentence_list = [item.split('\t')[0] for item in src_f.readlines()]
        new_sentence_list = [item.strip() for item in new_f.readlines()]
        src_lenght = len(src_sentence_list)
        new_lenght = len(new_sentence_list)
        assert src_lenght == new_lenght#1356075
        for i in range(src_lenght):
            if src_sentence_list[i] == new_sentence_list[i]:
                matched_sencetence_count += 1
    print matched_sencetence_count/float(src_lenght)#0.299136847151
# check_unigram_accuracy()
def gen_aw_accuarcy():
    '''计算词的长度'''
    src_filename = os.path.join(PATH, '0709modify', 'unigram', 'unigram_varify_sample_with_cuted_input_role.txt')
    total_count = 0
    with codecs.open(src_filename, encoding='utf-8') as f:
        for line in f.readlines():
            line_words_list_count = line.split('\t')[-1].strip().split()
            total_count += len(line_words_list_count)
    print total_count#5787244
# gen_aw_accuarcy()
def get_sentence_accuracy_top_one():
    '''样本文件中词的准确度'''
    from cut_sentence import Cut_Sentence
    matched_words_count = 0
    total_words_count = 312525.0
    cs = Cut_Sentence()
    correct_sentence_set = set()
    top_one_sentence_list = []
    correct_sentence_list = []
    checkout_filename = os.path.join(PATH, '0709modify', 'aaaaaaaaaaaa_weight.txt')
    with codecs.open(checkout_filename, encoding='utf-8') as f:
        count = 0
        for line in f.readlines():
            if line.startswith('*'):
                # correct_sentence_list.extend(cs.cut_with_weight(line.strip()[1:]))
                # correct_sentence_list = cs.cut_with_weight(line.strip()[1:])
                correct_sentence_set = cs.cut_with_weight(line.strip()[1:])
                count = 0
            else:
                count += 1
                if count == 1:
                    sentence = line.split('\t')[0]
                    # top_one_sentence_list.extend(cs.cut_with_weight(sentence))
                    top_one_sentence_list = cs.cut_with_weight(sentence)
                    for words in top_one_sentence_list:
                        if words in correct_sentence_set:
                            matched_words_count += 1
    # print len(top_one_sentence_list), len(correct_sentence_list)
    print matched_words_count/total_words_count

                    # re_combine_sentence = ' '.join(cs.cut_with_weight(sentence))
                    # print re_combine_sentence
                    # time.sleep(1)
# get_sentence_accuracy_top_one()
