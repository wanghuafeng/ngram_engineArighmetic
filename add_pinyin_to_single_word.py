__author__ = 'wanghuafeng'
#coding:utf8
import os
import time
import codecs

PATH = os.path.dirname(os.path.abspath(__file__))
class AddPinyin:
    def __init__(self):
        self.single_word_dic = {}
        self._load_word_pinyin()
    def _load_word_pinyin(self):
        hzout_notone_filename = os.path.join(PATH, 'HZout_NoTone.txt')
        with codecs.open(hzout_notone_filename, encoding='utf16') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                pinyin = splited_line[1]
                freq_int = int(splited_line[-1])
                try:
                    if self.single_word_dic[word][-1] < freq_int:
                        self.single_word_dic[word] = [pinyin, freq_int]
                except:
                    self.single_word_dic[word] = [pinyin, freq_int]
    def get_pinyin(self, single_word):
        try:
            assert isinstance(single_word, unicode)
        except AssertionError:
            single_word = single_word.decode('utf-8')

        # print self.single_word_dic[single_word][0]
        return self.single_word_dic[single_word][0]
if  __name__ == '__main__':
    addpinyin = AddPinyin()
    addpinyin.get_pinyin('单')
