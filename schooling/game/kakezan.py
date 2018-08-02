from random import randint
import time
import math

tokuten = 0
start = time.time()

for i in range(10):
    kazu1 = randint(1, 10)
    kazu2 = randint(1, 10)
    print(kazu1, " x ", kazu2, " = ", end="")
    kotae = int(input())
    if kotae == kazu1 * kazu2:
        tokuten = tokuten + 1

print(f"とくてん＝ {tokuten * 10} 点です")
finish = time.time()
print(f"けいかじかん:{math.floor(finish - start)}びょうでした")
