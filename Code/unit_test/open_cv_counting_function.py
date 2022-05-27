import pytest

from main import finger_count, THUMB_COORD, FINGER_COORD

HAND_NUM = 0  # This is one hand, but its index is 0
TOT_NUM_HANDS = 1

# Fingers pointing upwards
# HU = Hands upwards
HU_LEFT_THUMB_DOWN = [580, 600]
HU_RIGHT_THUMB_DOWN = [600, 580]  # tip of thumb left / thumb joint x positions
HU_FINGER_DOWN = [330, 280]

# Fingers pointing downwards
# HD = Hands downwards


@pytest.fixture
def hands_up_thumb_left():
    hand_up_all_fingers_up_thumb_left = [
        [728, 600], [631, 560], [555, 480], [504, 412], [447, 380], [640, 343],
        [624, 247], [617, 188], [612, 135], [704, 333], [714, 221], [721, 152],
        [725, 96], [760, 348], [781, 246], [792, 183], [797, 128], [811, 381],
        [847, 314], [865, 269], [875, 227]
    ]
    return hand_up_all_fingers_up_thumb_left


@pytest.fixture
def hands_up_thumb_right():
    hand_up_all_fingers_up_thumb_right = [
        [419, 597], [502, 580], [569, 535], [621, 501], [668, 493], [520, 420],
        [542, 348], [553, 306], [563, 268], [473, 406], [483, 324], [490, 275],
        [496, 234], [428, 408], [434, 333], [442, 290], [451, 252], [381, 424],
        [376, 366], [377, 330], [382, 297]
    ]
    return hand_up_all_fingers_up_thumb_right


def test_counting_function_hand_upwards_all_fingers_up_thumb_right(
        hands_up_thumb_right):
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
                                   hands_up_thumb_right,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_upwards_thumb_down_thumb_right(
        hands_up_thumb_right):
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
    hand_list = hands_up_thumb_right

    hand_list[THUMB_COORD[0]][0] = HU_RIGHT_THUMB_DOWN[1]
    hand_list[THUMB_COORD[1]][0] = HU_RIGHT_THUMB_DOWN[0]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 30


def test_counting_function_hand_upwards_index_down_thumb_right(
        hands_up_thumb_right):
    """
    All fingers up for one hand, except for the index finger. Should return 4 in
    decimal and 29 in binary.

    Thumb joint is indexed as 6 and 8 in hand_list. We care about the y-pos
    for whether it is up of not

    return: None
    """
    thumb_left = False
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_right
    index_finger = FINGER_COORD[0]
    hand_list[index_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[index_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 29


def test_counting_function_hand_upwards_middle_down_thumb_right(
        hands_up_thumb_right):
    """
    All fingers up for one hand, except for the middle finger. Should return
    4 in decimal and 27 in binary.

    Thumb joint is indexed as 10 and 12 in hand_list. We care about the y-pos
    for whether it is up of not

    return: None
    """
    thumb_left = False
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_right
    middle_finger = FINGER_COORD[1]
    hand_list[middle_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[middle_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 27


def test_counting_function_hand_upwards_ring_down_thumb_right(
        hands_up_thumb_right):
    """
    All fingers up for one hand, except for the ring finger. Should return 4 in
    decimal and 25 in binary.

    return: None
    """
    thumb_left = False
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_right
    ring_finger = FINGER_COORD[2]
    hand_list[ring_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[ring_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 23


def test_counting_function_hand_upwards_pinky_down_thumb_right(
        hands_up_thumb_right):
    """
    All fingers up for one hand, except for the middle finger. Should return
    4 in decimal and 15 in binary.

    return: None
    """
    thumb_left = False
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_right
    pinky_finger = FINGER_COORD[3]
    hand_list[pinky_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[pinky_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 15


def test_counting_function_hand_upwards_all_fingers_up_thumb_left(
        hands_up_thumb_left):
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
                                   hands_up_thumb_left,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_upwards_thumb_down_thumb_left(
        hands_up_thumb_left):
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
    hand_list = hands_up_thumb_left
    hand_list[THUMB_COORD[0]][0] = HU_LEFT_THUMB_DOWN[1]
    hand_list[THUMB_COORD[1]][0] = HU_LEFT_THUMB_DOWN[0]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 15


def test_counting_function_hand_upwards_index_down_thumb_left(
        hands_up_thumb_left):
    """
    All fingers up for one hand, except for the index finger. Should return 4 in
    decimal and 29 in binary.

    Thumb joint is indexed as 6 and 8 in hand_list. We care about the y-pos
    for whether it is up of not

    return: None
    """
    thumb_left = True
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_left
    index_finger = FINGER_COORD[0]
    hand_list[index_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[index_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 23


def test_counting_function_hand_upwards_middle_down_thumb_left(
        hands_up_thumb_left):
    """
    All fingers up for one hand, except for the middle finger. Should return
    4 in decimal and 27 in binary.

    Thumb joint is indexed as 10 and 12 in hand_list. We care about the y-pos
    for whether it is up of not

    return: None
    """
    thumb_left = True
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_left
    middle_finger = FINGER_COORD[1]
    hand_list[middle_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[middle_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 27


def test_counting_function_hand_upwards_ring_down_thumb_left(
        hands_up_thumb_left):
    """
    All fingers up for one hand, except for the ring finger. Should return 4 in
    decimal and 25 in binary.

    return: None
    """
    thumb_left = True
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_left
    ring_finger = FINGER_COORD[2]
    hand_list[ring_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[ring_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 29


def test_counting_function_hand_upwards_pinky_down_thumb_left(
        hands_up_thumb_left):
    """
    All fingers up for one hand, except for the middle finger. Should return
    4 in decimal and 15 in binary.

    return: None
    """
    thumb_left = True
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_left
    pinky_finger = FINGER_COORD[3]
    hand_list[pinky_finger[0]][1] = HU_FINGER_DOWN[0]
    hand_list[pinky_finger[1]][1] = HU_FINGER_DOWN[1]
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, HAND_NUM, TOT_NUM_HANDS,
                                   decimal, binary)
    assert decimal == 4
    assert binary == 30
