try:
	from Keybindings import *
except ModuleNotFoundError:
	from game.PingPongRebound.Keybindings import *

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
WIN_SCORE = 8

# game states
STARTING = 0
PLAYING = 1
ENDING = 2
#PAUSED = 3

# game modes
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
BOT_CAN_PLAY = True
BOT_INSTANT_REACT = False

BOT_M_FACTOR = 4
BOT_PLAY_FREQUENCY = 10
BOT_SEE_FREQUENCY = 60
BOT_DEPTH = 5
BOT_PRECISION = 40
BOT_KICK_DISTANCE = 160

# DEBUG
if cfg.DEBUG_MODE:
	WIN_SIZE = 1280
	COL_BGR = pg.Color('black')
	COL_FNT = pg.Color('grey25')
	COL_OBJ = pg.Color('white')

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
