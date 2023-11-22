import GameControler as gc
import pygame as pg
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
		if key == pg.K_SPACE or key == pg.K_KP0:
			self.playMove( ad.STOP )
		elif key == pg.K_w or key == pg.K_UP:
			self.playMove( ad.UP )
		elif key == pg.K_d or key == pg.K_RIGHT:
			self.playMove( ad.RIGHT )
		elif key == pg.K_s or key == pg.K_DOWN:
			self.playMove( ad.DOWN )
		elif key == pg.K_a or key == pg.K_LEFT:
			self.playMove( ad.LEFT )
		elif (key == pg.K_RETURN): #							NOTE : DEBUG
			for i in range(len(self.game.balls)):
				self.game.respawnBall( self.game.balls[i] )
		else:
			print("Error: invalid move")
