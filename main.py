#!usr/bin/python3
# main.py

from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)
#web page
page="""
<html>
<head>
<title>Video Streaming Demonstration</title>
</head>
<body>
<h1>Video Streaming Demonstration</h1>
<img id="bg" src="{{ url_for('0.0.0.0:5000/video_feed') }}" style="width:500px;height:600;">
</body>
</html>
"""
@app.route('/')

def index():
	return page
        #return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	#return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace;boundary=frame')

 	return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace;boundary=frame')
@app.route('/face')
def face():
	import cv2
	import numpy as np

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
	cap=cv2.VideoCapture(0)
	while True:
		status,frame=cap.read()
		grayimg=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(grayimg,1.15,5)
		for (x,y,w,h) in  faces:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
			roi_gray=grayimg[y:y+h,x:x+w]
			roi_color=frame[y:y+h,x:x+w]
		# showing current image
		cv2.imshow("current image",frame)
		if cv2.waitKey (1) & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()
	cap.release()
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
