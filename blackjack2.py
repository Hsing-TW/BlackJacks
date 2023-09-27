'''create a Score function with total and soft_ace_count attributes.'''
'''use namedtuple to create Stand.'''

from collections import defaultdict, namedtuple
from functools import total_ordering
import random
import sys
import csv


Score = namedtuple('Score', 'total, soft_ace_count')
Stand = namedtuple('Stand', 'stand, total')

def get_card():
    return random.randint(1,13)

def score(cards):
    total = 0
    soft_ace_count = 0

    for card in cards:
        if card == 1:
            soft_ace_count += 1
            total += 11
        elif card >= 10:
            total += 10
        else:
            total += card
    
    while total > 21 and soft_ace_count > 0:
        total -= 10
        soft_ace_count -=1
    return Score (total, soft_ace_count)


'''Stand: use boolean to indicate whether stand or not. 
Total: represents final total score.'''
def stand(stand_on_value, stand_on_soft, cards):
    total, soft_ace_count = score(cards)

    is_stand = False

    if total < stand_on_value:
        is_stand = False
    elif total > stand_on_value:
        is_stand = True
    elif stand_on_soft:
        is_stand = True
    elif soft_ace_count:
        is_stand = True
    
    return Stand(is_stand, total)


'''create the play_hand function to read total values.'''
'''if total>22, return 22. if total < 22, return actual value.'''

def play_hand(stand_on_value, stand_on_soft):
    cards = [get_card(), get_card()]

    stand_object = stand(stand_on_value, stand_on_soft, cards)

    while not stand_object.stand:
        cards.append(get_card())
        stand_object = stand(stand_on_value, stand_on_soft, cards)

    return stand_object.total if stand_object.total <22  else 22



def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <num-simulations>")
        exit(1)

    try:
        simulation_time = int(sys.argv[1])
    except ValueError as e:
        print(e)
        exit(1)

    score_percentages = []

    '''loop stand_on_value(13-20) and stand_on_soft, stand_on_hard'''
    '''run the specific number of simulations for each strategy.'''
    '''track the number of simulations in each total value.'''
    '''use defaultdict to count the number of hands. (play_hand function)'''

    for i in range(13, 21):
        for j in [False, True]:
            row_simulation_result = defaultdict(float)

            for _ in range(simulation_time):
                final_score = play_hand(i, j)
                row_simulation_result[final_score] += 1

            row_result = ["0.00"] * 11
            row_result[0] = f"H{i}" if not j else f"S{i}"
            for value, time in row_simulation_result.items():
                percentage = row_simulation_result[value] / simulation_time * 100
                row_result[value - 12] = f"{round(percentage, 2):.2f}"

            score_percentages.append(row_result)

    '''provide output using csv.writer'''
    result_writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    header_row = ["STRATEGY", "13", "14", "15", "16", "17", "18", "19", "20", "21", "BUST"]
    result_writer.writerow(header_row)
    result_writer.writerows(score_percentages)


if __name__ == '__main__':
    main()


    