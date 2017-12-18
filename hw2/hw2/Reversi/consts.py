
#==============================================================================
# Game pieces
# - EM is an empty location on the board.
#==============================================================================
EM = ' '

X_PLAYER = 'X'
O_PLAYER = 'O'
TIE = 'tie'

#===============================================================================
# Board Shape
#===============================================================================
BOARD_ROWS = BOARD_COLS = 8

# The Opponent of each Player
OPPONENT_COLOR = {
    X_PLAYER: O_PLAYER,
    O_PLAYER: X_PLAYER
}

#===============================================================================
# Other consts
#===============================================================================

NUM_OF_MOVES_IN_OPENING_BOOK = 10
PERCENTAGE_OF_TIME_TO_SPLIT_EQUALY = 0.9
PERCENTAGE_OF_TIME_TO_SPLIT_NOT_EQUALY = 1 - PERCENTAGE_OF_TIME_TO_SPLIT_EQUALY
