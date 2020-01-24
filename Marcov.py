import MeCab, re

def Marcov(data):
    m = MeCab.Tagger().parse(data)
    lines = m.split("\n")
    words = []
    for line in lines:
        words.append((re.split('[\t,]', line)[0]))
    print(words)

if __name__ == "__main__":
    data = "私達は昨年の９月ににわか君に武蔵境の牛角で焼肉の食べ放題をおごってもらう約束をしました。"

    print(Marcov(data))

