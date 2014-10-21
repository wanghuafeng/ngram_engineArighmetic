#coding:utf-8
from sentence2pinyin import *

class Sentence2Digits:
    def __init__(self, options = None):
        if not options:
            options = {}
        if not options.has_key('slicerModule'):
            options['slicerModule'] = 'slice.basic_slicer'
        if not options.has_key('vocab_file'):
            options['vocab_file'] = None
        self.s2p = Sentence2Pinyin(options)

    def get_input_role_num(self, pinyin, unicode_mark=False):
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        if unicode_mark:
            pinyin = pinyin.replace(' ', '')[1:]
            assert not pinyin.isalpha(), 'pinyin_input is not alpha...'
        else:
            pinyin = pinyin.replace(' ', '')
            assert pinyin.isalpha(), 'pinyin_input is not alpha...'
        role_num = ''.join([coding_map[letter] for letter in pinyin if letter.isalpha()])
        return role_num

    def sentence2digits(self, sentence, high_freq=False):
        """
        Convert a sentence to a pinyin list
        @param:
            sentence - a Chinese sentence
        @return a list of pinyin list
        """
        # s2p = Sentence2Pinyin(self.options)
        if not high_freq:
            pinyinLists = self.s2p.sentence2pinyin(sentence)
            role_num_list = [self.get_input_role_num(item[0], unicode_mark=True) for item in pinyinLists if item]
            return role_num_list
        else:
            pinyin_str = self.s2p.sentence_to_matched_pinyin(sentence)
            role_num = self.get_input_role_num(pinyin_str, unicode_mark=False)
            return [role_num]
    def sentence_to_matched_pinyin(self, sentence):
        pinyin_str = self.s2p.sentence_to_matched_pinyin(sentence)
        role_num = self.get_input_role_num(pinyin_str, unicode_mark=False)
        return [role_num]
if __name__ == '__main__':
    options_dic = {'slicerModule':'slice.basic_slicer', 'vocab_file':None}
    sd = Sentence2Digits(options_dic)
    print sd.sentence2digits(u'谁', high_freq=True)
    # matched_digit = sd.sentence_to_matched_pinyin('1单')
    # print matched_digit