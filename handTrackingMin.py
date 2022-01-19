import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
"""below Hands object has the following parameters
def __init__(self,
               static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
Static image mode continues the tracking only if it has a
reasonably high detection confidence. 
"""
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    """hands object uses only rgb objects"""
    results = hands.process(imgRGB)
    """print(results.multi_hand_landmarks)"""

    if(results.multi_hand_landmarks):
        for handLms in results.multi_hand_landmarks:
            """handLms represents a single hand"""
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int (lm.y*h)
                print(id, cx, cy)
                """we get the x and y pixel values of the dots on the image (denoted by ids)"""
                #if id == 0:
                cv2.circle(img, (cx, cy), 10, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            """draw on the image on webcam
            #HAND_CONNECTIONS draws the lines between the dots"""

    """code to calculate and display the fps is below"""
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3,
    (255, 0, 255), 3)
    """code for fps ends"""

    cv2.imshow("Image", img)
    cv2.waitKey(1)