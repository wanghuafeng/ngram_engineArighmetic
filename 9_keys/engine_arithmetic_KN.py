__author__ = 'wanghuafeng'
#coding:utf8
import os
import glob
import re
import time
import codecs
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()
MAX_LENGHT = 100
class EngineArithmetic:
    def __init__(self):
        self.src_data_path = r'E:\SVN\linguistic_model\9_keys\big_linguistic_data\data'
        self.bigram_item_total_count = 7080444038.0#所有二元模型元素的频度之和
        self.real_prefix_set = set()#真前缀列表
        self._real_prefix_rolenum()
        self.total_mapping_dic = {}#输入规则的字典
        self._load_mapping_rolenum_wordlist()
        self.kn_smooth_param_dic = {}#低阶平滑参数
        self._load_kn_smooth_param()
        self.second_word_count_dic = {}#二元模型中second_word的total_count与所有二元组元素之和的比例
        self._load_second_word_count()
        self.first_word_count_dic = {}#所有二元模型中first_wrod的total_count
        self._load_first_word_freq_count()
        self.word_weight_dic = {}#二元模型字典
        self._load_word_weigh()
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_filename = os.path.join(self.src_data_path, 'prefix_if_mapping_role_num.txt')
        with codecs.open(real_prefix_filename, encoding='utf-8') as f:
            self.real_prefix_set = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(self.src_data_path, 'combine_top60000_and_5041_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_kn_smooth_param(self):
        '''加载kn_smooth参数'''
        kn_smooth_filename = os.path.join(self.src_data_path, 'kn_smooth_param.txt')
        assert os.path.isfile(kn_smooth_filename)
        with codecs.open(kn_smooth_filename, encoding='utf-8') as f:
            self.kn_smooth_param_dic = dict([(item.split('\t')[0], float(item.split('\t')[1])) for item in f.readlines()])
    def _load_second_word_count(self):
        '''二元模型中second_word的total_count与所有二元组元素之和的比例'''
        second_word_filename = os.path.join(self.src_data_path, 'second_word_count.txt')
        assert os.path.isfile(second_word_filename)
        with codecs.open(second_word_filename, encoding='utf-8') as f:
            self.second_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])/self.bigram_item_total_count) for item in f.readlines()])
    def _load_first_word_freq_count(self):
        '''二元模型中first_word的total_count'''
        first_word_filename = os.path.join(self.src_data_path, 'first_word_freq_count.txt')
        assert os.path.isfile(first_word_filename)
        with codecs.open(first_word_filename, encoding='utf-8') as f:
            self.first_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])) for item in f.readlines()])
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与词频成字典'''
        D1=0.352182669442
        D2=1.02440824334
        D3=1.68988623401
        word_weight_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_word_freq_remove_20.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                bigram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                freq = freq_int - (D1 if freq_int == 1 else D2 if freq_int == 2 else D3)
                self.word_weight_dic[bigram_item] = freq
            # words_weight_list = [(item.split('\t')[0], int(item.split('\t')[1])) for item in f.readlines()]
            # self.word_weight_dic = dict(words_weight_list)
    def handle_key_input_str(self, key_input, top_count=1):
        key_input = key_input.strip()
        matched_route_list = [('#',[],1)]
        prefix_route_list = []
        lenght_key_input = len(key_input)
        key_input_index = 0
        for key in key_input:
            #key是否有mapping匹配
            temp_matched_route_list = []
            temp_prefix_route_list = []
            key_mapping_word_list = self.total_mapping_dic.get(key)
            #如果key有汉字匹配
            if key_mapping_word_list:
                #对matched_route_list的影响
                for mapping_word in key_mapping_word_list:
                    for last_matched_route_param in matched_route_list:
                        #matched_route_list三元组中汉字部分是否为空数组
                        if last_matched_route_param[1]:#如果不为空
                            bigram_item = last_matched_route_param[1][-1]+','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic[last_matched_route_param[1][-1]]*self.second_word_count_dic.get(mapping_word, 0))/self.first_word_count_dic[last_matched_route_param[1][-1]]
                            #如果查不到bigram_item对应的weight
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight * last_matched_route_param[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                        #key_input_str中的第一个key有匹配
                        else:
                            bigram_item = 'BOS'+','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic['BOS']*self.second_word_count_dic.get(mapping_word, 0))/self.first_word_count_dic['BOS']
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight * last_matched_route_param[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                ##对prefix_route_list的影响
                for last_matched_route_param in matched_route_list:
                    prefix_route_word_list = last_matched_route_param[1] + []
                    prefix_route_weight = last_matched_route_param[-1]
                    temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))
            #key不匹配mapping_word
            else:
                ##对prefix_route_list的影响
                for last_matched_route_param in matched_route_list:
                    prefix_route_word_list = last_matched_route_param[1] + []
                    prefix_route_weight = last_matched_route_param[-1]
                    temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))
            if len(temp_matched_route_list)>MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1], reverse=True)
                temp_matched_route_list = temp_matched_route_list[:MAX_LENGHT]
            if len(temp_prefix_route_list)>MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1], reverse=True)
                temp_prefix_route_list = temp_prefix_route_list[:MAX_LENGHT]
            #key+old_key_str是否有对应汉字匹配
            for prefix_route_param_tuple in prefix_route_list:
                old_key_str = prefix_route_param_tuple[0]
                new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                new_keys_mapping_words_list = self.total_mapping_dic.get(new_combine_keys)
                #如果combine_keys对应有汉字匹配
                if new_keys_mapping_words_list:
                    #对matched_route_list的影响
                    for mapping_word in new_keys_mapping_words_list:
                        #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                        if not prefix_route_param_tuple[1]:
                            bigram_item = 'BOS'+','+mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic['BOS']*self.second_word_count_dic.get(mapping_word, 0))/self.first_word_count_dic['BOS']
                            temp_matched_route_list.append(('#', [mapping_word], weight))
                        #（old_key_str,[],weight）第二个参数不为空
                        else:
                            bigram_item = prefix_route_param_tuple[1][-1]+','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic[prefix_route_param_tuple[1][-1]]*self.second_word_count_dic.get(mapping_word, 0))/self.first_word_count_dic[prefix_route_param_tuple[1][-1]]
                            new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                            new_weight = weight * prefix_route_param_tuple[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                    #对prefix_route_list的影响
                    new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                    new_prefix_route_weight = prefix_route_param_tuple[-1]
                    temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                #key+old_key_str是否有对应汉字匹配
                else:
                    if new_combine_keys in self.real_prefix_set:
                        new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

            if len(temp_matched_route_list)>MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1], reverse=True)
                matched_route_list = temp_matched_route_list[:MAX_LENGHT]
                # self.max_weight_in_complete_path = max(matched_route_list, key=lambda x:x[-1])
            else:
                matched_route_list = temp_matched_route_list[:]
            if len(temp_prefix_route_list)>MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1], reverse=True)
                prefix_route_list = temp_prefix_route_list[:MAX_LENGHT]
                # self.max_weight_in_incomplete_path = max(prefix_route_list, key=lambda x:x[-1])
            else:
                prefix_route_list = temp_prefix_route_list[:]

            ##按键到最后一位时，添加EOS
            key_input_index += 1
            if key_input_index == lenght_key_input:
                final_bigram_weight_list = []
                for matched_route_param in matched_route_list:
                    mapping_word_list = matched_route_param[1]
                    if mapping_word_list:
                        bigram_item = mapping_word_list[-1]+','+'EOS'
                        weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic[mapping_word_list[-1]]*self.second_word_count_dic['EOS'])/self.first_word_count_dic[mapping_word_list[-1]]
                        new_matched_word_list = mapping_word_list
                        new_weight = weight * matched_route_param[-1]
                        final_bigram_weight_list.append((' '.join(new_matched_word_list), new_weight))
                return sorted(final_bigram_weight_list, key=lambda x:x[-1], reverse=True)[:top_count]

# ea = EngineArithmetic()
# key_input = '248943264742642874'
# start_time = time.time()
# top_matched_sentence_weight_list = ea.handle_key_input_str(key_input,5)
# end_time = time.time()
# print end_time - start_time
# # print top_matched_sentence_weight_list
# for param_tuple in top_matched_sentence_weight_list:
#     print param_tuple[0]

class EngineArithmeticNoBOS:
    def __init__(self):
        self.src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify\bigram'
        # self.bigram_item_total_count = 399767948.0#所有二元模型元素的频度之和
        self.real_prefix_set = set()#真前缀列表
        self._real_prefix_rolenum()
        self.total_mapping_dic = {}#输入规则的字典
        self._load_mapping_rolenum_wordlist()
        self.kn_smooth_param_dic = {}#低阶平滑参数
        self._load_kn_smooth_param()
        self.second_word_percentage_dic = {}#二元模型中second_word的total_count与所有二元组元素之和的比例
        self._load_second_word_count()
        self.first_word_count_dic = {}#所有二元模型中first_wrod的total_count
        self._load_first_word_freq_count()
        self.word_weight_dic = {}#二元模型字典
        self._load_unigram_percentage()#加载一元模型数据
        self._load_word_weigh()
    def _real_prefix_rolenum(self):
        '''加载所有真前缀组合'''
        real_prefix_filename = os.path.join(self.src_data_path, 'prefix_if_mapping_role_num.txt')
        with codecs.open(real_prefix_filename, encoding='utf-8') as f:
            self.real_prefix_set = set([item.strip() for item in f.readlines()])
    def _load_mapping_rolenum_wordlist(self):
        '''以输入规则为key，以与该输入规则对应的基础词库中词元素集合所构成的数组为value生成字典'''
        mapping_filename = os.path.join(self.src_data_path, 'combine_5233_and_top60000_pinyin_role_inorder_mapping.txt')
        with codecs.open(mapping_filename, encoding='utf-8') as f:
            role_num_words = [(item.split('\t')[0], item.split('\t')[1].strip().split(',')) for item in f.readlines()]
            self.total_mapping_dic = dict(role_num_words)
    def _load_kn_smooth_param(self):
        '''加载kn_smooth参数'''
        kn_smooth_filename = os.path.join(self.src_data_path, 'kn_smooth_param.txt')
        assert os.path.isfile(kn_smooth_filename)
        with codecs.open(kn_smooth_filename, encoding='utf-8') as f:
            self.kn_smooth_param_dic = dict([(item.split('\t')[0], float(item.split('\t')[1])) for item in f.readlines()])
    def _load_second_word_count(self):
        '''二元模型中second_word的total_count与所有二元组元素之和的比例'''
        second_word_filename = os.path.join(self.src_data_path, 'second_word_percentage.txt')
        assert os.path.isfile(second_word_filename)
        with codecs.open(second_word_filename, encoding='utf-8') as f:
            # self.second_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])/self.bigram_item_total_count) for item in f.readlines()])
            for line in f.readlines():
                splited_line = line.split('\t')
                second_word = splited_line[0]
                percentage = float(splited_line[-1])
                self.second_word_percentage_dic[second_word] = percentage
    def _load_first_word_freq_count(self):
        '''二元模型中first_word的total_count'''
        first_word_filename = os.path.join(self.src_data_path, 'first_word_freq_count.txt')
        assert os.path.isfile(first_word_filename)
        with codecs.open(first_word_filename, encoding='utf-8') as f:
            self.first_word_count_dic = dict([(item.split('\t')[0], int(item.split('\t')[-1])) for item in f.readlines()])
    def _load_unigram_percentage(self):
        filename = os.path.join(self.src_data_path, 'unigram_item_percentage.txt')
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                ngram_item = splited_line[0]
                percentage = float(splited_line[-1])
                self.word_weight_dic[ngram_item] = percentage
    def _load_word_weigh(self):
        '''加载二元组模型，以二元组元素为key，与词频成字典'''
        D1=0.630999593298
        D2=1.09109751165
        D3=1.46364610581
        word_weight_filename = os.path.join(self.src_data_path, 'combine_bigram_freq_cutoff_5.txt')
        with codecs.open(word_weight_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                bigram_item = splited_line[0]
                freq_int = int(splited_line[-1])
                freq = freq_int - (D1 if freq_int == 1 else D2 if freq_int == 2 else D3)
                self.word_weight_dic[bigram_item] = freq
    def handle_key_input_str(self, key_input, top_count=1):
        key_input = key_input.strip()
        matched_route_list = [('#',[],1)]
        prefix_route_list = []
        lenght_key_input = len(key_input)
        key_input_index = 0
        for key in key_input:
            #key是否有mapping匹配
            temp_matched_route_list = []
            temp_prefix_route_list = []
            key_mapping_word_list = self.total_mapping_dic.get(key)
            #如果key有汉字匹配
            if key_mapping_word_list:
                #对matched_route_list的影响
                for mapping_word in key_mapping_word_list:
                    for last_matched_route_param in matched_route_list:
                        #matched_route_list三元组中汉字部分是否为空数组
                        if last_matched_route_param[1]:#如果不为空
                            bigram_item = last_matched_route_param[1][-1]+','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic.get(last_matched_route_param[1][-1], 0)*self.second_word_percentage_dic.get(mapping_word, 0))/self.first_word_count_dic.get(last_matched_route_param[1][-1], 200000)
                            #如果查不到bigram_item对应的weight
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight * last_matched_route_param[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                        #key_input_str中的第一个key有匹配
                        else:
                            bigram_item = mapping_word
                            # weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic['BOS']*self.second_word_percentage_dic.get(mapping_word, 0))/self.first_word_count_dic['BOS']
                            weight =self.word_weight_dic.get(bigram_item, 1)
                            new_matched_word_list = last_matched_route_param[1] + [mapping_word]
                            new_weight = weight * last_matched_route_param[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                    ##对prefix_route_list的影响
                for last_matched_route_param in matched_route_list:
                    prefix_route_word_list = last_matched_route_param[1] + []
                    prefix_route_weight = last_matched_route_param[-1]
                    temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))
            #key不匹配mapping_word
            else:
                ##对prefix_route_list的影响
                for last_matched_route_param in matched_route_list:
                    prefix_route_word_list = last_matched_route_param[1] + []
                    prefix_route_weight = last_matched_route_param[-1]
                    temp_prefix_route_list.append((key, prefix_route_word_list, prefix_route_weight))
            if len(temp_matched_route_list)>MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1], reverse=True)
                temp_matched_route_list = temp_matched_route_list[:MAX_LENGHT]
            if len(temp_prefix_route_list)>MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1], reverse=True)
                temp_prefix_route_list = temp_prefix_route_list[:MAX_LENGHT]
                #key+old_key_str是否有对应汉字匹配
            for prefix_route_param_tuple in prefix_route_list:
                old_key_str = prefix_route_param_tuple[0]
                # new_combine_keys = ''.join((old_key_str, key))#新输入的key为最末位
                new_combine_keys = old_key_str + key#新输入的key为最末位
                new_keys_mapping_words_list = self.total_mapping_dic.get(new_combine_keys)
                #如果combine_keys对应有汉字匹配
                if new_keys_mapping_words_list:
                    #对matched_route_list的影响
                    for mapping_word in new_keys_mapping_words_list:
                        #如果new_combine_keys第一次匹配，即（old_key_str,[],weight）第二个参数为空
                        if not prefix_route_param_tuple[1]:
                            # bigram_item = 'BOS'+','+mapping_word
                            bigram_item = mapping_word
                            # weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic['BOS']*self.second_word_percentage_dic.get(mapping_word, 0))/self.first_word_count_dic['BOS']
                            weight = self.word_weight_dic.get(bigram_item, 1)
                            temp_matched_route_list.append(('#', [mapping_word], weight))
                        #（old_key_str,[],weight）第二个参数不为空
                        else:
                            bigram_item = prefix_route_param_tuple[1][-1]+','+ mapping_word
                            weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic.get(prefix_route_param_tuple[1][-1], 0)*self.second_word_percentage_dic.get(mapping_word, 0))/self.first_word_count_dic.get(prefix_route_param_tuple[1][-1], 200000)
                            new_matched_word_list = prefix_route_param_tuple[1] + [mapping_word]
                            new_weight = weight * prefix_route_param_tuple[-1]
                            temp_matched_route_list.append(('#', new_matched_word_list, new_weight))
                        #对prefix_route_list的影响
                    new_prefix_route_tuple = prefix_route_param_tuple[1] + []
                    new_prefix_route_weight = prefix_route_param_tuple[-1]
                    temp_prefix_route_list.append((new_combine_keys, new_prefix_route_tuple, new_prefix_route_weight))
                #key+old_key_str是否有对应汉字匹配
                else:
                    if new_combine_keys in self.real_prefix_set:
                        new_prefix_route_wordlist = prefix_route_param_tuple[1] + []
                        new_prefix_route_weight = prefix_route_param_tuple[-1]
                        temp_prefix_route_list.append((new_combine_keys, new_prefix_route_wordlist, new_prefix_route_weight))

            if len(temp_matched_route_list)>MAX_LENGHT:
                temp_matched_route_list = sorted(temp_matched_route_list, key=lambda x:x[-1], reverse=True)
                matched_route_list = temp_matched_route_list[:MAX_LENGHT]
                # self.max_weight_in_complete_path = max(matched_route_list, key=lambda x:x[-1])
            else:
                matched_route_list = temp_matched_route_list[:]
            if len(temp_prefix_route_list)>MAX_LENGHT:
                temp_prefix_route_list = sorted(temp_prefix_route_list, key=lambda x:x[-1], reverse=True)
                prefix_route_list = temp_prefix_route_list[:MAX_LENGHT]
                # self.max_weight_in_incomplete_path = max(prefix_route_list, key=lambda x:x[-1])
            else:
                prefix_route_list = temp_prefix_route_list[:]

            ##按键到最后一位时，添加EOS
            # key_input_index += 1
            # if key_input_index == lenght_key_input:
            #     return matched_route_list[:top_count]
            key_input_index += 1
            if key_input_index == lenght_key_input:
                # output_inorder_list = sorted(matched_route_list, key=lambda x:x[-1], reverse=True)[:top_count]
                output_inorder_list = matched_route_list[:top_count]
                sentence_weight_tuple_list = []
                for items in output_inorder_list:
                    mark, word_list, weight = items
                    output_tuple = (''.join(word_list), weight)
                    sentence_weight_tuple_list.append(output_tuple)
                return sentence_weight_tuple_list
                # final_bigram_weight_list = []
                # for matched_route_param in matched_route_list:
                #     mapping_word_list = matched_route_param[1]
                #     if mapping_word_list:
                #         bigram_item = mapping_word_list[-1]+','+'EOS'
                #         weight = (self.word_weight_dic.get(bigram_item, 0) + self.kn_smooth_param_dic[mapping_word_list[-1]]*self.second_word_percentage_dic['EOS'])/self.first_word_count_dic[mapping_word_list[-1]]
                #         new_matched_word_list = mapping_word_list
                #         new_weight = weight * matched_route_param[-1]
                #         final_bigram_weight_list.append((' '.join(new_matched_word_list), new_weight))
                # return sorted(final_bigram_weight_list, key=lambda x:x[-1], reverse=True)[:top_count]
# ea = EngineArithmeticNoBOS()
# key_input = '248943264742642874'
# start_time = time.time()
# top_matched_sentence_weight_list = ea.handle_key_input_str(key_input,5)
# end_time = time.time()
# print end_time - start_time
# # print top_matched_sentence_weight_list
# for param_tuple in top_matched_sentence_weight_list:
#     print param_tuple[1], param_tuple[-1]
def caculate_sentence_percentage():
    ea = EngineArithmeticNoBOS()
    start_time = time.time()
    varify_sample_filename = os.path.join(PATH, '0709modify', 'cuted_varify_sample_pinyin_role_no_repeat.txt')
    checkout_sample_filename_backward = os.path.join(PATH, '0709modify', 'Kneser_Ney_smooth_checkout.txt')
    with codecs.open(varify_sample_filename, encoding='utf-8') as f,\
    codecs.open(checkout_sample_filename_backward, mode='wb', encoding='utf-8') as wf:
        count = 0
        for line in f.readlines():
            temp_list_for_write = []
            count += 1
            print count
            splited_line = line.split('\t')
            sentence = splited_line[0]
            key_str = splited_line[-1]
            com_str = '*'+sentence+'\n'
            temp_list_for_write.append(com_str)
            top_matched_sentence_weight_list = ['\t'.join((item[0], str(item[1])))+'\n' for item in ea.handle_key_input_str(key_str, 5)]
            temp_list_for_write.extend(top_matched_sentence_weight_list)
            wf.writelines(temp_list_for_write)
    end_time = time.time()
    print end_time-start_time
# caculate_sentence_percentage()

def get_sentence_accuracy_top_n():
    '''样本文件中句子的精确度AS'''
    PATH = r'E:\SVN\linguistic_model\9_keys\0709modify'
    checkout_filename = os.path.join(PATH, 'Kneser_Ney_smooth_checkout.txt')
    # checkout_filename = os.path.join(PATH, '0709modify', 'cut_path_lenght_limit_100_delete_2.txt')
    top_n_sentence_list = []
    correct_sentence = ''
    matched_sentence_count = 0
    total_count = 0
    top_count = 1
    with codecs.open(checkout_filename, encoding='utf-8')as f:
        for line in f.readlines():
            if line.startswith('*'):
                total_count += 1
                if correct_sentence in top_n_sentence_list[:top_count]:
                    matched_sentence_count += 1
                top_n_sentence_list[:] = []
                correct_sentence = line.strip()[1:]
            else:
                sentence = line.split('\t')[0].replace(' ','')
                top_n_sentence_list.append(sentence)
    print total_count, matched_sentence_count
    print str(matched_sentence_count/float(total_count)*100)+'%'
# get_sentence_accuracy_top_n()

def _load_word_weigh():
    '''加载二元组模型，以二元组元素为key，与权重构成字典'''
    word_weight_filename = os.path.join(PATH,  'cuted_linguistic_sample', 'combine_bigram_freq_weight.txt')
    # word_weight_filename = os.path.join(PATH, '0709modify',  'aaaaaaaaaaaa_weight.txt')
    with codecs.open(word_weight_filename, encoding='utf-8') as f:
        words_weight_list = [(item.split('\t')[0], item.split('\t')[1].strip()) for item in f.readlines()]
        word_weight_dic = dict(words_weight_list)
        return word_weight_dic

def check_weight():
    item_weight_dic = _load_word_weigh()
    while 1:
        bigram_item = raw_input('bigram_item:').decode('utf-8')
        item_weight = item_weight_dic.get(bigram_item)
        print 'item_weight:%s'%item_weight
        if not item_weight:
            item_weight = item_weight_dic.get(bigram_item.split(',')[0]+','+'*')
            print 'weight * :%s'%item_weight
# check_weight()

def unigram_percentage():
    src_data_file_path = r'E:\SVN\linguistic_model\9_keys'
    filename = os.path.join(src_data_file_path, '0709modify', 'bigram', 'unigram_combine_word_freq.txt')
    total_line_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        line_list = f.readlines()
        total_freq = sum([int(item.split('\t')[-1]) for item in line_list])
        print total_freq
        time.sleep(4)
    for line in line_list:
        splited_line = line.split('\t')
        ngram_item = splited_line[0]
        freq_int = int(splited_line[-1])
        percentage = freq_int/float(total_freq)
        # if percentage == 0:
        #     percentage = 1
        com_str = ngram_item + '\t' + str(percentage) + '\n'
        total_line_list.append(com_str)
    filename_to_write = os.path.join(src_data_file_path, '0709modify', 'bigram', 'unigram_item_percentage.txt')
    codecs.open(filename_to_write, mode='wb', encoding='utf-8').writelines(total_line_list)
# unigram_percentage()

def multi_thread(filepart, start_index, end_index):
    ea = EngineArithmeticNoBOS()
    start_time = time.time()
    src_data_path = r'E:\SVN\linguistic_model\9_keys\0709modify'
    varify_sample_filename = os.path.join(src_data_path, 'cuted_varify_sample_pinyin_role_no_repeat.txt')
    des_path = r'E:\SVN\linguistic_model\9_keys\0709modify'
    checkout_sample_filename_backward = os.path.join(des_path,'Kneser_Ney_smooth_checkout_limit_100_fourgram_%s.txt'%filepart)
    with codecs.open(varify_sample_filename, encoding='utf-8') as f, \
        codecs.open(checkout_sample_filename_backward, mode='wb', encoding='utf-8') as wf:
        count = 0
        for line in f.readlines()[start_index:end_index]:
            temp_list_for_write = []
            count += 1
            print count
            splited_line = line.split('\t')
            sentence = splited_line[0]
            key_str = splited_line[-1]
            com_str = '*'+sentence+'\n'
            temp_list_for_write.append(com_str)
            top_matched_sentence_weight_list = ['\t'.join((item[0], str(item[1])))+'\n' for item in ea.handle_key_input_str(key_str, 5)]
            temp_list_for_write.extend(top_matched_sentence_weight_list)
            wf.writelines(temp_list_for_write)
    end_time = time.time()
    print end_time-start_time

def combine_file_part_accuracy():
    glob_filepath = r'E:\SVN\linguistic_model\N_gram\splited_linguistic_data\running_in_ali\Kneser_Ney_smooth_checkout_limit_100_fourgram_*.txt'
    matched_file_list = glob.glob(glob_filepath)
    n_part_file_list = [item for item in matched_file_list if re.match(r'\d', item.split('.')[0][-1])]
    total_files_lines_list = []
    for filename in n_part_file_list:
        with codecs.open(filename, encoding='utf-8') as f:
            total_files_lines_list.extend(f.readlines())

    top_n_sentence_list = []
    correct_sentence = ''
    matched_sentence_count = 0
    total_count = 0
    top_count = 1
    for line in total_files_lines_list:
        if line.startswith('*'):
            total_count += 1
            if correct_sentence in top_n_sentence_list[:top_count]:
                matched_sentence_count += 1
            top_n_sentence_list[:] = []
            correct_sentence = line.strip()[1:]
        else:
            sentence = line.split('\t')[0].replace(' ','')
            top_n_sentence_list.append(sentence)
    print total_count, matched_sentence_count
    print str(matched_sentence_count/float(total_count)*100)+'%'
# combine_file_part_accuracy()
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes=2)
#     pool.apply_async(multi_thread, (1, 0, 40000))
#     pool.apply_async(multi_thread, (2, 40000, 72000))
#     pool.close()
#     pool.join()
