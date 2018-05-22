#!/usr/bin/python
import random
import os
import sys
import logging
import numpy as np
from datetime import datetime
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras import backend as K
from envs.tetris_env import TetrisEnv

HOME = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.join(HOME, 'log/tetris_DQNtrain.log'),
                    filemode='a+')

logger = logging.getLogger(__name__)

class DQNAgent:
    def __init__(self, state_size, action_size, model_name="model"):
        self.model_name = os.path.join(HOME, model_name)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.load()

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

    def load(self):
        if os.path.exists(self.model_name):
            self.model.load_weights(self.model_name)

    def save(self):
        try:
            self.model.save_weights(self.model_name)
        except KeyboardInterrupt:
            self.model.save_weights(self.model_name)
            sys.exit(0)

def train(train_seconds, observatime, batch_size):
    start = datetime.now()
    env = TetrisEnv()
    agent = DQNAgent(env.state_size, env.action_size)
    while True:
        train_loop(agent, env, observatime) 
        agent.replay(batch_size)
        agent.save()
        test(env, agent)
        current = datetime.now()
        if (current-start).seconds >= train_seconds:
            break
        
def train_loop(agent, env, observatime):
    done = False
    state = env.reset()
    state = np.expand_dims(state, axis=0) 
    for _ in range(observatime):
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        next_state = np.expand_dims(next_state, axis=0)
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        if done:
            state = env.reset()
            state = np.expand_dims(state, axis=0)     

def test(env, agent):
    observation = env.reset()
    state = np.expand_dims(observation, axis=0)
    done = False
    tot_reward = 0.0
    while not done:
        Q = agent.act(state)        
        action = np.argmax(Q)         
        next_state, reward, done, info = env.step(action)
        state = np.expand_dims(next_state, axis=0) 
        tot_reward += reward
    print('Game ended! Total reward: {}'.format(reward))
    logger.info('Game ended! Total reward: {}'.format(reward))

if __name__ == "__main__":
    train(60*60*24,100,50)
    
    
        
    

