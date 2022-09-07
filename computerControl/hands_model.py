import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

rate = 0
count = 0
version = ''

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

        key = cv2.waitKey(1)
        if key == ord('s'):
          rate = abs(hands_points['middle'][0].y-hands_points['wrist'].y)+0.01
          between = abs(hands_points['index'][-1].x-hands_points['middle'][-1].x)
          print(rate, between)

        if rate > 0:
          current_rate = abs(hands_points['middle'][0].y-hands_points['wrist'].y)
          current_between = abs(hands_points['index'][-1].x-hands_points['middle'][-1].x)

          if current_between < between*(current_rate/rate):
            # print(hands_points['index'][-1].x, hands_points['middle'][-1].x)
            count += 1
            print(count)
            if count > 40:
              version = 'mouse_move'
              print(version)
          else:
            count = 0

        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

    

cap.release()