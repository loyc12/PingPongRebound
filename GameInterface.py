import time
import asyncio as asy

try:
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg
		import sys #	to exit properly
	from master import go
	from master import gc

	import PlayerControler as pl
	import BotControler as bc
	import defs as df

except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	from game.PingPongRebound.master import go
	from game.PingPongRebound.master import gc

	import game.PingPongRebound.PlayerControler as pl
	import game.PingPongRebound.BotControler as bc
	import game.PingPongRebound.defs as df

# game class
class Game:
	name = "Game"
	mode = df.SOLO
	racketCount = 1
	state = df.STARTING
	hard_break = False

	width = 1536
	height = 1024
	invW = 1.0 / width
	invH = 1.0 / height

	size_b = 20
	size_r = 160

	size_l = 10
	size_font = 768

	speed_b = 10
	speed_r = 5
	speed_m_b = 60
	speed_m_r = 60
	framerate = cfg.FRAME_RATE # 		max fps

	factor_wall = 0.75
	factor_rack = 1.10
	gravity = 0

	start_time = 0 #					NOTE : DEBUG
	last_time = 0 #						NOTE : DEBUG

	last_ponger = 0
	step_count = 0

	score_mode = df.GOALS
	scores = [ 0 ]

	iPosR1 = ( width * (1 / 2), height - size_b, "x" )
	iPosR2 = None
	iPosR3 = None
	iPosR4 = None

	iPosB1 = ( width * (3 / 8), size_b )
	#iPosB2 = None
	#iPosB3 = None
	#iPosB4 = None

	# ------------------------------------------- INITIALIZATION ------------------------------------------- #

	def __init__(self, gameID, connector = None):

		self.gameID = gameID
		self.connector = connector

		#self.gameLock = asy.Lock() # TODO :implement me

		self.last_ponger = 0
		self.step_count = 0

		if cfg.DEBUG_MODE:
			self.font = pg.font.Font(None, self.size_font)
			self.debug_font = pg.font.Font(None, 32)

			self.last_time = time.time()
			self.delta_time = cfg.FRAME_DELAY

		self.useAI = True
		self.winnerID = 0 #				NOTE : this is the scores[] index (to allow teams)

		self.playerCount = 0
		self.controlerCount = 0

		self.rackets = []
		self.controlers = []
		self.balls = []

		self.initRackets()
		self.initBalls()


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[0], self.iPosR1[1], self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[0], self.iPosB1[1], self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, self.speed_b )
		self.balls[0].setDirs( 1, 1 )

	# --------------------------------------------- PLAYER & AI -------------------------------------------- #

	def initBots(self):
		while self.controlerCount < self.racketCount:
			self.addBot("bot #" + str(self.racketCount - self.controlerCount))


	def addBot(self, botname):
		if (self.controlerCount >= self.racketCount):
			raise Exception("Too many bots for this game")

		bot = bc.BotControler( self, botname )
		bot.setRacket( self.rackets[ len(self.controlers) ].id )
		bot.recordDefaultPos()
		bot.setFrequencyOffset( self.racketCount )
		self.controlers.append( bot )

		self.controlerCount += 1
		return ( bot )


	# def removeBots(self): # NOTE : not needed anymore


	def makeBotsPlay(self):
		if self.useAI and self.playerCount < self.racketCount:
			for i in range(self.playerCount, self.controlerCount):
				if (self.controlers[i].mode == gc.df.BOT):

					val = ( self.step_count + self.controlers[i].frequency_offset )


					if ( val % df.BOT_SEE_FREQUENCY ) == 0:
						#print( "bot #" + str(i) + " is seeing  on step #" + str( self.step_count ) )#		NOTE : DEBUG
						self.controlers[i].seeBall()
					if ( val % df.BOT_PLAY_FREQUENCY ) == 0:
						#print( "bot #" + str(i) + " is playing on step #" + str( self.step_count ) )#		NOTE : DEBUG
						self.controlers[i].playMove()

			self.step_count += 1
			self.step_count %= df.BOT_PLAY_FREQUENCY * df.BOT_SEE_FREQUENCY

	# --------------------------------------------------------------

	def addPlayer(self, username, playerID):
		if self.state != df.STARTING:
			print ("cannot add players once the game started")
		elif (self.isGameFull()):
			print ("this game is full")

		player = pl.PlayerControler( self, username, playerID )
		player.setRacket( self.rackets[ self.playerCount ].id )
		self.controlers.append( player )

		self.playerCount += 1
		self.controlerCount += 1
		return ( player )


	def removePlayer(self, playerID): #						NOTE : do we close empty games here (?)
		for i in range(len(self.controlers)):
			if (self.controlers[i].playerID == playerID):
				racketID = self.controlers[i].racketID
				self.controlers.pop(i)
				self.playerCount -= 1
				self.controlerCount -= 1
				#return ( racketID )
		print ("player #" + str(playerID) + " not found in this game")


	def getPlayerControler(self, username):
		for i in range(len(self.controlers)):
			if (self.controlers[i].username == username):
				return ( self.controlers[i] )
		return None


	def printControlers(self):
		print( "controler list: " )
		for i in range(len(self.controlers)):
			print( "racket #" + str(i + 1) + " : " + self.controlers[i].name)

	# --------------------------------------------------------------


	def hasPlayer(self, username):
		for i in range(len(self.controlers)):
			if (self.controlers[i].username == username):
				return ( True )
		return ( False )

	def isGameFull(self):
		return ( self.playerCount >= self.racketCount )


	def isGameEmpty(self):
		return ( self.playerCount == 0 )

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
				if move == df.NULL:
					return
				elif (move == df.STOP):
					rack.fx = 0
					rack.fy = 0
				elif (move == df.LEFT):
					if (self.hard_break and rack.fx > 0):
						rack.fx = 0
					else:
						rack.fx -= 1
				elif (move == df.UP):
					if (self.hard_break and rack.fy > 0):
						rack.fy = 0
					else:
						rack.fy -= 1
				elif (move == df.RIGHT):
					if (self.hard_break and rack.fx < 0):
						rack.fx = 0
					else:
						rack.fx += 1
				elif (move == df.DOWN):
					if (self.hard_break and rack.fy < 0):
						rack.fy = 0
					else:
						rack.fy += 1
				else:
					print("Error: invalid move : " + str( move ))
				return

	# --------------------------------------------------------------

#	Possible event types :
#		- "start_game"
#		- "end_game"
#		- "key_press"
#		- "key_release"
#		- ...

#		class Event {
#			sender_id; // 	playerID (0 for server)
#			type; // 		event type (see above)
#			code; // 		key code (when key related)
#		}

	def getNextEvent(self):
		if cfg.DEBUG_MODE:
			return pg.event.get()
		else:
			self.connector.getEvent()


	def eventControler(self):
		for event in self.getNextEvent():

			# quiting the game
			if event.type == df.CLOSE:
				if cfg.DEBUG_MODE:
					self.close()
				else:
					pass # TODO : implement me ( is it needed ? )

			# starting the game
			#elif event.type == df.START:
			#	pass # TODO : implement me ( is it needed ? )

			# handling key presses
			elif event.type == df.KEYPRESS:
				if not cfg.DEBUG_MODE:
					self.handleUserInputs( event.sender_id, event.code )

				else: #							NOTE : FOR DEBUG MODE ONLY
					# quiting the game(s)
					if event.key == df.ESCAPE:
						self.close()

					# respawning the ball(s)
					elif event.key == df.RETURN:
						for i in range(len(self.balls)):
							self.respawnBall( self.balls[i] )

					else:
						self.handlePygameInputs( event.key )


	def handleUserInputs(self, playerID, key):
		for i in range( len( self.controlers )):
			if (self.controlers[i].playerID == playerID):
				self.controlers[i].handleInputs( key )
				return

		print( "player #" + str( playerID ) + " is not in this game" )


	def handlePygameInputs(self, key): #		NOTE : DEBUG
		for i in range(0, self.controlerCount):
			if (self.controlers[i].mode == gc.df.PLAYER):
				rack = self.controlers[i].racket
				if key == df.KS or key == df.DOWN:
					self.makeMove( rack.id, df.STOP )
				elif key == df.KA or key == df.LEFT:
					self.makeMove( rack.id, df.LEFT )
				elif key == df.KD or key == df.RIGHT:
					self.makeMove( rack.id, df.RIGHT )


	# ---------------------------------------------- CORE CMDS --------------------------------------------- #

	def start(self):
		if (self.state == df.STARTING):
			self.initBots()
			self.state = df.PLAYING
			self.start_time = time.time()
			print( "starting a game of " + self.name )
		else:
			print( "game is either running or over" )


	def close(self):
		self.state = df.ENDING
		print("closed a game of " + self.name)

	# --------------------------------------------------------------

	def run(self): #							NOTE : DEBUG MODE ONLY

		if not cfg.DEBUG_MODE:
			print( "cannot use run() without debug mode" )
			return

		if self.state == df.ENDING:
			print( "The game of " + self.name + " is over" )
			pg.quit()
			sys.exit()

		if self.state != df.PLAYING:
			print(f"{self.name} is not running")
			return

		# main game loop
		while self.state == df.PLAYING:
			self.eventControler()
			self.step( True )
			self.clock.tick (self.framerate)



	def step(self, display = False):

		# TODO : use connector.getEvent() to move rackets

		if self.state != df.PLAYING:
			print( str( self.name ) + " is not running" )
			return

		if not cfg.DEBUG_MODE or cfg.MOVE_OBJECTS:
			self.moveObjects()
			self.makeBotsPlay()

		if cfg.DEBUG_MODE:
			self.clock.tick(0)
			if (display):
				self.refreshScreen()
		else:
			pass #		NOTE : useless (packet sending is done by game manager now)

		if cfg.PRINT_PACKETS:
			print( self.getUpdateInfo() ) #		NOTE : DEBUG


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
		if (not rack.isInScreen()):
			rack.bounceOnWall( "stop" )

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

	# --------------------------------------------------------------

	# bouncing off the rackets
	def checkRackets(self, ball):
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
			if ball.isOverlaping( rack ):
				ball.setPosY( rack.getPosY() - self.size_b ) # '-' because the ball is going above the racket
				ball.bounceOnRack( rack, "y" )
				self.scorePoint( rack.id, df.HITS )


	# bouncing on the walls
	def checkWalls(self, ball):
		if ball.getLeft() <= 0 or ball.getRight() >= self.width or ball.getTop() <= 0:

			# bouncing off the sides
			if ball.getLeft() <= 0 or ball.getRight() >= self.width:
				ball.bounceOnWall( "x" )

			# bouncing off the top (no bounce factor)
			if ball.getTop() <= 0:
				ball.bounceOnWall( "y" )


	# scoring a goal
	def checkGoals(self, ball):
		if ball.getBottom() >= self.height:
			self.scorePoint( self.last_ponger, df.GOALS )
			self.respawnBall( ball )

	# --------------------------------------------------------------

	def scorePoint(self, controler_id, mode):
		if controler_id > 0:
			if mode == df.GOALS: #					if the ball went out of bounds
				if self.score_mode == df.GOALS: #		if goals give points
					self.scores[controler_id - 1] += 1
				else: # 								if racket hits give points
					self.scores[controler_id - 1] = 0
				self.last_ponger = 0

			elif mode == df.HITS: #					if the ball hit a racket
				if self.score_mode == df.HITS: #		if racket hits give points
					self.scores[controler_id - 1] += 1
				else: #									if goals give points
					pass
				self.last_ponger = controler_id
		else:
			self.last_ponger = 0

		# check if someone won
		for i in range(len(self.scores)):
			score = self.scores[i]
			if score >= df.WIN_SCORE:
				self.winGame( i + 1 )


	def winGame(self, teamID):
		self.winnerID = teamID
		self.state = df.ENDING
		print( f"Team #{ teamID } won the game of { self.name }" )
		if cfg.PRINT_PACKETS:
			print( self.getEndInfo() )


	def respawnBall(self, ball):
		ball.setDirs( -ball.fx, 1 )
		ball.setPosY( self.size_b )
		ball.setSpeeds( self.speed_b, self.speed_b )


	def respawnAllBalls(self):
		for i in range(len(self.balls)):
			self.respawnBall( self.balls[i] )


	# ------------------------------------------- GAME RENDERING ------------------------------------------- #
 	#										NOTE : DEBUG MODE ONLY

	def setWindow(self, _win):
		self.win = _win
		self.clock = pg.time.Clock()


	def refreshScreen(self):

		self.win.fill( df.COL_BGR )
		self.drawScores()

		for rack in self.rackets: # 	copies the racket's data
			rack.drawSelf()

		self.drawLines()

		for ball in self.balls: # 		copies the ball's data
			ball.drawSelf()

		self.drawFps()
		pg.display.flip() #				drawing the newly prepared frame


	def drawLines(self):
		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, df.COL_FNT, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ), ( self.width, 0 ), self.size_l * 2 )


	def drawScores(self):
		for score in self.scores: #		copies the racket's data
			text = self.font.render(f'{score}', True, df.COL_FNT)
			self.win.blit( text, text.get_rect( center = ( self.width * (2 / 4), self.height * (2 / 4) )))


	def drawFps(self):

		new_time = time.time()
		self.delta_time = (( new_time - self.last_time ) + ( self.delta_time * cfg.FPS_SMOOTHING )) / ( cfg.FPS_SMOOTHING + 1)
		self.last_time = new_time

		text = self.debug_font.render( "{:.1f}".format( 1 / self.delta_time ), True, df.COL_FNT )
		self.win.blit( text, text.get_rect( center = ( 64, 32 )))


	# -------------------------------------------- GAME PACKETS -------------------------------------------- #


	def getUpdateInfo(self):
		infoDict = {}

		infoDict["gameID"] = self.gameID
		infoDict["racketPos"] = self.getRacketPos()
		infoDict["ballPos"] = self.getBallPos()
		infoDict["lastPonger"] = self.last_ponger
		infoDict["scores"] = self.scores

		return( infoDict )


	def getRacketPos(self):
		pos = []

		for i in range( len( self.rackets )):
			pos.append( self.rackets[i].getPosX() )
			pos.append( self.rackets[i].getPosY() )

		return( pos )


	def getBallPos(self):
		pos = []

		for i in range( len( self.balls )):
			pos.append( self.balls[i].getPosX() )
			pos.append( self.balls[i].getPosY() )

		return( pos )


	def getMode( self ): #				NOTE : useless???

		if (self.mode == df.SOLO):
			return "solo"
		elif (self.mode == df.DUAL):
			return "dual"
		elif (self.mode == df.FREEPLAY):
			return "freeplay"
		elif (self.mode == df.TOURN_RND_1):
			return "tournament (1)"
		elif (self.mode == df.TOURN_RND_2):
			return "tournament (2)"
		else:
			return "unknown"


	def getState(self): #				NOTE : useless???
		if (self.state == df.STARTING):
			return "starting"
		elif (self.state == df.PLAYING):
			return "playing"
		elif (self.state == df.ENDING):
			return "ending"
		else:
			return "unknown"

	# --------------------------------------------------------------

	def getEndInfo(self):
		infoDict = {}

		infoDict["gameID"] = self.gameID

		if self.winnerID == 0:
			infoDict["winingTeam"] = -1
		else:
			infoDict["winingTeam"] = self.winnerID

		infoDict["scores"] = self.scores

		return ( infoDict )


if __name__ == '__main__': #			NOTE : DEBUG MODE ONLY

	pg.init()
	g = Game(1)

	g.setWindow(pg.display.set_mode((1280, 1280)))
	pg.display.set_caption(g.name)

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()