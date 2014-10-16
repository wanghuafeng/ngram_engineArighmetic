#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'renchangshun'

import math
import os
import codecs

PATH = os.path.dirname(os.path.abspath(__file__))

MULTI_PINYIN_FILE_NAME = os.path.join(PATH,  'MultiPinyinHanziPyCode.txt')

#计算困惑度
#input: p_arr 测试语料句子概率 [p(s1),p(s2)...p(si)] wT 验证语料分词个数
#output:Perplexity
class PinyinCode(object):
    def __init__(self):
        self.multi_pinyin_code_dict = {}
        self.load_multi_pinyin_data()
    def calculate_perplexity(self,p_arr, wT):
        if p_arr is None:return
        multi_p = p_arr[0]

        for p in p_arr[1:]:
            if p is not 0 :
                multi_p *= p
        l = (math.log(multi_p, 2))/wT
        return math.pow(2, -l)


    #获得多音字编码
    def get_multi_pinyin_code(self, word, pinyin):
        if self.multi_pinyin_code_dict.keys() is 0:return
        if not isinstance(word, unicode):
            word = word.decode('utf-8')
        if not isinstance(pinyin, unicode):
            pinyin = pinyin.decode('utf-8')

        return self.multi_pinyin_code_dict[word + pinyin]

    #载入多音编码文件
    def load_multi_pinyin_data(self):
        with codecs.open(MULTI_PINYIN_FILE_NAME, encoding='utf-16') as cf:
            line_list = cf.readlines()
            for line in line_list:
                line = line.split('\t')
                key = line[0]+line[1]
                self.multi_pinyin_code_dict[key] = line[2].rstrip()

if __name__=='__main__':
    pc = PinyinCode()
    print pc.get_multi_pinyin_code('乘', 'sheng')