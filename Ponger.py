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


class Ponger( gi.Game ):
	type = "Ponger"

	score_mode = df.GOALS

	width = 1536
	height = 1280

	size_f = 768

	factor_rack = 1.05

	racket_count = 4
	score_count = 2

	iPosR1 = ( int( width * ( 2 / 7 )), int( 3 * gi.Game.size_b	 )				, "x" )
	iPosR2 = ( int( width * ( 2 / 7 )), int( height - ( 3 * gi.Game.size_b ))	, "x" )
	iPosR3 = ( int( width * ( 5 / 7 )), int( gi.Game.size_b	 )					, "x" )
	iPosR4 = ( int( width * ( 5 / 7 )), int( height - gi.Game.size_b )			, "x" )

	iPosB1 = ( int( width * ( 1 / 2 )), int( height * ( 3 / 4 )))

	posS1 = ( int( width * ( 1 / 2 )), int( height * ( 3 / 4 )), 0.4, 1, -1, -1)
	posS2 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )), 0.4, 1, 1, 1)


	posN1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )))
	posN2 = ( int( width * ( 1 / 2 )), int( height * ( 3 / 4 )))

	lines = [
	[( 0, 0 ), ( 0 , 1 ), 2 ],
	[( 0, 0.5 ), ( 1, 0.5 ), 1 ],
	[( 1, 0 ), ( 1, 1 ), 2 ]]


	def initRackets( self ):
		# setting up rackets :             id, game, _x              , _y              , _w         , _h         , _maxSpeed
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets.append( go.GameObject( 2, self, self.iPosR2[ 0 ], self.iPosR2[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets.append( go.GameObject( 3, self, self.iPosR3[ 0 ], self.iPosR3[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets.append( go.GameObject( 4, self, self.iPosR4[ 0 ], self.iPosR4[ 1 ], self.size_r, self.size_b, self.speed_m_r ))

		self.rackets[ 0 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 1 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 2 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 3 ].setSpeeds( self.speed_r, 0 )


	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				if( rack.id == 1 or rack.id == 3 ):
					ball.setPosY( rack.getPosY() + self.size_b )# '+' because the ball is going under
				elif( rack.id == 2 or rack.id == 4 ):
					ball.setPosY( rack.getPosY() - self.size_b )# '-' because the ball is going over

				ball.bounceOnRack( rack, "y" )
				self.last_ponger = rack.id
				self.ballEvent( ball, df.HITS, rack.id )

				break # 									NOTE : prevents multihits


	# bouncing on the walls
	def checkWalls( self, ball ):
		# bouncing off the sides
		if ball.getLeft() < 0 or ball.getRight() > self.width:
			ball.bounceOnWall( "x" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getTop() < 0 or ball.getBottom() > self.height:

			if ball.getTop() <= 0:
				self.ballEvent( ball, df.GOALS, 2 )

			if ball.getBottom() >= self.height:
				self.ballEvent( ball, df.GOALS, 1 )

			if self.connector != None:
				self.connector.update_scores( self.scores )


	def respawnBall( self, ball ):
		self.last_ponger = 0

		s = self.spawns[ self.spawn_target ]

		ball.setPos( s[ 0 ], s[ 1 ])
		ball.setSpeeds( s[ 2 ] * self.speed_b, s[ 3 ] * self.speed_b )
		ball.setDirs( -ball.fx, s[ 5 ] )

	def getTeamID( self, racketID ):
		if racketID == 1 or racketID == 3:
			return 1
		else:
			return 2