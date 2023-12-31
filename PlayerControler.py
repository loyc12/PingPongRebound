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
			self.stopHere()
		elif key == df.KW or key == df.KUP:
			self.goUp( 8 )
		elif key == df.KD or key == df.KRIGHT:
			self.goRight( 8 )
		elif key == df.KS or key == df.KDOWN:
			self.goDown( 8 )
		elif key == df.KA or key == df.KLEFT:
			self.goLeft( 8 )

		elif( cfg.DEBUG_MODE and key == df.RETURN ):
			for i in range( len( self.game.balls )):
				self.game.respawnBall( self.game.balls[ i ] )

		else:
			print( "Error: invalid move" )
