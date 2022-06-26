from logging import exception
import numpy as np
import argparse
import cv2
import signal

from functools import wraps
import errno
import os
import copy
from kivy.logger import Logger

text = 'Hello World'
debug = 'Debug'
state = "STATE"

# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
# fontScale
fontScale = 1
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2


def detect_ball(image , low_color , high_color ):

    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    blur = cv2.GaussianBlur(image_bgr,(5,5),0)
    hsv_frame  = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    hsv_frame = hsv_frame[:600 , :] # y,x
    low_color = np.array(low_color)
    high_color = np.array(high_color)
    mask = cv2.inRange(hsv_frame , low_color , high_color)
    del(hsv_frame)
    contours, hierarchy = cv2.findContours(mask , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    del(mask)

    cv2.putText(image_bgr, debug, (10,600), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(image_bgr, state, (10,650), font, 
                   fontScale, color, thickness, cv2.LINE_AA)

    if not contours:
        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGBA)
        return  (image , (-1,-1 ,-1,-1))
    contours = sorted(contours , key = lambda x:cv2.contourArea(x) , reverse = True)
    

    (x,y,w,h) = cv2.boundingRect(contours[0])
    cv2.rectangle(image_bgr , (x, y) , (x+w , y+h) , (0,0,255) , 2)
    x = x+w//2
    y = y+h//2
        
        
    text = str(x) + " , " + str(y) + " , " + str(w) + " , " + str(h)
    org = (10 , 30)
    cv2.putText(image_bgr, text, org, font, 
                fontScale, color, thickness, cv2.LINE_AA)


    image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGBA)
    return (image , (x,y,w,h) )


def find_color(image):

    Logger.info(f"Image Processing: in color finder" )
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    hsv_frame  = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    crop_img = hsv_frame[10:100, 10:100]
    average = crop_img.mean(axis=0).mean(axis=0)
    cv2.rectangle(image_bgr , (10, 10) , (100 , 100) , (0,0,255) , 2)
    avg_color = str(int(average[0])) +" , " + str(int(average[1])) +" , " + str(int(average[2])) 
    Logger.info(f"Image Processing: im color " + avg_color)
    cv2.putText(image_bgr, avg_color , (10,600), font, 
                   fontScale, color, thickness, cv2.LINE_AA) 
    image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGBA)

    return image

def detect_arm(image , low_color , high_color):
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    blur = cv2.GaussianBlur(image_bgr,(5,5),0)

    cv2.putText(image_bgr, debug, (10,600), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(image_bgr, state, (10,650), font, 
                   fontScale, color, thickness, cv2.LINE_AA)


    hsv_frame  = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    hsv_frames = []
    hsv_frames.append(hsv_frame[390:500 , 230: ])
    hsv_frames.append(hsv_frame[390:500 , :140 ])
    del(hsv_frame)
    low_color = np.array(low_color)
    high_color = np.array(high_color)
    coordinates_list = []
    for i in range(2):
        mask = cv2.inRange(hsv_frames[i] , low_color , high_color)
        contours, hierarchy = cv2.findContours(mask , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
        del(mask)

        if not contours:
            image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGBA)
            return  (image , [(-1,-1 ,-1,-1)])
        contours = sorted(contours , key = lambda x:cv2.contourArea(x) , reverse = True)
        (x,y,w,h) = cv2.boundingRect(contours[0])
        if i == 0:
            x+=230
            y+=390
        if i == 1:
            y+=390
        cv2.rectangle(image_bgr , (x, y) , (x+w , y+h) , (0,0,255) , 2)
        x = x+w//2
        y = y+h//2
        coordinates_list.append((x,y,w,h))
        text = str(x) + " , " + str(y) + " , " + str(w) + " , " + str(h)
        org = (10 , 30) if i == 0 else (10 , 70) ## if 2 countors then will display coordinates one below another
        cv2.putText(image_bgr, text, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    del(hsv_frames)

    cv2.putText(image_bgr, debug, (10,600), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(image_bgr, state, (10,650), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    
            
        
        


    image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGBA)
    return (image , coordinates_list)
