import requests
import numpy as np
import cv2
# ftp://imminho.cafe24.com/www/image/KakaoTalk_20231018_130914644.jpg

# server_url = 'http://localhost:5000/uploads/image.jpg'  # Replace with the actual filename
server_url = 'http://imminho.cafe24.com/image/a.jpg'  # Replace with the actual filename

response = requests.get(server_url)

if response.status_code == 200:
    # Convert the response content to a numpy array
    image_data = np.frombuffer(response.content, dtype=np.uint8)

    # Decode the image using OpenCV
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # Display the image using OpenCV
    cv2.imshow('Received Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print('Image received successfully')
else:
    print(f'Failed to retrieve image. Status code: {response.status_code}')