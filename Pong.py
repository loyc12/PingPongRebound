import asyncio
import pygame as pg
import GameObject as go
import sys	# to exit properly

# TODO : make an array of balls and rackets instead, so that the number can vary during runtime
# TODO : make the ball restart's trajectory more random

# ------------------------------------------- INITIALIZATION ------------------------------------------- #

# setup & vars

pg.init()
clock = pg.time.Clock()
window = pg.display.set_mode((go.win_w, go.win_h))

pg.display.set_caption('Pongtest') #	window title

size_l = 10 # 							middle line width
fnt_size = 768 # 						font size
font = pg.font.Font(None, fnt_size) #	font

# game vars
size_b = 20 #	ball size & racket width
size_r = 160 #	racket lenght

speed_b = 10 #	ball default speed
speed_r = 6 #	racket speed increment

f_abs = 0.75 #	by how much the ball bounces when it hits a wall
f_rck = 1.10 #	by how much the ball bounces when it hits a racket

hard_break = True # whether the racket stops immediately when changing direction

score_1 = 0
score_2 = 0

# -------------------------------------------- GAME OBJECTS -------------------------------------------- #

# TODO : make an array of balls and rackets instead, so that the number can vary during runtime

# setting up game objects: win   , _x                , _y          , _w    , _h
rack_1 = go.GameObject( 1, window, size_b            , go.win_h / 2, size_b, size_r )
rack_2 = go.GameObject( 2, window, go.win_w - size_b , go.win_h / 2, size_b, size_r )
ball_1 = go.GameObject( 1, window, go.win_w * (1 / 4), go.win_h / 2, size_b, size_b )
#ball_2 = go.GameObject( 2, window, go.win_w * (3 / 4), go.win_h / 2, size_b, size_b )

# setting up object speeds
rack_1.setSpeeds( 0, speed_r )
rack_2.setSpeeds( 0, speed_r )
ball_1.setSpeeds( speed_b, speed_b)
#ball_2.setSpeeds( speed_b, speed_b)

# setting up ball directions
ball_1.setDirs	( 1, 1 )
#ball_2.setDirs	( -1, -1 )

# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #

#  function : handling keypresses
def handleInputs(key):
	global rack_1, rack_2

	# left racket controller
	if key == pg.K_a or key == pg.K_d:
		rack_1.fy = 0

	elif key == pg.K_w:
		if hard_break and rack_1.fy > 0:
			rack_1.fy = 0
		else:
			rack_1.fy -= 1

	elif key == pg.K_s:
		if hard_break and rack_1.fy < 0:
			rack_1.fy = 0
		else:
			rack_1.fy += 1

	# right racket controller
	if key == pg.K_LEFT or key == pg.K_RIGHT:
		rack_2.fy = 0

	elif key == pg.K_UP:
		if hard_break and rack_2.fy > 0:
			rack_2.fy = 0
		else:
			rack_2.fy -= 1

	elif key == pg.K_DOWN:
		if hard_break and rack_2.fy < 0:
			rack_2.fy = 0
		else:
			rack_2.fy += 1

#  function : updating the ball position
def moveBall(ball):
	global rack_1, rack_2, score_1, score_2

	ball.updatePos ()

	# bouncing off the top and bottom
	if ball.box.top <= 0 or ball.box.bottom >= go.win_h:
		ball.collideWall( "ver" )
		ball.dy *= f_abs
		ball.clampSpeed()

	# bounce off the rackets
	if ball.box.colliderect( rack_1.box ):
		ball.collideWall( "hor" )
		ball.collideRack( rack_1, "hor" )
		ball.setPos( rack_1.box.centerx + size_b, ball.box.centery )
		ball.dx *= f_rck
	elif ball.box.colliderect( rack_2.box ):
		ball.collideWall( "hor" )
		ball.collideRack( rack_2, "hor" )
		ball.setPos( rack_2.box.centerx - size_b, ball.box.centery )
		ball.dx *= f_rck

	# scoring a goal
	if ball.box.left <= 0 or ball.box.right >= go.win_w:
		# checking who scored
		if ball.box.left <= 0:
			score_2 += 1
			ball.setDirs( -1, -ball.fy )
			ball.setPos (go.win_w * (3 / 4), (go.win_h - size_b) / 2 )
		elif ball.box.right >= go.win_w:
			score_1 += 1
			ball.setDirs( 1, -ball.fy )
			ball.setPos (go.win_w * (1 / 4), (go.win_h - size_b) / 2 )

		# reseting the ball's speed
		ball.setSpeeds( speed_b, ball.dy )
		ball.clampSpeed()

	ball.clampPos ()

#  function : updating the rackets position
def moveRacket(rack):

	rack.updatePos ()

	# prevent racket from going off screen
	if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= go.win_h and rack.fy > 0):
		rack.collideWall( "wall" )

	rack.clampPos ()

# function : redrawing on the screen
def refreshScreen(window):

	window.fill	 ( go.bgr_colour )
	pg.draw.line ( window, go.fnt_colour, (go.win_w / 2, 0), (go.win_w / 2, go.win_h), size_l )

	text_1 = font.render(f'{score_1}', True, go.fnt_colour)
	text_2 = font.render(f'{score_2}', True, go.fnt_colour)

	window.blit(text_1, text_1.get_rect(center = (go.win_w * (1 / 4), go.win_h / 2)))
	window.blit(text_2, text_2.get_rect(center = (go.win_w * (3 / 4), go.win_h / 2)))

	moveRacket	 ( rack_1 )
	moveRacket	 ( rack_2 )
	moveBall	 ( ball_1 )
	#moveBall	 ( ball_2 )

	rack_1.drawSelf ()
	rack_2.drawSelf ()
	ball_1.drawSelf ()
	#ball_2.drawSelf ()

	pg.display.flip ()			# drawing the next frame
	clock.tick ( go.framerate )	# max tick per second

# ---------------------------------------------- MAIN LOOP ---------------------------------------------- #

async def run():

	# game logic loop
	while True:

		# handling inputs
		for event in pg.event.get ():

			# quiting the game
			if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
				pg.quit ()
				sys.exit ()
			elif event.type == pg.KEYDOWN:
				handleInputs( event.key )

		refreshScreen( window )

		await asyncio.sleep(0)

if __name__ == '__main__':
	asyncio.run( run() )