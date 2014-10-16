#coding:utf-8
import simplejson
import time
import urllib2
from add_pinyin_to_single_word import AddPinyin
import sogou_cloud_words

coding_map = {'a': '2', 'c': '2', 'b': '2', 'e': '3', 'd': '3', 'g': '4', 'f': '3', 'i': '4', 'h': '4', 'k': '5', 'j': '5', 'm': '6', 'l': '5', 'o': '6', 'n': '6', 'q': '7', 'p': '7', 's': '7', 'r': '7', 'u': '8', 't': '8', 'w': '9', 'v': '8', 'y': '9', 'x': '9', 'z': '9'}

def get_pinyin(sentence):
    add_pinyin = AddPinyin()
    pinyin_list = []
    for word in sentence:
        pinyin = add_pinyin.get_pinyin(word)
        pinyin_list.append(pinyin)
    pinyin_str = ''.join(pinyin_list)
    role_num = ''.join([coding_map[letter] for letter in pinyin_str if letter.isalpha()])
    return role_num

def post_to_ali(role_num):
    url = 'http://ali_0000.baiwenbao.com:5000/%s'%role_num
    html = urllib2.urlopen(url).read()
    json_list = simplejson.loads(html)
    print json_list[0]
def post_to_local(role_num):
    url = 'http://127.0.0.1:5000/%s'%role_num
    html = urllib2.urlopen(url).read()
    json_list = simplejson.loads(html)
    print json_list[0]

if __name__ == "__main__":
    start_time = time.time()
    sentence = u'我吓坏了'
    role_num = get_pinyin(sentence)
    # role_num = '366428332472436832338247484'
    # role_num = 'jintianyourenqudapingpangqiuma'
    post_to_ali(role_num)
    # post_to_local(role_num)
