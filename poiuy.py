from ftplib import FTP
import os
import cv2
import time

MAX_RETRIES = 3

def upload_folder_to_ftp(local_folder, server_address, username, password, remote_folder):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Connect to the FTP server
            ftp = FTP(server_address)
            ftp.login(username, password)

            # Change to the desired remote directory
            ftp.cwd(remote_folder)

            # Upload each file in the local folder
            local_filepath = os.path.join(local_folder).replace("\\", "/")
            with open(file = local_filepath, mode = 'rb') as file:
                ftp.storbinary(f'STOR a.jpg', file)

            # Close the FTP connection
            ftp.quit()
            print("Upload successful.")
            break
        
        except Exception as e:
            retries += 1
            print(f"Error: {e}")
            print(f"Retrying... ({retries}/{MAX_RETRIES})")

# Example usage
local_folder_path = 'C:/Users/user/Desktop/mdp html/camera.jpg'
server_address = 'uws7-032.cafe24.com'
username = 'imminho'
password = 'mu3102!!'
remote_folder_path = '/www/image/'
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
while(1):
    time.sleep(0.3)
    ret, frame = cap.read()
    cv2.imwrite('C:/Users/user/Desktop/mdp html/camera.jpg', frame)
    upload_folder_to_ftp(local_folder_path, server_address, username, password, remote_folder_path)
cap.release()
