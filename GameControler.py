import GameInterface as gi

# controler class
class Controler:
	name = "unnamed"
	racket = 0

	def __init__(self, _game, _playerName, _racketID):
		self.game = _game
		self.name = _playerName
		for i in range(len(self.game.rackets)):
			rack = self.game.rackets[i]
			if rack.id == _racketID:
				self.racket = rack

		if (self.racket <= 0):
			raise ValueError("Error: no racket with id " + str(_racketID) + " found in game " + self.game.name)

