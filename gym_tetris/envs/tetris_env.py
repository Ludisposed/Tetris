# -*- coding: utf-8 -*-
# @Author: Li Qin
# @Date:   2018-05-14 17:34:44
# @Last Modified by:   Li Qin
# @Last Modified time: 2018-05-14 17:37:15

import gym
class TetrisEnv(gym.Env):
    def __init__(self):
        self.__version__ = "0.1.0"