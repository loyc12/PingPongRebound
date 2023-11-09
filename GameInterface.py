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
	height = 1024
	size_font = 768

	factor_wall = 1.00
	factor_rack = 1.00
	gravity = 0.5
	hard_break = True
	framerate = 60 # 					max fps

	col_bgr = pg.Color('black')
	col_fnt = pg.Color('grey25')
	col_obj = pg.Color('white')

	# ------------------------------------------- INITIALIZATION ------------------------------------------- #

	def __init__(self, _name):
		self.running = False
		self.name = _name

		pg.init()
		self.clock = pg.time.Clock()
		self.win = pg.display.set_mode((self.width, self.height)) #		TODO : abstract away from pygame's window ystem
		self.font = pg.font.Font(None, self.size_font) #				TODO : abstract away from pygame's window system
		pg.display.set_caption(_name) #			 						TODO : abstract away from pygame's window system

		self.rackets = []
		self.balls = []
		self.scores = []

		self.initRackets()
		self.initBalls()
		self.initScores()


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self.win, self.width * (2 / 4), self.height - self.size_b , self.size_r, self.size_b ))


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self.win, self.width * (2 / 4), self.height * (1 / 16) , self.size_b, self.size_b ))
		self.balls[0].setSpeeds( 0, 0 )


	def initScores(self):
		self.scores.append( 0 )


	def reset(self):
		raise NotImplementedError("Unimplemented : game.reset()")


	# ---------------------------------------------- INTERFACE --------------------------------------------- #

	def makeMove(self, target_id, move):
		if (target_id <= 0):
			print("Error: no target selected")
			return
		for rack in self.rackets:
			if (rack.id == target_id):
				if (move == "LEFT"):
					if (go.hard_break and rack.fx > 0):
						rack.fx = 0
					else:
						rack.fx -= 1
				elif (move == "RIGHT"):
					if (go.hard_break and rack.fx < 0):
						rack.fx = 0
					else:
						rack.fx += 1
				elif (move == "UP"):
					if (go.hard_break and rack.fy > 0):
						rack.fy = 0
					else:
						rack.fy -= 1
				elif (move == "DOWN"):
					if (go.hard_break and rack.fy < 0):
						rack.fy = 0
					else:
						rack.fy += 1
				elif (move == "STOP"):
					rack.fx == 0
					rack.fy == 0
				else:
					print("Error: invalid move")
					return

				print(f" > Moved rack_{target_id} {move} successfully")

	def handleInputs(self, key):
		for rack in self.rackets:
			if key == pg.K_s or key == pg.K_DOWN:
				self.makeMove( rack.id, "STOP" )
			elif key == pg.K_a or key == pg.K_LEFT:
				self.makeMove( rack.id, "LEFT" )
			elif key == pg.K_d or key == pg.K_RIGHT:
				self.makeMove( rack.id, "RIGHT" )

	# ---------------------------------------------- CORE CMDS --------------------------------------------- #

	def start(self):
		self.running = True
		print("Starting game " + self.name)


	def stop(self):
		self.running = False
		print("Stopping game " + self.name)


	def getState(self):
		raise NotImplementedError("Unimplemented : game.getState()")


	def run(self):

		if self.running == False:
			print("Game " + self.name + " is not running")
			return

		# main game loop
		while self.running:
			self.step()

		print("Game " + self.name + " is over")


	def step(self):

		if self.running == False:
			print("Game " + self.name + " is not running")
			return

		self.pygameInputs() #	TODO : abstract away from pygame's event system

		self.moveObjects()
		self.refreshScreen()
		self.clock.tick (self.framerate)

	def pygameInputs(self):
		for event in pg.event.get():

			# quiting the game
			if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
				pg.quit()
				sys.exit()

			# handling key presses
			elif event.type == pg.KEYDOWN:
				self.handleInputs( event.key )


	# ------------------------------------------- GAME MECHANICS ------------------------------------------- #

	def moveObjects(self):

		for rack in self.rackets:
			self.moveRacket(rack)

		for ball in self.balls:
			self.moveBall(ball)


	def moveRacket(self, rack):
		rack.clampSpeed ()
		rack.updatePos()

		# prevent racket from going off screen
		if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= go.win_h and rack.fy > 0):
			rack.collideWall( "stop" )
		if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= go.win_w and rack.fx > 0):
			rack.collideWall( "stop" )

		rack.clampPos()


	def moveBall(self, ball):
		if self.gravity != 0:
			if ball.fy > 0:
				ball.dy += self.gravity
			else:
				ball.dy -= self.gravity

		ball.clampSpeed()

		self.checkWalls( ball )
		self.checkRackets( ball )
		self.checkGoals( ball )

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
				self.scores[0] += 1


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= go.win_h:
			self.scores[0] = 0
			ball.setDirs( -ball.fx / 2, 0 )

			# reseting the ball's position
			ball.setPos( ball.box.centerx, 0 )
			ball.setSpeeds( (ball.dx + self.speed_b) / 3, (ball.dy + self.speed_b) / 3)
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
		#pg.draw.line ( self.win, self.col_fnt, ( self.width / 2, 0 ),  ( self.width / 2, self.height ), self.size_l )
		#pg.draw.line ( self.win, self.col_fnt, ( 0, self.height / 2 ), ( self.width, self.height / 2 ), self.size_l )
		return


	def drawScores(self):
		for score in self.scores:
			text = self.font.render(f'{score}', True, self.col_fnt)
			self.win.blit( text, text.get_rect( center = ( self.width * (2 / 4), self.height * (2 / 4) )))
