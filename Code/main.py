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
from math import cos, sin, atan
from random import randint
import sys
import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports

PORT_NAME = '/dev/cu.usbmodem1413101'
BAUD_RATE = 115200
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


def start_serial():
    """
    This starts the serial communication for the decided port.

    return (Serial): the serial connection to the specified port,
    """
    serial_com = None
    my_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    for ports in my_ports:
        print(ports)
        if PORT_NAME in ports[0]:
            serial_com = serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE,
                                       timeout=1)
            if serial_com.isOpen():
                serial_com.close()
            serial_com.open()
    if not serial_com:
        print("Serial port not found")
    return serial_com


def convert_coords_to_pixels(hand_lms, image):
    """
    Convert each of the co-ordinates for every landmark to pixel
    positions

    Parameter:
        hand_lms (list): list containing x, y, z  of finger points
        image (array): array containing content about the image

    return (list): list containing the finger points in pixels
    """
    hands_list = []
    for _i, hand_landmarks in enumerate(hand_lms):
        hand_container = []
        for _idx, landmark in enumerate(hand_landmarks.landmark):
            height, width, _coordinate = image.shape
            c_x, c_y = int(landmark.x * width), int(landmark.y * height)
            hand_container.append((c_x, c_y))
        hands_list.append(hand_container)
    return order_hands(hands_list)


def wrist_position(hand):
    """

    Parameter:
        hand (list): contains tuple that has each joints co-ordinates

    return (int): int value relating to the wrist x-position
    """
    return hand[0][0]


def order_hands(hand_list):
    """
    This orders the hand in the order they appear from left to right. This is
    done by comparing the x-values of each hand's wrist.

    Parameter:
        hand_list (list): list containing the finger points in pixels

    return (list): hand_list ordered with hands from left to right
    """
    return sorted(hand_list, key=wrist_position, reverse=False)


def draw_points(hand_list, image, hand_colour):
    """
    This draws the circles above each of the hand landmarks

    parameter:
        hand_list (list): list containing the finger points in pixels
        image (array): array containing content about the image
        hand_colour (dict): contains tuples that have three ints from 0-255

    return:
    """
    for index, hand in enumerate(hand_list):
        colour = hand_colour[index]
        for point in hand:
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
    returned_finger_list = []
    for hand in hand_list:
        finger_list = finger_position_relative_to_focal_point(
            hand, THUMB_COORD, thumb=True)
        finger_list += finger_position_relative_to_focal_point(
            hand, FINGER_COORD, thumb=False)
        returned_finger_list.append(determine_thumb_position(hand,
                                                             finger_list))
    return returned_finger_list


def is_hand_sideways(hand_list):
    """
    The hand is counted as sideways or downwards if the thumb MCP or pinky
    MCP joint is below the wrist. In terms of pixels if their y-position is
    greater than the wrist it will be counted as sideways or downwards.

    Parameter:
        hand_list (list): tuple containing the joints coords

    return (list): booleans relating to if the hand is sideways/downwards
    """
    hand_sideways = []
    for hand in hand_list:
        wrist_y = hand[0][1]
        thumb_y = hand[2][1]
        pinky_y = hand[17][1]
        if pinky_y > wrist_y or thumb_y > wrist_y:
            hand_sideways.append(True)
        else:
            hand_sideways.append(False)
    return hand_sideways


def find_num_of_sideways_hands(hand_index, hand_sideways, hand_tot):
    """

    Parameter
        hand_index (int): number of the hand being processed
        hand_sideways (list):  booleans relating to if the hand is
                               sideways/downwards
        hand_tot (int): total number of hands on the screen

    return (int): number of hands sideways indexed after the current hand
    """
    if hand_index != hand_tot - 1:
        num_of_hands_sideways = hand_sideways[hand_index + 1:].count(True)
    else:
        num_of_hands_sideways = hand_index
    return num_of_hands_sideways


def finger_counter(finger_list, hand_sideways):
    """
    Returns the number of fingers/thumbs that are up.
    Additionally, it calculates the binary representation if each finger is a
    binary digit.
    The counter also starts from the leftmost hand to the right.
    Leftmost finger on screen is 2**(5*tot_num_hands). Rightmost is 2**0

    Parameter:
        finger_list (list): list containing the x or y points of the joints
        hand_sideways (list): booleans relating to if the hand is
                              sideways/downwards

    return (tuple): Number of fingers up, binary count
    """
    binary = 0
    decimal = 0
    hand_tot = len(finger_list)
    for hand_index, hand in enumerate(finger_list):
        num_of_hands_sideways = find_num_of_sideways_hands(hand_index,
                                                           hand_sideways,
                                                           hand_tot)
        finger_tot = len(hand)  # In most circumstance it is 5
        exponent = ((hand_tot - num_of_hands_sideways) * finger_tot) - 1
        for finger_index, finger in enumerate(hand):
            finger_tip = finger[0]
            finger_joint = finger[1]
            if finger_tip > finger_joint:
                if not hand_sideways[hand_index]:
                    binary += 2**(exponent - finger_index)
                decimal += 1
    return decimal, binary


def calculate_hand_angle(hand):
    """
    This calculates the angle of the hand using the wrist position and the
    middle finger's MCP joint. By using arc-tan, the angle can be calculated
    as the x and y values can be treated as the adjacent and opposite values.
    The angle and then a simple boolean of the orientation of the had is
    returned.

    Parameter:
        hand (list): list containing tuples of the x and y pos of each joint

    return (tuple): Angle of the hand, boolean if the hand is downwards,
                    and if it is pointing towards the left.
    """
    x_len = hand[0][0] - hand[9][0]
    y_len = hand[0][1] - hand[9][1]
    hand_downwards = False
    hand_leftwards = False
    if y_len < 0:
        hand_downwards = True
    if x_len > 0:
        hand_leftwards = True

    angle = 0 if y_len == 0 else atan(x_len/abs(y_len))
    return angle, hand_downwards, hand_leftwards


def print_hand_number(image, hand_list, hand_sideways, count_decimal):
    """
    This prints the number of the hand beneath it. With the largest index
    appearing on the leftmost hand and the smallest index appearing on the
    rightmost hand.

    Parameter:
        image (ndarray): array used to represent the image
        hand_list (list): list containing the finger points in pixels
        hand_sideways (list): booleans relating to if the hand is
                              sideways/downwards
        count_decimal (bool): determines if it is counting in decimal

    return: None
    """
    for index, hand in enumerate(hand_list):
        angle, hand_downwards, hand_leftwards = calculate_hand_angle(hand)

        multiplier = (
            sin(angle) / 2.5 if hand_leftwards else sin(angle) * 1.2,  # x-pos
            -1 / 2 * cos(angle) if hand_downwards else cos(angle)  # y-pos
        )
        wrist = (hand[0][0], hand[0][1])
        if count_decimal:
            text = str(len(hand_list) - index)
        else:
            num_of_hands_sideways = find_num_of_sideways_hands(index,
                                                               hand_sideways,
                                                               len(hand_list))
            text = (None if hand_sideways[index] else
                    str(len(hand_list) - num_of_hands_sideways))
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 5, 5)
        text_place = (
            int(wrist[0] + (multiplier[0] * text_size[1])),  # x-pos
            int(wrist[1] + (multiplier[1] * text_size[0][0]))  # y-pos
        )
        cv2.putText(image, text, text_place,
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)


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


def display_text(image, num_vals, count_decimal, serial_com):
    """
    This puts the text on the image for when it is shown.

    Parameter:
        image (ndarray): array used to represent the image
        num_vals (list): contains decimal, binary, last printed val and type
        count_decimal (bool): determines if it is counting in decimal
        serial_com (Serial): the serial connection to the specified port

    return: None
    """
    if count_decimal:
        count_str = "Decimal"
        display_number = num_vals[0]
    else:
        count_str = "Binary"
        display_number = num_vals[1]
    cv2.putText(image, str(display_number), (150, 150),
                cv2.FONT_HERSHEY_PLAIN, 12, (0, 255, 0), 12)
    cv2.putText(image, f"Counting in {count_str}", (150, 200),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    if serial_com and (display_number != num_vals[2] or
                       count_str != num_vals[3]):
        serial_com.write(f'{count_str}:\n'.encode('ascii'))
        serial_com.write(f'{display_number}\n'.encode('ascii'))
        num_vals[2] = display_number
        num_vals[3] = count_str


def main():
    """
    This is the main function of the program. It starts the camera and checks
    there is a valid camera that can be used. It then processes the image to
    find the landmarks. The landmarks and then used for the logic to see if
    the fingers are up or down.

    return:
    """
    success, image, cap = start_camera()
    serial_com = start_serial()
    count_decimal = True

    while success:
        # Grab the image and convert to RGB. Following this, identifying if
        # there are any hand landmarks.
        success, image = cap.read()
        image = cv2.flip(image, flipCode=1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = HANDS.process(rgb_image)
        multi_land_marks = results.multi_hand_landmarks
        num_vals = [0, 0, -1, ""]  # decimal, binary and previous printed val

        if multi_land_marks:
            for hand_num, _hand in enumerate(multi_land_marks):

                if hand_num not in hand_dict:
                    hand_dict[hand_num] = (randint(0, 255), randint(0, 255),
                                           randint(0, 255))
                MP_DRAW.draw_landmarks(image, multi_land_marks[hand_num],
                                       MP_HANDS.HAND_CONNECTIONS)

            hand_list = convert_coords_to_pixels(multi_land_marks, image)
            hand_sideways = is_hand_sideways(hand_list)
            draw_points(hand_list, image, hand_dict)
            finger_list = collect_finger_points(hand_list)
            num_vals[0], num_vals[1] = finger_counter(finger_list,
                                                      hand_sideways)
            print_hand_number(image, hand_list, hand_sideways, count_decimal)

        count_decimal, success = keyboard_input(count_decimal, success)
        display_text(image, num_vals, count_decimal, serial_com)
        cv2.imshow("Counting number of fingers", image)

    cap.release()
    cv2.destroyAllWindows()
    serial_com.close()


if __name__ == "__main__":
    main()
