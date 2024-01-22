import cv2
import time
from functions import send_mail, clean_folder
import glob
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    # Process delta of frames
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Apply threshold to change in black white output
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # get contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # plot frame around found contours
    for contour in contours:
        # threshold
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_obj = all_images[index]

    # update status list
    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)

    # check for sending out mail
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_mail, args=(image_with_obj, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
clean_thread.start()
