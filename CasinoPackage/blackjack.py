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
        self._deck = self._create_deck()
        self._player_list = self._create_players(player_count, bot_count)
        self._dealer = Dealer(self)
    
    @property
    def deck(self):
        """Set by the the _create_deck method

        :return: deck instance member variable 
        :rtype: list of card object
        """
        return self._deck

    @property
    def player_list(self):
        """Set by the _create_players method

        :return: player_list instance member variable 
        :type list of :class:`player.Player` implementations
        """
        return self._player_list
    
    def _create_players(self, player_count, bot_count):
        """Called by c'tor to create the player list and assign it to player_list attribute

        :param player_count: number of human players to add
        :type player_count: int
        :param bot_count: number of human players to add
        :type bot_count: int
        :return: sequence of players
        :rtype: list
        """
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
        """Called by c'tor to create the 52 card objects and place them in the _deck private instance attribute

        :return: sequence of cards
        :rtype: list
        """
        number_list = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        suit_list = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        return [(number, suit) for number, suit in product(number_list, suit_list)]
    
    def _shuffle(self):
        """Shuffles the private class attribute _deck
        """
        random.shuffle(self.deck)

    def _give_card(self):
        """Pops a card off the top of the deck

        :return: a card object
        :rtype: a namedtuple
        """
        return self.deck.pop(0)

    def _deal(self, cards_count=2):
        """Gives out 2 cards to every player including the dealer
        """
        players_dealer_list = self.player_list + [self._dealer]
        while cards_count > 0:
            for player in players_dealer_list:
                player.hand = self._give_card()
            cards_count -= 1

    def _display_all(self):
        """Display all starting cards to the cli
        """
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
