##
## Part I: Connect Four Setup
##

from board import Board

##
## Problem 6.1) A Connect Four Player Class
##

class Player:
    '''A datatype representing a player in the game of connect four'''

    def __init__(self,checker):
        '''the constructor for objects of type Player'''
        self.checker = checker ## where checker must either be an X or O
        self.num_moves = 0
        self.test = 0 ## adding in this attribute so I can specify input for testing later

    def __repr__(self):
        '''Returns a string represention for a Player object'''
        s = 'Player %s' % self.checker
        return s

    def opponent_checker(self):
        '''Returns the checker of the Player's opponent, assuming
        the Player has a checker that is either X or O'''
        if self.checker == 'X':
            return 'O'
        elif self.checker == 'O':
            return 'X'

    def next_move(self,board):
        '''Gets input from user where they want to make the next move, and
        returns the column number if it is a valid move'''
        if self.test == 1:
        ## allows me to set the input rather than take input from user for testing
            column = 3 ## sets the column to 3 for my tests
        else:
            column = int(input('Enter a column: '))
        while board.can_add_to(column) == False:
            print('Try again!')
            column = int(input('Enter a column: '))
        self.num_moves += 1
        return column


## Test functions

def test_init_repr():
    '''Test for constructor and print methods'''
    p1 = Player('X')
    assert p1.__repr__() == 'Player X'
    p2 = Player('O')
    assert p2.__repr__() == 'Player O'

test_init_repr()

def test_opponent_checker():
    '''test for opponent_checker method'''
    p1 = Player('X')
    p2 = Player('O')
    assert p1.opponent_checker() == 'O', "usual case failed"
    assert p2.opponent_checker() == 'X', "usual case failed"


test_opponent_checker()


def test_next_move():
    '''Test for next_move normal player'''
    p1 = Player('X')
    p1.test = 1 ## sets the column number to 3 in my next_move function for testing
    b = Board(6,7)
    assert p1.next_move(b) == 3
    p1.test = 0 ## returns the next_move function to its normal state for non-testing use

test_next_move()
