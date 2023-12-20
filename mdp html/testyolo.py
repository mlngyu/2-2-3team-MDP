import cv2
from ultralytics import YOLO
import threading
import mysql.connector
import numpy as np
import queue

# Define a global variable for object number
objectnumber = 0
frame_queue = queue.Queue()
num = 0

def get_frame():
    ret, frame = cap.read()
    frame = cv2.flip(frame,0)
    return ret,frame

def process_frames():
    global objectnumber
    global num

    ret, frame = get_frame()
    results = model(frame,conf=0.5)
    bbox = results[0].boxes.xyxy
    confidences = results[0].boxes.conf
    boxes = np.array(bbox)
    objectnumber = len(bbox)
    insert_query = "INSERT INTO test VALUES (%s,0, %s)"
    delete_query = "DELETE FROM test ORDER BY number ASC LIMIT 1;"
    cursor.execute(delete_query)
    cursor.execute(insert_query, (str(objectnumber),str(num)))
    connection.commit()
    num += 1
    color = (0, 255, 0)
    thickness = 2
    i = 0
    for box in boxes:
        start_x, start_y, end_x, end_y = box
        confidence = confidences[i]
        i += 1
        cv2.rectangle(frame, (int(start_x), int(start_y)), (int(end_x), int(end_y)), color, thickness)
        label = f'rabit: {confidence:.2f}'
        cv2.putText(frame, label, (int(start_x), int(start_y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    objectnumber_s = f'count : {objectnumber}'
    cv2.putText(frame, objectnumber_s, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
    frame_queue.put(frame)

# Database information
host = '183.111.138.176'
user = 'imminho'
password = 'mu3102!!'
database = 'imminho'

# Load YOLOv5 model
model = YOLO("C:/Users/user/Downloads/best6.pt")
cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
cursor = connection.cursor()
insert_query = "INSERT INTO test VALUES (0,0,0)"
delete_query = "DELETE FROM test"
cursor.execute(delete_query)
cursor.execute(insert_query)
cursor.execute(insert_query)
cursor.execute(insert_query)
connection.commit()
# Create a thread for processing frames
while(1):
    processing_thread = threading.Thread(target=process_frames)

    # Start the processing thread
    processing_thread.start()
    try:
        frame = frame_queue.get(timeout=1)  # 필요에 따라 타임아웃 값 조정
        cv2.imshow('', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print('q')
            break  # 'q' 키를 누르면 루프를 종료함
    except queue.Empty:
        pass

    processing_thread.join()

# Release resources
cap.release()
# cv2.destroyAllWindows()
cursor.close()
connection.close()