#coding:utf-8
import re
import os
import  codecs

def divide_odd_even_line():
    path = os.path.dirname(__file__)
    odd_line_list = []
    even_line_list = []
    filename = os.path.join(path, 'forum_high_freq_sentence_sougou_checkout.txt')
    with codecs.open(filename, encoding='utf-8') as f:
        new_line_list = sorted(f.readlines(), key=lambda x:len(x.split('\t')[-1]))
        count = 0
        for line in new_line_list:
            count += 1
            if count%2 == 0:
                even_line_list.append(line)
            else:
                odd_line_list.append(line)
    even_filename = os.path.join(path, 'even_line.txt')
    odd_filename = os.path.join(path, 'odd_line.txt')
    codecs.open(even_filename, mode='wb', encoding='utf-8').writelines(even_line_list)
    codecs.open(odd_filename, mode='wb', encoding='utf-8').writelines(odd_line_list)


def test_pinyin_add_module():
    from  pinyin_add_mudule.add_words_spell import WordsSearch
    ws = WordsSearch()
    word = u'是谁'
    print ws.get_splited_pinyin(word)

a = 'ni3 shi4 shei2'
splited_list =  re.split(r'\d', a)
print [''.join(splited_list)]