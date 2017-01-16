# -*- coding: utf-8 -*-
import nltk
import re
from nltk.parse import DependencyGraph

## Start Example IV.1 (12_3_5_dep_1.py)
def cabocha2depgraph(t):
    dg = DependencyGraph()
    i = 0
    for line in t.splitlines():

        if line.startswith("*"):
            # start of bunsetsu

            cells = line.strip().split(" ", 3)
            m = re.match(r"([\-0-9]*)([ADIP])", cells[2])

            # nltk.parse.DependencyGraphの定義が
            # NLTK 2と3で異なっているので変更している
            #
            # node = dg.nodelist[i]
            node = dg.nodes[i]
            
            node.update(
                {'address': i,
                'rel': m.group(2), # dep_type
                'word': [],
                'tag': []
                })
            dep_parent = int(m.group(1))

            while len(dg.nodes) < i+1 or len(dg.nodes) < dep_parent+1:
                idx = len(dg.nodes) # 新たに追加

                # nltk.parse.DependencyGraph#node['dps']の定義が
                # 異なっていること、属性closedはのちほど使うので
                # 定義変更
                # dg.nodelist.append({'word':[], 'deps':[], 'tag': []})
                dg.nodes[idx].update({'word':[], 'tag': [], 'closed': False})

            if dep_parent == -1:
                dg.root = node
            else:
                # DependencyGraphのメソッドを利用する
                #dg.nodes[dep_parent]['deps'].append(i)
                dg.add_arc(i,dep_parent)
            i += 1
        elif not line.startswith("EOS"):
            # normal morph
            cells = line.strip().split()
            morph = (cells[0], tuple(cells[1].split(',')))
            dg.nodes[i-1]['word'].append(morph[0])
            dg.nodes[i-1]['tag'].append(morph[1])

    return dg

def reset_deps(dg):
    # DependencyGraphの変更にともない修正
    #for node in dg.nodelist:
    for node in dg.nodes.values():

        # node['deps'] = []
        node.update({'deps': nltk.defaultdict(list)})
        
    #dg.root = dg.nodelist[-1]
    dg.root = dg.nodes[len(dg.nodes)-1]

## End Example IV.1 (12_3_5_dep_1.py)

## Start Example IV.2 (12_3_5_dep_2.py)
def set_head_form(dg):
    # DependencyGraphの変更にともない修正
    # for node in dg.nodelist:
    for node in dg.nodes.values():
        tags = node['tag']
        num_morphs = len(tags)

        # extract bhead (主辞) and bform (語形)
        bhead = -1
        bform = -1
        for i in xrange(num_morphs-1, -1, -1):
            if tags[i][0] == u"記号":
                continue
            else:
                if bform == -1: bform = i
                if not (tags[i][0] == u"助詞"
                    or (tags[i][0] == u"動詞" and tags[i][1] == u"非自立")
                    or tags[i][0] == u"助動詞"):
                    if bhead == -1: bhead = i

        node['bhead'] = bhead
        node['bform'] = bform

## End Example IV.2 (12_3_5_dep_2.py)

## Start Example IV.3 (12_3_5_dep_3.py)

NEXT_NODE = 1
NEXT_VERB_NODE = 2
NEXT_NOUN_NODE = 3
def get_dep_type(node):
    bform_tag = node['tag'][node['bform']]
    if bform_tag[0] == u"助詞" and bform_tag[1] == u"格助詞":
        return NEXT_VERB_NODE
    elif bform_tag[0] == u"助動詞" and bform_tag[-1] == u"タ":
        return NEXT_NOUN_NODE
    else:
        return NEXT_NODE

## End Example IV.3 (12_3_5_dep_3.py)

## Start Example IV.4 (12_3_5_dep_4.py)
def analyze_dependency(dg):
    num_nodes = len(dg.nodes)
    for i in xrange(num_nodes-1, 0, -1):
        node = dg.nodes[i]
        if i == num_nodes - 1:                        # ... (1)
            # last node -> to_node = 0
            to_node = 0
        elif i == num_nodes - 2:                      # ... (2)
            # one from the last node -> to_node = num_nodes - 1
            to_node = num_nodes - 1
        else:
            # other nodes
            dep_type = get_dep_type(node)             # ... (3)
            if dep_type == NEXT_NODE:                 # ... (4)
                to_node = i + 1
            elif (dep_type == NEXT_VERB_NODE or
                dep_type == NEXT_NOUN_NODE):          # ... (4)
                for j in xrange(i+1, num_nodes):
                    node_j = dg.nodes[j]
                    node_j_headtag = node_j['tag'][node_j['bhead']]
                    if (node_j['closed'] == False and #original version
                        (dep_type == NEXT_VERB_NODE and node_j_headtag[0] == u"動詞") or
                        (dep_type == NEXT_NOUN_NODE and node_j_headtag[0] == u"名詞" and
                        node_j_headtag[1] != u"形容動詞語幹")):
                        to_node = j
                        break

        node['head'] = to_node
        #dg.nodes[to_node]['deps'].append(i)    # ... (5)
        dg.add_arc(to_node, i)   # ... (5)
        for j in xrange(i+1, to_node):
            dg.nodes[j]['closed'] = True       # ... (6)

## End Example IV.4 (12_3_5_dep_4.py)

## Start Example IV.5 (12_3_5_dep_5.py)
## サンプル文字列のみ

cabocha_result = u'''* 0 7D 0/1 0.000000
太郎 名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー B-PERSON
は 助詞,係助詞,*,*,*,*,は,ハ,ワ O
* 1 2D 0/0 1.468291
この 連体詞,*,*,*,*,*,この,コノ,コノ O
* 2 4D 0/1 0.742535
本 名詞,一般,*,*,*,*,本,ホン,ホン O
を 助詞,格助詞,一般,*,*,*,を,ヲ,ヲ O
* 3 4D 1/2 1.892480
二 名詞,数,*,*,*,*,二,ニ,ニ O
郎 名詞,一般,*,*,*,*,郎,ロウ,ロー O
を 助詞,格助詞,一般,*,*,*,を,ヲ,ヲ O
* 4 6D 0/1 0.702689
見 動詞,自立,*,*,一段,連用形,見る,ミ,ミ O
た 助動詞,*,*,*,特殊・タ,基本形,た,タ,タ O
* 5 6D 0/1 1.193842
きれい 名詞,形容動詞語幹,*,*,*,*,きれい,キレイ,キレイ O
な 助動詞,*,*,*,特殊・ダ,体言接続,だ,ナ,ナ O
* 6 7D 0/1 0.000000
女性 名詞,一般,*,*,*,*,女性,ジョセイ,ジョセイ O
に 助詞,格助詞,一般,*,*,*,に,ニ,ニ O
* 7 -1D 0/1 0.000000
渡し 動詞,自立,*,*,五段・サ行,連用形,渡す,ワタシ,ワタシ O
た 助動詞,*,*,*,特殊・タ,基本形,た,タ,タ O
。 記号,句点,*,*,*,*,。,。,。 O
EOS
'''

## End Example IV.5 (12_3_5_dep_5.py)
