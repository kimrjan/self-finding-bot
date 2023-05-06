"""
Module with Environment class
"""
import random
from typing import List

import numpy as np

from app.src.utils import Utils


class Environment:
    """
    Represents environment in which the bot is. All coordinates are [row, column].
    """
    def __init__(self, environment_map: np.ndarray, bot_pos: np.ndarray = None, bot_dir: np.ndarray = None):
        self.map = environment_map.astype(int)
        self.size = np.asarray(self.map.shape)

        self.bot_pos = bot_pos
        self.bot_dir = bot_dir

        if bot_pos is None or self.map[tuple(bot_pos)] == 0:
            print('Bot position is None or inside a wall. Choosing random position.')
            non_zero = np.where(self.map > 0)
            random_idx = random.randint(0, len(non_zero[0]) - 1)

            self.bot_pos = np.array([non_zero[0][random_idx], non_zero[1][random_idx]])

        if bot_dir is None:
            print('Bot direction is None. Choosing random direction.')
            self.bot_dir = Utils.number_to_dir(random.randint(0, 3))

        self.initial_bot_pos = self.bot_pos
        self.initial_bot_dir = self.bot_dir

    def rotate(self, direction: str) -> None:
        """
        Rotates bot in specified direction.
        :param direction: left/right. direction to rotate bot in
        """

        self.bot_dir = Utils.rotate_coords(self.bot_dir, direction)

    def move(self) -> bool:
        """
        If possible moves bot one step forward. In case the bot is in front of a barrier (map value is 0), bot's position stays same.
        :return: True if bot's position changed one step in bot's direction.
        """
        previous_position = self.bot_pos
        if self.map[tuple(np.clip(self.bot_pos + self.bot_dir, [0, 0], self.size - 1))] == 0:
            return False

        self.bot_pos = np.clip(self.bot_pos + self.bot_dir, [0, 0], self.size - 1)
        return np.array_equal(previous_position + self.bot_dir, self.bot_pos)

    def get_nearby_environment(self, bot_map: np.ndarray, bot_map_coords: np.ndarray, sight_range: int):
        """
        Adds bots surroundings to bot's map
        :param bot_map:
        :param bot_map_coords:
        :param sight_range:
        :return:
        """
        rotation_diff = (Utils.dir_to_number(self.initial_bot_dir) - Utils.dir_to_number(Utils.initial_dir)) % 4

        for dx in range(-sight_range, sight_range + 1):
            for dy in range(-sight_range, sight_range + 1):
                delta = np.array([dx, dy])
                coords = bot_map_coords + Utils.rotate_coords(delta, 'right', rotation_diff)
                env_coords = self.bot_pos + delta

                if not 0 <= env_coords[0] < self.map.shape[0] or not 0 <= env_coords[1] < self.map.shape[1]:
                    continue

                bot_map[coords[0], coords[1]] = self.map[env_coords[0], env_coords[1]]

    def print_map(self, possible_current_poss: List[tuple]) -> None:
        """
        Prints map. Bot is arrow and possible positions of the bot are yellow.
        :param possible_current_poss: These positions are printed with yellow background
        """
        possible_current_poss = [(list(pos), d) for pos, d in possible_current_poss]

        for row in range(self.map.shape[0]):
            for col in range(self.map.shape[1]):
                fg_color = None
                bg_color = None
                tile = ' '
                if self.map[row, col] == 0:
                    neighbours = 0
                    if row > 0 and self.map[row - 1, col] == 0:
                        neighbours += 1
                    if row < self.map.shape[0] - 1 and self.map[row + 1, col] == 0:
                        neighbours += 2
                    if col > 0 and self.map[row, col - 1] == 0:
                        neighbours += 4
                    if col < self.map.shape[1] - 1 and self.map[row, col + 1] == 0:
                        neighbours += 8

                    tile = Utils.num_to_unicode_wall(neighbours)
                elif np.array_equal(self.bot_pos, [row, col]):
                    tile = Utils.dir_to_unicode_arrow(self.bot_dir)
                    fg_color = 'black'

                if any(([row, col], d) in possible_current_poss for d in range(4)):
                    bg_color = 'yellow'

                Utils.print_colored(tile, fg_color=fg_color, bg_color=bg_color, end='')
            print()

        print('Legend:')
        Utils.print_colored(Utils.dir_to_unicode_arrow(self.bot_dir), fg_color='black', bg_color='yellow', end='')
        print(' - bot')
        Utils.print_colored(' ', fg_color='black', bg_color='yellow', end='')
        print(' - possible bot position')

    def print_bot_stats(self, path: List[str], steps: int, possible_current_positions_string: str, discovered_tiles: int) -> None:
        """
        Prints bot stats
        :param path:
        :param steps:
        :param possible_current_positions_string:
        :param discovered_tiles:
        """
        print('Bot',
              f'Position and direction: ({self.bot_pos} {Utils.dir_to_unicode_arrow(self.bot_dir)})',
              f'Moves to do: {path}',
              f'Steps: {steps}',
              f'Possible current positions: {possible_current_positions_string}',
              f'Discovered tiles: {discovered_tiles}',
              80 * '-', sep='\n')

    def check_position(self, expected_position: tuple[np.ndarray, int]) -> bool:
        """
        :param expected_position: (pos, dir as number)
        :return: True if expected position and direction match starting position and direction
        """
        return np.array_equal(self.initial_bot_pos, expected_position[0]) and np.array_equal(self.initial_bot_dir, Utils.number_to_dir(expected_position[1]))
