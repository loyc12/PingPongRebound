
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

# bot stuff
BOT_FREQUENCY = 10


def getSign(value):
	if value < 0:
		return -1
	if value > 0:
		return 1
	return 0