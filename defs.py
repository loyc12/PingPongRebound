try:
	from Keybindings import *
except ModuleNotFoundError:
	from game.PingPongRebound.Keybindings import *

# controler modes
CONTROLER = 0
PLAYER = 1
BOT = 2

# game objects
OBJ_BASE = 0
OBJ_BALL = 1
OBJ_RACKET = 2
OBJ_OBSTACLE = 3


# movements
NULL = 0
STOP = 1
UP = 2
RIGHT = 3
DOWN = 4
LEFT = 5

KICK_FACTOR = 1.0 #				NOTE : how much of the racket's speed is transfered the the ball when hitting it
NO_STUCK_BALLS = True #			NOTE : this prevent balls from having 0 speed on either X or Y (no straight bounces)

# scores
GOALS = 1
HITS = 2

WIN_SCORE = 8
MAX_MISS = 3

# game states
STARTING = 1
PLAYING = 2
ENDING = 3

# game modes
SOLO = 1
DUAL = 2
FREEPLAY = 3
TOURNAMENT = 4
FORCE_MODE_TO = DUAL #		NOTE : only used if FORCE_MODE is set to True in cfg.py

# bot difficulty
EASY = 1
MEDIUM = 2
HARD = 3

# bot stuff
BOT_CAN_PLAY = True
BOT_PLAY_FREQUENCY = 12
BOT_M_FACTOR = 3 #			how many times dx or dy can the bot move at

BOT_INSTANT_REACT = False #	TODO : put me to false before pushing (overrides BOT_SEE_FREQUENCY everywhere)
BOT_QUICK_REACT = True #	TODO : put me to false before pushing (overides BOT_SEE_FREQUENCY close to the bot)
BOT_SEE_FREQUENCY = 60 #	TODO : put me to cfg.FRAME_RATE (aka 1hz) before pushing

BOT_CAN_KICK = True
BOT_KICK_DIST = 160
BOT_REACT_DIST = 320 #		used by BOT_QUICK_REACT
BOT_KICK_FACTOR = 1
BOT_PRECISION = 50 #		max = rSize / 2 (80) : how far from the center of the racket will the AI tolerate to hit with

BOT_GO_TO_DEFAULT = True
BOT_HARD_BREAK = True
BOT_SEARCH_DEPTH = 4 #		how many bounces ahead does the AI look

# pygame (debug) stuff
if cfg.DEBUG_MODE:
	DEF_WIN_SIZE = 1280
	COL_BGR = pg.Color( 'black' )
	COL_FNT = pg.Color( 'grey25' )
	COL_OBJ = pg.Color( 'white' )

def getSign( value ):
	if value < 0:
		return -1
	if value > 0:
		return 1
	return 0

def isInZone( px, py, x1, y1, x2, y2 ):
	if px <= x1 or x2 <= px:
		return False
	if py <= y1 or y2 <= py:
		return False
	return True
