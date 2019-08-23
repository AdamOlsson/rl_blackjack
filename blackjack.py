import numpy as np 
from Hand import Hand
import random

class BlackJack():
    def __init__(self):
        self.nA = 2
        self.actions = {0:'Stick', 1:'Hit'}
        self.nS = 19 # Sum of hand from 4 to 21, a hand > 22 is terminal state

        self.policy_shape = (19,10,2,self.nA)
        self.value_shape = (19,10,2)

    def deal_card(self):
        return random.randint(2,11)

    def gen_episode(self, policy):

        episode = []
        player = Hand(hand=[random.randint(2,11), random.randint(2,11)])
        dealer = Hand(hand=[random.randint(2,11), random.randint(2,11)])
        
        # Players turn
        while True:

            state = (player.sum, dealer.hand[0], player.has_usable_ace)
            action = np.argmax(policy[max(22, state[0])-4][state[1]-2][1 if state[2] else 0])

            # Bust
            if player.bust:
                episode.append((state, 0, -1))
                return episode
            # Win or Stick
            elif player.sum == 21 or action == 0:
                break
            else:
                # Hit
                player.add_card(self.deal_card())
                episode.append((state, action, 0))

        # Dealers turn
        while True:
            # Bust
            if dealer.bust:
                episode.append((state, action, 1))
                return episode
            # Dealer win
            elif dealer.sum == 21:
                episode.append((state, action, -1 if not player.sum == 21 else 0))
                return episode
            else:
                if dealer.sum < 17:
                    dealer.add_card(self.deal_card())
                else:
                    episode.append((state, action, max(-1, min(1, player.sum-dealer.sum))))
                    return episode

            


if __name__ == "__main__":
    env = BlackJack()

    policy = np.ones(env.policy_shape) / env.nA

    for i in range(1000):
        #env.gen_episode(policy)
        print(env.gen_episode(policy))
