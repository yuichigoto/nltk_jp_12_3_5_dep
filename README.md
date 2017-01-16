# nltk_jp_12_3_5_dep

## はじめに

このリポジトリは、[NLTK Book](http://www.nltk.org/book/)の日本語訳版である [入門 自然言語処理](https://www.oreilly.co.jp/books/9784873114705/) の[第12章「Python による日本語自然言語処理」](http://www.nltk.org/book-jp/ch12.html)の「12.3.5　係り受け解析」に掲載されているソースコードをNLTK 3対応に書き直したものです。

関連リンクは以下のとおりです。
- [NLTK Book](http://www.nltk.org/book/)
- [第12章「Pythonによる日本語自然言語処理」](http://www.nltk.org/book-jp/ch12.html)：「入門 自然言語処理」の著者である萩原氏が当該部分をWebページとして公開している
-

## 書き直し部分


[「12.3.5　係り受け解析」](http://www.nltk.org/book-jp/ch12.html#id59)にある以下のソースコードを書き直している。
- Example IV.1 (12_3_5_dep_1.py)
- Example IV.2 (12_3_5_dep_2.py
- Example IV.3 (12_3_5_dep_3.py)
- Example IV.4 (12_3_5_dep_4.py)
- Example IV.5 (12_3_5_dep_5.py)

書き直し理由は、NLTK 3.0環境では、上記のソースコードが動かなかったため。理由は、上記のコードで利用されている nltk.parse.dependencygraph の仕様が変わったためだと思われる。そこで、[NLTK 3.0 documentation: nltk.parse.dependencygraph](http://www.nltk.org/_modules/nltk/parse/dependencygraph.html) に基づき、書き直した。

## 確認環境

- RedHat 5 (CentOS 5)
- Python 2.7.12
- NLTK 3.0

## 使用方法

```
% git clone https://github.com/yuichigoto/nltk_jp_12_3_5_dep.git
% cd nltk_jp_12_3_5_dep
% python -i nltk_jp_12_3_5_dep.py
>>> from jp_pp import *
>>> dg = cabocha2depgraph(cabocha_result)
>>> reset_deps(dg)
>>> set_head_form(dg)
>>> analyze_dependency(dg)
>>> print ppo(dg.tree())
([u'渡し', u'た', u'。']
  ([u'女性', u'に']
    ([u'見', u'た']
      ([u'本', u'を'] [u'この'])
      [u'二', u'郎', u'を'])
    [u'きれい', u'な']))

>>> for node in dg.nodes.values():
...   print node['address'], ppo(node['word']), node['deps']
... 
0 [u'太郎', u'は'] defaultdict(<type 'list'>, {u'D': [7]})
1 [u'この'] defaultdict(<type 'list'>, {})
2 [u'本', u'を'] defaultdict(<type 'list'>, {u'D': [1]})
3 [u'二', u'郎', u'を'] defaultdict(<type 'list'>, {})
4 [u'見', u'た'] defaultdict(<type 'list'>, {u'D': [3, 2]})
5 [u'きれい', u'な'] defaultdict(<type 'list'>, {})
6 [u'女性', u'に'] defaultdict(<type 'list'>, {u'D': [5, 4]})
7 [u'渡し', u'た', u'。'] defaultdict(<type 'list'>, {u'D': [6]})
```
