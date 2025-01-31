import pandas as panda
import cv2
import time as t
from datetime import datetime

initialState = None

motionTracklist = [None, None]

motionTime = []

dataFrame = panda.DataFrame(columns=["Initial", "Final"])

video = cv2.VideoCapture(0)

while True:
    check, current_frame = video.read()

    var_motion = 0
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    gray_frame = cv2.GaussianBlur(gray, (21, 21), 0)

    if initialState is None:
        initialState = gray_frame
        continue

    differ = cv2.absdiff(initialState, gray_frame)

    thresh_frame = cv2.threshold(differ, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cont,_ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cur in cont:
        if cv2.contourArea(cur)<10000:
            continue
        var_motion = 1
        (cur_x, cur_y, cur_w, cur_h) = cv2.boundingRect(cur)

        cv2.rectangle(current_frame, (cur_x, cur_y), (cur_x + cur_w, cur_y + cur_h), (0, 255, 0), 3)

    motionTracklist.append(var_motion)
    motionTracklist = motionTracklist[-2:]

    if motionTracklist[-1] == 1 and motionTracklist[-2] == 0:
        motionTime.append(datetime.now())

    cv2.imshow("Gray Frame Capture", gray_frame)
    cv2.imshow("Static and Current Frame", differ)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colour Frame", current_frame)

    wait_key = cv2.waitKey(1)

    if wait_key == ord('m'):
        if var_motion == 1:
            motionTime.append(datetime.now())
        break

for a in range(0, len(motionTime), 2):
    dataFrame = dataFrame.append({"Initial" : t[a], "Final" : motionTime[a + 1]}, ignore_index=True)

dataFrame.to_csv("Movement.csv")

video.release()
cv2.destroyAllWindows()