import cv2
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import autopy
import time
import math

hCam, wCam = 640, 480
cTime, pTime = 0, 0
detector = htm.handDetector(maxHands= 1)
wScr, hScr = autopy.screen.size()
frameR = 100
smoothening = 5
#print(wScr, hScr)


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
plocX, plocY = 0, 0
clocX, clocY  = 0, 0

while True:
    #1. Get the Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #2. Get the tip of the index finger and middle finger
    if (len(lmList) != 0):
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print (x1, y1, x2, y2)


    #3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
    #4. Only index finger: Moving Mode
        if fingers[1]==1 and fingers[2]==0:

    #5. Convert Coordinates
            cv2.rectangle(img, (frameR, frameR), (hCam - frameR,wCam - frameR), (255, 0, 255), 2)
            x3 = np.interp(x1, (frameR, hCam-frameR), (0, wScr))
            y3 = np.interp (y1, (frameR, wCam-frameR), (0, hScr))

    #6. Smoothen Values
            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3 - plocY)/smoothening
    #7. Move Mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

            plocX, plocY = clocX, clocY
    #8. Both Index and Middle fingers are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()
    #9. Find the distance between fingers
    #10. Click mouse if distance is short
    #11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0,0), 3)



    #12. Display
    cv2.imshow("Image",img)
    cv2.waitKey(1)
