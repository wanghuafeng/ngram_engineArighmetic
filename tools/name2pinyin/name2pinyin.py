#coding:utf-8
import re
import itertools
from word2pinyin import Word2Pinyin
from slicer_base import *

class Name2Pinyin:
    def __init__(self):
        self.family_name_filename = os.path.join(PATH, 'data', 'family_name_with_pinyin.txt')
        self.total_words_pinyin_filename = os.path.join(PATH, 'data', 'Cizu_and_singleword_komoxo95K.txt')
        self.slicer_family_name = SlicerBase({'vocab_file':self.family_name_filename})
        self.slicer_name = SlicerBase({'vocab_file':self.total_words_pinyin_filename})
        self.w2p_family_name = Word2Pinyin(vocab_file= self.family_name_filename)
        self.w2p_name = Word2Pinyin(vocab_file=self.total_words_pinyin_filename)

    def _get_family_name_pinyin(self, full_name):
        '''
        @param
            full_name
        @return
            pinyin list
        '''
        family_name = self.slicer_family_name.slice(full_name)[0]
        pinyin_list = self.w2p_family_name.word2pinyin(family_name)
        return pinyin_list[0]


    def _fullname_without_pinyin(self, full_name):
        '''
        @param:
            full_name
        @return:
            list of splited full_name without family_name
        '''
        without_family_name_list = self.slicer_family_name.slice(full_name)
        return without_family_name_list[1:]

    def _partial_name_to_pinyin(self, full_name):
        """
        Convert a sentence to a pinyin list
        @param:
            sentence - a Chinese sentence
        @return a list of pinyin list
        """
        total_pinyin_list = []
        words_list = self._fullname_without_pinyin(full_name)
        for words in words_list:
            pinyin_list = self.w2p_name.word2pinyin(words)
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

    def name2pinyin(self, full_name):
        '''
        @param
            full_name
        @return
            list of pinyin
        '''
        pinyin = self._get_family_name_pinyin(full_name)
        partial_pinyin_list = self._partial_name_to_pinyin(full_name)
        full_name_pinyin_list = [' '.join(pinyin+item) for item in partial_pinyin_list]
        return full_name_pinyin_list

if __name__ == '__main__':
    sp = Name2Pinyin()
    full_name = '北唐单类'
    # print sp._get_family_name_pinyin(word)
    full_name_pinyin_list = sp.name2pinyin(full_name)
    print full_name_pinyin_list
