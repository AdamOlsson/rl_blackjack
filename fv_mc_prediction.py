import gym
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import collections


def first_visit_MC_prediction(env, discount_factor=1.0, iterations = 100):

    vfn = collections.defaultdict(float)
    states_count = collections.defaultdict(int)

    returns = collections.defaultdict(float)

    for i in range(iterations):
        episode = play_episode(env)
        G = 0

        states_in_episode = list(set([sar[0] for sar in episode]))

        for t, (state, action, reward) in enumerate(episode):
            
            G = G*discount_factor + reward

            if not state in states_in_episode[0:t]:
                returns[state] += G
                states_count[state] += 1
                vfn[state] = returns[state] / states_count[state]

    return vfn
            

def play_episode(env):
    episode = []
    state = env.reset()
    while True:
        probs = [0.8, 0.2] if state[0] > 18 else [0.2, 0.8]
        action = np.random.choice(np.arange(2), p=probs)
        next_state, reward, done, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if done:
            break
    return episode

if __name__ == "__main__":
    env = gym.make('Blackjack-v0')

    policy = np.zeros([32,11,2])

    vfn = first_visit_MC_prediction(env, iterations=500000)

    states_0 = np.zeros([32,11])
    states_1 = np.zeros([32,11])
    
    for (s0,s1,s2), v in vfn.items():
        if s2:
            states_1[s0][s1] = v
        else:
            states_0[s0][s1] = v

    fig = plt.figure()
    ax0 = fig.add_subplot(1,2,1, projection='3d')
    ax1 = fig.add_subplot(1,2,2, projection='3d')

    ax0.set_title('No Usable Ace')
    ax1.set_title('Usable Ace')

    ax0.set_xlabel('Sum Player Hand')
    ax1.set_xlabel('Sum Player Hand')

    ax0.set_ylabel('Dealers Showing Card')
    ax1.set_ylabel('Dealers Showing Card')

    x, y = states_0.shape
    X, Y = np.meshgrid(np.arange(x), np.arange(y))

    Z = states_0
    surf0 = ax0.plot_surface( X, Y, Z.T, linewidth=0, antialiased=False)

    Z = states_1
    surf1 = ax1.plot_surface( X, Y, Z.T, linewidth=0, antialiased=False)

    plt.show()
    
