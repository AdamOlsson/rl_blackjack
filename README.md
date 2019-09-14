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


## Monte Carlo Control
Now we know how to make an estimate of the value function and can apply it to the GPI scheme. But first, we know how to evaluate the value function of a policy so how to we improve it? Since we don't have complete knowledge of the system we cant iterate over all actions and states to find the best action. Instead, whenever we iterate through state <em>s</em> in an episode we will have to estimate <em>q(a,s)</em>, i.e the expected reward of taking action <em>a</em> in state <em>s</em>. Estimating the state-action function is done by averaging the returns for each state action pair among all episodes. Then we update our policy with the state-action pair that returns the highest expected rewards. However there is one problem with this, some state-action pairs might never be visited due to that the policy doesn't favor some actions and therefor their expected reward would be non existing This is where the notation of _exploring_ comes in. Letting an algorithm explore allows it to visit more state-action pairs and spread out the experience. We allow an algorithm to explore by setting all probabilities to take action <em>a</em> to non-zero.

Finally we can apply the GPI scheme which here is called Monte Carlo Control.

Below is the final policy for Blackjack after playing 10 000 000 episodes. Some additional methods has been applied here; during an episode whenever we select action, I use something called <em>&epsilon;-greedy</em> policy which means that the greedy actions is selected with probability 1 <em>- &epsilon; + &epsilon;/|A(s)|</em> and a non-greedy action is selected with probability <em>&epsilon;/|A(s)|</em>. This enables exploration which previously mentioned is important so all state-action pairs are visited. The other method used is that <em>&epsilon;</em> starts high to promote exploration at start and decreased episode by episode.

<p align="center"><img src=https://github.com/AdamOlsson/rl_blackjack/blob/master/on_policy_mc_control.png>Resulting policy after 10 000 000 games of Blackjack. Purple = Stick, Yellow = Hit. Note, ignore the vertical purple areas to the left most of each heatmap as well as the horizontal top of the right heatmap. For some reason I could not get rid of them.</p>
