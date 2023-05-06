"""
Module with Bot class
"""
import time
from typing import List

import numpy as np

from app.src.environment import Environment
from app.src.finding_algorithm.distributed_greedy_bfs import DistributedGreedyBFS
from app.src.utils import Utils


class Bot:
    """
    Represents bot at an unknown position in given environment. Bot can find itself. All coordinates are [row, column].
    """

    def __init__(self, environment: Environment, sight_range: int = 1):
        self.finding_algorithm = DistributedGreedyBFS(environment.map)
        self.environment = environment

        self.relative_dir = Utils.initial_dir
        self.relative_pos = np.array([0, 0])

        self.sight_range = sight_range

        bot_map_size = (max(self.environment.map.shape) + self.sight_range) * 2 + 1
        self.bot_map = np.ones((bot_map_size, bot_map_size)) * -1

    def rotate(self, direction: str) -> None:
        """
        Rotates bot in specified direction both in bot map and in environment map
        :param direction: left/right. Direction to rotate bot in
        """
        self.environment.rotate(direction)

        self.relative_dir = Utils.rotate_coords(self.relative_dir, direction)

    def move(self) -> None:
        """If possible moves bot one tile forward in the direction of the bot."""
        if self.environment.move():
            self.relative_pos = self.relative_pos + self.relative_dir
            self.add_environment_to_map()

    def find_itself(self, print_map: bool = True, wait_time: int = 0) -> tuple[List[tuple[np.ndarray, int]], int]:
        """
        Finds bot starting position using finding algorithm.
        :param print_map: If True prints map. For large maps recommended using False.
        :param wait_time: Time to wait between individual steps. Used for better readability. Good value is around 0.5 second.
        :return: (positions, steps) Bot starting position or possible starting positions and number of steps needed.
        """
        self.add_environment_to_map()
        path = self.finding_algorithm.get_path_controller(self.environment.map, self.bot_map, self.relative_pos,
                                                          self.relative_dir)

        if print_map:
            self.environment.print_map(self.finding_algorithm.possible_current_poss(self.relative_pos, self.relative_dir))
        self.environment.print_bot_stats(path, self.finding_algorithm.steps,
                                         self.finding_algorithm.possible_current_poss_to_str(self.relative_pos,
                                                                                             self.relative_dir),
                                         self.get_discovered_tiles_count())
        time.sleep(wait_time)

        while True:
            if len(path) == 0:
                path = self.finding_algorithm.get_path_controller(self.environment.map, self.bot_map, self.relative_pos,
                                                                  self.relative_dir)

                if len(path) == 0:
                    self.print_search_result(print_map)
                    return self.finding_algorithm.possible_starting_poss, self.finding_algorithm.steps

            action = path.pop(0)
            self.finding_algorithm.steps += 1

            if action == 'move':
                self.move()
            else:
                self.rotate(action)

            if print_map:
                self.environment.print_map(
                    self.finding_algorithm.possible_current_poss(self.relative_pos, self.relative_dir))
            self.environment.print_bot_stats(path, self.finding_algorithm.steps,
                                             self.finding_algorithm.possible_current_poss_to_str(self.relative_pos,
                                                                                                 self.relative_dir),
                                             self.get_discovered_tiles_count())
            time.sleep(wait_time)

    def add_environment_to_map(self) -> None:
        """Adds environment in bots sight range to bots map."""
        bot_map_coords = self.relative_pos + np.asarray(self.bot_map.shape) // 2
        self.environment.get_nearby_environment(self.bot_map, bot_map_coords, self.sight_range)

    def print_search_result(self, print_map: bool = True) -> None:
        """Prints result of the search after search is done."""
        if print_map:
            self.environment.print_map(self.finding_algorithm.possible_current_poss(self.relative_pos, self.relative_dir))

        print('Search finished')
        if self.finding_algorithm.is_bot_found:
            print(
                f'Bot is found. Current position: {self.finding_algorithm.possible_current_poss_to_str(self.relative_pos, self.relative_dir)}. Starting position: {self.finding_algorithm.possible_starting_poss_to_str()}',
                f'Is found position correct: {self.environment.check_position(self.finding_algorithm.possible_starting_poss[0])}',
                sep='\n')
        else:
            print(
                f'Starting position cannot be definitely found. Possible starting positions are: {self.finding_algorithm.possible_starting_poss_to_str()}',
                f'Is one of those positions starting position: {any(self.environment.check_position(pos) for pos in self.finding_algorithm.possible_starting_poss)} ({self.environment.initial_bot_pos} {Utils.dir_to_unicode_arrow(self.environment.initial_bot_dir)})',
                sep='\n')
        print(f'Steps: {self.finding_algorithm.steps}',
              f'Discovered tiles: {self.get_discovered_tiles_count()}', sep='\n')

    def get_discovered_tiles_count(self) -> int:
        """
        :return: Number of discovered tiles in bot map
        """
        return np.count_nonzero(self.bot_map + 1)
