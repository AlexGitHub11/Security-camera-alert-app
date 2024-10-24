import cv2
import time
from send_mail import send

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []

while True:

    status = 0

    # Capture frames and apply gray scale and blur
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)


    # Get first frame for comparison
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Identify movement
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("Vidio", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Ignore FP and highlight movement
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame,(x, y), (x+w, y+h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1

    # Call send function when movement leaves frame
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send()

    cv2.imshow("vidio", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
