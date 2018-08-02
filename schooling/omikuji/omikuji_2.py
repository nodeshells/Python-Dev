# for文を追加して10連おみくじに変える

import random
kuji = ["大吉", "中吉", "小吉", "凶"]
for i in range(10):
    godbox = random.randint(0, 3)
    print(kuji[godbox])
