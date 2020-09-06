# Crossword

**Description**: The AI in this project solves an optimization problem by generating a solved crossword puzzle based on a given structure, the AI does this by satisfying the three constraints that a crossword puzzle naturally gives us.

Video Demonstration 
--------------------

[![Project 3: Crossword | CS50 AI 202](http://img.youtube.com/vi/0a_oZJ9MgQQ/0.jpg)](https://youtu.be/0a_oZJ9MgQQ)

Background
-----------

In this optimization problem, there are three constraints that must be satisfied for these crosswords to be completed correctly:
1. ***Unary Constraint***: Length of the word. More specifically, the length of the word should not exceed the variable (grid) length.
2. ***Binary Constraint***: Overlapping with neighboring variables. Words that share a grid should have the same value (letter) in that grid.
3. ***Additional Constraint***: No repetition of words.

Below shows an example of what is run on the terminal and what output is obtained.

```
$ python generate.py data/structure1.txt data/words1.txt output.png
```
<img src="https://github.com/amanudde1999/CS50-AI/blob/master/crossword/output.png">.

