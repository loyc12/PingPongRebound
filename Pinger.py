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


class Pinger( gi.Game ):
	name = "Pinger"

	divide_sides = True
	score_mode = df.GOALS

	width = 1536
	height = 1280

	size_f = 768

	factor_rack = 1.05

	racket_count = 4
	score_count = 2

	iPosR1 = ( int( width * ( 2 / 7 )), int( gi.Game.size_b )			, "x" )
	iPosR2 = ( int( width * ( 5 / 7 )), int( gi.Game.size_b )			, "x" )
	iPosR3 = ( int( width * ( 2 / 7 )), int( height - gi.Game.size_b )	, "x" )
	iPosR4 = ( int( width * ( 5 / 7 )), int( height - gi.Game.size_b )	, "x" )

	iPosB1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )))

	iPosS1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))
	iPosS2 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 2 )))

	lines = [
	[( 0, 0 ), ( 0, 1 ), 2 ],
	[( 0.5, 0 ), ( 0.5, 1 ), 1 ],
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


	def initBalls( self ):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
		self.balls[ 0 ].setSpeeds( self.speed_b * ( 2 / 3 ), self.speed_b )
		self.balls[ 0 ].setDirs( 1, 1 )


	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				if( rack.id == 1 or rack.id == 2 ):
					ball.setPosY( rack.getPosY() + self.size_b )# '+' because the ball is going under
				elif( rack.id == 3 or rack.id == 4 ):
					ball.setPosY( rack.getPosY() - self.size_b )# '-' because the ball is going over

				ball.bounceOnRack( rack, "y" )
				self.scorePoint( rack.id, df.HITS )

				break # 									NOTE : prevents multihits


	# bouncing on the walls
	def checkWalls( self, ball ):
		# bouncing off the sides
		if ball.getLeft() < 0 or ball.getRight() > self.width:
			ball.bounceOnWall( "x" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getTop() < 0 or ball.getBottom() > self.height:

			# checking who scored
			if ball.getRight() < self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 2, df.GOALS )

			if ball.getLeft() > self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 1, df.GOALS )

			self.respawnBall( ball )
			if self.connector != None:
				self.connector.update_scores( self.scores )


	def respawnBall( self, ball ):
		ball.setSpeeds(( self.speed_b + ball.dx ) * ( 1 / 3 ), self.speed_b )

		if( ball.getPosX() < self.width / 2 ):
			ball.setDirs( -1, ball.fy )
		else:
			ball.setDirs( 1, ball.fy )

		if( ball.getPosY() < self.height / 2 ):
			ball.setDirs( ball.fx, 1 )
			ball.setPos( self.width * ( 1 / 2 ), self.height * ( 1 / 4 ))
		else:
			ball.setDirs( ball.fx, -1 )
			ball.setPos( self.width * ( 1 / 2 ), self.height * ( 3 / 4 ))


	def drawScores( self ):
		text1 = self.font.render( f'{self.scores[ 0 ]}', True, df.COL_FNT )
		text2 = self.font.render( f'{self.scores[ 1 ]}', True, df.COL_FNT )

		self.win.blit( text1, text1.get_rect( center = self.iPosS1 ))
		self.win.blit( text2, text2.get_rect( center = self.iPosS2 ))
