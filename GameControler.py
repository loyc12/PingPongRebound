import Addons as ad

# controler class
class GameControler:
	name = "unnamed"
	# gameType = "normal" # "tournament"
	game = None
	racket = None
	next_move = ad.NULL

	mode = ad.CONTROLER
	isActive = True


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName
		self.racketID = 0


	def setRacket(self, _racketID):
		for i in range(len(self.game.rackets)):
			rack = self.game.rackets[i]
			if (_racketID <= 0):
				raise ValueError(f"Error: no racket with id {_racketID} found in {self.game.name}")
			elif rack.id == _racketID:
				self.racket = rack
				self.racketID = rack.id


	def playMove(self, move):
		if self.isActive:
			self.game.makeMove( self.racketID , move )


	def setNextMove(self, move):
		self.next_move = move


	def playStep(self):

		if self.racket == 0:
			raise ValueError("Error: no racket selected")
		if self.isActive:
			self.playMove( self.next_move )
			self.next_move = ad.NULL


	def deactivate(self):
		self.isActive = False

