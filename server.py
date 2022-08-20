import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
# from cv_thread import CvThread

app = Flask(__name__)
app.static_folder = 'static'

# 현재 표시중인 이미지의 번호
i = 0


@app.route('/')
def hello():
    return ("hello")


@app.route('/method')
def method():
    # 이미지 파일 리셋
    filePath = 'static/result'
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
    filePath = 'static/uploaded_imgs'
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)

    # index.html 실행
    return render_template('/index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = 'static/uploaded_imgs'
        file.save(os.path.join(filepath, filename))
        return redirect('/search', code=302)


@app.route('/search')
def search():
    # AI로 비슷한 이미지 찾기
    # 찾은 이미지들을 static/result 폴더에 저장
    return redirect('/result', code=302)


@app.route('/result')
def result():
    # 검색 결과 Render
    global i
    imgs = os.listdir('static/result')

    if len(imgs) == 0:
        return redirect('/method', code=302)
    else:
        search_result = []
        for filename in imgs:
            search_result.append('static/result/'+filename)
        index = open('templates/index.txt', 'r', encoding='utf-8').read()
        source = index.format(search_result[i])
        return source


@app.route('/up')
def up():
    # 이전 이미지로 이동
    if len(os.listdir('static/result')) != 0:
        global i
        if i != 0:
            i = i - 1
        else:
            i = len(os.listdir('static/result'))-1
    return redirect('/result', code=302)


@app.route('/down')
def down():
    # 다음 이미지로 이동
    if len(os.listdir('static/result')) != 0:
        global i
        if i != len(os.listdir('static/result'))-1:
            i = i + 1
        else:
            i = 0
    return redirect('/result', code=302)


if __name__ == '__main__':
    # cv = CvThread()
    # cv.start()
    app.run(port=5000, debug=True)
