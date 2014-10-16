__author__ = 'wanghuafeng'
from flask import Flask
import simplejson
from N_gram_engin_arithmetic import AliEngineArithmetic

app = Flask(__name__)
ea = AliEngineArithmetic()

@app.route('/<key_input>',methods=['GET', 'POST'])
def get_pinyin(key_input):
    matched_sentence_list = []
    ngram_weight_tuple_list = ea.handle_key_input_str(key_input)
    if ngram_weight_tuple_list:
        for ngram_weight_tuple in ngram_weight_tuple_list:
            matched_sentence_list.append(ngram_weight_tuple[0])
        return simplejson.dumps(matched_sentence_list)
    else:
        return simplejson.dumps([])

if __name__ == "__main__":

    # app.debug = True
    app.run(host='127.0.0.1')