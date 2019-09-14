# Reinforcement Learning Part 3

<p>Part 3 of my Reinforcement Learning (RL) series. During this series, I dwell into the field of RL by applying various methods to video games to learn and understand how an algorthm can learn to play by itself. The motivation for doing this series is simply by pure interest and to gain knowledge and experience in the field of Machine Learning.

The litterature follow throughout this series is <em>Reinforcement Learning</em> "An Introduction" by Ricard S. Button and Andrew G. Barto. 
ISBN: 9780262039246
</p>

## Monte Carlo Methods
Up until now, we have assumed that we have a complete knowledgde about the envirnoment and could iterate through each and every state state (DP problems). Monte Carlo Methods (MCM) do not learn through iterating through all states of an envirnoment, it instead learns from <em>experience</em>. By experience we mean just like a human learns through experiences and playing a game. MCM will simulate episodes from a game and try to estimate the value function from the experience. The iterative process of updating a policy as in Value Iteration is also adopted by MCM and is more formely known as General Policy Itereation, or GPI. For now I will stick with episodic games which have a clearly defined started and end, like Blackjack. We also introduce another type of value function dependent on state-action pairs, compared to only dependent on state, called <em>Q(a,s)</em>.

## Monte Carlo Prediction
Just as in Dynamic Programming, we start with methods for estimating the state-value function for a given policy. Here we considered First-visit Monte Carlo predition. We start by generating an episode following policy &pi;. Then for each state in that episode we update the value function with the corresponding state by averaging the returns from all episodes. If we in an episode encounter the same state more than once, we ignore updating the value function after the first time we encounter said state. This is where 'first-visit' comes in. There are also methods for every-visit but they have a slightly different theoretical properties. 

Below is the estimated value function with 500 000 episodes of Blackjack for a policy than has a probaility of 0.8 to Stick if the player hand is above 18 and 0.2 otherwise. The states are defined as a tuple (sum player hand, dealer showing card, usable Ace on hand) and rewards are 1 on win, -1 on bust and 0 otherwise. It is quite clear that if the player has an usable Ace on hand the value of that state is higher which intuitively should be correct since an Ace has the possibility to become a 1 if the hand goes over 21. 
<p align="center"><img src=https://github.com/AdamOlsson/rl_blackjack/blob/master/fv_mc_pred_val_fcn.png></p>
