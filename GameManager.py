import time
import asyncio as asy
import random as rdm

# NOTE : two different ways to import( standalone vs in transcendance )
try:
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg
		import sys #	to exit properly
	import defs as df
	from games import *

except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	import game.PingPongRebound.defs as df
	from game.PingPongRebound.games import *


class GameManager:

	if cfg.DEBUG_MODE:
		gameTypeCount = 8
		windowID = 0


	# ------------------------------------------- INITIALIZATION ------------------------------------------- #


	def __init__( self, _gg = None ):

		self.gameGateway = _gg #			NOTE : use me to broadcast game states

		self.gameCount = 0
		self.maxGameCount = 0
		self.runGames = False

		self.dictLock = asy.Lock()
		self.tickLock = asy.Lock()
		self.previousTime = 0.0
		self.currentTime = 0.0
		self.sleep_loss = 0.0 # 			NOTE : will adjust itself over time
		self.meanDt = cfg.FRAME_DELAY #		NOTE : DEBUG

		self.gameDict = {}

		if cfg.DEBUG_MODE:
			pg.init()
			self.win = pg.display.set_mode(( 2048, 1280 ))
			pg.display.set_caption( "Game Manager" )


	# ---------------------------------------------- GAME CMDS --------------------------------------------- #


	async def addGame( self, gameType, gameID, connector = None, gameMode = df.SOLO ):
		Initialiser = self.getInitialiser( gameType, connector )

		if( Initialiser == None ):
			print( "could not add game of type " + gameType )
			return 0

		if( self.gameDict.get( gameID )!= None ):
			print( "game #" + str( gameID ) + " already exists" )
			return 0

		async with self.dictLock:

			self.gameDict[ gameID ] = Initialiser( gameID, gameMode, connector )

			if cfg.DEBUG_MODE :
				self.gameDict.get( gameID ).setWindow( self.win )

				if( len( self.gameDict ) > self.maxGameCount ):
					self.maxGameCount = len( self.gameDict )

			if not self.runGames:
				self.runGames = True

				if not cfg.DEBUG_MODE:
					# we do this so the games can run asynchronously with the rest of the server
					asy.get_event_loop().create_task( self.mainloop() )

		return gameID


	async def removeGame( self, gameID ):
			game = self.gameDict.get( gameID )

			if game == None:
				print( "game #" + str( gameID ) + " does not exist" )
				return

			async with game.gameLock:

				if( game.state != df.ENDING ):
					game.close()

				# NOTE : ian check icitte pour le closing

				if game.connector != None:
					await self.gameGateway.manage_end_game( game.getEndInfo() )

			async with self.dictLock:
				self.gameDict.pop( gameID )

				if len( self.gameDict ) == 0:
					self.runGames = False

	# --------------------------------------------------------------

	async def startGame( self, gameID ):
		game = self.gameDict.get( gameID )

		if game == None:
			print( "game #" + str( gameID ) + " does not exist" )
			print( "could not start game #" + str( gameID ))
			return

		async with game.gameLock:
			game.start()


	async def closeGame( self, gameID ):
		game = self.gameDict.get( gameID )

		if game == None:
			print( "game #" + str( gameID ) + " does not exist" )
			print( "could not close close #" + str( gameID ))
			return

		async with game.gameLock:
			game.close()


	async def hasGame( self, gameID ):
		if self.gameDict.get( gameID )!= None:
			return True
		return False


	# -------------------------------------------- PLAYER CMDS --------------------------------------------- #


	async def addPlayerToGame( self, playerID, name, gameID ):
		game = self.gameDict.get( gameID )

		if game == None:
			print( "game #" + str( gameID ) + " does not exist" )
			print( "could not add player #" + str( playerID ) + " to game #" + str( gameID ))
			return

		async with game.gameLock:
			game.addPlayer( name, playerID )
			if game.mode == df.DUAL and game.racketCount > 1:
				game.addPlayer( "guest", 0 )


	async def removePlayerFromGame( self, playerID, gameID ):
		game = self.gameDict.get( gameID )

		if game == None:
			print( "game #" + str( gameID ) + " does not exist" )
			print( "could not remove player #" + str( playerID ) + " from game #" + str( gameID ))
			return

		async with game.gameLock:
			if not game.hasPlayer( playerID ):
				print( "player #" + str( playerID ) + " is absent from game #" + str( gameID ))
				print( "could not remove player #" + str( playerID ) + " from game #" + str( gameID ))
				return

			game.removePlayer( playerID )



	# -------------------------------------------- CORE CMDS --------------------------------------------- #


	async def mainloop( self ):

		print( "> STARTING MAINLOOP <" )

		self.currentTime = time.monotonic()

		try:
			await asy.sleep( 0 )
		except asy.exceptions.CancelledError:
			print( "preemtively removed sleep errors..." )

		# NOTE : to allow time between frames to be cfg.FRAME_DELAY on next update
		await asy.sleep( cfg.FRAME_DELAY * 0.75 )

		if cfg.DEBUG_MODE:
			self.emptyDisplay()

		while self.runGames:

			if cfg.DEBUG_MODE:
				self.managePygameInputs()

			await self.tickGames()

			if cfg.PRINT_PACKETS and not cfg.DEBUG_MODE:
				print( self.getGameUpdates() )

			if self.gameGateway != None:
				await self.gameGateway.async_send_all_updates( self.getGameUpdates(), True )


			await asy.sleep( self.getNextSleepDelay() )

		print( "> EXITING MAINLOOP <" )

	# --------------------------------------------------------------

	# NOTE : runs a single game step( what to do between to frames )
	async def tickGames( self ):
		deleteList = []

		async with self.tickLock:
			#async with self.dictLock:
				for( key, game )in self.gameDict.items():
					async with game.gameLock:

						if game.connector != None and not cfg.DEBUG_MODE:
							await game.eventControler()

						if game.state == df.STARTING:
							pass

						elif game.state == df.PLAYING:
							game.step()

							if cfg.DEBUG_MODE:
								if key == self.windowID:
									self.displayGame( game )

						elif game.state == df.ENDING:
							if cfg.DEBUG_MODE and self.windowID == key:
								print( "this game no longer exists" )
								print( "please select a valid game( 1-8 )" )
								self.emptyDisplay()

							else: #					send closing info packet from here ?
								pass

							deleteList.append( key )

		for key in deleteList:
			await self.removeGame( key )

	# --------------------------------------------------------------

#	NOTE : this assumes load is generally small and constant, and aims to keep the mean frame time at cfg.FRAME_DELAY
#	NOTE : doing this without correction is too imprecise because of asy.sleep() being a bitch
	def getNextSleepDelay( self ):
		self.previousTime = self.currentTime
		self.currentTime = time.monotonic()
		dt = self.currentTime - self.previousTime

		diversion = cfg.FRAME_DELAY - dt

		correction = ( self.sleep_loss + diversion ) * 0.1

		self.sleep_loss -= correction

		delay = ( cfg.FRAME_DELAY - self.sleep_loss ) * cfg.FRAME_FACTOR

		if cfg.PRINT_FRAMES: #			NOTE : DEBUG PRINTS
			self.meanDt = ( dt + ( self.meanDt * cfg.FPS_SMOOTHING )) / ( cfg.FPS_SMOOTHING + 1 )
			print( "frame time: {:.5f} \t".format( dt ), "mean time: {:.5f} \t".format( self.meanDt ), "sleep time: {:.5f} \t".format( delay ))
			#print( "diversion: {:.5f} \t".format( diversion ), "sleep loss: {:.5f} \t".format( self.sleep_loss ), "correction: {:.5f} \t".format( correction ))

		return delay


	# ---------------------------------------------- DEBUG CMDS -------------------------------------------- #


	def managePygameInputs( self ): # 					NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				k = event.key
				initialID = self.windowID

				# closes the game
				if k == pg.K_ESCAPE:
					for game in self.gameDict.values():
						game.close()
					self.runGames = False
					sys.exit()

				# respawns the ball
				elif k == df.RETURN:
					if self.windowID != 0:
						if self.gameDict.get( self.windowID )!= None:
							game = self.gameDict.get( self.windowID )
							game.respawnAllBalls()
							print( "respawning the ball( s )" )
						else:
							print( "coud not respawn the ball( s )" )
					else:
						print( "please select a valid game( 1-8 )" )
					return

				# find the next game to view
				elif k == pg.K_q or k == pg.K_e:
					i = 0
					# NOTE : this loops over the games until it finds one that can be displayed
					while i <= self.maxGameCount:

						i += 1
						if k == pg.K_e: #			NOTE : to go forward
							self.windowID += 1
						else: #						NOTE : to go backward
							self.windowID -= 1

						if self.windowID > self.maxGameCount:
							self.windowID = 1
						elif self.windowID < 0:
							self.windowID = self.maxGameCount

						if self.gameDict.get( self.windowID ) != None:
							i += self.maxGameCount #	NOTE : to break out of the loop

				# select game to view
				elif k == pg.K_0:
					self.windowID = 0
				elif k == pg.K_1:
					self.windowID = 1
				elif k == pg.K_2:
					self.windowID = 2
				elif k == pg.K_3:
					self.windowID = 3
				elif k == pg.K_4:
					self.windowID = 4
				elif k == pg.K_5:
					self.windowID = 5
				elif k == pg.K_6:
					self.windowID = 6
				elif k == pg.K_7:
					self.windowID = 7
				elif k == pg.K_8:
					self.windowID = 8
				elif k == pg.K_9:
					self.windowID = 9

				# checks if viewed game changed
				if initialID != self.windowID:
					game = self.gameDict.get( self.windowID )

					if game == None:
						print( "could not switch to game #" + str( self.windowID ))
						print( "please select a valid game( 1-8 )" )
						self.emptyDisplay()
					else:
						print( f"{ self.windowID} )  { game.name }  \t: switched game viewed ")
						game.delta_time = cfg.FRAME_DELAY
						game.last_time = time.time()
						pg.display.set_caption( game.name )
					return

				# handling movement keys presses
				if self.gameDict.get( self.windowID ) == None:
					if self.windowID != 0:
						print( "game #" + str( self.windowID ) + " no longer exists" )
					print( "please select a valid game( 1-8 )" )
				else:
					self.gameDict.get( self.windowID ).handlePygameInput( k )

# --------------------------------------------------------------

	async def addGameDebug( self, gameType, gameID, _gameMode ):
		await self.addGame( gameType, gameID, gameMode=_gameMode )

		if cfg.ADD_DEBUG_PLAYER:
			await self.addPlayerToGame( 1, "DBG", gameID )

		await self.startGame( gameID )

		return gameID + 1


	async def addAllGames( self ): #					NOTE : DEBUG
		gameID = 1
		gameMode = df.SOLO

		gameID = await self.addGameDebug( "Pi", gameID, df.SOLO )
		gameID = await self.addGameDebug( "Po", gameID, df.SOLO  )
		gameID = await self.addGameDebug( "Ping", gameID, gameMode )
		gameID = await self.addGameDebug( "Pong", gameID, gameMode )
		gameID = await self.addGameDebug( "Pinger", gameID, gameMode )
		gameID = await self.addGameDebug( "Ponger", gameID, gameMode )
		gameID = await self.addGameDebug( "Pingest", gameID, gameMode )
		gameID = await self.addGameDebug( "Pongest", gameID, gameMode )

		print( "select a player( 1-8 )" )


	def displayGame( self, game ): # 					NOTE : DEBUG
		if game.state == df.PLAYING:
			if game.width != self.win.get_width()or game.height != self.win.get_height():
				self.win = pg.display.set_mode(( game.width, game.height ))
				pg.display.set_caption( game.name )

			game.refreshScreen()


	def emptyDisplay( self ): # 						NOTE : DEBUG
		pg.display.set_caption( "Game Manager" )
		self.win = pg.display.set_mode(( 2048, 1280 ))
		self.win.fill( pg.Color( 'black' ))


	# ---------------------------------------------- INFO CMDS --------------------------------------------- #


	@staticmethod
	def getInitInfo( gameType ): #				INIT INFO GENERATOR
		gameClass = GameManager.getGameClass( gameType )
		initRacketsPos = GameManager.getRacketInitPos( gameClass )

		if( gameClass == None ):
			print( "Error : GameManager.getInitInfo(): invalid game type" )
			return None

		return {
			'gameType': gameClass.name,
			'sizeInfo': GameManager.getSizeInfo( gameClass ),
			'racketCount': gameClass.racketCount,
			'scorePos': GameManager.getScorePos( gameClass ),
			'lines': gameClass.lines,
			'scoreSize': gameClass.size_font,
			'orientations': [ initRacketsPos[( i * 3 ) + 2 ] for i in range( gameClass.racketCount )],
			'update': {
				'racketPos': [ coord for coord in initRacketsPos if not isinstance( coord, str )],
				'ballPos': GameManager.getBallInitPos( gameClass ),
				'lastPonger': 0,
				'scores': [ 0 for _ in range( gameClass.racketCount )]
			}
		}


	def getPlayerInfo( self, gameID ):
		game = self.gameDict.get( gameID )

		if game == None:
			print( "game #" + str( gameID ) + " does not exist" )
			print( "could not get player info from from game #" + str( gameID ))
			return

		return( game.getPlayerInfo() )


	def getGameUpdates( self ): #					UPDATE INFO GENERATOR
		return { key: game.getUpdateInfo() for key, game in self.gameDict.items() }

		# updateDict = {}
		# for key, game in self.gameDict.items():
		# 	updateDict[ key ] = game.getUpdateInfo()
		# return updateDict

	# --------------------------------------------------------------

	@staticmethod
	def getSizeInfo( gameClass ):
		return {
			"width": gameClass.width,
			"height": gameClass.height,
			"sRacket": gameClass.size_r,
			"sBall": gameClass.size_b
		}


	@staticmethod
	def getRacketInitPos( gameClass ):
		racksPos = []

		if( gameClass.iPosR1 != None ):
			racksPos.append( gameClass.iPosR1[ 0 ] )# position x
			racksPos.append( gameClass.iPosR1[ 1 ] )# position y
			racksPos.append( gameClass.iPosR1[ 2 ] )# direction
		if( gameClass.iPosR2 != None ):
			racksPos.append( gameClass.iPosR2[ 0 ] )
			racksPos.append( gameClass.iPosR2[ 1 ] )
			racksPos.append( gameClass.iPosR2[ 2 ] )
		if( gameClass.iPosR3 != None ):
			racksPos.append( gameClass.iPosR3[ 0 ] )
			racksPos.append( gameClass.iPosR3[ 1 ] )
			racksPos.append( gameClass.iPosR3[ 2 ] )
		if( gameClass.iPosR4 != None ):
			racksPos.append( gameClass.iPosR4[ 0 ] )
			racksPos.append( gameClass.iPosR4[ 1 ] )
			racksPos.append( gameClass.iPosR4[ 2 ] )

		return( racksPos )


	@staticmethod
	def getBallInitPos( gameClass ):
		ballsPos = []

		if( gameClass.iPosB1 != None ):
			ballsPos.append( gameClass.iPosB1[ 0 ] )# position x
			ballsPos.append( gameClass.iPosB1[ 1 ] )# position y

		return( ballsPos )


	@staticmethod
	def getScorePos( gameClass ):
		scoresPos = []

		if( gameClass.iPosS1 != None ):
			scoresPos.append( gameClass.iPosS1[ 0 ] )
			scoresPos.append( gameClass.iPosS1[ 1 ] )

		return( scoresPos )


	# --------------------------------------------- CLASS CMDS --------------------------------------------- #


	@staticmethod
	def getMaxPlayerCount( gameType ):
		gameClass = GameManager.getGameClass( gameType )

		if( gameClass != None ):
			return gameClass.racketCount

		print( "Error : GameManager.getMaxPlayerCount(): invalid game type" )
		return 0


	@staticmethod
	def getInitialiser( gameType, rdmStart = 4 ):
		return GameManager.getGameClass( gameType )

	@staticmethod
	def getGameClass( gameType, rdmStart = 4 ):
		if gameType == "Pi":
			return Pi
		elif gameType == "Po":
			return Po
		elif gameType == "Ping":
			return Ping
		elif gameType == "Pong":
			return Pong
		elif gameType == "Pinger":
			return Pinger
		elif gameType == "Ponger":
			return Ponger
		elif gameType == "Pingest":
			return Pingest
		elif gameType == "Pongest":
			return Pongest
		elif gameType == "Random":
			return GameManager.getRandomGameClass( rdmStart )

		print( "Error : GameManager.getGameClass(): invalid game type" )
		return None


	@staticmethod
	def getRandomGameClass( playerCount = 1 ):
		if playerCount == 1:
			start = 0
		elif playerCount == 2:
			start = 2
		elif playerCount == 4:
			start = 4
		else:
			print( "Error : GameManager.getRandomGameClass(): invalid player count" )
			return None

		value = rdm.randint( start, GameManager.gameTypeCount - 1 )
		if value == 0:
			return "Pi"
		elif value == 1:
			return "Po"
		elif value == 2:
			return "Ping"
		elif value == 3:
			return "Pong"
		elif value == 4:
			return "Pinger"
		elif value == 5:
			return "Ponger"
		elif value == 6:
			return "Pingest"
		elif value == 7:
			return "Pongest"


	# --------------------------------------------- CLASS END ---------------------------------------------- #


def testAllGames():
	gm = GameManager()

	#print( gm.getInitInfo( "Ping" ))
	#print( gm.getInitInfo( "Pong" ))
	#print( gm.getInitInfo( "Pingest" ))

	asy.run( gm.addAllGames() )
	if cfg.DEBUG_MODE:
		asy.run( gm.mainloop() )


if __name__ == '__main__':
	testAllGames()