import pytest

from main import (finger_position_relative_to_wrist, THUMB_COORD, FINGER_COORD)


@pytest.fixture
def hands_up_thumb_left():
    hand_up_all_fingers_up_thumb_left = [
        [500, 500], [0, 0], [520, 430], [0, 0], [530, 400], [0, 0],
        [510, 360], [0, 0], [510, 320], [0, 0], [500, 280], [0, 0],
        [500, 240], [0, 0], [490, 300], [0, 0], [490, 250], [0, 0],
        [475, 350], [0, 0], [450, 300]
    ]
    return hand_up_all_fingers_up_thumb_left


@pytest.fixture
def hand_pointing_right():
    hand_up_all_fingers_up = [
        [117, 355], [0, 0], [326, 573], [0, 0], [543, 654], [0, 0],
        [654, 456], [0, 0], [821, 459], [0, 0], [671, 351], [0, 0],
        [866, 337], [0, 0], [630, 266], [0, 0], [808, 260], [0, 0],
        [535, 180], [0, 0], [672, 156]
    ]
    return hand_up_all_fingers_up


def test_finger_position_function_hand_upright(hands_up_thumb_left):
    """
    This is to check that the finger_position_relative_to_wrist returns the
    correct output. Depending on the largest difference x/y position it
    should return that for each joint. However, for the thumb it should
    return the smallest difference.

    return: None
    """
    finger_pos = finger_position_relative_to_wrist(hands_up_thumb_left,
                                                   FINGER_COORD)
    thumb_pos = finger_position_relative_to_wrist(hands_up_thumb_left,
                                                  THUMB_COORD, thumb=True)
    finger_pos += thumb_pos
    expected_output = [[180, 140], [260, 220], [250, 200],
                       [200, 150], [30, 20]]
    assert expected_output == finger_pos


def test_finger_position_function_hand_pointing_right(hand_pointing_right):
    """
    return: None
    """
    finger_pos = finger_position_relative_to_wrist(hand_pointing_right,
                                                   FINGER_COORD)
    thumb_pos = finger_position_relative_to_wrist(hand_pointing_right,
                                                  THUMB_COORD, thumb=True)
    finger_pos += thumb_pos
    expected_output = [[704, 537], [749, 554], [691, 513], [555, 418],
                       [299, 209]]
    assert expected_output == finger_pos
