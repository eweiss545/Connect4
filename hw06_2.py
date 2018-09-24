##
## Part II: Connect Four Play
##

from board import Board
from hw06_1 import Player
import random

def connect_four(player1, player2):
    """ Plays a game of Connect Four between the two specified players,
        and returns the Board object as it looks at the end of the game.
        inputs: player1 and player2 are objects representing Connect Four
                  players (objects of the Player class or a subclass of Player).
                  One player should use 'X' checkers and the other should
                  use 'O' checkers.
    """
    # Make sure one player is 'X' and one player is 'O'.
    # STENCIL CODE, DO NOT CHANGE
    if player1.checker not in 'XO' or player2.checker not in 'XO' \
       or player1.checker == player2.checker:
        print('need one X player and one O player.')
        return None

    # Reset players
    player1.num_moves = 0
    player2.num_moves = 0

    print('Welcome to Connect Four!')
    print()
    board = Board(6, 7)
    print(board)

    while True:
        if process_move(player1, board):
            return board

        if process_move(player2, board):
            return board

##
## Problem 6.2a) process_move
##

def process_move(player,board):
    '''Takes two parameters, a player object and a board object, and
    performs all the steps involved in processing a single move by
    the specified player on the specified board.'''
    p1 = player
    print("%s's turn" % p1) ## Prints Player X's turn, or Player O's turn
    move_column = p1.next_move(board) ## sets column number of user choice
    board.add_checker(p1.checker, move_column) ## adds checker to correct column
    print('')
    print(board)
    if board.is_win_for(p1.checker):
        print('%s wins in %d moves.' % (p1,p1.num_moves))
        print('Congratulations!')
        return True
    else:
        if board.is_full():
            print("It's a tie!")
            return True
        else:
            return False


def test_process_move():
    '''Test for process_move'''
    b = Board(2,4)
    b.add_checkers('001122')
    p1 = Player('X')
    p2 = Player('O')
    p1.test = 1 ## sets the column to 3 in next_move to allow for testing
    p2.test = 1 ## ditto
    ## below, player 1 just won because they added an 'X' to column 3
    assert process_move(p1, b) == True
    ## below, player 2 just won because they added an 'O' to column 3
    assert process_move(p2, b) == True
    b.remove_checker(3)
    b.remove_checker(3)
    assert process_move(p2, b) == False ## player 2 did not win/tie
    ##below, player 1 just made the board full by adding an 'X' to column 3;
    ##tied the game
    assert process_move(p1, b) == True
    ##below, sets the next_move function to its normal state
    ##for non-testing use
    p1.test = 0
    p2.test = 0 ## ditto

test_process_move()



##
## Problem 6.2b) RandomPlayer
##

class RandomPlayer(Player):
    '''A datatype representing a random player in the game of
    connect four; inherits most methods from Player class'''

    def next_move(self,board):
        self.num_moves += 1
        available_col = []
        for col in range(board.width):
            if board.can_add_to(col):
                available_col.append(col)
        column = random.choice(available_col)
        return column

def test_RP_next_move():
    '''A test for random player next move'''
    p1 = RandomPlayer('X')
    p2 = RandomPlayer('O')
    b = Board(2,4)
    b.add_checkers('001223')
    col = p1.next_move(b)
    b.add_checker(p1.checker,col)
    assert col in [1,3] ## only open columns are 1 AND 3
    col2 = p2.next_move(b)
    b.add_checker(p2.checker, col2)
    assert col2 in [1,3] ## only open columns still must be 1 OR 3
    assert b.is_full ## board should now be full


test_RP_next_move()
