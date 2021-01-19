# virtual_mouse
control your mouse movements ,clicking , and dragging with your hand

this is a yolo2 implemented on darkflow to detect 3 hands gestures that controls the mouse movement , clicking , and dragging 

it takes the label midpoint coordinate and use it for controlling the mouse with the pyinput library

to run the code :

1- first download the knectv2 yolo master folder from this repository https://github.com/valdivj/KinectV2_YOLO and install all the requirements


2- replace kinect_yolo.py with my virmouse.py


3- open virmouse.py , and go to line 40 and change the ip webcam to your ip , or change it to '0' to use your webcam


3- put yolov2-fist-palm-click.cfg inside the cfg folder


4- download the weights file from https://drive.google.com/file/d/1PPAmlFkbxx8M3aDoXCgGhTQejmOsf3ST/view?usp=sharing


5- create bin folder and put the weights file in it


6- open cmd or anaconda in KinectV2_YOLO-master path 


7- run the command python virmouse
