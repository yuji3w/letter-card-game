from enum import Enum
from enum import IntEnum
from random import randint

fullDeck = []
partialDeck = []
playerList = []

class status(Enum):
	ELIMINATED = 0
	NORMAL = 1
	PROTECTED = 2

class cardName(IntEnum):
	GUARD = 1
	SPY = 2
	BARON = 3
	HANDMAIDEN = 4
	PRINCE = 5
	KING = 6
	COUNTESS = 7
	PRINCESS = 8

class player:
	numPlayers = 0

	def __init__(self):
		self.playerNo = player.numPlayers
		player.numPlayers += 1

		self.hand = []
		self.draw_card(partialDeck)

		#TODO: Create list of known cards of each player or probabilities of cards'
		self.known = []

		self.status = status.NORMAL

	def display_cards(self):
		print("You have these cards:")
		for i in range (0, len(self.hand)):
			print(self.hand[i].name)

	def input_card(self):
		card = int(input("What is the card number?"))
		while card < 1 or card > 8:
			print("This card does not exist.")
			card = int(input("What is the card number?"))
		return cardName(card)

	def input_player_no(self):
		playerNo = int(input("What is the player number?"))
		return playerNo

	def card_in_hand(self, card):
		for i in range (0, len(self.hand)):
			if card == self.hand[i].name:
				return True
		return False

	def matching_card_obj(self, card):
		for i in range (0, len(self.hand)):
			if card == self.hand[i].name:
				return self.hand[i]

	def draw_card(self, deck):
		rand_card = randint(0,len(deck)-1)
		card = deck.pop(rand_card)
		self.hand.append(card)

	def countess_condition(self):
		if (self.hand[0].name == cardType.PRINCE or self.hand[0].name == cardType.KING or 
			self.hand[1].name == cardType.PRINCE or self.hand[1].name == cardType.PRINCE):
			if self.hand[0].name == cardType.COUNTESS or self.hand[1].name == cardType.COUNTESS:
				return True
		return False

	def start_turn(self):
		self.draw_card(partialDeck)
		self.status = status.NORMAL
		self.display_cards()

		#this is where the bot will be hooked up

		card = self.input_card()
		while not self.card_in_hand(card):
			print("This card is not in your hand.")
			card = self.input_card()
		card = self.matching_card_obj(card)
		playerNo = self.input_player_no()
		playerNo = playerNo - 1
		while playerNo > player.numPlayers:
			print("This player does not exist.")
			playerNo = self.input_player_no - 1
		if card.name == cardName.GUARD:
			print("Guess the card number.")
			guess = self.input_card()
		else:
			guess = cardName.GUARD

		self.turn(playerList[playerNo], card, guess)



	def turn(self, attackedPlayer, card, guess):
		success = card.play(self, attackedPlayer, guess = cardName.GUARD)
		if success:
			self.hand.pop(card)
		else:
			print("Your turn could not be completed.")
			self.start_turn()



class cardType:

	'''
	creating method to override for testing
	since both players are passed by reference no need for player ID
	or array of player
	'''

	def play(self, attackingPlayer, attackedPlayer):

		'''
		Default behavior is putting down card
		and playing message
		Should not have access to attackingPlayer's deck
		(behavior should be handled by attackingPlayer obj after playing)
		'''

		self.play_message(attackingPlayer, attackedPlayer)

	def play_message(self, attackingPlayer, attackedPlayer):

		#each player should be initialized with a name

		print("{} played {} against {}.".format(attackingPlayer.name, 
			self.name, attackedPlayer.name))

	def is_player_normal(self, attackingPlayer, attackedPlayer):
		#true if attackable, false if not
		if (attackedPlayer.status == status.NORMAL):
			return True
		else:
			return False

class guard(cardType):
	def __init__(self):

		'''
		This should be an intenum, not a number so intenum's 
		name can be printed in play_message
		'''

		self.name = cardName.GUARD

	def play(self, attackingPlayer, attackedPlayer, guess):

		'''
		attackingPlayer guesses card from attackedPlayer's deck
		the card guessed cannot be cardName.GUARD
		behavior if it is will be handled by player
		attackedPlayer is eliminated if guess is correct
		'''

		if not self.is_player_normal(attackingPlayer, attackedPlayer):
			return False
		if guess == cardName.GUARD:
			return False
		if guess in attackedPlayer.hand:
			attackedPlayer.status = status.ELIMINATED
		return True

class spy(cardType):
	def __init__(self):
		self.name = cardName.SPY

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		#spy reveals attackedPlayer.hand
		#TODO: implement the lists of knowns

		if not self.is_player_normal(attackingPlayer, attackedPlayer):
			return False
		print("{} is Player {}'s card.".format(attackedPlayer.hand[0].name, 
			attackedPlayer.playerNo))
		return True

class baron(cardType):
	def __init__(self):
		self.name = cardName.BARON

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		'''
		compare hands with other player, higher hand wins
		must have 2 cards in hand, if no cards left in incompleteDeck, game ends with
		comparison
		'''

		if not self.is_player_normal(attackingPlayer, attackedPlayer):
			return False
		if self is attackingPlayer.hand[0]:
			card = attackingPlayer.hand[1]
		else:
			card = attackingPlayer.hand[0]

		card2 = attackedPlayer.hand[0]
		if card.name.value > card2.name.value:
			attackedPlayer.status = status.ELIMINATED
		elif card.name.value < card2.name.value:
			attackingPlayer.status = status.ELIMINATED

		#if tie, nothing happens

		return True

class handmaiden(cardType):
	def __init__(self):
		self.name = cardName.HANDMAIDEN

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		#player is protected until next turn

		attackingPlayer.status = status.PROTECTED
		return True

class prince(cardType):
	def __init__(self):
		self.name = cardName.PRINCE

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		'''
		attackedPlayer must discard hand and redraw
		if there's nothing left they lose
		'''

		if not self.is_player_normal(attackingPlayer, attackedPlayer):
			return False

		#countess must be played if prince or king
		
		if attackingPlayer.countess_condition():
			print("You must play countess.")
			return False
		if partialDeck == []:
			attackedPlayer.status = status.ELIMINATED
		else:
			attackedPlayer.hand.clear()
			attackedPlayer.draw_card(partialDeck)
		return True

class king(cardType):
	def __init__(self):
		self.name = cardName.KING

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		'''
		trade hands with other player
		'''

		if not self.is_player_normal(attackingPlayer, attackedPlayer):
			return False
		if attackingPlayer.countess_condition():
			print("You must play countess.")
			return False
		if self is attackingPlayer.hand[0]:
			temp = attackingPlayer.hand[1]
			attackingPlayer.hand[1] = attackedPlayer.hand[0]
			attackedPlayer.hand[0] = temp
		else:
			temp = attackingPlayer.hand[0]
			attackingPlayer.hand[0] = attackedPlayer.hand[0]
			attackedPlayer.hand[0] = temp
		return True

class countess(cardType):
	def __init__(self):
		self.name = cardName.COUNTESS

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):
		return True

class princess(cardType):
	def __init__(self):
		self.name = cardName.PRINCESS

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):
		attackingPlayer.status = status.ELIMINATED
		return True

fullDeck = [
	guard(), guard(), guard(), guard(), guard(), 
	spy(), spy(),
	baron(), baron(),
	handmaiden(), handmaiden(),
	prince(),
	king(),
	countess(),
	princess()]

partialDeck = list(fullDeck)


playerList = [player(), player()]
playerList[0].start_turn()