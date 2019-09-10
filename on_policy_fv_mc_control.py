import gym, collections, matplotlib
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def on_policy_mc_control(env, policy, gamma=0.1, epsilon=1.0, iterations=1000):
    
    Q = collections.defaultdict(float)
    state_actions_count = collections.defaultdict(int)
    returns = collections.defaultdict(float)

    for itr in range(iterations):

        if itr%1000 == 0:
            print('Playing episode {} out of {}.'.format(itr, iterations))

        episode = play_episode(env, policy)
        G = 0

        # encourage exploration at start
        epsilon = max(epsilon*0.99995, 0.01)

        state_actions_in_episode = [(s, a) for (s,a,r) in episode]

        for t, (state, action, reward) in enumerate(episode):
            G = gamma*G + reward

            if not (state, action) in state_actions_in_episode[0:t]:
                returns[(state,action)] += G
                state_actions_count[(state, action)] += 1
                Q[(state,action)] = returns[(state, action)] / state_actions_count[(state, action)]

                best_action = np.argmax([Q[(state, 0)], Q[(state, 1)]])

                for a in range(env.action_space.n): # enumerate action space
                    if a == best_action:
                        policy[state[0], state[1], int(state[2])][a] = 1 - epsilon + epsilon / env.action_space.n
                    else:
                        policy[state[0], state[1], int(state[2])][a] = epsilon / env.action_space.n
    return Q, policy


def play_episode(env, policy):
    episode = []
    state = env.reset()
    while True:
        action = np.random.choice(2, p=policy[state[0], state[1], int(state[2])])
        next_state, reward, done, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if done:
            break
    return episode


def plot_policy(p):

    p_no_ace = p[:,:,0]
    p_have_ace = p[:,:,1]

    best_policy_no_ace = np.argmax(p_no_ace, axis=2)
    best_policy_have_ace = np.argmax(p_have_ace, axis=2)

    fig, ax = plt.subplots(ncols=2, figsize=(20, 20))
    
    ax1, ax2 = ax

    m1 = ax1.matshow(best_policy_no_ace)
    m2 = ax2.matshow(best_policy_have_ace)

    xticks = np.arange(11, 22)
    yticks = np.arange(1, 11)
    # Show all ticks, remove what rows and columns to not to show
    ax1.set_yticks(xticks)
    ax1.set_xticks(yticks)
    ax2.set_yticks(xticks)
    ax2.set_xticks(yticks)

    ax1.set_ylabel('Player sum', fontsize=16)
    ax1.set_xlabel('Dealer showing card', fontsize=16)
    ax2.set_ylabel('Player sum', fontsize=16)
    ax2.set_xlabel('Dealer showing card', fontsize=16)

    ax1.set_title('Policy, no usable ace', fontsize=22)
    ax2.set_title('Policy, with usable ace', fontsize=22)

    fig.colorbar(m1, ax=ax1)
    fig.colorbar(m2, ax=ax2)

    plt.show()


if __name__ == "__main__":
    env = gym.make('Blackjack-v0')

    nA = env.action_space.n
    obs_space = [dim.n for dim in env.observation_space]
    policy_space = [obs_space[0], obs_space[1], obs_space[2], nA]

    policy = np.ones(policy_space) / nA # 50/50 policy

    Q, p = on_policy_mc_control(env, policy, iterations=1000000)

    plot_policy(p)