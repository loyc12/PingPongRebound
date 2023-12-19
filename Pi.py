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

	posS1 = ( width * ( 1 / 2 ), gi.Game.size_b, 1, 0, 1, 1 )

	posN1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 2 )))