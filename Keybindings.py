debugKeys = False
try:
	import cfg
	if cfg.DEBUG_MODE:
		import pygame as pg
		debugKeys = True

except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	cfg.DEBUG_MODE = False


if debugKeys:
	# keyboard keys
	KUP		= pg.K_UP
	KDOWN 	= pg.K_DOWN
	KLEFT	= pg.K_LEFT
	KRIGHT	= pg.K_RIGHT
	SPACE	= pg.K_SPACE

	# keypad keys
	KW		= pg.K_w
	KS		= pg.K_s
	KA		= pg.K_a
	KD		= pg.K_d
	NZERO	= pg.K_KP0

	# event types
	START		= pg.K_p
	CLOSE		= pg.QUIT
	KEYPRESS	= pg.KEYDOWN
	ESCAPE		= pg.K_ESCAPE
	RETURN		= pg.K_RETURN

else:
	# keyboard keys
	KUP		= 'up'
	KDOWN	= 'dn'
	KLEFT	= 'lf'
	KRIGHT	= 'rt'
	SPACE	= ' '

	# keypad keys
	KW		= 'w'
	KS		= 's'
	KA		= 'a'
	KD		= 'd'
	NZERO	= '0'

	# event types
	START		= 'start_game'
	CLOSE		= 'end_game'
	KEYPRESS	= 'key_press'
	ESCAPE		= None
	RETURN		= None
