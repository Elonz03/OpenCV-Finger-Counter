import pytest

from main import (THUMB_COORD, FINGER_COORD,
                  finger_position_relative_to_focal_point, finger_counter,
                  determine_thumb_position)

HAND_NUM = 0  # This is one hand, but its index is 0
TOT_NUM_HANDS = 1


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


@pytest.fixture
def hands_down_thumb_left():
    hand_down_all_fingers_up_thumb_left = [
        [525, 135], [489, 201], [462, 262], [423, 303], [387, 333], [556, 333],
        [547, 414], [542, 465], [540, 512], [590, 317], [621, 405], [641, 460],
        [661, 510], [612, 280], [655, 354], [682, 406], [705, 456], [625, 229],
        [667, 271], [691, 306], [713, 344]
    ]
    return hand_down_all_fingers_up_thumb_left


@pytest.fixture
def hands_down_thumb_right():
    hand_down_all_fingers_up_thumb_right = [
        [688, 324], [753, 294], [818, 301], [860, 328], [914, 350], [808, 424],
        [838, 487], [847, 530], [848, 574], [746, 458], [762, 538], [762, 588],
        [756, 634], [682, 465], [680, 545], [669, 594], [658, 638], [619, 452],
        [579, 518], [546, 558], [518, 596]
    ]
    return hand_down_all_fingers_up_thumb_right


def test_counting_function_hand_upwards_all_fingers_up_thumb_right(
        hands_up_thumb_right):
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb right is from the perspective of the user to the device.

    return: None
    """
    decimal = 0
    binary = 0

    finger_list = finger_position_relative_to_focal_point(
        hands_up_thumb_right, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hands_up_thumb_right, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hands_up_thumb_right, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_upwards_all_fingers_up_thumb_left(
        hands_up_thumb_left):
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb left is from the perspective of the user to the device.

    return: None
    """
    decimal = 0
    binary = 0

    finger_list = finger_position_relative_to_focal_point(
        hands_up_thumb_left, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hands_up_thumb_left, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hands_up_thumb_left, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_downwards_all_fingers_up_thumb_left(
        hands_down_thumb_left):
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb left is from the perspective of the user to the device.
    The hand is upside down

    return: None
    """
    decimal = 0
    binary = 0

    finger_list = finger_position_relative_to_focal_point(
        hands_down_thumb_left, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hands_down_thumb_left, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hands_down_thumb_left, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == 5
    assert binary == 31


def test_counting_function_hand_downwards_all_fingers_up_thumb_right(
        hands_down_thumb_right):
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb left is from the perspective of the user to the device.
    The hand is upside down

    return: None
    """
    decimal = 0
    binary = 0

    finger_list = finger_position_relative_to_focal_point(
        hands_down_thumb_right, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hands_down_thumb_right, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hands_down_thumb_right, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == 5
    assert binary == 31


@pytest.mark.parametrize("test_input,expected",
                         [
                             (THUMB_COORD[0], [4, 30]),  # thumb down
                             (FINGER_COORD[0], [4, 29]),  # index down
                             (FINGER_COORD[1], [4, 27]),  # middle down
                             (FINGER_COORD[2], [4, 23]),  # ring down
                             (FINGER_COORD[3], [4, 15])  # pinky down
                         ]
                         )
def test_counting_function_hand_upwards_thumb_right(
        test_input, expected, hands_up_thumb_right):
    """
    The position of this hand has the fingers pointing upwards, with the
    thumb on the right side. This test alternates between fingers putting
    them 'down' by switching the co-ordinates of the joints and
    fingertips.

    return: None
    """
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_right
    temp_list = hand_list[test_input[0]]

    hand_list[test_input[0]] = hand_list[test_input[1]]
    hand_list[test_input[1]] = temp_list

    finger_list = finger_position_relative_to_focal_point(
        hand_list, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hand_list, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hand_list, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == expected[0]
    assert binary == expected[1]


@pytest.mark.parametrize("test_input,expected",
                         [
                             (THUMB_COORD[0], [4, 15]),  # thumb down
                             (FINGER_COORD[0], [4, 23]),  # index down
                             (FINGER_COORD[1], [4, 27]),  # middle down
                             (FINGER_COORD[2], [4, 29]),  # ring down
                             (FINGER_COORD[3], [4, 30])  # pinky down
                         ]
                         )
def test_counting_function_hand_upwards_thumb_left(
        test_input, expected, hands_up_thumb_left):
    """
    The position of this hand has the fingers pointing upwards, with the
    thumb on the left side. This test alternates between fingers putting
    them 'down' by switching the co-ordinates of the joints and
    fingertips.

    return: None
    """
    decimal = 0
    binary = 0
    hand_list = hands_up_thumb_left
    temp_list = hand_list[test_input[0]]

    hand_list[test_input[0]] = hand_list[test_input[1]]
    hand_list[test_input[1]] = temp_list

    finger_list = finger_position_relative_to_focal_point(
        hand_list, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hand_list, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hand_list, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == expected[0]
    assert binary == expected[1]


@pytest.mark.parametrize("test_input,expected",
                         [
                             (THUMB_COORD[0], [4, 15]),  # thumb down
                             (FINGER_COORD[0], [4, 23]),  # index down
                             (FINGER_COORD[1], [4, 27]),  # middle down
                             (FINGER_COORD[2], [4, 29]),  # ring down
                             (FINGER_COORD[3], [4, 30])  # pinky down
                         ]
                         )
def test_counting_function_hand_downwards_thumb_left(
        test_input, expected, hands_down_thumb_left):
    """
    The position of this hand has the fingers pointing downwards, with the
    thumb on the left side. This test alternates between fingers putting
    them 'down' by switching the co-ordinates of the joints and
    fingertips.

    return: None
    """
    decimal = 0
    binary = 0
    hand_list = hands_down_thumb_left
    temp_list = hand_list[test_input[0]]

    hand_list[test_input[0]] = hand_list[test_input[1]]
    hand_list[test_input[1]] = temp_list

    finger_list = finger_position_relative_to_focal_point(
        hand_list, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hand_list, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hand_list, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == expected[0]
    assert binary == expected[1]


@pytest.mark.parametrize("test_input,expected",
                         [
                             (THUMB_COORD[0], [4, 30]),  # thumb down
                             (FINGER_COORD[0], [4, 29]),  # index down
                             (FINGER_COORD[1], [4, 27]),  # middle down
                             (FINGER_COORD[2], [4, 23]),  # ring down
                             (FINGER_COORD[3], [4, 15])  # pinky down
                         ]
                         )
def test_counting_function_hand_downwards_thumb_right(
        test_input, expected, hands_down_thumb_right):
    """
    The position of this hand has the fingers pointing downwards, with the
    thumb on the left side. This test alternates between fingers putting
    them 'down' by switching the co-ordinates of the joints and
    fingertips.

    return: None
    """
    decimal = 0
    binary = 0
    hand_list = hands_down_thumb_right
    temp_list = hand_list[test_input[0]]

    hand_list[test_input[0]] = hand_list[test_input[1]]
    hand_list[test_input[1]] = temp_list

    finger_list = finger_position_relative_to_focal_point(
        hand_list, THUMB_COORD, thumb=True)
    finger_list += finger_position_relative_to_focal_point(
        hand_list, FINGER_COORD, thumb=False)
    finger_list = determine_thumb_position(hand_list, finger_list)
    decimal, binary = finger_counter(finger_list, HAND_NUM, TOT_NUM_HANDS,
                                     decimal, binary)
    assert decimal == expected[0]
    assert binary == expected[1]
