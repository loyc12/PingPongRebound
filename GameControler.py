import Addons as ad

# controler class
class GameControler:
	name = "unnamed"
	# gameType = "normal" # "tournament"
	game = None
	racket = None

	mode = ad.CONTROLER


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
		if self.racket == 0:
			print("Error: no racket selected")
		elif self.game.state == ad.STARTING:
			print("The game has not started yet")
		elif self.game.state == ad.ENDING:
			print("The game is over")
		elif move != ad.NULL:
			self.game.makeMove( self.racketID, move )