# cs50ai-nim

Write an AI that teaches itself to play Nim through reinforcement learning.

This repository is part of my solution to the assignment set by cs50ai.

## STANDARD OUTPUT

      $ python play.py
      Playing training game 1
      Playing training game 2
      Playing training game 3
      ...
      Playing training game 9999
      Playing training game 10000
      Done training

      Piles:
      Pile 0: 1
      Pile 1: 3
      Pile 2: 5
      Pile 3: 7

      AI's Turn
      AI chose to take 1 from pile 2.

## ASSIGNMENT

Complete the implementation of get_q_value, update_q_value, best_future_reward, and choose_action in nim.py. For each of these functions, any time a function accepts a state as input, you may assume it is a list of integers. Any time a function accepts an action as input, you may assume it is an integer pair (i, j) of a pile i and a number of objects j.

The get_q_value function should accept as input a state and action and return the corresponding Q-value for that state/action pair.

      - Recall that Q-values are stored in the dictionary self.q. The keys of self.q should be in the form of (state, action) pairs, where state is a tuple of all piles sizes in order, and action is a tuple (i, j) representing a pile and a number.
      - If no Q-value for the state/action pair exists in self.q, then the function should return 0.


The update_q_value function takes a state state, an action action, an existing Q value old_q, a current reward reward, and an estimate of future rewards future_rewards, and updates the Q-value for the state/action pair according to the Q-learning formula.

      - Recall that the Q-learning formula is: Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)
      - Recall that alpha is the learning rate associated with the NimAI object.
      - The old value estimate is just the existing Q-value for the state/action pair. The new value estimate should be the sum of the current reward and the estimated future reward.


The best_future_reward function accepts a state as input and returns the best possible reward for any available action in that state, according to the data in self.q.

      - For any action that doesn’t already exist in self.q for the given state, you should assume it has a Q-value of 0.
      - If no actions are available in the state, you should return 0.


The choose_action function should accept a state as input (and optionally an epsilon flag for whether to use the epsilon-greedy algorithm), and return an available action in that state.

      - If epsilon is False, your function should behave greedily and return the best possible action available in that state (i.e., the action that has the highest Q-value, using 0 if no Q-value is known).
      - If epsilon is True, your function should behave according to the epsilon-greedy algorithm, choosing a random available action with probability self.epsilon and otherwise choosing the best action available.
      - If multiple actions have the same Q-value, any of those options is an acceptable return value.
