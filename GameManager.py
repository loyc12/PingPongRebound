import time
import asyncio as asy
import random as rdm

try:
	from master import cfg
	if cfg.DEBUG_MODE:
		from master import pg
		import sys #	to exit properly
	import Addons as ad

	from Pi import Pi
	from Po import Po
	from Ping import Ping
	from Pong import Pong
	from Pinger import Pinger
	from Ponger import Ponger
	from Pingest import Pingest
	from Pongest import Pongest

except ModuleNotFoundError:
	from game.PingPongRebound.master import cfg
	import game.PingPongRebound.Addons as ad

	from game.PingPongRebound.Pi import Pi
	from game.PingPongRebound.Po import Po
	from game.PingPongRebound.Ping import Ping
	from game.PingPongRebound.Pong import Pong
	from game.PingPongRebound.Pinger import Pinger
	from game.PingPongRebound.Ponger import Ponger
	from game.PingPongRebound.Pingest import Pingest
	from game.PingPongRebound.Pongest import Pongest


class GameManager:

	gameTypeCount = 8

	windowID = 0 #							NOTE : DEBUG

	def __init__( self ):

		self.gameCount = 0
		self.maxGameCount = 0
		self.runGames = False

		self.lock = asy.Lock()
		self.previousTime = 0.0
		self.currentTime = 0.0
		self.sleep_loss = 0.001 # 			NOTE : will adjust itself over time
		self.meanDt = cfg.FRAME_DELAY #		NOTE : DEBUG

		self.gameDict = {}

		if cfg.DEBUG_MODE:
			pg.init()
			self.win = pg.display.set_mode((2048, 1280))
			pg.display.set_caption("Game Manager")


	# ---------------------------------------------- GAME CMDS --------------------------------------------- #

	async def addGame( self, gameType, gameID):
		async with self.lock:
			Initialiser = self.getInitialiser( gameType )

			if (Initialiser == None):
				print ("could not add game of type " + gameType)
				return 0

			if (self.gameDict.get( gameID ) != None):
				print ("game #" + str( gameID ) + " already exists")
				return 0

			self.gameDict[ gameID ] = Initialiser( gameID )

			if cfg.DEBUG_MODE:
				self.gameDict.get( gameID ).setWindow(self.win)
				self.addPlayerToGame( gameID, "Tester " + str( gameID ), gameID ) #		NOTE : DEBUG

				if len( self.gameDict ) > self.maxGameCount:
					self.maxGameCount = len( self.gameDict )

			if not self.runGames:
				self.runGames = True

				#asy.get_event_loop().create_task(self.mainloop()) #					NOTE : does nothing ?

		return gameID


	async def removeGame( self, gameID ):
		async with self.lock: #						NOTE : not needed, makes shit crash
			game = self.gameDict.get( gameID )

			if game == None:
				print ("game #" + str( gameID ) + " does not exist")
				return

			game.close()
			self.gameDict.pop(gameID)

			if len ( self.gameDict ) == 0:
				self.runGames = False


	async def addPlayerToGame( self, playerID, name, gameID ):

		async with self.lock:
			game = self.gameDict.get( gameID )

			if game == None:
				print ("game #" + str( gameID ) + " does not exist")
				print ("could not add player #" + str( playerID ) + " to game #" + str( gameID ))
				return

			self.gameDict.get( gameID ).addPlayer( name, playerID )


	async def removePlayerFromGame( self, playerID, gameID ):
		async with self.lock:
			game = self.gameDict.get( gameID )

			if game == None:
				print ("game #" + str( gameID ) + " does not exist")
				print ("could not remove player #" + str( playerID ) + " from game #" + str( gameID ))
				return

			if not game.hasPlayer( playerID ):
				print ("player #" + str( playerID ) + " is absent from game #" + str( gameID ))
				print ("could not remove player #" + str( playerID ) + " from game #" + str( gameID ))
				return

			# NOTE : to know how to handle player leaving
			#if game.state == ad.STARTING:
			#	pass
			#elif game.state == ad.PLAYING:
			#	pass
			#elif game.state == ad.ENDING:
			#	pass

			game.removePlayer( playerID )


	async def startGame( self, gameID ):
		async with self.lock:
			game = self.gameDict.get( gameID )

			if game == None:
				print ("game #" + str( gameID ) + " does not exist")
				print ("could not start game #" + str( gameID ))
				return

			game.start()


	async def closeGame( self, gameID ):
		async with self.lock:
			game = self.gameDict.get( gameID )

			if game == None:
				print ("game #" + str( gameID ) + " does not exist")
				print ("could not close close #" + str( gameID ))
				return

			game.close()


	def runGameStep( self, game ):
		if game.state == ad.PLAYING:

			game.moveObjects()
			game.makeBotsPlay()
			game.tickTime() #			NOTE : only does stuff in debug mode

		else:
			print (" this game is not currently running ")


	async def tickGames(self):
		deleteList = []
		#async with self.lock: #					NOTE : useless???
		for key, game in self.gameDict.items():

			if game.state == ad.STARTING:
				pass #								send player info packet from here

			elif game.state == ad.PLAYING:
				game.step( False )

				if cfg.DEBUG_MODE: #				NOTE : DEBUG
					if key == self.windowID:
						self.displayGame( game )

			elif game.state == ad.ENDING:
				if cfg.DEBUG_MODE and self.windowID == key:
					print ( "this game no longer exists" )
					print ( "please select a valid game (1-8)" )
					self.windowID = 0
					self.emptyDisplay()

				else: #								send closing info packet from here
					pass

				deleteList.append(key)

		for key in deleteList:
			await self.removeGame( key )


#	NOTE : this assumes load is generally small and constant, and aims to keep the mean frame time at cfg.FRAME_DELAY
	def getNextSleepDelay(self):
		self.currentTime = time.monotonic()
		dt = self.currentTime - self.previousTime
		self.previousTime = self.currentTime
		#print('time between frames: ', dt)

		self.meanDt = self.meanDt * 0.95 + dt * 0.05
		print('mean between frames: ', self.meanDt)

		diversion = cfg.FRAME_DELAY - dt

		correction = ( self.sleep_loss + diversion) * 0.1

		self.sleep_loss -= correction

		delay = ( cfg.FRAME_DELAY - self.sleep_loss ) * 0.85

		#print('next sleep delay   : ', delay)
		#print("delta time: ", dt, "diversion: ", diversion, "sleep loss: ", self.sleep_loss, "correction: ", correction)

		return delay


#	NOTE : this does not work precisely due to sleep being an imprecise bitch
#	async def SmartSleep(self):
#		self.currentTime = time.monotonic()
#		print("frame_time : ", str( self.currentTime - self.debugTime ))
#		self.debugTime = self.currentTime
#
#		dt = self.currentTime - self.previousTime #how long processing took
#
#		delay = cfg.FRAME_DELAY - dt
#
#		if (delay > 0):
#			await asy.sleep( delay )
#			#print("delay : " + str( delay ) + "\t : dt : " + str( dt ))
#
#		self.previousTime = time.monotonic()


	async def mainloop(self):

		print( ">  STARTING MAINLOOP  <" )

		self.currentTime = time.monotonic()
		await asy.sleep( cfg.FRAME_DELAY - self.sleep_loss )

		if not cfg.DEBUG_MODE:
			while self.runGames:
				await self.tickGames()
				await asy.sleep( self.getNextSleepDelay() )

		else:
			self.emptyDisplay()

			while self.runGames:
				self.takePlayerInputs()
				await self.tickGames()
				await asy.sleep( self.getNextSleepDelay() )

		print( ">  EXITED MAINLOOP  <" )


	# ---------------------------------------------- DEBUG CMDS -------------------------------------------- #

	def displayGame( self, game ): # 					NOTE : DEBUG
		if game.state == ad.PLAYING:
			if game.width != self.win.get_width() or game.height != self.win.get_height():
				self.win = pg.display.set_mode( (game.width, game.height) )
				pg.display.set_caption( game.name ) #

			game.refreshScreen()


	def emptyDisplay( self ): # 						NOTE : DEBUG
		pg.display.set_caption("Game Manager")
		self.win = pg.display.set_mode((2048, 1280))
		self.win.fill( pg.Color('black') )


	def takePlayerInputs( self ): # 					NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				k = event.key

				if cfg.DEBUG_MODE:
					initialID = self.windowID

					# closes the game
					if k == pg.K_ESCAPE:
						for game in self.gameDict.values():
							game.close()
						self.runGames = False
						sys.exit()

					# respawns the ball
					elif k == ad.RETURN:
						if self.windowID != 0:
							if self.gameDict.get(self.windowID) != None:
								game = self.gameDict.get(self.windowID)
								game.respawnAllBalls()
								print ( "respawning the ball(s)" )
							else:
								print ( "coud not respawn the ball(s)" )
						else:
							print ( "please select a valid game (1-8)" )
						return

					# rotate game to view
					elif k == pg.K_q or k == pg.K_e:
						if k == pg.K_e:
							self.windowID += 1
						else:
							self.windowID -= 1

						if self.windowID <= 0:
							self.windowID = self.maxGameCount
						elif self.windowID > self.maxGameCount:
							self.windowID = 1

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
						if self.gameDict.get(self.windowID) == None:
							print( "could not switch to game #" + str( self.windowID ) )
							print( "please select a valid game (1-8)" )
							self.emptyDisplay()
						else:
							print( "now playing in game #" + str( self.windowID ) )
							pg.display.set_caption( self.gameDict.get(self.windowID).name )
						return

				# handling movement keys presses
				if self.gameDict.get(self.windowID) == None:
					if self.windowID != 0:
						print( "game #" + str( self.windowID ) + " no longer exists" )
					print( "please select a valid game (1-8)" )
				else:
					controler = self.gameDict.get(self.windowID).controlers[0]
					if controler.mode != ad.PLAYER:
						print ( "cannot move a bot's racket" )
					else:
						controler.handleKeyInput(k)


	async def addAllGames( self ): #					NOTE : DEBUG
		gameID = 1

		await self.startGame( await self.addGame( "Pi", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Po", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Ping", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Pong", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Pinger", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Ponger", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Pingest", gameID ))
		gameID += 1
		await self.startGame( await self.addGame( "Pongest", gameID ))
		gameID += 1

		print ("select a player (1-8)")


	# ---------------------------------------------- INFO CMDS --------------------------------------------- #

	@staticmethod
	def getMaxPlayerCount( gameType ):
		if gameType == "Pi":
			return Pi.maxPlayerCount
		elif gameType == "Ping":
			return Ping.maxPlayerCount
		elif gameType == "Pinger":
			return Pinger.maxPlayerCount
		elif gameType == "Pingest":
			return Pingest.maxPlayerCount
		elif gameType == "Po":
			return Po.maxPlayerCount
		elif gameType == "Pong":
			return Pong.maxPlayerCount
		elif gameType == "Ponger":
			return Ponger.maxPlayerCount
		elif gameType == "Pongest":
			return Pongest.maxPlayerCount
		else:
			print ( "Error : GameManager.getMaxPlayerCount() : invalid game type" )
			return 0


	@staticmethod
	def getInitialiser( gameType, rdmStart = 4 ):
		if gameType == "Pi":
			return Pi
		elif gameType == "Ping":
			return Ping
		elif gameType == "Pinger":
			return Pinger
		elif gameType == "Pingest":
			return Pingest
		elif gameType == "Po":
			return Po
		elif gameType == "Pong":
			return Pong
		elif gameType == "Ponger":
			return Ponger
		elif gameType == "Pongest":
			return Pongest
		elif gameType == "Random":
			return GameManager.getRandomGameType(rdmStart)
		else:
			print ( "Error : GameManager.getInitialiser() : invalid game type" )
			return None


	@staticmethod
	def getRandomGameType(playerCount = 1):
		if playerCount == 1:
			start = 0
		elif playerCount == 2:
			start = 2
		elif playerCount == 4:
			start = 4
		else:
			print( "Error : GameManager.getRandomGameType() : invalid player count" )
			return None

		value = rdm.randint(start, GameManager.gameTypeCount - 1 )
		if value == 0:
			return "Pi"
		elif value == 2:
			return "Ping"
		elif value == 4:
			return "Pinger"
		elif value == 6:
			return "Pingest"
		elif value == 1:
			return "Po"
		elif value == 3:
			return "Pong"
		elif value == 5:
			return "Ponger"
		elif value == 7:
			return "Pongest"


def testAllGames():
	gm = GameManager()
	asy.run ( gm.addAllGames() )
	asy.run ( gm.mainloop() )


if __name__ == '__main__':
	testAllGames()