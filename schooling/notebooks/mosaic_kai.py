import tkinter as tk
import tkinter.filedialog as fd
import PIL.Image
import PIL.ImageTk
# 機械学習で使うモジュール
import numpy
import cv2
import time

globalfilename = ""
globalmaskfilename = ""

# 画像ファイルを数値リストに変換する


def imageToData(filename):
    global globalfilename
    globalfilename = filename
    grayImage = PIL.Image.open(filename)
    # その画像を表示する
    dispImgae(grayImage)

# リサイズ関数


def resize_image(image, height, width):

    # 元々のサイズを取得
    org_height, org_width = image.shape[:2]

    # 大きい方のサイズに合わせて縮小
    if float(height)/org_height > float(width)/org_width:
        ratio = float(height)/org_height
    else:
        ratio = float(width)/org_width

    # リサイズ
    resized = cv2.resize(image, (int(org_height*ratio), int(org_width*ratio)))

    return resized


# モザイクの生成

def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio,
                       interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

# 指定座標にモザイクをかける


def mosaic_area(src, x, y, width, height, ratio=0.1):
    dst = src.copy()
    dst[y:y + height, x:x +
        width] = mosaic(dst[y:y + height, x:x + width], ratio)
    return dst

# 指定座標にマスクをかぶせる


def mask_area(src, x, y, width, height):
    global globalmaskfilename
    src_image = src.copy()
    size = (height, width)
    srcsize = (300, 300)

    maskimage = cv2.imread(globalmaskfilename, cv2.IMREAD_UNCHANGED)

    # お面をリサイズ
    maskimage = resize_image(maskimage, height, width)

    # BGRAからRGBAへ変換
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    overlay_image_RGBA = cv2.cvtColor(maskimage, cv2.COLOR_BGRA2RGBA)

    # PILに変換
    src_image_PIL = PIL.Image.fromarray(src_image_RGBA)
    overlay_image_PIL = PIL.Image.fromarray(overlay_image_RGBA)

    # 合成のため、RGBAモードに変更
    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')

    # 同じ大きさの透過キャンパスを用意
    tmp = PIL.Image.new('RGBA', src_image_PIL.size, (255, 255, 255, 0))
    # 用意したキャンパスに上書き
    tmp.paste(overlay_image_PIL, (x, y), overlay_image_PIL)
    # オリジナルとキャンパスを合成して保存
    result = PIL.Image.alpha_composite(src_image_PIL, tmp)

    return cv2.cvtColor(numpy.asarray(result), cv2.COLOR_RGBA2BGRA)


def dispImgae(Image):
    img = PIL.ImageTk.PhotoImage(Image.resize((400, 400)))
    imageLabel.configure(image=img)
    imageLabel.image = img
    imageLabel.pack()
    # ↓プログラムが最後まで読まれないと画像が表示されない問題を回避
    root.update_idletasks()


def detectFace(src):
    # カスケードファイルを使用して顔の位置をcv2に割り出させる
    face_cascade_path = 'data/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # 顔の座標を代入
    faces = face_cascade.detectMultiScale(src_gray)
    return faces


def openMaskFile():
    global globalmaskfilename
    globalmaskfilename = fd.askopenfilename()

# ファイルダイアログを開く


def openFile():
    fpath = fd.askopenfilename()
    if fpath:
        # 画像ファイルを読み込んで表示する
        imageToData(fpath)


def startMasking():
    global globalmaskfilename
    global globalfilename
    src = cv2.imread(globalfilename)
    if globalmaskfilename != "":
        # マスクが選択されていたら
        faces = detectFace(src)
        for x, y, w, h in faces:
            print(x, y, w, h)
            dst_face = mask_area(src, x, y, w, h)

        # 顔をモザイク化した画像を書き出し
        cv2.imwrite('data/output/opencv_mask_face.jpg', dst_face)
        # 顔をモザイク化した画像を画面に表示
        outputImage = PIL.Image.open('data/output/opencv_mask_face.jpg')
        # 画像を描写
        dispImgae(outputImage)
    else:
        # マスクが選択されていなかったら
        faces = detectFace(src)
        for x, y, w, h in faces:
            print(x, y, w, h)
            dst_face = mosaic_area(src, x, y, w, h)

        # 顔をモザイク化した画像を書き出し
        cv2.imwrite('data/output/opencv_mosaic_face.jpg', dst_face)
        # 顔をモザイク化した画像を画面に表示
        outputImage = PIL.Image.open('data/output/opencv_mosaic_face.jpg')
        # 画像を描写
        dispImgae(outputImage)


# アプリのウィンドウを作る
root = tk.Tk()
root.geometry("600x600")

btn = tk.Button(root, text="お面をかぶる人のファイルを開く", command=openFile)
btn2 = tk.Button(root, text="お面の画像を開く", command=openMaskFile)
btn3 = tk.Button(root, text="お面を顔に合成する", command=startMasking)
imageLabel = tk.Label()
btn.pack()
btn2.pack()
btn3.pack()
# 予測結果を表示するラベル
textLabel = tk.Label(text="かおにお面をつけます")
textLabel.pack()

tk.mainloop()
