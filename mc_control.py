import gym, collections
import numpy as np

## TODO: CURRENTLY BROKEN
def mc_es(env, gamma=0.1):
    policy = np.ones([32,11,2,env.action_space.n]) / env.action_space.n

    Q = collections.defaultdict(float)
    state_action_count = collections.defaultdict(int)
    returns = collections.defaultdict(float)

    while True:
        # choose S0 and A0 and random
        # How do i start an episode from selected state?
        episode = play_episode(env, policy=policy)
        G = 0

        states_in_episode = list(set([sar[0] for sar in episode]))
        for t, (state, action, reward) in enumerate(episode):
            G = gamma*G + reward

            if not state in states_in_episode[0:t]:
                returns[state, action] += G
                state_action_count[state, action] += 1
                Q[state, action] = returns[state, action] / state_action_count[state, action]
                policy[state[0], state] = np.argmax(Q[state, action])

    return 0

# TODO: Add policy
def play_episode(env, policy=[]):
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

    mc_es()