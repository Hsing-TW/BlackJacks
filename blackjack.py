import random
from xml.dom.minidom import CharacterData

'''Return a random value between 1 and 13.'''
def get_card():
    return random.randit(1,13)

'''1 =ace, 2-10 are number cards, 11,12,13 are jack,queen,king'''
'''consider the situation when the card number is 1 (ace) and 11,12,13 (greater than 10.)'''

def score(cards):
    total = 0
    soft_ace_count = 0
    
    for card in cards:
        
        if card == 1:
            soft_ace_count += 1
            total += 11
        
        elif card > 10:
            total += 10

        else:
            total += card

    while total > 21 and soft_ace_count > 0:
        total -= 10
        soft_ace_count -= 1

    return (total,soft_ace_count)


'''Boolen value indicating wether the player will stand on a 'soft' hand or 'hard' hand.'''
'''True : if the player will 'stand' on the hand. / False otherwise. '''
'''List of integer to represent the cards in Blackjacks hands.'''
'''return boolen values.'''

def stand(stand_on_value, stand_on_soft, cards):
    total, soft_ace_count = score(cards)

    if total < stand_on_value:
        return False
    
    elif total > stand_on_value:
        return True

    if stand_on_soft or not soft_ace_count:
        return True

    return False


''' First: an integer to run (greater than 0.) '''
''' Second: int between 1 and 20, these are stand-on value.'''
''' Third: soft/hard. (choose the strategy.)'''

''' ValueError if somthing is incorrect. Also convert the data from str to desired data type.'''

'''Loop for num-simulations: List for two cards and keep adding cards. 
    The list will use 'get_card' function. 
    Add values to the 'stand' function.'''

'''Output should be the percentage of stimulations.'''