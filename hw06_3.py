##
## Part III: AI Player
##

import random
from hw06_2 import *

##
## Problem 6.3) AIPlayer Class
##

class AIPlayer(Player):
    '''A datatype representing a random player in the game of
    connect four; inherits most methods from Player class'''

    def __init__(self, checker, tiebreak, lookahead):
        '''The constructor for objects of type AIPlayer'''
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead

    def __repr__(self):
        '''Overrides the inherited repr method so as to return a string
        representation of object AIPlayer'''
        s = 'Player %s (%s, %d)' % (self.checker, self.tiebreak,self.lookahead)
        return s

    def max_score_column(self,scores):
        '''Takes a list scores containing a score fo each column of
        the board, and returns the column number with the
        maximum score. If two+ columns contain the max score, then this
        function will implement the tiebreak strategy in order to choose
        the column'''
        ## e.g. if scores = [50,50,50,50,50,50,50], return [0,1,2,3,4,5,6]
        ## & if strategy is LEFT, return O, strategy is RIGHT, return 6,
        max_score = max(scores)
        max_score_list = []
        for i in range(len(scores)):
            if scores[i] == max_score:
                max_score_list.append(i)
        if self.tiebreak == 'LEFT':
            return max_score_list[0]
        if self.tiebreak == 'RIGHT':
            return max_score_list[-1]
        if self.tiebreak == 'RANDOM':
            return random.choice(max_score_list)

    def scores_for(self,board):
        '''Takes a board and determines the called AIPlayer's scores
        for the columns in board. Each column is assigned four possible
        scores: -1 (column full), 0 (move results in a loss), 100
        (move results in a win), and 50 (move results in neither win
        nor loss). Method returns a list containing one score per column'''
        scores = [2] * board.width
        for col in range(board.width):
            if board.can_add_to(col) == False:
            ## if the column is full, return -1 for that column
                scores[col] = -1
            elif board.is_win_for(self.checker):
            ## if the player has already won, return 100 for column
                scores[col] = 100
            elif board.is_win_for(self.opponent_checker()):
            ## if the player's opponent has won, return 0 for column
                scores[col] = 0
            elif self.lookahead == 0:
            ## board is neither win nor loss, so at lookahead of 0, every
            ## column must have a score of 50
                scores[col] = 50
            else:
                ## add a checker to the current column
                board.add_checker(self.checker, col)
                ## create an opponent AI with opp checker, same tiebreak,
                ## and lookahead - 1
                new_lookahead = (self.lookahead) - 1
                opp_player = AIPlayer(self.opponent_checker(), self.tiebreak, \
                new_lookahead)
                ##make a recursive call to dermine the scores that opp_player
                ##would give to current board
                opp_scores = opp_player.scores_for(board)
                ## if opponent is losing, we are winning!
                if max(opp_scores) == 0:
                    scores[col] = 100
                ## if opponent is winning, we are losing.. :(
                elif max(opp_scores) == 100:
                    scores[col] = 0
                ## if opponent is neither win/loss, we are neither win/loss
                elif max(opp_scores) == 50:
                    scores[col] = 50
                ## if the opponent has a full column, we have a full column
                elif max(opp_scores) == -1:
                    scores[col] = -1
                board.remove_checker(col)

        return scores

    def next_move(self,board):
        '''Returns the called AIPlayer's judgment of its best possible move;
        output is the column number where it should play next'''
        self.num_moves += 1
        ## get the AI's list of scores for the columns
        AI_scores = self.scores_for(board)
        ## get the column number for the highest score in that list
        ## (depending on method tiebreak)
        column_no = self.max_score_column(AI_scores)
        ## return the column number for the next move!
        return column_no

##
### Testing for AIPlayer class
##

def test_init_repr():
    '''Test for constructor and printing methods'''
    p1 = AIPlayer('X', 'LEFT', 1)
    assert p1.__repr__() == 'Player X (LEFT, 1)'
    p2 = AIPlayer('O', 'RANDOM', 2)
    assert p2.__repr__() == 'Player O (RANDOM, 2)'

test_init_repr()

def test_max_score_column():
    '''Test for max_score_column function'''
    ### testing when all scores are the same
    scores = [50,50,50,50,50,50,50]
    poss_indices = [0,1,2,3,4,5,6]
    p1 = AIPlayer('X', 'LEFT', 1)
    assert p1.max_score_column(scores) == 0
    p1 = AIPlayer('X', 'RIGHT', 1)
    assert p1.max_score_column(scores) == 6
    p1 = AIPlayer('X', 'RANDOM', 1)
    assert p1.max_score_column(scores) in poss_indices
    ### testing with a diverse array of scores
    scores = [-1,100,100,0,0,100,50]
    poss_indices = [1,2,5]
    p1 = AIPlayer('X', 'LEFT', 1)
    assert p1.max_score_column(scores) == 1
    p1 = AIPlayer('X', 'RIGHT', 1)
    assert p1.max_score_column(scores) == 5
    p1 = AIPlayer('X', 'RANDOM', 1)
    assert p1.max_score_column(scores) in poss_indices

test_max_score_column()

def test_scores_for():
    '''Test scores_for function'''
    b = Board(6,7)
    b.add_checkers('1211244445')
    AI_1 = AIPlayer('X', 'LEFT', 0)
    assert AI_1.scores_for(b) == [50, 50, 50, 50, 50, 50, 50]
    AI_2 = AIPlayer('O', 'LEFT', 1)
    assert AI_2.scores_for(b) == [50, 50, 50, 100, 50, 50, 50]
    AI_1 = AIPlayer('X', 'LEFT', 1)
    assert AI_1.scores_for(b) == [50, 50, 50, 50, 50, 50, 50]
    AI_1 = AIPlayer('X', 'LEFT', 2)
    assert AI_1.scores_for(b) == [0, 0, 0, 50, 0, 0, 0]
    AI_1 = AIPlayer('X', 'LEFT', 3)
    assert AI_1.scores_for(b) == [0, 0, 0, 100, 0, 0, 0]
    AI_2 = AIPlayer('O', 'LEFT', 3)
    assert AI_2.scores_for(b) == [50, 50, 50, 100, 50, 50, 50]


test_scores_for()

def test_next_move():
    '''Test next_move function'''
    b = Board(6,7)
    b.add_checkers('1211244445')
    AI_1 = AIPlayer('X', 'LEFT', 0)
    ## scores list looks like this: [50, 50, 50, 50, 50, 50, 50]
    assert AI_1.next_move(b) == 0
    AI_2 = AIPlayer('O', 'RANDOM', 1)
    ## scores list: [50, 50, 50, 100, 50, 50, 50]
    assert AI_2.next_move(b) == 3
    AI_1 = AIPlayer('X', 'RIGHT', 1)
    ## scores list: [50, 50, 50, 50, 50, 50, 50]
    assert AI_1.next_move(b) == 6
    AI_1 = AIPlayer('X', 'LEFT', 2)
    ## scores list: [0, 0, 0, 50, 0, 0, 0]
    assert AI_1.next_move(b) == 3
    AI_1 = AIPlayer('X', 'RIGHT', 3)
    ## scores list: [0, 0, 0, 100, 0, 0, 0]
    assert AI_1.next_move(b) == 3
    AI_2 = AIPlayer('O', 'RANDOM', 3)
    ## scores list: [50, 50, 50, 100, 50, 50, 50]
    assert AI_2.next_move(b) == 3

test_next_move()
