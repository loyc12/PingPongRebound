import pygame as pg
import GameObject as go
import GameControler as gc
import BotControler as ai
import PlayerControler as pl
import Addons as ad
import time #						NOTE : DEBUG
import sys #	to exit properly

# game class
class Game:
	name = "Game"

	width = 1536
	height = 1024

	size_l = 10
	size_b = 20
	size_r = 160
	size_font = 768

	speed_b = 10
	speed_r = 5
	speed_m_b = 60
	speed_m_r = 60
	framerate = 60 # 		max fps

	factor_wall = 0.75
	factor_rack = 1.10
	gravity = 0
	hard_break = False

	col_bgr = pg.Color('black')
	col_fnt = pg.Color('grey25')
	col_obj = pg.Color('white')

	last_ponger = 0
	step_count = 0
	score_mode = ad.GOALS

	last_time = time.time_ns() #			NOTE : DEBUG


	# ------------------------------------------- INITIALIZATION ------------------------------------------- #

	def __init__(self):
		self.running = False
		self.playerCount = 0
		self.controlerCount = 0
		self.racketCount = 0

		pg.init()
		self.clock = pg.time.Clock()
		self.win = pg.display.set_mode((self.width, self.height)) #		TODO : abstract away from pygame's window system
		self.font = pg.font.Font(None, self.size_font) #				TODO : abstract away from pygame's window system
		self.debug_font = pg.font.Font(None, 32) #						TODO : abstract away from pygame's window system
		pg.display.set_caption(self.name) #			 					TODO : abstract away from pygame's window system

		self.rackets = []
		self.controlers = []
		self.balls = []
		self.scores = []

		self.initRackets()
		self.initControlers()
		self.initBalls()
		self.initScores()


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.width * (1 / 2), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )

		self.racketCount = 1


	def initControlers(self):
		self.addBot("bot 1")


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (3 / 8), self.size_b, self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, self.speed_b )
		self.balls[0].setDirs( 1, 1 )


	def initScores(self):
		self.scores.append( 0 )


	# --------------------------------------------- PLAYER & AI -------------------------------------------- #

	def addBot(self, botname):
		if (self.controlerCount >= self.racketCount):
			raise Exception("Too many bots for this game")

		bot = ai.BotControler( self, botname )
		bot.setRacket( self.rackets[ len(self.controlers) ].id )
		bot.recordDefaultPos()
		bot.setFrequencyOffset( self.racketCount )
		self.controlers.append( bot )

		self.controlerCount += 1

		return ( bot )


	def makeBotsPlay(self):
		if self.playerCount < self.racketCount:
			for i in range(self.playerCount, self.controlerCount):
				if (self.controlers[i].mode == gc.ad.BOT):
					if (( self.step_count + self.controlers[i].frequency_offset ) % ad.BOT_FREQUENCY ) == 0:
						self.controlers[i].playStep()
						#time.sleep(0.25) # NOTE : DEBUG
			self.step_count += 1
			self.step_count %= ad.BOT_FREQUENCY


	def addPlayer(self, username):
		if (self.playerCount >= self.racketCount):
			raise Exception("Too many players for this game")

		player = pl.PlayerControler( self, username )
		self.controlers[self.playerCount] = player
		player.setRacket( self.rackets[ self.playerCount ].id )

		self.playerCount += 1

		return ( player )


	def isGameFull(self):
		return ( self.playerCount >= self.racketCount )


	def hasPlayer(self, username):
		for i in range(len(self.controlers)):
			if (self.controlers[i].username == username):
				return ( True )
		return ( False )


	def getPlayer(self, username):
		for i in range(len(self.controlers)):
			if (self.controlers[i].username == username):
				return ( self.controlers[i] )
		return None


	def handleUserInputs(self, username, key):
		for i in range(len(self.controlers)):
			if (self.controlers[i].username == username):
				self.controlers[i].handleInputs( key )
				return

		raise Exception("Playernot found in this game")

	# ---------------------------------------------- INTERFACE --------------------------------------------- #

	def makeMove(self, target_id, move):
		if (target_id <= 0):
			print("Error: no target selected")
			return
		if move < 0:
			return
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
			if (rack.id == target_id):
				if move == ad.NULL:
					return
				elif (move == ad.STOP):
					rack.fx = 0
					rack.fy = 0
				#elif (move == ad.BALL):
				#	for i in range(len(self.balls)):
				#		self.respawnBall( self.balls[i] )
				elif (move == ad.LEFT):
					if (self.hard_break and rack.fx > 0):
						rack.fx = 0
					else:
						rack.fx -= 1
				elif (move == ad.UP):
					if (self.hard_break and rack.fy > 0):
						rack.fy = 0
					else:
						rack.fy -= 1
				elif (move == ad.RIGHT):
					if (self.hard_break and rack.fx < 0):
						rack.fx = 0
					else:
						rack.fx += 1
				elif (move == ad.DOWN):
					if (self.hard_break and rack.fy < 0):
						rack.fy = 0
					else:
						rack.fy += 1
				else:
					print("Error: invalid move : " + str(move))
				return


	def handlePygameInputs(self, key):
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
			if key == pg.K_s or key == pg.K_DOWN:
				self.makeMove( rack.id, ad.STOP )
			elif key == pg.K_a or key == pg.K_LEFT:
				self.makeMove( rack.id, ad.LEFT )
			elif key == pg.K_d or key == pg.K_RIGHT:
				self.makeMove( rack.id, ad.RIGHT )


	# ---------------------------------------------- CORE CMDS --------------------------------------------- #

	def start(self):
		self.running = True
		print("Starting a game of " + self.name)


	def pause(self):
		self.running = False
		print("Paused a game of " + self.name)


	def stop(self):
		raise NotImplementedError("Unimplemented : game.stop()")


	def run(self):
		if self.running == False:
			print(f"{self.name} is not running")
			return

		# main game loop
		while self.running:
			self.step()
			self.debugControler() #					NOTE : DEBUG
			self.clock.tick (self.framerate)

		print("The game of " + self.name + " is over")

		pg.quit()
		sys.exit()


	def step(self):

		if self.running == False:
			print(f"{self.name} is not running")
			return

		self.moveObjects()
		self.refreshScreen()

		self.makeBotsPlay()


	def debugControler(self): #			NOTE : DEBUG : use PlayerControler class instance instead
		for event in pg.event.get():
			# quiting the game
			if event.type == pg.QUIT:
				self.running = False

			# handling key presses
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.running = False

				elif event.key == pg.K_RETURN:
					for i in range(len(self.balls)):
						self.respawnBall( self.balls[i] )

				else:
					self.handlePygameInputs( event.key )


	def getInfo(self): # NOTE : send this fct's value to the client
		raise NotImplementedError("Unimplemented : game.getInfo()")


	# ------------------------------------------- GAME MECHANICS ------------------------------------------- #

	def moveObjects(self):
		for i in range(len(self.rackets)):
			self.moveRacket(self.rackets[i])

		for i in range(len(self.balls)):
			self.moveBall(self.balls[i])


	def moveRacket(self, rack):
		rack.clampSpeed()
		rack.updatePos(self.speed_m_r)

		# prevent racket from going off screen
		if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= self.height and rack.fy > 0):
			rack.collideWall( "stop" )
		if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= self.width and rack.fx > 0):
			rack.collideWall( "stop" )

		rack.clampPos()


	def moveBall(self, ball):

		self.aplyGravity( ball )

		ball.clampSpeed()
		ball.updatePos(self.speed_m_b)
		ball.clampPos()


		self.checkRackets( ball )
		self.checkWalls( ball )
		self.checkGoals( ball )

		ball.clampSpeed()


	def aplyGravity(self, ball):
		if self.gravity != 0:
			ball.dy += self.gravity * ball.fy


	# bouncing off the rackets
	def checkRackets(self, ball):
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
			if ball.overlaps( rack ):
				ball.setPos( ball.box.centerx, rack.box.centery - self.size_b ) # '-' because the ball is going above the racket
				ball.collideRack( rack, "y" )
				self.scorePoint( rack.id, ad.HITS )


	# bouncing on the walls
	def checkWalls(self, ball):
		if ball.box.left <= 0 or ball.box.right >= self.width or ball.box.top <= 0:

			# bouncing off the sides
			if ball.box.left <= 0 or ball.box.right >= self.width:
				ball.collideWall( "x" )

			# bouncing off the top (no bounce factor)
			if ball.box.top <= 0:
				ball.collideWall( "y" )
				ball.dy /= self.factor_wall


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= self.height:
			self.scorePoint( self.last_ponger, ad.GOALS )
			self.respawnBall( ball )


	def scorePoint(self, controler_id, mode):
		if controler_id > 0:
			if mode == ad.GOALS: #		if the ball went out of bounds
				if self.score_mode == ad.GOALS: #	if goals give points
					self.scores[controler_id - 1] += 1
				else: # 							if racket hits give points
					self.scores[controler_id - 1] = 0
				self.last_ponger = 0

			elif mode == ad.HITS: #		if the ball hit a racket
				if self.score_mode == ad.HITS: #	if racket hits give points
					self.scores[controler_id - 1] += 1
				else: #								if goals give points
					pass
				self.last_ponger = controler_id
		else:
			self.last_ponger = 0


	def respawnBall(self, ball):
		ball.setDirs( -ball.fx, 1 )
		ball.setPos( ball.box.centerx, self.size_b )
		ball.setSpeeds( self.speed_b, self.speed_b )

	# ------------------------------------------- GAME RENDERING ------------------------------------------- #

	# TODO : abstract away from pygame's window system

	def refreshScreen(self):

		self.win.fill( self.col_bgr )

		self.drawScores()

		for rack in self.rackets: # 	copies the racket's data
			rack.drawSelf()

		self.drawLines()

		for ball in self.balls: # 		copies the ball's data
			ball.drawSelf()

		self.drawFps() #				NOTE : DEBUG

		pg.display.flip() #				drawing the newly prepared frame


	def drawLines(self):
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( self.width, 0 ), self.size_l * 2 )


	def drawScores(self):
		for score in self.scores: #		copies the racket's data
			text = self.font.render(f'{score}', True, self.col_fnt)
			self.win.blit( text, text.get_rect( center = ( self.width * (2 / 4), self.height * (2 / 4) )))

	delta_time = framerate * 2
	smoothness = 15

	def drawFps(self): #				NOTE : DEBUG

		new_time = time.time_ns()
		self.delta_time *= self.smoothness - 1
		self.delta_time += new_time - self.last_time
		self.delta_time /= self.smoothness
		self.last_time = new_time

		#time.sleep(0.02)

		text = self.debug_font.render(f'{int(1000000000 / self.delta_time)}', True, self.col_fnt)
		#text = self.debug_font.render(f'{int(self.clock.get_fps())}', True, self.col_fnt)
		self.win.blit( text, text.get_rect( center = ( 32, 32 )))
