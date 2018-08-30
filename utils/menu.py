import sys
from utils import game_lib

def print_form(number_of_options):
    print()
    for categories, options in number_of_options.items():
        print(categories + ' :')
        for option in options.items():
            print("{: >5}) {}".format(option[0], option[1]))
    print ("\n0. Quit")

# save subsection answer and then answer
def get_answers_from_user(number_of_options):
    print('-' * 74)
    answers = {}
    for categories, options in number_of_options.items():
        wrong_answer = True
        answers[categories] = input("Please enter answer for {} >>> ".format(categories))
        # Check validity of answer
        while (wrong_answer):
            if answers[categories] == str(0):
                handle_exit_input()
            elif not answers[categories] in number_of_options[categories]:
                answers[categories] = input(
                    "Ooops! Invalid input {} for {}, please enter new  answer >>> ".format(answers[categories],
                                                                                           categories))
                continue
            wrong_answer = False
        answers[categories] = number_of_options[categories][answers[categories]]
    return answers

def handle_exit_input():
    answer = input("Are you sure you want to exit? (y/n)")
    if answer.lower() == 'y':
        sys.exit()
    return
	
def handle_continue_playing():
    answer = input("Do you want to continue playing? (y/n)")
    if answer.lower() == 'y':
        return True
    return False