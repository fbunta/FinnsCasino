from abc import ABC,abstractmethod, abstractproperty
from time import sleep

class Player(ABC):
    """Abstract interface for use by the blackjack game object

    :param game: A handle to the :class:`balckjack.Game` object
    :type game: :class:`blackjack.Game` object
    :param name: An identifier for each player object to use
    :type name: str
    """
    def __init__(self, game, name):
        self._game = game
        self.name = name
        self._hand = []

    @abstractproperty
    def type(self):
        """Used to identify between unique implementations of the Player interface
        """
        pass

    @property
    def hand(self):
        """Iterable of tuples that which are cards

        :return: sequence of card tuples
        :rtype: list
        """
        return self._hand

    @hand.setter
    def hand(self, value):
        """A method to add another card to the player's hand. We do not allow cards
        to ever leave a player's hand. 

        :param value: must be a card tuple e.g. ('7', 'Spades')
        :type value: tuple
        :raises TypeError: if passed a type other than tuple
        """
        if isinstance(value, tuple):
            self._hand.append(value)
        else:
            raise TypeError("must be a tuple")

    @abstractmethod
    def play_hand(self):
        """Public method called by Game class to facilitate player's turn
        """
        pass

    def _hit(self):
        return self._game._give_card()

    def _calculate_score(self):
        score = 0
        for number, suit in self.hand:
            if number in ('J','Q','K'):
                score += 10
            elif number == 'A':
                score += 11
            else:
                score += int(number)
        if score > 21:
            for number, suit in self.hand:
                if number == 'A':
                    score -= 10
                if score <= 21:
                    break
        return score

class ComputerPlayer(Player):
    def __init__(self, *args):
        super().__init__(*args)
    
    @property
    def type(self):
        """The type string
        :return: 'Bot'
        :rtype: string
        """
        return 'Bot'
    
    def play_hand(self):
        """Implementation of player interface for bots

        :return: score of the turn for this player
        :rtype: int
        """
        while self._calculate_score() <= 21:
            score = self._calculate_score()
            print(f'{self.type} {self.name} is at {score}')
            sleep(1)
            if score >= 16:
                break
            else:
                print('hit!')
                self.hand = self._hit()
                print(f'hand is now {self.hand}')
        if self._calculate_score() > 21:
            print(f'{self.type} {self.name} busted!\n')
            return 0
        else:
            score = self._calculate_score()
            print(f'{self.type} {self.name} final score is {score}\n')
            return score

class Dealer(Player):
    def __init__(self, game):
        super().__init__(game, name='Jack')

    @property
    def type(self):
        """The type string
        :return: 'Dealer'
        :rtype: string
        """
        return 'Dealer'
    
    def play_hand(self):
        """Implementation of player interface for the dealer

        :return: score of the turn for this player
        :rtype: int
        """
        while self._calculate_score() <= 21:
            score = self._calculate_score()
            print(f'{self.type} {self.name} is at {score}')
            if score >= 17:
                break
            else:
                print('hit!')
                self.hand = self._hit()
                print(f'hand is now {self.hand}')
        if self._calculate_score() > 21:
            print('busted!\n')
            return 0
        else:
            score = self._calculate_score()
            print(f'{self.type} {self.name} final score is {score}\n')
            return score

    def display_one_card(self):
        """Important additional public method to ensure only one card is initially
        face up in the dealer's hand.

        :return: a face up card and a face down card
        :rtype: tuple
        """
        return self._hand[0], ('-', '-----')

class HumanPlayer(Player):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def type(self):
        """The type string
        :return: 'Player'
        :rtype: string
        """
        return 'Player'

    def play_hand(self):
        """Implementation of player interface for a human player thus it requires command
        line interaction.

        :return: score of the turn for this player
        :rtype: int
        """
        while self._calculate_score() <= 21:
            print(f'{self.type} {self.name} is at {self._calculate_score()}')
            choice = input('would you like to stick or hit?\n')
            if choice == 'stick':
                break
            elif choice == 'hit':
                self.hand = self._hit()
                print(f'{self.name} hand is {self.hand}')
            else:
                print('could not understand, please enter "stick" or "hit"')
        if self._calculate_score() > 21:
            print(f'{self.type} {self.name} busted!\n')
            return 0
        else:
            score = self._calculate_score()
            print(f'{self.type} {self.name} final score is {score}\n')
            return score