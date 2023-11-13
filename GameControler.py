import GameInterface as gi

# controler class
class GameControler:
	name = "unnamed"
	# gameType = "normal" # "tournament"
	game = None
	racket = None
	next_move = 0


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName

	def setRacket(self, _racketID):
		for i in range(len(self.game.rackets)):
			rack = self.game.rackets[i]
			if (_racketID <= 0):
				raise ValueError(f"Error: no racket with id {_racketID} found in {self.game.name}")
			elif rack.id == _racketID:
				self.racket = rack


	def playMove(self, move):
		self.game.makeMove( self.racket.id, move )


	def setNextMove(self, move):
		self.next_move = move


	def playStep(self):

		if self.racket == 0:
			raise ValueError("Error: no racket selected")

		self.playMove( self.next_move )
		self.next_move = 0


	def getInfo(self):
		return self.game.getState() #	TODO : implement this more (???)

