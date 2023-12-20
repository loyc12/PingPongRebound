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


class Pong( gi.Game ):
	type = "Pong"

	score_mode = df.GOALS

	width = 2048
	height = 1024

	size_f = 768

	racket_count = 2
	score_count = 2

	iPosR1 = ( int( gi.Game.size_b ), int( height * ( 1 / 2 ))			, "y" )
	iPosR2 = ( int( width - gi.Game.size_b ), int( height * ( 1 / 2 ))	, "y" )

	iPosB1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))

	posS1 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 2 )), 1.5, 1, 1, -1 )
	posS2 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )), 1.5, 1, 1, 1 )

	posN1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))
	posN2 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 2 )))

	lines = [
	[( 0, 0 ), ( 1, 0 ), 2 ],
	[( 0.5, 0 ), ( 0.5, 1 ), 1 ],
	[( 0, 1 ), ( 1, 1 ), 2 ]]


	def initRackets( self ):
		# setting up rackets :             id, game, _x              , _y              , _w         , _h         , _maxSpeed
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_b, self.size_r, self.speed_m_r ))
		self.rackets.append( go.GameObject( 2, self, self.iPosR2[ 0 ], self.iPosR2[ 1 ], self.size_b, self.size_r, self.speed_m_r ))

		self.rackets[ 0 ].setSpeeds( 0, self.speed_r )
		self.rackets[ 1 ].setSpeeds( 0, self.speed_r )



	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				if( rack.id == 1 ):
					ball.setPosX( rack.getPosX() + self.size_b )# '+' because the ball is going to the right
				elif( rack.id == 2 ):
					ball.setPosX( rack.getPosX() - self.size_b )# '-' because the ball is going to the left

				ball.bounceOnRack( rack, "x" )
				self.last_ponger = rack.id
				self.ballEvent( ball, df.HITS, rack.id )

				break # 									NOTE : prevents multihits


	# bouncing on the walls
	def checkWalls( self, ball ):
		if ball.getTop() < 0 or ball.getBottom() > self.height:
			ball.bounceOnWall( "y" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getLeft() <= 0 or ball.getRight() >= self.width:

			# checking who scored
			if ball.getLeft() <= 0:
				self.ballEvent( ball, df.GOALS, 2 )

			if ball.getRight() >= self.width:
				self.ballEvent( ball, df.GOALS, 1 )

			if self.connector != None:
				self.connector.update_scores( self.scores )


	def respawnBall( self, ball ):
		self.last_ponger = 0

		s = self.spawns[ self.spawn_target ]

		ball.setPos( s[ 0 ], s[ 1 ])
		ball.setSpeeds( s[ 2 ] * self.speed_b, s[ 3 ] * self.speed_b )
		ball.setDirs( s[ 4 ], ball.fy )
