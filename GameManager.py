from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest
from Pongester import Pongester
from GameInterface import Game

import pygame as pg
import asyncio as asy
import Addons as ad
import sys

class GameManager:

	playerID = 0 #									NOTE : DEBUG
	debugMode = True #								NOTE : DEBUG

	def __init__( self ):
		self.lastGameID = 0
		self.gameCount = 0
		self.runGames = True
		self.gameDict = {}


	def addGame( self, Initialiser, GameID): #		TODO : take game id as argument instead

		newGame = Initialiser( self.win, pg.time.Clock() ) # 	TODO : detach from pygame
		newGame.debugMode = self.debugMode #					NOTE : DEBUG

		self.gameDict[GameID] = newGame
		self.gameCount += 1

		return GameID


	def addPlayer( self, key, name, _playerID ):
		try:
			self.gameDict[key].addPlayer( name )
		except:
			print ("Could not add player #" + str( _playerID ) + " to game #" + str( key ))


	def removePlayer( self, key, _playerID ):
		#try:
		#	self.gameDict[key].removePlayer( _playerID )
		#except:
		#	print ("Could not remove player #" + str( _playerID ) + " from game #" + str( key ))
		pass


	def startGame( self, key ):
		#self.gameDict[key].addPlayer( "Player " + str( key ))
		self.gameDict[key].start()


	def pauseGame( self, key ):
		#self.gameDict[key].addPlayer( "Player " + str( key ))
		self.gameDict[key].pause()


	def removeGame( self, key ):
		self.gameDict[key].stop()
		self.gameDict.pop(key)
		self.gameCount -= 1



	async def tickGames(self):
		for key in self.gameDict.keys():
			game = self.gameDict[key]

			if game.isOver:
				self.removeGame( game.id )
			elif game.isRunning:
				self.runGameStep( game )

				if self.debugMode:
					if key == self.playerID:
						self.displayGame( game )

		if self.playerID == 0 and ( ad.WIN_SIZE != self.win.get_width() or ad.WIN_SIZE != self.win.get_height() ): # 	NOTE : DEBUG
			self.win = pg.display.set_mode( (ad.WIN_SIZE, ad.WIN_SIZE) ) # 												NOTE : ...
			self.win.fill( pg.Color('black') ) # 																		NOTE : ...
			pg.display.set_caption("Game Manager") # 																	NOTE : ...

		await asy.sleep(0)


	def runGameStep( self, game ):
		if game.isRunning:

			game.moveObjects()
			game.makeBotsPlay()
			game.clock.tick (game.framerate) # 	TODO : detach from pygame

			#print ( game.getInfo() )

		else:
			print (" This game is not running")

	def displayGame( self, game ): # 			NOTE : DEBUG
		if game.isRunning:
			if game.width != self.win.get_width() or game.height != self.win.get_height(): # 		TODO : detach from pygame
				self.win = pg.display.set_mode( (game.width, game.height) )
				pg.display.set_caption( game.name ) #

			game.refreshScreen()
		else:
			self.win.fill( self.col_bgr )
			print (" This game is not running")


	def takePlayerInputs( self ): # 			NOTE : DEBUG
		# read local player inputs
		for event in pg.event.get():

			if event.type == pg.KEYDOWN:
				# closes the game
				if event.key == pg.K_ESCAPE:
					for game in self.gameDict.values():
						game.stop()
					self.runGames = False
					sys.exit()

				# switches game to control
				if event.key == pg.K_0:
					print ("please select a valid game (1-8)")

				# switches game to control
				elif event.key == pg.K_1 or event.key == pg.K_2 or event.key == pg.K_3 or event.key == pg.K_4 or event.key == pg.K_5 or event.key == pg.K_6 or event.key == pg.K_7 or event.key == pg.K_8 or event.key == pg.K_9:
					if event.key == pg.K_1:
						self.playerID = 1
					elif event.key == pg.K_2:
						self.playerID = 2
					elif event.key == pg.K_3:
						self.playerID = 3
					elif event.key == pg.K_4:
						self.playerID = 4
					elif event.key == pg.K_5:
						self.playerID = 5
					elif event.key == pg.K_6:
						self.playerID = 6
					elif event.key == pg.K_7:
						self.playerID = 7
					elif event.key == pg.K_8:
						self.playerID = 8
					elif event.key == pg.K_9:
						self.playerID = 9
					print ("now playing in game #" + str( self.playerID ))


					try:
						game = self.gameDict[self.playerID]
					except:
						print ("Could not switch to game #" + str( self.playerID ))
						print ("no longer playeing in any game")
						self.playerID = 0

				# handling game movement keys
				else:
					if self.playerID > 0 and self.playerID < 9 and self.gameDict[self.playerID] and self.gameDict[self.playerID].controlers[0].mode == ad.PLAYER:
						self.gameDict[self.playerID].controlers[0].handleKeyInput(event.key)
					else:
						print ("Could not pass input from player for game #" + str( self.playerID ))


def main():

	gm = GameManager()

	if (gm.debugMode):
		pg.init() # 													NOTE : DEBUG
		pg.display.set_caption("Game Manager") # 						NOTE : ...
		gm.win = pg.display.set_mode((2048, 1024)) # 		NOTE : ...
		gm.win.fill( pg.Color('black') ) # 								NOTE : ...

	addAllGames( gm )

	while gm.runGames:

		if gm.debugMode:
			gm.takePlayerInputs()
		asy.run( gm.tickGames() ) # ASYNC IS HERE

if __name__ == '__main__':
	main()


def addAllGames( gm ):
	gameID = 1

	gm.startGame( gm.addGame( Game, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Ping, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pinger, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pingest, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pong, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Ponger, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pongest, gameID ))
	gameID += 1
	gm.startGame( gm.addGame( Pongester, gameID ))
	gameID += 1

	print ("select a player (1-8)")


