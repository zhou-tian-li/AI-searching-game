from utils import menu, game_lib
import sys

def start_game():
    games = game_lib.load_all_games_from_data_file('input.txt')
    for game in games:
        board_game= [[], [], []]
        open_list= []
        closed_list = []
        game_lib.populate_board(board_game, game)
        current_slider_position = game_lib.get_starting_position(board_game)
        while(not game_lib.goal_state(board_game)):
            game_lib.print_board(board_game)
            next_move = ask_user_for_next_move(open_list, current_slider_position)
            game_lib.update_board_positions(board_game, current_slider_position, next_move)
            current_slider_position = next_move
            closed_list.append(current_slider_position)
            current_slider_position = game_lib.letter_to_coordinates(next_move)
        game_lib.print_board(board_game)
        print('\nCONGRATULATIONS!!!\nSequence Of Moves: ')
        print(''.join(closed_list))
        with open('output.txt', "a+") as text_file:
            text_file.write(''.join(closed_list) + '\n')
        if(menu.handle_continue_playing() == False):
            sys.exit()

def ask_user_for_next_move(open_list, current_slider_position):
    open_list = game_lib.get_possible_moves(current_slider_position)
    available_options = game_lib.format_open_list(open_list)
    invalid_answer = True
    while invalid_answer:
        answer = input("Please enter next move >>> ")
        if answer in available_options:
            invalid_answer = False
        else:
            print("Oops, invalid input.")
    return answer



