import operator
import pickle
import re
from Reversi.consts import *

NUMBER_OF_GAMES = 70

def create_gamae_book():
    opening_book_file = open('book.gam', 'r')
    openings = {}

    for line in opening_book_file.readlines():
        game = line[:(NUM_OF_MOVES_IN_OPENING_BOOK*3)]
        if game in openings:
            openings[game] += 1
        else:
            openings[game] = 1

    best_openings = dict(sorted(openings.items(), key=operator.itemgetter(1), reverse=True)[:NUMBER_OF_GAMES])

    dict_of_best_moves_with_values = {}

    for key, value in best_openings.items():
        moves = re.split('[+-]', key)[1:]
        moves_conc = ""

        for m in moves:
            if moves_conc in dict_of_best_moves_with_values:
                if value > dict_of_best_moves_with_values[moves_conc][1]:
                    dict_of_best_moves_with_values[moves_conc] = (m, value)
            else:
                dict_of_best_moves_with_values[moves_conc] = (m, value)
            moves_conc += m

    dict_seq_to_move = {key: value[0] for key, value in dict_of_best_moves_with_values.items()}

    with open('opening_book.pkl', 'wb') as target:
        pickle.dump(dict_seq_to_move, target, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    create_gamae_book()
