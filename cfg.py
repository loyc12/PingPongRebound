# DEBUG MODE STUFF (only active with DEBUG_MODE ( pygame ))
DEBUG_MODE = True
FORCE_MODE = False #		forces the gameMode to be df.FORCE_MODE_TO
PRINT_DEBUG = True #		shows fps and racket names
MOVE_OBJECTS = True #		allows objects to move
ADD_DEBUG_PLAYER = True #	adds a player to every game

# LOGS PRINT STUFF
PRINT_COLLISIONS = False #	racket and wall collisions
PRINT_PACKETS = False #		client packets to be sent
PRINT_FRAMES = False #		frame processing info
PRINT_STATES = True #		general game status (starting, ending, etc)
PRINT_POINTS = True #		point changes (scoring and reseting)
PRINT_EXTRA = False #		random additional info (clamping and shit)
PRINT_MOVES = True #		player moves, if PRINT_BOTS : bot moves
PRINT_BOTS = False #			bot creation ans other bot related things

# GAMERULES STUFF
BOT_DIFFICULTY = 3 #		1 is easy, 3 is hard (DEFAULT IS 3)

# UPDATED TIME STUFF
FRAME_RATE = 60 # 					number of frames per second (DEFAULT IS 60)
FRAME_DELAY = 1.0 / FRAME_RATE # 	time taken for each frame
FPS_SMOOTHING = FRAME_RATE / 2 #	how many frame do we average over for FPS displaying

if DEBUG_MODE:
	FRAME_FACTOR = 0.60 #			multiplier to asy.sleep()'s time( to avoid oversleeping )
else:
	FRAME_FACTOR = 0.90
