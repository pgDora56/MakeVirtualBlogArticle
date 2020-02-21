# -*- coding: utf-8 -*-
import MeCab, re, glob, random


output = ""

# I try to use snake_case...
class Word:
    def __init__(self, deep, maxi):
        self.deep = deep
        self.count = 0
        self.nexts = {}
        self.MAXI_CHAIN = maxi

    def add(self, words):
        self.count += 1
        if len(words) < 1: return
        if len(words) < self.MAXI_CHAIN - self.deep - 1:
            # print(f"{len(words)}/{self.MAXI_CHAIN}/{self.deep} -> {words}") 
            return 
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

    def pick(self):
        r = random.randrange(self.count)
        cnt = 0
        for k, n in self.nexts.items():
            cnt += n.count
            # print(f"{cnt} -> {r}/{self.count}")
            if r < cnt:
                # print(f"HIT")
                return k
        raise Exception("Tree Counter is broken.")

class MarkovTree:
    def __init__(self, maxi = 3):
        self.root = Word(-1, maxi)
        self.MAXI_CHAIN = maxi

    def add_tree(self, data):
        lines = data.split("\n")
        words = ["[START]"]
        for line in lines:
            words.extend(self.separate(line))
            if words[-1].startswith("NEW LINE-"):
                n = int(words[-1].split("-")[1])
                words[-1] = f"NEW LINE-{n+1}"
            else:
                words.append("NEW LINE-1")
        words[-1] = "[END]"
        self.make_chain(words)

    def make_chain(self, words_list):
        for i in range(len(words_list)):
            self.root.add(words_list[i:])

    def separate(self, data):
        m = MeCab.Tagger().parse(data)
        lines = m.split("\n")
        words = []
        for line in lines:
            words.append((re.split('[\t,]', line)[0]))
        for _ in range(2): words.pop() # 最後の謎の空白2こを削除
        return words
    
    def create(self, files):
        for path in files:
            with open(path, encoding = "utf-8") as f:
                s = f.read()
                s = self.cut_unneccesarry(s)
                s = self.replace_spletters(s)
                self.add_tree(s)

    def cut_unneccesarry(self, s):
        s = re.sub("---+[\s\S]---+", "", s)
        s = re.sub("(http|https)://([\w\-]+\.)+[\w\-]+(/[\w\-./?%&=]*)?", "", s)
        return s

    def replace_spletters(self, data):
        data = data.replace("&lt;", "<")
        data = data.replace("&gt;", ">")
        data = data.replace("&amp;", "&")
        data = data.replace("&quot;", '"')
        data = data.replace("&#39;", "'")
        data = data.replace("&nbsp;", " ")
        return data


if __name__ == "__main__":
    tree = MarkovTree()
    files = glob.glob("output/417/*.txt")
    tree.create(files)

    with open("output3.txt", mode = "w", encoding = "utf-8") as f2:
        f2.write(tree.root.show())

