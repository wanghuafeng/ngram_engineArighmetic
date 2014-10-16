#coding:utf-8
import re
import itertools
from word2pinyin import Word2Pinyin
from slice.slicer_base import *

class Sentence2Pinyin:
    def __init__(self, options = None):
        if not options:
            options = {}
        if not options.has_key('slicerModule'):
            options['slicerModule'] = 'slice.basic_slicer'
        self.slicer = SlicerBase.fromName(options['slicerModule'])
        if not options.has_key('vocab_file'):
            options['vocab_file'] = None
        self.w2p = Word2Pinyin(options['vocab_file'])

    def sentence2pinyin(self, sentence):
        """
        Convert a sentence to a pinyin list
        @param:
            sentence - a Chinese sentence
        @return a list of pinyin list
        """
        total_pinyin_list = []
        words_list = self.slicer.slice(sentence)
        # print ' '.join(words_list)
        for words in words_list:
            pinyin_list = self.w2p.word2pinyin(words)
            if len(pinyin_list) <= 1:
                for splited_pinyin in pinyin_list:
                    total_pinyin_list.append([' '.join(splited_pinyin)])
            else:
                multi_pinyin_list = []
                for splited_pinyin in pinyin_list:
                    multi_pinyin_list.append(' '.join(splited_pinyin))
                total_pinyin_list.append(multi_pinyin_list)
        # print total_pinyin_list
        pattern = re.compile(r"[\(\)]")
        pinyin_path_list = ['']
        output_pinyin_list = []
        for pinyin_list in total_pinyin_list:
            pinyin_path_list = itertools.product(pinyin_path_list, pinyin_list)
        for pinyin_path in pinyin_path_list:
            cuted_pinyin_path = ' '.join(str(pinyin_path).split(',')[1:])
            output_pinyin_list.append([pattern.sub('', cuted_pinyin_path)])
        return output_pinyin_list

if __name__ == '__main__':
    options_dic = {'slicerModule':'slice.basic_slicer'}
    sp = Sentence2Pinyin(options_dic)
    sentence = '直接写类名调用藏谁是'
    pinyin_list = sp.sentence2pinyin(sentence)
    print pinyin_list
