import pygame as pg
import asyncio as asy
import random as rdm
import Addons as ad
import sys

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

	def __init__( self, _debugMode = True ):
		self.debugMode = _debugMode #		NOTE : DEBUG

		self.gameCount = 0
		self.maxGameCount = 0
		self.runGames = True

		self.gameDict = {}


	def addGame( self, gameType, gameID):

		Initialiser = self.getInitialiser( gameType )

		if (Initialiser == None):
			print ("could not add game of type " + gameType)
			return 0

		newGame = Initialiser( gameID, self.debugMode ) # 	TODO : detach from pygame
		if self.debugMode:
			newGame.setWindow(self.win)
		self.gameDict[gameID] = newGame
		self.gameCount += 1
		if self.gameCount > self.maxGameCount:
			self.maxGameCount = self.gameCount

		#if self.debugMode:
			#self.addPlayerToGame( GameID, "Tester " + str( GameID ), GameID ) #		NOTE : DEBUG

		return gameID


	def addPlayerToGame( self, playerID, name, key ):
		try:
			self.gameDict.get(key).addPlayer( name, playerID )
		except:
			print ("could not add player #" + str( playerID ) + " to game #" + str( key ))


	def startGame( self, key ):
		self.gameDict.get(key).start()


	def removePlayerFromGame( self, _playerID, key ):
		if ( self.gameDict.get(key).removePlayer( _playerID )):
			pass
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
			game.clock.tick (game.framerate) # 	TODO : detach from pygame

		else:
			print (" this game is not currently running ")



	def tickGames(self):
		try: #		 NOTE : ineloquent but ffs why the fuck can't you edit a dict while itterating in it...
			 #				like isn't that the whole fucking point of not using a different type of container
			for key in self.gameDict.keys():
				game = self.gameDict.get( key )

				if game.state == ad.ENDING:
					if self.debugMode and self.windowID == key:
						print ("this game no longer exists")
						print ("please select a valid game (1-8)")
						self.windowID = 0
						self.emptyDisplay()

					else: #								send closing info packet from here
						pass

					self.removeGame( key )

				elif game.state == ad.PLAYING:
					self.runGameStep( game )

					if self.debugMode: #				NOTE : DEBUG
						if key == self.windowID:
							self.displayGame( game )
		except:
			print("GameManager Error : tickGames() : removed item while iterating over gameDict")


	def takePlayerInputs( self ): # 					NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				k = event.key

				if self.debugMode:
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
			if game.width != self.win.get_width() or game.height != self.win.get_height(): # 	TODO : detach from pygame
				self.win = pg.display.set_mode( (game.width, game.height) )
				pg.display.set_caption( game.name ) #

			game.refreshScreen()


	def emptyDisplay( self ):
		pg.display.set_caption("Game Manager") # 			NOTE : DEBUG
		self.win = pg.display.set_mode((2048, 1280)) # 		NOTE : ...
		self.win.fill( pg.Color('black') ) # 				NOTE : ...


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
			print ( "GameManager Error : getMaxPlayerCount() : invalid game type" )
			return 0

	@staticmethod
	def getRandomGameType(playerCount = 1):
		if playerCount == 1:
			start = 0
		elif playerCount == 2:
			start = 2
		elif playerCount == 4:
			start = 4
		else:
			print( "GameManager Error : getRandomGameType() : invalid player count" )
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

	@staticmethod
	def getInitialiser( gameType ):
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
		else:
			return None


async def main():  # ASYNC IS HERE

	gm = GameManager()

	if (gm.debugMode):
		pg.init()
		gm.emptyDisplay()

	addAllGames( gm )

	while gm.runGames:

		if gm.debugMode:
			gm.takePlayerInputs()

		gm.tickGames()

	if gm.debugMode:
		await asy.sleep(0)
	else: # 											NOTE : put fps here if not in debugMode
		pass


def addAllGames( gm ): #								NOTE : DEBUG
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


