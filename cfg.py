DEBUG_MODE = False
PRINT_GAME_DEBUG = True

PRINT_PACKETS = True
PRINT_COLLISIONS = True
PRINT_FRAMES = True

MOVE_OBJECTS = True

FRAME_RATE = 60 # 					number of frames per second
FRAME_DELAY = 1.0 / FRAME_RATE # 	time taken for each frame
FPS_SMOOTHING = FRAME_RATE / 2 #	how many frame do we average over for FPS displaying

if DEBUG_MODE:
	FRAME_FACTOR = 0.60 #			multiplier to asy.sleep()'s time (to avoid oversleeping)
else:
	FRAME_FACTOR = 0.90
