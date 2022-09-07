## 딥러닝을 이용해서 손가락을 인식하여 마우스를 컨트롤하는 프로젝트입니다.
---
👉 사용한 모듈: cv2, mediapipe, pyautogui

👉 사용한 딥러닝: mediapipe-hands https://google.github.io/mediapipe/solutions/hands

---
👉 프로젝트의 기능 (ver. 1): 웹캠에 보이는 손가락을 이용하여 마우스를 움직이고 클릭할 수 있습니다.

---

![image](https://user-images.githubusercontent.com/38881094/188765953-fc8d255c-48f7-43f4-bf5d-5cd18c0bca9a.png)

👉 위의 점들의 간격을 생각하여 계산했습니다.

```
hands_points = { 
            'wrist': hand_landmarks.landmark[0],
            'thumb': [x for x in hand_landmarks.landmark[1:5]],
            'index': [x for x in hand_landmarks.landmark[5:9]],
            'middle': [x for x in hand_landmarks.landmark[9:13]],
            'ring': [x for x in hand_landmarks.landmark[13:17]],
            'pinky': [x for x in hand_landmarks.landmark[17:21]]
        }
```

👉 먼저 각 점들을 기억하기 쉽게 손가락이름으로 지정해놓았습니다.

👉 조건들을 이용하여 마우스를 움직이고 클릭 할 수 있습니다.

---
👉 ver. 1 : 아직 조건문이 미숙하여 약간의 오류가 생김 

-> (next version) 초기 설정을 통해 자주 사용하는 거리를 입력하여 거리를 계산하여 멀리서도 작동하게 바꿀 예정
