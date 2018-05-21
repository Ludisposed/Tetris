import gym
from random import choice

env = gym.make('MountainCar-v0')
observation = env.reset() 
print(observation)
print(env.action_space.n)
action = choice(range(env.action_space.n))
obs, reward, done, _ = env.step(action)
print(obs)
print(env.observation_space.shape)