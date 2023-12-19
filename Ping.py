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


class Ping( gi.Game ):
	name = "Ping"

	divide_sides = True
	score_mode = df.GOALS

	width = 2048
	height = 1024

	size_f = 768

	factor_rack = 0.9
	factor_wall = 0.6

	gravity = 0.333

	racket_count = 2
	score_count = 2

	iPosR1 = ( int( width * ( 1 / 3 )), int( height - gi.Game.size_b ), "x" )
	iPosR2 = ( int( width * ( 2 / 3 )), int( height - gi.Game.size_b ), "x" )

	iPosB1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 3 )))

	iPosS1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))
	iPosS2 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 2 )))

	lines = [
	[( 0.5, 0 ), ( 0.5, 1 ), 1 ],
	[( 0, 0 ), ( 0, 1 ), 2 ],
	[( 1, 0 ), ( 1, 1 ), 2 ],
	[( 0, 0 ), ( 1, 0 ), 2 ]]


	def initRackets( self ):
		# setting up rackets :             id, game, _x              , _y              , _w         , _h         , _maxSpeed
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets[ 0 ].setSpeeds( self.speed_r, 0 )

		self.rackets.append( go.GameObject( 2, self, self.iPosR2[ 0 ], self.iPosR2[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
		self.rackets[ 1 ].setSpeeds( self.speed_r, 0 )


	def initBalls( self ):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
		self.balls[ 0 ].setSpeeds( self.speed_b * ( 2 / 3 ), self.speed_b * ( 3 / 2 ) )
		self.balls[ 0 ].setDirs( 1, -1 )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getBottom() > self.height:

			# checking who scored
			if ball.getRight() < self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 2, df.GOALS )
				ball.setDirs( -1, -1 )

			if ball.getLeft() > self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 1, df.GOALS )
				ball.setDirs( 1, -1 )

			self.respawnBall( ball )
			if self.connector != None:
				self.connector.update_scores( self.scores )


	def respawnBall( self, ball ):
		ball.setPos( self.width * ( 1 / 2 ), self.height * ( 1 / 3 ))
		ball.setSpeeds(( ball.dx + self.speed_b ) / 3, self.speed_b  * ( 3 / 2 ) )


	def drawScores( self ):
		text1 = self.font.render( f'{self.scores[ 0 ]}', True, df.COL_FNT )
		text2 = self.font.render( f'{self.scores[ 1 ]}', True, df.COL_FNT )

		self.win.blit( text1, text1.get_rect( center = self.iPosS1 ))
		self.win.blit( text2, text2.get_rect( center = self.iPosS2 ))
