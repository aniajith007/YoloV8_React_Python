import cv2
from ultralytics import YOLO

# Load a YOLOv8 model (e.g., yolov8n, yolov8s, yolov8m, yolov8l, yolov8x)
model = YOLO('yolov8n.pt')  # yolov8n is the Nano model, you can choose other models as well

# Open the video capture (0 for webcam or provide a video file path)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)  # You can also use model.predict(frame)
    
    # To View What it contains : 
    
    # print("In Results : ",results[0].boxes)
    # box = results[0].boxes[0]
    # x1,y1,x2,y2 = map(int, box.xyxy[0])
    # conf = box.conf[0]  # Confidence score
    # cls = int(box.cls[0])  # Class label (integer)
    # print("Printing labels from model : ",model.names) # Model.names is a dict
    # print("Co-Ordinates : ",x1,y1,x2,y2,"conf score : ",conf,"Label : ",model.names[cls] )    
    # break
    
    # Iterate over detected objects and draw bounding boxes
    # print(results[1].boxes)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Extract coordinates and confidence score
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            cls = int(box.cls[0])  # Class label (integer)
            print(conf)
            # Draw the bounding box on the frame
            # Restricted By other classes and conf score
            if(cls==0 and conf>=0.80):                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)                
            if(cls==0 and conf>=0.80):                
                label = f'{model.names[cls]}: {conf:.2f}'
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with detections
    cv2.imshow('YOLOv8 Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()