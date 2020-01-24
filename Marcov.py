import MeCab, re

MAXI_CHAIN = 3

# I try to use snake_case...
class Word:
    def __init__(self, deep):
        self.deep = deep
        self.count = 0
        self.nexts = {}

    def add(self, words):
        if len(words) < MAXI_CHAIN - self.deep:
            return 
        w = words[0]
        if not w in self.nexts:
            self.nexts[w] = Word(self.deep+1)
        self.nexts[w].count += 1
        if self.nexts[w].deep < MAXI_CHAIN:
            self.nexts[w].add(words[1:])

    def show(self):
        for w in self.nexts:
            blank = ""
            for _ in range(self.deep): blank += "\t"
            print(blank + w)
            self.nexts[w].show()

def Marcov(data):
    words = separate(data)
    make_chain(words)

def make_chain(words_list):
    words_list.insert(0, "[START]") # 最初にMARKを入れる
    words_list.pop() # 最後の謎の空白を削除
    words_list[-1] = "[END]" # 最後のMARKを入れる
    words = {}
    root = Word(0)
    for i in range(len(words_list)-MAXI_CHAIN):
        root.add(words_list[i:])
    root.show()
    


def separate(data):
    m = MeCab.Tagger().parse(data)
    lines = m.split("\n")
    words = []
    for line in lines:
        words.append((re.split('[\t,]', line)[0]))
    return words

if __name__ == "__main__":
    data = "私達は昨年の９月ににわか君に武蔵境の牛角で焼肉の食べ放題をおごってもらう約束をしました。"

    Marcov(data)

