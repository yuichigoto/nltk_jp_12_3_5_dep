import re, pprint

# ref http://www.nltk.org/book-jp/ch12.html#id3
def pp(obj):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    str = pp.pformat(obj)
    return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1),16)), str)

# ref http://qiita.com/HirofumiYashima/items/4a5d6f1f0a23e787bc34
def ppo(obj):
    return eval("u'''%s'''" % obj).encode('utf-8')
