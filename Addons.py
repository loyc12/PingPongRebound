
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

# score modes
GOALS = 0
HITS = 1

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
WIN_SIZE = 256


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