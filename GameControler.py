try:
	import defs as df
except ModuleNotFoundError:
	import game.PingPongRebound.defs as df

# controler class
class GameControler:
	name = "unnamed"
	game = None
	racket = None
	racketDir = 'z'

	playerID = 0
	racketID = 0
	mode = df.CONTROLER

	def __init__( self, _game ):
		self.game = _game


	def setRacket( self, _racketID ):
		for i in range( len( self.game.rackets )):
			rack = self.game.rackets[ i ]
			if( _racketID <= 0 ):
				raise ValueError( f"Error: no racket with id {_racketID} found in {self.game.name}" )
			elif rack.id == _racketID:
				self.racket = rack
				self.racketID = rack.id
				if rack.dx != 0:
					self.racketDir = 'x'
				elif rack.dy != 0:
					self.racketDir = 'y'


	def playMove( self, move ):
		if self.racket == 0:
			print( "Error: no racket selected" )
		elif self.game.state == df.STARTING:
			print( "The game has not started yet" )
		elif self.game.state == df.ENDING:
			print( "The game is over" )
		elif move != df.NULL:
			self.game.makeMove( self.racketID, move )


	def getInfo( self ):
		if (self.mode == df.PLAYER):
			isBot = False
		else:
			isBot = True

		return {
			"isBot": isBot,
			"name": self.name,
			"playerID": self.playerID,
			"teamID": self.racketID
		}

