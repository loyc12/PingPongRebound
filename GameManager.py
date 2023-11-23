from Pi import Pi
from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Po import Po
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest

import pygame as pg
import asyncio as asy
import Addons as ad
import sys

class GameManager:

	playerID = 0 #							NOTE : DEBUG
	debugMode = True #						NOTE : DEBUG

	def __init__( self ):
		self.lastGameID = 0
		self.gameCount = 0
		self.runGames = True
		self.gameDict = {}


	def getMaxPlayerCount( self, gameType ):
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
			return 0

	def getInitialiser( self, gameType ):
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


	def addGame( self, gameType, GameID):

		Initialiser = self.getInitialiser( gameType )

		if (Initialiser == None):
			print ("could not add game of type " + gameType)
			return 0

		newGame = Initialiser( self.debugMode ) # 	TODO : detach from pygame
		if self.debugMode:
			newGame.setWindow(self.win)
		self.gameDict[GameID] = newGame
		self.gameCount += 1

		#if self.debugMode:
			#self.addPlayerToGame( GameID, "Tester " + str( GameID ), GameID ) #		NOTE : DEBUG

		return GameID


	def addPlayerToGame( self, playerID, name, key ):
		try:
			self.gameDict.get(key).addPlayer( name, playerID )
		except:
			print ("could not add player #" + str( playerID ) + " to game #" + str( key ))


	def startGame( self, key ):
		self.gameDict.get(key).start()


	def removePlayerFromGame( self, _playerID, key ):
		#try:
		#	self.gameDict.get(key).removePlayer( _playerID )
		#except:
		#	print ("Could not remove player #" + str( _playerID ) + " from game #" + str( key ))
		pass


	def removeGame( self, key ):
		self.gameDict.get(key).close()
		self.gameDict.pop(key)
		self.gameCount -= 1



	def tickGames(self):
		try: #		 NOTE : ineloquent but ffs why the fuck can't you edit a dict while itterating in it...
			 #				like isn't that the whole fucking point of not using a different type of container
			for key in self.gameDict.keys():
				game = self.gameDict.get( key )

				if game.state == ad.ENDING:
					if self.debugMode and self.playerID == key:
						print ("this game no longer exists")
						print ("please select a valid game (1-8)")
						self.playerID = 0
						self.emptyDisplay()

					self.removeGame( key )

				elif game.state == ad.PLAYING:
					self.runGameStep( game )

					if self.debugMode: #				NOTE : DEBUG
						if key == self.playerID:
							self.displayGame( game )
		except:
			print("GameManager Error : tickGames() : removed item while iterating over gameDict")


	def runGameStep( self, game ):
		if game.state == ad.PLAYING:

			game.moveObjects()
			game.makeBotsPlay()
			game.clock.tick (game.framerate) # 	TODO : detach from pygame

		else:
			print ("this game is not running")

	def displayGame( self, game ): # 			NOTE : DEBUG
		if game.state == ad.PLAYING:
			if game.width != self.win.get_width() or game.height != self.win.get_height(): # 	TODO : detach from pygame
				self.win = pg.display.set_mode( (game.width, game.height) )
				pg.display.set_caption( game.name ) #

			game.refreshScreen()


	def takePlayerInputs( self ): # 			NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				k = event.key

				# closes the game
				if k == pg.K_ESCAPE:
					for game in self.gameDict.values():
						game.close()
					self.runGames = False
					sys.exit()

				# respawns the ball
				elif k == pg.K_RETURN:
					if self.playerID != 0:
						if self.gameDict.get(self.playerID) != None:
							game = self.gameDict.get(self.playerID)
							game.respawnAllBalls()
							print ( "respawning the ball(s)" )
						else:
							print ( "coud not respawn the ball(s)" )
					else:
						print ( "please select a valid game (1-8)" )

				# switches game to control
				elif k == pg.K_0:
					print ("please select a valid game (1-8)")
					self.playerID = 0
					self.emptyDisplay()

				# switches game to control
				elif k == pg.K_1 or k == pg.K_2 or k == pg.K_3 or k == pg.K_4 or k == pg.K_5 or k == pg.K_6 or k == pg.K_7 or k == pg.K_8 or k == pg.K_9:
					if k == pg.K_1:
						self.playerID = 1
					elif k == pg.K_2:
						self.playerID = 2
					elif k == pg.K_3:
						self.playerID = 3
					elif k == pg.K_4:
						self.playerID = 4
					elif k == pg.K_5:
						self.playerID = 5
					elif k == pg.K_6:
						self.playerID = 6
					elif k == pg.K_7:
						self.playerID = 7
					elif k == pg.K_8:
						self.playerID = 8
					elif k == pg.K_9:
						self.playerID = 9
					print ("now playing in game #" + str( self.playerID ))

					if self.gameDict.get(self.playerID) == None:
						print ("Could not switch to game #" + str( self.playerID ))
						print ("please select a valid game (1-8)")
						self.playerID = 0
						self.emptyDisplay()
					else:
						pg.display.set_caption( self.gameDict.get(self.playerID).name )

				# handling movement keys presses
				else:
					if self.gameDict.get(self.playerID) == None:
						if self.playerID != 0:
							print ("game #" + str( self.playerID ) + " does not exist")
						print ( "please select a valid game (1-8)" )
					else:
						controler = self.gameDict.get(self.playerID).controlers[0]
						if controler.mode != ad.PLAYER:
							print ("cannot move a bot's racket")
						else:
							controler.handleKeyInput(k)


	def emptyDisplay( self ):
		print("here")
		pg.display.set_caption("Game Manager") # 			NOTE : DEBUG
		self.win = pg.display.set_mode((2048, 1280)) # 		NOTE : ...
		self.win.fill( pg.Color('black') ) # 				NOTE : ...


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
	else: # 					NOTE : put fps here if not in debugMode
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


