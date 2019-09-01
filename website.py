from flask import Flask, render_template, Response,url_for,redirect
from camera_pi import Camera
import Maincode4

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html',name=name)

@app.route('/videostop')
def stop():
    return redirect(url_for('index.'))

@app.route('/video')
def video():
    """Video streaming home page."""
    return render_template('video.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/exec')
def parse(name=None):
    Maincode4.recog()
    print("done")
    return redirect(url_for('index'))

def run():
    app.run(host='192.168.137.124',port=5550)
    
if __name__ == '__main__':
    run()
    
    