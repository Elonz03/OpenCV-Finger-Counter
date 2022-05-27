from main import finger_count, THUMB_COORD, FINGER_COORD

HAND_NUM = 0  # This is one hand, but its index is 0
TOT_NUM_HANDS = 1

# Fingers pointing upwards
LEFT_THUMB_DOWN = [580, 600]
RIGHT_THUMB_DOWN = [600, 580]  # tip of thumb left / thumb joint x positions

HAND_UP_ALL_FINGERS_UP_THUMB_LEFT = [
    [728, 600], [631, 560], [555, 480], [504, 412], [447, 380], [640, 343],
    [624, 247], [617, 188], [612, 135], [704, 333], [714, 221], [721, 152],
    [725, 96], [760, 348], [781, 246], [792, 183], [797, 128], [811, 381],
    [847, 314], [865, 269], [875, 227]
]

HAND_UP_ALL_FINGERS_UP_THUMB_RIGHT = [
    [419, 597], [502, 580], [569, 535], [621, 501], [668, 493], [520, 420],
    [542, 348], [553, 306], [563, 268], [473, 406], [483, 324], [490, 275],
    [496, 234], [428, 408], [434, 333], [442, 290], [451, 252], [381, 424],
    [376, 366], [377, 330], [382, 297]
]

# Fingers pointing downwards


def test_counting_function_hand_upwards_all_fingers_up_thumb_right():
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb right is from the perspective of the user to the device.

    return: None
    """
    thumb_left = False
    decimal = 0
    binary = 0

    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD,
                                   HAND_UP_ALL_FINGERS_UP_THUMB_RIGHT,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_upwards_thumb_down_thumb_right():
    """
    All fingers up for one hand, except for the thumb. Should return 4 in
    decimal and 30 in binary.
    Thumb right is from the perspective of the user to the device.

    Thumb joint is indexed as 2 and 4 in hand_list. We care about the x-pos
    for whether it is up of not

    return: None
    """
    thumb_left = False
    decimal = 0
    binary = 0
    hand_list = HAND_UP_ALL_FINGERS_UP_THUMB_RIGHT

    hand_list[THUMB_COORD[0]][0] = RIGHT_THUMB_DOWN[1]
    hand_list[THUMB_COORD[1]][0] = RIGHT_THUMB_DOWN[0]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 30


def test_counting_function_hand_upwards_all_fingers_up_thumb_left():
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb left is from the perspective of the user to the device.

    return: None
    """
    thumb_left = True
    decimal = 0
    binary = 0
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD,
                                   HAND_UP_ALL_FINGERS_UP_THUMB_LEFT,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_upwards_thumb_down_thumb_left():
    """
    All fingers up for one hand, except for the thumb. Should return 4 in
    decimal and 15 in binary.
    Thumb left is from the perspective of the user to the device.

    Thumb joint is indexed as 2 and 4 in hand_list. We care about the x-pos
    for whether it is up of not

    return: None
    """
    thumb_left = True
    decimal = 0
    binary = 0
    hand_list = HAND_UP_ALL_FINGERS_UP_THUMB_LEFT
    hand_list[THUMB_COORD[0]][0] = LEFT_THUMB_DOWN[1]
    hand_list[THUMB_COORD[1]][0] = LEFT_THUMB_DOWN[0]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 15
