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
	name = "Ponger"

	width = 1536
	height = 1024

	gravity = 0
	racketCount = 4

	score_mode = df.GOALS
	scores = [ 0, 0 ]

	iPosR1 = ( int( width * ( 2 / 7 )), int( 3 * gi.Game.size_b	 )			, "x" )
	iPosR2 = ( int( width * ( 2 / 7 )), int( height - ( 3 * gi.Game.size_b ))	, "x" )
	iPosR3 = ( int( width * ( 5 / 7 )), int( gi.Game.size_b	 )				, "x" )
	iPosR4 = ( int( width * ( 5 / 7 )), int( height - gi.Game.size_b	 )		, "x" )

	iPosB1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )))

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
		self.balls[ 0 ].setSpeeds( self.speed_b * ( 2 / 3 ), self.speed_b )
		self.balls[ 0 ].setDirs( 1, 1 )


	# def handlePygameInput( self, key ): #		NOTE : DEBUG
	# 	# player 1
	# 	if( self.controlers[ 0 ].mode == df.PLAYER ):
	# 		if key == df.KS:
	# 			self.makeMove( 1, df.STOP )
	# 			self.makeMove( 4, df.STOP )
	# 		elif key == df.KA:
	# 			self.makeMove( 1, df.LEFT )
	# 			self.makeMove( 4, df.LEFT )
	# 		elif key == df.KD:
	# 			self.makeMove( 1, df.RIGHT )
	# 			self.makeMove( 4, df.RIGHT )

	# 	# player 2
	# 	if( self.controlers[ 1 ].mode == df.PLAYER ):
	# 		if key == df.DOWN:
	# 			self.makeMove( 2, df.STOP )
	# 			self.makeMove( 3, df.STOP )
	# 		elif key == df.LEFT:
	# 			self.makeMove( 2, df.LEFT )
	# 			self.makeMove( 3, df.LEFT )
	# 		elif key == df.RIGHT:
	# 			self.makeMove( 2, df.RIGHT )
	# 			self.makeMove( 3, df.RIGHT )


	def aplyGravity( self, ball ):
		if self.gravity != 0:
			if ball.getPosY() > self.height / 2:
				if ball.fy > 0:
					ball.dy += self.gravity
				else:
					ball.dy -= self.gravity
			if ball.getPosY() < self.height / 2:
				if ball.fy > 0:
					ball.dy -= self.gravity
				else:
					ball.dy += self.gravity


	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):
				if( rack.id == 1 or rack.id == 3 ):
					ball.setPosY( rack.getPosY() + self.size_b )# '+' because the ball is going under
				elif( rack.id == 2 or rack.id == 4 ):
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
			if ball.getTop() < 0:
				if self.last_ponger > 0:
					self.scorePoint( 2, df.GOALS )
				ball.setDirs( -1, -1 )
				ball.setPos( self.width * ( 1 / 2 ), self.height * ( 3 / 4 ))

			elif ball.getBottom() > self.height:
				if self.last_ponger > 0:
					self.scorePoint( 1, df.GOALS )
				ball.setDirs( 1, 1 )
				ball.setPos( self.width * ( 1 / 2 ), self.height * ( 1 / 4 ))

			self.respawnBall( ball )


	def respawnBall( self, ball ):
		ball.setPosX( self.width * ( 1 / 2 ))
		ball.setSpeeds(( self.speed_b + ball.dx ) * ( 1 / 3 ), self.speed_b )


	def drawLines( self ):
		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, df.COL_FNT, ( 0, self.height / 2 ), ( self.width, self.height / 2 ), self.size_l )
		pg.draw.line( self.win, df.COL_FNT, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )


	def drawScores( self ):
		text1 = self.font.render( f'{self.scores[ 0 ]}', True, df.COL_FNT )
		text2 = self.font.render( f'{self.scores[ 1 ]}', True, df.COL_FNT )

		self.win.blit( text1, text1.get_rect( center = ( self.width * ( 2 / 4 ), self.height * ( 1 / 4 ))))
		self.win.blit( text2, text2.get_rect( center = ( self.width * ( 2 / 4 ), self.height * ( 3 / 4 ))))


if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Ponger( 1 )

	if cfg.DEBUG_MODE:
		g.setWindow( pg.display.set_mode(( Ponger.width, Ponger.height )))
		pg.display.set_caption( g.name )

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()