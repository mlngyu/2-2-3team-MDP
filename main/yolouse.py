import cv2
import torch
import threading
from mdp_send_db import add_data_to_mariadb
import queue

# Define a global variable for object number
objectnumber = 0
frame_queue = queue.Queue()

def get_frame():
    ret, frame = cap.read()
    return ret,frame

# Function to process frames
def process_frames():
    global objectnumber

    ret, frame = get_frame()
    results = model(frame)
    confidences = results.xyxy[0][:, 4]
    class_label = results.xyxy[0][:, 5]
    threshold = 0.7
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
    frame_queue.put(frame)


# Database information
db_host = "127.0.0.1"
db_user = "root"
db_password = "root"
db_name = "snow_life"

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/user/Downloads/best.pt', force_reload=True)
# Open video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create a thread for processing frames
while(1):
    processing_thread = threading.Thread(target=process_frames)

    # Start the processing thread
    processing_thread.start()

    # Main thread continues to do other tasks if needed
    # ...
    try:
        frame = frame_queue.get(timeout=1)  # 필요에 따라 타임아웃 값 조정
        cv2.imshow('', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print('q')
            break  # 'q' 키를 누르면 루프를 종료함
    except queue.Empty:
        pass

    processing_thread.join()

    # Wait for the processing thread to finish (optional)

# Release resources
cap.release()
cv2.destroyAllWindows()
