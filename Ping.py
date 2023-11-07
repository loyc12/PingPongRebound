import pygame as pg
import GameObject as go
import sys	# to exit properly

# ------------------------------------------- INITIALIZATION ------------------------------------------- #

# screen setup & vars
win_w = 2048 #	window width
win_h = 1024 #	window height

pg.init()
clock = pg.time.Clock()

window = pg.display.set_mode((win_w, win_h))

pg.display.set_caption('Pongtest') #	window title

bgr_colour = pg.Color('black') #		background colour
fnt_colour = pg.Color('gray25') #		font & line colour
obj_colour = pg.Color('white') #		ball & racket colour

size_l = 10 # 							middle line width
fnt_size = 768 # 						font size
font = pg.font.Font(None, fnt_size) #	font

# game vars
size_b = 20 #	ball size & racket width
size_r = 160 #	racket lenght

speed_b = 6 #	ball default speed
speed_r = 6 #	racket speed increment

f_abs = 0.50 #	by how much the ball bounces when it hits a wall
f_rck = 1.05 #	by how much the ball bounces when it hits a racket

hard_break = True # whether the racket stops immediately when changing direction

score_1 = 0
score_2 = 0

# -------------------------------------------- GAME OBJECTS -------------------------------------------- #

# TODO : make an array of balls and rackets instead, so that the number can vary during runtime

# setting up game objects: win, _x                               , _y                  , _w    , _h
rack_1 = go.GameObject( 1, window, win_w * (1 / 4) - (size_r / 2), win_h - (2 * size_b), size_r, size_b )
rack_2 = go.GameObject( 2, window, win_w * (3 / 4) - (size_r / 2), win_h - (4 * size_b), size_r, size_b )
rack_3 = go.GameObject( 3, window, win_w * (1 / 4) - (size_r / 2), (4 * size_b)		   , size_r, size_b )
rack_4 = go.GameObject( 4, window, win_w * (3 / 4) - (size_r / 2), (2 * size_b)		   , size_r, size_b )

ball_1 = go.GameObject( 1, window, (win_w - size_b) / 2          , win_h * (3 / 4)     , size_b, size_b )
#ball_2 = go.GameObject( 2, window, (win_w - size_b) / 2          , win_h * (4 / 4)     , size_b, size_b )

# setting up object speeds
rack_1.setSpeeds( speed_r, 0 )
rack_2.setSpeeds( speed_r, 0 )
ball_1.setSpeeds( speed_b , speed_b)
#ball_2.setSpeeds( speed_b , speed_b)

# setting up ball directions
ball_1.setDirs	( 1, -1 )
#ball_2.setDirs	( -1, -1 )

# ---------------------------------------------- FUNCTIONS ---------------------------------------------- #

#  function : handling keypresses
def handleInputs(key):
	global rack_1, rack_2

	# left racket controller
	if key == pg.K_w or key == pg.K_s:
		rack_1.fx = 0
	elif key == pg.K_a:
		if hard_break and rack_1.fx > 0:
			rack_1.fx = 0
		else:
			rack_1.fx -= 1
	elif key == pg.K_d:
		if hard_break and rack_1.fx < 0:
			rack_1.fx = 0
		else:
			rack_1.fx += 1

	# right racket controller
	if key == pg.K_UP or key == pg.K_DOWN:
		rack_2.fx = 0
	elif key == pg.K_LEFT:
		if hard_break and rack_2.fx > 0:
			rack_2.fx = 0
		else:
			rack_2.fx -= 1
	elif key == pg.K_RIGHT:
		if hard_break and rack_2.fx < 0:
			rack_2.fx = 0
		else:
			rack_2.fx += 1

	rack_3.fx = rack_1.fx
	rack_3.dx = rack_1.dx
	rack_4.fx = rack_2.fx
	rack_4.dx = rack_2.dx

#  function : updating the ball position
def moveBall(ball):	#						TODO: add sound effects
	global score_1, score_2, rack_1, rack_2, rack_3, rack_4

	ball.updatePos ()

	# bouncing off the sides
	if ball.box.left <= 0 or ball.box.right >= win_w:
		ball.collide( "hor" )
		ball.dx *= f_abs

	# bounce off the rackets
	if ball.box.colliderect( rack_1.box ):
		ball.collide( "ver" )
		ball.collideWith( rack_1, "ver" )
		ball.setPos( ball.box.x, rack_1.box.y - size_b )
		ball.dy *= f_rck
	elif ball.box.colliderect( rack_2.box ):
		ball.collide( "ver" )
		ball.collideWith( rack_2, "ver" )
		ball.setPos( ball.box.x, rack_2.box.y - size_b )
		ball.dy *= f_rck
	elif ball.box.colliderect( rack_3.box ):
		ball.collide( "ver" )
		ball.collideWith( rack_3, "ver" )
		ball.setPos( ball.box.x, rack_3.box.y + size_b )
		ball.dy *= f_rck
	elif ball.box.colliderect( rack_4.box ):
		ball.collide( "ver" )
		ball.collideWith( rack_4, "ver" )
		ball.setPos( ball.box.x, rack_4.box.y + size_b )
		ball.dy *= f_rck

	# scoring a goal
	if ball.box.bottom >= win_h or ball.box.top <= 0:
		# checking who scored
		if ball.box.bottom >= win_h:
			score_1 += 1
			ball.setDirs( -ball.fx, 1 )
			ball.setPos ( (win_w - size_b) / 2, win_h * (1 / 4) )
		if ball.box.top <= 0:
			score_2 += 1
			ball.setDirs( -ball.fx, -1 )
			ball.setPos ( (win_w - size_b) / 2, win_h * (3 / 4) )

		# reseting the ball's position
		ball.setSpeeds( ball.dx * (2 / 3) , speed_b )

	ball.clampPos ()

#  function : updating the rackets position
def moveRacket(rack):
	rack.updatePos ()

	# prevent racket from going off screen
	if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= win_w and rack.fx > 0):
		rack.collide( "block" )

	rack.clampPos ()

# function : redrawing on the screen
def refreshScreen(window):

	window.fill	 ( bgr_colour )

	text_1 = font.render(f'{score_1}', True, fnt_colour)
	text_2 = font.render(f'{score_2}', True, fnt_colour)

	window.blit(text_1, text_1.get_rect(center = (win_w / 2, win_h * (1 / 4))))
	window.blit(text_2, text_2.get_rect(center = (win_w / 2, win_h * (3 / 4))))

	moveRacket	 ( rack_1 )
	moveRacket	 ( rack_2 )

	moveRacket	 ( rack_3 )
	moveRacket	 ( rack_4 )

	moveBall	 ( ball_1 )
	#moveBall	 ( ball_2 )

	rack_1.drawSelf ()
	rack_2.drawSelf ()
	rack_3.drawSelf ()
	rack_4.drawSelf ()

	pg.draw.line ( window, fnt_colour, (0, win_h / 2), (win_w, win_h / 2), size_l )

	ball_1.drawSelf ()
	#ball_2.drawSelf ()

	pg.display.flip ()	# drawing the next frame
	clock.tick ( 60 )	# max tick per second

# ---------------------------------------------- MAIN LOOP ---------------------------------------------- #

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