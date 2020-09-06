# Nim

**Description**: In this project, an AI trains to play Nim through Reinforcement learning by playing a specified amount of training games and then you can play the AI.

Video Demonstration 
-------------------
[![Project 4b: Nim | CS50 AI 2020](http://img.youtube.com/vi/BmO0kIl5oOo/0.jpg)](https://youtu.be/BmO0kIl5oOo)

Background
-------------

The concept of this game of Nim is such that you have all these matches in different piles as shown below and you can take as many matches from one pile as you want per turn and whoever is left to take the last match is the loser. 
Now, with the more games that the AI plays, the more proficient it becomes in this game and harder to beat. This is due to the Q-learning formula, where the AI tries to learn a reward for every (state,action) pair and an action that results
in a loss has a reward of -1, actions that results in the other player losing is a reward of 1 and an action that results in the game continuing has an immediate reward of zero but may have some future reward.

```
              Q-learning formula: Q(s,a) <- Q(s,a) + alpha(newValueEstimate - oldValueEstimate)
```
where s is the state, a is the action, alpha is the learning rate (how much we value new information compared to information we already have), newValueEstimate is the sum of the reward recieved for the current action **and** the estimate of all future rewards 
that may be recieved in the future and oldValueEstimate is just the existing value for Q(s,a). Now when we keep applying this with more training games, the AI eventually learns which actions are better in any state.

<img src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/NimGame.svg/330px-NimGame.svg.png">

How to play the game and run the code:
 ```
 $ python play.py
 Playing training game 1
 ...
 Playing training game n (n being the # of games you choose)
 
Piles:
Pile 0: 1
Pile 1: 3
Pile 2: 5
Pile 3: 7

 ```
 Then just choose a pile and the number of matches you want to take away.
 
 **Project Page:** https://cs50.harvard.edu/ai/2020/projects/4/nim/#:~:text=Piles:Pile%200:%201Pile%201:%203Pile%202:%205Pile%203:%207
 
 **Nim Image**: https://en.wikipedia.org/wiki/Nim
