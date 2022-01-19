import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

"""camera parameters"""
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
"""set the parameters of width and height of cam, 
based on propID, 3 for width and 4 for height"""
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

"""use the class from the module"""
detector = htm.handDetector(detectionCon=0.7)

"""the code for getting system volume using pycaw"""
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
"""volume range returns a list with the values of volume, [minVol, maxVol, ...]
Access it using variables"""
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    """find the hands and pass it to img"""
    img = detector.findHands(img)
    """Below code gets a list of positions of all 
    landmark points on the hand. Get the values of thumb and index tip
    from the figure on mediapipe hands website"""
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        """Get the x and y coordinates from the lmList for the points"""
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        """find the center of the line between lm4 and lm8"""
        cx, cy = (x1+x2)//2, (y1+y2)//2

        """Draw bigger circles on thumb and index"""
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        """draw a line between the two dots and a circle for mid-point"""
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        """calculate the length of the line using hypotenuse function"""
        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        """Hand range 50 - 200
        Volume range -96 - 0
        Co-relate the hand range and the volume range using numpy as below"""
        vol = np.interp(length, [50, 230], [minVol, maxVol])
        """volume and volume % for the bar on the image is calculated below"""
        volBar = np.interp(length, [50, 230], [400, 150])
        volPer = np.interp(length, [50, 230], [0, 100])
        print(int(length), vol)
        """this sets the master volume to whatever is indicated by the hands"""
        volume.SetMasterVolumeLevel(vol, None)

        """prints out a circle if length goes below 50"""
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    """creating a volume bar on the image as a visual representation"""
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)

    """code to calculate fps"""
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)