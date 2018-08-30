from utils import menu, game_lib
import heapq
import timeit

def start_game():
    for file_number in range(1,5):
        games = game_lib.load_all_games_from_data_file ('input{}.txt'.format(file_number))
        # features' weights
        i = 1
        k = 5
        j = 5
        z = 1
        total_solution_paths_length = 0
        for game in games:
            # set up root node
            total_number_of_visited_nodes = 0
            start = timeit.default_timer()
            node = {'board': [[], [], []], 'id': 0,'parent_id': 0, 'heuristic_value': 0, 'parent_move': None, 'slider_pos': None, 'cost': 0}
            game_lib.populate_board (node['board'], game)
            current_slider_position = game_lib.get_starting_position (node['board'])
            node['slider_pos'] = current_slider_position
            # start game
            visited = node
            open_list = []                # priority queue based on heuristic value
            closed_list = []
            while (not game_lib.goal_state (visited['board'])):
                children_nodes = game_lib.get_children_nodes(visited, i, j, k, z, total_number_of_visited_nodes)
                game_lib.add_children_to_open_list(children_nodes, open_list, closed_list)
                closed_list.append(visited)
                visited = heapq.heappop(open_list)[2]
                total_number_of_visited_nodes += 1

            goal_state = visited
            solution_path = game_lib.get_solution_path(closed_list, goal_state)
            total_solution_paths_length += len (solution_path)
            end = timeit.default_timer()

            with open('output{}.txt'.format(file_number), "a+") as text_file:
                text_file.write(''.join(solution_path) + '\n' + str(int((end-start)*1000)) + 'ms' + '\n')

            display_moves_of_solved_game (game, solution_path)

        with open('output{}.txt'.format(file_number), "a+") as text_file:
            text_file.write(str(total_solution_paths_length))

    menu.handle_exit_input()

def display_moves_of_solved_game(game, solution_path):
        board_game= [[], [], []]
        closed_list = []
        game_lib.populate_board(board_game, game)
        current_slider_position = game_lib.get_starting_position(board_game)
        i = 0
        while(not game_lib.goal_state(board_game)):
            game_lib.print_board(board_game)
            next_move = solution_path[i]
            if (i < len(solution_path)):
                print('\nMove to play: ' + solution_path[i])
            i += 1
            game_lib.update_board_positions(board_game, current_slider_position, next_move)
            current_slider_position = game_lib.letter_to_coordinates(next_move)
        game_lib.print_board(board_game)
        print('\nCONGRATULATIONS!!!\nSequence Of Moves: ')
        print(''.join(solution_path))