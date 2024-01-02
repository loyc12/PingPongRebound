# DEBUG MODE STUFF
DEBUG_MODE = True
PRINT_DEBUG_INFO = True
ADD_DEBUG_PLAYER = False

# LOGS PRINT STUFF
PRINT_COLLISIONS = False
PRINT_STATES = True
PRINT_FRAMES = False
PRINT_PACKETS = False
PRINT_DEBUG = False

# GAMERULES STUFF
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
