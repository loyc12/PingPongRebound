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

speed_b = 10 #	ball default speed
speed_r = 6 #	racket speed increment

f_abs = 0.75 #	by how much the ball bounces when it hits a wall
f_rck = 0.85 #	by how much the ball bounces when it hits a racket
gravity = 0.2 #	by how much the ball accelerates down every frame

hard_break = True # whether the racket stops immediately when changing direction

score_1 = 0
score_2 = 0

# -------------------------------------------- GAME OBJECTS -------------------------------------------- #

# TODO : make an array of balls and rackets instead, so that the number can vary during runtime

# setting up game objects: win, _x                               , _y                  , _w    , _h
rack_1 = go.GameObject( 1, window, win_w * (1 / 4) - (size_r / 2), win_h - (2 * size_b), size_r, size_b )
rack_2 = go.GameObject( 2, window, win_w * (3 / 4) - (size_r / 2), win_h - (2 * size_b), size_r, size_b )
ball_1 = go.GameObject( 1, window, (win_w - size_b) / 2          , win_h / 3           , size_b, size_b )
#ball_2 = go.GameObject( 2, window, (win_w - size_b) / 2         , win_h / 3           , size_b, size_b )

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

#  function : updating the ball position
def moveBall(ball):	#						TODO: add sound effects
	global score_1, score_2, rack_1, rack_2

	if ball.fy > 0:
		ball.dy += gravity
	else:
		ball.dy -= gravity

	ball.updatePos ()

	# bouncing off the sides
	if ball.box.left <= 0 or ball.box.right >= win_w:
		ball.collide( "hor" )
		ball.dx *= f_abs

	# bouncing off the top
	if ball.box.top <= 0:
		ball.collide( "ver" )
		ball.dy *= f_abs

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

	# scoring a goal
	if ball.box.bottom >= win_h:
		# checking who scored
		if ball.box.left <= win_w / 2:
			score_2 += 1
			ball.setDirs( -1, -1 )
		if ball.box.right >= win_w / 2:
			score_1 += 1
			ball.setDirs( 1, -1 )

		# reseting the ball's position
		ball.setPos   ( (win_w - size_b) / 2, win_h / 3 )
		ball.setSpeeds( ball.dx * (2 / 3) , speed_b )

	ball.clampPos ()

#  function : updating the rackets position
def moveRacket(rack):
	rack.updatePos ()

	# prevent racket from going off screen
	if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= win_w and rack.fx > 0):
		rack.collide( "block" )

	# prevent racket from crossing the middle line
	if rack.id == 1 and rack.box.right > win_w / 2:
		rack.collide( "block" )
		rack.setPos( (win_w / 2) - size_r, rack.box.y )
	elif rack.id == 2 and rack.box.left < win_w / 2:
		rack.collide( "block" )
		rack.setPos( win_w / 2, rack.box.y )

	rack.clampPos ()

# function : redrawing on the screen
def refreshScreen(window):

	window.fill	 ( bgr_colour )

	text_1 = font.render(f'{score_1}', True, fnt_colour)
	text_2 = font.render(f'{score_2}', True, fnt_colour)

	window.blit(text_1, text_1.get_rect(center = (win_w * (1 / 4), win_h / 2)))
	window.blit(text_2, text_2.get_rect(center = (win_w * (3 / 4), win_h / 2)))

	moveRacket	 ( rack_1 )
	moveRacket	 ( rack_2 )
	moveBall	 ( ball_1 )
	#moveBall	 ( ball_2 )

	rack_1.drawSelf ()
	rack_2.drawSelf ()

	pg.draw.line ( window, fnt_colour, (win_w / 2, 0), (win_w / 2, win_h), size_l )

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