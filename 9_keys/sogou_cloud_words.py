import urllib
import struct
import sys
import os
import codecs
import time

def rc(x):
    start = 0
    for c in x:
        start ^= ord(c)
    return chr(start)
    
def serial_keys(keys):    
    token = '\x00\x05\x00\x00\x00\x00\x01'
    total_len = len(token) + len(keys) + 3
    data = ''.join([chr(total_len), token, chr(len(keys)), keys])
    return data + rc(data)

def key_from_serial(data):
    token = '\x00\x05\x00\x00\x00\x00\x01'
    total_len = ord(data[0])
    key_len = total_len - len(token) - 3
    keys = data[-1 - key_len :-1]
    return keys

def open_sogou(keys, durtot=0, version='3.7'):
    url = 'http://shouji.sogou.com/web_ime/mobile.php?durtot=%(durtot)d&h=000000000000000&r=store_mf_wandoujia&v=%(version)s' % vars()  
    data = serial_keys(keys)
    return urllib.urlopen(url, data)

def get_base_url(durtot=0, version='3.7'):
    return 'http://shouji.sogou.com/web_ime/mobile.php?durtot=%(durtot)d&h=000000000000000&r=store_mf_wandoujia&v=%(version)s' % vars()
        
def parse_result(result):
    words = []
    if ord(result[0]) + 2 != len(result):
        print 'Error: invalid size'
        return words

    num_words = struct.unpack('<H', result[0x12 : 0x12+2])[0]
    if num_words == 0 or num_words > 32:
        print 'Warning: strange words num', num_words

    print num_words
    # data packet start at 0x14
    pos = 0x14
    for i in xrange(num_words):
        str_len = struct.unpack('<H', result[pos : pos+2])[0]
        if str_len == 0 or str_len > 0xFF:
            raise ValueError(result)            
        pos += 2
        if str_len == 0:
            continue
        word = result[pos : pos+str_len].decode('utf-16-le')
        try:
            word.encode('gb18030')
        except:
            print 'Warning: word %s cant encode to gb18030' % repr(word)

        words.append(word)
        
        # str itself    
        pos += str_len
        # unknown part, like 0x12c, 0x12b, etc
        str_len = struct.unpack('<H', result[pos : pos+2])[0]
        pos += str_len + 2
        # unknown part, like 0x01, 0x2, 0x03, 0x04, 0x05 etc
        str_len = struct.unpack('<H', result[pos : pos+2])[0]
        pos += str_len + 2 + 1

    if pos != len(result):
        print 'Warning: buffer not exhausted!'
        
    return words
    
def get_cloud_words(keys):
    res = open_sogou(keys)
    if res.code != 200:
        print 'Error: invalid response for input <%s>' % keys
        return []

    result = res.read()
    return parse_result(result)

# #####################################################################
if __name__ == "__main__":
    matched_list = get_cloud_words('4346')
    if matched_list:
        for matched_word in matched_list:
            print matched_word
