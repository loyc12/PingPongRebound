# DEBUG MODE STUFF
DEBUG_MODE = True
PRINT_DEBUG = True #		screen debug info (for debug_mode / pygame only)
ADD_DEBUG_PLAYER = False #	adds a player to every game (for debug_mode / pygame only)

# LOGS PRINT STUFF
PRINT_COLLISIONS = False #	racket and wall collisions
PRINT_PACKETS = False #		client packets to be sent
PRINT_FRAMES = False #		frame processing info
PRINT_STATES = False #		general game status (starting, ending, etc)
PRINT_POINTS = True #		point changes (scoring and reseting)
PRINT_EXTRA = False #		random additional info (clamping and shit)
PRINT_MOVES = True #		player moves, if PRINT_BOTS : bot moves
PRINT_BOTS = False #		bot creation

# GAMERULES STUFF
BOT_DIFFICULTY = 3 #		1 is easy, 3 is hard (normally 3)
MOVE_OBJECTS = True
FORCE_MODE = False

# UPDATED TIME STUFF
FRAME_RATE = 60 # 					number of frames per second (normally 60)
FRAME_DELAY = 1.0 / FRAME_RATE # 	time taken for each frame
FPS_SMOOTHING = FRAME_RATE / 2 #	how many frame do we average over for FPS displaying

if DEBUG_MODE:
	FRAME_FACTOR = 0.60 #			multiplier to asy.sleep()'s time( to avoid oversleeping )
else:
	FRAME_FACTOR = 0.90
