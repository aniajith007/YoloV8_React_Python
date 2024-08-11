from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import time

import cv2
from ultralytics import YOLO
import base64

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")
CORS(app)
model = YOLO('yolov8n.pt')

ALLOWED_CLASSES = {''}   # Full capitalized text treated as set in here

def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text

def generate_frames():
    cap = cv2.VideoCapture(0)  # Use 0 for webcam

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Perform object detection
        results = model(frame)
        detections = []
        for result in results:            
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                # detections.append({
                #     'bbox': [x1, y1, x2, y2],
                #     'confidence': conf,
                #     'label': label
                # })     
                
                if label in ALLOWED_CLASSES:
                    # Draw the bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Put label and confidence score
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)                           
                    
                
        # Encode the frame to base64
        encoded_frame = encode_image_to_base64(frame)
        data = {
            'image': encoded_frame        
        }

        socketio.emit("frame",data)
        socketio.sleep(0)
        #time.sleep(0.5)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit("classes",model.names)
    # emit("frame",{'frame': 'your_frame_data_here'})
    socketio.start_background_task(generate_frames)    

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    
@socketio.on('label')
def handle_custom_event(data):
    print('Received data:', data['data'],data['action'])
    # You can process the data here
    # For example, if the data contains an image, you can decode and process it
    # Or if it's some command, you can execute specific logic

    # Optionally, you can emit a response back to the client    
    if data['action'] == 'add':
        ALLOWED_CLASSES.add(data['data'])    
        socketio.emit('response_event', {'message': 'Data added successfully!'})    
    elif data['action'] == 'remove':
        ALLOWED_CLASSES.remove(data['data'])    
        socketio.emit('response_event', {'message': 'Data removed successfully!'})    
    
    print(ALLOWED_CLASSES)

if __name__ == '__main__':
    socketio.run(app, debug=True)
