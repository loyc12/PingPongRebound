try:
	import cfg
	from master import gc
	import defs as df
except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	from game.PingPongRebound.master import gc
	import game.PingPongRebound.defs as df

# controler class
class PlayerControler( gc.GameControler ):

	mode = df.PLAYER

	def __init__( self, _game, _playerName, _playerID ):
		self.game = _game
		self.name = _playerName
		self.playerID = _playerID

		self.defaultX = _game.width / 2
		self.defaultY = _game.height / 2


	def handleKeyInput( self, key ):
		if key == df.SPACE or key == df.NZERO:
			self.playMove( df.STOP )
		elif key == df.KW or key == df.KUP:
			self.playMove( df.UP )
		elif key == df.KD or key == df.KRIGHT:
			self.playMove( df.RIGHT )
		elif key == df.KS or key == df.KDOWN:
			self.playMove( df.DOWN )
		elif key == df.KA or key == df.KLEFT:
			self.playMove( df.LEFT )
		elif( cfg.DEBUG_MODE and key == df.RETURN ): #		NOTE : DEBUG
			for i in range( len( self.game.balls )):
				self.game.respawnBall( self.game.balls[ i ] )
		else:
			print( "Error: invalid move" )
