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

	state = df.STARTING
	hard_break = False #		NOTE : automatically stop racket when decelerating
	divide_sides = False #		NOTE : prevents rackets from crossing the middle of the screen

	width = 1536
	height = 1024

	racket_count = 1
	score_count = 1

	size_b = 20
	size_r = 160

	size_l = 10
	size_font = 768

	speed_b = 8
	speed_r = 8
	speed_m_b = 60
	speed_m_r = 60

	factor_wall = 0.75
	factor_rack = 1.10
	gravity = 0

	start_time = 0 #			NOTE : DEBUG
	last_time = 0 #				NOTE : DEBUG

	last_ponger = 0
	step_count = 0

	score_mode = df.GOALS
	scores = [ 0 ]

	iPosR1 = ( width * ( 1 / 2 ), height - size_b, "x" )
	iPosR2 = None
	iPosR3 = None
	iPosR4 = None

	iPosB1 = ( width * ( 3 / 8 ), size_b )
	iPosB2 = None
	iPosB3 = None
	iPosB4 = None

	iPosS1 = ( width * ( 1 / 2 ), height * ( 1 / 2 ))
	iPosS2 = None
	iPosS3 = None
	iPosS4 = None

	lines = [
	[( 0, 0 ), ( 0, 1 ), 2 ],
	[( 1, 0 ), ( 1, 1 ), 2 ],
	[( 0, 0 ), ( 1, 0 ), 2 ]]


	# ------------------------------------------- INITIALIZATION ------------------------------------------- #


	def __init__( self, _gameID, _gameMode = df.SOLO, connector = None ): # NOTE : take in gametype

		self.gameID = _gameID
		self.connector = connector

		if cfg.FORCE_MODE:
			print ( "WARNING: game mode has been forced to " + str( df.FORCE_MODE_TO ))
			self.mode = df.FORCE_MODE_TO
		else:
			self.mode = _gameMode

		self.gameLock = asy.Lock()

		self.last_ponger = 0
		self.step_count = 0

		if cfg.DEBUG_MODE:
			self.font = pg.font.Font( None, self.size_font )
			self.debug_font = pg.font.Font( None, 42 )
			self.racket_font = pg.font.Font( None, 21 )

			self.last_time = time.time()
			self.delta_time = cfg.FRAME_DELAY

		self.useAI = True
		self.winnerID = 0 #				NOTE : this is a scores[] index( teamID )
		self.quitterID = 0 #			NOTE : this is a playerID

		self.playerCount = 0
		self.controlerCount = 0

		self.rackets = []
		self.controlers = []
		self.balls = []

		self.initRackets()
		self.initBalls()
		self.initScores()

		if (cfg.PRINT_STATES):
			print( f"{self.gameID} )  {self.name}  \t: game has been created" )# 		NOTE : DEBUG


	def initRackets( self ):
		# setting up rackets :             id, game, _x              , _y              , _w         , _h         , _maxSpeed
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_r, self.size_b, self.speed_m_r ))

		self.rackets[ 0 ].setSpeeds( self.speed_r, 0 )


	def initBalls( self ):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
		self.balls[ 0 ].setSpeeds( self.speed_b, self.speed_b )
		self.balls[ 0 ].setDirs( 1, 1 )


	def initScores( self ):
		self.scores = []

		for _ in range( self.score_count ):
			self.scores.append( 0 )


	# --------------------------------------------- PLAYER & AI -------------------------------------------- #


	def initBots( self ):
		while self.controlerCount < self.racket_count:
			self.addBot( "B" + str( self.controlerCount + 1 ))


	def addBot( self, botname ):
		if( self.controlerCount >= self.racket_count ):
			raise Exception( "Too many bots for this game" )

		bot = bc.BotControler( self, botname )
		bot.setRacket( self.rackets[ len( self.controlers )].id )
		bot.recordDefaultPos()
		bot.setFrequencyOffset( self.racket_count )
		self.controlers.append( bot )

		self.controlerCount += 1
		return( bot )


	# def removeBots( self ): # NOTE : not needed anymore


	def makeBotsPlay( self ):
		if self.useAI and self.playerCount < self.racket_count:
			for i in range( self.playerCount, self.controlerCount ):
				if( self.controlers[ i ].mode == df.BOT ):

					val = ( self.step_count + self.controlers[ i ].frequency_offset )


					if( val % df.BOT_SEE_FREQUENCY ) == 0:
						#print( "bot #" + str( i ) + " is seeing  on step #" + str( self.step_count ))#		NOTE : DEBUG
						self.controlers[ i ].seeBall()
					if( val % df.BOT_PLAY_FREQUENCY ) == 0:
						#print( "bot #" + str( i ) + " is playing on step #" + str( self.step_count ))#		NOTE : DEBUG
						self.controlers[ i ].playMove()

			self.step_count += 1
			self.step_count %= df.BOT_PLAY_FREQUENCY * df.BOT_SEE_FREQUENCY

	# --------------------------------------------------------------

	def addPlayer( self, username, playerID ):
		if( self.state != df.STARTING ):
			print( "cannot add players once the game started" )
		elif( self.isGameFull() ):
			print( "this game is full" )

		player = pl.PlayerControler( self, username, playerID )
		player.setRacket( self.rackets[ self.playerCount ].id )
		self.controlers.append( player )

		self.playerCount += 1
		self.controlerCount += 1
		return( player )


	def removePlayer( self, playerID ):
		for i in range( len( self.controlers )):
			if( self.controlers[ i ].playerID == playerID ):
				racketID = self.controlers[ i ].racketID
				self.controlers.pop( i )
				self.playerCount -= 1
				self.controlerCount -= 1

		print( "player #" + str( playerID ) + " not found in this game" )


	def getPlayerControler( self, username ):
		for i in range( len( self.controlers )):
			if( self.controlers[ i ].username == username ):
				return( self.controlers[ i ] )
		return None


	def printControlers( self ):
		print( "controler list: " )
		for i in range( len( self.controlers )):
			print( "racket #" + str( i + 1 ) + " : " + self.controlers[ i ].name )

	# --------------------------------------------------------------


	def hasPlayer( self, username ):
		for i in range( len( self.controlers )):
			if( self.controlers[ i ].username == username ):
				return( True )
		return( False )

	def isGameFull( self ):
		return( self.playerCount >= self.racket_count )


	def isGameEmpty( self ):
		return( self.playerCount == 0 )

	# ---------------------------------------------- INTERFACE --------------------------------------------- #


	def makeMove( self, target_id, move ):
		if target_id <= 0 :
			print( "Error: no target selected" )
			return

		if move <= df.NULL:
			if move < df.NULL:
				print( "Error: invalid move : " + str( move ))
			return

		for i in range( len( self.rackets )):
			rack = self.rackets[ i ]

			if( rack.id == target_id ):

				if( move == df.STOP ):
					rack.fx = 0
					rack.fy = 0
				elif( move == df.LEFT ):
					if( self.hard_break and rack.fx > 0 ):
						rack.fx = 0
					else:
						rack.fx -= 1
				elif( move == df.UP ):
					if( self.hard_break and rack.fy > 0 ):
						rack.fy = 0
					else:
						rack.fy -= 1
				elif( move == df.RIGHT ):
					if( self.hard_break and rack.fx < 0 ):
						rack.fx = 0
					else:
						rack.fx += 1
				elif( move == df.DOWN ):
					if( self.hard_break and rack.fy < 0 ):
						rack.fy = 0
					else:
						rack.fy += 1
				else:
					print( "Error: invalid move : " + str( move ))
				return

	# --------------------------------------------------------------

#	Possible event types :
#		- "start_game"
#		- "end_game"
#		- "key_press"

#		class Event {
#			id; // 		playerID	( 0 for server commands )
#			type; // 	event type	( see above )
#			key; // 	event code	( key when keyboard related )
#		}

	async def getNextEvents( self ):
		if cfg.DEBUG_MODE:
			return pg.event.get()

		elif( self.connector != None ):
			return await self.connector.getEvents()


	async def eventControler( self ):
		for event in await self.getNextEvents():

			# starting the game
			if event.type == df.START:
				if event.id == 0:
					self.start()

			# closing the game
			elif event.type == df.CLOSE:
				if not cfg.DEBUG_MODE:
					if event.id != 0: #					NOTE : if the event is not from the server
						self.quitterID = event.id #		NOTE : add the quitter's id to the end packet

				self.close()

			# handling key presses
			elif event.type == df.KEYPRESS:

				if not cfg.DEBUG_MODE:
					self.handleUserInput( event.id, event.key )

				else:
					# quiting the game( s )
					if event.key == df.ESCAPE:
						self.close()
						continue

					# respawning the ball( s )
					elif event.key == df.RETURN:
						for i in range( len( self.balls )):
							self.respawnBall( self.balls[ i ] )
						continue

					# passing the key to the player controler
					self.handlePygameInput( event.key )


	def handleUserInput( self, playerID, key ):
		if self.mode == df.DUAL and self.racket_count > 1:
			if key == df.KUP or key == df.KRIGHT or key == df.KDOWN or key == df.KLEFT or key == df.NZERO: # check which player played
				self.controlers[ 1 ].handleKeyInput( key )
			else:
				self.controlers[ 0 ].handleKeyInput( key )

		else:
			for i in range( len( self.controlers )):
				if( self.controlers[ i ].playerID == playerID ):
					self.controlers[ i ].handleKeyInput( key )
					return

			print( "player #" + str( playerID ) + " is not in this game" )


	def handlePygameInput( self, key ): #				NOTE : DEBUGGS
		if self.mode == df.DUAL and self.racket_count > 1:
			if key == df.KUP or key == df.KRIGHT or key == df.KDOWN or key == df.KLEFT or key == df.NZERO:
				self.controlers[ 1 ].handleKeyInput( key )
			else:
				self.controlers[ 0 ].handleKeyInput( key )
		else:
			for i in range( self.controlerCount ):
				if self.controlers[ i ].mode == df.PLAYER:
					self.controlers[ i ].handleKeyInput( key )


	# ---------------------------------------------- CORE CMDS --------------------------------------------- #

	def start( self ):
		if( self.state == df.STARTING ):
			self.initBots()
			self.state = df.PLAYING
			self.start_time = time.time()
			if (cfg.PRINT_STATES):
				print( f"{self.gameID} )  {self.name}  \t: game has been started" )# 		NOTE : DEBUG
			if cfg.PRINT_PACKETS:
				print( self.getPlayerInfo() )# 												NOTE : DEBUG

		else:
			print( "game is either running or over" )


	def close( self ):
		self.state = df.ENDING

		if (cfg.PRINT_STATES):
			print( f"{self.gameID} )  {self.name}  \t: game has been closed" )# 			NOTE : DEBUG

	# --------------------------------------------------------------

	async def run( self ):

		if not cfg.DEBUG_MODE:
			print( "cannot use run()without debug mode" )
			return

		if self.state != df.PLAYING:
			print( f"{ self.name } is not running" )
			return

		# main game loop
		while self.state == df.PLAYING:
			await self.eventControler()
			self.step( True )
			self.clock.tick( cfg.FRAME_RATE )



	def step( self, display = False ):

		if self.state != df.PLAYING:
			print( str( self.name ) + " is not running" )
			return

		if not cfg.DEBUG_MODE or cfg.MOVE_OBJECTS:
			self.moveObjects()
			self.makeBotsPlay()

		if cfg.DEBUG_MODE:
			self.clock.tick( 0 )
			if( display ):
				self.refreshScreen()
		else:
			pass #		NOTE : useless( packet sending is done by game manager now )

		if cfg.DEBUG_MODE and cfg.PRINT_PACKETS:
			print( self.getUpdateInfo() )#		NOTE : DEBUG


	# ------------------------------------------- GAME MECHANICS ------------------------------------------- #


	def moveObjects( self ):
		for i in range( len( self.rackets )):
			self.moveRacket( self.rackets[ i ] )

		for i in range( len( self.balls )):
			self.moveBall( self.balls[ i ] )


	def moveRacket( self, rack ):
		rack.clampSpeed()
		rack.updatePos()

		# prevent racket from going off screen
		if( not rack.isInScreen() ):
			rack.bounceOnWall( "stop" )

		# prevent rackets from crossing the middle lines
		if self.divide_sides:
			if( rack.id == 1 or rack.id == 3 ) and rack.getRight() > self.width / 2:
				rack.bounceOnWall( "stop" )
				rack.setPosX(( self.width - self.size_r ) / 2 )

			elif( rack.id == 2 or rack.id == 4 ) and rack.getLeft() < self.width / 2:
				rack.bounceOnWall( "stop" )
				rack.setPosX(( self.width + self.size_r ) / 2 )

		rack.clampPos()


	def moveBall( self, ball ):

		self.aplyGravity( ball )

		ball.clampSpeed()
		ball.updatePos()


		self.checkRackets( ball )
		self.checkWalls( ball )
		self.checkGoals( ball )

		ball.clampPos()


	def aplyGravity( self, ball ):
		if self.gravity != 0:
			ball.dy += self.gravity * ball.fy

	# --------------------------------------------------------------

	# bouncing off the rackets
	def checkRackets( self, ball ):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				ball.setPosY( rack.getPosY() - self.size_b )# '-' because the ball is going above the racket
				ball.bounceOnRack( rack, "y" )
				self.scorePoint( rack.id, df.HITS )


	# bouncing on the walls
	def checkWalls( self, ball ):
		if ball.getLeft() < 0 or ball.getRight() > self.width or ball.getTop() < 0:

			# bouncing off the sides
			if ball.getLeft() < 0 or ball.getRight() > self.width:
				ball.bounceOnWall( "x" )

			# bouncing off the top( no bounce factor )
			if ball.getTop() < 0:
				ball.bounceOnWall( "y" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getBottom() > self.height:
			self.scorePoint( self.last_ponger, df.GOALS )
			self.respawnBall( ball )
			if self.connector != None:
				self.connector.update_scores( self.scores )

	# --------------------------------------------------------------

	def scorePoint( self, teamID, mode ):
		if teamID > 0:
			if mode == df.GOALS: #					if the ball went out of bounds
				if self.score_mode == df.GOALS: #		if goals give points
					self.scores[ teamID - 1 ] += 1
					if cfg.PRINT_STATES:
						print( f"{self.gameID} )  {self.name}  \t: team #{ teamID } scored a point" )
				else: # 								if racket hits give points
					self.scores[ teamID - 1 ] = 0
				self.last_ponger = 0

			elif mode == df.HITS: #					if the ball hit a racket
				if self.score_mode == df.HITS: #		if racket hits give points
					self.scores[ teamID - 1 ] += 1
				# else: #								if goals give points, do nothing

				self.last_ponger = teamID
		else:
			self.last_ponger = 0

		# check if someone won
		for i in range( self.score_count ):
			score = self.scores[ i ]
			if score >= df.WIN_SCORE:
				self.winGame( i + 1 )


	def winGame( self, teamID ):
		self.winnerID = teamID
		self.close()

		if cfg.PRINT_STATES:
			print( f"{self.gameID} )  {self.name}  \t: game has been won by team #{ teamID }" )# 		NOTE : DEBUG

		if cfg.DEBUG_MODE and cfg.PRINT_PACKETS:
			print( self.getEndInfo() )


	def respawnBall( self, ball ):
		ball.setDirs( ball.fx, 1 )
		ball.setPosY( self.size_b )
		ball.setSpeeds( self.speed_b, self.speed_b )


	def respawnAllBalls( self ):
		for i in range( len( self.balls )):
			self.respawnBall( self.balls[ i ] )


	# ------------------------------------------- GAME RENDERING ------------------------------------------- #
 	#									NOTE : DEBUG MODE ONLY

	def setWindow( self, _win ):
		self.win = _win
		self.clock = pg.time.Clock()


	def refreshScreen( self ):

		self.win.fill( df.COL_BGR )
		self.drawScores()

		for rack in self.rackets: # 	copies the racket's data
			rack.drawSelf()

		self.drawLines()

		for ball in self.balls: # 		copies the ball's data
			ball.drawSelf()

		if cfg.PRINT_DEBUG_INFO:
			self.drawFps()
			self.drawNames()

		pg.display.flip()#				drawing the newly prepared frame


	def drawLines( self ):
		for line in self.lines:
			start = ( int( self.width * line[ 0 ][ 0 ]), int( self.height * line[ 0 ][ 1 ]))
			end = ( int( self.width * line[ 1 ][ 0 ]), int( self.height * line[ 1 ][ 1 ]))

			pg.draw.line( self.win, df.COL_FNT, start, end, int( self.size_l * line[ 2 ]))


	def drawScores( self ):
		text = self.font.render( f'{ self.scores[ 0 ]}', True, df.COL_FNT )

		self.win.blit( text, text.get_rect( center = self.iPosS1 ))


	def drawFps( self ):

		new_time = time.time()
		self.delta_time = (( new_time - self.last_time ) + ( self.delta_time * cfg.FPS_SMOOTHING )) / ( cfg.FPS_SMOOTHING + 1 )
		self.last_time = new_time

		text = self.debug_font.render( "{:.1f}".format( 1 / self.delta_time ), True, df.COL_FNT )
		self.win.blit( text, text.get_rect( center = ( 82, 41 )))


	def drawNames( self ):
		for i in range( len( self.controlers )):
			racket = self.controlers[ i ].racket

			text = self.racket_font.render( self.controlers[ i ].name, True, df.COL_FNT )
			self.win.blit( text, text.get_rect( center = racket.box.center ))


	# -------------------------------------------- GAME PACKETS -------------------------------------------- #


	def getUpdateInfo( self ):
		return {
			"racketPos": self.getRacketPos(),
			"ballPos": self.getBallPos(),
			"lastPonger": self.last_ponger,
			"scores": self.scores
		}


	def getRacketPos( self ):
		return [ coord for rack in self.rackets for coord in ( rack.getPosX(), rack.getPosY() )]

		# pos = []
		# for i in range( len( self.rackets )):
		# 	pos.append( self.rackets[ i ].getPosX() )
		# 	pos.append( self.rackets[ i ].getPosY() )
		# return( pos )


	def getBallPos( self ):
		return [ coord for ball in self.balls for coord in ( ball.getPosX(), ball.getPosY() )]

		# pos = []
		# for i in range( len( self.balls )):
		# 	pos.append( self.balls[ i ].getPosX() )
		# 	pos.append( self.balls[ i ].getPosY() )
		# return( pos )


	def getMode( self ):

		if( self.mode == df.SOLO ):
			return "solo"
		elif( self.mode == df.DUAL ):
			return "dual"
		elif( self.mode == df.FREEPLAY ):
			return "freeplay"
		elif( self.mode == df.TOURNAMENT ):
			return "tournament"
		else:
			return "unknown"


	def getState( self ):
		if( self.state == df.STARTING ):
			return "starting"
		elif( self.state == df.PLAYING ):
			return "playing"
		elif( self.state == df.ENDING ):
			return "ending"
		else:
			return "unknown"

	# --------------------------------------------------------------

	def getPlayerInfo( self ):
		playerDict = {}

		for i in range( len( self.controlers )):
			playerDict[ str( i + 1 )] = self.controlers[ i ].getInfo()

		return( playerDict )

	# --------------------------------------------------------------

	def getEndInfo( self ):
		infoDict = {}

		infoDict[ "gameConnector" ] = self.connector

		infoDict[ "gameType" ] = self.name
		infoDict[ "gameMode" ] = self.getMode()

		if self.quitterID != 0:
			infoDict[ "endState" ] = df.END_QUIT
		elif self.winnerID != 0:
			infoDict[ "endState" ] = df.END_WIN
		else:
			infoDict[ "endState" ] = df.END_ABORT

		if self.winnerID != 0:
			infoDict[ "winingTeam" ] = self.winnerID
		else:
			infoDict[ "winingTeam" ] = -1

		infoDict[ "quitter" ] = self.quitterID
		infoDict[ "scores" ] = self.scores

		infoDict[ "playerInfo" ] = self.getPlayerInfo()

		return( infoDict )


	# --------------------------------------------- CLASS END ---------------------------------------------- #


if __name__ == '__main__': #			NOTE : DEBUG MODE ONLY

	pg.init()
	g = Game( 1 )

	g.setWindow( pg.display.set_mode(( 1280, 1280 )))
	pg.display.set_caption( g.name )

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()