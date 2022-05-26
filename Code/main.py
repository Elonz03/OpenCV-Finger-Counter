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

from random import randint

FINGER_COORD = [(8, 6), (12, 10), (16, 14), (20, 18)]
THUMB_COORD = (4, 2)


def convert_coords_to_pixels(hand_lms, hand_list, image):
    # Convert each of the co-ordinates for every landmark to pixel
    # positions
    for idx, lm in enumerate(hand_lms.landmark):
        h, w, c = image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        hand_list.append((cx, cy))
    return hand_list


def draw_points(hand_list, image, colour):
    # Draw the circles for the landmarks
    for point in hand_list:
        cv2.circle(image, point, 10, colour, cv2.FILLED)


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


def finger_count(finger_coord, thumb_coord, hand_list, thumb_left, hand_num,
                 tot_num_of_hands, decimal, binary):
    """
    Returns the number of fingers/thumbs that are up.
    Additionally, it calculates the binary representation if each finger is a
    binary digit.
    The counter also starts from the leftmost hand to the right.
    Leftmost finger on screen is 2**(5*tot_num_hands). Rightmost is 2**0

    Parameter:
        finger_coord (list): tuple containing the finger joints
        thumb_coord (list): tuple containing thumb joints
        hand_list (list): tuple containing the joints coords
        thumb_left (bool): position if thumb is left of wrist
        hand_num (int): number of the hand that is being counted
        tot_num_of_hands (int): total number of hands on screen
        decimal (int): current total number of fingers counted
        binary (int): current total of binary number represented

    return (tuple): Number of fingers up, binary count
    """
    #  Exponent counted from number of hands times fingers minus one as the
    #  last finger is in the position 2**0.
    binary_exponent = ((tot_num_of_hands - hand_num) * 5) - 1
    if thumb_left:
        # TODO: Change logic to account for thumb y position instead of
        #  just x position
        if hand_list[thumb_coord[0]][0] < hand_list[thumb_coord[1]][0]:
            decimal += 1
            binary += 2**binary_exponent
            binary_exponent -= 1

    finger_binary_constant = binary_exponent
    for finger_index in range(len(finger_coord)):
        coordinate = finger_coord[finger_index]
        binary_exponent = finger_binary_constant - finger_index
        if (hand_list[coordinate[0]][1] <
                hand_list[coordinate[1]][1]):
            decimal += 1
            binary += 2**binary_exponent

    if not thumb_left:
        binary_exponent -= 1
        if hand_list[thumb_coord[0]][0] > hand_list[thumb_coord[1]][0]:
            decimal += 1
            binary += 2**binary_exponent
    return decimal, binary


def keyboard_input(count_decimal, success):
    """
    This handles the input from the keyboard

    Parameter:
        count_decimal (bool): Determines if counting in decimal or binary
        success (bool): Determines if program continues
    return (tuple): boolean values
    """
    pressed_key = cv2.waitKey(1)
    if pressed_key == ord('q'):
        success = False
    elif pressed_key == ord('b'):
        count_decimal = False
    elif pressed_key == ord('d'):
        count_decimal = True
    elif pressed_key == ord('t'):
        count_decimal = not count_decimal
    return count_decimal, success


def display_text(image, decimal, binary, count_decimal):
    """
    This puts the text on the image for when it is shown.

    Parameter:
        image (ndarray): array used to represent the image
        decimal (int): decimal representation of fingers that are up
        binary (int): binary number calculated
        count_decimal (bool): determines if it is counting in decimal
    return: None
    """
    if count_decimal:
        count_str = "Decimal"
        display_number = decimal
    else:
        count_str = "Binary"
        display_number = binary
    cv2.putText(image, str(display_number), (150, 150),
                cv2.FONT_HERSHEY_PLAIN, 12, (0, 255, 0), 12)
    cv2.putText(image, f"Counting in {count_str}", (150, 200),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)


def main():
    # Use the web-camera on your device
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    success, image = cap.read()

    mp_hands = mp.solutions.hands  # Used to detect hands in the input image
    hands = mp_hands.Hands(max_num_hands=6)  # Used to process the detected
    # hands
    mp_draw = mp.solutions.drawing_utils  # Used to draw the hands
    hand_dict = {}
    count_decimal = True

    while success:
        # Grab the image and convert to RGB. Following this, identifying if
        # there are any hand landmarks.
        success, image = cap.read()
        image = cv2.flip(image, flipCode=1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)
        multi_land_marks = results.multi_hand_landmarks
        decimal = 0
        binary = 0

        # Nested for loop used to draw each of the landmarks for each hand,
        # if multiple are present
        if multi_land_marks:
            tot_num_of_hands = len(multi_land_marks)
            for hand_num in range(tot_num_of_hands):
                hand_list = []

                if hand_num not in hand_dict:
                    hand_dict[hand_num] = (randint(0, 255), randint(0, 255),
                                           randint(0, 255))
                colour = hand_dict[hand_num]
                hand_lms = multi_land_marks[hand_num]
                mp_draw.draw_landmarks(image, hand_lms,
                                       mp_hands.HAND_CONNECTIONS)
                hand_list = convert_coords_to_pixels(hand_lms, hand_list, image)
                draw_points(hand_list, image, colour)
                thumb_left = determine_thumb_position(hand_list)
                decimal, binary = finger_count(
                    FINGER_COORD, THUMB_COORD, hand_list, thumb_left,
                    hand_num, tot_num_of_hands, decimal, binary)
        count_decimal, success = keyboard_input(count_decimal, success)
        display_text(image, decimal, binary, count_decimal)

        cv2.imshow("Counting number of fingers", image)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
