DEBUG_MODE = False
MOVE_OBJECTS = True



FRAME_RATE = 60 # 					number of frames per second
FRAME_DELAY = 1.0 / FRAME_RATE # 	time taken for each frame
FPS_SMOOTHING = FRAME_RATE / 3 #	how many frame do we average over for FPS displaying

if DEBUG_MODE:
	FRAME_FACTOR = 0.75 #			multiplier sleep time (to help avoid oversleeping)
else:
	FRAME_FACTOR = 0.90
