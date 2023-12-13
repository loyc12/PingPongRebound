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

class Pingest( gi.Game ):
	name = "Pingest"

	width = 1536
	height = 1024
	racketCount = 4

	score_mode = df.GOALS
	scores = [ 0, 0, 0, 0 ]

	iPosR1 = ( int( width * ( 2 / 7 )), int( gi.Game.size_b )			, "x" )
	iPosR2 = ( int( width * ( 5 / 7 )), int( gi.Game.size_b )			, "x" )
	iPosR3 = ( int( width * ( 2 / 7 )), int( height - gi.Game.size_b )	, "x" )
	iPosR4 = ( int( width * ( 5 / 7 )), int( height - gi.Game.size_b )	, "x" )

	iPosB1 = ( int( width * ( 3 / 4 )), int( height * ( 3 / 4 )))

	def initRackets( self ):
		# setting up rackets :             id, game, _x              , _y              , _w         , _h
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 2, self, self.iPosR2[ 0 ], self.iPosR2[ 1 ], self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 3, self, self.iPosR3[ 0 ], self.iPosR3[ 1 ], self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 4, self, self.iPosR4[ 0 ], self.iPosR4[ 1 ], self.size_r, self.size_b ))

		self.rackets[ 0 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 1 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 2 ].setSpeeds( self.speed_r, 0 )
		self.rackets[ 3 ].setSpeeds( self.speed_r, 0 )


	def initBalls( self ):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ], self.size_b, self.size_b ))
		self.balls[ 0 ].setSpeeds( self.speed_b, ( self.speed_b * ( 2 / 3 )))
		self.balls[ 0 ].setDirs( -1, -1 )


	def moveRacket( self, rack ):
		rack.clampSpeed()
		rack.updatePos( self.speed_m_r )

		# prevent racket from going off screen
		if( not rack.isInScreen() ):
			rack.bounceOnWall( "stop" )

		# prevent racket from crossing the middle line
		if( rack.id == 1 or rack.id == 3 )and rack.getRight() > self.width / 2:
			rack.bounceOnWall( "stop" )
			rack.setPosX(( self.width - self.size_r ) / 2 )
		elif( rack.id == 2 or rack.id == 4 )and rack.getLeft() < self.width / 2:
			rack.bounceOnWall( "stop" )
			rack.setPosX(( self.width + self.size_r ) / 2 )

		rack.clampPos()


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


	# bouncing on the walls
	def checkWalls( self, ball ):
		# bouncing off the sides
		if ball.getLeft() < 0 or ball.getRight() > self.width:
			ball.bounceOnWall( "x" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getTop() < 0 or ball.getBottom() > self.height:

			# checking who scored
			if( self.last_ponger > 0 ):
				self.scorePoint( self.last_ponger, df.GOALS )
				if self.last_ponger == 1:
					ball.setDirs( -1, -1 )
				elif self.last_ponger == 2:
					ball.setDirs( 1, -1 )
				elif self.last_ponger == 3:
					ball.setDirs( -1, 1 )
				elif self.last_ponger == 4:
					ball.setDirs( 1, 1 )
			else:
				ball.setDirs( -ball.fx, -ball.fy )

			self.respawnBall( ball )


	def respawnBall( self, ball ):
		ball.setPos( self.width / 2, self.height / 2 )
		ball.setSpeeds(( self.speed_b + ball.dx ) / 2, ( self.speed_b + ball.dy ) / 3 )


	def drawLines( self ):
		pg.draw.line( self.win, df.COL_FNT, ( self.width / 2, 0 ), ( self.width / 2, self.height ), self.size_l )
		pg.draw.line( self.win, df.COL_FNT, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )

		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ), ( 0, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, df.COL_FNT, ( 0, self.height / 2 ), ( self.width, self.height / 2 ), self.size_l )



	def drawScores( self ):
		text1 = self.font.render( f'{self.scores[ 0 ]}', True, df.COL_FNT )
		text2 = self.font.render( f'{self.scores[ 1 ]}', True, df.COL_FNT )
		text3 = self.font.render( f'{self.scores[ 2 ]}', True, df.COL_FNT )
		text4 = self.font.render( f'{self.scores[ 3 ]}', True, df.COL_FNT )

		self.win.blit( text1, text1.get_rect( center = ( self.width * ( 1 / 4 ), self.height * ( 1 / 4 ))))
		self.win.blit( text2, text2.get_rect( center = ( self.width * ( 3 / 4 ), self.height * ( 1 / 4 ))))
		self.win.blit( text3, text3.get_rect( center = ( self.width * ( 1 / 4 ), self.height * ( 3 / 4 ))))
		self.win.blit( text4, text4.get_rect( center = ( self.width * ( 3 / 4 ), self.height * ( 3 / 4 ))))
