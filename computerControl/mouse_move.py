import pyautogui
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

screenWidth, secreenHeight = pyautogui.size()
before_index_X, before_index_Y = 0, 0
click_flag = False
mouse_down_flag = True

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      continue

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        hands_points = { 
            'wrist': hand_landmarks.landmark[0],
            'thumb': [x for x in hand_landmarks.landmark[1:5]],
            'index': [x for x in hand_landmarks.landmark[5:9]],
            'middle': [x for x in hand_landmarks.landmark[9:13]],
            'ring': [x for x in hand_landmarks.landmark[13:17]],
            'pinky': [x for x in hand_landmarks.landmark[17:21]]
        }

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        between = ((hands_points['index'][-1].x-hands_points['middle'][-1].x)**2 + (hands_points['index'][-1].y-hands_points['middle'][-1].y)**2)**0.5

        if between < 0.05 and (hands_points['index'][2].y > hands_points['index'][3].y):
            if before_index_X == 0 and before_index_Y == 0:
                before_index_X = hands_points['index'][3].x * screenWidth
                before_index_Y = hands_points['index'][3].y * secreenHeight
            
            currentMouseX, currentMouseY = pyautogui.position()

            move_X = hands_points['index'][3].x * screenWidth - before_index_X
            move_Y = hands_points['index'][3].y * secreenHeight - before_index_Y
            
            temp = hands_points['middle'][-1].x - hands_points['index'][-1].x
            if mouse_down_flag and temp < 0:
              mouse_down_flag = False
              pyautogui.mouseDown()
            else: 
              pyautogui.mouseUp()
              mouse_down_flag = True

            if pyautogui.onScreen(currentMouseX + move_X, currentMouseY + move_Y):
              pyautogui.moveTo(currentMouseX + move_X, currentMouseY + move_Y)

            before_index_X = hands_points['index'][3].x * screenWidth
            before_index_Y = hands_points['index'][3].y * secreenHeight

            if hands_points['index'][0].x > hands_points['thumb'][3].x : click_flag = True
            if click_flag and (hands_points['index'][0].x < hands_points['thumb'][3].x):
                pyautogui.click(currentMouseX, currentMouseY, 1, 1)
                click_flag = False
            
        else:
            before_index_X, before_index_Y = 0, 0
            click_flag = False
    

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

    

cap.release()

# pyautogui.onScreen(currentMouseX, currentMouseY)