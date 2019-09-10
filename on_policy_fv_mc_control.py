import gym, collections
import numpy as np

def on_policy_mc_control(env, policy, gamma=0.1, epsilon=0.2, iterations=1000):
    
    Q = np.zeros(policy.shape)
    state_actions_count = collections.defaultdict(int)
    returns = collections.defaultdict(float)

    for itr in range(iterations):
        episode = play_episode(env, policy, epsilon)
        G = 0

        state_actions_in_episode = set([(s, a) for (s,a,r) in episode])

        for t, (state, action, reward) in enumerate(episode):
            G = gamma*G + reward

            if not (state, action) in state_actions_in_episode:
                returns[(state,action)] += G
                state_actions_count[(state, action)] += 1
                Q[state[0], state[1], state[2], action] = returns[(state, action)] / state_actions_count[(state, action)]

                most_prob_action = np.argmax(Q[state])

                for i, a in enumerate(Q[state]):
                    if a == most_prob_action:
                        policy[state[0], state[1], int(state[2])][i] = 1 - epsilon + epsilon/len(Q[state])
                    else:
                        policy[state[0], state[1], int(state[2])][i] = epsilon / len(Q[state])
    return Q, policy

# Selecting action with greed might be wrong
def play_episode(env, policy, epsilon):
    episode = []
    state = env.reset()
    while True:
        greedy_action = np.argmax(policy[state[0], state[1], int(state[2])])
        explore_action = 1 - greedy_action # works in this case when there only are 2 actions
        action = np.random.choice([greedy_action, explore_action], p=[1 - epsilon - epsilon/len(policy), epsilon/len(policy)])
        next_state, reward, done, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if done:
            break
    return episode

# Selecting action with greed might be wrong
def play_episode2(env, policy):
    episode = []
    state = env.reset()
    while True:
        action = np.random.choice(2, p=policy[state])
        next_state, reward, done, info = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        if done:
            break
    return episode


if __name__ == "__main__":
    env = gym.make('Blackjack-v0')

    nA = env.action_space.n
    obs_space = [dim.n for dim in env.observation_space]
    policy_space = [obs_space[0], obs_space[1], obs_space[2], nA]

    policy = np.ones(policy_space) / nA # 50/50 policy

    #Q, p = on_policy_mc_control(env, policy)

    #print(play_episode(env, policy))