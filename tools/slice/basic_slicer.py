#coding:utf-8
from slicer_base import *

class Slicer(SlicerBase):
    # def slice(self, sentence):
    #     pass
    def __init__(self, vocab_file = None):

        option_dic = {"withoutWeight": False, "vocab_file": vocab_file}
        super(Slicer, self).__init__(option_dic)

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

    def slice(self, sentence):
        '''
        if lengh not equal:
            chose the shorter one,
        else:
            chose the back_forward sliced one
        '''
        sentence = self.to_unicode(sentence)
        cut_forward_list = super(Slicer, self).cut_forward(sentence)
        cut_backward_list = super(Slicer, self).cut_backwords(sentence)
        if len(cut_forward_list) != len(cut_backward_list):
            return min(cut_backward_list, cut_forward_list, key=lambda x:len(x))
        else:
            return cut_backward_list

if __name__ == '__main__':
    cut_without_weight = Slicer()
    sentence = u'直接写类名调用'
    return_list =  cut_without_weight.slice(sentence)
    print ' '.join(return_list)