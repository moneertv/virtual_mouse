import cv2 ## COPY
from darkflow.net.build import TFNet
import numpy as np
import time
import tensorflow as tf
import math
import pynput
from pynput.mouse import Button, Controller

def stabelize(width,height,x,y):
    print('x: ',x,' and y: ',y)
    i=0
    j=0
    while i<width:
        if x>i and x < i+10:
            x = i
        i+=10
    while j<height:
        if y>j and y < j+10:
            y = j
        j+=10
    return x,y
    
    


config = tf.ConfigProto(log_device_placement=True)
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    options = {
            'model': 'cfg/yolov2-fist-palm-click.cfg',
            'load': 'bin/yolov2-fist-palm-click_last.weights',
            'threshold': 0.6,
            'gpu': 0.7
                    }
    tfnet = TFNet(options)

colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

capture = cv2.VideoCapture('http://192.168.1.15:8080/video')
width  = int(capture .get(3))
height = int(capture .get(4))
mouse=Controller()
one_time_fist = 1
one_time_palm = 1
while True:
    stime = time.time()
    ret, frame = capture.read()    
    if ret:
        results = tfnet.return_predict(frame)        
        length = (len(results))   
        

        if length:
            for color, result in zip(colors, results):
                tl = (result['topleft']['x'], result['topleft']['y'])
                br = (result['bottomright']['x'], result['bottomright']['y'])
                label = result['label']
                x1 = result['topleft']['x']
                y1 = result['topleft']['y']
                x2 = result['bottomright']['x']
                y2 = result['bottomright']['y']
                xm =math.floor(abs(( x1 + ( (x2-x1) / 2 ))-width))
                ym =math.floor( y1 + ( (y2-y1) / 2 ))	
                xm,ym=stabelize(width,height,xm,ym)
                #confidence = result['confidence']
                text = '{}:{}'.format(xm,ym) #label, confidence * 100
                
                frame = cv2.circle(frame, (x1,y1), radius=10, color=(0, 0, 255), thickness=2)
                frame = cv2.circle(frame, (x2,y2), radius=10, color=(0, 255, 0), thickness=2)
                frame = cv2.circle(frame, (xm,ym), radius=10, color=(255, 0, 0), thickness=2)
                frame = cv2.rectangle(frame, tl, br, color, 4)
                frame = cv2.putText(
                    frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)      
               
                
                if label == 'click' and one_time_click == 1:
                    mouse.click(Button.left)                  
                    one_time_click = 0

                   
                if label == 'fist' and one_time_fist == 1: 
                    mouse.press(Button.left) 
                    one_time_fist == 0
                if label == 'fist':   
                    mouse.position = (xm*2,ym*2)    

                if label == 'palm':
                    one_time_click = 1 
                    one_time_fist = 1 
                    mouse.release(Button.left)   
                    mouse.position = (xm*2,ym*2)                                       
                    
        
        cv2.imshow('frame', frame)        
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))

    if cv2.waitKey(1) & 0xFF == ord('q'):        
        capture.release()       
        break
capture.release()
cv2.destroyAllWindows()