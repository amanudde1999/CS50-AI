# Minesweeper

**Description**: An AI that can win a game of Minesweeper using propositional logic and inference.

Video Demonstration
-------------------

[![Project 1b: Minesweeper | CS50 AI 2020](http://img.youtube.com/vi/u2G3X_9Ldfo/0.jpg)](https://youtu.be/u2G3X_9Ldfo)

To run:
```
$ python runner.py
```
A pygame window will appear where you can either play the game as you would by yourself or click the 'AI Move' button for the AI to make a single move on the minesweeper grid. One thing to note is that the AI will not always necassarily win, this is because it needs to make a random move at times where it cannot draw out any inferences about where the mines are with its knowledge base at that moment, for example at the start of the minesweeper game it may make several random moves before it can make ones drawn using inference. 

**Project Page:** https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/
