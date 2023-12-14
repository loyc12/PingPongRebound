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
GOALS = 1
HITS = 2

WIN_SCORE = 420

# game states
STARTING = 1
PLAYING = 2
ENDING = 3

# end states
END_WIN = "win"
END_QUIT = "quit"
END_ABORT = "abort"

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
BOT_INSTANT_REACT = False #	TODO : put me to false before pushing
BOT_HARD_BREAK = True
BOT_NO_STUCK = True

BOT_M_FACTOR = 4 #			how many times dx or dy can the racket go at
BOT_PRECISION = 30 #		max = rSize / 2 : buffer zones one each side of the racket the AI tries to avoid hitting the ball with
BOT_SEARCH_DEPTH = 5 #		how many bounces ahead does the AI look

BOT_PLAY_FREQUENCY = 15
BOT_SEE_FREQUENCY = 30 #	TODO : put me to 60 before pushing
BOT_KICK_DISTANCE = 160
BOT_KICK_FACTOR = 2

# pygame (debug) stuff
if cfg.DEBUG_MODE:
	WIN_SIZE = 1280
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
