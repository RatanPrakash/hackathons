import torch
import cv2, time
import numpy as np
from djitellopy import Tello
from torchvision import models

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained = True)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')

tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()

boxes = []

def tracker(frame, coordinates):
    # x1, y1, x2, y2 = coordinates
    area = (coordinates[1] - coordinates[0]) * (coordinates[3] - coordinates[2])
    # frame_area = (frame.shape[0]) * (frame.shape[1])
    x3_frame = 720 / 3
    y3_frame = 480 / 3

    ##vertical lines
    cv2.line(frame, (int(x3_frame), 0), (int(x3_frame), frame.shape[1]), (255, 0, 0))
    cv2.line(frame, (int(2*x3_frame), 0), (int(2*x3_frame), frame.shape[1]), (255, 0, 0))

    print(area)
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 10
    if coordinates[-2] > x3_frame and coordinates[-2] < 2 * x3_frame:
        print("Object in sight, HOVERING!!")

    elif coordinates[-2] < x3_frame and coordinates[-2]>0:
        print('Rotating LEFT <--')
        yv = -speed

    elif coordinates[-2] > 2 * x3_frame:
        print("Rotating RIGHT -->")
        yv = speed

    # elif coordinates[-2]==0:
    #     print('exceptional case, object NOT in sight')

    if area >= 0.6 and area <0.9:
        print('Object at right distance, Hoveringggg')

    elif area < 500 and area > 0:
        print('TOO FAR, APPROACHING OBJECT')
        fb = speed

    elif area > 500:
        print('TOO CLOSE, MOVING BACK')
        fb = -speed
    # elif area <= 0:
    #     print('exceptional case, probably no object in sight')

    tello.send_rc_control(lr, fb, ud, yv)


## MAINLOOP
tello.takeoff()
time.sleep(1)
while True:
    frame = tello.get_frame_read().frame
    frame = cv2.resize(frame, (720,480))

    cv2.putText(frame, f"Battery : {tello.get_battery()}%", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 1)


    # Object detection code here
    results = model(frame)
    prediction = results.pandas().xyxy[0]
    #      xmin    ymin    xmax   ymax  confidence  class    name
    #  0      1        2      3       4         5        6      7
    try:
        prediction['x_cen'] = (prediction['xmin']+prediction['xmax'])/2
        prediction['y_cen'] = (prediction['ymin']+prediction['ymax'])/2
        xmin =  int(prediction['xmin'][0])
        ymin =  int(prediction['ymin'][0])
        x_max = int(prediction['xmax'][0])
        y_max = int(prediction['ymax'][0])
        y_max = int(prediction['ymax'][0])
        x_cen = int(prediction['x_cen'][0])
        y_cen = int(prediction['y_cen'][0])

        coordinates = (xmin, ymin, x_max, y_max, x_cen, y_cen)    ##tuple of coordinates

        confidence = prediction['confidence'][0]
        class_name = prediction['name'][0]
    except:
        pass

    # Draw a bounding box around the detected object
    try:
        cv2.rectangle(frame, (xmin, ymin), (x_max, y_max), (0,0,0), 2)
        text = "{}: {:.2f}%".format(class_name, confidence * 100)
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (xmin, ymin-text_height-baseline), (xmin+text_width, ymin), (0, 255, 0), -1)
        cv2.putText(frame, text, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.circle(frame, (x_cen,y_cen), 2, (0, 0, 255))
        tracker(frame, coordinates)
    except:
        pass

    ##tracking the object in camera frame 

    cv2.imshow("Tello Video Stream", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # quit the loop if 'q' key is pressed
        break
