import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
#from cv_thread import CvThread

app = Flask(__name__)
app.static_folder = 'static'


@app.route('/')
def hello():
    return ("hello")


@app.route('/method')
def method():
    return render_template('/index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = 'static/uploaded_imgs'
        file.save(os.path.join(filepath, filename))
        return method()


if __name__ == '__main__':
    #cv = CvThread()
    # cv.start()
    app.run(port=5000, debug=True)
