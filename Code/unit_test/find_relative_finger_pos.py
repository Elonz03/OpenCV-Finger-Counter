import pytest

from main import (finger_position_relative_to_focal_point, THUMB_COORD,
                  FINGER_COORD)


hand_up_all_fingers_up_thumb_left = [
    (502, 503), (420, 460), (359, 402), (322, 347), (283, 312), (428, 309),
    (396, 208), (381, 149), (374, 104), (485, 300), (481, 182), (482, 114),
    (489, 68), (539, 309), (530, 198), (529, 133), (530, 83), (590, 331),
    (591, 251), (591, 205), (590, 167)
]


hand_up_all_fingers_up = [
    (155, 313), (256, 435), (363, 487), (458, 525), (528, 568), (485, 383),
    (635, 375), (717, 367), (782, 360), (483, 297), (645, 276), (738, 262),
    (805, 251), (456, 217), (604, 197), (691, 187), (754, 183), (414, 150),
    (527, 123), (589, 112), (643, 108)
]

hand_diagonally_right = [
    (336, 564), (431, 618), (539, 624), (624, 605), (697, 602), (607, 486),
    (707, 457), (768, 434), (820, 413), (579, 426), (683, 365), (752, 325),
    (812, 289), (530, 385), (629, 322), (696, 286), (756, 256), (465, 357),
    (531, 299), (579, 265), (626, 237)
]


hand_diagonally_right_thumb_down = [
    (475, 621), (544, 636), (621, 621), (633, 566), (602, 525), (670, 532),
    (737, 491), (774, 462), (805, 435), (643, 493), (712, 427), (754, 385),
    (787, 349), (606, 471), (663, 405), (701, 364), (733, 328), (556, 458),
    (595, 401), (622, 367), (648, 336)
]


@pytest.mark.parametrize("test_input",
                         (
                                 hand_up_all_fingers_up_thumb_left,
                                 hand_up_all_fingers_up,
                                 hand_diagonally_right
                          )
                         )
def test_finger_position_function_all_fingers_up(test_input):
    """
    This is to check that the finger_position_relative_to_focal_point returns
    the correct output. Depending on the largest difference x/y position it
    should return that for each joint.

    return: None
    """
    finger_pos = finger_position_relative_to_focal_point(
        test_input, FINGER_COORD)
    thumb_pos = finger_position_relative_to_focal_point(
        test_input, THUMB_COORD, thumb=True)
    finger_pos += thumb_pos

    assert all(finger_point[0] > finger_point[1] for
               finger_point in finger_pos)


def test_finger_position_function_thumb_down():
    """
    All but the thumb should have the returned 0th index greater than the 1st
    index

    return: None
    """
    finger_pos = finger_position_relative_to_focal_point(
        hand_diagonally_right_thumb_down, FINGER_COORD)
    thumb_pos = finger_position_relative_to_focal_point(
        hand_diagonally_right_thumb_down, THUMB_COORD, thumb=True)
    finger_pos += thumb_pos

    assert all(finger_point[0] > finger_point[1] for
               finger_point in finger_pos[:len(finger_pos)-1])
    assert finger_pos[4][0] < finger_pos[4][1]
