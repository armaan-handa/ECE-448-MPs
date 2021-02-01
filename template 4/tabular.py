import math

import gym
import numpy as np
import torch

import utils
from policies import QPolicy


class TabQPolicy(QPolicy):
    def __init__(self, env, buckets, actionsize, lr, gamma, model=None):
        """
        Inititalize the tabular q policy

        @param env: the gym environment
        @param buckets: specifies the discretization of the continuous state space for each dimension
        @param actionsize: dimension of the descrete action space.
        @param lr: learning rate for the model update 
        @param gamma: discount factor
        @param model (optional): Stores the Q-value for each state-action
            model = np.zeros(self.buckets + (actionsize,))
            
        """
        super().__init__(len(buckets), actionsize, lr, gamma)
        # print(buckets)
        self.env = env
        self.lr = lr
        self.lr_constant = 100
        self.gamma = gamma
        self.buckets = buckets
        if model is None:
            self.model = np.zeros(self.buckets + (actionsize,))
        else:
            self.model = model
        self.Ntable = np.zeros(self.buckets + (actionsize,))
        # print(self.model)
        

    def discretize(self, obs):
        """
        Discretizes the continuous input observation

        @param obs: continuous observation
        @return: discretized observation  
        """
        upper_bounds = [self.env.observation_space.high[0], self.env.observation_space.high[1]]
        lower_bounds = [self.env.observation_space.low[0], self.env.observation_space.low[1]]
        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

    def qvals(self, states):
        """
        Returns the q values for the states.

        @param state: the state
        
        @return qvals: the q values for the state for each action.
        """
        ret = []
        # print(states)
        for state in states:
            idx = self.discretize(state)
            # print(idx)
            ret.append(self.model[idx])
        # print(ret)
        return ret

    def td_step(self, state, action, reward, next_state, done):
        """
        One step TD update to the model

        @param state: the current state
        @param action: the action
        @param reward: the reward of taking the action at the current state
        @param next_state: the next state after taking the action at the
            current state
        @param done: true if episode has terminated, false otherwise
        @return loss: total loss the at this time step
        """
        # if done and next_state[0] >= 0.5:
        #     reward = 1.0

        if done and next_state[0] >= 0.5:
            # reward = 1.0
            target = 1.0
            # print("terminal")
            # env.reset()
        else:
            target = reward + self.gamma * np.max(self.qvals([next_state])[0]) 
            # print(np.argmax(self.qvals([next_state])[0]))

        loss = (target - self.qvals([state])[0][action])
        self.model[self.discretize(state)][action] += min(self.lr, (self.lr_constant/(self.lr_constant + self.Ntable[self.discretize(state)][action])))*loss
        self.Ntable[self.discretize(state)][action] += 1
        # print(self.model[self.discretize(state)][action])
        return loss**2


    def save(self, outpath):
        """
        saves the model at the specified outpath
        """
        torch.save(self.model, outpath)


if __name__ == '__main__':
    args = utils.hyperparameters()

    env = gym.make('MountainCar-v0')

    statesize = env.observation_space.shape[0]
    actionsize = env.action_space.n
    policy = TabQPolicy(env, buckets=(30, 20), actionsize=actionsize, lr=args.lr, gamma=args.gamma)

    utils.qlearn(env, policy, args)
    # policy = TabQPolicy(env, buckets=(12, 9), actionsize=actionsize, lr=args.lr, gamma=args.gamma, model=policy.model)
    # utils.qlearn(env, policy, args)
    # print(policy.model)

    torch.save(policy.model, 'models/tabular.npy')
