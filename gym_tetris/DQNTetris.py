#!/usr/bin/python
import random
import os
import logging
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K
from envs.tetris_env import TetrisEnv

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/aries/log/tetris_DQNtrain.log',
                    filemode='a+')

logger = logging.getLogger(__name__)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        if os.path.exists("/home/aries/tetris/gym_tetris/model") and os.path.exists("/home/aries/tetris/gym_tetris/model_tmp"):
            try:
                self.load("/home/aries/tetris/gym_tetris/model")
            except:
                logger.error("model error")
                os.system("rm -f /home/aries/tetris/gym_tetris/model")
                self.load("/home/aries/tetris/gym_tetris/model_tmp")

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_shape=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
        
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

def train():
    env = TetrisEnv()
    agent = DQNAgent(env.state_size, env.action_size)
    iter_max = 10000
    for i in range(iter_max):
        i += 1
        total_reward = game_loop(agent, env)
        
        logger.info("[+] Episode {0} ended with reward {1}".format(i, total_reward))
        os.system("mv -f /home/aries/tetris/gym_tetris/model /home/aries/tetris/gym_tetris/model_tmp")
        agent.save("/home/aries/tetris/gym_tetris/model")

def game_loop(agent, env, render = False):
    total_reward = 0
    done = False
    state = env.reset()
    while not done:
        action = agent.act(state)
        if render:env.render()
        
        next_state, reward, done, info = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
    return total_reward

# copy learning from somewhere else
# def learning():
#     minibatch = random.sample(D, mb_size)                              # Sample some moves

#     inputs_shape = (mb_size,) + state.shape[1:]
#     inputs = np.zeros(inputs_shape)
#     targets = np.zeros((mb_size, env.action_space.n))

#     for i in range(0, mb_size):
#         state = minibatch[i][0]
#         action = minibatch[i][1]
#         reward = minibatch[i][2]
#         state_new = minibatch[i][3]
#         done = minibatch[i][4]
        
#     # Build Bellman equation for the Q function
#         inputs[i:i+1] = np.expand_dims(state, axis=0)
#         targets[i] = model.predict(state)
#         Q_sa = model.predict(state_new)
        
#         if done:
#             targets[i, action] = reward
#         else:
#             targets[i, action] = reward + gamma * np.max(Q_sa)

#     # Train network to output the Q function
#         model.train_on_batch(inputs, targets)
    

def test():
    # play game
    pass

if __name__ == "__main__":
    train()
    
    
        
    

