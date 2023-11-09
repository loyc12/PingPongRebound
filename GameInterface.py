import pygame as pg
import GameObject as go
import sys	# to exit properly

class Game:
	name = "unnamed"

	width = 2048
	height = 1024

	rackCount = 1
	ballCount = 1
	scoreCount = 1

	size_l = 10
	size_b = 20
	size_r = 160
	size_font = 768

	speed_b = 6
	speed_r = 6
	speed_m = 60
	framerate = 60 # 		max fps

	factor_wall = 0.75
	factor_rack = 1.00
	gravity = 0.4
	hard_break = True

	col_bgr = pg.Color('black')
	col_fnt = pg.Color('grey25')
	col_obj = pg.Color('white')

	# ------------------------------------------- INITIALIZATION ------------------------------------------- #

	def __init__(self):
		self.running = False

		pg.init()
		self.clock = pg.time.Clock()
		self.win = pg.display.set_mode((self.width, self.height)) #		TODO : abstract away from pygame's window system
		self.font = pg.font.Font(None, self.size_font) #				TODO : abstract away from pygame's window system
		pg.display.set_caption(self.name) #			 					TODO : abstract away from pygame's window system

		self.rackets = []
		self.balls = []
		self.scores = []

		self.initRackets()
		self.initBalls()
		self.initScores()


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.width * (2 / 4), self.height - self.size_b , self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )

	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (3 / 8), self.height * (1 / 8) , self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, 0 )
		self.balls[0].setDirs( 1, 1 )


	def initScores(self):
		self.scores.append( 0 )


	def reset(self):
		raise NotImplementedError("Unimplemented : game.reset()")


	# ---------------------------------------------- INTERFACE --------------------------------------------- #

	def makeMove(self, target_id, move):
		if (target_id <= 0):
			print("Error: no target selected")
			return
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
			if (rack.id == target_id):
				if (move == "LEFT"):
					if (self.hard_break and rack.fx > 0):
						rack.fx = 0
					else:
						rack.fx -= 1
				elif (move == "RIGHT"):
					if (self.hard_break and rack.fx < 0):
						rack.fx = 0
					else:
						rack.fx += 1
				elif (move == "UP"):
					if (self.hard_break and rack.fy > 0):
						rack.fy = 0
					else:
						rack.fy -= 1
				elif (move == "DOWN"):
					if (self.hard_break and rack.fy < 0):
						rack.fy = 0
					else:
						rack.fy += 1
				elif (move == "STOP"):
					rack.fx == 0
					rack.fy == 0
				else:
					print("Error: invalid move")
					return


	def handleInputs(self, key):
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
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
			self.clock.tick (self.framerate)

		print("Game " + self.name + " is over")

		pg.quit()
		sys.exit()



	def step(self):

		if self.running == False:
			print("Game " + self.name + " is not running")
			return

		self.pgLoop()

		self.moveObjects()
		self.refreshScreen()


	def pgLoop(self): #						TODO : abstract away from pygame's event system
		for event in pg.event.get():

			# quiting the game
			if event.type == pg.QUIT or ( event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE ):
				self.running = False

			# handling key presses
			elif event.type == pg.KEYDOWN:
				self.handleInputs( event.key )


	# ------------------------------------------- GAME MECHANICS ------------------------------------------- #

	def moveObjects(self):

		for i in range(len(self.rackets)):
			self.moveRacket(self.rackets[i])

		for i in range(len(self.balls)):
			self.moveBall(self.balls[i])


	def moveRacket(self, rack):
		rack.clampSpeed()
		rack.updatePos()

		# prevent racket from going off screen
		if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= self.height and rack.fy > 0):
			rack.collideWall( "stop" )
		if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= self.width and rack.fx > 0):
			rack.collideWall( "stop" )

		rack.clampPos()


	def moveBall(self, ball):
		if self.gravity != 0:
			if ball.fy > 0:
				ball.dy += self.gravity
			else:
				ball.dy -= self.gravity

		ball.clampSpeed()
		ball.updatePos()

		self.checkWalls( ball )
		self.checkRackets( ball )
		self.checkGoals( ball )

		ball.clampPos()

	# bouncing on the walls
	def checkWalls(self, ball):
		if ball.box.left <= 0 or ball.box.right >= self.width or ball.box.top <= 0:

			# bouncing off the sides
			if ball.box.left <= 0 or ball.box.right >= self.width:
				ball.collideWall( "x" )

			# bouncing off the top
			if ball.box.top <= 0:
				ball.collideWall( "y" )
				ball.dy = 1

			ball.dx *= self.factor_wall
			ball.clampSpeed()

	# bouncing off the rackets
	def checkRackets(self, ball):
		for rack in self.rackets: #		copies the racket's data
			if ball.overlaps( rack ):
				ball.collideWall( "y" )
				ball.dy *= self.factor_rack
				ball.clampSpeed()
				ball.collideRack( rack, "y" )
				ball.setPos( ball.box.centerx, rack.box.centery - self.size_b ) # '-' because the ball is going above the racket
				self.scores[0] += 1


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= self.height:
			self.scores[0] = 0
			ball.setDirs( -ball.fx, 1 )
			ball.setPos( ball.box.centerx, 0 )
			ball.setSpeeds( (ball.dx + self.speed_b) / 2, 0)
			ball.clampSpeed()


	# ------------------------------------------- GAME RENDERING ------------------------------------------- #

	# TODO : abstract away from pygame's window system

	def refreshScreen(self):

		self.win.fill( self.col_bgr )

		for rack in self.rackets: # 	copies the racket's data
			rack.drawSelf()

		self.drawScores()
		self.drawLines()

		for ball in self.balls: # 		copies the ball's data
			ball.drawSelf()

		pg.display.flip() #				drawing the newly prepared frame


	def drawLines(self):
		#pg.draw.line ( self.win, self.col_fnt, ( self.width / 2, 0 ),  ( self.width / 2, self.height ), self.size_l )
		#pg.draw.line ( self.win, self.col_fnt, ( 0, self.height / 2 ), ( self.width, self.height / 2 ), self.size_l )
		pass


	def drawScores(self):
		for score in self.scores: #		copies the racket's data
			text = self.font.render(f'{score}', True, self.col_fnt)
			self.win.blit( text, text.get_rect( center = ( self.width * (2 / 4), self.height * (2 / 4) )))
