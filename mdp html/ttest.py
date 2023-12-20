import cv2
cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)
while(1):
    ret, frame = cap.read()
    cv2.imshow('', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        print('q')
        break  # 'q' 키를 누르면 루프를 종료함
cap.release()