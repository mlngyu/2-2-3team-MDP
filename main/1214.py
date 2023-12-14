import cv2
import torch
import threading
import queue
import mysql.connector

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
    threshold = 0.6
    high_confidence_indices = confidences > threshold
    objectnumber = int(len(results.xyxy[0][high_confidence_indices]))
    insert_query = "INSERT INTO test VALUES (%s,0)"
    delete_query = "DELETE FROM test LIMIT 1"
    cursor.execute(delete_query)
    cursor.execute(insert_query, (str(objectnumber),))
    connection.commit()
    print('send')

# Database information
host = '183.111.138.176'
user = 'imminho'
password = 'mu3102!!'
database = 'imminho'

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/user/Downloads/best.pt', force_reload=True)
# Open video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
cursor = connection.cursor()
# Create a thread for processing frames
while(1):
    processing_thread = threading.Thread(target=process_frames)

    # Start the processing thread
    processing_thread.start()

    processing_thread.join()

# Release resources
cap.release()
# cv2.destroyAllWindows()
cursor.close()
connection.close()
