#coding:utf-8
import os
import sys
import codecs

try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

class SlicerBase(object):
    def __init__(self, options=None):
        if not options:
            options = {}
        self.options = options
        if not self.options.has_key('vocab_file') or not self.options['vocab_file']:
            self.options['vocab_file'] = os.path.join(PATH, 'data', 'Cizu_and_singleword_komoxo95K.txt')
        self.total_base_word_set = self._load_base_wordlist()

    def _load_base_wordlist(self):
        with codecs.open(self.options['vocab_file'], encoding='utf-8') as f:
            total_base_word_set = set([item.split('\t')[0] for item in f.readlines()])
        return total_base_word_set

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

    def cut_forward(self, complexWords):
        '''cut forword'''
        point_position = len(complexWords) + 1
        new_postion = 0
        temp_splited_sentence_list = []
        while point_position-new_postion >= 1:
            point_position -= 1
            point_complex_words = complexWords[new_postion:point_position]
            if point_complex_words in self.total_base_word_set:
                temp_splited_sentence_list.append(point_complex_words)
                new_postion = point_position
                point_position = len(complexWords) + 1
            if new_postion != len(complexWords) and point_position == new_postion + 1:
                temp_splited_sentence_list.append(point_complex_words)
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
            if point_complex_words in self.total_base_word_set:
                # print point_complex_words
                splited_setence_list.append(point_complex_words)
                new_position,point_posttion = -1,new_position
            if new_position + 1 == point_posttion and point_posttion != 0:
                splited_setence_list.append(point_complex_words)
                new_position = -1
                point_posttion -= 1
        splited_setence_list.reverse()
        return splited_setence_list

    def slice(self, sentence):
        '''
        if lengh not equal:
            chose the shorter one,
        else:
            chose the back_forward sliced one
        '''
        sentence = self.to_unicode(sentence)
        cut_forward_list = self.cut_forward(sentence)
        cut_backward_list = self.cut_backwords(sentence)
        if len(cut_forward_list) != len(cut_backward_list):
            return min(cut_backward_list, cut_forward_list, key=lambda x:len(x))
        else:
            return cut_backward_list
if __name__ == "__main__":
    def test_cut_forward():
        s = SlicerBase({'vocab_file':r'F:\klm\ngram\varify_sample_lvjun\pinyin_add_mudule\doc\Cizu_komoxo95K.txt'})
        print ' '.join(s.cut_forward(u'直接写类名调用'))
        # test_cut_forward()
    def test_cut_backward():
        s = SlicerBase({'vocab_file':r'F:\klm\ngram\varify_sample_lvjun\pinyin_add_mudule\doc\Cizu_komoxo95K.txt'})
        print ' '.join(s.cut_backwords(u'直接写类名调用'))
    # test_cut_backward()
    def test_basic_slicer_module():
        slicer = SlicerBase()
        sliced_words_list = slicer.slice('北唐写类')
        print ' '.join(sliced_words_list)
    test_basic_slicer_module()
    # test_both_slice_module()