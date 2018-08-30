from random import shuffle
a = 'g b r w p p y r b g w e r r y'

arr = a.split()

for i in range (10):
    shuffle(arr)
    with open('generated_games.txt', "a+") as text_file:
        text_file.write(' '.join(arr) + '\n')
