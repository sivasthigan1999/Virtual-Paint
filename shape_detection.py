import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",0,179,empty)
cv2.createTrackbar("Threshold2","Parameters",19,179,empty)
cv2.createTrackbar("areamin","Parameters",0,5000,empty)


def getContours(img,imgcontours):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        areamin = cv2.getTrackbarPos("areamin", "Parameters")
        if area>areamin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            cv2.putText(imgContour,'points'+str(len(approx)),(x + w + 20,y + 20),cv2.FONT_HERSHEY_COMPLEX,0.7
                        ,(255,0,0),2)


            cv2.putText(imgContour, 'area' + str(int(area)), (x + w + 20,y + 45),cv2.FONT_HERSHEY_COMPLEX, 0.7
                        , (0,0,255), 2)


while True:

    _, img = cap.read()
    imgContour = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    Threshold1=cv2.getTrackbarPos("Threshold1","Parameters")
    Threshold2=cv2.getTrackbarPos("Threshold2","Parameters")

    imgCanny = cv2.Canny(imgBlur, Threshold1, Threshold2)
    kernel=np.ones((5,5))
    print(kernel)
    imgdil=cv2.dilate(imgCanny,kernel,iterations=1)
    getContours(imgdil,imgContour)
    #cv2.imshow("original", img)
    #cv2.imshow("Result", imgHSV)



    cv2.imshow("original", img)
    cv2.imshow("imgGray", imgGray)
    cv2.imshow("imgResult", imgCanny)
    cv2.imshow('dilationimage',imgdil)
    cv2.imshow('imgContour', imgContour)
    if cv2.waitKey(1) and 0xFF == ord('q'):

        break