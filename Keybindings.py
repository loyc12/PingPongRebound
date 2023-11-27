import cfg

if cfg.DEBUG_MODE:
    import pygame as pg

    # keyboard keys
    UP = pg.K_UP
    DOWN = pg.K_DOWN
    LEFT = pg.K_LEFT
    RIGHT = pg.K_RIGHT
    SPACE = pg.K_SPACE
    RETURN = pg.K_RETURN

    # keypad keys
    KW = pg.K_w
    KS = pg.K_s
    KA = pg.K_a
    KD = pg.K_d
    NZERO = pg.K_KP0

else:
	# keyboard keys # TODO: Change them, these are wrong. Check with javascript event key codes.
	UP =     'up'
	DOWN =   'dn'
	LEFT =   'lf'
	RIGHT =  'rt'
	SPACE =  ' '
	RETURN = '\r'

	# keypad keys
	KW = 'w'
	KS = 's'
	KA = 'a'
	KD = 'd'
	NZERO = '0'
