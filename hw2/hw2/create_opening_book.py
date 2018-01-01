import operator
import pickle
import re

NUMBER_OF_GAMES = 70
NUM_OF_MOVES_IN_OPENING_BOOK = 10

def create_file(best_openings, file_name, b_create_file):
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

    if b_create_file:
        with open(file_name, 'wb') as target:
            pickle.dump(dict_seq_to_move, target, protocol=pickle.HIGHEST_PROTOCOL)

    return dict_seq_to_move


def create_gamae_book():
    opening_book_file = open('book.gam', 'r')
    openings = {}

    for line in opening_book_file.readlines():
        game = line[:(NUM_OF_MOVES_IN_OPENING_BOOK * 3)]
        if game in openings:
            openings[game] += 1
        else:
            openings[game] = 1

    best_openings = dict(sorted(openings.items(), key=operator.itemgetter(1), reverse=True)[:NUMBER_OF_GAMES])

    create_file(best_openings, 'opening_book.pkl', True)


def update_dict(dict, line, win):
    if line in dict:
        dict[line] += 1 if win else -1
    else:
        dict[line] = 1 if win else -1


def create_dict_of_best_moves_with_values(best_openings, modulo):
    dict_of_best_moves_with_values = {}

    for key, value in best_openings.items():
        moves = re.split('[+-]', key)[1:]
        moves_con = ""
        counter = 0

        for m in moves:
            if modulo == counter % 2:
                moves_con += m
                counter += 1
                continue
            if moves_con in dict_of_best_moves_with_values:
                if value > dict_of_best_moves_with_values[moves_con][1]:
                    dict_of_best_moves_with_values[moves_con] = (m, value)
            else:
                dict_of_best_moves_with_values[moves_con] = (m, value)
            moves_con += m
            counter += 1

        return dict_of_best_moves_with_values


def create_better_opening_book(b_create_file):
    opening_book_file = open('book.gam', 'r')

    first_player_dict_openings_to_wins = {}
    second_player_dict_openings_to_wins = {}

    for line in opening_book_file.readlines():
        is_tie = line[-5] == '0' and line[-6] == '0'

        if is_tie:
            continue

        update_dict(dict=first_player_dict_openings_to_wins, line=line, win=line[-7] == '+')
        update_dict(dict=second_player_dict_openings_to_wins, line=line, win=line[-7] == '-')

    best_openings_first = dict(
        sorted(first_player_dict_openings_to_wins.items(), key=operator.itemgetter(1), reverse=True)[
        :int(NUMBER_OF_GAMES)])
    best_openings_second = dict(
        sorted(second_player_dict_openings_to_wins.items(), key=operator.itemgetter(1), reverse=True)[
        :int(NUMBER_OF_GAMES)])

    dict_of_best_moves_with_values = create_dict_of_best_moves_with_values(best_openings_first, 1)
    dict_of_best_moves_with_values.update(create_dict_of_best_moves_with_values(best_openings_second, 0))

    dict_seq_to_move = {key: value[0] for key, value in dict_of_best_moves_with_values.items()}

    if b_create_file:
        with open('opening_book_better.pkl', 'wb') as target:
            pickle.dump(dict_seq_to_move, target, protocol=pickle.HIGHEST_PROTOCOL)

    return dict_seq_to_move


if __name__ == '__main__':
    create_gamae_book()
    create_better_opening_book(b_create_file=True)
