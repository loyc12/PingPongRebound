try:
	import defs as df
except ModuleNotFoundError:
	import game.PingPongRebound.defs as df

# controler class
class GameControler:
	name = "unnamed"
	game = None
	racket = None
	racketDir = None

	playerID = 0
	mode = df.CONTROLER

	def __init__( self, _game ):
		self.game = _game

		self.defaultX = _game.width / 2
		self.defaultY = _game.height / 2


	def setRacket( self, _racketID ):
		for i in range( self.game.racket_count ):
			rack = self.game.rackets[ i ]

			if rack.id == _racketID:
				self.racket = rack

				self.recordDefaultPos()
				break

		print( f"Warning: no racket with id {_racketID} found in game #{self.game.gameID}" )


	def recordDefaultPos( self ):
		self.defaultX = self.racket.getPosX()
		self.defaultY = self.racket.getPosY()

		if self.racket.dx != 0:
			self.racketDir = 'x'
		elif self.racket.dy != 0:
			self.racketDir = 'y'

		self.goal = self.findOwnGoal()


	def findOwnGoal( self ):
		rack = self.racket

		if rack.dx != 0:
			if( self.defaultY < self.game.height / 2 ): # goal is on the top
				return df.UP
			else:
				return df.DOWN

		elif rack.dy != 0:
			if( self.defaultX < ( self.game.width / 2 )): # goal is on the left
				return df.LEFT
			else:
				return df.RIGHT


	def playMove( self, move ):
		if self.racket == 0:
			print( "Error: no racket selected" )
		elif self.game.state == df.STARTING:
			print( "The game has not started yet" )
		elif self.game.state == df.ENDING:
			print( "The game is over" )
		elif move != df.NULL:
			self.game.makeMove( self.racket.id, move )


	def getInfo( self ):
		if (self.mode == df.PLAYER):
			isBot = False
		else:
			isBot = True

		return {
			"isBot": isBot,
			"name": self.name,
			"playerID": self.playerID,
			"teamID": self.racket.id
		}

