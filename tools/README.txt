usage: slicer [-vocab vocab_file] [-module Module] sentence
1、slicer:
python test.py slicer 文件中训练语言模型
python test.py slicer -module "slice.basic_slicer" 文件中训练语言模型
python test.py slicer -module "slice.basic_weight_slicer" 文件中训练语言模型
python test.py slicer -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" 文件中训练语言模型
python test.py slicer -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" -module "slice.basic_weight_slicer" 文件中训练语言模型

2、word2pinyin
python test.py word2pinyin 文件
python test.py word2pinyin -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" 文件

3、sentence2pinyin
python test.py sentence2pinyin 文件中训练语言模型
python test.py sentence2pinyin -module "slice.basic_slicer" 文件中训练语言模型
python test.py sentence2pinyin -module "slice.basic_weight_slicer" 文件中训练语言模型
python test.py sentence2pinyin -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" 文件中训练语言模型
python test.py sentence2pinyin -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" -module "slice.basic_weight_slicer" 文件中训练语言模型

4、sentence2digits
python test.py sentence2digits 文件中训练语言模型
python test.py sentence2digits -module "slice.basic_slicer" 文件中训练语言模型
python test.py sentence2digits -module "slice.basic_weight_slicer" 文件中训练语言模型
python test.py sentence2digits -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" 文件中训练语言模型
python test.py sentence2digits -vocab "F:\\klm\\tools\\slice\\Cizu_and_singleword_komoxo95K.txt" -module "slice.basic_weight_slicer" 文件中训练语言模型
