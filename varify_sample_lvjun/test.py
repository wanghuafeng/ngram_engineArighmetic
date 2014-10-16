#coding:utf-8

from varify_sample_lvjun import VarifyNgramData, GenMappingWordLengh

def test_VarifyNgramData():
	vnd = VarifyNgramData('E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words')
	print vnd.get_pinyin_list('谁知道')
	print vnd.get_input_role('yes')

	prefix, mapping_word_list = vnd.get_code_sentence('快快乐乐的')
	print prefix, mapping_word_list

def test_GenMappingWordLengh():
	gw = GenMappingWordLengh()
	print gw.get_input_role('hello')
if __name__ == '__main__':
	test_GenMappingWordLengh()
	