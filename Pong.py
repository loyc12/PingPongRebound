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
	name = "Pong"

	width = 2048
	height = 1024

	size_font = 768

	racket_count = 2
	score_count = 2

	score_mode = df.GOALS
	scores = [ 0, 0 ]

	iPosR1 = ( int( gi.Game.size_b ), int( height * ( 1 / 2 ))			, "y" )
	iPosR2 = ( int( width - gi.Game.size_b ), int( height * ( 1 / 2 ))	, "y" )

	iPosB1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))

	iPosS1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))
	iPosS2 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 2 )))

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


	def initBalls( self ):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ] , self.size_b, self.size_b, self.speed_m_b ))
		self.balls[ 0 ].setSpeeds( self.speed_b * ( 3 / 2 ), self.speed_b )
		self.balls[ 0 ].setDirs( 1, 1 )


	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				if( rack.id == 1 ):
					ball.setPosX( rack.getPosX() + self.size_b )# '+' because the ball is going to the right
				elif( rack.id == 2 ):
					ball.setPosX( rack.getPosX() - self.size_b )# '-' because the ball is going to the left

				ball.bounceOnRack( rack, "x" )
				self.scorePoint( rack.id, df.HITS )


	# bouncing on the walls
	def checkWalls( self, ball ):
		if ball.getTop() < 0 or ball.getBottom() > self.height:
			ball.bounceOnWall( "y" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getLeft() < 0 or ball.getRight() > self.width:
			# checking who scored
			if ball.getLeft() < 0:
				if self.last_ponger > 0:
					self.scorePoint( 2, df.GOALS )
				ball.setDirs( -1, ball.fy )
				ball.setPos( self.width * ( 3 / 4 ), self.height * ( 1 / 2 ))
			if ball.getRight() > self.width:
				if self.last_ponger > 0:
					self.scorePoint( 1, df.GOALS )
				ball.setDirs( 1, ball.fy )
				ball.setPos( self.width * ( 1 / 4 ), self.height * ( 1 / 2 ))

			self.respawnBall( ball )
			if self.connector != None:
				self.connector.update_scores( self.scores )


	def respawnBall( self, ball ):
		ball.setPosY( self.height * ( 1 / 2 ))
		ball.setSpeeds( self.speed_b * ( 3 / 2 ), ( ball.dy + self.speed_b ) * ( 1 / 2 ))


	def drawScores( self ):
		text1 = self.font.render( f'{self.scores[ 0 ]}', True, df.COL_FNT )
		text2 = self.font.render( f'{self.scores[ 1 ]}', True, df.COL_FNT )

		self.win.blit( text1, text1.get_rect( center = self.iPosS1 ))
		self.win.blit( text2, text2.get_rect( center = self.iPosS2 ))
