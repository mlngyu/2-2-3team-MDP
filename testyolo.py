import cv2
import torch
import threading
import requests
import numpy as np
from mdp_send_db import add_data_to_mariadb

# Define a global variable for object number
objectnumber = 0
server_url = 'http://imminho.cafe24.com/image/a.jpg'
def get_objectnum():
    return objectnumber

# Function to process frames
def process_frames():
    global objectnumber

    while True:

        response = requests.get(server_url)
        if response.status_code == 200:
            # Convert the response content to a numpy array
            image_data = np.frombuffer(response.content, dtype=np.uint8)

            # Decode the image using OpenCV
            img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model(frame)
        confidences = results.xyxy[0][:, 4]
        class_label = results.xyxy[0][:, 5]
        threshold = 0.6
        high_confidence_indices = confidences > threshold
        boxes = results.xyxy[0][high_confidence_indices].cpu().numpy()
        objectnumber = int(len(results.xyxy[0][high_confidence_indices]))
        add_data_to_mariadb(db_host, db_user, db_password, db_name, str(objectnumber))
        color = (0, 255, 0)
        thickness = 2

        for box in boxes:
            start_x, start_y, end_x, end_y, confidence, class_label = box
            cv2.rectangle(frame, (int(start_x), int(start_y)), (int(end_x), int(end_y)), color, thickness)
            label = f'{model.names[int(class_label)]}: {confidence:.2f}'
            cv2.putText(frame, label, (int(start_x), int(start_y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

        objectnumber_s = f'count : {objectnumber}'
        cv2.putText(frame, objectnumber_s, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('', frame1)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Database information
db_host = "127.0.0.1"
db_user = "root"
db_password = "root"
db_name = "snow_life"

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/user/Downloads/best.pt', force_reload=True)
model = model
# Open video capture

# Create a thread for processing frames
processing_thread = threading.Thread(target=process_frames)

# Start the processing thread
processing_thread.start()

# Main thread continues to do other tasks if needed
# ...

# Wait for the processing thread to finish (optional)
processing_thread.join()

# Release resources
cv2.destroyAllWindows()