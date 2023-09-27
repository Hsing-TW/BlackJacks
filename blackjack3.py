import random
import sys
import csv

'''class that encapsulates a blackjack hand.'''
class Hand:
    
    '''pass in a list of card integers. if none: empty list, others: call total and soft_ace_count'''
    def __init__(self, cards=None):
        self.cards = []
        self.total = 0
        self.soft_ace_count = 0

        if cards is not None:
            for card in cards:
                self.cards.append(card)
                self.score()

    '''return a string representing the hand.'''
    def __str__(self):
        return f"cards: [{', '.join(self.cards)}], total: {self.total}, soft_ace_count: {self.soft_ace_count}"

    '''Randomly select card and call score method.'''
    def add_card(self):
        self.cards.append(random.randint(1, 13))
        self.score()

    '''return True if Hand represent Blackjack.'''
    def is_blackjack(self):
        if len(self.cards) != 2:
            return False

        return self.total == 21

    '''Return true if Hand total > 21'''
    def is_bust(self):
        return self.total > 21

    '''loop the values for total and soft_ace_count'''
    def score(self):
        card = self.cards[-1]

        if card == 1:
            self.soft_ace_count += 1
            self.total += 11
        elif card >= 10:
            self.total += 10
        else:
            self.total += card

        while self.total > 21 and self.soft_ace_count > 0:
            self.total -= 10
            self.soft_ace_count -= 1


class Strategy:
    
    '''initialize the attributes based on the values passed in.'''
    def __init__(self, stand_on_value, stand_on_soft):
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft

    '''return the “canonical” string representation of the object.'''
    def __repr__(self):
        return f"stand_on_value: {self.stand_on_value}, stand_on_soft: {self.stand_on_soft}"

    '''H or S by stand_on_value, and the stand_on_value'''
    def __str__(self):
        return f"{'S' if self.stand_on_soft else 'H'}{self.stand_on_value}"

    '''hit: False, stand:True'''
    def stand(self, hand):
        total = hand.total
        soft_ace_count = hand.soft_ace_count
        is_stand = False

        if total < self.stand_on_value:
            is_stand = False
        elif total > self.stand_on_value:
            is_stand = True
        elif self.stand_on_soft:
            is_stand = True
        elif not soft_ace_count:
            is_stand = True

        return is_stand

    '''return the Hand object.'''
    def play(self):
        hand = Hand()
        hand.add_card()
        hand.add_card()

        while not self.stand(hand):
            hand.add_card()

        return hand


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <num-simulations>")
        exit(1)

    try:
        simulation_time = int(sys.argv[1])
    except ValueError as e:
        print(e)
        exit(1)


    '''player go first, if bust, lose.'''
    '''second: dealer, going by strategy, if bust, players win.'''
    '''the one with blackjack wins.'''
    '''having same score: tie, no wins'''
    '''higher total wins.'''

    winning_percentages = []

    '''loop from 13 to 20.'''
    strategies = [(i, j) for i in range(13, 21) for j in [False, True]]
    header_row = ["P-Strategy"]
    is_header_row_initial = False

    for player_s in strategies:
        player = Strategy(player_s[0], player_s[1])
        row_result = ["P-" + str(player)]
        for dealer_s in strategies:
            dealer = Strategy(dealer_s[0], dealer_s[1])
            if not is_header_row_initial:
                header_row.append("D-" + str(dealer))

            player_win = 0
            for _ in range(simulation_time):
                player_card = player.play()
                if player_card.is_bust():
                    continue

                dealer_card = dealer.play()
                if dealer_card.is_bust():
                    player_win += 1
                    continue

                if player_card.total != dealer_card.total and player_card.total > dealer_card.total:
                    player_win += 1

            percentage = player_win / simulation_time * 100
            row_result.append(f"{round(percentage, 2):.2f}")

        is_header_row_initial = True
        winning_percentages.append(row_result)

    '''produce output using csv.writer. row: different player strategies/ columns: different dealer strategies.'''
    result_writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    result_writer.writerow(header_row)
    result_writer.writerows(winning_percentages)


if __name__ == '__main__':
    main()
