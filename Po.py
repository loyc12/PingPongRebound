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


class Po( gi.Game ):
	name = "Po"

	width = 1280
	height = 1280

	size_font = 768

	factor_rack = 1.2
	factor_wall = 0.9

	score_mode = gi.df.HITS
	scores = [ 0 ]

	iPosR1 = ( int( width * ( 1 / 2 )), int( height - gi.Game.size_b ), "x" )

	iPosB1 = ( int( width * ( 3 / 8 )), int( gi.Game.size_b ))

	iPosS1 = ( width * ( 1 / 2 ), height * ( 1 / 2 ))
