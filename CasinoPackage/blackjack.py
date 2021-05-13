from itertools import product
import random

from players import HumanPlayer, ComputerPlayer, Dealer


class Game:
    """Object that plays the game of blackjack!

    :param player_count: number of human players you want at the table
    :type player_count: int, defualts to 1
    :param bot_count: number of bots you want at the table
    :type bot_count: int, defualts to 1
    """
    def __init__(self, player_count=1, bot_count=1):
        self.deck = self._create_deck()
        self.player_list = self._create_players(player_count, bot_count)
        self._dealer = Dealer(self)
    
    def _create_players(self, player_count, bot_count):
        player_list = []
        order = 1
        while player_count > 0:
            player_list.append(HumanPlayer(self, order))
            order += 1
            player_count -= 1
        order = 1
        while bot_count > 0:
            player_list.append(ComputerPlayer(self, order))
            order += 1
            bot_count -= 1
        return player_list

    @staticmethod
    def _create_deck():
        number_list = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        suit_list = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        return [(number, suit) for number, suit in product(number_list, suit_list)]
    
    def _shuffle(self):
        random.shuffle(self.deck)

    def _give_card(self):
        return self.deck.pop(0)

    def _deal(self, cards_count=2):
        players_dealer_list = self.player_list + [self._dealer]
        while cards_count > 0:
            for player in players_dealer_list:
                player.hand = self._give_card()
            cards_count -= 1

    def _display_all(self):
        for player in self.player_list:
            score = player._calculate_score()
            print(f"{player.type} {player.name} score is {score}")
            if score == 21:
                print('BLACKJACK!')
            print(f'{player.hand}\n')
        print(f"Dealer Jack's hand is")
        print(self._dealer.display_one_card())
        print('\n---------------------------------\n')

    def play(self):
        """Kicks off the game by shuffling, dealing and interacting with players
        """
        self._shuffle()
        self._deal()
        self._display_all()
        results = {}
        for player in self.player_list:
            score = player.play_hand()
            results[f'{player.type} {player.name}'] = score
        print('Dealer flips over second card...')
        print(self._dealer.hand)
        dealer_score = self._dealer.play_hand()
        print('\n---------------------------------\n')
        for name, score in results.items():
            if score == 0:
                print(f'{name} lost')
            elif score > dealer_score:
                print(f'{name} wins')
            elif score == dealer_score:
                print(f'{name} pushes')
            else:
                print(f'{name} lost')

if __name__ == "__main__":
    g = Game(player_count=2, bot_count=2)
    g.play()
