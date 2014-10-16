__author__ = 'wanghuafeng'
#coding:utf-8

from sentence2digits import *
from sentence2pinyin import *
from word2pinyin import *
from slice.slicer_base import *

def slicer_base(sentence, module_name='slice.basic_slicer', vocab_file=None):
    slicer = SlicerBase.fromName(module_name, vocab_file)
    sliced_words_list = slicer.slice(sentence)
    return ' '.join(sliced_words_list).encode('gbk')

def word2pinyin(sentence, vocab_file=None):
    w2p = Word2Pinyin(vocab_file=vocab_file)
    return w2p.word2pinyin(sentence)

def sentence2pinyin(sentence, module_name='slice.basic_slicer', vocab_file=None):
    options_dic = {'slicerModule':module_name, 'vocab_file':vocab_file}
    sp = Sentence2Pinyin(options_dic)
    return sp.sentence2pinyin(sentence)

def sentence2digits(sentence, module_name='slice.basic_slicer', vocab_file=None):
    options_dic = {'slicerModule':module_name, 'vocab_file':vocab_file}
    sd = Sentence2Digits(options_dic)
    return sd.sentence2digits(sentence)

# OPTION_DIC = {'-basic_slicer':slicer_base, '-basic_weight_slicer':slicer_base, '-word2pinyin':word2pinyin, '-sentence2pinyin':sentence2pinyin, '-sentence2digits':sentence2digits}
#
HELP = """usage: slicer [-vocab vocab_file] [-module Module] sentence
  """
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print HELP
        sys.exit(0)

    base_word_filename = None
    args = [item for item in sys.argv[1:]]

    if args[0] in ['-h', '-help']:
        print HELP

    if args[0] == 'slicer':
        if len(args) == 6:
            if args[1] == '-vocab' and os.path.isfile(args[2]):
                if args[3] == '-module' and args[4] in ['slice.basic_slicer', 'slice.basic_weight_slicer']:
                    sentence = args[5]
                    if sentence:
                        print slicer_base(sentence, module_name=args[4], vocab_file=args[2])
                    else:
                        print 'sentence is null.'
                else:
                    print 'no such module name. Please check.'
            else:
                print 'base_word_list file does not exists.'
        if len(args) == 4:
            if args[1] == '-module' and args[2] in ['slice.basic_slicer', 'slice.basic_weight_slicer']:
                sentence = args[3]
                if sentence:
                    print slicer_base(sentence, module_name=args[2])
                else:
                    print 'sentence is null.'

            elif args[1] == '-vocab' and os.path.isfile(args[2]):
                sentence = args[3]
                if sentence:
                    print slicer_base(sentence, vocab_file=args[2])
                else:
                    print 'sentence is null.'

        if len(args) == 2:
            sentence = args[1]
            if sentence:
                print slicer_base(sentence)
            else:
                print 'sentence is null.'

    if args[0] == 'word2pinyin':
        if len(args) == 4:
            if args[1] == '-vocab' and os.path.isfile(args[2]):
                sentence = args[3]
                if sentence:
                    print word2pinyin(sentence, vocab_file=args[2])
                else:
                    print 'sentence is null.'
            else:
                print 'base_word_list file does not exists.'
        if len(args) == 2:
            sentence = args[1]
            if sentence:
                print word2pinyin(sentence)
            else:
                print 'sentence is null.'

    if args[0] == 'sentence2pinyin':
        if len(args) == 6:
            if args[1] == '-vocab' and os.path.isfile(args[2]):
                if args[3] == '-module' and args[4] in ['slice.basic_slicer', 'slice.basic_weight_slicer']:
                    sentence = args[5]
                    if sentence:
                        print sentence2pinyin(sentence, module_name=args[4], vocab_file=args[2])
                    else:
                        print 'sentence is null.'
                else:
                    print 'no such module name. Please check.'
            else:
                print 'wrong option(-vocab) or base_word_list file does not exists.'
        if len(args) == 4:
            if args[1] == '-module' and args[2] in ['slice.basic_slicer', 'slice.basic_weight_slicer']:
                sentence = args[3]
                if sentence:
                    print sentence2pinyin(sentence, module_name=args[2])
                else:
                    print 'sentence is null.'
            elif args[1] == '-vocab' and os.path.isfile(args[2]):
                sentence = args[3]
                if sentence:
                    print sentence2pinyin(sentence, vocab_file=args[2])
                else:
                    print 'sentence is null.'

        if len(args) == 2:
            sentence = args[1]
            if sentence:
                print sentence2pinyin(sentence)
            else:
                print 'sentence is null.'
    if args[0] == 'sentence2digits':
        if len(args) == 6:
            if args[1] == '-vocab' and os.path.isfile(args[2]):
                if args[3] == '-module' and args[4] in ['slice.basic_slicer', 'slice.basic_weight_slicer']:
                    sentence = args[5]
                    if sentence:
                        print sentence2digits(sentence, module_name=args[4], vocab_file=args[2])
                    else:
                        print 'sentence is null.'
                else:
                    print 'no such module name. Please check.'
            else:
                print 'base_word_list file does not exists.'
        if len(args) == 4:
            if args[1] == '-module' and args[2] in ['slice.basic_slicer', 'slice.basic_weight_slicer']:
                sentence = args[3]
                if sentence:
                    print sentence2digits(sentence, module_name=args[2])
                else:
                    print 'sentence is null.'
            elif args[1] == '-vocab' and os.path.isfile(args[2]):
                sentence = args[3]
                if sentence:
                    print sentence2digits(sentence, vocab_file=args[2])
                else:
                    print 'sentence is null.'
        if len(args) == 2:
            sentence = args[1]
            if sentence:
                print sentence2digits(sentence)
            else:
                print 'sentence is null.'

