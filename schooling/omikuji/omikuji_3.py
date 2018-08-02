# if文を追加して大吉しか出ない10連おみくじに変える

import random
kuji = ["大吉", "中吉", "小吉", "凶"]
for i in range(10):
    godbox = random.randint(0, 3)
    if(kuji[godbox] != "大吉"):
        godbox = 0
        print(kuji[godbox])
    else:
        print(kuji[godbox])
