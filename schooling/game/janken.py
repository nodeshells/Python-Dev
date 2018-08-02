import random

dlc = {"a": "グー", "b": "チョキ", "c": "パー"}

draw = "DRAW"
win = "あなたの勝ちです！!"
lose = "あなたの負けです!!"


user_co = 0
pc_co = 0
judge = 0

i = 1
while (user_co + pc_co) < 3:
    if judge == win or judge == lose:
        print(u"じゃーんけーん")
    else:
        print(u"あーいこーで")
    print(u"a=グー b=チョキ c=パー aかbかcを入力")
    user = input('>>>  ')

    user_choice = user.lower()
    try:
        user_choice = dlc[user]
    except:
        print("aかbかcを入力してください。")
        continue
    pc = dlc[str(random.choice("abc"))]

    if user_choice == pc:
        judge = draw
    else:
        if user_choice == "グー":
            if pc == "":
                judge = win
            else:
                judge = lose
        elif user_choice == "チョキ":
            if pc == "パー":
                judge = win
            else:
                judge = lose
        else:
            if pc == u"グー":
                judge = win
            else:
                judge = lose
    if judge == win:
        user_co += 1
    elif judge == lose:
        pc_co += 1
    print(u"あなたが選んだのは %s" % user_choice)
    print(u"コンピューターが選んだのは %s" % pc)
    print((u"%d戦目の結果は%s") % (i, judge))
    print(u"")

    i += 1

if user_co >= pc_co:
    print(u"%d勝%d敗であなたの勝ちです" % (user_co, pc_co))
else:
    print(u"%d勝%d敗であなたの負けです" % (user_co, pc_co))
