import time
from train import main 

node = [2, 4, 8, 16, 32, 64]
node_a = [2, 4, 8]


for i in node:
    for j in node:
        for q in node:
            start = time.time()
            main(i,j,q)
            end = time.time()
            print(end-start)
