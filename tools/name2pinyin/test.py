#coding:utf-8
import sys
from name2pinyin import Name2Pinyin

name2pinyin = Name2Pinyin()

def test_name2pinyin(full_name):
    full_name_pinyin_list = name2pinyin.name2pinyin(full_name)
    return full_name_pinyin_list

HELP = '''
USAGE:  name2pinyin full_name
'''
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print HELP
        sys.exit(0)

    args = [item for item in sys.argv[1:]]

    if args[0] in ['-h', '-help']:
        print HELP

    if args[0] == 'name2pinyin':
        if args[1].strip():
            print test_name2pinyin(args[1])
        else:
            print 'full_name is null'
    else:
        print HELP
