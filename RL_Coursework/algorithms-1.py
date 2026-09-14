import gym
from typing import Callable, Tuple
from collections import defaultdict
from tqdm import trange
import numpy as np
from policy import create_blackjack_policy, create_epsilon_policy


def generate_episode(env: gym.Env, policy: Callable, es: bool = False):
    """A function to generate one episode and collect the sequence of (s, a, r) tuples

    This function will be useful for implementing the MC methods

    Args:
        env (gym.Env): a Gym API compatible environment
        policy (Callable): A function that represents the policy.
        es (bool): Whether to use exploring starts or not
    """
    episode = []
    state = env.reset()
    max_ticks=459
    while True:
        if es and len(episode) == 0:
            action = env.action_space.sample()
        else:
            action = policy(state)
            print(f"action: {action}")
        next_state, reward, done, _ = env.step(action)
        episode.append((state, action, reward))
        if done:
            break
        state = next_state
        if len(episode) == max_ticks:
            break
    return episode


def on_policy_mc_evaluation(
    env: gym.Env,
    policy: Callable,
    num_episodes: int,
    gamma: float,
) -> defaultdict:
    """On-policy Monte Carlo policy evaluation. First visits will be used.

    Args:
        env (gym.Env): a Gym API compatible environment
        policy (Callable): A function that represents the policy.
        num_episodes (int): Number of episodes
        gamma (float): Discount factor of MDP

    Returns:
        V (defaultdict): The values for each state. V[state] = value.
    """
    # We use defaultdicts here for both V and N for convenience. The states will be the keys.
    V = defaultdict(float)
    N = defaultdict(int)

    for _ in trange(num_episodes, desc="Episode"):
        #print("__________NEW EPISODE___________")
        episode = generate_episode(env, policy)
        #print(episode)
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            # TODO Q3a
            # Update V and N here according to first visit MC
            #print(f"t: {t}")
            #print(f"G: {G}")
            G = gamma*G + episode[t][2]
            N[episode[t][0]]+=1
            first_visit = True
            #searching upward through episode to current time step t looking for the state of time step t
            #if it finds one before current step t, then it is not the first-visit
            for t_ in range(t):
                if episode[t][0] == episode[t_][0]:
                    first_visit = False
            if first_visit:
                V[episode[t][0]] = V[episode[t][0]] + (G - V[episode[t][0]]) / N[episode[t][0]]
    return V


def on_policy_mc_control_es(
    env: gym.Env, num_episodes: int, gamma: float
) -> Tuple[defaultdict, Callable]:
    """On-policy Monte Carlo control with exploring starts for Blackjack

    Args:
        env (gym.Env): a Gym API compatible environment
        num_episodes (int): Number of episodes
        gamma (float): Discount factor of MDP
    """
    # We use defaultdicts here for both Q and N for convenience. The states will be the keys and the values will be numpy arrays with length = num actions
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    N = defaultdict(lambda: np.zeros(env.action_space.n))

    # If the state was seen, use the greedy action using Q values.
    # Else, default to the original policy of sticking to 20 or 21.
    policy = create_blackjack_policy(Q)

    for _ in trange(num_episodes, desc="Episode"):
        #Q3b
        # Note there is no need to update the policy here directly.
        # By updating Q, the policy will automatically be updated.
        
        episode = generate_episode(env, policy, es=True)
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            G = gamma*G + episode[t][2]
            N[episode[t][0]][episode[1]]+=1
            first_visit = True
            for t_ in range(t):
                if episode[t][:2] == episode[t_][:2]:
                    first_visit = False
            if first_visit:
                Old_Q = Q[episode[t][0]][episode[1]]
                Q[episode[t][0]][episode[1]] = Old_Q + (G - Old_Q) / (N[episode[t][0]][episode[1]])
                
    return Q, policy


def on_policy_mc_control_epsilon_soft(
    env: gym.Env, num_episodes: int, gamma: float, epsilon: float
):
    """On-policy Monte Carlo policy control for epsilon soft policies.

    Args:
        env (gym.Env): a Gym API compatible environment
        num_episodes (int): Number of episodes
        gamma (float): Discount factor of MDP
        epsilon (float): Parameter for epsilon soft policy (0 <= epsilon <= 1)
    Returns:

    """
    Q = defaultdict(lambda: np.zeros(env.action_space.n))
    N = defaultdict(lambda: np.zeros(env.action_space.n))
    policy = create_epsilon_policy(Q, epsilon)

    returns = np.zeros(num_episodes)
    for _ in trange(num_episodes, desc="Episode", leave=False):
        # TODO Q4
        # For each episode calculate the return
        # Update Q
        #print(f"generating episode {_}")
        episode = generate_episode(env, policy)
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            G = gamma*G + episode[t][2]
            N[episode[t][0]][episode[1]]+=1
            first_visit = True
            for t_ in range(t):
                if episode[t][:2] == episode[t_][:2]:
                    first_visit = False
            if first_visit:
                Old_Q = Q[episode[t][0]][episode[1]]
                Q[episode[t][0]][episode[1]] = Old_Q + (G - Old_Q) / (N[episode[t][0]][episode[1]]) 
            returns[_]=G
        # Note there is no need to update the policy here directly.
        # By updating Q, the policy will automatically be updated.

    return returns
