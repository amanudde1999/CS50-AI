from copy import deepcopy
import math

"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turns = 0
    
    for row in board:
        turns+= row.count(EMPTY)
    # Since X plays first it'll be the odd player
    if (turns % 2 != 0):
        return X
    else:
        return O
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    setActions = set()
    
    if (terminal(board) == False):
        # Nested for loop will iterate through the whole matrix/board
        for i in range(3):
            for j in range(3):
                # Find all the unplayed spots on the grid
                if board[i][j] == EMPTY:
                    setActions.add((i,j))
        return setActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if terminal(board):
        raise Exception("The game is over.")
    
    elif action not in actions(board):
        raise Exception("Invalid move.")
    
    else:
        currentPlayer = player(board)
        boardCopy = deepcopy(board)
        i,j = action
        boardCopy[i][j] = currentPlayer

    return boardCopy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    current_player = player(board)

    if board[0][0] == board[0][1] == board[0][2] != None:
        if current_player == O:
            return X
        else:
            return O
    elif board[1][0] == board[1][1] == board[1][2] != None: 
        if current_player == O:
            return X
        else:
            return O
    elif board[2][0] == board[2][1] == board[2][2] != None:
        if current_player == O:
            return X
        else:
            return O
    elif board[0][0] == board[1][0] == board[2][0] != None:
        if current_player == O:
            return X
        else:
            return O
    elif board[0][1] == board[1][1] == board[2][1] != None:
        if current_player == O:
            return X
        else:
            return O
    elif board[0][2] == board[1][2] == board[2][2] != None:
        if current_player == O:
            return X
        else:
            return O
    elif board[0][0] == board[1][1] == board[2][2] != None:
        if current_player == O:
            return X
        else:
            return O
    elif board[0][2] == board[1][1] == board[2][0] != None:
        if current_player == O:
            return X
        else:
            return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Either X or O won
    if winner(board) != None:
        return True
    
    # All cells were filled
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
                
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == X):
        return 1
    
    elif (winner(board) == O): 
        return -1
    
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    
    if board == initial_state():
        return(0,0) 

    if currentPlayer == X:
        # The X (maximiser) knows that O will try to minimize
        v = -math.inf
        optimalMove = None
        for action in actions(board):
            min_Value = minValue(result(board, action))
            if min_Value > v:
                v = min_Value
                optimalMove = action

    elif currentPlayer == O:
        v = math.inf
        optimalMove = None
        for action in actions(board):
            max_Value = maxValue(result(board, action))
            if max_Value < v:
                v = max_Value
                optimalMove = action            
    return optimalMove
    
def maxValue(board):
    """
    Returns the best possible outcome for X on a board (maximiser)
    Implemented from the lecture notes pseudocode
    """
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    
    return v


def minValue(board):
    """
    Returns the best possible outcome for O on a board (minimiser)
    Implemented from the lecture notes pseudocode
    """
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, maxValue(result(board, action)))

    return v
