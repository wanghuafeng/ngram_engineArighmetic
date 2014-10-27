#coding:utf-8
import os
import re
import sys
import codecs
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

class Word2Pinyin(object):

    def __init__(self, vocab_file=None):
        if not vocab_file:
            vocab_file = os.path.join(PATH, 'data', 'Cizu_and_singleword_komoxo95K.txt')
        self.vocab_file = vocab_file
        self.word_pinyinlist_dic = {}#key:word, value:list of all multi pinyin
        self.word_high_freq_pinyin_dic = {}#key:word, value:the high freq pinyin
        self._load_base_word_list()

    def to_unicode(self, sentence):
        if isinstance(sentence, str):
            try:
                sentence = sentence.decode('utf-8')
            except Exception,e:
                try:
                    sentence = sentence.decode('gbk')
                except Exception:
                    raise ValueError('unknown coding...')
        return sentence

    def _load_base_word_list(self):
        pattern = re.compile(r'\d')
        with codecs.open(self.vocab_file, encoding='utf-8') as f:
            for line in [item.strip() for item in f.readlines()]:
                splited_line = line.split('\t')
                words = splited_line[0]
                pinyin = pattern.sub('', splited_line[1])
                self.word_pinyinlist_dic.setdefault(words, []).append(pinyin)

    def word2pinyin(self, word):
        """
        Convert a word to a pinyin list
        @param:
            word - a Chinese word
        @return a list of pinyin list
        """
        total_pinyin_list = []
        word = self.to_unicode(word)
        pinyin_list = self.word_pinyinlist_dic.get(word)
        if not pinyin_list:
            raise ValueError('Chinese word you input do not in base_word_list...')
        for pinyin_str in pinyin_list:
            total_pinyin_list.append(pinyin_str.split())
        return total_pinyin_list

    def get_pinyin(self, word):
        '''
        Get high freq pinyin
        @param:
            word - a Chinese word
        @return a matched pinyin
        '''
        word = self.to_unicode(word)
        return self.word_high_freq_pinyin_dic.get(word)[0]


if __name__ == '__main__':

    w2p = Word2Pinyin(vocab_file=None)
    print w2p.word2pinyin(u'谁是')
    # print w2p.get_pinyin(u'谁是')

