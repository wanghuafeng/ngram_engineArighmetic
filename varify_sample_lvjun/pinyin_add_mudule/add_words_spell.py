#coding:utf8
import os
import time
import re
import math
import codecs
from os.path import dirname as pd
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
#THIS_PATH = pd(pd(pd(pd(os.path.abspath(__file__)))))
# BASE_WORDS_ADD_NAME = os.path.join(THIS_PATH, "data","Add_Name.txt")#coding:gbk
BASE_WORDS_CIZU = os.path.join(THIS_PATH, "doc","Cizu_komoxo95K.txt")#coding:gbk
BASE_WORDS_HZOUT = os.path.join(THIS_PATH, "doc","HZout_NoTone.txt")#coding:utf-16
BASE_NEW_ADD_WORDS = os.path.join(THIS_PATH,"doc","low_freq_words.txt")#coding:utf-16
BASE_OMIT_CHECK_WORDS = os.path.join(THIS_PATH,"doc","omit_check_words.txt")#coding:utf8
# BASE_ENCODING_DIC = {"BASE_WORDS_ADD_NAME":"gbk","BASE_WORDS_CIZU":"gbk","BASE_WORDS_HZOUT":"utf-16"}
omit_adjust_dic = {u"行":"hang",u"都":"du",u"地":"di"}

multi_familyname_dic = {u'解': u'xie', u'查': u'zha', u'薄': u'bo',
                        u'仇': u'qiu', u'缪': u'miao', u'卜': u'bu',
                        u'宓': u'fu', u'贲': u'fei',u'单': u'shan',
                        u'臧': u'zang', u'隗': u'kui', u'盖': u'ge',
                        u'能': u'nai', u'乜': u'nie', u'曾': u'zeng'}
class WordsSearch(object):
    '''  '''
    def __init__(self):
        self.found_words_list = []
        self.omit_check_words_set = set()#omit check words in set
        self.words_pinyin_freq_dic = {}
        self.repeat_words_pinyin_dic = {}#the four column append to update.txt
        self.high_freq_single_word_dic = {}#word just with highest freq
        self.high_freq_pinyin_dic = {}#high frequence pinyin
        self.combined_set = self._individual_group_set()
        self._load_omit_check_words()
        self._get_high_freq()

    def _load_cizu(self):
        splited_word_set = set()
        fileObj = codecs.open(BASE_WORDS_CIZU,mode="rb",encoding="gbk")
        for line in fileObj.readlines():
            if line.startswith(";") or  not line.strip():
                continue
            else:
                splited_line = line.strip().split("\t")
                words = splited_line[0]
                pinyin_with_num = splited_line[1]
                freq = splited_line[-1]
                split_spell_list = re.split(r"\d",pinyin_with_num)
                pinyin_part = ''.join(split_spell_list)#spells without num
                split_tuple = (words,pinyin_part,freq)
                key_check_val_tuple = self.words_pinyin_freq_dic.get(words)#current word as the key
                if key_check_val_tuple:#if words repeat,add mark to the value of dict
                    if self.words_pinyin_freq_dic[splited_line[0]][1]  == pinyin_part:
                        self.repeat_words_pinyin_dic[words] = pinyin_part
                    else:
                        self.repeat_words_pinyin_dic[words] = key_check_val_tuple[1] + ','+\
                                                                        pinyin_part
                        self.words_pinyin_freq_dic[words] = key_check_val_tuple + tuple("*")
                else:# key_check_val is None ,means words not repeat,then just add value to dict
                    self.words_pinyin_freq_dic[words] = split_tuple
                    splited_word_set.add(words)
        fileObj.close()
        return splited_word_set

    def _load_single_word(self):
        '''load all single word'''
        fileObj= codecs.open(BASE_WORDS_HZOUT,mode="rb",encoding="utf-16")
        single_words_set = set()
        for line in fileObj.readlines():
            splited_line = line.split("\t")
            splited_tuple =  splited_line[0],splited_line[1],splited_line[2]
            key_check_val_tuple = self.words_pinyin_freq_dic.get(splited_line[0])
            if key_check_val_tuple:#word already in dict,add mark to the value of the dict
                if self.words_pinyin_freq_dic[splited_line[0]][1] == splited_line[1]:
                    self.repeat_words_pinyin_dic[splited_line[0]] = splited_line[1]
                else:
                    self.repeat_words_pinyin_dic[splited_line[0]] = self.repeat_words_pinyin_dic[splited_line[0]] + ','+splited_line[1]
                self.words_pinyin_freq_dic[splited_line[0]] = key_check_val_tuple + tuple("*")
            else:#key_check_val is None,means not repeat word,then just add to the dict
                single_words_set.add(splited_line[0])
                self.words_pinyin_freq_dic[splited_line[0]] = splited_tuple
                self.repeat_words_pinyin_dic[splited_line[0]] = splited_line[1]
            #words just with high freq
            word = splited_line[0]
            check_word_exists = self.high_freq_single_word_dic.get(word)
            if check_word_exists: #if word exists
                check_word_exists.append(splited_line)
            else:#if word not exists
                list_bak = []
                list_bak.append(splited_line)
                self.high_freq_single_word_dic[word] = list_bak
        fileObj.close()
        return single_words_set

    def _new_add_words(self):
        '''data in self.words_pinyin_freq_dic generate by _load_cizu() will effect this function,
        if words load here already in words_pinyin_freq_dic,it will regard as the repeat words and
        add mark.So first_run_flag need to add here'''
        fileObj= codecs.open(BASE_NEW_ADD_WORDS,mode="rb",encoding="utf-16")
        if not os.path.isfile(BASE_NEW_ADD_WORDS):
            raise ValueError('File %s not exist!' % BASE_WORDS_HZOUT)
        single_words_set = set()
        for line in fileObj.readlines():
            first_run_flag = False  #make sure self.words_pinyin_freq_dic will not effect by exists load word of __load_cizu
            splited_line = line.split("\t")
            pinyin_tuple = tuple(splited_line[1].split())
            splited_tuple =  splited_line[0],pinyin_tuple,splited_line[2]
            key_check_val_tuple = self.words_pinyin_freq_dic.get(splited_line[0])
            if first_run_flag and key_check_val_tuple:#key already in dict,add mark to the value of the dict
                if self.words_pinyin_freq_dic[splited_line[0]][1] == pinyin_tuple:
                    self.repeat_words_pinyin_dic[splited_line[0]] = pinyin_tuple
                else:
                    # print self.repeat_words_pinyin_dic[splited_line[0]]
                    self.repeat_words_pinyin_dic[splited_line[0]] = self.repeat_words_pinyin_dic[splited_line[0]] +\
                                                                    pinyin_tuple
                self.words_pinyin_freq_dic[splited_line[0]] = key_check_val_tuple + tuple("*")
            else:#key_check_val is None,means not repeat word,then just add to the dict
                first_run_flag = True
                single_words_set.add(splited_line[0])
                self.words_pinyin_freq_dic[splited_line[0]] = splited_tuple
                self.repeat_words_pinyin_dic[splited_line[0]] = pinyin_tuple
        fileObj.close()
        return single_words_set

    def _load_omit_check_words(self):
        ''' load omit check words into self.omit_check_words_set'''
        with codecs.open(BASE_OMIT_CHECK_WORDS,encoding="utf-8") as f:
            for line in f.readlines():
                self.omit_check_words_set.add(line.strip())

    def _get_high_freq(self):
        '''get high frequence pinyin '''
        for word in self.high_freq_single_word_dic:
            word_pinyin_freq_list_len = len(self.high_freq_single_word_dic[word])
            if word_pinyin_freq_list_len > 1:
                high_word_pinyin_freq_list = max(self.high_freq_single_word_dic[word], key=lambda x: float(x[2]))
                self.high_freq_pinyin_dic[word] = high_word_pinyin_freq_list[1]

    def _individual_group_set(self):
        individual_set = self._load_single_word()
        group_set = self._load_cizu()
        new_add_set = self._new_add_words()
        temp_set = individual_set.union(group_set)
        combined_set = temp_set.union(new_add_set)
        # combined_set = individual_set.union(group_set)
        # print len(combined_set)
        return combined_set

    def normal_case_words(self, normalwords):
        ''' words in base file'''
        temp_found_words_list = []
        if normalwords in self.combined_set:
            star_normal_word = normalwords + "*"
            star_words_set = set([normalwords,star_normal_word])
            if star_words_set.issubset(self.combined_set):#word repeat
                star_add_repeat_tuple = self.words_pinyin_freq_dic[normalwords] + tuple("*")
                temp_found_words_list.append(star_add_repeat_tuple)
            else:#not repeat
                temp_found_words_list.append(self.words_pinyin_freq_dic[normalwords])
        return temp_found_words_list

    def search_length_priority_froward(self, complexWords):
        ''' search forward ,need to recombine ,but do not have star mark'''
        point_position = len(complexWords)
        new_postion = 0
        temp_splited_sentence_list = []
        while point_position-new_postion > 1:
            point_position -= 1
            point_complex_words = complexWords[new_postion:point_position]
            if point_complex_words in self.combined_set:

                star_point_word = point_complex_words + "*"
                star_word_set = set([point_complex_words,star_point_word])
                if star_word_set.issubset(self.combined_set):
                    star_add_repeat_tuple = self.words_pinyin_freq_dic[point_complex_words] + tuple("*")
                    temp_splited_sentence_list.append(star_add_repeat_tuple)
                else:
                    temp_splited_sentence_list.append(self.words_pinyin_freq_dic[point_complex_words])
                new_postion = point_position
                point_position = len(complexWords) + 1
        return temp_splited_sentence_list

    def search_length_priority_backwords(self, complexWords):
        '''search backward '''
        point_posttion = len(complexWords)
        new_position = 0
        splited_setence_list = []
        while point_posttion - new_position > 1:
            new_position += 1
            point_complex_words = complexWords[new_position:point_posttion]
            if point_complex_words in self.combined_set:
                star_point_word = point_complex_words + "*"
                star_word_set = set([point_complex_words,star_point_word])
                if star_word_set.issubset(self.combined_set):
                    star_add_repeat_tuple = self.words_pinyin_freq_dic[point_complex_words] + tuple("*")
                    splited_setence_list.append(star_add_repeat_tuple)
                else:
                    splited_setence_list.append(self.words_pinyin_freq_dic[point_complex_words])
                new_position,point_posttion = -1,new_position
        splited_setence_list.reverse()
        return splited_setence_list

    def frequence_sum_compare(self, param):
        '''get sum of frequence when length of splited sentence do not equal '''
        assert type(param) is list
        freq_num = 0
        for word_spell_freq in param:
            if word_spell_freq[2].strip() == '0':
                word_freq = 1
            else:
                word_freq = word_spell_freq[2].strip()
            freq_num += math.log10(long(word_freq))
        return freq_num

    def chose_efficiency_back_forward(self, word):
        normal_case_words = self.normal_case_words(word)
        if normal_case_words:
            return normal_case_words
        else:
            search_forward = self.search_length_priority_froward(word)
            search_backward = self.search_length_priority_backwords(word)
            if len(search_forward) != len(search_backward):
                return min(search_backward,search_forward,key=lambda x:len(x))
            else:
                return max(search_forward,search_backward,key=self.frequence_sum_compare)

    def get_splited_words(self, words):
        '''return splited words '''
        splited_list = self.chose_efficiency_back_forward(words)
        splited_words_list = []
        for splited_word in splited_list:
            splited_words_list.append(splited_word[0])
        return tuple(splited_words_list)

    def _get_splited_pinyin_1(self, words):
        '''return splited words,word group recombine with blank
         "u"在同一片广阔的天空下""-->(u'zai tong', u'yi pian', u'guang kuo',
          u'de', '*', u'tian kong', u'xia')'''
        splited_list = self.chose_efficiency_back_forward(words)
        splited_pinyin_list = []
        for splited_pinyin_tuple in splited_list:
            if "*" in splited_pinyin_tuple:
                if isinstance(splited_pinyin_tuple[1], tuple):
                    splited_pinyin_list.append(" ".join(splited_pinyin_tuple[1]))
                    splited_pinyin_list.append("*")
                else:
                    splited_pinyin_list.append(splited_pinyin_tuple[1])
                    splited_pinyin_list.append("*")
            else:

                if isinstance(splited_pinyin_tuple[1], tuple):
                    splited_pinyin_list.append(" ".join(splited_pinyin_tuple[1]))
                else:
                    splited_pinyin_list.append(splited_pinyin_tuple[1])
        return tuple(splited_pinyin_list)
    def _get_splited_pinyin_2(self, words):
        '''return splited words,word group recombine with comma
         "zhiwu,'baoweizhan'"-->"zhi,wu,bao,wei,zhan"
         '''
        splited_list = self.chose_efficiency_back_forward(words)
        splited_pinyin_list = []
        for splited_pinyin_tuple in splited_list:
            if "*" in splited_pinyin_tuple:
                if isinstance(splited_pinyin_tuple[1], tuple):
                    splited_pinyin_list.append("*")
                    splited_pinyin_list.append(" ".join(splited_pinyin_tuple[1]))
                else:
                    splited_pinyin_list.append("*")
                    splited_pinyin_list.append(splited_pinyin_tuple[1])
            else:
                if isinstance(splited_pinyin_tuple[1], tuple):
                    splited_pinyin_list.append(" ".join(splited_pinyin_tuple[1]))
                else:
                    splited_pinyin_list.append(splited_pinyin_tuple[1])
        return tuple(splited_pinyin_list)

    def to_unicode(self, sentence):
        '''判断是否为Unicode，若否，则转换为Unicode'''
        if isinstance(sentence, str):
            try:
                sentence = sentence.decode('utf-8')
            except Exception,e:
                sentence = sentence.decode('gbk')
        return sentence

    def get_splited_pinyin(self, words, verify_flag=False):
        '''return splited words,word group recombine with comma
         splited_word_list = [{u'\u5df7': (u'hang', u'xiang')}, {u'\u8bf4': (u'yue', u'shuo')}]
         splited_list = [(u'\u8def', u'lu', u'4756911\r\n'), (u'\u7684', u'de', u'148709248\r\n',
          '*'), (u'\u987f\u6cb3', (u'dun', u'he'), u'1580000\r\n')]
          splited_list = [(u'\u66fe', u'zeng', u'1485067\r\n', '*'),()]'''
        words = self.to_unicode(words)
        splited_list = self.chose_efficiency_back_forward(words)
        if not splited_list:
            pass
        else:
            # first_word_pinyin_freq_tuple = splited_list[0]
            first_word = splited_list[0][0]
            if first_word in multi_familyname_dic:#word in multi_familyname_dic
                # if isinstance(first_word_pinyin_freq_tuple[1], unicode):#pinyin part is unicode
                #     first_word = first_word_pinyin_freq_tuple[0]
                splited_list[0] = (first_word, multi_familyname_dic[first_word])
        splited_pinyin_list = []
        # splited_word_list = []
        splited_word_pinyin_dic = {}
        for splited_pinyin_tuple in splited_list:
            #splited_pinyin_tuple = (u'\u90fd', u'du', u'3093398\r\n', '*')
            if "*" in splited_pinyin_tuple:
                if isinstance(splited_pinyin_tuple[1], tuple):# pinyin part is tuple
                    star_add_words ="*" + " ".join(splited_pinyin_tuple[1])
                    splited_pinyin_list.append(star_add_words)
                    # temp_dic = {}
                    # temp_dic[splited_pinyin_tuple[0]] = self.repeat_words_pinyin_dic[splited_pinyin_tuple[0]]
                    # splited_word_list.append(temp_dic)

                    splited_word_pinyin_dic[splited_pinyin_tuple[0]] = self.repeat_words_pinyin_dic[splited_pinyin_tuple[0]]

                else:  #pinyin part is not tuple,means word is single
                    if splited_pinyin_tuple[0] in self.omit_check_words_set:#word in omit list
                        if verify_flag:
                            omit_pinyin_adjust = omit_adjust_dic.get(splited_pinyin_tuple[0])
                            if omit_pinyin_adjust:
                                high_freq_pinyin = omit_pinyin_adjust
                            else:
                                high_freq_pinyin = self.high_freq_pinyin_dic[splited_pinyin_tuple[0]]
                        else:
                            high_freq_pinyin = self.high_freq_pinyin_dic[splited_pinyin_tuple[0]]
                        splited_pinyin_list.append(high_freq_pinyin)
                    else:
                        # print splited_pinyin_tuple[0]
                        star_add_single_word = "*" + splited_pinyin_tuple[1]
                        splited_pinyin_list.append(star_add_single_word)
                        splited_word_pinyin_dic[splited_pinyin_tuple[0]] = self.repeat_words_pinyin_dic[splited_pinyin_tuple[0]]
            else:
                if isinstance(splited_pinyin_tuple[1],tuple):
                    splited_pinyin_list.append(" ".join(splited_pinyin_tuple[1]))
                else:
                    splited_pinyin_list.append(splited_pinyin_tuple[1])
        # print splited_pinyin_list,splited_word_list
        return splited_pinyin_list,splited_word_pinyin_dic

if __name__=="__main__":

    ws = WordsSearch()

    result_pinyin = ws.get_splited_pinyin(u"先回家了是谁了藏")

    print result_pinyin

