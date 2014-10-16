#coding:utf8
import os
import re
import math
import codecs

PATH = os.path.dirname(os.path.abspath(__file__))

class Cut_Sentence(object):
    '''  '''
    def __init__(self):
        self.combined_set = self._individual_group_set()
    def _individual_group_set(self):
        new_word_list_filename = os.path.join(PATH, 'data', 'single_word_weight_5329.txt')
        with codecs.open(new_word_list_filename, encoding='utf-8') as f:
            line_list = f.readlines()
            assert len(line_list[0].split('\t')) == 2
            combined_set = set([item.split('\t')[0] for item in line_list])
            self.word_weight = dict([(item.split('\t')[0], item.split('\t')[1].strip()) for item in line_list])
        return combined_set

    def cut_forward(self, complexWords):
        '''正向切割'''
        point_position = len(complexWords) + 1
        new_postion = 0
        temp_splited_sentence_list = []
        while point_position-new_postion >= 1:
            point_position -= 1
            # print new_postion, point_position
            point_complex_words = complexWords[new_postion:point_position]
            # print point_complex_words
            if point_complex_words in self.combined_set:
                # print point_complex_words
                temp_splited_sentence_list.append(point_complex_words)
                new_postion = point_position
                point_position = len(complexWords) + 1
            if new_postion != len(complexWords) and point_position == new_postion:
                new_postion += 1
                point_position = len(complexWords) + 1
        return temp_splited_sentence_list

    def cut_backwords(self, complexWords):
        '''cut backward '''
        point_posttion = len(complexWords)
        new_position = -1
        splited_setence_list = []
        while point_posttion - new_position >= 1:
            new_position += 1
            # print new_position, point_posttion
            point_complex_words = complexWords[new_position:point_posttion]
            if point_complex_words in self.combined_set:
                # print point_complex_words
                splited_setence_list.append(point_complex_words)
                new_position,point_posttion = -1,new_position
            if new_position == point_posttion and point_posttion != 0:
                new_position = -1
                point_posttion -= 1
        splited_setence_list.reverse()
        return splited_setence_list

    def cut(self, word):
        '''长度如果不相等，取长度较小的一个，若相等则取逆向切割结果'''
        cut_forward_list = self.cut_forward(word)
        cut_backward_list = self.cut_backwords(word)
        if len(cut_forward_list) != len(cut_backward_list):
            return min(cut_backward_list, cut_forward_list, key=lambda x:len(x))
        else:
            return cut_backward_list

    def cut_with_weight(self, word):
        '''词频不等取高频，相等比较长度，长度不等去较小者，若相等则取逆向切割结果'''
        cut_forward_list = self.cut_forward(word)
        cut_backward_list = self.cut_backwords(word)
        weight_of_forward = sum([int(self.word_weight.get(item)) for item in cut_forward_list])
        weight_of_backward = sum([int(self.word_weight[item]) for item in cut_backward_list])
        # print weight_of_forward, '====='.join(cut_forward_list)
        # print weight_of_backward, '====='.join(cut_backward_list)
        if weight_of_forward != weight_of_backward:
            return cut_forward_list if weight_of_forward < weight_of_backward else cut_backward_list
        else:
            if len(cut_forward_list) != len(cut_backward_list):
                return min(cut_forward_list, cut_backward_list, key=lambda x:len(x))
            else:
                return  cut_backward_list

    def caculate_percentage_of_backward_forward(self, word):
        '''取正向切割或反向切割时各自所占的比例'''
        cut_forward_list = self.cut_forward(word)
        cut_backward_list = self.cut_backwords(word)
        weight_of_forward = sum([int(self.word_weight.get(item)) for item in cut_forward_list])
        weight_of_backward = sum([int(self.word_weight[item]) for item in cut_backward_list])
        if weight_of_forward != weight_of_backward:
            return 1 if weight_of_forward < weight_of_backward else 2
        else:
            lenght_forward = len(cut_forward_list)
            lenght_backward = len(cut_backward_list)
            if lenght_forward != lenght_backward:
                return 1 if len(cut_forward_list) < weight_of_backward else 2
            else:
                return False

    def compare_backward_forward(self, word):
        '''比较歧义句子在原始语料中所占的比例'''
        cut_forward_list = self.cut_forward(word)
        cut_backward_list = self.cut_backwords(word)
        backward_str = '-'.join(cut_forward_list)
        forward_str = '-'.join(cut_backward_list)
        if forward_str == backward_str:
            return True
        else:
            return False

if __name__=="__main__":
    ws = Cut_Sentence()
    def percentage_of_forward_backward_when_ambiguous():
        '''1、统计出歧义句子所占比例
        2、统计这些歧义句子中，取正向和反向的比例'''
        cuted_sentence_filename = os.path.join(PATH, '0709modify', 'cuted_sentence.txt')
        total_count = 0
        not_equal_count = 0
        forward_count = 0
        backward_count = 0
        f = codecs.open(cuted_sentence_filename, encoding='utf-8')
        while 1:
            line = f.readline()
            if not line:
                break
            check_equal_value = ws.caculate_percentage_of_backward_forward(line.strip())
            total_count += 1#每做一次切割，total_count 自增1
            if check_equal_value:#句子歧义
                not_equal_count += 1 #每次句子歧义，not_equal_count 自增1
                if check_equal_value == 1:
                    forward_count += 1 # 若果返回值为1，则说明取值为正向切割结果，forward_count自增1
                elif check_equal_value == 2:
                    backward_count += 1 #若返回值为2，则说名取值为反向切割结果，backward_count自增1
        print 'ambugiout_percentage is %s'%(not_equal_count/float(total_count))
        print 'forward_percentage is %s'%(forward_count/float(not_equal_count))
        print 'backward_percentage is %s'%(backward_count/float(not_equal_count))
    # percentage_of_forward_backward_when_ambiguous()
    def test_cut_with_weight():
        word = u'大英帝国的'
        print '*'.join(ws.cut_with_weight(word))
    test_cut_with_weight()
    def check_percentage_when_forward_not_equal_backward():
        '''切割原始原料，输入正向切割与反向切割不相等所占的比例'''
        total_num = 0
        not_equal_num = 0
        linguistic_data_filename = r'E:\SVN\language_model\cuted_linguistic_data.txt'
        f = codecs.open(linguistic_data_filename, encoding='utf-8')
        while 1:
            line = f.readline()
            if not line:
                break
            check_equal_value = ws.compare_backward_forward(line.strip())
            total_num += 1
            if not check_equal_value:
                not_equal_num += 1
        print not_equal_num/float(total_num)