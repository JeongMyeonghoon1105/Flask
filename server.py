from flask import Flask, render_template
#from cv_thread import CvThread

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def hello():
    return("hello")

@app.route('/method')
def method():
    return render_template('/index.html')

if __name__ == '__main__':
    #cv = CvThread()
    #cv.start()
    app.run(port=5000, debug=True)