import cv2
import torch

def get_objectnum():
    return objectnumber

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/user/Downloads/best.pt', force_reload=True)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Error reading frame")
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame)
    confidences = results.xyxy[0][:, 4]
    class_label = results.xyxy[0][:, 5]
    threshold = 0.6
    high_confidence_indices = confidences > threshold
    boxes = results.xyxy[0][high_confidence_indices].cpu().numpy()
    objectnumber = int(len(results.xyxy[0][high_confidence_indices]))
    color = (0, 255, 0) 
    thickness = 2

    for box in boxes:
        start_x, start_y, end_x, end_y, confidence, class_label = box
        cv2.rectangle(frame, (int(start_x), int(start_y)), (int(end_x), int(end_y)), color, thickness)
        label = f'{model.names[int(class_label)]}: {confidence:.2f}'
        cv2.putText(frame, label, (int(start_x), int(start_y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    objectnumber = f'count : {objectnumber}'
    cv2.putText(frame, objectnumber, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('',frame1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
