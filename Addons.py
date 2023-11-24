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

# controler modes
CONTROLER = 0
PLAYER = 1
BOT = 2

# movements
NULL = 0
STOP = 1
UP = 2
RIGHT = 3
DOWN = 4
LEFT = 5

# scores
GOALS = 0
HITS = 1

# game stuff
WIN_SCORE = 8

STARTING = 0
PLAYING = 1
ENDING = 2
#PAUSED = 3

SOLO = 0
DUAL = 1
FREEPLAY = 2
TOURN_RND_1 = 3
TOURN_RND_2 = 4
#TOURN_RND_3 = 5

# bot difficulty
EASY = 0
MEDIUM = 1
HARD = 2

# bot stuff
BOT_M_FACTOR = 4
BOT_FREQUENCY = 10
BOT_DEPTH = 5
BOT_PRECISION = 40
BOT_KICK_DISTANCE = 160

# DEBUG
WIN_SIZE = 1280

def getSign(value):
	if value < 0:
		return -1
	if value > 0:
		return 1
	return 0

def isInZone(x, y, border, game):
	if x < border or x > ( game.width - border ):
		return False
	if y < border or y > ( game.height - border ):
		return False
	return True