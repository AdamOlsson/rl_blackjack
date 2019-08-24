from blackjack import BlackJack
import numpy as np
import collections


def first_visit_MC_prediction(env, policy, discount_factor=1.0, iterations = 100):

    vfn = collections.defaultdict(float)
    states_count = collections.defaultdict(int)

    returns = collections.defaultdict(float)

    for i in range(iterations):
        episode = env.gen_episode(policy)
        G = 0

        states_in_episode = list(set([sar[0] for sar in episode]))

        for t, (state, action, reward) in enumerate(episode):
            
            G = G*discount_factor + reward

            if not state in states_in_episode[0:t]:
                returns[state] += G
                states_count[state] += 1
                vfn[state] = returns[state] / states_count[state]
    return vfn
            

if __name__ == "__main__":
    env = BlackJack() 

    policy = np.zeros([env.nS, env.nA])

    for s0 in range(4,23):
        for s1 in range(2,12):
            for s2 in range(0,2):
                if s0 < 20: # hit on player sum < 20
                    policy[env.state_to_index((s0, s1, s2))] = np.array([0,1])
                else:
                    policy[env.state_to_index((s0, s1, s2))] = np.array([1,0])

                #print('({}, {}, {})'.format(s0,s1,s2), policy[env.state_to_index((s0, s1, s2))])

    vfn = first_visit_MC_prediction(env, policy, iterations=500000)

    for k, v in vfn.items():
        print('{} : {}'.format(k,v))
