import datetime

import cv2
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    img_dir = "static/imgs/"
    if request.method == 'GET': img_path=None
    elif request.method == 'POST':
        #### POSTにより受け取った画像を読み込む
        stream = request.files['img'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        #### グレースケール化
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #### 現在時刻を名前として「imgs/」に保存する
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        img_path = img_dir + dt_now + ".jpg"
        cv2.imwrite(img_path, img)
    #### 保存した画像ファイルのpathをHTMLに渡す
    return render_template('index.html', img_path=img_path) 

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=8888)