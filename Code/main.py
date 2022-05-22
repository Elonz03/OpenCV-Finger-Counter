"""
This project was coded following the steps outlined in:
https://www.section.io/engineering-education/creating-a-finger-counter/#introduction
"""
import cv2
import mediapipe as mp

# Use the web-camera on your device
cap = cv2.VideoCapture(0)

mp_Hands = mp.solutions.hands  # Used to detect hands in the input image
hands = mp_Hands.Hands()  # Used to process the detected hands
mpDraw = mp.solutions.drawing_utils  # Used to draw the hands
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4, 2)

while True:
    # Grab the image and convert to RGB. Following this, identifying if there
    # are any hand landmarks.
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    # Nested for loop used to draw each of the landmarks for each hand,
    # if multiple are present
    if multiLandMarks:
        handList = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            # Convert each of the co-ordinates for every landmark to pixel
            # positions
            for idx, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))
            # Draw the circles for the landmarks
            for point in handList:
                cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)
            upCount = 0
            for coordinate in finger_Coord:
                if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                    upCount += 1
            if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
                upCount += 1
            cv2.putText(image, str(upCount), (150, 150), cv2.FONT_HERSHEY_PLAIN,
                        12, (0, 255, 0), 12)
        cv2.imshow("Counting number of fingers", image)
        cv2.waitKey(1)
