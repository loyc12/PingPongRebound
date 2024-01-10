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


class Game:
	type = "None"

	divide_sides = False #		NOTE : prevents rackets from crossing the middle of the screen
	score_mode = df.GOALS

	width = 1536
	height = 1024

	size_b = 20
	speed_b = 8
	speed_m_b = 56

	size_r = 160
	speed_r = 8
	speed_m_r = 64

	size_l = 10
	size_f = 768

	factor_wall = 0.75
	factor_rack = 1.10

	gravity = 0.0

	racket_count = 1
	score_count = 1

	# racket init positions			px, py					 , dir
	iPosR1 = ( int( width * ( 1 / 2 )), int( height - size_b), "x" )
	iPosR2 = None
	iPosR3 = None
	iPosR4 = None

	# ball init positions			px, py
	iPosB1 = ( int( width * ( 3 / 8 )), int( size_b ))
	iPosB2 = None
	iPosB3 = None
	iPosB4 = None

	# spawn positions			   px, py			, s, s, d, d
	posS1 = ( int( width * ( 1 / 2 )), int( size_b ), 1, 1, 1, 1 )
	posS2 = None
	posS3 = None
	posS4 = None

	# score positions			   px, py
	posN1 = ( int( width * ( 1 / 2 )), int( height * ( 1 / 2 )))
	posN2 = None
	posN3 = None
	posN4 = None

	lines = [
	[( 0, 0 ), ( 0, 1 ), 2 ],
	[( 1, 0 ), ( 1, 1 ), 2 ],
	[( 0, 0 ), ( 1, 0 ), 2 ]]


	# ------------------------------------------- INITIALIZATION ------------------------------------------- #


	def __init__( self, _gameID, _gameMode = df.SOLO, connector = None ):

		self.gameID = _gameID
		self.mode = _gameMode
		self.connector = connector
		self.difficulty = cfg.BOT_DIFFICULTY

		self.gameLock = asy.Lock()
		self.state = df.STARTING

		self.useAI = True
		self.step_count = 0

		self.playerCount = 0
		self.controlerCount = 0

		self.last_ponger = 0
		self.spawn_target = 0
		self.spawn_queue = []
		self.missed_shots = 0

		self.winnerID = 0 #			NOTE : this is a scores[] index ( same as teamID ) ( 0 == null)
		self.quitterID = 0 #		NOTE : this is a player index ( same as playerID ) ( 0 == null)

		self.rackets = []
		self.controlers = []
		self.balls = []
		self.scores = []
		self.spawns = []

		self.onInit()


	def onInit( self ):
		self.initRackets()
		self.initBalls()
		self.initSpawns()
		self.initScores()

		if cfg.PRINT_STATES:
			print( f"{self.gameID} )  {self.type}  \t: game has been created" )

		if cfg.DEBUG_MODE:
			self.font = pg.font.Font( None, self.size_f )
			self.debug_font = pg.font.Font( None, 42 )
			self.racket_font = pg.font.Font( None, 21 )

			self.start_time = time.time()
			self.last_time = self.start_time
			self.delta_time = cfg.FRAME_DELAY

			if cfg.FORCE_MODE:
				print ( "Warning : game mode has been forced to " + str( df.FORCE_MODE_TO ))
				self.mode = df.FORCE_MODE_TO

	# --------------------------------------------------------------

	def initRackets( self ):
		if self.iPosR1 != None: #			   id, game, _x              , _y              , _w         , _h         , _maxSpeed
			self.rackets.append( go.GameObject( 1, self, self.iPosR1[ 0 ], self.iPosR1[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
			self.rackets[ 0 ].setSpeeds( self.speed_r, 0 )
		if self.iPosR2 != None:
			self.rackets.append( go.GameObject( 2, self, self.iPosR2[ 0 ], self.iPosR2[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
			self.rackets[ 1 ].setSpeeds( self.speed_r, 0 )
		if self.iPosR3 != None:
			self.rackets.append( go.GameObject( 3, self, self.iPosR3[ 0 ], self.iPosR3[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
			self.rackets[ 2 ].setSpeeds( self.speed_r, 0 )
		if self.iPosR4 != None:
			self.rackets.append( go.GameObject( 4, self, self.iPosR4[ 0 ], self.iPosR4[ 1 ], self.size_r, self.size_b, self.speed_m_r ))
			self.rackets[ 3 ].setSpeeds( self.speed_r, 0 )


	def initBalls( self ):
		if self.iPosB1 != None:
			self.balls.append( go.GameObject( 1, self, self.iPosB1[ 0 ], self.iPosB1[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
			self.balls[ 0 ].setSpeeds( self.posS1[ 2 ] * self.speed_b, self.posS1[ 3 ] * self.speed_b )
			self.balls[ 0 ].setDirs( self.posS1[ 4 ], self.posS1[ 5 ] )
		if self.iPosB2 != None:
			self.balls.append( go.GameObject( 2, self, self.iPosB2[ 0 ], self.iPosB2[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
			self.balls[ 1 ].setSpeeds( self.posS2[ 2 ] * self.speed_b, self.posS2[ 3 ] * self.speed_b )
			self.balls[ 1 ].setDirs( self.posS2[ 4 ], self.posS2[ 5 ] )
		if self.iPosB3 != None:
			self.balls.append( go.GameObject( 3, self, self.iPosB3[ 0 ], self.iPosB3[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
			self.balls[ 2 ].setSpeeds( self.posS3[ 2 ] * self.speed_b, self.posS3[ 3 ] * self.speed_b )
			self.balls[ 2 ].setDirs( self.posS3[ 4 ], self.posS3[ 5 ] )
		if self.iPosB4 != None:
			self.balls.append( go.GameObject( 4, self, self.iPosB4[ 0 ], self.iPosB4[ 1 ], self.size_b, self.size_b, self.speed_m_b ))
			self.balls[ 3 ].setSpeeds( self.posS4[ 2 ] * self.speed_b, self.posS4[ 3 ] * self.speed_b )
			self.balls[ 3 ].setDirs( self.posS4[ 4 ], self.posS4[ 5 ] )


	def initSpawns( self ):
		if self.posS1 != None:
			self.spawns.append( self.posS1 )
		if self.posS2 != None:
			self.spawns.append( self.posS2 )
		if self.posS3 != None:
			self.spawns.append( self.posS3 )
		if self.posS4 != None:
			self.spawns.append( self.posS4 )


	def initScores( self ):
		self.scores = []

		for _ in range( self.score_count ):
			self.scores.append( 0 )


	# --------------------------------------------- PLAYER & AI -------------------------------------------- #


	def initBots( self ):
		while self.controlerCount < self.racket_count:
			self.addBot( "B" + str( self.controlerCount + 1 ), self.difficulty )
			if cfg.PRINT_BOTS:
				print( f"{self.gameID} )  {self.type}  \t: bot #{ self.controlerCount }  has been added with difficulty #{ self.difficulty }" )


	def addBot( self, botname, difficulty = df.HARD ):
		if( self.controlerCount >= self.racket_count ):
			print( "Warning : game #" + str( self.gameID ) + " is full" )

		bot = bc.BotControler( self, botname, difficulty )
		bot.setRacket( self.rackets[ len( self.controlers )].id )
		bot.setFrequencyOffset( self.racket_count )
		self.controlers.append( bot )

		self.controlerCount += 1
		return( bot )


	# def removeBots( self ): #		NOTE : obsolete; bots are only added on game start now, so we never have to remove any


	def makeBotsPlay( self ):
		if self.useAI and self.playerCount < self.racket_count:
			for i in range( self.playerCount, self.controlerCount ):

				if( self.controlers[ i ].mode == df.BOT ):
					val = ( self.step_count + self.controlers[ i ].frequency_offset )

					if( val % df.BOT_SEE_FREQUENCY ) == 0:
						self.controlers[ i ].seeBall()
						if cfg.PRINT_EXTRA and cfg.PRINT_BOTS:
							print( f"{self.gameID} )  {self.type}  \t: bot #{i}  is seeing  on step #{self.step_count}" )

					if( val % df.BOT_PLAY_FREQUENCY ) == 0:
						self.controlers[ i ].playMove()
						if cfg.PRINT_EXTRA and cfg.PRINT_BOTS:
							print( f"{self.gameID} )  {self.type}  \t: bot #{i}  is playing on step #{self.step_count}" )


			self.step_count += 1
			self.step_count %= df.BOT_PLAY_FREQUENCY * df.BOT_SEE_FREQUENCY


	def getRacket( self, racketID ):
		for i in range( len( self.rackets )):
			if( self.rackets[ i ].id == racketID ):
				return( self.rackets[ i ] )
		print( "Warning : racket #" + str( racketID ) + " not found in this game" )
		return None

	# --------------------------------------------------------------

	def addPlayer( self, username, playerID ):
		if( self.state != df.STARTING ):
			print( "Warning : cannot add players once the game started" )
		elif( self.isGameFull() ):
			print( "Warning : game #" + str( self.gameID ) + " is full" )

		player = pl.PlayerControler( self, username, playerID )
		player.setRacket( self.rackets[ self.playerCount ].id )
		self.controlers.append( player )

		self.playerCount += 1
		self.controlerCount += 1
		return( player )


	def removePlayer( self, playerID ):
		for i in range( len( self.controlers )):
			if( self.controlers[ i ].playerID == playerID ):
				racketID = self.controlers[ i ].racket.id
				self.controlers.pop( i )
				self.playerCount -= 1
				self.controlerCount -= 1

		print( "Warning : player #" + str( playerID ) + " not found in this game" )


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
			print( "Warning : no target selected" )
			return

		if move <= df.NULL:
			if move < df.NULL:
				print( "Warning : invalid move : " + str( move ))
			return

		for i in range( len( self.rackets )):
			rack = self.rackets[ i ]

			if( rack.id == target_id ):
				moveName = "INVALID"

				if( move == df.STOP ):
					rack.fx = 0
					rack.fy = 0
					moveName = "STOP"

				elif( move == df.LEFT ):
					if(df.PLAYER_HARD_BREAK and rack.fx > 0 ):
						rack.fx = 0
					else:
						rack.fx -= 1
					moveName = "LEFT"

				elif( move == df.UP ):
					if(df.PLAYER_HARD_BREAK and rack.fy > 0 ):
						rack.fy = 0
					else:
						rack.fy -= 1
					moveName = "UP"

				elif( move == df.RIGHT ):
					if(df.PLAYER_HARD_BREAK and rack.fx < 0 ):
						rack.fx = 0
					else:
						rack.fx += 1
					moveName = "RIGHT"

				elif( move == df.DOWN ):
					if(df.PLAYER_HARD_BREAK and rack.fy < 0 ):
						rack.fy = 0
					else:
						rack.fy += 1
					moveName = "DOWN"

				else:
					print( "Warning : invalid move : " + str( move ))

				if cfg.PRINT_MOVES:
					ctrlr = self.controlers[ i ]
					if ctrlr.mode == df.PLAYER:
						print( f"{self.gameID} )  {self.type}  \t: player #{ ctrlr.playerID }  is making move { moveName } on racket #{ rack.id }" )
					elif cfg.PRINT_BOTS:
						print( f"{self.gameID} )  {self.type}  \t: bot #{ rack.id }  is making move { moveName }" )

	# --------------------------------------------------------------

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

			print( "Warning : player #" + str( playerID ) + " is not in this game" )


	def handlePygameInput( self, key ): #				NOTE : DEBUG MODE ONLY
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

			if cfg.PRINT_PACKETS:
				print( f"{self.gameID} )  {self.type}  \t: player info\t: {self.getPlayerInfo()}" )

				if cfg.DEBUG_MODE:
					import GameManager as gm
					print( f"{self.gameID} )  {self.type}  \t: init info\t: {gm.GameManager.getInitInfo( self.type )}" )

			if cfg.PRINT_STATES:
				print( f"{self.gameID} )  {self.type}  \t: game has been started" )
		else:
			print( "Warning : game # " + str( self.gameID ) + " is already running or over" )


	def close( self ):
		self.state = df.ENDING

		if cfg.PRINT_STATES:
			print( f"{self.gameID} )  {self.type}  \t: game has been closed" )

	# --------------------------------------------------------------

	async def run( self ):

		if not cfg.DEBUG_MODE:
			print( "Warning : cannot use game.run() without DEBUG_MODE on" )
			return

		if self.state != df.PLAYING:
			print( "Warning : game #" + str( self.gameID ) + " was not started" )
			return

		# main game loop
		while self.state == df.PLAYING:
			await self.eventControler()
			self.step( True )
			self.clock.tick( cfg.FRAME_RATE )



	def step( self, display = False ):

		if self.state != df.PLAYING:
			print( "Warning : game #" + str( self.gameID ) + " was not started" )
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

		if cfg.DEBUG_MODE and cfg.PRINT_EXTRA and cfg.PRINT_PACKETS:
			print( f"{self.gameID} )  {self.type}  \t: update info\t: {self.getUpdateInfo()}" )


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
		if not rack.isOnScreen():
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
				self.last_ponger = rack.id
				self.ballEvent( ball, df.HITS, self.getTeamID( self.last_ponger ) ) #	NOTE : does not handle multiple rackets scoring

				break # 																NOTE : prevents multihits


	# bouncing on the walls
	def checkWalls( self, ball ):
		if ball.getLeft() < 0 or ball.getRight() > self.width or ball.getTop() < 0:

			# bouncing off the sides
			if ball.getLeft() < 0 or ball.getRight() > self.width:
				ball.bounceOnWall( "x" )

			# bouncing off the top
			if ball.getTop() < 0:
				ball.bounceOnWall( "y" )


	# scoring a goal
	def checkGoals( self, ball ):
		if ball.getBottom() >= self.height:
			self.ballEvent( ball, df.GOALS, self.getTeamID( self.last_ponger ) )

			if self.connector != None:
				self.connector.update_scores( self.scores )

	# --------------------------------------------------------------

	# called when a ball either hits a racket or scores a goal
	def ballEvent( self, ball, mode, teamID ):
		if self.score_mode == df.HITS: #	if racket hits give points

			if mode == df.HITS: # 				if it was a hit
				self.scorePoint( teamID )

			elif self.last_ponger > 0: # 							if it was a goal
				self.scores[ teamID - 1 ] = 0
				if cfg.PRINT_POINTS:
					print( f"{self.gameID} )  {self.type}  \t: team #{ teamID }  dropped the ball ( resets their score )" )

		else: #								if goals give points
			if self.last_ponger <= 0: #			if it was a serve ball
				self.missShot()
			elif mode == df.GOALS: # 			if it was a goal
				self.scorePoint( teamID )

		if mode == df.HITS: # 			reset the miss counter if it was a hit
			self.miss_shots = 0
		else: # 						respawn the ball if it was a goal
			self.respawnBall( ball )


	def scorePoint( self, teamID ):
		self.scores[ teamID - 1 ] += 1

		if cfg.PRINT_POINTS:
			if self.score_mode == df.GOALS:
				print( f"{self.gameID} )  {self.type}  \t: team #{ teamID }  scored a point" )
			else:
				print( f"{self.gameID} )  {self.type}  \t: team #{ teamID }  hit the ball" )

		self.findNextSpawn( "goal" )
		self.checkWin( teamID )


	def missShot( self ):
		self.missed_shots += 1

		if self.missed_shots >= df.MAX_MISS:
			self.missed_shots = 0
			self.findNextSpawn( "miss" )

			if cfg.PRINT_STATES:
				print( f"{self.gameID} )  {self.type}  \t: resetting miss_shots" )


	def findNextSpawn( self, mode ):

		if mode == "miss":
			self.spawn_target += 1
			self.spawn_target %= self.score_count
		if mode == "goal":
			self.spawn_target = self.getTeamID( self.last_ponger ) % self.score_count # rotatea target on goal

	# --------------------------------------------------------------

	def checkWin( self, teamID ):
		score = self.scores[ teamID ]

		if score >= df.WIN_SCORE:
			self.winnerID = teamID #	NOTE : this is a scores[] index ( same as teamID ) ( 0 == null)

			if cfg.PRINT_STATES:
				print( f"{self.gameID} )  {self.type}  \t: game has been won by team #{ self.winnerID }" )

			if cfg.PRINT_PACKETS:
				print( f"{self.gameID} )  {self.type}  \t: end info\t: {self.getEndInfo()}" )

			self.close()


	def respawnBall( self, ball ):
		self.last_ponger = 0

		s = self.spawns[ self.spawn_target ]

		ball.setPos( s[ 0 ], s[ 1 ])
		ball.setSpeeds( s[ 2 ] * self.speed_b, s[ 3 ] * self.speed_b )
		ball.setDirs( s[ 4 ], s[ 5 ] )


	def respawnAllBalls( self ): #				NOTE : made to handle more than one ball, but there is only one for now
		for i in range( len( self.balls )):
			self.respawnBall( self.balls[ i ] )


	def getTeamID( self, racketID ):
		return( racketID )

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

		if cfg.PRINT_DEBUG:
			self.drawFps()
			self.drawNames()

		pg.display.flip()#				drawing the newly prepared frame


	def drawLines( self ):
		for line in self.lines:
			start = ( int( self.width * line[ 0 ][ 0 ]), int( self.height * line[ 0 ][ 1 ]))
			end = ( int( self.width * line[ 1 ][ 0 ]), int( self.height * line[ 1 ][ 1 ]))

			pg.draw.line( self.win, df.COL_FNT, start, end, int( self.size_l * line[ 2 ]))


	def drawScores( self ):
		if self.posN1 != None:
			text = self.font.render( f'{ self.scores[ 0 ]}', True, df.COL_FNT )
			self.win.blit( text, text.get_rect( center = self.posN1 ))
		if self.posN2 != None:
			text = self.font.render( f'{ self.scores[ 1 ]}', True, df.COL_FNT )
			self.win.blit( text, text.get_rect( center = self.posN2 ))
		if self.posN3 != None:
			text = self.font.render( f'{ self.scores[ 2 ]}', True, df.COL_FNT )
			self.win.blit( text, text.get_rect( center = self.posN3 ))
		if self.posN4 != None:
			text = self.font.render( f'{ self.scores[ 3 ]}', True, df.COL_FNT )
			self.win.blit( text, text.get_rect( center = self.posN4 ))


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

		for i in range( len( self.balls )):
			ball = self.balls[ i ]

			text = self.racket_font.render( str( self.last_ponger ), True, df.COL_FNT )
			self.win.blit( text, text.get_rect( center = ball.box.center ))


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

		infoDict[ "gameType" ] = self.type
		infoDict[ "gameMode" ] = self.getMode()
		infoDict[ "endState" ] = self.getEndState()

		infoDict[ "winningTeam" ] = self.winnerID
		infoDict[ "quitter" ] = self.quitterID
		infoDict[ "scores" ] = self.scores

		infoDict[ "playerInfo" ] = self.getPlayerInfo()

		return( infoDict )

	def getEndState( self ):
		if( self.quitterID != 0 ):
			return "quit"
		elif( self.winnerID != 0):
			return "win"
		else:
			return "abort" #							NOTE : LL see if frontend needs this to be crash instead

	# --------------------------------------------- CLASS END ---------------------------------------------- #


if __name__ == '__main__': #			NOTE : DEBUG MODE ONLY

	pg.init()
	g = Game( 1 )

	g.setWindow( pg.display.set_mode(( 1280, 1280 )))
	pg.display.set_caption( g.type )

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()