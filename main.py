import glob
import time
from Markov import MarkovTree

print("Start")

t = time.time()
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
    m = ""
    for l in lis:
        if l.startswith("NEW LINE-"):
            n = int(l.split("-")[1])
            for _ in range(n): m += "\n"
        else:
            m += l
    f2.write(m)
    
print(f"End: {time.time() - t}")
