import glob
from Markov import MarkovTree

tree = MarkovTree()
files = glob.glob("output/417/*.txt")
tree.create(files)

lis = []

fst = "[START]"
tree.root.nexts[fst].show()
snd = tree.root.nexts[fst].pick()
lis.append(snd)

while snd != "[END]":
    newsnd = tree.root.nexts[fst].nexts[snd].pick()
    lis.append(newsnd)
    fst = snd
    snd = newsnd

lis.pop()

with open("output.dat", mode = "w", encoding = "utf-8") as f2:
    f2.write(''.join(lis))

