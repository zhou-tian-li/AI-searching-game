from utils import menu
import heapq
import copy

SAMPLE_BOARD = [['A', 'B', 'C', 'D', 'E'], ['F', 'G', 'H', 'I', 'J'], ['K', 'L', 'M', 'N', 'O']]
COORDINATE_POSITION = {'A': (0, 0), 'B': (0, 1), 'C': (0, 2), 'D': (0, 3), 'E': (0, 4),
                       'F': (1, 0), 'G': (1, 1), 'H': (1, 2), 'I': (1, 3), 'J': (1, 4),
                       'K': (2, 0), 'L': (2, 1), 'M': (2, 2), 'N': (2, 3), 'O': (2, 4)}
LETTER_POSITION = {(0, 0): 'A', (0, 1): 'B', (0, 2): 'C', (0, 3): 'D', (0, 4): 'E',
                   (1, 0): 'F', (1, 1): 'G', (1, 2): 'H', (1, 3): 'I', (1, 4): 'J',
                   (2, 0): 'K', (2, 1): 'L', (2, 2): 'M', (2, 3): 'N', (2, 4): 'O'}

ID = 0

def populate_board(new_board, game_line_from_input_data):
    row_1 = game_line_from_input_data[:10].split()
    row_2 = game_line_from_input_data[10:20].split()
    row_3 = game_line_from_input_data[20:].split()
    new_board[0] = row_1
    new_board[1] = row_2
    new_board[2] = row_3


def load_all_games_from_data_file(file_directory):
    with open (file_directory) as f:
        all_games = f.readlines ()
    return all_games


def get_starting_position(board):
    for i in range (0, 3):
        for j in range (0, 5):
            if board[i][j] == 'e':
                return (i, j)
    return None

def letter_to_coordinates(letter_board_move):
    return COORDINATE_POSITION[letter_board_move]

def goal_state(new_board):
    return new_board[0] == new_board[2]


def get_possible_moves(slider_postion):
    posx, posy = slider_postion
    next_possible_moves = [(x, y) for x, y in ((posx - 1, posy), (posx + 1, posy), (posx, posy - 1), (posx, posy + 1))
                           if 0 <= x < 3 and 0 <= y < 5]
    # we get our coordinates for our slider (posx, posy)
    # we know that we can go up, down, left, right  ie.  (posx - 1, posy), (posx + 1, posy), (posx, posy - 1), (posx, posy + 1)
    # and that the new moves have to be WITHIN the board limits ie. 0 <= x < 3 and 0 <= y < 5
    return next_possible_moves


def print_board(board_game):
    print ("\nCurrent Game: \t\t\t Moves Table:")
    board = "|{}|{}|{}|{}|{}|\t\t\t|{}|{}|{}|{}|{}|"
    for i in range (0, 3):
        print (board.format (*board_game[i], *SAMPLE_BOARD[i]))


def format_open_list(open_list):
    options = []
    for possible_move in open_list:
        options.append (LETTER_POSITION[possible_move])
    return options


def update_board_positions(board_game, slider_coordinates, next_move_letter):
    next_move_coordinates = COORDINATE_POSITION[next_move_letter]
    # make the move
    make_move(board_game, slider_coordinates, next_move_coordinates)


def make_move(board_game, slider_coordinates, next_move_coordinates):
    board_game[slider_coordinates[0]][slider_coordinates[1]] = board_game[next_move_coordinates[0]][
        next_move_coordinates[1]]
    board_game[next_move_coordinates[0]][next_move_coordinates[1]] = 'e'


def get_children_nodes(parent_node, i, j, k, z, totalNumberOfVisited2):
    children_nodes = []
    possible_moves = get_possible_moves(parent_node['slider_pos'])
    # create a new child node for each possible move of the parent node
    for move in possible_moves:
        global ID
        ID = ID + 1
        new_node = {'board': copy.deepcopy (parent_node['board']), 'id': ID,
                    'parent_id': parent_node['id'], 'heuristic_value': None, 'parent_move': LETTER_POSITION[move],
                    'slider_pos': move, 'cost': parent_node['cost'] + z}
        make_move(new_node['board'], parent_node['slider_pos'], move)
        if totalNumberOfVisited2 > 1300:
            new_node['heuristic_value'] = get_heuristic_value (new_node['board'], i, j, k) + new_node['cost'] + 40
        elif new_node['cost'] > 7:
            new_node['heuristic_value'] = get_heuristic_value (new_node['board'], i, j, k) + new_node['cost'] + 90
        elif new_node['cost'] > 5:
            new_node['heuristic_value'] = get_heuristic_value (new_node['board'], i, j, k) + new_node['cost'] + 80
        elif new_node['cost'] > 3:
            new_node['heuristic_value'] = get_heuristic_value (new_node['board'], i, j, k) + new_node['cost'] + 40
        else:
            new_node['heuristic_value'] = get_heuristic_value(new_node['board'], i, 1, k)
        children_nodes.append(new_node)
    return children_nodes

def add_children_to_open_list(children_nodes, open_list, closed_list):
    for child_node in children_nodes:
        already_in_closed_or_open = already_visited(child_node, open_list, closed_list)
        if already_in_closed_or_open:
            continue
        heapq.heappush(open_list, (child_node['heuristic_value'], child_node['id'], child_node))

def already_visited(child_node, open_list, closed_list):
    for elm_index, elm in enumerate(open_list):
        if child_node['board'] == elm[2]['board']:
            if child_node['cost'] < elm[2]['cost']:
                pass
                del open_list[elm_index]
                heapq.heapify (open_list)
                heapq.heappush (open_list, (child_node['heuristic_value'], child_node['id'], child_node))
            return True
    for elm in closed_list:
        if child_node['board'] == elm['board']:
            if child_node['cost'] < elm['cost']:
                pass
                heapq.heappush (open_list, (child_node['heuristic_value'], child_node['id'], child_node))
            return True
    return False


def get_heuristic_value(board, i, j, k):
    heuristic = 100
    for x in range(5):
        if x in range(1,4):
            if board[0][x-1] == board[2][x] or board[0][x] == board[2][x] or board[0][x+1] == board[2][x]:
                heuristic -= k
            elif board[1][x-1] == board[2][x] or board[1][x] == board[2][x] or board[1][x+1] == board[2][x]:
                heuristic -= k
            elif board[2][x - 1] == board[2][x] or board[2][x + 1] == board[2][x]:
                heuristic -= k

            elif board[2][x-1] == board[2][x] or board[2][x] == board[0][x] or board[2][x+1] == board[0][x]:
                heuristic -= k
            elif board[1][x-1] == board[0][x] or board[1][x] == board[0][x] or board[1][x+1] == board[0][x]:
                heuristic -= k
            elif board[0][x - 1] == board[0][x] or board[0][x + 1] == board[0][x]:
                heuristic -= k
        elif x == 0:
            if board[0][x] == board[2][x] or board[0][x+1] == board[2][x]:
                heuristic -= k
            elif board[1][x] == board[2][x] or board[1][x + 1] == board[2][x]:
                heuristic -= k
            elif board[2][x+1] == board[2][x]:
                heuristic -= k

            if board[2][x] == board[0][x] or board[2][x+1] == board[0][x]:
                heuristic -= k
            elif board[1][x] == board[0][x] or board[1][x + 1] == board[0][x]:
                heuristic -= k
            elif board[0][x+1] == board[0][x]:
                heuristic -= k
        elif x == 4:
            if board[0][x] == board[2][x] or board[0][x-1] == board[2][x]:
                heuristic -= k
            elif board[1][x] == board[2][x] or board[1][x - 1] == board[2][x]:
                heuristic -= k
            elif board[2][x-1] == board[2][x]:
                heuristic -= k

            if board[2][x] == board[0][x] or board[2][x-1] == board[0][x]:
                heuristic -= k
            elif board[1][x] == board[0][x] or board[1][x - 1] == board[0][x]:
                heuristic -= k
            elif board[0][x-1] == board[0][x]:
                heuristic -= k
        if board[0][x] == board[2][x]:
            heuristic -= j
    return heuristic

def get_solution_path(closed_list, goal_state):
    solution_path = []
    solution_path.append (goal_state['parent_move'])
    parent_node_id = goal_state['parent_id']
    for elm in reversed(closed_list):
        if parent_node_id == 0:
            return solution_path
        if elm['id'] == parent_node_id:
            solution_path.insert(0, elm['parent_move'])
            parent_node_id = elm['parent_id']
