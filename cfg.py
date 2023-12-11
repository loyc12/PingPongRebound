# DEBUG MODE STUFF
DEBUG_MODE = False
PRINT_GAME_DEBUG = True
ADD_DEBUG_PLAYER = False

# LOGS PRINT STUFF
PRINT_PACKETS = False
PRINT_COLLISIONS = True
PRINT_FRAMES = False
PRINT_STATES = True

# WEATHER TO MOVE RACKS AND BALLS
MOVE_OBJECTS = True

# UPDATED TIME STUFF
FRAME_RATE = 60 # 					number of frames per second (normally 60)
FRAME_DELAY = 1.0 / FRAME_RATE # 	time taken for each frame
FPS_SMOOTHING = FRAME_RATE / 2 #	how many frame do we average over for FPS displaying

if DEBUG_MODE:
	FRAME_FACTOR = 0.60 #			multiplier to asy.sleep()'s time( to avoid oversleeping )
else:
	FRAME_FACTOR = 0.90
