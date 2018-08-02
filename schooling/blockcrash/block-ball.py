# ブロック崩し
from tkinter import *
import random

# ゲーム中で使う変数の一覧
blocks = []
block_size = {"x": 75, "y": 30}
ball = {"dirx": 15, "diry": -15, "x": 350, "y": 300, "w": 10}
bar = {"x": 0, "w": 100}
is_gameover = False
point = 0

# ウィンドウの作成
win = Tk()
cv = Canvas(win, width=600, height=400)
cv.pack()

# ゲームの初期化


def init_game():
    global is_gameover, point
    is_gameover = False
    ball["y"] = 250
    ball["diry"] = -10
    point = 0
    # ブロックを配置する
    for iy in range(0, 5):
        for ix in range(0, 8):
            color = "red"
            if (iy + ix) % 2 == 1:
                color = "blue"
            x1 = 4 + ix * block_size["x"]
            x2 = x1 + block_size["x"]
            y1 = 4 + iy * block_size["y"]
            y2 = y1 + block_size["y"]
            blocks.append([x1, y1, x2, y2, color])
    win.title("START")

# オブジェクトを描画する


def draw_objects():
    cv.delete('all')  # 既存の描画を破棄
    cv.create_rectangle(0, 0, 600, 400, fill="black", width=0)
    # ブロックを一つずつ描画
    for w in blocks:
        x1, y1, x2, y2, c = w
        cv.create_rectangle(x1, y1, x2, y2, fill=c, width=0)
    # ボールを描画
    cv.create_oval(ball["x"] - ball["w"], ball["y"] - ball["w"],
                   ball["x"] + ball["w"], ball["y"] + ball["w"], fill="green")
    # バーを描画
    cv.create_rectangle(bar["x"], 390, bar["x"] + bar["w"], 400,
                        fill="yellow")

# ボールの移動


def move_ball():
    global is_gameover, point
    if is_gameover:
        return
    bx = ball["x"] + ball["dirx"]
    by = ball["y"] + ball["diry"]
    # 上左右の壁に当たった？
    if bx < 0 or bx > 600:
        ball["dirx"] *= -1
    if by < 0:
        ball["diry"] *= -1
    # プレイヤーの操作するバーに当たった？
    if by > 390 and (bar["x"] <= bx <= (bar["x"] + bar["w"])):
        ball["diry"] *= -1
        if random.randint(0, 1) == 0:
            ball["dirx"] *= -1
        by = 380
    # ボールがブロックに当たった？
    hit_i = -1
    for i, w in enumerate(blocks):
        x1, y1, x2, y2, color = w
        w3 = ball["w"] / 3
        if (x1-w3 <= bx <= x2+w3) and (y1-w3 <= by <= y2+w3):
            hit_i = i
            break
    if hit_i >= 0:
        del blocks[hit_i]
        if random.randint(0, 1) == 0:
            ball["dirx"] *= -1
        ball["diry"] *= -1
        point += 10
        win.title("GAME SCORE = " + str(point))
    # ゲームオーバー？
    if by >= 400:
        win.title("Game Over!! score=" + str(point))
        is_gameover = True
    if 0 <= bx <= 600:
        ball["x"] = bx
    if 0 <= by <= 400:
        ball["y"] = by


def game_loop():
    draw_objects()
    move_ball()
    win.after(50, game_loop)

# マウスイベントの処理


def motion(e):  # マウスポインタの移動
    bar["x"] = e.x


def click(e):  # クリックでリスタート
    if is_gameover:
        init_game()


# マウスイベントを登録
win.bind('<Motion>', motion)
win.bind('<Button-1>', click)
# ゲームのメイン処理
init_game()
game_loop()
win.mainloop()
