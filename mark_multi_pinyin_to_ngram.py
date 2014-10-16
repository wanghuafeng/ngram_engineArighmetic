__author__ = 'wanghuafeng'
#coding:utf-8
import os
import time
import codecs

def get_multi_pinyin():
    '''从基础词表中筛选出多音字部分，保存到本地'''
    total_word_dic = {}
    filename = r'E:\SVN\chocolate_ime\doc\HZout_NoTone.txt'
    with codecs.open(filename, encoding='utf16') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            word = splited_line[0]
            pinyin = splited_line[1]
            if not total_word_dic.get(word):
                total_word_dic[word] = [pinyin]
            else:
                total_word_dic[word].append(pinyin)
            # print total_word_dic
            # time.sleep(1)
    com_str_list = []
    for word, pinyin_list in total_word_dic.items():
        if len(pinyin_list) > 1:
            com_str = '\t'.join((word, ','.join(pinyin_list)))+'\n'
            com_str_list.append(com_str)
    file_to_write_filename = r'E:\SVN\linguistic_model\N_gram\bigram\bak\multi_pinyin_in_basefile.txt'
    codecs.open(file_to_write_filename, mode='wb', encoding='utf-8').writelines(com_str_list)

def _load_mulit_pinyin_words():
    '''加载多音字元素，返回set类型'''
    mulit_pinyin_filename = r'E:\SVN\linguistic_model\N_gram\bigram\bak\multi_pinyin_in_basefile.txt'
    with codecs.open(mulit_pinyin_filename, encoding='utf-8') as f:
        multi_pinyin_set = set([item.split('\t')[0] for item in f.readlines()])
    return multi_pinyin_set

def gen_mulit_pinyin_ngram():
    '''筛选出语言模型中包含多音字的元素'''
    multi_ngram_line_set = set()
    muliti_pinyin_set = _load_mulit_pinyin_words()
    filename = r'E:\SVN\linguistic_model\N_gram\bigram\combine_ngram_weight.txt'
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            ngram_item = splited_line[0]
            for single_word in ngram_item:
                if single_word in muliti_pinyin_set:
                    multi_ngram_line_set.add(line)
    multi_ngram_line_filename = r'E:\SVN\linguistic_model\N_gram\bigram\mulit_pinyin_ngram.txt'
    codecs.open(multi_ngram_line_filename, mode='wb', encoding='utf-8').writelines(multi_ngram_line_set)


class SouGouCloudWord(object):
    def __init__(self, module_path='E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'):
        import sys
        # module_path = 'E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'
        sys.path.append(module_path)
        from  add_words_spell_m import WordsSearch
        self.ws = WordsSearch()

    def to_unicode(self, sentence):
        '''输入:字符编码、或Unicode编码
           输出:Unicode编码'''
        if isinstance(sentence, str):
            try:
                sentence = sentence.decode('utf-8')
            except Exception,e:
                sentence = sentence.decode('gbk')
        return sentence

    def get_input_role(self, pinyin):
        '''输入:拼音
           输出:按键规则（数字串）'''
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        role_num = ''.join([coding_map[letter] for letter in pinyin if letter.isalpha()])
        return role_num

    def get_pinyin(self, sentence):
        '''输入:unicode格式句子
           输出:输出pinyin(拼音字符串，中间用空格隔开)'''
        sentence = self.to_unicode(sentence)
        pinyin_str = ' '.join(self.ws.get_splited_pinyin(sentence)[0]).replace('*', '')
        return pinyin_str

    def mark_multi_pinyin(self):
        com_str_list = []
        mulit_pinyin_item_filename = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun\forum_high_freq_sentence.txt'
        with codecs.open(mulit_pinyin_item_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split()
                ngram_item = splited_line[0]
                pinyin_str = ' '.join(self.ws.get_splited_pinyin(ngram_item)[0]).replace('*', '')
                # print ngram_item, pinyin_str
                # time.sleep(1)
                no_blank_pinyin_str = pinyin_str.replace(' ', '')
                role_num = self.get_input_role(no_blank_pinyin_str)
                com_str = '\t'.join((ngram_item, role_num)) + '\n'
                com_str_list.append(com_str)
        filename_to_write = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun\forum_high_freq_sentence_role_num.txt'
        codecs.open(filename_to_write, mode='wb', encoding='utf-8').writelines(com_str_list)
    # mark_multi_pinyin()

    def sougou_cloud_word(self):
        import sogou_cloud_words
        src_data_path = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun'
        varify_sample_filename = os.path.join(src_data_path, 'forum_high_freq_sentence_role_num.txt')
        des_path = r'E:\SVN\linguistic_model\N_gram\varify_sample_lvjun'
        checkout_sample_filename_backward = os.path.join(des_path, 'forum_high_freq_sentence_sougou_checkout.txt')
        with codecs.open(varify_sample_filename, encoding='utf-8') as f, \
            codecs.open(checkout_sample_filename_backward, mode='wb', encoding='utf-8') as wf:
            count = 0
            for line in f.readlines():
                mapping_sentence_role_num_list = []
                count += 1
                print count
                splited_line = line.split()
                sentence = splited_line[0]
                key_str = splited_line[-1].strip().encode('utf-8')
                matched_sentence = sogou_cloud_words.get_cloud_words(key_str)[0]
                if matched_sentence == sentence:
                    mapping_sentence_role_num_list.append('%s\t%s\n'%(sentence, key_str))
                wf.writelines(mapping_sentence_role_num_list)
    # sougou_cloud_word()
sg = SouGouCloudWord(module_path='E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words')
sg.get_pinyin('数字串')

def mulit_pinyin_with_start_mark():
    pinyin_filename = r'E:\SVN\linguistic_model\N_gram\bigram\bak\multi_pinyin_ngram_add_pinyin.txt'
    start_filename = r'E:\SVN\linguistic_model\N_gram\bigram\bak\multi_pinyin_ngram_add_pinyin_with_start.txt'
    start_line_list = []
    with codecs.open(pinyin_filename, encoding='utf-8') as f:
        for line in f.readlines():
            if '*' in line:
                start_line_list.append(line)
    codecs.open(start_filename, mode='wb', encoding='utf-8').writelines(start_line_list)
# mulit_pinyin_with_start_mark()

def mk_single_word_inorder():
    '''对单字按词频进行排序'''
    filename = r'E:\SVN\linguistic_model\N_gram\data\single_word_5329.txt'
    with codecs.open(filename, encoding='utf-8') as f:
        inorder_list = sorted(f.readlines(), key=lambda x:int(x.split('\t')[-1]), reverse=True)
    inorder_filename = r'E:\SVN\linguistic_model\N_gram\data\single_word_5329_inorder.txt'
    codecs.open(inorder_filename, mode='wb', encoding='utf-8').writelines(inorder_list)
# mk_single_word_inorder()
