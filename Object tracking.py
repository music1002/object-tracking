import cv2
import os
from os.path import isfile,join
import matplotlib.pyplot as plt

def convert_frame_to_video(pathIn,pathOut,fps):
    frame_array=[]
    files= [f for f in sorted(os.listdir(pathIn)) if isfile(join(pathIn, f))]
    
    for f in range(len(files)-1):
        filename=os.path.join(pathIn, files[f])
        img=cv2.imread(filename)
        height,width,_ =img.shape
        assert img.shape[:2]==(height,width)
        frame_array.append(img)

    fourcc=cv2.VideoWriter_fourcc(*"MJPG")    
    out=cv2.VideoWriter(pathOut,fourcc,fps,(width,height),True)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
       
    out.release()
convert_frame_to_video("Ball_Dataset","ball_video.avi" , 25)

first_frame="Ball_Dataset/00000001.jpg"
x=200
y=110
w=50
h=50
roi=cv2.imread(first_frame)[y:y+h,x:x+w]
plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))


roi=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
roi_hist=cv2.calcHist([roi],[0],None,[180],[0,180])
#print(roi_hist)

vid= cv2.VideoCapture("ball_video.avi")
ret= True
i=0
while True:
    ret,frame= vid.read()
    if not ret:
        print(i)
        print("Video Broken")
        break
    i+=1
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    term_criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)
    mask=cv2.calcBackProject([hsv], [0], roi_hist, [0,180],1)
    _,trackWindow = cv2.meanShift(mask, (x,y,w,h), term_criteria)
    x,y,w,h= trackWindow
    cv2.rectangle(frame, (x+w,y+h),(x,y),(0,255,0),2)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.show()
    
    