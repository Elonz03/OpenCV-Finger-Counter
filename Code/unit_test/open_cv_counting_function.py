import pytest

from main import finger_count, THUMB_COORD, FINGER_COORD


def test_counting_function_hand_upwards_all_fingers_up_thumb_right():
    """
    All fingers up for one hand. Should return 5 in decimal and 31 in
    binary.
    Thumb right is from the perspective of the user to the device.

    return: None
    """
    thumb_left = False
    hand_num = 0  # This is one hand, but its index is 0
    tot_num_hands = 1
    decimal = 0
    binary = 0
    hand_list = ([(419, 597), (502, 580), (569, 535), (621, 501), (668, 493),
                 (520, 420), (542, 348), (553, 306), (563, 268), (473, 406),
                 (483, 324), (490, 275), (496, 234), (428, 408), (434, 333),
                 (442, 290), (451, 252), (381, 424), (376, 366), (377, 330),
                 (382, 297)])
    decimal, binary = finger_count(FINGER_COORD, THUMB_COORD, hand_list,
                                   thumb_left, hand_num, tot_num_hands,
                                   decimal, binary)
    assert decimal == 5
    assert binary == 31
