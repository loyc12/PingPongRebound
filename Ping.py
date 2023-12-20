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
	type = "Ping"

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

	iPosB1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )))

	posS1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )), 1, 1, -1, -1)
	posS2 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 4 )), 1, 1, 1, -1)

	posN1 = ( int( width * ( 1 / 4 )), int( height * ( 1 / 2 )))
	posN2 = ( int( width * ( 3 / 4 )), int( height * ( 1 / 2 )))

	lines = [
	[( 0.5, 0 ), ( 0.5, 1 ), 1 ],
	[( 0, 0 ), ( 0, 1 ), 2 ],
	[( 1, 0 ), ( 1, 1 ), 2 ],
	[( 0, 0 ), ( 1, 0 ), 2 ]]


	def checkGoals( self, ball ):
		if ball.getBottom() > self.height:

			# checking who scored
			if ball.getPosX() <= self.width / 2:
				self.ballEvent( ball, df.GOALS, 2 )

			else:
				self.ballEvent( ball, df.GOALS, 1 )

			if self.connector != None:
				self.connector.update_scores( self.scores )
