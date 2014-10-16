#coding:utf-8
import os
import sys
import time
import codecs

try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

class VarifyNgramData(object):

    def __init__(self, add_pinyin_module_path='E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'):
        self.module_path = add_pinyin_module_path
        self._load_module()
        self.word_pinyin_code_dic = {}
        self._load_HanziCode()
        self.input_role_mapping_word_dic = {}
        self._load_input_role_mapping_word()
        self._load_word_pinyin_list()

    def _load_module(self):
        '''加入标音模块'''
        from  pinyin_add_mudule.add_words_spell import WordsSearch
        self.ws = WordsSearch()

    def _load_word_pinyin_list(self):
        '''key为文件中的word，value为文件中所有该汉字对应的拼音的数组'''
        hzout_notone_filename = os.path.join(PATH, 'data', 'HZout_NoTone.txt')
        single_word_pinyin_list_dic = {}
        with codecs.open(hzout_notone_filename, encoding='utf16') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                pinyin = splited_line[1]
                try:
                    single_word_pinyin_list_dic[word].append(pinyin)
                except KeyError:
                    single_word_pinyin_list_dic[word] = [pinyin]
        # self.mulit_word_pinyin_dic = dict([(k,v) for (k,v) in single_word_pinyin_list_dic.items() if len(v) > 1])
        self.mulit_word_pinyin_dic = dict([(k,v) for (k,v) in single_word_pinyin_list_dic.items()])

    def _load_HanziCode(self):
        '''加载科文多音字编码'''
        filename =os.path.join(PATH, 'data', 'MultiPinyinHanziPyCode.txt')
        with codecs.open(filename, encoding='utf16') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                single_word = splited_line[0]
                pinyin = splited_line[1]
                code = splited_line[-1].strip()
                word_pinyin_str = single_word + pinyin
                self.word_pinyin_code_dic[word_pinyin_str] = code

    def _load_input_role_mapping_word(self):
        filename = os.path.join(PATH, 'data', 'single_word_5329_pinyin_role_inorder_mapping_9key.txt')
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                input_role = splited_line[0]
                mapping_word_list = splited_line[-1].strip().split(',')
                self.input_role_mapping_word_dic[input_role] = mapping_word_list

    def to_unicode(self, sentence):
        '''判断是否为Unicode，若否，则转换为Unicode'''
        if isinstance(sentence, str):
            try:
                sentence = sentence.decode('utf-8')
            except Exception,e:
                sentence = sentence.decode('gbk')
        return sentence

    def get_pinyin_list(self, sentence):
        '''输入:句子
           输出:拼音数组'''
        sentence = self.to_unicode(sentence)
        pinyin_str_str = ' '.join(self.ws.get_splited_pinyin(sentence)[0])
        return pinyin_str_str.split()

    def get_input_role(self, pinyin):
        '''输入:拼音
           输出:按键规则（数字串）'''
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        role_num = ''.join([coding_map[letter] for letter in pinyin if letter.isalpha()])
        return role_num

    def get_mapping_word_list(self, role_num):
        '''输入: 按键规则（数字串）
           输出:该按键规则所对应的汉字列表'''
        mapping_word_list = self.input_role_mapping_word_dic[role_num]
        return mapping_word_list

    def get_code_sentence(self, sentence):
        '''输入:句子
           输出:prefix,word_list'''
        sentence_input = self.to_unicode(sentence)
        pinyin_list = self.get_pinyin_list(sentence_input)
        singleword_pinyin_tuple_list = zip(sentence_input, pinyin_list)
        partial_sentence = ''
        for word_pinyin_tuple in singleword_pinyin_tuple_list[:-1]:#不对最后一个字进行处理
            try:
                partial_sentence += eval('u"%s"'%self.word_pinyin_code_dic['%s%s'%word_pinyin_tuple])
            except:
                partial_sentence += word_pinyin_tuple[0]
            # partial_sentence += self.word_pinyin_code_dic.get('%s%s'%word_pinyin_tuple, word_pinyin_tuple[0])
        role_num = self.get_input_role(pinyin_list[-1])
        mapping_word_list = self.get_mapping_word_list(role_num)
        return partial_sentence, mapping_word_list
    # key_word_value_markpinyin()

    def get_single_word_pinyin_list(self, single_word):
        '''输入:单字
           输出:该字所对应的拼音数组'''
        single_word = self.to_unicode(single_word)
        return self.mulit_word_pinyin_dic[single_word]

# obj = VarifyNgramData()
# print obj.get_pinyin_list('拼音数组')
# print obj.get_pinyin_list('拼')
class GenMappingWordLengh(object):

    def __init__(self, fuzzy=False):
        self.fuzzy = fuzzy
        self.mulit_word_pinyin_dic = {}
        self._load_multi_word_pinyin_dic()

    def _load_multi_word_pinyin_dic(self):
        '''返回字典
        key为文件中的word，
        value为word所对应的pinyin_list'''
        fuzzy_dic = {'z':'zh', 'zh':'z', 'c':'ch', 'ch':'c', 's':'sh', 'sh':'s', 'h':'f', 'f':'h', 'n':'l', 'l':'n',
                     'in':'ing', 'ing':'in', 'en':'eng', 'eng':'en', 'an':'ang', 'ang':'an', 'ian':'iang', 'iang':'ian', 'uan':'uang', 'uang':'uan'}
        # print set(fuzzy_dic.keys())== set(fuzzy_dic.values())
        fuzzy_list = [ 'sh', 'ch', 'zh', 'f', 'iang', 'h', 'c','eng', 'ing', 'l', 'n', 's', 'en', 'in', 'an', 'ian', 'z', 'ang', 'uan', 'uang']
        exception_list = ['sh', 'ch', 'zh']
        # hzout_notone_filename = r'E:\SVN\linguistic_model\N_gram\HZout_NoTone.txt'
        hzout_notone_filename = os.path.join(PATH,'data', 'HZout_NoTone.txt')
        single_word_pinyin_list_dic = {}
        with codecs.open(hzout_notone_filename, encoding='utf16') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                pinyin = splited_line[1]
                try:
                    single_word_pinyin_list_dic[word].append(pinyin)
                except KeyError:
                    single_word_pinyin_list_dic[word] = [pinyin]
                if self.fuzzy:#是否进行模糊音匹配
                    prefix_fuzzy = ''
                    suffix_fuzzy = ''
                    zh_z_mark = True
                    for fuzzy_pinyin in fuzzy_list:
                        if zh_z_mark:
                            if pinyin.startswith(fuzzy_pinyin):
                                prefix_fuzzy = fuzzy_pinyin
                                if fuzzy_pinyin in exception_list:
                                    zh_z_mark = False
                                replace_pinyin = pinyin.replace(fuzzy_pinyin, fuzzy_dic[fuzzy_pinyin])
                                single_word_pinyin_list_dic[word].append(replace_pinyin)
                                # print replace_pinyin
                        if pinyin.endswith(fuzzy_pinyin) and fuzzy_pinyin != 'n':
                            suffix_fuzzy = fuzzy_pinyin
                            replace_pinyin = pinyin.replace(fuzzy_pinyin, fuzzy_dic[fuzzy_pinyin])
                            single_word_pinyin_list_dic[word].append(replace_pinyin)
                            # print replace_pinyin
                    if suffix_fuzzy and prefix_fuzzy:
                        first_replace_pinyin = pinyin.replace(prefix_fuzzy, fuzzy_dic[prefix_fuzzy])
                        second_replace_pinyin = first_replace_pinyin.replace(suffix_fuzzy, fuzzy_dic[suffix_fuzzy])
                        replace_pinyin = second_replace_pinyin
                        single_word_pinyin_list_dic[word].append(replace_pinyin)
                    zh_z_mark = True
        self.mulit_word_pinyin_dic = dict([(k,v) for (k,v) in single_word_pinyin_list_dic.items()])
        # print len(mulit_word_pinyin_dic), len(word_pinyin_list_dic)
        # return mulit_word_pinyin_dic
        # mulit_word_pinyin_dic = gen_multi_word_pinyin_dic()
    # print mulit_word_pinyin_dic[u'量']

    def get_input_role(self, pinyin):
        '''输入:拼音
           输出:按键规则（数字串）'''
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        role_num = ''.join([coding_map[letter] for letter in pinyin if letter.isalpha()])
        return role_num

    def get_word_mapping_role_num(self, word):
        '''输入:单字
           输出:该单字所对应的按键序列（fuzzy参数表示是否含有模糊音匹配）'''
        # mulit_word_pinyin_dic = gen_multi_word_pinyin_dic()
        return [self.get_input_role(pinyin) for pinyin in set(self.mulit_word_pinyin_dic[word])]

    def gen_max_mapping_word_lenght_and_role_num_list_lenght(self):
        '''1、计算所给文件的中单字对应role_num去重后的个数（254）
           2、计算role_num所对应的汉字数组中最长的数组有多少个汉字（244）'''
        gram_danzi_inputrole_dic = {}
        # mulit_word_pinyin_dic = gen_multi_word_pinyin_dic()
        filename = r'C:\Users\wanghuafeng\Desktop\ngram_model\gram_danzi_list.txt'
        with codecs.open(filename, encoding='utf16') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                word = splited_line[0]
                gram_danzi_inputrole_dic[word] = [self.get_input_role(pinyin) for pinyin in set(
                    self.mulit_word_pinyin_dic[word])]
        role_num_word_dic = {}
        for single_word,input_role_list in gram_danzi_inputrole_dic.items():
            for role_num in input_role_list:
                try:
                    role_num_word_dic[role_num].append(single_word)
                except KeyError:
                    role_num_word_dic[role_num] = [single_word]

        max_lenght_mapping_word = max(role_num_word_dic.values(), key=lambda x:len(x))
        print len(max_lenght_mapping_word), len(role_num_word_dic)

class SouGouCloudWord(object):
    def __init__(self, module_path='E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'):
        # module_path = 'E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words'
        # sys.path.append(module_path)
        # from  add_words_spell_m import WordsSearch
        from pinyin_add_mudule.add_words_spell import WordsSearch
        self.ws = WordsSearch()

    def to_unicode(self, sentence):
        '''输入:字符编码、或Unicode编码
           输出:Unicode编码'''
        if isinstance(sentence, str):
            try:
                sentence = sentence.decode('utf-8')
            except Exception,e:
                sentence = sentence.decode('gbk')
        return sentence

    def get_input_role_num(self, pinyin):
        '''输入:拼音
           输出:按键规则（数字串）'''
        coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}
        role_num = ''.join([coding_map[letter] for letter in pinyin if letter.isalpha()])
        return role_num

    def get_pinyin(self, sentence):
        '''输入:unicode格式句子
           输出:输出pinyin(拼音字符串，中间用空格隔开)'''
        sentence = self.to_unicode(sentence)
        pinyin_str = ' '.join(self.ws.get_splited_pinyin(sentence)[0]).replace('*', '')
        return pinyin_str

    def form_sentence_to_role_num(self, sentence):
        '''输入:句子
           输出:按键序列（数字串）'''
        sentence = self.to_unicode(sentence)
        pinyin = self.get_pinyin(sentence)
        no_blank_pinyin = pinyin.replace(' ', '')
        role_num = self.get_input_role_num(no_blank_pinyin)
        return role_num

    def request_sougou_cloud_word(self, role_num):
        '''输入:数字串
           输出:与该字符串相匹配的搜狗云词'''
        import sogou_cloud_words
        if isinstance(role_num, int):
            role_num = str(role_num)
        matched_sentence = sogou_cloud_words.get_cloud_words(role_num)[0]
        return matched_sentence

# sg = SouGouCloudWord(module_path='E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words')
# print sg.get_pinyin('数字串')
# print sg.form_sentence_to_role_num('数字串')#7489424826
# sg.request_sougou_cloud_word('7489424826')

# if __name__ == '__main__':
    # vnd = VarifyNgramData('E:\SVN\chocolate_ime\script\gen_update_words\gen_hot_words')
    #print vnd.get_pinyin_list('谁知道')
    # print vnd.get_input_role('yes')
    # prefix, mapping_word_list = vnd.get_code_sentence('快快乐乐的')
    # print prefix, mapping_word_list

    # mulit_word_pinyin_dic = gen_multi_word_pinyin_dic()
    # print mulit_word_pinyin_dic[u'量']
    # gw = GenMappingWordLengh()