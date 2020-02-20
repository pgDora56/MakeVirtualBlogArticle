import MeCab

with open(r"output\417\001.txt", encoding="utf-8") as f:
    s = f.read()
    m = MeCab.Tagger().parse(s)
    print(m)

