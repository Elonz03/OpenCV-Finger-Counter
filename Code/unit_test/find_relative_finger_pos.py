import pytest

from main import (finger_position_relative_to_focal_point, THUMB_COORD,
                  FINGER_COORD)


@pytest.fixture
def hands_up_thumb_left():
    hand_up_all_fingers_up_thumb_left = [
        (502, 503), (420, 460), (359, 402), (322, 347), (283, 312), (428, 309),
        (396, 208), (381, 149), (374, 104), (485, 300), (481, 182), (482, 114),
        (489, 68), (539, 309), (530, 198), (529, 133), (530, 83), (590, 331),
        (591, 251), (591, 205), (590, 167)
    ]
    return hand_up_all_fingers_up_thumb_left


@pytest.fixture
def hand_pointing_right():
    hand_up_all_fingers_up = [
        (155, 313), (256, 435), (363, 487), (458, 525), (528, 568), (485, 383),
        (635, 375), (717, 367), (782, 360), (483, 297), (645, 276), (738, 262),
        (805, 251), (456, 217), (604, 197), (691, 187), (754, 183), (414, 150),
        (527, 123), (589, 112), (643, 108)
    ]
    return hand_up_all_fingers_up


def test_finger_position_function_hand_upright(hands_up_thumb_left):
    """
    This is to check that the finger_position_relative_to_focal_point returns the
    correct output. Depending on the largest difference x/y position it
    should return that for each joint.

    return: None
    """
    finger_pos = finger_position_relative_to_focal_point(
        hands_up_thumb_left, FINGER_COORD)
    thumb_pos = finger_position_relative_to_focal_point(
        hands_up_thumb_left, THUMB_COORD, thumb=True)
    finger_pos += thumb_pos
    expected_output = [[399, 295], [435, 321], [420, 305], [336, 252],
                       [307, 162]]
    assert all(finger_point[0] > finger_point[1] for
               finger_point in expected_output)


def test_finger_position_function_hand_pointing_right(hand_pointing_right):
    """
    return: None
    """
    finger_pos = finger_position_relative_to_focal_point(
        hand_pointing_right, FINGER_COORD)
    thumb_pos = finger_position_relative_to_focal_point(
        hand_pointing_right, THUMB_COORD, thumb=True)
    finger_pos += thumb_pos
    expected_output = [[704, 537], [749, 554], [691, 513], [555, 418],
                       [299, 209]]
    assert all(finger_point[0] > finger_point[1] for
               finger_point in expected_output)
