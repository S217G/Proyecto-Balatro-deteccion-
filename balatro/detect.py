import cv2
from ultralytics import YOLO
from flask import Flask, Response
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = YOLO('best.pt')
rtmp_url = "rtmp://rtmp-server:1935/live/balatro"

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(rtmp_url)
    frame_count = 0 
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # PROCESAR SOLO 1 DE CADA 3 CUADROS para liberar a la CPU
        frame_count += 1
        if frame_count % 3 != 0:
            continue

        # Inferencia
        results = model.predict(frame, conf=0.7, iou=0.45, device='cpu', verbose=False)
        annotated_frame = results[0].plot() 
        
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)