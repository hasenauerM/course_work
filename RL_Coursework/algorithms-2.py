from ast import Pass
from math import exp
import gym
from typing import Optional
from collections import defaultdict
from typing import Tuple
import numpy as np

def egreedy_action(Q: defaultdict, state: Tuple[int, int], epsilon:float):
    greedy_action = np.random.choice([a for a in range(len(Q[state])) if Q[state][a] == max(Q[state])])
    exp_action = np.random.choice([0,1,2,3])
    action = np.random.choice([greedy_action, exp_action], p=[1-epsilon, epsilon])
    return action

def sarsa(env: gym.Env, num_steps: int, gamma: float, epsilon: float, step_size: float):
    """SARSA algorithm.

    Args:
        env (gym.Env): a Gym API compatible environment
        num_steps (int): Number of steps
        gamma (float): Discount factor of MDP
        epsilon (float): epsilon for epsilon greedy
        step_size (float): step size
    """
    # TODO
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    num_episodes = 0
    eps_perstep = [num_episodes]
    #initial vals
    S = env.reset()
    A = egreedy_action(Q,S,epsilon)
    for t in num_steps:
        S_prime, reward, done, _ = env.step(A)
        if done:
            num_episodes+=1
        eps_perstep.append(num_episodes)
        A_prime = egreedy_action(S_prime)
        Q[S][A] = Q[S][A] + step_size*(reward + gamma*Q[S_prime][A_prime] - Q[S][A])
        S=S_prime
        A=A_prime
    return eps_perstep

def nstep_sarsa(
    env: gym.Env,
    num_steps: int,
    gamma: float,
    epsilon: float,
    step_size: float,
):
    """N-step SARSA

    Args:
        env (gym.Env): a Gym API compatible environment
        num_steps (int): Number of steps
        gamma (float): Discount factor of MDP
        epsilon (float): epsilon for epsilon greedy
        step_size (float): step size
    """
    # n = 4
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    num_episodes = 0
    eps_perstep = []
    n = 4
    
    t=0
    T = math.Inf
    while t < num_steps:
           #initial vals
        S = []
        A = []
        R = [0]
        S.append(env.reset())
        A.append(egreedy_action(Q,S,epsilon))
        done = False
        

    return eps_perstep
    


def exp_sarsa(
    env: gym.Env,
    num_steps: int,
    gamma: float,
    epsilon: float,
    step_size: float,
):
    """Expected SARSA

    Args:
        env (gym.Env): a Gym API compatible environment
        num_steps (int): Number of steps
        gamma (float): Discount factor of MDP
        epsilon (float): epsilon for epsilon greedy
        step_size (float): step size
    """
    # TODO
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    num_episodes = 0
    eps_perstep = [num_episodes]
    #initial vals
    S = env.reset()
    A = egreedy_action(Q,S,epsilon)
    for t in num_steps:
        S_prime, reward, done, _ = env.step(A)
        if done:
            num_episodes+=1
        eps_perstep.append(num_episodes)
        #A_prime = egreedy_action(S_prime)
        max_a = np.random.choice([a for a in range(len(Q[S_prime])) if Q[S_prime][a] == max(Q[S_prime])])
        pi_Q = 0
        for a in range(len(Q[S])):
            if a == max_a:
                pi_Q+=((1-epsilon) + (epsilon/4))*Q[S][a]
            else:
                pi_Q+=(epsilon/4)*Q[S][a]
        Q[S][A] = Q[S][A] + step_size*(reward + gamma*pi_Q - Q[S][A])
        S=S_prime
        A=egreedy_action(Q,S,epsilon)
    return eps_perstep


def q_learning(
    env: gym.Env,
    num_steps: int,
    gamma: float,
    epsilon: float,
    step_size: float,
):
    """Q-learning

    Args:
        env (gym.Env): a Gym API compatible environment
        num_steps (int): Number of steps
        gamma (float): Discount factor of MDP
        epsilon (float): epsilon for epsilon greedy
        step_size (float): step size
    """
    # TODO
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    num_episodes = 0
    eps_perstep = [num_episodes]
    #initial vals
    S = env.reset()
    for t in num_steps:
        A = egreedy_action(Q,S,epsilon)
        S_prime, reward, done, _ = env.step(A)
        if done:
            num_episodes+=1
        eps_perstep.append(num_episodes)
        A_prime = np.random.choice([a for a in range(len(Q[S_prime])) if Q[S_prime][a] == max(Q[S_prime])])
        Q[S][A] = Q[S][A] + step_size*(reward + gamma*Q[S_prime][A_prime] - Q[S][A])
        S=S_prime
    return eps_perstep

def td_prediction(env: gym.Env, gamma: float, episodes, n=1) -> defaultdict:
    """TD Prediction

    This generic function performs TD prediction for any n >= 1. TD(0) corresponds to n=1.

    Args:
        env (gym.Env): a Gym API compatible environment
        gamma (float): Discount factor of MDP
        episodes : the evaluation episodes. Should be a sequence of (s, a, r) tuples or a dict.
        n (int): The number of steps to use for TD update. Use n=1 for TD(0).
    """
    V = defaultdict(float)
    num_episodes = 0
    eps_perstep = []
    
    


def learning_targets(
    V: defaultdict, gamma: float, episodes, n: Optional[int] = None
) -> np.ndarray:
    """Compute the learning targets for the given evaluation episodes.

    This generic function computes the learning targets for Monte Carlo (n=None), TD(0) (n=1), or TD(n) (n=n).

    Args:
        V (defaultdict) : A dict of state values
        gamma (float): Discount factor of MDP
        episodes : the evaluation episodes. Should be a sequence of (s, a, r) tuples or a dict.
        n (int or None): The number of steps for the learning targets. Use n=1 for TD(0), n=None for MC.
    """
    # TODO
    targets = np.zeros(len(episodes))
    if n == None:
        # Monte Carlo target, the discounted sum of future rewards
        for i in range(len(episodes)):
            #collect an episode from list of episodes

            G = 0
            #initialize G to 0 for each episode

            #cycle through episode from the end forward, collecting rewards and multiplying previous G by gamma
            for t in range(len(episodes[i])-1, -1, -1):
                G = gamma * G + episodes[i][t][2]
            #set target for this episode equal to final G value after complete cycle
            targets[i] = G
    elif n == 1:
        #TD(0)
        targets_TD0 = []
        for i in range(len(episodes)):
            temp=[]
            #collect an episode from the episodes
            for t in range(len(episodes)-1):
                #reward received plus the discounted value of the future state
                targets_TD0.append(episodes[i][t][2] + gamma*V[episodes[i][t+1][0]])
    else:
        #TD(n) need to extend to n case
        targets_TDN=[]
        for i in range(len(episodes)):
            temp=[]
            #collect an episode from the episodes
            for t in range(len(episodes)-1):
                #reward received plus the discounted value of the future state
                targets_TD0.append(episodes[i][t][2] + gamma*V[episodes[i][t+1][0]])