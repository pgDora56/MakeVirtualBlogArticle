# -*- coding: utf-8 -*-
import MeCab, re, glob


output = ""

# I try to use snake_case...
class Word:
    def __init__(self, deep, maxi):
        self.deep = deep
        self.count = 0
        self.nexts = {}
        self.MAXI_CHAIN = maxi

    def add(self, words):
        if len(words) < self.MAXI_CHAIN - self.deep:
            return 
        self.count += 1
        w = words.pop(0)
        if self.deep < self.MAXI_CHAIN - 1:
            if not w in self.nexts:
                self.nexts[w] = Word(self.deep+1, self.MAXI_CHAIN)
            self.nexts[w].add(words)

    def show(self):
        text = ""
        for w in self.nexts:
            blank = ""
            for _ in range(self.deep): blank += "  "
            text += blank + w + "[" + str(self.nexts[w].deep) + " / " + str(self.nexts[w].count) + "]"
            if self.deep < self.MAXI_CHAIN - 1:
                text += " -> " + self.nexts[w].show() + "\n"
        return text

class MarkovTree:
    def __init__(self, maxi = 3):
        self.root = Word(-1, maxi)
        self.MAXI_CHAIN = maxi

    def add_tree(self, data):
        words = self.separate(data)
        self.make_chain(words)

    def make_chain(self, words_list):
        words_list.insert(0, "[START]") # 最初にMARKを入れる
        words_list.pop() # 最後の謎の空白を削除
        words_list[-1] = "[END]" # 最後のMARKを入れる
        for i in range(len(words_list)-self.MAXI_CHAIN):
            self.root.add(words_list[i:])

    def separate(self, data):
        m = MeCab.Tagger().parse(data)
        lines = m.split("\n")
        words = []
        for line in lines:
            words.append((re.split('[\t,]', line)[0]))
        return words

if __name__ == "__main__":
    tree = MarkovTree()
    files = glob.glob("output/417/*.txt")
    for path in files:
        with open(path, encoding = "utf-8") as f:
            s = f.read()
            tree.add_tree(s)
    with open("output3.txt", mode = "w", encoding = "utf-8") as f2:
        f2.write(tree.root.show())

