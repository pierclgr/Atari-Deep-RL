from abc import ABC, abstractmethod
import random
from typing import Type

import gym
import torch
from src.models import RLNN


# TODO documentation

# define a superclass "Agent" for all the possible Agents; this will act as an interface for the other classes
class Agent(ABC):
    """
    A class representing an agent interface for other agents
    """

    @abstractmethod
    def __init__(self, env: gym.Env, *args) -> None:
        """
        Constructor method of the class that initializes the agent with the environment characteristics

        :param env: the gym environment that the agent should interact with (gym.Env)
        :param args: other arguments passed to the agent
        """

        # set action space size
        self.action_space = env.action_space
        self.observation_space = env.observation_space
        self.action_space_size = env.action_space.n
        self.observation_space_shape = env.observation_space.shape

    @abstractmethod
    def select_action(self, *args) -> int:
        """
        Method to select an action from the action space accordingly to a certain policy

        :param args: arguments passed to the agent to make the selection
        :return: the action selected by the environment (int)
        """
        pass


# define a class "RandomAgent" which is an agent following the random action selection policy
class RandomAgent(Agent):
    """
    A class representing an agent that follows random action selection policy
    """

    def __init__(self, env: gym.Env) -> None:
        """
        Constructor method for the class RandomAgent that just calls the constructor of its superclass Agent

        :param env: the gym environment that the agent should interact with (gym.Env)
        """
        super(RandomAgent, self).__init__(env)

    def select_action(self) -> int:
        """
        Method that selects an action to take from the action space randomly

        :return: action from the action space selected randomly (int)
        """

        # select an action randomly from the action space by using the action space size
        selected_action = random.randint(0, self.action_space_size - 1)
        return selected_action


# create an agent that plays by following DQN algorithm
class DQNAgent(Agent):
    def __init__(self, env: gym.Env, model: Type[RLNN]) -> None:
        super(DQNAgent, self).__init__(env)
        self.model = model(self.action_space_size, self.observation_space_shape)

    def select_action(self, state: torch.Tensor) -> int:
        selected_action = self.model(state)
        return selected_action
