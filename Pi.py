try:
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg
	from master import go
	from master import gi

except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	from game.PingPongRebound.master import go
	from game.PingPongRebound.master import gi


class Pi( gi.Game ):
	type = "Pi"

	score_mode = gi.df.HITS

	width = 1280
	height = 1280

	factor_rack = 0.9
	factor_wall = 0.6

	gravity = 0.3

	iPosR1 = ( int( width * ( 1 / 2 )), int( height - gi.Game.size_b ), "x" )

	iPosB1 = ( int( width * ( 3 / 8 )), int( gi.Game.size_b ))

	iPosS1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 2 )))


	def initBalls( self ):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ], self.size_b, self.size_b, self.speed_m_r ))
		self.balls[ 0 ].setSpeeds( self.speed_b, 0 )
		self.balls[ 0 ].setDirs( 1, 1 )

	def respawnBall( self, ball ):
		ball.setDirs( ball.fx, 1 )
		ball.setPosY( self.size_b )
		ball.setSpeeds( self.speed_b, 0 )
