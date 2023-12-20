try:
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg
	from master import go
	from master import gi
	import defs as df

except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	from game.PingPongRebound.master import go
	from game.PingPongRebound.master import gi
	import game.PingPongRebound.defs as df


class Pongest( gi.Game ):
	type = "Pongest"

	score_mode = df.GOALS

	width = 1280
	height = 1280

	speed_m_b = 20

	size_f = 512

	factor_rack = 1.05

	racket_count = 4
	score_count = 4

	iPosR1 = ( int( width * ( 1 / 2 )), int( gi.Game.size_b )			, "x" )
	iPosR2 = ( int( width - gi.Game.size_b ), int( height * ( 1 / 2 ))	, "y" )
	iPosR3 = ( int( width * ( 1 / 2 )), int( height - gi.Game.size_b )	, "x" )
	iPosR4 = ( int( gi.Game.size_b ), int( height * ( 1 / 2 ))			, "y" )

	iPosB1 = ( int( width * ( 3 / 4 )), int( height * ( 3 / 4 )))

	posS1 = ( int( width * ( 3 / 4 )), int( height * ( 3 / 4 )), 0.5, 1, -1, -1)
	posS2 = ( int( width * ( 1 / 4 )), int( height * ( 3 / 4 )), 1, 0.5, 1, -1)
	posS3 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 4 )), 0.5, 1, 1, 1)
	posS4 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 4 )), 1, 0.5, -1, 1)

	posN1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 5 )))
	posN2 = ( int( width * ( 4 / 5 )), int( height * ( 1 / 2 )))
	posN3 = ( int( width * ( 1 / 2 )), int( height * ( 4 / 5 )))
	posN4 = ( int( width * ( 1 / 5 )), int( height * ( 1 / 2 )))

	lines = [
	[( 0, 0 ), ( 1, 1 ), 1.4 ],
	[( 0, 1 ), ( 1, 0 ), 1.4 ]]


	def initRackets( self ):
		# setting up rackets :             id, game, _x              , _y              , _w         , _h         , _maxSpeed
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets.append( go.GameObject( 2, self, self.iPosR2[ 0 ], self.iPosR2[ 1 ], self.size_b, self.size_r, self.speed_m_r ))
		self.rackets.append( go.GameObject( 3, self, self.iPosR3[ 0 ], self.iPosR3[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets.append( go.GameObject( 4, self, self.iPosR4[ 0 ], self.iPosR4[ 1 ], self.size_b, self.size_r, self.speed_m_r ))

		self.rackets[ 0 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 1 ].setSpeeds( 0, self.speed_r )
		self.rackets[ 2 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 3 ].setSpeeds( 0, self.speed_r )


	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				if( rack.id == 1 ):
					ball.setPosY( rack.getPosY() + self.size_b )# '+' because the ball is going under
					ball.bounceOnRack( rack, "y" )
				elif( rack.id == 2 ):
					ball.setPosX( rack.getPosX() - self.size_b )# '-' because the ball is going left
					ball.bounceOnRack( rack, "x" )
				elif( rack.id == 3 ):
					ball.setPosY( rack.getPosY() - self.size_b )# '-' because the ball is going over
					ball.bounceOnRack( rack, "y" )
				elif( rack.id == 4 ):
					ball.setPosX( rack.getPosX() + self.size_b )# '+' because the ball is going right
					ball.bounceOnRack( rack, "x" )

				self.last_ponger = rack.id
				self.ballEvent( ball, df.HITS, rack.id)

				break # 									NOTE : prevents multihits


	# bouncing on the walls( walls are absent in Pongester )
	def checkWalls( self, ball ):
		pass


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getTop() < 0 or ball.getBottom() > self.height or ball.getLeft() < 0 or ball.getRight() > self.width:
			self.ballEvent( ball, df.GOALS, self.last_ponger )

			if self.connector != None:
				self.connector.update_scores( self.scores )
