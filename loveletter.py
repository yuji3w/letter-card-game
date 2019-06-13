class game:
	
	def __init__(self):
		self.playerNo = 0



	#dump info of opponent for debug




	def reset(self):
		global partialDeck, playerList, fullDeck
		self.playerNo = 0
		partialDeck = list(fullDeck)
		player.numPlayers = 0
		playerList = [player(), player()]

		playerList[0].draw_card(partialDeck)

		obs = self.return_observation(playerList[self.playerNo])
		return obs

	













#TODO: add neural network with inputs
'''
hand, previous cards, known cards input
card, attackedplayer, guess output
'''