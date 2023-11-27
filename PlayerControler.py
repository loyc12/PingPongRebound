from master import cfg
from master import gc
import Addons as ad

# controler class
class PlayerControler(gc.GameControler):


	def __init__(self, _game, _playerName, _playerID):
		self.game = _game
		self.name = _playerName
		self.mode = ad.PLAYER
		self.playerID = _playerID


	# NOTE : temporary (uses pygame keys)
	def handleKeyInput(self, key):
		if key == ad.SPACE or key == ad.NZERO:
			self.playMove( ad.STOP )
		elif key == ad.KW or key == ad.UP:
			self.playMove( ad.UP )
		elif key == ad.KD or key == ad.RIGHT:
			self.playMove( ad.RIGHT )
		elif key == ad.KS or key == ad.DOWN:
			self.playMove( ad.DOWN )
		elif key == ad.KA or key == ad.LEFT:
			self.playMove( ad.LEFT )
		elif (cfg.DEBUG_MODE and key == ad.RETURN): #		NOTE : DEBUG
			for i in range(len(self.game.balls)):
				self.game.respawnBall( self.game.balls[i] )
		else:
			print("Error: invalid move")
