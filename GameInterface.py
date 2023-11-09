import pygame as pg
import GameObject as go
import sys	# to exit properly

class Game:

	rackCount = 1
	ballCount = 1
	scoreCount = 1

	size_l = 10
	size_b = 20
	size_r = 160
	width = 2048
	height = 1536

	factor_wall = 1.00
	factor_rack = 1.00

	font = pg.font.Font(None, 768) #	score font
	framerate = 60 # 					max fps

	col_bgr = pg.Color('black')
	col_fnt = pg.Color('grey25')
	col_obj = pg.Color('white')

	# ------------------------------------------- INITIALIZATION ------------------------------------------- #

	def __init__(self, _name):
		self.name = _name

		pg.init()
		self.clock = pg.time.Clock()
		self.win = pg.display.set_mode((self.width, self.height)) #			TODO : abstract away from pygame's window system
		pg.display.set_caption(_name) #			 							TODO : abstract away from pygame's window system

		self.rackets[self.rackCount]
		self.balls[self.ballCount]
		self.scores[self.scoreCount]

		self.running = False

	# ---------------------------------------------- INTERFACE --------------------------------------------- #

	def giveInput(self, _id, _input):
		raise NotImplementedError("Subclass must implement giveInput method")

	# ---------------------------------------------- CORE CMDS --------------------------------------------- #

	def start(self):
		self.running = True
		print("Starting game " + self.name)


	def stop(self):
		self.running = False
		print("Stopping game " + self.name)


	def reset(self):
		raise NotImplementedError("Subclass must implement reset method")


	def getState(self):
		raise NotImplementedError("Subclass must implement getState method")


	# game logic loop
	def run(self):

		if self.running == False:
			print("Game " + self.name + " is not running")
			return

		# main game loop
		while self.running:
			self.step()

		print("Game " + self.name + " is finished")


	def step(self):
		# handling inputs
		for event in pg.event.get ():

			# quiting the game
			if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
				pg.quit ()
				sys.exit ()
			elif event.type == pg.KEYDOWN:
				self.handleInputs( event.key )

		self.moveObjects()
		self.refreshScreen()
		self.clock.tick ()

	# ------------------------------------------- GAME MECHANICS ------------------------------------------- #

	def moveObjects(self):

		for rack in self.rackets:
			self.moveRacket(rack)

		for ball in self.balls:
			self.moveBall(ball)


	def moveRacket(self, rack):
		rack.clampSpeed ()
		rack.updatePos  ()

		# prevent racket from going off screen
		if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= go.win_h and rack.fy > 0):
			rack.collideWall( "stop" )
		if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= go.win_w and rack.fx > 0):
			rack.collideWall( "stop" )

		rack.clampPos   ()


	def moveball(self, ball):
		ball.clampSpeed ()

		self.checkWalls(ball)
		self.checkRackets(ball)
		self.checkGoals(ball)

		ball.updatePos()
		ball.clampPos()

	# bouncing on the walls
	def checkWalls(self, ball):
		# bouncing off the top and bottom
		if ball.box.top <= 0 or ball.box.bottom >= go.win_h:
			ball.collideWall( "y" )
			ball.dy *= self.factor_wall
			ball.clampSpeed()

		# bouncing off the left and right
		if ball.box.left <= 0 or ball.box.right >= go.win_w:
			ball.collideWall( "x" )
			ball.dx *= self.factor_wall
			ball.clampSpeed()


	# bouncing off the rackets
	def checkRackets(self, ball):
		for rack in self.rackets:
			if ball.overlaps( rack ):
				ball.collideWall( "y" )
				ball.dy *= self.factor_rack
				ball.clampSpeed()
				ball.collideRack( rack, "y" )
				ball.setPos( ball.box.centerx, rack.box.centery - self.size_b ) # '-' because the ball is going above the racket

	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= go.win_h:
			# updating all (1) scores
			for score in self.scores:
				score += 1
			ball.setDirs( -ball.fx / 2, 0 )

			# reseting the ball's position
			ball.setPos( 0, go.win_h / 2 )
			ball.setSpeeds( (ball.dx + self.speed_b) / 3, self.speed_b / 2)
			ball.clampSpeed()


	# ------------------------------------------- GAME RENDERING ------------------------------------------- #

	# TODO : abstract away from pygame's window system

	def refreshScreen(self):

		self.win.fill( go.bgr_colour )

		for rack in self.rackets:
			rack.drawSelf()

		self.drawScores()
		self.drawLines()

		for ball in self.balls:
			ball.drawSelf()

		pg.display.flip()	# drawing the newly prepared frame


	def drawLines(self):
		pg.draw.line ( self.win, self.col_fnt, ( self.width / 2, 0 ), ( self.width / 2, self.height ), self.size_l )


	def drawScores(self):
		for score in self.scores:
			text = self.font.render(f'{score}', True, self.col_fnt)
			self.win.blit( text, text.get_rect( center = ( self.width * (2 / 4), self.height * (2 / 4) ) ) )