# -*- coding: utf-8 -*-
import MeCab, re, glob

MAXI_CHAIN = 3

output = ""

# I try to use snake_case...
class Word:
    def __init__(self, deep):
        self.deep = deep
        self.count = 0
        self.nexts = {}

    def add(self, words):
        if len(words) < MAXI_CHAIN - self.deep:
            return 
        self.count += 1
        w = words.pop(0)
        if self.deep < MAXI_CHAIN - 1:
            if not w in self.nexts:
                self.nexts[w] = Word(self.deep+1)
            self.nexts[w].add(words)

    def show(self):
        text = ""
        for w in self.nexts:
            blank = ""
            for _ in range(self.deep): blank += "  "
            text += blank + w + "[" + str(self.nexts[w].deep) + " / " + str(self.nexts[w].count) + "]"
            if self.deep < MAXI_CHAIN - 1:
                text += " -> " + self.nexts[w].show() + "\n"
        return text

def Marcov(data):
    words = separate(data)
    make_chain(words)

root = Word(-1)
def make_chain(words_list):
    words_list.insert(0, "[START]") # 最初にMARKを入れる
    words_list.pop() # 最後の謎の空白を削除
    words_list[-1] = "[END]" # 最後のMARKを入れる
    words = {}
    for i in range(len(words_list)-MAXI_CHAIN):
        root.add(words_list[i:])

def separate(data):
    m = MeCab.Tagger().parse(data)
    lines = m.split("\n")
    words = []
    for line in lines:
        words.append((re.split('[\t,]', line)[0]))
    return words

if __name__ == "__main__":
    files = glob.glob("output/417/*.txt")
    for path in files:
        with open(path, encoding = "utf-8") as f:
            s = f.read()
            Marcov(s)
    with open("output2.txt", mode = "w", encoding = "utf-8") as f2:
        f2.write(root.show())

