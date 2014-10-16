__author__ = 'wanghuafeng'
#coding:utf-8
import os
import codecs
import time
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()
#****************************************************************
# 修正的Kneser-Ney平滑算法
#****************************************************************
def every_bigram_item_detele_1():
    filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq.txt')
    com_str_list = []
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            splited_line = line.split('\t')
            bigram_item = splited_line[0]
            freq_int = int(splited_line[-1])
            if freq_int <= 2:
                continue
            else:
                freq_int = freq_int - 2
            com_str = '\t'.join((bigram_item, str(freq_int)+'\n'))
            com_str_list.append(com_str)
    freq_delete_1_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2.txt')
    codecs.open(freq_delete_1_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
# every_bigram_item_detele_1()
def gen_freq_count_of_1_and_2():
    '''统计出词频数为1，或者为2的二元模型的数目'''
    total_count = 0#36292642
    n1 = 0#17050532
    n2 = 0#5462655
    n3 = 0
    n4 = 0
    bigram_freq_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_word_freq_remove_20.txt')
    with codecs.open(bigram_freq_filename, encoding='utf-8') as f:
        for line in f.readlines():
            total_count += 1
            splited_line = line.strip().split('\t')
            if splited_line[-1] == '1':
                n1 += 1
            elif splited_line[-1] == '2':
                n2 += 1
            elif splited_line[-1] == '3':
                n3 += 1
            elif splited_line[-1] == '4':
                n4 += 1
    print 'total_lenght is %s'%total_count
    print 'count_lenght_1 is %s'%n1
    print 'count_lenght_2 is %s'%n2
    print 'count_lenght >= 3 is %s'%(total_count-n1-n2)
    print 'count_lenght_3 is %s'%n3
    print 'count_lenght_4 is %s'%n4
    Y = float(n1)/(n1+2*n2)
    print 'Y=%s'%Y#Y=n1/(n1+2*n2)
    print 'D1=%s'%(1-2*Y*(float(n2)/n1))#D1=1-2Y(n2/n1)
    print 'D2=%s'%(2-3*Y*(float(n3)/n2))#D2=2-3Y(n3/n2)
    print 'D3=%s'%(3-4*Y*(float(n4)/n3))#D3=3-4Y(n4/n3)
    # print 'Y=n1/(n1+2*n2) ====>> %s'%Y
    # print 'D1=1-2Y(n2/n1) ====>> %s'%(1-2*Y*(float(n2)/n1))
    # print 'D2=2-3Y(n3/n2) ====>> %s'%(2-3*Y*(float(n3)/n2))
    # print 'D3=3-4Y(n4/n3) ====>> %s'%(3-4*Y*(float(n4)/n3))
# total_lenght is 19071617
# count_lenght_1 is 4182352
# count_lenght_2 is 2545827
# count_lenght >= 3 is 12343438
# count_lenght_3 is 1735861
# count_lenght_4 is 1388726
# Y=n1/(n1+2*n2) ====>> 0.450975770341
# D1=1-2Y(n2/n1) ====>> 0.450975770341
# D2=2-3Y(n3/n2) ====>> 1.07751243308
# D3=3-4Y(n4/n3) ====>> 1.55683887675

# gen_freq_count_of_1_and_2()

def mk_bigram_item_inorder():
    '''对二元组元素按照第一个汉字进行排序'''
    freq_delete_1_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2.txt')
    line_inorder_list = sorted(codecs.open(freq_delete_1_filename, encoding='utf-8').readlines())
    file_inorder_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
    codecs.open(file_inorder_filename, mode='wb', encoding='utf-8').writelines(line_inorder_list)
# mk_bigram_item_inorder()

class SmoothArithmetic:
    '''Kneser-Ney平滑算法'''
    def __init__(self):
        self.src_data_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_word_freq_remove_20.txt')

    def gen_first_word_total_freq_dic(self):
        '''以第一个元素相同的二元组中元素为key，该元素所有频度之和为value生成字典'''
        inorder_bigaram_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_word_freq_remove_20.txt')
        assert os.path.isfile(inorder_bigaram_filename)
        total_frist_word_freq_dic = {}
        with codecs.open(inorder_bigaram_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                first_word_of_unigram_item = line.split(',')[0]
                # print first_word_of_unigram_item
                # time.sleep(1)
                freq_int = int(splited_line[-1])
                try:
                    total_frist_word_freq_dic[first_word_of_unigram_item] += freq_int
                except KeyError:
                    total_frist_word_freq_dic[first_word_of_unigram_item] = freq_int
        # return total_frist_word_freq_dic
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in total_frist_word_freq_dic.items()]
        temp_filename = r'E:\SVN\linguistic_model\9_keys\big_linguistic_data\data\first_word_freq_count.txt'
        first_word_freq_filename = os.path.join(PATH, 'first_word_freq_count.txt')
        codecs.open(temp_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def get_total_freq_int(self):
        '''计算所有二元模型频度之和(869,788,684)（一元模型单词统计855，995，524）'''
        inorder_bigaram_filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
        total_freq_int = sum([int(item.split('\t')[-1]) for item in codecs.open(self.src_data_filename, encoding='utf-8').readlines()])
        print total_freq_int#7080444038
    def KN_smooth(self):
        '''对词频为1,2,3+的first_word分别做不同处理'''
        D1=0.352182669442
        D2=1.02440824334
        D3=1.68988623401
        KN_smooth_dic = {}
        filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
        with codecs.open(self.src_data_filename, encoding='utf-8') as f:
            for line in f.readlines():
                first_word = line.split(',')[0]
                freq_int = int(line.split('\t')[-1])
                if freq_int == 1:
                    smooth_param = D1
                elif freq_int == 2:
                    smooth_param = D2
                else:
                    smooth_param = D3
                # smooth_param = D1 if freq_int == 1 else D2 if freq_int == 2 else D3
                try:
                    KN_smooth_dic[first_word] += freq_int*smooth_param
                except KeyError:
                    KN_smooth_dic[first_word] = freq_int*smooth_param
                # print KN_smooth_dic
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in KN_smooth_dic.items()]
        kn_smooth_param_filename = os.path.join(PATH,  'kn_smooth_param.txt')
        temp_filename = r'E:\SVN\linguistic_model\9_keys\big_linguistic_data\data\kn_smooth_param.txt'
        codecs.open(temp_filename, mode='wb', encoding='utf-8').writelines(com_str_list)
    def second_word_count(self):
        '''获取所要查询二元模型的second_word的total_count'''
        filename = os.path.join(PATH, '0709modify', 'cuted_linguistic_stample', 'combine_bigram_freq_delete_2_inorder.txt')
        second_freq_dic = {}
        with codecs.open(self.src_data_filename, encoding='utf-8') as f:
            for line in f.readlines():
                splited_line = line.split('\t')
                second_word = splited_line[0].split(',')[-1]
                freq_int = int(splited_line[-1])
                try:
                    second_freq_dic[second_word] += freq_int
                except KeyError:
                    second_freq_dic[second_word] = freq_int
        com_str_list = ['\t'.join((k,str(v)))+'\n' for k,v in second_freq_dic.items()]
        second_word_count_filename = os.path.join(PATH, 'second_word_count.txt')
        temp_filename = r'E:\SVN\linguistic_model\9_keys\big_linguistic_data\data\second_word_count.txt'
        codecs.open(temp_filename, mode='wb', encoding='utf-8').writelines(com_str_list)

# sa = SmoothArithmetic()
# sa.second_word_count()
