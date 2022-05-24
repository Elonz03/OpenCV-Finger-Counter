"""
This project was coded following the steps outlined in:
https://www.section.io/engineering-education/creating-a-finger-counter/#introduction

Hand landmark numbers:
0. WRIST
1. THUMB CMC
2. THUMB MCP
3. THUMB IP
4, THUMB TIP
5. INDEX FINGER MCP
6. INDEX FINGER PIP
7. INDEX FINGER DIP
8. INDEX FINGER TIP
9. MIDDLE FINGER MCP
10. MIDDLE FINGER PIP
11. MIDDLE FINGER DIP
12. MIDDLE FINGER TIP
13. RING FINGER MCP
14. RING FINGER PIP
15. RING FINGER DIP
16. RING FINGER TIP
17. PINKY MCP
18. PINKY PIP
19. PINKY DIP
20. PINKY TIP
"""
import cv2
import mediapipe as mp


def convert_coords_to_pixels(hand_lms, hand_list, image):
    # Convert each of the co-ordinates for every landmark to pixel
    # positions
    for idx, lm in enumerate(hand_lms.landmark):
        h, w, c = image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        hand_list.append((cx, cy))


def draw_points(hand_list, image):
    # Draw the circles for the landmarks
    for point in hand_list:
        cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)


def determine_thumb_position(hand_list):
    """
    Returns true if thumb is left of wrist. Otherwise, false. Using the x
    coord. The thumb is left if the x-pos pixel is less than the wrist x-pos

    Parameter:
        hand_list (list): tuple containing the joints coords

    return (bool): If thumb is left of hand or not
    """
    thumb_left = False
    if hand_list[0][0] > hand_list[1][0]:
        thumb_left = True
    return thumb_left


def finger_count(finger_coord, thumb_coord, hand_list, thumb_left):
    """
    Returns the number of fingers/thumb that is up
    Parameter:
        finger_coord (list): tuple containing the finger joints
        thumb_coord (list): tuple containing thumb joints
        hand_list (list): tuple containing the joints coords
        thumb_left (bool): position if thumb is left of wrist

    return (int): Number of fingers up
    """
    up_count = 0
    for coordinate in finger_coord:
        if (hand_list[coordinate[0]][1] <
                hand_list[coordinate[1]][1]):
            up_count += 1
    # This uses the x-position of thumb. Can be changed in future to consider
    # y-position
    if thumb_left:
        if hand_list[thumb_coord[0]][0] < hand_list[thumb_coord[1]][0]:
            up_count += 1
    else:
        if hand_list[thumb_coord[0]][0] > hand_list[thumb_coord[1]][0]:
            up_count += 1
    return up_count


def main():
    # Use the web-camera on your device
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    success, image = cap.read()

    mp_hands = mp.solutions.hands  # Used to detect hands in the input image
    hands = mp_hands.Hands()  # Used to process the detected hands
    mp_draw = mp.solutions.drawing_utils  # Used to draw the hands
    finger_coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_coord = (4, 2)

    while success:
        # Grab the image and convert to RGB. Following this, identifying if
        # there are any hand landmarks.
        success, image = cap.read()
        image = cv2.flip(image, flipCode=1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)
        multi_land_marks = results.multi_hand_landmarks

        # Nested for loop used to draw each of the landmarks for each hand,
        # if multiple are present
        if multi_land_marks:
            hand_list = []
            for hand_lms in multi_land_marks:
                mp_draw.draw_landmarks(image, hand_lms,
                                       mp_hands.HAND_CONNECTIONS)
                convert_coords_to_pixels(hand_lms, hand_list, image)
                draw_points(hand_list, image)
                thumb_left = determine_thumb_position(hand_list)
                up_count = finger_count(finger_coord, thumb_coord, hand_list,
                                        thumb_left)
                cv2.putText(image, str(up_count), (150, 150),
                            cv2.FONT_HERSHEY_PLAIN,
                            12, (0, 255, 0), 12)
            cv2.imshow("Counting number of fingers", image)
            if cv2.waitKey(1) == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
