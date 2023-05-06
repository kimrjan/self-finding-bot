"""
Module with Utils class
"""
from typing import Union

import numpy as np


class Utils:
    """
    Helper functions
    """
    initial_dir = np.array([1, 0])
    neighbours = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]

    @staticmethod
    def rotate_coords(coords: np.ndarray, direction: str, count: int = 1) -> np.ndarray:
        """
        Rotates coords right or left
        :param coords: coords to rotate
        :param direction: right or left
        :param count: count of rotations
        :return:
        """
        if direction not in ('left', 'right'):
            raise ValueError('Unknown direction.')

        if not isinstance(coords, np.ndarray) or coords.shape != (2,):
            raise ValueError('Cords must be np.ndarray with shape (2, )')

        if count == 0:
            return coords

        count %= 4
        if count > 2:
            count = 4 - count
            direction = 'left' if direction == 'right' else 'right'

        for _ in range(count):
            if direction == 'left':
                coords = coords @ np.array([[0, 1], [-1, 0]])
            elif direction == 'right':
                coords = coords @ np.array([[0, -1], [1, 0]])

        return np.squeeze(np.asarray(coords))

    @staticmethod
    def dir_to_number(dir_coords: np.ndarray) -> int:
        """
        :param dir_coords: coordinates of direction - 2D np.ndarray
        :return: number of direction (0 - down, 1 - left, 2 - up, 3 - right)
        """
        if np.linalg.norm(dir_coords) == 0:
            raise ValueError('norm is 0')

        dir_coords = dir_coords / np.linalg.norm(dir_coords)

        if np.array_equal(np.array([1, 0]), dir_coords):
            return 0
        if np.array_equal(np.array([0, 1]), dir_coords):
            return 1
        if np.array_equal(np.array([-1, 0]), dir_coords):
            return 2
        if np.array_equal(np.array([0, -1]), dir_coords):
            return 3

        raise ValueError('dir_cords are not coords of any direction')

    @staticmethod
    def number_to_dir(dir_number: int):
        """
        :param dir_number: number of direction (0 - down, 1 - left, 2 - up, 3 - right)
        :return: coordinates of direction - 2D np.ndarray with norm of one
        """

        dir_number %= 4

        if dir_number == 0:
            return np.array([1, 0])
        if dir_number == 1:
            return np.array([0, 1])
        if dir_number == 2:
            return np.array([-1, 0])
        if dir_number == 3:
            return np.array([0, -1])

        raise ValueError('Unknown direction')

    walls = {
        0: '\u00b7',
        1: '\u2575',
        2: '\u2577',
        3: '\u2502',
        4: '\u2574',
        5: '\u2518',
        6: '\u2510',
        7: '\u2524',
        8: '\u2576',
        9: '\u2514',
        10: '\u250c',
        11: '\u251c',
        12: '\u2500',
        13: '\u2534',
        14: '\u252c',
        15: '\u253c',
    }

    @staticmethod
    def num_to_unicode_wall(num: int):
        """
        :param num: Sum of powers of two for neighbouring walls (up - 2^0, down - 2^1, left - 2^2, right - 2^3)
        :return: Unicode char for specified wall segment
        """

        wall = Utils.walls.get(num, None)

        if wall is not None:
            return wall

        raise ValueError('Unsupported wall')

    @staticmethod
    def load(file_name: str) -> np.ndarray:
        """
        Loads file with 'X' and ' ' to np.array
        :param file_name: file to load
        :return: 2D np.array with loaded file where 'X' is 0 and ' ' is 1.
        """
        with open(file_name, 'r', encoding='ascii') as file:
            lines = file.readlines()
            environment_map = [[0 if char == 'X' else 1 for char in line[: -1]] for line in lines]

            return np.array(environment_map, int)

    @staticmethod
    def dir_to_unicode_arrow(direction: Union[int, np.ndarray]):
        """
        :param direction:
        :return: Unicode arrow for give direction
        """
        if isinstance(direction, np.ndarray):
            direction = Utils.dir_to_number(direction)
        else:
            direction %= 4

        if direction == 0:
            return '\u2193'
        if direction == 1:
            return '\u2192'
        if direction == 2:
            return '\u2191'
        if direction == 3:
            return '\u2190'

        raise ValueError('Unsupported direction')

    @staticmethod
    def print_colored(string: str, *, fg_color: str = None, bg_color: str = None, end: str = '\n') -> None:
        """
        Prints string with specified fg and bg color
        :param string: string to print
        :param fg_color: foreground color. If none than default is used
        :param bg_color: background color. If none than default is used
        :param end: printed after string
        """
        fg_color_num = 30 + Utils.color_name_to_num(fg_color) if fg_color is not None else 0
        bg_color_num = 40 + Utils.color_name_to_num(bg_color) if bg_color is not None else 0

        print(f'\033[{fg_color_num};{bg_color_num}m{string}\033[0m', end=end)

    @staticmethod
    def color_name_to_num(color: str):
        """
        :param color: color name
        :return: color terminal number
        """

        num = None
        if color == 'black':
            num = 0
        if color == 'red':
            num = 1
        if color == 'green':
            num = 2
        if color == 'yellow':
            num = 3
        if color == 'blue':
            num = 4
        if color == 'magenta':
            num = 5
        if color == 'cyan':
            num = 6
        if color == 'white':
            num = 7

        if num is not None:
            return num

        raise ValueError('Unknown color')
