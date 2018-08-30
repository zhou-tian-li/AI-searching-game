from utils import menu, game_lib
import manual_game, automatic_game

# Main menu
def main_menu():
    print("\n-------------------------------- Welcome: --------------------------------")
    available_options = {'Game Selection': {'1': 'Manual Play', '2': 'Automatic AI Play'}}
    menu.print_form(available_options)
    answers = menu.get_answers_from_user(available_options)
    move_to_automatic_or_manual(answers)

def move_to_automatic_or_manual(answers):
    if answers['Game Selection'] == 'Manual Play':
        manual_game.start_game()
    elif answers['Game Selection'] == 'Automatic AI Play':
        automatic_game.start_game()

main_menu()