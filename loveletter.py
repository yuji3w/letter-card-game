from enum import Enum
from enum import IntEnum
from random import randint
import tensorflow as tf
import numpy as np

DEBUG = True

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

	def start_turn(self, restart = False, tfAgent = False, action = 15):
		if self.status == status.ELIMINATED:
			return False
		if not restart and not tfAgent:
			self.draw_card(partialDeck)
		self.status = status.NORMAL

		#this is where the bot will be hooked up

		if not tfAgent:
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
				self.turn(playerList[playerNo], cardName.GUARD, guess)
			#overhaul before changing everythin


		self.turn(playerList[playerNo], card, guess)

	def turn(self, attackedPlayer, card, guess):
		success = card.play(self, attackedPlayer, guess)
		if success:
			self.hand.remove(card)
		else:
			print("Your turn could not be completed.")
			self.start_turn(restart = True)



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

class game:
	global partialDeck, playerList, fullDeck

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
	player.numPlayers = 0
	playerList = [player(), player()]
	playerList[0].AI = True
	playerList[1].AI = True
	
	def __init__(self):
		self.playerNo = 0

	def play_game():
		global partialDeck, playerList, fullDeck
		playerNo = 0
		isWin = False

		while not isWin:
			playerList[playerNo].start_turn()

			if DEBUG:
				game.dump_info()

			isWin, survivors = player.check_winner()
			if isWin:
				for p in survivors:
					p.status = status.WINNER
					break

			playerNo = (playerNo + 1)%player.numPlayers

	#dump info of opponent for debug
	def dump_info():
		global partialDeck, playerList, fullDeck
		for p in playerList:
			print(p.playerNo)
			print(p.status)
			print()
			for card in p.hand:
				print(card.name)
			print()
			print()
		print("partialDeck:")
		for c in partialDeck:
			print(c.name, end = " ")

	def step(self, action):
		global partialDeck, playerList, fullDeck
		print("hey this is the action:")
		print(action)
		#Assume 0-13
		if(action == 14):
			print("YOU MESSED UP, action should not be 14")
			return 0, 0, 0
		reward = 0
		done = False
		obs = []
		isWin, survivors = player.check_winner()
		if isWin:
			done = True
			return obs, reward, done

		#2 players for ai, pass in action here
		playerList[0].start_turn(tfAgent=True)
		playerList[1].start_turn()

		#return obs after drawing card
		if len(partialDeck) > 0:
			playerList[0].draw_card(partialDeck)
		obs = self.return_observation(playerList[0])

		isWin, survivors = player.check_winner()
		if isWin:
			if playerList[0] in survivors:
				reward = 1
			else:
				reward = -1
			done = True
			return obs, reward, done


		self.playerNo = (self.playerNo + 1)%player.numPlayers

		return obs, reward, done

	def reset(self):
		global partialDeck, playerList, fullDeck
		self.playerNo = 0
		partialDeck = list(fullDeck)
		player.numPlayers = 0
		playerList = [player(), player()]

		playerList[0].draw_card(partialDeck)

		obs = self.return_observation(playerList[self.playerNo])
		return obs

	def return_observation(self, attackingPlayer):
		global partialDeck, playerList, fullDeck
		hand = [0]*15
		card1 = fullDeck.index(attackingPlayer.hand[0])
		card2 = fullDeck.index(attackingPlayer.hand[1])
		print(card1)
		print(card2)
		hand[card1] = 1
		hand[card2] = 1

		used = [0] * 15
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






fullDeck = [
	guard(), guard(), guard(), guard(), guard(), 
	spy(), spy(),
	baron(), baron(),
	handmaiden(), handmaiden(),
	prince(),
	king(),
	countess(),
	princess()]


def play_inifinite_ai():
	for i in range(0,100000):

		partialDeck = list(fullDeck)
		player.numPlayers = 0
		playerList = [player(), player()]

		#initialize all AIs
		playerList[0].AI = True
		playerList[1].AI = True

		#playerList[0].hand.clear()
		#playerList[0].hand.append(princess())

		game.dump_info()
		game.play_game()
		game.dump_info()



#TODO: fix all globals


#TODO: add neural network with inputs
'''
hand, previous cards, known cards input
card, attackedplayer, guess output
'''

num_inputs = 2 * 15
num_hidden = int(2 * 14 * 1.5)
num_outputs = 13

initializer = tf.contrib.layers.variance_scaling_initializer()

X = tf.placeholder(tf.float32, shape = [None, num_inputs])

hidden_layer_one = tf.layers.dense(X, num_hidden,activation=tf.nn.relu,
	kernel_initializer=initializer)

hidden_layer_two = tf.layers.dense(hidden_layer_one,num_hidden,activation=tf.nn.relu,
	kernel_initializer=initializer)

output_layer = tf.layers.dense(hidden_layer_two, num_outputs,activation=tf.nn.sigmoid,
	kernel_initializer=initializer)

probabilities = tf.concat(axis=1,values=[output_layer])
action = tf.multinomial(probabilities,num_samples=1)

init = tf.global_variables_initializer()

epi = 50
step_limit = 500
env = game()
abg_steps = []

with tf.Session() as sess:
	init.run()

	for i_episode in range(epi):
		obs = env.reset()

		for step in range(step_limit):
			action_val = action.eval(feed_dict = {X:obs.reshape(1,num_inputs)})
			obs,reward,done = env.step(action_val[0][0])

			if done:
				avg_steps.append(step)
				print("Done after {} steps.".format(steps))
				break






#tf stuff
'''
observations = tf.placeholder(tf.int32, shape=(14,2))
#maybe make int?

actions = tf.placeholder(tf.float32, shape = [None])

#model
Y = tf.layers.dense(observations, 200, activation=tf.nn.relu)
Ylogits = tf.layers.dense(Y,13)

#sample an action from predicted probabilities
sample_op = tf.multinomial(logits = Ylogits, num_samples=1)

#loss
cross_entropies = tf.losses.softmax_cross_entropy(onehot_labels=
	tf.one_hot(actions,13), logits = Ylogits)

loss = tf.reduce_sum(rewards * cross_entropies)

#training operation
optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001, decay=.99)
train_op = optimizer.minimize(loss)

with tf.Session as sess:
	...
	observation = return_observation(playerList[0])
	while not done: 
		action = sess.run(sample_op, feed_dict = {observations: [observation]})
		print("HEY HEY HEY")
		reward = cardGame.step(action)
		observations.append(observation)
		actions.append(action)
		rewards.append(reward)
'''