#!/usr/bin/python
import random
import os
import logging
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras import backend as K
from envs.tetris_env import TetrisEnv

HOME = os.path.dirname(os.path.realpath(__file__))

model_path = os.path.join(HOME, "model")
model_tmp_path = os.path.join(HOME, "model_tmp")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.join(HOME, 'log/tetris_DQNtrain.log'),
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
        self._load_model()

    def _load_model(self):
        
        if os.path.exists(model_path) and os.path.exists(model_tmp_path):
            try:
                self.load(model_path)
            except:
                logger.error("model error")
                os.system("rm -f {}".format(model_path))
                os.system("cp {} {}".format(model_tmp_path, model_path))
                self.load(model_path)

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_shape=self.state_size, activation='relu'))
        model.add(Flatten())
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
        
        agent.save(model_path)
        os.system("cp -f {} {}".format(model_path, model_tmp_path))

    agent.replay(200)

    total_reward = game_loop(agent, env)    
    print("[+] Ended with reward {1}".format(total_reward))


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


if __name__ == "__main__":
    train()
    
    
        
    

