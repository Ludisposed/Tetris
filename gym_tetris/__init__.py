# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-05-14 17:30:47
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-05-14 17:35:42
import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Tetris-v0',
    entry_point='gym_tetris.envs:TetrisEnv',
)
