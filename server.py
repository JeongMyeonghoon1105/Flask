import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
#from cv_thread import CvThread

app = Flask(__name__)
app.static_folder = 'static'

i = 0


@app.route('/')
def hello():
    return ("hello")


@app.route('/method')
def method():
    filePath = 'static/result'
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
    filePath = 'static/uploaded_imgs'
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
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
    # AI를 활용해 비슷한 이미지 찾기
    # 찾은 이미지들을 static/result 폴더에 저장
    return redirect('/result', code=302)


@app.route('/result')
def result():
    global i
    imgs = os.listdir('static/result')

    if len(imgs) == 0:
        return redirect('/method', code=302)
    else:
        search_result = []
        for filename in imgs:
            search_result.append('static/result/'+filename)
        index = open('templates/index.txt', 'r').read()
        source = index.format(search_result[i])
        return source


@app.route('/up')
def up():
    if len(os.listdir('static/result')) != 0:
        global i
        if i != 0:
            i = i - 1
        else:
            i = len(os.listdir('static/result'))-1
    return redirect('/result', code=302)


@app.route('/down')
def down():
    if len(os.listdir('static/result')) != 0:
        global i
        if i != len(os.listdir('static/result'))-1:
            i = i + 1
        else:
            i = 0
    return redirect('/result', code=302)


if __name__ == '__main__':
    #cv = CvThread()
    # cv.start()
    app.run(port=5000, debug=True)
