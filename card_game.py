from enum import Enum
from enum import IntEnum
from random import randint
import numpy as np

fullDeck = []
partialDeck = []
playerList = []

class status(Enum):
	ELIMINATED = 0
	NORMAL = 1
	PROTECTED = 2
	WINNER = 3

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
		self.AI = False

	def display_cards(self):
		print("You have these cards:")
		for i in range (0, len(self.hand)):
			print(self.hand[i].name)

	def input_card(self, AI = False):
		if AI:
			card = randint(1,8)
			print("AI say {}".format(card))
		else:
			card = int(input("What is the card number?"))
		while card < 1 or card > 8:
			print("This card does not exist.")
			if AI:
				card = randint(1,8)
				print("AI says {}".format(card))
			else:
				card = int(input("What is the card number?"))
		return cardName(card)

	def input_player_no(self, AI = False):
		if AI:
			playerNo = randint(0,len(playerList)-1)
			print("AI says {}".format(playerNo))
		else:
			playerNo = int(input("What is the player number? (Player 0, 1, etc)"))
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

	def check_winner():
		survivors = []
		for p in playerList:
			if p.status == status.NORMAL or p.status == status.PROTECTED:
				survivors.append(p)
		if len(survivors) < 2:
			print("There is 1 or 0 players remaining.")
			return True, survivors

		winners = []
		if len(partialDeck) == 0:
			print("The partialDeck is empty")
			#this must be done before cards are drawn for next turn. Call as class
			bestCard = []
			for p in survivors:
				bestCard.append(p.hand[0].name.value)
			bestCard = max(bestCard)
			for p in survivors:
				if p.hand[0].name.value == bestCard:
					winners.append(p)
				return True, winners


		return False, survivors

	def countess_condition(self):
		if (self.hand[0].name == cardName.PRINCE or self.hand[0].name == cardName.KING or 
			self.hand[1].name == cardName.PRINCE or self.hand[1].name == cardName.PRINCE):
			if self.hand[0].name == cardName.COUNTESS or self.hand[1].name == cardName.COUNTESS:
				return True
		return False

	def start_turn(self, restart = False, action = False):
		global playerNo
		if self.status == status.ELIMINATED:
			return False
		if not restart and action == False:
			self.draw_card(partialDeck)
		self.status = status.NORMAL

		#this is where the bot will be hooked up

		if action == False:
			print()
			print(self.playerNo)
			self.display_cards()
			card = self.input_card(AI = self.AI)
			while not self.card_in_hand(card):
				print("This card is not in your hand.")
				card = self.input_card(AI = self.AI)
			card = self.matching_card_obj(card)
			playerNo = self.input_player_no(AI = self.AI)
			while playerNo > player.numPlayers - 1:
				print("This player does not exist.")
				playerNo = self.input_player_no(AI = self.AI)
			if card.name == cardName.GUARD:
				print("Guess the card number.")
				guess = self.input_card(AI = self.AI)
			else:
				guess = cardName.GUARD
		else:
			#TODO: put this elsewhere later
			if action == 1:
				self.turn(playerList[playerNo], cardName.GUARD, guess, action = action)
			#overhaul before changing everythin


		self.turn(playerList[playerNo], card, guess)

	def turn(self, attackedPlayer, card, guess, action = False):
		success = card.play(self, attackedPlayer, guess)
		if success:
			self.hand.remove(card)
		else:
			print("Your turn could not be completed.")
			self.start_turn(restart = True, action = action)

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

	def is_player_normal(self, attackedPlayer):
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

		if not self.is_player_normal(attackedPlayer):
			print("Player {} is unavailable".format(attackedPlayer))
			return False
		if guess == cardName.GUARD:
			print("You cannot guess guard.")
			return False
		if guess == attackedPlayer.hand[0].name:
			print("You guessed correctly.")
			attackedPlayer.status = status.ELIMINATED
		else:
			print("You guessed incorrectly")
		return True

class spy(cardType):
	def __init__(self):
		self.name = cardName.SPY

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		#spy reveals attackedPlayer.hand
		#TODO: implement the lists of knowns

		if not self.is_player_normal(attackedPlayer):
			print("Player {} is unavailable".format(attackedPlayer))
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
		must have 2 cards in hand, if no cards left in partialDeck, game ends with
		comparison
		'''

		if not self.is_player_normal(attackedPlayer):
			print("Player {} is unavailable".format(attackedPlayer))
			return False
		card2 = attackedPlayer.hand[0]
		if self is attackingPlayer.hand[0]:
			card = attackingPlayer.hand[1]
		else:
			card = attackingPlayer.hand[0]

		if card.name.value > card2.name.value:
			attackedPlayer.status = status.ELIMINATED
		elif card.name.value < card2.name.value:
			attackingPlayer.status = status.ELIMINATED
		if attackingPlayer == attackedPlayer:
			attackedPlayer.status = status.NORMAL
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

		if not self.is_player_normal(attackedPlayer):
			print("Player {} is unavailable".format(attackedPlayer))
			return False

		#countess must be played if prince or king
		
		if attackingPlayer.countess_condition():
			print("You must play countess.")
			return False
		if attackedPlayer.hand[0].name == cardName.PRINCESS:
			print("Princess discarded correctly")
			attackedPlayer.status = status.ELIMINATED
		if partialDeck == []:
			print("The partialDeck is empty")
			attackedPlayer.status = status.ELIMINATED
		elif attackingPlayer is not attackedPlayer:
			attackedPlayer.hand.clear()
			attackedPlayer.draw_card(partialDeck)
		else:

			#remove not self from hand so player can remove self later
			print("You discarded your own hand")
			if self is attackedPlayer.hand[0]:
				attackedPlayer.hand.pop(1)
				attackedPlayer.draw_card(partialDeck)
			else:
				attackedPlayer.hand.pop(0)
				attackedPlayer.draw_card(partialDeck)

		return True

class king(cardType):
	def __init__(self):
		self.name = cardName.KING

	def play(self, attackingPlayer, attackedPlayer, guess = cardName.GUARD):

		'''
		trade hands with other player
		'''

		if not self.is_player_normal(attackedPlayer):
			print("Player {} is unavailable".format(attackedPlayer))
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
		prince(), prince(),
		king(),
		countess(),
		princess()]

#reset environment before using module

def reset():
	global partialDeck, playerList, playerNo
	partialDeck = list(fullDeck)
	player.numPlayers = 0
	playerNo = 0

	#TODO: add arguments to define below

	playerList = [player(), player()]
	playerList[0].draw_card(partialDeck)
	playerList[1].AI = True

def play_game():
	playerNo = 0
	isWin = False

	while not isWin:
		playerList[playerNo].start_turn()

		dump_info()

		isWin, survivors = player.check_winner()
		if isWin:
			for p in survivors:
				p.status = status.WINNER
				break

		playerNo = (playerNo + 1)%player.numPlayers

def dump_info():
	for p in playerList:
		print(p.playerNo)
		print(p.status, end = "\n\n")
		for card in p.hand:
			print(card.name)
		print("\n\n")
	print("partialDeck:")
	for c in partialDeck:
		print(c.name, end = "\t")

def return_observation(attackingPlayer):
	global partialDeck, playerList, fullDeck
	hand = [0]*16
	card1 = fullDeck.index(attackingPlayer.hand[0])
	card2 = fullDeck.index(attackingPlayer.hand[1])
	print(card1)
	print(card2)
	hand[card1] = 1
	hand[card2] = 1

	used = [0] * 16
	for c in fullDeck:
		if c not in partialDeck and c not in playerList[0].hand and c not in playerList[1].hand:
			index = fullDeck.index(c)
			used[index] = 1

	#add spied, recurse later

	observation = []
	observation.extend(hand)
	observation.extend(used)
	observation = np.array(observation)

	return observation

def play_action_turn(attackingPlayer, action):
	if action < 7:

		#get equivalent card name (cards start at 1)

		guess = action + 1
		guess = cardName(guess)
		attackingPlayer.turn(playerList[playerNo], cardName.GUARD, guess)

	if action == 1:
				self.turn(playerList[playerNo], cardName.GUARD, guess)


def step(action):
	reward = 0
	done = False
	obs = []

	global playerNo
	print("Your action is" + str(action))
	
	#not sure if I should include this because after should deal with it

	done, survivors = player.check_winner()
	if done:
		return obs, reward, done

	playerList[0].start_turn(action)
	playerList[1].start_turn()

	#return obs after drawing card
	if len(partialDeck) > 0:
		playerList[0].draw_card(partialDeck)
	obs = return_observation(playerList[0])

	done, survivors = player.check_winner()
	if done:
		if playerList[0] in survivors:
			reward = 100
		else:
			reward = -100
		done = True
		return obs, reward, done

	return obs, reward, done


reset()
playerList[1].AI = True
dump_info()
action = randint(0,13)
obs, reward, done = step(action)
dump_info()
print("ACTION:")
print(action)
print("OBS:")
print(obs)
print("REWARD:")
print(reward)
print("DONE:")
print(done)





'''
for i in range(0,100000):
	reset()

	#initialize all AIs
	playerList[0].AI = True
	playerList[1].AI = True

	dump_info()
	step(0)
	dump_info()
'''