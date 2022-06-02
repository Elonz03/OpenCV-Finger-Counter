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
from random import randint
import sys
import cv2
import mediapipe as mp


FINGER_COORD = [(8, 6), (12, 10), (16, 14), (20, 18)]
THUMB_COORD = [(4, 5), ]  # Thumb tip and index MCP
MP_DRAW = mp.solutions.drawing_utils  # Used to draw the hands
MP_HANDS = mp.solutions.hands  # Used to detect hands in the input image
HANDS = MP_HANDS.Hands(max_num_hands=2)  # Used to process the detected hands
hand_dict = {}


def start_camera():
    """
    This checks if there is a camera that can be used locally. If not it closes
    the program.

    return (tuple): contains - bool, array and address to camera
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        sys.exit()
    success, image = cap.read()
    return success, image, cap


def convert_coords_to_pixels(hand_lms, hand_list, image):
    """
    Convert each of the co-ordinates for every landmark to pixel
    positions

    Parameter:
        hand_lms (list): list containing x, y, z  of finger points
        hand_list (list): list containing the finger points in pixels
        image (array): array containing content about the image

    return (list): list containing the finger points in pixels
    """
    for _idx, landmark in enumerate(hand_lms.landmark):
        height, width, _coordinate = image.shape
        c_x, c_y = int(landmark.x * width), int(landmark.y * height)
        hand_list.append((c_x, c_y))
    return hand_list


def draw_points(hand_list, image, colour):
    """
    This draws the circles above each of the hand landmarks

    parameter:
        hand_list (list): list containing the finger points in pixels
        image (array): array containing content about the image
        colour (tuple): contains three ints from 0-255

    return:
    """
    for point in hand_list:
        cv2.circle(image, point, 10, colour, cv2.FILLED)


def finger_position_relative_to_focal_point(hand_list, finger_coord,
                                            thumb=False):
    """

    hand_list (list): list containing the finger points in pixels
    finger_coord (list): contains tuple containing the indices that are
                         compared for the fingers/thumb.
    thumb (bool): used to indicate if the thumb coord is passed in

    return (list): contains the x/y value relative to the focal point
    """
    if thumb:
        focal_index = 17  # pinky MCP
    else:
        focal_index = 0  # wrist
    focal_x_pos = hand_list[focal_index][0]
    focal_y_pos = hand_list[focal_index][1]
    normalised_fingers_pos = []
    for coordinate in finger_coord:
        finger_pos = []
        for finger_point in coordinate:
            x_pos = hand_list[finger_point][0]
            y_pos = hand_list[finger_point][1]
            x_len = focal_x_pos - x_pos
            y_len = focal_y_pos - y_pos
            if abs(y_len) > abs(x_len):
                finger_pos.append(abs(y_len))
            else:
                finger_pos.append(abs(x_len))
        normalised_fingers_pos.append(finger_pos)
    return normalised_fingers_pos


def determine_thumb_position(hand_list, finger_list):
    """
    Determines the order of the list. When given the list the thumb is the
    first item on the list. But, if the thumb is on the right side of the
    hand (from user facing the screen), then the list needs to be reversed.

    Parameter:
        hand_list (list): tuple containing the joints coords
        finger_list (list): list containing the x or y points of the joints

    return (list): list of fingers points in order from left to right of the
    screen
    """
    wrist = hand_list[0][0]
    thumb_knuckle = hand_list[1][0]
    if thumb_knuckle > wrist:
        finger_list.reverse()
    return finger_list


def collect_finger_points(hand_list):
    """
    This creates the finger_list based on the data from hand_list and the
    FINGER_COORD and THUMB_COORD. It creates the list so the thumb is in the
    0th index and then goes from index to pinky. Finally, it checks the
    position of the thumb and will reverse the list if the thumb is on the
    right side.

    Parameter:
        hand_list (list): tuple containing the joints coords

    return (list): contains list containing the x or y values relative to the
                   focal point
    """
    finger_list = finger_position_relative_to_focal_point(
        hand_list, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hand_list, FINGER_COORD, thumb=False)

    return determine_thumb_position(hand_list, finger_list)


def finger_counter(finger_list, hand_num, tot_num_of_hands, decimal, binary):
    """
    Returns the number of fingers/thumbs that are up.
    Additionally, it calculates the binary representation if each finger is a
    binary digit.
    The counter also starts from the leftmost hand to the right.
    Leftmost finger on screen is 2**(5*tot_num_hands). Rightmost is 2**0

    Parameter:
        finger_list (list): list containing the x or y points of the joints
        hand_num (int): number of the hand that is being counted
        tot_num_of_hands (int): total number of hands on screen
        decimal (int): current total number of fingers counted
        binary (int): current total of binary number represented

    return (tuple): Number of fingers up, binary count
    """
    binary_exponent = ((tot_num_of_hands - hand_num) * 5) - 1
    for finger in finger_list:
        finger_tip = finger[0]
        finger_joint = finger[1]

        if finger_tip > finger_joint:
            binary += 2**binary_exponent
            decimal += 1
        binary_exponent -= 1
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
    """
    This is the main function of the program. It starts the camera and checks
    there is a valid camera that can be used. It then processes the image to
    find the landmarks. The landmarks and then used for the logic to see if
    the fingers are up or down.

    return:
    """
    success, image, cap = start_camera()

    count_decimal = True

    while success:
        # Grab the image and convert to RGB. Following this, identifying if
        # there are any hand landmarks.
        success, image = cap.read()
        image = cv2.flip(image, flipCode=1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = HANDS.process(rgb_image)
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
                MP_DRAW.draw_landmarks(image, hand_lms,
                                       MP_HANDS.HAND_CONNECTIONS)
                hand_list = convert_coords_to_pixels(hand_lms, hand_list,
                                                     image)
                draw_points(hand_list, image, colour)
                finger_list = collect_finger_points(hand_list)
                decimal, binary = finger_counter(finger_list, hand_num,
                                                 tot_num_of_hands, decimal,
                                                 binary)
        count_decimal, success = keyboard_input(count_decimal, success)
        display_text(image, decimal, binary, count_decimal)

        cv2.imshow("Counting number of fingers", image)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
