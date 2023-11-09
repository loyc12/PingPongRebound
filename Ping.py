import pygame as pg
import GameObject as go
import sys	# to exit properly

# TODO : make an array of balls and rackets instead, so that the number can vary during runtime



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
f_rck = 0.95 #	by how much the ball bounces when it hits a racket

score_1 = 0
score_2 = 0

gravity = 0.4 #	by how much the ball accelerates down every frame

# -------------------------------------------- GAME OBJECTS -------------------------------------------- #

# TODO : make an array of balls and rackets instead, so that the number can vary during runtime

# setting up game objects: win   , _x                , _y                , _w    , _h
rack_1 = go.GameObject( 1, window, go.win_w * (1 / 4), go.win_h - size_b , size_r, size_b )
rack_2 = go.GameObject( 2, window, go.win_w * (3 / 4), go.win_h - size_b , size_r, size_b )
ball_1 = go.GameObject( 1, window, go.win_w / 2      , go.win_h * (2 / 3), size_b, size_b )
#ball_2 = go.GameObject( 2, window, go.win_w / 2      , go.win_h * (2 / 3), size_b, size_b )

# setting up object speeds
rack_1.setSpeeds( speed_r, 0 )
rack_2.setSpeeds( speed_r, 0 )
ball_1.setSpeeds( speed_b * (2 / 3), speed_b * 2 )
#ball_2.setSpeeds( speed_b * (2 / 3), speed_b * 2 )

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
		if go.hard_break and rack_1.fx > 0:
			rack_1.fx = 0
		else:
			rack_1.fx -= 1
	elif key == pg.K_d:
		if go.hard_break and rack_1.fx < 0:
			rack_1.fx = 0
		else:
			rack_1.fx += 1

	# right racket controller
	if key == pg.K_UP or key == pg.K_DOWN:
		rack_2.fx = 0
	elif key == pg.K_LEFT:
		if go.hard_break and rack_2.fx > 0:
			rack_2.fx = 0
		else:
			rack_2.fx -= 1
	elif key == pg.K_RIGHT:
		if go.hard_break and rack_2.fx < 0:
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

	ball.updatePos  ()
	ball.clampSpeed ()

	# bouncing off the sides
	if ball.box.left <= 0 or ball.box.right >= go.win_w:
		ball.collideWall( "x" )
		ball.dx *= f_abs

	# bouncing off the top
	if ball.box.top <= 0:
		ball.collideWall( "y" )
		ball.dx *= f_abs
		ball.dy = 1

	# bounce off a racket
	if ball.box.colliderect( rack_1.box ) or ball.box.colliderect( rack_2.box ):
		ball.collideWall( "y" )
		ball.dy *= f_rck
		ball.clampSpeed()

		if ball.box.colliderect( rack_1.box ):
			ball.collideRack( rack_1, "y" )
			ball.setPos( ball.box.centerx, rack_1.box.centery - size_b )
		elif ball.box.colliderect( rack_2.box ):
			ball.collideRack( rack_2, "y" )
			ball.setPos( ball.box.centerx, rack_2.box.centery - size_b )

	# scoring a goal
	if ball.box.bottom >= go.win_h:
		# checking who scored
		if ball.box.left <= go.win_w / 2:
			score_2 += 1
			ball.setDirs( -1, -1 )
		if ball.box.right >= go.win_w / 2:
			score_1 += 1
			ball.setDirs( 1, -1 )

		# reseting the ball's position
		ball.setPos   ( (go.win_w - size_b) / 2, go.win_h * (2 / 3) )
		ball.setSpeeds( (ball.dx + speed_b) / 3, speed_b * 2 )
		ball.clampSpeed()

	ball.clampPos ()

#  function : updating the rackets position
def moveRacket(rack):
	rack.updatePos ()

	# prevent racket from going off screen
	if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= go.win_w and rack.fx > 0):
		rack.collideWall( "stop" )

	# prevent racket from crossing the middle line
	if rack.id == 1 and rack.box.right > go.win_w / 2:
		rack.collideWall( "stop" )
		rack.setPos( (go.win_w - size_r) / 2, rack.box.centery )
	elif rack.id == 2 and rack.box.left < go.win_w / 2:
		rack.collideWall( "stop" )
		rack.setPos( (go.win_w + size_r) / 2, rack.box.centery )

	rack.clampPos ()

# function : redrawing on the screen
def refreshScreen(window):

	window.fill	 ( go.bgr_colour )

	text_1 = font.render(f'{score_1}', True, go.fnt_colour)
	text_2 = font.render(f'{score_2}', True, go.fnt_colour)

	window.blit(text_1, text_1.get_rect(center = (go.win_w * (1 / 4), go.win_h / 2)))
	window.blit(text_2, text_2.get_rect(center = (go.win_w * (3 / 4), go.win_h / 2)))

	rack_1.drawSelf ()
	rack_2.drawSelf ()

	pg.draw.line ( window, go.fnt_colour, (go.win_w / 2, 0), (go.win_w / 2, go.win_h), size_l )

	ball_1.drawSelf ()
	#ball_2.drawSelf ()

	pg.display.flip ()			# drawing the next frame

def moveObjects():
	moveRacket	 ( rack_1 )
	moveRacket	 ( rack_2 )

	moveBall	 ( ball_1 )
	#moveBall	 ( ball_2 )

# ---------------------------------------------- MAIN LOOP ---------------------------------------------- #

def run():

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

		moveObjects  ()
		refreshScreen( window )
		clock.tick ( go.framerate )	# max tick per second

if __name__ == '__main__':
	run()