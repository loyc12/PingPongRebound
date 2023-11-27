from master import cfg
if cfg.DEBUG_MODE:
	from master import pg
	import sys #	to exit properly
import asyncio as asy
import time
import random as rdm
import Addons as ad

from Pi import Pi
from Po import Po
from Ping import Ping
from Pong import Pong
from Pinger import Pinger
from Ponger import Ponger
from Pingest import Pingest
from Pongest import Pongest

class GameManager:

	gameTypeCount = 8

	windowID = 0 #							NOTE : DEBUG

	def __init__( self ):

		self.gameCount = 0
		self.maxGameCount = 0
		self.runGames = True

		self.lock = asy.Lock()
		self.t0 = None
		self.t1 = None
		self.sleep_loss = 0.001# Rough estimate. Will adjust over time

		self.gameDict = {}


	def addGame( self, gameType, gameID):

		Initialiser = self.getInitialiser( gameType )

		if (Initialiser == None):
			print ("could not add game of type " + gameType)
			return 0

		newGame = Initialiser( gameID ) # 	TODO : detach from pygame
		if cfg.DEBUG_MODE:
			newGame.setWindow(self.win)
		self.gameDict[gameID] = newGame
		self.gameCount += 1
		if self.gameCount > self.maxGameCount:
			self.maxGameCount = self.gameCount

		#if cfg.DEBUG_MODE:
			#self.addPlayerToGame( GameID, "Tester " + str( GameID ), GameID ) #		NOTE : DEBUG

		return gameID


	def addPlayerToGame( self, playerID, name, key ):
		if ( self.gameDict.get(key)):
			self.gameDict.get(key).addPlayer( name, playerID )
		else:
			print ("could not add player #" + str( playerID ) + " to game #" + str( key ))


	def startGame( self, key ):
		self.gameDict.get(key).start()


	def removePlayerFromGame( self, _playerID, key ):
		if ( self.gameDict.get(key)):
			self.gameDict.get(key).removePlayer( _playerID )
		else:
			print ("player #" + str( _playerID ) + " is absent from game #" + str( key ))

	def removeGame( self, key ):
		self.gameDict.get(key).close()
		self.gameDict.pop(key)
		self.gameCount -= 1


	def runGameStep( self, game ):
		if game.state == ad.PLAYING:

			game.moveObjects()
			game.makeBotsPlay()
			game.tickTime() #						NOTE : DEBUG

		else:
			print (" this game is not currently running ")



	async def tickGames(self):
		deleteList = []
		async with self.lock:
			for key, game in self.gameDict.items():

				if game.state == ad.STARTING:
					pass #								send player info packet from here

				elif game.state == ad.PLAYING:
					self.runGameStep( game )

					if cfg.DEBUG_MODE: #				NOTE : DEBUG
						if key == self.windowID:
							self.displayGame( game )

				elif game.state == ad.ENDING:
					if cfg.DEBUG_MODE and self.windowID == key:
						print ("this game no longer exists")
						print ("please select a valid game (1-8)")
						self.windowID = 0
						self.emptyDisplay()

					else: #								send closing info packet from here
						pass

					deleteList.append(key)

			for key in deleteList:
				self.removeGame( key )


	def getNextSleepDelay(self):
		self.t1 = time.monotonic()
		dt = self.t1 - self.t0
		self.t0 = self.t1

		diversion = dt - cfg.FRAME_DELAY

		correction = (diversion - self.sleep_loss) * 0.1
		self.sleep_loss += correction # (diversion - self.sleep_loss) * 0.1
		#print("delta time: ", dt, "diversion: ", diversion, "sleep loss: ", self.sleep_loss, "correction: ", correction)
		#print('next sleep delay: ', cfg.FRAME_DELAY - self.sleep_loss)
		return cfg.FRAME_DELAY - self.sleep_loss


	async def mainloop(self):

		await asy.sleep(cfg.FRAME_DELAY - self.sleep_loss)

		if  not cfg.DEBUG_MODE:
			while self.runGames:
				await self.tickGames()
				await asy.sleep(self.getNextSleepDelay())

		else:
			pg.init()
			self.emptyDisplay()
			addAllGames( self )

			while self.runGames:
				self.takePlayerInputs()
				await self.tickGames()

		print('MAINLOOP EXIT !')


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



	def displayGame( self, game ): # 						NOTE : DEBUG
		if game.state == ad.PLAYING:
			if game.width != self.win.get_width() or game.height != self.win.get_height():
				self.win = pg.display.set_mode( (game.width, game.height) )
				pg.display.set_caption( game.name ) #

			game.refreshScreen()


	def emptyDisplay( self ): # 							NOTE : DEBUG
		pg.display.set_caption("Game Manager")
		self.win = pg.display.set_mode((2048, 1280))
		self.win.fill( pg.Color('black') )


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


async def main():

	gm = GameManager()

	if  not cfg.DEBUG_MODE:
		while gm.runGames:
			await gm.tickGames()
			await asy.sleep(cfg.FRAME_DELAY)

	else:
		pg.init()
		gm.emptyDisplay()
		addAllGames( gm )

		while gm.runGames:
			gm.takePlayerInputs()
			await gm.tickGames()


def addAllGames( gm ): #					NOTE : DEBUG
	gameID = 1

	gm.startGame( gm.addGame( "Pi", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Po", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Ping", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Pong", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Pinger", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Ponger", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Pingest", gameID ))
	gameID += 1
	gm.startGame( gm.addGame( "Pongest", gameID ))
	gameID += 1

	print ("select a player (1-8)")

if __name__ == '__main__':
	asy.run( main())


