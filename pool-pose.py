import math
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture('side.mp4')
pTime = 0

cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE) 
initelbow = 999999
maxdrop = 0

initialear = 999999
maxhead = 0


with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      break

# Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    
    image_height, image_width, _ = image.shape
    image.flags.writeable = False
    results = holistic.process(image)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            
    rex = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].x 
    rey = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].y 
    
    rwx = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x
    rwy = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y
    
    myrads = math.atan2(rwy - rey, rwx - rex)
    mydegs = math.degrees(myrads)
    mydegs = abs(mydegs)
    mydegs = round(mydegs)
    
    if (initelbow == 999999):
        initelbow = rey
    elbowdrop = rey / initelbow
    #print(elbowdrop)
    elbowpercent = (1 - elbowdrop) * 100
    elbowpercent = round(elbowpercent)
    
    if (elbowpercent < maxdrop):
        maxdrop = elbowpercent
        
    
    eary = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].y 
    if (initialear == 999999):
        initialear = eary
        
    headrop = eary / initialear
    headpercent = (1 - headrop) * 100
    headpercent = round(headpercent)
    
    if (headpercent < maxhead):
        maxhead = headpercent
        
    cv2.putText(image, 'Elbow Angle = ' + str(int(mydegs)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0), 3)
    cv2.putText(image, 'Current Elbow Drop = ' + str(int(elbowpercent)) + '%', (50,100), cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0), 3)
    cv2.putText(image, 'Max Elbow Drop = ' + str(int(maxdrop)) + '%', (50,150), cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0), 3)
    cv2.putText(image, 'Current Head Drop = ' + str(int(headpercent)) + '%', (50,200), cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0), 3)
    cv2.putText(image, 'Max Head Drop = ' + str(int(maxhead)) + '%', (50,250), cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,0,0), 3) 
    
    cv2.imshow("window", image)
     
    #print(mydegs)
    #print(
    #      f'Right Elbow coordinates: ('
    #      f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].x * image_width}, '
    #      f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW].y * image_height})'
    #  )
      
    #print(
    #      f'Right Wrist coordinates: ('
    #      f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x * image_width}, '
    #      f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y * image_height})'
    #  )
      
        
      
    if cv2.waitKey(5) & 0xFF == 27:
      break
      
cap.release()